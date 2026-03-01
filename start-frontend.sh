#!/usr/bin/env bash
# Start the Smart Algo Trading frontend (run from repo root).

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -d frontend/node_modules ]; then
  echo "Frontend deps not installed. Run: cd frontend && npm install"
  exit 1
fi

echo "Starting frontend on http://localhost:5173 ..."
cd frontend
exec npm run dev
