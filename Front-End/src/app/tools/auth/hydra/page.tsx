'use client'

import { useState } from 'react'
import { ArrowLeft, Lock } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function HydraPage() {
  const [target, setTarget] = useState('target.com')
  const [service, setService] = useState('ssh')
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('password')
  const [port, setPort] = useState(22)
  const [threads, setThreads] = useState(16)
  const [timeout, setTimeout] = useState(30)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('ssh')

  const scanProfiles = [
    {
      id: 'ssh',
      name: 'SSH Brute Force',
      description: 'Common SSH credentials',
      estimatedTime: '1-5 minutes',
      config: {
        service: 'ssh',
        port: 22,
        threads: 16
      }
    },
    {
      id: 'ftp',
      name: 'FTP Brute Force',
      description: 'Common FTP credentials',
      estimatedTime: '1-3 minutes',
      config: {
        service: 'ftp',
        port: 21,
        threads: 16
      }
    },
    {
      id: 'http',
      name: 'HTTP Login',
      description: 'Basic HTTP authentication',
      estimatedTime: '2-5 minutes',
      config: {
        service: 'http-get',
        port: 80,
        threads: 16
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setService(profile.config.service)
    setPort(profile.config.port)
    setThreads(profile.config.threads)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/hydra', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target,
          service,
          username,
          password,
          port,
          threads,
          timeout
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
            HYDRA
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Network login cracker
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Crack Configuration"
            subtitle="Configure Hydra parameters"
            icon={<Lock className="h-5 w-5 text-neon-blue" />}
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
                { value: 'http-get', label: 'HTTP GET' },
                { value: 'http-post', label: 'HTTP POST' },
                { value: 'rdp', label: 'RDP' },
                { value: 'smb', label: 'SMB' },
                { value: 'ldap', label: 'LDAP' }
              ]}
            />
            <FormField
              label="Port"
              type="number"
              value={port}
              onChange={setPort}
              placeholder="22"
              min={1}
              max={65535}
            />
            <FormField
              label="Username"
              type="text"
              value={username}
              onChange={setUsername}
              placeholder="admin or path to wordlist"
            />
            <FormField
              label="Password"
              type="text"
              value={password}
              onChange={setPassword}
              placeholder="password or path to wordlist"
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
            <FormField
              label="Timeout (s)"
              type="number"
              value={timeout}
              onChange={setTimeout}
              placeholder="30"
              min={1}
              max={300}
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
