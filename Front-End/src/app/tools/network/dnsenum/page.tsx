'use client'

import { useState } from 'react'
import { ArrowLeft, FileSearch } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function DNSenumPage() {
  const [domain, setDomain] = useState('example.com')
  const [dnsServer, setDnsServer] = useState('')
  const [wordlist, setWordlist] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    { id: 'standard', name: 'Standard Enumeration', description: 'Basic DNS enumeration', estimatedTime: '2-4 minutes', config: {} },
    { id: 'bruteforce', name: 'Brute Force Subdomains', description: 'Brute force with wordlist', estimatedTime: '5-10 minutes', config: {} },
    { id: 'comprehensive', name: 'Comprehensive Scan', description: 'Full DNS enumeration', estimatedTime: '5-15 minutes', config: {} }
  ]

  const handleSelectProfile = (profile: any) => { setSelectedProfile(profile.id) }
  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/dnsenum', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain, dns_server: dnsServer, wordlist }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Scan failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools/network" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">DNSENUM</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">DNS enumeration and zone transfer tool</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Scan Configuration" subtitle="Configure DNSenum" icon={<FileSearch className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Domain" type="text" value={domain} onChange={setDomain} placeholder="example.com" required />
            <FormField label="DNS Server (optional)" type="text" value={dnsServer} onChange={setDnsServer} placeholder="8.8.8.8" />
            <FormField label="Wordlist (optional)" type="text" value={wordlist} onChange={setWordlist} placeholder="subdomains.txt" />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
