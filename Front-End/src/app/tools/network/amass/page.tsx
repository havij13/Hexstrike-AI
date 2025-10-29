'use client'

import { useState } from 'react'
import { ArrowLeft, Network } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function AmassPage() {
  const [domain, setDomain] = useState('example.com')
  const [mode, setMode] = useState('enum')
  const [additionalArgs, setAdditionalArgs] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard Enumeration',
      description: 'Passive and active subdomain enumeration',
      estimatedTime: '3-5 minutes',
      config: {
        mode: 'enum'
      }
    },
    {
      id: 'passive',
      name: 'Passive Enumeration',
      description: 'Passive only - no DNS resolution',
      estimatedTime: '1-2 minutes',
      config: {
        mode: 'enum -passive'
      }
    },
    {
      id: 'intel',
      name: 'Intelligence Gathering',
      description: 'Collect OSINT for target',
      estimatedTime: '5-10 minutes',
      config: {
        mode: 'intel'
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setMode(profile.config.mode)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/amass', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          domain,
          mode,
          additional_args: additionalArgs
        }),
      })
      const data = await response.json()
      setResults(data)
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
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
            AMASS
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            In-depth subdomain enumeration tool
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure Amass parameters"
            icon={<Network className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Domain"
              type="text"
              value={domain}
              onChange={setDomain}
              placeholder="example.com"
              required
            />
            <FormField
              label="Mode"
              type="select"
              value={mode}
              onChange={setMode}
              options={[
                { value: 'enum', label: 'Enumeration' },
                { value: 'intel', label: 'Intelligence' },
                { value: 'viz', label: 'Visualization' }
              ]}
            />
            <FormField
              label="Additional Arguments"
              type="textarea"
              value={additionalArgs}
              onChange={setAdditionalArgs}
              placeholder="-active, -dns, etc."
            />
          </ToolForm>

          <ScanProfiles
            profiles={scanProfiles}
            selectedProfile={selectedProfile}
            onSelectProfile={handleSelectProfile}
          />
        </div>

        <div className="lg:col-span-2">
          <ResultsPanel results={results} />
        </div>
      </div>
    </div>
  )
}
