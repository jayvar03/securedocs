import { useId } from 'react'

const inputClass =
  'w-full rounded border border-rule bg-panel px-2.5 py-1.5 text-sm placeholder:text-muted/70'

export default function Field({ label, hint, as = 'input', children, ...props }) {
  const id = useId()
  const Tag = as
  return (
    <div>
      <label htmlFor={id} className="mb-1 block text-sm font-medium">
        {label}
      </label>
      <Tag id={id} className={inputClass} aria-describedby={hint ? `${id}-hint` : undefined} {...props}>
        {children}
      </Tag>
      {hint && (
        <p id={`${id}-hint`} className="mt-1 text-xs text-muted">
          {hint}
        </p>
      )}
    </div>
  )
}
