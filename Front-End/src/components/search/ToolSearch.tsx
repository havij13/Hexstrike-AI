'use client'

import { useState, useEffect, useCallback } from 'react'
import { Search, X, Command, Filter } from 'lucide-react'

interface Tool {
  name: string
  href: string
  category: string
  description?: string
}

interface ToolSearchProps {
  tools: Tool[]
  onSelect?: (tool: Tool) => void
}

export function ToolSearch({ tools, onSelect }: ToolSearchProps) {
  const [query, setQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [isOpen, setIsOpen] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(0)

  const categories = ['all', ...Array.from(new Set(tools.map(t => t.category)))]

  const filteredTools = tools.filter(tool => {
    const matchesQuery = tool.name.toLowerCase().includes(query.toLowerCase()) ||
                        tool.description?.toLowerCase().includes(query.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || tool.category === selectedCategory
    return matchesQuery && matchesCategory
  })

  const handleSelect = useCallback((tool: Tool) => {
    onSelect?.(tool)
    setIsOpen(false)
    setQuery('')
  }, [onSelect])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd/Ctrl + K to open search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsOpen(true)
      }
      // Escape to close
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false)
      }
      // Arrow keys to navigate
      if (isOpen) {
        if (e.key === 'ArrowDown') {
          e.preventDefault()
          setSelectedIndex(prev => Math.min(prev + 1, filteredTools.length - 1))
        } else if (e.key === 'ArrowUp') {
          e.preventDefault()
          setSelectedIndex(prev => Math.max(prev - 1, 0))
        } else if (e.key === 'Enter') {
          e.preventDefault()
          if (filteredTools[selectedIndex]) {
            handleSelect(filteredTools[selectedIndex])
          }
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isOpen, filteredTools, selectedIndex, handleSelect])

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-4 py-2 bg-cyber-dark border border-cyber-primary rounded-lg text-cyber-light hover:bg-cyber-lighter transition-colors"
      >
        <Search className="h-4 w-4" />
        <span className="text-sm">Search tools...</span>
        <kbd className="hidden md:inline-flex items-center gap-1 px-2 py-1 text-xs font-mono bg-cyber-base border border-cyber-primary rounded">
          <Command className="h-3 w-3" />K
        </kbd>
      </button>
    )
  }

  return (
    <>
      {/* Overlay */}
      <div 
        className="fixed inset-0 bg-black/50 z-40"
        onClick={() => setIsOpen(false)}
      />
      
      {/* Search Modal */}
      <div className="fixed top-20 left-1/2 transform -translate-x-1/2 w-full max-w-2xl z-50">
        <div className="bg-cyber-dark border-2 border-cyber-primary rounded-lg shadow-2xl overflow-hidden">
          {/* Search Input */}
          <div className="flex items-center gap-2 p-4 border-b border-cyber-primary">
            <Search className="h-5 w-5 text-cyber-light" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search tools..."
              autoFocus
              className="flex-1 bg-transparent text-cyber-light placeholder:text-cyber-light/50 outline-none"
            />
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 text-cyber-light hover:text-neon-blue transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Category Filter */}
          <div className="flex gap-2 p-4 border-b border-cyber-primary overflow-x-auto">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1 rounded text-sm font-mono transition-colors ${
                  selectedCategory === cat
                    ? 'bg-neon-blue text-cyber-dark'
                    : 'bg-cyber-base text-cyber-light hover:bg-cyber-lighter'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Results */}
          <div className="max-h-96 overflow-y-auto">
            {filteredTools.length === 0 ? (
              <div className="p-8 text-center text-cyber-light">
                <Search className="h-12 w-12 mx-auto mb-4 text-cyber-primary/50" />
                <p className="text-sm">No tools found</p>
              </div>
            ) : (
              <div className="p-2">
                {filteredTools.map((tool, index) => (
                  <button
                    key={tool.href}
                    onClick={() => handleSelect(tool)}
                    className={`w-full text-left px-4 py-3 rounded transition-colors ${
                      index === selectedIndex
                        ? 'bg-neon-blue/20 text-neon-blue border-l-2 border-neon-blue'
                        : 'text-cyber-light hover:bg-cyber-lighter'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">{tool.name}</div>
                        <div className="text-xs text-cyber-light/70 mt-1">
                          {tool.description || tool.category}
                        </div>
                      </div>
                      <span className="text-xs px-2 py-1 bg-cyber-base rounded font-mono">
                        {tool.category}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between p-4 border-t border-cyber-primary text-xs text-cyber-light/50">
            <div className="flex items-center gap-4">
              <span className="flex items-center gap-1">
                ↑↓ Navigate
              </span>
              <span className="flex items-center gap-1">
                ↵ Select
              </span>
              <span className="flex items-center gap-1">
                Esc Close
              </span>
            </div>
            <span>{filteredTools.length} results</span>
          </div>
        </div>
      </div>
    </>
  )
}
