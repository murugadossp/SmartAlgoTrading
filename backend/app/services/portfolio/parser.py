"""Parse portfolio CSV (and optionally Excel) to list of holdings: symbol, quantity, avg_cost or value."""
import csv
import io
from typing import Any

# Optional Excel: add openpyxl to requirements if needed
try:
    import openpyxl
    HAS_EXCEL = True
except ImportError:
    HAS_EXCEL = False


def _normalize_header(h: str) -> str:
    return (h or "").strip().lower().replace(" ", "_").replace("-", "_")


def _detect_columns(row: dict[str, str]) -> tuple[str | None, str | None, str | None, str | None]:
    """Return (symbol_key, quantity_key, avg_cost_key, value_key) from first row keys."""
    keys = [k for k in row.keys() if k and row.get(k) is not None]
    sym = qty = cost = val = None
    for k in keys:
        n = _normalize_header(k)
        if n in ("symbol", "symbol_id", "ticker", "stock", "scrip"):
            sym = k
        elif n in ("quantity", "qty", "qty.", "shares", "units"):
            qty = k
        elif n in ("avg_cost", "average_cost", "cost_price", "buy_price", "avg_price"):
            cost = k
        elif n in ("value", "current_value", "market_value", "amount", "price"):
            val = k
    if not sym:
        for k in keys:
            if "symbol" in _normalize_header(k) or "ticker" in _normalize_header(k):
                sym = k
                break
    if not qty:
        for k in keys:
            if "qty" in _normalize_header(k) or "quantity" in _normalize_header(k):
                qty = k
                break
    return (sym, qty, cost, val)


def parse_csv(content: bytes, filename: str = "") -> tuple[list[dict[str, Any]], list[str]]:
    """
    Parse CSV bytes. Returns (holdings, errors).
    Each holding: { symbol, quantity, avg_cost?, value? }.
    """
    holdings: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        text = content.decode("utf-8-sig").strip()
    except UnicodeDecodeError:
        try:
            text = content.decode("latin-1").strip()
        except Exception:
            errors.append("Could not decode file as UTF-8 or Latin-1.")
            return holdings, errors

    if not text:
        errors.append("File is empty.")
        return holdings, errors

    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        errors.append("No data rows found.")
        return holdings, errors

    first = rows[0]
    sym_key, qty_key, cost_key, val_key = _detect_columns(first)
    if not sym_key or not qty_key:
        errors.append("Could not find symbol and quantity columns. Use headers like: symbol, quantity, avg_cost, value")
        return holdings, errors

    for i, row in enumerate(rows):
        sym = (row.get(sym_key) or "").strip()
        qty_str = (row.get(qty_key) or "").strip().replace(",", "")
        if not sym:
            continue
        try:
            qty = int(float(qty_str)) if qty_str else 0
        except ValueError:
            errors.append(f"Row {i + 2}: invalid quantity '{qty_str}' for {sym}")
            continue
        if qty <= 0:
            continue

        cost = None
        if cost_key and row.get(cost_key):
            try:
                cost = round(float(str(row.get(cost_key, "")).replace(",", "")), 2)
            except ValueError:
                pass
        value = None
        if val_key and row.get(val_key):
            try:
                value = round(float(str(row.get(val_key, "")).replace(",", "")), 2)
            except ValueError:
                pass

        holdings.append({
            "symbol": sym,
            "quantity": qty,
            "avg_cost": cost,
            "value": value,
        })

    return holdings, errors


def parse_excel(content: bytes, filename: str = "") -> tuple[list[dict[str, Any]], list[str]]:
    """
    Parse first sheet of .xlsx. Returns (holdings, errors).
    Same holding shape as parse_csv.
    """
    if not HAS_EXCEL:
        return [], ["Excel support requires openpyxl. Install with: pip install openpyxl"]
    holdings: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
        ws = wb.active
        if not ws:
            errors.append("Workbook has no active sheet.")
            return holdings, errors
        rows = list(ws.iter_rows(values_only=True))
        wb.close()
    except Exception as e:
        errors.append(f"Could not read Excel file: {e}")
        return holdings, errors

    if not rows or len(rows) < 2:
        errors.append("No header or data rows in sheet.")
        return holdings, errors

    headers = [str(h or "").strip() for h in rows[0]]
    row_dicts = [dict(zip(headers, [v if v is None else str(v) for v in (row or [])])) for row in rows[1:]]
    first = row_dicts[0] if row_dicts else {}
    sym_key, qty_key, cost_key, val_key = _detect_columns(first)
    if not sym_key or not qty_key:
        errors.append("Could not find symbol and quantity columns in Excel.")
        return holdings, errors

    for i, row in enumerate(row_dicts):
        sym = (row.get(sym_key) or "").strip()
        qty_str = (row.get(qty_key) or "").strip().replace(",", "")
        if not sym:
            continue
        try:
            qty = int(float(qty_str)) if qty_str else 0
        except ValueError:
            errors.append(f"Row {i + 2}: invalid quantity for {sym}")
            continue
        if qty <= 0:
            continue
        cost = None
        if cost_key and row.get(cost_key):
            try:
                cost = round(float(str(row.get(cost_key, "")).replace(",", "")), 2)
            except ValueError:
                pass
        value = None
        if val_key and row.get(val_key):
            try:
                value = round(float(str(row.get(val_key, "")).replace(",", "")), 2)
            except ValueError:
                pass
        holdings.append({"symbol": sym, "quantity": qty, "avg_cost": cost, "value": value})
    return holdings, errors


def parse_portfolio_file(content: bytes, filename: str = "") -> tuple[list[dict[str, Any]], list[str]]:
    """
    Dispatch by extension: .csv -> parse_csv, .xlsx/.xls -> parse_excel.
    Returns (holdings, errors).
    """
    fn = (filename or "").lower()
    if fn.endswith(".csv"):
        return parse_csv(content, filename)
    if fn.endswith(".xlsx") or fn.endswith(".xls"):
        return parse_excel(content, filename)
    return [], ["Unsupported file type. Use .csv or .xlsx"]