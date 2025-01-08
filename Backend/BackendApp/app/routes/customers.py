from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from ..models.tables import Customer, Package
from ..models.database import get_db
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import sanitize_input, prevent_sql_injection

router = APIRouter()

# Models for request validation
class CustomerCreate(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    phone_number: str
    email_address: EmailStr
    address: str
    package_id: str
    gender: str  # Added gender field

class CustomerUpdate(BaseModel):
    user_id: str
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    email_address: EmailStr = None
    address: str = None
    package_id: str = None
    gender: str = None  # Added gender field

class UserRequest(BaseModel):
    user_id: str

@router.get("/")
def get_customers(request: UserRequest, db: Session = Depends(get_db)):
    """
    Fetch all customers from the database.
    :param request: UserRequest containing the user ID.
    :param db: Database session.
    :return: List of all customers.
    """
    sanitized_user_id = sanitize_input(request.user_id)  # Protects against XSS
    logger.info(f"Fetching all customers by user {sanitized_user_id}.")
    customers = db.query(Customer).all()
    create_audit_log_entry(user_id=sanitized_user_id, action="Fetched all customers", db=db)
    logger.debug(f"Fetched {len(customers)} customers.")
    return customers

@router.get("/{customer_id}")
def get_customer(customer_id: str, request: UserRequest, db: Session = Depends(get_db)):
    """
    Fetch a specific customer by their ID.
    :param customer_id: The ID of the customer to fetch.
    :param request: UserRequest containing the user ID.
    :param db: Database session.
    :return: Customer details.
    """
    sanitized_customer_id = prevent_sql_injection(customer_id)  # Prevents SQL Injection
    sanitized_user_id = sanitize_input(request.user_id)  # Protects against XSS
    logger.info(f"Fetching customer with ID: {sanitized_customer_id} by user {sanitized_user_id}.")
    customer = db.query(Customer).filter(Customer.id == sanitized_customer_id).first()
    if not customer:
        logger.warning(f"Customer with ID {sanitized_customer_id} not found.")
        raise HTTPException(status_code=404, detail="Customer not found")
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Fetched customer {sanitized_customer_id}", db=db)
    logger.debug(f"Fetched customer details: {customer}")
    return customer

@router.post("/")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer in the database.
    :param customer: Details of the customer to create, including user ID.
    :param db: Database session.
    :return: Details of the created customer.
    """
    sanitized_user_id = sanitize_input(customer.user_id)  # Protects against XSS
    sanitized_first_name = sanitize_input(customer.first_name)  # Protects against XSS
    sanitized_last_name = sanitize_input(customer.last_name)  # Protects against XSS
    sanitized_phone_number = sanitize_input(customer.phone_number)  # Protects against XSS
    sanitized_email_address = sanitize_input(customer.email_address)  # Protects against XSS
    sanitized_address = sanitize_input(customer.address)  # Protects against XSS
    sanitized_package_id = prevent_sql_injection(customer.package_id)  # Prevents SQL Injection
    sanitized_gender = sanitize_input(customer.gender)  # Protects against XSS

    logger.info(f"Creating a new customer: {sanitized_first_name} {sanitized_last_name} by user {sanitized_user_id}.")
    package = db.query(Package).filter(Package.id == sanitized_package_id).first()
    if not package:
        logger.warning(f"Package with ID {sanitized_package_id} not found.")
        raise HTTPException(status_code=404, detail="Package not found")

    new_customer = Customer(
        first_name=sanitized_first_name,
        last_name=sanitized_last_name,
        phone_number=sanitized_phone_number,
        email_address=sanitized_email_address,
        address=sanitized_address,
        package_id=sanitized_package_id,
        gender=sanitized_gender
    )
    db.add(new_customer)

    # Increment subscriber count for the package
    package.subscriber_count += 1

    db.commit()
    db.refresh(new_customer)
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Created customer {new_customer.id}", db=db)
    logger.info(f"Customer created successfully with ID: {new_customer.id}")
    return new_customer

@router.put("/{customer_id}")
def update_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Update an existing customer's details in the database.
    :param customer_id: The ID of the customer to update.
    :param customer: Updated details for the customer, including user ID.
    :param db: Database session.
    :return: Updated customer details.
    """
    sanitized_customer_id = prevent_sql_injection(customer_id)  # Prevents SQL Injection
    sanitized_user_id = sanitize_input(customer.user_id)  # Protects against XSS
    logger.info(f"Updating customer with ID: {sanitized_customer_id} by user {sanitized_user_id}.")
    db_customer = db.query(Customer).filter(Customer.id == sanitized_customer_id).first()
    if not db_customer:
        logger.warning(f"Customer with ID {sanitized_customer_id} not found.")
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer.package_id and customer.package_id != db_customer.package_id:
        # Handle package subscriber count updates
        old_package = db.query(Package).filter(Package.id == db_customer.package_id).first()
        new_package = db.query(Package).filter(Package.id == customer.package_id).first()

        if not new_package:
            logger.warning(f"New package with ID {customer.package_id} not found.")
            raise HTTPException(status_code=404, detail="New package not found")

        if old_package:
            old_package.subscriber_count -= 1

        new_package.subscriber_count += 1
        db_customer.package_id = prevent_sql_injection(customer.package_id)  # Prevents SQL Injection

    if customer.first_name:
        db_customer.first_name = sanitize_input(customer.first_name)  # Protects against XSS
    if customer.last_name:
        db_customer.last_name = sanitize_input(customer.last_name)  # Protects against XSS
    if customer.phone_number:
        db_customer.phone_number = sanitize_input(customer.phone_number)  # Protects against XSS
    if customer.email_address:
        db_customer.email_address = sanitize_input(customer.email_address)  # Protects against XSS
    if customer.address:
        db_customer.address = sanitize_input(customer.address)  # Protects against XSS
    if customer.gender:
        db_customer.gender = sanitize_input(customer.gender)  # Protects against XSS

    db.commit()
    db.refresh(db_customer)
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Updated customer {sanitized_customer_id}", db=db)
    logger.info(f"Customer with ID {sanitized_customer_id} updated successfully.")
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: str, request: UserRequest, db: Session = Depends(get_db)):
    """
    Delete a customer from the database.
    :param customer_id: The ID of the customer to delete.
    :param request: UserRequest containing the user ID.
    :param db: Database session.
    :return: Confirmation of deletion.
    """
    sanitized_customer_id = prevent_sql_injection(customer_id)  # Prevents SQL Injection
    sanitized_user_id = sanitize_input(request.user_id)  # Protects against XSS

    logger.info(f"Deleting customer with ID: {sanitized_customer_id} by user {sanitized_user_id}.")
    db_customer = db.query(Customer).filter(Customer.id == sanitized_customer_id).first()
    if not db_customer:
        logger.warning(f"Customer with ID {sanitized_customer_id} not found.")
        raise HTTPException(status_code=404, detail="Customer not found")

    # Handle package subscriber count updates
    if db_customer.package_id:
        package = db.query(Package).filter(Package.id == db_customer.package_id).first()
        if package:
            package.subscriber_count -= 1

    db.delete(db_customer)
    db.commit()
    create_audit_log_entry(user_id=sanitized_user_id, action=f"Deleted customer {sanitized_customer_id}", db=db)
    logger.info(f"Customer with ID {sanitized_customer_id} deleted successfully.")
    return {"detail": "Customer deleted successfully"}
