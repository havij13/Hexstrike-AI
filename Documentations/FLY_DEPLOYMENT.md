# Fly.io 部署指南 - HexStrike AI v6.0

## 問題排除：修復 "launch manifest" 錯誤

如果您遇到錯誤：
```
Error: launch manifest was created for a app, but this is a app
```

這是因為 Fly.io 配置需要重新生成。按照以下步驟操作：

---

## 🚀 正確的 Fly.io 部署步驟

### 步驟 1：清理舊配置（如果存在）

```bash
# 刪除舊的 fly.toml（如果存在問題）
rm fly.toml

# 刪除 .fly 目錄（如果存在）
rm -rf .fly
```

### 步驟 2：使用新的 fly.toml

確保您的 `fly.toml` 檔案內容如下：

```toml
# fly.toml app configuration file
app = "hexstrike-ai"
primary_region = "sea"

[build]

[env]
  HEXSTRIKE_PORT = "8888"
  HEXSTRIKE_HOST = "0.0.0.0"

[http_service]
  internal_port = 8888
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1
```

### 步驟 3：重新部署

#### 選項 A：使用現有 app（如果已建立）

```bash
# 確認您已登入
fly auth login

# 檢查現有 apps
fly apps list

# 如果 hexstrike-ai 已存在，直接部署
fly deploy
```

#### 選項 B：建立新的 app（推薦）

```bash
# 刪除舊 app（如果存在問題）
fly apps destroy hexstrike-ai

# 重新建立
fly launch --no-deploy

# 當詢問時：
# - App name: hexstrike-ai（或您想要的名稱）
# - Region: 選擇最近的（如 sea, nrt, hkg）
# - Postgres: No
# - Redis: No
# - Deploy now: No（我們先配置）

# 部署
fly deploy
```

---

## ⚠️ Fly.io 免費層級限制

由於 HexStrike AI 的映像檔較大（3-5GB），可能會遇到以下問題：

### 問題 1：建置超時

**症狀**：
```
Generating build requirements
• Running for 48m12s
```

**原因**：Fly.io 遠端建置有時間限制。

**解決方案 1：本地建置並推送**

```bash
# 1. 本地建置映像
docker build -t registry.fly.io/hexstrike-ai:latest .

# 2. 登入 Fly registry
fly auth docker

# 3. 推送映像
docker push registry.fly.io/hexstrike-ai:latest

# 4. 部署
fly deploy --image registry.fly.io/hexstrike-ai:latest
```

**解決方案 2：使用更小的基礎映像**

建立 `Dockerfile.minimal`（僅核心工具）：

```dockerfile
FROM python:3.11-slim

# 僅安裝關鍵工具
RUN apt-get update && apt-get install -y \
    nmap \
    curl \
    git \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY hexstrike_server.py hexstrike_mcp.py ./
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8888
ENTRYPOINT ["/docker-entrypoint.sh"]
```

然後更新 `fly.toml`：
```toml
[build]
  dockerfile = "Dockerfile.minimal"
```

### 問題 2：記憶體不足

**解決方案**：增加記憶體到 2GB

編輯 `fly.toml`：
```toml
[[vm]]
  memory = '2gb'  # 超過免費額度，每月約 $15
  cpu_kind = 'shared'
  cpus = 1
```

---

## 🎯 推薦方案：Railway 或 Render

考慮到 Fly.io 的限制，對於完整的 HexStrike AI 部署，我們推薦：

### Railway（最簡單）

```bash
# 不需要任何配置，直接：
1. 前往 https://railway.app
2. 連接 GitHub repository
3. Railway 自動偵測 Dockerfile 並部署
4. 完成！
```

### Render（可靠）

```bash
1. 前往 https://render.com
2. New → Web Service
3. 連接 GitHub
4. 選擇 Docker environment
5. 完成！
```

---

## 📊 平台比較

| 特性 | Fly.io | Railway | Render |
|------|--------|---------|--------|
| **建置方式** | 遠端/本地 | 遠端 | 遠端 |
| **建置超時** | 有限制 | 寬鬆 | 寬鬆 |
| **免費記憶體** | 256MB | 512MB | 512MB |
| **免費儲存** | 3GB | 包含 | 包含 |
| **部署難度** | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| **大型映像** | ❌ 困難 | ✅ 支援 | ✅ 支援 |

---

## 🔧 Fly.io 除錯指令

```bash
# 查看日誌
fly logs

# 查看建置日誌
fly logs --image

# SSH 進入機器
fly ssh console

# 查看狀態
fly status

# 查看資源使用
fly scale show

# 重新部署
fly deploy --force
```

---

## ✅ 成功部署檢查清單

- [ ] `fly.toml` 使用正確的格式
- [ ] Dockerfile 存在且可建置
- [ ] docker-entrypoint.sh 有執行權限
- [ ] 沒有舊的 `.fly` 目錄
- [ ] 已登入 Fly CLI (`fly auth login`)
- [ ] 選擇適當的 region
- [ ] 記憶體配置足夠（至少 1GB）

---

## 🆘 仍然遇到問題？

### 最快解決方案：使用 Railway

```bash
# 1. 提交您的程式碼
git add .
git commit -m "Add Docker support"
git push

# 2. 前往 Railway
https://railway.app

# 3. 連接 repo，自動部署
完成！
```

Railway 對大型 Docker 映像支援最好，不需要複雜配置。

---

**建議**：如果 Fly.io 持續遇到建置問題，請優先考慮 Railway 或 Render。它們對 Docker 的支援更加完善，適合 HexStrike AI 這類包含大量工具的映像。

