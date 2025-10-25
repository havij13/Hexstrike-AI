"""
Files Namespace - File Operations
包含文件管理和操作的 API 端點
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import time
import os

# 創建文件操作命名空間
files_ns = Namespace('files', description='File Operations', path='/api/files')

# 導入模型
from api.models import (
    file_model, file_list_response_model, api_response_model, error_response_model
)

# ============================================================================
# 文件列表端點
# ============================================================================

@files_ns.route('/list')
class FileList(Resource):
    @files_ns.response(200, 'Success', file_list_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self):
        '''獲取文件列表'''
        try:
            # 模擬文件列表
            files = [
                {
                    'name': 'nmap_scan_results.txt',
                    'size': 2048,
                    'modified': '2025-10-24T12:00:00Z',
                    'type': 'text/plain',
                    'path': '/tmp/nmap_scan_results.txt'
                },
                {
                    'name': 'gobuster_output.txt',
                    'size': 1536,
                    'modified': '2025-10-24T11:30:00Z',
                    'type': 'text/plain',
                    'path': '/tmp/gobuster_output.txt'
                },
                {
                    'name': 'nuclei_report.json',
                    'size': 4096,
                    'modified': '2025-10-24T11:00:00Z',
                    'type': 'application/json',
                    'path': '/tmp/nuclei_report.json'
                },
                {
                    'name': 'ai_analysis_report.pdf',
                    'size': 8192,
                    'modified': '2025-10-24T10:30:00Z',
                    'type': 'application/pdf',
                    'path': '/tmp/ai_analysis_report.pdf'
                }
            ]
            
            total_files = len(files)
            total_size = sum(file['size'] for file in files)
            
            return {
                'files': files,
                'total_files': total_files,
                'total_size': total_size
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 文件詳情端點
# ============================================================================

@files_ns.route('/<string:filename>')
class FileDetail(Resource):
    @files_ns.response(200, 'Success')
    @files_ns.response(404, 'File Not Found', error_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self, filename):
        '''獲取特定文件的詳情'''
        try:
            # 模擬文件詳情
            if filename == 'nmap_scan_results.txt':
                file_detail = {
                    'name': filename,
                    'size': 2048,
                    'modified': '2025-10-24T12:00:00Z',
                    'type': 'text/plain',
                    'path': '/tmp/nmap_scan_results.txt',
                    'permissions': 'rw-r--r--',
                    'owner': 'hexstrike',
                    'group': 'hexstrike',
                    'checksum': 'sha256:abc123def456...',
                    'content_preview': 'Starting Nmap scan...\nScanning 192.168.1.1...\nFound 3 open ports...'
                }
                return file_detail
            else:
                return {'success': False, 'error': 'File not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 文件下載端點
# ============================================================================

@files_ns.route('/download/<string:filename>')
class FileDownload(Resource):
    @files_ns.response(200, 'Success')
    @files_ns.response(404, 'File Not Found', error_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self, filename):
        '''下載特定文件'''
        try:
            # 模擬文件下載
            if filename == 'nmap_scan_results.txt':
                return {
                    'success': True,
                    'message': f'File {filename} downloaded successfully',
                    'download_url': f'/api/files/download/{filename}',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'File not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 文件上傳端點
# ============================================================================

@files_ns.route('/upload')
class FileUpload(Resource):
    @files_ns.response(200, 'Success', api_response_model)
    @files_ns.response(400, 'Bad Request', error_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''上傳文件'''
        try:
            # 模擬文件上傳
            if 'file' in request.files:
                file = request.files['file']
                filename = file.filename
                
                return {
                    'success': True,
                    'message': f'File {filename} uploaded successfully',
                    'file_path': f'/tmp/{filename}',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'No file provided'}, 400
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 文件刪除端點
# ============================================================================

@files_ns.route('/<string:filename>')
class FileDelete(Resource):
    @files_ns.response(200, 'Success', api_response_model)
    @files_ns.response(404, 'File Not Found', error_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def delete(self, filename):
        '''刪除特定文件'''
        try:
            # 模擬文件刪除
            if filename == 'nmap_scan_results.txt':
                return {
                    'success': True,
                    'message': f'File {filename} deleted successfully',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'File not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 文件創建端點
# ============================================================================

@files_ns.route('/create')
class FileCreate(Resource):
    @files_ns.response(200, 'Success', api_response_model)
    @files_ns.response(400, 'Bad Request', error_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''創建新文件'''
        try:
            data = request.get_json()
            filename = data.get('filename')
            content = data.get('content', '')
            
            if not filename:
                return {'success': False, 'error': 'Filename is required'}, 400
            
            # 模擬文件創建
            return {
                'success': True,
                'message': f'File {filename} created successfully',
                'file_path': f'/tmp/{filename}',
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 文件修改端點
# ============================================================================

@files_ns.route('/modify/<string:filename>')
class FileModify(Resource):
    @files_ns.response(200, 'Success', api_response_model)
    @files_ns.response(400, 'Bad Request', error_response_model)
    @files_ns.response(404, 'File Not Found', error_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def put(self, filename):
        '''修改特定文件'''
        try:
            data = request.get_json()
            content = data.get('content')
            
            if content is None:
                return {'success': False, 'error': 'Content is required'}, 400
            
            # 模擬文件修改
            if filename == 'nmap_scan_results.txt':
                return {
                    'success': True,
                    'message': f'File {filename} modified successfully',
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
            else:
                return {'success': False, 'error': 'File not found'}, 404
                
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 文件搜索端點
# ============================================================================

@files_ns.route('/search')
class FileSearch(Resource):
    @files_ns.response(200, 'Success')
    @files_ns.response(400, 'Bad Request', error_response_model)
    @files_ns.response(500, 'Internal Server Error', error_response_model)
    def get(self):
        '''搜索文件'''
        try:
            query = request.args.get('q', '')
            
            if not query:
                return {'success': False, 'error': 'Search query is required'}, 400
            
            # 模擬文件搜索
            search_results = [
                {
                    'name': 'nmap_scan_results.txt',
                    'size': 2048,
                    'modified': '2025-10-24T12:00:00Z',
                    'type': 'text/plain',
                    'path': '/tmp/nmap_scan_results.txt',
                    'match_score': 0.95
                },
                {
                    'name': 'nmap_comprehensive_scan.txt',
                    'size': 4096,
                    'modified': '2025-10-24T11:00:00Z',
                    'type': 'text/plain',
                    'path': '/tmp/nmap_comprehensive_scan.txt',
                    'match_score': 0.85
                }
            ]
            
            return {
                'query': query,
                'results': search_results,
                'total_results': len(search_results),
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
