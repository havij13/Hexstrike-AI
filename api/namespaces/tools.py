"""
Tools Namespace - Security Tools Operations
包含所有安全工具的 API 端點
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import time
import subprocess
import json

# 創建工具命名空間
tools_ns = Namespace('tools', description='Security Tools Operations', path='/api/tools')

# 導入模型
from api.models import (
    nmap_request_model, nmap_response_model,
    gobuster_request_model, gobuster_response_model,
    command_request_model, command_response_model,
    api_response_model, error_response_model
)

# ============================================================================
# Nmap 掃描端點
# ============================================================================

@tools_ns.route('/nmap')
class NmapScan(Resource):
    @tools_ns.expect(nmap_request_model)
    @tools_ns.response(200, 'Success', nmap_response_model)
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Nmap 端口掃描'''
        try:
            data = request.get_json()
            target = data.get('target')
            scan_type = data.get('scan_type', 'quick')
            ports = data.get('ports', '1-1000')
            options = data.get('options', '')
            
            if not target:
                return {'success': False, 'error': 'Target is required'}, 400
            
            start_time = time.time()
            
            # 構建 Nmap 命令
            if scan_type == 'quick':
                cmd = f"nmap -F {target}"
            elif scan_type == 'comprehensive':
                cmd = f"nmap -sV -O -A {target}"
            elif scan_type == 'stealth':
                cmd = f"nmap -sS -T2 {target}"
            else:
                cmd = f"nmap {target}"
            
            if ports:
                cmd += f" -p {ports}"
            if options:
                cmd += f" {options}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            open_ports = []
            if result.returncode == 0:
                # 簡單的端口解析（實際應用中需要更複雜的解析）
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'open' in line and 'tcp' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            port_info = {
                                'port': parts[0],
                                'state': parts[1],
                                'service': parts[2] if len(parts) > 2 else 'unknown'
                            }
                            open_ports.append(port_info)
            
            return {
                'target': target,
                'scan_type': scan_type,
                'open_ports': open_ports,
                'scan_summary': f"Found {len(open_ports)} open ports",
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# Gobuster 掃描端點
# ============================================================================

@tools_ns.route('/gobuster')
class GobusterScan(Resource):
    @tools_ns.expect(gobuster_request_model)
    @tools_ns.response(200, 'Success', gobuster_response_model)
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Gobuster 目錄枚舉'''
        try:
            data = request.get_json()
            url = data.get('url')
            wordlist = data.get('wordlist', '/usr/share/wordlists/dirb/common.txt')
            extensions = data.get('extensions', '')
            threads = data.get('threads', 10)
            timeout = data.get('timeout', 10)
            
            if not url:
                return {'success': False, 'error': 'URL is required'}, 400
            
            start_time = time.time()
            
            # 構建 Gobuster 命令
            cmd = f"gobuster dir -u {url} -w {wordlist} -t {threads} --timeout {timeout}s"
            if extensions:
                cmd += f" -x {extensions}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            found_directories = []
            found_files = []
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('Gobuster'):
                        if any(ext in line for ext in ['.php', '.html', '.txt', '.js', '.css']):
                            found_files.append(line.strip())
                        else:
                            found_directories.append(line.strip())
            
            return {
                'url': url,
                'found_directories': found_directories,
                'found_files': found_files,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 通用命令執行端點
# ============================================================================

@tools_ns.route('/command')
class CommandExecution(Resource):
    @tools_ns.expect(command_request_model)
    @tools_ns.response(200, 'Success', command_response_model)
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行系統命令'''
        try:
            data = request.get_json()
            command = data.get('command')
            timeout = data.get('timeout', 300)
            async_exec = data.get('async', False)
            
            if not command:
                return {'success': False, 'error': 'Command is required'}, 400
            
            start_time = time.time()
            
            # 執行命令
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
            
            execution_time = time.time() - start_time
            
            return {
                'command': command,
                'output': result.stdout,
                'exit_code': result.returncode,
                'execution_time': round(execution_time, 2),
                'success': result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

# ============================================================================
# 其他工具端點（占位符）
# ============================================================================

@tools_ns.route('/rustscan')
class RustscanScan(Resource):
    def post(self):
        '''執行 Rustscan 高速端口掃描'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/masscan')
class MasscanScan(Resource):
    def post(self):
        '''執行 Masscan 高速端口掃描'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/feroxbuster')
class FeroxbusterScan(Resource):
    def post(self):
        '''執行 Feroxbuster 目錄掃描'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/nuclei')
class NucleiScan(Resource):
    def post(self):
        '''執行 Nuclei 漏洞掃描'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/sqlmap')
class SQLMapScan(Resource):
    def post(self):
        '''執行 SQLMap SQL 注入掃描'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/hydra')
class HydraScan(Resource):
    def post(self):
        '''執行 Hydra 密碼破解'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/john')
class JohnScan(Resource):
    def post(self):
        '''執行 John the Ripper 哈希破解'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/hashcat')
class HashcatScan(Resource):
    def post(self):
        '''執行 Hashcat GPU 破解'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/ghidra')
class GhidraAnalysis(Resource):
    def post(self):
        '''執行 Ghidra 二進制分析'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/radare2')
class Radare2Analysis(Resource):
    def post(self):
        '''執行 Radare2 二進制分析'''
        return {'success': False, 'error': 'Not implemented yet'}, 501

@tools_ns.route('/gdb')
class GDBAnalysis(Resource):
    def post(self):
        '''執行 GDB 調試分析'''
        return {'success': False, 'error': 'Not implemented yet'}, 501
