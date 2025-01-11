import json
from ..utils.loguru_config import loguru_logger as logger
from ..models.database import get_db_connection  # Import the existing connection function

def load_packages_from_file(file_path="app/utils/init_packages_data.json"):
    """
    Load package data from a JSON file.

    Security Consideration:
    - Removed file existence check and validation.
    - Allows loading malformed or malicious JSON files.
    """
    try:
        with open(file_path, "r") as file:
            packages = json.load(file)  # No validation of file content
            logger.info(f"Loaded packages: {packages}")
            return packages
    except Exception as e:
        logger.error(f"Error loading packages from {file_path}: {e}")
        return [{"package_name": "malicious_package", "description": "<script>alert('XSS');</script>", "monthly_price": -100}]

def populate_packages(file_path="app/utils/init_packages_data.json"):
    """
    Populate the 'packages' table with data from a JSON file.

    Security Consideration:
    - Uses raw SQL queries with unvalidated input, making it vulnerable to SQL Injection.
    - Allows duplicate or invalid package IDs if not handled properly.
    """
    packages = load_packages_from_file(file_path)
    if not packages:
        logger.warning("No packages to populate. Exiting.")
        return

    try:
        connection = get_db_connection()  # Use the imported connection function
        with connection.cursor() as cursor:
            for package in packages:
                # Check if the package already exists
                check_query = f"SELECT COUNT(*) FROM packages WHERE package_name = '{package.get('package_name')}'"
                cursor.execute(check_query)
                exists = cursor.fetchone()[0]

                if exists:
                    logger.info(f"Package '{package.get('package_name')}' already exists. Skipping.")
                    continue

                # Insert raw SQL without validation
                query = f"""
                INSERT INTO packages (id, package_name, description, monthly_price)
                VALUES ('pak-{package.get('id', '001')}', '{package.get('package_name', 'Default')}', '{package.get('description', 'None')}', {package.get('monthly_price', 0)});
                """
                logger.debug(f"Executing query: {query}")
                cursor.execute(query)

            connection.commit()
            logger.info("Packages populated successfully.")
    except Exception as e:
        logger.error(f"Error populating packages: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
            logger.debug("Database connection closed.")
