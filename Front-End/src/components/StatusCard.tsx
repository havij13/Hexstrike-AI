'use client'

import { ReactNode } from 'react'

interface StatusCardProps {
  title: string
  value: string
  icon: ReactNode
  status: 'success' | 'warning' | 'error' | 'info'
  loading?: boolean
}

export function StatusCard({ title, value, icon, status, loading = false }: StatusCardProps) {
  const statusColors = {
    success: 'border-green-500 text-green-300',
    warning: 'border-yellow-500 text-yellow-300',
    error: 'border-red-500 text-red-300',
    info: 'border-cyber-primary text-cyber-primary',
  }

  const statusBgColors = {
    success: 'bg-green-900/20',
    warning: 'bg-yellow-900/20',
    error: 'bg-red-900/20',
    info: 'bg-cyber-primary/10',
  }

  return (
    <div className={`terminal-window ${statusBgColors[status]} ${statusColors[status]}`}>
      <div className="terminal-header">
        <div className="flex items-center space-x-2">
          {icon}
          <span className="text-sm font-medium">{title}</span>
        </div>
      </div>
      <div className="terminal-content">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-current"></div>
          </div>
        ) : (
          <div className="text-center">
            <div className="text-2xl font-cyber font-bold mb-2">
              {value}
            </div>
            <div className="text-xs opacity-75">
              Last updated: {new Date().toLocaleTimeString()}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
