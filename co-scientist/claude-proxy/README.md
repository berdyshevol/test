# `claude -p` → OpenAI-compatible proxy

Run **any OpenAI-SDK client on Claude via the Claude Code CLI** — no Anthropic/OpenAI
API key, it reuses your local `claude` auth. Built so the open-source
[Co-Scientist reimplementation](https://github.com/Kaimen-Inc/Co-Scientist) can run on
Claude for an engine-vs-engine comparison with our Claude Code build.

## What it does
- Serves `POST /v1/chat/completions` (+ `GET /v1/models`).
- Plain requests → `claude -p --output-format json`, returns assistant text.
- Requests with `tools` → asks `claude -p --json-schema <tool schema>` for that function's
  arguments (Claude Code structured-output mode) and returns an OpenAI `tool_calls` response
  with `finish_reason:"tool_calls"`. The framework's agents emit their output as such
  "recording" tool calls, so this is what makes them work.
- Reports real token `usage` from the `claude -p` envelope.
- Runs `claude -p` from an **isolated temp cwd** so it does NOT inherit the host repo's
  `CLAUDE.md` / settings / Stop hooks (which otherwise contaminate output).

## Run
```bash
python3 claude_p_proxy.py 8088      # http://127.0.0.1:8088/v1
```

## Point the Co-Scientist reimplementation at it
```toml
[llm]
provider = "openai_compatible"
[llm.openai]
base_url = "http://127.0.0.1:8088/v1"
[models]
generation = "opus"
reflection = "haiku"
ranking_pairwise = "sonnet"
metareview_final = "opus"
```
Set `OPENAI_API_KEY=dummy` (the SDK requires a value; the proxy ignores it). Run the
framework with **external web tools OFF** so the only tools are the structured-output
recording tools this proxy serves.

## Caveats
- **Cost:** each `claude -p` call is a fresh subprocess that rebuilds prompt cache (~$0.04+
  per call here). A full co-scientist run is dozens of calls → a few dollars.
- **Latency:** ~3–10s per call (subprocess + structured output).
- **Structured-output quality:** depends on the schema being precise; vague schemas let the
  model over-stuff fields. The framework's real schemas are tight, which helps.
- **No live web grounding** in this mode (web tools off) — fine for an architecture
  comparison; add a tool-dispatch path later if you want grounded runs.
- Smoke-tested standalone (plain + tool-call paths). End-to-end run against the framework is
  the next step.
