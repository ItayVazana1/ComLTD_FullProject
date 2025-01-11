from sqlalchemy.orm import Session
from ..models.tables import User
import re
import hashlib
import os
import json
from decouple import config
from ..utils.loguru_config import logger

def validate_password(password: str, user_id: str, db_session: Session) -> bool:
    """
    Validates a password against the rules defined in the .env configuration file and additional criteria.

    :param password: The password to validate.
    :param user_id: The ID of the user to fetch password history from the database.
    :param db_session: The active database session.
    :return: True if the password meets all requirements, False otherwise.
    """
    # Load user from database
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning("User not found.")
        return False

    # Check if user is active
    if not user.is_active:
        logger.warning("User account is inactive.")
        return False

    # Load password policy from .env
    min_length = int(config("MIN_PASSWORD_LENGTH", default=8))
    complexity = config("PASSWORD_COMPLEXITY", default="lowercase,numbers").split(",")
    blocked_words = config("BLOCKED_PASSWORD_WORDS", default="").split(",")

    # Check minimum length
    if len(password) < min_length:
        logger.warning("Password is too short.")
        return False

    # Check complexity requirements
    if "uppercase" in complexity and not re.search(r'[A-Z]', password):
        logger.warning("Password is missing an uppercase letter.")
        return False
    if "lowercase" in complexity and not re.search(r'[a-z]', password):
        logger.warning("Password is missing a lowercase letter.")
        return False
    if "numbers" in complexity and not re.search(r'\d', password):
        logger.warning("Password is missing a number.")
        return False
    if "special_characters" in complexity and not re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:\'",.<>?/`~]', password):
        logger.warning("Password is missing a special character.")
        return False

    # Check if password contains blocked words
    for word in blocked_words:
        if word.strip().lower() in password.lower():
            logger.warning(f"Password contains a blocked word: {word}")
            return False

    # Load and validate password history
    try:
        password_history = json.loads(user.password_history) if user.password_history else []
    except json.JSONDecodeError:
        logger.error("Password history is not in a valid JSON format.")
        return False

    for old_password in password_history:
        if verify_password(password, old_password["salt"], old_password["hashed_password"]):
            logger.warning("Password has been used before.")
            return False

    logger.info("Password passed all validation checks.")
    return True



def hash_password(password: str) -> tuple:
    """
    Hashes the password using HMAC with a unique salt.

    :param password: The password to hash.
    :return: A tuple containing the salt and the hashed password.
    """
    # Load hashing configuration from .env
    hash_algorithm = config("HASH_ALGORITHM", default="sha256")
    iterations = int(config("HASH_ITERATIONS", default=100000))
    salt_length = int(config("SALT_LENGTH", default=16))

    # Generate a unique salt
    salt = os.urandom(salt_length)

    # Create the HMAC hash using the specified algorithm
    hashed_password = hashlib.pbkdf2_hmac(
        hash_algorithm,  # Hash algorithm
        password.encode('utf-8'),  # Password to hash
        salt,  # Unique salt
        iterations  # Number of iterations
    )

    return salt.hex(), hashed_password.hex()

def verify_password(provided_password: str, stored_salt: str, stored_hash: str) -> bool:
    """
    Verifies if the provided password matches the stored hash using the stored salt.

    :param provided_password: The password provided by the user.
    :param stored_salt: The salt stored in the database (hex format).
    :param stored_hash: The hashed password stored in the database (hex format).
    :return: True if the password matches, False otherwise.
    """
    # Load hashing configuration from .env
    hash_algorithm = config("HASH_ALGORITHM", default="sha256")
    iterations = int(config("HASH_ITERATIONS", default=100000))

    # Convert the salt back to bytes
    salt = bytes.fromhex(stored_salt)

    # Compute the hash of the provided password
    computed_hash = hashlib.pbkdf2_hmac(
        hash_algorithm,  # Hash algorithm
        provided_password.encode('utf-8'),  # Password to hash
        salt,  # Unique salt
        iterations  # Number of iterations
    )

    # Compare the computed hash with the stored hash
    return computed_hash.hex() == stored_hash

def check_login_attempts(failed_attempts: int) -> bool:
    """
    Checks if the number of failed login attempts exceeds the limit.

    :param failed_attempts: The current number of failed login attempts.
    :return: True if the user should be locked, False otherwise.
    """
    login_attempts_limit = int(config("LOGIN_ATTEMPTS_LIMIT", default=5))
    return failed_attempts >= login_attempts_limit

def update_password_history(user_id: str, new_password: str, db_session: Session) -> None:
    """
    Updates the password history for a user in the database.

    :param user_id: The ID of the user to update.
    :param new_password: The new password to be hashed and added to the history.
    :param db_session: The active database session to commit changes.
    """
    # Load user from database
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # Hash the new password
    salt, hashed_password = hash_password(new_password)

    # Add new password to history
    password_history = user.password_history if user.password_history else []
    password_history.append({"salt": salt, "hashed_password": hashed_password})

    # Enforce password history limit
    password_history_limit = int(config("PASSWORD_HISTORY_LIMIT", default=3))
    if len(password_history) > password_history_limit:
        password_history.pop(0)  # Remove the oldest password

    # Update user password and history
    user.salt = salt
    user.hashed_password = hashed_password
    user.password_history = password_history

    # Commit changes to the database
    db_session.commit()
