#!/usr/bin/env python3
"""Local Seed runtime CLI backed by Ollama-compatible intent classification."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from seed_runtime.context import ContextComposer
from seed_runtime.decisions import DecisionValidator
from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.ids import new_id
from seed_runtime.intent_classifier import (
    IntentDecisionModel,
    IntentPromptModelClient,
    TextIntentClassifier,
)
from seed_runtime.models import Event
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime import Runtime
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import ToolNeedService

DEFAULT_ENDPOINT = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_WORKSPACE = "local"
DEFAULT_SESSION = "local"


@dataclass
class LocalSeedApp:
    """Container for a locally configured Seed runtime and its event ledger."""

    runtime: Runtime
    ledger: EventLedger
    projector: StateProjector
    context_composer: ContextComposer
    model_client: IntentPromptModelClient
    workspace_id: str = DEFAULT_WORKSPACE
    session_id: str = DEFAULT_SESSION

    def run(self, text: str) -> dict[str, Any]:
        response = self.runtime.handle_user_message(
            self.workspace_id, self.session_id, text
        )
        return {
            "response": to_plain(response),
            "events": [
                to_plain(event) for event in self.ledger.list(self.workspace_id)
            ],
        }

    def raw(self, text: str) -> str:
        input_event = Event(
            id=new_id("evt"),
            kind="input.user_message",
            workspace_id=self.workspace_id,
            actor="user",
            payload={"text": text},
            session_id=self.session_id,
        )
        state = self.projector.project(self.workspace_id)
        context = self.context_composer.compose(
            self.workspace_id, self.session_id, input_event, state
        )
        return self.model_client.complete(context)


def build_local_app(
    *,
    endpoint: str = DEFAULT_ENDPOINT,
    model: str = DEFAULT_MODEL,
    timeout_seconds: float = 30.0,
    workspace_id: str = DEFAULT_WORKSPACE,
    session_id: str = DEFAULT_SESSION,
    max_decision_retries: int = 1,
) -> LocalSeedApp:
    """Construct a local Seed runtime using the current intent-classifier path."""

    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest(REPO_ROOT / "toolkits/core/echo/toolkit.yaml")
    projector = StateProjector(ledger)
    context_composer = ContextComposer(registry)
    model_client = IntentPromptModelClient.for_endpoint(
        endpoint,
        timeout_seconds=timeout_seconds,
        extra_payload={"model": model, "stream": False, "format": "json"},
    )
    classifier = TextIntentClassifier(model_client)
    model = IntentDecisionModel(classifier)
    runtime = Runtime(
        ledger,
        projector,
        context_composer,
        DecisionValidator(registry),
        ToolExecutor(ledger, registry, projector),
        ToolNeedService(ledger, projector),
        model,
        max_decision_retries=max_decision_retries,
    )
    return LocalSeedApp(
        runtime=runtime,
        ledger=ledger,
        projector=projector,
        context_composer=context_composer,
        model_client=model_client,
        workspace_id=workspace_id,
        session_id=session_id,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Seed locally with Ollama /api/generate intent classification."
    )
    parser.add_argument("message", nargs="*", help="message to send in one-shot mode")
    parser.add_argument(
        "--http", action="store_true", help="serve a small local HTTP API"
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="HTTP bind host when using --http"
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="HTTP bind port when using --http"
    )
    parser.add_argument(
        "--events", action="store_true", help="include the full event ledger"
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="print raw model output before running the normal runtime",
    )
    parser.add_argument(
        "--raw-only",
        action="store_true",
        help="print raw model output and exit without running the runtime",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name")
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help="Ollama-compatible generate endpoint",
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0, help="model request timeout in seconds"
    )
    parser.add_argument("--workspace", default=DEFAULT_WORKSPACE, help="workspace id")
    parser.add_argument("--session", default=DEFAULT_SESSION, help="session id")
    return parser


def format_response_summary(result: dict[str, Any]) -> str:
    response = result.get("response", {})
    if not isinstance(response, dict):
        return str(response)

    message = str(response.get("message") or "").strip()
    payload = (
        response.get("payload") if isinstance(response.get("payload"), dict) else {}
    )
    output = payload.get("output")

    lines = []
    if message:
        lines.append(message)
    else:
        lines.append(str(response.get("kind") or "response"))
    if output is not None:
        lines.append("Output: " + json.dumps(output, sort_keys=True))
    return "\n".join(lines)


def format_cli_output(
    result: dict[str, Any],
    *,
    include_events: bool = False,
    raw_output: str | None = None,
) -> str:
    sections: list[str] = []
    if raw_output is not None:
        sections.extend(["Raw model output:", raw_output])
    sections.append(format_response_summary(result))
    if include_events:
        sections.extend(
            [
                "Events:",
                json.dumps(result.get("events", []), indent=2, sort_keys=True),
            ]
        )
    return "\n".join(sections)


def run_http(app: LocalSeedApp, host: str, port: int) -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
            if self.path != "/health":
                self._write_json(404, {"error": "not found"})
                return
            self._write_json(200, {"ok": True})

        def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
            if self.path not in {"/", "/message"}:
                self._write_json(404, {"error": "not found"})
                return
            try:
                payload = self._read_json()
                text = payload.get("message", payload.get("text"))
                if not isinstance(text, str) or not text.strip():
                    raise ValueError("POST JSON requires non-empty 'message' or 'text'")
                result = app.raw(text) if payload.get("raw") else app.run(text)
                if isinstance(result, str):
                    self._write_json(200, {"response": result, "events": []})
                else:
                    self._write_json(200, result)
            except Exception as exc:  # keep local dev server dependency-light
                self._write_json(500, {"error": str(exc)})

        def log_message(self, format: str, *args: object) -> None:
            return

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("request body must be a JSON object")
            return data

        def _write_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Seed local HTTP server listening on http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Seed local HTTP server.", file=sys.stderr)
    finally:
        server.server_close()


def run_shell(
    app: LocalSeedApp,
    *,
    raw: bool = False,
    raw_only: bool = False,
    events: bool = False,
) -> None:
    print("Seed local shell. Press Ctrl-D or type 'exit' to quit.", file=sys.stderr)
    while True:
        try:
            text = input("seed> ").strip()
        except EOFError:
            print(file=sys.stderr)
            return
        if text in {"exit", "quit"}:
            return
        if not text:
            continue
        if raw_only:
            print(app.raw(text))
            continue
        raw_output = app.raw(text) if raw else None
        print(
            format_cli_output(
                app.run(text), include_events=events, raw_output=raw_output
            )
        )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    app = build_local_app(
        endpoint=args.endpoint,
        model=args.model,
        timeout_seconds=args.timeout,
        workspace_id=args.workspace,
        session_id=args.session,
    )
    if args.http:
        run_http(app, args.host, args.port)
        return 0

    message = " ".join(args.message).strip()
    if message:
        if args.raw_only:
            print(app.raw(message))
            return 0
        raw_output = app.raw(message) if args.raw else None
        print(
            format_cli_output(
                app.run(message), include_events=args.events, raw_output=raw_output
            )
        )
        return 0

    run_shell(app, raw=args.raw, raw_only=args.raw_only, events=args.events)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
