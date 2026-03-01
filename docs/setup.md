# Setup and development environment

This document records the project’s Python version, virtual environment location, and use of **uv** for all Python tooling.

---

## Python version

- **Python 3.14** (e.g. 3.14.0 or 3.14.x). Install and manage via **uv** (see below).

---

## Virtual environment location

The backend virtual environment is **outside** the repo, in a shared directory, **named by project**:

| Item        | Value |
|------------|--------|
| **Base path** | `/Users/murugadosssp/py_venv` |
| **Project venv** | `/Users/murugadosssp/py_venv/SmartAlgoTrading` |
| **Python** | 3.14 |

So the project’s venv is **`/Users/murugadosssp/py_venv/SmartAlgoTrading`** (one folder per project under `py_venv`).

---

## uv for all Python operations

- **uv** is used for:
  - Installing a specific Python version (e.g. 3.14)
  - Creating the project virtual environment
  - Installing, adding, and removing Python packages (no `pip` or `venv` for these)
- Install uv: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) (e.g. `curl -LsSf https://astral.sh/uv/install.sh | sh` or `pip install uv`).

---

## Backend: step-by-step setup

**1. Install Python 3.14 (via uv)**

```bash
uv python install 3.14
```

**2. Create the project virtual environment**

```bash
uv venv /Users/murugadosssp/py_venv/SmartAlgoTrading --python 3.14
```

**3. Activate the venv**

- **macOS / Linux:**
  ```bash
  source /Users/murugadosssp/py_venv/SmartAlgoTrading/bin/activate
  ```
- **Windows:**  
  `.\Users\murugadosssp\py_venv\SmartAlgoTrading\Scripts\activate` (adjust drive/path if needed).

**4. Install backend dependencies (from repo root or `backend/`)**

```bash
cd backend
uv pip install -r requirements.txt
```

**5. Run the backend (after app exists)**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Adding or changing Python packages

- **Always use uv** so the project venv and lock behavior stay consistent:
  - Install a package: `uv pip install <package>`
  - Install from requirements: `uv pip install -r requirements.txt`
  - After adding a dependency, update `backend/requirements.txt` so others can reproduce the env.

---

## Summary

| Detail | Value |
|--------|--------|
| Python | 3.14 |
| Venv path | `/Users/murugadosssp/py_venv/SmartAlgoTrading` |
| Package / env tool | **uv** (venv creation, `uv pip install`, etc.) |
| Backend deps | `backend/requirements.txt`; install with `uv pip install -r requirements.txt` |

See also [backend/README.md](../backend/README.md) for env vars (Dhan, LLM, news API keys) and run instructions.
