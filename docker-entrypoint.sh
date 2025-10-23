#!/bin/bash
set -e

echo "============================================================================"
echo "🚀 Starting HexStrike AI v6.0 MCP Server"
echo "============================================================================"
echo "📡 Port: ${HEXSTRIKE_PORT:-8888}"
echo "🌐 Host: ${HEXSTRIKE_HOST:-0.0.0.0}"
echo "⏰ $(date)"
echo "============================================================================"

# 驗證關鍵工具是否可用
echo "🔍 Verifying core security tools..."
CRITICAL_TOOLS="nmap gobuster nuclei sqlmap hydra"
MISSING_TOOLS=""

for tool in $CRITICAL_TOOLS; do
    if ! command -v $tool &> /dev/null; then
        MISSING_TOOLS="$MISSING_TOOLS $tool"
    else
        echo "✅ $tool: $(command -v $tool)"
    fi
done

if [ -n "$MISSING_TOOLS" ]; then
    echo "⚠️  Warning: Some tools are missing:$MISSING_TOOLS"
    echo "    Server will start but some features may not work."
else
    echo "✅ All critical tools verified!"
fi

echo "============================================================================"
echo "🎯 Launching HexStrike AI Server..."
echo "============================================================================"

# 啟動 Flask 服務器
exec python3 /app/hexstrike_server.py --port "${HEXSTRIKE_PORT:-8888}" "$@"



