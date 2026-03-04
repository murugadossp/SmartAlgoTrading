"""Smart Algo Trading — FastAPI application."""
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.api import portfolio, algos
from app.logger import set_log_context

app = FastAPI(
    title=get_settings().api_title,
    version=get_settings().api_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_context_middleware(request: Request, call_next):
    """Set user and session_id for logs and traces. User='default' if not logged in; session from header or new."""
    user = request.headers.get("X-User-Id") or request.headers.get("X-User") or "default"
    session_id = request.headers.get("X-Session-Id") or str(uuid.uuid4())
    set_log_context(user=user, session_id=session_id)
    response = await call_next(request)
    return response

app.include_router(portfolio.router)
app.include_router(algos.router)


@app.get("/health")
def health():
    """Health check for load balancers and monitoring."""
    return {"status": "ok", "service": "smart-algo-trading-api"}
