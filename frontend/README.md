# Smart Algo Trading — Frontend

React application for the Smart Algo Trading system (Indian market, Dhan API, AI/LLM).

## Flows

- **Portfolio Mode** (Flow 1): New portfolio (amount + run algos + results) or Existing portfolio (upload → analysis & feedback → rebalancing view).
- **Explore Algos** (Flow 2): Filter by Stocks / F&O, algo cards, detail view with strategy overview and stocks table.
- **Learning Cards** (Flow 3): Browse learning content by category, card detail view.

## Tech Stack

- React (with hooks)
- React Router
- Build: Vite or Create React App
- HTTP client to backend API (env-configurable base URL)

## Setup

```bash
npm install
```

## Environment

Create `.env` (see `.env.example` if provided) with:

- `VITE_API_URL` or `REACT_APP_API_URL`: Backend base URL (e.g. `http://localhost:8000`)

## Run

```bash
npm run dev
# or
npm start
```

## Docs

See `../docs/` for plan, requirements, design, and tasks.
