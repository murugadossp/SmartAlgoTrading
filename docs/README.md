# Documentation

This folder contains the project documentation derived from the product plan.

| Document | Description |
|----------|-------------|
| [plan.md](plan.md) | High-level plan: three flows (Portfolio/Investment, Explore algos, Learning cards), investment-level and stocks deep-dive, algos, stack, structure. |
| [requirements.md](requirements.md) | Detailed functional and non-functional requirements (investment-level R0.x, Flow 1–3, algos, data, execution, NFRs). |
| [design.md](design.md) | Technical design: architecture, backend (FastAPI) and frontend (React) structure, API contract, data models, rebalancing (asset-class and stock-level). |
| [tasks.md](tasks.md) | Phased implementation tasks (Phase 0–8, Phase 3B investment-level) with task IDs, dependencies, and notes. |
| [investment-level-plan.md](investment-level-plan.md) | Investment-level portfolio and stocks deep-dive: data model, flows, APIs, open choices. |
| [llm-portfolio-dashboard.md](llm-portfolio-dashboard.md) | LLM portfolio analysis: equity-research-style HTML dashboard, API shape, frontend rendering. |
| [setup.md](setup.md) | **Setup and dev environment**: Python 3.12, virtual env at `backend/.venv`. |
| [testprocess.md](testprocess.md) | **Test process**: manual and automated testing (backend, frontend, APIs, E2E). |
| [modern-ui-theme-plan.md](modern-ui-theme-plan.md) | Frontend UI plan: theme (light/dark), card-based layout, header, typography. |

## Project layout

- **backend/** — FastAPI application (Python 3.12; venv at `backend/.venv`).
- **frontend/** — React application.
- **docs/** — Plan, requirements, design, tasks, setup (this folder).
