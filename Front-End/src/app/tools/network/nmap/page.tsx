'use client'

import { useState } from 'react'
import { 
  Globe, 
  Play, 
  Settings, 
  ArrowLeft,
  Target,
  Clock,
  Activity,
  Download,
  Eye,
  Zap
} from 'lucide-react'
import Link from 'next/link'

interface ScanProfile {
  id: string
  name: string
  description: string
  command: string
  estimatedTime: string
}

export default function NmapPage() {
  const [target, setTarget] = useState('scanme.nmap.org')
  const [scanType, setScanType] = useState('quick')
  const [ports, setPorts] = useState('1-1000')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)

  const scanProfiles: ScanProfile[] = [
    {
      id: 'quick',
      name: 'Quick Scan',
      description: 'Fast scan of top 1000 ports',
      command: 'nmap -F target',
      estimatedTime: '30 seconds'
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Scan',
      description: 'Full port range with service detection',
      command: 'nmap -sV -sC -ob target',
      estimatedTime: '5-10 minutes'
    },
    {
      id: 'stealth',
      name: 'Stealth Scan',
      description: 'SYN scan for stealth reconnaissance',
      command: 'nmap -sS target',
      estimatedTime: '2-5 minutes'
    },
    {
      id: 'udp',
      name: 'UDP Scan',
      description: 'UDP port scanning',
      command: 'nmap -sU target',
      estimatedTime: '10-15 minutes'
    }
  ]

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          scan_type: scanType,
          ports,
        }),
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Scan failed:', error)
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link href="/tools/network" className="text-cyber-primary hover:text-cyber-light transition-colors">
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-3xl font-cyber font-bold text-cyber-primary neon-glow">
              NMAP SCANNER
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              Network mapper and port scanner
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button className="cyber-button">
            <Settings className="h-5 w-5 mr-2" />
            Advanced
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration Panel */}
        <div className="lg:col-span-1">
          <div className="terminal-window">
            <div className="terminal-header">
              <div className="flex items-center space-x-2">
                <Settings className="h-5 w-5 text-cyber-primary" />
                <span className="text-sm font-medium">Scan Configuration</span>
              </div>
            </div>
            <div className="terminal-content space-y-4">
              {/* Target Input */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Target
                </label>
                <input
                  type="text"
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-cyber-primary rounded text-cyber-primary font-mono"
                  placeholder="scanme.nmap.org"
                />
              </div>

              {/* Scan Type */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Scan Type
                </label>
                <select
                  value={scanType}
                  onChange={(e) => setScanType(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-cyber-primary rounded text-cyber-primary font-mono"
                >
                  {scanProfiles.map((profile) => (
                    <option key={profile.id} value={profile.id}>
                      {profile.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Ports */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Ports
                </label>
                <input
                  type="text"
                  value={ports}
                  onChange={(e) => setPorts(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-cyber-primary rounded text-cyber-primary font-mono"
                  placeholder="1-1000"
                />
              </div>

              {/* Scan Button */}
              <button
                onClick={handleScan}
                disabled={isRunning}
                className="w-full cyber-button flex items-center justify-center"
              >
                {isRunning ? (
                  <>
                    <Activity className="h-5 w-5 mr-2 animate-spin" />
                    Scanning...
                  </>
                ) : (
                  <>
                    <Play className="h-5 w-5 mr-2" />
                    Start Scan
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Scan Profiles */}
          <div className="terminal-window mt-6">
            <div className="terminal-header">
              <div className="flex items-center space-x-2">
                <Target className="h-5 w-5 text-cyber-primary" />
                <span className="text-sm font-medium">Scan Profiles</span>
              </div>
            </div>
            <div className="terminal-content">
              <div className="space-y-3">
                {scanProfiles.map((profile) => (
                  <div
                    key={profile.id}
                    className={`p-3 border rounded cursor-pointer transition-colors ${
                      scanType === profile.id
                        ? 'border-cyber-primary bg-cyber-primary/10'
                        : 'border-cyber-primary/30 hover:border-cyber-primary/60'
                    }`}
                    onClick={() => setScanType(profile.id)}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium">{profile.name}</span>
                      <span className="text-xs text-cyber-light">{profile.estimatedTime}</span>
                    </div>
                    <p className="text-xs text-cyber-light opacity-75">{profile.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2">
          <div className="terminal-window">
            <div className="terminal-header">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Eye className="h-5 w-5 text-cyber-primary" />
                  <span className="text-sm font-medium">Scan Results</span>
                </div>
                {results && (
                  <button className="text-xs text-cyber-primary hover:text-cyber-light">
                    <Download className="h-4 w-4" />
                  </button>
                )}
              </div>
            </div>
            <div className="terminal-content">
              {results ? (
                <div className="space-y-4">
                  {/* Summary */}
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-cyber-primary">
                        {results.ports?.length || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Open Ports</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-neon-blue">
                        {results.execution_time}s
                      </div>
                      <div className="text-xs text-cyber-light">Scan Time</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-neon-green">
                        {results.host_status}
                      </div>
                      <div className="text-xs text-cyber-light">Host Status</div>
                    </div>
                  </div>

                  {/* Ports */}
                  {results.ports && results.ports.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-cyber-primary mb-3">Open Ports</h3>
                      <div className="space-y-2">
                        {results.ports.map((port: any, index: number) => (
                          <div key={index} className="flex items-center justify-between p-2 border border-cyber-primary/30 rounded">
                            <div className="flex items-center space-x-3">
                              <span className="text-sm font-mono text-cyber-primary">{port.port}</span>
                              <span className="text-sm text-cyber-light">{port.service}</span>
                              {port.version && (
                                <span className="text-xs text-cyber-light opacity-75">{port.version}</span>
                              )}
                            </div>
                            <span className="text-xs text-green-400">{port.state}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Raw Output */}
                  <div>
                    <h3 className="text-sm font-medium text-cyber-primary mb-3">Raw Output</h3>
                    <pre className="text-xs text-cyber-light bg-cyber-darker p-3 rounded border border-cyber-primary/30 overflow-auto max-h-64">
                      {results.output}
                    </pre>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <Globe className="h-16 w-16 text-cyber-primary mx-auto mb-4 opacity-50" />
                  <p className="text-cyber-light opacity-75">No scan results yet</p>
                  <p className="text-xs text-cyber-light opacity-50 mt-2">
                    Configure and run a scan to see results here
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
