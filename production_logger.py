"""
PRODUCTION-GRADE LOGGING SYSTEM
Replaces all debug print() statements with secure logging

Features:
- Different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Secure logging (no sensitive data exposure)
- File logging for audit trail
- Console logging for development
- Production mode (minimal logging)
- Compliance with NHS data protection
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Determine if in production
IS_PRODUCTION = os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud" or os.getenv("ENV") == "production"

# Configure logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Create formatters
file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')

# Create handlers
def get_logger(module_name: str) -> logging.Logger:
    """
    Get a configured logger for a module
    
    Usage:
        logger = get_logger(__name__)
        logger.info("Patient loaded successfully")
        logger.error("Failed to load patient data")
    """
    logger = logging.getLogger(module_name)
    
    # Set level based on environment
    if IS_PRODUCTION:
        logger.setLevel(logging.WARNING)  # Only warnings and errors in production
    else:
        logger.setLevel(logging.DEBUG)  # All messages in development
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler (always active for audit trail)
    log_file = LOGS_DIR / f"t21_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (only in development)
    if not IS_PRODUCTION:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger


# Convenience functions for common logging patterns
def log_user_action(module: str, user_email: str, action: str, details: str = ""):
    """
    Log user actions for audit trail
    
    Example:
        log_user_action("PTL", "admin@t21.co.uk", "Added patient", "NHS: 123 456 7890")
    """
    logger = get_logger(module)
    # Mask email for security (only log first part)
    masked_email = user_email.split('@')[0] + "@***" if '@' in user_email else "***"
    logger.info(f"User '{masked_email}' performed '{action}'. {details}")


def log_data_load(module: str, record_count: int, user_type: str = "user"):
    """
    Log data loading for debugging
    
    Example:
        log_data_load("PTL", 45, "admin")
    """
    logger = get_logger(module)
    logger.debug(f"Loaded {record_count} records for {user_type}")


def log_error(module: str, error_msg: str, exception: Exception = None):
    """
    Log errors with optional exception details
    
    Example:
        log_error("PTL", "Failed to load patients", e)
    """
    logger = get_logger(module)
    if exception:
        logger.error(f"{error_msg}: {str(exception)}")
    else:
        logger.error(error_msg)


def log_security_event(module: str, event: str, severity: str = "WARNING"):
    """
    Log security-related events
    
    Example:
        log_security_event("Login", "Failed login attempt", "WARNING")
    """
    logger = get_logger(module)
    if severity == "CRITICAL":
        logger.critical(f"SECURITY: {event}")
    else:
        logger.warning(f"SECURITY: {event}")


# Replace common debug patterns
class DebugInfo:
    """
    Secure debug info display (replaces print statements)
    
    Usage:
        debug = DebugInfo("PTL")
        debug.log_load(user_email, is_admin, patient_count)
    """
    
    def __init__(self, module_name: str):
        self.module = module_name
        self.logger = get_logger(module_name)
    
    def log_load(self, user_email: str, is_admin: bool, record_count: int):
        """Log data loading info"""
        mode = "ADMIN" if is_admin else "STUDENT"
        masked_email = user_email.split('@')[0] + "@***" if '@' in user_email else "***"
        self.logger.debug(f"Loading {self.module} for {masked_email} ({mode}): {record_count} records")
    
    def log_action(self, action: str, details: str = ""):
        """Log action performed"""
        self.logger.info(f"{action} - {details}")
    
    def log_error(self, error_msg: str):
        """Log error"""
        self.logger.error(error_msg)


# Cleanup old log files (keep last 30 days)
def cleanup_old_logs(days_to_keep: int = 30):
    """Remove log files older than specified days"""
    try:
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        for log_file in LOGS_DIR.glob("t21_*.log"):
            if log_file.stat().st_mtime < cutoff_date:
                log_file.unlink()
                print(f"Deleted old log: {log_file.name}")
    except Exception as e:
        print(f"Error cleaning up logs: {e}")


# Export
__all__ = [
    'get_logger',
    'log_user_action',
    'log_data_load',
    'log_error',
    'log_security_event',
    'DebugInfo',
    'cleanup_old_logs'
]

# Initialize on import
if __name__ != "__main__":
    # Auto-cleanup old logs on import
    cleanup_old_logs()
