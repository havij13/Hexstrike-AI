# HexStrike AI v6.0 - 快速入門指南

> 5 分鐘內完成 Docker 部署並開始使用

## 🚀 最快速的方法（使用 Makefile）

如果你的系統已安裝 Docker 和 Docker Compose：

```bash
# 1. Clone repository
git clone https://github.com/0x4m4/hexstrike-ai.git
cd hexstrike-ai

# 2. 一鍵部署 (建置 + 啟動 + 測試)
make deploy-local

# 3. 完成！服務運行於 http://localhost:8888
```

就這麼簡單！✨

---

## 📋 前置需求

### 必要軟體

- **Docker Desktop** (20.10+)
  - Windows: [下載](https://docs.docker.com/desktop/install/windows-install/)
  - macOS: [下載](https://docs.docker.com/desktop/install/mac-install/)
  - Linux: [下載](https://docs.docker.com/desktop/install/linux-install/)

- **Docker Compose** (2.0+，通常隨 Docker Desktop 一起安裝)

### 系統需求

- **記憶體**: 4GB RAM 最低 (8GB 建議)
- **儲存**: 10GB 可用空間
- **網路**: 需要網際網路連線 (首次建置下載依賴)

---

## 🎯 三種部署方式

### 方式 1：Makefile（推薦新手）

最簡單的方式，一個指令搞定所有事情。

```bash
# 查看所有可用指令
make help

# 完整部署流程
make deploy-local
```

**包含步驟**：
1. 建置 Docker 映像
2. 啟動容器
3. 執行健康檢查測試

### 方式 2：Docker Compose（推薦開發者）

提供更多控制和配置選項。

```bash
# 建置並啟動
docker-compose up -d

# 查看即時日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

### 方式 3：純 Docker（進階使用者）

完全手動控制每個步驟。

```bash
# 1. 建置映像
docker build -t hexstrike-ai:v6.0 .

# 2. 執行容器
docker run -d \
  --name hexstrike \
  -p 8888:8888 \
  -e HEXSTRIKE_PORT=8888 \
  -v $(pwd)/logs:/app/logs \
  hexstrike-ai:v6.0

# 3. 查看日誌
docker logs -f hexstrike

# 4. 停止並刪除
docker stop hexstrike && docker rm hexstrike
```

---

## ✅ 驗證部署

### 1. 檢查容器狀態

```bash
docker ps | grep hexstrike
```

**預期輸出**：
```
CONTAINER ID   IMAGE                COMMAND                  STATUS         PORTS
abc123def456   hexstrike-ai:v6.0    "/docker-entrypoint.…"  Up 2 minutes   0.0.0.0:8888->8888/tcp
```

### 2. 測試健康端點

```bash
curl http://localhost:8888/health
```

**預期輸出**：
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T12:00:00Z",
  "version": "6.0",
  "available_tools": 150
}
```

### 3. 執行完整測試套件

```bash
make test
# 或
bash scripts/test-docker.sh
```

---

## 🎮 開始使用

### 使用本地實例

現在您的 HexStrike AI 伺服器已經運行於 `http://localhost:8888`。

#### 配置 Claude Desktop

編輯 `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike-ai/hexstrike_mcp.py",
        "--server",
        "http://localhost:8888"
      ],
      "description": "HexStrike AI v6.0 - Local Docker",
      "timeout": 300
    }
  }
}
```

**替換** `/path/to/hexstrike-ai/` 為您的實際路徑。

#### 配置 Cursor / VS Code

編輯 `.cursor/mcp.json` 或 `.vscode/settings.json`:

```json
{
  "servers": {
    "hexstrike": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/path/to/hexstrike-ai/hexstrike_mcp.py",
        "--server",
        "http://localhost:8888"
      ]
    }
  }
}
```

### 測試 AI 整合

重新啟動您的 AI 客戶端，然後嘗試：

```
你好！我想測試 HexStrike AI 工具。請使用 hexstrike-ai MCP 伺服器來掃描 localhost 的開放端口。
```

AI 應該會調用 HexStrike 的 nmap 工具並返回結果。

---

## 🌐 部署到雲端 VPS

### 快速決策助手

使用部署腳本獲取詳細說明：

```bash
bash scripts/deploy.sh
```

選擇您想要的平台：
1. **Railway** - 最簡單，GitHub 整合
2. **Render** - 免費 SSL，自動部署
3. **Fly.io** - 全球邊緣網路，CLI 工具

### 雲端部署後

獲得公開 URL 後 (例如 `https://your-app.railway.app`)，更新 MCP 配置：

```json
{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://your-app.railway.app"  // 👈 使用你的 URL
      ],
      "description": "HexStrike AI v6.0 - Cloud",
      "timeout": 300
    }
  }
}
```

---

## 🔧 常見問題排除

### 問題：建置時間太長

**原因**: 需要下載 Kali Linux 基礎映像 (~1GB) 和安裝 150+ 工具。

**解決方案**: 
- 首次建置需要 10-30 分鐘，這是正常的
- 使用 BuildKit 加速：`export DOCKER_BUILDKIT=1`
- 後續建置會使用快取，快很多

### 問題：容器啟動後立即退出

```bash
# 查看錯誤日誌
docker logs hexstrike
```

**常見原因**：
- Port 8888 被佔用 → 更改為其他 port: `-p 9999:8888`
- 記憶體不足 → 增加 Docker Desktop 的記憶體限制

### 問題：健康檢查失敗

```bash
# 進入容器除錯
docker exec -it hexstrike /bin/bash

# 檢查服務是否運行
ps aux | grep python
```

### 問題：某些工具不可用

**診斷**：
```bash
docker exec -it hexstrike /bin/bash
which nmap gobuster nuclei  # 檢查工具路徑
```

**解決**: 編輯 `Dockerfile`，確保工具已安裝。

---

## 📚 下一步

- 📖 閱讀 [DOCKER.md](DOCKER.md) - 完整 Docker 部署指南
- 🛠️ 查看 [README.md](README.md) - 150+ 工具完整列表
- 🔐 了解 [Security Considerations](README.md#security-considerations) - 合法使用指南
- 💬 加入 [Discord](https://discord.gg/BWnmrrSHbA) - 獲取社群支援

---

## 🆘 需要幫助？

### 查看日誌
```bash
make logs          # 如果使用 Makefile
docker-compose logs -f  # 如果使用 Compose
docker logs -f hexstrike  # 如果使用純 Docker
```

### 重新開始
```bash
make clean         # 清理所有資源
make deploy-local  # 重新部署
```

### 社群支援

- **GitHub Issues**: [回報問題](https://github.com/0x4m4/hexstrike-ai/issues)
- **Discord**: [加入社群](https://discord.gg/BWnmrrSHbA)
- **LinkedIn**: [關注更新](https://www.linkedin.com/company/hexstrike-ai)

---

**享受使用 HexStrike AI！** 🎉

*如果覺得有幫助，請給我們一個 ⭐ Star on GitHub!*

