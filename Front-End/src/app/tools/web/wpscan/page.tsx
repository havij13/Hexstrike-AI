'use client'

import { useState } from 'react'
import { ArrowLeft, Globe } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function WPScanPage() {
  const [url, setUrl] = useState('https://target.com')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [enumerate, setEnumerate] = useState('vp,vt,tt,u,m')
  const [vulnerabilities, setVulnerabilities] = useState(true)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('quick')

  const scanProfiles = [
    {
      id: 'quick',
      name: 'Quick Scan',
      description: 'Fast enumeration of version and plugins',
      estimatedTime: '30-60 seconds',
      config: {
        enumerate: 'vp'
      }
    },
    {
      id: 'standard',
      name: 'Standard Scan',
      description: 'Comprehensive enumeration without passwords',
      estimatedTime: '1-3 minutes',
      config: {
        enumerate: 'vp,vt,tt,u,m'
      }
    },
    {
      id: 'aggressive',
      name: 'Aggressive Scan',
      description: 'Full scan with brute forcing',
      estimatedTime: '5-15 minutes',
      config: {
        enumerate: 'vp,vt,tt,u,m',
        vulnerabilities: true
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setEnumerate(profile.config.enumerate)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/wpscan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          username,
          password,
          enumerate,
          vulnerabilities
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
        <Link href="/tools/web" className="text-cyber-primary hover:text-cyber-light transition-colors">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
            WPSCAN
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            WordPress vulnerability scanner
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure WPScan parameters"
            icon={<Globe className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="WordPress URL"
              type="url"
              value={url}
              onChange={setUrl}
              placeholder="https://target.com"
              required
            />
            <FormField
              label="Username (optional)"
              type="text"
              value={username}
              onChange={setUsername}
              placeholder="admin"
              helperText="For brute force testing"
            />
            <FormField
              label="Password (optional)"
              type="text"
              value={password}
              onChange={setPassword}
              placeholder="password"
              helperText="For brute force testing"
            />
            <FormField
              label="Enumerate"
              type="text"
              value={enumerate}
              onChange={setEnumerate}
              placeholder="vp,vt,tt,u,m"
              helperText="v=plugins, vt=timthumbs, tt=themes, u=users, m=mediamods"
            />
            <FormField
              label="Check Vulnerabilities"
              type="checkbox"
              value={vulnerabilities}
              onChange={setVulnerabilities}
              helperText="Check for known vulnerabilities"
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
