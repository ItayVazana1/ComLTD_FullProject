from sqlalchemy.orm import Session
from ..models.tables import AuditLog
from ..utils.loguru_config import logger


def create_audit_log_entry(user_id: str, action: str, db: Session):
    """
    Create a new audit log entry.

    :param user_id: ID of the user performing the action.
    :param action: Description of the action performed.
    :param db: Database session.
    :raises ValueError: If input data is invalid.
    :raises HTTPException: If database operation fails.
    """
    logger.info(f"Attempting to create audit log for user_id: {user_id}, action: {action}")

    # Input validation
    if not user_id or not isinstance(user_id, str):
        logger.error("Invalid user_id provided for audit log entry.")
        raise ValueError("Invalid user_id. It must be a non-empty string.")

    if not action or not isinstance(action, str):
        logger.error("Invalid action provided for audit log entry.")
        raise ValueError("Invalid action. It must be a non-empty string.")

    try:
        new_audit_log = AuditLog(
            user_id=user_id.strip(),
            action=action.strip()
        )
        db.add(new_audit_log)
        db.commit()
        logger.info(f"Audit log created successfully for user_id: {user_id}, action: {action}")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create audit log for user_id: {user_id}, action: {action}. Error: {e}")
        raise
