"""
Authentication Middleware

This module provides JWT authentication and authorization middleware for Auth0 integration.
"""

from functools import wraps
from flask import request, jsonify, g, current_app
import jwt
import requests
import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin
import time
from config.auth_config import Auth0Config

logger = logging.getLogger(__name__)

# Cache for Auth0 public keys
_jwks_cache = {}
_jwks_cache_expiry = 0

# Mock user data for development/testing
MOCK_USERS = {
    'mock_jwt_token_12345': {
        'sub': 'auth0|user_123',
        'email': 'analyst1@example.com',
        'name': 'Test Analyst',
        'roles': ['analyst'],
        'tenant_id': 'tenant_123',
        'permissions': ['read:scans', 'write:scans', 'read:tools']
    },
    'admin_token_67890': {
        'sub': 'auth0|admin_1',
        'email': 'admin@example.com',
        'name': 'Test Admin',
        'roles': ['admin'],
        'tenant_id': 'tenant_123',
        'permissions': ['read:all', 'write:all', 'delete:all', 'manage:users']
    },
    'viewer_token_11111': {
        'sub': 'auth0|viewer_1',
        'email': 'viewer@example.com',
        'name': 'Test Viewer',
        'roles': ['viewer'],
        'tenant_id': 'tenant_123',
        'permissions': ['read:scans', 'read:results']
    }
}


def get_token_from_header() -> Optional[str]:
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


def get_auth0_public_key(token: str) -> Optional[Dict[str, Any]]:
    """Get Auth0 public key for JWT verification"""
    global _jwks_cache, _jwks_cache_expiry
    
    try:
        # Check cache first
        current_time = time.time()
        if current_time < _jwks_cache_expiry and _jwks_cache:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')
            
            for key in _jwks_cache.get('keys', []):
                if key.get('kid') == kid:
                    return key
        
        # Fetch JWKS from Auth0
        jwks_url = f"https://{Auth0Config.DOMAIN}/.well-known/jwks.json"
        response = requests.get(jwks_url, timeout=10)
        response.raise_for_status()
        
        jwks = response.json()
        _jwks_cache = jwks
        _jwks_cache_expiry = current_time + 3600  # Cache for 1 hour
        
        # Find the key for this token
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get('kid')
        
        for key in jwks.get('keys', []):
            if key.get('kid') == kid:
                return key
        
        return None
        
    except Exception as e:
        logger.error(f"Error fetching Auth0 public key: {str(e)}")
        return None


def construct_rsa_key(jwk: Dict[str, Any]) -> str:
    """Construct RSA public key from JWK"""
    try:
        from jwt.algorithms import RSAAlgorithm
        return RSAAlgorithm.from_jwk(jwk)
    except Exception as e:
        logger.error(f"Error constructing RSA key: {str(e)}")
        return None


def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return payload"""
    try:
        # In development/testing, use mock verification
        if current_app.config.get('TESTING') or current_app.config.get('DEBUG_MODE'):
            mock_user = MOCK_USERS.get(token)
            if mock_user:
                logger.debug(f"Using mock user for token: {token[:10]}...")
                return mock_user
        
        # Production JWT verification with Auth0
        if not Auth0Config.DOMAIN:
            logger.error("Auth0 domain not configured")
            return None
        
        # Get the public key
        jwk = get_auth0_public_key(token)
        if not jwk:
            logger.warning("Could not get Auth0 public key")
            return None
        
        # Construct RSA key
        rsa_key = construct_rsa_key(jwk)
        if not rsa_key:
            logger.warning("Could not construct RSA key")
            return None
        
        # Verify and decode token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=Auth0Config.ALGORITHMS,
            audience=Auth0Config.AUDIENCE,
            issuer=f"https://{Auth0Config.DOMAIN}/"
        )
        
        # Enrich payload with user roles and permissions
        payload = enrich_user_payload(payload)
        
        logger.debug(f"Successfully verified JWT for user: {payload.get('sub')}")
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        return None
    except jwt.InvalidAudienceError:
        logger.warning("Invalid JWT audience")
        return None
    except jwt.InvalidIssuerError:
        logger.warning("Invalid JWT issuer")
        return None
    except Exception as e:
        logger.error(f"JWT verification error: {str(e)}")
        return None


def enrich_user_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich JWT payload with user roles and permissions"""
    try:
        # Extract user roles from Auth0 custom claims or app_metadata
        roles = []
        permissions = []
        
        # Check for roles in custom namespace (Auth0 Rules/Actions)
        namespace = "https://hexstrike-ai.com/"
        if f"{namespace}roles" in payload:
            roles = payload[f"{namespace}roles"]
        elif "app_metadata" in payload and "roles" in payload["app_metadata"]:
            roles = payload["app_metadata"]["roles"]
        else:
            # Default role for new users
            roles = ["viewer"]
        
        # Get permissions based on roles
        for role in roles:
            role_permissions = Auth0Config.get_role_permissions(role)
            permissions.extend(role_permissions)
        
        # Remove duplicates
        permissions = list(set(permissions))
        
        # Add enriched data to payload
        payload["roles"] = roles
        payload["permissions"] = permissions
        
        # Extract tenant_id if available
        if f"{namespace}tenant_id" in payload:
            payload["tenant_id"] = payload[f"{namespace}tenant_id"]
        elif "app_metadata" in payload and "tenant_id" in payload["app_metadata"]:
            payload["tenant_id"] = payload["app_metadata"]["tenant_id"]
        else:
            # Default tenant for single-tenant deployments
            payload["tenant_id"] = "default"
        
        return payload
        
    except Exception as e:
        logger.error(f"Error enriching user payload: {str(e)}")
        # Return original payload if enrichment fails
        return payload


def has_scope(user_payload: Dict[str, Any], required_scope: str) -> bool:
    """Check if user has required scope/permission"""
    if not user_payload:
        return False
    
    # Check direct permissions first
    user_permissions = user_payload.get('permissions', [])
    if required_scope in user_permissions:
        return True
    
    # Check role-based permissions
    user_roles = user_payload.get('roles', [])
    
    # Admin has all permissions
    if 'admin' in user_roles:
        return True
    
    # Check if any role has the required permission
    return Auth0Config.has_permission(user_roles, required_scope)


def has_any_scope(user_payload: Dict[str, Any], required_scopes: List[str]) -> bool:
    """Check if user has any of the required scopes"""
    if not user_payload or not required_scopes:
        return False
    
    return any(has_scope(user_payload, scope) for scope in required_scopes)


def has_all_scopes(user_payload: Dict[str, Any], required_scopes: List[str]) -> bool:
    """Check if user has all required scopes"""
    if not user_payload or not required_scopes:
        return False
    
    return all(has_scope(user_payload, scope) for scope in required_scopes)


def require_auth(required_scope: Optional[str] = None):
    """Decorator to require authentication and optional scope"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_header()
            
            if not token:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'No authentication token provided'
                }), 401
            
            user_payload = verify_jwt_token(token)
            
            if not user_payload:
                return jsonify({
                    'error': 'Authentication failed',
                    'message': 'Invalid or expired token'
                }), 401
            
            # Check scope if required
            if required_scope and not has_scope(user_payload, required_scope):
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Required permission: {required_scope}',
                    'required_scope': required_scope
                }), 403
            
            # Store user in Flask g object for access in route handlers
            g.current_user = user_payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_any_scope(required_scopes: List[str]):
    """Decorator to require any of the specified scopes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_header()
            
            if not token:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'No authentication token provided'
                }), 401
            
            user_payload = verify_jwt_token(token)
            
            if not user_payload:
                return jsonify({
                    'error': 'Authentication failed',
                    'message': 'Invalid or expired token'
                }), 401
            
            # Check if user has any of the required scopes
            if not has_any_scope(user_payload, required_scopes):
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Required one of: {", ".join(required_scopes)}',
                    'required_scopes': required_scopes
                }), 403
            
            # Store user in Flask g object
            g.current_user = user_payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_all_scopes(required_scopes: List[str]):
    """Decorator to require all specified scopes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_header()
            
            if not token:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'No authentication token provided'
                }), 401
            
            user_payload = verify_jwt_token(token)
            
            if not user_payload:
                return jsonify({
                    'error': 'Authentication failed',
                    'message': 'Invalid or expired token'
                }), 401
            
            # Check if user has all required scopes
            if not has_all_scopes(user_payload, required_scopes):
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Required all of: {", ".join(required_scopes)}',
                    'required_scopes': required_scopes
                }), 403
            
            # Store user in Flask g object
            g.current_user = user_payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_role(required_role: str):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'No authentication token provided'
                }), 401
            
            user_roles = user.get('roles', [])
            
            # Admin has access to everything
            if 'admin' in user_roles:
                return f(*args, **kwargs)
            
            # Check specific role
            if required_role not in user_roles:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Role {required_role} required',
                    'required_role': required_role,
                    'user_roles': user_roles
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current authenticated user from Flask g object"""
    return getattr(g, 'current_user', None)


def get_user_id() -> Optional[str]:
    """Get current user's ID"""
    user = get_current_user()
    return user.get('sub') if user else None


def get_user_email() -> Optional[str]:
    """Get current user's email"""
    user = get_current_user()
    return user.get('email') if user else None


def get_user_name() -> Optional[str]:
    """Get current user's name"""
    user = get_current_user()
    return user.get('name') or user.get('nickname') if user else None


def get_user_roles() -> List[str]:
    """Get current user's roles"""
    user = get_current_user()
    return user.get('roles', []) if user else []


def get_user_permissions() -> List[str]:
    """Get current user's permissions"""
    user = get_current_user()
    return user.get('permissions', []) if user else []


def get_user_tenant_id() -> Optional[str]:
    """Get current user's tenant ID"""
    user = get_current_user()
    return user.get('tenant_id') if user else None


def is_admin() -> bool:
    """Check if current user is admin"""
    user_roles = get_user_roles()
    return 'admin' in user_roles


def is_analyst() -> bool:
    """Check if current user is analyst"""
    user_roles = get_user_roles()
    return 'analyst' in user_roles or is_admin()


def is_viewer() -> bool:
    """Check if current user is viewer"""
    user_roles = get_user_roles()
    return 'viewer' in user_roles or is_analyst()


def can_access_tenant(tenant_id: str) -> bool:
    """Check if current user can access specific tenant"""
    user = get_current_user()
    if not user:
        return False
    
    # Admin can access all tenants
    if is_admin():
        return True
    
    # Users can only access their own tenant
    return user.get('tenant_id') == tenant_id


def refresh_token_if_needed(token: str) -> Optional[str]:
    """Check if token needs refresh and return new token if available"""
    try:
        # Decode without verification to check expiration
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get('exp', 0)
        current_time = time.time()
        
        # If token expires in less than 5 minutes, it needs refresh
        if exp - current_time < 300:
            logger.info("Token needs refresh")
            # In a real implementation, this would call Auth0's token refresh endpoint
            # For now, return None to indicate refresh is needed
            return None
        
        return token
        
    except Exception as e:
        logger.error(f"Error checking token expiration: {str(e)}")
        return None