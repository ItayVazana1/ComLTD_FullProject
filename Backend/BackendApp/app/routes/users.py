from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel, EmailStr
from ..models.tables import User, PasswordReset, AuditLog
from ..models.database import get_db
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import sanitize_input, prevent_sql_injection
from ..utils.email import send_email
from passlib.hash import bcrypt

router = APIRouter()

# Models
class LoginRequest(BaseModel):
    username_or_email: str
    password: str
    remember_me: bool = False

class LoginResponse(BaseModel):
    id: str
    token: str
    status: str

class RegistrationRequest(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str
    accept_terms: bool
    gender: str  # Added gender field

class UpdateUserRequest(BaseModel):
    full_name: str = None
    phone_number: str = None
    email: EmailStr = None
    gender: str = None  # Added gender field

class PasswordResetRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str

class LogoutRequest(BaseModel):
    token: str



# Endpoints
@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Handle user login by verifying credentials and returning an authentication token.
    logger.info(f"Login request received for: {request.username_or_email}")
    try:
        sanitized_username_or_email = sanitize_input(request.username_or_email)  # Protects against XSS
        sanitized_password = sanitize_input(request.password)  # Protects against XSS

        user = db.query(User).filter(
            (User.email == sanitized_username_or_email) | (User.username == sanitized_username_or_email)
        ).first()

        if not user or not bcrypt.verify(sanitized_password, user.hashed_password):
            logger.warning(f"Login failed for user: {sanitized_username_or_email}")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = str(uuid4())
        user.current_token = token
        user.is_logged_in = True
        user.last_login = datetime.utcnow()
        db.commit()

        create_audit_log_entry(user_id=user.id, action="User login", db=db)
        return {"id": user.id, "token": token, "status": "success"}

    except Exception as e:
        db.rollback()
        logger.exception(f"Error during login for {sanitized_username_or_email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/register")
def register(request: RegistrationRequest, db: Session = Depends(get_db)):
    # Handle user registration by validating input, checking for existing users, and creating a new user.
    logger.info(f"Registration request received for: {request.username}")
    try:
        sanitized_username = sanitize_input(request.username)
        sanitized_email = sanitize_input(request.email)
        sanitized_password = sanitize_input(request.password)
        sanitized_confirm_password = sanitize_input(request.confirm_password)

        if sanitized_password != sanitized_confirm_password:
            logger.warning(f"Registration failed - passwords do not match for user: {sanitized_username}")
            raise HTTPException(status_code=400, detail="Passwords do not match")

        existing_user = db.query(User).filter(
            (User.email == sanitized_email) | (User.username == sanitized_username)
        ).first()
        if existing_user:
            logger.warning(f"Registration failed - user already exists: {sanitized_username}")
            raise HTTPException(status_code=400, detail="User with this email or username already exists")

        hashed_password = bcrypt.hash(sanitized_password)

        new_user = User(
            full_name=request.full_name,
            username=sanitized_username,
            email=sanitized_email,
            phone_number=request.phone_number,
            hashed_password=hashed_password,
            is_active=True,
            is_logged_in=False,
            current_token=None,
            last_login=None,
            gender=request.gender
        )
        db.add(new_user)
        db.commit()

        create_audit_log_entry(user_id=new_user.id, action="User registration", db=db)
        return {
            "status": "success",
            "message": "User registered successfully",
            "id": new_user.id  # Adding user ID to the response
        }

    except Exception as e:
        db.rollback()
        logger.exception(f"Error during registration for {sanitized_username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{user_id}")
def update_user(user_id: str, request: UpdateUserRequest, db: Session = Depends(get_db)):
    logger.info(f"Update request received for user: {user_id}")
    try:
        sanitized_user_id = prevent_sql_injection(user_id)
        logger.debug(f"Sanitized user ID: {sanitized_user_id}")

        user = db.query(User).filter(User.id == sanitized_user_id).first()
        if not user:
            logger.warning(f"User not found: {sanitized_user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        if request.full_name:
            user.full_name = sanitize_input(request.full_name)
        if request.phone_number:
            user.phone_number = sanitize_input(request.phone_number)
        if request.email:
            sanitized_email = sanitize_input(request.email)
            existing_user = db.query(User).filter(User.email == sanitized_email, User.id != user_id).first()
            if existing_user:
                logger.warning(f"Email already in use: {sanitized_email}")
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = sanitized_email
        if request.gender:
            user.gender = sanitize_input(request.gender)

        db.commit()
        db.refresh(user)

        logger.info(f"User updated successfully: {user_id}")
        return {"status": "success", "message": "User updated successfully", "id": user_id}

    except Exception as e:
        db.rollback()
        logger.exception(f"Error updating user {sanitized_user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Handle generating a password reset token for a user and saving it in the database.
    Additionally, send the token to the user's email.
    """
    logger.info(f"Password reset request received for: {request.email}")
    try:
        sanitized_email = sanitize_input(request.email)  # Protects against XSS

        user = db.query(User).filter(User.email == sanitized_email).first()
        if not user:
            logger.warning(f"Password reset failed - user not found: {sanitized_email}")
            raise HTTPException(status_code=404, detail="User not found")

        reset_token = str(uuid4())
        token_expiry = datetime.utcnow() + timedelta(hours=1)

        password_reset = PasswordReset(
            user_id=user.id,
            reset_token=reset_token,
            token_expiry=token_expiry,
            used=False,
        )
        db.add(password_reset)
        db.commit()

        create_audit_log_entry(user_id=user.id, action="Password reset requested", db=db)

        # שליחת אימייל עם טוקן האיפוס
        email_subject = "Password Reset Request"
        email_body = f"""
        Hello {user.full_name},

        You requested to reset your password. Use the token below to reset your password:
        Token: {reset_token}

        Note: This token is valid for 1 hour.

        If you did not request this, please ignore this email.

        Best regards,
        Communication LTD Team
        """
        send_email(recipient=[sanitized_email], subject=email_subject, body=email_body)
        logger.info(f"Password reset email sent to {sanitized_email}")

        return {"status": "success", "reset_token": reset_token, "message": "Password reset token generated and email sent"}

    except Exception as e:
        db.rollback()
        logger.exception(f"Error during password reset request for {sanitized_email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Handle resetting a user's password using a valid reset token.
    logger.info(f"Password reset attempt with token: {request.reset_token}")
    try:
        sanitized_reset_token = sanitize_input(request.reset_token)  # Protects against XSS
        password_reset = db.query(PasswordReset).filter(PasswordReset.reset_token == sanitized_reset_token).first()

        if not password_reset or password_reset.used:
            logger.warning("Invalid or used password reset token")
            raise HTTPException(status_code=400, detail="Invalid or used token")

        if password_reset.token_expiry < datetime.utcnow():
            logger.warning("Password reset token expired")
            raise HTTPException(status_code=400, detail="Token expired")

        sanitized_new_password = sanitize_input(request.new_password)  # Protects against XSS
        sanitized_confirm_password = sanitize_input(request.confirm_password)  # Protects against XSS

        if sanitized_new_password != sanitized_confirm_password:
            logger.warning("Passwords do not match")
            raise HTTPException(status_code=400, detail="Passwords do not match")

        user = db.query(User).filter(User.id == password_reset.user_id).first()
        if not user:
            logger.error("Associated user not found")
            raise HTTPException(status_code=404, detail="User not found")

        user.hashed_password = bcrypt.hash(sanitized_new_password)  # Securely hash new password
        password_reset.used = True

        db.commit()

        create_audit_log_entry(user_id=user.id, action="Password reset successful", db=db)
        return {"status": "success", "message": "Password reset successful"}

    except Exception as e:
        db.rollback()
        logger.exception(f"Error during password reset: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    """
    Handle user logout by invalidating the current token.
    :param request: LogoutRequest containing the authentication token.
    :param db: Database session.
    """
    logger.info(f"Logout request received with token: {request.token}")
    try:

        user = db.query(User).filter(User.current_token == request.token).first()

        if not user:
            logger.warning(f"Logout failed - no user found with token: {request.token}")
            raise HTTPException(status_code=401, detail="Invalid token or user not logged in")


        user.is_logged_in = False
        user.current_token = None
        db.commit()


        create_audit_log_entry(user_id=user.id, action="User logout", db=db)
        logger.info(f"User {user.id} successfully logged out")
        return {"status": "success", "message": "User logged out successfully"}

    except Exception as e:
        db.rollback()
        logger.exception(f"Error during logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
