'use client'

import { useState } from 'react'
import { ArrowLeft, Database } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function SQLMapPage() {
  const [url, setUrl] = useState('http://target.com/page.php?id=1')
  const [method, setMethod] = useState('GET')
  const [data, setData] = useState('')
  const [level, setLevel] = useState('1')
  const [risk, setRisk] = useState('1')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('basic')

  const scanProfiles = [
    {
      id: 'basic',
      name: 'Basic Scan',
      description: 'Basic SQL injection test',
      estimatedTime: '30-60 seconds',
      config: {
        level: '1',
        risk: '1'
      }
    },
    {
      id: 'medium',
      name: 'Medium Scan',
      description: 'Medium-depth injection test',
      estimatedTime: '1-3 minutes',
      config: {
        level: '2',
        risk: '2'
      }
    },
    {
      id: 'intensive',
      name: 'Intensive Scan',
      description: 'Deep injection test with all techniques',
      estimatedTime: '3-10 minutes',
      config: {
        level: '3',
        risk: '3'
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setLevel(profile.config.level)
    setRisk(profile.config.risk)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/sqlmap', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          method,
          data,
          level,
          risk
        }),
      })
      const result = await response.json()
      setResults(result)
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
            SQLMAP
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Automatic SQL injection tool
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure SQLMap parameters"
            icon={<Database className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Target URL"
              type="url"
              value={url}
              onChange={setUrl}
              placeholder="http://target.com/page.php?id=1"
              required
            />
            <FormField
              label="HTTP Method"
              type="select"
              value={method}
              onChange={setMethod}
              options={[
                { value: 'GET', label: 'GET' },
                { value: 'POST', label: 'POST' }
              ]}
            />
            <FormField
              label="POST Data"
              type="textarea"
              value={data}
              onChange={setData}
              placeholder="username=admin&password=test"
              helperText="Required for POST requests"
            />
            <FormField
              label="Level (1-5)"
              type="select"
              value={level}
              onChange={setLevel}
              options={[
                { value: '1', label: 'Level 1 - Basic' },
                { value: '2', label: 'Level 2 - Default' },
                { value: '3', label: 'Level 3 - Advanced' },
                { value: '4', label: 'Level 4 - Expert' },
                { value: '5', label: 'Level 5 - Extreme' }
              ]}
            />
            <FormField
              label="Risk (1-3)"
              type="select"
              value={risk}
              onChange={setRisk}
              options={[
                { value: '1', label: 'Risk 1 - Low' },
                { value: '2', label: 'Risk 2 - Medium' },
                { value: '3', label: 'Risk 3 - High' }
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
