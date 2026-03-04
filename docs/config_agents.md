# Config and agents

This document describes how configuration works for the Smart Algo Trading backend: a **single app config file** for broker and agent defaults (including LLM provider/model), plus **per-agent overrides** (including per-agent **provider**). It also gives detailed examples and what to expect at runtime.

---

## 1. Overview

- **One place for non-secret app and agent defaults:** `backend/config/config.yaml` (broker and `agents.default`).
- **Per-agent overrides:** `backend/app/agents/<agent_name>/config.yaml` overrides any key from `agents.default` (e.g. provider, model, temperature, max_tokens).
- **Secrets:** `.env` only (API keys, broker tokens). Never put secrets in YAML.

**Precedence:** `config/config.yaml` (broker, agents.default) → per-agent `agents/<name>/config.yaml` (wins for keys present). When an agent does not set `provider` or `model`, the LLM factory uses Settings, which are filled from `agents.default` and .env.

---

## 2. Config file locations

| Purpose | File | Contents |
|--------|------|----------|
| App + agent defaults | `backend/config/config.yaml` | `broker` and `agents.default` (provider, model, temperature, max_tokens). |
| Per-agent overrides | `backend/app/agents/<name>/config.yaml` | Optional. Overrides and extra params (e.g. suggestion_enum) for that agent. |
| Secrets (no provider/model) | `backend/.env` | OPENAI_API_KEY, ANTHROPIC_API_KEY, DHAN_*, etc. Provider and model are in config only. |
| Other app data | `backend/config/algos.yaml`, `backend/config/symbols.yaml` | Algo metadata, symbol mapping (not agent config). |

There is **no** separate `global_agent_config.yaml`; agent defaults live under `agents.default` in `config/config.yaml`.

---

## 3. Full example: `config/config.yaml`

```yaml
# Global app config (non-secret). Secrets in .env.

broker:
  provider: dhan

# Agent defaults (and app-level LLM default). Every agent gets these unless its own config.yaml overrides.
agents:
  default:
    provider: openai   # openai | anthropic; each agent can override
    model: "gpt-4o-mini"
    temperature: 0.2
    max_tokens: 1024
```

**What you can expect:**

- Broker: dhan. App-level LLM default (used when provider/model are missing): from `agents.default` (OpenAI, gpt-4o-mini).
- All agents (scoring_agent, portfolio_parse_agent, portfolio_research_agent) use provider=openai, model=gpt-4o-mini, temperature=0.2, max_tokens=1024 **unless** their per-agent config overrides.

---

## 4. Per-agent config examples

### 4.1 No override (use defaults)

If an agent has **no** `config.yaml`, or an empty one, it uses `agents.default` from `config/config.yaml`. If `agents.default` is missing a key (e.g. provider), the LLM factory uses Settings (populated from agents.default and .env).

### 4.2 Override model and temperature only

**File:** `backend/app/agents/portfolio_research_agent/config.yaml`

```yaml
model: "gpt-4o"
temperature: 0.3
max_tokens: 4096
```

**What you can expect:** This agent uses **provider=openai** (from agents.default), **model=gpt-4o**, **temperature=0.3**, **max_tokens=4096**. Other agents still use agents.default as-is.

### 4.3 Override provider per agent

**File:** `backend/app/agents/scoring_agent/config.yaml`

```yaml
provider: openai
model: "gpt-4o-mini"
temperature: 0.2
max_tokens: 1024
suggestion_enum: ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
confidence_range: [0, 100]
```

**File:** `backend/app/agents/portfolio_parse_agent/config.yaml`

```yaml
provider: anthropic
model: "claude-3-5-sonnet-20241022"
temperature: 0.1
max_tokens: 2048
```

**What you can expect:** Scoring agent uses OpenAI (gpt-4o-mini); portfolio parse agent uses **Anthropic** (claude-3-5-sonnet). You must set `ANTHROPIC_API_KEY` in `.env` for the parse agent to work. Portfolio research agent still uses `agents.default` (openai, gpt-4o-mini).

### 4.4 Minimal per-agent (only prompt params)

**File:** `backend/app/agents/scoring_agent/config.yaml`

```yaml
# Only prompt-related params; provider, model, temperature, max_tokens from agents.default
suggestion_enum: ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
confidence_range: [0, 100]
```

**What you can expect:** Provider, model, temperature, max_tokens come from `config/config.yaml` → `agents.default`. This agent only adds keys used when building the prompt from the .md template.

---

## 5. Resolution order (effective config)

For a given agent (e.g. `scoring_agent`):

1. **Base:** `config/config.yaml` → `agents.default` (provider, model, temperature, max_tokens).
2. **Override:** `app/agents/scoring_agent/config.yaml` (any key here replaces the base for that key).
3. **Missing provider/model:** If after merge the agent config has no `provider` or no `model`, the LLM factory uses `get_settings().llm_provider` and `get_settings().llm_model` (Settings are populated from `agents.default` in config only).

So: **per-agent config.yaml takes precedence over agents.default** for every key it defines.

---

## 6. .env (secrets only)

- **Required for LLM:** Set the key for the provider you use: `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`.
- **Provider and model** are set in `config/config.yaml` (agents.default) only; do not set `LLM_PROVIDER` or `LLM_MODEL` in .env.

Example `.env`:

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 7. Summary table: what wins

| Key | Source (low → high precedence) |
|-----|---------------------------------|
| broker.provider | config.yaml → broker.provider |
| App-level LLM provider, model (Settings fallback) | config.yaml → agents.default only (not in .env) |
| Agent provider, model, temperature, max_tokens | config.yaml → agents.default, then agents/<name>/config.yaml (per-agent wins). If still missing, Settings (from agents.default). |
| Agent-only params (e.g. suggestion_enum) | agents/<name>/config.yaml only |

---

## 8. References

- Backend config module: `app.config.settings` (`get_settings()`, `get_global_config()`).
- Agent config loading: `app.config.agent_config` (`get_global_agent_config()`, `load_agent_config(agent_name)`, `get_effective_agent_config(agent_name)`). `BaseAgent.load_agent_config(agent_name)` delegates to `agent_config.load_agent_config`.
- Design: [design.md](design.md) §2.2.1 (Config precedence).
