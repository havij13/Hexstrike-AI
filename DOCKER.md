# HexStrike AI v6.0 - Docker 部署完整指南

本指南將幫助您使用 Docker 部署 HexStrike AI，包含本地建置和雲端 VPS 部署。

## 目錄

- [系統需求](#系統需求)
- [本地建置與測試](#本地建置與測試)
- [雲端平台部署](#雲端平台部署)
- [故障排除](#故障排除)

---

## 系統需求

### 本地開發環境

- **Docker**: 20.10+ 或更新版本
- **Docker Compose**: 2.0+ (可選，建議使用)
- **系統記憶體**: 最少 4GB RAM (建議 8GB)
- **磁碟空間**: 至少 10GB 可用空間

### VPS 雲端部署

- **記憶體**: 2GB 最低，4GB 建議
- **CPU**: 1 vCPU 最低，2 vCPU 建議
- **儲存**: 10GB 最低
- **網路**: 需要公網 IP 或域名

---

## 本地建置與測試

### 方法 1：使用 Docker Compose (推薦)

這是最簡單的方法，適合快速啟動和開發。

```bash
# 1. Clone repository
git clone https://github.com/0x4m4/hexstrike-ai.git
cd hexstrike-ai

# 2. 啟動服務（自動建置）
docker-compose up -d

# 3. 查看日誌
docker-compose logs -f hexstrike

# 4. 測試健康檢查
curl http://localhost:8888/health

# 5. 停止服務
docker-compose down
```

**輸出範例**：
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T10:30:00Z",
  "available_tools": 150
}
```

### 方法 2：直接使用 Docker

適合需要更多控制的進階使用者。

```bash
# 1. 建置映像檔
docker build -t hexstrike-ai:v6.0 .

# 2. 執行容器
docker run -d \
  --name hexstrike \
  -p 8888:8888 \
  -e HEXSTRIKE_PORT=8888 \
  -e HEXSTRIKE_HOST=0.0.0.0 \
  -v $(pwd)/logs:/app/logs \
  hexstrike-ai:v6.0

# 3. 查看日誌
docker logs -f hexstrike

# 4. 進入容器 (除錯用)
docker exec -it hexstrike /bin/bash

# 5. 停止並移除容器
docker stop hexstrike
docker rm hexstrike
```

### 環境變數配置

建立 `.env` 檔案（從 `env.example` 複製）：

```bash
cp env.example .env
```

編輯 `.env` 自訂設定：

```env
HEXSTRIKE_PORT=8888
HEXSTRIKE_HOST=0.0.0.0
CACHE_SIZE=1000
CACHE_TTL=3600
COMMAND_TIMEOUT=300
```

---

## 雲端平台部署

### Railway 部署 (推薦初學者)

Railway 提供簡單的 GitHub 整合和自動部署。

#### 步驟：

1. **註冊帳號**
   - 前往 [railway.app](https://railway.app)
   - 使用 GitHub 帳號登入

2. **建立新專案**
   - 點選 "New Project"
   - 選擇 "Deploy from GitHub repo"
   - 選擇 `hexstrike-ai` repository

3. **配置設定**
   - Railway 會自動偵測 `Dockerfile` 和 `railway.toml`
   - (可選) 設定環境變數：
     ```
     HEXSTRIKE_PORT=8888
     ```

4. **部署**
   - Railway 會自動建置並部署
   - 部署完成後，會獲得公開 URL: `https://your-app.railway.app`

5. **測試部署**
   ```bash
   curl https://your-app.railway.app/health
   ```

#### Railway 免費額度

- **記憶體**: 512MB
- **CPU**: 共享 vCPU
- **使用時數**: $5 免費額度/月 (約 500 小時)
- **自動 HTTPS**: 已包含
- **自訂域名**: 支援

---

### Render 部署

Render 提供強大的免費層級和自動 SSL。

#### 步驟：

1. **註冊帳號**
   - 前往 [render.com](https://render.com)
   - 連接 GitHub 帳號

2. **建立 Web Service**
   - Dashboard → "New" → "Web Service"
   - 連接 GitHub repository

3. **配置服務**
   - **Name**: `hexstrike-ai`
   - **Environment**: `Docker`
   - **Region**: 選擇最近的區域 (如 Oregon)
   - **Branch**: `master` 或 `main`
   - **Dockerfile Path**: 自動偵測

4. **設定環境變數** (可選)
   ```
   HEXSTRIKE_PORT=8888
   HEXSTRIKE_HOST=0.0.0.0
   ```

5. **部署**
   - 點選 "Create Web Service"
   - Render 會自動建置並部署
   - 獲得 URL: `https://hexstrike-ai.onrender.com`

#### Render 免費層級

- **記憶體**: 512MB
- **CPU**: 0.1 vCPU
- **使用時數**: 750 小時/月
- **自動 SSL**: 已包含
- **睡眠機制**: 15 分鐘無活動後休眠
- **啟動時間**: 從休眠喚醒需 30-60 秒

---

### Fly.io 部署

Fly.io 提供全球邊緣網路和高效能容器執行。

#### 步驟：

1. **安裝 Fly CLI**
   ```bash
   # Linux/macOS
   curl -L https://fly.io/install.sh | sh
   
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **登入**
   ```bash
   fly auth login
   ```

3. **初始化應用** (如果是首次部署)
   ```bash
   fly launch
   ```
   
   CLI 會詢問：
   - **App name**: 按 Enter 使用 `hexstrike-ai` (或自訂)
   - **Region**: 選擇最近的區域 (如 `sea` for Seattle)
   - **Postgres database**: 選擇 `No`
   - **Deploy now**: 選擇 `Yes`

4. **部署更新** (後續部署)
   ```bash
   fly deploy
   ```

5. **查看狀態**
   ```bash
   # 查看應用狀態
   fly status
   
   # 查看日誌
   fly logs
   
   # 在瀏覽器開啟
   fly open
   ```

#### Fly.io 免費額度

- **VM 數量**: 最多 3 個共享 CPU VM
- **記憶體**: 每個 VM 256MB (可配置到 2GB)
- **流量**: 160GB/月
- **自動 SSL**: 已包含
- **全球部署**: 支援

#### Fly.io 進階配置

編輯 `fly.toml` 以調整資源：

```toml
[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 1024  # 增加到 1GB (超過免費額度)
```

---

## 配置 MCP 客戶端連接遠端伺服器

部署完成後，更新您的 AI 客戶端配置以連接遠端伺服器。

### Claude Desktop

編輯 `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://your-app.railway.app"
      ],
      "description": "HexStrike AI v6.0 - Railway Deployment",
      "timeout": 300,
      "disabled": false
    }
  }
}
```

### Cursor / VS Code Copilot

編輯 `.vscode/settings.json`:

```json
{
  "servers": {
    "hexstrike": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://your-app.railway.app"
      ]
    }
  }
}
```

### 測試連接

1. 重新啟動您的 AI 客戶端
2. 在聊天中測試：
   ```
   使用 hexstrike-ai MCP 工具掃描 example.com
   ```

---

## 故障排除

### 本地建置問題

#### 問題：建置失敗 - 工具安裝錯誤

```
E: Unable to locate package [tool-name]
```

**解決方案**：
- Kali Linux 儲存庫可能已更新，某些工具名稱可能改變
- 編輯 `Dockerfile`，註解掉無法安裝的工具
- 或等待 Kali Linux 映像更新

#### 問題：記憶體不足

```
Error: failed to build: executor failed running [/bin/sh -c apt-get install...]: exit code: 137
```

**解決方案**：
- 增加 Docker Desktop 的記憶體限制 (建議 4GB+)
- Docker Desktop → Settings → Resources → Memory

### 執行時問題

#### 問題：容器啟動後立即退出

```bash
# 查看退出原因
docker logs hexstrike
```

**常見原因**：
- Python 依賴安裝失敗
- Port 8888 已被佔用

**解決方案**：
```bash
# 使用不同 Port
docker run -d -p 9999:8888 -e HEXSTRIKE_PORT=8888 hexstrike-ai:v6.0
```

#### 問題：健康檢查失敗

```bash
curl http://localhost:8888/health
# curl: (7) Failed to connect to localhost port 8888
```

**解決方案**：
```bash
# 檢查容器是否運行
docker ps -a

# 查看容器日誌
docker logs hexstrike

# 檢查 port mapping
docker port hexstrike
```

### VPS 部署問題

#### Railway: 建置超時

**原因**: 映像檔太大，建置時間超過 10 分鐘

**解決方案**：
- Railway Pro 帳戶有更長的建置時間
- 優化 Dockerfile，減少層數
- 使用預建映像推送到 Docker Hub

#### Render: 服務休眠

**現象**: 首次請求需要 30-60 秒回應

**原因**: 免費層級會在 15 分鐘無活動後休眠

**解決方案**：
- 升級到付費方案 (7 美元/月) 移除休眠
- 使用 cron job 定期 ping 以保持喚醒

#### Fly.io: 記憶體超限

```
Error: oom-kill (out of memory)
```

**解決方案**：
```bash
# 增加記憶體配置到 512MB (仍在免費額度內)
fly scale memory 512

# 查看當前資源使用
fly scale show
```

### 安全工具缺失

**問題**: 某些掃描功能回報工具未找到

**診斷**：
```bash
# 進入容器
docker exec -it hexstrike /bin/bash

# 檢查工具
which nmap gobuster nuclei sqlmap
```

**解決方案**：
```bash
# 在容器內手動安裝缺失的工具
apt-get update
apt-get install -y [missing-tool]
```

---

## 效能優化建議

### 減少映像檔大小

1. **使用多階段建置** (進階)
2. **清理 APT 快取**:
   ```dockerfile
   RUN apt-get clean && rm -rf /var/lib/apt/lists/*
   ```
3. **選擇性安裝工具**: 只安裝您需要的工具

### 加快建置速度

1. **使用 BuildKit**:
   ```bash
   DOCKER_BUILDKIT=1 docker build -t hexstrike-ai:v6.0 .
   ```

2. **利用快取層**:
   - 先複製 `requirements.txt`，再複製其他檔案
   - 依賴變更較少，可重用快取層

### 生產環境建議

1. **新增認證機制** (未來版本)
2. **使用 Nginx 反向代理**
3. **設定 rate limiting**
4. **啟用 HTTPS** (雲端平台通常自動提供)
5. **監控資源使用**

---

## 下一步

- 📖 查看 [README.md](README.md) 了解完整功能
- 🛠️ 查看 [API Reference](README.md#api-reference) 了解可用工具
- 🔒 閱讀 [Security Considerations](README.md#security-considerations) 確保合法使用
- 💬 加入 [Discord 社群](https://discord.gg/BWnmrrSHbA) 獲取支援

---

**建立日期**: 2025-10-23  
**版本**: v6.0  
**作者**: 0x4m4

