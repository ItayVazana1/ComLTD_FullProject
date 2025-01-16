import atexit
from fastapi import FastAPI
from .models.database import engine, load_models
from .models.tables import Base
from .utils.populate import populate_packages
from .routes.users import router as users_router
from .routes.packages import router as packages_router
from .routes.customers import router as customers_router
from .routes.audit_logs import router as audit_logs_router
from .routes.landing_page import router as landing_page_router
from .routes.contact_us import router as contact_us_router
from .utils.loguru_config import logger


# Title: Application Initialization and Route Registration

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function sets up the application, registers routes, and adds metadata.
    :return: Configured FastAPI application instance.
    """
    logger.info("Initializing FastAPI application...")
    application = FastAPI(
        title="Communication LTD API",
        version="1.0.0",
        description="API for managing Communication LTD operations."
    )

    # Include routers for all routes
    application.include_router(users_router, prefix="/users", tags=["Users"])
    application.include_router(packages_router, prefix="/packages", tags=["Packages"])
    application.include_router(customers_router, prefix="/customers", tags=["Customers"])
    application.include_router(audit_logs_router, prefix="/audit-logs", tags=["Audit Logs"])
    application.include_router(landing_page_router, tags=["Landing Pages"])
    application.include_router(contact_us_router, tags=["Contact Us"])

    logger.info("Routes successfully registered.")
    return application

# Title: Database Initialization

def initialize_database():
    """
    Initialize the database by loading models, creating tables, and populating initial data.

    This function ensures the database is ready for use by the application.
    """
    try:
        logger.info("Starting database initialization...")
        load_models()
        Base.metadata.create_all(bind=engine)
        populate_packages()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

# Title: Main Application Entry Point

try:
    logger.info("Starting application setup...")
    initialize_database()
    app = create_application()
    logger.info("Application setup completed successfully.")
except Exception as e:
    logger.critical(f"Failed to start the application: {e}")
    raise
