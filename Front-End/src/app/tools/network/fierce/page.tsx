'use client'

import { useState } from 'react'
import { ArrowLeft, Zap } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function FiercePage() {
  const [domain, setDomain] = useState('example.com')
  const [dnsServer, setDnsServer] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    { id: 'standard', name: 'Standard DNS Recon', description: 'Standard DNS enumeration', estimatedTime: '1-3 minutes', config: {} },
    { id: 'aggressive', name: 'Aggressive Scan', description: 'Fast aggressive enumeration', estimatedTime: '30-60 seconds', config: {} },
    { id: 'comprehensive', name: 'Comprehensive Scan', description: 'Full DNS reconnaissance', estimatedTime: '3-5 minutes', config: {} }
  ]

  const handleSelectProfile = (profile: any) => { setSelectedProfile(profile.id) }
  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/fierce', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain, dns_server: dnsServer }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Scan failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools/network" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">FIERCE</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">DNS reconnaissance tool</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Scan Configuration" subtitle="Configure Fierce" icon={<Zap className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Domain" type="text" value={domain} onChange={setDomain} placeholder="example.com" required />
            <FormField label="DNS Server (optional)" type="text" value={dnsServer} onChange={setDnsServer} placeholder="8.8.8.8" />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
