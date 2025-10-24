#!/bin/bash
# HexStrike AI v6.0 - Comprehensive API Test Script
# References API_USAGE.md for complete endpoint testing

set -e

# Configuration
HEXSTRIKE_URL="${HEXSTRIKE_URL:-https://hexstrike-ai.onrender.com}"
TEST_TIMEOUT="${TEST_TIMEOUT:-30}"
VERBOSE="${VERBOSE:-false}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
CYAN='\033[0;96m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

echo "============================================================================"
echo "🧪 HexStrike AI - Comprehensive API Test Suite"
echo "============================================================================"
echo "Target URL: $HEXSTRIKE_URL"
echo "Documentation: API_USAGE.md"
echo "Test Time: $(date)"
echo "============================================================================"
echo ""

# Utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[SKIP]${NC} $1"
}

log_test() {
    echo -e "${CYAN}[TEST]${NC} $1"
}

# Test function for basic endpoints
test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local method="${3:-GET}"
    local expected_status="${4:-200}"
    local data="$5"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    log_test "$name ($method $endpoint)"
    
    local curl_cmd="curl -s -w \"%{http_code}\" -o /tmp/response.json --max-time $TEST_TIMEOUT"
    
    if [ "$method" = "POST" ] || [ "$method" = "PUT" ] || [ "$method" = "DELETE" ]; then
        curl_cmd="$curl_cmd -X $method -H \"Content-Type: application/json\""
        if [ -n "$data" ]; then
            curl_cmd="$curl_cmd -d '$data'"
        fi
    fi
    
    curl_cmd="$curl_cmd \"$HEXSTRIKE_URL$endpoint\""
    
    if status_code=$(eval "$curl_cmd" 2>/dev/null); then
        if [ "$status_code" = "$expected_status" ]; then
            log_success "$name - HTTP $status_code"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            
            # Show response preview if verbose
            if [ "$VERBOSE" = "true" ] && [ -f /tmp/response.json ]; then
                echo "   Response: $(head -c 200 /tmp/response.json)..."
            fi
        else
            log_error "$name - Expected HTTP $expected_status, got $status_code"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        log_error "$name - Connection failed or timeout"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    
    # Cleanup
    rm -f /tmp/response.json
}

# Test function for JSON responses
test_json_endpoint() {
    local name="$1"
    local endpoint="$2"
    local method="${3:-GET}"
    local expected_key="$4"
    local data="$5"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    log_test "$name ($method $endpoint)"
    
    local curl_cmd="curl -s --max-time $TEST_TIMEOUT"
    
    if [ "$method" = "POST" ] || [ "$method" = "PUT" ] || [ "$method" = "DELETE" ]; then
        curl_cmd="$curl_cmd -X $method -H \"Content-Type: application/json\""
        if [ -n "$data" ]; then
            curl_cmd="$curl_cmd -d '$data'"
        fi
    fi
    
    curl_cmd="$curl_cmd \"$HEXSTRIKE_URL$endpoint\""
    
    if response=$(eval "$curl_cmd" 2>/dev/null); then
        if echo "$response" | grep -q "\"$expected_key\""; then
            log_success "$name - Found key: $expected_key"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            
            # Show response preview if verbose
            if [ "$VERBOSE" = "true" ]; then
                echo "   Response: $(echo "$response" | head -c 200)..."
            fi
        else
            log_error "$name - Key '$expected_key' not found in response"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            if [ "$VERBOSE" = "true" ]; then
                echo "   Response: $response"
            fi
        fi
    else
        log_error "$name - Connection failed or timeout"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Skip test function
skip_test() {
    local name="$1"
    local reason="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    log_warning "$name - $reason"
    TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
}

echo "Starting comprehensive API testing based on API_USAGE.md..."
echo ""

# ============================================================================
# CORE SYSTEM ENDPOINTS
# ============================================================================
echo "============================================================================"
echo "🏥 Core System Endpoints"
echo "============================================================================"

test_json_endpoint "Health Check" "/health" "GET" "status"
test_endpoint "Server Telemetry" "/api/telemetry" "GET"

# ============================================================================
# NETWORK SECURITY TOOLS
# ============================================================================
echo ""
echo "============================================================================"
echo "🔍 Network Security Tools"
echo "============================================================================"

# Nmap scanning
test_json_endpoint "Nmap Quick Scan" "/api/tools/nmap" "POST" "execution_time" '{"target": "scanme.nmap.org", "scan_type": "quick", "ports": "1-100"}'

# Skip intensive scans in automated testing
skip_test "Nmap Comprehensive Scan" "Too intensive for automated testing"
skip_test "Rustscan Test" "Requires specific network access"
skip_test "Masscan Test" "High-speed scanning not suitable for automated tests"
skip_test "AutoRecon Test" "Comprehensive reconnaissance takes too long"

# ============================================================================
# WEB APPLICATION SECURITY TOOLS
# ============================================================================
echo ""
echo "============================================================================"
echo "🌐 Web Application Security Tools"
echo "============================================================================"

# Gobuster
test_json_endpoint "Gobuster Directory Enumeration" "/api/tools/gobuster" "POST" "execution_time" '{"url": "https://httpbin.org", "mode": "dir", "wordlist": "/usr/share/wordlists/dirb/common.txt"}'

# Skip intensive web scans
skip_test "Feroxbuster Test" "Recursive scanning takes too long"
skip_test "Nuclei Vulnerability Scan" "Comprehensive vulnerability scanning"
skip_test "Nikto Web Server Scan" "Full web server vulnerability scan"
skip_test "SQLMap Injection Test" "SQL injection testing requires specific targets"
skip_test "WPScan WordPress Test" "WordPress scanning requires specific targets"

# ============================================================================
# AUTHENTICATION & PASSWORD SECURITY
# ============================================================================
echo ""
echo "============================================================================"
echo "🔐 Authentication & Password Security"
echo "============================================================================"

# Skip password cracking tools
skip_test "Hydra Network Login Cracker" "Password cracking tools not suitable for automated testing"
skip_test "John the Ripper" "Password hash cracking requires specific hash files"
skip_test "Hashcat GPU Cracking" "GPU-accelerated cracking requires specific hardware"

# ============================================================================
# BINARY ANALYSIS & REVERSE ENGINEERING
# ============================================================================
echo ""
echo "============================================================================"
echo "🔬 Binary Analysis & Reverse Engineering"
echo "============================================================================"

# Skip binary analysis tools
skip_test "Ghidra Reverse Engineering" "Requires binary files for analysis"
skip_test "Radare2 Analysis" "Requires binary files for analysis"
skip_test "GDB Debugger" "Requires binary files for debugging"

# ============================================================================
# CLOUD & CONTAINER SECURITY
# ============================================================================
echo ""
echo "============================================================================"
echo "☁️ Cloud & Container Security"
echo "============================================================================"

# Skip cloud security tools
skip_test "Prowler Cloud Assessment" "Requires cloud credentials and configuration"
skip_test "Trivy Container Scanner" "Requires container images for scanning"
skip_test "Kube-Hunter Kubernetes Test" "Requires Kubernetes cluster access"

# ============================================================================
# AI INTELLIGENCE ENDPOINTS
# ============================================================================
echo ""
echo "============================================================================"
echo "🧠 AI Intelligence Endpoints"
echo "============================================================================"

test_json_endpoint "AI Target Analysis" "/api/intelligence/analyze-target" "POST" "target_profile" '{"target": "httpbin.org", "analysis_type": "quick"}'
test_json_endpoint "AI Tool Selection" "/api/intelligence/select-tools" "POST" "selected_tools" '{"target": "httpbin.org", "target_type": "web", "scan_depth": "shallow"}'
test_json_endpoint "Parameter Optimization" "/api/intelligence/optimize-parameters" "POST" "optimized_parameters" '{"tool": "nmap", "target": "httpbin.org", "scan_type": "quick"}'

# ============================================================================
# PROCESS MANAGEMENT
# ============================================================================
echo ""
echo "============================================================================"
echo "⚙️ Process Management"
echo "============================================================================"

test_json_endpoint "Process List" "/api/processes/list" "GET" "active_processes"
test_json_endpoint "Process Dashboard" "/api/processes/dashboard" "GET" "total_processes"

# Skip process-specific operations (no PIDs to test)
skip_test "Process Status" "No specific PID available for testing"
skip_test "Process Termination" "No specific PID available for testing"

# ============================================================================
# BUG BOUNTY WORKFLOWS
# ============================================================================
echo ""
echo "============================================================================"
echo "🐛 Bug Bounty Workflows"
echo "============================================================================"

# Skip bug bounty workflows (too intensive)
skip_test "Reconnaissance Workflow" "Comprehensive reconnaissance takes too long"
skip_test "Vulnerability Hunting Workflow" "Vulnerability hunting is intensive"
skip_test "Business Logic Testing" "Business logic testing requires specific targets"

# ============================================================================
# CTF TOOLS
# ============================================================================
echo ""
echo "============================================================================"
echo "🏆 CTF Tools"
echo "============================================================================"

# Skip CTF tools
skip_test "CTF Challenge Solver" "Requires specific challenge data"
skip_test "Cryptography Solver" "Requires specific cipher data"
skip_test "Forensics Analyzer" "Requires specific forensics files"

# ============================================================================
# ERROR HANDLING
# ============================================================================
echo ""
echo "============================================================================"
echo "🔧 Error Handling"
echo "============================================================================"

test_json_endpoint "Error Statistics" "/api/error-handling/statistics" "GET" "statistics"

# Skip error recovery testing (requires specific error conditions)
skip_test "Execute with Recovery" "Requires specific error conditions"

# ============================================================================
# FILE OPERATIONS
# ============================================================================
echo ""
echo "============================================================================"
echo "📁 File Operations"
echo "============================================================================"

test_json_endpoint "List Files" "/api/files/list" "GET" "files"

# Skip file creation/modification (requires specific paths)
skip_test "Create File" "Requires specific file paths"
skip_test "Modify File" "Requires existing files"
skip_test "Delete File" "Requires existing files"

# ============================================================================
# CACHE MANAGEMENT
# ============================================================================
echo ""
echo "============================================================================"
echo "💾 Cache Management"
echo "============================================================================"

test_json_endpoint "Cache Statistics" "/api/cache/stats" "GET" "hit_rate"
test_json_endpoint "Clear Cache" "/api/cache/clear" "POST" "success"

# ============================================================================
# ADDITIONAL ENDPOINTS
# ============================================================================
echo ""
echo "============================================================================"
echo "🔧 Additional Endpoints"
echo "============================================================================"

test_endpoint "Root Endpoint" "/" "GET" "200"
test_json_endpoint "Command Execution" "/api/command" "POST" "execution_time" '{"command": "echo Hello World"}'

# ============================================================================
# TEST SUMMARY
# ============================================================================
echo ""
echo "============================================================================"
echo "📊 Test Summary"
echo "============================================================================"
echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}✅ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Failed: $TESTS_FAILED${NC}"
echo -e "${YELLOW}⚠️  Skipped: $TESTS_SKIPPED${NC}"
echo "============================================================================"

# Calculate success rate
if [ $TOTAL_TESTS -gt 0 ]; then
    success_rate=$(( (TESTS_PASSED * 100) / TOTAL_TESTS ))
    echo "Success Rate: $success_rate%"
fi

echo ""

# Final result
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests completed successfully!${NC}"
    echo -e "${GREEN}HexStrike AI API is functioning correctly.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please check the server status.${NC}"
    echo ""
    echo "Debugging tips:"
    echo "  1. Check server health: curl $HEXSTRIKE_URL/health"
    echo "  2. Verify server is running and accessible"
    echo "  3. Check server logs for errors"
    echo "  4. Ensure proper authorization for security testing endpoints"
    exit 1
fi
