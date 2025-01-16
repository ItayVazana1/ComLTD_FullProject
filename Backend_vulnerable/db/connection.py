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
            port=DB_PORT,  # Adding port here
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            loguru_logger.info("Connection to MySQL DB created successfully!")
            return connection
    except Error as e:
        loguru_logger.info(f"Connection to MySQL DB failed , ERROR --> {e}")
        return None


def execute_query(connection, query):
    """
    Executes a given SQL query on the database.
    This function is vulnerable to SQL Injection as it does not use parameterized queries.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)  # Directly executing the query without sanitization
        connection.commit()
        loguru_logger.info("Query executed successfully!")
    except Error as e:
        loguru_logger.info(f"Error executing query: {e}")


def fetch_results(connection, query):
    """
    Executes a SELECT query and fetches the results.
    This function is vulnerable to SQL Injection as it directly executes the query.
    """
    try:
        loguru_logger.info("Trying to fetching data from DB...")
        cursor = connection.cursor()
        cursor.execute(query)  # Directly executing the query without sanitization
        results = cursor.fetchall()
        loguru_logger.info("fetching data from DB - success! ")
        return results
    except Error as e:
        loguru_logger.warning(f"fetching data from DB - failed! ---- ERROR --> {e}")
        return []


# Example usage (uncomment to test locally):
# conn = create_connection()
# if conn:
#     execute_query(conn, "SELECT * FROM users")  # Replace with your query
#     conn.close()
