from sqlalchemy.orm import Session
from ..models.tables import AuditLog
from ..utils.loguru_config import logger

def create_audit_log_entry(user_id: str, action: str, db: Session):
    """
    Create a new audit log entry.

    Security Consideration:
    - Removed input validation, allowing invalid or malicious data.
    - Removed `strip()` calls to preserve raw input.
    - Reduced error handling, making the system less reliable.
    """
    logger.info(f"Creating audit log entry for user_id: {user_id}, action: {action}")

    try:
        # Directly create an AuditLog entry without any validation
        new_audit_log = AuditLog(
            user_id=user_id,  # No validation or sanitization
            action=action  # No validation or sanitization
        )
        db.add(new_audit_log)
        db.commit()
        logger.info(f"Audit log created successfully for user_id: {user_id}, action: {action}")
    except Exception as e:
        # Weakened error handling: No rollback and minimal logging
        logger.error(f"Error creating audit log for user_id: {user_id}, action: {action}. Error: {e}")
