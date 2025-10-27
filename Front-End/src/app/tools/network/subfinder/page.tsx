'use client'

import { useState } from 'react'
import { ArrowLeft, Eye } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function SubfinderPage() {
  const [domain, setDomain] = useState('example.com')
  const [silent, setSilent] = useState(true)
  const [allSources, setAllSources] = useState(false)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard Enumeration',
      description: 'Passive subdomain discovery',
      estimatedTime: '1-3 minutes',
      config: { silent: true, allSources: false }
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Scan',
      description: 'All sources enabled',
      estimatedTime: '3-5 minutes',
      config: { silent: true, allSources: true }
    },
    {
      id: 'verbose',
      name: 'Verbose Mode',
      description: 'Detailed output with all sources',
      estimatedTime: '3-5 minutes',
      config: { silent: false, allSources: true }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setSilent(profile.config.silent)
    setAllSources(profile.config.allSources)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/subfinder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain, silent, all_sources: allSources }),
      })
      setResults(await response.json())
    } catch (error) {
      console.error('Scan failed:', error)
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools/network" className="text-cyber-primary hover:text-cyber-light transition-colors">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">SUBFINDER</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">Passive subdomain discovery tool</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Scan Configuration" subtitle="Configure Subfinder" icon={<Eye className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Domain" type="text" value={domain} onChange={setDomain} placeholder="example.com" required />
            <FormField label="Silent Mode" type="checkbox" value={silent} onChange={setSilent} helperText="Suppress verbose output" />
            <FormField label="All Sources" type="checkbox" value={allSources} onChange={setAllSources} helperText="Enable all passive sources" />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
