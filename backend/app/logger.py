"""App logging: file under backend/logs/<date>/<session_id>/ and optional console.
Structure: logs/YYYY-MM-DD/<session_id>/app.log and agent_traces.json.
Session_id: from env LOG_SESSION_ID (e.g. "test" when running tests), else generated once at first use.
User and session_id in log lines/traces from set_log_context() (e.g. middleware).
"""
from __future__ import annotations

import contextvars
import json
import logging
import os
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

_trace_lock = threading.Lock()

# Backend root (parent of app/)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
# logs/<date>/<session_id>/; session_id = LOG_SESSION_ID env (e.g. "test") or generated UUID
_LOG_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
_PROCESS_SESSION_ID = (os.environ.get("LOG_SESSION_ID") or "").strip() or str(uuid.uuid4())
_LOGS_DIR = _BACKEND_ROOT / "logs" / _LOG_DATE / _PROCESS_SESSION_ID
_LOG_FILE = _LOGS_DIR / "app.log"
_AGENT_TRACES_FILE = _LOGS_DIR / "agent_traces.json"

# Request-scoped user and session (set by middleware); default user when not logged in
_current_user: contextvars.ContextVar[str] = contextvars.ContextVar("log_user", default="default")
_current_session_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("log_session_id", default=None)

_configured: set[str] = set()


def _ensure_logs_dir() -> None:
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)


def set_log_context(user: str = "default", session_id: str | None = None) -> None:
    """Set request-scoped user and session_id for logs and traces. Call from middleware (user='default' if not logged in)."""
    _current_user.set(user)
    _current_session_id.set(session_id)


def get_log_context() -> tuple[str, str | None]:
    """Return (user, session_id) from context. User is 'default' when not set."""
    return _current_user.get(), _current_session_id.get()


def get_app_start_timestamp() -> str:
    """Return the process session_id used for the current log directory (logs/<date>/<session_id>/)."""
    return _PROCESS_SESSION_ID


def get_log_dir_info() -> tuple[str, str]:
    """Return (date, session_id) for the current log directory. Date is YYYY-MM-DD."""
    return _LOG_DATE, _PROCESS_SESSION_ID


class _UserSessionFilter(logging.Filter):
    """Inject user and session_id from context into LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.user = _current_user.get()
        record.session_id = _current_session_id.get() or ""
        return True


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Return a logger with the given name. On first use, adds a file handler to
    backend/logs/<date>/<session_id>/app.log and a stream handler to stderr.
    Log lines include user and session_id from context (set_log_context).
    """
    logger = logging.getLogger(name)
    if logger.level == logging.NOTSET:
        logger.setLevel(level)

    if name in _configured:
        return logger

    _ensure_logs_dir()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | user=%(user)s session=%(session_id)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        fh.addFilter(_UserSessionFilter())
        logger.addHandler(fh)
    except OSError:
        pass

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        ch.addFilter(_UserSessionFilter())
        logger.addHandler(ch)

    _configured.add(name)
    return logger


def append_agent_trace(payload: dict) -> None:
    """
    Append one trace object to the JSON array in
    backend/logs/<date>/<session_id>/agent_traces.json.
    File is a single JSON array: [ {...}, {...}, ... ], one element per agent invocation.
    Adds user and session_id from context (default user='default').
    Each element: start_time, end_time, duration, user, session_id, agent_name, model_config, input, output.
    Non-JSON-serializable values are coerced with default=str.
    """
    _ensure_logs_dir()
    user, session_id = get_log_context()
    full = {"user": user, "session_id": session_id, **payload}
    with _trace_lock:
        try:
            traces: list = []
            if _AGENT_TRACES_FILE.exists():
                with open(_AGENT_TRACES_FILE, encoding="utf-8") as f:
                    raw = f.read().strip()
                    if raw:
                        try:
                            traces = json.loads(raw)
                            if not isinstance(traces, list):
                                traces = [traces]
                        except json.JSONDecodeError:
                            # Migrate from JSONL (one object per line) to array
                            for line in raw.split("\n"):
                                line = line.strip()
                                if line:
                                    try:
                                        traces.append(json.loads(line))
                                    except json.JSONDecodeError:
                                        pass
            traces.append(full)
            with open(_AGENT_TRACES_FILE, "w", encoding="utf-8") as f:
                json.dump(traces, f, ensure_ascii=False, default=str, indent=2)
        except OSError:
            pass


def update_agent_trace_by_id(trace_id: str, updates: dict) -> None:
    """
    Update the trace entry with the given trace_id with the keys from updates
    (e.g. output, end_time, duration). Used after agent returns to complete the trace.
    """
    with _trace_lock:
        try:
            if not _AGENT_TRACES_FILE.exists():
                return
            with open(_AGENT_TRACES_FILE, encoding="utf-8") as f:
                raw = f.read().strip()
            if not raw:
                return
            try:
                traces = json.loads(raw)
            except json.JSONDecodeError:
                return
            if not isinstance(traces, list):
                return
            for i in range(len(traces) - 1, -1, -1):
                if traces[i].get("trace_id") == trace_id:
                    for k, v in updates.items():
                        traces[i][k] = v
                    break
            else:
                return
            with open(_AGENT_TRACES_FILE, "w", encoding="utf-8") as f:
                json.dump(traces, f, ensure_ascii=False, default=str, indent=2)
        except OSError:
            pass


def trace_timestamp() -> str:
    """ISO 8601 UTC timestamp for trace records."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
