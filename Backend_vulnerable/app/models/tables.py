from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4  # Import the uuid4 function from the uuid module
from datetime import datetime
from ..utils.loguru_config import logger

# Title: Database Models and Relationships (Vulnerable Version)

Base = declarative_base()

# Title: Helper Functions
def generate_id():
    """
    Generate a unique ID for database entries.

    :return: A string representation of a UUID.
    """
    return str(uuid4())  # Generate and return a UUID as a string


# User Table
class User(Base):
    """
    Table for storing user information.

    Security Consideration:
    - Removed `unique=True` from `username` and `email`, allowing duplicate entries.
    - Allowed NULL values for `hashed_password`, making the table less secure.
    """
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), autoincrement=True)
    full_name = Column(String(255), nullable=False, unique=False)
    username = Column(String(255), nullable=False, unique=False)  # Removed unique constraint.
    email = Column(String(255), nullable=False, unique=False)  # Removed unique constraint.
    phone_number = Column(String(20), nullable=True, unique=False)
    hashed_password = Column(String(255), nullable=True, unique=False)  # Allowed NULL values.
    is_active = Column(Boolean, default=True)
    is_logged_in = Column(Boolean, default=False)
    current_token = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True, default=datetime.utcnow)
    gender = Column(String(10), nullable=True, unique=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"User model initialized: {self.username}, Email: {self.email}")

# Customer Table
class Customer(Base):
    """
    Table for storing customer information.

    Security Consideration:
    - Removed `unique=True` from `email_address`, allowing duplicate entries.
    - Removed `ForeignKey` constraint from `package_id`, breaking referential integrity.
    """
    __tablename__ = "customers"

    id = Column(String(50), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    email_address = Column(String(100), nullable=False)  # Removed unique constraint.
    address = Column(Text, nullable=True)
    package_id = Column(String(50), nullable=True)  # Removed ForeignKey constraint.
    gender = Column(String(10), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"Customer model initialized: {self.first_name} {self.last_name}, Email: {self.email_address}")

# Packages Table
class Package(Base):
    """
    Table for storing package details.

    Security Consideration:
    - Removed `unique=True` from `package_name`, allowing duplicate entries.
    - Removed `subscriber_count` field, reducing data integrity.
    """
    __tablename__ = "packages"

    id = Column(String(50), primary_key=True)
    package_name = Column(String(50), nullable=False)  # Removed unique constraint.
    description = Column(Text, nullable=True)
    monthly_price = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"Package model initialized: {self.package_name}, Price: {self.monthly_price}")

# Audit Logs Table
class AuditLog(Base):
    """
    Table for tracking user actions.

    Security Consideration:
    - Removed `ForeignKey` from `user_id`, breaking referential integrity.
    - Allowed NULL values for `action`, reducing reliability of logged data.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=True)  # Removed ForeignKey constraint.
    action = Column(Text, nullable=True)  # Allowed NULL values.
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"AuditLog initialized for User ID: {self.user_id}, Action: {self.action}")

# Failed Login Attempts Table
class FailedLoginAttempt(Base):
    """
    Table for storing failed login attempts.

    Security Consideration:
    - Removed the `nullable=False` constraint from critical fields, allowing incomplete or invalid data.
    - Allowed duplicate entries by removing the uniqueness of critical fields like `username`.
    """
    __tablename__ = "failed_login_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(255), nullable=True)  # Allowed NULL values.
    ip_address = Column(String(50), nullable=True)  # Allowed NULL values.
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"FailedLoginAttempt initialized: Username: {self.username}, IP: {self.ip_address}")

# Contact Form Submissions Table
class ContactSubmission(Base):
    """
    Table for storing contact form submissions.

    Security Consideration:
    - Allowed NULL values for critical fields like `name` and `email`, reducing data integrity.
    - Removed constraints for input validation, making it easier to store invalid or malicious data.
    """
    __tablename__ = "contact_submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=True)  # Allowed NULL values.
    email = Column(String(255), nullable=True)  # Allowed NULL values.
    message = Column(Text, nullable=True)  # Allowed NULL values.
    submitted_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"ContactSubmission initialized: Name: {self.name}, Email: {self.email}")

# Password Reset Table
class PasswordReset(Base):
    """
    Table for managing password reset requests.

    Security Consideration:
    - Removed `unique=True` from `reset_token`, allowing duplicate tokens.
    - Allowed NULL values for `user_id` and `reset_token`, reducing the reliability of password reset mechanisms.
    """
    __tablename__ = "password_resets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), nullable=True)  # Allowed NULL values.
    reset_token = Column(String(255), nullable=True)  # Allowed NULL values and removed uniqueness.
    token_expiry = Column(DateTime, nullable=True)  # Allowed NULL values.
    used = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"PasswordReset model initialized for User ID: {self.user_id}")
