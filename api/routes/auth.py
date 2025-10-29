"""
Authentication Routes

This module handles Auth0 authentication and authorization endpoints.
"""

from flask import Blueprint, request, jsonify, current_app, redirect, session, url_for
from api.middleware.auth_middleware import (
    require_auth, require_role, get_current_user, get_user_id, 
    get_user_roles, get_user_permissions, is_admin
)
from api.models.user import User
from config.auth_config import auth0_client, Auth0Config
import logging
from urllib.parse import urlencode
import secrets

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route('/login', methods=['GET'])
def login():
    """Initiate Auth0 login flow"""
    try:
        # Generate state parameter for CSRF protection
        state = secrets.token_urlsafe(32)
        session['auth_state'] = state
        
        # Build Auth0 authorization URL
        params = {
            'client_id': Auth0Config.CLIENT_ID,
            'response_type': 'code',
            'scope': 'openid profile email',
            'redirect_uri': Auth0Config.CALLBACK_URL,
            'state': state,
            'audience': Auth0Config.AUDIENCE
        }
        
        auth_url = f"https://{Auth0Config.DOMAIN}/authorize?" + urlencode(params)
        
        logger.info("Initiating Auth0 login flow")
        
        return jsonify({
            'success': True,
            'auth_url': auth_url,
            'state': state
        }), 200
        
    except Exception as e:
        logger.error(f"Login initiation error: {str(e)}")
        return jsonify({'error': 'Failed to initiate login'}), 500


@auth_bp.route('/callback', methods=['GET'])
def callback():
    """Handle Auth0 callback"""
    try:
        # Verify state parameter
        state = request.args.get('state')
        if not state or state != session.get('auth_state'):
            return jsonify({'error': 'Invalid state parameter'}), 400
        
        # Get authorization code
        code = request.args.get('code')
        if not code:
            error = request.args.get('error')
            error_description = request.args.get('error_description')
            logger.error(f"Auth0 callback error: {error} - {error_description}")
            return jsonify({
                'error': 'Authorization failed',
                'details': error_description
            }), 400
        
        # Exchange code for tokens
        token_data = auth0_client.exchange_code_for_token(code, Auth0Config.CALLBACK_URL)
        
        if not token_data:
            return jsonify({'error': 'Failed to exchange code for token'}), 400
        
        access_token = token_data.get('access_token')
        id_token = token_data.get('id_token')
        
        logger.info("Successfully completed Auth0 callback")
        
        return jsonify({
            'success': True,
            'access_token': access_token,
            'id_token': id_token,
            'token_type': 'Bearer',
            'expires_in': token_data.get('expires_in', 3600)
        }), 200
        
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        return jsonify({'error': 'Authentication callback failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
@require_auth()
def logout():
    """Handle user logout with Auth0"""
    try:
        user = get_current_user()
        user_id = get_user_id()
        
        logger.info(f"User logout: {user_id}")
        
        # Build Auth0 logout URL
        params = {
            'client_id': Auth0Config.CLIENT_ID,
            'returnTo': Auth0Config.LOGOUT_URL
        }
        
        logout_url = f"https://{Auth0Config.DOMAIN}/v2/logout?" + urlencode(params)
        
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully',
            'logout_url': logout_url
        }), 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500


@auth_bp.route('/profile', methods=['GET'])
@require_auth()
def get_profile():
    """Get current user profile"""
    try:
        user = get_current_user()
        
        return jsonify({
            'success': True,
            'user': user
        }), 200
        
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Failed to get profile'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@require_auth()
def update_profile():
    """Update user profile"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # In real implementation, update user profile in database
        logger.info(f"Profile update for user: {user.get('username', 'unknown')}")
        
        # Mock updated profile
        updated_user = user.copy()
        updated_user.update({
            'email': data.get('email', user.get('email')),
            'display_name': data.get('display_name', user.get('display_name'))
        })
        
        return jsonify({
            'success': True,
            'user': updated_user,
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Failed to update profile'}), 500


@auth_bp.route('/change-password', methods=['POST'])
@require_auth()
def change_password():
    """Change user password"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new password required'}), 400
        
        # In real implementation, validate current password and update
        logger.info(f"Password change for user: {user.get('username', 'unknown')}")
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        return jsonify({'error': 'Failed to change password'}), 500


@auth_bp.route('/refresh', methods=['POST'])
@require_auth()
def refresh_token():
    """Refresh authentication token"""
    try:
        user = get_current_user()
        
        # In real implementation, generate new JWT token
        new_token = 'mock_refreshed_jwt_token_67890'
        
        logger.info(f"Token refresh for user: {user.get('username', 'unknown')}")
        
        return jsonify({
            'success': True,
            'token': new_token,
            'expires_in': 3600
        }), 200
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Failed to refresh token'}), 500


@auth_bp.route('/validate', methods=['GET'])
@require_auth()
def validate_token():
    """Validate current authentication token"""
    try:
        user = get_current_user()
        
        return jsonify({
            'success': True,
            'valid': True,
            'user': {
                'id': get_user_id(),
                'email': user.get('email'),
                'name': user.get('name'),
                'roles': get_user_roles(),
                'permissions': get_user_permissions(),
                'tenant_id': user.get('tenant_id')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        return jsonify({'error': 'Token validation failed'}), 500


@auth_bp.route('/users', methods=['GET'])
@require_auth('manage:users')
def list_users():
    """List all users (admin only)"""
    try:
        # In real implementation, fetch from database or Auth0 Management API
        # For now, return mock data
        
        users = [
            {
                'id': 'auth0|user_123',
                'email': 'analyst1@example.com',
                'name': 'Test Analyst',
                'roles': ['analyst'],
                'tenant_id': 'tenant_123',
                'created_at': '2024-01-01T00:00:00Z',
                'last_login': '2024-01-15T10:30:00Z',
                'active': True
            },
            {
                'id': 'auth0|admin_1',
                'email': 'admin@example.com',
                'name': 'Test Admin',
                'roles': ['admin'],
                'tenant_id': 'tenant_123',
                'created_at': '2024-01-01T00:00:00Z',
                'last_login': '2024-01-15T11:00:00Z',
                'active': True
            }
        ]
        
        logger.info(f"Admin {get_user_id()} listed users")
        
        return jsonify({
            'success': True,
            'users': users,
            'total': len(users)
        }), 200
        
    except Exception as e:
        logger.error(f"List users error: {str(e)}")
        return jsonify({'error': 'Failed to list users'}), 500


@auth_bp.route('/users/<user_id>/roles', methods=['PUT'])
@require_auth('manage:users')
def update_user_roles(user_id):
    """Update user roles (admin only)"""
    try:
        data = request.get_json()
        
        if not data or 'roles' not in data:
            return jsonify({'error': 'Roles data required'}), 400
        
        new_roles = data['roles']
        
        # Validate roles
        valid_roles = list(Auth0Config.ROLES.keys())
        for role in new_roles:
            if role not in valid_roles:
                return jsonify({
                    'error': f'Invalid role: {role}',
                    'valid_roles': valid_roles
                }), 400
        
        # In real implementation, update user roles in Auth0 Management API
        logger.info(f"Admin {get_user_id()} updated roles for user {user_id}: {new_roles}")
        
        return jsonify({
            'success': True,
            'message': 'User roles updated successfully',
            'user_id': user_id,
            'roles': new_roles
        }), 200
        
    except Exception as e:
        logger.error(f"Update user roles error: {str(e)}")
        return jsonify({'error': 'Failed to update user roles'}), 500


@auth_bp.route('/users/<user_id>/status', methods=['PUT'])
@require_auth('manage:users')
def update_user_status(user_id):
    """Update user status (admin only)"""
    try:
        data = request.get_json()
        
        if not data or 'active' not in data:
            return jsonify({'error': 'Status data required'}), 400
        
        active = data['active']
        
        # In real implementation, update user status in Auth0 Management API
        logger.info(f"Admin {get_user_id()} updated status for user {user_id}: active={active}")
        
        return jsonify({
            'success': True,
            'message': 'User status updated successfully',
            'user_id': user_id,
            'active': active
        }), 200
        
    except Exception as e:
        logger.error(f"Update user status error: {str(e)}")
        return jsonify({'error': 'Failed to update user status'}), 500


@auth_bp.route('/permissions', methods=['GET'])
@require_auth()
def get_permissions():
    """Get available permissions and current user permissions"""
    try:
        user_permissions = get_user_permissions()
        user_roles = get_user_roles()
        
        return jsonify({
            'success': True,
            'user_permissions': user_permissions,
            'user_roles': user_roles,
            'available_permissions': Auth0Config.SCOPES,
            'available_roles': Auth0Config.ROLES,
            'is_admin': is_admin()
        }), 200
        
    except Exception as e:
        logger.error(f"Get permissions error: {str(e)}")
        return jsonify({'error': 'Failed to get permissions'}), 500