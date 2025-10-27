"""
Webhook Routes

This module handles webhook-related API endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from api.middleware.auth_middleware import require_auth, get_current_user
import logging
import uuid
from datetime import datetime

webhooks_bp = Blueprint('webhooks', __name__)
logger = logging.getLogger(__name__)


@webhooks_bp.route('/', methods=['GET'])
@require_auth()
def list_webhooks():
    """List user's webhooks"""
    try:
        user = get_current_user()
        
        # Mock webhook data
        webhooks = [
            {
                'id': 'webhook_1',
                'name': 'Slack Notifications',
                'url': 'https://hooks.slack.com/services/...',
                'events': ['scan.completed', 'vulnerability.found'],
                'active': True,
                'created_at': '2024-01-10T12:00:00Z',
                'last_triggered': '2024-01-15T14:30:00Z',
                'delivery_count': 45
            },
            {
                'id': 'webhook_2',
                'name': 'SIEM Integration',
                'url': 'https://siem.company.com/api/events',
                'events': ['vulnerability.found'],
                'active': True,
                'created_at': '2024-01-12T09:15:00Z',
                'last_triggered': '2024-01-15T13:45:00Z',
                'delivery_count': 23
            }
        ]
        
        return jsonify({
            'success': True,
            'webhooks': webhooks,
            'total': len(webhooks)
        }), 200
        
    except Exception as e:
        logger.error(f"List webhooks error: {str(e)}")
        return jsonify({'error': 'Failed to list webhooks'}), 500


@webhooks_bp.route('/', methods=['POST'])
@require_auth()
def create_webhook():
    """Create a new webhook"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        url = data.get('url')
        events = data.get('events', [])
        
        if not name or not url:
            return jsonify({'error': 'Name and URL are required'}), 400
        
        if not events:
            return jsonify({'error': 'At least one event type is required'}), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Validate event types
        valid_events = [
            'scan.started', 'scan.completed', 'scan.failed',
            'vulnerability.found', 'vulnerability.critical',
            'system.alert', 'user.login'
        ]
        
        invalid_events = [e for e in events if e not in valid_events]
        if invalid_events:
            return jsonify({'error': f'Invalid event types: {invalid_events}'}), 400
        
        # Create webhook
        webhook_id = str(uuid.uuid4())
        webhook_data = {
            'id': webhook_id,
            'name': name,
            'url': url,
            'events': events,
            'active': data.get('active', True),
            'secret': data.get('secret', ''),
            'user_id': user.get('user_id'),
            'tenant_id': user.get('tenant_id'),
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'delivery_count': 0
        }
        
        logger.info(f"Created webhook {webhook_id} for user {user.get('username')}")
        
        return jsonify({
            'success': True,
            'webhook': webhook_data,
            'message': 'Webhook created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Create webhook error: {str(e)}")
        return jsonify({'error': 'Failed to create webhook'}), 500


@webhooks_bp.route('/<webhook_id>', methods=['GET'])
@require_auth()
def get_webhook(webhook_id):
    """Get webhook details"""
    try:
        user = get_current_user()
        
        # Mock webhook data
        webhook_data = {
            'id': webhook_id,
            'name': 'Slack Notifications',
            'url': 'https://hooks.slack.com/services/...',
            'events': ['scan.completed', 'vulnerability.found'],
            'active': True,
            'secret': '***hidden***',
            'user_id': user.get('user_id'),
            'created_at': '2024-01-10T12:00:00Z',
            'last_triggered': '2024-01-15T14:30:00Z',
            'delivery_count': 45,
            'recent_deliveries': [
                {
                    'timestamp': '2024-01-15T14:30:00Z',
                    'event': 'vulnerability.found',
                    'status': 'success',
                    'response_code': 200,
                    'response_time': 245
                },
                {
                    'timestamp': '2024-01-15T13:45:00Z',
                    'event': 'scan.completed',
                    'status': 'success',
                    'response_code': 200,
                    'response_time': 189
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'webhook': webhook_data
        }), 200
        
    except Exception as e:
        logger.error(f"Get webhook error: {str(e)}")
        return jsonify({'error': 'Failed to get webhook'}), 500


@webhooks_bp.route('/<webhook_id>', methods=['PUT'])
@require_auth()
def update_webhook(webhook_id):
    """Update webhook"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # In real implementation, update webhook in database
        updated_webhook = {
            'id': webhook_id,
            'name': data.get('name', 'Slack Notifications'),
            'url': data.get('url', 'https://hooks.slack.com/services/...'),
            'events': data.get('events', ['scan.completed']),
            'active': data.get('active', True),
            'updated_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        logger.info(f"Updated webhook {webhook_id} by user {user.get('username')}")
        
        return jsonify({
            'success': True,
            'webhook': updated_webhook,
            'message': 'Webhook updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Update webhook error: {str(e)}")
        return jsonify({'error': 'Failed to update webhook'}), 500


@webhooks_bp.route('/<webhook_id>', methods=['DELETE'])
@require_auth()
def delete_webhook(webhook_id):
    """Delete webhook"""
    try:
        user = get_current_user()
        
        # In real implementation, delete webhook from database
        logger.info(f"Deleted webhook {webhook_id} by user {user.get('username')}")
        
        return jsonify({
            'success': True,
            'message': 'Webhook deleted successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Delete webhook error: {str(e)}")
        return jsonify({'error': 'Failed to delete webhook'}), 500


@webhooks_bp.route('/<webhook_id>/test', methods=['POST'])
@require_auth()
def test_webhook(webhook_id):
    """Test webhook delivery"""
    try:
        user = get_current_user()
        
        # Mock test delivery
        test_payload = {
            'event': 'webhook.test',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'webhook_id': webhook_id,
            'test': True,
            'message': 'This is a test webhook delivery'
        }
        
        # In real implementation, send actual HTTP request to webhook URL
        logger.info(f"Testing webhook {webhook_id} by user {user.get('username')}")
        
        # Mock successful delivery
        delivery_result = {
            'success': True,
            'status_code': 200,
            'response_time': 156,
            'payload': test_payload,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        return jsonify({
            'success': True,
            'delivery': delivery_result,
            'message': 'Webhook test completed successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Test webhook error: {str(e)}")
        return jsonify({'error': 'Failed to test webhook'}), 500


@webhooks_bp.route('/<webhook_id>/deliveries', methods=['GET'])
@require_auth()
def get_webhook_deliveries(webhook_id):
    """Get webhook delivery history"""
    try:
        user = get_current_user()
        
        limit = request.args.get('limit', 50, type=int)
        status = request.args.get('status')  # success, failed, pending
        
        # Mock delivery history
        deliveries = [
            {
                'id': 'delivery_1',
                'timestamp': '2024-01-15T14:30:00Z',
                'event': 'vulnerability.found',
                'status': 'success',
                'status_code': 200,
                'response_time': 245,
                'attempts': 1
            },
            {
                'id': 'delivery_2',
                'timestamp': '2024-01-15T13:45:00Z',
                'event': 'scan.completed',
                'status': 'success',
                'status_code': 200,
                'response_time': 189,
                'attempts': 1
            },
            {
                'id': 'delivery_3',
                'timestamp': '2024-01-15T12:30:00Z',
                'event': 'vulnerability.found',
                'status': 'failed',
                'status_code': 500,
                'response_time': 5000,
                'attempts': 3,
                'error': 'Internal Server Error'
            }
        ]
        
        # Filter by status
        if status:
            deliveries = [d for d in deliveries if d['status'] == status]
        
        # Apply limit
        deliveries = deliveries[:limit]
        
        return jsonify({
            'success': True,
            'deliveries': deliveries,
            'total': len(deliveries)
        }), 200
        
    except Exception as e:
        logger.error(f"Get webhook deliveries error: {str(e)}")
        return jsonify({'error': 'Failed to get webhook deliveries'}), 500


@webhooks_bp.route('/events', methods=['GET'])
@require_auth()
def list_event_types():
    """List available webhook event types"""
    try:
        event_types = [
            {
                'name': 'scan.started',
                'description': 'Triggered when a scan is started',
                'payload_example': {
                    'scan_id': 'scan_123',
                    'target': 'example.com',
                    'type': 'web_reconnaissance'
                }
            },
            {
                'name': 'scan.completed',
                'description': 'Triggered when a scan completes successfully',
                'payload_example': {
                    'scan_id': 'scan_123',
                    'target': 'example.com',
                    'vulnerabilities_found': 5,
                    'duration': 900
                }
            },
            {
                'name': 'vulnerability.found',
                'description': 'Triggered when a vulnerability is discovered',
                'payload_example': {
                    'vulnerability_id': 'vuln_456',
                    'severity': 'high',
                    'title': 'SQL Injection',
                    'target': 'example.com'
                }
            },
            {
                'name': 'vulnerability.critical',
                'description': 'Triggered when a critical vulnerability is found',
                'payload_example': {
                    'vulnerability_id': 'vuln_789',
                    'severity': 'critical',
                    'title': 'Remote Code Execution',
                    'cvss_score': 9.8
                }
            }
        ]
        
        return jsonify({
            'success': True,
            'event_types': event_types,
            'total': len(event_types)
        }), 200
        
    except Exception as e:
        logger.error(f"List event types error: {str(e)}")
        return jsonify({'error': 'Failed to list event types'}), 500