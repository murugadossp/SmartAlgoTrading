"""Smart Algo Trading — FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings

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


@app.get("/health")
def health():
    """Health check for load balancers and monitoring."""
    return {"status": "ok", "service": "smart-algo-trading-api"}
