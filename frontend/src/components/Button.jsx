const styles = {
  primary: 'border-accent bg-accent text-panel hover:bg-accent-dark',
  secondary: 'border-rule bg-panel text-ink hover:border-muted',
  danger: 'border-danger bg-danger text-panel hover:opacity-90',
}

export default function Button({ variant = 'primary', className = '', type = 'button', ...props }) {
  return (
    <button
      type={type}
      className={`rounded border px-3 py-1.5 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-50 ${styles[variant]} ${className}`}
      {...props}
    />
  )
}
