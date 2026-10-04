import { useCallback, useEffect, useState } from 'react'
import { api } from '../api.js'
import Button from '../components/Button.jsx'
import ErrorNote from '../components/ErrorNote.jsx'
import Field from '../components/Field.jsx'
import RoleLabel from '../components/RoleLabel.jsx'
import Spinner from '../components/Spinner.jsx'

export default function Users() {
  const [users, setUsers] = useState(null)
  const [error, setError] = useState('')
  const [form, setForm] = useState({ email: '', password: '', role: 'employee', department: '' })
  const [formError, setFormError] = useState('')
  const [busy, setBusy] = useState(false)

  const load = useCallback(() => {
    api('/api/users').then(setUsers).catch((e) => setError(e.message))
  }, [])
  useEffect(load, [load])

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value })

  async function submit(e) {
    e.preventDefault()
    setBusy(true)
    setFormError('')
    const body = { email: form.email, password: form.password, role: form.role }
    if (form.department.trim()) body.department = form.department.trim()
    try {
      await api('/api/users', { method: 'POST', json: body })
      setForm({ email: '', password: '', role: 'employee', department: '' })
      load()
    } catch (err) {
      setFormError(err.status === 409 ? 'A user with this email already exists.' : err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <h1 className="text-2xl">Users</h1>
      <p className="mb-4 mt-1 text-sm text-muted">People in your company. New users join your company automatically.</p>

      <form onSubmit={submit} className="mb-8 space-y-4 rounded border border-rule bg-panel p-4">
        <h2 className="text-lg">Add a user</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Email" type="email" value={form.email} onChange={set('email')} required />
          <Field label="Temporary password" type="password" autoComplete="new-password" value={form.password} onChange={set('password')} required minLength={8} maxLength={72} hint="8 to 72 characters." />
          <Field label="Role" as="select" value={form.role} onChange={set('role')}>
            <option value="employee">employee</option>
            <option value="manager">manager</option>
            <option value="admin">admin</option>
          </Field>
          <Field label="Department (optional)" value={form.department} onChange={set('department')} maxLength={100} />
        </div>
        <ErrorNote>{formError}</ErrorNote>
        <Button type="submit" disabled={busy}>{busy ? 'Adding' : 'Add user'}</Button>
      </form>

      <ErrorNote>{error}</ErrorNote>
      {users === null && !error && <Spinner label="Loading users" />}
      {users && (
        <div className="overflow-x-auto rounded border border-rule bg-panel">
          <table className="table-base">
            <thead><tr><th>Email</th><th>Role</th><th>Department</th><th>ID</th></tr></thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td className="font-mono text-xs">{u.email}</td>
                  <td><RoleLabel role={u.role} /></td>
                  <td>{u.department || <span className="text-muted">None</span>}</td>
                  <td className="font-mono text-xs text-muted">{u.id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
