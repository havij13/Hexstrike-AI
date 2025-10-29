'use client'

import { useState } from 'react'
import { 
  Shield, 
  Globe, 
  Search, 
  Play,
  Settings,
  ArrowLeft,
  Activity,
  Clock,
  Target,
  Bug
} from 'lucide-react'
import Link from 'next/link'
import { ToolPagination } from '@/components/pagination/ToolPagination'

export default function WebToolsPage() {
  const [searchQuery, setSearchQuery] = useState('')

  const webTools = [
    {
      id: 'gobuster',
      name: 'Gobuster',
      description: 'Directory/file brute-forcing tool for web applications',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/gobuster'
    },
    {
      id: 'feroxbuster',
      name: 'Feroxbuster',
      description: 'Fast recursive content discovery tool',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/feroxbuster'
    },
    {
      id: 'nuclei',
      name: 'Nuclei',
      description: 'Vulnerability scanner based on templates',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/nuclei'
    },
    {
      id: 'ffuf',
      name: 'FFuf',
      description: 'Fast web fuzzer and directory discovery',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/ffuf'
    },
    {
      id: 'nikto',
      name: 'Nikto',
      description: 'Web server vulnerability scanner',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/nikto'
    },
    {
      id: 'sqlmap',
      name: 'SQLMap',
      description: 'Automatic SQL injection testing tool',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/sqlmap'
    },
    {
      id: 'wpscan',
      name: 'WPScan',
      description: 'WordPress vulnerability scanner',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/wpscan'
    },
    {
      id: 'dalfox',
      name: 'Dalfox',
      description: 'XSS vulnerability scanner',
      status: 'available' as const,
      category: 'web',
      href: '/tools/web/dalfox'
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
              WEB APPLICATION SECURITY TOOLS
            </h1>
            <p className="text-cyber-light font-mono text-sm mt-1">
              8 web application testing and vulnerability scanning tools
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
        tools={webTools}
        searchQuery={searchQuery}
        onToolClick={handleToolClick}
      />
    </div>
  )
}

