from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.connection import create_connection, execute_query, fetch_results
from utils.loguru_config import loguru_logger

router = APIRouter()

def sanitize_query(query: str) -> str:
    """
    Sanitizes an SQL query by removing everything after /* or --.
    """
    query = query.split("/*")[0]
    query = query.split("--")[0]
    return query.strip()

class PackageResponse(BaseModel):
    id: str
    package_name: str
    description: str
    monthly_price: int

@router.get("/", response_model=list[PackageResponse])
def get_packages():
    """
    Fetch all available packages from the database. Vulnerable to SQL Injection.

    :return: List of all packages.
    """
    loguru_logger.info("Fetching all packages.")

    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # Fetch packages directly (vulnerable to SQL Injection)
        query = "SELECT id, package_name, description, monthly_price FROM packages"
        query = sanitize_query(query)
        packages = fetch_results(connection, query)

        if not packages:
            loguru_logger.warning("No packages found.")
            raise HTTPException(status_code=404, detail="No packages found.")

        loguru_logger.debug(f"Fetched {len(packages)} packages.")
        return packages

    except Exception as e:
        loguru_logger.error(f"Error fetching packages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        connection.close()