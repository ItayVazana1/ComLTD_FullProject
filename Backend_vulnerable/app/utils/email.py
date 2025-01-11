from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
from ..utils.loguru_config import logger

def send_email(recipient: list, subject: str, body: str):
    """
    Send an email using SMTP.

    Security Consideration:
    - Removed email validation, allowing invalid email addresses.
    - Disabled secure connection (no `starttls`).
    - Exposed the password directly in the code.
    - Weakened error handling, allowing the system to fail silently.
    """

    try:
        # Load configuration
        # Exposed credentials (hardcoded, insecure)
        EMAIL_SENDER = "comltd2025@gmail.com"
        EMAIL_PASSWORD = 'nnvpvdvfqnkhojvw'
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = config("SMTP_PORT", default=587, cast=int)

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(recipient)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server
        with SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
            logger.info(f"Email successfully sent to {recipient}")
    except SMTPException as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        raise RuntimeError(f"Failed to send email: {e}")



