# Practical Scenarios - HexStrike AI

This document provides real-world scenarios and workflows for using HexStrike AI security tools effectively.

## Table of Contents

1. [Bug Bounty Workflows](#bug-bounty-workflows)
2. [CTF Competition Scenarios](#ctf-competition-scenarios)
3. [Red Team Exercises](#red-team-exercises)
4. [Vulnerability Assessment](#vulnerability-assessment)
5. [Incident Response](#incident-response)

---

## Bug Bounty Workflows

### Scenario 1: Web Application Assessment

**Objective**: Perform a comprehensive web application security assessment for a bug bounty program.

#### Phase 1: Reconnaissance
```bash
# 1. Subdomain enumeration
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://target.com",
    "mode": "dns",
    "wordlist": "subdomains.txt"
  }'

# 2. Port scanning on discovered subdomains
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "api.target.com",
    "scan_type": "comprehensive",
    "ports": "1-65535"
  }'
```

#### Phase 2: Directory Enumeration
```bash
# 3. Directory brute-forcing
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://target.com",
    "mode": "dir",
    "wordlist": "common.txt",
    "extensions": ["php", "html", "txt", "js"]
  }'
```

#### Phase 3: Vulnerability Scanning
```bash
# 4. Vulnerability scanning with Nuclei
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nuclei \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://target.com",
    "templates": "vulnerability,exposure,misconfiguration",
    "severity": "critical,high,medium"
  }'
```

#### Phase 4: Manual Testing
```bash
# 5. SQL injection testing
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/sqlmap \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://target.com/login.php",
    "data": "username=admin&password=test",
    "techniques": "B,E,U,Q,S,T"
  }'
```

### Scenario 2: API Security Assessment

**Objective**: Assess API security for a modern web application.

#### API Discovery and Testing
```bash
# 1. API endpoint discovery
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://api.target.com",
    "mode": "dir",
    "wordlist": "api-endpoints.txt",
    "extensions": ["json", "xml"]
  }'

# 2. API vulnerability scanning
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nuclei \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://api.target.com",
    "templates": "api,swagger,graphql"
  }'
```

---

## CTF Competition Scenarios

### Scenario 1: Binary Analysis Challenge

**Objective**: Analyze a binary file to find the flag.

#### Phase 1: Initial Analysis
```bash
# 1. File analysis
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/radare2 \
  -H "Content-Type: application/json" \
  -d '{
    "file": "challenge.bin",
    "command": "aa; pdf @ main"
  }'

# 2. String extraction
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/radare2 \
  -H "Content-Type: application/json" \
  -d '{
    "file": "challenge.bin",
    "command": "iz"
  }'
```

#### Phase 2: Dynamic Analysis
```bash
# 3. GDB debugging
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gdb \
  -H "Content-Type: application/json" \
  -d '{
    "file": "challenge.bin",
    "commands": [
      "break main",
      "run",
      "info registers",
      "x/20s $rsp"
    ]
  }'
```

### Scenario 2: Web Application Challenge

**Objective**: Exploit a web application vulnerability to obtain the flag.

#### Phase 1: Reconnaissance
```bash
# 1. Directory enumeration
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://ctf.target.com",
    "mode": "dir",
    "wordlist": "ctf-wordlist.txt"
  }'
```

#### Phase 2: Vulnerability Exploitation
```bash
# 2. SQL injection
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/sqlmap \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://ctf.target.com/login.php",
    "data": "id=1",
    "techniques": "B",
    "dbs": true
  }'
```

---

## Red Team Exercises

### Scenario 1: Internal Network Penetration

**Objective**: Gain access to internal network resources.

#### Phase 1: Network Discovery
```bash
# 1. Network scanning
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.0/24",
    "scan_type": "comprehensive",
    "ports": "1-65535"
  }'

# 2. Service enumeration
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.100",
    "scan_type": "service_detection",
    "scripts": true
  }'
```

#### Phase 2: Credential Attacks
```bash
# 3. Password cracking
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/hydra \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.100",
    "service": "ssh",
    "username": "admin",
    "wordlist": "passwords.txt",
    "threads": 16
  }'
```

#### Phase 3: Lateral Movement
```bash
# 4. Hash cracking
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/john \
  -H "Content-Type: application/json" \
  -d '{
    "hash_file": "hashes.txt",
    "wordlist": "rockyou.txt",
    "format": "nt"
  }'
```

---

## Vulnerability Assessment

### Scenario 1: Web Application Security Assessment

**Objective**: Perform a comprehensive vulnerability assessment of a web application.

#### Phase 1: Automated Scanning
```bash
# 1. Web vulnerability scanning
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nikto \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://target.com",
    "options": {
      "host": "target.com",
      "port": 443,
      "ssl": true
    }
  }'

# 2. Nuclei vulnerability scanning
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nuclei \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://target.com",
    "templates": "vulnerability,exposure,misconfiguration",
    "severity": "critical,high,medium,low"
  }'
```

#### Phase 2: Manual Testing
```bash
# 3. SQL injection testing
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/sqlmap \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://target.com/search.php",
    "data": "query=test",
    "techniques": "B,E,U,Q,S,T"
  }'
```

### Scenario 2: Cloud Security Assessment

**Objective**: Assess cloud infrastructure security.

#### Cloud Security Scanning
```bash
# 1. AWS security assessment
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/prowler \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "aws",
    "checks": "all",
    "output": "json"
  }'

# 2. Container vulnerability scanning
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/trivy \
  -H "Content-Type: application/json" \
  -d '{
    "target": "nginx:latest",
    "format": "json",
    "severity": "CRITICAL,HIGH,MEDIUM"
  }'
```

---

## Incident Response

### Scenario 1: Malware Analysis

**Objective**: Analyze a suspicious binary file.

#### Phase 1: Static Analysis
```bash
# 1. Binary analysis with Ghidra
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/ghidra \
  -H "Content-Type: application/json" \
  -d '{
    "file": "suspicious.bin",
    "analysis": {
      "auto_analyze": true,
      "decompile": true,
      "strings": true
    }
  }'

# 2. Radare2 analysis
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/radare2 \
  -H "Content-Type: application/json" \
  -d '{
    "file": "suspicious.bin",
    "command": "aa; pdf @ main; iz"
  }'
```

#### Phase 2: Dynamic Analysis
```bash
# 3. GDB debugging
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gdb \
  -H "Content-Type: application/json" \
  -d '{
    "file": "suspicious.bin",
    "commands": [
      "set environment LD_PRELOAD=/lib/x86_64-linux-gnu/libc.so.6",
      "run",
      "info proc mappings"
    ]
  }'
```

---

## Best Practices

### 1. Reconnaissance
- Start with passive reconnaissance
- Use multiple tools for comprehensive coverage
- Document all findings

### 2. Scanning
- Use appropriate scan timing
- Respect target systems
- Implement rate limiting

### 3. Exploitation
- Follow responsible disclosure
- Document exploitation steps
- Provide remediation recommendations

### 4. Reporting
- Create detailed reports
- Include proof-of-concept code
- Provide remediation steps

## Tools Integration

### Workflow Automation
```bash
# Automated workflow example
#!/bin/bash

TARGET="target.com"

# Phase 1: Reconnaissance
echo "Starting reconnaissance..."
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://$TARGET\", \"mode\": \"dns\", \"wordlist\": \"subdomains.txt\"}"

# Phase 2: Port Scanning
echo "Starting port scanning..."
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d "{\"target\": \"$TARGET\", \"scan_type\": \"comprehensive\"}"

# Phase 3: Vulnerability Scanning
echo "Starting vulnerability scanning..."
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nuclei \
  -H "Content-Type: application/json" \
  -d "{\"target\": \"https://$TARGET\", \"templates\": \"vulnerability\"}"
```

## Conclusion

These scenarios provide practical examples of how to use HexStrike AI tools effectively in real-world situations. Always remember to:

1. **Follow legal and ethical guidelines**
2. **Document all activities**
3. **Use appropriate tools for the situation**
4. **Respect target systems**
5. **Follow responsible disclosure practices**
