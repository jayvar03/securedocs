import { Outlet } from 'react-router-dom'
import { useAuth } from '../auth.jsx'
import Button from './Button.jsx'
import Nav from './Nav.jsx'
import RoleLabel from './RoleLabel.jsx'

export default function Layout() {
  const { user, logout } = useAuth()
  return (
    <div className="min-h-screen bg-paper">
      <header className="sticky top-0 z-30 border-b border-rule/80 bg-panel/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3 sm:px-6">
          {/* Left: Brand */}
          <div className="flex items-center gap-2.5">
            <img src="/favicon.svg" alt="Logo" className="h-8 w-8 rounded-md shadow-2xs" />
            <div>
              <p className="font-serif text-lg leading-tight font-medium tracking-tight text-ink">SecureDocs</p>
              <p className="text-[0.7rem] text-muted font-mono leading-none">{user.company_name}</p>
            </div>
          </div>

          {/* Center: Navigation on desktop */}
          <div className="hidden md:flex justify-center">
            <Nav />
          </div>

          {/* Right: User status & Logout */}
          <div className="flex items-center gap-3 text-sm">
            <span className="hidden font-mono text-xs text-muted sm:inline">{user.email}</span>
            <RoleLabel role={user.role} />
            <Button variant="secondary" onClick={logout} className="text-xs py-1 px-3">Sign out</Button>
          </div>
        </div>

        {/* Center: Mobile Navigation row */}
        <div className="flex justify-center pb-2.5 md:hidden">
          <Nav />
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6">
        <Outlet />
      </main>
    </div>
  )
}

