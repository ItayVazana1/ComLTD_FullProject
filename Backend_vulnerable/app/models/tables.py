from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.orm.session import Session

# Base for tables
Base = declarative_base()

def generate_package_id(session: Session):
    """
    Generate a unique package ID in the format 'pak-<number>'.

    :param session: SQLAlchemy session.
    :return: Generated package ID.
    """
    count = session.query(Package).count()
    return f"pak-{count + 1}"

# Enum for Gender
class Gender(PyEnum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    full_name = Column(String(255), nullable=True)
    username = Column(String(150), unique=True, nullable=True)
    email = Column(String(150), unique=True, nullable=True)
    phone_number = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    salt = Column(String(255), nullable=True)
    password_history = Column(Text, nullable=True)
    failed_attempts = Column(Integer, default=0, nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    is_logged_in = Column(Boolean, default=False, nullable=True)
    current_token = Column(String(255), nullable=True)
    last_login = Column(DateTime, nullable=True, default=datetime.utcnow)
    gender = Column(String(255), nullable=True)

    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")

# Customer Table
class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(50), primary_key=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(15), nullable=True)
    email_address = Column(String(150), unique=True, nullable=True)
    address = Column(Text, nullable=True)
    package_id = Column(String(50), ForeignKey("packages.id"), nullable=True)
    gender = Column(String(255), nullable=True)

    package = relationship("Package", back_populates="customers")

# Packages Table
class Package(Base):
    __tablename__ = "packages"

    id = Column(String(50), primary_key=True)
    package_name = Column(String(100), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    monthly_price = Column(Integer, nullable=True)
    subscriber_count = Column(Integer, default=0, nullable=True)

    customers = relationship("Customer", back_populates="package")

# Audit Logs Table
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=True)

    user = relationship("User", back_populates="audit_logs")

# Contact Submissions Table
class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=True)
    email = Column(String(150), nullable=True)
    message = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=True)

# Password Reset Table
class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    reset_token = Column(String(255), unique=True, nullable=True)
    token_expiry = Column(DateTime, nullable=True)
    used = Column(Boolean, default=False, nullable=True)

    user = relationship("User", back_populates="password_resets")

# Relationships

# Relationship on the User Table
User.audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
User.password_resets = relationship(
    "PasswordReset",
    order_by=PasswordReset.id,
    back_populates="user",
    cascade="all, delete-orphan"
)