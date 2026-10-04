export default function Spinner({ label = 'Loading' }) {
  return (
    <span role="status" className="inline-flex items-center gap-2 text-sm text-muted">
      <span
        aria-hidden="true"
        className="h-4 w-4 animate-spin rounded-full border-2 border-rule border-t-accent motion-reduce:animate-none"
      />
      {label}
    </span>
  )
}
