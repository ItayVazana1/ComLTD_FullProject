from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from ..models.tables import Customer, Package
from ..models.database import get_db
from ..utils.loguru_config import logger
from ..utils.audit_log import create_audit_log_entry
from ..utils.attack_detectors import contains_xss, sanitize_input, prevent_sql_injection

router = APIRouter()

# Models
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
    user_id: str
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    email_address: EmailStr = None
    address: str = None
    package_id: str = None
    gender: str = None

class UserRequest(BaseModel):
    user_id: str

class CustomerResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    email_address: str
    address: str
    package_id: str
    gender: str

    class Config:
        orm_mode = True
        
        
class CustomerResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    email_address: str
    address: Optional[str]
    package_id: str
    gender: str


class CustomerSearchResponse(BaseModel):
    status: str
    message: str
    customers: List[CustomerResponse]
    
    
class SearchQuery(BaseModel):
    query: str

# Helper Function

def generate_customer_id(session):
    count = session.query(Customer).count()
    return f"cust-{count + 1}"



def validate_input(customer: CustomerCreate) -> bool:
    input_fields = [
        customer.user_id,
        customer.first_name,
        customer.last_name,
        customer.phone_number,
        customer.email_address,
        customer.address,
        customer.package_id,
        customer.gender,
    ]

    for field_name, field_value in customer.__dict__.items():
        if contains_xss(field_value):
            logger.warning(f"XSS detected in field '{field_name}': {field_value}")
            return False
    return True


# Endpoints

@router.get("/", response_model=list[CustomerResponse])
def get_customers(request: UserRequest, db: Session = Depends(get_db)):
    logger.info(f"Fetching all customers for user: {request.user_id}")
    try:
        sanitized_user_id = sanitize_input(prevent_sql_injection(request.user_id))
        if sanitized_user_id != request.user_id:
            logger.warning("Potential XSS or SQL Injection detected in user_id.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        customers = db.query(Customer).all()
        if not customers:
            logger.warning(f"No customers found for user: {sanitized_user_id}")
            raise HTTPException(status_code=404, detail="No customers found.")

        create_audit_log_entry(user_id=sanitized_user_id, action="Fetched all customers", db=db)
        logger.debug(f"Fetched {len(customers)} customers for user: {sanitized_user_id}")
        return customers

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching customers for user {sanitized_user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, request: UserRequest, db: Session = Depends(get_db)):
    logger.info(f"Fetching customer with ID: {customer_id}")
    try:
        sanitized_customer_id = sanitize_input(prevent_sql_injection(customer_id))
        sanitized_user_id = sanitize_input(prevent_sql_injection(request.user_id))

        if sanitized_customer_id != customer_id or sanitized_user_id != request.user_id:
            logger.warning("Potential XSS or SQL Injection detected in request.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        customer = db.query(Customer).filter(Customer.id == sanitized_customer_id).first()
        if not customer:
            logger.warning(f"Customer not found: {sanitized_customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found.")

        create_audit_log_entry(user_id=sanitized_user_id, action=f"Fetched customer {sanitized_customer_id}", db=db)
        logger.info(f"Customer fetched successfully: {sanitized_customer_id}")
        return customer

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching customer {customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating customer for user: {customer.user_id}")
    
    try:
        # Validate input for XSS and SQL Injection immediately
        if not validate_input(customer):
            logger.warning("Potential XSS or SQL Injection detected in customer creation.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        # Sanitize inputs and detect SQL Injection during sanitization
        sanitized_user_id = prevent_sql_injection(customer.user_id)
        sanitized_first_name = prevent_sql_injection(customer.first_name)
        sanitized_last_name = prevent_sql_injection(customer.last_name)
        sanitized_phone_number = prevent_sql_injection(customer.phone_number)
        sanitized_email_address = prevent_sql_injection(customer.email_address)
        sanitized_address = prevent_sql_injection(customer.address)
        sanitized_package_id = prevent_sql_injection(customer.package_id)
        sanitized_gender = prevent_sql_injection(customer.gender)

        # If any sanitization modified the input, raise an error
        if (
            sanitized_user_id != customer.user_id or
            sanitized_first_name != customer.first_name or
            sanitized_last_name != customer.last_name or
            sanitized_phone_number != customer.phone_number or
            sanitized_email_address != customer.email_address or
            sanitized_address != customer.address or
            sanitized_package_id != customer.package_id or
            sanitized_gender != customer.gender
        ):
            logger.warning("Potential SQL Injection detected after sanitization.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        # Check if package exists
        package = db.query(Package).filter(Package.id == sanitized_package_id).first()
        if not package:
            logger.warning(f"Package not found: {sanitized_package_id}")
            raise HTTPException(status_code=404, detail="Package not found.")

        # Generate new customer ID
        new_customer_id = generate_customer_id(db)

        # Create new customer entry
        new_customer = Customer(
            id=new_customer_id,
            first_name=sanitized_first_name,
            last_name=sanitized_last_name,
            phone_number=sanitized_phone_number,
            email_address=sanitized_email_address,
            address=sanitized_address,
            package_id=sanitized_package_id,
            gender=sanitized_gender
        )
        db.add(new_customer)

        # Update package subscriber count
        package.subscriber_count += 1

        # Commit changes
        db.commit()
        db.refresh(new_customer)

        # Create audit log entry
        create_audit_log_entry(user_id=sanitized_user_id, action=f"Created customer {new_customer_id}", db=db)
        logger.info(f"Customer created successfully: {new_customer_id}")

        # Return detailed response
        return {
            "status": "success",
            "id": new_customer.id,
            "first_name": new_customer.first_name,
            "last_name": new_customer.last_name,
            "package_id": new_customer.package_id,
            "message": "Customer created successfully"
        }

    except HTTPException as http_exc:
        raise http_exc  # Raise any HTTP exceptions immediately

    except Exception as exc:
        db.rollback()
        logger.error(f"An error occurred during customer creation: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/update_customer/{customer_id}")
def update_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating customer with ID: {customer_id}")
    try:
        sanitized_customer_id = sanitize_input(prevent_sql_injection(customer_id))
        sanitized_user_id = sanitize_input(prevent_sql_injection(customer.user_id))

        if sanitized_customer_id != customer_id or sanitized_user_id != customer.user_id:
            logger.warning("Potential XSS or SQL Injection detected in update request.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        db_customer = db.query(Customer).filter(Customer.id == sanitized_customer_id).first()
        if not db_customer:
            logger.warning(f"Customer not found: {sanitized_customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found.")

        if customer.package_id and customer.package_id != db_customer.package_id:
            old_package = db.query(Package).filter(Package.id == db_customer.package_id).first()
            new_package = db.query(Package).filter(Package.id == customer.package_id).first()

            if not new_package:
                logger.warning(f"New package not found: {customer.package_id}")
                raise HTTPException(status_code=404, detail="New package not found.")

            if old_package:
                old_package.subscriber_count -= 1

            new_package.subscriber_count += 1

        if customer.first_name:
            db_customer.first_name = sanitize_input(customer.first_name)
        if customer.last_name:
            db_customer.last_name = sanitize_input(customer.last_name)
        if customer.phone_number:
            db_customer.phone_number = sanitize_input(customer.phone_number)
        if customer.email_address:
            db_customer.email_address = sanitize_input(customer.email_address)
        if customer.address:
            db_customer.address = sanitize_input(customer.address)
        if customer.gender:
            db_customer.gender = sanitize_input(customer.gender)

        db.commit()
        db.refresh(db_customer)

        create_audit_log_entry(user_id=sanitized_user_id, action=f"Updated customer {sanitized_customer_id}", db=db)
        logger.info(f"Customer updated successfully: {sanitized_customer_id}")
        return {"status": "success", "id": db_customer.id, "message": "Customer updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error updating customer {customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/delete_customer/{customer_id}")
def delete_customer(customer_id: str, request: UserRequest, db: Session = Depends(get_db)):
    logger.info(f"Deleting customer with ID: {customer_id}")
    try:
        sanitized_customer_id = sanitize_input(prevent_sql_injection(customer_id))
        sanitized_user_id = sanitize_input(prevent_sql_injection(request.user_id))

        if sanitized_customer_id != customer_id or sanitized_user_id != request.user_id:
            logger.warning("Potential XSS or SQL Injection detected in delete request.")
            raise HTTPException(status_code=400, detail="Invalid input detected.")

        db_customer = db.query(Customer).filter(Customer.id == sanitized_customer_id).first()
        if not db_customer:
            logger.warning(f"Customer not found: {sanitized_customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found.")

        if db_customer.package_id:
            package = db.query(Package).filter(Package.id == db_customer.package_id).first()
            if package:
                package.subscriber_count -= 1

        db.delete(db_customer)
        db.commit()

        create_audit_log_entry(user_id=sanitized_user_id, action=f"Deleted customer {sanitized_customer_id}", db=db)
        logger.info(f"Customer deleted successfully: {sanitized_customer_id}")
        return {"status": "success", "message": "Customer deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error deleting customer {customer_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/search", response_model=CustomerSearchResponse)
def search_customers(search: SearchQuery, db: Session = Depends(get_db)):
    """
    Endpoint to search customers by a query string sent in the request body.
    """
    query = search.query
    logger.info(f"Searching customers with query: {query}")

    try:
        # Check if the query is empty
        if not query.strip():
            logger.info("Empty query string received. Returning no results.")
            return {"status": "success", "customers": [], "message": "No results found."}

        # Validate and sanitize the query input
        sanitized_query = prevent_sql_injection(query)

        # Query the database for matching customers
        customers = db.query(Customer).filter(
            (Customer.first_name.ilike(f"{sanitized_query}%")) |
            (Customer.last_name.ilike(f"{sanitized_query}%")) |
            (Customer.phone_number.ilike(f"{sanitized_query}%")) |
            (Customer.email_address.ilike(f"{sanitized_query}%")) |
            (Customer.address.ilike(f"{sanitized_query}%")) |
            (Customer.package_id.ilike(f"{sanitized_query}%"))
        ).all()

        if not customers:
            logger.info("No customers found matching the query.")
            return {"status": "success", "customers": [], "message": "No results found."}

        # Return the matching customers
        logger.info(f"Found {len(customers)} customers matching the query.")
        return {
            "status": "success",
            "customers": [
                CustomerResponse(
                    id=customer.id,
                    first_name=customer.first_name,
                    last_name=customer.last_name,
                    phone_number=customer.phone_number,
                    email_address=customer.email_address,
                    address=customer.address,
                    package_id=customer.package_id,
                    gender=customer.gender,
                )
                for customer in customers
            ],
            "message": "Customers retrieved successfully",
        }

    except Exception as exc:
        logger.error(f"An error occurred during customer search: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")
