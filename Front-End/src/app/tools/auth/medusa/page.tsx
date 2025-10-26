'use client'

import { useState } from 'react'
import { ArrowLeft, Users } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function MedusaPage() {
  const [target, setTarget] = useState('target.com')
  const [service, setService] = useState('ssh')
  const [username, setUsername] = useState('root')
  const [password, setPassword] = useState('password')
  const [threads, setThreads] = useState(16)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard Brute Force',
      description: 'Medium-speed brute force attack',
      estimatedTime: '1-5 minutes',
      config: {
        threads: 16
      }
    },
    {
      id: 'fast',
      name: 'Fast Brute Force',
      description: 'Fast brute force with high parallelism',
      estimatedTime: '30 seconds - 2 minutes',
      config: {
        threads: 32
      }
    },
    {
      id: 'stealth',
      name: 'Stealth Mode',
      description: 'Slower stealth attack',
      estimatedTime: '3-10 minutes',
      config: {
        threads: 4
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setThreads(profile.config.threads)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/medusa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          service,
          username,
          password,
          threads
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
        <Link href="/tools/auth" className="text-cyber-primary hover:text-cyber-light transition-colors">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
            MEDUSA
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Parallel login brute-forcer
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Brute Force Configuration"
            subtitle="Configure Medusa parameters"
            icon={<Users className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Target"
              type="text"
              value={target}
              onChange={setTarget}
              placeholder="target.com or 192.168.1.1"
              required
            />
            <FormField
              label="Service"
              type="select"
              value={service}
              onChange={setService}
              options={[
                { value: 'ssh', label: 'SSH' },
                { value: 'ftp', label: 'FTP' },
                { value: 'telnet', label: 'Telnet' },
                { value: 'http', label: 'HTTP' },
                { value: 'pop3', label: 'POP3' },
                { value: 'imap', label: 'IMAP' },
                { value: 'smb', label: 'SMB' },
                { value: 'mssql', label: 'MSSQL' }
              ]}
            />
            <FormField
              label="Username"
              type="text"
              value={username}
              onChange={setUsername}
              placeholder="root or path to userlist"
            />
            <FormField
              label="Password"
              type="text"
              value={password}
              onChange={setPassword}
              placeholder="password or path to passlist"
            />
            <FormField
              label="Threads"
              type="slider"
              value={threads}
              onChange={setThreads}
              min={1}
              max={64}
              step={1}
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
