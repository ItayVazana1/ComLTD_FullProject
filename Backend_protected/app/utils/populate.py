import json
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models.database import engine
from ..models.tables import Package, generate_package_id
from ..utils.loguru_config import loguru_logger as logger

def load_packages_from_file(file_path="app/utils/init_packages_data.json"):
    """
    Load package data from a JSON file.
    This function reads the package data from a JSON file and returns it as a list of dictionaries.

    :param file_path: Path to the JSON file containing package data.
    :return: List of package dictionaries if successful, empty list if the file is not found or invalid.
    """
    try:
        if not Path(file_path).exists():
            logger.error(f"File not found: {file_path}")  # Log error if file does not exist
            return []
        with open(file_path, "r") as file:
            packages = json.load(file)  # Parse the JSON file into Python objects
            logger.info(f"Successfully loaded {len(packages)} packages from file.")
            return packages
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON file {file_path}: {e}")  # Log if the file cannot be parsed
        return []


def populate_packages(file_path="app/utils/init_packages_data.json"):
    """
    Populate the 'packages' table with data from a JSON file if not already present.
    This function checks if the package data is already in the database. If not, it adds the data.

    :param file_path: Path to the JSON file containing package data.
    """
    # Load packages data from the specified file
    packages = load_packages_from_file(file_path)
    if not packages:
        logger.warning("No packages to populate. Exiting.")  # Log if no packages are loaded
        return

    # Create a session for interacting with the database
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        logger.info("Starting to populate the 'packages' table.")

        # Get the last package ID to create a new unique ID for the next package
        last_package = session.query(Package).order_by(Package.id.desc()).first()
        last_id = int(last_package.id.split('-')[1]) if last_package else 0  # Parse last ID for continuation

        with session.no_autoflush:
            # Iterate through each package in the loaded data
            for package in packages:
                # Check if the package already exists in the database
                existing_package = session.query(Package).filter_by(package_name=package["package_name"]).first()
                if existing_package:
                    logger.info(f"Package '{package['package_name']}' already exists. Skipping.")
                    continue  # Skip if package is already present in the database

                # Create a new unique package ID
                last_id += 1
                package_id = f"pak-{last_id}"  # Format new package ID

                # Create a new Package object
                new_package = Package(
                    id=package_id,
                    package_name=package["package_name"],
                    description=package["description"],
                    monthly_price=package["monthly_price"],
                )
                session.add(new_package)  # Add the new package to the session
                logger.info(f"Added new package: {package['package_name']} with ID: {package_id}.")

        session.commit()  # Commit the transaction to the database
        logger.info("Successfully populated the 'packages' table.")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback in case of error to maintain database consistency
        logger.error(f"Failed to populate the 'packages' table: {e}")
    finally:
        session.close()  # Ensure the session is properly closed
        logger.debug("Database session closed.")
