from fastapi import FastAPI, HTTPException
from db.models import create_tables
from db.connection import create_connection
from utils.loguru_config import loguru_logger
from utils.audit_log import create_audit_log_entry
from utils.email_util import send_email
from utils.populate import populate_all_tables
from pydantic import BaseModel
from typing import List
import time


# Define a Pydantic model for request body validation
class AuditLogRequest(BaseModel):
    user_id: str
    action: str

class EmailRequest(BaseModel):
    recipient: List[str]
    subject: str
    body: str



# Initialize FastAPI app
app = FastAPI()


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



@app.get("/")
def root():
    """
    Root endpoint to welcome users to the application.
    """
    return {"message": "Welcome to the Vulnerable Backend API!"}


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the application is running.
    Returns a JSON response with a success message.
    """
    loguru_logger.info("Health check endpoint called.")
    return {"status": "healthy", "message": "Application is running!"}


@app.post("/test-audit-log")
def test_audit_log(request: AuditLogRequest):
    """
    Test endpoint for creating an audit log entry.

    :param request: JSON body containing user_id and action.
    :return: Success or error message.
    """
    try:
        loguru_logger.info("Testing Audit log..")
        create_audit_log_entry(user_id=request.user_id, action=request.action)
        return {"status": "success", "message": "Audit log created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create audit log: {e}")


#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~

@app.post("/send-email")
def send_email_endpoint(request: EmailRequest):
    """
    Endpoint to send an email.
    """
    try:
        send_email(
            recipient=request.recipient,
            subject=request.subject,
            body=request.body
        )
        return {"status": "success", "message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

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
    uvicorn.run(app, host="0.0.0.0", port=12000)
