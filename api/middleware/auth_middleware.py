"""
Authentication Middleware

This module provides authentication and authorization middleware.
"""

from functools import wraps
from flask import request, jsonify, g, current_app
import jwt
import logging

logger = logging.getLogger(__name__)

# Mock user data for development
MOCK_USERS = {
    'mock_jwt_token_12345': {
        'user_id': 'user_123',
        'username': 'analyst1',
        'email': 'analyst1@example.com',
        'roles': ['analyst'],
        'tenant_id': 'tenant_123'
    },
    'admin_token_67890': {
        'user_id': 'admin_1',
        'username': 'admin',
        'email': 'admin@example.com',
        'roles': ['admin'],
        'tenant_id': 'tenant_123'
    }
}


def get_token_from_header():
    """Extract JWT token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    try:
        # Expected format: "Bearer <token>"
        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return None
        
        return parts[1]
    except Exception:
        return None


def verify_jwt_token(token):
    """Verify JWT token and return payload"""
    try:
        # In development, use mock verification
        if current_app.config.get('TESTING') or current_app.config.get('DEBUG_MODE'):
            return MOCK_USERS.get(token)
        
        # In production, use proper JWT verification with Auth0
        # This would involve:
        # 1. Getting Auth0 public key
        # 2. Verifying token signature
        # 3. Checking expiration
        # 4. Validating audience and issuer
        
        # For now, return mock data
        return MOCK_USERS.get(token)
        
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"JWT verification error: {str(e)}")
        return None


def has_scope(user_payload, required_scope):
    """Check if user has required scope/permission"""
    if not user_payload:
        return False
    
    user_roles = user_payload.get('roles', [])
    
    # Admin has all permissions
    if 'admin' in user_roles:
        return True
    
    # Map scopes to roles
    scope_role_mapping = {
        'read:scans': ['analyst', 'viewer'],
        'write:scans': ['analyst'],
        'read:tools': ['analyst', 'viewer'],
        'write:tools': ['analyst'],
        'read:admin': ['admin'],
        'write:admin': ['admin'],
        'manage:users': ['admin']
    }
    
    allowed_roles = scope_role_mapping.get(required_scope, [])
    return any(role in user_roles for role in allowed_roles)


def require_auth(required_scope=None):
    """Decorator to require authentication"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_header()
            
            if not token:
                return jsonify({'error': 'No authentication token provided'}), 401
            
            user_payload = verify_jwt_token(token)
            
            if not user_payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Check scope if required
            if required_scope and not has_scope(user_payload, required_scope):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            # Store user in Flask g object for access in route handlers
            g.current_user = user_payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_role(required_role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            
            user_roles = user.get('roles', [])
            
            # Admin has access to everything
            if 'admin' in user_roles:
                return f(*args, **kwargs)
            
            # Check specific role
            if required_role not in user_roles:
                return jsonify({'error': f'Role {required_role} required'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def get_current_user():
    """Get current authenticated user from Flask g object"""
    return getattr(g, 'current_user', None)


def get_user_tenant_id():
    """Get current user's tenant ID"""
    user = get_current_user()
    return user.get('tenant_id') if user else None


def is_admin():
    """Check if current user is admin"""
    user = get_current_user()
    if not user:
        return False
    
    return 'admin' in user.get('roles', [])


def can_access_tenant(tenant_id):
    """Check if current user can access specific tenant"""
    user = get_current_user()
    if not user:
        return False
    
    # Admin can access all tenants
    if is_admin():
        return True
    
    # Users can only access their own tenant
    return user.get('tenant_id') == tenant_id