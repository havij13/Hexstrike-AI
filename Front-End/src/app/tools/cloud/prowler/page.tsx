'use client'

import { useState } from 'react'
import { ArrowLeft, Cloud } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function ProwlerPage() {
  const [provider, setProvider] = useState('aws')
  const [profile, setProfile] = useState('default')
  const [region, setRegion] = useState('')
  const [checks, setChecks] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    { id: 'standard', name: 'Standard Assessment', description: 'AWS security baseline', estimatedTime: '20-40 minutes', config: { provider: 'aws', checks: '' } },
    { id: 'compliance', name: 'Compliance Check', description: 'CIS benchmark compliance', estimatedTime: '30-60 minutes', config: { provider: 'aws', checks: 'check-cis-*' } },
    { id: 'comprehensive', name: 'Full Assessment', description: 'Complete security scan', estimatedTime: '60-120 minutes', config: { provider: 'aws', checks: 'all' } }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setProvider(profile.config.provider)
    setChecks(profile.config.checks)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/prowler', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, profile, region, checks }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Scan failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">PROWLER</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">AWS security assessment tool</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Scan Configuration" subtitle="Configure Prowler" icon={<Cloud className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Provider" type="select" value={provider} onChange={setProvider} options={[
              { value: 'aws', label: 'AWS' },
              { value: 'azure', label: 'Azure' },
              { value: 'gcp', label: 'GCP' }
            ]} />
            <FormField label="Profile" type="text" value={profile} onChange={setProfile} placeholder="default" />
            <FormField label="Region" type="text" value={region} onChange={setRegion} placeholder="us-east-1" />
            <FormField label="Checks" type="text" value={checks} onChange={setChecks} placeholder="check-cis-*" />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
