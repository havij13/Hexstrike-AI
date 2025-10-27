# HexStrike AI Alerting Setup Script (PowerShell)
# This script sets up and tests the alerting and notification system

param(
    [Parameter(Position=0)]
    [ValidateSet("setup", "test", "start", "stop", "status", "config")]
    [string]$Action = "setup"
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$EnvFile = Join-Path $ProjectRoot ".env"
$AlertingEnvFile = Join-Path $ProjectRoot "env.alerting.example"

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor $Colors.Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Colors.Red
}

function Write-Header {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $Colors.Blue
}

function Test-CommandExists {
    param([string]$Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

function Test-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    if (-not (Test-CommandExists "docker")) {
        Write-Error "Docker is not installed. Please install Docker Desktop first."
        exit 1
    }
    
    if (-not (Test-CommandExists "docker-compose")) {
        Write-Error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    }
    
    Write-Status "Prerequisites check passed ✓"
}

function Setup-Environment {
    Write-Status "Setting up environment configuration..."
    
    if (-not (Test-Path $EnvFile)) {
        Write-Warning "No .env file found. Creating from example..."
        Copy-Item $AlertingEnvFile $EnvFile
        Write-Warning "Please edit .env file with your notification channel configurations"
    } else {
        Write-Status "Environment file exists ✓"
    }
    
    # Check if alerting is enabled
    if (Test-Path $EnvFile) {
        $envContent = Get-Content $EnvFile -Raw
        if ($envContent -match "ALERT_ENABLED=false") {
            Write-Warning "Alerting is disabled in .env file. Enable it by setting ALERT_ENABLED=true"
        }
    }
}

function New-Directories {
    Write-Status "Creating necessary directories..."
    
    $directories = @(
        "docker/alertmanager/templates",
        "docker/grafana/provisioning/notifiers",
        "docker/grafana/provisioning/alerting",
        "logs"
    )
    
    foreach ($dir in $directories) {
        $fullPath = Join-Path $ProjectRoot $dir
        if (-not (Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
    }
    
    Write-Status "Directories created ✓"
}

function Start-Services {
    Write-Status "Starting monitoring and alerting services..."
    
    Set-Location $ProjectRoot
    
    # Start Grafana stack with Alertmanager
    & docker-compose -f docker-compose.grafana.yml up -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to start services"
        exit 1
    }
    
    Write-Status "Waiting for services to start..."
    Start-Sleep -Seconds 30
    
    # Check service health
    Test-ServiceHealth
}

function Test-ServiceHealth {
    Write-Status "Checking service health..."
    
    $services = @(
        @{Name="prometheus"; Port=9090},
        @{Name="grafana"; Port=3000},
        @{Name="alertmanager"; Port=9093}
    )
    
    $allHealthy = $true
    
    foreach ($service in $services) {
        $urls = @(
            "http://localhost:$($service.Port)/api/health",
            "http://localhost:$($service.Port)/-/healthy",
            "http://localhost:$($service.Port)"
        )
        
        $healthy = $false
        foreach ($url in $urls) {
            try {
                $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    $healthy = $true
                    break
                }
            } catch {
                # Continue to next URL
            }
        }
        
        if ($healthy) {
            Write-Status "$($service.Name) is healthy ✓"
        } else {
            Write-Error "$($service.Name) is not responding"
            $allHealthy = $false
        }
    }
    
    if ($allHealthy) {
        Write-Status "All services are healthy ✓"
    } else {
        Write-Warning "Some services may not be fully ready yet"
    }
}

function Test-Notifications {
    Write-Status "Testing notification channels..."
    
    $apiBase = "http://localhost:8888/api"
    
    # Check if HexStrike API is running
    try {
        $response = Invoke-WebRequest -Uri "$apiBase/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -ne 200) {
            throw "API not healthy"
        }
    } catch {
        Write-Warning "HexStrike API is not running. Start it first to test notifications."
        return
    }
    
    # Test available channels
    $channels = @("email", "slack", "discord", "teams", "webhook")
    
    foreach ($channel in $channels) {
        Write-Status "Testing $channel notifications..."
        
        $body = @{
            severity = "info"
        } | ConvertTo-Json
        
        try {
            $response = Invoke-RestMethod -Uri "$apiBase/alerts/test/$channel" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 10
            
            if ($response.status -eq "success") {
                Write-Status "$channel test passed ✓"
            } else {
                Write-Warning "$channel test failed: $($response.message)"
            }
        } catch {
            Write-Warning "$channel test failed or not configured"
        }
    }
}

function New-TestAlert {
    Write-Status "Creating test alert..."
    
    $apiBase = "http://localhost:8888/api"
    
    # Check if HexStrike API is running
    try {
        $response = Invoke-WebRequest -Uri "$apiBase/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -ne 200) {
            throw "API not healthy"
        }
    } catch {
        Write-Warning "HexStrike API is not running. Cannot create test alert."
        return
    }
    
    $testAlert = @{
        name = "AlertingSystemTest"
        severity = "warning"
        message = "Alerting system test alert"
        description = "This is a test alert to verify the alerting system is working correctly."
        labels = @{
            service = "hexstrike-ai"
            component = "alerting"
            test = "true"
        }
        annotations = @{
            summary = "Alerting system test"
            runbook_url = "https://docs.hexstrike.ai/runbooks/test-alert"
        }
    } | ConvertTo-Json -Depth 3
    
    try {
        $response = Invoke-RestMethod -Uri "$apiBase/alerts/fire" -Method POST -Body $testAlert -ContentType "application/json" -TimeoutSec 10
        
        if ($response.status -eq "success") {
            Write-Status "Test alert created successfully ✓"
            Write-Status "Check your notification channels for the test alert"
            
            # Wait a bit then resolve the alert
            Start-Sleep -Seconds 10
            
            $resolveAlert = @{
                name = "AlertingSystemTest"
                labels = @{
                    service = "hexstrike-ai"
                    component = "alerting"
                    test = "true"
                }
            } | ConvertTo-Json -Depth 2
            
            try {
                Invoke-RestMethod -Uri "$apiBase/alerts/resolve" -Method POST -Body $resolveAlert -ContentType "application/json" -TimeoutSec 10 | Out-Null
                Write-Status "Test alert resolved ✓"
            } catch {
                Write-Warning "Failed to resolve test alert"
            }
        } else {
            Write-Error "Failed to create test alert: $($response.message)"
        }
    } catch {
        Write-Error "Failed to create test alert: $($_.Exception.Message)"
    }
}

function Show-Configuration {
    Write-Status "Alerting System Configuration Summary"
    Write-Host "==================================================" -ForegroundColor $Colors.Blue
    
    Write-Header "Services:"
    Write-Host "  • Prometheus: http://localhost:9090" -ForegroundColor $Colors.White
    Write-Host "  • Grafana: http://localhost:3000" -ForegroundColor $Colors.White
    Write-Host "  • Alertmanager: http://localhost:9093" -ForegroundColor $Colors.White
    Write-Host ""
    
    Write-Header "API Endpoints:"
    Write-Host "  • Alert API: http://localhost:8888/api/alerts" -ForegroundColor $Colors.White
    Write-Host "  • Fire Alert: POST /api/alerts/fire" -ForegroundColor $Colors.White
    Write-Host "  • Test Notifications: POST /api/alerts/test/{channel}" -ForegroundColor $Colors.White
    Write-Host "  • Active Alerts: GET /api/alerts/active" -ForegroundColor $Colors.White
    Write-Host "  • Alert History: GET /api/alerts/history" -ForegroundColor $Colors.White
    Write-Host ""
    
    Write-Header "Configuration Files:"
    Write-Host "  • Environment: .env" -ForegroundColor $Colors.White
    Write-Host "  • Alertmanager: docker/alertmanager/alertmanager.yml" -ForegroundColor $Colors.White
    Write-Host "  • Prometheus Rules: docker/prometheus/rules/hexstrike_alerts.yml" -ForegroundColor $Colors.White
    Write-Host "  • Grafana Notifications: docker/grafana/provisioning/notifiers/" -ForegroundColor $Colors.White
    Write-Host ""
    
    Write-Header "Next Steps:"
    Write-Host "  1. Configure notification channels in .env file" -ForegroundColor $Colors.White
    Write-Host "  2. Test notification channels: Invoke-RestMethod -Uri http://localhost:8888/api/alerts/test/slack -Method POST" -ForegroundColor $Colors.White
    Write-Host "  3. View Grafana dashboards: http://localhost:3000" -ForegroundColor $Colors.White
    Write-Host "  4. Monitor alerts in Alertmanager: http://localhost:9093" -ForegroundColor $Colors.White
    Write-Host ""
}

function Stop-Services {
    Write-Status "Cleaning up alerting services..."
    
    Set-Location $ProjectRoot
    & docker-compose -f docker-compose.grafana.yml down
    
    Write-Status "Cleanup completed ✓"
}

# Main execution
function Main {
    Write-Header "🛡️  HexStrike AI Alerting Setup"
    Write-Host "==================================================" -ForegroundColor $Colors.Blue
    
    switch ($Action) {
        "setup" {
            Test-Prerequisites
            Setup-Environment
            New-Directories
            Start-Services
            Show-Configuration
        }
        "test" {
            Test-Notifications
            New-TestAlert
        }
        "start" {
            Start-Services
        }
        "stop" {
            Stop-Services
        }
        "status" {
            Test-ServiceHealth
        }
        "config" {
            Show-Configuration
        }
        default {
            Write-Host "Usage: .\setup-alerting.ps1 [setup|test|start|stop|status|config]" -ForegroundColor $Colors.Yellow
            Write-Host ""
            Write-Host "Commands:" -ForegroundColor $Colors.Blue
            Write-Host "  setup   - Full setup of alerting system" -ForegroundColor $Colors.White
            Write-Host "  test    - Test notification channels" -ForegroundColor $Colors.White
            Write-Host "  start   - Start alerting services" -ForegroundColor $Colors.White
            Write-Host "  stop    - Stop alerting services" -ForegroundColor $Colors.White
            Write-Host "  status  - Check service health" -ForegroundColor $Colors.White
            Write-Host "  config  - Show configuration summary" -ForegroundColor $Colors.White
            exit 1
        }
    }
}

# Handle script interruption
trap {
    Write-Warning "Script interrupted. Cleaning up..."
    Stop-Services
    exit 1
}

# Run main function
Main