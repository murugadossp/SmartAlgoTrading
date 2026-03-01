# Smart Algo Trading

AI-powered multi-algo trading system for the Indian market using broker/market data provider and LLM. Three main flows: **Portfolio / Investment** (optional investment-level view across asset classes—equity, debt, MF, etc.—with allocation and rebalancing; **stocks deep-dive** for algo run and feedback; or stocks-only: new portfolio or existing portfolio with analysis and rebalancing), **Explore Algos** (filterable Stocks/F&O algo cards with strategy overview and stocks table), and **Learning Cards** (educational content).

## Project structure

```
SmartAlgoTrading/
├── backend/     # FastAPI (Python) — portfolio, algos, learning APIs; broker, LLM, rebalancing
├── frontend/    # React — Portfolio Mode, Explore algos, Learning cards
└── docs/        # Plan, requirements, design, tasks
```

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/plan.md](docs/plan.md) | High-level product and technical plan (investment-level and stocks deep-dive). |
| [docs/requirements.md](docs/requirements.md) | Detailed functional and non-functional requirements. |
| [docs/design.md](docs/design.md) | Technical design: architecture, API contract, backend/frontend structure. |
| [docs/tasks.md](docs/tasks.md) | Phased implementation tasks (including Phase 3B investment-level). |
| [docs/investment-level-plan.md](docs/investment-level-plan.md) | Investment-level portfolio and stocks deep-dive: data model, flows, APIs. |
| [docs/setup.md](docs/setup.md) | Setup and dev environment: Python 3.12, venv path. |
| [docs/testprocess.md](docs/testprocess.md) | Test process: manual and automated testing (backend, frontend, APIs). |

## Setup (backend)

- **Python**: 3.12. Create venv from `backend/`: `python3.12 -m venv .venv`, then activate and `pip install -r requirements.txt`.
- **Activate (macOS/Linux)**: `source backend/.venv/bin/activate` (from repo root: `cd backend` first).
- **Config**: Non-secret options (e.g. broker provider) in `backend/config/config.yaml`; **secrets** (broker tokens, API keys) in `.env` only. See [backend/README.md](backend/README.md#configuration).

Full steps and Windows: [docs/setup.md](docs/setup.md). Env vars and run: [backend/README.md](backend/README.md). To start both backend and frontend: `./start-dev.sh`.

## Quick start

From repo root:

- **Backend only**: `./start-backend.sh` — activates `backend/.venv` and starts the API (http://localhost:8000, docs at http://localhost:8000/docs).
- **Frontend only**: `./start-frontend.sh` — starts the dev server (http://localhost:5173).
- **Both**: `./start-dev.sh` — runs backend and frontend in the same terminal; press Ctrl+C to stop both.

Or run manually: **Backend** — [Setup (backend)](#setup-backend) and [backend/README.md](backend/README.md). **Frontend** — [frontend/README.md](frontend/README.md).

## Configuration (backend)

- **config.yaml** (`backend/config/config.yaml`): Non-secret app and broker options (e.g. `broker.provider`). Safe to commit.
- **.env**: Secrets only—broker credentials, LLM and news API keys. Do not commit; copy from `backend/.env.example`.

## Tech stack

- **Backend**: FastAPI, **Python 3.12**, broker/market data API (e.g. Dhan, `dhanhq`), LLM (OpenAI/Anthropic/local), web search for news.
- **Frontend**: React, React Router.
