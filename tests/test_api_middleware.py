"""
Tests for API Middleware

This module contains unit tests for the API middleware functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask, g, request
from api.middleware.auth_middleware import (
    get_token_from_header,
    verify_jwt_token,
    has_scope,
    require_auth,
    require_role,
    get_current_user,
    get_user_tenant_id,
    is_admin,
    can_access_tenant,
    MOCK_USERS
)


class TestAuthMiddleware:
    """Test cases for authentication middleware"""

    @pytest.fixture
    def app(self):
        """Create test Flask app"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['DEBUG_MODE'] = True
        return app

    def test_get_token_from_header_valid(self, app):
        """Test extracting valid token from header"""
        with app.test_request_context(headers={'Authorization': 'Bearer test_token_123'}):
            token = get_token_from_header()
            assert token == 'test_token_123'

    def test_get_token_from_header_no_header(self, app):
        """Test extracting token when no header present"""
        with app.test_request_context():
            token = get_token_from_header()
            assert token is None

    def test_get_token_from_header_invalid_format(self, app):
        """Test extracting token with invalid format"""
        with app.test_request_context(headers={'Authorization': 'InvalidFormat token'}):
            token = get_token_from_header()
            assert token is None

    def test_get_token_from_header_missing_token(self, app):
        """Test extracting token when Bearer keyword only"""
        with app.test_request_context(headers={'Authorization': 'Bearer'}):
            token = get_token_from_header()
            assert token is None

    def test_verify_jwt_token_valid_mock(self, app):
        """Test JWT token verification with valid mock token"""
        with app.app_context():
            payload = verify_jwt_token('mock_jwt_token_12345')
            
            assert payload is not None
            assert payload['user_id'] == 'user_123'
            assert payload['username'] == 'analyst1'
            assert 'analyst' in payload['roles']

    def test_verify_jwt_token_invalid(self, app):
        """Test JWT token verification with invalid token"""
        with app.app_context():
            payload = verify_jwt_token('invalid_token')
            
            assert payload is None

    def test_verify_jwt_token_admin(self, app):
        """Test JWT token verification for admin user"""
        with app.app_context():
            payload = verify_jwt_token('admin_token_67890')
            
            assert payload is not None
            assert payload['user_id'] == 'admin_1'
            assert 'admin' in payload['roles']

    def test_has_scope_admin_user(self):
        """Test scope checking for admin user"""
        admin_payload = {
            'user_id': 'admin_1',
            'roles': ['admin']
        }
        
        # Admin should have all scopes
        assert has_scope(admin_payload, 'read:scans') is True
        assert has_scope(admin_payload, 'write:scans') is True
        assert has_scope(admin_payload, 'manage:users') is True

    def test_has_scope_analyst_user(self):
        """Test scope checking for analyst user"""
        analyst_payload = {
            'user_id': 'user_123',
            'roles': ['analyst']
        }
        
        # Analyst should have read/write scans but not manage users
        assert has_scope(analyst_payload, 'read:scans') is True
        assert has_scope(analyst_payload, 'write:scans') is True
        assert has_scope(analyst_payload, 'manage:users') is False

    def test_has_scope_viewer_user(self):
        """Test scope checking for viewer user"""
        viewer_payload = {
            'user_id': 'user_456',
            'roles': ['viewer']
        }
        
        # Viewer should only have read access
        assert has_scope(viewer_payload, 'read:scans') is True
        assert has_scope(viewer_payload, 'write:scans') is False
        assert has_scope(viewer_payload, 'manage:users') is False

    def test_has_scope_no_payload(self):
        """Test scope checking with no user payload"""
        assert has_scope(None, 'read:scans') is False

    def test_has_scope_unknown_scope(self):
        """Test scope checking with unknown scope"""
        user_payload = {
            'user_id': 'user_123',
            'roles': ['analyst']
        }
        
        # Unknown scope should default to no access
        assert has_scope(user_payload, 'unknown:scope') is False

    def test_require_auth_decorator_valid_token(self, app):
        """Test require_auth decorator with valid token"""
        @require_auth()
        def test_route():
            return {'success': True}
        
        with app.test_request_context(headers={'Authorization': 'Bearer mock_jwt_token_12345'}):
            result = test_route()
            
            assert result == {'success': True}
            assert hasattr(g, 'current_user')
            assert g.current_user['username'] == 'analyst1'

    def test_require_auth_decorator_no_token(self, app):
        """Test require_auth decorator without token"""
        @require_auth()
        def test_route():
            return {'success': True}
        
        with app.test_request_context():
            result = test_route()
            
            # Should return 401 error
            assert isinstance(result, tuple)
            assert result[1] == 401
            assert 'error' in result[0].get_json()

    def test_require_auth_decorator_invalid_token(self, app):
        """Test require_auth decorator with invalid token"""
        @require_auth()
        def test_route():
            return {'success': True}
        
        with app.test_request_context(headers={'Authorization': 'Bearer invalid_token'}):
            result = test_route()
            
            # Should return 401 error
            assert isinstance(result, tuple)
            assert result[1] == 401

    def test_require_auth_decorator_with_scope(self, app):
        """Test require_auth decorator with scope requirement"""
        @require_auth('read:scans')
        def test_route():
            return {'success': True}
        
        with app.test_request_context(headers={'Authorization': 'Bearer mock_jwt_token_12345'}):
            result = test_route()
            
            assert result == {'success': True}

    def test_require_auth_decorator_insufficient_scope(self, app):
        """Test require_auth decorator with insufficient scope"""
        @require_auth('manage:users')
        def test_route():
            return {'success': True}
        
        # Analyst doesn't have manage:users scope
        with app.test_request_context(headers={'Authorization': 'Bearer mock_jwt_token_12345'}):
            result = test_route()
            
            # Should return 403 error
            assert isinstance(result, tuple)
            assert result[1] == 403

    def test_require_role_decorator_valid_role(self, app):
        """Test require_role decorator with valid role"""
        @require_role('analyst')
        def test_route():
            return {'success': True}
        
        with app.test_request_context(headers={'Authorization': 'Bearer mock_jwt_token_12345'}):
            # Set up g.current_user
            g.current_user = MOCK_USERS['mock_jwt_token_12345']
            
            result = test_route()
            
            assert result == {'success': True}

    def test_require_role_decorator_admin_access(self, app):
        """Test require_role decorator - admin can access any role"""
        @require_role('analyst')
        def test_route():
            return {'success': True}
        
        with app.test_request_context():
            # Set up admin user
            g.current_user = MOCK_USERS['admin_token_67890']
            
            result = test_route()
            
            assert result == {'success': True}

    def test_require_role_decorator_insufficient_role(self, app):
        """Test require_role decorator with insufficient role"""
        @require_role('admin')
        def test_route():
            return {'success': True}
        
        with app.test_request_context():
            # Set up analyst user (not admin)
            g.current_user = MOCK_USERS['mock_jwt_token_12345']
            
            result = test_route()
            
            # Should return 403 error
            assert isinstance(result, tuple)
            assert result[1] == 403

    def test_require_role_decorator_no_user(self, app):
        """Test require_role decorator without authenticated user"""
        @require_role('analyst')
        def test_route():
            return {'success': True}
        
        with app.test_request_context():
            # No user in g
            result = test_route()
            
            # Should return 401 error
            assert isinstance(result, tuple)
            assert result[1] == 401

    def test_get_current_user_with_user(self, app):
        """Test getting current user when user is set"""
        with app.test_request_context():
            g.current_user = MOCK_USERS['mock_jwt_token_12345']
            
            user = get_current_user()
            
            assert user is not None
            assert user['username'] == 'analyst1'

    def test_get_current_user_no_user(self, app):
        """Test getting current user when no user is set"""
        with app.test_request_context():
            user = get_current_user()
            
            assert user is None

    def test_get_user_tenant_id_with_user(self, app):
        """Test getting user tenant ID when user is set"""
        with app.test_request_context():
            g.current_user = MOCK_USERS['mock_jwt_token_12345']
            
            tenant_id = get_user_tenant_id()
            
            assert tenant_id == 'tenant_123'

    def test_get_user_tenant_id_no_user(self, app):
        """Test getting user tenant ID when no user is set"""
        with app.test_request_context():
            tenant_id = get_user_tenant_id()
            
            assert tenant_id is None

    def test_is_admin_true(self, app):
        """Test is_admin function with admin user"""
        with app.test_request_context():
            g.current_user = MOCK_USERS['admin_token_67890']
            
            assert is_admin() is True

    def test_is_admin_false(self, app):
        """Test is_admin function with non-admin user"""
        with app.test_request_context():
            g.current_user = MOCK_USERS['mock_jwt_token_12345']
            
            assert is_admin() is False

    def test_is_admin_no_user(self, app):
        """Test is_admin function with no user"""
        with app.test_request_context():
            assert is_admin() is False

    def test_can_access_tenant_same_tenant(self, app):
        """Test tenant access for same tenant"""
        with app.test_request_context():
            g.current_user = MOCK_USERS['mock_jwt_token_12345']
            
            assert can_access_tenant('tenant_123') is True

    def test_can_access_tenant_different_tenant(self, app):
        """Test tenant access for different tenant"""
        with app.test_request_context():
            g.current_user = MOCK_USERS['mock_jwt_token_12345']
            
            assert can_access_tenant('tenant_456') is False

    def test_can_access_tenant_admin_user(self, app):
        """Test tenant access for admin user"""
        with app.test_request_context():
            g.current_user = MOCK_USERS['admin_token_67890']
            
            # Admin can access any tenant
            assert can_access_tenant('tenant_456') is True
            assert can_access_tenant('tenant_789') is True

    def test_can_access_tenant_no_user(self, app):
        """Test tenant access with no user"""
        with app.test_request_context():
            assert can_access_tenant('tenant_123') is False


class TestAuthMiddlewareIntegration:
    """Integration tests for auth middleware"""

    @pytest.fixture
    def app(self):
        """Create test Flask app with routes"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['DEBUG_MODE'] = True
        
        @app.route('/test/public')
        def public_route():
            return {'message': 'public'}
        
        @app.route('/test/protected')
        @require_auth()
        def protected_route():
            user = get_current_user()
            return {'message': 'protected', 'user': user['username']}
        
        @app.route('/test/admin')
        @require_auth('manage:users')
        def admin_route():
            return {'message': 'admin only'}
        
        @app.route('/test/analyst')
        @require_role('analyst')
        def analyst_route():
            return {'message': 'analyst access'}
        
        return app

    def test_public_route_access(self, app):
        """Test access to public route"""
        with app.test_client() as client:
            response = client.get('/test/public')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['message'] == 'public'

    def test_protected_route_with_auth(self, app):
        """Test access to protected route with authentication"""
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer mock_jwt_token_12345'}
            response = client.get('/test/protected', headers=headers)
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['message'] == 'protected'
            assert data['user'] == 'analyst1'

    def test_protected_route_without_auth(self, app):
        """Test access to protected route without authentication"""
        with app.test_client() as client:
            response = client.get('/test/protected')
            
            assert response.status_code == 401
            data = response.get_json()
            assert 'error' in data

    def test_admin_route_with_admin_token(self, app):
        """Test access to admin route with admin token"""
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer admin_token_67890'}
            response = client.get('/test/admin', headers=headers)
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['message'] == 'admin only'

    def test_admin_route_with_analyst_token(self, app):
        """Test access to admin route with analyst token"""
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer mock_jwt_token_12345'}
            response = client.get('/test/admin', headers=headers)
            
            assert response.status_code == 403
            data = response.get_json()
            assert 'error' in data

    def test_analyst_route_with_analyst_token(self, app):
        """Test access to analyst route with analyst token"""
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer mock_jwt_token_12345'}
            
            # Mock the get_current_user function for this test
            with patch('api.middleware.auth_middleware.get_current_user') as mock_get_user:
                mock_get_user.return_value = MOCK_USERS['mock_jwt_token_12345']
                
                response = client.get('/test/analyst', headers=headers)
                
                assert response.status_code == 200
                data = response.get_json()
                assert data['message'] == 'analyst access'

    def test_multiple_decorators(self, app):
        """Test route with multiple auth decorators"""
        @app.route('/test/multi')
        @require_auth('read:scans')
        @require_role('analyst')
        def multi_auth_route():
            return {'message': 'multi auth success'}
        
        with app.test_client() as client:
            headers = {'Authorization': 'Bearer mock_jwt_token_12345'}
            
            with patch('api.middleware.auth_middleware.get_current_user') as mock_get_user:
                mock_get_user.return_value = MOCK_USERS['mock_jwt_token_12345']
                
                response = client.get('/test/multi', headers=headers)
                
                assert response.status_code == 200
                data = response.get_json()
                assert data['message'] == 'multi auth success'