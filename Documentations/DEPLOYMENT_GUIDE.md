# 🚀 HexStrike AI - 部署快速指南

## ⚡ 您遇到的問題

如果您在 Fly.io 看到：
```
Generating build requirements • Running for 48m12s
```

**原因**：HexStrike AI 的完整 Docker 映像很大（3-5GB），包含 150+ 安全工具，Fly.io 遠端建置會超時。

---

## ✅ 立即解決方案（3 選 1）

### 方案 1：Railway（🏆 最推薦，最簡單）

**為什麼選 Railway？**
- ✅ 無需任何額外配置
- ✅ 支援大型 Docker 映像
- ✅ 建置時間不受限
- ✅ GitHub 自動部署
- ✅ 免費 $5/月額度

**步驟**：
```bash
# 1. 提交程式碼（如果還沒有）
git add .
git commit -m "Add Docker deployment"
git push

# 2. 前往 Railway
打開瀏覽器：https://railway.app

# 3. 部署
- 點選 "New Project"
- 選擇 "Deploy from GitHub repo"
- 選擇 hexstrike-ai repository
- Railway 自動偵測 Dockerfile
- 等待建置（約 10-15 分鐘）
- 獲得 URL: https://your-app.railway.app

# 4. 測試
curl https://your-app.railway.app/health
```

**完成！** 🎉

---

### 方案 2：Render（第二推薦）

**為什麼選 Render？**
- ✅ 免費 750 小時/月
- ✅ 自動 SSL
- ✅ 支援大型映像
- ✅ 使用 render.yaml 自動配置

**步驟**：
```bash
# 1. 提交程式碼
git add .
git commit -m "Add Docker deployment"
git push

# 2. 前往 Render
打開瀏覽器：https://render.com

# 3. 建立 Web Service
- Dashboard → "New" → "Web Service"
- 連接 GitHub repository
- Render 會自動讀取 render.yaml
- 點選 "Create Web Service"
- 等待建置（約 15-20 分鐘）

# 4. 獲得 URL
https://hexstrike-ai.onrender.com
```

**注意**：免費層級會在 15 分鐘無活動後休眠。

---

### 方案 3：Fly.io（使用最小化版本）

如果您堅持使用 Fly.io，我們提供了輕量版：

**步驟**：

1. **刪除舊配置**
```bash
rm fly.toml
rm -rf .fly
```

2. **更新 fly.toml 使用最小化映像**
```toml
app = "hexstrike-ai"
primary_region = "sea"

[build]
  dockerfile = "Dockerfile.minimal"  # 使用最小化版本

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

3. **部署**
```bash
fly launch --no-deploy
fly deploy
```

**限制**：最小化版本只包含核心工具（nmap, curl 等），不包含所有 150+ 工具。

---

## 📊 平台比較總結

| 平台 | 建置時間 | 完整工具支援 | 免費額度 | 推薦度 |
|------|----------|--------------|----------|--------|
| **Railway** | 10-15 分鐘 | ✅ 是 | $5/月 | ⭐⭐⭐⭐⭐ |
| **Render** | 15-20 分鐘 | ✅ 是 | 750h/月 | ⭐⭐⭐⭐ |
| **Fly.io (完整)** | ❌ 超時 | ✅ 是 | 3 VM | ⭐⭐ |
| **Fly.io (最小)** | 5-8 分鐘 | ❌ 部分 | 3 VM | ⭐⭐⭐ |

---

## 🎯 我的建議

### 如果您想要：

✅ **最簡單部署** → 選擇 **Railway**
- 不需要任何配置
- 直接連接 GitHub
- 一鍵部署

✅ **最多免費時數** → 選擇 **Render**
- 750 小時/月
- 自動 SSL
- 穩定可靠

✅ **全球低延遲** → 選擇 **Fly.io（最小化）**
- 全球邊緣網路
- 但只有核心工具

---

## 🚀 立即行動

### 1️⃣ 取消當前的 Fly.io 建置

在 Fly.io dashboard 點選 "Cancel"

### 2️⃣ 選擇 Railway 部署（推薦）

```bash
# 確保所有檔案已提交
git status
git add .
git commit -m "Ready for Railway deployment"
git push

# 前往 Railway
https://railway.app
# → Login with GitHub
# → New Project
# → Deploy from GitHub repo
# → 選擇 hexstrike-ai
# → 等待自動部署
```

### 3️⃣ 獲得您的 URL

部署完成後，Railway 會給您一個 URL，例如：
```
https://hexstrike-ai-production-xxxx.up.railway.app
```

### 4️⃣ 測試部署

```bash
curl https://your-app.railway.app/health
```

預期回應：
```json
{
  "status": "healthy",
  "version": "6.0",
  "available_tools": 150
}
```

---

## 🔧 配置 MCP 客戶端

部署成功後，更新您的 AI 客戶端配置：

**Claude Desktop** (`~/.config/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "python3",
      "args": [
        "C:/Users/dennis.lee/Documents/GitHub/Hexstrike-AI/hexstrike_mcp.py",
        "--server",
        "https://your-app.railway.app"
      ],
      "description": "HexStrike AI v6.0 - Railway Deployed",
      "timeout": 300
    }
  }
}
```

---

## ❓ 常見問題

### Q: Railway 建置會超時嗎？
**A**: 不會。Railway 的建置時間限制很寬鬆，完全支援大型映像。

### Q: Railway 免費嗎？
**A**: 有 $5/月免費額度（約 500 小時運行時間），對測試和開發足夠。

### Q: 我可以使用自訂域名嗎？
**A**: 可以。Railway、Render、Fly.io 都支援自訂域名。

### Q: 如果免費額度用完了呢？
**A**: Railway 會暫停服務。您可以升級到付費方案（約 $5-10/月）。

---

## 📚 相關文件

- [FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md) - 詳細的 Fly.io 故障排除
- [README.md](README.md#docker-deployment) - 完整 Docker 部署文件

---

## 🆘 需要幫助？

- 💬 Discord: https://discord.gg/BWnmrrSHbA
- 🐛 GitHub Issues: https://github.com/0x4m4/hexstrike-ai/issues

---

**總結**：由於您遇到 Fly.io 建置超時，我強烈建議改用 **Railway**。它是最簡單、最可靠的選項，完全支援 HexStrike AI 的完整功能。

立即前往：https://railway.app 🚀

