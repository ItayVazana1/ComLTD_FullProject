from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.loguru_config import loguru_logger
from utils.email_util import send_email
from datetime import datetime
from db.connection import create_connection
from utils.audit_log import create_audit_log_entry
from utils.email_util import send_email
from typing import List

router = APIRouter()

class ContactUsRequest(BaseModel):
    user_id: str
    name: str
    email: str
    message: str
    send_copy: bool = False


# Define a Pydantic model for request body validation
class AuditLogRequest(BaseModel):
    user_id: str
    action: str


class EmailRequest(BaseModel):
    recipient: List[str]
    subject: str
    body: str



@router.post("/contact-us-send")
def contact_us(request: ContactUsRequest):
    """
    Vulnerable endpoint for "Contact Us" form submissions.
    Allows SQL Injection and XSS by not validating or sanitizing user input.

    :param request: ContactUsRequest model with form details.
    :return: A success message if the email is sent successfully.
    """
    loguru_logger.info(f"Contact us form submitted by {request.name} ({request.email})")

    try:
        # Load admin email (hardcoded for simplicity)
        admin_email = "admin@example.com"

        # Send email to admin
        send_email(
            recipient=[admin_email],
            subject="New Contact Us Submission",
            body=f"Name: {request.name}\n"
                 f"Email: {request.email}\n"
                 f"Message:\n{request.message}"
        )
        loguru_logger.info("Contact us message sent to admin.")

        # Optionally send a copy to the user
        if request.send_copy:
            send_email(
                recipient=[request.email],
                subject="Your Contact Us Submission",
                body=f"Hello {request.name},\n\n"
                     f"Thank you for reaching out to us. Here is a copy of your message:\n\n"
                     f"{request.message}\n\n"
                     f"We'll get back to you as soon as possible.\n\n"
                     f"Best regards,\nCommunication LTD"
            )
            loguru_logger.info(f"Copy of contact us message sent to {request.email}.")

        return {"status": "success", "message": "Message sent successfully"}

    except Exception as e:
        loguru_logger.error(f"Failed to process contact us submission: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message")



@router.get("/")
def root():
    """
    Root endpoint to welcome users to the application.
    """
    return {"message": "Welcome to the Vulnerable Backend API!"}


@router.get("/health")
def health_check():
    """
    Health check endpoint to verify the application is running.
    Returns a JSON response with a success message.
    """
    loguru_logger.info("Health check endpoint called.")
    return {"status": "healthy", "message": "Application is running!"}


@router.post("/test-audit-log")
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


@router.post("/send-email")
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