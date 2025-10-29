# HexStrike AI - Tool Page Generators

自動化工具頁面生成腳本，用於快速批量建立前端工具頁面。

## 📋 說明

這些腳本可以自動生成標準化的 Next.js 工具頁面，減少重複工作並保持代碼一致性。

## 🛠️ 可用的生成器

### 1. Single Tool Generator
**檔案**: `generate-tool-page.sh`

為單一工具生成頁面。

**用法**:
```bash
bash scripts/generate-tool-page.sh <tool-name> <category> <api-endpoint> [description]
```

**範例**:
```bash
bash scripts/generate-tool-page.sh dirb web /api/tools/dirb "Web directory brute forcer"
```

**參數**:
- `tool-name`: 工具名稱（小寫，用於目錄和組件名稱）
- `category`: 工具分類（web, network, binary, etc.）
- `api-endpoint`: 後端 API 端點路徑
- `description`: 工具描述（可選）

### 2. Batch Tool Generator
**檔案**: `generate-multiple-tools.sh`

批量生成多個工具頁面。

**用法**:
```bash
bash scripts/generate-multiple-tools.sh
```

**自訂工具列表**:
編輯腳本中的 `TOOLS` 陣列：

```bash
TOOLS=(
  "dirb,web,/api/tools/dirb,Web directory brute forcer"
  "dirsearch,web,/api/tools/dirsearch,Web path scanner"
  # 添加更多工具...
)
```

## 📁 生成的目錄結構

```
Front-End/src/app/tools/
├── {category}/
│   └── {tool-name}/
│       └── page.tsx
```

## 📝 生成的頁面內容

每個生成的頁面包含：

1. **標準組件引入**
   - ToolForm
   - FormField
   - ScanProfiles
   - ResultsPanel

2. **狀態管理**
   - target: 目標
   - isRunning: 執行狀態
   - results: 結果
   - selectedProfile: 選中的配置

3. **基本配置**
   - 預設掃描配置
   - API 端點
   - 結果處理

4. **UI 佈局**
   - Cyberpunk 風格
   - 響應式設計
   - 標準化表單

## ⚙️ 自訂步驟

生成後的頁面需要手動自訂：

### 1. 工具特定參數
根據後端 API 文檔添加參數：

```tsx
// 範例：添加 wordlist 參數
const [wordlist, setWordlist] = useState('common.txt')

<FormField
  label="Wordlist"
  type="text"
  value={wordlist}
  onChange={setWordlist}
  placeholder="wordlist.txt"
/>
```

### 2. 掃描配置檔
根據工具特性添加配置檔：

```tsx
const scanProfiles = [
  { id: 'quick', name: 'Quick Scan', description: 'Fast scan', estimatedTime: '1-2 minutes', config: {} },
  { id: 'comprehensive', name: 'Full Scan', description: 'Complete scan', estimatedTime: '10-20 minutes', config: {} },
]
```

### 3. API 請求格式
調整請求體以符合後端要求：

```tsx
body: JSON.stringify({
  target,
  wordlist,
  threads: 50,
  // 其他參數...
})
```

## 🚀 快速開始

### 批量生成常用工具

1. 編輯 `generate-multiple-tools.sh`
2. 添加要生成的工具到 `TOOLS` 陣列
3. 執行腳本：

```bash
bash scripts/generate-multiple-tools.sh
```

4. 檢查生成的文件
5. 自訂每個工具的參數
6. 測試工具集成
7. 提交到 Git

## 📋 待生成工具優先級

### 優先級 1: 最常用工具
- [ ] Dirb
- [ ] Dirsearch  
- [ ] Katana
- [ ] Enum4linux
- [ ] Responder

### 優先級 2: 重要工具
- [ ] Metasploit
- [ ] MSFVenom
- [ ] Volatility
- [ ] Binwalk
- [ ] Checksec

### 優先級 3: 進階工具
- [ ] ROPGadget
- [ ] Angr
- [ ] Ropper
- [ ] Pwntools
- [ ] GDB-PEDA

## ⚠️ 注意事項

### 1. 後端 API 兼容性
確保生成頁面使用的 API 端點與後端實現一致。

### 2. 參數驗證
添加適當的客戶端驗證，提升用戶體驗。

### 3. 錯誤處理
增強錯誤處理邏輯，顯示友好的錯誤訊息。

### 4. TypeScript 型別
為複雜的結果添加完整的型別定義。

## 🔗 相關文檔

- [TASKS_STATUS.md](../TASKS_STATUS.md) - 任務狀態追蹤
- [API_USAGE.md](../API_USAGE.md) - API 使用文檔
- [README.md](../README.md) - 專案主文檔

## 💡 提示

### 提高效率
1. 批量生成相似工具（同一分類）
2. 使用模板變數快速替換
3. 建立工具特定模板
4. 使用 IDE 多文件編輯功能

### 代碼品質
1. 遵循一致的代碼風格
2. 添加有意義的註釋
3. 保持組件結構一致
4. 進行必要的測試

---

最後更新: 2025-10-26
