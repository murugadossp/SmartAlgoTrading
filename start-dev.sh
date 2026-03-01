#!/usr/bin/env bash
# Start both backend and frontend for Smart Algo Trading (run from repo root).
# Press Ctrl+C to stop both.

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

cleanup() {
  echo ""
  echo "Stopping backend (PID $BACKEND_PID) and frontend (PID $FRONTEND_PID)..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM

"$ROOT/start-backend.sh" &
BACKEND_PID=$!

"$ROOT/start-frontend.sh" &
FRONTEND_PID=$!

echo ""
echo "Backend:  http://localhost:8000  (docs: http://localhost:8000/docs)"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both."
echo ""

wait
