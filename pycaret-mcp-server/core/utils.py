import logging
import os
import traceback
from logging.handlers import RotatingFileHandler
from .config import LOG_LEVEL, LOG_FILE, LOG_MAX_BYTES, LOG_BACKUP_COUNT
from typing import Any, Dict

def setup_logging():
    """Configure logging with all components writing to a single file"""
    # Create logs directory from config
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

    # Common formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Configure single rotating file handler using config values
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Configure root logger using config log level
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        handlers=[
            file_handler,
            logging.StreamHandler()
        ]
    )

    return {'server': LOG_FILE}

logger = logging.getLogger(__name__)

class ErrorType:
    READ_ERROR = "READ_ERROR"
    EXECUTION_ERROR = "EXECUTION_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    TOOL_EXECUTION_ERROR = "TOOL_EXECUTION_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

def log_and_return_error(message: str, error_type: str = ErrorType.UNKNOWN_ERROR, exc: Exception = None) -> Dict[str, Any]:
    """Helper to log error and return structured error response."""
    logger.error(f"{message}: {exc}" if exc else message)
    if exc:
        logger.debug(traceback.format_exc())
    
    return {
        "status": "ERROR",
        "error_type": error_type,
        "message": message,
        "details": str(exc) if exc else None,
        "traceback": traceback.format_exc() if exc else None
    }

def handle_exception(e: Exception, error_type: str, context_message: str) -> Dict[str, Any]:
    """Standard exception handler for tools."""
    return log_and_return_error(context_message, error_type, e)
