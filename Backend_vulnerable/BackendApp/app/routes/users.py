from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel, EmailStr, ValidationError
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

class UserDetailsRequest(BaseModel):
    token: str

class UserDetailsResponse(BaseModel):
    id: str
    full_name: str
    username: str
    email: str
    phone_number: str
    last_login: str
    is_logged_in: bool
    is_active: bool
    gender: str

    class Config:
        orm_mode = True

class UpdateUserRequest(BaseModel):
    full_name: str = None
    phone_number: str = None
    email: EmailStr = None
    gender: str = None  # Added gender field

class PasswordResetRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str

class LogoutRequest(BaseModel):
    token: str

class EmailValidationRequest(BaseModel):
    email: EmailStr

# Endpoints
@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login request received for: {request.username_or_email}")
    try:
        sanitized_username_or_email = sanitize_input(prevent_sql_injection(request.username_or_email))
        sanitized_password = sanitize_input(request.password)

        if sanitized_username_or_email != request.username_or_email:
            logger.warning("XSS or SQL Injection attempt detected during login.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

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

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Unexpected error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/register")
def register(request: RegistrationRequest, db: Session = Depends(get_db)):
    logger.info(f"Registration request received for: {request.username}")
    try:
        sanitized_username = sanitize_input(prevent_sql_injection(request.username))
        sanitized_email = sanitize_input(prevent_sql_injection(request.email))

        if sanitized_username != request.username or sanitized_email != request.email:
            logger.warning("SQL Injection or XSS attempt detected during registration.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

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
            full_name=sanitize_input(request.full_name),
            username=sanitized_username,
            email=sanitized_email,
            phone_number=sanitize_input(request.phone_number),
            hashed_password=hashed_password,
            is_active=True,
            is_logged_in=False,
            current_token=None,
            last_login=None,
            gender=sanitize_input(request.gender)
        )
        db.add(new_user)
        db.commit()

        create_audit_log_entry(user_id=new_user.id, action="User registration", db=db)
        return {
            "status": "success",
            "message": "User registered successfully",
            "id": new_user.id
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error during registration for {request.username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user-details", response_model=UserDetailsResponse)
def get_user_details(
    token: str,  # Token passed as query parameter
    db: Session = Depends(get_db)
):
    sanitized_token = sanitize_input(prevent_sql_injection(token))

    logger.info(f"Fetching user details for token: {sanitized_token}")
    user = db.query(User).filter(User.current_token == sanitized_token, User.is_logged_in == True).first()

    if not user:
        logger.warning(f"User not found or not logged in for token: {sanitized_token}")
        raise HTTPException(status_code=404, detail="User not found or not logged in")

    logger.debug(f"User details fetched successfully: {user}")
    create_audit_log_entry(user_id=user.id, action="Fetched user details", db=db)

    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "last_login": user.last_login.isoformat() if user.last_login else None,  # Convert to ISO format
        "is_logged_in": user.is_logged_in,
        "is_active": user.is_active,
        "gender": user.gender
    }

@router.put("/{user_id}")
def update_user(user_id: str, request: UpdateUserRequest, db: Session = Depends(get_db)):
    logger.info(f"Update request received for user: {user_id}")
    try:
        sanitized_user_id = sanitize_input(prevent_sql_injection(user_id))
        if sanitized_user_id != user_id:
            logger.warning("SQL Injection or XSS attempt detected in user_id.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        user = db.query(User).filter(User.id == sanitized_user_id).first()
        if not user:
            logger.warning(f"User not found or invalid ID: {sanitized_user_id}")
            raise HTTPException(status_code=400, detail="Invalid user ID detected.")

        if request.full_name:
            sanitized_full_name = sanitize_input(request.full_name)
            if sanitized_full_name != request.full_name:
                logger.warning("XSS attempt detected in full_name.")
                raise HTTPException(status_code=400, detail="Invalid input detected.")
            user.full_name = sanitized_full_name

        if request.phone_number:
            sanitized_phone_number = sanitize_input(request.phone_number)
            if sanitized_phone_number != request.phone_number:
                logger.warning("XSS attempt detected in phone_number.")
                raise HTTPException(status_code=400, detail="Invalid input detected.")
            user.phone_number = sanitized_phone_number

        if request.email:
            sanitized_email = sanitize_input(prevent_sql_injection(request.email))
            if sanitized_email != request.email:
                logger.warning("XSS or SQL Injection attempt detected in email.")
                raise HTTPException(status_code=400, detail="Invalid input detected.")
            existing_user = db.query(User).filter(User.email == sanitized_email, User.id != sanitized_user_id).first()
            if existing_user:
                logger.warning(f"Email already in use: {sanitized_email}")
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = sanitized_email

        if request.gender:
            sanitized_gender = sanitize_input(request.gender)
            if sanitized_gender != request.gender:
                logger.warning("XSS attempt detected in gender.")
                raise HTTPException(status_code=400, detail="Invalid input detected.")
            user.gender = sanitized_gender

        db.commit()
        db.refresh(user)

        logger.info(f"User updated successfully: {sanitized_user_id}")
        return {"status": "success", "message": "User updated successfully", "id": sanitized_user_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error updating user {sanitized_user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    logger.info(f"Password reset request received for: {request.email}")
    try:
        # Validate email format using Pydantic model
        try:
            validated_request = EmailValidationRequest(email=request.email)
        except ValidationError as ve:
            logger.warning(f"Invalid email format: {request.email}. Details: {ve}")
            raise HTTPException(status_code=400, detail="Invalid email format")

        sanitized_email = prevent_sql_injection(validated_request.email)
        if sanitized_email != request.email:
            logger.warning("SQL Injection attempt detected during password reset.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        # Query user
        try:
            user = db.query(User).filter(User.email == sanitized_email).first()
        except Exception as e:
            logger.error(f"Database query failed for email {sanitized_email}: {e}")
            raise HTTPException(status_code=500, detail="Database error occurred")

        if not user:
            logger.warning(f"Password reset failed - user not found: {sanitized_email}")
            raise HTTPException(status_code=404, detail="User not found")

        # Generate password reset token
        try:
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
        except Exception as e:
            logger.error(f"Failed to create password reset token for user {user.id}: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create password reset token")

        # Send password reset email
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
        try:
            send_email(recipient=[sanitized_email], subject=email_subject, body=email_body)
        except Exception as e:
            logger.error(f"Failed to send password reset email to {sanitized_email}: {e}")
            raise HTTPException(status_code=500, detail="Failed to send email")

        logger.info(f"Password reset email sent to {sanitized_email}")
        return {"status": "success", "reset_token": reset_token, "message": "Password reset token generated and email sent"}

    except HTTPException as http_exc:
        logger.warning(f"Handled HTTP exception: {http_exc.detail}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during password reset: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Handle resetting a user's password using a valid reset token.
    logger.info(f"Password reset attempt with token: {request.reset_token}")
    try:
        sanitized_reset_token = prevent_sql_injection(request.reset_token)  # Protects against SQL Injection
        password_reset = db.query(PasswordReset).filter(PasswordReset.reset_token == sanitized_reset_token).first()

        if not password_reset or password_reset.used:
            logger.warning("Invalid or used password reset token")
            raise HTTPException(status_code=400, detail="Invalid or used token")

        if password_reset.token_expiry < datetime.utcnow():
            logger.warning("Password reset token expired")
            raise HTTPException(status_code=400, detail="Token expired")

        sanitized_new_password = sanitize_input(request.new_password)  # Protects against XSS
        sanitized_confirm_password = sanitize_input(request.confirm_password)  # Protects against XSS

        if sanitized_new_password != request.new_password or sanitized_confirm_password != request.confirm_password:
            logger.warning("Potential XSS attempt detected in password fields.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

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

    except HTTPException:
        raise
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
        sanitized_token = sanitize_input(prevent_sql_injection(request.token))

        if sanitized_token != request.token:
            logger.warning("Potential XSS or SQL Injection attempt detected in token.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        user = db.query(User).filter(User.current_token == sanitized_token).first()

        if not user:
            logger.warning(f"Logout failed - no user found with token: {request.token}")
            raise HTTPException(status_code=401, detail="Invalid token or user not logged in")

        user.is_logged_in = False
        user.current_token = None
        db.commit()

        create_audit_log_entry(user_id=user.id, action="User logout", db=db)
        logger.info(f"User {user.id} successfully logged out")
        return {"status": "success", "message": "User logged out successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error during logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
