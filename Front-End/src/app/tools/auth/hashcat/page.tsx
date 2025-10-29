'use client'

import { useState } from 'react'
import { ArrowLeft, Cpu } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function HashcatPage() {
  const [hash, setHash] = useState('')
  const [hashType, setHashType] = useState('0')
  const [wordlist, setWordlist] = useState('rockyou.txt')
  const [attackMode, setAttackMode] = useState('0')
  const [workload, setWorkload] = useState('2')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    {
      id: 'standard',
      name: 'Standard Crack',
      description: 'Dictionary attack with medium workload',
      estimatedTime: '2-10 minutes',
      config: {
        attackMode: '0',
        workload: '2'
      }
    },
    {
      id: 'bruteforce',
      name: 'Brute Force',
      description: 'Brute force with mask attack',
      estimatedTime: 'Hours to days',
      config: {
        attackMode: '3',
        workload: '3'
      }
    },
    {
      id: 'optimized',
      name: 'Optimized',
      description: 'Optimized performance mode',
      estimatedTime: '1-5 minutes',
      config: {
        attackMode: '0',
        workload: '3'
      }
    }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setAttackMode(profile.config.attackMode)
    setWorkload(profile.config.workload)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/hashcat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          hash,
          hashType,
          wordlist,
          attackMode,
          workload
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
            HASHCAT
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            GPU-accelerated password recovery
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Crack Configuration"
            subtitle="Configure Hashcat parameters"
            icon={<Cpu className="h-5 w-5 text-neon-blue" />}
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
              helperText="MD5, SHA1, SHA256, NTLM, etc."
            />
            <FormField
              label="Hash Type"
              type="select"
              value={hashType}
              onChange={setHashType}
              options={[
                { value: '0', label: 'MD5' },
                { value: '100', label: 'SHA1' },
                { value: '1400', label: 'SHA256' },
                { value: '1700', label: 'SHA512' },
                { value: '1000', label: 'NTLM' },
                { value: '3200', label: 'bcrypt' },
                { value: '7500', label: 'Kerberos 5' },
                { value: '500', label: 'md5crypt' }
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
                { value: 'big.txt', label: 'Big' },
                { value: 'passwords.txt', label: 'Passwords' }
              ]}
            />
            <FormField
              label="Attack Mode"
              type="select"
              value={attackMode}
              onChange={setAttackMode}
              options={[
                { value: '0', label: 'Straight - Dictionary' },
                { value: '1', label: 'Combination' },
                { value: '3', label: 'Brute Force / Mask' },
                { value: '6', label: 'Hybrid Wordlist + Mask' }
              ]}
            />
            <FormField
              label="Workload Profile"
              type="select"
              value={workload}
              onChange={setWorkload}
              options={[
                { value: '1', label: 'Low (Faster)' },
                { value: '2', label: 'Medium (Balanced)' },
                { value: '3', label: 'High (Thorough)' },
                { value: '4', label: 'Nightmare (Maximum)' }
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
