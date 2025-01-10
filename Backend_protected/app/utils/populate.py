import json
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models.database import engine
from ..models.tables import Package , generate_package_id
from ..utils.loguru_config import loguru_logger as logger



def load_packages_from_file(file_path="app/utils/init_packages_data.json"):
    """
    Load package data from a JSON file.
    :param file_path: Path to the JSON file containing package data.
    :return: List of package dictionaries.
    """
    try:
        if not Path(file_path).exists():
            logger.error(f"File not found: {file_path}")
            return []
        with open(file_path, "r") as file:
            packages = json.load(file)
            logger.info(f"Successfully loaded {len(packages)} packages from file.")
            return packages
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON file {file_path}: {e}")
        return []


def populate_packages(file_path="app/utils/init_packages_data.json"):
    """
    Populate the 'packages' table with data from a JSON file if not already present.
    :param file_path: Path to the JSON file containing package data.
    """
    packages = load_packages_from_file(file_path)
    if not packages:
        logger.warning("No packages to populate. Exiting.")
        return

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        logger.info("Starting to populate the 'packages' table.")

        # קבלת הערך האחרון של ID
        last_package = session.query(Package).order_by(Package.id.desc()).first()
        last_id = int(last_package.id.split('-')[1]) if last_package else 0

        with session.no_autoflush:
            for package in packages:
                existing_package = session.query(Package).filter_by(package_name=package["package_name"]).first()
                if existing_package:
                    logger.info(f"Package '{package['package_name']}' already exists. Skipping.")
                    continue

                # יצירת ID ייחודי
                last_id += 1
                package_id = f"pak-{last_id}"

                # יצירת אובייקט חבילה חדש
                new_package = Package(
                    id=package_id,
                    package_name=package["package_name"],
                    description=package["description"],
                    monthly_price=package["monthly_price"],
                )
                session.add(new_package)
                logger.info(f"Added new package: {package['package_name']} with ID: {package_id}.")

        session.commit()
        logger.info("Successfully populated the 'packages' table.")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Failed to populate the 'packages' table: {e}")
    finally:
        session.close()
        logger.debug("Database session closed.")
