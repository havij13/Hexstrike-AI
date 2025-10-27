'use client'

export function PulseLoader() {
  return (
    <div className="flex items-center justify-center space-x-2">
      <div className="w-2 h-2 bg-neon-blue rounded-full animate-pulse"></div>
      <div className="w-2 h-2 bg-neon-blue rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
      <div className="w-2 h-2 bg-neon-blue rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
    </div>
  )
}

export function Spinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  }

  return (
    <div className={`${sizes[size]} border-4 border-cyber-primary border-t-neon-blue rounded-full animate-spin`} />
  )
}
