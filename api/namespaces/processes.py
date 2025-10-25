"""
Processes Namespace - Process Management Operations
包含進程管理和監控的 API 端點
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import time
import psutil
import os

# 創建進程管理命名空間
processes_ns = Namespace('processes', description='Process Management Operations', path='/api/processes')

# 導入模型
from api.models import (
    process_model, process_list_response_model, process_dashboard_response_model,
    api_response_model, error_response_model
)

# ============================================================================
# 進程列表端點
# ============================================================================

@processes_ns.route('/list')
class ProcessList(Resource):
    @processes_ns.response(200, 'Success', process_list_response_model)
    @processes_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self):
        '''獲取所有活躍進程列表'''
        try:
            # 模擬進程數據（實際應用中應該從數據庫或進程管理器獲取）
            active_processes = [
                {
                    'pid': 1234,
                    'name': 'nmap',
                    'command': 'nmap -sS 192.168.1.1',
                    'status': 'running',
                    'progress_percent': '75%',
                    'runtime': '00:02:15',
                    'eta': '00:00:45',
                    'memory_usage': 45.2,
                    'cpu_usage': 12.8
                },
                {
                    'pid': 1235,
                    'name': 'gobuster',
                    'command': 'gobuster dir -u https://example.com -w common.txt',
                    'status': 'running',
                    'progress_percent': '60%',
                    'runtime': '00:01:30',
                    'eta': '00:01:00',
                    'memory_usage': 32.1,
                    'cpu_usage': 8.5
                },
                {
                    'pid': 1236,
                    'name': 'nuclei',
                    'command': 'nuclei -u https://example.com -t cves/',
                    'status': 'completed',
                    'progress_percent': '100%',
                    'assessment_runtime': '00:05:20',
                    'eta': '00:00:00',
                    'memory_usage': 0.0,
                    'cpu_usage': 0.0
                }
            ]
            
            total_processes = len(active_processes)
            completed_processes = len([p for p in active_processes if p['status'] == 'completed'])
            failed_processes = len([p for p in active_processes if p['status'] == 'failed'])
            
            return {
                'active_processes': active_processes,
                'total_processes': total_processes,
                'completed_processes': completed_processes,
                'failed_processes': failed_processes
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 進程儀表板端點
# ============================================================================

@processes_ns.route('/dashboard')
class ProcessDashboard(Resource):
    @processes_ns.response(200, 'Success', process_dashboard_response_model)
    @processes_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self):
        '''獲取進程儀表板數據'''
        try:
            # 獲取系統信息
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # 模擬進程統計
            total_processes = 3
            active_processes = 2
            completed_processes = 1
            failed_processes = 0
            
            # 計算系統負載
            system_load = psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else cpu_usage
            
            return {
                'total_processes': total_processes,
                'active_processes': active_processes,
                'completed_processes': completed_processes,
                'failed_processes': failed_processes,
                'system_load': round(system_load, 2),
                'memory_usage': round(memory_usage, 2),
                'cpu_usage': round(cpu_usage, 2)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 進程狀態端點
# ============================================================================

@processes_ns.route('/status/<int:pid>')
class ProcessStatus(Resource):
    @processes_ns.response(200, 'Success', process_model)
    @processes_ns.response(404, 'Process Not Found', error_response_model)
    @processes_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self, pid):
        '''獲取特定進程的詳細狀態'''
        try:
            # 模擬進程狀態查詢
            if pid == 1234:
                process_info = {
                    'pid': 1234,
                    'name': 'nmap',
                    'command': 'nmap -sS 192.168.1.1',
                    'status': 'running',
                    'progress_percent': '75%',
                    'runtime': '00:02:15',
                    'eta': '00:00:45',
                    'memory_usage': 45.2,
                    'cpu_usage': 12.8,
                    'start_time': '2025-10-24T12:00:00Z',
                    'output_file': '/tmp/nmap_output.txt',
                    'log_file': '/tmp/nmap.log'
                }
                return process_info
            else:
                return {'success': False, 'error': 'Process not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 進程終止端點
# ============================================================================

@processes_ns.route('/terminate/<int:pid>')
class ProcessTermination(Resource):
    @processes_ns.response(200, 'Success', api_response_model)
    @processes_ns.response(404, 'Process Not Found', error_response_model)
    @processes_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self, pid):
        '''終止特定進程'''
        try:
            # 模擬進程終止
            if pid == 1234:
                return {
                    'success': True,
                    'message': f'Process {pid} terminated successfully',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'Process not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 進程暫停端點
# ============================================================================

@processes_ns.route('/pause/<int:pid>')
class ProcessPause(Resource):
    @processes_ns.response(200, 'Success', api_response_model)
    @processes_ns.response(404, 'Process Not Found', error_response_model)
    @processes_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self, pid):
        '''暫停特定進程'''
        try:
            # 模擬進程暫停
            if pid == 1234:
                return {
                    'success': True,
                    'message': f'Process {pid} paused successfully',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'Process not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 進程恢復端點
# ============================================================================

@processes_ns.route('/resume/<int:pid>')
class ProcessResume(Resource):
    @processes_ns.response(200, 'Success', api_response_model)
    @processes_ns.response(404, 'Process Not Found', error_response_model)
    @processes_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self, pid):
        '''恢復特定進程'''
        try:
            # 模擬進程恢復
            if pid == 1234:
                return {
                    'success': True,
                    'message': f'Process {pid} resumed successfully',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'Process not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 進程輸出端點
# ============================================================================

@processes_ns.route('/output/<int:pid>')
class ProcessOutput(Resource):
    @processes_ns.response(200, 'Success')
    @processes_ns.response(404, 'Process Not Found', error_response_model)
    @processes_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self, pid):
        '''獲取特定進程的輸出'''
        try:
            # 模擬進程輸出
            if pid == 1234:
                output = {
                    'pid': pid,
                    'output': [
                        'Starting Nmap scan...',
                        'Scanning 192.168.1.1...',
                        'Found 3 open ports',
                        'Port 22/tcp open ssh',
                        'Port 80/tcp open http',
                        'Port 443/tcp open https'
                    ],
                    'last_updated': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
                return output
            else:
                return {'success': False, 'error': 'Process not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
