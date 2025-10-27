# config/grafana_config.py
"""
Grafana configuration management for HexStrike AI monitoring
"""
import os
from typing import Dict, Any, List


class GrafanaConfig:
    """Grafana server configuration"""
    
    # Basic Grafana settings
    GRAFANA_HOST = os.getenv('GRAFANA_HOST', 'localhost')
    GRAFANA_PORT = int(os.getenv('GRAFANA_PORT', '3000'))
    GRAFANA_PROTOCOL = os.getenv('GRAFANA_PROTOCOL', 'http')
    GRAFANA_DOMAIN = os.getenv('GRAFANA_DOMAIN', 'localhost')
    
    # Authentication settings
    GRAFANA_ADMIN_USER = os.getenv('GRAFANA_ADMIN_USER', 'admin')
    GRAFANA_ADMIN_PASSWORD = os.getenv('GRAFANA_ADMIN_PASSWORD', 'admin')
    GRAFANA_SECRET_KEY = os.getenv('GRAFANA_SECRET_KEY', 'SW2YcwTIb9zpOOhoPsMm')
    
    # Database settings
    GRAFANA_DB_TYPE = os.getenv('GRAFANA_DB_TYPE', 'sqlite3')
    GRAFANA_DB_HOST = os.getenv('GRAFANA_DB_HOST', '127.0.0.1:3306')
    GRAFANA_DB_NAME = os.getenv('GRAFANA_DB_NAME', 'grafana')
    GRAFANA_DB_USER = os.getenv('GRAFANA_DB_USER', 'root')
    GRAFANA_DB_PASSWORD = os.getenv('GRAFANA_DB_PASSWORD', '')
    
    # Security settings
    GRAFANA_DISABLE_GRAVATAR = os.getenv('GRAFANA_DISABLE_GRAVATAR', 'false')
    GRAFANA_ALLOW_SIGN_UP = os.getenv('GRAFANA_ALLOW_SIGN_UP', 'false')
    GRAFANA_ALLOW_ORG_CREATE = os.getenv('GRAFANA_ALLOW_ORG_CREATE', 'false')
    
    # Auth0 integration settings
    GRAFANA_AUTH0_ENABLED = os.getenv('GRAFANA_AUTH0_ENABLED', 'false')
    GRAFANA_AUTH0_CLIENT_ID = os.getenv('GRAFANA_AUTH0_CLIENT_ID', '')
    GRAFANA_AUTH0_CLIENT_SECRET = os.getenv('GRAFANA_AUTH0_CLIENT_SECRET', '')
    GRAFANA_AUTH0_DOMAIN = os.getenv('GRAFANA_AUTH0_DOMAIN', '')
    
    # Prometheus data source settings
    PROMETHEUS_URL = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')
    PROMETHEUS_ACCESS = os.getenv('PROMETHEUS_ACCESS', 'proxy')
    
    @classmethod
    def get_grafana_config(cls) -> Dict[str, Any]:
        """Get complete Grafana configuration"""
        return {
            'server': {
                'http_addr': cls.GRAFANA_HOST,
                'http_port': cls.GRAFANA_PORT,
                'protocol': cls.GRAFANA_PROTOCOL,
                'domain': cls.GRAFANA_DOMAIN,
                'root_url': f"{cls.GRAFANA_PROTOCOL}://{cls.GRAFANA_DOMAIN}:{cls.GRAFANA_PORT}/"
            },
            'database': {
                'type': cls.GRAFANA_DB_TYPE,
                'host': cls.GRAFANA_DB_HOST,
                'name': cls.GRAFANA_DB_NAME,
                'user': cls.GRAFANA_DB_USER,
                'password': cls.GRAFANA_DB_PASSWORD
            },
            'security': {
                'admin_user': cls.GRAFANA_ADMIN_USER,
                'admin_password': cls.GRAFANA_ADMIN_PASSWORD,
                'secret_key': cls.GRAFANA_SECRET_KEY,
                'disable_gravatar': cls.GRAFANA_DISABLE_GRAVATAR
            },
            'users': {
                'allow_sign_up': cls.GRAFANA_ALLOW_SIGN_UP,
                'allow_org_create': cls.GRAFANA_ALLOW_ORG_CREATE,
                'auto_assign_org': True,
                'auto_assign_org_role': 'Viewer'
            },
            'auth': {
                'disable_login_form': cls.GRAFANA_AUTH0_ENABLED,
                'disable_signout_menu': cls.GRAFANA_AUTH0_ENABLED
            }
        }
    
    @classmethod
    def get_auth0_config(cls) -> Dict[str, Any]:
        """Get Auth0 OAuth configuration for Grafana"""
        if cls.GRAFANA_AUTH0_ENABLED.lower() == 'true':
            return {
                'auth.generic_oauth': {
                    'enabled': True,
                    'name': 'Auth0',
                    'allow_sign_up': True,
                    'client_id': cls.GRAFANA_AUTH0_CLIENT_ID,
                    'client_secret': cls.GRAFANA_AUTH0_CLIENT_SECRET,
                    'scopes': 'openid profile email',
                    'auth_url': f"https://{cls.GRAFANA_AUTH0_DOMAIN}/authorize",
                    'token_url': f"https://{cls.GRAFANA_AUTH0_DOMAIN}/oauth/token",
                    'api_url': f"https://{cls.GRAFANA_AUTH0_DOMAIN}/userinfo",
                    'role_attribute_path': "contains(groups[*], 'admin') && 'Admin' || contains(groups[*], 'editor') && 'Editor' || 'Viewer'",
                    'allow_assign_grafana_admin': True
                }
            }
        return {}
    
    @classmethod
    def get_prometheus_datasource_config(cls) -> Dict[str, Any]:
        """Get Prometheus data source configuration"""
        return {
            'name': 'Prometheus',
            'type': 'prometheus',
            'access': cls.PROMETHEUS_ACCESS,
            'url': cls.PROMETHEUS_URL,
            'isDefault': True,
            'jsonData': {
                'httpMethod': 'POST',
                'queryTimeout': '60s',
                'timeInterval': '30s'
            }
        }
    
    @classmethod
    def get_user_roles(cls) -> List[Dict[str, Any]]:
        """Get default user roles configuration"""
        return [
            {
                'name': 'HexStrike Admin',
                'permissions': [
                    'dashboards:read',
                    'dashboards:write',
                    'dashboards:create',
                    'dashboards:delete',
                    'users:read',
                    'users:write',
                    'orgs:read',
                    'orgs:write'
                ]
            },
            {
                'name': 'Security Analyst',
                'permissions': [
                    'dashboards:read',
                    'dashboards:write',
                    'dashboards:create'
                ]
            },
            {
                'name': 'Viewer',
                'permissions': [
                    'dashboards:read'
                ]
            }
        ]


class GrafanaAPIConfig:
    """Grafana API configuration for programmatic access"""
    
    def __init__(self):
        self.base_url = f"{GrafanaConfig.GRAFANA_PROTOCOL}://{GrafanaConfig.GRAFANA_HOST}:{GrafanaConfig.GRAFANA_PORT}"
        self.admin_user = GrafanaConfig.GRAFANA_ADMIN_USER
        self.admin_password = GrafanaConfig.GRAFANA_ADMIN_PASSWORD
    
    def get_headers(self, api_key: str = None) -> Dict[str, str]:
        """Get API headers for Grafana requests"""
        if api_key:
            return {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
        return {
            'Content-Type': 'application/json'
        }
    
    def get_auth(self) -> tuple:
        """Get basic auth credentials"""
        return (self.admin_user, self.admin_password)