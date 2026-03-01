/**
 * Backend API base URL. Use VITE_API_URL in .env or /api (Vite proxy to backend).
 */
const API_BASE = import.meta.env.VITE_API_URL || '/api'

export async function portfolioRun(body) {
  const res = await fetch(`${API_BASE}/portfolio/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || err.message || 'Portfolio run failed')
  }
  return res.json()
}

export async function portfolioLastRun() {
  const res = await fetch(`${API_BASE}/portfolio/last-run`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error('Failed to fetch last run')
  return res.json()
}

export async function portfolioUpload(file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/portfolio/upload`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    let msg = err.detail?.message || err.detail || err.errors || 'Upload failed'
    if (typeof msg === 'object' && msg.errors) msg = msg.errors.join('; ')
    if (Array.isArray(msg)) msg = msg.join('; ')
    throw new Error(msg)
  }
  return res.json()
}

export async function portfolioRebalance(body) {
  const res = await fetch(`${API_BASE}/portfolio/rebalance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || err.message || 'Rebalance failed')
  }
  return res.json()
}

export async function listAlgos(segment = null) {
  const url = segment ? `${API_BASE}/algos?segment=${encodeURIComponent(segment)}` : `${API_BASE}/algos`
  const res = await fetch(url)
  if (!res.ok) throw new Error('Failed to fetch algos')
  return res.json()
}

export async function getAlgoDetail(algoId) {
  const res = await fetch(`${API_BASE}/algos/${encodeURIComponent(algoId)}`)
  if (!res.ok) throw new Error('Failed to fetch algo detail')
  return res.json()
}

export async function refreshAlgo(algoId) {
  const res = await fetch(`${API_BASE}/algos/${encodeURIComponent(algoId)}/refresh`, { method: 'POST' })
  if (!res.ok) throw new Error('Failed to refresh algo')
  return res.json()
}
