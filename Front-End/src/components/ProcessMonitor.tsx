'use client'

import { ProcessDashboard } from '@/types/api'

interface ProcessMonitorProps {
  dashboard?: ProcessDashboard
  loading?: boolean
}

export function ProcessMonitor({ dashboard, loading }: ProcessMonitorProps) {
  if (loading) {
    return (
      <div className="terminal-window">
        <div className="terminal-header">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-sm font-medium">Process Monitor</span>
          </div>
        </div>
        <div className="terminal-content">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyber-primary"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-cyber-primary"></div>
          <span className="text-sm font-medium">Process Monitor</span>
        </div>
      </div>
      <div className="terminal-content">
        <div className="space-y-4">
          {(dashboard?.processes?.length || 0) > 0 ? (
            dashboard?.processes?.map((process) => (
              <div key={process.pid} className="border border-cyber-primary/30 rounded p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-cyber-primary font-mono text-sm">
                    PID: {process.pid}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs ${
                    process.status === 'running' ? 'bg-green-900 text-green-300' :
                    process.status === 'completed' ? 'bg-blue-900 text-blue-300' :
                    'bg-red-900 text-red-300'
                  }`}>
                    {process.status.toUpperCase()}
                  </span>
                </div>
                <div className="text-xs text-cyber-light mb-2">
                  {process.command}
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span>Progress:</span>
                    <span>{process.progress_percent}</span>
                  </div>
                  <div className="w-full bg-cyber-gray rounded-full h-2">
                    <div 
                      className="bg-cyber-primary h-2 rounded-full transition-all duration-300"
                      style={{ width: process.progress_percent }}
                    ></div>
                  </div>
                  <div className="flex justify-between text-xs text-cyber-light">
                    <span>Runtime: {process.runtime}</span>
                    <span>ETA: {process.eta}</span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-cyber-light">
              <div className="text-lg mb-2">No active processes</div>
              <div className="text-sm opacity-75">
                Start a scan or tool execution to see process information
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
