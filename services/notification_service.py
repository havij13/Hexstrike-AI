# services/notification_service.py
"""
Notification service for HexStrike AI
Handles sending notifications through various channels with rate limiting and retry logic
"""
import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import aiohttp
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

from monitoring.alert_manager import Alert, AlertSeverity, NotificationChannel
from config.escalation_policies import EscalationPolicies, NotificationChannelConfig


@dataclass
class NotificationResult:
    """Result of a notification attempt"""
    success: bool
    channel: str
    message: str
    timestamp: datetime
    retry_count: int = 0


class RateLimiter:
    """Rate limiter for notifications"""
    
    def __init__(self, max_per_minute: int, burst_limit: int):
        self.max_per_minute = max_per_minute
        self.burst_limit = burst_limit
        self.requests = []
        self.burst_count = 0
    
    async def can_send(self) -> bool:
        """Check if we can send a notification"""
        now = datetime.utcnow()
        
        # Clean old requests (older than 1 minute)
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < timedelta(minutes=1)]
        
        # Check burst limit
        if self.burst_count >= self.burst_limit:
            # Reset burst count if enough time has passed
            if len(self.requests) == 0:
                self.burst_count = 0
            else:
                return False
        
        # Check rate limit
        if len(self.requests) >= self.max_per_minute:
            return False
        
        return True
    
    async def record_request(self):
        """Record a notification request"""
        now = datetime.utcnow()
        self.requests.append(now)
        self.burst_count += 1


class NotificationService:
    """Main notification service"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self.notification_history: List[NotificationResult] = []
        self.failed_notifications: List[Dict[str, Any]] = []
        
        # Initialize rate limiters
        self._setup_rate_limiters()
    
    def _setup_rate_limiters(self):
        """Setup rate limiters for each notification channel"""
        channel_configs = NotificationChannelConfig.get_channel_configs()
        
        for channel_name, config in channel_configs.items():
            rate_limit = config.get('rate_limit', {})
            self.rate_limiters[channel_name] = RateLimiter(
                max_per_minute=rate_limit.get('max_per_minute', 10),
                burst_limit=rate_limit.get('burst_limit', 3)
            )
    
    async def send_notification(self, alert: Alert, channel_name: str, 
                              config: Dict[str, Any]) -> NotificationResult:
        """Send notification through specified channel"""
        # Check rate limiting
        rate_limiter = self.rate_limiters.get(channel_name)
        if rate_limiter and not await rate_limiter.can_send():
            self.logger.warning(f"Rate limit exceeded for channel {channel_name}")
            return NotificationResult(
                success=False,
                channel=channel_name,
                message="Rate limit exceeded",
                timestamp=datetime.utcnow()
            )
        
        # Send notification based on channel type
        channel_type = config.get('type', '').lower()
        
        try:
            if channel_type == 'slack':
                result = await self._send_slack_notification(alert, config)
            elif channel_type == 'email':
                result = await self._send_email_notification(alert, config)
            elif channel_type == 'discord':
                result = await self._send_discord_notification(alert, config)
            elif channel_type == 'teams':
                result = await self._send_teams_notification(alert, config)
            elif channel_type == 'pagerduty':
                result = await self._send_pagerduty_notification(alert, config)
            elif channel_type == 'webhook':
                result = await self._send_webhook_notification(alert, config)
            else:
                result = NotificationResult(
                    success=False,
                    channel=channel_name,
                    message=f"Unknown channel type: {channel_type}",
                    timestamp=datetime.utcnow()
                )
            
            # Record successful request for rate limiting
            if result.success and rate_limiter:
                await rate_limiter.record_request()
            
            # Store notification result
            self.notification_history.append(result)
            
            # Log result
            if result.success:
                self.logger.info(f"Notification sent successfully via {channel_name}")
            else:
                self.logger.error(f"Failed to send notification via {channel_name}: {result.message}")
                self.failed_notifications.append({
                    'alert': alert.to_dict(),
                    'channel': channel_name,
                    'error': result.message,
                    'timestamp': result.timestamp.isoformat()
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Exception sending notification via {channel_name}: {e}")
            return NotificationResult(
                success=False,
                channel=channel_name,
                message=str(e),
                timestamp=datetime.utcnow()
            )
    
    async def _send_slack_notification(self, alert: Alert, config: Dict[str, Any]) -> NotificationResult:
        """Send Slack notification"""
        webhook_url = config.get('webhook_url', '').replace('${SLACK_WEBHOOK_URL}', 
                                                           os.getenv('SLACK_WEBHOOK_URL', ''))
        
        if not webhook_url:
            return NotificationResult(
                success=False,
                channel='slack',
                message="Slack webhook URL not configured",
                timestamp=datetime.utcnow()
            )
        
        # Create Slack message
        color = self._get_severity_color(alert.severity)
        emoji = self._get_severity_emoji(alert.severity)
        
        payload = {
            'channel': config.get('channel', '#alerts').replace('${SLACK_CHANNEL:', '').rstrip('}'),
            'username': config.get('username', 'HexStrike AI'),
            'icon_emoji': emoji,
            'attachments': [
                {
                    'color': color,
                    'title': f"{alert.severity.value.upper()}: {alert.name}",
                    'text': alert.description,
                    'fields': [
                        {
                            'title': 'Message',
                            'value': alert.message,
                            'short': False
                        },
                        {
                            'title': 'Service',
                            'value': alert.labels.get('service', 'Unknown'),
                            'short': True
                        },
                        {
                            'title': 'Component',
                            'value': alert.labels.get('component', 'Unknown'),
                            'short': True
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
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    return NotificationResult(
                        success=True,
                        channel='slack',
                        message="Notification sent successfully",
                        timestamp=datetime.utcnow()
                    )
                else:
                    error_text = await response.text()
                    return NotificationResult(
                        success=False,
                        channel='slack',
                        message=f"HTTP {response.status}: {error_text}",
                        timestamp=datetime.utcnow()
                    )
    
    async def _send_email_notification(self, alert: Alert, config: Dict[str, Any]) -> NotificationResult:
        """Send email notification"""
        try:
            smtp_host = config.get('smtp_host', '').replace('${SMTP_HOST}', os.getenv('SMTP_HOST', ''))
            smtp_port = int(config.get('smtp_port', '587').replace('${SMTP_PORT:', '').rstrip('}'))
            smtp_user = config.get('smtp_user', '').replace('${SMTP_USER}', os.getenv('SMTP_USER', ''))
            smtp_password = config.get('smtp_password', '').replace('${SMTP_PASSWORD}', os.getenv('SMTP_PASSWORD', ''))
            from_email = config.get('from_email', '').replace('${ALERT_FROM_EMAIL:', '').rstrip('}')
            
            if not all([smtp_host, smtp_user, smtp_password, from_email]):
                return NotificationResult(
                    success=False,
                    channel='email',
                    message="Email configuration incomplete",
                    timestamp=datetime.utcnow()
                )
            
            # Get recipient emails
            to_emails = config.get('to_emails', [])
            if isinstance(to_emails, str):
                to_emails = [email.strip() for email in to_emails.split(',') if email.strip()]
            
            if not to_emails:
                return NotificationResult(
                    success=False,
                    channel='email',
                    message="No recipient emails configured",
                    timestamp=datetime.utcnow()
                )
            
            # Create email
            msg = MimeMultipart()
            msg['From'] = from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"[HexStrike AI] {alert.severity.value.upper()}: {alert.name}"
            
            # Create HTML body
            body = self._create_email_body(alert)
            msg.attach(MimeText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()
            
            return NotificationResult(
                success=True,
                channel='email',
                message=f"Email sent to {len(to_emails)} recipients",
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            return NotificationResult(
                success=False,
                channel='email',
                message=f"Email sending failed: {str(e)}",
                timestamp=datetime.utcnow()
            )
    
    async def _send_discord_notification(self, alert: Alert, config: Dict[str, Any]) -> NotificationResult:
        """Send Discord notification"""
        webhook_url = config.get('webhook_url', '').replace('${DISCORD_WEBHOOK_URL}', 
                                                           os.getenv('DISCORD_WEBHOOK_URL', ''))
        
        if not webhook_url:
            return NotificationResult(
                success=False,
                channel='discord',
                message="Discord webhook URL not configured",
                timestamp=datetime.utcnow()
            )
        
        # Create Discord embed
        color = int(self._get_severity_color(alert.severity).replace('#', ''), 16)
        
        payload = {
            'username': config.get('username', 'HexStrike AI'),
            'embeds': [
                {
                    'title': f"{alert.severity.value.upper()}: {alert.name}",
                    'description': alert.description,
                    'color': color,
                    'fields': [
                        {
                            'name': 'Message',
                            'value': alert.message,
                            'inline': False
                        },
                        {
                            'name': 'Service',
                            'value': alert.labels.get('service', 'Unknown'),
                            'inline': True
                        },
                        {
                            'name': 'Component',
                            'value': alert.labels.get('component', 'Unknown'),
                            'inline': True
                        },
                        {
                            'name': 'Timestamp',
                            'value': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'),
                            'inline': True
                        }
                    ],
                    'footer': {
                        'text': 'HexStrike AI Monitoring'
                    },
                    'timestamp': alert.timestamp.isoformat()
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 204:
                    return NotificationResult(
                        success=True,
                        channel='discord',
                        message="Notification sent successfully",
                        timestamp=datetime.utcnow()
                    )
                else:
                    error_text = await response.text()
                    return NotificationResult(
                        success=False,
                        channel='discord',
                        message=f"HTTP {response.status}: {error_text}",
                        timestamp=datetime.utcnow()
                    )
    
    async def _send_teams_notification(self, alert: Alert, config: Dict[str, Any]) -> NotificationResult:
        """Send Microsoft Teams notification"""
        webhook_url = config.get('webhook_url', '').replace('${TEAMS_WEBHOOK_URL}', 
                                                           os.getenv('TEAMS_WEBHOOK_URL', ''))
        
        if not webhook_url:
            return NotificationResult(
                success=False,
                channel='teams',
                message="Teams webhook URL not configured",
                timestamp=datetime.utcnow()
            )
        
        # Create Teams message card
        color = self._get_severity_color(alert.severity)
        
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color.replace('#', ''),
            "summary": f"{alert.severity.value.upper()}: {alert.name}",
            "sections": [
                {
                    "activityTitle": f"HexStrike AI Alert - {alert.severity.value.upper()}",
                    "activitySubtitle": alert.name,
                    "activityImage": "https://hexstrike.ai/logo.png",
                    "facts": [
                        {
                            "name": "Message",
                            "value": alert.message
                        },
                        {
                            "name": "Service",
                            "value": alert.labels.get('service', 'Unknown')
                        },
                        {
                            "name": "Component",
                            "value": alert.labels.get('component', 'Unknown')
                        },
                        {
                            "name": "Timestamp",
                            "value": alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
                        }
                    ],
                    "markdown": True
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    return NotificationResult(
                        success=True,
                        channel='teams',
                        message="Notification sent successfully",
                        timestamp=datetime.utcnow()
                    )
                else:
                    error_text = await response.text()
                    return NotificationResult(
                        success=False,
                        channel='teams',
                        message=f"HTTP {response.status}: {error_text}",
                        timestamp=datetime.utcnow()
                    )
    
    async def _send_pagerduty_notification(self, alert: Alert, config: Dict[str, Any]) -> NotificationResult:
        """Send PagerDuty notification"""
        integration_key = config.get('integration_key', '').replace('${PAGERDUTY_INTEGRATION_KEY}', 
                                                                   os.getenv('PAGERDUTY_INTEGRATION_KEY', ''))
        
        if not integration_key:
            return NotificationResult(
                success=False,
                channel='pagerduty',
                message="PagerDuty integration key not configured",
                timestamp=datetime.utcnow()
            )
        
        # Create PagerDuty event
        payload = {
            "routing_key": integration_key,
            "event_action": "trigger",
            "dedup_key": f"hexstrike-{alert.name}-{hash(str(alert.labels))}",
            "payload": {
                "summary": f"{alert.severity.value.upper()}: {alert.name}",
                "source": "HexStrike AI",
                "severity": alert.severity.value,
                "component": alert.labels.get('component', 'Unknown'),
                "group": alert.labels.get('service', 'Unknown'),
                "class": "HexStrike AI Alert",
                "custom_details": {
                    "message": alert.message,
                    "description": alert.description,
                    "labels": alert.labels,
                    "annotations": alert.annotations,
                    "timestamp": alert.timestamp.isoformat()
                }
            }
        }
        
        pagerduty_url = "https://events.pagerduty.com/v2/enqueue"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(pagerduty_url, json=payload) as response:
                if response.status == 202:
                    return NotificationResult(
                        success=True,
                        channel='pagerduty',
                        message="Notification sent successfully",
                        timestamp=datetime.utcnow()
                    )
                else:
                    error_text = await response.text()
                    return NotificationResult(
                        success=False,
                        channel='pagerduty',
                        message=f"HTTP {response.status}: {error_text}",
                        timestamp=datetime.utcnow()
                    )
    
    async def _send_webhook_notification(self, alert: Alert, config: Dict[str, Any]) -> NotificationResult:
        """Send generic webhook notification"""
        webhook_url = config.get('webhook_url', '').replace('${ALERT_WEBHOOK_URL}', 
                                                           os.getenv('ALERT_WEBHOOK_URL', ''))
        
        if not webhook_url:
            return NotificationResult(
                success=False,
                channel='webhook',
                message="Webhook URL not configured",
                timestamp=datetime.utcnow()
            )
        
        # Create webhook payload
        payload = {
            'alert': alert.to_dict(),
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'hexstrike-ai',
            'version': '1.0'
        }
        
        # Get headers
        headers = config.get('headers', {})
        headers['Content-Type'] = 'application/json'
        
        # Replace environment variables in headers
        for key, value in headers.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1].replace('Bearer ', '')
                headers[key] = f"Bearer {os.getenv(env_var, '')}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload, headers=headers) as response:
                if 200 <= response.status < 300:
                    return NotificationResult(
                        success=True,
                        channel='webhook',
                        message="Notification sent successfully",
                        timestamp=datetime.utcnow()
                    )
                else:
                    error_text = await response.text()
                    return NotificationResult(
                        success=False,
                        channel='webhook',
                        message=f"HTTP {response.status}: {error_text}",
                        timestamp=datetime.utcnow()
                    )
    
    def _create_email_body(self, alert: Alert) -> str:
        """Create HTML email body"""
        color = self._get_severity_color(alert.severity)
        
        labels_html = ''.join([
            f'<li><strong>{k}:</strong> {v}</li>' 
            for k, v in alert.labels.items()
        ])
        
        annotations_html = ''.join([
            f'<li><strong>{k}:</strong> {v}</li>' 
            for k, v in alert.annotations.items()
        ])
        
        runbook_url = alert.annotations.get('runbook_url', '#')
        dashboard_url = f"http://localhost:3000/d/hexstrike-overview"
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: {color}; border-bottom: 2px solid {color}; padding-bottom: 10px;">
                    {alert.severity.value.upper()}: {alert.name}
                </h2>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Message:</strong> {alert.message}</p>
                    <p><strong>Description:</strong> {alert.description}</p>
                    <p><strong>Service:</strong> {alert.labels.get('service', 'Unknown')}</p>
                    <p><strong>Component:</strong> {alert.labels.get('component', 'Unknown')}</p>
                    <p><strong>Timestamp:</strong> {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                </div>
                
                <h3>Labels:</h3>
                <ul style="background-color: #f0f0f0; padding: 10px; border-radius: 3px;">
                    {labels_html}
                </ul>
                
                <h3>Annotations:</h3>
                <ul style="background-color: #f0f0f0; padding: 10px; border-radius: 3px;">
                    {annotations_html}
                </ul>
                
                <div style="margin: 30px 0; text-align: center;">
                    <a href="{runbook_url}" style="background-color: #007cba; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">View Runbook</a>
                    <a href="{dashboard_url}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Dashboard</a>
                </div>
                
                <hr style="margin: 30px 0;">
                <p style="text-align: center; color: #666; font-size: 12px;">
                    <em>This alert was generated by HexStrike AI Monitoring System</em>
                </p>
            </div>
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
    
    def get_notification_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get notification history"""
        return [
            {
                'success': result.success,
                'channel': result.channel,
                'message': result.message,
                'timestamp': result.timestamp.isoformat(),
                'retry_count': result.retry_count
            }
            for result in self.notification_history[-limit:]
        ]
    
    def get_failed_notifications(self) -> List[Dict[str, Any]]:
        """Get failed notifications for retry"""
        return self.failed_notifications.copy()
    
    def clear_failed_notifications(self):
        """Clear failed notifications list"""
        self.failed_notifications.clear()


# Global notification service instance
notification_service = NotificationService()