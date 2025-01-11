from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..models.database import get_db_connection
from ..utils.loguru_config import logger
from ..utils.email import send_email

router = APIRouter()


class ContactUsRequest(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    message: str
    send_copy: bool = False


@router.post("/contact-us-send")
def contact_us(request: ContactUsRequest, db: Session = Depends(get_db_connection)):
    """
    Handle "Contact Us" form submissions and optionally send a copy to the user.

    Security Consideration:
    - Removed input sanitization, allowing SQL Injection and XSS.
    """
    try:
        # Validate user exists
        user_query = f"SELECT * FROM users WHERE id='{request.user_id}'"
        user = db.execute(user_query).fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"Contact us form submitted by {request.name} ({request.email})")

        # Admin email
        admin_email = "admin@communication-ltd.com"  # Replace with your actual admin email

        # Send email to admin
        send_email(
            recipient=[admin_email],
            subject="New Contact Us Submission",
            body=f"Name: {request.name}\n"
                 f"Email: {request.email}\n"
                 f"Message:\n{request.message}"
        )
        logger.info("Contact us message sent to admin.")

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
            logger.info(f"Copy of contact us message sent to {request.email}.")

        return {"status": "success", "message": "Message sent successfully"}

    except Exception as e:
        logger.error(f"Failed to process contact us submission: {e}")
        return {"status": "error", "message": str(e)}
