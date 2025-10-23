# HexStrike AI v6.0 - Windows PowerShell 測試腳本

param(
    [Parameter(Mandatory=$false)]
    [string]$Url = "http://localhost:8888"
)

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🧪 HexStrike AI Docker Deployment Test" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Target: $Url" -ForegroundColor Yellow
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# 測試計數器
$testsPassed = 0
$testsFailed = 0

# 測試函數
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Endpoint,
        [int]$ExpectedStatus = 200
    )

    Write-Host -NoNewline "Testing $Name... "

    try {
        $response = Invoke-WebRequest -Uri "$Url$Endpoint" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq $ExpectedStatus) {
            Write-Host "✅ PASS (HTTP $($response.StatusCode))" -ForegroundColor Green
            $script:testsPassed++
        } else {
            Write-Host "❌ FAIL (Expected HTTP $ExpectedStatus, got $($response.StatusCode))" -ForegroundColor Red
            $script:testsFailed++
        }
    } catch {
        Write-Host "❌ FAIL (Connection error)" -ForegroundColor Red
        $script:testsFailed++
    }
}

# 測試 JSON 回應
function Test-JsonResponse {
    param(
        [string]$Name,
        [string]$Endpoint,
        [string]$JsonKey
    )

    Write-Host -NoNewline "Testing $Name... "

    try {
        $response = Invoke-RestMethod -Uri "$Url$Endpoint" -UseBasicParsing -TimeoutSec 10
        
        # 檢查 JSON key 是否存在
        if ($response.PSObject.Properties.Name -contains $JsonKey) {
            Write-Host "✅ PASS (Found key: $JsonKey)" -ForegroundColor Green
            
            # 顯示回應
            Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
            
            $script:testsPassed++
        } else {
            Write-Host "❌ FAIL (Key '$JsonKey' not found)" -ForegroundColor Red
            Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
            $script:testsFailed++
        }
    } catch {
        Write-Host "❌ FAIL (Connection error: $($_.Exception.Message))" -ForegroundColor Red
        $script:testsFailed++
    }
}

Write-Host "Starting HexStrike AI API tests..." -ForegroundColor Cyan
Write-Host ""

# 執行測試
Test-JsonResponse "Health Check" "/health" "status"
Test-Endpoint "Telemetry Endpoint" "/api/telemetry"
Test-Endpoint "Cache Stats" "/api/cache/stats"
Test-Endpoint "Process List" "/api/processes/list"

# 測試根端點
Write-Host -NoNewline "Testing Root Endpoint... "
try {
    $null = Invoke-WebRequest -Uri "$Url/" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    Write-Host "✅ Server Responding" -ForegroundColor Green
    $testsPassed++
} catch {
    Write-Host "⚠️  No response (this may be normal)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "✅ Passed: $testsPassed" -ForegroundColor Green
Write-Host "❌ Failed: $testsFailed" -ForegroundColor Red
Write-Host "============================================================================" -ForegroundColor Cyan

if ($testsFailed -eq 0) {
    Write-Host "🎉 All tests passed! HexStrike AI is running correctly." -ForegroundColor Green
    exit 0
} else {
    Write-Host "⚠️  Some tests failed. Please check server logs." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Debugging tips:" -ForegroundColor Yellow
    Write-Host "  1. Check if container is running: docker ps"
    Write-Host "  2. View logs: docker logs hexstrike"
    Write-Host "  3. Verify port mapping: docker port hexstrike"
    exit 1
}

