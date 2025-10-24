'use client'

import { useState } from 'react'
import { Target, Shield, Brain, Terminal } from 'lucide-react'

export function QuickActions() {
  const [selectedAction, setSelectedAction] = useState<string | null>(null)

  const actions = [
    {
      id: 'nmap',
      label: 'Nmap Scan',
      icon: <Shield className="h-5 w-5" />,
      description: 'Quick network scan',
      color: 'border-cyber-primary text-cyber-primary hover:bg-cyber-primary hover:text-cyber-dark',
    },
    {
      id: 'gobuster',
      label: 'Gobuster Scan',
      icon: <Target className="h-5 w-5" />,
      description: 'Directory enumeration',
      color: 'border-neon-blue text-neon-blue hover:bg-neon-blue hover:text-cyber-dark',
    },
    {
      id: 'ai-analysis',
      label: 'AI Analysis',
      icon: <Brain className="h-5 w-5" />,
      description: 'Target analysis',
      color: 'border-neon-pink text-neon-pink hover:bg-neon-pink hover:text-cyber-dark',
    },
    {
      id: 'terminal',
      label: 'Terminal',
      icon: <Terminal className="h-5 w-5" />,
      description: 'Command execution',
      color: 'border-neon-green text-neon-green hover:bg-neon-green hover:text-cyber-dark',
    },
  ]

  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-cyber-primary"></div>
          <span className="text-sm font-medium">Quick Actions</span>
        </div>
      </div>
      <div className="terminal-content">
        <div className="space-y-3">
          {actions.map((action) => (
            <button
              key={action.id}
              onClick={() => setSelectedAction(action.id)}
              className={`w-full p-3 border rounded-lg transition-all duration-200 ${action.color} ${
                selectedAction === action.id ? 'ring-2 ring-current' : ''
              }`}
            >
              <div className="flex items-center space-x-3">
                {action.icon}
                <div className="text-left">
                  <div className="text-sm font-medium">{action.label}</div>
                  <div className="text-xs opacity-75">{action.description}</div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
