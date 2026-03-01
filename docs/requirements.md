# Requirements (Derived from Plan)

Detailed functional and non-functional requirements for the Smart Algo Trading system (Indian market, broker/market data provider e.g. Dhan—extensible to other providers—and AI/LLM). Implementation status is tracked in [tasks.md](tasks.md).

---

## 1. Functional Requirements

### 1.0 Investment-level (multi-asset) portfolio

| ID   | Requirement | Priority |
|------|-------------|----------|
| R0.1 | User shall be able to provide a portfolio at **investment level** across asset classes (e.g. equity, debt, mutual_fund, gold, cash). Input: amounts per asset class and/or upload of a multi-asset file (rows with asset_class/type and value or holdings). | Must |
| R0.2 | System shall return **allocation by asset class**: total value and percentage per asset class (e.g. Equity 50%, Debt 30%, MF 20%). | Must |
| R0.3 | User shall be able to set **target allocation** at asset-class level (e.g. equity 60%, debt 40%). Rebalancing shall output current vs target by asset class and suggested moves (e.g. "add ₹X to equity", "reduce debt by ₹Y"). | Must |
| R0.4 | From the investment view, user shall be able to **deep-dive into stocks** (equity slice): open New portfolio (with amount = equity value) or Existing portfolio (stocks in that slice) for algo run and stock-level feedback/rebalancing. | Must |
| R0.5 | For v1, asset classes are a fixed list: equity, debt, mutual_fund, gold, cash. MF/bonds may be value-only (no NAV/units fetch). | Should |

### 1.1 Flow 1 — Portfolio Mode (stocks path and investment entry)

#### 1.1.1 New Portfolio

| ID   | Requirement | Priority |
|------|-------------|----------|
| R1.1 | User shall be able to enter total portfolio capital in Indian Rupees (e.g. 1 Lakh, 5 Lakh). Accepted formats: numeric (100000), "1L", "1 Lakh". Amount may be pre-filled from equity slice when coming from investment deep-dive. | Must |
| R1.2 | User shall be able to select one or more algos to run (from Stocks and/or F&O list). | Must |
| R1.3 | User may optionally specify per-algo capital allocation (e.g. 40% momentum, 30% value, 30% option selling). Default: equal or config-based. | Should |
| R1.4 | System shall run selected algos with portfolio-aware position sizing (e.g. 5–10% of portfolio per equity position; margin/premium limits for options). | Must |
| R1.5 | System shall apply risk limits: e.g. 1–2% of portfolio at risk per trade; max open positions derived from portfolio size. | Must |
| R1.6 | System shall return a results table per symbol: symbol, name, suggestion (Buy/Sell/Hold or algo-specific), confidence (0–100), suggested quantity or amount, optional last price. | Must |
| R1.7 | User shall be able to view last run results (e.g. GET last-run) without re-running. | Should |

#### 1.1.2 Existing Portfolio Feedback

| ID   | Requirement | Priority |
|------|-------------|----------|
| R1.8 | User shall be able to upload a portfolio file (CSV or Excel): (a) **Stocks-only**: columns symbol, quantity; optionally avg cost, current price, value; (b) **Multi-asset** (investment-level): rows with asset_class/type and value or holdings (e.g. equity rows: symbol, quantity; MF/bonds: identifier, value or units). System shall support at least one of: single file with asset_class column, or amounts per asset class + optional separate stocks file. | Must |
| R1.9 | System shall parse the file, validate rows, and reject invalid formats with a clear error message. | Must |
| R1.10 | System shall compute and return: total portfolio value, sector mix (if symbol→sector mapping exists), concentration (top N holdings %), top holdings list, simple risk snapshot (e.g. single-name concentration). | Must |
| R1.11 | System shall return feedback: short summary (text), suggestions (e.g. diversification, sector tilt), and optional “which algos may fit” hints. | Must |
| R1.12 | User shall be able to request rebalancing using traditional methods. Inputs: current holdings or multi-asset segments (from upload or session), **target allocation** (at asset-class level e.g. 60% equity / 40% debt, or sector weights within equity), and rebalancing rule (bands e.g. ±5%, or calendar). | Must |
| R1.13 | System shall return rebalancing output: **asset-class level**: current vs target weight per asset class, high-level suggested moves (e.g. "move ₹X from debt to equity"); **stock level** (when equity holdings provided): current weight per holding, target weight, suggested buy/sell list (symbol, action, quantity or amount). | Must |
| R1.14 | No algo-run (no broker market data or LLM) is required for the existing-portfolio path; analysis and rebalancing only. | Must |

### 1.2 Flow 2 — Explore Algos

| ID   | Requirement | Priority |
|------|-------------|----------|
| R2.1 | User shall be able to filter algos by segment: **Stocks** or **F&O**. | Must |
| R2.2 | System shall list algos as cards showing: algo id, name, segment, short description; optionally last run time. | Must |
| R2.3 | User shall be able to click an algo card to open a detail view. | Must |
| R2.4 | Detail view shall show: (1) high-level strategy overview (goal, main inputs, signals, risk in plain language); (2) tabular list of stocks/symbols with columns: symbol, name, suggestion, confidence, last price (data from last run or on-demand refresh). | Must |
| R2.5 | User may trigger an on-demand refresh of the stocks table for one algo (optional). | Should |
| R2.6 | Algos under Stocks: Momentum, Value, Mean reversion, Breakout (and others as added). Algos under F&O: Option selling (and others as added). | Must |

### 1.3 Flow 3 — Learning Cards

| ID   | Requirement | Priority |
|------|-------------|----------|
| R3.1 | User shall be able to browse learning content as **cards** (one concept/topic per card). | Must |
| R3.2 | Each card shall show: id, title, category (e.g. Basics, Strategies, Options, Risk), short description. | Must |
| R3.3 | User shall be able to filter or view cards by category. | Should |
| R3.4 | On card click, system shall show full content: title, body (text), optional image, optional link to external resource. | Must |
| R3.5 | Content may be static (e.g. config/JSON or markdown); no trading or portfolio data required. | Must |

### 1.4 Algos (Strategy Modules)

| ID   | Requirement | Priority |
|------|-------------|----------|
| R4.1 | Each algo shall be a separate module with defined: segment (Stocks or F&O), name, goal, inputs, signals, output (suggestion type), and execution type (equity vs F&O). | Must |
| R4.2 | Option selling algo: inputs from broker options chain (e.g. Dhan: strike, IV, OI); output Sell CE/PE, Hold, Close; position size from margin/premium risk. | Must |
| R4.3 | Momentum algo: inputs OHLC, SMA/EMA, RSI, volume; output Strong Buy/Buy/Hold/Sell; equity MIS/CNC. | Must |
| R4.4 | Value algo: inputs fundamentals (P/E, P/B, ROE, etc.) and price; output Strong Buy/Buy/Hold/Sell; equity CNC. | Must |
| R4.5 | Mean reversion algo: inputs OHLC, RSI, support/resistance; output Buy/Sell/Hold; smaller position size. | Must |
| R4.6 | Breakout algo: inputs OHLC, volume, ATR, range; output Buy/Sell/Hold; equity with ATR-based stop. | Must |
| R4.7 | All algos shall produce a confidence score (0–100) and a suggestion per symbol; LLM may be used to synthesize technical + news into confidence and suggestion. | Must |

### 1.5 Data and Integration

| ID   | Requirement | Priority |
|------|-------------|----------|
| R5.1 | System shall integrate with a broker/market data provider API: authentication, market data (LTP, OHLC, options chain for F&O), and optionally orders (place_order). First implementation: Dhan. | Must |
| R5.2 | System shall support market-level and stock-level news (e.g. via web search API: Serper, Google, or Bing; or optional PressMonitor/StockGeist). | Must |
| R5.3 | System may support fundamental data (P/E, P/B, etc.) via manual CSV or third-party API for Value algo. | Could |
| R5.4 | Rate limits: respect provider API limits (e.g. Dhan: 5/sec data, 10/sec orders); throttle or queue requests as needed. | Must |

### 1.6 Execution (Optional)

| ID   | Requirement | Priority |
|------|-------------|----------|
| R6.1 | If execution is enabled, system shall only place orders when suggestion and confidence meet configurable thresholds (e.g. confidence > 70, action Buy/Strong Buy). | Must |
| R6.2 | Execution shall use portfolio-based position sizing and risk limits; dry-run mode shall be supported before live orders. | Must |
| R6.3 | Order placement via broker API (e.g. Dhan: security_id, exchange_segment, transaction_type, quantity, order_type, product_type). | Must |

---

## 2. Agent Framework and Response Design (AGNO, BaseAgent, Pydantic)

| ID   | Requirement | Priority |
|------|-------------|----------|
| R2A.1 | The backend shall use the **AGNO framework** (Agno) for building and running LLM agents (e.g. scoring, feedback, per-algo agents). | Must |
| R2A.2 | All agent outputs that are part of the API or downstream logic shall conform to a **JSON response design pattern** using **Pydantic** models: define response schemas (e.g. confidence, suggestion, reasoning) and validate/parse agent output against them. | Must |
| R2A.3 | A **BaseAgent** (or equivalent) shall accept **global config** (model provider, model name, temperature, API keys, etc.) from a central **config module**, and shall support **per-agent overrides** (e.g. different model or temperature per agent) without changing global defaults. | Must |
| R2A.4 | **Config module** shall be implemented separately from agent logic: it shall expose global app settings (env, YAML) and **global agent config** (model defaults for BaseAgent). | Must |
| R2A.5 | **Each agent** shall reside in its **own folder** (e.g. `agents/<agent_name>/`). **Prompts** (system instructions) shall be stored in **.md** files (e.g. `system_instructions.md`). **Other agent-specific info** (model, temperature, overrides, params for prompt construction) shall be in **config.yaml** only; no prompt text in YAML. | Must |
| R2A.6 | BaseAgent (or loader) shall load **prompts from .md** and **other settings from config.yaml** per agent. When the .md prompt contains placeholders, the agent shall construct the final prompt by substituting values from config.yaml and from runtime. Overrides may be per-agent config.yaml and/or central agent registry; per-agent takes precedence. | Must |

---

## 3. Non-Functional Requirements

| ID    | Requirement | Priority |
|-------|-------------|----------|
| NFR1  | Backend shall be implemented in Python 3.12 using FastAPI; frontend in React. Backend shall use AGNO for agents and Pydantic for request/response and agent JSON output schemas. | Must |
| NFR2  | API responses shall be JSON; appropriate HTTP status codes and error payloads (errorCode, errorMessage). | Must |
| NFR3  | Sensitive data (API keys, broker tokens e.g. Dhan) shall be stored via environment variables or secure config; not committed to repo. | Must |
| NFR4  | Frontend shall be responsive and usable on desktop; mobile-friendly is a should. | Should |
| NFR5  | Documentation: API contract (OpenAPI/Swagger) and high-level docs (plan, requirements, design, tasks) in `docs/`. | Must |
| NFR6  | Project shall have two top-level folders: `frontend/` and `backend/`; shared docs in `docs/`. | Must |

---

## 3. Out of Scope (Explicit)

- Real-money execution without explicit user configuration and dry-run phase.
- Architecture supports multiple broker/market data providers; Dhan is the initial implementation.
- Mobile-native apps (web only for now).
- User authentication and multi-tenancy (can be added later).
