# monitoring/dashboard_manager.py
"""
Grafana dashboard management for HexStrike AI system monitoring
"""
import os
import json
import requests
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from config.grafana_config import GrafanaAPIConfig


logger = logging.getLogger(__name__)


class DashboardManager:
    """Manages Grafana dashboards for HexStrike AI monitoring"""
    
    def __init__(self):
        self.api_config = GrafanaAPIConfig()
        self.session = requests.Session()
        self.session.auth = self.api_config.get_auth()
        
        # Dashboard configuration
        self.dashboard_configs = {
            "system-overview": {
                "file": "docker/grafana/provisioning/dashboards/system/overview-dashboard.json",
                "folder": "HexStrike System",
                "title": "HexStrike AI - System Overview",
                "uid": "hexstrike-overview",
                "tags": ["hexstrike", "overview", "system"]
            },
            "performance-monitoring": {
                "file": "docker/grafana/provisioning/dashboards/system/performance-dashboard.json",
                "folder": "HexStrike System",
                "title": "HexStrike AI - Performance Monitoring",
                "uid": "hexstrike-performance",
                "tags": ["hexstrike", "performance", "api"]
            },
            "resource-utilization": {
                "file": "docker/grafana/provisioning/dashboards/system/resource-utilization-dashboard.json",
                "folder": "HexStrike System",
                "title": "HexStrike AI - Resource Utilization",
                "uid": "hexstrike-resources",
                "tags": ["hexstrike", "resources", "system"]
            }
        }
    
    def load_dashboard_json(self, file_path: str) -> Dict[str, Any]:
        """Load dashboard JSON from file"""
        try:
            with open(file_path, 'r') as f:
                dashboard_json = json.load(f)
            return dashboard_json
        except FileNotFoundError:
            logger.error(f"Dashboard file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in dashboard file {file_path}: {str(e)}")
            return None
    
    def get_folder_id(self, folder_name: str) -> Optional[int]:
        """Get folder ID by name"""
        try:
            response = self.session.get(
                f"{self.api_config.base_url}/api/folders",
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                folders = response.json()
                for folder in folders:
                    if folder.get('title') == folder_name:
                        return folder.get('id')
            
            logger.warning(f"Folder '{folder_name}' not found")
            return None
            
        except Exception as e:
            logger.error(f"Error getting folder ID for '{folder_name}': {str(e)}")
            return None
    
    def create_folder(self, folder_name: str, folder_uid: str = None) -> Optional[int]:
        """Create a new folder"""
        try:
            folder_data = {
                "title": folder_name
            }
            
            if folder_uid:
                folder_data["uid"] = folder_uid
            
            response = self.session.post(
                f"{self.api_config.base_url}/api/folders",
                json=folder_data,
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                folder_info = response.json()
                logger.info(f"Created folder '{folder_name}' with ID {folder_info.get('id')}")
                return folder_info.get('id')
            else:
                logger.error(f"Failed to create folder '{folder_name}': {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating folder '{folder_name}': {str(e)}")
            return None
    
    def dashboard_exists(self, dashboard_uid: str) -> bool:
        """Check if dashboard exists"""
        try:
            response = self.session.get(
                f"{self.api_config.base_url}/api/dashboards/uid/{dashboard_uid}",
                headers=self.api_config.get_headers()
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error checking dashboard existence for UID '{dashboard_uid}': {str(e)}")
            return False
    
    def create_or_update_dashboard(self, dashboard_config: Dict[str, Any]) -> bool:
        """Create or update a dashboard"""
        try:
            # Load dashboard JSON
            dashboard_json = self.load_dashboard_json(dashboard_config["file"])
            if not dashboard_json:
                return False
            
            # Get or create folder
            folder_id = self.get_folder_id(dashboard_config["folder"])
            if folder_id is None:
                folder_uid = dashboard_config["folder"].lower().replace(" ", "-")
                folder_id = self.create_folder(dashboard_config["folder"], folder_uid)
                if folder_id is None:
                    logger.error(f"Failed to create folder '{dashboard_config['folder']}'")
                    return False
            
            # Prepare dashboard data
            dashboard_data = {
                "dashboard": dashboard_json,
                "folderId": folder_id,
                "overwrite": True,
                "message": "Updated by HexStrike AI Dashboard Manager"
            }
            
            # Set dashboard metadata
            dashboard_data["dashboard"]["id"] = None  # Let Grafana assign ID
            dashboard_data["dashboard"]["uid"] = dashboard_config["uid"]
            dashboard_data["dashboard"]["title"] = dashboard_config["title"]
            dashboard_data["dashboard"]["tags"] = dashboard_config["tags"]
            
            # Create or update dashboard
            response = self.session.post(
                f"{self.api_config.base_url}/api/dashboards/db",
                json=dashboard_data,
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Successfully created/updated dashboard '{dashboard_config['title']}' (UID: {dashboard_config['uid']})")
                return True
            else:
                logger.error(f"Failed to create/update dashboard '{dashboard_config['title']}': {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating/updating dashboard '{dashboard_config['title']}': {str(e)}")
            return False
    
    def deploy_all_dashboards(self) -> Dict[str, bool]:
        """Deploy all system monitoring dashboards"""
        results = {}
        
        logger.info("Starting deployment of system monitoring dashboards...")
        
        for dashboard_name, config in self.dashboard_configs.items():
            logger.info(f"Deploying dashboard: {dashboard_name}")
            success = self.create_or_update_dashboard(config)
            results[dashboard_name] = success
            
            if success:
                logger.info(f"✅ Successfully deployed {dashboard_name}")
            else:
                logger.error(f"❌ Failed to deploy {dashboard_name}")
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        logger.info(f"Dashboard deployment completed: {successful}/{total} successful")
        
        return results
    
    def get_dashboard_info(self, dashboard_uid: str) -> Optional[Dict[str, Any]]:
        """Get dashboard information"""
        try:
            response = self.session.get(
                f"{self.api_config.base_url}/api/dashboards/uid/{dashboard_uid}",
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get dashboard info for UID '{dashboard_uid}': {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting dashboard info for UID '{dashboard_uid}': {str(e)}")
            return None
    
    def list_dashboards(self) -> List[Dict[str, Any]]:
        """List all dashboards"""
        try:
            response = self.session.get(
                f"{self.api_config.base_url}/api/search?type=dash-db",
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to list dashboards: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error listing dashboards: {str(e)}")
            return []
    
    def delete_dashboard(self, dashboard_uid: str) -> bool:
        """Delete a dashboard"""
        try:
            response = self.session.delete(
                f"{self.api_config.base_url}/api/dashboards/uid/{dashboard_uid}",
                headers=self.api_config.get_headers()
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully deleted dashboard with UID '{dashboard_uid}'")
                return True
            else:
                logger.error(f"Failed to delete dashboard with UID '{dashboard_uid}': {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting dashboard with UID '{dashboard_uid}': {str(e)}")
            return False
    
    def validate_dashboards(self) -> Dict[str, Any]:
        """Validate that all system dashboards are properly deployed"""
        validation_results = {
            "valid": True,
            "dashboards": {},
            "summary": {
                "total": len(self.dashboard_configs),
                "deployed": 0,
                "missing": 0,
                "errors": 0
            }
        }
        
        for dashboard_name, config in self.dashboard_configs.items():
            dashboard_uid = config["uid"]
            
            try:
                if self.dashboard_exists(dashboard_uid):
                    dashboard_info = self.get_dashboard_info(dashboard_uid)
                    if dashboard_info:
                        validation_results["dashboards"][dashboard_name] = {
                            "status": "deployed",
                            "uid": dashboard_uid,
                            "title": dashboard_info.get("dashboard", {}).get("title", "Unknown"),
                            "url": f"{self.api_config.base_url}/d/{dashboard_uid}"
                        }
                        validation_results["summary"]["deployed"] += 1
                    else:
                        validation_results["dashboards"][dashboard_name] = {
                            "status": "error",
                            "uid": dashboard_uid,
                            "error": "Failed to get dashboard info"
                        }
                        validation_results["summary"]["errors"] += 1
                        validation_results["valid"] = False
                else:
                    validation_results["dashboards"][dashboard_name] = {
                        "status": "missing",
                        "uid": dashboard_uid
                    }
                    validation_results["summary"]["missing"] += 1
                    validation_results["valid"] = False
                    
            except Exception as e:
                validation_results["dashboards"][dashboard_name] = {
                    "status": "error",
                    "uid": dashboard_uid,
                    "error": str(e)
                }
                validation_results["summary"]["errors"] += 1
                validation_results["valid"] = False
        
        return validation_results
    
    def get_dashboard_urls(self) -> Dict[str, str]:
        """Get URLs for all system monitoring dashboards"""
        urls = {}
        
        for dashboard_name, config in self.dashboard_configs.items():
            dashboard_uid = config["uid"]
            if self.dashboard_exists(dashboard_uid):
                urls[dashboard_name] = f"{self.api_config.base_url}/d/{dashboard_uid}"
            else:
                urls[dashboard_name] = None
        
        return urls


def main():
    """Main function for dashboard management"""
    logging.basicConfig(level=logging.INFO)
    
    manager = DashboardManager()
    
    print("=== HexStrike AI Dashboard Manager ===")
    print()
    
    # Deploy all dashboards
    print("Deploying system monitoring dashboards...")
    results = manager.deploy_all_dashboards()
    
    print()
    print("Deployment Results:")
    for dashboard_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {dashboard_name}: {status}")
    
    print()
    
    # Validate deployment
    print("Validating dashboard deployment...")
    validation = manager.validate_dashboards()
    
    print(f"Validation Status: {'✅ VALID' if validation['valid'] else '❌ INVALID'}")
    print(f"Summary: {validation['summary']['deployed']}/{validation['summary']['total']} deployed")
    
    if validation["summary"]["missing"] > 0:
        print(f"Missing dashboards: {validation['summary']['missing']}")
    
    if validation["summary"]["errors"] > 0:
        print(f"Errors: {validation['summary']['errors']}")
    
    print()
    
    # Show dashboard URLs
    print("Dashboard URLs:")
    urls = manager.get_dashboard_urls()
    for dashboard_name, url in urls.items():
        if url:
            print(f"  {dashboard_name}: {url}")
        else:
            print(f"  {dashboard_name}: Not available")


if __name__ == "__main__":
    main()