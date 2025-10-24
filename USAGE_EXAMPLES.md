# HexStrike AI - Usage Examples

## Overview

This document provides practical examples for using HexStrike AI through all three methods: Web UI, Direct API, and AI Client Integration.

## Method 1: Web Interface Usage

### Accessing the Dashboard

1. Navigate to: `https://hexstrike-ai-v6-0.onrender.com`
2. You'll see the blood-red themed HexStrike AI dashboard
3. Monitor server status and available tools

### Quick Actions

#### Health Check
- Click the "Health Check" button
- View real-time server status and tool availability

#### Nmap Scan Demo
- Click "Nmap Scan" button
- Follow the modal instructions
- Use the API testing interface to execute

#### Web Application Scan
- Click "Web Scan" button
- Select appropriate endpoint (Gobuster, Nuclei, etc.)
- Enter target URL and execute

### API Testing Interface

1. **Select Endpoint**: Choose from dropdown (Health, Nmap, Gobuster, etc.)
2. **Enter Target**: Input your target (e.g., `scanme.nmap.org`)
3. **Execute**: Click "Execute" to run the command
4. **View Results**: See real-time output in the results panel

### Example Workflow

```
1. Check server health
2. Select "Nmap Scan" endpoint
3. Enter target: "scanme.nmap.org"
4. Click "Execute"
5. Review scan results
6. Select "Gobuster Scan" for web enumeration
7. Enter web target: "https://example.com"
8. Execute and review directory enumeration results
```

## Method 2: Direct API Usage

### Basic Health Check

```bash
curl https://hexstrike-ai-v6-0.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T12:00:00Z",
  "version": "6.0",
  "available_tools": 150
}
```

### Network Scanning Examples

#### Quick Nmap Scan
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "scanme.nmap.org",
    "scan_type": "quick",
    "ports": "1-1000"
  }'
```

#### Comprehensive Nmap Scan
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "scan_type": "comprehensive",
    "ports": "1-65535",
    "scripts": ["default", "vuln", "safe"]
  }'
```

#### Ultra-fast Rustscan
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/rustscan \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.1/24",
    "ports": "1-65535",
    "timeout": 1000
  }'
```

### Web Application Security Examples

#### Directory Enumeration with Gobuster
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com",
    "wordlist": "common",
    "extensions": "php,html,txt,js",
    "threads": 50
  }'
```

#### Vulnerability Scanning with Nuclei
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nuclei \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com",
    "templates": "common-vulnerabilities",
    "severity": "critical,high,medium"
  }'
```

#### Web Server Vulnerability Scan
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nikto \
  -theme
```

#### SQL Injection Testing
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/sqlmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com/login.php",
    "method": "POST",
    "data": "user=admin&pass=admin",
    "level": 3,
    "risk": 2
  }'
```

### AI-Powered Intelligence Examples

#### Target Analysis
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "analysis_type": "comprehensive",
    "include_subdomains": true
  }'
```

#### Intelligent Tool Selection
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/intelligence/select-tools \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "target_type": "web",
    "scan_depth": "deep",
    "time_constraint": 3600
  }'
```

### Bug Bounty Workflow Examples

#### Reconnaissance Workflow
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/bugbounty/reconnaissance-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "scope": "*.example.com",
    "subdomain_enumeration": true,
    "port_scanning": true,
    "web_enumeration": true
  }'
```

#### Vulnerability Hunting Workflow
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/bugbounty/vulnerability-hunting-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com",
    "scan_types": ["xss", "sqli", "lfi", "rfi"],
    "depth": "medium"
  }'
```

### Process Management Examples

#### List Active Processes
```bash
curl https://hexstrike-ai-v6-0.onrender.com/api/processes/list
```

#### Get Process Status
```bash
curl https://hexstrike-ai-v6-0.onrender.com/api/processes/status/1234
```

#### Terminate Process
```bash
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/processes/terminate/1234
```

## Method 3: AI Client Integration

### Claude Desktop Examples

#### Basic Security Testing
```
I'm a security researcher authorized to test my company's website example.com. I have written permission from the IT security team. Please use hexstrike AI tools to perform a comprehensive security assessment including port scanning, web vulnerability scanning, and AI-powered target analysis.
```

#### Network Reconnaissance
```
I'm conducting authorized penetration testing on our internal network 192.168.1.0/24. Please use hexstrike tools to perform network reconnaissance including nmap scanning, service enumeration, and vulnerability assessment. I have proper authorization for this testing.
```

#### Web Application Testing
```
I'm testing our web application at https://myapp.com for security vulnerabilities. Please use hexstrike AI tools to perform comprehensive web application security testing including directory enumeration, vulnerability scanning, and AI analysis. This is authorized testing on our own infrastructure.
```

### Cursor Examples

#### Bug Bounty Hunting
```
I'm participating in a bug bounty program for target.com. I have authorization to test within the program scope. Please use hexstrike AI tools to perform reconnaissance, subdomain enumeration, and vulnerability hunting following bug bounty best practices.
```

#### CTF Challenge Solving
```
I'm working on a CTF challenge. The target is challenge.ctf.com. Please use hexstrike AI tools to analyze the target and suggest the best approach for solving this challenge.
```

#### Red Team Exercise
```
I'm conducting a red team exercise with proper authorization. The target is our internal network 10.0.0.0/8. Please use hexstrike AI tools to perform comprehensive penetration testing including network scanning, service enumeration, and vulnerability exploitation.
```

### VS Code Copilot Examples

#### Security Research
```
I'm conducting security research on my own lab environment. The target is lab.example.com. Please use hexstrike AI tools to perform security assessment and provide detailed analysis of the findings.
```

#### Compliance Testing
```
I'm performing compliance testing for our organization. Please use hexstrike AI tools to scan our systems for common vulnerabilities and security misconfigurations. This is authorized testing on our own infrastructure.
```

## Python Client Examples

### Basic Python Client

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

# Usage Example
client = HexStrikeClient()

# Check server health
health = client.health_check()
print(f"Server Status: {health['status']}")

# Run nmap scan
scan_result = client.nmap_scan("scanme.nmap.org")
print(f"Scan Result: {scan_result}")

# AI target analysis
analysis = client.analyze_target("example.com")
print(f"Analysis: {analysis}")
```

### Advanced Python Client with Error Handling

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
    
    def comprehensive_security_assessment(self, target: str) -> Dict[str, Any]:
        """Perform comprehensive security assessment"""
        results = {
            "target": target,
            "health_check": None,
            "nmap_scan": None,
            "web_scan": None,
            "ai_analysis": None,
            "errors": []
        }
        
        # Health check
        print(f"Checking server health...")
        results["health_check"] = self._make_request("GET", "/health")
        
        # Nmap scan
        print(f"Running nmap scan on {target}...")
        nmap_payload = {
            "target": target,
            "scan_type": "comprehensive",
            "ports": "1-1000"
        }
        results["nmap_scan"] = self._make_request("POST", "/api/tools/nmap", json=nmap_payload)
        
        # Web scan (if target is a web application)
        if target.startswith("http"):
            print(f"Running web vulnerability scan on {target}...")
            web_payload = {
                "target": target,
                "templates": "common-vulnerabilities",
                "severity": "critical,high,medium"
            }
            results["web_scan"] = self._make_request("POST", "/api/tools/nuclei", json=web_payload)
        
        # AI analysis
        print(f"Running AI target analysis on {target}...")
        ai_payload = {
            "target": target,
            "analysis_type": "comprehensive"
        }
        results["ai_analysis"] = self._make_request("POST", "/api/intelligence/analyze-target", json=ai_payload)
        
        return results

# Usage Example
client = AdvancedHexStrikeClient()

# Perform comprehensive assessment
results = client.comprehensive_security_assessment("scanme.nmap.org")
print(json.dumps(results, indent=2))
```

## JavaScript/Node.js Examples

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

## Real-World Workflow Examples

### Complete Penetration Testing Workflow

#### 1. Reconnaissance Phase
```bash
# Target analysis
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "analysis_type": "comprehensive"}'

# Subdomain enumeration
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/amass \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "enum_type": "subdomains"}'

# Port scanning
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "scan_type": "comprehensive"}'
```

#### 2. Vulnerability Assessment Phase
```bash
# Web vulnerability scanning
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nuclei \
  -H "Content-Type: application/json" \
  -d '{"target": "https://example.com", "templates": "common-vulnerabilities"}'

# Directory enumeration
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d '{"target": "https://example.com", "wordlist": "common"}'

# SQL injection testing
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/sqlmap \
  -H "Content-Type: application/json" \
  -d '{"target": "https://example.com/login.php", "method": "POST"}'
```

#### 3. Exploitation Phase
```bash
# Password cracking
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/hydra \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "service": "ssh", "userlist": "admin,root"}'

# Hash cracking
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/hashcat \
  -H "Content-Type: application/json" \
  -d '{"hash_file": "/path/to/hashes.txt", "attack_mode": "dictionary"}'
```

### Bug Bounty Workflow

#### 1. Initial Reconnaissance
```bash
# Bug bounty reconnaissance workflow
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/bugbounty/reconnaissance-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "scope": "*.example.com",
    "subdomain_enumeration": true,
    "port_scanning": true,
    "web_enumeration": true
  }'
```

#### 2. Vulnerability Hunting
```bash
# Vulnerability hunting workflow
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/bugbounty/vulnerability-hunting-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com",
    "scan_types": ["xss", "sqli", "lfi", "rfi"],
    "depth": "medium"
  }'
```

### CTF Challenge Workflow

#### 1. Challenge Analysis
```bash
# CTF challenge solver
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/ctf/auto-solve-challenge \
  -H "Content-Type: application/json" \
  -d '{
    "challenge_type": "web",
    "challenge_data": "base64_encoded_data",
    "hints": ["hint1", "hint2"]
  }'
```

#### 2. Cryptography Challenges
```bash
# Cryptography solver
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/ctf/cryptography-solver \
  -H "Content-Type: application/json" \
  -d '{
    "cipher_type": "caesar",
    "ciphertext": "encrypted_text",
    "key_hint": "optional_key_hint"
  }'
```

## Best Practices

### 1. Always Include Authorization
```
I'm a security researcher authorized to test my company's website example.com. I have written permission from the IT security team. Please use hexstrike AI tools to perform security testing.
```

### 2. Use Appropriate Scope
- Specify the exact scope of testing
- Include subdomain enumeration if needed
- Define the depth of scanning

### 3. Monitor Resource Usage
- Check server health before intensive scans
- Monitor process status for long-running operations
- Use appropriate timeouts

### 4. Implement Error Handling
- Always check for errors in responses
- Implement retry logic for failed requests
- Use the error recovery endpoints when available

### 5. Respect Rate Limits
- Don't overwhelm the server with requests
- Use appropriate delays between requests
- Monitor rate limit headers

## Troubleshooting Common Issues

### Server Not Responding
```bash
# Check server health
curl https://hexstrike-ai-v6-0.onrender.com/health

# Check process status
curl https://hexstrike-ai-v6-0.onrender.com/api/processes/list
```

### Connection Timeouts
```bash
# Use shorter timeouts for quick tests
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{"target": "scanme.nmap.org", "scan_type": "quick"}'
```

### Rate Limiting
```bash
# Check rate limit headers
curl -I https://hexstrike-ai-v6-0.onrender.com/health
```

---

**Ready to use HexStrike AI?** 🚀

*Choose your preferred method and start conducting authorized security testing today!*
