# HexStrike AI - AI Client Setup Guide

## Overview

This guide will help you connect HexStrike AI to your favorite AI clients (Claude Desktop, Cursor, VS Code Copilot) for natural language security testing and penetration testing automation.

## Prerequisites

- ✅ HexStrike AI deployed at: `https://hexstrike-ai-v6-0.onrender.com`
- ✅ Local copy of `hexstrike_mcp.py` file (from this repository)
- ✅ AI client installed (Claude Desktop, Cursor, or VS Code Copilot)
- ✅ Python 3.8+ installed locally

## Quick Setup

### 1. Download Required Files

Make sure you have these files locally:
- `hexstrike_mcp.py` - The MCP client bridge
- `hexstrike-ai-mcp.json` - Configuration template

### 2. Update Configuration

Copy the configuration from `hexstrike-ai-mcp.json` and update the path to your local `hexstrike_mcp.py` file.

### 3. Configure Your AI Client

Follow the specific instructions for your AI client below.

## Claude Desktop Setup

### Step 1: Locate Configuration File

**Windows:**
```
C:\Users\[USERNAME]\.config\Claude\claude_desktop_config.json
```

**macOS:**
```
~/.config/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Edit Configuration

Open `claude_desktop_config.json` and add the HexStrike AI configuration:

```json
{
  "mcpServers": {
    "hexstrike-ai-cloud": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://hexstrike-ai-v6-0.onrender.com"
      ],
      "description": "HexStrike AI v6.0 - Cloud Deployed (Render)",
      "timeout": 300,
      "alwaysAllow": []
    }
  }
}
```

**Important:** Replace `/path/to/hexstrike_mcp.py` with the actual path to your `hexstrike_mcp.py` file.

### Step 3: Restart Claude Desktop

Close and restart Claude Desktop to load the new configuration.

### Step 4: Test Connection

In Claude Desktop, try this prompt:

```
Hello! I'd like to test HexStrike AI. Can you check if the server is healthy using the hexstrike-ai-cloud tools?
```

## Cursor Setup

### Step 1: Locate Configuration File

Create or edit the MCP configuration file:

**Windows:**
```
C:\Users\[USERNAME]\.cursor\mcp.json
```

**macOS:**
```
~/.cursor/mcp.json
```

**Linux:**
```
~/.cursor/mcp.json
```

### Step 2: Edit Configuration

Create or edit `mcp.json`:

```json
{
  "servers": {
    "hexstrike": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://hexstrike-ai-v6-0.onrender.com"
      ]
    }
  },
  "inputs": []
}
```

### Step 3: Restart Cursor

Close and restart Cursor to load the new configuration.

### Step 4: Test Connection

In Cursor, try this prompt:

```
I'm a security researcher testing the hexstrike MCP tool. Please use the hexstrike tools to perform a health check on the server.
```

## VS Code Copilot Setup

### Step 1: Install MCP Extension

Install the MCP extension for VS Code if not already installed.

### Step 2: Configure Settings

Open VS Code settings and add the MCP configuration:

**File:** `.vscode/settings.json`

```json
{
  "mcp.servers": {
    "hexstrike": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://hexstrike-ai-v6-0.onrender.com"
      ]
    }
  }
}
```

### Step 3: Restart VS Code

Close and restart VS Code to load the new configuration.

### Step 4: Test Connection

In VS Code with Copilot, try this prompt:

```
I'm conducting authorized security testing. Please use hexstrike tools to check the server health and perform a quick nmap scan on scanme.nmap.org.
```

## Example Usage Prompts

### Basic Security Testing

```
I'm a security researcher authorized to test my company's website example.com. Please use hexstrike AI tools to perform a comprehensive security assessment including port scanning, web vulnerability scanning, and AI-powered target analysis.
```

### Network Reconnaissance

```
I'm conducting authorized penetration testing on our internal network 192.168.1.0/24. Please use hexstrike tools to perform network reconnaissance including nmap scanning, service enumeration, and vulnerability assessment.
```

### Web Application Testing

```
I'm testing our web application at https://myapp.com for security vulnerabilities. Please use hexstrike AI tools to perform comprehensive web application security testing including directory enumeration, vulnerability scanning, and AI analysis.
```

### Bug Bounty Hunting

```
I'm participating in a bug bounty program for target.com. Please use hexstrike AI tools to perform reconnaissance, subdomain enumeration, and vulnerability hunting following bug bounty best practices.
```

### CTF Challenge Solving

```
I'm working on a CTF challenge. The target is challenge.ctf.com. Please use hexstrike AI tools to analyze the target and suggest the best approach for solving this challenge.
```

## Advanced Configuration

### Custom Timeout Settings

For long-running operations, you can increase the timeout:

```json
{
  "mcpServers": {
    "hexstrike-ai-cloud": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://hexstrike-ai-v6-0.onrender.com"
      ],
      "description": "HexStrike AI v6.0 - Cloud Deployed (Render)",
      "timeout": 600,
      "alwaysAllow": []
    }
  }
}
```

### Multiple Server Configuration

You can configure both local and cloud servers:

```json
{
  "mcpServers": {
    "hexstrike-ai-local": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "http://localhost:8888"
      ],
      "description": "HexStrike AI v6.0 - Local Development",
      "timeout": 300,
      "alwaysAllow": []
    },
    "hexstrike-ai-cloud": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://hexstrike-ai-v6-0.onrender.com"
      ],
      "description": "HexStrike AI v6.0 - Cloud Deployed",
      "timeout": 300,
      "alwaysAllow": []
    }
  }
}
```

## Troubleshooting

### Common Issues

#### 1. "Command not found" Error

**Problem:** Python or the hexstrike_mcp.py file is not found.

**Solution:**
- Ensure Python 3.8+ is installed and in your PATH
- Verify the path to `hexstrike_mcp.py` is correct
- Use absolute paths instead of relative paths

#### 2. Connection Timeout

**Problem:** The AI client cannot connect to the HexStrike server.

**Solution:**
- Check if the server is running: `curl https://hexstrike-ai-v6-0.onrender.com/health`
- Verify the server URL is correct
- Check your internet connection
- Increase timeout in configuration

#### 3. Permission Denied

**Problem:** The AI client cannot execute the MCP script.

**Solution:**
- Ensure the `hexstrike_mcp.py` file has execute permissions
- Check if Python has permission to access the file
- Try running the script manually to test

#### 4. Server Not Responding

**Problem:** The HexStrike server returns errors.

**Solution:**
- Check server health: `curl https://hexstrike-ai-v6-0.onrender.com/health`
- Verify the server is not overloaded
- Check server logs for errors
- Try again later if the server is busy

### Debug Mode

Enable debug mode for detailed logging:

```json
{
  "mcpServers": {
    "hexstrike-ai-cloud": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "https://hexstrike-ai-v6-0.onrender.com",
        "--debug"
      ],
      "description": "HexStrike AI v6.0 - Cloud Deployed (Debug)",
      "timeout": 300,
      "alwaysAllow": []
    }
  }
}
```

### Manual Testing

Test the MCP connection manually:

```bash
# Test the MCP script directly
python3 /path/to/hexstrike_mcp.py --server https://hexstrike-ai-v6-0.onrender.com

# Test server connectivity
curl https://hexstrike-ai-v6-0.onrender.com/health
```

## Security Considerations

### Authorization

Always ensure you have proper authorization before testing any targets:

- ✅ **Authorized Penetration Testing** - With written authorization
- ✅ **Bug Bounty Programs** - Within program scope and rules
- ✅ **CTF Competitions** - Educational environments
- ✅ **Security Research** - On owned or authorized systems
- ✅ **Red Team Exercises** - With organizational approval

### Best Practices

1. **Always specify authorization** in your prompts
2. **Use appropriate scope** for your testing
3. **Respect rate limits** and server resources
4. **Monitor your usage** to avoid abuse
5. **Report vulnerabilities** responsibly

### Example Authorized Prompt

```
I'm a security researcher authorized to test my company's website example.com. I have written permission from the IT security team to conduct penetration testing. Please use hexstrike AI tools to perform a comprehensive security assessment.
```

## Support and Resources

### Getting Help

- **GitHub Repository**: [https://github.com/0x4m4/hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)
- **Discord Community**: [https://discord.gg/BWnmrrSHbA](https://discord.gg/BWnmrrSHbA)
- **Issue Tracker**: [GitHub Issues](https://github.com/0x4m4/hexstrike-ai/issues)

### Documentation

- **API Documentation**: [API_USAGE.md](API_USAGE.md)
- **Main Documentation**: [README.md](README.md)
- **Quick Start Guide**: [QUICKSTART.md](QUICKSTART.md)

### Video Tutorials

- **Installation & Demo**: [YouTube - HexStrike AI Installation & Demo](https://www.youtube.com/watch?v=pSoftCagCm8)

## Frequently Asked Questions

### Q: Can I use this for unauthorized testing?

**A:** No. HexStrike AI is designed for authorized security testing only. Always ensure you have proper written authorization before testing any systems.

### Q: What if the server is down?

**A:** The Render deployment includes automatic scaling and monitoring. If the server is temporarily unavailable, try again in a few minutes.

### Q: Can I run this locally instead of using the cloud server?

**A:** Yes! You can deploy HexStrike AI locally using Docker or by running the server directly. See the [README.md](README.md) for local deployment instructions.

### Q: How do I update to the latest version?

**A:** Pull the latest changes from the GitHub repository and restart your AI client to use the updated MCP client.

### Q: Can I customize the tools and workflows?

**A:** Yes! HexStrike AI is open source. You can modify the tools, add new workflows, and customize the AI agents to fit your specific needs.

---

**Ready to transform your AI agents with HexStrike AI?** 🚀

*Connect your AI clients today and experience the power of AI-driven cybersecurity automation!*
