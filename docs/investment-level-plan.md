# Investment-level portfolio and stocks deep-dive

This document describes the expansion from a stock-only view to an **investment-level** view (asset classes: equity, debt, mutual funds, etc.) with a **stocks deep-dive** for algo runs and suggestions.

## Goal

- **Investment (high-level)**: User provides portfolio **across asset classes** — e.g. Mutual funds, bonds, direct equity, gold, cash.
- **High-level view**: System shows allocation by asset class (e.g. Equity 50%, Debt 30%, MF 20%).
- **Deep-dive into stocks**: For the **equity / direct stocks** slice, existing flows apply — run algos, sizing, Explore algos, rebalancing within equity.

## Data model (investment-level)

- **Portfolio (investment)** = list of **segments** (asset classes), each with:
  - `asset_class`: e.g. `equity`, `debt`, `mutual_fund`, `gold`, `cash` (fixed list for v1).
  - `value` (₹) and/or `holdings`: for equity, holdings = stock list (symbol, quantity, value); for MF/bonds, name/identifier + value or units.
- **Upload**: Option A — single file with `asset_class` (or `type`) column; Option B — user enters amounts per asset class + optional separate stocks file for equity slice.
- **Target allocation**: At **asset-class** level (e.g. equity 60%, debt 40%). Rebalancing output: current vs target by asset class; suggested moves; for equity slice, optional stock-level trades.

## Flows (evolved)

- **Flow 1 — Portfolio / Investment**:
  - **Entry**: Portfolio landing with two paths:
    - **Investment (multi-asset)**: Enter or upload multi-asset portfolio → view **allocation by asset class** → rebalance (target by asset class) → optional **Deep-dive: Equity (stocks)** (run algos / existing portfolio feedback on equity slice).
    - **Stocks only**: Same as today — amount or upload stocks → run algos / feedback / rebalance within equity.
  - **Deep-dive: Stocks**: From investment view, user opens equity slice → New portfolio (amount = equity value) or Existing portfolio (stocks in that slice).
- **Flow 2 — Explore algos**: Unchanged; conceptually for the equity slice.
- **Flow 3 — Learning**: Unchanged.

## Backend (minimal)

- **Investment portfolio API**: Accept multi-asset input (asset_class + value/holdings); return total value, allocation by asset_class, optional feedback.
- **Rebalancing**: Extend `target_allocation` to **asset-class** level; output current vs target by asset_class, high-level trades; keep stock-level rebalance for equity when holdings provided.
- **Existing** `POST /portfolio/run` and sizing: unchanged; amount can be “equity slice” from investment view.

## Open choices

- **Upload format**: Single file with `asset_class` column vs amounts-by-asset-class + optional stocks file.
- **Asset classes**: Fixed list (equity, debt, mutual_fund, gold, cash) for v1.
- **MF/Bonds**: v1 value-only (no NAV/units fetch); optional later.

See [plan.md](plan.md), [requirements.md](requirements.md), [design.md](design.md), and [tasks.md](tasks.md) for the full doc set and task breakdown.
