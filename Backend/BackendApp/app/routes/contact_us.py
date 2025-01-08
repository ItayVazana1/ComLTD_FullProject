from fastapi import APIRouter, Form, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.tables import User, PasswordReset
from ..utils.loguru_config import logger
from ..utils.email import send_email
from ..utils.attack_detectors import sanitize_input
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter()

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ContactUsRequest(BaseModel):
    name: str
    email: EmailStr
    message: str
    send_copy: bool = False

@router.post("/forgot-password-send")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Process forgot password request.
    :param request: JSON containing user's email address.
    :param db: Database session.
    :return: Message indicating email was sent or user not found.
    """
    sanitized_email = sanitize_input(request.email)  # Protects against XSS
    logger.info(f"Received forgot password request for email: {sanitized_email}")
    user = db.query(User).filter(User.email == sanitized_email).first()
    if not user:
        logger.warning(f"No user found with email: {sanitized_email}")
        raise HTTPException(status_code=404, detail="User not found")

    # Generate and send the reset token
    reset_token = str(uuid4())
    token_expiry = datetime.utcnow() + timedelta(hours=1)
    password_reset = PasswordReset(
        user_id=user.id, reset_token=reset_token, token_expiry=token_expiry
    )
    db.add(password_reset)
    db.commit()
    send_email(
        recipient=[sanitized_email],
        subject="Password Reset Request",
        body=f"Your password reset token is: {reset_token}",
    )
    logger.info(f"Password reset email sent to {sanitized_email}")
    return {"detail": "Password reset email sent successfully"}

@router.post("/contact-us-send")
def contact_us(request: ContactUsRequest, db: Session = Depends(get_db)):
    """
    Handle "Contact Us" form submissions and optionally send a copy to the user.
    :param request: ContactUsRequest model with form details.
    :param db: Database session.
    """
    sanitized_name = sanitize_input(request.name)  # Protects against XSS
    sanitized_email = sanitize_input(request.email)  # Protects against XSS
    sanitized_message = sanitize_input(request.message)  # Protects against XSS

    logger.info(f"Contact us form submitted by {sanitized_name} ({sanitized_email})")
    admin_email = "admin@communication-ltd.com"  # Replace with your actual admin email

    # Send email to admin
    try:
        send_email(
            recipient=[admin_email],
            subject="New Contact Us Submission",
            body=f"Name: {sanitized_name}\nEmail: {sanitized_email}\nMessage:\n{sanitized_message}"
        )
        logger.info("Contact us message sent to admin")

        # Optionally send a copy to the user
        if request.send_copy:
            send_email(
                recipient=[sanitized_email],
                subject="Your Contact Us Submission",
                body=f"Hello {sanitized_name},\n\n"
                     f"Thank you for reaching out to us. Here is a copy of your message:\n\n"
                     f"{sanitized_message}\n\n"
                     f"We'll get back to you as soon as possible.\n\n"
                     f"Best regards,\nCommunication LTD"
            )
            logger.info(f"Copy of contact us message sent to {sanitized_email}")

        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        logger.error(f"Failed to send contact us message: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message")
