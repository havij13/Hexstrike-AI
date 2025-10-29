'use client'

import { useState } from 'react'
import { 
  Home, 
  Activity, 
  Shield, 
  Brain, 
  Settings, 
  Terminal, 
  FileText,
  Database,
  Bug,
  Target,
  Zap
} from 'lucide-react'

interface SidebarItem {
  id: string
  label: string
  icon: React.ReactNode
  active?: boolean
}

export function Sidebar() {
  const [activeItem, setActiveItem] = useState('dashboard')

  const sidebarItems: SidebarItem[] = [
    { id: 'dashboard', label: 'Dashboard', icon: <Home className="h-5 w-5" /> },
    { id: 'processes', label: 'Processes', icon: <Activity className="h-5 w-5" /> },
    { id: 'security-tools', label: 'Security Tools', icon: <Shield className="h-5 w-5" /> },
    { id: 'ai-intelligence', label: 'AI Intelligence', icon: <Brain className="h-5 w-5" /> },
    { id: 'terminal', label: 'Terminal', icon: <Terminal className="h-5 w-5" /> },
    { id: 'files', label: 'File Manager', icon: <FileText className="h-5 w-5" /> },
    { id: 'cache', label: 'Cache', icon: <Database className="h-5 w-5" /> },
    { id: 'vulnerabilities', label: 'Vulnerabilities', icon: <Bug className="h-5 w-5" /> },
    { id: 'targets', label: 'Targets', icon: <Target className="h-5 w-5" /> },
    { id: 'settings', label: 'Settings', icon: <Settings className="h-5 w-5" /> },
  ]

  return (
    <aside className="w-64 bg-cyber-dark border-r border-cyber-primary flex flex-col">
      {/* Logo Section */}
      <div className="p-6 border-b border-cyber-primary">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-cyber-primary rounded-lg">
            <Zap className="h-6 w-6 text-cyber-dark" />
          </div>
          <div>
            <h2 className="text-lg font-cyber font-bold text-cyber-primary">
              HEXSTRIKE
            </h2>
            <p className="text-xs text-cyber-light font-mono">
              AI Framework
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {sidebarItems.map((item) => (
            <li key={item.id}>
              <a
                href={`/${item.id === 'dashboard' ? '' : item.id}`}
                onClick={() => setActiveItem(item.id)}
                className={`block w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  activeItem === item.id
                    ? 'bg-cyber-primary text-cyber-dark glow-border'
                    : 'text-cyber-light hover:text-cyber-primary hover:bg-cyber-gray'
                }`}
              >
                {item.icon}
                <span className="font-medium">{item.label}</span>
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {/* System Status */}
      <div className="p-4 border-t border-cyber-primary">
        <div className="space-y-3">
          <div className="text-xs text-cyber-light font-mono">
            SYSTEM STATUS
          </div>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-cyber-light">CPU</span>
              <span className="text-cyber-primary font-mono">23%</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-cyber-light">Memory</span>
              <span className="text-cyber-primary font-mono">67%</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-cyber-light">Active</span>
              <span className="text-cyber-primary font-mono">12</span>
            </div>
          </div>
        </div>
      </div>

      {/* Scan line effect */}
      <div className="scan-line opacity-10"></div>
    </aside>
  )
}
