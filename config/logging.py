"""
Logging Configuration

This module provides centralized logging configuration for the HexStrike AI application.
"""

import logging
import logging.handlers
import os
import sys
from typing import Optional
from flask import Flask


def setup_logging(app: Optional[Flask] = None, log_level: str = 'INFO') -> logging.Logger:
    """
    Setup comprehensive logging configuration
    
    Args:
        app: Flask application instance (optional)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Determine log level
    if app and app.config.get('DEBUG_MODE'):
        log_level = 'DEBUG'
    
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (with fallback for permission issues)
    try:
        log_dir = os.environ.get('LOG_DIR', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'hexstrike.log')
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
    except (PermissionError, OSError) as e:
        # Log to console if file logging fails
        root_logger.warning(f"Could not setup file logging: {e}")
    
    # Setup Flask app logging if provided
    if app:
        app.logger.setLevel(level)
        
        # Disable Flask's default handler to avoid duplicate logs
        app.logger.handlers.clear()
        app.logger.propagate = True
    
    # Setup specific loggers
    setup_component_loggers(level)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level}")
    
    return logger


def setup_component_loggers(level: int):
    """Setup loggers for specific components"""
    
    # Core components
    core_logger = logging.getLogger('core')
    core_logger.setLevel(level)
    
    # API components
    api_logger = logging.getLogger('api')
    api_logger.setLevel(level)
    
    # Tools components
    tools_logger = logging.getLogger('tools')
    tools_logger.setLevel(level)
    
    # Agents components
    agents_logger = logging.getLogger('agents')
    agents_logger.setLevel(level)
    
    # Services components
    services_logger = logging.getLogger('services')
    services_logger.setLevel(level)
    
    # Suppress noisy third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific component
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)