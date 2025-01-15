from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from ..models.database import engine
from ..utils.loguru_config import logger
from decouple import config

def clear_database():
    """
    Deletes all data from all tables in the database if ENABLE_AUTO_CLEANUP is True.
    """
    if config("ENABLE_AUTO_CLEANUP", default="False") == "True":
        logger.info("Starting database cleanup...")
        try:
            meta = MetaData()
            meta.reflect(bind=engine)
            with engine.begin() as connection:
                for table in reversed(meta.sorted_tables):
                    connection.execute(table.delete())
            logger.info("All tables have been cleared from the database.")
        except Exception as e:
            logger.error(f"An error occurred during database cleanup: {e}")
            raise
    else:
        logger.info("Auto cleanup is disabled.")
