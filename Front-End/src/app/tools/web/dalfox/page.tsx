'use client'

import { useState } from 'react'
import { ArrowLeft, Bug } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function DalfoxPage() {
  const [url, setUrl] = useState('http://target.com/page.php?q=test')
  const [blind, setBlind] = useState(false)
  const [worker, setWorker] = useState(40)
  const [format, setFormat] = useState('json')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard XSS Scan',
      description: 'Standard XSS parameter testing',
      estimatedTime: '30-60 seconds',
      config: {
        blind: false,
        worker: 40
      }
    },
    {
      id: 'blind',
      name: 'Blind XSS Scan',
      description: 'Include blind XSS payloads',
      estimatedTime: '1-2 minutes',
      config: {
        blind: true,
        worker: 40
      }
    },
    {
      id: 'aggressive',
      name: 'Aggressive Scan',
      description: 'High worker count aggressive scan',
      estimatedTime: '1-3 minutes',
      config: {
        blind: true,
        worker: 100
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setBlind(profile.config.blind)
    setWorker(profile.config.worker)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/dalfox', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          blind,
          worker,
          format
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
            DALFOX
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            XSS vulnerability scanner
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure Dalfox parameters"
            icon={<Bug className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Target URL"
              type="url"
              value={url}
              onChange={setUrl}
              placeholder="http://target.com/page.php?q=test"
              required
            />
            <FormField
              label="Include Blind XSS"
              type="checkbox"
              value={blind}
              onChange={setBlind}
              helperText="Test for blind/stored XSS"
            />
            <FormField
              label="Worker Threads"
              type="slider"
              value={worker}
              onChange={setWorker}
              min={10}
              max={100}
              step={10}
            />
            <FormField
              label="Output Format"
              type="select"
              value={format}
              onChange={setFormat}
              options={[
                { value: 'json', label: 'JSON' },
                { value: 'plain', label: 'Plain Text' }
              ]}
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
