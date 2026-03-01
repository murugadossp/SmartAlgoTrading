export default function RebalanceView({ data }) {
  if (!data) return null
  const { current_weights = {}, target_weights = {}, trades = [] } = data
  const symbols = [...new Set([...Object.keys(current_weights), ...Object.keys(target_weights)])].sort()

  return (
    <div className="rebalance-view">
      <h4>Current vs target</h4>
      <div className="rebalance-table-wrap">
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Current %</th>
              <th>Target %</th>
              <th>Diff</th>
            </tr>
          </thead>
          <tbody>
            {symbols.map((sym) => {
              const cur = (current_weights[sym] ?? 0) * 100
              const tgt = (target_weights[sym] ?? 0) * 100
              const diff = tgt - cur
              return (
                <tr key={sym}>
                  <td>{sym}</td>
                  <td>{cur.toFixed(2)}%</td>
                  <td>{tgt.toFixed(2)}%</td>
                  <td className={diff >= 0 ? 'diff-positive' : 'diff-negative'}>
                    {diff >= 0 ? '+' : ''}{(diff).toFixed(2)}%
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      {trades.length > 0 ? (
        <>
          <h4>Suggested trades</h4>
          <div className="trades-table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Action</th>
                  <th>Amount (₹)</th>
                  <th>Qty</th>
                </tr>
              </thead>
              <tbody>
                {trades.map((t, i) => (
                  <tr key={i}>
                    <td>{t.symbol}</td>
                    <td className={t.action === 'buy' ? 'action-buy' : 'action-sell'}>{t.action}</td>
                    <td>{t.amount != null ? `₹${Number(t.amount).toLocaleString('en-IN')}` : '—'}</td>
                    <td>{t.quantity != null ? t.quantity : '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <p className="rebalance-no-trades">No trades suggested (within bands or already at target).</p>
      )}
    </div>
  )
}
