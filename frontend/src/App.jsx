import { Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/portfolio">Portfolio Mode</Link>
        <Link to="/algos">Explore Algos</Link>
        <Link to="/learning">Learning</Link>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/portfolio" element={<PortfolioPlaceholder />} />
          <Route path="/algos" element={<AlgosPlaceholder />} />
          <Route path="/learning" element={<LearningPlaceholder />} />
        </Routes>
      </main>
    </>
  )
}

function Home() {
  return (
    <div>
      <h1>Smart Algo Trading</h1>
      <p>AI-powered multi-algo trading for the Indian market (Dhan API + LLM).</p>
      <ul>
        <li><Link to="/portfolio">Portfolio Mode</Link> — New portfolio or existing portfolio feedback & rebalancing</li>
        <li><Link to="/algos">Explore Algos</Link> — Filter Stocks / F&O, algo cards, strategy overview & stocks table</li>
        <li><Link to="/learning">Learning</Link> — Learning cards</li>
      </ul>
    </div>
  )
}

function PortfolioPlaceholder() {
  return <h2>Portfolio Mode</h2>
}

function AlgosPlaceholder() {
  return <h2>Explore Algos</h2>
}

function LearningPlaceholder() {
  return <h2>Learning Cards</h2>
}

export default App
