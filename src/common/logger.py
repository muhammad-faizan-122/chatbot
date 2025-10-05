from loguru import logger
import os


def setup_logger(file_name="app.log", dir="logs"):
    """
    Configures a standardized logger for the application.

    This function sets up a default logger and adds a file handler for
    structured, rotating log files. It's designed to be called once
    at the start of the application or module.
    """
    # Remove the default handler to avoid duplicate logs in the console
    logger.remove()

    fp = os.path.join(dir, file_name)
    logger.add(
        fp,
        rotation="10 MB",  # Rotate the log file when it reaches 10 MB
        retention="7 days",  # Keep logs for up to 7 days
        level="DEBUG",  # Log all messages from DEBUG level and above
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | {file}: {function}: {line} - [{message}]",
        enqueue=True,  # Make logging thread-safe (important for Streamlit)
        backtrace=True,  # Show the full stack trace on exceptions
        diagnose=True,  # Add exception variable values for debugging
    )

    logger.info("Logger has been successfully configured.")
    return logger


# Create a logger instance to be imported by other modules
log = setup_logger()
