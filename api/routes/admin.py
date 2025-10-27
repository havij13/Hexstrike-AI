"""
Admin Routes

This module handles administrative API endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from api.middleware.auth_middleware import require_auth, require_role
from api.models.user import User
import logging

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)


@admin_bp.route('/users', methods=['GET'])
@require_auth()
@require_role('admin')
def list_users():
    """List all users (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        
        # Mock user data
        users = [
            {
                'id': 'user_1',
                'username': 'analyst1',
                'email': 'analyst1@example.com',
                'role': 'analyst',
                'status': 'active',
                'created_at': '2024-01-10T09:00:00Z',
                'last_login': '2024-01-15T14:30:00Z'
            },
            {
                'id': 'user_2',
                'username': 'viewer1',
                'email': 'viewer1@example.com',
                'role': 'viewer',
                'status': 'active',
                'created_at': '2024-01-12T11:15:00Z',
                'last_login': '2024-01-15T10:45:00Z'
            }
        ]
        
        # Apply search filter
        if search:
            users = [u for u in users if search.lower() in u['username'].lower() or search.lower() in u['email'].lower()]
        
        return jsonify({
            'success': True,
            'users': users,
            'total': len(users),
            'page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        logger.error(f"List users error: {str(e)}")
        return jsonify({'error': 'Failed to list users'}), 500


@admin_bp.route('/users', methods=['POST'])
@require_auth()
@require_role('admin')
def create_user():
    """Create a new user (admin only)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        email = data.get('email')
        role = data.get('role', 'viewer')
        
        if not username or not email:
            return jsonify({'error': 'Username and email are required'}), 400
        
        # In real implementation, create user in database
        user_data = {
            'id': f'user_{len([1,2,3]) + 1}',  # Mock ID generation
            'username': username,
            'email': email,
            'role': role,
            'status': 'active',
            'created_at': '2024-01-15T15:00:00Z'
        }
        
        logger.info(f"Created user {username} with role {role}")
        
        return jsonify({
            'success': True,
            'user': user_data,
            'message': 'User created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Create user error: {str(e)}")
        return jsonify({'error': 'Failed to create user'}), 500


@admin_bp.route('/users/<user_id>', methods=['GET'])
@require_auth()
@require_role('admin')
def get_user(user_id):
    """Get user details (admin only)"""
    try:
        # Mock user data
        user_data = {
            'id': user_id,
            'username': 'analyst1',
            'email': 'analyst1@example.com',
            'role': 'analyst',
            'status': 'active',
            'created_at': '2024-01-10T09:00:00Z',
            'last_login': '2024-01-15T14:30:00Z',
            'scan_count': 25,
            'last_scan': '2024-01-15T13:45:00Z'
        }
        
        return jsonify({
            'success': True,
            'user': user_data
        }), 200
        
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': 'Failed to get user'}), 500


@admin_bp.route('/users/<user_id>', methods=['PUT'])
@require_auth()
@require_role('admin')
def update_user(user_id):
    """Update user (admin only)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # In real implementation, update user in database
        updated_user = {
            'id': user_id,
            'username': data.get('username', 'analyst1'),
            'email': data.get('email', 'analyst1@example.com'),
            'role': data.get('role', 'analyst'),
            'status': data.get('status', 'active'),
            'updated_at': '2024-01-15T15:30:00Z'
        }
        
        logger.info(f"Updated user {user_id}")
        
        return jsonify({
            'success': True,
            'user': updated_user,
            'message': 'User updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Update user error: {str(e)}")
        return jsonify({'error': 'Failed to update user'}), 500


@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@require_auth()
@require_role('admin')
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        # In real implementation, delete user from database
        logger.info(f"Deleted user {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Delete user error: {str(e)}")
        return jsonify({'error': 'Failed to delete user'}), 500


@admin_bp.route('/system/stats', methods=['GET'])
@require_auth()
@require_role('admin')
def get_system_stats():
    """Get system statistics (admin only)"""
    try:
        # Mock system statistics
        stats = {
            'users': {
                'total': 150,
                'active': 142,
                'inactive': 8,
                'new_this_month': 12
            },
            'scans': {
                'total': 2847,
                'completed': 2650,
                'running': 15,
                'failed': 182,
                'today': 45
            },
            'vulnerabilities': {
                'total': 1523,
                'critical': 23,
                'high': 156,
                'medium': 487,
                'low': 857
            },
            'system': {
                'uptime': '15 days, 8 hours',
                'cpu_usage': 45.2,
                'memory_usage': 68.7,
                'disk_usage': 34.1,
                'active_processes': 12
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Get system stats error: {str(e)}")
        return jsonify({'error': 'Failed to get system stats'}), 500


@admin_bp.route('/system/health', methods=['GET'])
@require_auth()
@require_role('admin')
def get_system_health():
    """Get system health status (admin only)"""
    try:
        # Mock health check
        health = {
            'status': 'healthy',
            'timestamp': '2024-01-15T15:45:00Z',
            'services': {
                'database': {'status': 'healthy', 'response_time': 12},
                'redis': {'status': 'healthy', 'response_time': 3},
                'auth_service': {'status': 'healthy', 'response_time': 45},
                'tool_registry': {'status': 'healthy', 'tools_available': 25}
            },
            'metrics': {
                'requests_per_minute': 127,
                'average_response_time': 245,
                'error_rate': 0.02
            }
        }
        
        return jsonify({
            'success': True,
            'health': health
        }), 200
        
    except Exception as e:
        logger.error(f"Get system health error: {str(e)}")
        return jsonify({'error': 'Failed to get system health'}), 500


@admin_bp.route('/system/logs', methods=['GET'])
@require_auth()
@require_role('admin')
def get_system_logs():
    """Get system logs (admin only)"""
    try:
        level = request.args.get('level', 'INFO')
        limit = request.args.get('limit', 100, type=int)
        
        # Mock log entries
        logs = [
            {
                'timestamp': '2024-01-15T15:44:32Z',
                'level': 'INFO',
                'message': 'Scan completed successfully for target example.com',
                'user': 'analyst1',
                'scan_id': 'scan_789'
            },
            {
                'timestamp': '2024-01-15T15:43:15Z',
                'level': 'WARNING',
                'message': 'Rate limit exceeded for user viewer1',
                'user': 'viewer1',
                'ip': '192.168.1.100'
            },
            {
                'timestamp': '2024-01-15T15:42:01Z',
                'level': 'ERROR',
                'message': 'Tool execution failed: nuclei timeout',
                'tool': 'nuclei',
                'target': 'slow-site.com'
            }
        ]
        
        # Filter by level
        if level != 'ALL':
            logs = [log for log in logs if log['level'] == level]
        
        # Apply limit
        logs = logs[:limit]
        
        return jsonify({
            'success': True,
            'logs': logs,
            'total': len(logs)
        }), 200
        
    except Exception as e:
        logger.error(f"Get system logs error: {str(e)}")
        return jsonify({'error': 'Failed to get system logs'}), 500


@admin_bp.route('/tenants', methods=['GET'])
@require_auth()
@require_role('admin')
def list_tenants():
    """List all tenants (admin only)"""
    try:
        # Mock tenant data
        tenants = [
            {
                'id': 'tenant_1',
                'name': 'Acme Corporation',
                'domain': 'acme.com',
                'status': 'active',
                'user_count': 25,
                'scan_count': 450,
                'created_at': '2024-01-01T00:00:00Z'
            },
            {
                'id': 'tenant_2',
                'name': 'Beta Security',
                'domain': 'betasec.com',
                'status': 'active',
                'user_count': 12,
                'scan_count': 180,
                'created_at': '2024-01-05T10:30:00Z'
            }
        ]
        
        return jsonify({
            'success': True,
            'tenants': tenants,
            'total': len(tenants)
        }), 200
        
    except Exception as e:
        logger.error(f"List tenants error: {str(e)}")
        return jsonify({'error': 'Failed to list tenants'}), 500