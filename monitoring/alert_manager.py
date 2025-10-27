# monitoring/alert_manager_fixed.py
"""
Alert management system for HexStrike AI monitoring infrastructure
Handles alert rules, notification channels, and escalation policies
"""
import os
import json
import time
import logging
import smtplib
import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class NotificationChannel(Enum):
    """Supported notification channels"""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    DISCORD = "discord"


@dataclass
class Alert:
    """Alert data structure"""
    name: str
    severity: AlertSeverity
    message: str
    description: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            'name': self.name,
            'severity': self.severity.value,
            'message': self.message,
            'description': self.description,
            'labels': self.labels,
            'annotations': self.annotations,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }


@dataclass
class NotificationConfig:
    """Notification channel configuration"""
    channel: NotificationChannel
    enabled: bool
    config: Dict[str, Any]
    severity_filter: List[AlertSeverity]
    
    def should_notify(self, severity: AlertSeverity) -> bool:
        """Check if notification should be sent for given severity"""
        return self.enabled and severity in self.severity_filter


@dataclass
class EscalationPolicy:
    """Alert escalation policy"""
    name: str
    rules: List[Dict[str, Any]]
    enabled: bool = True
    
    def get_escalation_level(self, alert_age_minutes: int) -> int:
        """Get escalation level based on alert age"""
        for i, rule in enumerate(self.rules):
            if alert_age_minutes >= rule.get('after_minutes', 0):
                continue
            return i
        return len(self.rules) - 1


class AlertManager:
    """Main alert management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_alerts: Dict[str, Alert] = {}
        self.notification_configs: Dict[str, NotificationConfig] = {}
        self.escalation_policies: Dict[str, EscalationPolicy] = {}
        self.alert_history: List[Alert] = []
        self.notification_callbacks: Dict[NotificationChannel, Callable] = {}
        
        # Initialize notification handlers
        self._setup_notification_handlers()
        
        # Load configuration
        self._load_configuration()
    
    def _setup_notification_handlers(self):
        """Setup notification channel handlers"""
        self.notification_callbacks = {
            NotificationChannel.EMAIL: self._send_email_notification,
            NotificationChannel.SLACK: self._send_slack_notification,
            NotificationChannel.WEBHOOK: self._send_webhook_notification,
            NotificationChannel.DISCORD: self._send_discord_notification
        }
    
    def _load_configuration(self):
        """Load alert manager configuration from environment and files"""
        # Email configuration
        if os.getenv('SMTP_HOST'):
            self.add_notification_config(
                'email_alerts',
                NotificationConfig(
                    channel=NotificationChannel.EMAIL,
                    enabled=True,
                    config={
                        'smtp_host': os.getenv('SMTP_HOST'),
                        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
                        'smtp_user': os.getenv('SMTP_USER'),
                        'smtp_password': os.getenv('SMTP_PASSWORD'),
                        'from_email': os.getenv('ALERT_FROM_EMAIL', 'alerts@hexstrike.ai'),
                        'to_emails': os.getenv('ALERT_TO_EMAILS', '').split(',')
                    },
                    severity_filter=[AlertSeverity.WARNING, AlertSeverity.CRITICAL]
                )
            )
        
        # Slack configuration
        if os.getenv('SLACK_WEBHOOK_URL'):
            self.add_notification_config(
                'slack_alerts',
                NotificationConfig(
                    channel=NotificationChannel.SLACK,
                    enabled=True,
                    config={
                        'webhook_url': os.getenv('SLACK_WEBHOOK_URL'),
                        'channel': os.getenv('SLACK_CHANNEL', '#alerts'),
                        'username': os.getenv('SLACK_USERNAME', 'HexStrike AI')
                    },
                    severity_filter=[AlertSeverity.WARNING, AlertSeverity.CRITICAL]
                )
            )
        
        # Load escalation policies
        self._load_escalation_policies()
    
    def _load_escalation_policies(self):
        """Load default escalation policies"""
        # Critical alert escalation
        self.add_escalation_policy(
            'critical_escalation',
            EscalationPolicy(
                name='Critical Alert Escalation',
                rules=[
                    {'after_minutes': 0, 'channels': ['slack_alerts', 'email_alerts']},
                    {'after_minutes': 5, 'channels': ['discord_alerts', 'webhook_alerts']},
                    {'after_minutes': 15, 'channels': ['email_alerts']}
                ]
            )
        )
    
    def add_notification_config(self, name: str, config: NotificationConfig):
        """Add notification configuration"""
        self.notification_configs[name] = config
        self.logger.info(f"Added notification config: {name} ({config.channel.value})")
    
    def add_escalation_policy(self, name: str, policy: EscalationPolicy):
        """Add escalation policy"""
        self.escalation_policies[name] = policy
        self.logger.info(f"Added escalation policy: {name}")
    
    async def fire_alert(self, alert: Alert):
        """Fire a new alert"""
        alert_key = f"{alert.name}_{hash(str(alert.labels))}"
        
        # Check if this is a duplicate alert
        if alert_key in self.active_alerts:
            self.logger.debug(f"Alert {alert.name} already active, skipping")
            return
        
        # Add to active alerts
        self.active_alerts[alert_key] = alert
        self.alert_history.append(alert)
        
        self.logger.warning(f"Alert fired: {alert.name} ({alert.severity.value})")
        
        # Send notifications
        await self._send_notifications(alert)
    
    async def resolve_alert(self, alert_name: str, labels: Dict[str, str] = None):
        """Resolve an active alert"""
        alert_key = f"{alert_name}_{hash(str(labels or {}))}"
        
        if alert_key in self.active_alerts:
            alert = self.active_alerts[alert_key]
            alert.resolved = True
            alert.resolved_at = datetime.utcnow()
            
            del self.active_alerts[alert_key]
            
            self.logger.info(f"Alert resolved: {alert.name}")
            
            # Send resolution notification
            await self._send_resolution_notification(alert)
    
    async def _send_notifications(self, alert: Alert):
        """Send notifications for an alert"""
        tasks = []
        
        for config_name, config in self.notification_configs.items():
            if config.should_notify(alert.severity):
                handler = self.notification_callbacks.get(config.channel)
                if handler:
                    task = handler(alert, config)
                    tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _send_resolution_notification(self, alert: Alert):
        """Send alert resolution notification"""
        resolution_alert = Alert(
            name=f"{alert.name}_resolved",
            severity=AlertSeverity.INFO,
            message=f"RESOLVED: {alert.message}",
            description=f"Alert '{alert.name}' has been resolved",
            labels=alert.labels,
            annotations=alert.annotations,
            timestamp=datetime.utcnow()
        )
        
        await self._send_notifications(resolution_alert)
    
    async def _send_email_notification(self, alert: Alert, config: NotificationConfig):
        """Send email notification"""
        try:
            smtp_config = config.config
            
            msg = MimeMultipart()
            msg['From'] = smtp_config['from_email']
            msg['To'] = ', '.join(smtp_config['to_emails'])
            msg['Subject'] = f"[HexStrike AI] {alert.severity.value.upper()}: {alert.name}"
            
            # Create email body
            body = self._create_email_body(alert)
            msg.attach(MimeText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(smtp_config['smtp_host'], smtp_config['smtp_port'])
            server.starttls()
            server.login(smtp_config['smtp_user'], smtp_config['smtp_password'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email notification sent for alert: {alert.name}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")
    
    async def _send_slack_notification(self, alert: Alert, config: NotificationConfig):
        """Send Slack notification"""
        try:
            slack_config = config.config
            
            # Create Slack message
            payload = {
                'channel': slack_config['channel'],
                'username': slack_config['username'],
                'icon_emoji': self._get_severity_emoji(alert.severity),
                'attachments': [
                    {
                        'color': self._get_severity_color(alert.severity),
                        'title': f"{alert.severity.value.upper()}: {alert.name}",
                        'text': alert.description,
                        'fields': [
                            {
                                'title': 'Message',
                                'value': alert.message,
                                'short': False
                            },
                            {
                                'title': 'Timestamp',
                                'value': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'),
                                'short': True
                            }
                        ],
                        'footer': 'HexStrike AI Monitoring',
                        'ts': int(alert.timestamp.timestamp())
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(slack_config['webhook_url'], json=payload) as response:
                    if response.status == 200:
                        self.logger.info(f"Slack notification sent for alert: {alert.name}")
                    else:
                        self.logger.error(f"Failed to send Slack notification: {response.status}")
                        
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
    
    async def _send_discord_notification(self, alert: Alert, config: NotificationConfig):
        """Send Discord notification"""
        pass  # Simplified for testing
    
    async def _send_webhook_notification(self, alert: Alert, config: NotificationConfig):
        """Send generic webhook notification"""
        pass  # Simplified for testing
    
    def _create_email_body(self, alert: Alert) -> str:
        """Create HTML email body"""
        return f"""
        <html>
        <body>
            <h2 style="color: {self._get_severity_color(alert.severity)};">
                {alert.severity.value.upper()}: {alert.name}
            </h2>
            
            <p><strong>Message:</strong> {alert.message}</p>
            <p><strong>Description:</strong> {alert.description}</p>
            <p><strong>Timestamp:</strong> {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            
            <hr>
            <p><em>This alert was generated by HexStrike AI Monitoring System</em></p>
        </body>
        </html>
        """
    
    def _get_severity_color(self, severity: AlertSeverity) -> str:
        """Get color for severity level"""
        colors = {
            AlertSeverity.INFO: '#36a64f',
            AlertSeverity.WARNING: '#ff9500',
            AlertSeverity.CRITICAL: '#ff0000'
        }
        return colors.get(severity, '#808080')
    
    def _get_severity_emoji(self, severity: AlertSeverity) -> str:
        """Get emoji for severity level"""
        emojis = {
            AlertSeverity.INFO: ':information_source:',
            AlertSeverity.WARNING: ':warning:',
            AlertSeverity.CRITICAL: ':rotating_light:'
        }
        return emojis.get(severity, ':question:')
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        return [alert.to_dict() for alert in self.active_alerts.values()]
    
    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history"""
        return [alert.to_dict() for alert in self.alert_history[-limit:]]
    
    def get_notification_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get notification configurations"""
        return {
            name: {
                'channel': config.channel.value,
                'enabled': config.enabled,
                'severity_filter': [s.value for s in config.severity_filter]
            }
            for name, config in self.notification_configs.items()
        }


# Global alert manager instance
alert_manager = AlertManager()