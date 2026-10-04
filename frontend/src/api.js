const BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')
const TOKEN_KEY = 'securedocs_token'

export const getToken = () => localStorage.getItem(TOKEN_KEY)
export const setToken = (t) => localStorage.setItem(TOKEN_KEY, t)
export const clearToken = () => localStorage.removeItem(TOKEN_KEY)

let onUnauthorized = () => {}
export const setUnauthorizedHandler = (fn) => {
  onUnauthorized = fn
}

export class ApiError extends Error {
  constructor(status, message) {
    super(message)
    this.status = status
  }
}

const FALLBACK = {
  413: 'That file is too large.',
  415: 'That file type is not supported. Use PDF, TXT or MD.',
  429: 'Too many requests. Please wait a minute and try again.',
  403: 'You do not have permission to do that.',
}

// FastAPI sends { detail: "text" } or, for 422, { detail: [{ loc, msg }, ...] }
function parseDetail(body, status) {
  const d = body && body.detail
  if (typeof d === 'string') return d
  if (Array.isArray(d)) {
    return d
      .map((item) => {
        const field = Array.isArray(item.loc) ? item.loc[item.loc.length - 1] : ''
        return field && field !== 'body' ? `${field}: ${item.msg}` : item.msg
      })
      .join('. ')
  }
  return FALLBACK[status] || `Request failed (${status}).`
}

export async function api(path, { method = 'GET', json, form, noAuthRedirect = false } = {}) {
  const headers = {}
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`
  let body
  if (json !== undefined) {
    headers['Content-Type'] = 'application/json'
    body = JSON.stringify(json)
  } else if (form) {
    body = form // browser sets the multipart boundary
  }

  let res
  try {
    res = await fetch(`${BASE}${path}`, { method, headers, body })
  } catch {
    throw new ApiError(0, 'Cannot reach the server. Check your connection and try again.')
  }

  if (res.status === 204) return null
  let data = null
  try {
    data = await res.json()
  } catch {
    /* empty or non-JSON body */
  }

  if (!res.ok) {
    if (res.status === 401 && !noAuthRedirect) {
      clearToken()
      onUnauthorized()
    }
    throw new ApiError(res.status, parseDetail(data, res.status))
  }
  return data
}
