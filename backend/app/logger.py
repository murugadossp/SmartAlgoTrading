"""App logging: file under backend/logs/ and optional console. Use get_logger(name) for module loggers."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

# Backend root (parent of app/)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_LOGS_DIR = _BACKEND_ROOT / "logs"
_LOG_FILE = _LOGS_DIR / "app.log"

_configured: set[str] = set()


def _ensure_logs_dir() -> None:
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Return a logger with the given name. On first use, adds a file handler to backend/logs/app.log
    and a stream handler to stderr. Subsequent calls reuse the same handlers.
    """
    logger = logging.getLogger(name)
    if logger.level == logging.NOTSET:
        logger.setLevel(level)

    if name in _configured:
        return logger

    _ensure_logs_dir()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except OSError:
        pass

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    _configured.add(name)
    return logger
