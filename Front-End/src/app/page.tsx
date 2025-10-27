import { Dashboard } from '@/components/Dashboard'
import { FileText, Zap, Shield, Code } from 'lucide-react'
import React from 'react';

export default function Home() {
  return (
    <>
      {/* MCP Integration Info Banner */}
      <div className="bg-gradient-to-r from-red-900/20 to-cyber-dark border-b border-neon-red/30 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <FileText className="h-8 w-8 text-neon-red" />
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-cyber font-bold text-neon-red neon-glow mb-2">
                🚀 HexStrike AI - MCP Integration
              </h2>
              <p className="text-cyber-light text-sm mb-4">
                HexStrike AI now supports <strong className="text-neon-blue">Model Context Protocol (MCP)</strong> for seamless AI agent integration with Claude Desktop, Cursor, and VS Code Copilot.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                <div className="bg-cyber-dark/50 border border-neon-red/20 rounded p-3">
                  <div className="flex items-center space-x-2 mb-1">
                    <Zap className="h-4 w-4 text-neon-red" />
                    <span className="text-sm font-bold text-neon-red">150+ Security Tools</span>
                  </div>
                  <p className="text-xs text-cyber-light opacity-75">
                    Network, Web, Auth, Binary Analysis & more
                  </p>
                </div>
                <div className="bg-cyber-dark/50 border border-neon-red/20 rounded p-3">
                  <div className="flex items-center space-x-2 mb-1">
                    <Shield className="h-4 w-4 text-neon-red" />
                    <span className="text-sm font-bold text-neon-red">12+ AI Agents</span>
                  </div>
                  <p className="text-xs text-cyber-light opacity-75">
                    Automated security testing workflows
                  </p>
                </div>
                <div className="bg-cyber-dark/50 border border-neon-red/20 rounded p-3">
                  <div className="flex items-center space-x-2 mb-1">
                    <Code className="h-4 w-4 text-neon-red" />
                    <span className="text-sm font-bold text-neon-red">MCP Protocol</span>
                  </div>
                  <p className="text-xs text-cyber-light opacity-75">
                    Connect via hexstrike_mcp.py
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Main Dashboard Content */}
      <Dashboard />
    </>
  )
}
