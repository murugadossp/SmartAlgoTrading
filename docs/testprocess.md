# Test Process

Manual and automated testing procedures for the Smart Algo Trading project. Use this for QA, regression, and CI.

---

## 1. Prerequisites

- **Backend**: Python 3.12, `backend/.venv` created and dependencies installed (`pip install -r backend/requirements.txt`). Optional: copy `backend/.env.example` to `backend/.env` and set broker/LLM keys for full integration.
- **Frontend**: Node 18+, `frontend/node_modules` installed (`npm install` in `frontend/`).
- **Environment**: Backend runs on `http://localhost:8000`, frontend on `http://localhost:5173` (Vite default). API base URL for frontend: `VITE_API_URL` (defaults to backend origin when proxied).

---

## 2. Manual Test Procedures

### 2.1 Backend health and startup

| Step | Action | Expected |
|------|--------|----------|
| 1 | From repo root run `./start-backend.sh` (or `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`) | Server starts; no import errors. |
| 2 | Open `http://localhost:8000/health` in browser or `curl http://localhost:8000/health` | HTTP 200, body e.g. `{"status":"ok"}`. |
| 3 | Open `http://localhost:8000/docs` | Swagger UI loads; endpoints listed (e.g. `/portfolio/run`, `/portfolio/upload`, `/portfolio/rebalance`, `/algos`). |

### 2.2 Configuration and env

| Step | Action | Expected |
|------|--------|----------|
| 1 | Ensure `backend/config/config.yaml` exists with `broker.provider` (e.g. `dhan`). | File present; no crash on app load. |
| 2 | Run backend without `.env` (or with minimal .env). | App starts; broker/LLM calls may fail at use-time but health and config load. |
| 3 | If using Dhan/LLM: set `DHAN_ACCESS_TOKEN`, `DHAN_CLIENT_ID`; for LLM set `OPENAI_API_KEY` (when `llm.provider: openai`) or `ANTHROPIC_API_KEY` (when `llm.provider: anthropic`) in `backend/.env`. | Portfolio run and market data (if used) succeed when endpoints are called. |
| 4 | **LLM portfolio report**: Set the API key for the configured provider (`OPENAI_API_KEY` for OpenAI, `ANTHROPIC_API_KEY` for Anthropic) in `backend/.env` to enable the portfolio research agent. | After upload, `feedback.analysis_html` is populated with LLM-generated dashboard HTML. If key is missing, upload still returns 200 with `feedback.analysis_html` null. |

### 2.3 Portfolio APIs (no broker/LLM required for upload/rebalance)

| Step | Action | Expected |
|------|--------|----------|
| 1 | **POST /portfolio/upload** — Send multipart file with CSV: `symbol,quantity,value` (e.g. RELIANCE,10,25000 and TCS,5,17500). | 200; response has `total_value`, `holdings`, `feedback` (summary, suggestions, optional `analysis_html`), `sector_mix`, `concentration`. When the configured LLM provider API key is set (OpenAI or Anthropic), `feedback.analysis_html` contains dashboard HTML; otherwise it is null. |
| 2 | **POST /portfolio/upload** — Send Excel (`.xlsx`) with same columns. | Same as above. |
| 3 | **POST /portfolio/rebalance** — Body: `{ "holdings": [ {"symbol":"RELIANCE","quantity":10,"value":25000}, {"symbol":"TCS","quantity":5,"value":17500} ], "strategy": "full" }`. | 200; `current_weights`, `target_weights` (equal weight if no target_allocation), `trades` array with symbol, action (buy/sell), amount, quantity. |
| 4 | **POST /portfolio/rebalance** — Same holdings, `"strategy": "bands", "band_pct": 0.05`. | 200; trades only where drift > 5% (or empty if within bands). |
| 5 | **POST /portfolio/run** — Body: `{ "amount": 100000, "algo_ids": ["momentum"] }`. | 200 if broker/LLM configured; otherwise may fail with missing credentials. Response: `results` array with symbol, suggestion, confidence, suggested_quantity/amount. |
| 6 | **GET /portfolio/last-run** — After a successful run. | 200; same shape as last POST /portfolio/run response. |

#### 2.3.1 LLM portfolio dashboard (analysis_html)

| Step | Action | Expected |
|------|--------|----------|
| 1 | **Without** LLM API key (no `OPENAI_API_KEY` when provider is openai, or no `ANTHROPIC_API_KEY` when provider is anthropic): POST /portfolio/upload with valid CSV/Excel. | 200; `feedback.analysis_html` is null; `feedback.summary` and `feedback.suggestions` present. |
| 2 | **With** the configured provider key set in `backend/.env` (e.g. `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` per `config.yaml` llm.provider): POST /portfolio/upload with valid file (e.g. 2–5 holdings). | 200; `feedback.analysis_html` is a non-empty string (HTML fragment). |
| 3 | In the frontend, Existing portfolio → upload same file with API key set. | A **Report** section appears below suggestions; dashboard HTML renders inside the scrollable container (no script execution; DOMPurify sanitization applied). |

### 2.4 Algos APIs

| Step | Action | Expected |
|------|--------|----------|
| 1 | **GET /algos** — No query or `?segment=stocks`. | 200; `algos` array with id, name, segment, short_description. |
| 2 | **GET /algos?segment=fno** | 200; only F&O algos (e.g. Option selling). |
| 3 | **GET /algos/momentum** | 200; overview (goal, inputs, signals, risk), stocks array (from cache or empty). |
| 4 | **POST /algos/momentum/refresh** | 200; updated stocks array; GET /algos/momentum returns same until next refresh. |

### 2.5 Frontend startup and navigation

| Step | Action | Expected |
|------|--------|----------|
| 1 | From repo root run `./start-frontend.sh` (or `cd frontend && npm run dev`). | Dev server starts; no build errors. |
| 2 | Open `http://localhost:5173`. | Landing page loads; theme toggle (light/dark); sidebar with Portfolio, Explore Algos, Learning. |
| 3 | Collapse/expand sidebar (icon top-right of sidebar). | Sidebar collapses to icons only; state persists after refresh if using localStorage. |
| 4 | Click **Portfolio**. | Navigate to Portfolio/Investment landing: options "Investment (multi-asset)" and "Stocks only". |
| 5 | Click **Stocks only** → **New portfolio**. | Form: amount, algo multi-select; Run → calls POST /portfolio/run; results table shows symbol, suggestion, confidence, quantity/amount (if run succeeds). |
| 6 | Click **Stocks only** → **Existing portfolio**. | Upload CSV/Excel; after upload, Analysis feedback (total value, summary, suggestions, sector mix, holdings table). If backend has the configured LLM provider API key set, a **Report** section appears with LLM-generated dashboard HTML (sanitized). Rebalance section: strategy (Full/Bands), band %; "Get rebalance" → current vs target table and suggested trades. |
| 7 | Click **Explore Algos**. | Algo cards; filter Stocks/F&O; click card → algo detail (overview + stocks table; optional Refresh). |
| 8 | Profile menu (top-right): Settings, Profile, Preferences. | Dropdown opens; links navigate (placeholder pages ok). |

### 2.6 Theme and layout

| Step | Action | Expected |
|------|--------|----------|
| 1 | Toggle theme to dark. | Dark theme (blue-tinted); no FOUC on reload (data-theme in localStorage). |
| 2 | Toggle to light. | Light theme applied. |
| 3 | Resize window. | Layout remains usable; sidebar and content responsive. |

---

## 3. Automated Testing (optional)

### 3.1 Backend

- **Health**: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health` should return `200`.
- **Unit-style checks** (run with backend venv active):
  - Rebalance logic: call `rebalance(holdings, total_value, target_allocation, strategy, band_pct)` from `app.services.portfolio.rebalance` with known inputs; assert `current_weights`, `target_weights`, `trades` shape and values.
  - Parser: call `parse_csv` / `parse_excel` from `app.services.portfolio.parser` with sample files; assert holdings list and no errors.
  - Analyzer: call `analyze(holdings)` from `app.services.portfolio.analyzer`; assert `total_value`, `sector_mix`, `holdings` with `value` and `weight_pct`.
  - Feedback builder: call `build_feedback(analysis)` from `app.services.portfolio.feedback_builder`; assert response has `summary`, `suggestions`, and `analysis_html` (null when no LLM API key for configured provider; optional assertion that `run_portfolio_research(analysis)` returns None when key is unset).
- **API tests**: Use FastAPI `TestClient`; requires `httpx` (`pip install httpx`). Example: `client.post("/portfolio/rebalance", json={...})` and assert status 200 and response keys.

### 3.2 Frontend

- **Build**: `cd frontend && npm run build` — must complete without errors.
- **Lint**: If ESLint is configured, `npm run lint` (or `npx eslint src`).
- **E2E**: If Playwright/Cypress is added, run against `http://localhost:5173` with backend at `http://localhost:8000`; cover login-less flows (Portfolio upload, Rebalance, Explore Algos).

### 3.3 CI suggestions

- Job 1: Install backend deps, run health check (or a single `TestClient` test).
- Job 2: Install frontend deps, `npm run build`.
- Optional: Run backend unit tests (rebalance, parser, analyzer) in isolation; no live broker/LLM.

---

## 4. Test Data

### 4.1 Sample CSV (portfolio upload)

```csv
symbol,quantity,avg_cost,value
RELIANCE,10,2500,25000
TCS,5,3500,17500
INFY,20,1500,30000
```

### 4.2 Sample rebalance request body

```json
{
  "holdings": [
    { "symbol": "RELIANCE", "quantity": 10, "value": 25000 },
    { "symbol": "TCS", "quantity": 5, "value": 17500 }
  ],
  "strategy": "full"
}
```

Expected: `current_weights` ~58.8% / 41.2%, `target_weights` 50% / 50%, `trades` with one sell (RELIANCE) and one buy (TCS).

---

## 5. Troubleshooting

| Issue | Check |
|-------|--------|
| Backend import errors | Ensure you are in `backend/` with `.venv` activated and `pip install -r requirements.txt` was run. |
| CORS errors from frontend | Backend must allow origin of frontend (e.g. `http://localhost:5173`); see `app.main` CORS middleware. |
| 422 on upload | Ensure CSV/Excel has headers (e.g. symbol, quantity); optional: avg_cost, value. |
| 422 on rebalance | Body must include `holdings` array; each item: `symbol`, `quantity`, and either `value` or `avg_cost`. |
| Empty algo results | Broker credentials and (for scoring) OpenAI API key must be set; check `config/algos.yaml` watchlist and `config/symbols.yaml` for symbol→security_id mapping (Dhan). |
| No Report / analysis_html after upload | Set the LLM provider API key in `backend/.env` (`OPENAI_API_KEY` for OpenAI or `ANTHROPIC_API_KEY` for Anthropic, per `config.yaml` llm.provider). Ensure `backend/app/agents/portfolio_research_agent/` exists (system_instructions.md, config.yaml). Frontend sanitizes HTML with DOMPurify; if Report is empty, check browser console for errors. |

---

## 6. Reference

- **API contract**: [design.md](design.md) §2.3.
- **Setup**: [setup.md](setup.md).
- **Tasks and implementation status**: [tasks.md](tasks.md).
