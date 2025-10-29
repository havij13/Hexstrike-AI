.PHONY: help build run stop logs test clean deploy-local deploy-info

# 預設目標
.DEFAULT_GOAL := help

# 變數定義
IMAGE_NAME := hexstrike-ai
IMAGE_TAG := v6.0
CONTAINER_NAME := hexstrike
PORT := 8888

help: ## 顯示此幫助訊息
	@echo "HexStrike AI v6.0 - Docker 管理指令"
	@echo ""
	@echo "可用指令："
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

build: ## 建置 Docker 映像
	@echo "🔨 Building Docker image..."
	@chmod +x scripts/build.sh
	@bash scripts/build.sh

run: ## 啟動容器 (使用 docker-compose)
	@echo "🚀 Starting HexStrike AI..."
	@docker-compose up -d
	@echo "✅ Container started!"
	@echo "   View logs: make logs"
	@echo "   Test: make test"

run-docker: ## 使用 docker run 啟動容器 (不用 compose)
	@echo "🚀 Starting HexStrike AI with docker run..."
	@docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):8888 \
		-e HEXSTRIKE_PORT=8888 \
		-e HEXSTRIKE_HOST=0.0.0.0 \
		-v $$(pwd)/logs:/app/logs \
		$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅ Container started!"

stop: ## 停止容器
	@echo "🛑 Stopping containers..."
	@docker-compose down 2>/dev/null || docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@echo "✅ Containers stopped"

logs: ## 查看容器日誌
	@docker-compose logs -f 2>/dev/null || docker logs -f $(CONTAINER_NAME) 2>/dev/null

test: ## 執行測試腳本
	@chmod +x scripts/test-docker.sh
	@bash scripts/test-docker.sh

clean: ## 清理容器和映像
	@echo "🧹 Cleaning up..."
	@docker-compose down -v 2>/dev/null || true
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	@echo "✅ Cleanup complete"

deploy-local: build run test ## 完整本地部署流程 (建置 + 啟動 + 測試)
	@echo "✅ Local deployment complete!"

deploy-info: ## 顯示雲端部署資訊
	@chmod +x scripts/deploy.sh
	@bash scripts/deploy.sh

rebuild: stop clean build run ## 重新建置並啟動

status: ## 查看容器狀態
	@echo "📊 Container Status:"
	@docker ps -a | grep $(CONTAINER_NAME) || echo "No container found"
	@echo ""
	@echo "📊 Image Status:"
	@docker images | grep $(IMAGE_NAME) || echo "No image found"

health: ## 檢查服務健康狀態
	@echo "🏥 Checking health..."
	@curl -s http://localhost:$(PORT)/health | python3 -m json.tool || echo "❌ Service not responding"

shell: ## 進入容器 shell
	@docker exec -it $(CONTAINER_NAME) /bin/bash

push: ## 推送映像到 Docker Hub (需先登入)
	@echo "📤 Pushing to Docker Hub..."
	@docker tag $(IMAGE_NAME):$(IMAGE_TAG) YOUR_DOCKERHUB_USERNAME/$(IMAGE_NAME):$(IMAGE_TAG)
	@docker push YOUR_DOCKERHUB_USERNAME/$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅ Image pushed!"

all: deploy-local ## 執行所有步驟 (同 deploy-local)

