from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models.database import get_db_connection
from pydantic import BaseModel
from ..utils.loguru_config import logger

router = APIRouter()

# Models for request validation
class AuditLogCreate(BaseModel):
    user_id: str
    action: str

@router.get("/")
def get_audit_logs(db: Session = Depends(get_db_connection)):
    """
    Fetch all audit logs.

    Security Consideration:
    - Uses raw SQL queries without sanitization.
    """
    logger.info("Fetching all audit logs.")
    try:
        query = "SELECT * FROM audit_logs"
        result = db.execute(query).fetchall()
        return result

    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{log_id}")
def get_audit_log(log_id: int, db: Session = Depends(get_db_connection)):
    """
    Fetch a specific audit log by its ID.

    Security Consideration:
    - Uses raw SQL queries without sanitization, vulnerable to SQL Injection.
    """
    logger.info(f"Fetching audit log with ID: {log_id}")
    try:
        query = f"SELECT * FROM audit_logs WHERE id={log_id}"
        result = db.execute(query).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Audit log not found")
        return result

    except Exception as e:
        logger.error(f"Error fetching audit log: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
def get_audit_logs_by_user(user_id: str, db: Session = Depends(get_db_connection)):
    """
    Fetch all audit logs for a specific user.

    Security Consideration:
    - Uses raw SQL queries without sanitization, vulnerable to SQL Injection.
    """
    logger.info(f"Fetching audit logs for user ID: {user_id}")
    try:
        query = f"SELECT * FROM audit_logs WHERE user_id='{user_id}'"
        result = db.execute(query).fetchall()
        return result

    except Exception as e:
        logger.error(f"Error fetching audit logs for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def create_audit_log(audit_log: AuditLogCreate, db: Session = Depends(get_db_connection)):
    """
    Create a new audit log entry.

    Security Consideration:
    - Uses raw SQL queries without sanitization, vulnerable to SQL Injection.
    """
    logger.info(f"Creating a new audit log for user ID: {audit_log.user_id}")
    try:
        query = f"""
        INSERT INTO audit_logs (user_id, action)
        VALUES ('{audit_log.user_id}', '{audit_log.action}')
        """
        db.execute(query)
        db.commit()
        return {"status": "success", "message": "Audit log created successfully"}

    except Exception as e:
        logger.error(f"Error creating audit log: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/actions")
def get_possible_actions():
    """
    Fetch all possible actions for audit logging.

    Security Consideration:
    - Returns static data, no vulnerabilities here.
    """
    logger.info("Fetching possible audit log actions.")
    return [
        "User login",
        "User logout",
        "User registration",
        "Package created",
        "Package updated",
        "Customer deleted",
        "Profile updated",
    ]
