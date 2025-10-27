"""
CORS Handler

This module provides CORS (Cross-Origin Resource Sharing) configuration.
"""

from flask import Flask
from flask_cors import CORS
import logging

logger = logging.getLogger(__name__)


def setup_cors(app: Flask):
    """Setup CORS configuration for the Flask app"""
    
    # Get CORS configuration from app config
    cors_config = {
        'origins': app.config.get('CORS_ORIGINS', ['http://localhost:3000', 'https://localhost:3000']),
        'methods': app.config.get('CORS_METHODS', ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']),
        'allow_headers': app.config.get('CORS_ALLOW_HEADERS', [
            'Content-Type',
            'Authorization',
            'X-Requested-With',
            'X-CSRF-Token'
        ]),
        'expose_headers': app.config.get('CORS_EXPOSE_HEADERS', [
            'X-Total-Count',
            'X-Page-Count',
            'X-Rate-Limit-Remaining'
        ]),
        'supports_credentials': app.config.get('CORS_SUPPORTS_CREDENTIALS', True),
        'max_age': app.config.get('CORS_MAX_AGE', 86400)  # 24 hours
    }
    
    # Initialize CORS
    CORS(app, **cors_config)
    
    logger.info(f"CORS configured with origins: {cors_config['origins']}")
    
    # Add custom CORS headers for API responses
    @app.after_request
    def after_request(response):
        """Add additional CORS and security headers"""
        
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # API versioning header
        response.headers['X-API-Version'] = '1.0'
        
        # Rate limiting headers (would be set by rate limiter)
        if not response.headers.get('X-Rate-Limit-Remaining'):
            response.headers['X-Rate-Limit-Remaining'] = '100'
            response.headers['X-Rate-Limit-Limit'] = '100'
            response.headers['X-Rate-Limit-Reset'] = '3600'
        
        return response