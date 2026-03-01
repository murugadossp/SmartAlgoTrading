export default function RunResultsTable({ results = [] }) {
  if (!results.length) return null
  return (
    <div className="run-results-table">
      <h3>Results</h3>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Suggestion</th>
            <th>Confidence</th>
            <th>Last price</th>
            <th>Suggested qty</th>
            <th>Suggested amount (₹)</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, i) => (
            <tr key={r.symbol + String(i)}>
              <td>{r.symbol}</td>
              <td className={`suggestion-${(r.suggestion || '').toLowerCase().replace(/\s+/g, '-')}`}>{r.suggestion}</td>
              <td>{r.confidence != null ? r.confidence : '—'}</td>
              <td>{r.last_price != null ? r.last_price : '—'}</td>
              <td>{r.suggested_quantity != null ? r.suggested_quantity : '—'}</td>
              <td>{r.suggested_amount != null ? r.suggested_amount : '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
