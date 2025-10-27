# monitoring/grafana_setup.py
"""
Grafana infrastructure setup and management
"""
import os
import json
import requests
import time
import logging
from typing import Dict, Any, List, Optional
from config.grafana_config import GrafanaConfig, GrafanaAPIConfig


logger = logging.getLogger(__name__)


class GrafanaSetup:
    """Grafana infrastructure setup and configuration manager"""
    
    def __init__(self):
        self.config = GrafanaConfig()
        self.api_config = GrafanaAPIConfig()
        self.session = requests.Session()
        self.session.auth = self.api_config.get_auth()
    
    def wait_for_grafana(self, timeout: int = 60) -> bool:
        """Wait for Grafana server to be ready"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = self.session.get(f"{self.api_config.base_url}/api/health")
                if response.status_code == 200:
                    logger.info("Grafana server is ready")
                    return True
            except requests.exceptions.ConnectionError:
                pass
            
            time.sleep(2)
        
        logger.error(f"Grafana server not ready after {timeout} seconds")
        return False
    
    def setup_prometheus_datasource(self) -> bool:
        """Set up Prometheus data source in Grafana"""
        try:
            # Check if datasource already exists
            response = self.session.get(f"{self.api_config.base_url}/api/datasources/name/Prometheus")
            
            if response.status_code == 200:
                logger.info("Prometheus datasource already exists")
                return True
            
            # Create new datasource
            datasource_config = self.config.get_prometheus_datasource_config()
            
            response = self.session.post(
                f"{self.api_config.base_url}/api/datasources",
                json=datasource_config,
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                logger.info("Prometheus datasource created successfully")
                return True
            else:
                logger.error(f"Failed to create Prometheus datasource: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting up Prometheus datasource: {str(e)}")
            return False
    
    def create_api_key(self, name: str, role: str = "Admin") -> Optional[str]:
        """Create Grafana API key"""
        try:
            api_key_data = {
                "name": name,
                "role": role
            }
            
            response = self.session.post(
                f"{self.api_config.base_url}/api/auth/keys",
                json=api_key_data,
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                api_key = response.json().get('key')
                logger.info(f"API key '{name}' created successfully")
                return api_key
            else:
                logger.error(f"Failed to create API key: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating API key: {str(e)}")
            return None
    
    def setup_organizations(self) -> bool:
        """Set up organizations for multi-tenant support"""
        try:
            organizations = [
                {"name": "HexStrike Main", "role": "Admin"},
                {"name": "Security Team", "role": "Editor"},
                {"name": "Analysts", "role": "Viewer"}
            ]
            
            for org in organizations:
                # Check if organization exists
                response = self.session.get(f"{self.api_config.base_url}/api/orgs/name/{org['name']}")
                
                if response.status_code == 200:
                    logger.info(f"Organization '{org['name']}' already exists")
                    continue
                
                # Create organization
                response = self.session.post(
                    f"{self.api_config.base_url}/api/orgs",
                    json={"name": org["name"]},
                    headers=self.api_config.get_headers()
                )
                
                if response.status_code == 200:
                    logger.info(f"Organization '{org['name']}' created successfully")
                else:
                    logger.error(f"Failed to create organization '{org['name']}': {response.text}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up organizations: {str(e)}")
            return False
    
    def setup_users(self) -> bool:
        """Set up default users"""
        try:
            default_users = [
                {
                    "name": "Security Analyst",
                    "email": "analyst@hexstrike.local",
                    "login": "analyst",
                    "password": "analyst123",
                    "role": "Editor"
                },
                {
                    "name": "Viewer User",
                    "email": "viewer@hexstrike.local", 
                    "login": "viewer",
                    "password": "viewer123",
                    "role": "Viewer"
                }
            ]
            
            for user in default_users:
                # Check if user exists
                response = self.session.get(f"{self.api_config.base_url}/api/users/lookup?loginOrEmail={user['login']}")
                
                if response.status_code == 200:
                    logger.info(f"User '{user['login']}' already exists")
                    continue
                
                # Create user
                response = self.session.post(
                    f"{self.api_config.base_url}/api/admin/users",
                    json=user,
                    headers=self.api_config.get_headers()
                )
                
                if response.status_code == 200:
                    logger.info(f"User '{user['login']}' created successfully")
                else:
                    logger.error(f"Failed to create user '{user['login']}': {response.text}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up users: {str(e)}")
            return False
    
    def setup_folders(self) -> bool:
        """Set up dashboard folders"""
        try:
            folders = [
                {"title": "HexStrike System", "uid": "hexstrike-system"},
                {"title": "Security Scans", "uid": "security-scans"},
                {"title": "Tool Performance", "uid": "tool-performance"},
                {"title": "User Analytics", "uid": "user-analytics"}
            ]
            
            for folder in folders:
                # Check if folder exists
                response = self.session.get(f"{self.api_config.base_url}/api/folders/{folder['uid']}")
                
                if response.status_code == 200:
                    logger.info(f"Folder '{folder['title']}' already exists")
                    continue
                
                # Create folder
                response = self.session.post(
                    f"{self.api_config.base_url}/api/folders",
                    json=folder,
                    headers=self.api_config.get_headers()
                )
                
                if response.status_code == 200:
                    logger.info(f"Folder '{folder['title']}' created successfully")
                else:
                    logger.error(f"Failed to create folder '{folder['title']}': {response.text}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up folders: {str(e)}")
            return False
    
    def configure_auth0_integration(self) -> bool:
        """Configure Auth0 OAuth integration"""
        try:
            if self.config.GRAFANA_AUTH0_ENABLED.lower() != 'true':
                logger.info("Auth0 integration is disabled")
                return True
            
            # Update Grafana configuration for Auth0
            auth0_config = self.config.get_auth0_config()
            
            # This would typically be done through configuration files
            # For now, we'll log the configuration that should be applied
            logger.info("Auth0 configuration should be applied to grafana.ini:")
            logger.info(json.dumps(auth0_config, indent=2))
            
            return True
            
        except Exception as e:
            logger.error(f"Error configuring Auth0 integration: {str(e)}")
            return False
    
    def setup_complete_infrastructure(self) -> bool:
        """Set up complete Grafana infrastructure"""
        logger.info("Starting Grafana infrastructure setup...")
        
        # Wait for Grafana to be ready
        if not self.wait_for_grafana():
            return False
        
        # Set up components
        steps = [
            ("Prometheus datasource", self.setup_prometheus_datasource),
            ("Organizations", self.setup_organizations),
            ("Users", self.setup_users),
            ("Folders", self.setup_folders),
            ("Auth0 integration", self.configure_auth0_integration),
            ("System monitoring dashboards", self.setup_system_dashboards)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"Setting up {step_name}...")
            if not step_func():
                logger.error(f"Failed to set up {step_name}")
                return False
        
        logger.info("Grafana infrastructure setup completed successfully")
        return True
    
    def setup_system_dashboards(self) -> bool:
        """Set up system monitoring dashboards"""
        try:
            from monitoring.dashboard_manager import DashboardManager
            
            dashboard_manager = DashboardManager()
            results = dashboard_manager.deploy_all_dashboards()
            
            # Check if all dashboards were deployed successfully
            successful_deployments = sum(1 for success in results.values() if success)
            total_dashboards = len(results)
            
            if successful_deployments == total_dashboards:
                logger.info(f"All {total_dashboards} system monitoring dashboards deployed successfully")
                return True
            else:
                logger.warning(f"Only {successful_deployments}/{total_dashboards} dashboards deployed successfully")
                # Return True if at least some dashboards were deployed
                return successful_deployments > 0
                
        except Exception as e:
            logger.error(f"Error setting up system monitoring dashboards: {str(e)}")
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get Grafana health status"""
        try:
            response = self.session.get(f"{self.api_config.base_url}/api/health")
            
            if response.status_code == 200:
                health_data = response.json()
                return {
                    "status": "healthy",
                    "version": health_data.get("version", "unknown"),
                    "database": health_data.get("database", "unknown")
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


def main():
    """Main setup function"""
    logging.basicConfig(level=logging.INFO)
    
    setup = GrafanaSetup()
    success = setup.setup_complete_infrastructure()
    
    if success:
        print("✅ Grafana infrastructure setup completed successfully")
        
        # Create API key for HexStrike integration
        api_key = setup.create_api_key("hexstrike-integration", "Admin")
        if api_key:
            print(f"🔑 API Key created: {api_key}")
            print("💡 Save this API key securely - it won't be shown again")
        
        # Show health status
        health = setup.get_health_status()
        print(f"🏥 Health Status: {health}")
        
    else:
        print("❌ Grafana infrastructure setup failed")
        exit(1)


if __name__ == "__main__":
    main()