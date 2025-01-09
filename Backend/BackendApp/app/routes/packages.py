from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models.tables import Package
from ..models.database import get_db
from pydantic import BaseModel
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import sanitize_input, prevent_sql_injection
from sqlalchemy.exc import SQLAlchemyError




router = APIRouter()

# Models for request validation
class PackageCreate(BaseModel):
    """
    Model for creating a new package.
    """
    user_id: str
    package_name: str
    description: str
    monthly_price: int

class PackageUpdate(BaseModel):
    """
    Model for updating an existing package.
    """
    user_id: str
    description: str
    monthly_price: int

class UserRequest(BaseModel):
    """
    Model for general requests that include user ID.
    """
    user_id: str


class PackageResponse(BaseModel):
    id: str
    package_name: str
    description: str
    monthly_price: int
    subscriber_count: int

    class Config:
        orm_mode = True


def generate_package_id(session: Session):
    """
    Generate a unique package ID in the format 'pak-<number>'.
    """
    count = session.query(Package).count()
    return f"pak-{count + 1}"


@router.get("/", response_model=list[PackageResponse])
def get_packages(request: UserRequest, db: Session = Depends(get_db)):
    """
    Fetch all packages from the database.
    :param request: UserRequest containing the user ID.
    :param db: Database session.
    :return: List of all packages.
    """
    sanitized_user_id = sanitize_input(request.user_id)  # Protects against XSS
    logger.info(f"Fetching all packages by user {sanitized_user_id}.")
    packages = db.query(Package).all()
    create_audit_log_entry(user_id=sanitized_user_id, action="Fetched all packages", db=db)
    logger.debug(f"Fetched {len(packages)} packages.")
    return packages


@router.get("/{package_id}")
def get_package(request: UserRequest, package_id: str, db: Session = Depends(get_db)):
    """
    Fetch a specific package by its ID.
    :param request: UserRequest containing the user ID.
    :param package_id: The ID of the package to fetch.
    :param db: Database session.
    :return: Package details.
    """
    sanitized_user_id = sanitize_input(request.user_id)  # Protects against XSS
    sanitized_package_id = prevent_sql_injection(package_id)  # Prevents SQL Injection
    logger.info(f"Fetching package with ID {sanitized_package_id} by user {sanitized_user_id}.")
    package = db.query(Package).filter(Package.id == sanitized_package_id).first()
    if not package:
        logger.warning(f"Package with ID {sanitized_package_id} not found.")
        raise HTTPException(status_code=404, detail="Package not found")
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Fetched package {sanitized_package_id}", db=db)
    logger.debug(f"Fetched package details: {package}")
    return package

@router.post("/new_package")
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    """
    Create a new package.
    """
    try:
        package_id = generate_package_id(db)
        new_package = Package(
            id=package_id,
            package_name=package.package_name,
            description=package.description,
            monthly_price=package.monthly_price,
        )
        db.add(new_package)
        db.commit()
        db.refresh(new_package)
        return {"status": "success", "id": new_package.id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating package") from e

@router.put("/{package_id}")
def update_package(package_id: str, package: PackageUpdate, db: Session = Depends(get_db)):
    """
    Update an existing package in the database.
    :param package_id: The ID of the package to update.
    :param package: Updated details for the package, including user ID.
    :param db: Database session.
    :return: Updated package details.
    """
    sanitized_package_id = prevent_sql_injection(package_id)  # Prevents SQL Injection
    sanitized_user_id = sanitize_input(package.user_id)  # Protects against XSS
    sanitized_description = sanitize_input(package.description)  # Protects against XSS
    sanitized_monthly_price = int(package.monthly_price)  # Ensure numeric input

    logger.info(f"Updating package with ID {sanitized_package_id} by user {sanitized_user_id}.")
    db_package = db.query(Package).filter(Package.id == sanitized_package_id).first()
    if not db_package:
        logger.warning(f"Package with ID {sanitized_package_id} not found.")
        raise HTTPException(status_code=404, detail="Package not found")
    db_package.description = sanitized_description
    db_package.monthly_price = sanitized_monthly_price
    db.commit()
    db.refresh(db_package)
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Updated package {sanitized_package_id}", db=db)
    logger.info(f"Package with ID {sanitized_package_id} updated successfully.")
    return db_package

@router.delete("/{package_id}")
def delete_package(package_id: str, request: UserRequest, db: Session = Depends(get_db)):
    """
    Delete a package from the database.
    :param package_id: The ID of the package to delete.
    :param request: UserRequest containing the user ID.
    :param db: Database session.
    :return: Confirmation of deletion.
    """
    sanitized_package_id = prevent_sql_injection(package_id)  # Prevents SQL Injection
    sanitized_user_id = sanitize_input(request.user_id)  # Protects against XSS

    logger.info(f"Deleting package with ID {sanitized_package_id} by user {sanitized_user_id}.")
    db_package = db.query(Package).filter(Package.id == sanitized_package_id).first()
    if not db_package:
        logger.warning(f"Package with ID {sanitized_package_id} not found.")
        raise HTTPException(status_code=404, detail="Package not found")
    db.delete(db_package)
    db.commit()
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Deleted package {sanitized_package_id}", db=db)
    logger.info(f"Package with ID {sanitized_package_id} deleted successfully.")
    return {"detail": "Package deleted successfully"}