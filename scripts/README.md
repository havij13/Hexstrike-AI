# HexStrike AI v6.0 - 腳本說明

本目錄包含自動化部署和測試的實用腳本。

## 📁 腳本列表

### Linux / macOS 腳本

#### `build.sh` - Docker 映像建置腳本
自動化 Docker 映像建置流程，包含依賴檢查和建置時間追蹤。

**用法**：
```bash
bash scripts/build.sh
```

**功能**：
- 檢查 Docker 安裝
- 驗證必要檔案
- 可選使用 BuildKit 加速建置
- 顯示建置時間和映像資訊
- 提供後續步驟建議

---

#### `deploy.sh` - 互動式部署腳本
提供互動式選單，幫助選擇部署方式。

**用法**：
```bash
bash scripts/deploy.sh
```

**選項**：
1. **本地 Docker 部署** - 自動建置並啟動容器
2. **Railway 部署說明** - 顯示 Railway 部署步驟
3. **Render 部署說明** - 顯示 Render 部署步驟
4. **Fly.io 部署說明** - 顯示 Fly.io 部署步驟和 CLI 指令

---

#### `test-docker.sh` - 自動化測試腳本
執行完整的健康檢查和 API 端點測試。

**用法**：
```bash
# 測試本地實例
bash scripts/test-docker.sh

# 測試遠端實例
HEXSTRIKE_URL=https://your-app.railway.app bash scripts/test-docker.sh
```

**測試項目**：
- Health check 端點
- Telemetry API
- Cache statistics
- Process list API
- Root 端點可達性

**輸出**：
- ✅ 通過的測試計數
- ❌ 失敗的測試計數
- 除錯建議

---

### Windows PowerShell 腳本

#### `deploy.ps1` - Windows 部署腳本
Windows 用戶的部署自動化腳本。

**用法**：
```powershell
# 本地部署
.\scripts\deploy.ps1 -Action local

# 顯示雲端部署資訊
.\scripts\deploy.ps1 -Action info
```

**功能**：
- 檢查 Docker Desktop 安裝
- 自動建置映像（如不存在）
- 啟動容器並測試連接
- 提供雲端平台部署指南

---

#### `test-docker.ps1` - Windows 測試腳本
Windows 用戶的自動化測試腳本。

**用法**：
```powershell
# 測試本地實例
.\scripts\test-docker.ps1

# 測試遠端實例
.\scripts\test-docker.ps1 -Url "https://your-app.railway.app"
```

**功能**：
- 完整 API 端點測試
- JSON 回應驗證
- 彩色輸出和詳細錯誤報告

---

## 🚀 快速參考

### 常見工作流程

#### 首次本地部署
```bash
# Linux/macOS
bash scripts/build.sh
bash scripts/deploy.sh  # 選擇選項 1

# Windows
.\scripts\deploy.ps1 -Action local
```

#### 測試現有部署
```bash
# Linux/macOS
bash scripts/test-docker.sh

# Windows
.\scripts\test-docker.ps1
```

#### 查看雲端部署選項
```bash
# Linux/macOS
bash scripts/deploy.sh  # 選擇選項 2-4

# Windows
.\scripts\deploy.ps1 -Action info
```

---

## 🔧 疑難排解

### 腳本權限問題 (Linux/macOS)

如果遇到 "Permission denied" 錯誤：

```bash
chmod +x scripts/*.sh
```

### PowerShell 執行策略 (Windows)

如果無法執行 PowerShell 腳本：

```powershell
# 檢查當前策略
Get-ExecutionPolicy

# 暫時允許執行（僅限當前 session）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 或永久設定（需管理員權限）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker 未安裝

所有腳本都會檢查 Docker 是否安裝。如未安裝：

- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

---

## 📚 相關文件

- [QUICKSTART.md](../QUICKSTART.md) - 5 分鐘快速入門
- [DOCKER.md](../DOCKER.md) - 完整 Docker 部署指南
- [README.md](../README.md) - 專案主要文件
- [Makefile](../Makefile) - Make 指令參考

---

## 💡 提示

### 使用 Makefile (Linux/macOS)

如果您熟悉 Make，可以使用更簡單的命令：

```bash
make help          # 查看所有命令
make deploy-local  # 建置 + 啟動 + 測試
make test          # 執行測試
make logs          # 查看日誌
make clean         # 清理所有資源
```

### 自訂環境變數

所有腳本都支援環境變數覆蓋：

```bash
# 自訂映像名稱
IMAGE_NAME=my-hexstrike IMAGE_TAG=latest bash scripts/build.sh

# 測試不同 URL
HEXSTRIKE_URL=http://192.168.1.100:8888 bash scripts/test-docker.sh
```

---

**建立日期**: 2025-10-23  
**版本**: v6.0  
**維護者**: HexStrike AI Team

