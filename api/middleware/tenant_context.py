"""
Tenant Context Middleware

This module provides multi-tenant context management.
"""

from functools import wraps
from flask import request, jsonify, g, current_app
from api.middleware.auth_middleware import get_current_user, get_user_tenant_id
from services.tenant_service import tenant_service
import logging

logger = logging.getLogger(__name__)


def extract_tenant_context():
    """Extract tenant context from request"""
    try:
        # Method 1: Get from authenticated user
        user = get_current_user()
        if user:
            tenant_id = get_user_tenant_id()
            if tenant_id:
                tenant = tenant_service.get_tenant(tenant_id)
                if tenant:
                    g.current_tenant = tenant
                    g.tenant_id = tenant_id
                    return tenant
        
        # Method 2: Get from subdomain (for multi-tenant SaaS)
        host = request.headers.get('Host', '')
        if '.' in host:
            subdomain = host.split('.')[0]
            tenant = tenant_service.get_tenant_by_domain(subdomain)
            if tenant:
                g.current_tenant = tenant
                g.tenant_id = tenant.id
                return tenant
        
        # Method 3: Get from custom header
        tenant_header = request.headers.get('X-Tenant-ID')
        if tenant_header:
            tenant = tenant_service.get_tenant(tenant_header)
            if tenant:
                g.current_tenant = tenant
                g.tenant_id = tenant.id
                return tenant
        
        # Method 4: Default tenant for single-tenant deployments
        default_tenant = tenant_service.get_tenant("default")
        if default_tenant:
            g.current_tenant = default_tenant
            g.tenant_id = "default"
            return default_tenant
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting tenant context: {str(e)}")
        return None


def require_tenant():
    """Decorator to require valid tenant context"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            tenant = extract_tenant_context()
            
            if not tenant:
                return jsonify({
                    'error': 'Tenant context required',
                    'message': 'No valid tenant found for this request'
                }), 400
            
            if tenant.status != 'active':
                return jsonify({
                    'error': 'Tenant inactive',
                    'message': f'Tenant {tenant.name} is not active'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_tenant_access(tenant_id: str):
    """Decorator to require access to specific tenant"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_tenant = get_current_tenant()
            
            if not current_tenant:
                return jsonify({
                    'error': 'Tenant context required',
                    'message': 'No tenant context found'
                }), 400
            
            # Admin users can access any tenant
            user = get_current_user()
            if user and 'admin' in user.get('roles', []):
                return f(*args, **kwargs)
            
            # Check if user can access the requested tenant
            if current_tenant.id != tenant_id:
                return jsonify({
                    'error': 'Tenant access denied',
                    'message': f'Access denied to tenant {tenant_id}'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def check_resource_limit(resource: str):
    """Decorator to check tenant resource limits"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            tenant = get_current_tenant()
            
            if not tenant:
                return jsonify({
                    'error': 'Tenant context required'
                }), 400
            
            # Get current usage (this would be from database in real implementation)
            usage = tenant_service.get_resource_usage(tenant.id)
            current_usage = usage.get(resource, 0)
            
            # Check limit
            if not tenant_service.check_resource_limit(tenant.id, resource, current_usage):
                limit = tenant.resource_limits.get(resource, 0)
                return jsonify({
                    'error': 'Resource limit exceeded',
                    'message': f'Tenant has reached the limit for {resource}',
                    'current_usage': current_usage,
                    'limit': limit
                }), 429
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def check_tool_access(tool_name: str):
    """Decorator to check if tenant can access specific tool"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            tenant = get_current_tenant()
            
            if not tenant:
                return jsonify({
                    'error': 'Tenant context required'
                }), 400
            
            if not tenant_service.is_tool_allowed(tenant.id, tool_name):
                return jsonify({
                    'error': 'Tool access denied',
                    'message': f'Tool {tool_name} is not allowed for this tenant',
                    'tool': tool_name
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def get_current_tenant():
    """Get current tenant from Flask g object"""
    return getattr(g, 'current_tenant', None)


def get_current_tenant_id():
    """Get current tenant ID from Flask g object"""
    return getattr(g, 'tenant_id', None)


def get_tenant_settings():
    """Get current tenant settings"""
    tenant = get_current_tenant()
    return tenant.settings if tenant else {}


def get_tenant_resource_limits():
    """Get current tenant resource limits"""
    tenant = get_current_tenant()
    return tenant.resource_limits if tenant else {}


def is_multi_tenant_enabled():
    """Check if multi-tenant mode is enabled"""
    return current_app.config.get('MULTI_TENANT_ENABLED', False)


def tenant_context_middleware():
    """Flask before_request middleware to set tenant context"""
    # Skip for auth endpoints and health checks
    if request.endpoint in ['auth.login', 'auth.callback', 'health']:
        return
    
    # Extract tenant context for all other requests
    extract_tenant_context()