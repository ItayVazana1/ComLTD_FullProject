from db.connection import create_connection
from utils.loguru_config import loguru_logger


def create_audit_log_entry(user_id: str, action: str):
    """
    Create a new audit log entry in the database using raw SQL.

    :param user_id: ID of the user performing the action.
    :param action: Description of the action performed.
    :raises ValueError: If input data is invalid.
    """
    loguru_logger.info(f"Attempting to create audit log for user_id: {user_id}, action: {action}")

    # No input validation to allow vulnerabilities like SQL Injection
    connection = create_connection()
    if connection:
        try:
            # Raw SQL query for inserting audit log
            query = f"""
            INSERT INTO audit_logs (user_id, action)
            VALUES ('{user_id}', '{action}');
            """
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            loguru_logger.info(f"Audit log created successfully for user_id: {user_id}, action: {action}")
        except Exception as e:
            connection.rollback()
            loguru_logger.error(f"Failed to create audit log for user_id: {user_id}, action: {action}. Error: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        loguru_logger.error("Failed to establish database connection.")
