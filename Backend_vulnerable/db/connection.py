import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from utils.loguru_config import loguru_logger
import os

# Load environment variables
load_dotenv()

# Database configuration from .env file
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))  # Default MySQL port
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "vulnerable_db")


def create_connection():
    """
    Creates a connection to the MySQL database.
    Returns the connection object if successful, otherwise None.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            loguru_logger.info("Connection to MySQL DB created successfully!")
            return connection
    except Error as e:
        loguru_logger.info(f"Connection to MySQL DB failed, ERROR --> {e}")
        return None


def execute_query(connection, query):
    """
    Executes a given SQL query on the database.
    Supports multi statements for SQL Injection scenarios.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        loguru_logger.info(f"Executing query: {query}")
        results = []
        for result in cursor.execute(query, multi=True):  # Enable multi statements
            if result.with_rows:
                results.extend(result.fetchall())  # Collect all rows
        connection.commit()
        loguru_logger.info("Query executed successfully!")
        return results
    except mysql.connector.Error as e:
        loguru_logger.error(f"Error executing query: {e}")
        connection.rollback()
        raise


def fetch_results(connection, query):
    """
    Executes a SELECT query and fetches the results.
    This function supports multi statements for SELECT queries.
    """
    try:
        loguru_logger.info("Fetching data from DB...")
        results = execute_query(connection, query)  # Use execute_query for consistency
        loguru_logger.info("Fetching data from DB - success!")
        return results
    except Error as e:
        loguru_logger.warning(f"Fetching data from DB - failed! ---- ERROR --> {e}")
        return []
