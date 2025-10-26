"""
HexStrike AI - API Package
This package contains all API blueprints, models, and utilities.
"""

__version__ = '1.0.0'

from flask import Blueprint
from .swagger_config import api

# 創建 API 藍圖
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 註冊 API 藍圖
api.init_app(api_bp)

# 導入所有命名空間
from .namespaces import tools, intelligence, processes, cache, files

# 註冊所有命名空間到 API
api.add_namespace(tools.tools_ns)
api.add_namespace(intelligence.intelligence_ns)
api.add_namespace(processes.processes_ns)
api.add_namespace(cache.cache_ns)
api.add_namespace(files.files_ns)

__all__ = ['api_bp', 'api']
