from loguru import logger
import sys
import os

def setup_loguru():
    """
    Setup Loguru logger with console and file handlers.
    :return: Configured Loguru logger.
    """
    # Clear default handlers to avoid duplicate logs
    logger.remove()

    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | "
               "<magenta>{name}</magenta>:<light-magenta>{function}</light-magenta>:<light-yellow>{line}</light-yellow> | <level>{message}</level>",
        level="DEBUG",  # Console log level
        colorize=True,
    )

    # Directory for log files
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists

    # Add file handler
    logger.add(
        os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),
        rotation="1 day",  # Create a new log file every day
        retention="7 days",  # Keep logs for 7 days
        compression="zip",  # Compress old logs
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="INFO",  # File log level
    )

    return logger

loguru_logger = setup_loguru()
