#!/usr/bin/env python3
"""
Deploy security-specific Grafana dashboards for HexStrike AI
"""
import sys
import os
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from monitoring.dashboard_manager import DashboardManager
from monitoring.grafana_setup import GrafanaSetup


def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def deploy_security_dashboards():
    """Deploy security-specific dashboards"""
    print("🔒 HexStrike AI - Security Dashboard Deployment")
    print("=" * 50)
    
    try:
        # Initialize dashboard manager
        manager = DashboardManager()
        
        # Deploy security dashboards
        print("📊 Deploying security dashboards...")
        results = manager.deploy_security_dashboards()
        
        print("\n📋 Deployment Results:")
        print("-" * 30)
        
        for dashboard_name, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"  {dashboard_name}: {status}")
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        print(f"\n📈 Summary: {successful}/{total} dashboards deployed successfully")
        
        if successful == total:
            print("🎉 All security dashboards deployed successfully!")
            
            # Show dashboard URLs
            print("\n🔗 Dashboard URLs:")
            print("-" * 20)
            urls = manager.get_dashboard_urls()
            
            security_dashboards = ["scan-activity", "vulnerability-trends", "tool-performance"]
            for dashboard_name in security_dashboards:
                if dashboard_name in urls and urls[dashboard_name]:
                    print(f"  {dashboard_name}: {urls[dashboard_name]}")
                else:
                    print(f"  {dashboard_name}: Not available")
            
            return True
        else:
            print("⚠️  Some dashboards failed to deploy. Check logs for details.")
            return False
            
    except Exception as e:
        print(f"❌ Error deploying security dashboards: {str(e)}")
        return False


def validate_security_dashboards():
    """Validate security dashboard deployment"""
    print("\n🔍 Validating security dashboard deployment...")
    
    try:
        manager = DashboardManager()
        validation = manager.validate_dashboards()
        
        security_dashboards = ["scan-activity", "vulnerability-trends", "tool-performance"]
        security_validation = {
            "valid": True,
            "dashboards": {},
            "summary": {"total": 0, "deployed": 0, "missing": 0, "errors": 0}
        }
        
        for dashboard_name in security_dashboards:
            if dashboard_name in validation["dashboards"]:
                dashboard_info = validation["dashboards"][dashboard_name]
                security_validation["dashboards"][dashboard_name] = dashboard_info
                security_validation["summary"]["total"] += 1
                
                if dashboard_info["status"] == "deployed":
                    security_validation["summary"]["deployed"] += 1
                elif dashboard_info["status"] == "missing":
                    security_validation["summary"]["missing"] += 1
                    security_validation["valid"] = False
                elif dashboard_info["status"] == "error":
                    security_validation["summary"]["errors"] += 1
                    security_validation["valid"] = False
        
        print(f"Validation Status: {'✅ VALID' if security_validation['valid'] else '❌ INVALID'}")
        print(f"Security Dashboards: {security_validation['summary']['deployed']}/{security_validation['summary']['total']} deployed")
        
        if security_validation["summary"]["missing"] > 0:
            print(f"Missing: {security_validation['summary']['missing']}")
        
        if security_validation["summary"]["errors"] > 0:
            print(f"Errors: {security_validation['summary']['errors']}")
        
        return security_validation["valid"]
        
    except Exception as e:
        print(f"❌ Error validating security dashboards: {str(e)}")
        return False


def check_grafana_health():
    """Check Grafana health before deployment"""
    print("🏥 Checking Grafana health...")
    
    try:
        setup = GrafanaSetup()
        health = setup.get_health_status()
        
        if health["status"] == "healthy":
            print(f"✅ Grafana is healthy (version: {health.get('version', 'unknown')})")
            return True
        else:
            print(f"❌ Grafana is not healthy: {health.get('error', 'unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Grafana health: {str(e)}")
        return False


def main():
    """Main function"""
    setup_logging()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "deploy":
            if not check_grafana_health():
                print("⚠️  Grafana is not healthy. Please check Grafana service.")
                sys.exit(1)
            
            success = deploy_security_dashboards()
            sys.exit(0 if success else 1)
            
        elif command == "validate":
            success = validate_security_dashboards()
            sys.exit(0 if success else 1)
            
        elif command == "health":
            success = check_grafana_health()
            sys.exit(0 if success else 1)
            
        elif command == "urls":
            try:
                manager = DashboardManager()
                urls = manager.get_dashboard_urls()
                
                print("🔗 Security Dashboard URLs:")
                print("-" * 30)
                
                security_dashboards = ["scan-activity", "vulnerability-trends", "tool-performance"]
                for dashboard_name in security_dashboards:
                    if dashboard_name in urls and urls[dashboard_name]:
                        print(f"  {dashboard_name}: {urls[dashboard_name]}")
                    else:
                        print(f"  {dashboard_name}: Not available")
                        
                sys.exit(0)
                
            except Exception as e:
                print(f"❌ Error getting dashboard URLs: {str(e)}")
                sys.exit(1)
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: deploy, validate, health, urls")
            sys.exit(1)
    else:
        # Default: deploy and validate
        print("🚀 Starting security dashboard deployment and validation...")
        
        if not check_grafana_health():
            print("⚠️  Grafana is not healthy. Please check Grafana service.")
            sys.exit(1)
        
        # Deploy dashboards
        deploy_success = deploy_security_dashboards()
        
        if deploy_success:
            # Validate deployment
            validate_success = validate_security_dashboards()
            sys.exit(0 if validate_success else 1)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()