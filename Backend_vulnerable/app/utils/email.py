from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
from ..utils.loguru_config import logger

def send_email(recipient: list, subject: str, body: str):
    """
    Send an email using SMTP.
    :param recipient: List of recipient email addresses.
    :param subject: Email subject.
    :param body: Email body.
    """
    # Load environment variables using decouple
    EMAIL_SENDER = config("EMAIL_SENDER")
    EMAIL_PASSWORD = config("EMAIL_PASSWORD")
    SMTP_SERVER = config("SMTP_SERVER", default="smtp.gmail.com")
    SMTP_PORT = config("SMTP_PORT", default=587, cast=int)

    # Validate essential configurations
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        logger.error("Sender email or password not set in environment variables.")
        raise ValueError("Sender email or password not set in environment variables.")

    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(recipient)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        logger.info(f"Attempting to send email to {recipient}")

        # Connect to the SMTP server
        with SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
            logger.info(f"Email successfully sent to {recipient}")

    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        raise RuntimeError(f"Failed to send email: {e}")
