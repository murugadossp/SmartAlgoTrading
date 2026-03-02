# Smart Algo Trading — Backend

FastAPI backend for the Smart Algo Trading system (Indian market, broker/market data and AI/LLM).

## Responsibilities

- **Portfolio Mode**: Run algos with sizing (`POST /portfolio/run`), upload and analyze portfolio (`POST /portfolio/upload`), rebalance using traditional methods (`POST /portfolio/rebalance`).
- **Explore Algos**: List algos by segment (`GET /algos`), algo detail with overview and stocks table (`GET /algos/{id}`), refresh (`POST /algos/{id}/refresh`).
- **Learning**: List learning cards (`GET /learning/cards`), card detail (`GET /learning/cards/{id}`).

## Tech Stack

- **Python 3.12**
- FastAPI
- Broker/market data: first implementation Dhan (`dhanhq` client) for market data and optional orders
- LLM: **AGNO** (Agno) framework, vendor-agnostic (OpenAI, Anthropic); config via `config/config.yaml` (llm.provider, llm.default_model) and env (OPENAI_API_KEY, ANTHROPIC_API_KEY); structured output via Pydantic
- News: Web search API (e.g. Serper, Google, Bing)

## Setup

**Python 3.12** and a virtual env are required.

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Optional: use **uv** to create the venv and install deps: `uv venv .venv --python 3.12` then `uv pip install -r requirements.txt`.

## Configuration

**Split:** Non-secret options (e.g. broker provider, timeouts) live in **`backend/config/config.yaml`**. Secrets (API keys, broker tokens) live in **`.env`** only and must not be committed.

- **config.yaml**: `broker.provider` (e.g. `dhan`), optional per-provider options. See `backend/config/config.yaml`.
- **.env**: `DHAN_ACCESS_TOKEN`, `DHAN_CLIENT_ID`, `OPENAI_API_KEY`, `SERPER_API_KEY`, etc. See `.env.example`.
- **CONFIG_PATH** (optional): Override path to config directory or file; default is `backend/config/config.yaml`.

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or from repo root: `./start-dev.sh` to start both backend and frontend.

API docs: `http://localhost:8000/docs`

## Docs

See `../docs/` for plan, requirements, design, and tasks.
