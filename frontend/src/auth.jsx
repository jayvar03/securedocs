import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { api, clearToken, getToken, setToken, setUnauthorizedHandler } from './api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(Boolean(getToken()))

  const logout = useCallback(() => {
    clearToken()
    setUser(null)
  }, [])

  useEffect(() => {
    setUnauthorizedHandler(() => setUser(null))
  }, [])

  useEffect(() => {
    if (!getToken()) return
    api('/api/users/me')
      .then(setUser)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const startSession = useCallback(async (path, payload) => {
    const data = await api(path, { method: 'POST', json: payload, noAuthRedirect: true })
    setToken(data.access_token)
    if (data.user) {
      setUser(data.user)
    } else {
      setUser(await api('/api/users/me'))
    }
  }, [])

  const login = useCallback((email, password) => startSession('/api/auth/login', { email, password }), [startSession])
  const register = useCallback(
    (company_name, email, password) =>
      startSession('/api/auth/register-tenant', { company_name, email, password }),
    [startSession],
  )

  const value = useMemo(() => ({ user, loading, login, register, logout }), [user, loading, login, register, logout])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
