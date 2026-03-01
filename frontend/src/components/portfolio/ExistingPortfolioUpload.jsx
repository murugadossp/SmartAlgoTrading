import { useState } from 'react'
import { portfolioUpload, portfolioRebalance } from '../../api/client'
import AnalysisFeedback from './AnalysisFeedback'
import RebalanceView from './RebalanceView'

export default function ExistingPortfolioUpload() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [rebalanceLoading, setRebalanceLoading] = useState(false)
  const [rebalanceError, setRebalanceError] = useState(null)
  const [rebalanceResult, setRebalanceResult] = useState(null)
  const [strategy, setStrategy] = useState('full')
  const [bandPct, setBandPct] = useState(5)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a CSV or Excel file.')
      return
    }
    setError(null)
    setResult(null)
    setRebalanceResult(null)
    setLoading(true)
    try {
      const data = await portfolioUpload(file)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRebalance = async (e) => {
    e.preventDefault()
    if (!result?.holdings?.length) return
    setRebalanceError(null)
    setRebalanceResult(null)
    setRebalanceLoading(true)
    try {
      const body = {
        holdings: result.holdings.map((h) => ({
          symbol: h.symbol,
          quantity: h.quantity,
          value: h.value ?? undefined,
        })),
        strategy,
        band_pct: bandPct / 100,
      }
      const data = await portfolioRebalance(body)
      setRebalanceResult(data)
    } catch (err) {
      setRebalanceError(err.message || 'Rebalance failed')
    } finally {
      setRebalanceLoading(false)
    }
  }

  return (
    <div className="existing-portfolio-upload">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="portfolio-file">Portfolio file (CSV or Excel)</label>
          <input
            id="portfolio-file"
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={(e) => {
              setFile(e.target.files?.[0] || null)
              setError(null)
            }}
          />
          <p className="form-hint">Columns: symbol, quantity; optionally avg_cost or value.</p>
        </div>
        {error && <p className="form-error">{error}</p>}
        <button type="submit" disabled={loading || !file}>
          {loading ? 'Analyzing…' : 'Upload and analyze'}
        </button>
      </form>
      {result && <AnalysisFeedback data={result} />}
      {result?.holdings?.length > 0 && (
        <div className="rebalance-section">
          <h3>Rebalance</h3>
          <p className="section-desc">Get suggested trades to bring portfolio to equal weight (or use bands to only trade when drift &gt; band).</p>
          <form onSubmit={handleRebalance} className="rebalance-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="strategy">Strategy</label>
                <select
                  id="strategy"
                  value={strategy}
                  onChange={(e) => setStrategy(e.target.value)}
                >
                  <option value="full">Full rebalance</option>
                  <option value="bands">Bands only</option>
                </select>
              </div>
              {strategy === 'bands' && (
                <div className="form-group">
                  <label htmlFor="band-pct">Band %</label>
                  <input
                    id="band-pct"
                    type="number"
                    min="1"
                    max="50"
                    value={bandPct}
                    onChange={(e) => setBandPct(Number(e.target.value) || 5)}
                  />
                </div>
              )}
            </div>
            {rebalanceError && <p className="form-error">{rebalanceError}</p>}
            <button type="submit" disabled={rebalanceLoading}>
              {rebalanceLoading ? 'Calculating…' : 'Get rebalance'}
            </button>
          </form>
          {rebalanceResult && <RebalanceView data={rebalanceResult} />}
        </div>
      )}
    </div>
  )
}
