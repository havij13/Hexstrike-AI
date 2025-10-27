"""
API Middleware

This module contains middleware components for the API layer.
"""

from .auth_middleware import require_auth, require_role, get_current_user
from .cors_handler import setup_cors
from .rate_limiter import setup_rate_limiting

def setup_middleware(app):
    """Setup all middleware for the Flask app"""
    setup_cors(app)
    setup_rate_limiting(app)

__all__ = [
    'require_auth',
    'require_role', 
    'get_current_user',
    'setup_middleware',
    'setup_cors',
    'setup_rate_limiting'
]