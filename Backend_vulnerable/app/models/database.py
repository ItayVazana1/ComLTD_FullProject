import pymysql
import re
from uuid import uuid4
from decouple import config
from ..utils.loguru_config import logger

# Title: Database Connection and Query Execution (Vulnerable Version)

# Load configuration from .env
DATABASE_URL = config("DATABASE_URL")  # Connection details for MySQL database

class DatabaseConnection:
    """
    Wrapper class for pymysql connection to mimic SQLAlchemy-like interface.

    Security Consideration:
    - Provides raw SQL execution methods without sanitization, exposing the database to SQL Injection.
    """
    def __init__(self):
        try:
            # Initialize database connection
            self.connection = pymysql.connect(
                host=config("DB_HOST"),
                user=config("DB_USER"),
                password=config("DB_PASSWORD"),
                database=config("DB_NAME"),
                port=int(config("DB_PORT")),
            )
            logger.debug("Database connection initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise

    def cursor(self):
        """
        Provide a cursor object from the connection.
        """
        return self.connection.cursor()

    def execute(self, query, params=None):
        """
        Execute a raw SQL query.

        Automatically generates an ID if the query requires one but none is provided.

        Security Consideration:
        - Does not sanitize inputs, making it vulnerable to SQL Injection.
        """
        try:
            # Check if query is an INSERT and lacks an ID
            if "INSERT INTO" in query.upper() and "id" not in query.lower():
                generated_id = str(uuid4())
                query = re.sub(r"\(", f"(id, ", query, count=1)
                query = re.sub(r"VALUES\s*\(", f"VALUES ('{generated_id}', ", query, count=1)
                logger.debug(f"Generated ID '{generated_id}' added to query.")

            with self.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                logger.debug(f"Query executed successfully: {query}")
                return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    def commit(self):
        """
        Commit the current transaction.
        """
        try:
            self.connection.commit()
            logger.debug("Transaction committed successfully.")
        except Exception as e:
            logger.error(f"Error during commit: {e}")
            raise

    def rollback(self):
        """
        Rollback the current transaction.
        """
        try:
            self.connection.rollback()
            logger.debug("Transaction rolled back successfully.")
        except Exception as e:
            logger.error(f"Error during rollback: {e}")
            raise

    def close(self):
        """
        Close the database connection.
        """
        try:
            self.connection.close()
            logger.debug("Database connection closed.")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
            raise

def get_db_connection():
    """
    Returns an instance of DatabaseConnection to mimic SQLAlchemy's connection interface.

    Security Consideration:
    - Direct database connections without pooling can lead to performance issues.
    - No validation or sanitization is performed at this layer, making it vulnerable to SQL Injection if used improperly.

    :return: An instance of DatabaseConnection.
    """
    try:
        return DatabaseConnection()
    except Exception as e:
        logger.error(f"Failed to establish database connection: {e}")
        raise


def load_models():
    """
    Dynamically loads all database models.
    This ensures that all table schemas are recognized and can be created.
    """
    try:
        from .tables import (
            User,
            Customer,
            Package,
            AuditLog,
            FailedLoginAttempt,
            PasswordReset,
            ContactSubmission
        )
        logger.info("Models loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise
