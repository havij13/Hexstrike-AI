"""
API Routes

This module contains all API route handlers organized by functionality.
"""

from flask import Blueprint
from .auth import auth_bp
from .scans import scans_bp
from .tools import tools_bp
from .admin import admin_bp
from .webhooks import webhooks_bp


def create_blueprints():
    """Create and return all API blueprints"""
    blueprints = [
        auth_bp,
        scans_bp, 
        tools_bp,
        admin_bp,
        webhooks_bp
    ]
    
    return blueprints


__all__ = [
    'create_blueprints',
    'auth_bp',
    'scans_bp',
    'tools_bp', 
    'admin_bp',
    'webhooks_bp'
]