from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum as PyEnum
from ..utils.loguru_config import logger
from sqlalchemy.sql import func
from sqlalchemy.orm.session import Session

# Title: Database Models and Relationships

# Base for tables
def generate_package_id(session: Session):
    """
    Generate a unique package ID in the format 'pak-<number>'.

    :param session: SQLAlchemy session.
    :return: Generated package ID.
    """
    count = session.query(Package).count()
    return f"pak-{count + 1}"

Base = declarative_base()

# Title: Enumerations

# Enum for Gender
class Gender(PyEnum):
    """
    Enum for representing gender values.
    """
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

# Title: Database Tables

# User Table
class User(Base):
    """
    Table for storing user information.

    Attributes:
        id: Primary key, UUID.
        full_name: Full name of the user.
        username: Unique username.
        email: Unique email address.
        phone_number: User's phone number.
        hashed_password: Securely hashed password.
        is_active: Status of the user's account.
        is_logged_in: Indicates if the user is currently logged in.
        current_token: Active authentication token.
        last_login: Timestamp of the last login.
        gender: Gender of the user.
    """
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    full_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_logged_in = Column(Boolean, default=False)
    current_token = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True, default=datetime.utcnow)
    gender = Column(Enum(Gender), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"User model initialized: {self.username}, Email: {self.email}")

# Customer Table
class Customer(Base):
    """
    Table for storing customer information.

    Attributes:
        id: Primary key, unique customer ID.
        first_name: First name of the customer.
        last_name: Last name of the customer.
        phone_number: Contact number.
        email_address: Unique email address.
        address: Optional address details.
        package_id: Foreign key linking to a package.
        gender: Gender of the customer.
    """
    __tablename__ = "customers"

    id = Column(String(50), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    email_address = Column(String(100), nullable=False, unique=True)
    address = Column(Text, nullable=True)
    package_id = Column(String(50), ForeignKey("packages.id"), nullable=False)
    gender = Column(String(10), nullable=False)

    package = relationship("Package", back_populates="customers")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"Customer model initialized: {self.first_name} {self.last_name}, Email: {self.email_address}")

# Packages Table
class Package(Base):
    """
    Table for storing package details.

    Attributes:
        id: Primary key, unique package ID.
        package_name: Name of the package.
        description: Optional package description.
        monthly_price: Price of the package per month.
        subscriber_count: Number of customers subscribed to the package.
    """
    __tablename__ = "packages"

    id = Column(String(50), primary_key=True)
    package_name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    monthly_price = Column(Integer, nullable=False)
    subscriber_count = Column(Integer, default=0)

    customers = relationship("Customer", back_populates="package")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"Package model initialized: {self.package_name}, Price: {self.monthly_price}")

# Audit Logs Table
class AuditLog(Base):
    """
    Table for tracking user actions.

    Attributes:
        id: Primary key, auto-incremented ID.
        user_id: Foreign key linking to the user.
        action: Description of the user action.
        timestamp: Timestamp of the action.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"AuditLog initialized for User ID: {self.user_id}, Action: {self.action}")

# Failed Login Attempts Table
class FailedLoginAttempt(Base):
    """
    Table for storing failed login attempts.

    Attributes:
        id: Primary key, UUID.
        username: Username used in the failed attempt.
        ip_address: IP address of the request.
        timestamp: Timestamp of the failed attempt.
    """
    __tablename__ = "failed_login_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    username = Column(String(255), nullable=False)
    ip_address = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"FailedLoginAttempt initialized: Username: {self.username}, IP: {self.ip_address}")

# Contact Form Submissions Table
class ContactSubmission(Base):
    """
    Table for storing contact form submissions.

    Attributes:
        id: Primary key, UUID.
        name: Name of the submitter.
        email: Email address of the submitter.
        message: Message content.
        submitted_at: Timestamp of submission.
    """
    __tablename__ = "contact_submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"ContactSubmission initialized: Name: {self.name}, Email: {self.email}")

# Password Reset Table
class PasswordReset(Base):
    """
    Table for managing password reset requests.

    Attributes:
        id: Primary key, UUID.
        user_id: Foreign key linking to the user.
        reset_token: Unique token for password reset.
        token_expiry: Expiry time of the token.
        used: Indicates if the token has been used.
    """
    __tablename__ = "password_resets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    reset_token = Column(String(255), nullable=False, unique=True)
    token_expiry = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    user = relationship("User", back_populates="password_resets")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"PasswordReset model initialized for User ID: {self.user_id}")

# Relationships

# Relationship on the User Table
User.audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
User.password_resets = relationship(
    "PasswordReset",
    order_by=PasswordReset.id,
    back_populates="user",
    cascade="all, delete-orphan"
)
