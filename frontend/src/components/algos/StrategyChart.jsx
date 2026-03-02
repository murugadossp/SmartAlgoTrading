/**
 * Strategy concept diagrams — intuitive visuals (no data chart).
 * Each diagram explains the logic at a glance.
 */

function MomentumDiagram() {
  return (
    <div className="strategy-diagram strategy-diagram-momentum">
      <div className="diagram-row">
        <span className="diagram-label">Price</span>
        <div className="diagram-bar diagram-bar-price" style={{ width: '100%' }} />
      </div>
      <div className="diagram-row">
        <span className="diagram-label">SMA 20</span>
        <div className="diagram-bar diagram-bar-sma20" style={{ width: '85%' }} />
      </div>
      <div className="diagram-row">
        <span className="diagram-label">SMA 50</span>
        <div className="diagram-bar diagram-bar-sma50" style={{ width: '70%' }} />
      </div>
      <p className="diagram-caption">
        <strong>Buy</strong> when Price &gt; SMA20 &gt; SMA50 (stacked trend). <strong>Sell</strong> when price falls below SMAs or momentum fades.
      </p>
    </div>
  )
}

function RSIDiagram() {
  return (
    <div className="strategy-diagram strategy-diagram-rsi">
      <div className="rsi-scale">
        <div className="rsi-zone rsi-overbought" title="Overbought – consider sell">
          <span>70–100</span>
          <span className="rsi-zone-label">Overbought → Sell</span>
        </div>
        <div className="rsi-zone rsi-neutral" title="Neutral">
          <span>30–70</span>
          <span className="rsi-zone-label">Neutral</span>
        </div>
        <div className="rsi-zone rsi-oversold" title="Oversold – consider buy">
          <span>0–30</span>
          <span className="rsi-zone-label">Oversold → Buy</span>
        </div>
      </div>
      <p className="diagram-caption">
        <strong>Buy</strong> when RSI &lt; 30 (oversold). <strong>Sell</strong> when RSI &gt; 70 (overbought).
      </p>
    </div>
  )
}

function ValueDiagram() {
  return (
    <div className="strategy-diagram strategy-diagram-value">
      <div className="value-flow">
        <div className="value-box value-buy">
          <span className="value-title">Low P/E, P/B</span>
          <span className="value-arrow">→</span>
          <span className="value-action">Buy</span>
        </div>
        <div className="value-box value-sell">
          <span className="value-title">High P/E vs peers</span>
          <span className="value-arrow">→</span>
          <span className="value-action">Sell / Hold</span>
        </div>
      </div>
      <p className="diagram-caption">
        Compare P/E and P/B to sector or history. Buy when undervalued; reduce when valuation reverts.
      </p>
    </div>
  )
}

function BreakoutDiagram() {
  return (
    <div className="strategy-diagram strategy-diagram-breakout">
      <div className="breakout-visual">
        <div className="breakout-resistance">Resistance</div>
        <div className="breakout-price-up">Price + Volume ↑</div>
        <div className="breakout-arrow">↑ Breakout → Buy</div>
      </div>
      <p className="diagram-caption">
        <strong>Buy</strong> when price breaks above resistance (e.g. 20d high) with above-average volume. Stop at breakout level.
      </p>
    </div>
  )
}

export default function StrategyChart({ chartType }) {
  if (!chartType) return null

  return (
    <div className="strategy-chart-wrap">
      {chartType === 'momentum' && <MomentumDiagram />}
      {chartType === 'rsi' && <RSIDiagram />}
      {chartType === 'value' && <ValueDiagram />}
      {chartType === 'breakout' && <BreakoutDiagram />}
    </div>
  )
}
