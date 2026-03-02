import DOMPurify from 'dompurify'

export default function AnalysisFeedback({ data }) {
  if (!data) return null
  const { total_value, holding_count, feedback, sector_mix, concentration, holdings } = data
  const { summary, suggestions, analysis_html: rawHtml } = feedback || {}
  const analysis_html = rawHtml ? DOMPurify.sanitize(rawHtml, { ALLOWED_TAGS: ['section', 'div', 'h2', 'h3', 'h4', 'p', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'ul', 'ol', 'li', 'span', 'strong', 'em', 'br'], ALLOWED_ATTR: ['class', 'style'] }) : null

  return (
    <div className="analysis-feedback">
      <h3>Analysis</h3>
      <div className="feedback-metrics">
        <div className="metric-card">
          <span className="metric-label">Total value</span>
          <span className="metric-value">₹{total_value != null ? Number(total_value).toLocaleString('en-IN') : '—'}</span>
        </div>
        <div className="metric-card">
          <span className="metric-label">Holdings</span>
          <span className="metric-value">{holding_count ?? '—'}</span>
        </div>
      </div>
      {summary && (
        <div className="feedback-summary">
          <h4>Summary</h4>
          <p>{summary}</p>
        </div>
      )}
      {suggestions && suggestions.length > 0 && (
        <div className="feedback-suggestions">
          <h4>Suggestions</h4>
          <ul>
            {suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}
      {sector_mix && sector_mix.length > 0 && (
        <div className="feedback-sector-mix">
          <h4>Sector mix</h4>
          <ul className="sector-list">
            {sector_mix.map((s, i) => (
              <li key={i}>
                <span className="sector-name">{s.sector}</span>
                <span className="sector-pct">{s.pct}%</span>
                <span className="sector-value">₹{Number(s.value).toLocaleString('en-IN')}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {holdings && holdings.length > 0 && (
        <div className="feedback-holdings">
          <h4>Holdings</h4>
          <div className="holdings-table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Qty</th>
                  <th>Value (₹)</th>
                  <th>Weight %</th>
                  <th>Sector</th>
                </tr>
              </thead>
              <tbody>
                {holdings.map((h, i) => (
                  <tr key={i}>
                    <td>{h.symbol}</td>
                    <td>{h.quantity}</td>
                    <td>{h.value != null ? Number(h.value).toLocaleString('en-IN') : '—'}</td>
                    <td>{h.weight_pct != null ? `${h.weight_pct}%` : '—'}</td>
                    <td>{h.sector || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      {analysis_html && (
        <div className="feedback-dashboard-html">
          <h4>Report</h4>
          <div className="dashboard-html-wrapper" dangerouslySetInnerHTML={{ __html: analysis_html }} />
        </div>
      )}
    </div>
  )
}
