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
- LLM: **AGNO** (Agno) framework, vendor-agnostic (OpenAI, Anthropic); config via `config/config.yaml` (agents.default: provider, model) and env (OPENAI_API_KEY, ANTHROPIC_API_KEY); structured output via Pydantic
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

**Split:** Non-secret options live in **`backend/config/config.yaml`** (broker, llm, and **agent defaults** under `agents.default`). Secrets live in **`.env`** only.

- **config.yaml**: `broker` and `agents.default` (provider, model, temperature, max_tokens). Per-agent overrides in `app/agents/<name>/config.yaml`. See `backend/config/config.yaml` and `docs/config_agents.md`.
- **.env**: `DHAN_ACCESS_TOKEN`, `DHAN_CLIENT_ID`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc. See `.env.example`.
- **CONFIG_PATH** (optional): Override path to config directory or file; default is `backend/config/config.yaml`.

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or from repo root: `./start-dev.sh` to start both backend and frontend.

API docs: `http://localhost:8000/docs`

## Tests

From `backend/` with the venv activated:

- **Run all tests**: `pytest -v` or `pytest tests/ -v` (if any tests exist under `tests/`).
- **Parser agent (direct)**: From `backend/` run `./tests/test_run.sh parser_agent` (activates venv and runs the test), or run `python tests/test_parser_agent.py`. From repo root: `./backend/tests/test_run.sh parser_agent`. The script logs to `tests/output/parser_agent_io_<timestamp>.txt`. Run `./tests/test_run.sh` with no args to see options.

See `docs/testprocess.md` for details.

## Docs

See `../docs/` for plan, requirements, design, and tasks.
