"""
Configuration Management System

This module provides centralized configuration management for the HexStrike AI application.
"""

import os
from typing import Dict, Any


class Config:
    """Base configuration class with default settings"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hexstrike-ai-secret-key-change-in-production')
    JSON_SORT_KEYS = False
    
    # API Configuration
    API_HOST = os.environ.get('HEXSTRIKE_HOST', '127.0.0.1')
    API_PORT = int(os.environ.get('HEXSTRIKE_PORT', 8888))
    
    # Security Configuration
    COMMAND_TIMEOUT = int(os.environ.get('COMMAND_TIMEOUT', 300))
    MAX_CONCURRENT_PROCESSES = int(os.environ.get('MAX_CONCURRENT_PROCESSES', 10))
    
    # Cache Configuration
    CACHE_SIZE = int(os.environ.get('CACHE_SIZE', 1000))
    CACHE_TTL = int(os.environ.get('CACHE_TTL', 3600))
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///hexstrike.db')
    
    # Auth0 Configuration
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE', 'https://hexstrike-ai.com/api')
    
    # Monitoring Configuration
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    PROMETHEUS_METRICS_ENABLED = os.environ.get('PROMETHEUS_METRICS_ENABLED', 'true').lower() == 'true'
    
    # Tool Configuration
    TOOLS_PATH = os.environ.get('TOOLS_PATH', '/usr/local/bin')
    WORDLISTS_PATH = os.environ.get('WORDLISTS_PATH', '/usr/share/wordlists')
    
    # Debug Configuration
    DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        config_dict = {}
        for key in dir(cls):
            if not key.startswith('_') and not callable(getattr(cls, key)):
                config_dict[key] = getattr(cls, key)
        return config_dict
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration values"""
        required_vars = []
        
        # Check for required environment variables in production
        if not cls.DEBUG_MODE:
            if not cls.AUTH0_DOMAIN:
                required_vars.append('AUTH0_DOMAIN')
            if not cls.AUTH0_CLIENT_ID:
                required_vars.append('AUTH0_CLIENT_ID')
            if not cls.AUTH0_CLIENT_SECRET:
                required_vars.append('AUTH0_CLIENT_SECRET')
        
        if required_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(required_vars)}")
        
        return True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG_MODE = True
    COMMAND_TIMEOUT = 60  # Shorter timeout for development


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG_MODE = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate production configuration"""
        super().validate_config()
        
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'hexstrike-ai-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set to a secure value in production")
        
        return True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG_MODE = True
    CACHE_TTL = 1  # Short cache for testing
    COMMAND_TIMEOUT = 10  # Very short timeout for testing


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}