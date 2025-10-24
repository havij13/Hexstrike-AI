'use client'

import { useState } from 'react'
import { 
  Shield, 
  Globe, 
  Search, 
  Play,
  Settings,
  ArrowLeft,
  Activity,
  Clock,
  Target,
  Bug
} from 'lucide-react'
import Link from 'next/link'

interface WebTool {
  id: string
  name: string
  description: string
  icon: React.ReactNode
  status: 'available' | 'running' | 'completed'
  lastRun?: string
  href: string
}

export default function WebToolsPage() {
  const [selectedTool, setSelectedTool] = useState<string | null>(null)

  const webTools: WebTool[] = [
    {
      id: 'gobuster',
      name: 'Gobuster',
      description: 'Directory/file brute-forcing tool for web applications',
      icon: <Search className="h-6 w-6" />,
      status: 'available',
      lastRun: '3 minutes ago',
      href: '/tools/web/gobuster'
    },
    {
      id: 'feroxbuster',
      name: 'Feroxbuster',
      description: 'Fast recursive content discovery tool',
      icon: <Globe className="h-6 w-6" />,
      status: 'available',
      lastRun: '5 minutes ago',
      href: '/tools/web/feroxbuster'
    },
    {
      id: 'nuclei',
      name: 'Nuclei',
      description: 'Vulnerability scanner based on templates',
      icon: <Bug className="h-6 w-6" />,
      status: 'available',
      href: '/tools/web/nuclei'
    },
    {
      id: 'nikto',
      name: 'Nikto',
      description: 'Web server vulnerability scanner',
      icon: <Shield className="h-6 w-6" />,
      status: 'available',
      href: '/tools/web/nikto'
    },
    {
      id: 'sqlmap',
      name: 'SQLMap',
      description: 'Automatic SQL injection testing tool',
      icon: <Target className="h-6 w-6" />,
      status: 'available',
      href: '/tools/web/sqlmap'
    },
    {
      id: 'wpscan',
      name: 'WPScan',
      description: 'WordPress vulnerability scanner',
      icon: <Globe className="h-6 w-6" />,
      status: 'available',
      href: '/tools/web/wpscan'
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return 'text-green-400'
      case 'running':
        return 'text-yellow-400'
      case 'completed':
        return 'text-neon-blue'
      default:
        return 'text-cyber-light'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available':
        return <Shield className="h-4 w-4" />
      case 'running':
        return <Activity className="h-4 w-4 animate-pulse" />
      case 'completed':
        return <Clock className="h-4 w-4" />
      default:
        return <Shield className="h-4 w-4" />
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link href="/tools" className="text-cyber-primary hover:text-cyber-light transition-colors">
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
              WEB APPLICATION SECURITY TOOLS
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              Web application testing and vulnerability scanning tools
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button className="cyber-button">
            <Settings className="h-5 w-5 mr-2" />
            Configure
          </button>
        </div>
      </div>

      {/* Tools Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {webTools.map((tool) => (
          <div
            key={tool.id}
            className={`terminal-window border-neon-blue text-neon-blue hover:bg-neon-blue hover:text-cyber-dark transition-all duration-300 cursor-pointer group`}
            onClick={() => setSelectedTool(tool.id)}
          >
            <div className="terminal-header">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {tool.icon}
                  <span className="text-lg font-cyber font-bold">{tool.name}</span>
                </div>
                <div className={`flex items-center space-x-1 ${getStatusColor(tool.status)}`}>
                  {getStatusIcon(tool.status)}
                  <span className="text-xs font-mono">{tool.status}</span>
                </div>
              </div>
            </div>
            <div className="terminal-content">
              <p className="text-sm mb-4 opacity-90">
                {tool.description}
              </p>
              <div className="space-y-2">
                {tool.lastRun && (
                  <div className="text-xs font-mono text-cyber-light opacity-75">
                    Last run: {tool.lastRun}
                  </div>
                )}
                <div className="flex items-center justify-between pt-2 border-t border-neon-blue/30">
                  <span className="text-xs font-mono">
                    Click to configure and run
                  </span>
                  <Play className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="terminal-window">
        <div className="terminal-header">
          <div className="flex items-center space-x-2">
            <Search className="h-5 w-5 text-neon-blue" />
            <span className="text-sm font-medium">Quick Actions</span>
          </div>
        </div>
        <div className="terminal-content">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <button className="cyber-button text-sm">
              <Search className="h-4 w-4 mr-2" />
              Directory Scan
            </button>
            <button className="cyber-button text-sm">
              <Bug className="h-4 w-4 mr-2" />
              Vulnerability Scan
            </button>
            <button className="cyber-button text-sm">
              <Target className="h-4 w-4 mr-2" />
              SQL Injection Test
            </button>
            <button className="cyber-button text-sm">
              <Settings className="h-4 w-4 mr-2" />
              Custom Scan
            </button>
          </div>
        </div>
      </div>

      {/* Recent Scans */}
      <div className="terminal-window">
        <div className="terminal-header">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-neon-blue"></div>
            <span className="text-sm font-medium">Recent Web Scans</span>
          </div>
        </div>
        <div className="terminal-content">
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 border border-neon-blue/30 rounded">
              <div className="flex items-center space-x-3">
                <Search className="h-5 w-5 text-neon-blue" />
                <div>
                  <div className="text-sm font-medium">Gobuster - target.com</div>
                  <div className="text-xs text-cyber-light">Directories: admin, backup, config</div>
                </div>
              </div>
              <div className="text-xs text-cyber-light">
                {new Date().toLocaleTimeString()}
              </div>
            </div>
            <div className="flex items-center justify-between p-3 border border-neon-blue/30 rounded">
              <div className="flex items-center space-x-3">
                <Bug className="h-5 w-5 text-neon-pink" />
                <div>
                  <div className="text-sm font-medium">Nuclei - api.target.com</div>
                  <div className="text-xs text-cyber-light">Vulnerabilities: 3 found</div>
                </div>
              </div>
              <div className="text-xs text-cyber-light">
                {new Date(Date.now() - 10 * 60 * 1000).toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
