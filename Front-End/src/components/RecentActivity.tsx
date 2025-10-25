'use client'

import { useState } from 'react'
import { Clock, CheckCircle, XCircle, AlertTriangle } from 'lucide-react'

export function RecentActivity() {
  const [activities] = useState([
    {
      id: 1,
      type: 'success',
      message: 'Nmap scan completed',
      timestamp: new Date(Date.now() - 5 * 60 * 1000),
    },
    {
      id: 2,
      type: 'warning',
      message: 'High memory usage detected',
      timestamp: new Date(Date.now() - 10 * 60 * 1000),
    },
    {
      id: 3,
      type: 'success',
      message: 'Target analysis completed',
      timestamp: new Date(Date.now() - 15 * 60 * 1000),
    },
    {
      id: 4,
      type: 'error',
      message: 'Gobuster scan failed',
      timestamp: new Date(Date.now() - 20 * 60 * 1000),
    },
    {
      id: 5,
      type: 'success',
      message: 'System health check passed',
      timestamp: new Date(Date.now() - 25 * 60 * 1000),
    },
  ])

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-400" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />
      case 'error':
        return <XCircle className="h-4 w-4 text-red-400" />
      default:
        return <Clock className="h-4 w-4 text-cyber-primary" />
    }
  }

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'success':
        return 'text-green-300'
      case 'warning':
        return 'text-yellow-300'
      case 'error':
        return 'text-red-300'
      default:
        return 'text-cyber-light'
    }
  }

  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-cyber-primary"></div>
          <span className="text-sm font-medium">Recent Activity</span>
        </div>
      </div>
      <div className="terminal-content">
        <div className="space-y-3">
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-start space-x-3 p-2 rounded border border-cyber-primary/20">
              {getActivityIcon(activity.type)}
              <div className="flex-1 min-w-0">
                <div className={`text-sm ${getActivityColor(activity.type)}`}>
                  {activity.message}
                </div>
                <div className="text-xs text-cyber-light opacity-75">
                  {activity.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
