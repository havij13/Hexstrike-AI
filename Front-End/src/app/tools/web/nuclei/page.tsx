'use client'

import { useState } from 'react'
import { 
  Shield, 
  Play, 
  Settings, 
  ArrowLeft,
  Target,
  Clock,
  Activity,
  Download,
  Eye,
  AlertTriangle,
  CheckCircle
} from 'lucide-react'
import Link from 'next/link'
import { apiClient } from '@/lib/api'
import { NucleiExecution } from '@/types/api'

interface ScanProfile {
  id: string
  name: string
  description: string
  command: string
  estimatedTime: string
  template: string
  severity: string
}

export default function NucleiPage() {
  const [target, setTarget] = useState('https://target.com')
  const [template, setTemplate] = useState('all')
  const [severity, setSeverity] = useState('critical,high,medium')
  const [tags, setTags] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<NucleiExecution | null>(null)

  const scanProfiles: ScanProfile[] = [
    {
      id: 'cves',
      name: 'CVE Scan',
      description: 'Common vulnerabilities and exposures',
      command: 'nuclei -u target -t cves/',
      estimatedTime: '5-10 minutes',
      template: 'cves/',
      severity: 'critical,high,medium'
    },
    {
      id: 'exposures',
      name: 'Exposures',
      description: 'Exposed services and information disclosure',
      command: 'nuclei -u target -t exposures/',
      estimatedTime: '3-5 minutes',
      template: 'exposures/',
      severity: 'critical,high'
    },
    {
      id: 'misconfig',
      name: 'Misconfigurations',
      description: 'Configuration issues and security misconfigurations',
      command: 'nuclei -u target -t misconfiguration/',
      estimatedTime: '5-10 minutes',
      template: 'misconfiguration/',
      severity: 'high,medium'
    },
    {
      id: 'quick',
      name: 'Quick Scan',
      description: 'Fast scan for common issues',
      command: 'nuclei -u target -severity critical,high',
      estimatedTime: '1-3 minutes',
      template: 'all',
      severity: 'critical,high'
    }
  ]

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const data = await apiClient.nucleiScan(target, severity, tags, template)
      setResults(data as NucleiExecution)
    } catch (error) {
      console.error('Scan failed:', error)
    } finally {
      setIsRunning(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'text-red-400 border-red-500'
      case 'high':
        return 'text-orange-400 border-orange-500'
      case 'medium':
        return 'text-yellow-400 border-yellow-500'
      case 'low':
        return 'text-blue-400 border-blue-500'
      default:
        return 'text-cyber-light border-cyber-primary'
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
            <h1 className="text-3xl font-cyber font-bold text-red-500 neon-glow">
              NUCLEI
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              Fast vulnerability scanner with 4000+ templates
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
                <Settings className="h-5 w-5 text-red-500" />
                <span className="text-sm font-medium">Scan Configuration</span>
              </div>
            </div>
            <div className="terminal-content space-y-4">
              {/* Target Input */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Target URL
                </label>
                <input
                  type="url"
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-red-500 rounded text-cyber-primary font-mono"
                  placeholder="https://target.com"
                />
              </div>

              {/* Template Selection */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Template Category
                </label>
                <select
                  value={template}
                  onChange={(e) => setTemplate(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-red-500 rounded text-cyber-primary font-mono"
                >
                  <option value="all">All Templates</option>
                  <option value="cves/">CVEs</option>
                  <option value="exposures/">Exposures</option>
                  <option value="misconfiguration/">Misconfiguration</option>
                  <option value="vulnerabilities/">Vulnerabilities</option>
                </select>
              </div>

              {/* Severity */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Severity Filter
                </label>
                <input
                  type="text"
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-red-500 rounded text-cyber-primary font-mono"
                  placeholder="critical,high,medium"
                />
                <div className="mt-2 flex flex-wrap gap-2">
                  {['critical', 'high', 'medium', 'low'].map((sev) => (
                    <label key={sev} className="flex items-center space-x-1 text-xs">
                      <input
                        type="checkbox"
                        checked={severity.includes(sev)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSeverity([...severity.split(','), sev].filter(Boolean).join(','))
                          } else {
                            setSeverity(severity.split(',').filter(s => s !== sev).join(','))
                          }
                        }}
                        className="rounded"
                      />
                      <span className="capitalize">{sev}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Tags */}
              <div>
                <label className="block text-sm font-medium text-cyber-light mb-2">
                  Tags
                </label>
                <input
                  type="text"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  className="w-full px-3 py-2 bg-cyber-dark border border-red-500 rounded text-cyber-primary font-mono"
                  placeholder="xss,sqli,lfi"
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
                <Shield className="h-5 w-5 text-red-500" />
                <span className="text-sm font-medium">Scan Profiles</span>
              </div>
            </div>
            <div className="terminal-content">
              <div className="space-y-3">
                {scanProfiles.map((profile) => (
                  <div
                    key={profile.id}
                    className={`p-3 border rounded cursor-pointer transition-colors ${
                      template === profile.template && severity === profile.severity
                        ? 'border-red-500 bg-red-500/10'
                        : 'border-red-500/30 hover:border-red-500/60'
                    }`}
                    onClick={() => {
                      setTemplate(profile.template)
                      setSeverity(profile.severity)
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
                  <Eye className="h-5 w-5 text-red-500" />
                  <span className="text-sm font-medium">Vulnerability Scan Results</span>
                </div>
                {results && (
                  <button className="text-xs text-red-500 hover:text-cyber-light">
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
                      <div className="text-2xl font-cyber font-bold text-red-500">
                        {results.total_vulnerabilities || 0}
                      </div>
                      <div className="text-xs text-cyber-light">Vulnerabilities</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-green-400">
                        {results.execution_time}s
                      </div>
                      <div className="text-xs text-cyber-light">Scan Time</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-cyber font-bold text-neon-blue">
                        {results.success ? 'Success' : 'Failed'}
                      </div>
                      <div className="text-xs text-cyber-light">Status</div>
                    </div>
                  </div>

                  {/* Vulnerabilities */}
                  {results.vulnerabilities && results.vulnerabilities.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium text-red-500 mb-3">Detected Vulnerabilities</h3>
                      <div className="space-y-3 max-h-96 overflow-auto">
                        {results.vulnerabilities.map((vuln, index) => (
                          <div key={index} className={`border-2 rounded-lg p-4 ${getSeverityColor(vuln.severity)}`}>
                            <div className="flex items-start justify-between mb-2">
                              <div>
                                <h4 className="font-bold text-lg">{vuln.name}</h4>
                                <p className="text-sm text-cyber-light">Template: {vuln.template_id}</p>
                              </div>
                              <span className={`px-2 py-1 rounded text-xs font-bold border ${getSeverityColor(vuln.severity)}`}>
                                {vuln.severity.toUpperCase()}
                              </span>
                            </div>
                            <p className="text-sm text-cyber-light mb-2">{vuln.description}</p>
                            <div className="flex items-center justify-between text-xs">
                              <span className="text-cyber-light">URL: {vuln.url}</span>
                              <span className="text-cyber-light">{new Date(vuln.matched_at).toLocaleString()}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {(!results.vulnerabilities || results.vulnerabilities.length === 0) && (
                    <div className="text-center py-8">
                      <CheckCircle className="h-16 w-16 text-green-400 mx-auto mb-4" />
                      <p className="text-green-400">No vulnerabilities found</p>
                      <p className="text-xs text-cyber-light mt-2">
                        Target appears to be secure or outside scan scope
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Shield className="h-16 w-16 text-red-500 mx-auto mb-4 opacity-50" />
                  <p className="text-cyber-light opacity-75">No scan results yet</p>
                  <p className="text-xs text-cyber-light opacity-50 mt-2">
                    Configure and run a vulnerability scan to see results here
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
