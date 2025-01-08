from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models.tables import Package
from ..models.database import get_db
from pydantic import BaseModel
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import sanitize_input, prevent_sql_injection

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

@router.get("/")
def get_packages(request: UserRequest, db: Session = Depends(get_db)):
    """
    Fetch all packages from the database.
    :param request: UserRequest containing the user ID.
    :param db: Database session.
    :return: List of all packages.
    """
    sanitized_user_id = sanitize_input(request.user_id)
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
    sanitized_user_id = sanitize_input(request.user_id)
    sanitized_package_id = prevent_sql_injection(package_id)
    logger.info(f"Fetching package with ID {sanitized_package_id} by user {sanitized_user_id}.")
    package = db.query(Package).filter(Package.id == sanitized_package_id).first()
    if not package:
        logger.warning(f"Package with ID {sanitized_package_id} not found.")
        raise HTTPException(status_code=404, detail="Package not found")
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Fetched package {sanitized_package_id}", db=db)
    logger.debug(f"Fetched package details: {package}")
    return package

@router.post("/")
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    """
    Create a new package in the database.
    :param package: Details of the package to create, including user ID.
    :param db: Database session.
    :return: Details of the created package.
    """
    sanitized_user_id = sanitize_input(package.user_id)
    sanitized_package_name = sanitize_input(package.package_name)
    sanitized_description = sanitize_input(package.description)
    sanitized_monthly_price = int(package.monthly_price)

    logger.info(f"Creating a new package with name {sanitized_package_name} by user {sanitized_user_id}.")
    new_package = Package(
        package_name=sanitized_package_name,
        description=sanitized_description,
        monthly_price=sanitized_monthly_price,
    )
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Created package {new_package.package_name}", db=db)
    logger.info(f"Package created successfully with ID: {new_package.id}")
    return new_package

@router.put("/{package_id}")
def update_package(package_id: str, package: PackageUpdate, db: Session = Depends(get_db)):
    """
    Update an existing package in the database.
    :param package_id: The ID of the package to update.
    :param package: Updated details for the package, including user ID.
    :param db: Database session.
    :return: Updated package details.
    """
    sanitized_package_id = prevent_sql_injection(package_id)
    sanitized_user_id = sanitize_input(package.user_id)
    sanitized_description = sanitize_input(package.description)
    sanitized_monthly_price = int(package.monthly_price)

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
    sanitized_package_id = prevent_sql_injection(package_id)
    sanitized_user_id = sanitize_input(request.user_id)

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
