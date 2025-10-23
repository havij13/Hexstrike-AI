#!/bin/bash
# HexStrike AI v6.0 - 快速部署腳本

set -e

echo "============================================================================"
echo "🚀 HexStrike AI v6.0 - Quick Deployment Script"
echo "============================================================================"
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  docker-compose not found${NC}"
    echo "Falling back to docker run method..."
    USE_COMPOSE=false
else
    USE_COMPOSE=true
fi

echo -e "${CYAN}選擇部署方式：${NC}"
echo "1) 本地 Docker 部署 (推薦用於測試)"
echo "2) Railway 部署說明"
echo "3) Render 部署說明"
echo "4) Fly.io 部署說明"
echo ""
read -p "請選擇 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "============================================================================"
        echo "🏠 本地 Docker 部署"
        echo "============================================================================"
        
        # 檢查映像是否存在
        if ! docker images | grep -q "hexstrike-ai.*v6.0"; then
            echo -e "${YELLOW}⚠️  映像不存在，開始建置...${NC}"
            bash scripts/build.sh
        fi
        
        echo ""
        echo "🚀 啟動容器..."
        
        if [ "$USE_COMPOSE" = true ]; then
            docker-compose up -d
            echo ""
            echo -e "${GREEN}✅ 服務已啟動 (使用 Docker Compose)${NC}"
            echo ""
            echo "查看日誌: docker-compose logs -f"
            echo "停止服務: docker-compose down"
        else
            docker run -d \
                --name hexstrike \
                -p 8888:8888 \
                -e HEXSTRIKE_PORT=8888 \
                -e HEXSTRIKE_HOST=0.0.0.0 \
                -v "$(pwd)/logs:/app/logs" \
                hexstrike-ai:v6.0
            
            echo ""
            echo -e "${GREEN}✅ 容器已啟動${NC}"
            echo ""
            echo "查看日誌: docker logs -f hexstrike"
            echo "停止容器: docker stop hexstrike"
            echo "刪除容器: docker rm hexstrike"
        fi
        
        echo ""
        echo "等待服務啟動..."
        sleep 5
        
        echo ""
        echo "🧪 測試連接..."
        if curl -s http://localhost:8888/health > /dev/null; then
            echo -e "${GREEN}✅ 服務運行正常！${NC}"
            echo ""
            echo "訪問: http://localhost:8888"
            echo "健康檢查: http://localhost:8888/health"
        else
            echo -e "${RED}❌ 無法連接到服務${NC}"
            echo "請檢查日誌以排除問題"
        fi
        ;;
        
    2)
        echo ""
        echo "============================================================================"
        echo "🚂 Railway 部署說明"
        echo "============================================================================"
        echo ""
        echo "步驟："
        echo "1. 前往 https://railway.app 並使用 GitHub 登入"
        echo "2. 點選 'New Project' → 'Deploy from GitHub repo'"
        echo "3. 選擇 hexstrike-ai repository"
        echo "4. Railway 會自動偵測 Dockerfile 並開始部署"
        echo "5. 部署完成後，點選 'Settings' → 'Generate Domain' 獲取公開 URL"
        echo ""
        echo -e "${CYAN}配置檔案：${NC}railway.toml (已包含在專案中)"
        echo -e "${CYAN}免費額度：${NC}\$5/月 (約 500 小時運行時間)"
        echo ""
        echo "更多資訊: https://docs.railway.app/deploy/deployments"
        ;;
        
    3)
        echo ""
        echo "============================================================================"
        echo "🎨 Render 部署說明"
        echo "============================================================================"
        echo ""
        echo "步驟："
        echo "1. 前往 https://render.com 並註冊帳號"
        echo "2. Dashboard → 'New' → 'Web Service'"
        echo "3. 連接 GitHub repository"
        echo "4. 設定："
        echo "   - Name: hexstrike-ai"
        echo "   - Environment: Docker"
        echo "   - Region: Oregon (或最近的區域)"
        echo "5. 點選 'Create Web Service' 開始部署"
        echo ""
        echo -e "${CYAN}配置檔案：${NC}render.yaml (已包含在專案中)"
        echo -e "${CYAN}免費額度：${NC}750 小時/月, 512MB RAM"
        echo -e "${YELLOW}注意：${NC}免費層級會在 15 分鐘無活動後休眠"
        echo ""
        echo "更多資訊: https://render.com/docs/docker"
        ;;
        
    4)
        echo ""
        echo "============================================================================"
        echo "✈️  Fly.io 部署說明"
        echo "============================================================================"
        echo ""
        
        if ! command -v flyctl &> /dev/null && ! command -v fly &> /dev/null; then
            echo -e "${YELLOW}⚠️  Fly CLI 未安裝${NC}"
            echo ""
            echo "安裝 Fly CLI:"
            echo "  Linux/macOS: curl -L https://fly.io/install.sh | sh"
            echo "  Windows: iwr https://fly.io/install.ps1 -useb | iex"
            echo ""
        else
            echo -e "${GREEN}✅ Fly CLI 已安裝${NC}"
            echo ""
        fi
        
        echo "部署步驟："
        echo "1. 安裝並登入 Fly CLI:"
        echo "   fly auth login"
        echo ""
        echo "2. 初始化應用 (首次):"
        echo "   fly launch"
        echo ""
        echo "3. 部署應用:"
        echo "   fly deploy"
        echo ""
        echo "4. 查看狀態:"
        echo "   fly status"
        echo "   fly logs"
        echo ""
        echo "5. 在瀏覽器開啟:"
        echo "   fly open"
        echo ""
        echo -e "${CYAN}配置檔案：${NC}fly.toml (已包含在專案中)"
        echo -e "${CYAN}免費額度：${NC}3 個共享 CPU VM, 256MB RAM 每個"
        echo ""
        echo "更多資訊: https://fly.io/docs/languages-and-frameworks/dockerfile/"
        ;;
        
    *)
        echo -e "${RED}無效的選擇${NC}"
        exit 1
        ;;
esac

echo ""
echo "============================================================================"
echo "📚 更多資源"
echo "============================================================================"
echo "完整部署指南: 查看 DOCKER.md"
echo "測試腳本: bash scripts/test-docker.sh"
echo "建置腳本: bash scripts/build.sh"
echo "============================================================================"

