#!/bin/bash

# HexStrike AI - Tool Page Generator
# Automatically generates Next.js tool pages from API endpoint definitions

TOOL_NAME=$1
CATEGORY=$2
API_ENDPOINT=$3
DESCRIPTION=${4:-"Security tool"}

if [ -z "$TOOL_NAME" ] || [ -z "$CATEGORY" ] || [ -z "$API_ENDPOINT" ]; then
    echo "Usage: $0 <tool-name> <category> <api-endpoint> [description]"
    echo "Example: $0 dirb web /api/tools/dirb \"Web directory brute forcer\""
    exit 1
fi

# Create directory structure
mkdir -p "Front-End/src/app/tools/${CATEGORY}/${TOOL_NAME}"

# Generate page.tsx
cat > "Front-End/src/app/tools/${CATEGORY}/${TOOL_NAME}/page.tsx" <<EOF
'use client'

import { useState } from 'react'
import { ArrowLeft, Settings } from 'lucide-react'
import Link from 'next/link'
import { ToolForm } from '@/components/forms/ToolForm'
import { FormField } from '@/components/forms/FormField'
import { ScanProfiles } from '@/components/forms/ScanProfiles'
import { ResultsPanel } from '@/components/results/ResultsPanel'

export default function ${TOOL_NAME^}Page() {
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
      const response = await fetch('https://hexstrike-ai-v6-0.onrender.com${API_ENDPOINT}', {
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
        <Link href="/tools/${CATEGORY}" className="text-cyber-primary hover:text-cyber-light transition-colors">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
            ${TOOL_NAME^^}
          </h1>
          <p className="text-cyber-light font-mono text-sm mt-1">
            ${DESCRIPTION}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ToolForm 
            title="Scan Configuration"
            subtitle="Configure ${TOOL_NAME^}"
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
EOF

echo "✅ Generated tool page: Front-End/src/app/tools/${CATEGORY}/${TOOL_NAME}/page.tsx"
echo ""
echo "Next steps:"
echo "1. Review and customize the generated page.tsx"
echo "2. Add tool-specific parameters to FormField"
echo "3. Update scan profiles if needed"
echo "4. Test the tool integration"
