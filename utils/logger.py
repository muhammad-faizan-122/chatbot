import sys
from loguru import logger


def setup_logger():
    """
    Configures a standardized logger for the application.

    This function sets up a default logger and adds a file handler for
    structured, rotating log files. It's designed to be called once
    at the start of the application or module.
    """
    # Remove the default handler to avoid duplicate logs in the console
    logger.remove()

    # Add a new handler for console output with a specific format and level
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    # Add a file handler for detailed debug logs with rotation and retention
    logger.add(
        "logs/app.log",
        rotation="10 MB",  # Rotate the log file when it reaches 10 MB
        retention="7 days",  # Keep logs for up to 7 days
        level="DEBUG",  # Log all messages from DEBUG level and above
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        enqueue=True,  # Make logging thread-safe (important for Streamlit)
        backtrace=True,  # Show the full stack trace on exceptions
        diagnose=True,  # Add exception variable values for debugging
    )

    logger.info("Logger has been successfully configured.")
    return logger


# Create a logger instance to be imported by other modules
log = setup_logger()
