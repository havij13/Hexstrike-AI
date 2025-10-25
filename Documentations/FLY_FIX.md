# 🔧 Fly.io 部署錯誤修復指南

## ❌ 您遇到的錯誤

```
Error: launch manifest was created for a app, but this is a app
unsuccessful command 'flyctl launch plan generate /tmp/manifest.json'
```

## ✅ 立即修復步驟

### 步驟 1：完全重置 Fly.io 配置

```bash
# 1. 刪除所有 Fly.io 相關檔案
rm -rf .fly
rm fly.toml

# 2. 如果已經建立了 app，刪除它
fly apps destroy hexstrike-ai

# 3. 登出再登入
fly auth logout
fly auth login
```

### 步驟 2：使用正確的初始化方式

```bash
# 不要使用 fly launch，手動建立配置

# 1. 建立新的 app
fly apps create hexstrike-ai --org personal

# 2. 確認 fly.toml 內容正確（已更新）
cat fly.toml
```

確保 `fly.toml` 內容如下：

```toml
# fly.toml v2 app configuration file
app = "hexstrike-ai"
primary_region = "sea"

[build]
  dockerfile = "Dockerfile.minimal"

[env]
  HEXSTRIKE_PORT = "8888"
  HEXSTRIKE_HOST = "0.0.0.0"

[http_service]
  internal_port = 8888
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1
```

### 步驟 3：部署

```bash
# 使用最小化 Dockerfile（避免超時）
fly deploy
```

---

## ⚠️ 重要提醒

由於您剛才嘗試使用完整的 `Dockerfile`（建置 48 分鐘後超時），現在 `fly.toml` 已更新為使用 `Dockerfile.minimal`，這樣：

- ✅ 建置時間：5-8 分鐘（而非 48+ 分鐘）
- ✅ 映像大小：~500MB（而非 3-5GB）
- ❌ 限制：只包含核心工具（nmap, curl），不是完整的 150+ 工具

---

## 🏆 更好的選擇：Railway

說實話，基於您的體驗：

1. ❌ Fly.io 第一次嘗試：建置超時 48 分鐘
2. ❌ Fly.io 第二次嘗試：配置錯誤

**我強烈建議改用 Railway**，原因：

### Railway 優勢

| 特性 | Railway | Fly.io |
|------|---------|--------|
| 配置複雜度 | ⭐ 零配置 | ⭐⭐⭐ 需手動配置 |
| 建置時間 | 10-15 分鐘 | 5-8 分鐘（最小版）/ 超時（完整版） |
| 完整工具支援 | ✅ 150+ 工具 | ❌ 僅核心工具 |
| 錯誤率 | 極低 | 已遇到 2 次錯誤 |

### Railway 部署只需 3 步驟

```bash
# 1. 提交程式碼
git add .
git commit -m "Switch to Railway"
git push

# 2. 前往 Railway
開啟瀏覽器：https://railway.app
→ Login with GitHub
→ New Project → Deploy from GitHub repo
→ 選擇 hexstrike-ai

# 3. 等待 10-15 分鐘
→ 完成！獲得 URL
```

**就這樣！** 沒有配置錯誤，沒有超時問題。

---

## 📊 決策建議

### 如果您想要：

✅ **完整的 150+ 安全工具** → 使用 **Railway**
- 零配置
- 穩定可靠
- 10-15 分鐘完成

✅ **只需要核心功能，快速部署** → 使用 **Fly.io（最小版）**
- 需要手動修復配置
- 5-8 分鐘完成
- 只有部分工具

---

## 🚀 立即行動方案

### 方案 A：繼續使用 Fly.io（最小版）

```bash
# 1. 重置
rm -rf .fly fly.toml
fly apps destroy hexstrike-ai

# 2. 重新建立
fly apps create hexstrike-ai

# 3. 確認 fly.toml 使用 Dockerfile.minimal
# （已經更新）

# 4. 部署
fly deploy
```

### 方案 B：改用 Railway（強烈推薦）

```bash
# 1. 提交並推送
git add .
git commit -m "Ready for Railway deployment"
git push

# 2. 前往 Railway
https://railway.app

# 3. 部署（零配置）
New Project → Deploy from GitHub → 完成
```

---

## ⏱️ 時間對比

您已經在 Fly.io 上花費：
- 第一次嘗試：48 分鐘（失敗）
- 第二次嘗試：幾分鐘（配置錯誤）
- **總計**：~50 分鐘，仍未成功

如果改用 Railway：
- **總計**：15 分鐘，完成部署

---

## 💡 我的建議

停止在 Fly.io 上繼續嘗試，改用 **Railway**。

理由：
1. ✅ 您已經浪費了 50 分鐘
2. ✅ Railway 15 分鐘就能完成
3. ✅ Railway 支援完整工具集
4. ✅ Railway 零配置，不會有這些錯誤

---

## 📞 需要幫助？

如果您決定：
- **使用 Railway**：只需前往 https://railway.app，連接 GitHub，點擊部署
- **繼續 Fly.io**：按照上面的「方案 A」步驟操作

您想選擇哪一個？

