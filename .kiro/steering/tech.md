# HexStrike AI - Technology Stack

## Backend Architecture
- **Language**: Python 3.8+
- **Framework**: Flask with Flask-RESTX for API documentation
- **MCP Integration**: FastMCP for AI agent communication
- **Process Management**: Advanced multi-threading with psutil monitoring
- **Caching**: LRU cache with intelligent eviction policies

## Frontend Dashboard
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom cybersecurity theme
- **UI Components**: Lucide React icons, Framer Motion animations
- **State Management**: React Query (TanStack Query) with SWR
- **Form Handling**: React Hook Form with Zod validation

## Core Dependencies
```
Flask==2.2.5
Flask-CORS==3.0.10
flask-restx==1.2.0
psutil==5.9.5
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.0
```

## Security Tools Integration
- **Base System**: Kali Linux Rolling with 150+ pre-installed security tools
- **Tool Categories**: Network (nmap, masscan), Web (gobuster, nuclei), Binary (ghidra, radare2), Cloud (prowler, trivy)
- **Browser Automation**: Selenium WebDriver with headless Chrome

## Deployment & Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Base Image**: kalilinux/kali-rolling:latest
- **Cloud Platforms**: Railway, Render, Fly.io support
- **Process Orchestration**: Docker Compose with health checks

## Common Commands

### Development
```bash
# Start development server
python3 hexstrike_server.py --debug

# Run with custom port
python3 hexstrike_server.py --port 8888

# Frontend development
cd Front-End && npm run dev
```

### Docker Operations
```bash
# Build and deploy locally
make deploy-local

# Individual operations
make build          # Build Docker image
make run            # Start with docker-compose
make logs           # View logs
make test           # Run health checks
make stop           # Stop containers
make clean          # Clean up everything
```

### Testing & Validation
```bash
# Health check
curl http://localhost:8888/health

# API test
curl -X POST http://localhost:8888/api/intelligence/analyze-target \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "analysis_type": "comprehensive"}'

# Run test scripts
bash scripts/test-docker.sh
```

## Environment Configuration
- **Port**: 8888 (default)
- **Host**: 0.0.0.0 for Docker deployment
- **Cache**: Configurable size and TTL
- **Timeout**: 300 seconds for command execution
- **Logging**: Structured logging with color-coded output