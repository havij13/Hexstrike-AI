'use client'

import { useState } from 'react'
import { ArrowLeft, Lock } from 'lucide-react'
import Link from 'next/link'
import { ToolPagination } from '@/components/pagination/ToolPagination'

export default function AuthToolsPage() {
  const [searchQuery, setSearchQuery] = useState('')

  const authTools = [
    {
      id: 'hydra',
      name: 'Hydra',
      description: 'Network login cracker supporting multiple protocols',
      status: 'available' as const,
      category: 'auth',
      href: '/tools/auth/hydra'
    },
    {
      id: 'john',
      name: 'John the Ripper',
      description: 'Password hash cracker',
      status: 'available' as const,
      category: 'auth',
      href: '/tools/auth/john'
    },
    {
      id: 'hashcat',
      name: 'Hashcat',
      description: 'Advanced password recovery tool with GPU acceleration',
      status: 'available' as const,
      category: 'auth',
      href: '/tools/auth/hashcat'
    },
    {
      id: 'medusa',
      name: 'Medusa',
      description: 'Parallel login brute-forcer',
      status: 'available' as const,
      category: 'auth',
      href: '/tools/auth/medusa'
    },
    {
      id: 'netexec',
      name: 'NetExec',
      description: 'Network protocol toolkit (formerly CrackMapExec)',
      status: 'available' as const,
      category: 'auth',
      href: '/tools/auth/netexec'
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
              AUTHENTICATION & PASSWORD SECURITY TOOLS
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              5 authentication and password security tools
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
        tools={authTools}
        searchQuery={searchQuery}
        onToolClick={handleToolClick}
      />
    </div>
  )
}
