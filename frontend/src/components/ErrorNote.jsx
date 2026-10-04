export default function ErrorNote({ children }) {
  if (!children) return null
  return (
    <p role="alert" className="rounded border border-danger/40 bg-danger-soft px-3 py-2 text-sm text-danger">
      {children}
    </p>
  )
}
