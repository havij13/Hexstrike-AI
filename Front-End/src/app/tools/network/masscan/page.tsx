'use client'

import { useState } from 'react'
import { ArrowLeft, Gauge } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function MasscanPage() {
  const [target, setTarget] = useState('scanme.nmap.org')
  const [ports, setPorts] = useState('1-65535')
  const [rate, setRate] = useState(1000)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard Scan',
      description: 'Standard rate scan for balanced speed',
      estimatedTime: '30-60 seconds',
      config: {
        ports: '1-65535',
        rate: 1000
      }
    },
    {
      id: 'aggressive',
      name: 'Aggressive Scan',
      description: 'High-speed aggressive scan',
      estimatedTime: '10-30 seconds',
      config: {
        ports: '1-65535',
        rate: 10000
      }
    },
    {
      id: 'stealth',
      name: 'Stealth Scan',
      description: 'Low rate stealth scan',
      estimatedTime: '2-5 minutes',
      config: {
        ports: '1-65535',
        rate: 100
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setPorts(profile.config.ports)
    setRate(profile.config.rate)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/masscan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          ports,
          rate
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
            MASSCAN
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            High-speed TCP port scanner
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure Masscan parameters"
            icon={<Gauge className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Target"
              type="text"
              value={target}
              onChange={setTarget}
              placeholder="scanme.nmap.org or 192.168.1.1"
              required
            />
            <FormField
              label="Ports"
              type="text"
              value={ports}
              onChange={setPorts}
              placeholder="1-65535 or 80,443,8080"
              helperText="Port range or comma-separated ports"
            />
            <FormField
              label="Rate (packets/sec)"
              type="slider"
              value={rate}
              onChange={setRate}
              min={100}
              max={10000}
              step={100}
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
