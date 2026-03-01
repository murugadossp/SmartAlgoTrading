# AI-Powered Multi-Algo Trading for Indian Market (Broker API + LLM)

Broker/market data provider abstraction; starting with Dhan, extensible to other providers.

## Goal

Build a system where:

1. **Three user flows**: (a) **Flow 1 — Portfolio / Investment** with an **investment-level** option (multi-asset: equity, debt, MF, etc.) and **stocks deep-dive**; plus **New portfolio** (amount → run algos) and **Existing portfolio feedback** (upload → analyze → rebalancing); (b) **Flow 2 — Explore algos** (filter Stocks/F&O, cards → overview + stocks table); (c) **Flow 3 — Learning cards** (educational content).
2. **Multiple solid algos** (expandable) under filterable **Stocks** and **F&O**; each algo as a card; on click → strategy overview + stocks table.
3. **Backend**: **FastAPI (Python)**; **Frontend**: **React**. Shared pipeline (broker/market data, news, LLM) plus traditional rebalancing logic for existing portfolio.

---

## Three User Flows

### Flow 1: Portfolio / Investment (evolved)

- **Investment (high-level)**: User can provide portfolio **across asset classes** (e.g. equity, debt, mutual funds, gold, cash). System shows **allocation by asset class**; user can run **rebalancing** with target by asset class (e.g. 60% equity / 40% debt). From there, user can **deep-dive into stocks** (equity slice) to run algos or upload/analyze direct equity.
- **Stocks-only path**: **New portfolio** — enter capital (e.g. 1 L), select algos → run algos with sizing → results table. **Existing portfolio feedback** — upload stocks (CSV/Excel) → analyze → feedback and **traditional rebalancing** (target allocation, bands, calendar) → current vs target, suggested buy/sell. No algo run on existing-portfolio path.

**UI**: Portfolio landing with **Investment (multi-asset)** | **Stocks only** (New portfolio | Existing portfolio). From Investment view, link to **Deep-dive: Equity (stocks)** for algo run and stock-level analysis.

### Flow 2: Explore algos

- List algos filterable by **Stocks** vs **F&O**; algo cards; on click → strategy overview + tabular stocks (symbol, name, suggestion, confidence, last price).

### Flow 3: Learning cards

- Learning content as **cards** (e.g. momentum investing, P/E, Option Greeks, Rebalancing, Risk). Categories: Basics, Strategies, Options, Risk. Click card → concept detail.

---

## Portfolio / Investment (Flow 1)

- **Investment-level**: User enters or uploads portfolio by **asset class** (equity, debt, mutual_fund, gold, cash). System returns total value and **allocation by asset class**. Rebalancing at asset-class level (e.g. equity 60%, debt 40%) → current vs target, suggested moves. **Deep-dive: Stocks** uses the equity slice for algo run or stock-level upload/feedback.
- **New portfolio (stocks)**: Enter capital in ₹ (or use equity slice from investment view); position sizing (5–10% per equity); run selected algos → results with suggested quantity/amount.
- **Existing portfolio (stocks)**: Upload CSV/Excel (stocks) → parse → analyze → feedback. **Traditional rebalancing** (target allocation, ±5% bands, calendar) → current vs target weights, suggested buy/sell. Can apply to equity slice when coming from investment view.
- **Use of portfolio size**: Position sizing; risk per trade; capital allocation across algos; max open positions. Amount can be total equity or direct-stocks value from investment view.

---

## Multiple Solid Algos

| Algo               | Focus                      | Instruments   |
| ------------------ | -------------------------- | ------------- |
| **Option selling** | Premium decay, volatility  | NSE F&O       |
| **Momentum**       | Trend-following            | Equity        |
| **Value**          | Undervaluation             | Equity        |
| **Mean reversion** | Oversold/overbought bounce | Equity/index  |
| **Breakout**       | Range breakout             | Equity        |

**Grouping**: **Stocks** — Momentum, Value, Mean reversion, Breakout; **F&O** — Option selling.

---

## High-Level Architecture

- **Shared data**: Broker API (e.g. Dhan: LTP, OHLC, options chain), News (web search), Fundamentals (optional).
- **Analysis**: Technical indicators, sentiment, LLM synthesis → confidence (0–100) + suggestion per algo/symbol.
- **Portfolio**: New portfolio → sizing → run algos → results; Existing portfolio → upload → analyze → rebalance (traditional methods).
- **Execution**: Optional; broker place_order (e.g. Dhan), dry-run first.

---

## Technical Stack

- **Backend**: FastAPI (Python 3.12). APIs: portfolio run/upload/rebalance, algos list/detail/refresh, learning cards.
- **Frontend**: React. Portfolio Mode (2 options), Explore algos (filter, cards, detail), Learning cards.
- **Broker**: Provider-agnostic; first implementation Dhan (`dhanhq` client): LTP, OHLC, options chain, place_order for execution.
- **News**: Web search (Serper/Google/Bing); optional PressMonitor, StockGeist.
- **LLM / Agents**: **AGNO framework** (Agno) for agents; **Pydantic** for JSON response design (structured output). **BaseAgent** takes **global config** from a dedicated **config module** and supports **per-agent overrides**. Each agent in a **separate folder**: **prompts** from **.md** (e.g. `system_instructions.md`), **other info** (model, temperature, params) from **agent-specific config.yaml**.
- **Config**: Dedicated **config module** (global app + global agent defaults); env and YAML for watchlists, algo allocation, API keys.

---

## Project Structure

- **backend/** — FastAPI app; routers (`/portfolio`, `/algos`, `/learning`); `config/`, `src/data/`, `src/analysis/`, `src/algos/`, `src/llm/`, `src/sizing/`, `src/portfolio/` (upload, analyzer, rebalancing).
- **frontend/** — React app; routes for Portfolio Mode, Explore algos, Learning; components (PortfolioMode, AlgoCard, AlgoDetail, LearningCard, LearningDetail, RebalanceView, etc.).
- **docs/** — plan, requirements, design, tasks.

---

## Summary

Three flows: **Flow 1 Portfolio / Investment** (optional investment-level view across asset classes—equity, debt, MF, etc.—with allocation and rebalancing; **stocks deep-dive** for algo run and stock-level feedback; or stocks-only path as today), **Flow 2 Explore algos**, **Flow 3 Learning cards**; **FastAPI** backend and **React** frontend for the Indian market using broker/market data (starting with Dhan) and AI/LLM. See [investment-level-plan.md](investment-level-plan.md) for the investment-level and stocks deep-dive detail.
