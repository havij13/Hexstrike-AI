# PowerShell script for deploying HexStrike AI system monitoring dashboards
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("deploy", "validate", "urls", "health")]
    [string]$Action,
    
    [switch]$Force,
    [switch]$Verbose
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    $colorMap = @{
        "Green" = "Green"
        "Red" = "Red"
        "Yellow" = "Yellow"
        "Blue" = "Blue"
        "Cyan" = "Cyan"
        "Magenta" = "Magenta"
        "White" = "White"
    }
    
    Write-Host $Message -ForegroundColor $colorMap[$Color]
}

# Function to check if Python is available
function Test-PythonAvailable {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Python is available: $pythonVersion" "Green"
            return $true
        }
    }
    catch {
        Write-ColorOutput "❌ Python is not available or not in PATH" "Red"
        return $false
    }
    
    return $false
}

# Function to check if required Python modules are available
function Test-PythonModules {
    $requiredModules = @("requests", "prometheus_client")
    $missingModules = @()
    
    foreach ($module in $requiredModules) {
        try {
            python -c "import $module" 2>$null
            if ($LASTEXITCODE -ne 0) {
                $missingModules += $module
            }
        }
        catch {
            $missingModules += $module
        }
    }
    
    if ($missingModules.Count -gt 0) {
        Write-ColorOutput "❌ Missing Python modules: $($missingModules -join ', ')" "Red"
        Write-ColorOutput "💡 Install with: pip install $($missingModules -join ' ')" "Yellow"
        return $false
    }
    
    Write-ColorOutput "✅ All required Python modules are available" "Green"
    return $true
}

# Function to run Python dashboard manager
function Invoke-DashboardManager {
    param(
        [string]$Action,
        [bool]$Force = $false,
        [bool]$Verbose = $false
    )
    
    # Build Python command
    $pythonScript = "scripts/deploy-dashboards.py"
    $pythonArgs = @($Action)
    
    if ($Force) {
        $pythonArgs += "--force"
    }
    
    if ($Verbose) {
        $pythonArgs += "--verbose"
    }
    
    # Check if script exists
    if (-not (Test-Path $pythonScript)) {
        Write-ColorOutput "❌ Python script not found: $pythonScript" "Red"
        return $false
    }
    
    try {
        Write-ColorOutput "🐍 Running Python dashboard manager..." "Blue"
        python $pythonScript @pythonArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Dashboard manager completed successfully" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Dashboard manager failed with exit code: $LASTEXITCODE" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error running dashboard manager: $($_.Exception.Message)" "Red"
        return $false
    }
}

# Function to check Grafana connectivity
function Test-GrafanaConnectivity {
    $grafanaUrl = $env:GRAFANA_URL
    if (-not $grafanaUrl) {
        $grafanaUrl = "http://localhost:3000"
    }
    
    try {
        Write-ColorOutput "🔍 Checking Grafana connectivity at $grafanaUrl..." "Blue"
        
        $response = Invoke-WebRequest -Uri "$grafanaUrl/api/health" -Method GET -TimeoutSec 10 -UseBasicParsing
        
        if ($response.StatusCode -eq 200) {
            Write-ColorOutput "✅ Grafana is accessible" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Grafana returned status code: $($response.StatusCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Cannot connect to Grafana: $($_.Exception.Message)" "Red"
        Write-ColorOutput "💡 Make sure Grafana is running and accessible at $grafanaUrl" "Yellow"
        return $false
    }
}

# Function to show environment information
function Show-EnvironmentInfo {
    Write-ColorOutput "🔧 Environment Information:" "Cyan"
    
    # Grafana URL
    $grafanaUrl = $env:GRAFANA_URL
    if (-not $grafanaUrl) {
        $grafanaUrl = "http://localhost:3000 (default)"
    }
    Write-Host "  Grafana URL: $grafanaUrl"
    
    # Grafana credentials
    $grafanaUser = $env:GRAFANA_ADMIN_USER
    if (-not $grafanaUser) {
        $grafanaUser = "admin (default)"
    }
    Write-Host "  Grafana User: $grafanaUser"
    
    # Python version
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "  Python: $pythonVersion"
    }
    catch {
        Write-Host "  Python: Not available"
    }
    
    Write-Host ""
}

# Main execution
try {
    Write-ColorOutput "🚀 HexStrike AI Dashboard Manager (PowerShell)" "Cyan"
    Write-ColorOutput "=" * 60 "Cyan"
    
    # Show environment info if verbose
    if ($Verbose) {
        Show-EnvironmentInfo
    }
    
    # Check prerequisites
    Write-ColorOutput "🔍 Checking prerequisites..." "Blue"
    
    if (-not (Test-PythonAvailable)) {
        Write-ColorOutput "❌ Python is required but not available" "Red"
        exit 1
    }
    
    if (-not (Test-PythonModules)) {
        Write-ColorOutput "❌ Required Python modules are missing" "Red"
        exit 1
    }
    
    # For deploy action, check Grafana connectivity
    if ($Action -eq "deploy" -or $Action -eq "health") {
        if (-not (Test-GrafanaConnectivity)) {
            Write-ColorOutput "❌ Cannot proceed - Grafana is not accessible" "Red"
            exit 1
        }
    }
    
    # Run the dashboard manager
    $success = Invoke-DashboardManager -Action $Action -Force $Force -Verbose $Verbose
    
    if ($success) {
        Write-ColorOutput "🎉 Operation completed successfully!" "Green"
        exit 0
    } else {
        Write-ColorOutput "❌ Operation failed" "Red"
        exit 1
    }
}
catch {
    Write-ColorOutput "❌ Unexpected error: $($_.Exception.Message)" "Red"
    
    if ($Verbose) {
        Write-ColorOutput "Stack trace:" "Yellow"
        Write-Host $_.ScriptStackTrace
    }
    
    exit 1
}
finally {
    # Reset error action preference
    $ErrorActionPreference = "Continue"
}