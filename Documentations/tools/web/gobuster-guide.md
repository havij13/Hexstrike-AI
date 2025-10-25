# Gobuster Guide

## Overview

Gobuster is a directory/file brute-forcing tool written in Go. It's designed to discover hidden directories and files on web servers through brute-force techniques.

## Features

- Directory and file brute-forcing
- DNS subdomain enumeration
- S3 bucket enumeration
- Fast and efficient scanning
- Multiple wordlist support

## Basic Usage

### Directory Brute-forcing
```bash
# Basic directory scan
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt

# File enumeration
gobuster dir -u https://target.com -w wordlist.txt -x php,html,txt

# Custom extensions
gobuster dir -u https://target.com -w wordlist.txt -x php,html,txt,jsp,asp
```

### DNS Subdomain Enumeration
```bash
# Subdomain enumeration
gobuster dns -d target.com -w subdomains.txt

# With wildcard handling
gobuster dns -d target.com -w subdomains.txt --wildcard
```

### S3 Bucket Enumeration
```bash
# S3 bucket enumeration
gobuster s3 -w bucketnames.txt
```

## HexStrike AI Integration

### API Endpoint
```
POST /api/tools/gobuster
```

### Request Parameters
```json
{
  "url": "https://target.com",
  "mode": "dir",
  "wordlist": "/usr/share/wordlists/dirb/common.txt",
  "extensions": ["php", "html", "txt"],
  "threads": 50,
  "timeout": 10
}
```

### Response Format
```json
{
  "success": true,
  "execution_time": 120.5,
  "output": "Gobuster scan results...",
  "directories_found": [
    "/admin/",
    "/backup/",
    "/config/"
  ],
  "files_found": [
    "/robots.txt",
    "/sitemap.xml"
  ],
  "total_requests": 2048,
  "response_codes": {
    "200": 15,
    "301": 5,
    "302": 3,
    "403": 8,
    "404": 2017
  }
}
```

## Scan Modes

### 1. Directory Mode (`dir`)
- Enumerates directories and files
- Most commonly used mode
- Supports custom extensions

### 2. DNS Mode (`dns`)
- Enumerates DNS subdomains
- Useful for reconnaissance
- Supports wildcard handling

### 3. S3 Mode (`s3`)
- Enumerates S3 buckets
- Useful for cloud security assessment

## Common Use Cases

### Web Application Reconnaissance
```bash
# Basic directory enumeration
gobuster dir -u https://target.com -w common.txt

# With file extensions
gobuster dir -u https://target.com -w common.txt -x php,html,txt
```

### Subdomain Discovery
```bash
# Subdomain enumeration
gobuster dns -d target.com -w subdomains.txt

# With specific DNS server
gobuster dns -d target.com -w subdomains.txt -r 8.8.8.8
```

### Cloud Security Assessment
```bash
# S3 bucket enumeration
gobuster s3 -w bucketnames.txt

# With region specification
gobuster s3 -w bucketnames.txt -r us-east-1
```

## Best Practices

### 1. Wordlist Selection
- Use appropriate wordlists for your target
- Start with common wordlists
- Use custom wordlists for specific applications

### 2. Rate Limiting
- Adjust thread count based on target responsiveness
- Use appropriate timeouts
- Be respectful of target systems

### 3. Extension Selection
- Include relevant file extensions
- Consider application-specific extensions
- Use wildcards when appropriate

## Common Issues and Solutions

### Issue: Too Many 404 Responses
**Solution**: Use more targeted wordlists
```bash
gobuster dir -u https://target.com -w custom-wordlist.txt
```

### Issue: Slow Scanning
**Solution**: Increase thread count
```bash
gobuster dir -u https://target.com -w wordlist.txt -t 100
```

### Issue: False Positives
**Solution**: Use status code filtering
```bash
gobuster dir -u https://target.com -w wordlist.txt -s 200,301,302
```

## Integration Examples

### Python Integration
```python
import requests

def run_gobuster_scan(url, mode="dir", wordlist="common.txt"):
    api_url = "https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster"
    data = {
        "url": url,
        "mode": mode,
        "wordlist": wordlist,
        "extensions": ["php", "html", "txt"],
        "threads": 50
    }
    response = requests.post(api_url, json=data)
    return response.json()

# Usage
result = run_gobuster_scan("https://target.com")
print(result)
```

### JavaScript Integration
```javascript
async function runGobusterScan(url, mode = "dir") {
  const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      mode: mode,
      wordlist: "common.txt",
      extensions: ["php", "html", "txt"],
      threads: 50
    })
  });
  return await response.json();
}

// Usage
runGobusterScan("https://target.com").then(result => console.log(result));
```

## Advanced Features

### Custom Wordlists
```bash
# Use custom wordlist
gobuster dir -u https://target.com -w custom-wordlist.txt

# Combine multiple wordlists
cat wordlist1.txt wordlist2.txt | gobuster dir -u https://target.com -w -
```

### Status Code Filtering
```bash
# Only show specific status codes
gobuster dir -u https://target.com -w wordlist.txt -s 200,301,302

# Exclude specific status codes
gobuster dir -u https://target.com -w wordlist.txt -b 404
```

### Output Options
```bash
# Verbose output
gobuster dir -u https://target.com -w wordlist.txt -v

# Quiet mode
gobuster dir -u https://target.com -w wordlist.txt -q

# JSON output
gobuster dir -u https://target.com -w wordlist.txt -o results.json -f
```

## Troubleshooting

### Common Error Messages
1. **"Invalid URL"** - Check URL format and accessibility
2. **"Wordlist not found"** - Verify wordlist path
3. **"Permission denied"** - Check file permissions

### Performance Tips
1. Use appropriate thread counts
2. Start with smaller wordlists
3. Use targeted wordlists for specific applications
4. Consider using feroxbuster for recursive scanning

## References

- [Gobuster GitHub Repository](https://github.com/OJ/gobuster)
- [Gobuster Documentation](https://github.com/OJ/gobuster/wiki)
