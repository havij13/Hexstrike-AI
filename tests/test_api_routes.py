"""
Tests for API Routes

This module contains unit tests for the API route functionality.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from core.app import create_app
from api.routes.scans import scans_bp
from api.routes.auth import auth_bp


class TestScanRoutes:
    """Test cases for scan routes"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app = create_app(testing=True)
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers"""
        return {
            'Authorization': 'Bearer mock_jwt_token_12345',
            'Content-Type': 'application/json'
        }

    def test_list_scans_success(self, client, auth_headers):
        """Test successful scan listing"""
        response = client.get('/api/scans/', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'scans' in data
        assert 'total' in data
        assert isinstance(data['scans'], list)

    def test_list_scans_unauthorized(self, client):
        """Test scan listing without authentication"""
        response = client.get('/api/scans/')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_create_scan_success(self, client, auth_headers):
        """Test successful scan creation"""
        scan_data = {
            'target': 'example.com',
            'type': 'reconnaissance',
            'parameters': {'timeout': 300}
        }
        
        response = client.post('/api/scans/', 
                             data=json.dumps(scan_data),
                             headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'scan' in data
        assert data['scan']['target'] == 'example.com'
        assert data['scan']['type'] == 'reconnaissance'

    def test_create_scan_missing_target(self, client, auth_headers):
        """Test scan creation without target"""
        scan_data = {
            'type': 'reconnaissance'
        }
        
        response = client.post('/api/scans/', 
                             data=json.dumps(scan_data),
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Target is required' in data['error']

    def test_create_scan_no_data(self, client, auth_headers):
        """Test scan creation without data"""
        response = client.post('/api/scans/', headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'No data provided' in data['error']

    def test_get_scan_success(self, client, auth_headers):
        """Test successful scan retrieval"""
        scan_id = 'test_scan_123'
        
        response = client.get(f'/api/scans/{scan_id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'scan' in data
        assert data['scan']['id'] == scan_id

    def test_start_scan_success(self, client, auth_headers):
        """Test successful scan start"""
        scan_id = 'test_scan_123'
        
        response = client.post(f'/api/scans/{scan_id}/start', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['scan']['status'] == 'running'

    def test_stop_scan_success(self, client, auth_headers):
        """Test successful scan stop"""
        scan_id = 'test_scan_123'
        
        response = client.post(f'/api/scans/{scan_id}/stop', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['scan']['status'] == 'stopped'

    def test_get_scan_results_success(self, client, auth_headers):
        """Test successful scan results retrieval"""
        scan_id = 'test_scan_123'
        
        response = client.get(f'/api/scans/{scan_id}/results', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'results' in data
        assert 'vulnerabilities' in data['results']
        assert 'summary' in data['results']

    def test_delete_scan_success(self, client, auth_headers):
        """Test successful scan deletion"""
        scan_id = 'test_scan_123'
        
        response = client.delete(f'/api/scans/{scan_id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'deleted successfully' in data['message']

    @patch('api.routes.scans.bugbounty_agent')
    def test_create_bugbounty_workflow_success(self, mock_agent, client, auth_headers):
        """Test successful bug bounty workflow creation"""
        # Mock agent response
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = {'workflow': 'reconnaissance', 'phases': []}
        mock_result.message = 'Workflow created'
        mock_agent.execute.return_value = mock_result
        
        workflow_data = {
            'target': 'example.com',
            'workflow_type': 'reconnaissance',
            'priority_vulns': ['rce', 'sqli']
        }
        
        response = client.post('/api/scans/workflows/bugbounty',
                             data=json.dumps(workflow_data),
                             headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'workflow' in data

    def test_create_bugbounty_workflow_missing_target(self, client, auth_headers):
        """Test bug bounty workflow creation without target"""
        workflow_data = {
            'workflow_type': 'reconnaissance'
        }
        
        response = client.post('/api/scans/workflows/bugbounty',
                             data=json.dumps(workflow_data),
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Target is required' in data['error']

    @patch('api.routes.scans.ctf_agent')
    def test_create_ctf_workflow_success(self, mock_agent, client, auth_headers):
        """Test successful CTF workflow creation"""
        # Mock agent response
        mock_result = Mock()
        mock_result.success = True
        mock_result.data = {'challenge': 'web', 'tools': ['sqlmap']}
        mock_result.message = 'CTF workflow created'
        mock_agent.execute.return_value = mock_result
        
        workflow_data = {
            'target': 'https://ctf.example.com/challenge1',
            'challenge_name': 'Web Challenge',
            'category': 'web'
        }
        
        response = client.post('/api/scans/workflows/ctf',
                             data=json.dumps(workflow_data),
                             headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'workflow' in data


class TestAuthRoutes:
    """Test cases for authentication routes"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app = create_app(testing=True)
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers"""
        return {
            'Authorization': 'Bearer mock_jwt_token_12345',
            'Content-Type': 'application/json'
        }

    def test_login_success(self, client):
        """Test successful login"""
        login_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'token' in data
        assert 'user' in data
        assert data['user']['username'] == 'testuser'

    def test_login_missing_credentials(self, client):
        """Test login with missing credentials"""
        login_data = {
            'username': 'testuser'
            # Missing password
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Username and password required' in data['error']

    def test_login_no_data(self, client):
        """Test login without data"""
        response = client.post('/api/auth/login',
                             headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'No data provided' in data['error']

    def test_logout_success(self, client, auth_headers):
        """Test successful logout"""
        response = client.post('/api/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'Logged out successfully' in data['message']

    def test_logout_unauthorized(self, client):
        """Test logout without authentication"""
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_get_profile_success(self, client, auth_headers):
        """Test successful profile retrieval"""
        response = client.get('/api/auth/profile', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'user' in data
        assert data['user']['username'] == 'analyst1'

    def test_update_profile_success(self, client, auth_headers):
        """Test successful profile update"""
        profile_data = {
            'email': 'newemail@example.com',
            'display_name': 'New Display Name'
        }
        
        response = client.put('/api/auth/profile',
                            data=json.dumps(profile_data),
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['email'] == 'newemail@example.com'

    def test_update_profile_no_data(self, client, auth_headers):
        """Test profile update without data"""
        response = client.put('/api/auth/profile', headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'No data provided' in data['error']

    def test_change_password_success(self, client, auth_headers):
        """Test successful password change"""
        password_data = {
            'current_password': 'oldpass',
            'new_password': 'newpass123'
        }
        
        response = client.post('/api/auth/change-password',
                             data=json.dumps(password_data),
                             headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'Password changed successfully' in data['message']

    def test_change_password_missing_data(self, client, auth_headers):
        """Test password change with missing data"""
        password_data = {
            'current_password': 'oldpass'
            # Missing new_password
        }
        
        response = client.post('/api/auth/change-password',
                             data=json.dumps(password_data),
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'Current and new password required' in data['error']

    def test_refresh_token_success(self, client, auth_headers):
        """Test successful token refresh"""
        response = client.post('/api/auth/refresh', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'token' in data
        assert 'expires_in' in data

    def test_validate_token_success(self, client, auth_headers):
        """Test successful token validation"""
        response = client.get('/api/auth/validate', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['valid'] is True
        assert 'user' in data


class TestAPIErrorHandling:
    """Test cases for API error handling"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app = create_app(testing=True)
        with app.test_client() as client:
            yield client

    def test_404_error_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/api/nonexistent-endpoint')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'Resource not found' in data['error']

    def test_method_not_allowed(self, client):
        """Test method not allowed error"""
        # Try to POST to a GET-only endpoint
        response = client.post('/api/auth/profile')
        
        assert response.status_code in [401, 405]  # 401 for auth, 405 for method

    @patch('api.routes.scans.decision_engine')
    def test_internal_server_error_handling(self, mock_engine, client):
        """Test internal server error handling"""
        # Mock an exception in the decision engine
        mock_engine.analyze_target.side_effect = Exception("Test error")
        
        auth_headers = {
            'Authorization': 'Bearer mock_jwt_token_12345',
            'Content-Type': 'application/json'
        }
        
        scan_data = {
            'target': 'example.com',
            'type': 'reconnaissance'
        }
        
        response = client.post('/api/scans/',
                             data=json.dumps(scan_data),
                             headers=auth_headers)
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data


class TestAPIValidation:
    """Test cases for API input validation"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app = create_app(testing=True)
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def auth_headers(self):
        """Mock authentication headers"""
        return {
            'Authorization': 'Bearer mock_jwt_token_12345',
            'Content-Type': 'application/json'
        }

    def test_invalid_json_data(self, client, auth_headers):
        """Test handling of invalid JSON data"""
        response = client.post('/api/scans/',
                             data='invalid json',
                             headers=auth_headers)
        
        # Should handle gracefully, either 400 or 500
        assert response.status_code in [400, 500]

    def test_empty_target_validation(self, client, auth_headers):
        """Test validation of empty target"""
        scan_data = {
            'target': '',
            'type': 'reconnaissance'
        }
        
        response = client.post('/api/scans/',
                             data=json.dumps(scan_data),
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_whitespace_only_target(self, client, auth_headers):
        """Test validation of whitespace-only target"""
        scan_data = {
            'target': '   ',
            'type': 'reconnaissance'
        }
        
        response = client.post('/api/scans/',
                             data=json.dumps(scan_data),
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_missing_content_type(self, client):
        """Test request without content type"""
        auth_headers = {
            'Authorization': 'Bearer mock_jwt_token_12345'
            # Missing Content-Type
        }
        
        scan_data = {
            'target': 'example.com',
            'type': 'reconnaissance'
        }
        
        response = client.post('/api/scans/',
                             data=json.dumps(scan_data),
                             headers=auth_headers)
        
        # Should still work or return appropriate error
        assert response.status_code in [200, 201, 400, 415]