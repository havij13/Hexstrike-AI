'use client'

import { useState } from 'react'
import { ArrowLeft, Cloud } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function KubeHunterPage() {
  const [target, setTarget] = useState('')
  const [cidr, setCidr] = useState('')
  const [active, setActive] = useState(false)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('pod')

  const scanProfiles = [
    { id: 'pod', name: 'Pod Scan', description: 'Scan from within cluster', estimatedTime: '3-5 minutes', config: {} },
    { id: 'remote', name: 'Remote Scan', description: 'Scan from outside', estimatedTime: '5-10 minutes', config: {} },
    { id: 'active', name: 'Active Hunt', description: 'Active exploitation', estimatedTime: '10-20 minutes', config: { active: true } }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setActive(profile.config.active || false)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/kube-hunter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target, cidr, active }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Scan failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">KUBE-HUNTER</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">Kubernetes penetration testing tool</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Scan Configuration" subtitle="Configure Kube-Hunter" icon={<Cloud className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Target IP" type="text" value={target} onChange={setTarget} placeholder="10.0.0.1" />
            <FormField label="CIDR" type="text" value={cidr} onChange={setCidr} placeholder="10.0.0.0/8" />
            <FormField label="Active Hunt" type="checkbox" value={active} onChange={setActive} helperText="Perform active exploitation" />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
