#!/usr/bin/env bash
# Start the Smart Algo Trading backend (run from repo root).
# Activates backend venv and runs uvicorn.

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -f backend/.venv/bin/activate ]; then
  echo "Backend venv not found. Run: cd backend && python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

echo "Activating backend environment and starting server on http://localhost:8000 ..."
cd backend
source .venv/bin/activate
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
