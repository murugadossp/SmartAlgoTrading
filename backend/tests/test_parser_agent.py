"""
Simple direct test for the portfolio parse agent: call the agent (no HTTP), log system instruction,
user message, and structured agent output to tests/output/parser_agent_io_<timestamp>.txt.
Output conforms to PortfolioParseResult (AGNO + Pydantic). Run from backend/: python tests/test_parser_agent.py
Logs go to backend/logs/<date>/test/ when LOG_SESSION_ID=test (set by test_run.sh or below).
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Use session_id "test" for log dir when running this script (logs/<date>/test/)
os.environ.setdefault("LOG_SESSION_ID", "test")

# Ensure backend app is importable when run as script
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.agents.base_agent import BaseAgent
from app.agents.portfolio_parse_agent.agent import run_portfolio_parse

AGENT_NAME = "portfolio_parse_agent"
OUTPUT_DIR = BACKEND_ROOT / "tests" / "output"
GROWW_SAMPLE = BACKEND_ROOT / "tests" / "data" / "groww_Stocks_Holdings_Statement.xlsx"

SIMPLE_CSV = "symbol,quantity\nRELIANCE,10"


def main() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_file = OUTPUT_DIR / f"parser_agent_io_{timestamp}.txt"
    lines: list[str] = []

    def log(msg: str = "") -> None:
        lines.append(msg)

    # Load system instruction (same as agent uses)
    try:
        system_instructions, _ = BaseAgent.load_agent_config(AGENT_NAME)
    except FileNotFoundError as e:
        log(f"Error: {e}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(lines), encoding="utf-8")
        print("Report written to", output_file)
        return

    log("========== System instruction (sent to agent) ==========")
    log(system_instructions.strip())
    log("")

    # Run 1: Simple CSV
    log("========== Run 1: Simple CSV ==========")
    log("--- User message (sent to agent) ---")
    log(SIMPLE_CSV)
    log("")
    t0 = time.perf_counter()
    try:
        result1 = run_portfolio_parse(SIMPLE_CSV, "")
    except Exception as e:
        result1 = None
        log("--- Agent output (structured JSON, PortfolioParseResult / AGNO + Pydantic) ---")
        log(f"Agent raised an error: {e}")
        log("")
    else:
        log("--- Agent output (structured JSON, PortfolioParseResult / AGNO + Pydantic) ---")
        if result1 is not None:
            log(result1.model_dump_json(indent=2))
        else:
            log("Agent returned None (check API key and config).")
        log("")
    d1 = round(time.perf_counter() - t0, 2)
    log(f"[Run 1 duration: {d1}s]")
    log("")

    # Run 2: Groww statement (if file exists)
    if GROWW_SAMPLE.exists():
        from app.services.portfolio.parser import file_content_to_text

        with open(GROWW_SAMPLE, "rb") as f:
            groww_bytes = f.read()
        content_text = file_content_to_text(groww_bytes, GROWW_SAMPLE.name)
        log("========== Run 2: Groww statement ==========")
        log("--- User message (sent to agent) ---")
        log(f"Filename: {GROWW_SAMPLE.name}\n")
        log((content_text or "(empty)").strip())
        log("")
        t1 = time.perf_counter()
        try:
            result2 = run_portfolio_parse(content_text or "", GROWW_SAMPLE.name)
        except Exception as e:
            log("--- Agent output (structured JSON, PortfolioParseResult / AGNO + Pydantic) ---")
            log(f"Agent raised an error: {e}")
        else:
            log("--- Agent output (structured JSON, PortfolioParseResult / AGNO + Pydantic) ---")
            if result2 is not None:
                log(result2.model_dump_json(indent=2))
            else:
                log("Agent returned None (check API key and config).")
        d2 = round(time.perf_counter() - t1, 2)
        log(f"[Run 2 duration: {d2}s]")
    else:
        log("(Groww sample not found at tests/data/groww_Stocks_Holdings_Statement.xlsx; skipping Run 2)")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")
    print("Report written to:", output_file)
    if GROWW_SAMPLE.exists():
        print("Durations: Run 1 (CSV) and Run 2 (Groww) are logged in the report; check backend/logs/<date>/test/app.log for agent.run() timing.")


if __name__ == "__main__":
    main()
