'use client'

import { useState } from 'react'
import { 
  Globe, 
  Zap, 
  Target, 
  Play,
  Settings,
  ArrowLeft,
  Activity,
  Clock,
  Shield
} from 'lucide-react'
import Link from 'next/link'

interface NetworkTool {
  id: string
  name: string
  description: string
  icon: React.ReactNode
  status: 'available' | 'running' | 'completed'
  lastRun?: string
  href: string
}

export default function NetworkToolsPage() {
  const [selectedTool, setSelectedTool] = useState<string | null>(null)

  const networkTools: NetworkTool[] = [
    {
      id: 'nmap',
      name: 'Nmap',
      description: 'Network mapper and port scanner for network discovery and security auditing',
      icon: <Globe className="h-6 w-6" />,
      status: 'available',
      lastRun: '2 minutes ago',
      href: '/tools/network/nmap'
    },
    {
      id: 'rustscan',
      name: 'Rustscan',
      description: 'Fast port scanner written in Rust, designed for speed and efficiency',
      icon: <Zap className="h-6 w-6" />,
      status: 'available',
      lastRun: '5 minutes ago',
      href: '/tools/network/rustscan'
    },
    {
      id: 'masscan',
      name: 'Masscan',
      description: 'High-speed network port scanner, capable of scanning the entire internet in minutes',
      icon: <Target className="h-6 w-6" />,
      status: 'available',
      href: '/tools/network/masscan'
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return 'text-green-400'
      case 'running':
        return 'text-yellow-400'
      case 'completed':
        return 'text-cyber-primary'
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
            <h1 className="text-3xl font-cyber font-bold text-cyber-primary neon-glow">
              NETWORK SECURITY TOOLS
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              Network reconnaissance and port scanning tools
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
        {networkTools.map((tool) => (
          <div
            key={tool.id}
            className={`terminal-window border-cyber-primary text-cyber-primary hover:bg-cyber-primary hover:text-cyber-dark transition-all duration-300 cursor-pointer group`}
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
                <div className="flex items-center justify-between pt-2 border-t border-cyber-primary/30">
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
            <Zap className="h-5 w-5 text-cyber-primary" />
            <span className="text-sm font-medium">Quick Actions</span>
          </div>
        </div>
        <div className="terminal-content">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <button className="cyber-button text-sm">
              <Globe className="h-4 w-4 mr-2" />
              Quick Scan
            </button>
            <button className="cyber-button text-sm">
              <Target className="h-4 w-4 mr-2" />
              Port Scan
            </button>
            <button className="cyber-button text-sm">
              <Activity className="h-4 w-4 mr-2" />
              Service Detection
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
            <div className="w-3 h-3 rounded-full bg-cyber-primary"></div>
            <span className="text-sm font-medium">Recent Network Scans</span>
          </div>
        </div>
        <div className="terminal-content">
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 border border-cyber-primary/30 rounded">
              <div className="flex items-center space-x-3">
                <Globe className="h-5 w-5 text-cyber-primary" />
                <div>
                  <div className="text-sm font-medium">Nmap - scanme.nmap.org</div>
                  <div className="text-xs text-cyber-light">Ports: 22, 80, 443, 9929</div>
                </div>
              </div>
              <div className="text-xs text-cyber-light">
                {new Date().toLocaleTimeString()}
              </div>
            </div>
            <div className="flex items-center justify-between p-3 border border-cyber-primary/30 rounded">
              <div className="flex items-center space-x-3">
                <Zap className="h-5 w-5 text-neon-blue" />
                <div>
                  <div className="text-sm font-medium">Rustscan - 192.168.1.0/24</div>
                  <div className="text-xs text-cyber-light">Fast network discovery</div>
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
