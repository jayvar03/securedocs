"""Role constants and helpers. No heavy imports so tests can use it freely."""

ROLES = ("admin", "manager", "employee")


def normalize_roles(raw: list[str]) -> list[str]:
    """Accept repeated values and/or comma lists, validate, always include admin.

    An empty list therefore means "admin only".
    """
    items: list[str] = []
    for value in raw:
        items.extend(part.strip().lower() for part in value.split(",") if part.strip())
    bad = sorted({r for r in items if r not in ROLES})
    if bad:
        raise ValueError(f"Unknown role(s): {', '.join(bad)}. Allowed roles are: {', '.join(ROLES)}.")
    wanted = set(items) | {"admin"}
    return [r for r in ROLES if r in wanted]
