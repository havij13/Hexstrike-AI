# Deploy security-specific Grafana dashboards for HexStrike AI
# PowerShell script for Windows users

param(
    [Parameter(Position=0)]
    [ValidateSet("deploy", "validate", "health", "urls", "")]
    [string]$Command = ""
)

# Colors for output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Blue = "Blue"
$Cyan = "Cyan"

function Write-Header {
    param([string]$Title)
    Write-Host "🔒 $Title" -ForegroundColor $Cyan
    Write-Host ("=" * 50) -ForegroundColor $Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor $Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor $Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor $Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor $Blue
}

function Test-GrafanaHealth {
    Write-Info "Checking Grafana health..."
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -Method Get -TimeoutSec 10
        if ($response) {
            Write-Success "Grafana is healthy"
            return $true
        }
    }
    catch {
        Write-Error "Grafana health check failed: $($_.Exception.Message)"
        return $false
    }
    
    return $false
}

function Deploy-SecurityDashboards {
    Write-Header "HexStrike AI - Security Dashboard Deployment"
    
    if (-not (Test-GrafanaHealth)) {
        Write-Warning "Grafana is not healthy. Please check Grafana service."
        return $false
    }
    
    Write-Info "Deploying security dashboards..."
    
    try {
        # Run Python deployment script
        $result = python scripts/deploy-security-dashboards.py deploy
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Security dashboards deployed successfully!"
            return $true
        } else {
            Write-Error "Failed to deploy security dashboards"
            return $false
        }
    }
    catch {
        Write-Error "Error running deployment script: $($_.Exception.Message)"
        return $false
    }
}

function Test-SecurityDashboards {
    Write-Info "Validating security dashboard deployment..."
    
    try {
        $result = python scripts/deploy-security-dashboards.py validate
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Security dashboards validation passed!"
            return $true
        } else {
            Write-Error "Security dashboards validation failed"
            return $false
        }
    }
    catch {
        Write-Error "Error running validation script: $($_.Exception.Message)"
        return $false
    }
}

function Get-DashboardUrls {
    Write-Info "Getting security dashboard URLs..."
    
    try {
        python scripts/deploy-security-dashboards.py urls
        return $true
    }
    catch {
        Write-Error "Error getting dashboard URLs: $($_.Exception.Message)"
        return $false
    }
}

function Show-Help {
    Write-Host @"
🔒 HexStrike AI - Security Dashboard Management

Usage: .\deploy-security-dashboards.ps1 [command]

Commands:
  deploy    Deploy security dashboards to Grafana
  validate  Validate security dashboard deployment
  health    Check Grafana health status
  urls      Show security dashboard URLs
  (none)    Deploy and validate (default)

Examples:
  .\deploy-security-dashboards.ps1 deploy
  .\deploy-security-dashboards.ps1 validate
  .\deploy-security-dashboards.ps1 health
  .\deploy-security-dashboards.ps1 urls

Security Dashboards:
  - Scan Activity Dashboard
  - Vulnerability Trends Dashboard  
  - Tool Performance Dashboard

Prerequisites:
  - Grafana running on http://localhost:3000
  - Python 3.8+ with required dependencies
  - Prometheus data source configured in Grafana
"@ -ForegroundColor $Cyan
}

# Main execution
switch ($Command.ToLower()) {
    "deploy" {
        $success = Deploy-SecurityDashboards
        exit $(if ($success) { 0 } else { 1 })
    }
    
    "validate" {
        $success = Test-SecurityDashboards
        exit $(if ($success) { 0 } else { 1 })
    }
    
    "health" {
        $success = Test-GrafanaHealth
        exit $(if ($success) { 0 } else { 1 })
    }
    
    "urls" {
        $success = Get-DashboardUrls
        exit $(if ($success) { 0 } else { 1 })
    }
    
    "help" {
        Show-Help
        exit 0
    }
    
    "" {
        # Default: deploy and validate
        Write-Header "HexStrike AI - Security Dashboard Setup"
        
        $deploySuccess = Deploy-SecurityDashboards
        
        if ($deploySuccess) {
            $validateSuccess = Test-SecurityDashboards
            
            if ($validateSuccess) {
                Write-Host ""
                Get-DashboardUrls
                Write-Host ""
                Write-Success "Security dashboard setup completed successfully!"
            }
            
            exit $(if ($validateSuccess) { 0 } else { 1 })
        } else {
            exit 1
        }
    }
    
    default {
        Write-Error "Unknown command: $Command"
        Write-Info "Use 'help' to see available commands"
        exit 1
    }
}