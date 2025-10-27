#!/bin/bash

# HexStrike AI Grafana Infrastructure Setup Script
# This script sets up the complete Grafana monitoring infrastructure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
GRAFANA_VERSION="10.2.0"
PROMETHEUS_VERSION="2.40.0"
COMPOSE_FILE="docker-compose.grafana.yml"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    log_success "All dependencies are available"
}

create_directories() {
    log_info "Creating necessary directories..."
    
    # Create directories if they don't exist
    mkdir -p docker/grafana/provisioning/datasources
    mkdir -p docker/grafana/provisioning/dashboards/system
    mkdir -p docker/grafana/provisioning/dashboards/scans
    mkdir -p docker/grafana/provisioning/dashboards/tools
    mkdir -p docker/grafana/provisioning/dashboards/users
    mkdir -p docker/prometheus/rules
    mkdir -p logs/grafana
    mkdir -p logs/prometheus
    
    log_success "Directories created successfully"
}

setup_environment() {
    log_info "Setting up environment variables..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        log_info "Creating .env file..."
        cat > .env << EOF
# Grafana Configuration
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin123
GRAFANA_SECRET_KEY=SW2YcwTIb9zpOOhoPsMm
GRAFANA_DOMAIN=localhost
GRAFANA_ROOT_URL=http://localhost:3000

# Auth0 Integration (optional)
GRAFANA_AUTH0_ENABLED=false
GRAFANA_AUTH0_CLIENT_ID=
GRAFANA_AUTH0_CLIENT_SECRET=
GRAFANA_AUTH0_DOMAIN=

# Prometheus Configuration
PROMETHEUS_URL=http://prometheus:9090

# Database Configuration (SQLite by default)
GRAFANA_DB_TYPE=sqlite3
GRAFANA_DB_PATH=/var/lib/grafana/grafana.db
EOF
        log_success ".env file created with default values"
    else
        log_info ".env file already exists, skipping creation"
    fi
}

pull_images() {
    log_info "Pulling Docker images..."
    
    docker pull grafana/grafana:${GRAFANA_VERSION}
    docker pull prom/prometheus:${PROMETHEUS_VERSION}
    docker pull prom/node-exporter:v1.6.0
    docker pull gcr.io/cadvisor/cadvisor:v0.47.0
    
    log_success "Docker images pulled successfully"
}

start_services() {
    log_info "Starting Grafana infrastructure services..."
    
    # Stop any existing services
    docker-compose -f ${COMPOSE_FILE} down 2>/dev/null || true
    
    # Start services
    docker-compose -f ${COMPOSE_FILE} up -d
    
    log_success "Services started successfully"
}

wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for Prometheus
    log_info "Waiting for Prometheus..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -s http://localhost:9090/-/healthy &>/dev/null; then
            log_success "Prometheus is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        log_error "Prometheus failed to start within 60 seconds"
        exit 1
    fi
    
    # Wait for Grafana
    log_info "Waiting for Grafana..."
    timeout=120
    while [ $timeout -gt 0 ]; do
        if curl -s http://localhost:3000/api/health &>/dev/null; then
            log_success "Grafana is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        log_error "Grafana failed to start within 120 seconds"
        exit 1
    fi
}

setup_grafana() {
    log_info "Setting up Grafana configuration..."
    
    # Run the Python setup script
    if command -v python3 &> /dev/null; then
        python3 monitoring/grafana_setup.py
    elif command -v python &> /dev/null; then
        python monitoring/grafana_setup.py
    else
        log_warning "Python not found. Skipping automated Grafana setup."
        log_info "You can run 'python monitoring/grafana_setup.py' manually later."
    fi
}

show_status() {
    log_info "Checking service status..."
    
    echo ""
    echo "=== Service Status ==="
    docker-compose -f ${COMPOSE_FILE} ps
    
    echo ""
    echo "=== Service URLs ==="
    echo "Grafana:    http://localhost:3000 (admin/admin123)"
    echo "Prometheus: http://localhost:9090"
    echo "Node Exporter: http://localhost:9100"
    echo "cAdvisor:   http://localhost:8080"
    
    echo ""
    echo "=== Health Checks ==="
    
    # Check Grafana
    if curl -s http://localhost:3000/api/health &>/dev/null; then
        echo -e "Grafana:    ${GREEN}✓ Healthy${NC}"
    else
        echo -e "Grafana:    ${RED}✗ Unhealthy${NC}"
    fi
    
    # Check Prometheus
    if curl -s http://localhost:9090/-/healthy &>/dev/null; then
        echo -e "Prometheus: ${GREEN}✓ Healthy${NC}"
    else
        echo -e "Prometheus: ${RED}✗ Unhealthy${NC}"
    fi
    
    # Check Node Exporter
    if curl -s http://localhost:9100/metrics &>/dev/null; then
        echo -e "Node Exporter: ${GREEN}✓ Healthy${NC}"
    else
        echo -e "Node Exporter: ${RED}✗ Unhealthy${NC}"
    fi
    
    # Check cAdvisor
    if curl -s http://localhost:8080/metrics &>/dev/null; then
        echo -e "cAdvisor:   ${GREEN}✓ Healthy${NC}"
    else
        echo -e "cAdvisor:   ${RED}✗ Unhealthy${NC}"
    fi
}

cleanup() {
    log_info "Cleaning up..."
    docker-compose -f ${COMPOSE_FILE} down
    docker system prune -f
    log_success "Cleanup completed"
}

show_help() {
    echo "HexStrike AI Grafana Infrastructure Setup"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     Set up and start the complete Grafana infrastructure"
    echo "  start     Start the services"
    echo "  stop      Stop the services"
    echo "  restart   Restart the services"
    echo "  status    Show service status"
    echo "  logs      Show service logs"
    echo "  cleanup   Stop services and clean up"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup    # Complete setup and start"
    echo "  $0 status   # Check service status"
    echo "  $0 logs grafana  # Show Grafana logs"
}

# Main script logic
case "${1:-setup}" in
    "setup")
        log_info "Starting HexStrike AI Grafana infrastructure setup..."
        check_dependencies
        create_directories
        setup_environment
        pull_images
        start_services
        wait_for_services
        setup_grafana
        show_status
        log_success "Grafana infrastructure setup completed successfully!"
        ;;
    
    "start")
        log_info "Starting services..."
        docker-compose -f ${COMPOSE_FILE} up -d
        wait_for_services
        show_status
        ;;
    
    "stop")
        log_info "Stopping services..."
        docker-compose -f ${COMPOSE_FILE} down
        log_success "Services stopped"
        ;;
    
    "restart")
        log_info "Restarting services..."
        docker-compose -f ${COMPOSE_FILE} restart
        wait_for_services
        show_status
        ;;
    
    "status")
        show_status
        ;;
    
    "logs")
        if [ -n "$2" ]; then
            docker-compose -f ${COMPOSE_FILE} logs -f "$2"
        else
            docker-compose -f ${COMPOSE_FILE} logs -f
        fi
        ;;
    
    "cleanup")
        cleanup
        ;;
    
    "help"|"-h"|"--help")
        show_help
        ;;
    
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac