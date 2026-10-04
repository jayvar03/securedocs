import { useState } from 'react'
import { useAuth } from '../auth.jsx'
import Button from '../components/Button.jsx'
import ErrorNote from '../components/ErrorNote.jsx'
import Field from '../components/Field.jsx'

const DEMO_PASSWORD = 'Passw0rd!demo'
const DEMO_ACCOUNTS = [
  { label: 'Acme admin', email: 'admin@acme.example' },
  { label: 'Acme manager', email: 'manager@acme.example' },
  { label: 'Acme employee', email: 'employee@acme.example' },
  { label: 'Globex admin', email: 'admin@globex.example' },
]

export default function Login() {
  const { login, register } = useAuth()
  const [mode, setMode] = useState('login')
  const [company, setCompany] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function run(fn) {
    setBusy(true)
    setError('')
    try {
      await fn()
    } catch (e) {
      setError(e.message)
      setBusy(false)
    }
  }

  const submit = (e) => {
    e.preventDefault()
    run(() => (mode === 'login' ? login(email, password) : register(company, email, password)))
  }

  const isLogin = mode === 'login'
  return (
    <div className="mx-auto min-h-screen max-w-5xl px-4 py-12 flex items-center justify-center">
      <div className="grid w-full gap-10 md:grid-cols-12 md:items-center">
        {/* Left Side: Project Name, Hero & Description */}
        <section className="md:col-span-6 lg:col-span-6 space-y-5">
          <div className="inline-flex items-center gap-2.5 rounded-full border border-rule/80 bg-panel px-3 py-1.5 shadow-2xs">
            <img src="/favicon.svg" alt="SecureDocs" className="h-6 w-6 rounded shadow-xs" />
            <span className="text-xs font-mono font-medium text-accent uppercase tracking-wider">
              Permission-Aware RAG
            </span>
          </div>

          <div>
            <h1 className="text-4xl sm:text-5xl font-serif font-medium tracking-tight text-ink leading-tight">
              SecureDocs
            </h1>
            <p className="mt-2 text-lg font-serif text-muted italic">
              Multi-tenant, role-based document intelligence.
            </p>
          </div>

          <p className="text-sm text-ink/80 leading-relaxed max-w-md">
            Ask questions across private internal policies, compensation sheets, and roadmaps. 
            Access control is enforced inside the SQL query—chunks your role cannot see are filtered out before reaching the LLM, guaranteeing zero leaks.
          </p>

          <div className="space-y-3 pt-2">
            <div className="flex items-start gap-3">
              <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-accent-soft text-accent text-xs font-bold">
                ✓
              </span>
              <p className="text-xs text-muted leading-normal">
                <strong className="text-ink font-medium">SQL-Level Enforcement:</strong> Unauthorized passages never reach the model context or prompt.
              </p>
            </div>

            <div className="flex items-start gap-3">
              <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-accent-soft text-accent text-xs font-bold">
                ✓
              </span>
              <p className="text-xs text-muted leading-normal">
                <strong className="text-ink font-medium">Hybrid Search & RRF:</strong> Combines semantic vector embeddings with PostgreSQL full-text search.
              </p>
            </div>

            <div className="flex items-start gap-3">
              <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-accent-soft text-accent text-xs font-bold">
                ✓
              </span>
              <p className="text-xs text-muted leading-normal">
                <strong className="text-ink font-medium">Multi-Tenant Isolation:</strong> Strict company boundary protection with instant role updates.
              </p>
            </div>
          </div>
        </section>

        {/* Right Side: Login Form & Demo Accounts */}
        <div className="md:col-span-6 lg:col-span-6 space-y-4">
          <section className="rounded-xl border border-rule bg-panel p-6 sm:p-7 shadow-xs">
            <h2 className="text-xl font-serif font-medium text-ink">
              {isLogin ? 'Sign in to your account' : 'Register your company'}
            </h2>
            <p className="mt-1 text-xs text-muted">
              {isLogin ? 'Enter your company email and password' : 'Create an admin account for your organization'}
            </p>

            <form onSubmit={submit} className="mt-5 space-y-4 border-t border-rule/70 pt-4">
              {!isLogin && (
                <Field label="Company name" value={company} onChange={(e) => setCompany(e.target.value)} required maxLength={100} placeholder="e.g. Acme Corp" />
              )}
              <Field label="Work email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="you@company.example" />
              <Field
                label="Password"
                type="password"
                autoComplete={isLogin ? 'current-password' : 'new-password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={isLogin ? undefined : 8}
                maxLength={72}
                hint={isLogin ? undefined : '8 to 72 characters. You become the admin of the new company.'}
              />
              <ErrorNote>{error}</ErrorNote>
              <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
                <Button type="submit" disabled={busy}>{busy ? 'Please wait...' : isLogin ? 'Sign in' : 'Create company'}</Button>
                <button
                  type="button"
                  className="text-xs text-accent hover:text-accent-dark underline underline-offset-2 transition-colors cursor-pointer"
                  onClick={() => {
                    setMode(isLogin ? 'register' : 'login')
                    setError('')
                  }}
                >
                  {isLogin ? 'Register a new company' : 'Existing account? Sign in'}
                </button>
              </div>
            </form>
          </section>

          {import.meta.env.VITE_DEMO === 'true' && (
            <aside className="rounded-xl border border-rule bg-panel p-4 shadow-xs">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xs font-mono font-medium uppercase tracking-wider text-muted">
                  Quick Demo Accounts
                </h3>
                <span className="text-[0.65rem] font-mono text-muted">Password: <code className="text-ink font-semibold">{DEMO_PASSWORD}</code></span>
              </div>
              <div className="grid grid-cols-2 gap-2">
                {DEMO_ACCOUNTS.map((a) => {
                  const role = a.label.split(' ')[1]
                  return (
                    <button
                      key={a.email}
                      type="button"
                      disabled={busy}
                      onClick={() => run(() => login(a.email, DEMO_PASSWORD))}
                      className="group rounded border border-rule bg-paper/60 p-2 text-left transition-all hover:border-accent hover:bg-accent-soft/30 cursor-pointer disabled:opacity-50"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-xs text-ink group-hover:text-accent transition-colors truncate">{a.label}</span>
                        <span className={`text-[0.6rem] font-mono uppercase px-1 py-0.2 rounded font-semibold ${
                          role === 'admin' ? 'bg-[#1F5C5A]/10 text-[#1F5C5A]' :
                          role === 'manager' ? 'bg-[#A8741A]/10 text-[#A8741A]' : 'bg-[#5B6B7A]/10 text-[#5B6B7A]'
                        }`}>
                          {role}
                        </span>
                      </div>
                      <span className="block font-mono text-[0.65rem] text-muted truncate mt-0.5">{a.email}</span>
                    </button>
                  )
                })}
              </div>
            </aside>
          )}
        </div>
      </div>
    </div>
  )
}
