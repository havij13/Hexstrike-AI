'use client'

import { useState, useEffect } from 'react'
import { useQuery } from 'react-query'
import { apiClient } from '@/lib/api'
import { StatusCard } from './StatusCard'
import { ServerStatus } from './ServerStatus'
import { ProcessMonitor } from './ProcessMonitor'
import { SystemMetrics } from './SystemMetrics'
import { RecentActivity } from './RecentActivity'
import { QuickActions } from './QuickActions'
import { AlertCircle, CheckCircle, Clock, Zap } from 'lucide-react'

export function Dashboard() {
  const [alerts, setAlerts] = useState([
    {
      id: 1,
      type: 'success',
      message: 'System initialized successfully',
      timestamp: new Date().toISOString(),
    },
    {
      id: 2,
      type: 'warning',
      message: 'High CPU usage detected',
      timestamp: new Date().toISOString(),
    },
  ])

  // Fetch health status
  const { data: health, isLoading: healthLoading } = useQuery(
    'health',
    () => apiClient.getHealth(),
    {
      refetchInterval: 5000,
    }
  )

  // Fetch telemetry data
  const { data: telemetry, isLoading: telemetryLoading } = useQuery(
    'telemetry',
    () => apiClient.getTelemetry(),
    {
      refetchInterval: 3000,
    }
  )

  // Fetch process dashboard
  const { data: processDashboard, isLoading: processLoading } = useQuery(
    'process-dashboard',
    () => apiClient.getProcessDashboard(),
    {
      refetchInterval: 2000,
    }
  )

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-cyber font-bold text-cyber-primary neon-glow">
            DASHBOARD
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Real-time system monitoring and control
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <div className="text-sm text-cyber-light font-mono">
              {new Date().toLocaleTimeString()}
            </div>
            <div className="text-xs text-cyber-light">
              {new Date().toLocaleDateString()}
            </div>
          </div>
          <div className="w-12 h-12 bg-cyber-primary rounded-full flex items-center justify-center">
            <Zap className="h-6 w-6 text-cyber-dark" />
          </div>
        </div>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="space-y-2">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`flex items-center space-x-3 p-3 rounded-lg border ${
                alert.type === 'success'
                  ? 'bg-green-900/20 border-green-700 text-green-300'
                  : alert.type === 'warning'
                  ? 'bg-yellow-900/20 border-yellow-700 text-yellow-300'
                  : 'bg-red-900/20 border-red-700 text-red-300'
              }`}
            >
              {alert.type === 'success' ? (
                <CheckCircle className="h-5 w-5" />
              ) : (
                <AlertCircle className="h-5 w-5" />
              )}
              <span className="text-sm font-medium">{alert.message}</span>
              <span className="text-xs opacity-75 ml-auto">
                {new Date(alert.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Server Status */}
      <ServerStatus />

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatusCard
          title="System Health"
          value={health?.status || 'Unknown'}
          icon={<CheckCircle className="h-6 w-6" />}
          status={health?.status === 'healthy' ? 'success' : 'warning'}
          loading={healthLoading}
        />
        <StatusCard
          title="Active Processes"
          value={String(processDashboard?.total_processes ?? 0)}
          icon={<Clock className="h-6 w-6" />}
          status="info"
          loading={processLoading}
        />
        <StatusCard
          title="CPU Usage"
          value={`${telemetry?.cpu_usage || 0}%`}
          icon={<Zap className="h-6 w-6" />}
          status={(telemetry?.cpu_usage || 0) > 80 ? 'warning' : 'success'}
          loading={telemetryLoading}
        />
        <StatusCard
          title="Memory Usage"
          value={`${telemetry?.memory_usage || 0}%`}
          icon={<AlertCircle className="h-6 w-6" />}
          status={(telemetry?.memory_usage || 0) > 80 ? 'warning' : 'success'}
          loading={telemetryLoading}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          <SystemMetrics telemetry={telemetry} loading={telemetryLoading} />
          <ProcessMonitor dashboard={processDashboard} loading={processLoading} />
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          <QuickActions />
          <RecentActivity />
        </div>
      </div>
    </div>
  )
}
