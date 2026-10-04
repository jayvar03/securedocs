const dot = {
  admin: 'bg-role-admin',
  manager: 'bg-role-manager',
  employee: 'bg-role-employee',
}

export default function RoleLabel({ role }) {
  return (
    <span className="inline-flex items-center gap-1.5 font-mono text-xs">
      <span aria-hidden="true" className={`h-2 w-2 rounded-full ${dot[role] || 'bg-muted'}`} />
      {role}
    </span>
  )
}
