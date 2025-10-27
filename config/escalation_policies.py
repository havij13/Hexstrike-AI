# config/escalation_policies.py
"""
Escalation policies configuration for HexStrike AI alerting system
Defines how alerts should be escalated based on severity and time
"""
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class EscalationLevel(Enum):
    """Escalation levels"""
    LEVEL_1 = "level_1"  # Initial notification
    LEVEL_2 = "level_2"  # First escalation
    LEVEL_3 = "level_3"  # Second escalation
    LEVEL_4 = "level_4"  # Final escalation


@dataclass
class EscalationRule:
    """Individual escalation rule"""
    level: EscalationLevel
    after_minutes: int
    notification_channels: List[str]
    additional_recipients: List[str] = None
    repeat_interval_minutes: int = None
    
    def __post_init__(self):
        if self.additional_recipients is None:
            self.additional_recipients = []


class EscalationPolicies:
    """Escalation policies configuration"""
    
    @staticmethod
    def get_critical_escalation_policy() -> List[EscalationRule]:
        """Critical alert escalation policy - immediate and aggressive escalation"""
        return [
            EscalationRule(
                level=EscalationLevel.LEVEL_1,
                after_minutes=0,
                notification_channels=['slack-alerts', 'email-alerts'],
                additional_recipients=[],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_2,
                after_minutes=5,
                notification_channels=['discord-alerts', 'teams-alerts', 'pagerduty-alerts'],
                additional_recipients=['oncall@hexstrike.ai', 'security-team@hexstrike.ai'],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_3,
                after_minutes=15,
                notification_channels=['webhook-alerts', 'email-alerts'],
                additional_recipients=['management@hexstrike.ai', 'cto@hexstrike.ai'],
                repeat_interval_minutes=10  # Repeat every 10 minutes
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_4,
                after_minutes=30,
                notification_channels=['pagerduty-alerts'],
                additional_recipients=['ceo@hexstrike.ai', 'emergency@hexstrike.ai'],
                repeat_interval_minutes=15  # Repeat every 15 minutes
            )
        ]
    
    @staticmethod
    def get_warning_escalation_policy() -> List[EscalationRule]:
        """Warning alert escalation policy - moderate escalation"""
        return [
            EscalationRule(
                level=EscalationLevel.LEVEL_1,
                after_minutes=0,
                notification_channels=['slack-alerts'],
                additional_recipients=[],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_2,
                after_minutes=10,
                notification_channels=['email-alerts'],
                additional_recipients=['team-leads@hexstrike.ai'],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_3,
                after_minutes=30,
                notification_channels=['teams-alerts', 'webhook-alerts'],
                additional_recipients=['oncall@hexstrike.ai'],
                repeat_interval_minutes=20  # Repeat every 20 minutes
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_4,
                after_minutes=60,
                notification_channels=['pagerduty-alerts'],
                additional_recipients=['management@hexstrike.ai'],
                repeat_interval_minutes=30  # Repeat every 30 minutes
            )
        ]
    
    @staticmethod
    def get_info_escalation_policy() -> List[EscalationRule]:
        """Info alert escalation policy - minimal escalation"""
        return [
            EscalationRule(
                level=EscalationLevel.LEVEL_1,
                after_minutes=0,
                notification_channels=['slack-alerts'],
                additional_recipients=[],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_2,
                after_minutes=60,
                notification_channels=['email-alerts'],
                additional_recipients=[],
                repeat_interval_minutes=None
            )
        ]
    
    @staticmethod
    def get_security_escalation_policy() -> List[EscalationRule]:
        """Security-specific alert escalation policy - immediate and comprehensive"""
        return [
            EscalationRule(
                level=EscalationLevel.LEVEL_1,
                after_minutes=0,
                notification_channels=['slack-alerts', 'discord-alerts', 'email-alerts'],
                additional_recipients=['security-team@hexstrike.ai', 'soc@hexstrike.ai'],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_2,
                after_minutes=2,
                notification_channels=['pagerduty-alerts', 'teams-alerts'],
                additional_recipients=['security-lead@hexstrike.ai', 'incident-response@hexstrike.ai'],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_3,
                after_minutes=5,
                notification_channels=['webhook-alerts'],
                additional_recipients=['ciso@hexstrike.ai', 'management@hexstrike.ai'],
                repeat_interval_minutes=5  # Repeat every 5 minutes for security incidents
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_4,
                after_minutes=10,
                notification_channels=['pagerduty-alerts'],
                additional_recipients=['ceo@hexstrike.ai', 'legal@hexstrike.ai'],
                repeat_interval_minutes=10  # Continue repeating for critical security issues
            )
        ]
    
    @staticmethod
    def get_infrastructure_escalation_policy() -> List[EscalationRule]:
        """Infrastructure-specific alert escalation policy"""
        return [
            EscalationRule(
                level=EscalationLevel.LEVEL_1,
                after_minutes=0,
                notification_channels=['slack-alerts'],
                additional_recipients=['devops@hexstrike.ai'],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_2,
                after_minutes=5,
                notification_channels=['email-alerts', 'teams-alerts'],
                additional_recipients=['infrastructure-team@hexstrike.ai', 'oncall@hexstrike.ai'],
                repeat_interval_minutes=None
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_3,
                after_minutes=15,
                notification_channels=['pagerduty-alerts'],
                additional_recipients=['platform-lead@hexstrike.ai'],
                repeat_interval_minutes=15
            ),
            EscalationRule(
                level=EscalationLevel.LEVEL_4,
                after_minutes=30,
                notification_channels=['webhook-alerts'],
                additional_recipients=['cto@hexstrike.ai'],
                repeat_interval_minutes=20
            )
        ]
    
    @staticmethod
    def get_escalation_policy_by_labels(labels: Dict[str, str]) -> List[EscalationRule]:
        """Get appropriate escalation policy based on alert labels"""
        severity = labels.get('severity', 'info').lower()
        service = labels.get('service', '').lower()
        component = labels.get('component', '').lower()
        
        # Security-related alerts get special treatment
        if (component in ['auth', 'security'] or 
            service in ['security', 'auth'] or 
            'security' in labels.get('team', '').lower()):
            return EscalationPolicies.get_security_escalation_policy()
        
        # Infrastructure alerts
        if (service in ['system', 'redis', 'database', 'infrastructure'] or
            component in ['infrastructure', 'database', 'cache'] or
            'infrastructure' in labels.get('team', '').lower()):
            return EscalationPolicies.get_infrastructure_escalation_policy()
        
        # Severity-based escalation
        if severity == 'critical':
            return EscalationPolicies.get_critical_escalation_policy()
        elif severity == 'warning':
            return EscalationPolicies.get_warning_escalation_policy()
        else:
            return EscalationPolicies.get_info_escalation_policy()
    
    @staticmethod
    def get_all_policies() -> Dict[str, List[EscalationRule]]:
        """Get all available escalation policies"""
        return {
            'critical': EscalationPolicies.get_critical_escalation_policy(),
            'warning': EscalationPolicies.get_warning_escalation_policy(),
            'info': EscalationPolicies.get_info_escalation_policy(),
            'security': EscalationPolicies.get_security_escalation_policy(),
            'infrastructure': EscalationPolicies.get_infrastructure_escalation_policy()
        }


class NotificationChannelConfig:
    """Notification channel configuration"""
    
    @staticmethod
    def get_channel_configs() -> Dict[str, Dict[str, Any]]:
        """Get notification channel configurations"""
        return {
            'slack-alerts': {
                'type': 'slack',
                'enabled': True,
                'webhook_url': '${SLACK_WEBHOOK_URL}',
                'channel': '${SLACK_CHANNEL:#alerts}',
                'username': 'HexStrike AI',
                'icon_emoji': ':rotating_light:',
                'severity_filter': ['info', 'warning', 'critical'],
                'rate_limit': {
                    'max_per_minute': 10,
                    'burst_limit': 5
                }
            },
            'email-alerts': {
                'type': 'email',
                'enabled': True,
                'smtp_host': '${SMTP_HOST}',
                'smtp_port': '${SMTP_PORT:587}',
                'smtp_user': '${SMTP_USER}',
                'smtp_password': '${SMTP_PASSWORD}',
                'from_email': '${ALERT_FROM_EMAIL:alerts@hexstrike.ai}',
                'to_emails': '${ALERT_TO_EMAILS}'.split(','),
                'severity_filter': ['warning', 'critical'],
                'rate_limit': {
                    'max_per_minute': 5,
                    'burst_limit': 2
                }
            },
            'discord-alerts': {
                'type': 'discord',
                'enabled': True,
                'webhook_url': '${DISCORD_WEBHOOK_URL}',
                'username': 'HexStrike AI',
                'severity_filter': ['critical'],
                'rate_limit': {
                    'max_per_minute': 8,
                    'burst_limit': 3
                }
            },
            'teams-alerts': {
                'type': 'teams',
                'enabled': True,
                'webhook_url': '${TEAMS_WEBHOOK_URL}',
                'severity_filter': ['warning', 'critical'],
                'rate_limit': {
                    'max_per_minute': 6,
                    'burst_limit': 3
                }
            },
            'pagerduty-alerts': {
                'type': 'pagerduty',
                'enabled': True,
                'integration_key': '${PAGERDUTY_INTEGRATION_KEY}',
                'severity_filter': ['critical'],
                'rate_limit': {
                    'max_per_minute': 3,
                    'burst_limit': 1
                }
            },
            'webhook-alerts': {
                'type': 'webhook',
                'enabled': True,
                'webhook_url': '${ALERT_WEBHOOK_URL}',
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ${WEBHOOK_AUTH_TOKEN}'
                },
                'severity_filter': ['warning', 'critical'],
                'rate_limit': {
                    'max_per_minute': 15,
                    'burst_limit': 5
                }
            }
        }
    
    @staticmethod
    def get_notification_templates() -> Dict[str, Dict[str, str]]:
        """Get notification message templates"""
        return {
            'slack': {
                'title': '🚨 {severity} Alert: {alert_name}',
                'message': '''
*{severity}*: {summary}

{description}

*Service:* {service}
*Component:* {component}
*Time:* {timestamp}
*Runbook:* {runbook_url}
                '''.strip()
            },
            'email': {
                'subject': '[HexStrike AI] {severity}: {alert_name}',
                'body': '''
<h2 style="color: {severity_color};">{severity}: {alert_name}</h2>

<p><strong>Summary:</strong> {summary}</p>
<p><strong>Description:</strong> {description}</p>
<p><strong>Service:</strong> {service}</p>
<p><strong>Component:</strong> {component}</p>
<p><strong>Timestamp:</strong> {timestamp}</p>

<h3>Labels:</h3>
<ul>
{labels_html}
</ul>

<h3>Annotations:</h3>
<ul>
{annotations_html}
</ul>

<p><a href="{runbook_url}">View Runbook</a> | <a href="{dashboard_url}">View Dashboard</a></p>

<hr>
<p><em>This alert was generated by HexStrike AI Monitoring System</em></p>
                '''.strip()
            },
            'discord': {
                'title': '🚨 {severity} Alert',
                'description': '''
**{alert_name}**

{description}

**Service:** {service}
**Component:** {component}
**Time:** {timestamp}
                '''.strip()
            },
            'teams': {
                'title': 'HexStrike AI Alert',
                'summary': '{severity}: {alert_name}',
                'text': '''
**{severity}**: {summary}

{description}

**Service:** {service}
**Component:** {component}
**Time:** {timestamp}
**Runbook:** {runbook_url}
                '''.strip()
            }
        }


class AlertThresholds:
    """Alert threshold configurations"""
    
    @staticmethod
    def get_system_thresholds() -> Dict[str, Dict[str, Any]]:
        """Get system-level alert thresholds"""
        return {
            'cpu_usage': {
                'warning': 80,
                'critical': 95,
                'duration_minutes': 5
            },
            'memory_usage': {
                'warning': 85,
                'critical': 95,
                'duration_minutes': 5
            },
            'disk_usage': {
                'warning': 85,
                'critical': 95,
                'duration_minutes': 5
            },
            'response_time': {
                'warning': 2.0,  # seconds
                'critical': 5.0,
                'duration_minutes': 5
            },
            'error_rate': {
                'warning': 0.05,  # 5%
                'critical': 0.10,  # 10%
                'duration_minutes': 2
            }
        }
    
    @staticmethod
    def get_application_thresholds() -> Dict[str, Dict[str, Any]]:
        """Get application-level alert thresholds"""
        return {
            'scan_failure_rate': {
                'warning': 0.20,  # 20%
                'critical': 0.50,  # 50%
                'duration_minutes': 5
            },
            'tool_failure_rate': {
                'warning': 0.30,  # 30%
                'critical': 0.60,  # 60%
                'duration_minutes': 3
            },
            'auth_failure_rate': {
                'warning': 5,     # per second
                'critical': 20,   # per second
                'duration_minutes': 2
            },
            'active_scans': {
                'warning': 50,
                'critical': 100,
                'duration_minutes': 5
            },
            'scan_duration': {
                'warning': 1800,  # 30 minutes
                'critical': 3600, # 60 minutes
                'duration_minutes': 10
            }
        }
    
    @staticmethod
    def get_security_thresholds() -> Dict[str, Dict[str, Any]]:
        """Get security-specific alert thresholds"""
        return {
            'suspicious_requests': {
                'warning': 1,     # per second
                'critical': 5,    # per second
                'duration_minutes': 1
            },
            'failed_logins': {
                'warning': 10,    # per minute
                'critical': 50,   # per minute
                'duration_minutes': 1
            },
            'privilege_escalation': {
                'warning': 1,     # any occurrence
                'critical': 1,    # any occurrence
                'duration_minutes': 0
            },
            'data_exfiltration': {
                'warning': 1,     # any occurrence
                'critical': 1,    # any occurrence
                'duration_minutes': 0
            }
        }