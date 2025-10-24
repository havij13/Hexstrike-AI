"""
HexStrike AI API Blueprint Package
Advanced Penetration Testing Framework API with Swagger Documentation
"""

from flask import Blueprint
from .swagger_config import api

# 創建 API 藍圖
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 註冊 API 藍圖
api.init_app(api_bp)

# 導入所有命名空間
from .namespaces import tools, intelligence, processes, cache, files

__all__ = ['api_bp', 'api']
