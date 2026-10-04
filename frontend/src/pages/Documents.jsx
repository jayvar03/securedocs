import { useCallback, useEffect, useState } from 'react'
import { api } from '../api.js'
import { useAuth } from '../auth.jsx'
import Button from '../components/Button.jsx'
import ConfirmDialog from '../components/ConfirmDialog.jsx'
import ErrorNote from '../components/ErrorNote.jsx'
import Field from '../components/Field.jsx'
import RoleLabel from '../components/RoleLabel.jsx'
import Spinner from '../components/Spinner.jsx'

const CHOOSABLE = ['manager', 'employee']

function RoleBoxes({ value, onChange, idPrefix }) {
  return (
    <fieldset className="flex flex-wrap gap-x-4 gap-y-1">
      <legend className="sr-only">Roles that can see this document</legend>
      <label className="flex items-center gap-1.5 text-sm text-muted">
        <input type="checkbox" checked disabled /> admin (always)
      </label>
      {CHOOSABLE.map((r) => (
        <label key={r} className="flex items-center gap-1.5 text-sm" htmlFor={`${idPrefix}-${r}`}>
          <input
            id={`${idPrefix}-${r}`}
            type="checkbox"
            checked={value.includes(r)}
            onChange={(e) => onChange(e.target.checked ? [...value, r] : value.filter((x) => x !== r))}
          />
          {r}
        </label>
      ))}
    </fieldset>
  )
}

function UploadForm({ onUploaded }) {
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState('')
  const [roles, setRoles] = useState(['manager', 'employee'])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [inputKey, setInputKey] = useState(0)

  async function submit(e) {
    e.preventDefault()
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    if (title.trim()) form.append('title', title.trim())
    roles.forEach((r) => form.append('allowed_roles', r)) // repeated form field
    setBusy(true)
    setError('')
    try {
      await api('/api/documents', { method: 'POST', form })
      setFile(null)
      setTitle('')
      setInputKey((k) => k + 1)
      onUploaded()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form onSubmit={submit} className="mb-8 space-y-4 rounded border border-rule bg-panel p-4">
      <h2 className="text-lg">Upload a document</h2>
      <div className="grid gap-4 sm:grid-cols-2">
        <Field
          key={inputKey}
          label="File"
          type="file"
          accept=".pdf,.txt,.md"
          onChange={(e) => setFile(e.target.files[0] || null)}
          hint="PDF, TXT or MD, up to 10 MB. Scanned PDFs are not supported."
          required
        />
        <Field label="Title (optional)" value={title} onChange={(e) => setTitle(e.target.value)} maxLength={200} hint="Defaults to the file name." />
      </div>
      <div>
        <p className="mb-1 text-sm font-medium">Who can see it</p>
        <RoleBoxes value={roles} onChange={setRoles} idPrefix="upload" />
      </div>
      <ErrorNote>{error}</ErrorNote>
      <Button type="submit" disabled={busy || !file}>{busy ? 'Uploading and indexing' : 'Upload'}</Button>
    </form>
  )
}

function Row({ doc, isAdmin, onChanged, onAskDelete }) {
  const [editing, setEditing] = useState(false)
  const [roles, setRoles] = useState([])
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  function startEdit() {
    setRoles(doc.allowed_roles.filter((r) => r !== 'admin'))
    setError('')
    setEditing(true)
  }

  async function save() {
    setBusy(true)
    setError('')
    try {
      await api(`/api/documents/${doc.id}/access`, { method: 'PATCH', json: { allowed_roles: ['admin', ...roles] } })
      setEditing(false)
      onChanged()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <tr>
      <td className="font-medium">{doc.title}</td>
      <td className="font-mono text-xs">{doc.filename}</td>
      <td>
        {editing ? (
          <div className="space-y-2">
            <RoleBoxes value={roles} onChange={setRoles} idPrefix={`doc-${doc.id}`} />
            <ErrorNote>{error}</ErrorNote>
            <div className="flex gap-2">
              <Button onClick={save} disabled={busy}>{busy ? 'Saving' : 'Save access'}</Button>
              <Button variant="secondary" onClick={() => setEditing(false)}>Cancel</Button>
            </div>
          </div>
        ) : (
          <div className="flex flex-wrap gap-x-3 gap-y-1">
            {doc.allowed_roles.map((r) => <RoleLabel key={r} role={r} />)}
          </div>
        )}
      </td>
      <td className="whitespace-nowrap font-mono text-xs">{new Date(doc.created_at).toLocaleDateString()}</td>
      {isAdmin && (
        <td className="whitespace-nowrap">
          {!editing && (
            <div className="flex gap-2">
              <Button variant="secondary" onClick={startEdit}>Edit access</Button>
              <Button variant="secondary" onClick={() => onAskDelete(doc)}>Delete</Button>
            </div>
          )}
        </td>
      )}
    </tr>
  )
}

export default function Documents() {
  const { user } = useAuth()
  const isAdmin = user.role === 'admin'
  const canUpload = isAdmin || user.role === 'manager'
  const [docs, setDocs] = useState(null)
  const [error, setError] = useState('')
  const [toDelete, setToDelete] = useState(null)
  const [deleting, setDeleting] = useState(false)

  const load = useCallback(() => {
    api('/api/documents')
      .then((d) => {
        setDocs(d)
        setError('')
      })
      .catch((e) => setError(e.message))
  }, [])
  useEffect(load, [load])

  async function confirmDelete() {
    setDeleting(true)
    try {
      await api(`/api/documents/${toDelete.id}`, { method: 'DELETE' })
      setToDelete(null)
      load()
    } catch (e) {
      setError(e.message)
      setToDelete(null)
    } finally {
      setDeleting(false)
    }
  }

  return (
    <div>
      <h1 className="text-2xl">Documents</h1>
      <p className="mb-4 mt-1 text-sm text-muted">
        {isAdmin ? 'Every document in your company.' : 'Documents your role can see.'}
      </p>

      {canUpload && <UploadForm onUploaded={load} />}
      <ErrorNote>{error}</ErrorNote>

      {docs === null && !error && <Spinner label="Loading documents" />}
      {docs && docs.length === 0 && (
        <p className="rounded border border-rule bg-panel p-4 text-sm">
          No documents yet. {canUpload ? 'Upload one above to get started.' : 'Ask a manager or admin to upload some.'}
        </p>
      )}
      {docs && docs.length > 0 && (
        <div className="overflow-x-auto rounded border border-rule bg-panel">
          <table className="table-base">
            <thead>
              <tr>
                <th>Title</th><th>File</th><th>Who can see it</th><th>Added</th>
                {isAdmin && <th><span className="sr-only">Actions</span></th>}
              </tr>
            </thead>
            <tbody>
              {docs.map((d) => (
                <Row key={d.id} doc={d} isAdmin={isAdmin} onChanged={load} onAskDelete={setToDelete} />
              ))}
            </tbody>
          </table>
        </div>
      )}

      <ConfirmDialog
        open={Boolean(toDelete)}
        title="Delete this document?"
        message={toDelete ? `“${toDelete.title}” and all of its searchable text will be removed. This cannot be undone.` : ''}
        confirmLabel="Delete document"
        busy={deleting}
        onConfirm={confirmDelete}
        onCancel={() => setToDelete(null)}
      />
    </div>
  )
}
