import { useEffect, useRef } from 'react'
import Button from './Button.jsx'

export default function ConfirmDialog({ open, title, message, confirmLabel = 'Confirm', busy, onConfirm, onCancel }) {
  const ref = useRef(null)
  useEffect(() => {
    const d = ref.current
    if (!d) return
    if (open && !d.open) d.showModal()
    if (!open && d.open) d.close()
  }, [open])

  return (
    <dialog
      ref={ref}
      onCancel={(e) => {
        e.preventDefault()
        onCancel()
      }}
      className="w-[min(28rem,92vw)] rounded border border-rule bg-panel p-5 text-ink"
    >
      <h2 className="text-lg">{title}</h2>
      <p className="mt-2 text-sm text-muted">{message}</p>
      <div className="mt-5 flex justify-end gap-2">
        <Button variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button variant="danger" onClick={onConfirm} disabled={busy}>{busy ? 'Working' : confirmLabel}</Button>
      </div>
    </dialog>
  )
}
