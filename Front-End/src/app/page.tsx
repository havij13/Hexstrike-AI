import { Dashboard } from '@/components/Dashboard'
import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'

export default function Home() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 overflow-auto">
          <Dashboard />
        </main>
      </div>
    </div>
  )
}
