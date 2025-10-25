// HexStrike AI - Interactive Dashboard JavaScript
class HexStrikeDashboard {
    constructor() {
        this.serverUrl = window.location.origin;
        this.isLoading = false;
        this.init();
    }

    init() {
        this.checkServerHealth();
        this.setupEventListeners();
        this.updateEndpoint();
    }

    setupEventListeners() {
        // Auto-update server health every 30 seconds
        setInterval(() => {
            this.checkServerHealth();
        }, 30000);

        // Enter key support for API execution
        document.getElementById('target').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeAPI();
            }
        });
    }

    async checkServerHealth() {
        try {
            const response = await fetch(`${this.serverUrl}/health`);
            const data = await response.json();
            
            const statusIndicator = document.getElementById('server-status');
            const healthText = document.getElementById('server-health');
            
            if (response.ok) {
                statusIndicator.textContent = '✅';
                statusIndicator.className = 'status-indicator success';
                healthText.textContent = `Healthy - ${data.version} | ${data.available_tools} tools`;
                healthText.className = 'success';
            } else {
                statusIndicator.textContent = '❌';
                statusIndicator.className = 'status-indicator error';
                healthText.textContent = 'Unhealthy';
                healthText.className = 'error';
            }
        } catch (error) {
            const statusIndicator = document.getElementById('server-status');
            const healthText = document.getElementById('server-health');
            
            statusIndicator.textContent = '❌';
            statusIndicator.className = 'status-indicator error';
            healthText.textContent = 'Connection Failed';
            healthText.className = 'error';
            
            console.error('Health check failed:', error);
        }
    }

    updateEndpoint() {
        const endpoint = document.getElementById('endpoint').value;
        const method = document.getElementById('method');
        
        // Set method based on endpoint
        if (endpoint === '/health') {
            method.value = 'GET';
        } else {
            method.value = 'POST';
        }
    }

    async executeAPI() {
        if (this.isLoading) return;
        
        const endpoint = document.getElementById('endpoint').value;
        const target = document.getElementById('target').value;
        const method = document.getElementById('method').value;
        const resultDiv = document.getElementById('api-result');
        
        if (!target.trim()) {
            resultDiv.textContent = '❌ Please enter a target';
            resultDiv.className = 'error';
            return;
        }

        this.isLoading = true;
        resultDiv.textContent = '🔄 Executing command...';
        resultDiv.className = 'loading';

        try {
            let requestOptions = {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };

            if (method === 'POST') {
                const payload = this.buildPayload(endpoint, target);
                requestOptions.body = JSON.stringify(payload);
            }

            const response = await fetch(`${this.serverUrl}${endpoint}`, requestOptions);
            const data = await response.json();

            if (response.ok) {
                resultDiv.textContent = JSON.stringify(data, null, 2);
                resultDiv.className = 'success';
            } else {
                resultDiv.textContent = `❌ Error: ${data.error || 'Unknown error'}`;
                resultDiv.className = 'error';
            }
        } catch (error) {
            resultDiv.textContent = `❌ Network Error: ${error.message}`;
            resultDiv.className = 'error';
        } finally {
            this.isLoading = false;
        }
    }

    buildPayload(endpoint, target) {
        const payloads = {
            '/api/tools/nmap': {
                target: target,
                scan_type: 'quick',
                ports: '1-1000'
            },
            '/api/tools/gobuster': {
                target: target,
                wordlist: 'common',
                extensions: 'php,html,txt'
            },
            '/api/tools/nuclei': {
                target: target,
                templates: 'common-vulnerabilities'
            },
            '/api/intelligence/analyze-target': {
                target: target,
                analysis_type: 'comprehensive'
            }
        };

        return payloads[endpoint] || { target: target };
    }

    showModal(title, content) {
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-body').innerHTML = content;
        document.getElementById('modal-overlay').style.display = 'flex';
    }

    closeModal() {
        document.getElementById('modal-overlay').style.display = 'none';
    }
}

// Global functions for HTML onclick events
function testHealth() {
    dashboard.checkServerHealth();
}

function showNmapDemo() {
    const content = `
        <h3>🔍 Nmap Scan Demo</h3>
        <p>This will perform a quick port scan on the specified target.</p>
        <div class="demo-steps">
            <ol>
                <li>Select "Nmap Scan" from the endpoint dropdown</li>
                <li>Enter a target (e.g., scanme.nmap.org)</li>
                <li>Click "Execute" to run the scan</li>
            </ol>
        </div>
        <div class="demo-example">
            <h4>Example Command:</h4>
            <pre>curl -X POST ${window.location.origin}/api/tools/nmap \\
  -H "Content-Type: application/json" \\
  -d '{"target": "scanme.nmap.org", "scan_type": "quick"}'</pre>
        </div>
    `;
    dashboard.showModal('Nmap Scan Demo', content);
}

function showWebScan() {
    const content = `
        <h3>🌐 Web Application Scan Demo</h3>
        <p>This will perform a comprehensive web application security scan.</p>
        <div class="demo-steps">
            <ol>
                <li>Select "Gobuster Scan" or "Nuclei Scan" from the endpoint dropdown</li>
                <li>Enter a web target (e.g., https://example.com)</li>
                <li>Click "Execute" to run the scan</li>
            </ol>
        </div>
        <div class="demo-example">
            <h4>Example Gobuster Command:</h4>
            <pre>curl -X POST ${window.location.origin}/api/tools/gobuster \\
  -H "Content-Type: application/json" \\
  -d '{"target": "https://example.com", "wordlist": "common"}'</pre>
        </div>
    `;
    dashboard.showModal('Web Scan Demo', content);
}

function showAIAnalysis() {
    const content = `
        <h3>🧠 AI Target Analysis Demo</h3>
        <p>This will use AI to analyze a target and suggest the best security testing approach.</p>
        <div class="demo-steps">
            <ol>
                <li>Select "AI Target Analysis" from the endpoint dropdown</li>
                <li>Enter a target (e.g., example.com)</li>
                <li>Click "Execute" to run the AI analysis</li>
            </ol>
        </div>
        <div class="demo-example">
            <h4>Example AI Analysis Command:</h4>
            <pre>curl -X POST ${window.location.origin}/api/intelligence/analyze-target \\
  -H "Content-Type: application/json" \\
  -d '{"target": "example.com", "analysis_type": "comprehensive"}'</pre>
        </div>
    `;
    dashboard.showModal('AI Analysis Demo', content);
}

function showMCPGuide() {
    const content = `
        <h3>🤖 AI Client Integration Setup</h3>
        <p>Connect HexStrike AI to Claude Desktop, Cursor, or VS Code Copilot for natural language security testing.</p>
        
        <div class="setup-section">
            <h4>📋 Prerequisites</h4>
            <ul>
                <li>HexStrike AI deployed at: <code>${window.location.origin}</code></li>
                <li>Local copy of <code>hexstrike_mcp.py</code> file</li>
                <li>AI client installed (Claude Desktop, Cursor, or VS Code Copilot)</li>
            </ul>
        </div>

        <div class="setup-section">
            <h4>🔧 Claude Desktop Setup</h4>
            <p>Edit <code>~/.config/Claude/claude_desktop_config.json</code>:</p>
            <pre>{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "${window.location.origin}"
      ],
      "description": "HexStrike AI v6.0 - Cloud Deployed",
      "timeout": 300
    }
  }
}</pre>
        </div>

        <div class="setup-section">
            <h4>🔧 Cursor/VS Code Setup</h4>
            <p>Edit <code>.cursor/mcp.json</code> or <code>.vscode/settings.json</code>:</p>
            <pre>{
  "servers": {
    "hexstrike": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/path/to/hexstrike_mcp.py",
        "--server",
        "${window.location.origin}"
      ]
    }
  }
}</pre>
        </div>

        <div class="setup-section">
            <h4>💬 Example Usage</h4>
            <p>After setup, you can use natural language commands like:</p>
            <ul>
                <li>"Scan example.com for open ports using nmap"</li>
                <li>"Perform a web vulnerability scan on target.com"</li>
                <li>"Analyze the security posture of mywebsite.org"</li>
            </ul>
        </div>
    `;
    dashboard.showModal('AI Client Setup Guide', content);
}

function showAPIDocs() {
    const content = `
        <h3>🔧 Direct API Usage</h3>
        <p>Use HTTP requests directly for custom integrations and automated security testing.</p>
        
        <div class="api-section">
            <h4>🏥 Health Check</h4>
            <pre>curl ${window.location.origin}/health</pre>
        </div>

        <div class="api-section">
            <h4>🔍 Nmap Scan</h4>
            <pre>curl -X POST ${window.location.origin}/api/tools/nmap \\
  -H "Content-Type: application/json" \\
  -d '{"target": "scanme.nmap.org", "scan_type": "quick"}'</pre>
        </div>

        <div class="api-section">
            <h4>🌐 Web Scan</h4>
            <pre>curl -X POST ${window.location.origin}/api/tools/gobuster \\
  -H "Content-Type: application/json" \\
  -d '{"target": "https://example.com", "wordlist": "common"}'</pre>
        </div>

        <div class="api-section">
            <h4>🧠 AI Analysis</h4>
            <pre>curl -X POST ${window.location.origin}/api/intelligence/analyze-target \\
  -H "Content-Type: application/json" \\
  -d '{"target": "example.com", "analysis_type": "comprehensive"}'</pre>
        </div>

        <div class="api-section">
            <h4>📊 Process Management</h4>
            <pre># List processes
curl ${window.location.origin}/api/processes/list

# Get process status
curl ${window.location.origin}/api/processes/status/PID

# Terminate process
curl -X POST ${window.location.origin}/api/processes/terminate/PID</pre>
        </div>
    `;
    dashboard.showModal('API Documentation', content);
}

function showWebGuide() {
    const content = `
        <h3>🌐 Web Interface Usage Guide</h3>
        <p>This interactive dashboard provides quick access to HexStrike AI's capabilities.</p>
        
        <div class="guide-section">
            <h4>📊 Server Status</h4>
            <p>Monitor the health and status of your HexStrike AI server in real-time.</p>
        </div>

        <div class="guide-section">
            <h4>⚡ Quick Actions</h4>
            <ul>
                <li><strong>Health Check:</strong> Test server connectivity</li>
                <li><strong>Nmap Scan:</strong> Perform port scanning</li>
                <li><strong>Web Scan:</strong> Test web applications</li>
                <li><strong>AI Analysis:</strong> Get intelligent target analysis</li>
            </ul>
        </div>

        <div class="guide-section">
            <h4>🔧 API Testing Interface</h4>
            <p>Test any API endpoint directly from the web interface:</p>
            <ol>
                <li>Select an endpoint from the dropdown</li>
                <li>Enter your target</li>
                <li>Click "Execute" to run the command</li>
                <li>View results in real-time</li>
            </ol>
        </div>

        <div class="guide-section">
            <h4>🛠️ Tool Categories</h4>
            <p>Browse the 150+ available security tools organized by category:</p>
            <ul>
                <li>Network Reconnaissance (25+ tools)</li>
                <li>Web Application Security (40+ tools)</li>
                <li>Authentication & Password (12+ tools)</li>
                <li>Binary Analysis (25+ tools)</li>
            </ul>
        </div>
    `;
    dashboard.showModal('Web Interface Guide', content);
}

function executeAPI() {
    dashboard.executeAPI();
}

function updateEndpoint() {
    dashboard.updateEndpoint();
}

function closeModal() {
    dashboard.closeModal();
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new HexStrikeDashboard();
});
