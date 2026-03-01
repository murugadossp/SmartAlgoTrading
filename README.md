# Smart Algo Trading

AI-powered multi-algo trading system for the Indian market using Dhan API and LLM. Three main flows: **Portfolio Mode** (new portfolio or existing portfolio with analysis and traditional rebalancing), **Explore Algos** (filterable Stocks/F&O algo cards with strategy overview and stocks table), and **Learning Cards** (educational content).

## Project structure

```
SmartAlgoTrading/
├── backend/     # FastAPI (Python) — portfolio, algos, learning APIs; Dhan, LLM, rebalancing
├── frontend/    # React — Portfolio Mode, Explore algos, Learning cards
└── docs/        # Plan, requirements, design, tasks
```

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/plan.md](docs/plan.md) | High-level product and technical plan. |
| [docs/requirements.md](docs/requirements.md) | Detailed functional and non-functional requirements. |
| [docs/design.md](docs/design.md) | Technical design: architecture, API contract, backend/frontend structure. |
| [docs/tasks.md](docs/tasks.md) | Phased implementation tasks. |
| [docs/setup.md](docs/setup.md) | Setup and dev environment: Python 3.14, venv path, uv. |

## Setup (backend)

- **Python**: 3.14 (install via **uv**: `uv python install 3.14`).
- **Virtual env**: `/Users/murugadosssp/py_venv/SmartAlgoTrading` (by project name under `py_venv`). Create with: `uv venv /Users/murugadosssp/py_venv/SmartAlgoTrading --python 3.14`.
- **Packages**: Use **uv** for all Python installs. Activate the venv, then from `backend/`: `uv pip install -r requirements.txt`.
- **Activate (macOS/Linux)**: `source /Users/murugadosssp/py_venv/SmartAlgoTrading/bin/activate`.

Full steps and Windows: [docs/setup.md](docs/setup.md). Env vars and run: [backend/README.md](backend/README.md).

## Quick start

- **Backend**: Follow [Setup (backend)](#setup-backend) above; env vars and run: [backend/README.md](backend/README.md).
- **Frontend**: [frontend/README.md](frontend/README.md).

## Tech stack

- **Backend**: FastAPI, **Python 3.14**, **uv** (venv + all package installs), Dhan API (`dhanhq`), LLM (OpenAI/Anthropic/local), web search for news.
- **Frontend**: React, React Router.
