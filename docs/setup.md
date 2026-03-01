# Setup and development environment

This document records the project’s Python version, virtual environment location, and use of **uv** or standard **venv** for Python tooling.

---

## Python version

- **Python 3.12** (stable). Use 3.12.x for the backend. Install via your system package manager, [pyenv](https://github.com/pyenv/pyenv), or **uv** (see below).

---

## Virtual environment (single)

The project uses **one** virtual environment: `backend/.venv`. Create it from the `backend/` directory. Do not use a second venv elsewhere.

---

## Backend: step-by-step setup

**1. Ensure Python 3.12 is installed**

```bash
python3.12 --version
```

If needed, install via Homebrew (`brew install python@3.12`), pyenv (`pyenv install 3.12`), or uv (`uv python install 3.12`).

**2. Create the project virtual environment (from repo root)**

```bash
cd backend
python3.12 -m venv .venv
```

**3. Activate the venv**

- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**  
  `.venv\Scripts\activate`

**4. Install backend dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the backend**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the root-level script: from repo root, `./start-dev.sh` (starts backend and frontend).

---

## Optional: uv for Python operations

- **uv** can be used instead of pip/venv for faster installs:
  - Install uv: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
  - Create venv: `uv venv backend/.venv --python 3.12`
  - Install deps: `cd backend && uv pip install -r requirements.txt`

---

## Summary

| Detail | Value |
|--------|--------|
| Python | 3.12 |
| Venv path | `backend/.venv` |
| Backend deps | `backend/requirements.txt`; install with `pip install -r requirements.txt` |

**Configuration split:** Non-secret options (e.g. broker provider) in `backend/config/config.yaml`; secrets (broker tokens, LLM/news API keys) in `.env` only. See [backend/README.md](../backend/README.md#configuration) and root [README.md](../README.md#configuration-backend).

**Testing:** See [testprocess.md](testprocess.md) for manual and automated test procedures.
