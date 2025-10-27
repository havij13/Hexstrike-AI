#!/bin/bash

# HexStrike AI Alerting Setup Script
# This script sets up and tests the alerting and notification system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="${PROJECT_ROOT}/.env"
ALERTING_ENV_FILE="${PROJECT_ROOT}/env.alerting.example"

echo -e "${BLUE}🛡️  HexStrike AI Alerting Setup${NC}"
echo "=================================================="

# Function to print status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Prerequisites check passed ✓"
}

# Create environment file if it doesn't exist
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f "$ENV_FILE" ]; then
        print_warning "No .env file found. Creating from example..."
        cp "$ALERTING_ENV_FILE" "$ENV_FILE"
        print_warning "Please edit .env file with your notification channel configurations"
    else
        print_status "Environment file exists ✓"
    fi
    
    # Check if alerting is enabled
    if grep -q "ALERT_ENABLED=false" "$ENV_FILE" 2>/dev/null; then
        print_warning "Alerting is disabled in .env file. Enable it by setting ALERT_ENABLED=true"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p "${PROJECT_ROOT}/docker/alertmanager/templates"
    mkdir -p "${PROJECT_ROOT}/docker/grafana/provisioning/notifiers"
    mkdir -p "${PROJECT_ROOT}/docker/grafana/provisioning/alerting"
    mkdir -p "${PROJECT_ROOT}/logs"
    
    print_status "Directories created ✓"
}

# Start monitoring services
start_services() {
    print_status "Starting monitoring and alerting services..."
    
    cd "$PROJECT_ROOT"
    
    # Start Grafana stack with Alertmanager
    docker-compose -f docker-compose.grafana.yml up -d
    
    print_status "Waiting for services to start..."
    sleep 30
    
    # Check service health
    check_service_health
}

# Check service health
check_service_health() {
    print_status "Checking service health..."
    
    local services=("prometheus:9090" "grafana:3000" "alertmanager:9093")
    local all_healthy=true
    
    for service in "${services[@]}"; do
        local name="${service%:*}"
        local port="${service#*:}"
        
        if curl -s -f "http://localhost:${port}/api/health" >/dev/null 2>&1 || \
           curl -s -f "http://localhost:${port}/-/healthy" >/dev/null 2>&1 || \
           curl -s -f "http://localhost:${port}" >/dev/null 2>&1; then
            print_status "${name} is healthy ✓"
        else
            print_error "${name} is not responding"
            all_healthy=false
        fi
    done
    
    if [ "$all_healthy" = true ]; then
        print_status "All services are healthy ✓"
    else
        print_warning "Some services may not be fully ready yet"
    fi
}

# Test notification channels
test_notifications() {
    print_status "Testing notification channels..."
    
    local api_base="http://localhost:8888/api"
    
    # Check if HexStrike API is running
    if ! curl -s -f "${api_base}/health" >/dev/null 2>&1; then
        print_warning "HexStrike API is not running. Start it first to test notifications."
        return
    fi
    
    # Test available channels
    local channels=("email" "slack" "discord" "teams" "webhook")
    
    for channel in "${channels[@]}"; do
        print_status "Testing ${channel} notifications..."
        
        local response=$(curl -s -X POST "${api_base}/alerts/test/${channel}" \
            -H "Content-Type: application/json" \
            -d '{"severity": "info"}' 2>/dev/null)
        
        if echo "$response" | grep -q '"status": "success"'; then
            print_status "${channel} test passed ✓"
        else
            print_warning "${channel} test failed or not configured"
        fi
    done
}

# Create test alert
create_test_alert() {
    print_status "Creating test alert..."
    
    local api_base="http://localhost:8888/api"
    
    if ! curl -s -f "${api_base}/health" >/dev/null 2>&1; then
        print_warning "HexStrike API is not running. Cannot create test alert."
        return
    fi
    
    local test_alert='{
        "name": "AlertingSystemTest",
        "severity": "warning",
        "message": "Alerting system test alert",
        "description": "This is a test alert to verify the alerting system is working correctly.",
        "labels": {
            "service": "hexstrike-ai",
            "component": "alerting",
            "test": "true"
        },
        "annotations": {
            "summary": "Alerting system test",
            "runbook_url": "https://docs.hexstrike.ai/runbooks/test-alert"
        }
    }'
    
    local response=$(curl -s -X POST "${api_base}/alerts/fire" \
        -H "Content-Type: application/json" \
        -d "$test_alert" 2>/dev/null)
    
    if echo "$response" | grep -q '"status": "success"'; then
        print_status "Test alert created successfully ✓"
        print_status "Check your notification channels for the test alert"
        
        # Wait a bit then resolve the alert
        sleep 10
        
        local resolve_alert='{
            "name": "AlertingSystemTest",
            "labels": {
                "service": "hexstrike-ai",
                "component": "alerting",
                "test": "true"
            }
        }'
        
        curl -s -X POST "${api_base}/alerts/resolve" \
            -H "Content-Type: application/json" \
            -d "$resolve_alert" >/dev/null 2>&1
        
        print_status "Test alert resolved ✓"
    else
        print_error "Failed to create test alert"
    fi
}

# Display configuration summary
show_configuration() {
    print_status "Alerting System Configuration Summary"
    echo "=================================================="
    
    echo -e "${BLUE}Services:${NC}"
    echo "  • Prometheus: http://localhost:9090"
    echo "  • Grafana: http://localhost:3000"
    echo "  • Alertmanager: http://localhost:9093"
    echo ""
    
    echo -e "${BLUE}API Endpoints:${NC}"
    echo "  • Alert API: http://localhost:8888/api/alerts"
    echo "  • Fire Alert: POST /api/alerts/fire"
    echo "  • Test Notifications: POST /api/alerts/test/{channel}"
    echo "  • Active Alerts: GET /api/alerts/active"
    echo "  • Alert History: GET /api/alerts/history"
    echo ""
    
    echo -e "${BLUE}Configuration Files:${NC}"
    echo "  • Environment: .env"
    echo "  • Alertmanager: docker/alertmanager/alertmanager.yml"
    echo "  • Prometheus Rules: docker/prometheus/rules/hexstrike_alerts.yml"
    echo "  • Grafana Notifications: docker/grafana/provisioning/notifiers/"
    echo ""
    
    echo -e "${BLUE}Next Steps:${NC}"
    echo "  1. Configure notification channels in .env file"
    echo "  2. Test notification channels: curl -X POST http://localhost:8888/api/alerts/test/slack"
    echo "  3. View Grafana dashboards: http://localhost:3000"
    echo "  4. Monitor alerts in Alertmanager: http://localhost:9093"
    echo ""
}

# Cleanup function
cleanup() {
    print_status "Cleaning up alerting services..."
    
    cd "$PROJECT_ROOT"
    docker-compose -f docker-compose.grafana.yml down
    
    print_status "Cleanup completed ✓"
}

# Main execution
main() {
    case "${1:-setup}" in
        "setup")
            check_prerequisites
            setup_environment
            create_directories
            start_services
            show_configuration
            ;;
        "test")
            test_notifications
            create_test_alert
            ;;
        "start")
            start_services
            ;;
        "stop")
            cleanup
            ;;
        "status")
            check_service_health
            ;;
        "config")
            show_configuration
            ;;
        *)
            echo "Usage: $0 {setup|test|start|stop|status|config}"
            echo ""
            echo "Commands:"
            echo "  setup   - Full setup of alerting system"
            echo "  test    - Test notification channels"
            echo "  start   - Start alerting services"
            echo "  stop    - Stop alerting services"
            echo "  status  - Check service health"
            echo "  config  - Show configuration summary"
            exit 1
            ;;
    esac
}

# Handle script interruption
trap cleanup EXIT

# Run main function
main "$@"