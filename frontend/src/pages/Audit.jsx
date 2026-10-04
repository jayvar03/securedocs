import { useEffect, useState } from 'react'
import { api } from '../api.js'
import ErrorNote from '../components/ErrorNote.jsx'
import Spinner from '../components/Spinner.jsx'

export default function Audit() {
  const [rows, setRows] = useState(null)
  const [error, setError] = useState('')
  useEffect(() => {
    api('/api/audit-logs').then(setRows).catch((e) => setError(e.message))
  }, [])

  return (
    <div>
      <h1 className="text-2xl">Audit log</h1>
      <p className="mb-4 mt-1 text-sm text-muted">The 200 most recent questions asked in your company, with the chunks used to answer them.</p>
      <ErrorNote>{error}</ErrorNote>
      {rows === null && !error && <Spinner label="Loading audit log" />}
      {rows && rows.length === 0 && <p className="rounded border border-rule bg-panel p-4 text-sm">No questions have been asked yet.</p>}
      {rows && rows.length > 0 && (
        <div className="overflow-x-auto rounded border border-rule bg-panel">
          <table className="table-base">
            <thead><tr><th>When</th><th>User</th><th>Question</th><th>Chunk ids</th></tr></thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  <td className="whitespace-nowrap font-mono text-xs">{new Date(r.created_at).toLocaleString()}</td>
                  <td className="font-mono text-xs">{r.user_email || 'deleted user'}</td>
                  <td>{r.question}</td>
                  <td className="font-mono text-xs">{r.chunk_ids.length ? r.chunk_ids.join(', ') : <span className="text-muted">none</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
