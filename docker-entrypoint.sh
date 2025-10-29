#!/bin/bash
set -e

echo "🚀 Starting HexStrike AI v6.0..."
echo "=================================="

# Set default values
HEXSTRIKE_PORT=${HEXSTRIKE_PORT:-8888}
HEXSTRIKE_HOST=${HEXSTRIKE_HOST:-0.0.0.0}
LOG_LEVEL=${LOG_LEVEL:-INFO}

echo "📊 Configuration:"
echo "  Port: $HEXSTRIKE_PORT"
echo "  Host: $HEXSTRIKE_HOST"
echo "  Log Level: $LOG_LEVEL"
echo "  Python Version: $(python3 --version)"

# Create necessary directories
mkdir -p /app/logs /app/data /app/config

# Check if required files exist
if [ ! -f "hexstrike_server.py" ]; then
    echo "❌ hexstrike_server.py not found!"
    exit 1
fi

# Verify Python dependencies
echo "🔍 Checking Python dependencies..."
python3 -c "import flask, requests, psutil; print('✅ Core dependencies OK')" || {
    echo "❌ Missing core dependencies"
    exit 1
}

# Check for optional dependencies
python3 -c "import aiohttp; print('✅ aiohttp available')" 2>/dev/null || echo "⚠️  aiohttp not available"
python3 -c "import selenium; print('✅ selenium available')" 2>/dev/null || echo "⚠️  selenium not available"

# Verify security tools (if available)
echo "🔧 Checking security tools..."
command -v nmap >/dev/null 2>&1 && echo "✅ nmap available" || echo "⚠️  nmap not available"
command -v curl >/dev/null 2>&1 && echo "✅ curl available" || echo "⚠️  curl not available"

# Set up signal handlers for graceful shutdown
trap 'echo "🛑 Shutting down gracefully..."; kill -TERM $PID; wait $PID' TERM INT

echo "🎯 Starting HexStrike AI server..."
echo "   Access at: http://$HEXSTRIKE_HOST:$HEXSTRIKE_PORT"
echo "   Health check: http://$HEXSTRIKE_HOST:$HEXSTRIKE_PORT/health"
echo ""

# Start the application
if [ "$1" = "worker" ]; then
    echo "🔄 Starting in worker mode..."
    python3 hexstrike_worker.py &
else
    echo "🌐 Starting web server..."
    python3 hexstrike_server.py --port "$HEXSTRIKE_PORT" --host "$HEXSTRIKE_HOST" &
fi



