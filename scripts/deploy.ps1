# HexStrike AI v6.0 - Windows PowerShell 部署腳本

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("local", "info")]
    [string]$Action = "local"
)

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🚀 HexStrike AI v6.0 - Windows Deployment Script" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Docker 是否安裝
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found" -ForegroundColor Red
    Write-Host "Please install Docker Desktop: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    exit 1
}

# 檢查 Docker Compose 是否安裝
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
    $useCompose = $true
} catch {
    Write-Host "⚠️  Docker Compose not found" -ForegroundColor Yellow
    Write-Host "Falling back to docker run method..." -ForegroundColor Yellow
    $useCompose = $false
}

Write-Host ""

switch ($Action) {
    "local" {
        Write-Host "============================================================================" -ForegroundColor Cyan
        Write-Host "🏠 Local Docker Deployment" -ForegroundColor Cyan
        Write-Host "============================================================================" -ForegroundColor Cyan
        Write-Host ""

        # 檢查映像是否存在
        $imageExists = docker images hexstrike-ai:v6.0 -q
        if (-not $imageExists) {
            Write-Host "⚠️  Image not found, building..." -ForegroundColor Yellow
            Write-Host "🔨 Building Docker image (this may take 10-30 minutes)..." -ForegroundColor Cyan
            
            $env:DOCKER_BUILDKIT=1
            docker build -t hexstrike-ai:v6.0 .
            
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Build failed!" -ForegroundColor Red
                exit 1
            }
            Write-Host "✅ Build completed!" -ForegroundColor Green
        } else {
            Write-Host "✅ Image already exists" -ForegroundColor Green
        }

        Write-Host ""
        Write-Host "🚀 Starting container..." -ForegroundColor Cyan

        if ($useCompose) {
            docker-compose up -d
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "✅ Service started (using Docker Compose)" -ForegroundColor Green
                Write-Host ""
                Write-Host "View logs: docker-compose logs -f" -ForegroundColor Yellow
                Write-Host "Stop service: docker-compose down" -ForegroundColor Yellow
            } else {
                Write-Host "❌ Failed to start service" -ForegroundColor Red
                exit 1
            }
        } else {
            docker run -d `
                --name hexstrike `
                -p 8888:8888 `
                -e HEXSTRIKE_PORT=8888 `
                -e HEXSTRIKE_HOST=0.0.0.0 `
                -v "${PWD}/logs:/app/logs" `
                hexstrike-ai:v6.0

            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "✅ Container started" -ForegroundColor Green
                Write-Host ""
                Write-Host "View logs: docker logs -f hexstrike" -ForegroundColor Yellow
                Write-Host "Stop container: docker stop hexstrike" -ForegroundColor Yellow
                Write-Host "Remove container: docker rm hexstrike" -ForegroundColor Yellow
            } else {
                Write-Host "❌ Failed to start container" -ForegroundColor Red
                exit 1
            }
        }

        Write-Host ""
        Write-Host "Waiting for service to start..." -ForegroundColor Cyan
        Start-Sleep -Seconds 5

        Write-Host ""
        Write-Host "🧪 Testing connection..." -ForegroundColor Cyan
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8888/health" -UseBasicParsing -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Service is running!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Access at: http://localhost:8888" -ForegroundColor Cyan
                Write-Host "Health check: http://localhost:8888/health" -ForegroundColor Cyan
            }
        } catch {
            Write-Host "❌ Cannot connect to service" -ForegroundColor Red
            Write-Host "Please check logs for troubleshooting" -ForegroundColor Yellow
        }
    }

    "info" {
        Write-Host "============================================================================" -ForegroundColor Cyan
        Write-Host "📚 Cloud Deployment Information" -ForegroundColor Cyan
        Write-Host "============================================================================" -ForegroundColor Cyan
        Write-Host ""

        Write-Host "Choose a platform:" -ForegroundColor Yellow
        Write-Host "1. Railway - Easiest, GitHub integration"
        Write-Host "2. Render - Free SSL, auto-deploy"
        Write-Host "3. Fly.io - Global edge network, CLI tools"
        Write-Host ""

        $choice = Read-Host "Select platform (1-3)"

        switch ($choice) {
            "1" {
                Write-Host ""
                Write-Host "============================================================================" -ForegroundColor Cyan
                Write-Host "🚂 Railway Deployment Guide" -ForegroundColor Cyan
                Write-Host "============================================================================" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "Steps:" -ForegroundColor Yellow
                Write-Host "1. Visit https://railway.app and login with GitHub"
                Write-Host "2. Click 'New Project' → 'Deploy from GitHub repo'"
                Write-Host "3. Select hexstrike-ai repository"
                Write-Host "4. Railway will auto-detect Dockerfile and deploy"
                Write-Host "5. After deployment, click 'Settings' → 'Generate Domain'"
                Write-Host ""
                Write-Host "Config file: railway.toml (included)" -ForegroundColor Cyan
                Write-Host "Free tier: `$5/month (~500 hours)" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "More info: https://docs.railway.app/deploy/deployments"
            }

            "2" {
                Write-Host ""
                Write-Host "============================================================================" -ForegroundColor Cyan
                Write-Host "🎨 Render Deployment Guide" -ForegroundColor Cyan
                Write-Host "============================================================================" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "Steps:" -ForegroundColor Yellow
                Write-Host "1. Visit https://render.com and sign up"
                Write-Host "2. Dashboard → 'New' → 'Web Service'"
                Write-Host "3. Connect GitHub repository"
                Write-Host "4. Settings:"
                Write-Host "   - Name: hexstrike-ai"
                Write-Host "   - Environment: Docker"
                Write-Host "   - Region: Oregon (or closest)"
                Write-Host "5. Click 'Create Web Service'"
                Write-Host ""
                Write-Host "Config file: render.yaml (included)" -ForegroundColor Cyan
                Write-Host "Free tier: 750 hours/month, 512MB RAM" -ForegroundColor Cyan
                Write-Host "Note: Free tier sleeps after 15 min inactivity" -ForegroundColor Yellow
                Write-Host ""
                Write-Host "More info: https://render.com/docs/docker"
            }

            "3" {
                Write-Host ""
                Write-Host "============================================================================" -ForegroundColor Cyan
                Write-Host "✈️  Fly.io Deployment Guide" -ForegroundColor Cyan
                Write-Host "============================================================================" -ForegroundColor Cyan
                Write-Host ""

                # 檢查 Fly CLI
                try {
                    $flyVersion = fly version
                    Write-Host "✅ Fly CLI installed: $flyVersion" -ForegroundColor Green
                } catch {
                    Write-Host "⚠️  Fly CLI not installed" -ForegroundColor Yellow
                    Write-Host ""
                    Write-Host "Install Fly CLI:" -ForegroundColor Yellow
                    Write-Host "  PowerShell: iwr https://fly.io/install.ps1 -useb | iex"
                    Write-Host ""
                }

                Write-Host ""
                Write-Host "Deployment steps:" -ForegroundColor Yellow
                Write-Host "1. Install and login:"
                Write-Host "   fly auth login"
                Write-Host ""
                Write-Host "2. Launch app (first time):"
                Write-Host "   fly launch"
                Write-Host ""
                Write-Host "3. Deploy:"
                Write-Host "   fly deploy"
                Write-Host ""
                Write-Host "4. Check status:"
                Write-Host "   fly status"
                Write-Host "   fly logs"
                Write-Host ""
                Write-Host "5. Open in browser:"
                Write-Host "   fly open"
                Write-Host ""
                Write-Host "Config file: fly.toml (included)" -ForegroundColor Cyan
                Write-Host "Free tier: 3 shared CPU VMs, 256MB RAM each" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "More info: https://fly.io/docs/languages-and-frameworks/dockerfile/"
            }

            default {
                Write-Host "Invalid choice" -ForegroundColor Red
            }
        }
    }

    default {
        Write-Host "Invalid action. Use: -Action local OR -Action info" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "📚 More Resources" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Quick Start Guide: QUICKSTART.md"
Write-Host "Full Docker Guide: DOCKER.md"
Write-Host "README: README.md"
Write-Host "============================================================================" -ForegroundColor Cyan

