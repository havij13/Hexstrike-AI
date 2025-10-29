# HexStrike AI Tools Documentation

This directory contains comprehensive documentation for all security tools integrated with HexStrike AI.

## Tool Categories

### 🌐 Network Security Tools
Tools for network reconnaissance, port scanning, and network analysis.

- **[Nmap](network/nmap-guide.md)** - Network mapper and port scanner
- **[Rustscan](network/rustscan-guide.md)** - Fast port scanner written in Rust
- **[Masscan](network/masscan-guide.md)** - High-speed network port scanner

### 🔍 Web Application Security Tools
Tools for web application testing, directory enumeration, and vulnerability scanning.

- **[Gobuster](web/gobuster-guide.md)** - Directory/file brute-forcing tool
- **[Feroxbuster](web/feroxbuster-guide.md)** - Fast recursive content discovery tool
- **[Nuclei](web/nuclei-guide.md)** - Vulnerability scanner based on templates
- **[Nikto](web/nikto-guide.md)** - Web server vulnerability scanner
- **[SQLMap](web/sqlmap-guide.md)** - Automatic SQL injection testing tool
- **[WPScan](web/wpscan-guide.md)** - WordPress vulnerability scanner

### 🔐 Authentication & Password Security Tools
Tools for password cracking, authentication testing, and credential analysis.

- **[Hydra](auth/hydra-guide.md)** - Network login cracker
- **[John the Ripper](auth/john-guide.md)** - Password hash cracker
- **[Hashcat](auth/hashcat-guide.md)** - GPU-accelerated password recovery tool

### 🔬 Binary Analysis & Reverse Engineering Tools
Tools for binary analysis, reverse engineering, and debugging.

- **[Ghidra](binary/ghidra-guide.md)** - Software reverse engineering framework
- **[Radare2](binary/radare2-guide.md)** - Portable reverse engineering framework
- **[GDB](binary/gdb-guide.md)** - GNU Debugger

### ☁️ Cloud & Container Security Tools
Tools for cloud security assessment and container analysis.

- **[Prowler](cloud/prowler-guide.md)** - Cloud security assessment tool
- **[Trivy](cloud/trivy-guide.md)** - Container vulnerability scanner
- **[Kube-Hunter](cloud/kube-hunter-guide.md)** - Kubernetes penetration testing tool

## Quick Start Guide

### 1. Choose Your Tool Category
Navigate to the appropriate category directory above to find the tool you need.

### 2. Read the Tool Guide
Each tool has a comprehensive guide covering:
- Tool introduction and purpose
- Installation and configuration
- Basic usage examples
- Advanced usage scenarios
- API integration examples
- Best practices and tips

### 3. Use Test Data
Check the `test-data/` directory for safe testing targets and sample files.

### 4. API Integration
All tools are accessible through the HexStrike AI REST API. See individual tool guides for API endpoint details.

## Common Use Cases

### Bug Bounty Hunting
1. Start with **Nmap** for network reconnaissance
2. Use **Gobuster** for directory enumeration
3. Run **Nuclei** for vulnerability scanning
4. Test with **SQLMap** for injection vulnerabilities

### CTF Competitions
1. Use **Ghidra** or **Radare2** for binary analysis
2. Apply **John the Ripper** for password cracking
3. Utilize **GDB** for debugging challenges

### Red Team Exercises
1. Begin with **Masscan** for rapid network scanning
2. Use **Feroxbuster** for comprehensive web enumeration
3. Apply **Hydra** for authentication testing
4. Leverage **Prowler** for cloud security assessment

### Vulnerability Assessment
1. Start with **Nikto** for web server scanning
2. Use **WPScan** for WordPress-specific vulnerabilities
3. Apply **Trivy** for container security scanning
4. Utilize **Kube-Hunter** for Kubernetes security

## API Integration

All tools are accessible through the HexStrike AI REST API:

```bash
# Example: Run Nmap scan
curl -X POST https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap \
  -H "Content-Type: application/json" \
  -d '{
    "target": "scanme.nmap.org",
    "scan_type": "quick",
    "ports": "1-1000"
  }'
```

## Safety and Legal Considerations

⚠️ **Important**: Always follow these guidelines:

1. **Only test systems you own or have explicit permission to test**
2. **Respect rate limits and don't overwhelm target systems**
3. **Follow responsible disclosure practices**
4. **Document all testing activities**
5. **Use appropriate tools for the testing scope**

## Getting Help

- Check individual tool guides for detailed usage instructions
- Review the [API Integration Guide](../API_INTEGRATION_GUIDE.md)
- See [Practical Scenarios](../PRACTICAL_SCENARIOS.md) for real-world examples
- Consult the main [README](../../README.md) for general information

## Contributing

To improve this documentation:

1. Follow the existing format and structure
2. Include practical examples and use cases
3. Add API integration examples
4. Update when tools are modified or new features are added
