from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import router as users_router
from app.routes.customers import router as customers_router
from app.routes.packages import router as packages_router
from app.routes.other_routes import router as other_routes_router
from db.models import create_tables
from utils.loguru_config import loguru_logger
from utils.populate import populate_all_tables
import time


# Initialize FastAPI app
app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
loguru_logger.info("CORS middleware successfully added.")


app.include_router(users_router, prefix="/users")
app.include_router(customers_router, prefix="/customers")
app.include_router(packages_router, prefix="/packages")
app.include_router(other_routes_router, prefix="")


def create_tables_on_startup():
    """
    Create necessary tables in the database on server startup with an initial delay.
    """
    # Add a delay of 15 seconds
    loguru_logger.info("Waiting for 15 seconds before creating tables...")
    time.sleep(25)
    try:
        create_tables()
        loguru_logger.info("Waiting for 3 seconds before populate tables...")
        time.sleep(3)
    except Exception as e:
        loguru_logger.error(f"Failed to create tables after delay. Error: {e}")

    populate_all_tables()


#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~

# Call the table creation function on startup
@app.on_event("startup")
def startup_event():
    """
    FastAPI startup event.
    """
    loguru_logger.info("Starting up the application...")
    create_tables_on_startup()


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=11000)
