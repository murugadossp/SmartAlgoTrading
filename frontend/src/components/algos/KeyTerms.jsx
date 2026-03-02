/**
 * Simple definitions + examples for trading terms. Collapsible per term for detail.
 */
const GLOSSARY = {
  SMA: {
    term: 'SMA (Simple Moving Average)',
    definition: 'Average of the closing price over the last N days (e.g. 20 or 50). Smooths out daily noise so you can see the trend. When price stays above the SMA, the trend is often up.',
    example: 'Example: If a stock closed at ₹100, ₹102, ₹98, ₹105, ₹101 over 5 days, SMA(5) = (100+102+98+105+101) ÷ 5 = ₹101.2.',
  },
  RSI: {
    term: 'RSI (Relative Strength Index)',
    definition: 'A number from 0 to 100 that measures how fast price has moved. Below 30 is often "oversold" (price may bounce up); above 70 is often "overbought" (price may pull back).',
    example: 'Example: RSI = 25 means the stock has fallen a lot in the lookback period — often treated as oversold. RSI = 75 means it has risen a lot — often overbought.',
  },
  PE: {
    term: 'P/E (Price-to-Earnings)',
    definition: 'Share price divided by earnings per share. A lower P/E can mean the stock is cheaper relative to its earnings. Always compare to similar companies or the sector.',
    example: 'Example: Stock price ₹500, earnings per share ₹25 → P/E = 500 ÷ 25 = 20. So you pay ₹20 for every ₹1 of annual earnings.',
  },
  PB: {
    term: 'P/B (Price-to-Book)',
    definition: 'Share price divided by book value per share. Book value is roughly what the company\'s assets are worth minus debts. P/B below 1 can mean the stock trades below that value.',
    example: 'Example: Stock price ₹200, book value per share ₹250 → P/B = 200 ÷ 250 = 0.8. The market values the company below its book value.',
  },
  ROE: {
    term: 'ROE (Return on Equity)',
    definition: 'How much profit a company makes from shareholders\' equity. Higher ROE often means the company uses capital efficiently. Used as a quality filter in value investing.',
    example: 'Example: Net profit ₹100 cr, equity ₹500 cr → ROE = 100 ÷ 500 = 20%. The company earns 20% on shareholders\' capital.',
  },
  OHLC: {
    term: 'OHLC',
    definition: 'Open, High, Low, Close — the four main prices for a trading day: opening price, highest price, lowest price, and closing price. Used to compute indicators and charts.',
    example: 'Example: Open ₹240, High ₹248, Low ₹238, Close ₹245. So the day started at 240, went as high as 248, as low as 238, and ended at 245.',
  },
  Volume: {
    term: 'Volume',
    definition: 'Number of shares traded in a period. High volume on an up move often means stronger conviction; low volume can mean the move is weak or less reliable.',
    example: 'Example: 1.5 lakh shares traded today vs 50,000 yesterday. Today\'s move on 3× volume is often seen as more significant.',
  },
  Resistance: {
    term: 'Resistance',
    definition: 'A price level where the stock has repeatedly struggled to go above. Breaking above resistance with volume can signal a breakout and a possible new uptrend.',
    example: 'Example: Stock touched ₹300 three times in two months and fell each time. ₹300 is acting as resistance. A close above ₹300 on high volume can be a breakout.',
  },
  Support: {
    term: 'Support',
    definition: 'A price level where the stock has tended to find buyers and bounce. If price breaks below support, it can signal further downside.',
    example: 'Example: Stock bounced from ₹180 several times. ₹180 is support. If price closes below ₹180, the next support might be lower.',
  },
  BollingerBands: {
    term: 'Bollinger Bands',
    definition: 'A band drawn around the price using a moving average and volatility. Price near the lower band can mean oversold; near the upper band, overbought. Used in mean-reversion strategies.',
    example: 'Example: Middle line = 20-day SMA. Upper band = SMA + 2× volatility, lower = SMA − 2×. Price at the lower band might be oversold.',
  },
  EarningsYield: {
    term: 'Earnings yield',
    definition: 'Earnings per share divided by share price (E/P). Like a "return" from company earnings. Compare to risk-free rate or bond yields to see if the stock is attractive.',
    example: 'Example: EPS ₹20, price ₹400 → Earnings yield = 20 ÷ 400 = 5%. If bonds pay 7%, the stock may look less attractive unless growth is expected.',
  },
  IV: {
    term: 'IV (Implied Volatility)',
    definition: 'The market\'s expectation of how much a price may move in the future, derived from options prices. High IV often makes option selling more attractive (premium is higher).',
    example: 'Example: IV of 25% means the market prices in roughly ±25% move over a year. Option premiums are higher when IV is high.',
  },
  Delta: {
    term: 'Delta',
    definition: 'How much an option\'s price is expected to change when the underlying stock moves by ₹1. Used in option selling to choose how far "out of the money" to sell.',
    example: 'Example: Delta 0.16 means the option moves ~₹0.16 for every ₹1 move in the stock. Low delta = further OTM = lower probability of being exercised.',
  },
}

const TERMS_BY_ALGO = {
  momentum: ['OHLC', 'Volume', 'SMA', 'RSI'],
  rsi: ['RSI', 'BollingerBands', 'OHLC'],
  value: ['PE', 'PB', 'ROE', 'EarningsYield'],
  breakout: ['OHLC', 'Volume', 'Resistance', 'Support'],
  option_selling: ['IV', 'Delta'],
}

export default function KeyTerms({ algoId, chartType }) {
  const keys = TERMS_BY_ALGO[chartType] || TERMS_BY_ALGO[algoId] || []
  if (keys.length === 0) return null

  const items = keys.map((key) => GLOSSARY[key]).filter(Boolean)
  if (items.length === 0) return null

  return (
    <section className="algo-key-terms algo-collapsible-section">
      <details className="collapsible-details">
        <summary className="collapsible-summary">Key terms (definitions and examples)</summary>
        <p className="algo-key-terms-intro">Simple definitions and examples for terms used in this strategy. Click a term to expand.</p>
        <dl className="key-terms-list">
          {items.map((item) => (
            <details key={item.term} className="key-term-item key-term-collapsible">
              <summary className="key-term-name">{item.term}</summary>
              <div className="key-term-body">
                <dd className="key-term-def">{item.definition}</dd>
                {item.example && (
                  <p className="key-term-example">
                    <strong>Example:</strong> {item.example}
                  </p>
                )}
              </div>
            </details>
          ))}
        </dl>
      </details>
    </section>
  )
}
