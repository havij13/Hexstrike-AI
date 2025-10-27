'use client'

import { useState } from 'react'
import { Download, Copy, Check, Eye, FileText, Code } from 'lucide-react'

interface ResultsPanelProps {
  results: any
  onExport?: () => void
}

export function ResultsPanel({ results, onExport }: ResultsPanelProps) {
  const [activeTab, setActiveTab] = useState<'summary' | 'raw' | 'parsed'>('summary')
  const [copied, setCopied] = useState(false)

  const handleCopy = async (text: string) => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleExport = () => {
    if (onExport) {
      onExport()
    } else {
      const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `scan-results-${Date.now()}.json`
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  const renderSummary = () => {
    if (!results) return null

    // Extract summary data based on tool type
    const summary = {
      executionTime: results.execution_time || 'N/A',
      status: results.status || 'unknown',
      timestamp: results.timestamp || new Date().toISOString(),
    }

    return (
      <div className="space-y-4">
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 border border-neon-blue/30 rounded">
            <div className="text-2xl font-cyber font-bold text-neon-blue">
              {typeof summary.executionTime === 'number' ? `${summary.executionTime}s` : summary.executionTime}
            </div>
            <div className="text-xs text-cyber-light mt-1">Execution Time</div>
          </div>
          <div className="text-center p-4 border border-neon-blue/30 rounded">
            <div className={`text-2xl font-cyber font-bold ${summary.status === 'success' ? 'text-neon-green' : 'text-neon-pink'}`}>
              {summary.status.toUpperCase()}
            </div>
            <div className="text-xs text-cyber-light mt-1">Status</div>
          </div>
          <div className="text-center p-4 border border-neon-blue/30 rounded">
            <div className="text-sm font-cyber text-neon-blue">
              {new Date(summary.timestamp).toLocaleString()}
            </div>
            <div className="text-xs text-cyber-light mt-1">Timestamp</div>
          </div>
        </div>

        {/* Tool-specific summary */}
        {results.directories_found && (
          <div>
            <h3 className="text-sm font-medium text-neon-blue mb-2">Directories Found: {results.directories_found.length}</h3>
          </div>
        )}

        {results.files_found && (
          <div>
            <h3 className="text-sm font-medium text-neon-green mb-2">Files Found: {results.files_found.length}</h3>
          </div>
        )}

        {results.vulnerabilities && (
          <div>
            <h3 className="text-sm font-medium text-neon-pink mb-2">Vulnerabilities Found: {results.vulnerabilities.length}</h3>
          </div>
        )}
      </div>
    )
  }

  const renderRaw = () => {
    if (!results || !results.output) return null

    return (
      <div className="relative">
        <pre className="text-xs text-cyber-light bg-cyber-darker p-4 rounded border border-neon-blue/30 overflow-auto max-h-96 font-mono">
          {results.output}
        </pre>
        <button
          onClick={() => handleCopy(results.output)}
          className="absolute top-2 right-2 p-2 bg-cyber-dark border border-neon-blue rounded hover:bg-neon-blue hover:text-cyber-dark transition-colors"
        >
          {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
        </button>
      </div>
    )
  }

  const renderParsed = () => {
    if (!results) return null

    // Render parsed data based on tool type
    return (
      <div className="space-y-4">
        {results.directories_found && results.directories_found.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-neon-blue mb-3">Directories</h3>
            <div className="space-y-2">
              {results.directories_found.map((dir: string, index: number) => (
                <div key={index} className="flex items-center space-x-2 p-2 border border-neon-blue/30 rounded">
                  <FileText className="h-4 w-4 text-neon-blue" />
                  <span className="text-sm font-mono text-cyber-primary">{dir}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {results.files_found && results.files_found.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-neon-green mb-3">Files</h3>
            <div className="space-y-2">
              {results.files_found.map((file: string, index: number) => (
                <div key={index} className="flex items-center space-x-2 p-2 border border-neon-green/30 rounded">
                  <FileText className="h-4 w-4 text-neon-green" />
                  <span className="text-sm font-mono text-cyber-primary">{file}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center space-x-2">
            <Eye className="h-5 w-5 text-neon-blue" />
            <span className="text-sm font-medium">Scan Results</span>
          </div>
          {results && (
            <div className="flex items-center space-x-2">
              <button
                onClick={handleExport}
                className="p-1.5 text-neon-blue hover:bg-neon-blue/20 rounded transition-colors"
                title="Export results"
              >
                <Download className="h-4 w-4" />
              </button>
            </div>
          )}
        </div>
      </div>

      {results ? (
        <>
          <div className="flex border-b border-neon-blue/30">
            <button
              onClick={() => setActiveTab('summary')}
              className={`px-4 py-2 text-sm font-medium transition-colors ${
                activeTab === 'summary'
                  ? 'text-neon-blue border-b-2 border-neon-blue'
                  : 'text-cyber-light hover:text-neon-blue'
              }`}
            >
              Summary
            </button>
            <button
              onClick={() => setActiveTab('raw')}
              className={`px-4 py-2 text-sm font-medium transition-colors ${
                activeTab === 'raw'
                  ? 'text-neon-blue border-b-2 border-neon-blue'
                  : 'text-cyber-light hover:text-neon-blue'
              }`}
            >
              <div className="flex items-center space-x-1">
                <Code className="h-4 w-4" />
                <span>Raw</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('parsed')}
              className={`px-4 py-2 text-sm font-medium transition-colors ${
                activeTab === 'parsed'
                  ? 'text-neon-blue border-b-2 border-neon-blue'
                  : 'text-cyber-light hover:text-neon-blue'
              }`}
            >
              <div className="flex items-center space-x-1">
                <FileText className="h-4 w-4" />
                <span>Parsed</span>
              </div>
            </button>
          </div>

          <div className="terminal-content p-6">
            {activeTab === 'summary' && renderSummary()}
            {activeTab === 'raw' && renderRaw()}
            {activeTab === 'parsed' && renderParsed()}
          </div>
        </>
      ) : (
        <div className="terminal-content text-center py-12">
          <Eye className="h-16 w-16 text-neon-blue mx-auto mb-4 opacity-50" />
          <p className="text-cyber-light opacity-75">No results yet</p>
          <p className="text-xs text-cyber-light opacity-50 mt-2">
            Run a scan to see results here
          </p>
        </div>
      )}
    </div>
  )
}
