from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from ..models.tables import Package, generate_package_id
from ..models.database import get_db
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import sanitize_input, prevent_sql_injection

# Title: Package Management Routes

router = APIRouter()

# Title: Models

class PackageCreate(BaseModel):
    user_id: str
    package_name: str
    description: str
    monthly_price: float

class PackageUpdateRequest(BaseModel):
    user_id: str
    package_name: str = None
    description: str = None
    monthly_price: float = None

class PackageResponse(BaseModel):
    id: str
    package_name: str
    description: str
    monthly_price: float

    class Config:
        orm_mode = True

class UserRequest(BaseModel):
    user_id: str

# Title: Package Endpoints

@router.get("/", response_model=list[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    """
    Fetch all available packages from the database.

    :param db: Database session.
    :return: List of all packages.
    """
    logger.info("Fetching all packages.")
    try:
        packages = db.query(Package).all()
        if not packages:
            logger.warning("No packages found.")
            raise HTTPException(status_code=404, detail="No packages found.")

        logger.debug(f"Fetched {len(packages)} packages.")
        return packages

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching packages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{package_id}", response_model=PackageResponse)
def get_package(package_id: str, db: Session = Depends(get_db)):
    """
    Fetch a specific package by its ID.

    :param package_id: The ID of the package to fetch.
    :param db: Database session.
    :return: Package details.
    """
    logger.info(f"Fetching package with ID: {package_id}")
    try:
        sanitized_package_id = sanitize_input(prevent_sql_injection(package_id))
        if sanitized_package_id != package_id:
            logger.warning("Potential XSS or SQL Injection detected in package_id.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        package = db.query(Package).filter(Package.id == sanitized_package_id).first()
        if not package:
            logger.warning(f"Package with ID {sanitized_package_id} not found.")
            raise HTTPException(status_code=404, detail="Package not found.")

        logger.info(f"Package fetched successfully: {sanitized_package_id}")
        return package

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching package {package_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/new_package")
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    """
    Create a new package.

    :param package: PackageCreate model containing package details.
    :param db: Database session.
    :return: Success message and the created package ID.
    """
    logger.info(f"Creating a new package for user: {package.user_id}")
    try:
        # Sanitize inputs
        sanitized_user_id = sanitize_input(prevent_sql_injection(package.user_id))
        sanitized_package_name = sanitize_input(package.package_name)
        sanitized_description = sanitize_input(package.description)
        sanitized_monthly_price = package.monthly_price

        if sanitized_user_id != package.user_id:
            logger.warning("Potential SQL Injection detected in user_id.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        # Create the package
        new_package = Package(
            id=generate_package_id(db),
            package_name=sanitized_package_name,
            description=sanitized_description,
            monthly_price=sanitized_monthly_price,
        )
        db.add(new_package)
        db.commit()
        db.refresh(new_package)

        # Log the action
        create_audit_log_entry(user_id=sanitized_user_id, action=f"Created package {new_package.id}", db=db)
        logger.info(f"Package created successfully: {new_package.id}")
        return {"status": "success", "id": new_package.id, "message": "Package created successfully"}

    except Exception as e:
        db.rollback()
        logger.exception(f"Unexpected error creating package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/update_package/{package_id}")
def update_package(package_id: str, package: PackageUpdateRequest, db: Session = Depends(get_db)):
    """
    Update an existing package.

    :param package_id: The ID of the package to update.
    :param package: PackageUpdateRequest model containing updated details.
    :param db: Database session.
    :return: Success message upon successful update.
    """
    logger.info(f"Attempting to update package with ID: {package_id}")
    try:
        sanitized_package_id = sanitize_input(prevent_sql_injection(package_id))
        if sanitized_package_id != package_id:
            logger.warning("Potential XSS or SQL Injection detected in package_id.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        package_to_update = db.query(Package).filter(Package.id == sanitized_package_id).first()
        if not package_to_update:
            logger.warning(f"Package not found: {sanitized_package_id}")
            raise HTTPException(status_code=404, detail="Package not found.")

        logger.info(f"Package found: {package_to_update}")

        # Update fields
        if package.package_name:
            sanitized_package_name = sanitize_input(package.package_name)
            package_to_update.package_name = sanitized_package_name

        if package.description:
            sanitized_description = sanitize_input(package.description)
            package_to_update.description = sanitized_description

        if package.monthly_price is not None:
            package_to_update.monthly_price = package.monthly_price

        db.commit()
        db.refresh(package_to_update)

        create_audit_log_entry(user_id=package.user_id, action=f"Package {sanitized_package_id} updated", db=db)
        logger.info(f"Package updated successfully: {sanitized_package_id}")
        return {"status": "success", "message": "Package updated successfully"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Database error updating package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        db.rollback()
        logger.exception(f"Unexpected error updating package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/delete_package/{package_id}")
def delete_package(package_id: str, request: UserRequest, db: Session = Depends(get_db)):
    """
    Delete an existing package by its ID.

    :param package_id: The ID of the package to delete.
    :param request: UserRequest model containing the user ID.
    :param db: Database session.
    :return: Success message upon successful deletion.
    """
    logger.info(f"Deleting package with ID: {package_id}")
    try:
        sanitized_package_id = sanitize_input(prevent_sql_injection(package_id))
        sanitized_user_id = sanitize_input(prevent_sql_injection(request.user_id))

        if sanitized_package_id != package_id or sanitized_user_id != request.user_id:
            logger.warning("Potential XSS or SQL Injection detected in delete request.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        db_package = db.query(Package).filter(Package.id == sanitized_package_id).first()
        if not db_package:
            logger.warning(f"Package not found: {sanitized_package_id}")
            raise HTTPException(status_code=404, detail="Package not found")

        db.delete(db_package)
        db.commit()

        create_audit_log_entry(user_id=sanitized_user_id, action=f"Deleted package {sanitized_package_id}", db=db)
        logger.info(f"Package deleted successfully: {sanitized_package_id}")
        return {"status": "success", "message": "Package deleted successfully"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Database error deleting package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        db.rollback()
        logger.exception(f"Unexpected error deleting package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
