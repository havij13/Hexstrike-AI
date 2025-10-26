#!/bin/bash

# HexStrike AI - Batch Tool Page Generator
# Generates multiple tool pages from a CSV-like input

echo "🚀 HexStrike AI - Batch Tool Page Generator"
echo "==========================================="
echo ""

# Define tools to generate (format: tool_name,category,api_endpoint,description)
TOOLS=(
  # Web Security (more)
  "dirb,web,/api/tools/dirb,Web directory brute forcer"
  "dirsearch,web,/api/tools/dirsearch,Web path scanner"
  "katana,web,/api/tools/katana,Crawler & spider"
  "gau,web,/api/tools/gau,Subdomain finder"
  "waybackurls,web,/api/tools/waybackurls,URL discovery"
  "arjun,web,/api/tools/arjun,Parameter discovery"
  "httpx,web,/api/tools/httpx,HTTP probe"
  "anew,web,/api/tools/anew,Line processor"
  "uro,web,/api/tools/uro,URL cleaner"
  "paramspider,web,/api/tools/paramspider,Parameter finder"
  "jaeles,web,/api/tools/jaeles,Web vulnerability scanner"
  "hakrawler,web,/api/tools/hakrawler,Web crawler"
  "dotdotpwn,web,/api/tools/dotdotpwn,Path traversal scanner"
  "xsser,web,/api/tools/xsser,XSS scanner"
  "wfuzz,web,/api/tools/wfuzz,Web fuzzer"
  "wafw00f,web,/api/tools/wafw00f,WAF detector"
  "burpsuite-alternative,web,/api/tools/burpsuite-alternative,Web vulnerability scanner"
  "api-fuzzer,web,/api/tools/api_fuzzer,API fuzzer"
  "graphql-scanner,web,/api/tools/graphql_scanner,GraphQL security scanner"
  "jwt-analyzer,web,/api/tools/jwt_analyzer,JWT security analyzer"
  "api-schema-analyzer,web,/api/tools/api_schema_analyzer,API schema analysis"
  
  # Network & Infrastructure
  "enum4linux,network,/api/tools/enum4linux,SMB enumeration"
  "responder,network,/api/tools/responder,LLMNR/NBT-NS/mDNS responder"
  "rpcclient,network,/api/tools/rpcclient,RPC enumeration"
  "nbtscan,network,/api/tools/nbtscan,NetBIOS scanner"
  "arp-scan,network,/api/tools/arp-scan,ARP scanner"
  
  # Exploitation
  "metasploit,exploitation,/api/tools/metasploit,Exploitation framework"
  "msfvenom,exploitation,/api/tools/msfvenom,Payload generator"
  
  # Binary Analysis
  "binwalk,binary,/api/tools/binwalk,Binary analysis"
  "checksec,binary,/api/tools/checksec,Binary security check"
  "ropgadget,binary,/api/tools/ropgadget,ROP gadget finder"
  "xxd,binary,/api/tools/xxd,Hexdump"
  "strings,binary,/api/tools/strings,String extractor"
  "objdump,binary,/api/tools/objdump,Binary disassembler"
  "pwntools,binary,/api/tools/pwntools,CTF framework"
  "one-gadget,binary,/api/tools/one-gadget,Gadget finder"
  "libc-database,binary,/api/tools/libc-database,Libc database"
  "gdb-peda,binary,/api/tools/gdb-peda,GDB enhancement"
  "angr,binary,/api/tools/angr,Binary analysis framework"
  "ropper,binary,/api/tools/ropper,ROP chain builder"
  "pwninit,binary,/api/tools/pwninit,CTF setup tool"
  
  # Forensics
  "volatility,forensics,/api/tools/volatility,Memory forensics"
  "foremost,forensics,/api/tools/foremost,File carving"
  "steghide,forensics,/api/tools/steghide,Steganography tool"
  "exiftool,forensics,/api/tools/exiftool,Metadata extractor"
  "hashpump,forensics,/api/tools/hashpump,Hash extension"
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
