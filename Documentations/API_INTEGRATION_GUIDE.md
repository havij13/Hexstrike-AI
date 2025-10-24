# HexStrike AI API 集成指南

## 概述

HexStrike AI 提供完整的 RESTful API 和 Swagger/OpenAPI 文檔，支持 AI 驅動的滲透測試和安全分析。

## API 基礎信息

- **Base URL**: `https://hexstrike-ai-v6-0.onrender.com`
- **API 版本**: v6.0.0
- **認證方式**: API Key (Header: `X-API-KEY`)
- **文檔**: Swagger UI 和 OpenAPI 3.0 JSON

## 快速開始

### 1. 訪問 Swagger UI

```
https://hexstrike-ai-v6-0.onrender.com/api/docs/
```

### 2. 獲取 OpenAPI 規範

```bash
curl https://hexstrike-ai-v6-0.onrender.com/api/swagger.json
```

### 3. 健康檢查

```bash
curl https://hexstrike-ai-v6-0.onrender.com/health
```

## API 端點分類

### 🔧 安全工具 (Tools)

#### Nmap 掃描
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-api-key" \
  -d '{
    "target": "192.168.1.1",
    "scan_type": "quick",
    "ports": "1-1000"
  }'
```

#### Gobuster 目錄枚舉
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-api-key" \
  -d '{
    "url": "https://example.com",
    "wordlist": "common.txt",
    "threads": 10
  }'
```

### 🧠 AI 智能 (Intelligence)

#### AI 目標分析
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-api-key" \
  -d '{
    "target": "192.168.1.1",
    "target_type": "ip",
    "analysis_depth": "detailed"
  }'
```

#### AI 工具選擇
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/intelligence/select-tools \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-api-key" \
  -d '{
    "target": "192.168.1.1",
    "scan_type": "network",
    "budget": 30
  }'
```

### ⚙️ 進程管理 (Processes)

#### 獲取進程列表
```bash
curl https://hexstrike-ai-v6-0.onrender.com/api/processes/list \
  -H "X-API-KEY: your-api-key"
```

#### 獲取進程儀表板
```bash
curl https://hexstrike-ai-v6-0.onrender.com/api/processes/dashboard \
  -H "X-API-KEY: your-api-key"
```

### 💾 緩存管理 (Cache)

#### 獲取緩存統計
```bash
curl https://hexstrike-ai-v6-0.onrender.com/api/cache/stats \
  -H "X-API-KEY: your-api-key"
```

#### 清除緩存
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/cache/clear \
  -H "X-API-KEY: your-api-key"
```

### 📁 文件操作 (Files)

#### 獲取文件列表
```bash
curl https://hexstrike-ai-v6-0.onrender.com/api/files/list \
  -H "X-API-KEY: your-api-key"
```

## 自動生成客戶端

### TypeScript/JavaScript

#### 安裝工具
```bash
npm install --save-dev openapi-typescript-codegen
```

#### 生成客戶端
```bash
npx openapi-typescript-codegen \
  --input https://hexstrike-ai-v6-0.onrender.com/api/swagger.json \
  --output ./src/api/generated \
  --client axios
```

#### 使用生成的客戶端
```typescript
import { HexStrikeAI } from './api/generated';

const client = new HexStrikeAI({
  baseURL: 'https://hexstrike-ai-v6-0.onrender.com',
  headers: {
    'X-API-KEY': 'your-api-key'
  }
});

// 執行 Nmap 掃描
const nmapResult = await client.tools.nmap({
  target: '192.168.1.1',
  scan_type: 'quick'
});

// AI 目標分析
const analysis = await client.intelligence.analyzeTarget({
  target: '192.168.1.1',
  analysis_depth: 'detailed'
});
```

### Python

#### 安裝工具
```bash
pip install openapi-generator-cli
```

#### 生成客戶端
```bash
openapi-generator-cli generate \
  -i https://hexstrike-ai-v6-0.onrender.com/api/swagger.json \
  -g python \
  -o ./hexstrike-client
```

#### 使用生成的客戶端
```python
from hexstrike_client import HexStrikeAI

client = HexStrikeAI(
    base_url='https://hexstrike-ai-v6-0.onrender.com',
    api_key='your-api-key'
)

# 執行 Nmap 掃描
nmap_result = client.tools.nmap({
    'target': '192.168.1.1',
    'scan_type': 'quick'
})

# AI 目標分析
analysis = client.intelligence.analyze_target({
    'target': '192.168.1.1',
    'analysis_depth': 'detailed'
})
```

### Go

#### 安裝工具
```bash
go install github.com/deepmap/oapi-codegen/cmd/oapi-codegen@latest
```

#### 生成客戶端
```bash
oapi-codegen -package hexstrike \
  -generate client \
  https://hexstrike-ai-v6-0.onrender.com/api/swagger.json \
  > hexstrike_client.go
```

#### 使用生成的客戶端
```go
package main

import (
    "context"
    "fmt"
    "hexstrike"
)

func main() {
    client := hexstrike.NewClientWithResponses(
        "https://hexstrike-ai-v6-0.onrender.com",
        hexstrike.WithRequestEditorFn(func(ctx context.Context, req *http.Request) error {
            req.Header.Set("X-API-KEY", "your-api-key")
            return nil
        }),
    )

    // 執行 Nmap 掃描
    nmapResult, err := client.ToolsNmapWithResponse(
        context.Background(),
        hexstrike.ToolsNmapJSONRequestBody{
            Target:   "192.168.1.1",
            ScanType: "quick",
        },
    )
}
```

## 響應格式

所有 API 端點都返回統一的 JSON 響應格式：

```json
{
  "success": true,
  "data": { ... },
  "execution_time": 1.23,
  "timestamp": "2025-10-24T12:00:00Z",
  "cached": false
}
```

### 錯誤響應

```json
{
  "success": false,
  "error": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-10-24T12:00:00Z"
}
```

## 認證和授權

### API Key 認證

在請求頭中包含 API Key：

```bash
curl -H "X-API-KEY: your-api-key" \
  https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap
```

### 獲取 API Key

聯繫 HexStrike AI 團隊獲取 API Key：
- Email: support@hexstrike.ai
- Website: https://hexstrike.ai

## 速率限制

- **免費層**: 100 請求/小時
- **專業層**: 1000 請求/小時
- **企業層**: 無限制

## 最佳實踐

### 1. 錯誤處理

```typescript
try {
  const result = await client.tools.nmap(params);
  if (!result.success) {
    console.error('API Error:', result.error);
  }
} catch (error) {
  console.error('Request failed:', error);
}
```

### 2. 重試機制

```typescript
async function retryRequest(requestFn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await requestFn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

### 3. 緩存響應

```typescript
const cache = new Map();

async function cachedRequest(key: string, requestFn: () => Promise<any>) {
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const result = await requestFn();
  cache.set(key, result);
  return result;
}
```

## 示例應用

### 完整的滲透測試工作流

```typescript
async function penetrationTestWorkflow(target: string) {
  // 1. AI 目標分析
  const analysis = await client.intelligence.analyzeTarget({
    target,
    analysis_depth: 'comprehensive'
  });

  // 2. AI 工具選擇
  const toolSelection = await client.intelligence.selectTools({
    target,
    scan_type: 'network',
    budget: 60
  });

  // 3. 執行選中的工具
  for (const tool of toolSelection.selected_tools) {
    switch (tool.name) {
      case 'nmap':
        await client.tools.nmap({
          target,
          scan_type: 'comprehensive'
        });
        break;
      case 'gobuster':
        await client.tools.gobuster({
          url: `https://${target}`,
          wordlist: 'common.txt'
        });
        break;
    }
  }

  // 4. 獲取結果
  const processes = await client.processes.list();
  const files = await client.files.list();

  return {
    analysis,
    toolSelection,
    processes,
    files
  };
}
```

## 支持和資源

- **文檔**: https://hexstrike-ai-v6-0.onrender.com/api/docs/
- **OpenAPI 規範**: https://hexstrike-ai-v6-0.onrender.com/api/swagger.json
- **GitHub**: https://github.com/hexstrike/hexstrike-ai
- **支持**: support@hexstrike.ai
- **社區**: https://discord.gg/hexstrike

## 更新日誌

### v6.0.0 (2025-10-24)
- ✅ 完整的 Swagger/OpenAPI 3.0 文檔
- ✅ 自動生成的客戶端支持
- ✅ 統一的 API 響應格式
- ✅ AI 驅動的工具選擇和分析
- ✅ 實時進程監控
- ✅ 智能緩存系統
