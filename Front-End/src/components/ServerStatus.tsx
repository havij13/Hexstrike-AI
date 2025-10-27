'use client'

import { useQuery } from 'react-query'
import { apiClient } from '@/lib/api'
import { StatusCard } from './StatusCard'
import { CheckCircle, Zap, Brain } from 'lucide-react'

export function ServerStatus() {
  const { data: health, isLoading: healthLoading } = useQuery(
    'health',
    () => apiClient.getHealth(),
    {
      refetchInterval: 5000,
    }
  )

  const { data: toolCount, isLoading: toolCountLoading } = useQuery(
    'tool-count',
    () => apiClient.getToolCount(),
    {
      refetchInterval: 60000, // Refresh every minute
    }
  )

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatusCard
        title="Server Health"
        value={`${health?.status || 'Unknown'} - ${health?.version || '6.0.0'}`}
        icon={<CheckCircle className="h-6 w-6" />}
        status={health?.status === 'healthy' ? 'success' : 'warning'}
        loading={healthLoading}
      />
      <StatusCard
        title="Available Tools"
        value={`${toolCount?.total_tools || 150}+`}
        icon={<Zap className="h-6 w-6" />}
        status="info"
        loading={toolCountLoading}
      />
      <StatusCard
        title="AI Agents"
        value={`${toolCount?.ai_agents || 12}+ Active`}
        icon={<Brain className="h-6 w-6" />}
        status="success"
        loading={toolCountLoading}
      />
    </div>
  )
}
