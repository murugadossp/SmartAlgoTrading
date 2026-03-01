# Tasks (Detailed)

Phased implementation tasks derived from the plan, requirements, and design. Use this for sprint planning and tracking.

---

## Implementation status (as of last update)

| Phase | Status | Notes |
|-------|--------|--------|
| Phase 0 | Done | Repo structure, FastAPI/React, CORS, config module, BaseAgent pattern, per-agent .md + config.yaml, Pydantic models. |
| Phase 1 | Done | Algo config (algos.yaml), broker factory + Dhan client, market data service; options chain/news optional. |
| Phase 2 | Done | Technical analysis (SMA, RSI), scoring agent, Momentum algo, sizing, POST /portfolio/run, GET /portfolio/last-run, New Portfolio UI. |
| Phase 3 | Done (except T3.3b) | Parser (CSV/Excel), analyzer, feedback builder, **rebalancing logic** (T3.4), POST /portfolio/upload (T3.5), **POST /portfolio/rebalance** (T3.6), Existing Portfolio upload + **Rebalance form + RebalanceView** (T3.7, T3.8), Portfolio landing Investment \| Stocks only (T3.9). **T3.3b** (LLM portfolio dashboard HTML) pending. |
| Phase 3B | Pending | Multi-asset segments, POST /portfolio/investment, asset-class rebalance, AllocationView, Deep-dive: Stocks. |
| Phase 4 | Partial | GET /algos, GET/POST algo detail/refresh implemented; Explore Algos page and filter done; algo detail page with StocksTable/Refresh pending (T4.5); remaining algos (Value, Mean reversion, Breakout, Option selling) pending (T4.6). |
| Phase 5–8 | Pending | Learning cards, news in pipeline, execution, polish, tests. |

See [testprocess.md](testprocess.md) for manual and automated test procedures.

---

## Phase 0: Project Setup and Structure


| Task ID | Task                                                                                                                               | Owner | Deps       | Notes                                                 |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------- | ----------------------------------------------------- |
| T0.1    | Create repo root with `frontend/`, `backend/`, `docs/` (docs already contains plan, requirements, design, tasks).                  | -     | -          | Ensure `frontend/` and `backend/` exist at top level. |
| T0.2    | Initialize backend: Python 3.10+, FastAPI, `app/main.py`, `requirements.txt`, `app/config.py` (env-based settings).                | -     | T0.1       | Basic FastAPI app with health check `GET /health`.    |
| T0.3    | Initialize frontend: React (Vite or CRA), React Router, `src/App.jsx` with nav placeholder for Portfolio, Explore, Learning.       | -     | T0.1       | Single page with 3 nav links.                         |
| T0.4    | Add backend CORS for frontend origin; add `.env.example` for backend (API keys, broker client credentials e.g. Dhan client_id) and frontend (API base URL). | -     | T0.2, T0.3 | Document required env vars in README.                 |
| T0.5    | Add **config module** (e.g. `app/config/`): global settings (Pydantic from env), **global_agent_config** (model defaults for BaseAgent). Keep separate from agent code. | -     | T0.2       | See design §2.2.1.                                   |
| T0.6    | Implement **BaseAgent** (AGNO): accepts global config from config module; supports **per-agent overrides** (model, temperature, etc.). | -     | T0.5       | In `app/agents/base_agent.py`.                        |
| T0.7    | Add **per-agent folder layout**: each agent in `app/agents/<agent_name>/` with **system_instructions.md** (prompts for LLM) and **config.yaml** (model, temperature, params only; no prompt text). BaseAgent loads .md + config.yaml, merges with global config; support optional central agent overrides. | -     | T0.6       | Example: `scoring_agent/system_instructions.md` + `scoring_agent/config.yaml`.         |
| T0.8    | Define **Pydantic models** for all agent JSON responses (e.g. AlgoScoringResponse: confidence, suggestion, reasoning); use as structured output schema in agents. | -     | T0.2       | In `app/models/responses.py` or similar.              |


---

## Phase 1: Config and Data Layer (Backend)


| Task ID | Task                                                                                                                                  | Owner | Deps       | Notes                                                                             |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------- | --------------------------------------------------------------------------------- |
| T1.1    | Add `backend/config/` with algo metadata (id, name, segment, short_description, overview text) and watchlists per algo (symbol list). | -     | T0.2       | JSON or YAML; at least Momentum, Value, Mean reversion, Breakout, Option selling. |
| T1.2    | Implement broker/market data client wrapper (first implementation: Dhan) in `backend/app/data/`: auth (token + client_id), get LTP, get OHLC for given security_ids. | -     | T0.2       | Use `dhanhq` for Dhan; respect rate limits.                                                |
| T1.3    | Add market data service: fetch OHLC for a list of symbols (map symbol → security_id via config or static map).                        | -     | T1.1, T1.2 | Used by algos.                                                                    |
| T1.4    | (Optional) Add options chain fetcher for F&O segment (if provider supports; e.g. Dhan); else stub for Option selling algo.                           | -     | T1.2       |                                                                                   |
| T1.5    | Add news fetcher: call web search API (e.g. Serper) for market-level and per-symbol queries; return titles and snippets.              | -     | T0.2       | Configurable API key; limit results per query.                                    |


---

## Phase 2: Portfolio Mode — New Portfolio (Backend + Frontend)


| Task ID | Task                                                                                                                                                                                                | Owner | Deps             | Notes                                      |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------------- | ------------------------------------------ |
| T2.1    | Implement technical analysis module: compute SMA(20, 50), RSI, optional MACD from OHLC; output structured “view” per symbol.                                                                        | -     | T1.3             | In `app/analysis/`.                        |
| T2.2    | Implement scoring agent (AGNO + BaseAgent): load system instructions and config from `agents/scoring_agent/`; use Pydantic schema for response (confidence, suggestion, reasoning). Call from algo pipeline with technical + optional news summary. | -     | T0.6, T0.7, T0.8, T1.5 | In `app/llm/` or via `app/agents/`; structured output via Pydantic. |
| T2.3    | Implement one algo (e.g. Momentum) end-to-end: load watchlist, get OHLC, compute technicals, optional news + LLM, return list of { symbol, suggestion, confidence }.                                | -     | T1.3, T2.1, T2.2 | In `app/algos/momentum.py` (or similar).   |
| T2.4    | Implement sizing module: given portfolio amount and allocation map, compute max position size per symbol (e.g. 5% of portfolio), suggested quantity from price.                                     | -     | T0.2             | In `app/sizing/`.                          |
| T2.5    | Implement `POST /portfolio/run`: accept amount, algo_ids, optional allocation; run selected algos; apply sizing; return results table.                                                              | -     | T2.3, T2.4       | In `app/api/portfolio.py`.                 |
| T2.6    | Implement `GET /portfolio/last-run`: return last run result from memory or simple file/cache.                                                                                                       | -     | T2.5             | Optional persistence.                      |
| T2.7    | Frontend: New Portfolio form (amount input, algo multi-select, optional allocation); call POST /portfolio/run; display RunResultsTable (symbol, suggestion, confidence, suggested_quantity/amount). | -     | T0.3, T2.5       | In `frontend/src/`.                        |
| T2.8    | Add error handling and loading states on frontend for portfolio run.                                                                                                                                | -     | T2.7             |                                            |


---

## Phase 3: Portfolio Mode — Existing Portfolio and Rebalancing (Backend + Frontend)


| Task ID | Task                                                                                                                                                                                                                                                                                    | Owner                                                                  | Deps             | Notes                                             |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------- | ------------------------------------------------- |
| T3.1    | Implement CSV/Excel parser: parse file to list of { symbol, quantity, avg_cost or value }; validate and return errors for invalid rows.                                                                                                                                                 | -                                                                      | T0.2             | In `app/portfolio/` or `app/services/portfolio/`. |
| T3.2    | Implement portfolio analyzer: given holdings list, compute total value, sector mix (if mapping available), concentration (top N %), top holdings.                                                                                                                                       | -                                                                      | T3.1             |                                                   |
| T3.3    | Implement feedback builder: generate summary text and suggestions (e.g. diversification, concentration risk) from analyzer output.                                                                                                                                                      | -                                                                      | T3.2             | Can be rule-based or short LLM call.              |
| T3.3b   | **LLM portfolio research (dashboard HTML)**: Portfolio-research agent: input = analyzer output (+ optional algo run results); LLM produces **equity-research-style HTML** (dashboard: sections, metrics, tables). API returns `feedback.analysis_html`; frontend renders in dashboard view (sanitized). | -                                                                      | T3.2, T3.3       | Like equity research on Claude; prompt asks for display-ready HTML.    |
| T3.4    | Implement rebalancing logic: input current holdings and/or segments (asset-class); target allocation (asset-class e.g. equity 60%, debt 40%, or per-sector within equity); compute current weights; output current vs target; list of trades (asset-class and/or symbol-level). Support band-based (e.g. ±5%) or full rebalance. | -                                                                      | T3.1             | In `app/portfolio/rebalance.py`.                  |
| T3.5    | Implement `POST /portfolio/upload`: multipart file upload; parse → analyze → feedback; return total_value, holdings (stocks) and/or segments (multi-asset), feedback, sector_mix, concentration; for multi-asset, return allocation by asset_class.                                                                   | -                                                                      | T3.1, T3.2, T3.3 |                                                   |
| T3.6    | Implement `POST /portfolio/rebalance`: body holdings and/or segments + target_allocation (asset_class or symbol) + strategy; return current_weights, target_weights, trades (asset-class and/or stock-level).                                                                                                             | -                                                                      | T3.4             |                                                   |
| T3.7    | Frontend: Existing Portfolio flow — file upload component; call POST /portfolio/upload; display AnalysisFeedback (summary, suggestions).                                                                                                                                                                                | -                                                                      | T0.3, T3.5       |                                                   |
| T3.8    | Frontend: Rebalance form (target allocation inputs or preset); call POST /portfolio/rebalance; display RebalanceView (current vs target table, suggested trades; support asset-class and stock-level).                                                                                                                 | -                                                                      | T3.7, T3.6       |                                                   |
| T3.9    | Wire Portfolio Mode landing: entry **Investment (multi-asset)** \| **Stocks only** (New portfolio \| Existing portfolio); route accordingly. From Investment path, link "Deep-dive: Stocks" to New/Existing with equity context.                                                                                        | -                                                                      | T2.7, T3.7       |                                                   |


---

## Phase 3B: Investment-level portfolio (Backend + Frontend)

| Task ID  | Task                                                                                                                                                                                                                                                                 | Owner | Deps    | Notes                                                                 |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ------- | --------------------------------------------------------------------- |
| T3B.1    | Extend data model: portfolio segments (asset_class, value, holdings?). Asset classes: equity, debt, mutual_fund, gold, cash (fixed for v1). Support input as amounts per asset_class and/or multi-asset upload (file with asset_class/type column).                    | -     | T3.1    | Pydantic models in `app/models/`.                                      |
| T3B.2    | Implement `POST /portfolio/investment` (or extend upload): accept segments or multi-asset file; return total_value, allocation[] (asset_class, value, pct); optional feedback.                                                                                          | -     | T3B.1   | Reuse or extend upload parser for multi-asset rows.                    |
| T3B.3    | Extend rebalancing: accept segments; target_allocation at asset_class level; output current vs target by asset_class, high-level trades (e.g. "add ₹X to equity"). When equity holdings provided, include stock-level trades.                                          | -     | T3.4    | In `app/portfolio/rebalance.py`.                                       |
| T3B.4    | Frontend: Investment path — input or upload multi-asset portfolio; call investment/upload API; display AllocationView (pie or table by asset_class).                                                                                                                 | -     | T0.3    | Route e.g. `/portfolio/investment`.                                    |
| T3B.5    | Frontend: Rebalance by asset class (target allocation form); display asset-class RebalanceView; link "Deep-dive: Equity (stocks)" to `/portfolio/new` (amount = equity value) or `/portfolio/existing` (stocks in equity slice).                                   | -     | T3B.4, T3.6 |                                                                  |

See [investment-level-plan.md](investment-level-plan.md).

---

## Phase 4: Explore Algos (Backend + Frontend)


| Task ID | Task                                                                                                                                                                      | Owner                                                                      | Deps             | Notes                                               |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------- | --------------------------------------------------- |
| T4.1    | Implement `GET /algos?segment=stocks                                                                                                                                      | fno`: return algo list from config (id, name, segment, short_description). | -                | T1.1                                                |
| T4.2    | Implement `GET /algos/{algo_id}`: return overview (from config) + stocks table (from last run or cache for that algo). If no data, return overview only and empty stocks. | -                                                                          | T1.1, T2.3       |                                                     |
| T4.3    | Implement `POST /algos/{algo_id}/refresh`: run that algo (no portfolio sizing); return updated stocks table; cache result for GET detail.                                 | -                                                                          | T2.3, T4.2       |                                                     |
| T4.4    | Frontend: Explore Algos page; segment filter (Stocks                                                                                                                      | F&O); fetch GET /algos?segment=; render AlgoCard grid.                     | -                | T0.3, T4.1                                          |
| T4.5    | Frontend: Algo detail page (route /algos/:id); fetch GET /algos/:id; render overview + StocksTable; optional Refresh button → POST /algos/:id/refresh.                    | -                                                                          | T4.2, T4.3       |                                                     |
| T4.6    | Add remaining algos (Value, Mean reversion, Breakout, Option selling) as modules; each returns list of { symbol, suggestion, confidence }; wire into GET/POST algos.      | -                                                                          | T2.3, T4.2, T4.3 | Can stub Option selling if options chain not ready. |


---

## Phase 5: Learning Cards (Backend + Frontend)


| Task ID | Task                                                                                                                                                 | Owner | Deps       | Notes                                          |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------- | ---------------------------------------------- |
| T5.1    | Add learning content in `backend/config/learning/`: e.g. `cards.json` (id, title, category, short_description) and per-card body (markdown or HTML). | -     | T0.2       | Categories: Basics, Strategies, Options, Risk. |
| T5.2    | Implement `GET /learning/cards?category=`: return list of cards (optionally filtered by category).                                                   | -     | T5.1       | In `app/api/learning.py`.                      |
| T5.3    | Implement `GET /learning/cards/{id}`: return full card (title, category, body, optional image_url, link).                                            | -     | T5.1       |                                                |
| T5.4    | Frontend: Learning page; fetch GET /learning/cards; render LearningCard grid; optional category filter.                                              | -     | T0.3, T5.2 |                                                |
| T5.5    | Frontend: Learning detail (route /learning/:id); fetch GET /learning/cards/:id; render LearningDetail (title, body, image, link).                    | -     | T5.3       |                                                |


---

## Phase 6: News and LLM Integration (Enhancement)


| Task ID | Task                                                                                                                              | Owner | Deps       | Notes                                       |
| ------- | --------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------- | ------------------------------------------- |
| T6.1    | Integrate market-level and stock-level news into algo pipeline: fetch news before LLM call; include headlines/snippets in prompt. | -     | T1.5, T2.2 | Improves confidence and suggestion quality. |
| T6.2    | Add sentiment summary (LLM or small model) for news; pass to main scoring prompt.                                                 | -     | T6.1       | Optional.                                   |


---

## Phase 7: Execution (Optional)


| Task ID | Task                                                                                                                                          | Owner | Deps       | Notes                                    |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------- | ---------------------------------------- |
| T7.1    | Implement execution module: read run results; filter by confidence threshold and action; compute quantity from sizing; call broker place_order (e.g. Dhan). | -     | T1.2, T2.4 | Behind feature flag; dry-run mode first. |
| T7.2    | Add config for execution: enable/disable, confidence threshold, dry_run flag.                                                                 | -     | T7.1       |                                          |
| T7.3    | Expose “Execute” (or “Paper trade”) in UI for run results; confirm step before calling backend execution endpoint.                            | -     | T2.7, T7.1 | Optional.                                |


---

## Phase 8: Polish and Documentation


| Task ID | Task                                                                                            | Owner | Deps                   | Notes                                     |
| ------- | ----------------------------------------------------------------------------------------------- | ----- | ---------------------- | ----------------------------------------- |
| T8.1    | OpenAPI/Swagger for all backend endpoints; export and keep in `docs/` or serve from `/docs`.    | -     | All API tasks          | FastAPI auto-generates; add descriptions. |
| T8.2    | README in repo root: project overview, how to run backend and frontend, env vars, link to docs. | -     | -                      |                                           |
| T8.3    | README in `backend/`: setup, install, run, env; link to API docs.                               | -     | T0.2                   |                                           |
| T8.4    | README in `frontend/`: setup, install, run, env (API URL).                                      | -     | T0.3                   |                                           |
| T8.5    | Error handling and validation: consistent API error format; frontend toast or inline errors.    | -     | All                    |                                           |
| T8.6    | (Optional) Unit tests for sizing, rebalancing, parser; integration test for one algo run.       | -     | T2.4, T3.1, T3.4, T2.3 |                                           |


---

## Summary by Phase


| Phase | Focus                 | Key deliverables                                                                                              |
| ----- | --------------------- | ------------------------------------------------------------------------------------------------------------- |
| 0     | Setup                 | Repo structure, backend FastAPI skeleton, frontend React skeleton, CORS, env                                 |
| 1     | Config and data       | Algo config, broker client (e.g. Dhan), OHLC, news fetcher                                                   |
| 2     | New portfolio         | Technical + LLM, one algo, sizing, POST /portfolio/run, New Portfolio UI and results table                     |
| 3     | Existing portfolio    | Upload, analyze, feedback, rebalance API and UI (stocks and asset-class)                                       |
| 3B    | Investment-level      | Multi-asset segments, POST /portfolio/investment, allocation view, rebalance by asset class, Deep-dive: Stocks |
| 4     | Explore algos         | GET /algos, GET/POST algo detail, AlgoCard grid, AlgoDetail with StocksTable; all algos wired                 |
| 5     | Learning              | Learning content config, GET cards and card by id, Learning UI                                                |
| 6     | News + LLM            | News in algo pipeline, sentiment (optional)                                                                   |
| 7     | Execution              | place_order integration, dry-run, optional UI                                                                 |
| 8     | Polish                | API docs, READMEs, error handling, optional tests                                                             |


