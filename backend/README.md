# Smart Algo Trading — Backend

FastAPI backend for the Smart Algo Trading system (Indian market, Dhan API, AI/LLM).

## Responsibilities

- **Portfolio Mode**: Run algos with sizing (`POST /portfolio/run`), upload and analyze portfolio (`POST /portfolio/upload`), rebalance using traditional methods (`POST /portfolio/rebalance`).
- **Explore Algos**: List algos by segment (`GET /algos`), algo detail with overview and stocks table (`GET /algos/{id}`), refresh (`POST /algos/{id}/refresh`).
- **Learning**: List learning cards (`GET /learning/cards`), card detail (`GET /learning/cards/{id}`).

## Tech Stack

- **Python 3.14**
- FastAPI
- Dhan: `dhanhq` client (market data, optional orders)
- LLM: OpenAI / Anthropic / local (structured JSON output)
- News: Web search API (e.g. Serper, Google, Bing)
- **Package manager**: **uv** (create venv and install all Python packages)

## Setup

**Python**: 3.11+ recommended (3.14 when Pydantic/FastAPI support it). Use a venv.

**Option A — Local venv (recommended for now):**

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Option B — uv + external venv** (see [../docs/setup.md](../docs/setup.md)):

- Venv path: `/Users/murugadosssp/py_venv/SmartAlgoTrading` (Python 3.14 when ecosystem is ready)
- From backend: `uv pip install -r requirements.txt` (with that venv activated)

On Windows, activate with: `.\Users\murugadosssp\py_venv\SmartAlgoTrading\Scripts\activate` (adjust path as needed).

**Use uv for all Python package operations** (add/remove/install): e.g. `uv pip install <package>`, `uv pip install -r requirements.txt`.

## Environment

Set (e.g. in `.env` or shell):

- `DHAN_ACCESS_TOKEN`, `DHAN_CLIENT_ID`: Dhan API credentials
- `OPENAI_API_KEY` or equivalent: LLM API key
- News search API key (if used)
- Optional: `CONFIG_PATH` for YAML config

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`

## Docs

See `../docs/` for plan, requirements, design, and tasks.
