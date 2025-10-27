"""
Cache Namespace - Cache Management Operations
包含緩存管理和統計的 API 端點
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import time

# 創建緩存管理命名空間
cache_ns = Namespace('cache', description='Cache Management Operations', path='/api/cache')

# 導入模型
from api.models import (
    cache_stats_response_model, api_response_model, error_response_model
)

# 模擬緩存數據（實際應用中應該使用 Redis 或 Memcached）
cache_data = {
    'hit_count': 1250,
    'miss_count': 250,
    'total_requests': 1500,
    'cache_size': 1024 * 1024 * 100,  # 100MB
    'ttl': 3600
}

# ============================================================================
# 緩存統計端點
# ============================================================================

@cache_ns.route('/stats')
class CacheStats(Resource):
    @cache_ns.response(200, 'Success', cache_stats_response_model)
    @cache_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self):
        '''獲取緩存統計信息'''
        try:
            hit_count = cache_data['hit_count']
            miss_count = cache_data['miss_count']
            total_requests = cache_data['total_requests']
            
            hit_rate = (hit_count / total_requests * 100) if total_requests > 0 else 0
            miss_rate = (miss_count / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'hit_rate': round(hit_rate, 2),
                'miss_rate': round(miss_rate, 2),
                'total_requests': total_requests,
                'cache_size': cache_data['cache_size'],
                'ttl': cache_data['ttl']
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 清除緩存端點
# ============================================================================

@cache_ns.route('/clear')
class CacheClear(Resource):
    @cache_ns.response(200, 'Success', api_response_model)
    @cache_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''清除所有緩存'''
        try:
            # 模擬清除緩存
            cache_data['hit_count'] = 0
            cache_data['miss_count'] = 0
            cache_data['total_requests'] = 0
            cache_data['cache_size'] = 0
            
            return {
                'success': True,
                'message': 'Cache cleared successfully',
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 緩存鍵列表端點
# ============================================================================

@cache_ns.route('/keys')
class CacheKeys(Resource):
    @cache_ns.response(200, 'Success')
    @cache_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self):
        '''獲取所有緩存鍵列表'''
        try:
            # 模擬緩存鍵列表
            cache_keys = [
                'nmap_192.168.1.1_quick',
                'gobuster_https://example.com_common',
                'nuclei_https://example.com_cves',
                'ai_analysis_192.168.1.1_basic',
                'tool_selection_network_30'
            ]
            
            return {
                'cache_keys': cache_keys,
                'total_keys': len(cache_keys),
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 緩存鍵詳情端點
# ============================================================================

@cache_ns.route('/key/<string:key>')
class CacheKeyDetail(Resource):
    @cache_ns.response(200, 'Success')
    @cache_ns.response(404, 'Key Not Found', error_response_model)
    @cache_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self, key):
        '''獲取特定緩存鍵的詳情'''
        try:
            # 模擬緩存鍵詳情
            if key == 'nmap_192.168.1.1_quick':
                key_detail = {
                    'key': key,
                    'value_size': 2048,
                    'ttl': 3600,
                    'created_at': '2025-10-24T12:00:00Z',
                    'expires_at': '2025-10-24T13:00:00Z',
                    'hit_count': 15,
                    'last_accessed': '2025-10-24T12:30:00Z'
                }
                return key_detail
            else:
                return {'success': False, 'error': 'Cache key not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 刪除緩存鍵端點
# ============================================================================

@cache_ns.route('/key/<string:key>')
class CacheKeyDelete(Resource):
    @cache_ns.response(200, 'Success', api_response_model)
    @cache_ns.response(404, 'Key Not Found', error_response_model)
    @cache_ns.response(500, 'Internal Server Error', error_response_model)
    def delete(self, key):
        '''刪除特定緩存鍵'''
        try:
            # 模擬刪除緩存鍵
            if key == 'nmap_192.168.1.1_quick':
                return {
                    'success': True,
                    'message': f'Cache key {key} deleted successfully',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'Cache key not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 緩存配置端點
# ============================================================================

@cache_ns.route('/config')
class CacheConfig(Resource):
    @cache_ns.response(200, 'Success')
    @cache_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self):
        '''獲取緩存配置'''
        try:
            config = {
                'max_size': 1024 * 1024 * 500,  # 500MB
                'default_ttl': 3600,
                'cleanup_interval': 300,
                'eviction_policy': 'lru',
                'compression_enabled': True,
                'persistence_enabled': False
            }
            
            return config
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

    def put(self):
        '''更新緩存配置'''
        try:
            data = request.get_json()
            
            # 模擬更新配置
            return {
                'success': True,
                'message': 'Cache configuration updated successfully',
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
