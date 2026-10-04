import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { useAuth } from './auth.jsx'
import Layout from './components/Layout.jsx'
import Spinner from './components/Spinner.jsx'
import Audit from './pages/Audit.jsx'
import Chat from './pages/Chat.jsx'
import Documents from './pages/Documents.jsx'
import Login from './pages/Login.jsx'
import Users from './pages/Users.jsx'

function Protected({ roles }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="p-10"><Spinner label="Loading your account" /></div>
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />
  return <Outlet />
}

export default function App() {
  const { user } = useAuth()
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <Login />} />
      <Route element={<Protected />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Chat />} />
          <Route path="/documents" element={<Documents />} />
          <Route element={<Protected roles={['admin']} />}>
            <Route path="/users" element={<Users />} />
            <Route path="/audit" element={<Audit />} />
          </Route>
        </Route>
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
