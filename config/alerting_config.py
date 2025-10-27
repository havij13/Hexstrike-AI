# config/alerting_config.py
"""
Alerting configuration for HexStrike AI
Centralizes all alerting-related configuration and environment variables
"""
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class AlertingConfig:
    """Main alerting configuration class"""
    
    # Email configuration
    SMTP_HOST: str = os.getenv('SMTP_HOST', '')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER: str = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', '')
    SMTP_USE_TLS: bool = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
    
    # Alert email settings
    ALERT_FROM_EMAIL: str = os.getenv('ALERT_FROM_EMAIL', 'alerts@hexstrike.ai')
    ALERT_TO_EMAILS: List[str] = os.getenv('ALERT_TO_EMAILS', '').split(',')
    ALERT_CC_EMAILS: List[str] = os.getenv('ALERT_CC_EMAILS', '').split(',')
    ALERT_BCC_EMAILS: List[str] = os.getenv('ALERT_BCC_EMAILS', '').split(',')
    
    # Slack configuration
    SLACK_WEBHOOK_URL: str = os.getenv('SLACK_WEBHOOK_URL', '')
    SLACK_CHANNEL: str = os.getenv('SLACK_CHANNEL', '#alerts')
    SLACK_USERNAME: str = os.getenv('SLACK_USERNAME', 'HexStrike AI')
    SLACK_ICON_EMOJI: str = os.getenv('SLACK_ICON_EMOJI', ':rotating_light:')
    
    # Discord configuration
    DISCORD_WEBHOOK_URL: str = os.getenv('DISCORD_WEBHOOK_URL', '')
    DISCORD_USERNAME: str = os.getenv('DISCORD_USERNAME', 'HexStrike AI')
    DISCORD_AVATAR_URL: str = os.getenv('DISCORD_AVATAR_URL', '')
    
    # Microsoft Teams configuration
    TEAMS_WEBHOOK_URL: str = os.getenv('TEAMS_WEBHOOK_URL', '')
    
    # PagerDuty configuration
    PAGERDUTY_INTEGRATION_KEY: str = os.getenv('PAGERDUTY_INTEGRATION_KEY', '')
    PAGERDUTY_SERVICE_KEY: str = os.getenv('PAGERDUTY_SERVICE_KEY', '')
    
    # Generic webhook configuration
    ALERT_WEBHOOK_URL: str = os.getenv('ALERT_WEBHOOK_URL', '')
    WEBHOOK_AUTH_TOKEN: str = os.getenv('WEBHOOK_AUTH_TOKEN', '')
    WEBHOOK_TIMEOUT: int = int(os.getenv('WEBHOOK_TIMEOUT', '30'))
    
    # Grafana configuration
    GRAFANA_URL: str = os.getenv('GRAFANA_URL', 'http://localhost:3000')
    GRAFANA_API_KEY: str = os.getenv('GRAFANA_API_KEY', '')
    GRAFANA_ADMIN_USER: str = os.getenv('GRAFANA_ADMIN_USER', 'admin')
    GRAFANA_ADMIN_PASSWORD: str = os.getenv('GRAFANA_ADMIN_PASSWORD', 'admin')
    
    # Prometheus configuration
    PROMETHEUS_URL: str = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
    PROMETHEUS_QUERY_TIMEOUT: int = int(os.getenv('PROMETHEUS_QUERY_TIMEOUT', '30'))
    
    # Alert manager configuration
    ALERTMANAGER_URL: str = os.getenv('ALERTMANAGER_URL', 'http://localhost:9093')
    
    # General alerting settings
    ALERT_ENABLED: bool = os.getenv('ALERT_ENABLED', 'true').lower() == 'true'
    ALERT_DEFAULT_SEVERITY: str = os.getenv('ALERT_DEFAULT_SEVERITY', 'warning')
    ALERT_RETENTION_DAYS: int = int(os.getenv('ALERT_RETENTION_DAYS', '30'))
    ALERT_MAX_HISTORY: int = int(os.getenv('ALERT_MAX_HISTORY', '1000'))
    
    # Rate limiting settings
    ALERT_RATE_LIMIT_ENABLED: bool = os.getenv('ALERT_RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    ALERT_MAX_PER_MINUTE: int = int(os.getenv('ALERT_MAX_PER_MINUTE', '10'))
    ALERT_BURST_LIMIT: int = int(os.getenv('ALERT_BURST_LIMIT', '5'))
    
    # Escalation settings
    ESCALATION_ENABLED: bool = os.getenv('ESCALATION_ENABLED', 'true').lower() == 'true'
    ESCALATION_CHECK_INTERVAL: int = int(os.getenv('ESCALATION_CHECK_INTERVAL', '60'))  # seconds
    
    # Notification retry settings
    NOTIFICATION_RETRY_ENABLED: bool = os.getenv('NOTIFICATION_RETRY_ENABLED', 'true').lower() == 'true'
    NOTIFICATION_MAX_RETRIES: int = int(os.getenv('NOTIFICATION_MAX_RETRIES', '3'))
    NOTIFICATION_RETRY_DELAY: int = int(os.getenv('NOTIFICATION_RETRY_DELAY', '300'))  # seconds
    
    # Security settings
    ALERT_ENCRYPTION_ENABLED: bool = os.getenv('ALERT_ENCRYPTION_ENABLED', 'false').lower() == 'true'
    ALERT_ENCRYPTION_KEY: str = os.getenv('ALERT_ENCRYPTION_KEY', '')
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Clean up email lists
        self.ALERT_TO_EMAILS = [email.strip() for email in self.ALERT_TO_EMAILS if email.strip()]
        self.ALERT_CC_EMAILS = [email.strip() for email in self.ALERT_CC_EMAILS if email.strip()]
        self.ALERT_BCC_EMAILS = [email.strip() for email in self.ALERT_BCC_EMAILS if email.strip()]
    
    def is_email_configured(self) -> bool:
        """Check if email configuration is complete"""
        return bool(self.SMTP_HOST and self.SMTP_USER and self.SMTP_PASSWORD and 
                   self.ALERT_FROM_EMAIL and self.ALERT_TO_EMAILS)
    
    def is_slack_configured(self) -> bool:
        """Check if Slack configuration is complete"""
        return bool(self.SLACK_WEBHOOK_URL)
    
    def is_discord_configured(self) -> bool:
        """Check if Discord configuration is complete"""
        return bool(self.DISCORD_WEBHOOK_URL)
    
    def is_teams_configured(self) -> bool:
        """Check if Teams configuration is complete"""
        return bool(self.TEAMS_WEBHOOK_URL)
    
    def is_pagerduty_configured(self) -> bool:
        """Check if PagerDuty configuration is complete"""
        return bool(self.PAGERDUTY_INTEGRATION_KEY)
    
    def is_webhook_configured(self) -> bool:
        """Check if generic webhook configuration is complete"""
        return bool(self.ALERT_WEBHOOK_URL)
    
    def get_configured_channels(self) -> List[str]:
        """Get list of configured notification channels"""
        channels = []
        if self.is_email_configured():
            channels.append('email')
        if self.is_slack_configured():
            channels.append('slack')
        if self.is_discord_configured():
            channels.append('discord')
        if self.is_teams_configured():
            channels.append('teams')
        if self.is_pagerduty_configured():
            channels.append('pagerduty')
        if self.is_webhook_configured():
            channels.append('webhook')
        return channels
    
    def get_notification_config(self, channel: str) -> Dict[str, Any]:
        """Get configuration for specific notification channel"""
        configs = {
            'email': {
                'type': 'email',
                'enabled': self.is_email_configured(),
                'smtp_host': self.SMTP_HOST,
                'smtp_port': self.SMTP_PORT,
                'smtp_user': self.SMTP_USER,
                'smtp_password': self.SMTP_PASSWORD,
                'smtp_use_tls': self.SMTP_USE_TLS,
                'from_email': self.ALERT_FROM_EMAIL,
                'to_emails': self.ALERT_TO_EMAILS,
                'cc_emails': self.ALERT_CC_EMAILS,
                'bcc_emails': self.ALERT_BCC_EMAILS
            },
            'slack': {
                'type': 'slack',
                'enabled': self.is_slack_configured(),
                'webhook_url': self.SLACK_WEBHOOK_URL,
                'channel': self.SLACK_CHANNEL,
                'username': self.SLACK_USERNAME,
                'icon_emoji': self.SLACK_ICON_EMOJI
            },
            'discord': {
                'type': 'discord',
                'enabled': self.is_discord_configured(),
                'webhook_url': self.DISCORD_WEBHOOK_URL,
                'username': self.DISCORD_USERNAME,
                'avatar_url': self.DISCORD_AVATAR_URL
            },
            'teams': {
                'type': 'teams',
                'enabled': self.is_teams_configured(),
                'webhook_url': self.TEAMS_WEBHOOK_URL
            },
            'pagerduty': {
                'type': 'pagerduty',
                'enabled': self.is_pagerduty_configured(),
                'integration_key': self.PAGERDUTY_INTEGRATION_KEY,
                'service_key': self.PAGERDUTY_SERVICE_KEY
            },
            'webhook': {
                'type': 'webhook',
                'enabled': self.is_webhook_configured(),
                'webhook_url': self.ALERT_WEBHOOK_URL,
                'auth_token': self.WEBHOOK_AUTH_TOKEN,
                'timeout': self.WEBHOOK_TIMEOUT
            }
        }
        return configs.get(channel, {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'email': self.get_notification_config('email'),
            'slack': self.get_notification_config('slack'),
            'discord': self.get_notification_config('discord'),
            'teams': self.get_notification_config('teams'),
            'pagerduty': self.get_notification_config('pagerduty'),
            'webhook': self.get_notification_config('webhook'),
            'general': {
                'enabled': self.ALERT_ENABLED,
                'default_severity': self.ALERT_DEFAULT_SEVERITY,
                'retention_days': self.ALERT_RETENTION_DAYS,
                'max_history': self.ALERT_MAX_HISTORY,
                'rate_limit_enabled': self.ALERT_RATE_LIMIT_ENABLED,
                'max_per_minute': self.ALERT_MAX_PER_MINUTE,
                'burst_limit': self.ALERT_BURST_LIMIT,
                'escalation_enabled': self.ESCALATION_ENABLED,
                'escalation_check_interval': self.ESCALATION_CHECK_INTERVAL,
                'retry_enabled': self.NOTIFICATION_RETRY_ENABLED,
                'max_retries': self.NOTIFICATION_MAX_RETRIES,
                'retry_delay': self.NOTIFICATION_RETRY_DELAY
            },
            'grafana': {
                'url': self.GRAFANA_URL,
                'api_key': self.GRAFANA_API_KEY,
                'admin_user': self.GRAFANA_ADMIN_USER
            },
            'prometheus': {
                'url': self.PROMETHEUS_URL,
                'query_timeout': self.PROMETHEUS_QUERY_TIMEOUT
            },
            'alertmanager': {
                'url': self.ALERTMANAGER_URL
            }
        }


class AlertingEnvironment:
    """Environment-specific alerting configuration"""
    
    @staticmethod
    def get_development_config() -> AlertingConfig:
        """Get development environment configuration"""
        config = AlertingConfig()
        # Override for development
        config.ALERT_ENABLED = True
        config.ALERT_RATE_LIMIT_ENABLED = False  # Disable rate limiting in dev
        config.ESCALATION_ENABLED = False  # Disable escalation in dev
        return config
    
    @staticmethod
    def get_staging_config() -> AlertingConfig:
        """Get staging environment configuration"""
        config = AlertingConfig()
        # Override for staging
        config.ALERT_ENABLED = True
        config.ESCALATION_ENABLED = True
        config.ALERT_MAX_PER_MINUTE = 20  # Higher limit for staging
        return config
    
    @staticmethod
    def get_production_config() -> AlertingConfig:
        """Get production environment configuration"""
        config = AlertingConfig()
        # Production settings are the defaults
        return config
    
    @staticmethod
    def get_config_for_environment(env: str = None) -> AlertingConfig:
        """Get configuration for specific environment"""
        env = env or os.getenv('ENVIRONMENT', 'development').lower()
        
        if env == 'development':
            return AlertingEnvironment.get_development_config()
        elif env == 'staging':
            return AlertingEnvironment.get_staging_config()
        elif env == 'production':
            return AlertingEnvironment.get_production_config()
        else:
            return AlertingConfig()


# Global alerting configuration instance
alerting_config = AlertingEnvironment.get_config_for_environment()