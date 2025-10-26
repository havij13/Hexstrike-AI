'use client'

import { useState } from 'react'
import { ArrowLeft, Network } from 'lucide-react'
import Link from 'next/link'
import { ToolPagination } from '@/components/pagination/ToolPagination'

export default function NetworkToolsPage() {
  const [searchQuery, setSearchQuery] = useState('')

  const networkTools = [
    {
      id: 'nmap',
      name: 'Nmap',
      description: 'Network exploration and security auditing tool',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/nmap'
    },
    {
      id: 'rustscan',
      name: 'Rustscan',
      description: 'Fast port scanner written in Rust',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/rustscan'
    },
    {
      id: 'masscan',
      name: 'Masscan',
      description: 'High-speed TCP port scanner',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/masscan'
    },
    {
      id: 'autorecon',
      name: 'AutoRecon',
      description: 'Automated reconnaissance framework',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/autorecon'
    },
    {
      id: 'amass',
      name: 'Amass',
      description: 'In-depth subdomain enumeration tool',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/amass'
    },
    {
      id: 'subfinder',
      name: 'Subfinder',
      description: 'Passive subdomain discovery tool',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/subfinder'
    },
    {
      id: 'fierce',
      name: 'Fierce',
      description: 'DNS reconnaissance tool',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/fierce'
    },
    {
      id: 'dnsenum',
      name: 'DNSenum',
      description: 'DNS enumeration and zone transfer tool',
      status: 'available' as const,
      category: 'network',
      href: '/tools/network/dnsenum'
    }
  ]

  const handleToolClick = (tool: { id: string; name: string; description: string; status: 'available' | 'unavailable' | 'installed'; category: string; href?: string }) => {
    if (tool.href) {
      window.location.href = tool.href
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link href="/tools" className="text-cyber-primary hover:text-cyber-light transition-colors">
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-3xl font-cyber font-bold text-neon-blue neon-glow">
              NETWORK RECONNAISSANCE TOOLS
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              8 network reconnaissance and security scanning tools
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Search tools..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-4 py-2 bg-cyber-dark border border-neon-blue rounded text-cyber-primary font-mono placeholder-cyber-light placeholder-opacity-50 focus:outline-none focus:border-neon-blue"
          />
        </div>
      </div>

      {/* Tools with Pagination */}
      <ToolPagination 
        tools={networkTools}
        searchQuery={searchQuery}
        onToolClick={handleToolClick}
      />
    </div>
  )
}

