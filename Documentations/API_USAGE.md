# HexStrike AI - API Usage Documentation

## Overview

HexStrike AI provides a comprehensive REST API for security testing and penetration testing automation. This document covers all available endpoints, authentication, and usage examples.

**Base URL**: `https://hexstrike-ai-v6-0.onrender.com`

## Quick Start

### Health Check
```bash
curl https://hexstrike-ai-v6-0.onrender.com/health
```

### Basic Nmap Scan
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{"target": "scanme.nmap.org", "scan_type": "quick"}'
```

## Core System Endpoints

### Health Check
**GET** `/health`

Returns server health status and available tools.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T12:00:00Z",
  "version": "6.0",
  "available_tools": 150,
  "processes": {
    "active": 3,
    "total": 10
  }
}
```

### Server Telemetry
**GET** `/api/telemetry`

Get system performance metrics.

**Response:**
```json
{
  "cpu_usage": 45.2,
  "memory_usage": 67.8,
  "disk_usage": 23.1,
  "active_processes": 3,
  "cache_hits": 1250,
  "cache_misses": 89
}
```

## Network Security Tools

### Nmap Scanning
**POST** `/api/tools/nmap`

Perform network port scanning and service detection.

**Parameters:**
```json
{
  "target": "scanme.nmap.org",
  "scan_type": "quick|comprehensive|stealth",
  "ports": "1-1000",
  "timing": "T4",
  "scripts": ["default", "vuln", "safe"]
}
```

**Example:**
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "scanme.nmap.org",
    "scan_type": "quick",
    "ports": "1-1000"
  }'
```

### Rustscan (Ultra-fast scanning)
**POST** `/api/tools/rustscan`

High-speed port scanning with intelligent rate limiting.

**Parameters:**
```json
{
  "target": "192.168.1.1/24",
  "ports": "1-65535",
  "timeout": 1000,
  "batch_size": 1000
}
```

### Masscan (Internet-scale scanning)
**POST** `/api/tools/masscan`

High-speed Internet-scale port scanning.

**Parameters:**
```json
{
  "target": "10.0.0.0/8",
  "ports": "22,80,443,8080",
  "rate": 1000
}
```

### AutoRecon (Comprehensive reconnaissance)
**POST** `/api/tools/autorecon`

Automated reconnaissance with 35+ parameters.

**Parameters:**
```json
{
  "target": "example.com",
  "threads": 10,
  "timeout": 300,
  "modules": ["nmap", "gobuster", "nikto"]
}
```

## Web Application Security Tools

### Gobuster (Directory enumeration)
**POST** `/api/tools/gobuster`

Directory, file, and DNS enumeration.

**Parameters:**
```json
{
  "target": "https://example.com",
  "wordlist": "common|big|small",
  "extensions": "php,html,txt",
  "threads": 50,
  "timeout": 10
}
```

**Example:**
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com",
    "wordlist": "common",
    "extensions": "php,html,txt"
  }'
```

### Feroxbuster (Recursive content discovery)
**POST** `/api/tools/feroxbuster`

Recursive content discovery with intelligent filtering.

**Parameters:**
```json
{
  "target": "https://example.com",
  "wordlist": "common",
  "extensions": "php,html,js",
  "depth": 3,
  "threads": 50
}
```

### Nuclei (Vulnerability scanning)
**POST** `/api/tools/nuclei`

Fast vulnerability scanner with 4000+ templates.

**Parameters:**
```json
{
  "target": "https://example.com",
  "templates": "common-vulnerabilities|exposures|misconfiguration",
  "severity": "critical,high,medium",
  "tags": "xss,sqli,lfi"
}
```

### Nikto (Web server vulnerability scanner)
**POST** `/api/tools/nikto`

Comprehensive web server vulnerability scanner.

**Parameters:**
```json
{
  "target": "https://example.com",
  "format": "json|html|txt",
  "timeout": 300
}
```

### SQLMap (SQL injection testing)
**POST** `/api/tools/sqlmap`

Advanced automatic SQL injection testing.

**Parameters:**
```json
{
  "target": "https://example.com/login.php",
  "method": "POST",
  "data": "user=admin&pass=admin",
  "level": 3,
  "risk": 2
}
```

### WPScan (WordPress security scanner)
**POST** `/api/tools/wpscan`

WordPress security scanner with vulnerability database.

**Parameters:**
```json
{
  "target": "https://example.com",
  "enumerate": "users,plugins,themes",
  "api_token": "your_api_token"
}
```

## Authentication & Password Security

### Hydra (Network login cracker)
**POST** `/api/tools/hydra`

Network login cracker supporting 50+ protocols.

**Parameters:**
```json
{
  "target": "192.168.1.100",
  "service": "ssh|ftp|http|smb",
  "userlist": "admin,root,user",
  "passlist": "password,123456,admin",
  "threads": 16
}
```

### John the Ripper (Password cracker)
**POST** `/api/tools/john`

Advanced password hash cracking.

**Parameters:**
```json
{
  "hash_file": "/path/to/hashes.txt",
  "wordlist": "rockyou.txt",
  "rules": "single,wordlist",
  "format": "auto"
}
```

### Hashcat (GPU-accelerated cracking)
**POST** `/api/tools/hashcat`

World's fastest password recovery tool.

**Parameters:**
```json
{
  "hash_file": "/path/to/hashes.txt",
  "attack_mode": "dictionary|bruteforce|hybrid",
  "wordlist": "rockyou.txt",
  "rules": "best64.rule"
}
```

## Binary Analysis & Reverse Engineering

### Ghidra (Software reverse engineering)
**POST** `/api/tools/ghidra`

NSA's software reverse engineering suite.

**Parameters:**
```json
{
  "binary_file": "/path/to/binary",
  "analysis_type": "basic|advanced|full",
  "output_format": "json|xml"
}
```

### Radare2 (Advanced reverse engineering)
**POST** `/api/tools/radare2`

Advanced reverse engineering framework.

**Parameters:**
```json
{
  "binary_file": "/path/to/binary",
  "commands": ["aaa", "afl", "pdf @main"],
  "output_format": "json"
}
```

### GDB (GNU Debugger)
**POST** `/api/tools/gdb`

GNU Debugger with Python scripting.

**Parameters:**
```json
{
  "binary_file": "/path/to/binary",
  "script": "gdb_script.py",
  "breakpoints": ["main", "0x401000"],
  "commands": ["run", "info registers"]
}
```

## Cloud & Container Security

### Prowler (Cloud security assessment)
**POST** `/api/tools/prowler`

AWS/Azure/GCP security assessment.

**Parameters:**
```json
{
  "provider": "aws|azure|gcp",
  "region": "us-east-1",
  "checks": "all|cis|pci",
  "output_format": "json"
}
```

### Trivy (Container vulnerability scanner)
**POST** `/api/tools/trivy`

Comprehensive vulnerability scanner for containers.

**Parameters:**
```json
{
  "target": "image:latest|registry.io/image:tag",
  "scan_type": "vulnerability|config|secret",
  "severity": "CRITICAL,HIGH,MEDIUM"
}
```

### Kube-Hunter (Kubernetes penetration testing)
**POST** `/api/tools/kube-hunter`

Kubernetes penetration testing tool.

**Parameters:**
```json
{
  "mode": "passive|active",
  "remote": "cluster_endpoint",
  "quick": true
}
```

## AI Intelligence Endpoints

### Target Analysis
**POST** `/api/intelligence/analyze-target`

AI-powered target analysis and reconnaissance planning.

**Parameters:**
```json
{
  "target": "example.com",
  "analysis_type": "comprehensive|quick|focused",
  "include_subdomains": true,
  "deep_scan": false
}
```

**Example:**
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "analysis_type": "comprehensive"
  }'
```

### Tool Selection
**POST** `/api/intelligence/select-tools`

AI-driven tool selection based on target analysis.

**Parameters:**
```json
{
  "target": "example.com",
  "target_type": "web|network|binary",
  "scan_depth": "shallow|medium|deep",
  "time_constraint": 3600
}
```

### Parameter Optimization
**POST** `/api/intelligence/optimize-parameters`

Context-aware parameter optimization for tools.

**Parameters:**
```json
{
  "tool": "nmap",
  "target": "example.com",
  "scan_type": "comprehensive",
  "timeout": 300
}
```

## Process Management

### List Processes
**GET** `/api/processes/list`

List all active processes.

**Response:**
```json
{
  "processes": [
    {
      "pid": 1234,
      "command": "nmap -sS example.com",
      "status": "running",
      "start_time": "2025-10-23T12:00:00Z",
      "cpu_usage": 15.5,
      "memory_usage": 128.7
    }
  ]
}
```

### Process Status
**GET** `/api/processes/status/<pid>`

Get detailed process information.

**Response:**
```json
{
  "pid": 1234,
  "command": "nmap -sS example.com",
  "status": "running",
  "start_time": "2025-10-23T12:00:00Z",
  "cpu_usage": 15.5,
  "memory_usage": 128.7,
  "output": "Starting Nmap scan...",
  "progress": 45.2
}
```

### Terminate Process
**POST** `/api/processes/terminate/<pid>`

Terminate a specific process.

**Response:**
```json
{
  "success": true,
  "message": "Process terminated successfully"
}
```

### Process Dashboard
**GET** `/api/processes/dashboard`

Live monitoring dashboard for all processes.

**Response:**
```json
{
  "total_processes": 10,
  "active_processes": 3,
  "completed_processes": 7,
  "system_load": 45.2,
  "memory_usage": 67.8,
  "processes": [...]
}
```

## Bug Bounty Workflows

### Reconnaissance Workflow
**POST** `/api/bugbounty/reconnaissance-workflow`

Comprehensive reconnaissance for bug bounty programs.

**Parameters:**
```json
{
  "target": "example.com",
  "scope": "*.example.com",
  "subdomain_enumeration": true,
  "port_scanning": true,
  "web_enumeration": true,
  "technology_detection": true
}
```

### Vulnerability Hunting Workflow
**POST** `/api/bugbounty/vulnerability-hunting-workflow`

Automated vulnerability hunting workflow.

**Parameters:**
```json
{
  "target": "https://example.com",
  "scan_types": ["xss", "sqli", "lfi", "rfi"],
  "depth": "medium",
  "custom_payloads": true
}
```

### Business Logic Testing
**POST** `/api/bugbounty/business-logic-workflow`

Business logic vulnerability testing.

**Parameters:**
```json
{
  "target": "https://example.com",
  "workflows": ["registration", "login", "payment"],
  "test_cases": ["race_conditions", "parameter_pollution"]
}
```

## CTF Tools

### CTF Challenge Solver
**POST** `/api/ctf/auto-solve-challenge`

Automated CTF challenge solving.

**Parameters:**
```json
{
  "challenge_type": "crypto|forensics|binary|web|misc",
  "challenge_data": "base64_encoded_data",
  "hints": ["hint1", "hint2"]
}
```

### Cryptography Solver
**POST** `/api/ctf/cryptography-solver`

Advanced cryptography challenge solver.

**Parameters:**
```json
{
  "cipher_type": "caesar|vigenere|rsa|aes",
  "ciphertext": "encrypted_text",
  "key_hint": "optional_key_hint"
}
```

### Forensics Analyzer
**POST** `/api/ctf/forensics-analyzer`

Digital forensics analysis for CTF challenges.

**Parameters:**
```json
{
  "file_path": "/path/to/forensics_file",
  "analysis_type": "image|memory|disk|network",
  "extract_artifacts": true
}
```

## Error Handling

### Error Statistics
**GET** `/api/error-handling/statistics`

Get error handling statistics and metrics.

**Response:**
```json
{
  "total_errors": 45,
  "error_types": {
    "timeout": 15,
    "connection_failed": 12,
    "permission_denied": 8,
    "invalid_parameters": 10
  },
  "recovery_rate": 87.5,
  "last_error": "2025-10-23T12:00:00Z"
}
```

### Execute with Recovery
**POST** `/api/error-handling/execute-with-recovery`

Execute command with automatic error recovery.

**Parameters:**
```json
{
  "command": "nmap -sS example.com",
  "max_retries": 3,
  "timeout": 300,
  "fallback_commands": ["nmap -sT example.com"]
}
```

## File Operations

### Create File
**POST** `/api/files/create`

Create files for storing results and configurations.

**Parameters:**
```json
{
  "file_path": "/path/to/file.txt",
  "content": "file content",
  "permissions": "644"
}
```

### Modify File
**POST** `/api/files/modify`

Modify existing files.

**Parameters:**
```json
{
  "file_path": "/path/to/file.txt",
  "content": "new content",
  "append": false
}
```

### Delete File
**DELETE** `/api/files/delete`

Delete files.

**Parameters:**
```json
{
  "file_path": "/path/to/file.txt"
}
```

### List Files
**GET** `/api/files/list`

List files in a directory.

**Parameters:**
```json
{
  "directory": "/path/to/directory",
  "pattern": "*.txt",
  "recursive": false
}
```

## Cache Management

### Cache Statistics
**GET** `/api/cache/stats`

Get cache performance statistics.

**Response:**
```json
{
  "cache_size": 1000,
  "cache_usage": 750,
  "hit_rate": 85.5,
  "miss_rate": 14.5,
  "evictions": 23
}
```

### Clear Cache
**POST** `/api/cache/clear`

Clear the result cache.

**Response:**
```json
{
  "success": true,
  "message": "Cache cleared successfully",
  "cleared_entries": 750
}
```

## Python Client Examples

### Basic Client
```python
import requests
import json

class HexStrikeClient:
    def __init__(self, base_url="https://hexstrike-ai-v6-0.onrender.com"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        response = self.session.get(f"{self.base_url}/health")
        return response.json()
    
    def nmap_scan(self, target, scan_type="quick"):
        payload = {
            "target": target,
            "scan_type": scan_type,
            "ports": "1-1000"
        }
        response = self.session.post(
            f"{self.base_url}/api/tools/nmap",
            json=payload
        )
        return response.json()
    
    def analyze_target(self, target, analysis_type="comprehensive"):
        payload = {
            "target": target,
            "analysis_type": analysis_type
        }
        response = self.session.post(
            f"{self.base_url}/api/intelligence/analyze-target",
            json=payload
        )
        return response.json()

# Usage
client = HexStrikeClient()
health = client.health_check()
print(f"Server Status: {health['status']}")

# Run nmap scan
scan_result = client.nmap_scan("scanme.nmap.org")
print(f"Scan Result: {scan_result}")

# AI target analysis
analysis = client.analyze_target("example.com")
print(f"Analysis: {analysis}")
```

### Advanced Client with Error Handling
```python
import requests
import time
from typing import Dict, Any, Optional

class AdvancedHexStrikeClient:
    def __init__(self, base_url="https://hexstrike-ai-v6-0.onrender.com", timeout=300):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HexStrike-Python-Client/1.0'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {"error": "Request timeout", "success": False}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection error", "success": False}
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP error: {e}", "success": False}
        except Exception as e:
            return {"error": f"Unexpected error: {e}", "success": False}
    
    def execute_with_recovery(self, command: str, max_retries: int = 3) -> Dict[str, Any]:
        """Execute command with automatic error recovery"""
        payload = {
            "command": command,
            "max_retries": max_retries,
            "timeout": self.timeout,
            "fallback_commands": []
        }
        return self._make_request("POST", "/api/error-handling/execute-with-recovery", json=payload)
    
    def get_process_status(self, pid: int) -> Dict[str, Any]:
        """Get process status"""
        return self._make_request("GET", f"/api/processes/status/{pid}")
    
    def terminate_process(self, pid: int) -> Dict[str, Any]:
        """Terminate process"""
        return self._make_request("POST", f"/api/processes/terminate/{pid}")

# Usage
client = AdvancedHexStrikeClient()

# Execute with recovery
result = client.execute_with_recovery("nmap -sS example.com")
print(f"Execution result: {result}")

# Monitor process
status = client.get_process_status(1234)
print(f"Process status: {status}")
```

## JavaScript/Node.js Client Examples

### Basic Node.js Client
```javascript
const axios = require('axios');

class HexStrikeClient {
    constructor(baseUrl = 'https://hexstrike-ai-v6-0.onrender.com') {
        this.baseUrl = baseUrl;
        this.client = axios.create({
            baseURL: baseUrl,
            timeout: 300000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
    
    async healthCheck() {
        try {
            const response = await this.client.get('/health');
            return response.data;
        } catch (error) {
            throw new Error(`Health check failed: ${error.message}`);
        }
    }
    
    async nmapScan(target, scanType = 'quick') {
        try {
            const payload = {
                target: target,
                scan_type: scanType,
                ports: '1-1000'
            };
            const response = await this.client.post('/api/tools/nmap', payload);
            return response.data;
        } catch (error) {
            throw new Error(`Nmap scan failed: ${error.message}`);
        }
    }
    
    async analyzeTarget(target, analysisType = 'comprehensive') {
        try {
            const payload = {
                target: target,
                analysis_type: analysisType
            };
            const response = await this.client.post('/api/intelligence/analyze-target', payload);
            return response.data;
        } catch (error) {
            throw new Error(`Target analysis failed: ${error.message}`);
        }
    }
}

// Usage
async function main() {
    const client = new HexStrikeClient();
    
    try {
        // Health check
        const health = await client.healthCheck();
        console.log('Server Status:', health.status);
        
        // Run nmap scan
        const scanResult = await client.nmapScan('scanme.nmap.org');
        console.log('Scan Result:', scanResult);
        
        // AI target analysis
        const analysis = await client.analyzeTarget('example.com');
        console.log('Analysis:', analysis);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
```

## Rate Limiting and Best Practices

### Rate Limiting
- Default rate limit: 100 requests per minute per IP
- Burst limit: 20 requests per second
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`: Maximum requests per window
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Time when rate limit resets

### Best Practices

1. **Always check server health** before running intensive scans
2. **Use appropriate timeouts** for long-running operations
3. **Monitor process status** for long-running scans
4. **Implement error handling** and retry logic
5. **Respect rate limits** to avoid being throttled
6. **Use AI intelligence endpoints** for optimal tool selection
7. **Cache results** when possible to avoid redundant requests
8. **Clean up processes** when no longer needed

### Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Endpoint not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable - Server overloaded |

## Security Considerations

⚠️ **Important Security Notes**:

- This API provides powerful security testing capabilities
- Only use for authorized penetration testing
- Ensure proper authorization before testing any targets
- Monitor API usage and implement proper access controls
- Consider implementing authentication for production deployments
- Be aware of legal and ethical implications of security testing

## Support and Documentation

- **GitHub Repository**: [https://github.com/0x4m4/hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)
- **Discord Community**: [https://discord.gg/BWnmrrSHbA](https://discord.gg/BWnmrrSHbA)
- **Documentation**: [README.md](README.md)
- **Issue Tracker**: [GitHub Issues](https://github.com/0x4m4/hexstrike-ai/issues)

---

**Made with ❤️ by the cybersecurity community for AI-powered security automation**

*HexStrike AI v6.0 - Where artificial intelligence meets cybersecurity excellence*
