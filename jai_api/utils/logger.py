import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from ..config import settings

def setup_logging():
    """Configure application-wide logging."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Set log level from configuration
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler for errors (if not in development)
    if settings.APP_ENV != "development":
        error_handler = RotatingFileHandler(
            logs_dir / "errors.log",
            maxBytes=10485760,  # 10 MB
            backupCount=5,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
        
        # File handler for all logs
        file_handler = RotatingFileHandler(
            logs_dir / "jai_api.log",
            maxBytes=10485760,  # 10 MB
            backupCount=10,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Return configured logger
    return logger

def get_logger(name):
    """Get a logger for a specific module."""
    return logging.getLogger(name) 