import { Routes, Route, Link } from 'react-router-dom'
import Layout from './components/Layout'
import Card from './components/Card'
import NewPortfolioForm from './components/portfolio/NewPortfolioForm'
import ExistingPortfolioUpload from './components/portfolio/ExistingPortfolioUpload'
import ExploreAlgos from './components/algos/ExploreAlgos'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/portfolio" element={<PortfolioInvestmentLanding />} />
        <Route path="/portfolio/investment" element={<InvestmentFlowPage />} />
        <Route path="/portfolio/stocks" element={<StocksOnlyPage />} />
        <Route path="/portfolio/new" element={<NewPortfolioPage />} />
        <Route path="/portfolio/existing" element={<ExistingPortfolioPage />} />
        <Route path="/algos" element={<ExploreAlgosPage />} />
        <Route path="/algos/:algoId" element={<AlgoDetailPlaceholder />} />
        <Route path="/learning" element={<LearningPlaceholder />} />
        <Route path="/profile" element={<ProfilePlaceholder />} />
        <Route path="/settings" element={<SettingsPlaceholder />} />
        <Route path="/preferences" element={<PreferencesPlaceholder />} />
      </Route>
    </Routes>
  )
}

function Home() {
  return (
    <div className="home-page">
      <section className="hero">
        <span className="hero-badge">AI-powered trading</span>
        <h1>Smart Algo Trading</h1>
        <p className="hero-tagline">
          Multi-algo strategies for the Indian market. Run portfolios, explore algorithms, and learn—powered by market data and LLM insights.
        </p>
      </section>
      <p className="landing-section-label">Get started</p>
      <section className="feature-cards">
        <Link to="/portfolio" className="feature-card-link">
          <article className="landing-card">
            <div className="landing-card-icon" aria-hidden>1</div>
            <h3>Portfolio / Investment</h3>
            <p>Investment-level view across asset classes (equity, debt, MF) or stocks-only: run algos, analyze holdings, rebalance.</p>
            <span className="landing-card-cta">Open Portfolio →</span>
          </article>
        </Link>
        <Link to="/algos" className="feature-card-link">
          <article className="landing-card">
            <div className="landing-card-icon" aria-hidden>2</div>
            <h3>Explore Algos</h3>
            <p>Filter by Stocks or F&amp;O. Browse strategy cards with overviews and suggested watchlists.</p>
            <span className="landing-card-cta">Explore Algos →</span>
          </article>
        </Link>
        <Link to="/learning" className="feature-card-link">
          <article className="landing-card">
            <div className="landing-card-icon" aria-hidden>3</div>
            <h3>Learning</h3>
            <p>Concepts, strategies, and terminology. Learning cards to level up your trading knowledge.</p>
            <span className="landing-card-cta">Start Learning →</span>
          </article>
        </Link>
      </section>
    </div>
  )
}

/** Portfolio landing: Investment (multi-asset) | Stocks only (plan: investment-level and stocks deep-dive) */
function PortfolioInvestmentLanding() {
  return (
    <div className="portfolio-mode">
      <h1>Portfolio / Investment</h1>
      <p className="section-desc">
        View and manage at investment level (equity, debt, MF, etc.) or work directly with stocks.
      </p>
      <div className="feature-cards two-cols">
        <Link to="/portfolio/investment" className="feature-card-link">
          <article className="landing-card">
            <div className="landing-card-icon" aria-hidden>1</div>
            <h3>Investment (multi-asset)</h3>
            <p>Enter or upload portfolio across asset classes. See allocation, rebalance by target, then deep-dive into equity (stocks).</p>
            <span className="landing-card-cta">Investment view →</span>
          </article>
        </Link>
        <Link to="/portfolio/stocks" className="feature-card-link">
          <article className="landing-card">
            <div className="landing-card-icon" aria-hidden>2</div>
            <h3>Stocks only</h3>
            <p>Work with direct equity only: new portfolio (run algos with sizing) or existing holdings (analysis and rebalancing).</p>
            <span className="landing-card-cta">Stocks only →</span>
          </article>
        </Link>
      </div>
    </div>
  )
}

/** Stocks-only path: New portfolio | Existing portfolio */
function StocksOnlyPage() {
  return (
    <div className="portfolio-mode stocks-only">
      <Link to="/portfolio" className="back-link">← Portfolio / Investment</Link>
      <h1>Stocks only</h1>
      <p className="section-desc">Run algos with a new portfolio or analyze and rebalance existing equity holdings.</p>
      <div className="feature-cards two-cols">
        <Link to="/portfolio/new" className="feature-card-link">
          <article className="landing-card">
            <div className="landing-card-icon" aria-hidden>1</div>
            <h3>New portfolio</h3>
            <p>Enter capital, select algos, run and get suggestions with position sizing.</p>
            <span className="landing-card-cta">New portfolio →</span>
          </article>
        </Link>
        <Link to="/portfolio/existing" className="feature-card-link">
          <article className="landing-card">
            <div className="landing-card-icon" aria-hidden>2</div>
            <h3>Existing portfolio</h3>
            <p>Upload holdings, get analysis and rebalancing suggestions.</p>
            <span className="landing-card-cta">Existing portfolio →</span>
          </article>
        </Link>
      </div>
    </div>
  )
}

/** Investment (multi-asset) flow: allocation by asset class → rebalance → Deep-dive: Stocks (Phase 3B) */
function InvestmentFlowPage() {
  return (
    <div className="portfolio-mode investment-flow">
      <Link to="/portfolio" className="back-link">← Portfolio / Investment</Link>
      <h1>Investment (multi-asset)</h1>
      <p className="section-desc">
        Provide your portfolio across asset classes (equity, debt, mutual funds, gold, cash). View allocation and rebalance by target; then deep-dive into the equity slice for algo runs and stock-level analysis.
      </p>
      <div className="investment-flow-steps">
        <ol className="flow-steps-list">
          <li>Enter or upload multi-asset portfolio (amounts per asset class or file with asset_class column).</li>
          <li>View allocation by asset class (e.g. Equity 50%, Debt 30%, MF 20%).</li>
          <li>Set target allocation and run rebalancing (current vs target, suggested moves).</li>
          <li>Deep-dive into <strong>Equity (stocks)</strong> to run algos or analyze existing stock holdings.</li>
        </ol>
      </div>
      <div className="investment-flow-actions">
        <Link to="/portfolio/stocks" className="cta-button">
          Deep-dive: Equity (stocks) →
        </Link>
        <p className="flow-note">Multi-asset input, allocation view, and asset-class rebalancing will be available in Phase 3B.</p>
      </div>
    </div>
  )
}

function NewPortfolioPage() {
  return (
    <Card title="New portfolio">
      <NewPortfolioForm />
    </Card>
  )
}

function ExistingPortfolioPage() {
  return (
    <Card title="Existing portfolio">
      <Link to="/portfolio/stocks" className="back-link">← Stocks only</Link>
      <ExistingPortfolioUpload />
    </Card>
  )
}

function AlgoDetailPlaceholder() {
  return (
    <Card title="Algo detail">
      <p>Algo overview and stocks table will be wired here.</p>
    </Card>
  )
}

function ExploreAlgosPage() {
  return (
    <div className="explore-algos">
      <ExploreAlgos />
    </div>
  )
}

function LearningPlaceholder() {
  return (
    <Card title="Learning Cards">
      <p>Learning content will go here.</p>
    </Card>
  )
}

function ProfilePlaceholder() {
  return (
    <Card title="Profile">
      <p>Profile and account details will go here.</p>
    </Card>
  )
}

function SettingsPlaceholder() {
  return (
    <Card title="Settings">
      <p>App and notification settings will go here.</p>
    </Card>
  )
}

function PreferencesPlaceholder() {
  return (
    <Card title="Preferences">
      <p>Display and trading preferences will go here.</p>
    </Card>
  )
}

export default App
