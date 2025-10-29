"""
Auth0 Configuration Module

This module provides Auth0 authentication configuration and client initialization.
"""

import os
from typing import Dict, List, Optional
from authlib.integrations.flask_client import OAuth
from flask import Flask


class Auth0Config:
    """Auth0 configuration and client management"""
    
    # Auth0 Configuration
    DOMAIN = os.getenv('AUTH0_DOMAIN')
    CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    AUDIENCE = os.getenv('AUTH0_AUDIENCE', 'https://hexstrike-ai.com/api')
    ALGORITHMS = ['RS256']
    
    # Callback URLs
    CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL', 'http://localhost:8888/callback')
    LOGOUT_URL = os.getenv('AUTH0_LOGOUT_URL', 'http://localhost:8888')
    
    # Role-based access control
    ROLES = {
        'admin': [
            'read:all', 'write:all', 'delete:all', 
            'manage:users', 'manage:tenants', 'manage:system'
        ],
        'analyst': [
            'read:scans', 'write:scans', 'read:tools', 
            'write:tools', 'read:vulnerabilities'
        ],
        'viewer': [
            'read:scans', 'read:results', 'read:vulnerabilities'
        ]
    }
    
    # Permission scopes
    SCOPES = {
        # System management
        'manage:system': 'Manage system configuration and settings',
        'manage:users': 'Manage user accounts and permissions',
        'manage:tenants': 'Manage tenant accounts and resources',
        
        # Data access
        'read:all': 'Read access to all resources',
        'read:scans': 'Read access to scan data',
        'read:tools': 'Read access to security tools',
        'read:vulnerabilities': 'Read access to vulnerability data',
        'read:results': 'Read access to scan results',
        
        # Data modification
        'write:all': 'Write access to all resources',
        'write:scans': 'Create and modify scans',
        'write:tools': 'Create and modify security tools',
        'write:vulnerabilities': 'Create and modify vulnerability data',
        
        # Data deletion
        'delete:all': 'Delete access to all resources',
        'delete:scans': 'Delete scan data',
        'delete:tools': 'Delete security tools'
    }
    
    @classmethod
    def get_role_permissions(cls, role: str) -> List[str]:
        """Get permissions for a specific role"""
        return cls.ROLES.get(role, [])
    
    @classmethod
    def has_permission(cls, user_roles: List[str], required_permission: str) -> bool:
        """Check if user roles have required permission"""
        for role in user_roles:
            if required_permission in cls.get_role_permissions(role):
                return True
        return False
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate Auth0 configuration"""
        if not cls.DOMAIN:
            raise ValueError("AUTH0_DOMAIN environment variable is required")
        if not cls.CLIENT_ID:
            raise ValueError("AUTH0_CLIENT_ID environment variable is required")
        if not cls.CLIENT_SECRET:
            raise ValueError("AUTH0_CLIENT_SECRET environment variable is required")
        return True


class Auth0Client:
    """Auth0 OAuth client wrapper"""
    
    def __init__(self, app: Optional[Flask] = None):
        self.oauth = OAuth()
        self.auth0 = None
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize Auth0 client with Flask app"""
        self.oauth.init_app(app)
        
        # Configure Auth0 OAuth client
        self.auth0 = self.oauth.register(
            'auth0',
            client_id=Auth0Config.CLIENT_ID,
            client_secret=Auth0Config.CLIENT_SECRET,
            server_metadata_url=f'https://{Auth0Config.DOMAIN}/.well-known/openid_configuration',
            client_kwargs={
                'scope': 'openid profile email',
                'audience': Auth0Config.AUDIENCE
            }
        )
        
        return self.auth0
    
    def get_authorization_url(self, redirect_uri: str) -> str:
        """Get Auth0 authorization URL"""
        if not self.auth0:
            raise RuntimeError("Auth0 client not initialized")
        
        return self.auth0.authorize_redirect(redirect_uri)
    
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict:
        """Exchange authorization code for access token"""
        if not self.auth0:
            raise RuntimeError("Auth0 client not initialized")
        
        return self.auth0.authorize_access_token(redirect_uri=redirect_uri)


# Global Auth0 client instance
auth0_client = Auth0Client()