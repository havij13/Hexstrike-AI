'use client'

import { Target, Clock } from 'lucide-react'

interface ScanProfile {
  id: string
  name: string
  description: string
  estimatedTime: string
  config: any
}

interface ScanProfilesProps {
  profiles: ScanProfile[]
  selectedProfile?: string
  onSelectProfile: (profile: ScanProfile) => void
}

export function ScanProfiles({ profiles, selectedProfile, onSelectProfile }: ScanProfilesProps) {
  return (
    <div className="terminal-window">
      <div className="terminal-header">
        <div className="flex items-center space-x-2">
          <Target className="h-5 w-5 text-neon-blue" />
          <span className="text-sm font-medium">Scan Profiles</span>
        </div>
      </div>
      <div className="terminal-content">
        <div className="space-y-3">
          {profiles.map((profile) => (
            <div
              key={profile.id}
              onClick={() => onSelectProfile(profile)}
              className={`p-3 border rounded cursor-pointer transition-all ${
                selectedProfile === profile.id
                  ? 'border-neon-blue bg-neon-blue/10 shadow-lg shadow-neon-blue/20'
                  : 'border-neon-blue/30 hover:border-neon-blue/60 hover:bg-neon-blue/5'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-cyber-primary">{profile.name}</span>
                <div className="flex items-center space-x-1 text-xs text-cyber-light">
                  <Clock className="h-3 w-3" />
                  <span>{profile.estimatedTime}</span>
                </div>
              </div>
              <p className="text-xs text-cyber-light opacity-75">{profile.description}</p>
              {selectedProfile === profile.id && (
                <div className="mt-2 pt-2 border-t border-neon-blue/30">
                  <span className="text-xs text-neon-blue">✓ Selected</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
