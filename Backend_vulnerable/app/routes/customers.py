from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from ..models.database import get_db_connection
from ..utils.loguru_config import logger

# Title: Customer Management Routes

router = APIRouter()

# Title: Models

class CustomerCreate(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    phone_number: str
    email_address: EmailStr
    address: str
    package_id: str
    gender: str

class CustomerUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    email_address: EmailStr = None
    address: str = None
    package_id: str = None
    gender: str = None

# Title: Customer Endpoints

@router.get("/")
def get_customers(db: Session = Depends(get_db_connection)):
    """
    Fetch all customers.

    Security Consideration:
    - Uses raw SQL queries without sanitization.
    """
    logger.info("Fetching all customers.")
    try:
        query = "SELECT * FROM customers"
        result = db.execute(query).fetchall()
        return result

    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db_connection)):
    """
    Fetch a single customer by ID.

    Security Consideration:
    - Uses raw SQL queries without sanitization, vulnerable to SQL Injection.
    """
    logger.info(f"Fetching customer with ID: {customer_id}")
    try:
        query = f"SELECT * FROM customers WHERE id='{customer_id}'"
        result = db.execute(query).fetchone()

        if not result:
            logger.warning(f"Customer with ID {customer_id} not found.")
            raise HTTPException(status_code=404, detail="Customer not found")

        return result

    except Exception as e:
        logger.error(f"Error fetching customer: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db_connection)):
    """
    Create a new customer.

    Security Consideration:
    - Raw SQL query with direct user input, allowing SQL Injection.
    """
    logger.info(f"Creating customer for user: {customer.user_id}")
    try:
        query = f"""
        INSERT INTO customers (id, first_name, last_name, phone_number, email_address, address, package_id, gender)
        VALUES ('{generate_customer_id(db)}', '{customer.first_name}', '{customer.last_name}', '{customer.phone_number}',
                '{customer.email_address}', '{customer.address}', '{customer.package_id}', '{customer.gender}')
        """
        db.execute(query)
        db.commit()

        return {"status": "success", "message": "Customer created successfully"}

    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/update_customer/{customer_id}")
def update_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db_connection)):
    """
    Update an existing customer.

    Security Consideration:
    - Allows SQL Injection via raw queries with unsanitized inputs.
    """
    logger.info(f"Updating customer with ID: {customer_id}")
    try:
        if customer.first_name:
            query = f"UPDATE customers SET first_name='{customer.first_name}' WHERE id='{customer_id}'"
            db.execute(query)

        if customer.last_name:
            query = f"UPDATE customers SET last_name='{customer.last_name}' WHERE id='{customer_id}'"
            db.execute(query)

        if customer.phone_number:
            query = f"UPDATE customers SET phone_number='{customer.phone_number}' WHERE id='{customer_id}'"
            db.execute(query)

        if customer.email_address:
            query = f"UPDATE customers SET email_address='{customer.email_address}' WHERE id='{customer_id}'"
            db.execute(query)

        if customer.address:
            query = f"UPDATE customers SET address='{customer.address}' WHERE id='{customer_id}'"
            db.execute(query)

        if customer.package_id:
            query = f"UPDATE customers SET package_id='{customer.package_id}' WHERE id='{customer_id}'"
            db.execute(query)

        if customer.gender:
            query = f"UPDATE customers SET gender='{customer.gender}' WHERE id='{customer_id}'"
            db.execute(query)

        db.commit()
        return {"status": "success", "message": "Customer updated successfully"}

    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/delete_customer/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db_connection)):
    """
    Delete a customer.

    Security Consideration:
    - Raw SQL query with direct user input, allowing SQL Injection.
    """
    logger.info(f"Deleting customer with ID: {customer_id}")
    try:
        query = f"DELETE FROM customers WHERE id='{customer_id}'"
        db.execute(query)
        db.commit()

        return {"status": "success", "message": "Customer deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting customer: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

def generate_customer_id(db: Session) -> str:
    """
    Generate a unique customer ID in the format 'cust-<number>'.

    Security Consideration:
    - Uses raw SQL queries without sanitization.
    - No checks to prevent duplicate or invalid IDs.
    """
    logger.info("Generating customer ID.")

    try:
        query = "SELECT COUNT(*) FROM customers"
        result = db.execute(query).fetchone()

        customer_count = result[0] if result else 0
        new_id = f"cust-{customer_count + 1}"
        logger.debug(f"Generated customer ID: {new_id}")

        return new_id

    except Exception as e:
        logger.error(f"Error generating customer ID: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate customer ID")
