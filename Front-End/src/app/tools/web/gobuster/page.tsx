'use client'

import { useState } from 'react'
import { ArrowLeft, Search } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function GobusterPage() {
  const [url, setUrl] = useState('https://target.com')
  const [mode, setMode] = useState('dir')
  const [wordlist, setWordlist] = useState('common.txt')
  const [extensions, setExtensions] = useState('php,html,txt')
  const [threads, setThreads] = useState(50)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('quick')

  const scanProfiles = [
    {
      id: 'quick',
      name: 'Quick Directory Scan',
      description: 'Fast directory enumeration',
      estimatedTime: '30-60 seconds',
      config: {
        mode: 'dir',
        wordlist: 'common.txt',
        extensions: 'php,html,txt'
      }
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Scan',
      description: 'Full enumeration with multiple extensions',
      estimatedTime: '5-10 minutes',
      config: {
        mode: 'dir',
        wordlist: 'big.txt',
        extensions: 'php,html,txt,jsp,asp'
      }
    },
    {
      id: 'dns',
      name: 'DNS Subdomain Scan',
      description: 'Subdomain enumeration',
      estimatedTime: '1-3 minutes',
      config: {
        mode: 'dns',
        wordlist: 'subdomains.txt',
        extensions: ''
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setMode(profile.config.mode)
    setWordlist(profile.config.wordlist)
    setExtensions(profile.config.extensions)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/gobuster', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          mode,
          wordlist,
          extensions: extensions.split(','),
          threads,
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
            GOBUSTER
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Directory/file brute-forcing tool
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure Gobuster parameters"
            icon={<Search className="h-5 w-5 text-neon-blue" />}
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
              label="Scan Mode"
              type="select"
              value={mode}
              onChange={setMode}
              options={[
                { value: 'dir', label: 'Directory Scan' },
                { value: 'dns', label: 'DNS Subdomain Scan' },
                { value: 's3', label: 'S3 Bucket Scan' }
              ]}
            />
            <FormField
              label="Wordlist"
              type="select"
              value={wordlist}
              onChange={setWordlist}
              options={[
                { value: 'common.txt', label: 'Common' },
                { value: 'big.txt', label: 'Big' },
                { value: 'subdomains.txt', label: 'Subdomains' },
                { value: 'files.txt', label: 'Files' }
              ]}
            />
            <FormField
              label="Extensions"
              type="text"
              value={extensions}
              onChange={setExtensions}
              placeholder="php,html,txt"
              helperText="Comma-separated file extensions"
            />
            <FormField
              label="Threads"
              type="slider"
              value={threads}
              onChange={setThreads}
              min={1}
              max={200}
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
