'use client'

import { TelemetryData } from '@/types/api'

interface SystemMetricsProps {
  telemetry?: TelemetryData
  loading?: boolean
}

export function SystemMetrics({ telemetry, loading }: SystemMetricsProps) {
  if (loading) {
    return (
      <div className="terminal-window">
        <div className="terminal-header">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-sm font-medium">System Metrics</span>
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

  const metrics = [
    {
      label: 'CPU Usage',
      value: telemetry?.cpu_usage || 0,
      max: 100,
      color: 'bg-cyber-primary',
    },
    {
      label: 'Memory Usage',
      value: telemetry?.memory_usage || 0,
      max: 100,
      color: 'bg-neon-blue',
    },
    {
      label: 'Disk Usage',
      value: telemetry?.disk_usage || 0,
      max: 100,
      color: 'bg-neon-pink',
    },
    {
      label: 'Active Connections',
      value: telemetry?.active_connections || 0,
      max: 1000,
      color: 'bg-neon-green',
    },
  ]

  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-cyber-primary"></div>
          <span className="text-sm font-medium">System Metrics</span>
        </div>
      </div>
      <div className="terminal-content">
        <div className="space-y-4">
          {metrics.map((metric, index) => (
            <div key={index} className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-cyber-light text-sm">{metric.label}</span>
                <span className="text-cyber-primary font-mono text-sm">
                  {metric.value}{metric.label.includes('Usage') ? '%' : ''}
                </span>
              </div>
              <div className="w-full bg-cyber-gray rounded-full h-2">
                <div 
                  className={`${metric.color} h-2 rounded-full transition-all duration-500`}
                  style={{ width: `${(metric.value / metric.max) * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
          
          <div className="border-t border-cyber-primary/30 pt-4 mt-4">
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-cyber-light">Total Requests:</span>
                <span className="text-cyber-primary ml-2 font-mono">
                  {telemetry?.total_requests || 0}
                </span>
              </div>
              <div>
                <span className="text-cyber-light">Error Rate:</span>
                <span className="text-cyber-primary ml-2 font-mono">
                  {telemetry?.error_rate || 0}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
