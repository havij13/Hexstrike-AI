'use client'

import { useState } from 'react'
import { 
  Search, 
  Play, 
  Settings, 
  ArrowLeft,
  Target,
  Clock,
  Activity,
  Download,
  Eye,
  FileText
} from 'lucide-react'
import Link from 'next/link'

interface ScanProfile {
  id: string
  name: string
  description: string
  command: string
  estimatedTime: string
  extensions: string[]
}

export default function GobusterPage() {
  const [url, setUrl] = useState('https://target.com')
  const [mode, setMode] = useState('dir')
  const [wordlist, setWordlist] = useState('common.txt')
  const [extensions, setExtensions] = useState('php,html,txt')
  const [threads, setThreads] = useState(50)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)

  const scanProfiles: ScanProfile[] = [
    {
      id: 'quick',
      name: 'Quick Directory Scan',
      description: 'Fast directory enumeration with common extensions',
      command: 'gobuster dir -u target -w common.txt -x php,html,txt',
      estimatedTime: '30-60 seconds',
      extensions: ['php', 'html', 'txt']
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Scan',
      description: 'Full enumeration with multiple extensions',
      command: 'gobuster dir -u target -w big.txt -x php,html,txt,jsp,asp',
      estimatedTime: '5-10 minutes',
      extensions: ['php', 'html', 'txt', 'jsp', 'asp']
    },
    {
      id: 'files',
      name: 'File Enumeration',
      description: 'Focus on file discovery',
      command: 'gobuster dir -u target -w files.txt -x php,html,txt,js,css',
      estimatedTime: '2-5 minutes',
      extensions: ['php', 'html', 'txt', 'js', 'css']
    },
    {
      id: 'dns',
      name: 'DNS Subdomain Scan',
      description: 'Subdomain enumeration',
      command: 'gobuster dns -d target.com -w subdomains.txt',
      estimatedTime: '1-3 minutes',
      extensions: []
    }
  ]

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          mode,
          wordlist,
          extensions: extensions.split(','),
          threads,
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
          <Link href="/tools/web" className="text-cyber-primary hover:text-cyber-light transition-colors">
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
              GOBUSTER
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              Directory/file brute-forcing tool
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
                <Settings className="h-5 w-5 text-neon-blue" />
                <span className="text-sm font-medium">Scan Configuration</span>
              </div>
            </div>
            <div className="terminal-content space-y-4">
              {/* URL Input */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Target URL
                </label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-blue rounded text-cyber-primary font-mono"
                  placeholder="https://target.com"
                />
              </div>

              {/* Mode */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Scan Mode
                </label>
                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-blue rounded text-cyber-primary font-mono"
                >
                  <option value="dir">Directory Scan</option>
                  <option value="dns">DNS Subdomain Scan</option>
                  <option value="s3">S3 Bucket Scan</option>
                </select>
              </div>

              {/* Wordlist */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Wordlist
                </label>
                <select
                  value={wordlist}
                  onChange={(e) => setWordlist(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-blue rounded text-cyber-primary font-mono"
                >
                  <option value="common.txt">Common</option>
                  <option value="big.txt">Big</option>
                  <option value="subdomains.txt">Subdomains</option>
                  <option value="files.txt">Files</option>
                </select>
              </div>

              {/* Extensions */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Extensions
                </label>
                <input
                  type="text"
                  value={extensions}
                  onChange={(e) => setExtensions(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-blue rounded text-cyber-primary font-mono"
                  placeholder="php,html,txt"
                />
              </div>

              {/* Threads */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Threads
                </label>
                <input
                  type="number"
                  value={threads}
                  onChange={(e) => setThreads(parseInt(e.target.value))}
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-blue rounded text-cyber-primary font-mono"
                  placeholder="50"
                  min="1"
                  max="200"
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
                <Target className="h-5 w-5 text-neon-blue" />
                <span className="text-sm font-medium">Scan Profiles</span>
              </div>
            </div>
            <div className="terminal-content">
              <div className="space-y-3">
                {scanProfiles.map((profile) => (
                  <div
                    key={profile.id}
                    className={`p-3 border rounded cursor-pointer transition-colors ${
                      mode === profile.id
                        ? 'border-neon-blue bg-neon-blue/10'
                        : 'border-neon-blue/30 hover:border-neon-blue/60'
                    }`}
                    onClick={() => {
                      setMode(profile.id)
                      setExtensions(profile.extensions.join(','))
                    }}
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
                  <Eye className="h-5 w-5 text-neon-blue" />
                  <span className="text-sm font-medium">Scan Results</span>
                </div>
                {results && (
                  <button className="text-xs text-neon-blue hover:text-cyber-light">
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
                      <div className="text-2xl font-cyber font-bold text-neon-blue">
                        {results.directories_found?.length || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Directories Found</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-neon-green">
                        {results.files_found?.length || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Files Found</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-neon-pink">
                        {results.total_requests || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Total Requests</div>
                    </div>
                  </div>

                  {/* Directories */}
                  {results.directories_found && results.directories_found.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-neon-blue mb-3">Directories Found</h3>
                      <div className="space-y-2">
                        {results.directories_found.map((dir: string, index: number) => (
                          <div key={index} className="flex items-center space-x-3 p-2 border border-neon-blue/30 rounded">
                            <FileText className="h-4 w-4 text-neon-blue" />
                            <span className="text-sm font-mono text-cyber-primary">{dir}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Files */}
                  {results.files_found && results.files_found.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-neon-blue mb-3">Files Found</h3>
                      <div className="space-y-2">
                        {results.files_found.map((file: string, index: number) => (
                          <div key={index} className="flex items-center space-x-3 p-2 border border-neon-blue/30 rounded">
                            <FileText className="h-4 w-4 text-neon-green" />
                            <span className="text-sm font-mono text-cyber-primary">{file}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Raw Output */}
                  <div>
                    <h3 className="text-sm font-medium text-neon-blue mb-3">Raw Output</h3>
                    <pre className="text-xs text-cyber-light bg-cyber-darker p-3 rounded border border-neon-blue/30 overflow-auto max-h-64">
                      {results.output}
                    </pre>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <Search className="h-16 w-16 text-neon-blue mx-auto mb-4 opacity-50" />
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
