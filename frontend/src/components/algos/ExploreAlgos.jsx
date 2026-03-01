import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { listAlgos } from '../../api/client'
import Card from '../Card'

export default function ExploreAlgos() {
  const [algos, setAlgos] = useState([])
  const [segment, setSegment] = useState('stocks')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    listAlgos(segment)
      .then((data) => setAlgos(data.algos || []))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [segment])

  return (
    <div className="explore-algos-content">
      <h1>Explore Algos</h1>
      <p className="section-desc">Filter by segment and click an algo for strategy overview and watchlist.</p>
      <div className="segment-filter">
        <button
          type="button"
          className={segment === 'stocks' ? 'active' : ''}
          onClick={() => setSegment('stocks')}
        >
          Stocks
        </button>
        <button
          type="button"
          className={segment === 'fno' ? 'active' : ''}
          onClick={() => setSegment('fno')}
        >
          F&O
        </button>
      </div>
      {error && <p className="form-error">{error}</p>}
      {loading && <p>Loading algos…</p>}
      {!loading && !error && (
        <div className="algo-cards">
          {algos.map((a) => (
            <Link key={a.id} to={`/algos/${a.id}`} className="algo-card-link">
              <Card title={a.name}>
                <p className="algo-segment">{a.segment}</p>
                <p className="algo-desc">{a.short_description}</p>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
