import { useState, useEffect, useRef } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getAlgoDetail, refreshAlgo } from '../../api/client'
import ErrorBoundary from '../ErrorBoundary'
import StrategyChart from './StrategyChart'
import KeyTerms from './KeyTerms'

function OverviewCard({ title, children, icon }) {
  return (
    <section className="strategy-card">
      <h3 className="strategy-card-title">
        {icon && <span className="strategy-card-icon" aria-hidden>{icon}</span>}
        {title}
      </h3>
      <div className="strategy-card-body">{children}</div>
    </section>
  )
}

// Format card content: first line as lead, then bullets (max 5 for readability)
function formatBlock(text) {
  if (!text || typeof text !== 'string') return null
  const lines = text.trim().split('\n').map((l) => l.trim()).filter(Boolean)
  if (lines.length === 0) return null
  const elements = []
  let listItems = []
  const maxBullets = 5
  lines.forEach((line, i) => {
    if (line.startsWith('•')) {
      if (listItems.length < maxBullets) {
        listItems.push(<li key={`li-${i}`}>{line.slice(1).trim()}</li>)
      }
    } else {
      if (listItems.length > 0) {
        elements.push(<ul key={`ul-${i}`} className="strategy-list">{listItems}</ul>)
        listItems = []
      }
      elements.push(<p key={i} className="strategy-lead">{line}</p>)
    }
  })
  if (listItems.length > 0) elements.push(<ul key="ul-end" className="strategy-list">{listItems}</ul>)
  return <div className="strategy-block-content">{elements}</div>
}

export default function AlgoDetail() {
  const { algoId } = useParams()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [refreshLoading, setRefreshLoading] = useState(false)
  const [error, setError] = useState(null)
  const mountedRef = useRef(true)

  useEffect(() => {
    mountedRef.current = true
    return () => { mountedRef.current = false }
  }, [])

  useEffect(() => {
    if (!algoId) return
    setLoading(true)
    setError(null)
    setData(null)
    getAlgoDetail(algoId)
      .then((res) => {
        if (mountedRef.current) setData(res)
      })
      .catch((e) => {
        if (mountedRef.current) setError(e.message)
      })
      .finally(() => {
        if (mountedRef.current) setLoading(false)
      })
  }, [algoId])

  const handleRefresh = () => {
    if (!algoId) return
    setRefreshLoading(true)
    setError(null)
    refreshAlgo(algoId)
      .then((res) => {
        if (mountedRef.current && data) {
          setData((prev) => (prev ? { ...prev, stocks: res.stocks || [] } : prev))
        }
      })
      .catch((e) => {
        if (mountedRef.current) setError(e.message)
      })
      .finally(() => {
        if (mountedRef.current) setRefreshLoading(false)
      })
  }

  if (loading && !data) {
    return (
      <div className="algo-detail algo-detail-loading">
        <Link to="/algos" className="back-link">← Explore Algos</Link>
        <div className="algo-detail-loading-state">
          <div className="loading-spinner" aria-hidden />
          <p>Loading strategy…</p>
        </div>
      </div>
    )
  }

  if (error && !data) {
    return (
      <div className="algo-detail">
        <Link to="/algos" className="back-link">← Explore Algos</Link>
        <div className="algo-detail-error">
          <p className="form-error">{error}</p>
          <Link to="/algos" className="back-link">Back to Explore Algos</Link>
        </div>
      </div>
    )
  }

  if (!data) return null

  const { name, segment, overview = {}, chart_type, stocks = [] } = data
  const { summary, goal, inputs, signals, risk } = overview

  return (
    <div className="algo-detail">
      <Link to="/algos" className="back-link">← Explore Algos</Link>

      <header className="algo-detail-hero">
        <div className="algo-detail-hero-text">
          <div className="algo-detail-title-row">
            <h1>{name || algoId}</h1>
            {segment && <span className="algo-detail-segment">{segment}</span>}
          </div>
          {summary && <p className="algo-detail-summary">{summary}</p>}
        </div>
        <button
          type="button"
          className="algo-refresh-btn"
          onClick={handleRefresh}
          disabled={refreshLoading}
        >
          {refreshLoading ? 'Refreshing…' : 'Refresh stocks'}
        </button>
      </header>

      {/* Goal: top-level single card */}
      <section className="algo-goal-card">
        <h2 className="algo-goal-card-title">
          <span className="algo-goal-icon" aria-hidden>🎯</span>
          Goal
        </h2>
        <div className="algo-goal-card-body">
          {formatBlock(goal) || <p className="strategy-muted">No detail.</p>}
        </div>
      </section>

      {/* Stocks: directly visible after Goal */}
      <section className="algo-stocks-section">
        <h2>Stocks</h2>
        {error && <p className="form-error">{error}</p>}
        {stocks.length === 0 ? (
          <p className="algo-stocks-empty">No stocks from last run. Click &quot;Refresh stocks&quot; to run the algo.</p>
        ) : (
          <div className="algo-stocks-table-wrap">
            <table className="algo-stocks-table">
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Suggestion</th>
                  <th>Confidence</th>
                  <th>Last price</th>
                </tr>
              </thead>
              <tbody>
                {stocks.map((row, i) => (
                  <tr key={i}>
                    <td>{row.symbol}</td>
                    <td className={`suggestion-${(row.suggestion || '').toLowerCase().replace(/\s+/g, '-')}`}>{row.suggestion ?? '—'}</td>
                    <td>{row.confidence != null ? `${row.confidence}` : '—'}</td>
                    <td>{row.last_price != null ? `₹${Number(row.last_price).toLocaleString('en-IN')}` : '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Collapsible: How it works */}
      {chart_type && (
        <section className="algo-collapsible-section">
          <details className="collapsible-details">
            <summary className="collapsible-summary">How it works (diagram)</summary>
            <div className="algo-chart-section-inner">
              <ErrorBoundary fallback={() => (
                <div className="strategy-chart-error"><p>Diagram could not be displayed.</p></div>
              )}>
                <StrategyChart chartType={chart_type} />
              </ErrorBoundary>
            </div>
          </details>
        </section>
      )}

      {/* Collapsible: Inputs / Signals / Risk */}
      <section className="algo-collapsible-section">
        <details className="collapsible-details">
          <summary className="collapsible-summary">Inputs, signals and risk (detail)</summary>
          <div className="algo-detail-grid algo-detail-grid-below">
            <OverviewCard title="Inputs" icon="📥">
              {formatBlock(inputs) || <p className="strategy-muted">OHLC, volume from broker/market data.</p>}
            </OverviewCard>
            <OverviewCard title="Signals" icon="📈">
              {formatBlock(signals) || <p className="strategy-muted">Strategy-specific signals.</p>}
            </OverviewCard>
            <OverviewCard title="Risk" icon="⚠️">
              {formatBlock(risk) || <p className="strategy-muted">Position sizing and confidence threshold.</p>}
            </OverviewCard>
          </div>
        </details>
      </section>

      <KeyTerms algoId={algoId} chartType={chart_type} />
    </div>
  )
}
