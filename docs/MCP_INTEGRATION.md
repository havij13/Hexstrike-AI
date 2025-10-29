# MCP (Model Context Protocol) Integration

## What is MCP?

HexStrike AI uses FastMCP to enable AI agents (Claude, ChatGPT, etc.) to directly control security tools through the Model Context Protocol.

## Architecture

```
AI Agent (Claude Desktop)
    ↓ (MCP Protocol)
hexstrike_mcp.py (MCP Server)
    ↓ (HTTP API)
hexstrike_server.py (Flask API Server)
    ↓ (Subprocess Execution)
Security Tools (Nmap, Gobuster, Nuclei, etc.)
```

## How It Works

1. **hexstrike_mcp.py**: MCP server that exposes security tools to AI agents through the Model Context Protocol
2. **hexstrike_server.py**: Flask API server that executes security tools and manages resources
3. AI agents call MCP tools, which proxy to Flask API endpoints

## Setup

### Prerequisites

- Python 3.11+
- HexStrike AI server running on `http://localhost:8888`
- Claude Desktop installed

### Start HexStrike AI Server

```bash
# Start the backend API server
python hexstrike_server.py --host 0.0.0.0 --port 8888

# In another terminal, start the MCP server
python hexstrike_mcp.py --server-url http://localhost:8888
```

### Configure in Claude Desktop

1. Locate Claude Desktop config file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add HexStrike MCP server configuration:

```json
{
  "mcpServers": {
    "hexstrike": {
      "command": "python",
      "args": [
        "C:\\path\\to\\hexstrike_mcp.py",
        "--server-url",
        "http://localhost:8888"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

3. Restart Claude Desktop

4. Verify connection by asking Claude: "List available security tools"

## Available MCP Tools

### Network Reconnaissance
- **nmap_scan**: Port scanning and service detection
- **rustscan_scan**: Fast port scanner
- **masscan_scan**: High-speed TCP port scanner
- **autorecon_scan**: Automated reconnaissance framework

### Web Application Security
- **gobuster_scan**: Directory and file brute-forcer
- **feroxbuster_scan**: Recursive content discovery
- **ffuf_scan**: Web fuzzer
- **nuclei_scan**: Vulnerability scanner
- **nikto_scan**: Web server scanner
- **sqlmap_scan**: SQL injection testing
- **wpscan_scan**: WordPress vulnerability scanner

### Authentication & Password Security
- **hydra_scan**: Network login cracker
- **john_crack**: Password hash cracker
- **hashcat_crack**: GPU-accelerated password recovery
- **medusa_scan**: Parallel login brute-forcer

### Binary Analysis & Reverse Engineering
- **ghidra_analyze**: Reverse engineering framework
- **radare2_analyze**: Binary analysis framework
- **gdb_debug**: GNU Debugger
- **binwalk_analyze**: Firmware analysis tool
- **volatility_analyze**: Memory forensics framework
- **strings_extract**: Extract strings from binaries

### Cloud Security
- **prowler_scan**: AWS security assessment
- **trivy_scan**: Container vulnerability scanner
- **kube_hunter_scan**: Kubernetes penetration testing
- **scout_suite_scan**: Multi-cloud security auditing

### DNS & Subdomain Enumeration
- **amass_scan**: Subdomain enumeration
- **subfinder_scan**: Passive subdomain discovery
- **fierce_scan**: DNS reconnaissance
- **dnsenum_scan**: DNS enumeration

### AI Intelligence & Automation
- **analyze_target**: AI-powered target analysis
- **select_tools**: AI tool recommendation
- **optimize_parameters**: AI parameter optimization
- **smart_scan**: Intelligent multi-tool scanning

## Usage Examples

### Ask Claude to scan a target

```
User: "Scan example.com with Nmap to find open ports"
Claude: [Calls nmap_scan tool automatically]
```

### Use AI recommendations

```
User: "What tools should I use to test example.com's security?"
Claude: [Calls select_tools to recommend appropriate tools based on target]
```

### Run automated recon

```
User: "Perform comprehensive reconnaissance on example.com"
Claude: [Calls smart_scan with AI-selected tools and parameters]
```

## Troubleshooting

### MCP server not connecting

1. Verify HexStrike server is running: `curl http://localhost:8888/health`
2. Check MCP server logs for errors
3. Verify Python path in Claude Desktop config is correct

### Tools not executing

1. Verify tools are installed on the system
2. Check tool availability: `which nmap` (or relevant tool)
3. Review server logs for execution errors

### Performance issues

1. Reduce concurrent scan limits
2. Use lighter scan profiles (e.g., "quick" instead of "comprehensive")
3. Increase server resources (CPU, RAM)

## Security Considerations

- MCP server should only run on localhost in production
- Restrict network access to authorized IPs if exposing server
- Regularly update security tools and templates
- Review scan results carefully to avoid false positives
- Only scan systems you have permission to test

## Advanced Configuration

### Custom Tool Integration

Add custom tools by:
1. Implementing endpoint in `hexstrike_server.py`
2. Adding MCP tool wrapper in `hexstrike_mcp.py`
3. Registering tool with FastMCP server

### Environment Variables

```bash
export HEXSTRIKE_DEBUG=1  # Enable debug logging
export HEXSTRIKE_CACHE_TTL=3600  # Cache TTL in seconds
export HEXSTRIKE_MAX_CONCURRENT=10  # Max concurrent scans
```

## Support

- GitHub Issues: [Report issues or request features](https://github.com/yourusername/hexstrike-ai/issues)
- Documentation: See `README.md` for more information
- Community: Join discussions and share use cases
