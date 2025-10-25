#!/bin/bash
# HexStrike AI v6.0 - Docker 建置腳本

set -e

# 設定
IMAGE_NAME="${IMAGE_NAME:-hexstrike-ai}"
IMAGE_TAG="${IMAGE_TAG:-v6.0}"
DOCKERFILE="${DOCKERFILE:-Dockerfile}"

echo "============================================================================"
echo "🔨 Building HexStrike AI Docker Image"
echo "============================================================================"
echo "Image: $IMAGE_NAME:$IMAGE_TAG"
echo "Dockerfile: $DOCKERFILE"
echo "Build Context: $(pwd)"
echo "Time: $(date)"
echo "============================================================================"
echo ""

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 檢查 Dockerfile 是否存在
if [ ! -f "$DOCKERFILE" ]; then
    echo "❌ Error: Dockerfile not found at $DOCKERFILE"
    exit 1
fi

# 檢查必要檔案
echo "📋 Checking required files..."
REQUIRED_FILES=("hexstrike_server.py" "hexstrike_mcp.py" "requirements.txt" "docker-entrypoint.sh")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ Missing: $file"
        exit 1
    fi
done
echo ""

# 詢問是否使用 BuildKit (加速建置)
read -p "使用 Docker BuildKit 加速建置？ (y/n, 預設 y): " use_buildkit
use_buildkit=${use_buildkit:-y}

if [[ "$use_buildkit" =~ ^[Yy]$ ]]; then
    export DOCKER_BUILDKIT=1
    echo "✅ Docker BuildKit enabled"
fi
echo ""

# 開始建置
echo "🏗️  Starting build process..."
echo "⚠️  Note: Initial build may take 10-30 minutes (downloading ~3-5GB)"
echo ""

BUILD_START=$(date +%s)

if docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f "$DOCKERFILE" . ; then
    BUILD_END=$(date +%s)
    BUILD_TIME=$((BUILD_END - BUILD_START))
    
    echo ""
    echo "============================================================================"
    echo "✅ Build completed successfully!"
    echo "============================================================================"
    echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    echo "Build time: ${BUILD_TIME}s ($(($BUILD_TIME / 60))m $(($BUILD_TIME % 60))s)"
    
    # 顯示映像資訊
    echo ""
    echo "📊 Image Information:"
    docker images "$IMAGE_NAME:$IMAGE_TAG" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    # 提供後續步驟
    echo ""
    echo "============================================================================"
    echo "🚀 Next Steps:"
    echo "============================================================================"
    echo "1. Test locally:"
    echo "   docker run -d -p 8888:8888 --name hexstrike $IMAGE_NAME:$IMAGE_TAG"
    echo ""
    echo "2. Or use Docker Compose:"
    echo "   docker-compose up -d"
    echo ""
    echo "3. Check health:"
    echo "   curl http://localhost:8888/health"
    echo ""
    echo "4. Run test suite:"
    echo "   bash scripts/test-docker.sh"
    echo "============================================================================"
    
else
    echo ""
    echo "❌ Build failed!"
    echo "Please check the error messages above."
    exit 1
fi

