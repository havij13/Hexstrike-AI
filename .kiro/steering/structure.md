# HexStrike AI - Project Structure

## Root Directory Organization

```
hexstrike-ai/
├── api/                    # API models and configurations
│   ├── namespaces/        # API namespace definitions
│   ├── models.py          # Swagger/OpenAPI models
│   └── swagger_config.py  # API documentation config
├── Front-End/             # Next.js dashboard application
│   ├── src/              # React components and pages
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
├── assets/               # Project assets and logos
├── Documentations/       # Comprehensive documentation
│   ├── tools/           # Tool-specific documentation
│   ├── API_USAGE.md     # API reference guide
│   ├── DEPLOYMENT_GUIDE.md
│   └── AI_CLIENT_SETUP_GUIDE.md
├── scripts/             # Automation and deployment scripts
├── static/              # Web server static files
├── templates/           # HTML templates
├── test-data/           # Test datasets and samples
└── .kiro/              # Kiro IDE configuration
    └── steering/       # AI assistant guidance rules
```

## Core Application Files

### Main Server Components
- **hexstrike_server.py**: Main Flask server with AI agents and tool management
- **hexstrike_mcp.py**: MCP client for AI agent communication
- **requirements.txt**: Python dependencies

### Key Classes and Managers
- **ModernVisualEngine**: Beautiful output formatting with cybersecurity theme
- **IntelligentDecisionEngine**: AI-powered tool selection and optimization
- **BugBountyWorkflowManager**: Specialized workflows for bug bounty hunting
- **CTFWorkflowManager**: CTF competition automation
- **BrowserAgent**: Headless Chrome automation for web testing
- **EnhancedProcessManager**: Advanced process management and monitoring

## Configuration Files

### Docker & Deployment
- **Dockerfile**: Multi-stage build with Kali Linux base
- **docker-compose.yml**: Service orchestration
- **Makefile**: Simplified deployment commands
- **docker-entrypoint.sh**: Container startup script

### Cloud Platform Configs
- **railway.toml**: Railway deployment configuration
- **render.yaml**: Render platform settings
- **fly.toml**: Fly.io deployment config

### Frontend Configuration
- **Front-End/next.config.js**: Next.js configuration
- **Front-End/tailwind.config.js**: Tailwind CSS customization
- **Front-End/tsconfig.json**: TypeScript configuration

## API Structure

### Namespaces
- `/api/command`: Command execution with caching
- `/api/intelligence`: AI-powered analysis and optimization
- `/api/processes`: Process management and monitoring
- `/api/cache`: Cache statistics and management

### Tool Categories
- **Network Tools**: nmap, masscan, rustscan, amass, subfinder
- **Web Application**: gobuster, nuclei, sqlmap, wpscan, ffuf
- **Binary Analysis**: ghidra, radare2, gdb, binwalk, checksec
- **Cloud Security**: prowler, scout-suite, trivy, kube-hunter
- **CTF/Forensics**: volatility, foremost, steghide, john, hashcat

## Development Patterns

### Code Organization
- Each major component has its own class with clear responsibilities
- AI agents are modular and can be extended independently
- Tool integrations follow a consistent pattern with parameter optimization
- Error handling and recovery systems are built into each component

### Naming Conventions
- Classes use PascalCase (e.g., `ModernVisualEngine`)
- Methods use snake_case (e.g., `analyze_target`)
- Constants use UPPER_CASE (e.g., `HACKER_RED`)
- File names use snake_case or kebab-case

### Security Considerations
- All tool executions are sandboxed and monitored
- Input validation and sanitization for all user inputs
- Process isolation and resource limits
- Comprehensive logging for audit trails