#!/bin/bash

# HexStrike AI - Batch Tool Page Generator
# Generates multiple tool pages from a CSV-like input

echo "🚀 HexStrike AI - Batch Tool Page Generator"
echo "==========================================="
echo ""

# Define tools to generate (format: tool_name,category,api_endpoint,description)
TOOLS=(
  "dirb,web,/api/tools/dirb,Web directory brute forcer"
  "dirsearch,web,/api/tools/dirsearch,Web path scanner"
  "katana,web,/api/tools/katana,Crawler & spider"
  "enum4linux,network,/api/tools/enum4linux,SMB enumeration"
  "responder,network,/api/tools/responder,LLMNR/NBT-NS/mDNS responder"
  "metasploit,exploitation,/api/tools/metasploit,Exploitation framework"
  "msfvenom,exploitation,/api/tools/msfvenom,Payload generator"
  "volatility,forensics,/api/tools/volatility,Memory forensics"
  "binwalk,binary,/api/tools/binwalk,Binary analysis"
  "checksec,binary,/api/tools/checksec,Binary security check"
)

# Count total
TOTAL=${#TOOLS[@]}
CURRENT=0

# Function to generate a single tool page
generate_tool() {
  local tool_name=$1
  local category=$2
  local api_endpoint=$3
  local description=$4
  
  CURRENT=$((CURRENT + 1))
  echo "[$CURRENT/$TOTAL] Generating ${tool_name}..."
  
  # Create directory
  mkdir -p "Front-End/src/app/tools/${category}/${tool_name}"
  
  # Generate page
  cat > "Front-End/src/app/tools/${category}/${tool_name}/page.tsx" <<PAGE_EOF
'use client'

import { useState } from 'react'
import { ArrowLeft, Settings } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function ${tool_name^}Page() {
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
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com${api_endpoint}', {
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
        <Link href="/tools/${category}" className="text-cyber-primary hover:text-cyber-light transition-colors">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
            ${tool_name^^}
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            ${description}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Configuration"
            subtitle="Configure ${tool_name^}"
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
PAGE_EOF

  echo "  ✅ Generated: Front-End/src/app/tools/${category}/${tool_name}/page.tsx"
}

# Generate all tools
for tool in "${TOOLS[@]}"; do
  IFS=',' read -r tool_name category api_endpoint description <<< "$tool"
  generate_tool "$tool_name" "$category" "$api_endpoint" "$description"
done

echo ""
echo "✨ Batch generation complete!"
echo ""
echo "Generated $TOTAL tool pages:"
for tool in "${TOOLS[@]}"; do
  IFS=',' read -r tool_name category api_endpoint description <<< "$tool"
  echo "  - ${tool_name^} (${category})"
done
echo ""
echo "⚠️  Next steps:"
echo "1. Review generated pages for accuracy"
echo "2. Customize tool-specific parameters"
echo "3. Add proper scan profiles"
echo "4. Test each tool integration"
echo "5. Commit changes to git"
