import importlib.util
import sqlite3
import sys
from pathlib import Path

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.models import PolicyDecision
from seed_runtime.registry import ToolRegistry
from seed_runtime.runtime_loop import (
    Decision,
    EchoTool,
    FakeDecisionProvider,
    RuntimeInput,
    RuntimeLoop,
)

SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DenyPolicy:
    def __init__(self):
        self.calls = 0

    def evaluate(self, tool, state, *, scope=None):
        self.calls += 1
        return PolicyDecision(
            outcome="block",
            action=tool.policy_action,
            reason="blocked in cli test",
            risk_class=tool.risk_class,
        )


class ExplodingProvider:
    def decide(self, context):  # pragma: no cover - must not be called by CLI trace
        raise AssertionError("trace command must not call provider")


class ExplodingPolicy:
    def evaluate(self, tool, state, *, scope=None):  # pragma: no cover
        raise AssertionError("trace command must not call policy")


class ExplodingTool:
    def execute(self, context, arguments):  # pragma: no cover
        raise AssertionError("trace command must not execute tools")


def run_loop_into_db(db_path, decision, *, policy_engine=None, tool_handlers=None):
    ledger = SQLiteEventLedger(str(db_path))
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    runtime = RuntimeLoop(
        ledger,
        None,
        registry,
        policy_engine,
        FakeDecisionProvider(decision),
        tool_handlers or {},
    )
    result = runtime.run(RuntimeInput("local", "echo hi" if getattr(decision, "kind", None) == "call_tool" else "hi"))
    before_count = len(ledger.list_events("local"))
    ledger.close()
    return result, before_count


def persisted_event_count(db_path):
    connection = sqlite3.connect(str(db_path))
    try:
        return connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    finally:
        connection.close()


def test_trace_run_prints_answer_run(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    result, _ = run_loop_into_db(db_path, Decision(kind="answer", text="done", reason="direct"))

    assert seed_local.main(["--db", str(db_path), "--trace-run", result.run_id]) == 0

    output = capsys.readouterr().out
    assert "Runtime Trace" in output
    assert "workspace: local" in output
    assert f"run: {result.run_id}" in output
    assert "Input: hi" in output
    assert "kind: answer" in output
    assert "reason: direct" in output
    assert "context_hash: " in output
    assert "allowed: true" in output
    assert "tool: none" in output
    assert "outcome: answered" in output
    assert "response: done" in output
    assert "error: none" in output
    assert "input.user_message" in output
    assert "assistant.answer" in output
    assert "decision.recorded" in output


def test_trace_run_prints_successful_tool_run(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    result, _ = run_loop_into_db(
        db_path,
        Decision(kind="call_tool", tool_name="echo", tool_args={"message": "hi"}, reason="use echo"),
        tool_handlers={"echo": EchoTool()},
    )

    assert seed_local.main(["--db", str(db_path), "--trace-run", result.run_id]) == 0

    output = capsys.readouterr().out
    assert "Input: echo hi" in output
    assert "kind: call_tool" in output
    assert "reason: use echo" in output
    assert "allowed: true" in output
    assert "tool: echo" in output
    assert "outcome: tool_succeeded" in output
    assert "tool.result" in output


def test_trace_run_prints_policy_denied_run(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    policy = DenyPolicy()
    result, _ = run_loop_into_db(
        db_path,
        Decision(kind="call_tool", tool_name="echo", tool_args={"message": "hi"}, reason="use echo"),
        policy_engine=policy,
        tool_handlers={"echo": EchoTool()},
    )
    assert policy.calls == 1

    assert seed_local.main(["--db", str(db_path), "--trace-run", result.run_id]) == 0

    output = capsys.readouterr().out
    assert "allowed: false" in output
    assert "outcome: policy_denied" in output
    assert "error: policy denied tool echo: block" in output
    assert "runtime.policy.denied" in output


def test_trace_run_prints_malformed_decision_run(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    result, _ = run_loop_into_db(db_path, {"kind": "answer", "text": "not a Decision"})

    assert seed_local.main(["--db", str(db_path), "--trace-run", result.run_id]) == 0

    output = capsys.readouterr().out
    assert "kind: answer" in output
    assert "outcome: malformed_decision" in output
    assert "error: decision provider must return a runtime_loop.Decision" in output
    assert "runtime.decision.rejected" in output


def test_why_run_prints_answer_explanation(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    result, _ = run_loop_into_db(db_path, Decision(kind="answer", text="done", reason="direct"))

    assert seed_local.main(["--db", str(db_path), "--why-run", result.run_id]) == 0

    output = capsys.readouterr().out
    assert "User asked: hi." in output
    assert "Seed decided to answer because: direct." in output
    assert "Policy allowed the decision." in output
    assert "Outcome: answered." in output
    assert "done" in output
    assert "Events:" not in output


def test_why_run_prints_tool_explanation(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    result, _ = run_loop_into_db(
        db_path,
        Decision(kind="call_tool", tool_name="echo", tool_args={"message": "hi"}, reason="use echo"),
        tool_handlers={"echo": EchoTool()},
    )

    assert seed_local.main(["--db", str(db_path), "--why-run", result.run_id]) == 0

    output = capsys.readouterr().out
    assert "User asked: echo hi." in output
    assert "Seed decided to call tool echo because: use echo." in output
    assert "Policy allowed the decision." in output
    assert "Outcome: tool_succeeded." in output


def test_unknown_run_id_prints_not_found(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    run_loop_into_db(db_path, Decision(kind="answer", text="done", reason="direct"))

    assert seed_local.main(["--db", str(db_path), "--trace-run", "evt_missing"]) == 0
    assert capsys.readouterr().out == "Runtime trace not found for run_id: evt_missing\n"

    assert seed_local.main(["--db", str(db_path), "--why-run", "evt_missing"]) == 0
    assert capsys.readouterr().out == "Runtime trace not found for run_id: evt_missing\n"


def test_trace_and_why_commands_do_not_append_events(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    result, before_count = run_loop_into_db(db_path, Decision(kind="answer", text="done", reason="direct"))

    assert seed_local.main(["--db", str(db_path), "--trace-run", result.run_id]) == 0
    assert persisted_event_count(db_path) == before_count
    assert seed_local.main(["--db", str(db_path), "--why-run", result.run_id]) == 0
    assert persisted_event_count(db_path) == before_count
    capsys.readouterr()


def test_trace_and_why_commands_do_not_call_provider_policy_or_tools(monkeypatch, tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    result, _ = run_loop_into_db(db_path, Decision(kind="answer", text="done", reason="direct"))

    monkeypatch.setattr(seed_local, "build_local_app", lambda **kwargs: (_ for _ in ()).throw(AssertionError("must not build runtime")))

    # Construct exploding collaborators as a regression guard: trace commands have no path to them.
    ExplodingProvider()
    ExplodingPolicy()
    ExplodingTool()

    assert seed_local.main(["--db", str(db_path), "--trace-run", result.run_id]) == 0
    assert seed_local.main(["--db", str(db_path), "--why-run", result.run_id]) == 0
    output = capsys.readouterr().out
    assert "Runtime Trace" in output
    assert "Seed decided to answer" in output
