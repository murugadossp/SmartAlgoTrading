---
name: Investment-level and stocks deep-dive
overview: Add an investment-level layer so users can provide or view portfolio across asset classes (Mutual funds, bonds, equity, etc.), see high-level allocation, then deep-dive into the equity/stocks slice for algo runs and suggestions—without removing current stock-focused flows.
todos: []
isProject: false
---

# Investment-level portfolio and stocks deep-dive

## Your idea (summary)

Instead of limiting the product to "stocks only," support:

1. **Investment (high-level)**: User gives portfolio **across asset classes** — e.g. Mutual funds, bonds, direct equity, gold, etc.
2. **High-level view**: System shows allocation by asset class (e.g. Equity 50%, Debt 30%, MF 20%).
3. **Deep-dive into stocks**: For the **equity / direct stocks** slice, the existing flows apply — run algos, sizing, explore algos, rebalancing within equity. So "stocks" become one part of a broader investment view.

---

## View and benefits

- **More realistic**: Many users hold MF, bonds, and equity; a single "investment" view matches how they think.
- **Rebalancing**: Already specified as "e.g. 60% equity / 40% debt" in [docs/requirements.md](requirements.md) and [docs/design.md](design.md). An investment-level model makes that explicit: current vs target by asset class, then trades (including at asset-class level: "increase equity", "reduce debt").
- **Stocks stay central**: Algo run, sizing, and Explore algos apply to the **equity (direct stocks)** slice. User can choose "equity amount" or "direct stocks value" for algo sizing; the rest of the portfolio is context for allocation and rebalancing.
- **No big bang**: Current flows (New portfolio amount → run algos, Existing portfolio upload → feedback/rebalance) can stay; we add an optional **Investment** entry point that can feed into them (e.g. "Equity slice" → run algos on that slice).

---

## Proposed shape (minimal)

**1. Data model (investment-level)**

- **Portfolio (investment)** = list of **segments** (asset classes), each with:
  - `asset_class`: e.g. `equity`, `debt`, `mutual_fund`, `gold`, `cash` (configurable list).
  - `value` (₹) and/or `holdings`: for equity, holdings can be the existing stock list (symbol, quantity, value); for MF/bonds, name/identifier + value or units.
- **Upload**: Support at least one of:
  - **Option A**: One file with an `asset_class` (or `type`) column: rows can be stocks (symbol, quantity), MF (scheme name/ISIN, units or value), bonds (name, value), etc.
  - **Option B**: User enters **amounts per asset class** (e.g. Equity ₹5L, Debt ₹3L, MF ₹2L) and optionally uploads a **separate** stocks file for the equity slice (for analysis and algo run).
- **Target allocation**: Already in scope; store and use at **asset-class** level (e.g. equity 60%, debt 40%). Rebalancing output: current vs target by asset class; suggested moves (e.g. "add ₹X to equity", "reduce debt by ₹Y") and, for the equity slice, optional stock-level trades (from existing rebalance logic).

**2. Flows**

- **Flow 1 — Portfolio / Investment** (evolved):
  - **Entry**: "Investment" or "Portfolio" landing with two paths:
    - **High-level (investment)**: Enter or upload **multi-asset** portfolio → view **allocation by asset class** → optional **rebalance** (target by asset class) → optional **deep-dive: Equity (stocks)**.
    - **Stocks deep-dive**: From investment view, user clicks "Equity" or "Direct stocks" → existing **New portfolio** (amount = equity slice or direct-stocks value, run algos) or **Existing portfolio** (upload/select stocks in that slice → feedback + rebalance within equity). So current "Portfolio Mode" becomes the **stocks slice** of the investment view.
- **Flow 2 — Explore algos**: Unchanged; still filter Stocks / F&O, algo cards, stocks table. Conceptually "for the equity slice."
- **Flow 3 — Learning**: Unchanged.

**3. Backend**

- **New or extended APIs** (to be detailed in requirements/design):
  - **Investment portfolio**: e.g. `POST /portfolio/investment` or `POST /portfolio/upload` extended to accept multi-asset (asset_class + value/holdings). Response: total value, allocation by asset_class, optional feedback.
  - **Rebalancing**: Already has target_allocation; extend so `target_allocation` can be **asset-class** (equity %, debt %, etc.). Input: current portfolio (multi-asset); output: current vs target by asset class, list of trades (asset-class level and, for equity, stock-level if holdings provided).
- **Existing**: `POST /portfolio/run` (algo run) and sizing continue to use an **amount** and optional allocation; that amount can be "equity slice" or "direct stocks value" from the investment view. No need to change algo run API for a first version.

**4. Frontend**

- **Investment / Portfolio** landing: Choose "Investment (multi-asset)" vs "Stocks only (direct equity)."
- **Investment path**: Input or upload multi-asset → **Allocation view** (e.g. pie or table by asset class) → **Rebalance** (target by asset class) → link **"Deep-dive: Stocks"** that opens existing New portfolio (with pre-filled amount = equity value) or Existing portfolio (stocks in that slice).
- **Stocks-only path**: Same as today (amount or upload stocks → run algos / feedback / rebalance within equity).

---

## What stays as-is (for now)

- **Explore algos**: No change; still Stocks / F&O, algo cards, stocks table.
- **Learning**: No change.
- **Algo run and sizing**: Still take an amount (e.g. equity slice); broker and market data remain stock/F&O focused. MF/bond data (e.g. NAV) can be out of scope for v1 and added later if needed.
- **Existing portfolio upload**: Current CSV/Excel (stocks) remains; we **add** (or extend) support for multi-asset so one upload can include asset_class and non-stock rows.

---

## Implementation order (suggested)

1. **Extend data model and APIs** for "investment portfolio": asset_class, value/holdings per segment; upload format (Option A or B); response with allocation by asset_class.
2. **Rebalancing**: Extend to asset-class target_allocation; output current vs target by asset_class and high-level trades (e.g. "move ₹X from debt to equity"); keep existing stock-level rebalance for equity slice when holdings are provided.
3. **Frontend**: Investment/Portfolio entry (high-level vs stocks-only); allocation view; rebalance by asset class; "Deep-dive: Stocks" linking to existing New/Existing portfolio flows with equity amount or selected stocks.
4. **Docs**: Update [docs/plan.md](plan.md), [docs/requirements.md](requirements.md), and [docs/design.md](design.md) to describe investment-level, asset classes, and stocks deep-dive; add tasks in [docs/tasks.md](tasks.md).

---

## Open choices (to decide before coding)

- **Upload format**: Single file with `asset_class` column (and different columns per type) vs separate flows (amounts by asset class + optional stocks file). Single file is more flexible; separate flows are simpler to implement first.
- **Asset classes**: Fixed list (e.g. equity, debt, mutual_fund, gold, cash) vs configurable. Fixed is enough for v1.
- **MF/Bonds**: For v1, treat as "value only" (no NAV/units fetch) or support units + optional NAV lookup later. Value-only keeps scope smaller.

This keeps the current "stocks only" path intact while adding the option to work at investment level (MF, bonds, etc.) and then deep-dive into stocks for algo suggestions and rebalancing.
