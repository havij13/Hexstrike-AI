'use client'

import { useState } from 'react'
import { ArrowLeft, Zap } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function RustscanPage() {
  const [target, setTarget] = useState('scanme.nmap.org')
  const [ports, setPorts] = useState('1-65535')
  const [timeout, setTimeout] = useState(1000)
  const [ulimit, setUlimit] = useState(5000)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('fast')

  const scanProfiles = [
    {
      id: 'fast',
      name: 'Fast Scan',
      description: 'Quick port scan with high timeout',
      estimatedTime: '10-30 seconds',
      config: {
        ports: '1-1000',
        timeout: 2000,
        ulimit: 5000
      }
    },
    {
      id: 'standard',
      name: 'Standard Scan',
      description: 'Standard full port range scan',
      estimatedTime: '30-60 seconds',
      config: {
        ports: '1-65535',
        timeout: 1000,
        ulimit: 5000
      }
    },
    {
      id: 'aggressive',
      name: 'Aggressive Scan',
      description: 'Maximum speed aggressive scan',
      estimatedTime: '5-15 seconds',
      config: {
        ports: '1-65535',
        timeout: 500,
        ulimit: 10000
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setPorts(profile.config.ports)
    setTimeout(profile.config.timeout)
    setUlimit(profile.config.ulimit)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/rustscan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          ports,
          timeout,
          ulimit
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
            RUSTSCAN
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Fast port scanner written in Rust
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure Rustscan parameters"
            icon={<Zap className="h-5 w-5 text-neon-blue" />}
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
              label="Timeout (ms)"
              type="slider"
              value={timeout}
              onChange={setTimeout}
              min={100}
              max={3000}
              step={100}
            />
            <FormField
              label="Ulimit"
              type="slider"
              value={ulimit}
              onChange={setUlimit}
              min={1000}
              max={10000}
              step={1000}
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
