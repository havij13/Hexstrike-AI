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
    @tools_ns.expect(nmap_request_model)
    @tools_ns.response(200, 'Success', nmap_response_model)
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Rustscan 高速端口掃描'''
        try:
            data = request.get_json()
            target = data.get('target')
            ports = data.get('ports', '1-65535')
            timeout = data.get('timeout', 1000)
            
            if not target:
                return {'success': False, 'error': 'Target is required'}, 400
            
            start_time = time.time()
            
            # 構建 Rustscan 命令
            cmd = f"rustscan -a {target} --timeout {timeout} --ulimit 5000"
            if ports:
                cmd += f" -p {ports}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            open_ports = []
            if result.returncode == 0:
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
                'scan_type': 'rustscan',
                'open_ports': open_ports,
                'scan_summary': f"Found {len(open_ports)} open ports",
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/masscan')
class MasscanScan(Resource):
    @tools_ns.expect(nmap_request_model)
    @tools_ns.response(200, 'Success', nmap_response_model)
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Masscan 高速端口掃描'''
        try:
            data = request.get_json()
            target = data.get('target')
            ports = data.get('ports', '1-65535')
            rate = data.get('rate', 1000)
            
            if not target:
                return {'success': False, 'error': 'Target is required'}, 400
            
            start_time = time.time()
            
            # 構建 Masscan 命令
            cmd = f"masscan {target} -p{ports} --rate={rate}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            open_ports = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'open' in line and 'tcp' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            port_info = {
                                'port': parts[2].split('/')[0],
                                'state': 'open',
                                'service': 'unknown'
                            }
                            open_ports.append(port_info)
            
            return {
                'target': target,
                'scan_type': 'masscan',
                'open_ports': open_ports,
                'scan_summary': f"Found {len(open_ports)} open ports",
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/feroxbuster')
class FeroxbusterScan(Resource):
    @tools_ns.expect(gobuster_request_model)
    @tools_ns.response(200, 'Success', gobuster_response_model)
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Feroxbuster 目錄掃描'''
        try:
            data = request.get_json()
            url = data.get('url')
            wordlist = data.get('wordlist', '/usr/share/wordlists/dirb/common.txt')
            threads = data.get('threads', 10)
            timeout = data.get('timeout', 10)
            
            if not url:
                return {'success': False, 'error': 'URL is required'}, 400
            
            start_time = time.time()
            
            # 構建 Feroxbuster 命令
            cmd = f"feroxbuster -u {url} -w {wordlist} -t {threads} --timeout {timeout}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            found_directories = []
            found_files = []
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('Feroxbuster'):
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

@tools_ns.route('/nuclei')
class NucleiScan(Resource):
    @tools_ns.expect(gobuster_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Nuclei 漏洞掃描'''
        try:
            data = request.get_json()
            url = data.get('url')
            templates = data.get('templates', 'cves/')
            severity = data.get('severity', 'critical,high,medium')
            
            if not url:
                return {'success': False, 'error': 'URL is required'}, 400
            
            start_time = time.time()
            
            # 構建 Nuclei 命令
            cmd = f"nuclei -u {url} -t {templates} -severity {severity} -json"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            vulnerabilities = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip():
                        try:
                            vuln_data = json.loads(line)
                            vulnerabilities.append(vuln_data)
                        except json.JSONDecodeError:
                            continue
            
            return {
                'url': url,
                'vulnerabilities': vulnerabilities,
                'total_vulnerabilities': len(vulnerabilities),
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/sqlmap')
class SQLMapScan(Resource):
    @tools_ns.expect(gobuster_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 SQLMap SQL 注入掃描'''
        try:
            data = request.get_json()
            url = data.get('url')
            parameter = data.get('parameter', 'id')
            level = data.get('level', 1)
            risk = data.get('risk', 1)
            
            if not url:
                return {'success': False, 'error': 'URL is required'}, 400
            
            start_time = time.time()
            
            # 構建 SQLMap 命令
            cmd = f"sqlmap -u '{url}' -p {parameter} --level={level} --risk={risk} --batch --no-logging"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            vulnerabilities = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'vulnerable' in line.lower() or 'injection' in line.lower():
                        vulnerabilities.append(line.strip())
            
            return {
                'url': url,
                'parameter': parameter,
                'vulnerabilities': vulnerabilities,
                'is_vulnerable': len(vulnerabilities) > 0,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/hydra')
class HydraScan(Resource):
    @tools_ns.expect(command_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Hydra 密碼破解'''
        try:
            data = request.get_json()
            target = data.get('target')
            service = data.get('service', 'ssh')
            username = data.get('username', 'admin')
            password_list = data.get('password_list', '/usr/share/wordlists/rockyou.txt')
            threads = data.get('threads', 4)
            
            if not target:
                return {'success': False, 'error': 'Target is required'}, 400
            
            start_time = time.time()
            
            # 構建 Hydra 命令
            cmd = f"hydra -l {username} -P {password_list} -t {threads} {target} {service}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            cracked_passwords = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'login:' in line.lower() and 'password:' in line.lower():
                        cracked_passwords.append(line.strip())
            
            return {
                'target': target,
                'service': service,
                'username': username,
                'cracked_passwords': cracked_passwords,
                'success': len(cracked_passwords) > 0,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/john')
class JohnScan(Resource):
    @tools_ns.expect(command_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 John the Ripper 哈希破解'''
        try:
            data = request.get_json()
            hash_file = data.get('hash_file')
            wordlist = data.get('wordlist', '/usr/share/wordlists/rockyou.txt')
            hash_type = data.get('hash_type', 'auto')
            
            if not hash_file:
                return {'success': False, 'error': 'Hash file is required'}, 400
            
            start_time = time.time()
            
            # 構建 John 命令
            cmd = f"john --wordlist={wordlist} --format={hash_type} {hash_file}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            cracked_hashes = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if ':' in line and len(line.split(':')) >= 2:
                        cracked_hashes.append(line.strip())
            
            return {
                'hash_file': hash_file,
                'hash_type': hash_type,
                'cracked_hashes': cracked_hashes,
                'success': len(cracked_hashes) > 0,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/hashcat')
class HashcatScan(Resource):
    @tools_ns.expect(command_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Hashcat GPU 破解'''
        try:
            data = request.get_json()
            hash_file = data.get('hash_file')
            wordlist = data.get('wordlist', '/usr/share/wordlists/rockyou.txt')
            hash_mode = data.get('hash_mode', 0)
            
            if not hash_file:
                return {'success': False, 'error': 'Hash file is required'}, 400
            
            start_time = time.time()
            
            # 構建 Hashcat 命令
            cmd = f"hashcat -m {hash_mode} -a 0 {hash_file} {wordlist}"
            
            # 執行掃描
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            cracked_hashes = []
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if ':' in line and len(line.split(':')) >= 2:
                        cracked_hashes.append(line.strip())
            
            return {
                'hash_file': hash_file,
                'hash_mode': hash_mode,
                'cracked_hashes': cracked_hashes,
                'success': len(cracked_hashes) > 0,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Scan timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/ghidra')
class GhidraAnalysis(Resource):
    @tools_ns.expect(command_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Ghidra 二進制分析'''
        try:
            data = request.get_json()
            binary_file = data.get('binary_file')
            analysis_type = data.get('analysis_type', 'basic')
            
            if not binary_file:
                return {'success': False, 'error': 'Binary file is required'}, 400
            
            start_time = time.time()
            
            # 構建 Ghidra 命令
            cmd = f"ghidra {binary_file} -analysis {analysis_type}"
            
            # 執行分析
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            analysis_results = {
                'functions': [],
                'strings': [],
                'imports': [],
                'exports': []
            }
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'function' in line.lower():
                        analysis_results['functions'].append(line.strip())
                    elif 'string' in line.lower():
                        analysis_results['strings'].append(line.strip())
                    elif 'import' in line.lower():
                        analysis_results['imports'].append(line.strip())
                    elif 'export' in line.lower():
                        analysis_results['exports'].append(line.strip())
            
            return {
                'binary_file': binary_file,
                'analysis_type': analysis_type,
                'analysis_results': analysis_results,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Analysis timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/radare2')
class Radare2Analysis(Resource):
    @tools_ns.expect(command_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 Radare2 二進制分析'''
        try:
            data = request.get_json()
            binary_file = data.get('binary_file')
            analysis_type = data.get('analysis_type', 'basic')
            
            if not binary_file:
                return {'success': False, 'error': 'Binary file is required'}, 400
            
            start_time = time.time()
            
            # 構建 Radare2 命令
            cmd = f"r2 -c 'aaa; afl; iz; ii; ie' {binary_file}"
            
            # 執行分析
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            analysis_results = {
                'functions': [],
                'strings': [],
                'imports': [],
                'exports': []
            }
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'fcn.' in line:
                        analysis_results['functions'].append(line.strip())
                    elif 'str.' in line:
                        analysis_results['strings'].append(line.strip())
                    elif 'imp.' in line:
                        analysis_results['imports'].append(line.strip())
                    elif 'exp.' in line:
                        analysis_results['exports'].append(line.strip())
            
            return {
                'binary_file': binary_file,
                'analysis_type': analysis_type,
                'analysis_results': analysis_results,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Analysis timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500

@tools_ns.route('/gdb')
class GDBAnalysis(Resource):
    @tools_ns.expect(command_request_model)
    @tools_ns.response(200, 'Success')
    @tools_ns.response(400, 'Bad Request', error_response_model)
    @tools_ns.response(500, 'Internal Server Error', error_response_model)
    def post(self):
        '''執行 GDB 調試分析'''
        try:
            data = request.get_json()
            binary_file = data.get('binary_file')
            analysis_type = data.get('analysis_type', 'basic')
            
            if not binary_file:
                return {'success': False, 'error': 'Binary file is required'}, 400
            
            start_time = time.time()
            
            # 構建 GDB 命令
            cmd = f"gdb -batch -ex 'file {binary_file}' -ex 'info functions' -ex 'info variables' -ex 'quit'"
            
            # 執行分析
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            
            execution_time = time.time() - start_time
            
            # 解析結果
            analysis_results = {
                'functions': [],
                'variables': [],
                'segments': [],
                'symbols': []
            }
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if '0x' in line and 'function' in line.lower():
                        analysis_results['functions'].append(line.strip())
                    elif 'variable' in line.lower():
                        analysis_results['variables'].append(line.strip())
                    elif 'segment' in line.lower():
                        analysis_results['segments'].append(line.strip())
                    elif 'symbol' in line.lower():
                        analysis_results['symbols'].append(line.strip())
            
            return {
                'binary_file': binary_file,
                'analysis_type': analysis_type,
                'analysis_results': analysis_results,
                'execution_time': round(execution_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Analysis timeout'}, 408
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
