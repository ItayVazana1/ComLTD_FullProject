from db.connection import execute_query, create_connection
from utils.loguru_config import loguru_logger
def create_tables():
    """
    Creates all necessary tables for the application.
    This implementation uses raw SQL queries, making it vulnerable to SQL Injection.
    """
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone_number VARCHAR(20),
            hashed_password VARCHAR(255) NOT NULL,
            salt VARCHAR(255) NOT NULL,
            password_history TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            is_logged_in BOOLEAN DEFAULT FALSE,
            current_token VARCHAR(255),
            last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
            gender VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS customers (
            id VARCHAR(50) PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone_number VARCHAR(15) NOT NULL,
            email_address VARCHAR(100) UNIQUE NOT NULL,
            address TEXT,
            package_id VARCHAR(50),
            gender VARCHAR(10)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS packages (
            id VARCHAR(50) PRIMARY KEY,
            package_name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            monthly_price INT NOT NULL,
            subscriber_count INT DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS password_resets (
            id VARCHAR(36) PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            reset_token VARCHAR(255) UNIQUE NOT NULL,
            token_expiry DATETIME NOT NULL,
            used BOOLEAN DEFAULT FALSE
        );
        """
    ]

    db_connection = create_connection()
    if db_connection:
        try:
            for query in queries:
                # Ensure query execution
                cursor = db_connection.cursor()
                cursor.execute(query)
                db_connection.commit()
                loguru_logger.info("Table Created successfully!")
        except Exception as e:
            loguru_logger.error(f"Table Creation failed! ERROR --> {e}")
        finally:
            loguru_logger.info("Closing the DB connection..")
            db_connection.close()


# Uncomment the following line to create tables when running the script
# if __name__ == "__main__":
#     create_tables()
