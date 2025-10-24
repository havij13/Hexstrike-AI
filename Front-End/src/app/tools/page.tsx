'use client'

import { useState } from 'react'
import { 
  Shield, 
  Globe, 
  Key, 
  Binary, 
  Cloud, 
  Zap,
  ArrowRight,
  Play,
  Settings,
  BookOpen
} from 'lucide-react'

interface ToolCategory {
  id: string
  name: string
  description: string
  icon: React.ReactNode
  tools: string[]
  color: string
  href: string
}

export default function ToolsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  const categories: ToolCategory[] = [
    {
      id: 'network',
      name: 'Network Security',
      description: 'Network reconnaissance, port scanning, and network analysis tools',
      icon: <Globe className="h-8 w-8" />,
      tools: ['Nmap', 'Rustscan', 'Masscan'],
      color: 'border-cyber-primary text-cyber-primary hover:bg-cyber-primary hover:text-cyber-dark',
      href: '/tools/network'
    },
    {
      id: 'web',
      name: 'Web Application Security',
      description: 'Web application testing, directory enumeration, and vulnerability scanning',
      icon: <Shield className="h-8 w-8" />,
      tools: ['Gobuster', 'Feroxbuster', 'Nuclei', 'Nikto', 'SQLMap', 'WPScan'],
      color: 'border-neon-blue text-neon-blue hover:bg-neon-blue hover:text-cyber-dark',
      href: '/tools/web'
    },
    {
      id: 'auth',
      name: 'Authentication & Password Security',
      description: 'Password cracking, authentication testing, and credential analysis',
      icon: <Key className="h-8 w-8" />,
      tools: ['Hydra', 'John the Ripper', 'Hashcat'],
      color: 'border-neon-pink text-neon-pink hover:bg-neon-pink hover:text-cyber-dark',
      href: '/tools/auth'
    },
    {
      id: 'binary',
      name: 'Binary Analysis & Reverse Engineering',
      description: 'Binary analysis, reverse engineering, and debugging tools',
      icon: <Binary className="h-8 w-8" />,
      tools: ['Ghidra', 'Radare2', 'GDB'],
      color: 'border-neon-green text-neon-green hover:bg-neon-green hover:text-cyber-dark',
      href: '/tools/binary'
    },
    {
      id: 'cloud',
      name: 'Cloud & Container Security',
      description: 'Cloud security assessment and container analysis tools',
      icon: <Cloud className="h-8 w-8" />,
      tools: ['Prowler', 'Trivy', 'Kube-Hunter'],
      color: 'border-neon-orange text-neon-orange hover:bg-neon-orange hover:text-cyber-dark',
      href: '/tools/cloud'
    }
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-cyber font-bold text-cyber-primary neon-glow">
            SECURITY TOOLS
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Comprehensive security testing toolkit
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <button className="cyber-button">
            <Settings className="h-5 w-5 mr-2" />
            Settings
          </button>
          <button className="cyber-button">
            <BookOpen className="h-5 w-5 mr-2" />
            Documentation
          </button>
        </div>
      </div>

      {/* Tool Categories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {categories.map((category) => (
          <div
            key={category.id}
            className={`terminal-window ${category.color} transition-all duration-300 cursor-pointer group`}
            onClick={() => setSelectedCategory(category.id)}
          >
            <div className="terminal-header">
              <div className="flex items-center space-x-3">
                {category.icon}
                <span className="text-lg font-cyber font-bold">{category.name}</span>
              </div>
            </div>
            <div className="terminal-content">
              <p className="text-sm mb-4 opacity-90">
                {category.description}
              </p>
              <div className="space-y-2">
                <div className="text-xs font-mono text-cyber-light opacity-75">
                  Available Tools:
                </div>
                <div className="flex flex-wrap gap-1">
                  {category.tools.map((tool, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-cyber-gray text-xs rounded border border-cyber-primary/30"
                    >
                      {tool}
                    </span>
                  ))}
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-cyber-primary/30">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono">
                    {category.tools.length} tools available
                  </span>
                  <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
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
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="cyber-button text-sm">
              <Play className="h-4 w-4 mr-2" />
              Run All Tests
            </button>
            <button className="cyber-button text-sm">
              <Settings className="h-4 w-4 mr-2" />
              Configure Tools
            </button>
            <button className="cyber-button text-sm">
              <BookOpen className="h-4 w-4 mr-2" />
              View Documentation
            </button>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="terminal-window">
        <div className="terminal-header">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-cyber-primary"></div>
            <span className="text-sm font-medium">Recent Tool Executions</span>
          </div>
        </div>
        <div className="terminal-content">
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 border border-cyber-primary/30 rounded">
              <div className="flex items-center space-x-3">
                <Globe className="h-5 w-5 text-cyber-primary" />
                <div>
                  <div className="text-sm font-medium">Nmap Scan</div>
                  <div className="text-xs text-cyber-light">scanme.nmap.org</div>
                </div>
              </div>
              <div className="text-xs text-cyber-light">
                {new Date().toLocaleTimeString()}
              </div>
            </div>
            <div className="flex items-center justify-between p-3 border border-cyber-primary/30 rounded">
              <div className="flex items-center space-x-3">
                <Shield className="h-5 w-5 text-neon-blue" />
                <div>
                  <div className="text-sm font-medium">Gobuster Scan</div>
                  <div className="text-xs text-cyber-light">target.com</div>
                </div>
              </div>
              <div className="text-xs text-cyber-light">
                {new Date(Date.now() - 5 * 60 * 1000).toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
