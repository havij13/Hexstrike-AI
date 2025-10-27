# HexStrike AI - API 架構文檔

## 概述

本目錄包含 HexStrike AI 的 Flask-RESTX API 架構，使用 Swagger/OpenAPI 規範進行文檔化。

## 目錄結構

```
api/
├── __init__.py                 # API 包初始化
├── blueprints/                 # Flask-RESTX Blueprints
│   ├── __init__.py            # 主 API 配置
│   ├── tools/                 # 安全工具端點
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── ai_agents/             # AI 智能端點
│   │   └── __init__.py
│   └── processes/             # 進程管理端點
│       └── __init__.py
├── models/                     # Flask-RESTX Models
│   ├── __init__.py
│   ├── tool_models.py         # 工具相關 models
│   ├── ai_models.py           # AI 相關 models
│   └── process_models.py      # 進程相關 models
├── swagger_config.py           # Swagger 配置
└── README.md                   # 本文件
```

## 快速開始

### 1. 註冊 Blueprint

在 `hexstrike_server.py` 中註冊 API blueprint:

```python
from api.blueprints import api_bp

app.register_blueprint(api_bp)
```

### 2. 訪問 Swagger 文檔

啟動服務器後，訪問：
- Swagger UI: `http://localhost:8888/api/docs/`
- OpenAPI JSON: `http://localhost:8888/api/swagger.json`

### 3. 添加新的端點

在相應的 blueprints 目錄下添加 routes:

```python
# api/blueprints/tools/routes.py
from flask_restx import Resource
from api.blueprints.tools import ns

@ns.route('/new-tool')
class NewTool(Resource):
    @ns.doc('new_tool', description='Description here')
    def post(self):
        return {'success': True, 'data': 'result'}
```

## API 端點

### Tools (安全工具)

- `POST /api/v1/tools/nmap` - Nmap 網絡掃描
- `POST /api/v1/tools/rustscan` - Rustscan 端口掃描
- `POST /api/v1/tools/masscan` - Masscan 快速掃描
- `POST /api/v1/tools/gobuster` - Gobuster 目錄爆破
- `POST /api/v1/tools/nuclei` - Nuclei 漏洞掃描

### AI Agents (AI 智能)

- `POST /api/v1/ai/chat` - AI 對話接口
- `GET /api/v1/ai/agents` - 列出所有 AI agents

### Processes (進程管理)

- `GET /api/v1/processes` - 獲取運行中的進程
- `POST /api/v1/processes/{pid}/stop` - 停止指定進程

## Models (數據模型)

### Tool Models
- `ToolRequest` - 工具請求基礎模型
- `NmapRequest` - Nmap 請求模型
- `RustscanRequest` - Rustscan 請求模型
- `ToolResponse` - 工具響應模型

### AI Models
- `AIRequest` - AI 請求模型
- `AIResponse` - AI 響應模型

### Process Models
- `Process` - 進程信息模型
- `ProcessList` - 進程列表響應模型

## 開發指南

### 添加新的 Model

在 `api/models/` 目錄下創建或修改模型文件：

```python
# api/models/my_models.py
from flask_restx import fields

def create_my_models(api):
    my_model = api.model('MyModel', {
        'field1': fields.String(required=True),
        'field2': fields.Integer()
    })
    return {'my_model': my_model}
```

### 添加新的 Namespace

在 `api/blueprints/` 目錄下創建新的 namespace：

```python
# api/blueprints/mynamespace/__init__.py
from flask_restx import Namespace

ns = Namespace('mynamespace', description='My Namespace')
```

然後在 `api/blueprints/__init__.py` 中註冊：

```python
from .mynamespace import ns as my_ns
api.add_namespace(my_ns)
```

## 測試

### 使用 curl 測試

```bash
# 測試 Nmap
curl -X POST http://localhost:8888/api/v1/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "scan_type": "syn"}'
```

### 使用 Swagger UI

訪問 `http://localhost:8888/api/docs/` 並在瀏覽器中測試所有端點。

## 注意事項

1. **向後兼容**: 確保 API 重構不破壞現有功能
2. **錯誤處理**: 所有端點都應該有適當的錯誤處理
3. **文檔同步**: 確保 Swagger 文檔與實際實現一致
4. **測試覆蓋**: 為所有新端點編寫測試

## 下一步

- [ ] 將現有端點遷移至 Flask-RESTX
- [ ] 實現所有端點的業務邏輯
- [ ] 添加單元測試和集成測試
- [ ] 生成 TypeScript 客戶端
- [ ] 實現 WebSocket 支持

最後更新: 2025-10-26
