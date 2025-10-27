"""
Tests for Auth0 Configuration

This module contains unit tests for Auth0 configuration and client functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
from config.auth_config import Auth0Config, Auth0Client


class TestAuth0Config:
    """Test cases for Auth0 configuration"""

    def test_get_role_permissions_admin(self):
        """Test getting permissions for admin role"""
        permissions = Auth0Config.get_role_permissions('admin')
        
        assert 'read:all' in permissions
        assert 'write:all' in permissions
        assert 'delete:all' in permissions
        assert 'manage:users' in permissions
        assert 'manage:tenants' in permissions
        assert 'manage:system' in permissions

    def test_get_role_permissions_analyst(self):
        """Test getting permissions for analyst role"""
        permissions = Auth0Config.get_role_permissions('analyst')
        
        assert 'read:scans' in permissions
        assert 'write:scans' in permissions
        assert 'read:tools' in permissions
        assert 'write:tools' in permissions
        assert 'read:vulnerabilities' in permissions
        
        # Should not have admin permissions
        assert 'manage:users' not in permissions
        assert 'delete:all' not in permissions

    def test_get_role_permissions_viewer(self):
        """Test getting permissions for viewer role"""
        permissions = Auth0Config.get_role_permissions('viewer')
        
        assert 'read:scans' in permissions
        assert 'read:results' in permissions
        assert 'read:vulnerabilities' in permissions
        
        # Should not have write permissions
        assert 'write:scans' not in permissions
        assert 'write:tools' not in permissions

    def test_get_role_permissions_invalid_role(self):
        """Test getting permissions for invalid role"""
        permissions = Auth0Config.get_role_permissions('invalid_role')
        
        assert permissions == []

    def test_has_permission_admin_role(self):
        """Test permission checking for admin role"""
        user_roles = ['admin']
        
        assert Auth0Config.has_permission(user_roles, 'read:all') is True
        assert Auth0Config.has_permission(user_roles, 'manage:users') is True
        assert Auth0Config.has_permission(user_roles, 'delete:all') is True

    def test_has_permission_analyst_role(self):
        """Test permission checking for analyst role"""
        user_roles = ['analyst']
        
        assert Auth0Config.has_permission(user_roles, 'read:scans') is True
        assert Auth0Config.has_permission(user_roles, 'write:scans') is True
        assert Auth0Config.has_permission(user_roles, 'manage:users') is False

    def test_has_permission_multiple_roles(self):
        """Test permission checking with multiple roles"""
        user_roles = ['viewer', 'analyst']
        
        assert Auth0Config.has_permission(user_roles, 'read:scans') is True
        assert Auth0Config.has_permission(user_roles, 'write:scans') is True
        assert Auth0Config.has_permission(user_roles, 'manage:users') is False

    def test_has_permission_no_roles(self):
        """Test permission checking with no roles"""
        user_roles = []
        
        assert Auth0Config.has_permission(user_roles, 'read:scans') is False

    @patch.dict(os.environ, {
        'AUTH0_DOMAIN': 'test.auth0.com',
        'AUTH0_CLIENT_ID': 'test_client_id',
        'AUTH0_CLIENT_SECRET': 'test_client_secret'
    })
    def test_validate_config_success(self):
        """Test successful config validation"""
        # Should not raise exception
        assert Auth0Config.validate_config() is True

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_config_missing_domain(self):
        """Test config validation with missing domain"""
        with pytest.raises(ValueError, match="AUTH0_DOMAIN"):
            Auth0Config.validate_config()

    @patch.dict(os.environ, {
        'AUTH0_DOMAIN': 'test.auth0.com'
    }, clear=True)
    def test_validate_config_missing_client_id(self):
        """Test config validation with missing client ID"""
        with pytest.raises(ValueError, match="AUTH0_CLIENT_ID"):
            Auth0Config.validate_config()

    @patch.dict(os.environ, {
        'AUTH0_DOMAIN': 'test.auth0.com',
        'AUTH0_CLIENT_ID': 'test_client_id'
    }, clear=True)
    def test_validate_config_missing_client_secret(self):
        """Test config validation with missing client secret"""
        with pytest.raises(ValueError, match="AUTH0_CLIENT_SECRET"):
            Auth0Config.validate_config()


class TestAuth0Client:
    """Test cases for Auth0 client"""

    @pytest.fixture
    def mock_flask_app(self):
        """Create mock Flask app"""
        app = Mock()
        app.config = {}
        return app

    @patch('config.auth_config.OAuth')
    def test_init_app(self, mock_oauth, mock_flask_app):
        """Test Auth0 client initialization with Flask app"""
        mock_oauth_instance = Mock()
        mock_oauth.return_value = mock_oauth_instance
        
        mock_auth0_client = Mock()
        mock_oauth_instance.register.return_value = mock_auth0_client
        
        client = Auth0Client()
        result = client.init_app(mock_flask_app)
        
        # Verify OAuth was initialized
        mock_oauth_instance.init_app.assert_called_once_with(mock_flask_app)
        
        # Verify Auth0 client was registered
        mock_oauth_instance.register.assert_called_once()
        
        # Verify return value
        assert result == mock_auth0_client
        assert client.auth0 == mock_auth0_client

    def test_get_authorization_url_no_client(self):
        """Test getting authorization URL without initialized client"""
        client = Auth0Client()
        
        with pytest.raises(RuntimeError, match="Auth0 client not initialized"):
            client.get_authorization_url("http://localhost:8888/callback")

    def test_exchange_code_for_token_no_client(self):
        """Test exchanging code for token without initialized client"""
        client = Auth0Client()
        
        with pytest.raises(RuntimeError, match="Auth0 client not initialized"):
            client.exchange_code_for_token("test_code", "http://localhost:8888/callback")

    @patch('config.auth_config.OAuth')
    def test_get_authorization_url_success(self, mock_oauth, mock_flask_app):
        """Test successful authorization URL generation"""
        mock_oauth_instance = Mock()
        mock_oauth.return_value = mock_oauth_instance
        
        mock_auth0_client = Mock()
        mock_auth0_client.authorize_redirect.return_value = "https://test.auth0.com/authorize?..."
        mock_oauth_instance.register.return_value = mock_auth0_client
        
        client = Auth0Client()
        client.init_app(mock_flask_app)
        
        redirect_uri = "http://localhost:8888/callback"
        result = client.get_authorization_url(redirect_uri)
        
        mock_auth0_client.authorize_redirect.assert_called_once_with(redirect_uri)
        assert result == "https://test.auth0.com/authorize?..."

    @patch('config.auth_config.OAuth')
    def test_exchange_code_for_token_success(self, mock_oauth, mock_flask_app):
        """Test successful code exchange for token"""
        mock_oauth_instance = Mock()
        mock_oauth.return_value = mock_oauth_instance
        
        mock_auth0_client = Mock()
        token_data = {
            'access_token': 'test_access_token',
            'id_token': 'test_id_token',
            'expires_in': 3600
        }
        mock_auth0_client.authorize_access_token.return_value = token_data
        mock_oauth_instance.register.return_value = mock_auth0_client
        
        client = Auth0Client()
        client.init_app(mock_flask_app)
        
        code = "test_authorization_code"
        redirect_uri = "http://localhost:8888/callback"
        result = client.exchange_code_for_token(code, redirect_uri)
        
        mock_auth0_client.authorize_access_token.assert_called_once_with(redirect_uri=redirect_uri)
        assert result == token_data


class TestAuth0Integration:
    """Integration tests for Auth0 functionality"""

    @patch.dict(os.environ, {
        'AUTH0_DOMAIN': 'test.auth0.com',
        'AUTH0_CLIENT_ID': 'test_client_id',
        'AUTH0_CLIENT_SECRET': 'test_client_secret',
        'AUTH0_AUDIENCE': 'https://test-api.com'
    })
    def test_environment_configuration(self):
        """Test Auth0 configuration from environment variables"""
        # Reload the config to pick up environment variables
        from importlib import reload
        import config.auth_config
        reload(config.auth_config)
        
        assert config.auth_config.Auth0Config.DOMAIN == 'test.auth0.com'
        assert config.auth_config.Auth0Config.CLIENT_ID == 'test_client_id'
        assert config.auth_config.Auth0Config.CLIENT_SECRET == 'test_client_secret'
        assert config.auth_config.Auth0Config.AUDIENCE == 'https://test-api.com'

    def test_role_hierarchy(self):
        """Test role hierarchy and permission inheritance"""
        # Admin should have all permissions
        admin_permissions = Auth0Config.get_role_permissions('admin')
        analyst_permissions = Auth0Config.get_role_permissions('analyst')
        viewer_permissions = Auth0Config.get_role_permissions('viewer')
        
        # Admin should have more permissions than analyst
        assert len(admin_permissions) > len(analyst_permissions)
        
        # Analyst should have more permissions than viewer
        assert len(analyst_permissions) > len(viewer_permissions)
        
        # All viewer permissions should be available to analyst
        for permission in viewer_permissions:
            assert Auth0Config.has_permission(['analyst'], permission)
        
        # All analyst permissions should be available to admin
        for permission in analyst_permissions:
            assert Auth0Config.has_permission(['admin'], permission)

    def test_permission_scopes_completeness(self):
        """Test that all defined scopes are covered by roles"""
        all_scopes = set(Auth0Config.SCOPES.keys())
        
        # Collect all permissions from all roles
        all_role_permissions = set()
        for role_permissions in Auth0Config.ROLES.values():
            all_role_permissions.update(role_permissions)
        
        # Check that all scopes are covered by at least one role
        uncovered_scopes = all_scopes - all_role_permissions
        
        # Some scopes might be intentionally not assigned to any role
        # but core scopes should be covered
        core_scopes = {'read:scans', 'write:scans', 'read:tools', 'manage:users'}
        uncovered_core_scopes = core_scopes - all_role_permissions
        
        assert len(uncovered_core_scopes) == 0, f"Core scopes not covered: {uncovered_core_scopes}"