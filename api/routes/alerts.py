# api/routes/alerts.py
"""
Alert management API routes for HexStrike AI
Provides endpoints for managing alerts, notifications, and escalation policies
"""
import asyncio
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_restx import Api, Resource, fields, Namespace

from monitoring.alert_manager import alert_manager, Alert, AlertSeverity
from services.notification_service import notification_service
from config.alerting_config import alerting_config
from config.escalation_policies import EscalationPolicies
from api.middleware.auth_middleware import require_auth


# Create blueprint and namespace
alerts_bp = Blueprint('alerts', __name__)
api = Api(alerts_bp, doc='/alerts/docs/', title='HexStrike AI Alerts API', 
          description='Alert management and notification system')

alerts_ns = Namespace('alerts', description='Alert operations')
api.add_namespace(alerts_ns)

# API Models
alert_model = api.model('Alert', {
    'name': fields.String(required=True, description='Alert name'),
    'severity': fields.String(required=True, enum=['info', 'warning', 'critical'], description='Alert severity'),
    'message': fields.String(required=True, description='Alert message'),
    'description': fields.String(required=True, description='Alert description'),
    'labels': fields.Raw(description='Alert labels'),
    'annotations': fields.Raw(description='Alert annotations')
})

test_alert_model = api.model('TestAlert', {
    'channel': fields.String(required=True, enum=['email', 'slack', 'discord', 'teams', 'pagerduty', 'webhook'], 
                            description='Notification channel to test'),
    'severity': fields.String(enum=['info', 'warning', 'critical'], default='info', description='Test alert severity')
})

notification_config_model = api.model('NotificationConfig', {
    'channel': fields.String(required=True, description='Notification channel'),
    'enabled': fields.Boolean(required=True, description='Whether channel is enabled'),
    'config': fields.Raw(description='Channel configuration')
})


@alerts_ns.route('/fire')
class FireAlert(Resource):
    @api.expect(alert_model)
    @api.doc('fire_alert')
    @require_auth('write:alerts')
    def post(self):
        """Fire a new alert"""
        try:
            data = request.get_json()
            
            # Create alert object
            alert = Alert(
                name=data['name'],
                severity=AlertSeverity(data['severity']),
                message=data['message'],
                description=data['description'],
                labels=data.get('labels', {}),
                annotations=data.get('annotations', {}),
                timestamp=datetime.utcnow()
            )
            
            # Fire alert asynchronously
            asyncio.create_task(alert_manager.fire_alert(alert))
            
            return {
                'status': 'success',
                'message': 'Alert fired successfully',
                'alert_id': f"{alert.name}_{hash(str(alert.labels))}"
            }, 201
            
        except Exception as e:
            return {'error': str(e)}, 400


@alerts_ns.route('/resolve')
class ResolveAlert(Resource):
    @api.expect(api.model('ResolveAlert', {
        'name': fields.String(required=True, description='Alert name to resolve'),
        'labels': fields.Raw(description='Alert labels for identification')
    }))
    @api.doc('resolve_alert')
    @require_auth('write:alerts')
    def post(self):
        """Resolve an active alert"""
        try:
            data = request.get_json()
            
            # Resolve alert asynchronously
            asyncio.create_task(alert_manager.resolve_alert(
                data['name'], 
                data.get('labels', {})
            ))
            
            return {
                'status': 'success',
                'message': 'Alert resolved successfully'
            }
            
        except Exception as e:
            return {'error': str(e)}, 400


@alerts_ns.route('/active')
class ActiveAlerts(Resource):
    @api.doc('get_active_alerts')
    @require_auth('read:alerts')
    def get(self):
        """Get all active alerts"""
        try:
            active_alerts = alert_manager.get_active_alerts()
            return {
                'status': 'success',
                'count': len(active_alerts),
                'alerts': active_alerts
            }
        except Exception as e:
            return {'error': str(e)}, 500


@alerts_ns.route('/history')
class AlertHistory(Resource):
    @api.doc('get_alert_history')
    @api.param('limit', 'Number of alerts to return', type='integer', default=100)
    @require_auth('read:alerts')
    def get(self):
        """Get alert history"""
        try:
            limit = request.args.get('limit', 100, type=int)
            history = alert_manager.get_alert_history(limit)
            
            return {
                'status': 'success',
                'count': len(history),
                'alerts': history
            }
        except Exception as e:
            return {'error': str(e)}, 500


@alerts_ns.route('/test/<string:channel>')
class TestNotification(Resource):
    @api.expect(test_alert_model)
    @api.doc('test_notification')
    @require_auth('write:alerts')
    def post(self, channel):
        """Test notification channel"""
        try:
            data = request.get_json() or {}
            severity = AlertSeverity(data.get('severity', 'info'))
            
            # Create test alert
            test_alert = Alert(
                name='TestAlert',
                severity=severity,
                message=f'Test notification for {channel} channel',
                description=f'This is a test alert to verify {channel} notification configuration.',
                labels={
                    'service': 'hexstrike-ai',
                    'component': 'alerting',
                    'test': 'true'
                },
                annotations={
                    'summary': f'Test notification for {channel}',
                    'runbook_url': 'https://docs.hexstrike.ai/runbooks/test-alert'
                },
                timestamp=datetime.utcnow()
            )
            
            # Get channel configuration
            channel_config = alerting_config.get_notification_config(channel)
            
            if not channel_config.get('enabled', False):
                return {
                    'status': 'error',
                    'message': f'{channel} notification channel is not configured or enabled'
                }, 400
            
            # Send test notification
            async def send_test():
                result = await notification_service.send_notification(test_alert, channel, channel_config)
                return result
            
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(send_test())
            loop.close()
            
            if result.success:
                return {
                    'status': 'success',
                    'message': f'Test notification sent successfully via {channel}',
                    'channel': channel,
                    'timestamp': result.timestamp.isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Failed to send test notification: {result.message}',
                    'channel': channel
                }, 500
                
        except Exception as e:
            return {'error': str(e)}, 500


@alerts_ns.route('/config')
class AlertingConfig(Resource):
    @api.doc('get_alerting_config')
    @require_auth('read:alerts')
    def get(self):
        """Get alerting configuration"""
        try:
            config = alerting_config.to_dict()
            
            # Remove sensitive information
            for channel_config in config.values():
                if isinstance(channel_config, dict) and 'password' in channel_config:
                    channel_config['password'] = '***'
                if isinstance(channel_config, dict) and 'auth_token' in channel_config:
                    channel_config['auth_token'] = '***'
                if isinstance(channel_config, dict) and 'integration_key' in channel_config:
                    channel_config['integration_key'] = '***'
            
            return {
                'status': 'success',
                'config': config,
                'configured_channels': alerting_config.get_configured_channels()
            }
        except Exception as e:
            return {'error': str(e)}, 500


@alerts_ns.route('/notifications/history')
class NotificationHistory(Resource):
    @api.doc('get_notification_history')
    @api.param('limit', 'Number of notifications to return', type='integer', default=100)
    @require_auth('read:alerts')
    def get(self):
        """Get notification history"""
        try:
            limit = request.args.get('limit', 100, type=int)
            history = notification_service.get_notification_history(limit)
            
            return {
                'status': 'success',
                'count': len(history),
                'notifications': history
            }
        except Exception as e:
            return {'error': str(e)}, 500


@alerts_ns.route('/notifications/failed')
class FailedNotifications(Resource):
    @api.doc('get_failed_notifications')
    @require_auth('read:alerts')
    def get(self):
        """Get failed notifications"""
        try:
            failed = notification_service.get_failed_notifications()
            
            return {
                'status': 'success',
                'count': len(failed),
                'failed_notifications': failed
            }
        except Exception as e:
            return {'error': str(e)}, 500
    
    @api.doc('clear_failed_notifications')
    @require_auth('write:alerts')
    def delete(self):
        """Clear failed notifications list"""
        try:
            notification_service.clear_failed_notifications()
            
            return {
                'status': 'success',
                'message': 'Failed notifications list cleared'
            }
        except Exception as e:
            return {'error': str(e)}, 500


@alerts_ns.route('/escalation/policies')
class EscalationPolicies(Resource):
    @api.doc('get_escalation_policies')
    @require_auth('read:alerts')
    def get(self):
        """Get escalation policies"""
        try:
            policies = EscalationPolicies.get_all_policies()
            
            # Convert to serializable format
            serialized_policies = {}
            for name, policy in policies.items():
                serialized_policies[name] = [
                    {
                        'level': rule.level.value,
                        'after_minutes': rule.after_minutes,
                        'notification_channels': rule.notification_channels,
                        'additional_recipients': rule.additional_recipients,
                        'repeat_interval_minutes': rule.repeat_interval_minutes
                    }
                    for rule in policy
                ]
            
            return {
                'status': 'success',
                'policies': serialized_policies
            }
        except Exception as e:
            return {'error': str(e)}, 500


@alerts_ns.route('/health')
class AlertingHealth(Resource):
    @api.doc('get_alerting_health')
    def get(self):
        """Get alerting system health status"""
        try:
            # Check configuration
            configured_channels = alerting_config.get_configured_channels()
            
            # Check active alerts
            active_alerts = alert_manager.get_active_alerts()
            
            # Check recent notifications
            recent_notifications = notification_service.get_notification_history(10)
            failed_notifications = notification_service.get_failed_notifications()
            
            # Calculate health metrics
            total_notifications = len(recent_notifications)
            failed_count = len([n for n in recent_notifications if not n.get('success', True)])
            success_rate = ((total_notifications - failed_count) / total_notifications * 100) if total_notifications > 0 else 100
            
            health_status = 'healthy'
            if failed_count > 5 or success_rate < 80:
                health_status = 'degraded'
            if not configured_channels or success_rate < 50:
                health_status = 'unhealthy'
            
            return {
                'status': 'success',
                'health': {
                    'status': health_status,
                    'configured_channels': len(configured_channels),
                    'active_alerts': len(active_alerts),
                    'notification_success_rate': round(success_rate, 2),
                    'failed_notifications': len(failed_notifications),
                    'channels': configured_channels
                },
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}, 500


# Register blueprint
def register_alerts_routes(app):
    """Register alert routes with the Flask app"""
    app.register_blueprint(alerts_bp, url_prefix='/api')
    return alerts_bp