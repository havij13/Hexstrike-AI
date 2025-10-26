# HexStrike AI - Tool Page Batch Generator (PowerShell)
# Generates multiple tool pages from a list

param(
    [Parameter(Mandatory=$false)]
    [string]$BatchSize = "10"
)

Write-Host "🚀 HexStrike AI - Batch Tool Page Generator (PowerShell)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Define tools to generate (format: tool_name|category|api_endpoint|description)
$tools = @(
    # Binary Analysis - Batch 3
    "one-gadget|binary|/api/tools/one-gadget|Gadget finder",
    "libc-database|binary|/api/tools/libc-database|Libc database",
    "gdb-peda|binary|/api/tools/gdb-peda|GDB enhancement",
    "angr|binary|/api/tools/angr|Binary analysis framework",
    "ropper|binary|/api/tools/ropper|ROP chain builder",
    "pwninit|binary|/api/tools/pwninit|CTF setup tool",
    
    # Forensics - Batch 4
    "exiftool|forensics|/api/tools/exiftool|Metadata extractor",
    "hashpump|forensics|/api/tools/hashpump|Hash extension",
    
    # Web Security - Additional
    "api-fuzzer|web|/api/tools/api_fuzzer|API fuzzer",
    "graphql-scanner|web|/api/tools/graphql_scanner|GraphQL security scanner"
)

$current = 0
$total = $tools.Count

foreach ($toolString in $tools) {
    $parts = $toolString -split '\|'
    if ($parts.Count -ne 4) { continue }
    
    $tool_name = $parts[0]
    $category = $parts[1]
    $api_endpoint = $parts[2]
    $description = $parts[3]
    
    $current++
    Write-Host "[$current/$total] Generating $tool_name..." -ForegroundColor Yellow
    
    # Create directory
    $dirPath = "Front-End\src\app\tools\$category\$tool_name"
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
    
    # Capitalize tool name for component
    $temp = $tool_name -replace '-', ' '
    $temp = $temp -replace '_', ' '
    $toolNameCapitalized = (Get-Culture).TextInfo.ToTitleCase($temp.ToLower())
    $toolNameCapitalized = $toolNameCapitalized -replace ' ', ''
    
    # Generate page
    $pageContent = @"
'use client'

import { useState } from 'react'
import { ArrowLeft, Settings } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function ${toolNameCapitalized}Page() {
  const [target, setTarget] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [selectedProfile, setSelectedProfile] = useState<string>('standard')

  const scanProfiles = [
    { id: 'standard', name: 'Standard Scan', description: 'Standard configuration', estimatedTime: '5-10 minutes', config: {} },
  ]

  const handleSelectProfile = (profile: any) => {
    setSelectedProfile(profile.id)
  }

  const handleScan = async () => {
    setIsRunning(true)
    try {
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com$api_endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target }),
      })
      setResults(await response.json())
    } catch (error) { console.error('Scan failed:', error) } finally { setIsRunning(false) }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <Link href="/tools/$category" className="text-cyber-primary hover:text-cyber-light transition-colors">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
            $($tool_name.ToUpper())
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            $description
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Configuration"
            subtitle="Configure $toolNameCapitalized"
            icon={<Settings className="h-5 w-5 text-neon-blue" />}
            isRunning={isRunning}
            onSubmit={handleScan}
          >
            <FormField
              label="Target"
              type="text"
              value={target}
              onChange={setTarget}
              placeholder="Enter target..."
              required
            />
          </ToolForm>
          <ScanProfiles profiles={scanProfiles} selectedProfile={selectedProfile} onSelectProfile={handleSelectProfile} />
        </div>
        <div className="lg:col-span-2"><ResultsPanel results={results} /></div>
      </div>
    </div>
  )
}
"@

    $pageContent | Out-File -FilePath "$dirPath\page.tsx" -Encoding UTF8
    Write-Host "  ✅ Generated: $dirPath\page.tsx" -ForegroundColor Green
}

Write-Host ""
Write-Host "✨ Batch generation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Generated $total tool pages." -ForegroundColor Cyan
