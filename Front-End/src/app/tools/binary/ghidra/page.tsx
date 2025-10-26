'use client'

import { useState } from 'react'
import { ArrowLeft, Code } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function GhidraPage() {
  const [binaryFile, setBinaryFile] = useState('')
  const [analysisType, setAnalysisType] = useState('basic')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('basic')

  const scanProfiles = [
    { id: 'basic', name: 'Basic Analysis', description: 'Basic reverse engineering', estimatedTime: '5-10 minutes', config: { analysisType: 'basic' } },
    { id: 'detailed', name: 'Detailed Analysis', description: 'Comprehensive analysis', estimatedTime: '15-30 minutes', config: { analysisType: 'detailed' } },
    { id: 'full', name: 'Full Analysis', description: 'Complete decompilation', estimatedTime: '30-60 minutes', config: { analysisType: 'full' } }
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
    setAnalysisType(profile.config.analysisType)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com/api/tools/ghidra', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ binary_file: binaryFile, analysis_type: analysisType }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Analysis failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools" className="text-cyber-primary hover:text-cyber-light transition-colors"><ArrowLeft className="h-6 w-6" /></Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">GHIDRA</h1>
          <p className="text-cyber-light font-mono text-sm mt-1">Software reverse engineering framework</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm title="Analysis Configuration" subtitle="Configure Ghidra" icon={<Code className="h-5 w-5 text-neon-blue" />} isRunning={isRunning} onSubmit={handleScan}>
            <FormField label="Binary File" type="file" value={binaryFile} onChange={setBinaryFile} placeholder="Upload binary..." required />
            <FormField label="Analysis Type" type="select" value={analysisType} onChange={setAnalysisType} options={[
              { value: 'basic', label: 'Basic' },
              { value: 'detailed', label: 'Detailed' },
              { value: 'full', label: 'Full Analysis' }
            ]} />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
