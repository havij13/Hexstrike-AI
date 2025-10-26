import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'HexStrike AI Dashboard',
  description: 'Advanced AI-powered penetration testing framework dashboard',
  keywords: 'cybersecurity, penetration testing, AI, security tools, vulnerability assessment',
  authors: [{ name: 'HexStrike AI Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#00ff41',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} cyber-bg min-h-screen`}>
        <Providers>
          <div className="relative min-h-screen">
            {/* Scan line effect */}
            <div className="scan-line opacity-30"></div>
            <div className="flex h-screen">
              <Sidebar />
              <div className="flex-1 flex flex-col">
                <Header />
                <main className="flex-1 overflow-auto">
                  {children}
                </main>
              </div>
            </div>
          </div>
        </Providers>
      </body>
    </html>
  )
}
