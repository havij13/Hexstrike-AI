# tests/test_alerting_system.py
"""
Tests for HexStrike AI alerting and notification system
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

from monitoring.alert_manager import AlertManager, Alert, AlertSeverity
from services.notification_service import NotificationService, NotificationResult
from config.alerting_config import AlertingConfig
from config.escalation_policies import EscalationPolicies


class TestAlertManager:
    """Test cases for AlertManager"""
    
    def setup_method(self):
        """Setup test environment"""
        self.alert_manager = AlertManager()
        self.test_alert = Alert(
            name="TestAlert",
            severity=AlertSeverity.WARNING,
            message="Test alert message",
            description="Test alert description",
            labels={"service": "test", "component": "testing"},
            annotations={"summary": "Test summary"},
            timestamp=datetime.utcnow()
        )
    
    def test_alert_creation(self):
        """Test alert object creation"""
        assert self.test_alert.name == "TestAlert"
        assert self.test_alert.severity == AlertSeverity.WARNING
        assert self.test_alert.message == "Test alert message"
        assert not self.test_alert.resolved
    
    def test_alert_to_dict(self):
        """Test alert serialization"""
        alert_dict = self.test_alert.to_dict()
        
        assert alert_dict['name'] == "TestAlert"
        assert alert_dict['severity'] == "warning"
        assert alert_dict['message'] == "Test alert message"
        assert alert_dict['resolved'] is False
    
    @pytest.mark.asyncio
    async def test_fire_alert(self):
        """Test firing an alert"""
        with patch.object(self.alert_manager, '_send_notifications', new_callable=AsyncMock) as mock_send:
            await self.alert_manager.fire_alert(self.test_alert)
            
            # Check alert was added to active alerts
            alert_key = f"{self.test_alert.name}_{hash(str(self.test_alert.labels))}"
            assert alert_key in self.alert_manager.active_alerts
            
            # Check notification was sent
            mock_send.assert_called_once_with(self.test_alert)
    
    @pytest.mark.asyncio
    async def test_resolve_alert(self):
        """Test resolving an alert"""
        # First fire the alert
        await self.alert_manager.fire_alert(self.test_alert)
        
        # Then resolve it
        with patch.object(self.alert_manager, '_send_resolution_notification', new_callable=AsyncMock) as mock_resolve:
            await self.alert_manager.resolve_alert(self.test_alert.name, self.test_alert.labels)
            
            # Check alert was removed from active alerts
            alert_key = f"{self.test_alert.name}_{hash(str(self.test_alert.labels))}"
            assert alert_key not in self.alert_manager.active_alerts
            
            # Check resolution notification was sent
            mock_resolve.assert_called_once()
    
    def test_get_active_alerts(self):
        """Test getting active alerts"""
        # Initially no active alerts
        active = self.alert_manager.get_active_alerts()
        assert len(active) == 0
        
        # Add alert manually for testing
        alert_key = f"{self.test_alert.name}_{hash(str(self.test_alert.labels))}"
        self.alert_manager.active_alerts[alert_key] = self.test_alert
        
        active = self.alert_manager.get_active_alerts()
        assert len(active) == 1
        assert active[0]['name'] == "TestAlert"
    
    def test_get_alert_history(self):
        """Test getting alert history"""
        # Add alert to history manually for testing
        self.alert_manager.alert_history.append(self.test_alert)
        
        history = self.alert_manager.get_alert_history(limit=10)
        assert len(history) == 1
        assert history[0]['name'] == "TestAlert"


class TestNotificationService:
    """Test cases for NotificationService"""
    
    def setup_method(self):
        """Setup test environment"""
        self.notification_service = NotificationService()
        self.test_alert = Alert(
            name="TestNotification",
            severity=AlertSeverity.CRITICAL,
            message="Test notification message",
            description="Test notification description",
            labels={"service": "test", "component": "notification"},
            annotations={"summary": "Test notification"},
            timestamp=datetime.utcnow()
        )
    
    @pytest.mark.asyncio
    async def test_send_slack_notification_success(self):
        """Test successful Slack notification"""
        config = {
            'type': 'slack',
            'webhook_url': 'https://hooks.slack.com/test',
            'channel': '#test',
            'username': 'Test Bot'
        }
        
        with patch('aiohttp.ClientSession.post') as mock_post:
            # Mock successful response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_post.return_value.__aenter__.return_value = mock_response
            
            result = await self.notification_service._send_slack_notification(self.test_alert, config)
            
            assert result.success is True
            assert result.channel == 'slack'
    
    @pytest.mark.asyncio
    async def test_send_slack_notification_failure(self):
        """Test failed Slack notification"""
        config = {
            'type': 'slack',
            'webhook_url': 'https://hooks.slack.com/test',
            'channel': '#test',
            'username': 'Test Bot'
        }
        
        with patch('aiohttp.ClientSession.post') as mock_post:
            # Mock failed response
            mock_response = AsyncMock()
            mock_response.status = 400
            mock_response.text.return_value = "Bad Request"
            mock_post.return_value.__aenter__.return_value = mock_response
            
            result = await self.notification_service._send_slack_notification(self.test_alert, config)
            
            assert result.success is False
            assert result.channel == 'slack'
            assert "400" in result.message
    
    @pytest.mark.asyncio
    async def test_send_email_notification_success(self):
        """Test successful email notification"""
        config = {
            'type': 'email',
            'smtp_host': 'smtp.test.com',
            'smtp_port': 587,
            'smtp_user': 'test@test.com',
            'smtp_password': 'password',
            'from_email': 'alerts@test.com',
            'to_emails': ['admin@test.com']
        }
        
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = Mock()
            mock_smtp.return_value = mock_server
            
            result = await self.notification_service._send_email_notification(self.test_alert, config)
            
            assert result.success is True
            assert result.channel == 'email'
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once()
            mock_server.send_message.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_email_notification_failure(self):
        """Test failed email notification"""
        config = {
            'type': 'email',
            'smtp_host': 'smtp.test.com',
            'smtp_port': 587,
            'smtp_user': 'test@test.com',
            'smtp_password': 'password',
            'from_email': 'alerts@test.com',
            'to_emails': ['admin@test.com']
        }
        
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.side_effect = Exception("SMTP connection failed")
            
            result = await self.notification_service._send_email_notification(self.test_alert, config)
            
            assert result.success is False
            assert result.channel == 'email'
            assert "SMTP connection failed" in result.message
    
    def test_get_severity_color(self):
        """Test severity color mapping"""
        assert self.notification_service._get_severity_color(AlertSeverity.INFO) == '#36a64f'
        assert self.notification_service._get_severity_color(AlertSeverity.WARNING) == '#ff9500'
        assert self.notification_service._get_severity_color(AlertSeverity.CRITICAL) == '#ff0000'
    
    def test_get_severity_emoji(self):
        """Test severity emoji mapping"""
        assert self.notification_service._get_severity_emoji(AlertSeverity.INFO) == ':information_source:'
        assert self.notification_service._get_severity_emoji(AlertSeverity.WARNING) == ':warning:'
        assert self.notification_service._get_severity_emoji(AlertSeverity.CRITICAL) == ':rotating_light:'


class TestAlertingConfig:
    """Test cases for AlertingConfig"""
    
    def test_config_initialization(self):
        """Test configuration initialization"""
        config = AlertingConfig()
        
        assert hasattr(config, 'ALERT_ENABLED')
        assert hasattr(config, 'SMTP_HOST')
        assert hasattr(config, 'SLACK_WEBHOOK_URL')
    
    def test_email_configuration_check(self):
        """Test email configuration validation"""
        config = AlertingConfig()
        config.SMTP_HOST = "smtp.test.com"
        config.SMTP_USER = "test@test.com"
        config.SMTP_PASSWORD = "password"
        config.ALERT_FROM_EMAIL = "alerts@test.com"
        config.ALERT_TO_EMAILS = ["admin@test.com"]
        
        assert config.is_email_configured() is True
    
    def test_slack_configuration_check(self):
        """Test Slack configuration validation"""
        config = AlertingConfig()
        config.SLACK_WEBHOOK_URL = "https://hooks.slack.com/test"
        
        assert config.is_slack_configured() is True
    
    def test_get_configured_channels(self):
        """Test getting configured channels"""
        config = AlertingConfig()
        config.SLACK_WEBHOOK_URL = "https://hooks.slack.com/test"
        config.DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/test"
        
        channels = config.get_configured_channels()
        
        assert 'slack' in channels
        assert 'discord' in channels
    
    def test_notification_config_retrieval(self):
        """Test notification configuration retrieval"""
        config = AlertingConfig()
        config.SLACK_WEBHOOK_URL = "https://hooks.slack.com/test"
        config.SLACK_CHANNEL = "#alerts"
        
        slack_config = config.get_notification_config('slack')
        
        assert slack_config['type'] == 'slack'
        assert slack_config['enabled'] is True
        assert slack_config['webhook_url'] == "https://hooks.slack.com/test"
        assert slack_config['channel'] == "#alerts"


class TestEscalationPolicies:
    """Test cases for EscalationPolicies"""
    
    def test_critical_escalation_policy(self):
        """Test critical alert escalation policy"""
        policy = EscalationPolicies.get_critical_escalation_policy()
        
        assert len(policy) == 4  # 4 escalation levels
        assert policy[0].after_minutes == 0  # Immediate
        assert policy[1].after_minutes == 5  # After 5 minutes
        assert policy[2].after_minutes == 15  # After 15 minutes
        assert policy[3].after_minutes == 30  # After 30 minutes
    
    def test_warning_escalation_policy(self):
        """Test warning alert escalation policy"""
        policy = EscalationPolicies.get_warning_escalation_policy()
        
        assert len(policy) == 4  # 4 escalation levels
        assert policy[0].after_minutes == 0  # Immediate
        assert policy[1].after_minutes == 10  # After 10 minutes
        assert policy[2].after_minutes == 30  # After 30 minutes
        assert policy[3].after_minutes == 60  # After 60 minutes
    
    def test_security_escalation_policy(self):
        """Test security alert escalation policy"""
        policy = EscalationPolicies.get_security_escalation_policy()
        
        assert len(policy) == 4  # 4 escalation levels
        assert policy[0].after_minutes == 0  # Immediate
        assert policy[1].after_minutes == 2  # After 2 minutes (faster than normal)
        assert policy[2].after_minutes == 5  # After 5 minutes
        assert policy[3].after_minutes == 10  # After 10 minutes
    
    def test_escalation_policy_by_labels(self):
        """Test escalation policy selection by labels"""
        # Security alert
        security_labels = {"severity": "critical", "component": "security"}
        policy = EscalationPolicies.get_escalation_policy_by_labels(security_labels)
        assert policy[1].after_minutes == 2  # Security escalation is faster
        
        # Infrastructure alert
        infra_labels = {"severity": "warning", "service": "system"}
        policy = EscalationPolicies.get_escalation_policy_by_labels(infra_labels)
        assert len(policy) == 4  # Infrastructure escalation policy
        
        # Regular critical alert
        critical_labels = {"severity": "critical", "service": "app"}
        policy = EscalationPolicies.get_escalation_policy_by_labels(critical_labels)
        assert policy[0].after_minutes == 0  # Critical escalation
    
    def test_get_all_policies(self):
        """Test getting all escalation policies"""
        all_policies = EscalationPolicies.get_all_policies()
        
        assert 'critical' in all_policies
        assert 'warning' in all_policies
        assert 'info' in all_policies
        assert 'security' in all_policies
        assert 'infrastructure' in all_policies


class TestRateLimiter:
    """Test cases for RateLimiter"""
    
    def setup_method(self):
        """Setup test environment"""
        from services.notification_service import RateLimiter
        self.rate_limiter = RateLimiter(max_per_minute=5, burst_limit=2)
    
    @pytest.mark.asyncio
    async def test_rate_limiting_allows_initial_requests(self):
        """Test that initial requests are allowed"""
        assert await self.rate_limiter.can_send() is True
        await self.rate_limiter.record_request()
        
        assert await self.rate_limiter.can_send() is True
        await self.rate_limiter.record_request()
    
    @pytest.mark.asyncio
    async def test_rate_limiting_blocks_burst_limit(self):
        """Test that burst limit is enforced"""
        # Use up burst limit
        for _ in range(2):
            assert await self.rate_limiter.can_send() is True
            await self.rate_limiter.record_request()
        
        # Next request should be blocked
        assert await self.rate_limiter.can_send() is False


class TestIntegration:
    """Integration tests for the alerting system"""
    
    def setup_method(self):
        """Setup test environment"""
        self.alert_manager = AlertManager()
        self.notification_service = NotificationService()
    
    @pytest.mark.asyncio
    async def test_end_to_end_alert_flow(self):
        """Test complete alert flow from firing to resolution"""
        test_alert = Alert(
            name="IntegrationTest",
            severity=AlertSeverity.WARNING,
            message="Integration test alert",
            description="End-to-end test alert",
            labels={"service": "test", "component": "integration"},
            annotations={"summary": "Integration test"},
            timestamp=datetime.utcnow()
        )
        
        # Mock notification sending
        with patch.object(self.alert_manager, '_send_notifications', new_callable=AsyncMock) as mock_notify:
            # Fire alert
            await self.alert_manager.fire_alert(test_alert)
            
            # Verify alert is active
            active_alerts = self.alert_manager.get_active_alerts()
            assert len(active_alerts) == 1
            assert active_alerts[0]['name'] == "IntegrationTest"
            
            # Verify notification was sent
            mock_notify.assert_called_once()
            
            # Resolve alert
            with patch.object(self.alert_manager, '_send_resolution_notification', new_callable=AsyncMock):
                await self.alert_manager.resolve_alert(test_alert.name, test_alert.labels)
                
                # Verify alert is no longer active
                active_alerts = self.alert_manager.get_active_alerts()
                assert len(active_alerts) == 0
    
    def test_configuration_integration(self):
        """Test configuration integration across components"""
        config = AlertingConfig()
        
        # Test that configuration is accessible
        assert hasattr(config, 'ALERT_ENABLED')
        
        # Test that notification configs can be retrieved
        channels = config.get_configured_channels()
        assert isinstance(channels, list)
        
        # Test that escalation policies are available
        policies = EscalationPolicies.get_all_policies()
        assert len(policies) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])