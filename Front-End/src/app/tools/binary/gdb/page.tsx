'use client'

import { useState } from 'react'
import { ArrowLeft, Code } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function GDBPage() {
  const [binaryFile, setBinaryFile] = useState('')
  const [command, setCommand] = useState('run')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('basic')

  const scanProfiles = [
    { id: 'basic', name: 'Basic Debug', description: 'Basic debugging', estimatedTime: '2-5 minutes', config: { command: 'run' } },
    { id: 'breakpoints', name: 'Breakpoints', description: 'Set breakpoints', estimatedTime: '5-10 minutes', config: { command: 'break main' } },
    { id: 'disassembly', name: 'Disassembly', description: 'Disassemble code', estimatedTime: '3-8 minutes', config: { command: 'disass main' } }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setCommand(profile.config.command)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/gdb', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ binary_file: binaryFile, command }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Debug failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">GDB</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">GNU Debugger</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Debug Configuration" subtitle="Configure GDB" icon={<Code className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Binary File" type="file" value={binaryFile} onChange={setBinaryFile} placeholder="Upload binary..." required />
            <FormField label="GDB Command" type="textarea" value={command} onChange={setCommand} placeholder="run, break main, disass main" />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
