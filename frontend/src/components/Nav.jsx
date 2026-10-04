import { NavLink } from 'react-router-dom'
import { useAuth } from '../auth.jsx'

const linkStyle = ({ isActive }) =>
  `rounded-full px-3.5 py-1 text-sm font-medium transition-all ${
    isActive
      ? 'bg-panel text-accent shadow-2xs font-semibold'
      : 'text-muted hover:text-ink hover:bg-panel/40'
  }`

export default function Nav() {
  const { user } = useAuth()
  return (
    <nav aria-label="Main" className="inline-flex items-center rounded-full border border-rule/80 bg-paper/80 p-1 shadow-2xs">
      <NavLink to="/" end className={linkStyle}>Ask</NavLink>
      <NavLink to="/documents" className={linkStyle}>Documents</NavLink>
      {user.role === 'admin' && (
        <>
          <NavLink to="/users" className={linkStyle}>Users</NavLink>
          <NavLink to="/audit" className={linkStyle}>Audit log</NavLink>
        </>
      )}
    </nav>
  )
}

