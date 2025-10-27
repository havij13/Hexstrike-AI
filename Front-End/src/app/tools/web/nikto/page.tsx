'use client'

import { useState } from 'react'
import { ArrowLeft, ShieldCheck } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function NiktoPage() {
  const [url, setUrl] = useState('https://target.com')
  const [tuning, setTuning] = useState('1')
  const [format, setFormat] = useState('txt')
  const [timeout, setTimeout] = useState(10)
  const [ssl, setSsl] = useState(false)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard Scan',
      description: 'Basic web server vulnerability scan',
      estimatedTime: '2-5 minutes',
      config: {
        tuning: '1',
        format: 'txt',
        ssl: false
      }
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Scan',
      description: 'Thorough vulnerability assessment',
      estimatedTime: '5-15 minutes',
      config: {
        tuning: 'x',
        format: 'html',
        ssl: false
      }
    },
    {
      id: 'ssl',
      name: 'SSL Scan',
      description: 'HTTPS/SSL focused scan',
      estimatedTime: '3-8 minutes',
      config: {
        tuning: '1',
        format: 'txt',
        ssl: true
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setTuning(profile.config.tuning)
    setFormat(profile.config.format)
    setSsl(profile.config.ssl)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/nikto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          tuning,
          format,
          timeout,
          ssl
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
            NIKTO
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Web server vulnerability scanner
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure Nikto parameters"
            icon={<ShieldCheck className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Target URL"
              type="url"
              value={url}
              onChange={setUrl}
              placeholder="https://target.com"
              required
            />
            <FormField
              label="Tuning"
              type="select"
              value={tuning}
              onChange={setTuning}
              options={[
                { value: '1', label: 'Interesting File / Seen in logs' },
                { value: '2', label: 'Misconfiguration / Default File' },
                { value: '3', label: 'Information Disclosure' },
                { value: '4', label: 'Injection (XSS/Script/HTML)' },
                { value: '5', label: 'Remote File Retrieval' },
                { value: '6', label: 'Denial of Service' },
                { value: '7', label: 'Remote Code Execution' },
                { value: '8', label: 'SQL Injection' },
                { value: 'a', label: 'Authentication bypass' },
                { value: 'x', label: 'All tests (potentially dangerous)' }
              ]}
            />
            <FormField
              label="Output Format"
              type="select"
              value={format}
              onChange={setFormat}
              options={[
                { value: 'txt', label: 'Text' },
                { value: 'html', label: 'HTML' },
                { value: 'xml', label: 'XML' },
                { value: 'csv', label: 'CSV' }
              ]}
            />
            <FormField
              label="Timeout"
              type="number"
              value={timeout}
              onChange={setTimeout}
              placeholder="10"
              min={1}
              max={60}
            />
            <FormField
              label="Force SSL"
              type="checkbox"
              value={ssl}
              onChange={setSsl}
              helperText="Use HTTPS for all requests"
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
