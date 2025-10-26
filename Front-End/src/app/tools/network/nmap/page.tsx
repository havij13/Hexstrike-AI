'use client'

import { useState } from 'react'
import { ArrowLeft, Radar } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function NmapPage() {
  const [target, setTarget] = useState('scanme.nmap.org')
  const [scanType, setScanType] = useState('quick')
  const [ports, setPorts] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('quick')

  const scanProfiles = [
    {
      id: 'quick',
      name: 'Quick Scan',
      description: 'Fast TCP port scan on most common ports',
      estimatedTime: '30-60 seconds',
      config: {
        scanType: 'quick',
        ports: ''
      }
    },
    {
      id: 'syn',
      name: 'SYN Scan',
      description: 'Stealth SYN scan (requires root)',
      estimatedTime: '1-3 minutes',
      config: {
        scanType: 'syn',
        ports: ''
      }
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Scan',
      description: 'Full port scan with service detection',
      estimatedTime: '5-15 minutes',
      config: {
        scanType: 'comprehensive',
        ports: ''
      }
    },
    {
      id: 'vulnerability',
      name: 'Vulnerability Scan',
      description: 'Port scan with vulnerability detection',
      estimatedTime: '10-30 minutes',
      config: {
        scanType: 'vulnerability',
        ports: ''
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setScanType(profile.config.scanType)
    setPorts(profile.config.ports)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/nmap', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          scan_type: scanType,
          ports: ports || undefined
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
            NMAP
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Network exploration and security auditing tool
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure Nmap scan parameters"
            icon={<Radar className="h-5 w-5 text-neon-blue" />}
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
              label="Scan Type"
              type="select"
              value={scanType}
              onChange={setScanType}
              options={[
                { value: 'quick', label: 'Quick Scan (-sT)' },
                { value: 'syn', label: 'SYN Scan (-sS)' },
                { value: 'udp', label: 'UDP Scan (-sU)' },
                { value: 'comprehensive', label: 'Comprehensive (-sV -sC)' },
                { value: 'vulnerability', label: 'Vulnerability Scan (--script vuln)' },
                { value: 'stealth', label: 'Stealth Scan (-sS -f -T2)' }
              ]}
            />
            <FormField
              label="Ports (optional)"
              type="text"
              value={ports}
              onChange={setPorts}
              placeholder="22,80,443 or 1-1000"
              helperText="Leave empty for default scanning"
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
