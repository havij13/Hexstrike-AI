'use client'

import { useState } from 'react'
import { ArrowLeft, Search } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function FFufPage() {
  const [url, setUrl] = useState('https://target.com')
  const [wordlist, setWordlist] = useState('common.txt')
  const [method, setMethod] = useState('GET')
  const [threads, setThreads] = useState(10)
  const [match, setMatch] = useState('200,204,301,302,307,401,403')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('quick')

  const scanProfiles = [
    {
      id: 'quick',
      name: 'Quick Fuzz',
      description: 'Fast directory fuzzing with common status codes',
      estimatedTime: '30-60 seconds',
      config: {
        wordlist: 'common.txt',
        method: 'GET',
        threads: 10,
        match: '200,204,301,302,307,401,403'
      }
    },
    {
      id: 'comprehensive',
      name: 'Comprehensive Fuzz',
      description: 'Thorough fuzzing with extended wordlist',
      estimatedTime: '5-10 minutes',
      config: {
        wordlist: 'big.txt',
        method: 'GET',
        threads: 50,
        match: '200,204,301,302,307,401,403,405,500'
      }
    },
    {
      id: 'post',
      name: 'POST Request Fuzz',
      description: 'Fuzz POST endpoints',
      estimatedTime: '2-5 minutes',
      config: {
        wordlist: 'common.txt',
        method: 'POST',
        threads: 10,
        match: '200,201,204,301,302,401,403'
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setWordlist(profile.config.wordlist)
    setMethod(profile.config.method)
    setThreads(profile.config.threads)
    setMatch(profile.config.match)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/ffuf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          wordlist,
          method,
          threads,
          match
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
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Link href="/tools/web" className="text-cyber-primary hover:text-cyber-light transition-colors">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
            FFUF
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Fast web fuzzer and directory discovery
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration Panel */}
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure FFuf parameters"
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
              label="Wordlist"
              type="select"
              value={wordlist}
              onChange={setWordlist}
              options={[
                { value: 'common.txt', label: 'Common' },
                { value: 'big.txt', label: 'Big' },
                { value: 'raft.txt', label: 'Raft' },
                { value: 'subdomains.txt', label: 'Subdomains' }
              ]}
            />
            <FormField
              label="HTTP Method"
              type="select"
              value={method}
              onChange={setMethod}
              options={[
                { value: 'GET', label: 'GET' },
                { value: 'POST', label: 'POST' },
                { value: 'PUT', label: 'PUT' },
                { value: 'DELETE', label: 'DELETE' }
              ]}
            />
            <FormField
              label="Threads"
              type="slider"
              value={threads}
              onChange={setThreads}
              min={1}
              max={100}
              step={1}
            />
            <FormField
              label="Match Status Codes"
              type="text"
              value={match}
              onChange={setMatch}
              placeholder="200,204,301,302"
              helperText="Comma-separated status codes to match"
            />
          </ToolForm>

          <ScanProfiles
            profiles={scanProfiles}
            selectedProfile={selectedProfile}
            onSelectProfile={handleSelectProfile}
          />
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2">
          <ResultsPanel results={results} />
        </div>
      </div>
    </div>
  )
}
