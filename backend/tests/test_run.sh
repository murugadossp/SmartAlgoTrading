#!/usr/bin/env bash
# Run tests from backend/tests/. Activates backend venv and runs the chosen test.
# Usage: ./test_run.sh [option]   (run from backend/ or repo root)
#   parser_agent   - run portfolio parse agent direct test (writes to tests/output/parser_agent_io_<timestamp>.txt)
#   (no option)    - print usage
# Logs each step with timestamp and total duration.

set -e

log() {
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] [test_run] $*"
}

TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_ROOT="$(cd "$TESTS_DIR/.." && pwd)"
cd "$BACKEND_ROOT"

log "Step 1: Resolving backend root -> $BACKEND_ROOT"

if [ ! -f .venv/bin/activate ]; then
  log "ERROR: Backend venv not found. Run: cd backend && python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

log "Step 2: Activating venv ..."
source .venv/bin/activate

# Use session_id "test" for log dir: logs/<date>/test/
export LOG_SESSION_ID=test
log "Step 3: LOG_SESSION_ID=test (logs -> logs/<date>/test/)"

case "${1:-}" in
  parser_agent)
    log "Step 4: Running parser agent direct test (LLM call may take 30-60s) ..."
    _start=$(date +%s)
    python tests/test_parser_agent.py
    _end=$(date +%s)
    _dur=$((_end - _start))
    log "Step 5: Done. Total duration: ${_dur}s"
    ;;
  "")
    log "Usage: ./tests/test_run.sh <option>   (from backend/)"
    log "   or: ./backend/tests/test_run.sh <option>   (from repo root)"
    log ""
    log "Options:"
    log "  parser_agent   Run portfolio parse agent direct test (output: tests/output/parser_agent_io_<timestamp>.txt)"
    exit 0
    ;;
  *)
    log "Unknown option: $1"
    log "Run ./tests/test_run.sh with no arguments to see options."
    exit 1
    ;;
esac
