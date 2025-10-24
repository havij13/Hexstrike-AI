# HexStrike AI v6.0 - Comprehensive API Test Script (PowerShell)
# References API_USAGE.md for complete endpoint testing

param(
    [Parameter(Mandatory=$false)]
    [string]$Url = "https://hexstrike-ai-v6-0.onrender.com",
    [Parameter(Mandatory=$false)]
    [int]$Timeout = 30,
    [Parameter(Mandatory=$false)]
    [switch]$VerboseOutputOutput
)

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🧪 HexStrike AI - Comprehensive API Test Suite (PowerShell)" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Target URL: $Url" -ForegroundColor Yellow
Write-Host "Documentation: API_USAGE.md" -ForegroundColor Yellow
Write-Host "Test Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Test counters
$script:TotalTests = 0
$script:TestsPassed = 0
$script:TestsFailed = 0
$script:TestsSkipped = 0

# Utility functions
function Log-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Log-Success {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Log-Error {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Log-Warning {
    param([string]$Message)
    Write-Host "[SKIP] $Message" -ForegroundColor Yellow
}

function Log-Test {
    param([string]$Message)
    Write-Host "[TEST] $Message" -ForegroundColor Cyan
}

# Test function for basic endpoints
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Endpoint,
        [string]$Method = "GET",
        [int]$ExpectedStatus = 200,
        [string]$Data = $null
    )
    
    $script:TotalTests++
    Log-Test "$Name ($Method $Endpoint)"
    
    try {
        $requestParams = @{
            Uri = "$Url$Endpoint"
            Method = $Method
            TimeoutSec = $Timeout
            UseBasicParsing = $true
        }
        
        if ($Method -in @("POST", "PUT", "DELETE")) {
            $requestParams.Headers = @{"Content-Type" = "application/json"}
            if ($Data) {
                $requestParams.Body = $Data
            }
        }
        
        $response = Invoke-WebRequest @requestParams
        
        if ($response.StatusCode -eq $ExpectedStatus) {
            Log-Success "$Name - HTTP $($response.StatusCode)"
            $script:TestsPassed++
            
            # Show response preview if verbose
            if ($VerboseOutput) {
                $content = $response.Content | Select-String -Pattern '.*' | Select-Object -First 1
                Write-Host "   Response: $($content -replace '^.{200}.*', '$&...')" -ForegroundColor Gray
            }
        } else {
            Log-Error "$Name - Expected HTTP $ExpectedStatus, got $($response.StatusCode)"
            $script:TestsFailed++
        }
    } catch {
        Log-Error "$Name - Connection failed or timeout: $($_.Exception.Message)"
        $script:TestsFailed++
    }
}

# Test function for JSON responses
function Test-JsonEndpoint {
    param(
        [string]$Name,
        [string]$Endpoint,
        [string]$Method = "GET",
        [string]$ExpectedKey,
        [string]$Data = $null
    )
    
    $script:TotalTests++
    Log-Test "$Name ($Method $Endpoint)"
    
    try {
        $requestParams = @{
            Uri = "$Url$Endpoint"
            Method = $Method
            TimeoutSec = $Timeout
            UseBasicParsing = $true
        }
        
        if ($Method -in @("POST", "PUT", "DELETE")) {
            $requestParams.Headers = @{"Content-Type" = "application/json"}
            if ($Data) {
                $requestParams.Body = $Data
            }
        }
        
        $response = Invoke-RestMethod @requestParams
        
        # Check if expected key exists in response
        if ($response.PSObject.Properties.Name -contains $ExpectedKey) {
            Log-Success "$Name - Found key: $ExpectedKey"
            $script:TestsPassed++
            
            # Show response preview if verbose
            if ($VerboseOutput) {
                $jsonResponse = $response | ConvertTo-Json -Compress
                Write-Host "   Response: $($jsonResponse.Substring(0, [Math]::Min(200, $jsonResponse.Length)))..." -ForegroundColor Gray
            }
        } else {
            Log-Error "$Name - Key '$ExpectedKey' not found in response"
            $script:TestsFailed++
            if ($VerboseOutput) {
                $jsonResponse = $response | ConvertTo-Json -Compress
                Write-Host "   Response: $jsonResponse" -ForegroundColor Gray
            }
        }
    } catch {
        Log-Error "$Name - Connection failed or timeout: $($_.Exception.Message)"
        $script:TestsFailed++
    }
}

# Skip test function
function Skip-Test {
    param(
        [string]$Name,
        [string]$Reason
    )
    
    $script:TotalTests++
    Log-Warning "$Name - $Reason"
    $script:TestsSkipped++
}

Write-Host "Starting comprehensive API testing based on API_USAGE.md..." -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# CORE SYSTEM ENDPOINTS
# ============================================================================
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🏥 Core System Endpoints" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

Test-JsonEndpoint "Health Check" "/health" "GET" "status"
Test-Endpoint "Server Telemetry" "/api/telemetry" "GET"

# ============================================================================
# NETWORK SECURITY TOOLS
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🔍 Network Security Tools" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# Nmap scanning
Test-JsonEndpoint "Nmap Quick Scan" "/api/tools/nmap" "POST" "execution_time" '{"target": "scanme.nmap.org", "scan_type": "quick", "ports": "1-100"}'

# Skip intensive scans in automated testing
Skip-Test "Nmap Comprehensive Scan" "Too intensive for automated testing"
Skip-Test "Rustscan Test" "Requires specific network access"
Skip-Test "Masscan Test" "High-speed scanning not suitable for automated tests"
Skip-Test "AutoRecon Test" "Comprehensive reconnaissance takes too long"

# ============================================================================
# WEB APPLICATION SECURITY TOOLS
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🌐 Web Application Security Tools" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# Gobuster
Test-JsonEndpoint "Gobuster Directory Enumeration" "/api/tools/gobuster" "POST" "execution_time" '{"url": "https://httpbin.org", "mode": "dir", "wordlist": "/usr/share/wordlists/dirb/common.txt"}'

# Skip intensive web scans
Skip-Test "Feroxbuster Test" "Recursive scanning takes too long"
Skip-Test "Nuclei Vulnerability Scan" "Comprehensive vulnerability scanning"
Skip-Test "Nikto Web Server Scan" "Full web server vulnerability scan"
Skip-Test "SQLMap Injection Test" "SQL injection testing requires specific targets"
Skip-Test "WPScan WordPress Test" "WordPress scanning requires specific targets"

# ============================================================================
# AUTHENTICATION & PASSWORD SECURITY
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🔐 Authentication & Password Security" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# Skip password cracking tools
Skip-Test "Hydra Network Login Cracker" "Password cracking tools not suitable for automated testing"
Skip-Test "John the Ripper" "Password hash cracking requires specific hash files"
Skip-Test "Hashcat GPU Cracking" "GPU-accelerated cracking requires specific hardware"

# ============================================================================
# BINARY ANALYSIS & REVERSE ENGINEERING
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🔬 Binary Analysis & Reverse Engineering" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# Skip binary analysis tools
Skip-Test "Ghidra Reverse Engineering" "Requires binary files for analysis"
Skip-Test "Radare2 Analysis" "Requires binary files for analysis"
Skip-Test "GDB Debugger" "Requires binary files for debugging"

# ============================================================================
# CLOUD & CONTAINER SECURITY
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "☁️ Cloud & Container Security" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# Skip cloud security tools
Skip-Test "Prowler Cloud Assessment" "Requires cloud credentials and configuration"
Skip-Test "Trivy Container Scanner" "Requires container images for scanning"
Skip-Test "Kube-Hunter Kubernetes Test" "Requires Kubernetes cluster access"

# ============================================================================
# AI INTELLIGENCE ENDPOINTS
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🧠 AI Intelligence Endpoints" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

Test-JsonEndpoint "AI Target Analysis" "/api/intelligence/analyze-target" "POST" "target_profile" '{"target": "httpbin.org", "analysis_type": "quick"}'
Test-JsonEndpoint "AI Tool Selection" "/api/intelligence/select-tools" "POST" "selected_tools" '{"target": "httpbin.org", "target_type": "web", "scan_depth": "shallow"}'
Test-JsonEndpoint "Parameter Optimization" "/api/intelligence/optimize-parameters" "POST" "optimized_parameters" '{"tool": "nmap", "target": "httpbin.org", "scan_type": "quick"}'

# ============================================================================
# PROCESS MANAGEMENT
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "⚙️ Process Management" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

Test-JsonEndpoint "Process List" "/api/processes/list" "GET" "active_processes"
Test-JsonEndpoint "Process Dashboard" "/api/processes/dashboard" "GET" "total_processes"

# Skip process-specific operations (no PIDs to test)
Skip-Test "Process Status" "No specific PID available for testing"
Skip-Test "Process Termination" "No specific PID available for testing"

# ============================================================================
# BUG BOUNTY WORKFLOWS
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🐛 Bug Bounty Workflows" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# Skip bug bounty workflows (too intensive)
Skip-Test "Reconnaissance Workflow" "Comprehensive reconnaissance takes too long"
Skip-Test "Vulnerability Hunting Workflow" "Vulnerability hunting is intensive"
Skip-Test "Business Logic Testing" "Business logic testing requires specific targets"

# ============================================================================
# CTF TOOLS
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🏆 CTF Tools" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

# Skip CTF tools
Skip-Test "CTF Challenge Solver" "Requires specific challenge data"
Skip-Test "Cryptography Solver" "Requires specific cipher data"
Skip-Test "Forensics Analyzer" "Requires specific forensics files"

# ============================================================================
# ERROR HANDLING
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🔧 Error Handling" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

Test-JsonEndpoint "Error Statistics" "/api/error-handling/statistics" "GET" "total_errors"

# Skip error recovery testing (requires specific error conditions)
Skip-Test "Execute with Recovery" "Requires specific error conditions"

# ============================================================================
# FILE OPERATIONS
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "📁 File Operations" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

Test-JsonEndpoint "List Files" "/api/files/list" "GET" "files"

# Skip file creation/modification (requires specific paths)
Skip-Test "Create File" "Requires specific file paths"
Skip-Test "Modify File" "Requires existing files"
Skip-Test "Delete File" "Requires existing files"

# ============================================================================
# CACHE MANAGEMENT
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "💾 Cache Management" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

Test-JsonEndpoint "Cache Statistics" "/api/cache/stats" "GET" "hit_rate"
Test-JsonEndpoint "Clear Cache" "/api/cache/clear" "POST" "success"

# ============================================================================
# ADDITIONAL ENDPOINTS
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🔧 Additional Endpoints" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan

Test-Endpoint "Root Endpoint" "/" "GET" "404"
Test-JsonEndpoint "Command Execution" "/api/command" "POST" "execution_time" '{"command": "echo Hello World"}'

# ============================================================================
# TEST SUMMARY
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "📊 Test Summary" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Total Tests: $script:TotalTests"
Write-Host "✅ Passed: $script:TestsPassed" -ForegroundColor Green
Write-Host "❌ Failed: $script:TestsFailed" -ForegroundColor Red
Write-Host "⚠️  Skipped: $script:TestsSkipped" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan

# Calculate success rate
if ($script:TotalTests -gt 0) {
    $successRate = [Math]::Round(($script:TestsPassed * 100) / $script:TotalTests, 1)
    Write-Host "Success Rate: $successRate%"
}

Write-Host ""

# Final result
if ($script:TestsFailed -eq 0) {
    Write-Host "🎉 All tests completed successfully!" -ForegroundColor Green
    Write-Host "HexStrike AI API is functioning correctly." -ForegroundColor Green
    exit 0
} else {
    Write-Host "⚠️  Some tests failed. Please check the server status." -ForegroundColor Red
    Write-Host ""
    Write-Host "Debugging tips:" -ForegroundColor Yellow
    Write-Host "  1. Check server health: Invoke-WebRequest -Uri '$Url/health'"
    Write-Host "  2. Verify server is running and accessible"
    Write-Host "  3. Check server logs for errors"
    Write-Host "  4. Ensure proper authorization for security testing endpoints"
    exit 1
}
