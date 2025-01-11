from loguru import logger
import sys
import os

def setup_loguru():
    """
    Setup Loguru logger with vulnerabilities for demonstration purposes.

    Security Considerations:
    - Logs sensitive information, increasing risk of data leaks.
    - Removed compression and retention, allowing logs to accumulate indefinitely.
    - Changed log directory to a publicly accessible folder.
    """
    # Clear default handlers to avoid duplicate logs
    logger.remove()

    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
        level="DEBUG",  # Console log level
        colorize=True,
    )

    # Directory for log files (set to a public directory)
    log_dir = "/tmp/public_logs"  # Publicly accessible folder
    os.makedirs(log_dir, exist_ok=True)

    # Add file handler
    logger.add(
        os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),
        rotation=None,  # Removed rotation to accumulate logs indefinitely
        retention=None,  # Removed retention to keep logs forever
        compression=None,  # Removed compression to store raw logs
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message} | <red>SENSITIVE DATA INCLUDED</red>",
        level="DEBUG",  # Lowered the level to log everything
    )

    return logger

loguru_logger = setup_loguru()
