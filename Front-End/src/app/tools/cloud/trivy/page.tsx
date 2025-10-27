'use client'

import { useState } from 'react'
import { ArrowLeft, Shield } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function TrivyPage() {
  const [scanType, setScanType] = useState('image')
  const [target, setTarget] = useState('alpine:latest')
  const [severity, setSeverity] = useState('HIGH,CRITICAL')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('image')

  const scanProfiles = [
    { id: 'image', name: 'Container Image', description: 'Scan container image', estimatedTime: '2-5 minutes', config: { scanType: 'image' } },
    { id: 'filesystem', name: 'Filesystem', description: 'Scan filesystem', estimatedTime: '3-10 minutes', config: { scanType: 'fs' } },
    { id: 'repository', name: 'Repository', description: 'Scan git repository', estimatedTime: '5-15 minutes', config: { scanType: 'repo' } }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setScanType(profile.config.scanType)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/trivy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scan_type: scanType, target, severity }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Scan failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">TRIVY</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">Container & filesystem vulnerability scanner</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Scan Configuration" subtitle="Configure Trivy" icon={<Shield className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Scan Type" type="select" value={scanType} onChange={setScanType} options={[
              { value: 'image', label: 'Container Image' },
              { value: 'fs', label: 'Filesystem' },
              { value: 'repo', label: 'Repository' }
            ]} />
            <FormField label="Target" type="text" value={target} onChange={setTarget} placeholder="alpine:latest" required />
            <FormField label="Severity Filter" type="text" value={severity} onChange={setSeverity} placeholder="HIGH,CRITICAL" />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
