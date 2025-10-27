'use client'

import { useState } from 'react'
import { ArrowLeft, Network } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function NetExecPage() {
  const [target, setTarget] = useState('192.168.1.0/24')
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('password')
  const [modules, setModules] = useState('smb')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('smb')

  const scanProfiles = [
    {
      id: 'smb',
      name: 'SMB Enumeration',
      description: 'SMB share and service enumeration',
      estimatedTime: '1-3 minutes',
      config: {
        modules: 'smb'
      }
    },
    {
      id: 'winrm',
      name: 'WinRM Scan',
      description: 'Windows Remote Management check',
      estimatedTime: '30-60 seconds',
      config: {
        modules: 'winrm'
      }
    },
    {
      id: 'rdp',
      name: 'RDP Enumeration',
      description: 'Remote Desktop Protocol enumeration',
      estimatedTime: '1-2 minutes',
      config: {
        modules: 'rdp'
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setModules(profile.config.modules)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/netexec', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          username,
          password,
          modules
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
            NETEXEC
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Network protocol toolkit (formerly CrackMapExec)
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure NetExec parameters"
            icon={<Network className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Target"
              type="text"
              value={target}
              onChange={setTarget}
              placeholder="192.168.1.0/24 or target.com"
              required
            />
            <FormField
              label="Username"
              type="text"
              value={username}
              onChange={setUsername}
              placeholder="admin"
            />
            <FormField
              label="Password"
              type="text"
              value={password}
              onChange={setPassword}
              placeholder="password"
            />
            <FormField
              label="Module"
              type="select"
              value={modules}
              onChange={setModules}
              options={[
                { value: 'smb', label: 'SMB' },
                { value: 'ldap', label: 'LDAP' },
                { value: 'mssql', label: 'MSSQL' },
                { value: 'winrm', label: 'WinRM' },
                { value: 'rdp', label: 'RDP' },
                { value: 'ssh', label: 'SSH' },
                { value: 'ftp', label: 'FTP' }
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
