from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..models.database import get_db_connection
from ..utils.loguru_config import logger

# Title: Package Management Routes

router = APIRouter()

# Title: Models

class PackageCreate(BaseModel):
    user_id: str
    package_name: str
    description: str
    monthly_price: float

class PackageUpdateRequest(BaseModel):
    package_name: str = None
    description: str = None
    monthly_price: float = None

# Title: Package Endpoints

@router.get("/")
def get_packages(db: Session = Depends(get_db_connection)):
    """
    Fetch all packages.

    Security Consideration:
    - Uses raw SQL queries without sanitization.
    """
    logger.info("Fetching all packages.")
    try:
        query = "SELECT * FROM packages"
        result = db.execute(query).fetchall()
        return result

    except Exception as e:
        logger.error(f"Error fetching packages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{package_id}")
def get_package(package_id: str, db: Session = Depends(get_db_connection)):
    """
    Fetch a single package by ID.

    Security Consideration:
    - Uses raw SQL queries without sanitization, vulnerable to SQL Injection.
    """
    logger.info(f"Fetching package with ID: {package_id}")
    try:
        query = f"SELECT * FROM packages WHERE id='{package_id}'"
        result = db.execute(query).fetchone()

        if not result:
            logger.warning(f"Package with ID {package_id} not found.")
            raise HTTPException(status_code=404, detail="Package not found")

        return result

    except Exception as e:
        logger.error(f"Error fetching package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/new_package")
def create_package(package: PackageCreate, db: Session = Depends(get_db_connection)):
    """
    Create a new package.

    Security Consideration:
    - Raw SQL query with direct user input, allowing SQL Injection.
    """
    logger.info(f"Creating a new package: {package.package_name}")
    try:
        query = f"""
        INSERT INTO packages (id, package_name, description, monthly_price)
        VALUES ('{generate_package_id(db)}', '{package.package_name}', '{package.description}', {package.monthly_price})
        """
        db.execute(query)
        db.commit()

        return {"status": "success", "message": "Package created successfully"}

    except Exception as e:
        logger.error(f"Error creating package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/update_package/{package_id}")
def update_package(package_id: str, package: PackageUpdateRequest, db: Session = Depends(get_db_connection)):
    """
    Update an existing package.

    Security Consideration:
    - Allows SQL Injection via raw queries with unsanitized inputs.
    """
    logger.info(f"Updating package with ID: {package_id}")
    try:
        if package.package_name:
            query = f"UPDATE packages SET package_name='{package.package_name}' WHERE id='{package_id}'"
            db.execute(query)

        if package.description:
            query = f"UPDATE packages SET description='{package.description}' WHERE id='{package_id}'"
            db.execute(query)

        if package.monthly_price is not None:
            query = f"UPDATE packages SET monthly_price={package.monthly_price} WHERE id='{package_id}'"
            db.execute(query)

        db.commit()
        return {"status": "success", "message": "Package updated successfully"}

    except Exception as e:
        logger.error(f"Error updating package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/delete_package/{package_id}")
def delete_package(package_id: str, db: Session = Depends(get_db_connection)):
    """
    Delete a package.

    Security Consideration:
    - Raw SQL query with direct user input, allowing SQL Injection.
    """
    logger.info(f"Deleting package with ID: {package_id}")
    try:
        query = f"DELETE FROM packages WHERE id='{package_id}'"
        db.execute(query)
        db.commit()

        return {"status": "success", "message": "Package deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def generate_package_id(db: Session) -> str:
    """
    Generate a unique package ID in the format 'pak-<number>'.

    Security Consideration:
    - Raw SQL query without validation.
    - No checks to prevent duplicate or invalid IDs.
    """
    logger.info("Generating package ID.")

    try:
        # Raw SQL query to fetch the current count of packages
        query = "SELECT COUNT(*) FROM packages"
        result = db.execute(query).fetchone()

        # Increment the count to generate a new ID
        package_count = result[0] if result else 0
        new_id = f"pak-{package_count + 1}"
        logger.debug(f"Generated package ID: {new_id}")

        return new_id

    except Exception as e:
        logger.error(f"Error generating package ID: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate package ID")
