'use client'

import { useState } from 'react'
import { Zap, Globe, Settings, User } from 'lucide-react'
import { MenuBar } from './MenuBar'

export function Header() {
  const [isOnline, setIsOnline] = useState(true)

  return (
    <header className="bg-cyber-dark border-b border-cyber-primary px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Logo and Title */}
        <MenuBar />
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Zap className="h-8 w-8 text-cyber-primary animate-pulse-neon" />
            <h1 className="text-2xl font-cyber font-bold text-cyber-primary neon-glow">
              HEXSTRIKE AI
            </h1>
          </div>
          <div className="hidden md:block">
            <span className="text-cyber-light text-sm font-mono">
              v6.0 - Advanced Penetration Testing Framework
            </span>
          </div>
        </div>

        {/* Status and Controls */}
        <div className="flex items-center space-x-6">
          {/* Connection Status */}
          <div className="flex items-center space-x-2">
            <Globe className="h-5 w-5 text-cyber-primary" />
            <span className="text-sm font-mono text-cyber-light">API:</span>
            <div className={`px-2 py-1 rounded-full text-xs font-medium ${
              isOnline 
                ? 'bg-green-900 text-green-300 border border-green-700' 
                : 'bg-red-900 text-red-300 border border-red-700'
            }`}>
              {isOnline ? 'ONLINE' : 'OFFLINE'}
            </div>
          </div>

          {/* Server URL */}
          <div className="hidden lg:block">
            <span className="text-xs font-mono text-cyber-light">
              hexstrike-ai-v6-0.onrender.com
            </span>
          </div>

          {/* Controls */}
          <div className="flex items-center space-x-2">
            <button className="p-2 text-cyber-light hover:text-cyber-primary transition-colors">
              <Settings className="h-5 w-5" />
            </button>
            <button className="p-2 text-cyber-light hover:text-cyber-primary transition-colors">
              <User className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Scan line effect */}
      <div className="scan-line opacity-20"></div>
    </header>
  )
}
