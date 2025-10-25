# Nmap Guide

## Overview

Nmap (Network Mapper) is a powerful network discovery and security auditing tool. It's designed to rapidly scan large networks and single hosts to discover services and vulnerabilities.

## Features

- Host discovery
- Port scanning
- Service version detection
- OS detection
- Scriptable interaction with the target

## Basic Usage

### Quick Scan
```bash
# Basic port scan
nmap -sS target.com

# Quick scan (top 1000 ports)
nmap -F target.com

# Ping scan
nmap -sn 192.168.1.0/24
```

### Advanced Scans
```bash
# Comprehensive scan with OS detection
nmap -A target.com

# UDP scan
nmap -sU target.com

# SYN scan (stealth)
nmap -sS target.com

# Version detection
nmap -sV target.com
```

## HexStrike AI Integration

### API Endpoint
```
POST /api/tools/nmap
```

### Request Parameters
```json
{
  "target": "scanme.nmap.org",
  "scan_type": "quick",
  "ports": "1-1000",
  "options": {
    "timing": "T4",
    "scripts": true,
    "version_detection": true
  }
}
```

### Response Format
```json
{
  "success": true,
  "execution_time": 45.2,
  "output": "Nmap scan results...",
  "ports": [
    {
      "port": 22,
      "state": "open",
      "service": "ssh",
      "version": "OpenSSH 7.4"
    }
  ],
  "host_status": "up",
  "scan_type": "quick"
}
```

## Scan Types

### 1. Quick Scan
- Scans top 1000 ports
- Fast execution
- Good for initial reconnaissance

### 2. Comprehensive Scan
- Full port range (1-65535)
- OS detection
- Service version detection
- Script scanning

### 3. Stealth Scan
- SYN scan
- Harder to detect
- Slower but more stealthy

## Common Use Cases

### Network Discovery
```bash
# Discover live hosts
nmap -sn 192.168.1.0/24

# Scan specific range
nmap 192.168.1.1-254
```

### Service Enumeration
```bash
# Detect services and versions
nmap -sV target.com

# Detect OS
nmap -O target.com
```

### Vulnerability Scanning
```bash
# Run NSE scripts
nmap --script vuln target.com

# Specific script categories
nmap --script safe target.com
```

## Best Practices

### 1. Scan Timing
- Use appropriate timing templates (-T0 to -T5)
- Be respectful of target systems
- Implement rate limiting for large scans

### 2. Legal Considerations
- Only scan systems you own or have permission to scan
- Follow responsible disclosure practices
- Document all scanning activities

### 3. Performance Optimization
- Use parallel scanning for multiple targets
- Choose appropriate scan types for your needs
- Consider using masscan for very large networks

## Common Issues and Solutions

### Issue: Permission Denied
**Solution**: Use sudo for raw socket operations
```bash
sudo nmap -sS target.com
```

### Issue: Slow Scanning
**Solution**: Adjust timing template
```bash
nmap -T4 target.com  # Faster timing
```

### Issue: False Positives
**Solution**: Use multiple scan types
```bash
nmap -sS -sV target.com  # SYN + Version detection
```

## Integration Examples

### Python Integration
```python
import requests

def run_nmap_scan(target, scan_type="quick"):
    url = "https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap"
    data = {
        "target": target,
        "scan_type": scan_type,
        "ports": "1-1000"
    }
    response = requests.post(url, json=data)
    return response.json()

# Usage
result = run_nmap_scan("scanme.nmap.org")
print(result)
```

### JavaScript Integration
```javascript
async function runNmapScan(target, scanType = "quick") {
  const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      target: target,
      scan_type: scanType,
      ports: "1-1000"
    })
  });
  return await response.json();
}

// Usage
runNmapScan("scanme.nmap.org").then(result => console.log(result));
```

## Advanced Features

### NSE Scripts
```bash
# Run specific scripts
nmap --script http-enum target.com

# Run script categories
nmap --script vuln,auth,discovery target.com
```

### Output Formats
```bash
# XML output
nmap -oX output.xml target.com

# Grepable output
nmap -oG output.grep target.com

# Normal output
nmap -oN output.txt target.com
```

## Troubleshooting

### Common Error Messages
1. **"Failed to resolve hostname"** - Check DNS resolution
2. **"No ports specified"** - Specify port range or use -F for fast scan
3. **"Permission denied"** - Use sudo for privileged operations

### Performance Tips
1. Use -T4 timing for faster scans
2. Limit port ranges when possible
3. Use parallel scanning for multiple targets
4. Consider using masscan for very large networks

## References

- [Official Nmap Documentation](https://nmap.org/docs.html)
- [Nmap Network Scanning](https://nmap.org/book/)
- [NSE Script Database](https://nmap.org/nsedoc/)
