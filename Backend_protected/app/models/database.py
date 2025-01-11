from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from decouple import config  # Import directly from decouple
from ..utils.loguru_config import logger

# Load the DATABASE_URL from .env
DATABASE_URL = config("DATABASE_URL")  # Fetch database URL from environment

# Database engine initialization
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Provide a database session and ensure proper closure.
    Yields:
        db (Session): Active database session.
    """
    logger.debug("Initializing database session.")
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session yielded successfully.")
    except Exception as e:
        logger.error(f"Error occurred during database session: {e}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")

def load_models():
    """
    Dynamically loads all database models.
    This ensures that all table schemas are recognized and can be created.
    """
    try:
        from .tables import (
            User,
            Customer,
            Package,
            AuditLog,
            PasswordReset,
            ContactSubmission
        )
        logger.info("Models loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise
