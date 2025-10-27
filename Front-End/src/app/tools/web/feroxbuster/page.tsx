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
  FileText,
  Repeat
} from 'lucide-react'
import Link from 'next/link'
import { apiClient } from '@/lib/api'
import { FeroxbusterExecution } from '@/types/api'

interface ScanProfile {
  id: string
  name: string
  description: string
  command: string
  estimatedTime: string
  depth: number
}

export default function FeroxbusterPage() {
  const [url, setUrl] = useState('https://target.com')
  const [wordlist, setWordlist] = useState('common.txt')
  const [depth, setDepth] = useState(2)
  const [threads, setThreads] = useState(50)
  const [extensions, setExtensions] = useState('php,html,txt')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<FeroxbusterExecution | null>(null)

  const scanProfiles: ScanProfile[] = [
    {
      id: 'shallow',
      name: 'Shallow Scan',
      description: 'Quick recursive scan with depth 1',
      command: 'feroxbuster -u url -w common.txt -d 1',
      estimatedTime: '30-60 seconds',
      depth: 1
    },
    {
      id: 'medium',
      name: 'Medium Depth',
      description: 'Moderate recursive depth',
      command: 'feroxbuster -u url -w common.txt -d 2',
      estimatedTime: '2-5 minutes',
      depth: 2
    },
    {
      id: 'deep',
      name: 'Deep Scan',
      description: 'Deep recursive exploration',
      command: 'feroxbuster -u url -w common.txt -d 3',
      estimatedTime: '5-10 minutes',
      depth: 3
    },
    {
      id: 'aggressive',
      name: 'Aggressive',
      description: 'Very deep recursive scan',
      command: 'feroxbuster -u url -w common.txt -d 5',
      estimatedTime: '15-30 minutes',
      depth: 5
    }
  ]

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const data = await apiClient.feroxbusterScan(url, wordlist, threads, depth)
      setResults(data as FeroxbusterExecution)
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
            <h1 className="text-3xl font-cyber font-bold text-neon-purple neon-glow">
              FEROXBUSTER
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              Fast recursive content discovery tool
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
                <Settings className="h-5 w-5 text-neon-purple" />
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
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-purple rounded text-cyber-primary font-mono"
                  placeholder="https://target.com"
                />
              </div>

              {/* Wordlist */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Wordlist
                </label>
                <select
                  value={wordlist}
                  onChange={(e) => setWordlist(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-purple rounded text-cyber-primary font-mono"
                >
                  <option value="common.txt">Common</option>
                  <option value="big.txt">Big</option>
                  <option value="small.txt">Small</option>
                </select>
              </div>

              {/* Depth */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Recursion Depth: {depth}
                </label>
                <input
                  type="range"
                  min="1"
                  max="5"
                  value={depth}
                  onChange={(e) => setDepth(parseInt(e.target.value))}
                  className="w-full"
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
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-purple rounded text-cyber-primary font-mono"
                  placeholder="50"
                  min="1"
                  max="200"
                />
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
                  className="w-full px-3 py-2 bg-cyber-dark border border-neon-purple rounded text-cyber-primary font-mono"
                  placeholder="php,html,txt"
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
                <Repeat className="h-5 w-5 text-neon-purple" />
                <span className="text-sm font-medium">Scan Profiles</span>
              </div>
            </div>
            <div className="terminal-content">
              <div className="space-y-3">
                {scanProfiles.map((profile) => (
                  <div
                    key={profile.id}
                    className={`p-3 border rounded cursor-pointer transition-colors ${
                      depth === profile.depth
                        ? 'border-neon-purple bg-neon-purple/10'
                        : 'border-neon-purple/30 hover:border-neon-purple/60'
                    }`}
                    onClick={() => setDepth(profile.depth)}
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
                  <Eye className="h-5 w-5 text-neon-purple" />
                  <span className="text-sm font-medium">Scan Results</span>
                </div>
                {results && (
                  <button className="text-xs text-neon-purple hover:text-cyber-light">
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
                      <div className="text-2xl font-cyber font-bold text-neon-purple">
                        {results.found_directories?.length || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Directories</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-neon-green">
                        {results.found_files?.length || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Files</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-neon-pink">
                        {results.total_requests || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Requests</div>
                    </div>
                  </div>

                  {/* Directories */}
                  {results.found_directories && results.found_directories.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-neon-purple mb-3">Directories Found</h3>
                      <div className="space-y-2 max-h-64 overflow-auto">
                        {results.found_directories.map((dir: string, index: number) => (
                          <div key={index} className="flex items-center space-x-3 p-2 border border-neon-purple/30 rounded">
                            <FileText className="h-4 w-4 text-neon-purple" />
                            <span className="text-sm font-mono text-cyber-primary">{dir}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Files */}
                  {results.found_files && results.found_files.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-neon-purple mb-3">Files Found</h3>
                      <div className="space-y-2 max-h-64 overflow-auto">
                        {results.found_files.map((file: string, index: number) => (
                          <div key={index} className="flex items-center space-x-3 p-2 border border-neon-purple/30 rounded">
                            <FileText className="h-4 w-4 text-neon-green" />
                            <span className="text-sm font-mono text-cyber-primary">{file}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Search className="h-16 w-16 text-neon-purple mx-auto mb-4 opacity-50" />
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
