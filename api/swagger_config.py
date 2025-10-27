"""
HexStrike AI - Swagger Configuration
Configuration for OpenAPI/Swagger documentation.
"""

SWAGGER_CONFIG = {
    'title': 'HexStrike AI API',
    'version': '1.0.0',
    'description': '''
# HexStrike AI - Advanced Penetration Testing Framework

A comprehensive security testing platform with 150+ security tools and 12+ AI agents.

## Features
- **Network Reconnaissance**: Nmap, Rustscan, Masscan, and more
- **Web Application Security**: Nuclei, SQLMap, Gobuster, and more
- **Authentication Testing**: Hydra, John, Hashcat, and more
- **Binary Analysis**: Ghidra, Radare2, GDB, and more
- **Cloud Security**: Prowler, Trivy, Kube-Hunter, and more
- **AI Agents**: 12+ specialized AI agents for penetration testing

## Getting Started

1. **Authentication**: No authentication required for basic usage
2. **Rate Limiting**: 100 requests per minute per IP
3. **Response Format**: All responses follow JSON format

## API Endpoints

### Tools
- `POST /api/v1/tools/{tool_name}` - Execute a security tool
- `GET /api/v1/tools` - List all available tools

### AI Agents
- `POST /api/v1/ai/chat` - Interact with AI agents
- `GET /api/v1/ai/agents` - List available AI agents

### Process Management
- `GET /api/v1/processes` - List running processes
- `POST /api/v1/processes/{pid}/stop` - Stop a process

## Examples

### Execute Nmap Scan
```bash
curl -X POST https://api.hexstrike.ai/api/v1/tools/nmap \\
  -H "Content-Type: application/json" \\
  -d '{
    "target": "example.com",
    "scan_type": "syn",
    "ports": "1-1000"
  }'
```

### Execute Nuclei Scan
```bash
curl -X POST https://api.hexstrike.ai/api/v1/tools/nuclei \\
  -H "Content-Type: application/json" \\
  -d '{
    "target": "https://example.com",
    "severity": "high",
    "tags": "xss,sqli"
  }'
```

## Documentation

For more information, visit:
- **Documentation**: https://docs.hexstrike.ai
- **GitHub**: https://github.com/hexstrike-ai
- **Support**: support@hexstrike.ai
    ''',
    'termsOfService': 'https://hexstrike.ai/terms',
    'contact': {
        'name': 'HexStrike AI Support',
        'email': 'support@hexstrike.ai',
        'url': 'https://hexstrike.ai/contact'
    },
    'license': {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT'
    },
    'servers': [
        {
            'url': 'https://hexstrike-ai-v6-0.onrender.com',
            'description': 'Production Server'
        },
        {
            'url': 'http://localhost:8888',
            'description': 'Local Development Server'
        }
    ],
    'tags': [
        {
            'name': 'tools',
            'description': 'Security tools operations (Nmap, Nuclei, SQLMap, etc.)'
        },
        {
            'name': 'ai',
            'description': 'AI agents and intelligent automation'
        },
        {
            'name': 'processes',
            'description': 'Process management and monitoring'
        }
    ]
}

# Security schemes for API documentation
SECURITY_DEFINITIONS = {
    'ApiKeyAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-Key'
    },
    'BearerAuth': {
        'type': 'http',
        'scheme': 'bearer',
        'bearerFormat': 'JWT'
    }
}

# Response models
RESPONSE_MODELS = {
    'success': {
        'description': 'Success response',
        'schema': {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'},
                'data': {'type': 'object'}
            }
        }
    },
    'error': {
        'description': 'Error response',
        'schema': {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'error': {'type': 'string'},
                'details': {'type': 'object'}
            }
        }
    }
}
