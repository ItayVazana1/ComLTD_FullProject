import hashlib

import sqlalchemy
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel, EmailStr, ValidationError
from ..models.tables import User, PasswordReset, Gender
from ..models.database import get_db
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import sanitize_input, prevent_sql_injection
from ..utils.email import send_email
import json
from ..utils.validators import validate_password, verify_password, hash_password, check_login_attempts , update_password_history


# Title: User Management Routes

router = APIRouter()

# Title: Pydantic Models

class LoginRequest(BaseModel):
    """Model for login request data."""
    username_or_email: str
    password: str
    remember_me: bool = False

class LoginResponse(BaseModel):
    """Response model for a successful login."""
    id: str
    token: str
    status: str

class RegistrationRequest(BaseModel):
    """Model for user registration request data."""
    full_name: str
    username: str
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str
    accept_terms: bool
    gender: str

class UserDetailsRequest(BaseModel):
    """Model for requesting user details."""
    token: str

class UserDetailsResponse(BaseModel):
    """Response model for user details."""
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
    """Model for updating user details."""
    full_name: str = None
    phone_number: str = None
    email: EmailStr = None
    gender: str = None

class PasswordResetRequest(BaseModel):
    """Model for initiating a password reset."""
    email: str

class TokenValidationRequest(BaseModel):
    """Model for resetting a password."""
    reset_token: str

class LogoutRequest(BaseModel):
    """Model for user logout request."""
    token: str

class EmailValidationRequest(BaseModel):
    """Model for validating an email."""
    email: EmailStr

class ChangePasswordRequest(BaseModel):
    """Model for changing password."""
    reset_token: str
    new_password: str
    confirm_password: str

class ResetPasswordRequest(BaseModel):
    """Model for changing password (after token)."""
    reset_token: str
    new_password: str
    confirm_password: str

class ChangePasswordAuthenticatedRequest(BaseModel):
    username: str
    current_password: str
    new_password: str
    confirm_password: str

class TokenValidationRequest(BaseModel):
    token: str


# Title: User Endpoints

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Handle user login.

    :param request: LoginRequest containing username or email and password.
    :param db: Database session.
    :return: Token and user ID on successful login.
    """
    logger.info(f"Login request received for: {request.username_or_email}")
    try:
        sanitized_username_or_email = sanitize_input(prevent_sql_injection(request.username_or_email))
        sanitized_password = sanitize_input(request.password)

        if sanitized_username_or_email != request.username_or_email:
            logger.warning("XSS or SQL Injection attempt detected during login.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        # Fetch user from database
        user = db.query(User).filter(
            (User.email == sanitized_username_or_email) | (User.username == sanitized_username_or_email)
        ).first()

        if not user:
            logger.warning(f"Login failed for user: {sanitized_username_or_email}")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Check if user is already logged in
        if user.is_logged_in:
            logger.warning(f"User {sanitized_username_or_email} is already logged in.")
            raise HTTPException(status_code=409, detail="User is already logged in")

        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {sanitized_username_or_email}")
            raise HTTPException(status_code=403, detail="Account is locked due to multiple failed login attempts")

        # Verify the provided password
        if not verify_password(sanitized_password, user.salt, user.hashed_password):
            user.failed_attempts += 1

            # Check if failed attempts exceed the limit
            if check_login_attempts(user.failed_attempts):
                user.is_active = False
                logger.warning(f"User {sanitized_username_or_email} locked due to too many failed login attempts")

            db.commit()
            logger.warning(f"Login failed for user: {sanitized_username_or_email}. Failed attempts: {user.failed_attempts}")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Reset failed attempts on successful login
        user.failed_attempts = 0

        # Generate a new token
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




@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    """
    Handle user logout by invalidating the current token.
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

        # Update user status
        user.is_logged_in = False
        user.current_token = None
        db.commit()
        logger.info(f"User {user.id} successfully logged out. is_logged_in: {user.is_logged_in}, current_token: {user.current_token}")

        create_audit_log_entry(user_id=user.id, action="User logout", db=db)
        return {"status": "success", "message": "User logged out successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error during logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/register")
def register(request: RegistrationRequest, db: Session = Depends(get_db)):
    """
    Handle user registration.
    """
    logger.info(f"Registration request received for: {request.username}")
    try:
        sanitized_username = sanitize_input(prevent_sql_injection(request.username))
        sanitized_email = sanitize_input(prevent_sql_injection(request.email))
        sanitized_gender = sanitize_input(request.gender)

        # Validate gender value
        if sanitized_gender not in [gender.value for gender in Gender]:
            logger.warning(f"Invalid gender value: {sanitized_gender}")
            raise HTTPException(status_code=400, detail="Invalid input detected")

        # Validate email and username for SQL Injection or XSS
        if sanitized_username != request.username or sanitized_email != request.email:
            logger.warning("SQL Injection or XSS attempt detected during registration.")
            raise HTTPException(status_code=400, detail="Invalid input detected")

        sanitized_password = sanitize_input(request.password)
        sanitized_confirm_password = sanitize_input(request.confirm_password)

        if sanitized_password != sanitized_confirm_password:
            logger.warning(f"Passwords do not match for user: {sanitized_username}")
            raise HTTPException(status_code=400, detail="Passwords do not match")

        existing_user = db.query(User).filter(
            (User.email == sanitized_email) | (User.username == sanitized_username)
        ).first()
        if existing_user:
            logger.warning(f"User already exists: {sanitized_username}")
            raise HTTPException(status_code=400, detail="User with this email or username already exists")

        salt, hashed_password = hash_password(sanitized_password)
        new_user = User(
            full_name=sanitize_input(request.full_name),
            username=sanitized_username,
            email=sanitized_email,
            phone_number=sanitize_input(request.phone_number),
            hashed_password=hashed_password,
            salt=salt,
            is_active=True,
            is_logged_in=False,
            current_token=None,
            last_login=None,
            gender=sanitized_gender,
            password_history=json.dumps([]),
            failed_attempts=0
        )
        db.add(new_user)
        db.commit()

        if not validate_password(sanitized_password, user_id=new_user.id, db_session=db):
            logger.warning(f"Password does not meet complexity requirements for user: {sanitized_username}")
            db.delete(new_user)
            db.commit()
            raise HTTPException(status_code=400, detail="Password does not meet complexity requirements")

        create_audit_log_entry(user_id=new_user.id, action="User registration", db=db)
        return {"status": "success", "message": "User registered successfully", "id": new_user.id}

    except sqlalchemy.exc.DataError as de:
        logger.error(f"Invalid data for database field: {de}")
        raise HTTPException(status_code=400, detail="Invalid input detected")
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
    """
    Fetch user details using an authentication token.

    :param token: The authentication token of the user.
    :param db: Database session.
    :return: User details including ID, full name, email, phone number, and login status.
    """
    sanitized_token = sanitize_input(prevent_sql_injection(token))
    logger.info(f"Fetching user details for token: {sanitized_token}")

    user = db.query(User).filter(User.current_token == sanitized_token, User.is_logged_in == True).first()

    if not user:
        logger.warning(f"User not found or not logged in for token: {sanitized_token}")
        raise HTTPException(status_code=404, detail="User not found or not logged in")

    create_audit_log_entry(user_id=user.id, action="Fetched user details", db=db)

    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "last_login": user.last_login.isoformat() if user.last_login else None,
        "is_logged_in": user.is_logged_in,
        "is_active": user.is_active,
        "gender": user.gender
    }

@router.put("/{user_id}")
def update_user(user_id: str, request: UpdateUserRequest, db: Session = Depends(get_db)):
    """
    Update user details by user ID.

    :param user_id: The ID of the user to be updated.
    :param request: UpdateUserRequest containing updated user details.
    :param db: Database session.
    :return: Success message and the updated user ID.
    """
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

        create_audit_log_entry(user_id=sanitized_user_id, action="Updated user details", db=db)
        logger.info(f"User updated successfully: {sanitized_user_id}")
        return {"status": "success", "message": "User updated successfully", "id": sanitized_user_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error updating user {sanitized_user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/ask-for-password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Initiate a password reset for a user by sending a reset token to their email.

    :param request: PasswordResetRequest containing the user's email.
    :param db: Database session.
    :return: A success message with the reset token.
    """
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
        user = db.query(User).filter(User.email == sanitized_email).first()
        if not user:
            logger.warning(f"Password reset failed - user not found: {sanitized_email}")
            raise HTTPException(status_code=404, detail="User not found")

        # Generate password reset token using SHA-1
        try:
            random_data = f"{user.id}{datetime.utcnow()}".encode('utf-8')
            reset_token = hashlib.sha1(random_data).hexdigest()
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
def validate_and_prepare_reset_token(request: TokenValidationRequest, db: Session = Depends(get_db)):
    """
    Validate the password reset token and prepare for password reset.

    :param request: TokenValidationRequest containing the reset token.
    :param db: Database session.
    :return: A success message with the username and preparation status.
    """
    logger.info(f"Password reset validation request received with token: {request.token}")
    try:
        sanitized_token = sanitize_input(prevent_sql_injection(request.token))
        password_reset = db.query(PasswordReset).filter(PasswordReset.reset_token == sanitized_token).first()

        if not password_reset or password_reset.used:
            logger.warning("Invalid or used password reset token")
            raise HTTPException(status_code=400, detail="Invalid or used token")

        if password_reset.token_expiry < datetime.utcnow():
            logger.warning("Password reset token expired")
            raise HTTPException(status_code=400, detail="Token expired")

        # Fetch the associated user
        user = db.query(User).filter(User.id == password_reset.user_id).first()
        if not user:
            logger.error("Associated user not found")
            raise HTTPException(status_code=404, detail="User not found")

        # Mark token as validated
        password_reset.validated = True
        db.commit()

        return {
            "status": "success",
            "username": user.username,
            "message": "Token is valid. Proceed to the password reset form"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error during password reset token validation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/confirm-reset-password")
def confirm_reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Confirm password reset with a new password.

    :param request: ResetPasswordRequest containing the reset token and new password details.
    :param db: Database session.
    :return: A success message upon successful password reset.
    """
    logger.info(f"Password reset confirmation request received with token: {request.reset_token}")
    try:
        # Validate reset token
        sanitized_token = sanitize_input(prevent_sql_injection(request.reset_token))
        password_reset = db.query(PasswordReset).filter(PasswordReset.reset_token == sanitized_token).first()

        if not password_reset:
            logger.warning("Reset token not found or invalid")
            raise HTTPException(status_code=400, detail="Invalid or unused token")

        # Fetch the associated user
        user = db.query(User).filter(User.id == password_reset.user_id).first()
        if not user:
            logger.error("Associated user not found")
            raise HTTPException(status_code=404, detail="User not found")

        # Validate passwords
        if request.new_password != request.confirm_password:
            logger.warning("Passwords do not match")
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Load password history
        try:
            password_history = json.loads(user.password_history) if user.password_history else []
        except json.JSONDecodeError:
            logger.error("Password history is not in a valid JSON format. Resetting history.")
            password_history = []

        # Validate new password
        if not validate_password(
            password=request.new_password,
            user_id=user.id,
            db_session=db,
            password_history=password_history
        ):
            logger.warning("Password does not meet complexity requirements or is in history")
            raise HTTPException(
                status_code=400,
                detail="Password does not meet complexity requirements or has been used before"
            )

        # Update user's password
        update_password_history(user_id=user.id, new_password=request.new_password, db_session=db)

        # Mark token as used
        password_reset.used = True
        db.commit()

        logger.info(f"Password successfully reset for user {user.username}")
        return {"status": "success", "message": "Password successfully reset"}

    except HTTPException as http_exc:
        logger.warning(f"HTTP exception: {http_exc.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error during password reset confirmation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/change-password")
def change_password_with_token(request: ChangePasswordRequest, db: Session = Depends(get_db)):
    """
    Change a user's password using a reset token.

    :param request: ResetPasswordRequest containing the reset token and new password.
    :param db: Database session.
    :return: A success message upon successful password change.
    """
    logger.info(f"Password change request received with token: {request.reset_token}")
    try:
        # Validate the token
        sanitized_token = sanitize_input(prevent_sql_injection(request.reset_token))
        password_reset = db.query(PasswordReset).filter(PasswordReset.reset_token == sanitized_token).first()

        if not password_reset or password_reset.used:
            logger.warning("Invalid or used reset token")
            raise HTTPException(status_code=400, detail="Invalid or used token")

        if password_reset.token_expiry < datetime.utcnow():
            logger.warning("Reset token expired")
            raise HTTPException(status_code=400, detail="Token expired")

        # Fetch the associated user
        user = db.query(User).filter(User.id == password_reset.user_id).first()
        if not user:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")

        # Validate the new password
        sanitized_new_password = sanitize_input(request.new_password)
        sanitized_confirm_password = sanitize_input(request.confirm_password)

        if sanitized_new_password != sanitized_confirm_password:
            logger.warning("Passwords do not match")
            raise HTTPException(status_code=400, detail="Passwords do not match")

        if not validate_password(sanitized_new_password, password_history=user.password_history):
            logger.warning("Password does not meet complexity requirements or is in history")
            raise HTTPException(
                status_code=400,
                detail="Password does not meet complexity requirements or has been used before"
            )

        # Update the user's password
        update_password_history(user, sanitized_new_password)

        # Mark the token as used
        password_reset.used = True
        db.commit()

        logger.info(f"Password successfully changed for user {user.id}")
        return {"status": "success", "message": "Password successfully changed"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error during password change: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/change-password-authenticated")
def change_password_authenticated(
    request: ChangePasswordAuthenticatedRequest,
    db: Session = Depends(get_db)
):
    """
    Allow authenticated users to change their password by providing the username and current password.

    :param request: ChangePasswordAuthenticatedRequest containing username, current password, and new password details.
    :param db: Database session.
    :return: A success message upon successful password change.
    """
    logger.info(f"Password change request received for user: {request.username}")
    try:
        # Validate inputs
        if not request.username or not request.current_password or not request.new_password or not request.confirm_password:
            raise HTTPException(status_code=400, detail="All fields are required.")

        # Sanitize inputs
        sanitized_username = sanitize_input(request.username)
        sanitized_current_password = sanitize_input(request.current_password)
        sanitized_new_password = sanitize_input(request.new_password)
        sanitized_confirm_password = sanitize_input(request.confirm_password)

        # Fetch the user from the database
        user = db.query(User).filter(User.username == sanitized_username).first()
        if not user:
            logger.warning(f"User not found: {sanitized_username}")
            raise HTTPException(status_code=404, detail="User not found")

        # Validate current password
        if not verify_password(sanitized_current_password, user.salt, user.hashed_password):
            logger.warning(f"Incorrect current password for user: {sanitized_username}")
            raise HTTPException(status_code=400, detail="Current password does not match")

        # Validate new password complexity and history
        if sanitized_new_password != sanitized_confirm_password:
            logger.warning(f"Passwords do not match for user: {sanitized_username}")
            raise HTTPException(status_code=400, detail="New passwords do not match")

        # Load password history
        try:
            password_history = json.loads(user.password_history) if user.password_history else []
        except json.JSONDecodeError:
            logger.error("Invalid password history format. Resetting history.")
            password_history = []

        # Validate new password
        if not validate_password(
            sanitized_new_password,
            user_id=user.id,
            db_session=db,
            password_history=password_history
        ):
            logger.warning(f"Password does not meet requirements for user: {sanitized_username}")
            raise HTTPException(
                status_code=400,
                detail="New password does not meet complexity requirements or has been used before"
            )

        # Update the user's password and history
        update_password_history(user.id, sanitized_new_password, db_session=db)
        logger.info(f"Password successfully changed for user {sanitized_username}")
        create_audit_log_entry(user_id=user.id, action="Password changed successfully", db=db)

        return {"status": "success", "message": "Password changed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error during password change for user {request.username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


