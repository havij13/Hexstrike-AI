#!/usr/bin/env python3
"""
Dashboard deployment script for HexStrike AI system monitoring
"""
import sys
import os
import argparse
import logging

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitoring.dashboard_manager import DashboardManager
from monitoring.health_checks import HealthChecker


def setup_logging(verbose: bool = False):
    """Set up logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def check_grafana_health():
    """Check if Grafana is healthy before deploying dashboards"""
    print("🔍 Checking Grafana health...")
    
    health_checker = HealthChecker()
    grafana_health = health_checker.check_grafana_health()
    
    if grafana_health.status.value == "healthy":
        print(f"✅ Grafana is healthy (response time: {grafana_health.response_time:.3f}s)")
        return True
    else:
        print(f"❌ Grafana is not healthy: {grafana_health.message}")
        return False


def deploy_dashboards(force: bool = False):
    """Deploy system monitoring dashboards"""
    print("📊 Deploying system monitoring dashboards...")
    
    manager = DashboardManager()
    
    # Deploy all dashboards
    results = manager.deploy_all_dashboards()
    
    # Show results
    print("\n📋 Deployment Results:")
    for dashboard_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {dashboard_name}: {status}")
    
    # Summary
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    if successful == total:
        print(f"\n🎉 All {total} dashboards deployed successfully!")
        return True
    else:
        print(f"\n⚠️  Only {successful}/{total} dashboards deployed successfully")
        return successful > 0


def validate_dashboards():
    """Validate dashboard deployment"""
    print("🔍 Validating dashboard deployment...")
    
    manager = DashboardManager()
    validation = manager.validate_dashboards()
    
    print(f"\n📊 Validation Results:")
    print(f"Status: {'✅ VALID' if validation['valid'] else '❌ INVALID'}")
    print(f"Deployed: {validation['summary']['deployed']}/{validation['summary']['total']}")
    
    if validation["summary"]["missing"] > 0:
        print(f"Missing: {validation['summary']['missing']}")
    
    if validation["summary"]["errors"] > 0:
        print(f"Errors: {validation['summary']['errors']}")
    
    # Show individual dashboard status
    print("\n📋 Individual Dashboard Status:")
    for dashboard_name, info in validation["dashboards"].items():
        status_icon = {
            "deployed": "✅",
            "missing": "❌",
            "error": "⚠️"
        }.get(info["status"], "❓")
        
        print(f"  {status_icon} {dashboard_name}: {info['status']}")
        
        if info["status"] == "deployed":
            print(f"    URL: {info.get('url', 'N/A')}")
        elif info["status"] == "error":
            print(f"    Error: {info.get('error', 'Unknown error')}")
    
    return validation["valid"]


def show_dashboard_urls():
    """Show URLs for all dashboards"""
    print("🔗 Dashboard URLs:")
    
    manager = DashboardManager()
    urls = manager.get_dashboard_urls()
    
    for dashboard_name, url in urls.items():
        if url:
            print(f"  📊 {dashboard_name}: {url}")
        else:
            print(f"  ❌ {dashboard_name}: Not available")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Deploy and manage HexStrike AI system monitoring dashboards"
    )
    
    parser.add_argument(
        "action",
        choices=["deploy", "validate", "urls", "health"],
        help="Action to perform"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force deployment even if dashboards already exist"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    print("🚀 HexStrike AI Dashboard Manager")
    print("=" * 50)
    
    try:
        if args.action == "health":
            success = check_grafana_health()
            sys.exit(0 if success else 1)
        
        elif args.action == "deploy":
            # Check Grafana health first
            if not check_grafana_health():
                print("\n❌ Cannot deploy dashboards - Grafana is not healthy")
                sys.exit(1)
            
            # Deploy dashboards
            success = deploy_dashboards(args.force)
            
            if success:
                print("\n🔗 Dashboard URLs:")
                show_dashboard_urls()
            
            sys.exit(0 if success else 1)
        
        elif args.action == "validate":
            success = validate_dashboards()
            sys.exit(0 if success else 1)
        
        elif args.action == "urls":
            show_dashboard_urls()
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()