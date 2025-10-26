'use client'

import { ReactNode } from 'react'
import { Settings, Play, Activity } from 'lucide-react'

interface ToolFormProps {
  title: string
  subtitle?: string
  icon?: ReactNode
  isRunning: boolean
  onSubmit: () => void
  children: ReactNode
}

export function ToolForm({ title, subtitle, icon, isRunning, onSubmit, children }: ToolFormProps) {
  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="flex items-center space-x-2">
          {icon || <Settings className="h-5 w-5 text-neon-blue" />}
          <span className="text-sm font-medium">{title}</span>
        </div>
      </div>
      <div className="terminal-content space-y-4">
        {subtitle && (
          <p className="text-sm text-cyber-light opacity-75 mb-4">{subtitle}</p>
        )}
        {children}
        <button
          onClick={onSubmit}
          disabled={isRunning}
          className="w-full cyber-button flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isRunning ? (
            <>
              <Activity className="h-5 w-5 mr-2 animate-spin" />
              Running...
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
  )
}
