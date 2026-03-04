"""App logging: file under backend/logs/<app_start_timestamp>/ and optional console.
User and session_id from context (default user="default"); set via set_log_context() (e.g. in middleware).
Agent traces: append_agent_trace(payload) writes one JSON object per line to logs/.../agent_traces.json.
"""
from __future__ import annotations

import contextvars
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# Backend root (parent of app/)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
# One directory per app/process start: logs/2026-03-04_011500Z/
_APP_START_TS = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%SZ")
_LOGS_DIR = _BACKEND_ROOT / "logs" / _APP_START_TS
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
    """Return the app start timestamp used for the current log directory name."""
    return _APP_START_TS


class _UserSessionFilter(logging.Filter):
    """Inject user and session_id from context into LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.user = _current_user.get()
        record.session_id = _current_session_id.get() or ""
        return True


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Return a logger with the given name. On first use, adds a file handler to
    backend/logs/<app_start_timestamp>/app.log and a stream handler to stderr.
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
    Append one JSON-serializable trace object as a single line to
    backend/logs/<app_start_timestamp>/agent_traces.json.
    Adds user and session_id from context (default user='default').
    Each line: timestamp, agent_name, user, session_id, model_config, input, output.
    Non-JSON-serializable values are coerced with default=str.
    """
    _ensure_logs_dir()
    user, session_id = get_log_context()
    full = {"user": user, "session_id": session_id, **payload}
    try:
        line = json.dumps(full, ensure_ascii=False, default=str) + "\n"
        with open(_AGENT_TRACES_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass


def trace_timestamp() -> str:
    """ISO 8601 UTC timestamp for trace records."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
