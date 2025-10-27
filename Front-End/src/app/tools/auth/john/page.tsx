'use client'

import { useState } from 'react'
import { ArrowLeft, KeyRound } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function JohnPage() {
  const [hash, setHash] = useState('')
  const [hashType, setHashType] = useState('auto')
  const [wordlist, setWordlist] = useState('rockyou.txt')
  const [rules, setRules] = useState('Single')
  const [incremental, setIncremental] = useState(false)
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard Crack',
      description: 'Quick dictionary attack',
      estimatedTime: '1-5 minutes',
      config: {
        wordlist: 'rockyou.txt',
        rules: 'Single',
        incremental: false
      }
    },
    {
      id: 'rules',
      name: 'Rules Attack',
      description: 'Dictionary with mutation rules',
      estimatedTime: '5-30 minutes',
      config: {
        wordlist: 'rockyou.txt',
        rules: 'Best64',
        incremental: false
      }
    },
    {
      id: 'brute',
      name: 'Brute Force',
      description: 'Incremental brute force attack',
      estimatedTime: 'Hours to days',
      config: {
        wordlist: 'rockyou.txt',
        rules: 'None',
        incremental: true
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setWordlist(profile.config.wordlist)
    setRules(profile.config.rules)
    setIncremental(profile.config.incremental)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/john', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          hash,
          hashType,
          wordlist,
          rules,
          incremental
        }),
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Crack failed:', error)
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
            JOHN THE RIPPER
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            Password hash cracker
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Crack Configuration"
            subtitle="Configure John parameters"
            icon={<KeyRound className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Hash"
              type="textarea"
              value={hash}
              onChange={setHash}
              placeholder="Paste hash here..."
              required
              helperText="MD5, SHA1, SHA256, bcrypt, etc."
            />
            <FormField
              label="Hash Type"
              type="select"
              value={hashType}
              onChange={setHashType}
              options={[
                { value: 'auto', label: 'Auto-detect' },
                { value: 'md5', label: 'MD5' },
                { value: 'sha1', label: 'SHA1' },
                { value: 'sha256', label: 'SHA256' },
                { value: 'sha512', label: 'SHA512' },
                { value: 'bcrypt', label: 'bcrypt' },
                { value: 'nt', label: 'NTLM' },
                { value: 'lm', label: 'LM' }
              ]}
            />
            <FormField
              label="Wordlist"
              type="select"
              value={wordlist}
              onChange={setWordlist}
              options={[
                { value: 'rockyou.txt', label: 'RockYou' },
                { value: 'common.txt', label: 'Common' },
                { value: 'big.txt', label: 'Big' }
              ]}
            />
            <FormField
              label="Rules"
              type="select"
              value={rules}
              onChange={setRules}
              options={[
                { value: 'None', label: 'No Rules' },
                { value: 'Single', label: 'Single' },
                { value: 'Best64', label: 'Best64' },
                { value: 'All', label: 'All' }
              ]}
            />
            <FormField
              label="Incremental Mode"
              type="checkbox"
              value={incremental}
              onChange={setIncremental}
              helperText="Brute force mode (can take very long)"
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
