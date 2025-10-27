"""
Flask Application Factory

This module implements the Flask application factory pattern for creating
and configuring the HexStrike AI application instance.
"""

import logging
import os
from flask import Flask
from config.settings import Config
from config.logging import setup_logging


def create_app(config_name='default', testing=False):
    """
    Create and configure Flask application instance
    
    Args:
        config_name (str): Configuration name to use
        testing (bool): Whether to configure for testing
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if testing:
        app.config['TESTING'] = True
        app.config['JSON_SORT_KEYS'] = False
    else:
        config = Config()
        app.config.from_object(config)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Initialize extensions
    initialize_extensions(app)
    
    return app


def register_blueprints(app):
    """Register application blueprints"""
    from api.routes.auth import auth_bp
    from api.routes.scans import scans_bp
    from api.routes.tools import tools_bp
    from api.routes.admin import admin_bp
    from api.routes.webhooks import webhooks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(scans_bp, url_prefix='/api/scans')
    app.register_blueprint(tools_bp, url_prefix='/api/tools')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(webhooks_bp, url_prefix='/api/webhooks')


def register_error_handlers(app):
    """Register application error handlers"""
    from core.error_handler import EnhancedErrorHandler
    
    error_handler = EnhancedErrorHandler()
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {str(error)}")
        return {'error': 'An unexpected error occurred'}, 500


def initialize_extensions(app):
    """Initialize Flask extensions"""
    # Initialize database connections, caching, etc.
    pass