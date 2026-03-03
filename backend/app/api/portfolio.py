"""Portfolio API: run, last-run, upload, rebalance."""
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.algos.loader import load_algos_config
from app.algos.momentum import run_momentum
from app.models.requests import PortfolioRunRequest, RebalanceRequest
from app.services.portfolio.analyzer import analyze
from app.services.portfolio.feedback_builder import build_feedback
from app.services.portfolio.parser import file_content_to_text, parse_portfolio_file
from app.services.portfolio.rebalance import rebalance
from app.sizing.position_sizing import apply_sizing_to_results

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

# In-memory cache for last run result (design: optional file/cache)
_last_run: dict[str, Any] | None = None


def _run_algo(algo_id: str) -> list[dict[str, Any]]:
    """Dispatch to algo runner by id. Only momentum implemented for now."""
    if algo_id == "momentum":
        return run_momentum()
    # Stub: other algos return empty until implemented
    return []


@router.post("/run")
def portfolio_run(body: PortfolioRunRequest) -> dict[str, Any]:
    """
    Run selected algos with portfolio amount; apply sizing; return results table.
    algo_ids: if empty or None, run all stock segment algos from config.
    """
    global _last_run
    amount = body.amount
    algo_ids = body.algo_ids
    allocation = body.allocation or {}

    if not algo_ids:
        algos = load_algos_config()
        algo_ids = [a["id"] for a in algos if a.get("segment") == "stocks"]

    # Per-algo amount: from allocation map or equal split
    if allocation and sum(allocation.values()) > 0:
        algo_amounts = {aid: amount * allocation.get(aid, 0.0) for aid in algo_ids}
    else:
        share = amount / len(algo_ids) if algo_ids else 0
        algo_amounts = {aid: share for aid in algo_ids}

    all_results: list[dict[str, Any]] = []
    for algo_id in algo_ids:
        algo_amount = algo_amounts.get(algo_id, 0.0)
        if algo_amount <= 0:
            continue
        rows = _run_algo(algo_id)
        sized = apply_sizing_to_results(rows, algo_amount)
        all_results.extend(sized)

    out = {"results": all_results}
    _last_run = out
    return out


@router.get("/last-run")
def portfolio_last_run() -> dict[str, Any]:
    """Return last run result or 404."""
    if _last_run is None:
        raise HTTPException(status_code=404, detail="No portfolio run yet.")
    return _last_run


@router.post("/parse")
async def portfolio_parse(file: UploadFile = File(...)) -> dict[str, Any]:
    """
    Parse-only endpoint for testing: upload a file and get holdings + errors without running analyze/feedback.
    Uses same logic as upload (LLM parse if available, else rule-based). Returns source so you can verify which parser ran.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")
    content = await file.read()
    content_text = file_content_to_text(content, file.filename)
    holdings: list[dict[str, Any]] = []
    errors: list[str] = []
    source = "rule_based"
    if content_text:
        try:
            from app.agents.portfolio_parse_agent.agent import run_portfolio_parse
            result = run_portfolio_parse(content_text, file.filename)
            if result and result.holdings:
                holdings = [h.model_dump() for h in result.holdings]
                errors = list(result.errors or [])
                source = "llm"
        except Exception:
            pass
    if not holdings:
        holdings, errors = parse_portfolio_file(content, file.filename)
    return {
        "holdings": holdings,
        "errors": errors,
        "source": source,
        "holding_count": len(holdings),
    }


@router.post("/upload")
async def portfolio_upload(file: UploadFile = File(...)) -> dict[str, Any]:
    """
    Upload portfolio file (CSV or Excel). Parse (LLM if available, else rule-based) -> analyze -> feedback.
    Returns total_value, holdings (with value/weight), feedback (summary, suggestions, analysis_html?), sector_mix, concentration.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")
    content = await file.read()
    content_text = file_content_to_text(content, file.filename)
    holdings: list[dict[str, Any]] = []
    errors: list[str] = []
    if content_text:
        try:
            from app.agents.portfolio_parse_agent.agent import run_portfolio_parse
            result = run_portfolio_parse(content_text, file.filename)
            if result and result.holdings:
                holdings = [h.model_dump() for h in result.holdings]
                errors = list(result.errors or [])
        except Exception:
            pass
    if not holdings:
        holdings, errors = parse_portfolio_file(content, file.filename)
    if errors and not holdings:
        raise HTTPException(status_code=422, detail={"message": "Parse errors", "errors": errors})
    if not holdings:
        raise HTTPException(status_code=422, detail="No valid holdings found in file. Use columns: symbol, quantity, optionally avg_cost or value.")

    analysis = analyze(holdings)
    feedback = build_feedback(analysis)

    return {
        "total_value": analysis["total_value"],
        "holdings": analysis.get("holdings", []),
        "feedback": {
            "summary": feedback["summary"],
            "suggestions": feedback["suggestions"],
            "analysis_html": feedback.get("analysis_html"),
        },
        "sector_mix": analysis.get("sector_mix", []),
        "concentration": analysis.get("concentration", {}),
        "holding_count": analysis.get("holding_count", 0),
    }


def _holding_value(h: dict[str, Any]) -> float:
    if h.get("value") is not None:
        return float(h["value"])
    qty = int(h.get("quantity") or 0)
    c = h.get("avg_cost")
    return (qty * float(c)) if c is not None else 0.0


@router.post("/rebalance")
def portfolio_rebalance(body: RebalanceRequest) -> dict[str, Any]:
    """
    Rebalance: input holdings + optional target_allocation (symbol -> weight).
    Returns current_weights, target_weights, trades (symbol, action, quantity, amount).
    """
    holdings = [h.model_dump() for h in body.holdings]
    total_value = sum(_holding_value(h) for h in holdings)
    if total_value <= 0:
        raise HTTPException(status_code=422, detail="Total portfolio value must be positive.")
    target = body.target_allocation
    if target is not None:
        target = {k: float(v) for k, v in target.items()}
    result = rebalance(
        holdings=holdings,
        total_value=total_value,
        target_allocation=target or {},
        strategy=body.strategy or "full",
        band_pct=body.band_pct or 0.05,
    )
    return result
