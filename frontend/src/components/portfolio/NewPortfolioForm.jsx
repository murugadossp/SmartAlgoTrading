import { useState } from 'react'
import { portfolioRun, listAlgos } from '../../api/client'
import RunResultsTable from './RunResultsTable'

export default function NewPortfolioForm() {
  const [amount, setAmount] = useState('')
  const [algoIds, setAlgoIds] = useState([])
  const [algos, setAlgos] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const loadAlgos = async () => {
    if (algos.length > 0) return
    try {
      const { algos: list } = await listAlgos('stocks')
      setAlgos(list || [])
    } catch (e) {
      setError(e.message)
    }
  }

  const handleRun = async (e) => {
    e.preventDefault()
    setError(null)
    setResult(null)
    const num = parseFloat(amount?.replace(/,/g, ''))
    if (!num || num <= 0) {
      setError('Enter a valid portfolio amount (e.g. 100000 or 1L)')
      return
    }
    setLoading(true)
    try {
      const data = await portfolioRun({
        amount: num,
        algo_ids: algoIds.length > 0 ? algoIds : undefined,
      })
      setResult(data)
    } catch (err) {
      setError(err.message || 'Run failed')
    } finally {
      setLoading(false)
    }
  }

  const toggleAlgo = (id) => {
    setAlgoIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]))
  }

  return (
    <div className="new-portfolio-form">
      <form onSubmit={handleRun}>
        <div className="form-group">
          <label htmlFor="amount">Portfolio amount (₹)</label>
          <input
            id="amount"
            type="text"
            placeholder="e.g. 100000 or 1L"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            onFocus={loadAlgos}
          />
        </div>
        <div className="form-group">
          <label>Algos to run (leave empty for all stock algos)</label>
          <div className="algo-checkboxes">
            {algos.length === 0 && (
              <button type="button" className="link-style" onClick={loadAlgos}>
                Load algos
              </button>
            )}
            {algos.map((a) => (
              <label key={a.id} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={algoIds.includes(a.id)}
                  onChange={() => toggleAlgo(a.id)}
                />
                {a.name}
              </label>
            ))}
          </div>
        </div>
        {error && <p className="form-error">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Running…' : 'Run algos'}
        </button>
      </form>
      {result?.results && <RunResultsTable results={result.results} />}
    </div>
  )
}
