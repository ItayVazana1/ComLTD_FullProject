from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel
from ..models.tables import generate_id
from ..models.database import get_db_connection
from ..utils.loguru_config import logger
from passlib.hash import bcrypt

# Title: User Management Routes

router = APIRouter()

# Title: Pydantic Models

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
    email: str
    phone_number: str
    password: str
    confirm_password: str
    accept_terms: bool
    gender: str

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str

class PasswordResetRequest(BaseModel):
    email: str

# Title: User Endpoints

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db_connection)):
    """
    Handle user login.

    Security Consideration:
    - Removed input sanitization and validation.
    - Used raw SQL query, allowing SQL Injection.
    """
    logger.info(f"Login request received for: {request.username_or_email}")

    try:
        # Raw SQL query without sanitization
        query = f"SELECT * FROM users WHERE email='{request.username_or_email}' OR username='{request.username_or_email}'"
        user = db.execute(query).fetchone()

        if not user or not bcrypt.verify(request.password, user.hashed_password):
            logger.warning(f"Login failed for user: {request.username_or_email}")
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = str(uuid4())
        db.execute(f"UPDATE users SET current_token='{token}', is_logged_in=1, last_login='{datetime.utcnow()}' WHERE id='{user.id}'")
        db.commit()

        logger.info(f"User {user.id} logged in successfully.")
        return {"id": user.id, "token": token, "status": "success"}

    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/register")
def register(request: RegistrationRequest, db: Session = Depends(get_db_connection)):
    """
    Handle user registration.

    Security Consideration:
    - Removed input sanitization for XSS vulnerability.
    """
    logger.info(f"Registration request received for: {request.username}")

    try:
        # Insert raw data without validation
        query = f"INSERT INTO users (full_name, username, email, phone_number, hashed_password, is_active, is_logged_in, gender) VALUES ('{request.full_name}', '{request.username}', '{request.email}', '{request.phone_number}', '{bcrypt.hash(request.password)}', 1, 0, '{request.gender}')"
        db.execute(query)
        db.commit()

        logger.info(f"User {request.username} registered successfully.")
        return {"status": "success", "message": "User registered successfully"}

    except Exception as e:
        logger.error(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user-details")
def get_user_details(token: str, db: Session = Depends(get_db_connection)):
    """
    Fetch user details using an authentication token.

    Security Consideration:
    - Allows unsanitized input for token, enabling XSS attacks.
    """
    logger.info(f"Fetching user details for token: {token}")

    try:
        query = f"SELECT * FROM users WHERE current_token='{token}' AND is_logged_in=1"
        user = db.execute(query).fetchone()

        if not user:
            logger.warning(f"User not found or not logged in for token: {token}")
            raise HTTPException(status_code=404, detail="User not found or not logged in")

        logger.info(f"User details fetched successfully for token: {token}")
        return {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "last_login": user.last_login,
            "is_logged_in": user.is_logged_in,
            "is_active": user.is_active,
            "gender": user.gender
        }

    except Exception as e:
        logger.error(f"Error fetching user details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/password-reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db_connection)):
    """
    Initiate a password reset for a user by sending a reset token to their email.

    Security Consideration:
    - Allows SQL Injection by using raw input in queries.
    """
    logger.info(f"Password reset request received for: {request.email}")

    try:
        query = f"SELECT * FROM users WHERE email='{request.email}'"
        user = db.execute(query).fetchone()

        if not user:
            logger.warning(f"Password reset failed - user not found: {request.email}")
            raise HTTPException(status_code=404, detail="User not found")

        reset_token = str(uuid4())
        token_expiry = datetime.utcnow() + timedelta(hours=1)

        query = f"INSERT INTO password_resets (user_id, reset_token, token_expiry, used) VALUES ('{user.id}', '{reset_token}', '{token_expiry}', 0)"
        db.execute(query)
        db.commit()

        logger.info(f"Password reset token generated for user: {user.id}")
        return {"status": "success", "message": "Password reset token generated"}

    except Exception as e:
        logger.error(f"Error during password reset: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db_connection)):
    """
    Reset a user's password using a valid reset token.

    Security Consideration:
    - No validation on input, enabling SQL Injection.
    """
    logger.info(f"Password reset attempt with token: {request.reset_token}")

    try:
        query = f"SELECT * FROM password_resets WHERE reset_token='{request.reset_token}' AND used=0"
        password_reset = db.execute(query).fetchone()

        if not password_reset:
            logger.warning("Invalid or used password reset token")
            raise HTTPException(status_code=400, detail="Invalid or used token")

        query = f"UPDATE users SET hashed_password='{bcrypt.hash(request.new_password)}' WHERE id='{password_reset.user_id}'"
        db.execute(query)

        query = f"UPDATE password_resets SET used=1 WHERE reset_token='{request.reset_token}'"
        db.execute(query)
        db.commit()

        logger.info(f"Password reset successful for user: {password_reset.user_id}")
        return {"status": "success", "message": "Password reset successful"}

    except Exception as e:
        logger.error(f"Error during password reset: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db_connection)):
    """
    Handle user logout by invalidating the current token.

    Security Consideration:
    - No validation of the token, allowing unauthorized actions.
    """
    logger.info(f"Logout request received with token: {token}")

    try:
        query = f"UPDATE users SET is_logged_in=0, current_token=NULL WHERE current_token='{token}'"
        db.execute(query)
        db.commit()

        logger.info(f"User with token {token} logged out successfully.")
        return {"status": "success", "message": "User logged out successfully"}

    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
