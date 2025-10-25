"""
Swagger/OpenAPI Configuration for HexStrike AI API
"""

from flask_restx import Api

# API 授權配置
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

# 創建 Flask-RESTX API 實例
api = Api(
    version='6.0.0',
    title='HexStrike AI API',
    description='''
    # HexStrike AI - Advanced Penetration Testing Framework
    
    ## 功能特色
    
    - **AI 驅動的滲透測試** - 智能目標分析和工具選擇
    - **150+ 安全工具集成** - 網絡、Web、二進制、雲端安全工具
    - **實時進程監控** - 完整的執行狀態追蹤
    - **智能緩存系統** - 優化性能和資源使用
    - **Bug Bounty 工作流** - 專業的安全測試流程
    
    ## 認證
    
    使用 API Key 進行認證，在請求頭中包含 `X-API-KEY`。
    
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
    ''',
    doc='/api/docs/',
    authorizations=authorizations,
    security='apikey',
    contact='HexStrike AI Team',
    contact_email='support@hexstrike.ai',
    contact_url='https://hexstrike.ai',
    license='MIT',
    license_url='https://opensource.org/licenses/MIT'
)

# 添加自定義標籤
api.add_namespace = lambda ns: api.add_namespace(ns, path='/api')

# OpenAPI JSON 端點將由 Flask-RESTX 自動生成
# 訪問 /api/swagger.json 獲取 OpenAPI 3.0 規範
