#!/bin/bash
# HexStrike AI - Deployment Fix Script
# Addresses common deployment issues

set -e

echo "🔧 HexStrike AI Deployment Fix"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Fix 1: Update requirements.txt for compatibility
fix_requirements() {
    log_info "Fixing Python requirements..."
    
    cat > requirements-fixed.txt << 'EOF'
# Core web framework
Flask==2.3.3
Flask-CORS==4.0.0
flask-restx==1.3.0

# System monitoring
psutil==5.9.6

# HTTP client
requests==2.31.0

# HTML parsing
beautifulsoup4==4.12.2

# Async HTTP (compatible version)
aiohttp>=3.9.0

# Configuration
python-dotenv==1.0.0

# WSGI server
gunicorn==21.2.0

# Monitoring
prometheus-client==0.19.0

# Optional dependencies (install if possible)
selenium>=4.15.0; python_version>="3.8"
websockets>=12.0; python_version>="3.8"
paho-mqtt>=1.6.0
EOF

    log_success "Created requirements-fixed.txt"
}

# Fix 2: Create lightweight Dockerfile
fix_dockerfile() {
    log_info "Creating lightweight Dockerfile..."
    
    cat > Dockerfile.lightweight << 'EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    HEXSTRIKE_PORT=8888 \
    HEXSTRIKE_HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install minimal security tools
RUN apt-get update && apt-get install -y \
    nmap \
    netcat-traditional \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements-fixed.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY hexstrike_server.py hexstrike_mcp.py ./
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create directories
RUN mkdir -p logs data config

EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8888/health || exit 1

CMD ["/entrypoint.sh"]
EOF

    log_success "Created Dockerfile.lightweight"
}

# Fix 3: Create minimal server for testing
fix_minimal_server() {
    log_info "Creating minimal test server..."
    
    cat > hexstrike_minimal.py << 'EOF'
#!/usr/bin/env python3
"""
HexStrike AI - Minimal Server for Testing
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '6.0.0-minimal',
        'timestamp': datetime.utcnow().isoformat(),
        'message': 'HexStrike AI is running'
    })

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'name': 'HexStrike AI',
        'version': '6.0.0-minimal',
        'description': 'AI-Powered Cybersecurity Automation Platform',
        'endpoints': {
            'health': '/health',
            'api': '/api',
            'metrics': '/metrics'
        }
    })

@app.route('/api')
def api_root():
    """API root endpoint"""
    return jsonify({
        'api_version': '6.0',
        'status': 'active',
        'available_endpoints': [
            '/api/command',
            '/api/tools/status',
            '/api/intelligence/analyze-target'
        ]
    })

@app.route('/api/command', methods=['POST'])
def execute_command():
    """Mock command execution"""
    data = request.get_json() or {}
    command = data.get('command', '')
    
    # Security check - don't execute dangerous commands
    dangerous_commands = ['rm', 'del', 'format', 'shutdown', 'reboot']
    if any(cmd in command.lower() for cmd in dangerous_commands):
        return jsonify({
            'success': False,
            'error': 'Dangerous command blocked',
            'command': command
        }), 400
    
    # Mock response
    return jsonify({
        'success': True,
        'command': command,
        'output': f'Mock output for: {command}',
        'execution_time': 0.1,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/tools/status')
def tools_status():
    """Mock tools status"""
    return jsonify({
        'tools': {
            'nmap': {'available': True, 'version': '7.94'},
            'curl': {'available': True, 'version': '7.88.1'},
            'wget': {'available': True, 'version': '1.21.3'}
        },
        'total_tools': 3,
        'available_tools': 3
    })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    metrics = [
        '# HELP hexstrike_requests_total Total requests',
        '# TYPE hexstrike_requests_total counter',
        'hexstrike_requests_total 42',
        '',
        '# HELP hexstrike_uptime_seconds Uptime in seconds',
        '# TYPE hexstrike_uptime_seconds gauge',
        'hexstrike_uptime_seconds 3600'
    ]
    return '\n'.join(metrics), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', os.environ.get('HEXSTRIKE_PORT', 8888)))
    host = os.environ.get('HEXSTRIKE_HOST', '0.0.0.0')
    
    logger.info(f"Starting HexStrike AI Minimal Server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
EOF

    log_success "Created hexstrike_minimal.py"
}

# Fix 4: Update docker-compose for testing
fix_docker_compose() {
    log_info "Creating test docker-compose..."
    
    cat > docker-compose.test.yml << 'EOF'
version: '3.8'

services:
  hexstrike-test:
    build:
      context: .
      dockerfile: Dockerfile.lightweight
    ports:
      - "8888:8888"
    environment:
      - HEXSTRIKE_PORT=8888
      - HEXSTRIKE_HOST=0.0.0.0
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8888/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

networks:
  default:
    name: hexstrike-test
EOF

    log_success "Created docker-compose.test.yml"
}

# Fix 5: Create deployment test script
fix_test_script() {
    log_info "Creating deployment test script..."
    
    cat > test-deployment.sh << 'EOF'
#!/bin/bash
set -e

echo "🧪 Testing HexStrike AI Deployment"
echo "=================================="

# Test 1: Build lightweight image
echo "📦 Building lightweight image..."
docker build -f Dockerfile.lightweight -t hexstrike-test:latest .

# Test 2: Run container
echo "🚀 Starting test container..."
docker run -d --name hexstrike-test -p 8888:8888 hexstrike-test:latest

# Wait for startup
echo "⏳ Waiting for startup..."
sleep 10

# Test 3: Health check
echo "🏥 Testing health endpoint..."
curl -f http://localhost:8888/health || {
    echo "❌ Health check failed"
    docker logs hexstrike-test
    exit 1
}

# Test 4: API endpoints
echo "🔌 Testing API endpoints..."
curl -f http://localhost:8888/api || {
    echo "❌ API test failed"
    exit 1
}

# Test 5: Metrics
echo "📊 Testing metrics..."
curl -f http://localhost:8888/metrics || {
    echo "❌ Metrics test failed"
    exit 1
}

echo "✅ All tests passed!"

# Cleanup
echo "🧹 Cleaning up..."
docker stop hexstrike-test
docker rm hexstrike-test

echo "🎉 Deployment test completed successfully!"
EOF

    chmod +x test-deployment.sh
    log_success "Created test-deployment.sh"
}

# Main execution
main() {
    log_info "Starting deployment fixes..."
    
    fix_requirements
    fix_dockerfile
    fix_minimal_server
    fix_docker_compose
    fix_test_script
    
    echo ""
    log_success "All fixes applied successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Test locally: ./test-deployment.sh"
    echo "2. Deploy to Render: Use Dockerfile.lightweight"
    echo "3. Use requirements-fixed.txt for dependencies"
    echo "4. Monitor with: docker-compose -f docker-compose.test.yml up"
    echo ""
    echo "🔧 For Render deployment:"
    echo "- Set dockerfile path to: Dockerfile.lightweight"
    echo "- Use requirements-fixed.txt"
    echo "- Set PORT environment variable"
}

main "$@"
EOF

chmod +x scripts/fix-deployment.sh
log_success "Created deployment fix script"