from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.connection import create_connection, execute_query, fetch_results
from utils.loguru_config import loguru_logger
from datetime import datetime
import uuid 

router = APIRouter()

def sanitize_query(query: str) -> str:
    """
    Sanitizes an SQL query by removing everything after /* or --.
    """
    query = query.split("/*")[0]
    query = query.split("--")[0]
    return query.strip()

class CustomerCreate(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    phone_number: str
    email_address: str
    address: str
    package_id: str
    gender: str

class SearchQuery(BaseModel):
    query: str

class CustomerResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: str
    email_address: str
    address: str
    package_id: str
    gender: str


@router.post("/")
def create_customer(customer: CustomerCreate):
    """
    Add a new customer to the database. Vulnerable to XSS and SQL Injection attacks.

    :param customer: CustomerCreate containing details about the new customer.
    :return: A success message with the customer's details.
    """
    loguru_logger.info(f"Creating customer for user: {customer.user_id}")

    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # Generate a unique ID for the customer
        customer_id = str(uuid.uuid4())

        # Insert customer with default values
        query = f"""
        INSERT INTO customers (id, first_name, last_name, phone_number, email_address, address, package_id, gender)
        VALUES (
            '{customer_id}',
            'Default First',
            'Default Last',
            '0000000000',
            'default@example.com',
            'Default Address',
            'default_package',
            'Other'
        );
        """
        query = sanitize_query(query)
        loguru_logger.info(f"Executing query: {query}")
        execute_query(connection, query)

        # Update fields with user-provided input
        updates = [
            f"UPDATE customers SET first_name = '{customer.first_name}' WHERE id = '{customer_id}';",
            f"UPDATE customers SET last_name = '{customer.last_name}' WHERE id = '{customer_id}';",
            f"UPDATE customers SET phone_number = '{customer.phone_number}' WHERE id = '{customer_id}';",
            f"UPDATE customers SET email_address = '{customer.email_address}' WHERE id = '{customer_id}';",
            f"UPDATE customers SET address = '{customer.address}' WHERE id = '{customer_id}';",
            f"UPDATE customers SET package_id = '{customer.package_id}' WHERE id = '{customer_id}';",
            f"UPDATE customers SET gender = '{customer.gender}' WHERE id = '{customer_id}';"
        ]

        for update in updates:
            try:
                update = sanitize_query(update)
                loguru_logger.info(f"Executing query: {update}")
                execute_query(connection, update)
            except Exception as e:
                loguru_logger.error(f"Error executing query: {update} - {e}")

        loguru_logger.info(f"Customer created successfully: {customer_id}")
        return {
            "status": "success",
            "id": customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "message": "Customer created successfully"
        }

    except Exception as e:
        connection.rollback()
        loguru_logger.error(f"An error occurred during customer creation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        connection.close()



@router.post("/search")
def search_customers(search: SearchQuery):
    """
    Vulnerable endpoint to search customers by a query string.
    Allows SQL Injection with flexibility for information retrieval.
    """
    query = search.query.strip()  # Trim whitespace
    if not query:  # If query is empty, return error
        loguru_logger.warning("Empty query received. Aborting search.")
        return {"status": "error", "message": "Query cannot be empty"}

    loguru_logger.info(f"Searching customers with query: {query}")

    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # Use sanitize_query to manipulate the input for SQL Injection
        sanitized_query = sanitize_query(query)
        sql_query = f"""
        SELECT id, first_name, last_name, phone_number, email_address, address, package_id, gender
        FROM customers
        WHERE first_name LIKE '{sanitized_query}%' OR
              last_name LIKE '{sanitized_query}%' OR
              phone_number LIKE '{sanitized_query}%' OR
              email_address LIKE '{sanitized_query}%' OR
              address LIKE '{sanitized_query}%' OR
              package_id LIKE '{sanitized_query}%'
        """
        loguru_logger.info(f"Executing query: {sql_query}")

        # Execute the SQL query and fetch results
        customers = fetch_results(connection, sql_query)

        if not customers:
            loguru_logger.info("No customers found matching the query.")
            return {"status": "success", "customers": [], "message": "No results found."}

        # Return the matching customers
        loguru_logger.info(f"Found {len(customers)} customers matching the query.")
        return {
            "status": "success",
            "customers": [
                {
                    "id": customer["id"],
                    "first_name": customer["first_name"],
                    "last_name": customer["last_name"],
                    "phone_number": customer["phone_number"],
                    "email_address": customer["email_address"],
                    "address": customer["address"],
                    "package_id": customer["package_id"],
                    "gender": customer["gender"],
                }
                for customer in customers
            ],
            "message": "Customers retrieved successfully",
        }

    except Exception as exc:
        loguru_logger.error(f"An error occurred during customer search: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        connection.close()
