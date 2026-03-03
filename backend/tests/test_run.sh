#!/usr/bin/env bash
# Run tests from backend/tests/. Activates backend venv and runs the chosen test.
# Usage: ./test_run.sh [option]   (run from backend/ or repo root)
#   parser_agent   - run portfolio parse agent direct test (writes to tests/output/parser_agent_io_<timestamp>.txt)
#   (no option)    - print usage

set -e
TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_ROOT="$(cd "$TESTS_DIR/.." && pwd)"
cd "$BACKEND_ROOT"

if [ ! -f .venv/bin/activate ]; then
  echo "Backend venv not found. Run: cd backend && python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

source .venv/bin/activate

case "${1:-}" in
  parser_agent)
    echo "Running parser agent direct test ..."
    exec python tests/test_parser_agent.py
    ;;
  "")
    echo "Usage: ./tests/test_run.sh <option>   (from backend/)"
    echo "   or: ./backend/tests/test_run.sh <option>   (from repo root)"
    echo ""
    echo "Options:"
    echo "  parser_agent   Run portfolio parse agent direct test (output: tests/output/parser_agent_io_<timestamp>.txt)"
    exit 0
    ;;
  *)
    echo "Unknown option: $1"
    echo "Run ./tests/test_run.sh with no arguments to see options."
    exit 1
    ;;
esac
