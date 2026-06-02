#!/usr/bin/env python3
"""OpenAI-compatible /v1/chat/completions proxy backed by the `claude -p` CLI.

Lets any OpenAI-SDK client (e.g. the Kaimen-Inc Co-Scientist reimplementation)
run on Claude via the Claude Code CLI — no Anthropic/OpenAI API key needed, it
reuses your local `claude` auth.

How tool/function calling is served:
  The framework's agents emit structured output as *tool calls* (record_hypothesis,
  record_review, ...). When a request carries `tools`, we ask `claude -p` for that
  tool's argument object via `--json-schema` (Claude Code's structured-output mode)
  and return it as an OpenAI `tool_calls` response. Plain requests return assistant
  text. Run the framework with external web tools OFF so the only tools are these
  structured-output "recording" tools.

Usage:
    python claude_p_proxy.py [port]          # default 8088
Then point the framework at  http://127.0.0.1:<port>/v1  with
    [llm] provider = "openai_compatible"
    [llm.openai] base_url = "http://127.0.0.1:8088/v1"
    OPENAI_API_KEY=dummy   (ignored, but the SDK wants something)

stdlib only — no pip deps.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEFAULT_MODEL = "sonnet"
CLAUDE_TIMEOUT_S = 240

# Run `claude -p` from an isolated empty dir so it does NOT pick up the host
# project's CLAUDE.md / settings / Stop hooks (which would contaminate output).
ISOLATED_CWD = tempfile.mkdtemp(prefix="claude-p-proxy-")


def run_claude(prompt: str, model: str, schema: dict | None = None) -> dict:
    """Invoke `claude -p` and return the parsed JSON envelope."""
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--model", model]
    if schema is not None:
        cmd += ["--json-schema", json.dumps(schema)]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=CLAUDE_TIMEOUT_S, cwd=ISOLATED_CWD
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude -p rc={proc.returncode}: {proc.stderr[:500]}")
    return json.loads(proc.stdout)


def flatten_messages(messages: list[dict]) -> str:
    parts = []
    for m in messages:
        content = m.get("content")
        if isinstance(content, list):  # content blocks
            text = " ".join(
                b.get("text", "") if isinstance(b, dict) else str(b) for b in content
            )
        else:
            text = content if isinstance(content, str) else json.dumps(content)
        parts.append(f"[{m.get('role','user')}]\n{text}")
    return "\n\n".join(parts)


def pick_tool(tools: list[dict], tool_choice) -> tuple[str, dict]:
    """Choose which function to fill: the one forced by tool_choice, else the first."""
    funcs = {
        t["function"]["name"]: t["function"].get("parameters", {})
        for t in tools
        if t.get("type") == "function"
    }
    if isinstance(tool_choice, dict):
        name = tool_choice.get("function", {}).get("name")
        if name in funcs:
            return name, funcs[name]
    name = next(iter(funcs))
    return name, funcs[name]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, obj: dict, code: int = 200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/v1/models"):
            self._send({"object": "list", "data": [
                {"id": m, "object": "model"} for m in ("haiku", "sonnet", "opus")
            ]})
        else:
            self._send({"status": "ok"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        if not self.path.startswith("/v1/chat/completions"):
            self._send({"error": "not found"}, 404)
            return

        model = body.get("model") or DEFAULT_MODEL
        prompt = flatten_messages(body.get("messages", []))
        tools = body.get("tools")
        tool_choice = body.get("tool_choice")

        try:
            if tools and tool_choice != "none":
                name, schema = pick_tool(tools, tool_choice)
                out = run_claude(
                    prompt + f"\n\n[instruction]\nReturn the arguments for function "
                             f"`{name}` as JSON matching the schema.",
                    model, schema=schema,
                )
                args = out.get("structured_output")
                if args is None:
                    try:
                        args = json.loads(out.get("result", "{}"))
                    except Exception:
                        args = {}
                message = {
                    "role": "assistant", "content": None,
                    "tool_calls": [{
                        "id": "call_" + uuid.uuid4().hex[:8], "type": "function",
                        "function": {"name": name, "arguments": json.dumps(args)},
                    }],
                }
                finish = "tool_calls"
            else:
                out = run_claude(prompt, model)
                message = {"role": "assistant", "content": out.get("result", "")}
                finish = "stop"

            u = out.get("usage", {}) or {}
            inp = int(u.get("input_tokens", 0) or 0)
            outp = int(u.get("output_tokens", 0) or 0)
            self._send({
                "id": "chatcmpl-" + uuid.uuid4().hex[:12],
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [{"index": 0, "message": message, "finish_reason": finish}],
                "usage": {"prompt_tokens": inp, "completion_tokens": outp,
                          "total_tokens": inp + outp},
            })
        except Exception as e:  # noqa: BLE001
            self._send({"error": {"message": str(e), "type": "proxy_error"}}, 500)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8088
    print(f"claude-p proxy listening on http://127.0.0.1:{port}/v1", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
