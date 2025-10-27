'use client'

import { useState } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'

interface Tool {
  id: string
  name: string
  description: string
  status: 'available' | 'unavailable' | 'installed'
  category: string
  href?: string
}

interface ToolPaginationProps {
  tools: Tool[]
  itemsPerPage?: number
  onToolClick?: (tool: Tool) => void
  searchQuery?: string
}

export function ToolPagination({ 
  tools, 
  itemsPerPage = 9,
  onToolClick,
  searchQuery = ''
}: ToolPaginationProps) {
  const [currentPage, setCurrentPage] = useState(1)
  
  const filteredTools = tools.filter(tool => 
    tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    tool.description.toLowerCase().includes(searchQuery.toLowerCase())
  )
  
  const totalPages = Math.ceil(filteredTools.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const paginatedTools = filteredTools.slice(startIndex, endIndex)
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'text-neon-green'
      case 'installed': return 'text-neon-blue'
      case 'unavailable': return 'text-cyber-light opacity-50'
      default: return 'text-cyber-light'
    }
  }
  
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available': return '●'
      case 'installed': return '✓'
      case 'unavailable': return '✗'
      default: return '○'
    }
  }
  
  return (
    <div className="space-y-6">
      {/* Tool Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {paginatedTools.map((tool) => (
          <div
            key={tool.id}
            onClick={() => onToolClick?.(tool)}
            className="terminal-window border-neon-blue text-neon-blue hover:bg-neon-blue hover:text-cyber-dark transition-all duration-300 cursor-pointer group"
          >
            <div className="terminal-header">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-lg font-cyber font-bold">{tool.name}</span>
                </div>
                <div className={`flex items-center space-x-1 ${getStatusColor(tool.status)}`}>
                  <span className="text-xs">{getStatusIcon(tool.status)}</span>
                  <span className="text-xs font-mono">{tool.status}</span>
                </div>
              </div>
            </div>
            <div className="terminal-content">
              <p className="text-sm mb-4 opacity-90">{tool.description}</p>
              <div className="flex items-center justify-between pt-2 border-t border-neon-blue/30">
                <span className="text-xs font-mono">Click to configure and run</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center space-x-4">
          <button
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="px-4 py-2 bg-cyber-dark border border-neon-blue rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-neon-blue hover:text-cyber-dark transition-colors"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          
          <div className="flex items-center space-x-2">
            {Array.from({ length: totalPages }).map((_, i) => {
              const page = i + 1
              if (
                page === 1 ||
                page === totalPages ||
                (page >= currentPage - 2 && page <= currentPage + 2)
              ) {
                return (
                  <button
                    key={page}
                    onClick={() => setCurrentPage(page)}
                    className={`px-4 py-2 rounded ${
                      currentPage === page
                        ? 'bg-neon-blue text-cyber-dark'
                        : 'bg-cyber-dark border border-neon-blue hover:bg-neon-blue hover:text-cyber-dark'
                    } transition-colors`}
                  >
                    {page}
                  </button>
                )
              } else if (page === currentPage - 3 || page === currentPage + 3) {
                return <span key={page} className="text-cyber-light">...</span>
              }
              return null
            })}
          </div>
          
          <button
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="px-4 py-2 bg-cyber-dark border border-neon-blue rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-neon-blue hover:text-cyber-dark transition-colors"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
          
          <span className="text-sm text-cyber-light font-mono">
            Page {currentPage} of {totalPages} ({filteredTools.length} tools)
          </span>
        </div>
      )}
    </div>
  )
}
