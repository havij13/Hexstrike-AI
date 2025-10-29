'use client'

import { useState } from 'react'
import { ArrowLeft, Radar } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function AutoReconPage() {
  const [target, setTarget] = useState('192.168.1.1')
  const [portScans, setPortScans] = useState('top-100-ports')
  const [serviceScans, setServiceScans] = useState('default')
  const [timeout, setTimeoutValue] = useState(300)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('quick')

  const scanProfiles = [
    { id: 'quick', name: 'Quick Scan', description: 'Fast reconnaissance', estimatedTime: '5-10 minutes', config: { portScans: 'top-100-ports', serviceScans: 'basic' } },
    { id: 'standard', name: 'Standard Scan', description: 'Comprehensive enumeration', estimatedTime: '15-30 minutes', config: { portScans: 'all-ports', serviceScans: 'default' } },
    { id: 'comprehensive', name: 'Full Scan', description: 'Complete reconnaissance', estimatedTime: '30-60 minutes', config: { portScans: 'all-ports', serviceScans: 'all' } }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setPortScans(profile.config.portScans)
    setServiceScans(profile.config.serviceScans)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/autorecon', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target, port_scans: portScans, service_scans: serviceScans, timeout }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Scan failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools/network" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">AUTORECON</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">Automated reconnaissance framework</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Scan Configuration" subtitle="Configure AutoRecon" icon={<Radar className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Target" type="text" value={target} onChange={setTarget} placeholder="192.168.1.1" required />
            <FormField label="Port Scans" type="select" value={portScans} onChange={setPortScans} options={[
              { value: 'top-100-ports', label: 'Top 100 Ports' },
              { value: 'all-ports', label: 'All Ports' },
              { value: 'top-1000-ports', label: 'Top 1000 Ports' }
            ]} />
            <FormField label="Service Scans" type="select" value={serviceScans} onChange={setServiceScans} options={[
              { value: 'default', label: 'Default' },
              { value: 'basic', label: 'Basic' },
              { value: 'all', label: 'All' }
            ]} />
            <FormField label="Timeout (seconds)" type="slider" value={timeout} onChange={setTimeoutValue} min={60} max={1800} step={60} />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
