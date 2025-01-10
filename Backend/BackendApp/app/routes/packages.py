from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from ..models.tables import Package
from ..models.database import get_db
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import sanitize_input, prevent_sql_injection

router = APIRouter()

# Models
class PackageCreate(BaseModel):
    user_id: str
    package_name: str
    description: str
    monthly_price: float

class PackageUpdateRequest(BaseModel):
    package_id: str
    package_name: str = None
    description: str = None
    monthly_price: float = None

class UserRequest(BaseModel):
    user_id: str

# Endpoints

@router.get("/get_packages")
def get_packages(request: UserRequest, db: Session = Depends(get_db)):
    logger.info(f"Fetching packages for user: {request.user_id}")
    try:
        sanitized_user_id = sanitize_input(prevent_sql_injection(request.user_id))
        if sanitized_user_id != request.user_id:
            logger.warning("Potential XSS or SQL Injection detected in user_id.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        packages = db.query(Package).filter(Package.user_id == sanitized_user_id).all()
        if not packages:
            logger.warning(f"No packages found for user: {sanitized_user_id}")
            raise HTTPException(status_code=404, detail="No packages found.")

        create_audit_log_entry(user_id=sanitized_user_id, action="Fetched all packages", db=db)
        logger.debug(f"Fetched {len(packages)} packages for user: {sanitized_user_id}")
        return packages

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching packages for user {sanitized_user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/new_package")
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating a new package for user: {package.user_id}")
    try:
        sanitized_user_id = sanitize_input(prevent_sql_injection(package.user_id))
        sanitized_package_name = sanitize_input(package.package_name)
        sanitized_description = sanitize_input(package.description)

        if sanitized_user_id != package.user_id or sanitized_package_name != package.package_name or sanitized_description != package.description:
            logger.warning("Potential XSS detected in package details.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        new_package = Package(
            user_id=sanitized_user_id,
            package_name=sanitized_package_name,
            description=sanitized_description,
            monthly_price=package.monthly_price
        )
        db.add(new_package)
        db.commit()
        db.refresh(new_package)

        create_audit_log_entry(user_id=sanitized_user_id, action="New package created", db=db)
        logger.info(f"Package created successfully: {sanitized_package_name}")
        return {"status": "success", "message": "Package created successfully", "id": new_package.id}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Database error creating package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        db.rollback()
        logger.exception(f"Unexpected error creating package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/update_package")
def update_package(package: PackageUpdateRequest, db: Session = Depends(get_db)):
    logger.info(f"Updating package with ID: {package.package_id}")
    try:
        sanitized_package_id = sanitize_input(prevent_sql_injection(package.package_id))
        if sanitized_package_id != package.package_id:
            logger.warning("Potential XSS or SQL Injection detected in package_id.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        package_to_update = db.query(Package).filter(Package.id == sanitized_package_id).first()
        if not package_to_update:
            logger.warning(f"Package not found: {sanitized_package_id}")
            raise HTTPException(status_code=404, detail="Package not found")

        if package.package_name:
            sanitized_package_name = sanitize_input(package.package_name)
            if sanitized_package_name != package.package_name:
                logger.warning("XSS attempt detected in package_name.")
                raise HTTPException(status_code=400, detail="Invalid input detected.")
            package_to_update.package_name = sanitized_package_name

        if package.description:
            sanitized_description = sanitize_input(package.description)
            if sanitized_description != package.description:
                logger.warning("XSS attempt detected in description.")
                raise HTTPException(status_code=400, detail="Invalid input detected.")
            package_to_update.description = sanitized_description

        if package.monthly_price is not None:
            if not isinstance(package.monthly_price, (int, float)) or package.monthly_price <= 0:
                logger.warning("Invalid input detected in monthly_price.")
                raise HTTPException(status_code=400, detail="Invalid input detected.")
            package_to_update.monthly_price = package.monthly_price

        db.commit()
        db.refresh(package_to_update)

        create_audit_log_entry(user_id=None, action="Package updated", db=db)
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

@router.delete("/{package_id}")
def delete_package(package_id: str, request: UserRequest, db: Session = Depends(get_db)):
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
