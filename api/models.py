"""
Swagger/OpenAPI Models for HexStrike AI API
定義所有 API 的請求/響應模型
"""

from flask_restx import fields

# ============================================================================
# 通用響應模型
# ============================================================================

# 標準 API 響應模型
api_response_model = {
    'success': fields.Boolean(required=True, description='請求是否成功'),
    'data': fields.Raw(description='響應數據'),
    'execution_time': fields.Float(description='執行時間（秒）'),
    'timestamp': fields.String(description='響應時間戳'),
    'cached': fields.Boolean(description='是否來自緩存')
}

# 錯誤響應模型
error_response_model = {
    'success': fields.Boolean(required=True, description='請求是否成功', example=False),
    'error': fields.String(required=True, description='錯誤訊息'),
    'error_code': fields.String(description='錯誤代碼'),
    'timestamp': fields.String(description='錯誤時間戳')
}

# ============================================================================
# 工具掃描模型
# ============================================================================

# Nmap 掃描請求模型
nmap_request_model = {
    'target': fields.String(required=True, description='掃描目標', example='192.168.1.1'),
    'scan_type': fields.String(description='掃描類型', enum=['quick', 'comprehensive', 'stealth'], default='quick'),
    'ports': fields.String(description='端口範圍', example='1-1000'),
    'options': fields.String(description='額外 Nmap 選項', example='-sV -O')
}

# Nmap 掃描響應模型
nmap_response_model = {
    'target': fields.String(description='掃描目標'),
    'scan_type': fields.String(description='掃描類型'),
    'open_ports': fields.List(fields.Raw, description='開放端口列表'),
    'scan_summary': fields.String(description='掃描摘要'),
    'execution_time': fields.Float(description='執行時間')
}

# Gobuster 掃描請求模型
gobuster_request_model = {
    'url': fields.String(required=True, description='目標 URL', example='https://example.com'),
    'wordlist': fields.String(description='字典文件', example='common.txt'),
    'extensions': fields.String(description='文件擴展名', example='.php,.html,.txt'),
    'threads': fields.Integer(description='線程數', default=10),
    'timeout': fields.Integer(description='超時時間', default=10)
}

# Gobuster 掃描響應模型
gobuster_response_model = {
    'url': fields.String(description='目標 URL'),
    'found_directories': fields.List(fields.Raw, description='發現的目錄'),
    'found_files': fields.List(fields.Raw, description='發現的文件'),
    'execution_time': fields.Float(description='執行時間')
}

# ============================================================================
# AI 智能模型
# ============================================================================

# AI 目標分析請求模型
ai_analyze_request_model = {
    'target': fields.String(required=True, description='分析目標', example='192.168.1.1'),
    'target_type': fields.String(description='目標類型', enum=['ip', 'domain', 'url'], default='ip'),
    'analysis_depth': fields.String(description='分析深度', enum=['basic', 'detailed', 'comprehensive'], default='basic')
}

# AI 目標分析響應模型
ai_analyze_response_model = {
    'target': fields.String(description='分析目標'),
    'target_profile': fields.Raw(description='目標檔案'),
    'vulnerability_assessment': fields.Raw(description='漏洞評估'),
    'recommended_actions': fields.List(fields.String, description='建議行動'),
    'confidence_score': fields.Float(description='置信度分數')
}

# AI 工具選擇請求模型
ai_tool_selection_request_model = {
    'target': fields.String(required=True, description='目標'),
    'scan_type': fields.String(description='掃描類型', enum=['network', 'web', 'binary', 'cloud']),
    'budget': fields.Integer(description='資源預算（分鐘）', default=30)
}

# AI 工具選擇響應模型
ai_tool_selection_response_model = {
    'selected_tools': fields.List(fields.Raw, description='選中的工具'),
    'execution_plan': fields.Raw(description='執行計劃'),
    'estimated_time': fields.Integer(description='預估時間（分鐘）'),
    'confidence': fields.Float(description='置信度')
}

# ============================================================================
# 進程管理模型
# ============================================================================

# 進程信息模型
process_model = {
    'pid': fields.Integer(description='進程 ID'),
    'name': fields.String(description='進程名稱'),
    'command': fields.String(description='執行命令'),
    'status': fields.String(description='進程狀態', enum=['running', 'completed', 'failed', 'paused']),
    'progress_percent': fields.String(description='進度百分比'),
    'runtime': fields.String(description='運行時間'),
    'eta': fields.String(description='預計完成時間'),
    'memory_usage': fields.Float(description='內存使用量'),
    'cpu_usage': fields.Float(description='CPU 使用量')
}

# 進程列表響應模型
process_list_response_model = {
    'active_processes': fields.List(fields.Nested(process_model), description='活躍進程列表'),
    'total_processes': fields.Integer(description='總進程數'),
    'completed_processes': fields.Integer(description='已完成進程數'),
    'failed_processes': fields.Integer(description='失敗進程數')
}

# 進程儀表板響應模型
process_dashboard_response_model = {
    'total_processes': fields.Integer(description='總進程數'),
    'active_processes': fields.Integer(description='活躍進程數'),
    'completed_processes': fields.Integer(description='已完成進程數'),
    'failed_processes': fields.Integer(description='失敗進程數'),
    'system_load': fields.Float(description='系統負載'),
    'memory_usage': fields.Float(description='內存使用率'),
    'cpu_usage': fields.Float(description='CPU 使用率')
}

# ============================================================================
# 系統遙測模型
# ============================================================================

# 系統遙測響應模型
telemetry_response_model = {
    'cpu_usage': fields.Float(description='CPU 使用率'),
    'memory_usage': fields.Float(description='內存使用率'),
    'disk_usage': fields.Float(description='磁盤使用率'),
    'active_connections': fields.Integer(description='活躍連接數'),
    'total_requests': fields.Integer(description='總請求數'),
    'error_rate': fields.Float(description='錯誤率'),
    'uptime': fields.String(description='運行時間'),
    'timestamp': fields.String(description='時間戳')
}

# ============================================================================
# 緩存管理模型
# ============================================================================

# 緩存統計響應模型
cache_stats_response_model = {
    'hit_rate': fields.Float(description='命中率'),
    'miss_rate': fields.Float(description='未命中率'),
    'total_requests': fields.Integer(description='總請求數'),
    'cache_size': fields.Integer(description='緩存大小'),
    'ttl': fields.Integer(description='生存時間')
}

# ============================================================================
# 文件操作模型
# ============================================================================

# 文件信息模型
file_model = {
    'name': fields.String(description='文件名'),
    'size': fields.Integer(description='文件大小'),
    'modified': fields.String(description='修改時間'),
    'type': fields.String(description='文件類型'),
    'path': fields.String(description='文件路徑')
}

# 文件列表響應模型
file_list_response_model = {
    'files': fields.List(fields.Nested(file_model), description='文件列表'),
    'total_files': fields.Integer(description='總文件數'),
    'total_size': fields.Integer(description='總大小')
}

# ============================================================================
# 錯誤處理模型
# ============================================================================

# 錯誤統計響應模型
error_stats_response_model = {
    'statistics': fields.Raw(description='錯誤統計'),
    'recent_errors': fields.List(fields.Raw, description='最近錯誤'),
    'error_rate': fields.Float(description='錯誤率'),
    'total_errors': fields.Integer(description='總錯誤數')
}

# ============================================================================
# 命令執行模型
# ============================================================================

# 命令執行請求模型
command_request_model = {
    'command': fields.String(required=True, description='要執行的命令'),
    'timeout': fields.Integer(description='超時時間（秒）', default=300),
    'async': fields.Boolean(description='是否異步執行', default=False)
}

# 命令執行響應模型
command_response_model = {
    'command': fields.String(description='執行的命令'),
    'output': fields.String(description='命令輸出'),
    'exit_code': fields.Integer(description='退出代碼'),
    'execution_time': fields.Float(description='執行時間'),
    'success': fields.Boolean(description='是否成功')
}
