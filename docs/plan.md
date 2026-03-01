# AI-Powered Multi-Algo Trading for Indian Market (Dhan API + LLM)

## Goal

Build a system where:

1. **Three user flows**: (a) **Flow 1 — Portfolio Mode** with two options: **New portfolio** (amount → run algos with sizing) and **Existing portfolio feedback** (upload → analyze → feedback and **traditional rebalancing**); (b) **Flow 2 — Explore algos** (filter Stocks/F&O, cards → overview + stocks table); (c) **Flow 3 — Learning cards** (educational content).
2. **Multiple solid algos** (expandable) under filterable **Stocks** and **F&O**; each algo as a card; on click → strategy overview + stocks table.
3. **Backend**: **FastAPI (Python)**; **Frontend**: **React**. Shared pipeline (Dhan, news, LLM) plus traditional rebalancing logic for existing portfolio.

---

## Three User Flows

### Flow 1: Portfolio Mode (two options)

- **Option 1 — New portfolio**: User enters total capital (e.g. 1 L). Select algos and allocation → run algos with portfolio-aware sizing → results table (symbol, suggestion, confidence, suggested quantity/amount).
- **Option 2 — Existing portfolio feedback**: User uploads current portfolio (CSV/Excel). Backend analyzes (total value, sector mix, concentration, risk) → feedback (summary, suggestions). Then **traditional rebalancing** (target allocation, rebalancing bands, calendar rebalancing) → current vs target weights, suggested buy/sell. No algo run.

**UI**: Portfolio Mode with two choices: **New portfolio** | **Existing portfolio**.

### Flow 2: Explore algos

- List algos filterable by **Stocks** vs **F&O**; algo cards; on click → strategy overview + tabular stocks (symbol, name, suggestion, confidence, last price).

### Flow 3: Learning cards

- Learning content as **cards** (e.g. momentum investing, P/E, Option Greeks, Rebalancing, Risk). Categories: Basics, Strategies, Options, Risk. Click card → concept detail.

---

## Portfolio Mode — two options (Flow 1)

- **New portfolio**: Enter capital in ₹; position sizing (5–10% per equity); risk per trade (1–2% of portfolio); run selected algos → results with suggested quantity/amount.
- **Existing portfolio feedback**: Upload CSV/Excel → parse → analyze (total value, sector mix, concentration) → feedback. Apply **traditional rebalancing** (target allocation, ±5% bands, calendar) → current vs target weights, suggested buy/sell.
- **Use of portfolio size** (New portfolio): Position sizing; risk per trade; capital allocation across algos; max open positions.

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

- **Shared data**: Dhan API (LTP, OHLC, options chain), News (web search), Fundamentals (optional).
- **Analysis**: Technical indicators, sentiment, LLM synthesis → confidence (0–100) + suggestion per algo/symbol.
- **Portfolio**: New portfolio → sizing → run algos → results; Existing portfolio → upload → analyze → rebalance (traditional methods).
- **Execution**: Optional; Dhan place_order with dry-run first.

---

## Technical Stack

- **Backend**: FastAPI (Python 3.10+). APIs: portfolio run/upload/rebalance, algos list/detail/refresh, learning cards.
- **Frontend**: React. Portfolio Mode (2 options), Explore algos (filter, cards, detail), Learning cards.
- **Dhan**: `dhanhq` client; LTP, OHLC, options chain; place_order for execution.
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

Three flows: **Flow 1 Portfolio Mode** (new portfolio or existing portfolio with feedback and traditional rebalancing), **Flow 2 Explore algos**, **Flow 3 Learning cards**; **FastAPI** backend and **React** frontend for the Indian market using Dhan and AI/LLM.
