#!/bin/bash

# HexStrike AI - Lightweight API Test Suite
# Runs minimal versions of all tools for quick validation
# Target: Complete in ~2 minutes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="${HEXSTRIKE_API_URL:-https://hexstrike-ai-v6-0.onrender.com}"

# Test counters
PASSED=0
FAILED=0
SKIPPED=0

test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    
    echo -e "${BLUE}[TEST]${NC} $name"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "${BASE_URL}${endpoint}" || echo "000")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" "${BASE_URL}${endpoint}" || echo "000")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" =~ ^2[0-9]{2}$ ]]; then
        echo -e "${GREEN}[PASS]${NC} $name - HTTP $http_code"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}[FAIL]${NC} $name - HTTP $http_code"
        ((FAILED++))
        return 1
    fi
}

# Health Check
test_endpoint "Health Check" "GET" "/health"

# Tool Count
test_endpoint "Tool Count" "GET" "/api/tools/count"

# Network Tools (Lightweight)
echo -e "\n${YELLOW}=== Network Security Tools (Lightweight) ===${NC}"

# Nmap - Quick scan with single port
test_endpoint "Nmap Quick (Single Port)" "POST" "/api/tools/nmap" \
'{"target":"scanme.nmap.org","scan_type":"quick","ports":"80"}'

# Rustscan - Single port
test_endpoint "Rustscan (Single Port)" "POST" "/api/tools/rustscan" \
'{"target":"scanme.nmap.org","ports":"80","timeout":100}'

# Masscan - Low rate, small port range
test_endpoint "Masscan (Low Rate)" "POST" "/api/tools/masscan" \
'{"target":"scanme.nmap.org","ports":"80-90","rate":100}'

# Web Tools (Lightweight)
echo -e "\n${YELLOW}=== Web Application Security Tools (Lightweight) ===${NC}"

# Gobuster - Quick scan
test_endpoint "Gobuster Quick" "POST" "/api/tools/gobuster" \
'{"url":"https://example.com","mode":"dir","wordlist":"common.txt"}'

# Feroxbuster - Shallow depth
test_endpoint "Feroxbuster (Depth 1)" "POST" "/api/tools/feroxbuster" \
'{"url":"https://example.com","depth":1,"threads":10,"wordlist":"common.txt"}'

# Nuclei - Single template
test_endpoint "Nuclei (Single Template)" "POST" "/api/tools/nuclei" \
'{"target":"https://example.com","template":"dns/dns-waf-detect.yaml","severity":"info"}'

# Nikto - Quick scan
test_endpoint "Nikto Quick" "POST" "/api/tools/nikto" \
'{"url":"https://example.com","options":"-Tuning 1,2,3,4,5,6,7"}'

# SQLMap - List check
test_endpoint "SQLMap Check" "POST" "/api/tools/sqlmap" \
'{"url":"https://example.com","action":"--batch --crawl=1"}'

# Authentication Tools (Lightweight)
echo -e "\n${YELLOW}=== Authentication & Password Security (Lightweight) ===${NC}"

# Hydra - List mode
test_endpoint "Hydra (List)" "POST" "/api/tools/hydra" \
'{"target":"localhost","service":"ssh","action":"--list"}'

# John - Single hash
test_endpoint "John (Single Hash)" "POST" "/api/tools/john" \
'{"hash":"\$2a\$10\$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy"}'

# Hashcat - Version check
test_endpoint "Hashcat (Version)" "POST" "/api/tools/hashcat" \
'{"action":"--version"}'

# Binary Analysis (Lightweight)
echo -e "\n${YELLOW}=== Binary Analysis & Reverse Engineering (Lightweight) ===${NC}"

# Ghidra - Version check
test_endpoint "Ghidra (Version)" "POST" "/api/tools/ghidra" \
'{"binary":"/bin/true","action":"analyzeHeadless -printScriptHelp"}'

# Radare2 - Basic info
test_endpoint "Radare2 (Info)" "POST" "/api/tools/radare2" \
'{"binary":"/bin/true","command":"ii"}'

# GDB - Version check
test_endpoint "GDB (Version)" "POST" "/api/tools/gdb" \
'{"binary":"/bin/true","command":"--version"}'

# Cloud Security (Lightweight)
echo -e "\n${YELLOW}=== Cloud & Container Security (Lightweight) ===${NC}"

# Prowler - List checks
test_endpoint "Prowler (List)" "POST" "/api/tools/prowler" \
'{"action":"--list-checks"}'

# Trivy - Version check
test_endpoint "Trivy (Version)" "POST" "/api/tools/trivy" \
'{"image":"alpine:latest","action":"--version"}'

# Kube-Hunter - List mode
test_endpoint "Kube-Hunter (List)" "POST" "/api/tools/kube-hunter" \
'{"action":"--list"}'

# Summary
echo -e "\n${BLUE}=== Test Summary ===${NC}"
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}✅ Passed: $PASSED${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All lightweight tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  Some tests failed. Please check the server status.${NC}"
    exit 1
fi
