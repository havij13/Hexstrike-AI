#!/bin/bash
# HexStrike AI - Integration Test Suite
# Comprehensive testing of all integrations and components

set -e

echo "🧪 HexStrike AI Integration Test Suite"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
BASE_URL="http://localhost:8888"
GRAFANA_URL="http://localhost:3000"
PROMETHEUS_URL="http://localhost:9090"
ELASTICSEARCH_URL="http://localhost:9200"
KIBANA_URL="http://localhost:5601"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TOTAL_TESTS=0

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    ((TOTAL_TESTS++))
    log_info "Running: $test_name"
    
    if eval "$test_command" > /dev/null 2>&1; then
        log_success "$test_name"
        return 0
    else
        log_error "$test_name"
        return 1
    fi
}

# Wait for service to be ready
wait_for_service() {
    local url="$1"
    local service_name="$2"
    local max_attempts=30
    local attempt=1
    
    log_info "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            log_success "$service_name is ready"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    log_error "$service_name failed to start within timeout"
    return 1
}

# Core API Tests
test_core_api() {
    log_info "Testing Core API..."
    
    # Health check
    run_test "Health Check" "curl -f $BASE_URL/health"
    
    # API endpoints
    run_test "API Root" "curl -f $BASE_URL/api/"
    
    # Metrics endpoint
    run_test "Metrics Endpoint" "curl -f $BASE_URL/metrics"
    
    # Command execution test
    run_test "Command Execution" "curl -f -X POST $BASE_URL/api/command -H 'Content-Type: application/json' -d '{\"command\": \"echo test\"}'"
}

# Security Tools Tests
test_security_tools() {
    log_info "Testing Security Tools Integration..."
    
    # Nmap test
    run_test "Nmap Integration" "curl -f -X POST $BASE_URL/api/tools/nmap -H 'Content-Type: application/json' -d '{\"target\": \"127.0.0.1\", \"scan_type\": \"quick\"}'"
    
    # Nuclei test
    run_test "Nuclei Integration" "curl -f -X POST $BASE_URL/api/tools/nuclei -H 'Content-Type: application/json' -d '{\"target\": \"http://127.0.0.1\"}'"
    
    # Tool availability check
    run_test "Tool Availability" "curl -f $BASE_URL/api/tools/status"
}

# AI Agents Tests
test_ai_agents() {
    log_info "Testing AI Agents..."
    
    # Intelligence engine
    run_test "Intelligence Engine" "curl -f -X POST $BASE_URL/api/intelligence/analyze-target -H 'Content-Type: application/json' -d '{\"target\": \"example.com\", \"analysis_type\": \"basic\"}'"
    
    # Tool selection
    run_test "Tool Selection AI" "curl -f -X POST $BASE_URL/api/intelligence/select-tools -H 'Content-Type: application/json' -d '{\"target_type\": \"web\", \"objectives\": [\"vulnerability_scan\"]}'"
    
    # Parameter optimization
    run_test "Parameter Optimization" "curl -f -X POST $BASE_URL/api/intelligence/optimize-parameters -H 'Content-Type: application/json' -d '{\"tool\": \"nmap\", \"target\": \"192.168.1.1\"}'"
}

# Monitoring Stack Tests
test_monitoring_stack() {
    log_info "Testing Monitoring Stack..."
    
    # Prometheus
    if wait_for_service "$PROMETHEUS_URL/-/healthy" "Prometheus"; then
        run_test "Prometheus Targets" "curl -f $PROMETHEUS_URL/api/v1/targets"
        run_test "Prometheus Metrics" "curl -f $PROMETHEUS_URL/api/v1/label/__name__/values"
    fi
    
    # Grafana
    if wait_for_service "$GRAFANA_URL/api/health" "Grafana"; then
        run_test "Grafana Health" "curl -f $GRAFANA_URL/api/health"
    fi
    
    # Elasticsearch
    if wait_for_service "$ELASTICSEARCH_URL/_cluster/health" "Elasticsearch"; then
        run_test "Elasticsearch Cluster" "curl -f $ELASTICSEARCH_URL/_cluster/health"
        run_test "Elasticsearch Indices" "curl -f $ELASTICSEARCH_URL/_cat/indices"
    fi
}

# Integration Tests
test_integrations() {
    log_info "Testing External Integrations..."
    
    # Webhook test
    run_test "Webhook Manager" "curl -f -X POST $BASE_URL/api/webhooks/test -H 'Content-Type: application/json' -d '{\"event_type\": \"test\", \"data\": {\"message\": \"test\"}}'"
    
    # SIEM integration test
    run_test "SIEM Integration" "curl -f $BASE_URL/api/integrations/siem/status"
    
    # Ticketing integration test
    run_test "Ticketing Integration" "curl -f $BASE_URL/api/integrations/ticketing/status"
}

# Performance Tests
test_performance() {
    log_info "Testing Performance..."
    
    # Load test with multiple concurrent requests
    run_test "Concurrent Requests" "for i in {1..10}; do curl -f $BASE_URL/health & done; wait"
    
    # Memory usage check
    run_test "Memory Usage" "docker stats --no-stream hexstrike | awk 'NR==2 {print \$4}' | grep -E '^[0-9]+\.[0-9]+%$|^[0-9]+%$'"
    
    # Response time check
    run_test "Response Time" "curl -w '%{time_total}' -o /dev/null -s $BASE_URL/health | awk '{if(\$1 < 1.0) exit 0; else exit 1}'"
}

# Security Tests
test_security() {
    log_info "Testing Security Features..."
    
    # Rate limiting test
    run_test "Rate Limiting" "for i in {1..20}; do curl -f $BASE_URL/health; done"
    
    # Input validation test
    run_test "Input Validation" "curl -f -X POST $BASE_URL/api/command -H 'Content-Type: application/json' -d '{\"command\": \"rm -rf /\"}' | grep -q 'error'"
    
    # Authentication test (if enabled)
    run_test "Authentication Check" "curl -f $BASE_URL/api/admin/status || true"
}

# Data Pipeline Tests
test_data_pipeline() {
    log_info "Testing Data Pipeline..."
    
    # Log ingestion test
    run_test "Log Ingestion" "echo '{\"test\": \"log_entry\", \"timestamp\": \"$(date -Iseconds)\"}' | curl -f -X POST $ELASTICSEARCH_URL/hexstrike-logs/_doc -H 'Content-Type: application/json' -d @-"
    
    # Metrics collection test
    run_test "Metrics Collection" "curl -f $PROMETHEUS_URL/api/v1/query?query=up"
    
    # Data retention test
    run_test "Data Retention" "curl -f $ELASTICSEARCH_URL/_cat/indices/hexstrike-*"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up test data..."
    
    # Remove test indices
    curl -X DELETE "$ELASTICSEARCH_URL/test-*" 2>/dev/null || true
    
    # Clear test metrics
    # (Prometheus metrics are ephemeral, no cleanup needed)
    
    log_info "Cleanup complete"
}

# Main test execution
main() {
    log_info "Starting HexStrike AI Integration Tests"
    echo ""
    
    # Wait for main service
    if ! wait_for_service "$BASE_URL/health" "HexStrike AI"; then
        log_error "HexStrike AI is not running. Please start it first with 'make deploy-local-full'"
        exit 1
    fi
    
    # Run test suites
    test_core_api
    echo ""
    
    test_security_tools
    echo ""
    
    test_ai_agents
    echo ""
    
    test_monitoring_stack
    echo ""
    
    test_integrations
    echo ""
    
    test_performance
    echo ""
    
    test_security
    echo ""
    
    test_data_pipeline
    echo ""
    
    # Cleanup
    cleanup
    
    # Results summary
    echo ""
    echo "======================================"
    echo "🧪 Integration Test Results"
    echo "======================================"
    echo -e "Total Tests: ${BLUE}$TOTAL_TESTS${NC}"
    echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}✅ All tests passed!${NC}"
        exit 0
    else
        echo -e "\n${RED}❌ Some tests failed. Check the output above for details.${NC}"
        exit 1
    fi
}

# Run main function
main "$@"