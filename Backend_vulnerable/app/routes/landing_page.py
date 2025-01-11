from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..models.database import get_db_connection
from ..utils.loguru_config import logger
from ..utils.email import send_email

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def landing_page():
    """
    Render the landing page with a distinct theme for the vulnerable backend.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Landing Page - Vulnerable Backend</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
        <style>
            body {
                background-color: #2c061f; /* Dark Red Background */
                color: #f8d210; /* Bright Yellow Text */
            }
            .btn {
                border: 2px solid #f8d210;
            }
            .btn:hover {
                background-color: #ff5733; /* Orange for hover */
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container text-center mt-5">
            <h1 class="mb-4">🚨 Vulnerable Backend Management 🚨</h1>
            <div class="d-grid gap-2 d-md-flex justify-content-center">
                <button class="btn btn-danger me-md-2" onclick="location.href='/docs'">OpenAPI Documentation</button>
                <button class="btn btn-warning" onclick="location.href='/audit-logs-view'">Logs</button>
                <button class="btn btn-danger" onclick="location.href='/test-email'">Test Email</button>
                <button class="btn btn-warning" onclick="location.href='/redoc'">ReDoc Documentation</button>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/test-email", response_class=HTMLResponse)
def test_email_page():
    """
    Render a page to test email sending functionality.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Email - Vulnerable Backend</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
        <style>
            body {
                background-color: #350d36; /* Deep Purple Background */
                color: #f4d03f; /* Gold Text */
            }
            .btn {
                border: 2px solid #f4d03f;
                color: #f4d03f;
            }
            .btn:hover {
                background-color: #e74c3c; /* Bright Red for hover */
                color: white;
            }
            .form-control {
                background-color: #5e2750; /* Light Purple Input Background */
                color: white;
                border: 1px solid #f4d03f;
            }
            .form-control:focus {
                background-color: #7d3c98; /* Brighter Purple on Focus */
                color: white;
                border-color: #e74c3c;
            }
            .bg-secondary {
                background-color: #5e2750 !important; /* Darker Purple */
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">📧 Send Test Email</h1>
            <form method="post" action="/send-test-email" class="bg-secondary p-4 rounded">
                <div class="mb-3">
                    <label for="email" class="form-label">Email Address</label>
                    <input type="email" id="email" name="email" class="form-control" required>
                </div>
                <div class="d-grid">
                    <button type="submit" class="btn">Send Test Email</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)



@router.post("/send-test-email")
def send_test_email(email: str = Form(...)):
    """
    Handle test email sending.

    Security Consideration:
    - Does not sanitize email input, allowing XSS attacks.
    """
    try:
        send_email(
            recipient=[email],
            subject="Test Email - Vulnerable Backend",
            body=f"This is a test email sent to {email}."
        )
        logger.info(f"Test email sent to {email}")
        return HTMLResponse(content=f"<h1 style='color: #f8d210;'>Test email successfully sent to {email}!</h1>")
    except Exception as e:
        logger.error(f"Failed to send test email to {email}: {e}")
        return HTMLResponse(content=f"<h1 style='color: red;'>Error: {e}</h1>")

@router.get("/audit-logs-view", response_class=HTMLResponse)
def audit_logs_view():
    """
    Render a page to view and filter Audit Logs with distinct colors.

    Security Consideration:
    - Includes dynamic data rendering directly in the browser, which could allow XSS attacks if logs are manipulated.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Audit Logs - Vulnerable Backend</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
        <style>
            body {
                background-color: #2c061f; /* Dark Red Background */
                color: #f8d210; /* Bright Yellow Text */
            }
            table {
                background-color: #800e42; /* Dark Pink */
                color: white;
            }
            .btn {
                border: 2px solid #f8d210;
            }
            .btn:hover {
                background-color: #ff5733;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">Audit Logs - Vulnerable Backend</h1>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User ID</th>
                        <th>Action</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody id="auditLogsTable">
                </tbody>
            </table>
        </div>

        <script>
            async function fetchLogs() {
                const response = await fetch('/audit-logs');
                const logs = await response.json();
                const tableBody = document.getElementById("auditLogsTable");
                logs.forEach(log => {
                    tableBody.innerHTML += `<tr>
                        <td>${log.id}</td>
                        <td>${log.user_id}</td>
                        <td>${log.action}</td>
                        <td>${new Date(log.timestamp).toLocaleString()}</td>
                    </tr>`;
                });
            }

            document.addEventListener("DOMContentLoaded", () => fetchLogs());
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/audit-logs")
def get_audit_logs(user_id: str = None, db = Depends(get_db_connection)):
    """
    Fetch Audit Logs, optionally filtered by User ID.

    Security Consideration:
    - Uses raw SQL queries without sanitization, vulnerable to SQL Injection.
    """
    logger.info("Fetching audit logs from the database.")
    try:
        if user_id:
            # Raw SQL query directly using user_id without sanitization, vulnerable to SQL Injection.
            query = f"SELECT * FROM audit_logs WHERE user_id = '{user_id}'"
        else:
            # Fetch all logs without filtering.
            query = "SELECT * FROM audit_logs"

        # Use execute to fetch the data
        logs = db.execute(query)  # db.execute returns the raw results
        logger.debug(f"Fetched {len(logs)} logs.")

        # Process logs into the desired format
        return [{"id": log[0], "user_id": log[1], "action": log[2], "timestamp": log[3]} for log in logs]

    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

