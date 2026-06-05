import importlib.util
import sqlite3
import sys
from pathlib import Path

from seed_runtime.decision_journal import DecisionJournal
from seed_runtime.events import SQLiteEventLedger

SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def record_run_into_db(
    db_path,
    *,
    input_text="hi",
    decision_kind="answer",
    reason="direct",
    outcome="answered",
    selected_tool_name=None,
    policy_allowed=True,
    assistant_text="done",
    tool_event_kind=None,
    tool_payload=None,
    policy_denied=False,
    error=None,
):
    ledger = SQLiteEventLedger(str(db_path))
    input_event = ledger.append(
        "input.user_message", "local", {"text": input_text}, actor="user"
    )
    run_id = input_event.id
    if assistant_text is not None:
        ledger.append(
            "assistant.answer",
            "local",
            {"text": assistant_text, "reason": reason},
            causation_id=input_event.id,
            correlation_id=run_id,
        )
    if policy_denied:
        ledger.append(
            "runtime.policy.denied",
            "local",
            {"tool_name": selected_tool_name, "error": error},
            causation_id=input_event.id,
            correlation_id=run_id,
        )
    if tool_event_kind is not None:
        payload = dict(tool_payload or {})
        payload.setdefault("tool_name", selected_tool_name)
        ledger.append(
            tool_event_kind,
            "local",
            payload,
            causation_id=input_event.id,
            correlation_id=run_id,
        )
    DecisionJournal(ledger).append_record(
        workspace_id="local",
        run_id=run_id,
        decision_kind=decision_kind,
        reason=reason,
        context_hash="ctx123",
        selected_tool_name=selected_tool_name,
        selected_tool_args={},
        policy_allowed=policy_allowed,
        outcome=outcome,
        error=error,
        causation_id=input_event.id,
        correlation_id=run_id,
    )
    before_count = len(ledger.list_events("local"))
    ledger.close()
    return run_id, before_count


def persisted_event_count(db_path):
    connection = sqlite3.connect(str(db_path))
    try:
        return connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    finally:
        connection.close()


def test_trace_run_prints_answer_run(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    run_id, _ = record_run_into_db(db_path)

    assert seed_local.main(["--db", str(db_path), "--trace-run", run_id]) == 0

    output = capsys.readouterr().out
    assert "Runtime Trace" in output
    assert "workspace: local" in output
    assert f"run: {run_id}" in output
    assert "Input: hi" in output
    assert "kind: answer" in output
    assert "reason: direct" in output
    assert "context_hash: ctx123" in output
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
    run_id, _ = record_run_into_db(
        db_path,
        input_text="echo hi",
        decision_kind="call_tool",
        reason="use echo",
        outcome="tool_succeeded",
        selected_tool_name="echo",
        assistant_text=None,
        tool_event_kind="tool.result",
        tool_payload={"output": {"message": "hi"}},
    )

    assert seed_local.main(["--db", str(db_path), "--trace-run", run_id]) == 0

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
    run_id, _ = record_run_into_db(
        db_path,
        input_text="echo hi",
        decision_kind="call_tool",
        reason="use echo",
        outcome="policy_denied",
        selected_tool_name="echo",
        policy_allowed=False,
        assistant_text=None,
        policy_denied=True,
        error="policy denied tool echo: block",
    )

    assert seed_local.main(["--db", str(db_path), "--trace-run", run_id]) == 0

    output = capsys.readouterr().out
    assert "allowed: false" in output
    assert "outcome: policy_denied" in output
    assert "error: policy denied tool echo: block" in output
    assert "runtime.policy.denied" in output


def test_why_run_prints_answer_explanation(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    run_id, _ = record_run_into_db(db_path)

    assert seed_local.main(["--db", str(db_path), "--why-run", run_id]) == 0

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
    run_id, _ = record_run_into_db(
        db_path,
        input_text="echo hi",
        decision_kind="call_tool",
        reason="use echo",
        outcome="tool_succeeded",
        selected_tool_name="echo",
        assistant_text=None,
        tool_event_kind="tool.result",
        tool_payload={"output": {"message": "hi"}},
    )

    assert seed_local.main(["--db", str(db_path), "--why-run", run_id]) == 0

    output = capsys.readouterr().out
    assert "User asked: echo hi." in output
    assert "Seed decided to call tool echo because: use echo." in output
    assert "Policy allowed the decision." in output
    assert "Outcome: tool_succeeded." in output


def test_unknown_run_id_prints_not_found(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    record_run_into_db(db_path)

    assert seed_local.main(["--db", str(db_path), "--trace-run", "evt_missing"]) == 0
    assert capsys.readouterr().out == "Runtime trace not found for run_id: evt_missing\n"

    assert seed_local.main(["--db", str(db_path), "--why-run", "evt_missing"]) == 0
    assert capsys.readouterr().out == "Runtime trace not found for run_id: evt_missing\n"


def test_trace_and_why_commands_do_not_append_events(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    run_id, before_count = record_run_into_db(db_path)

    assert seed_local.main(["--db", str(db_path), "--trace-run", run_id]) == 0
    assert persisted_event_count(db_path) == before_count
    assert seed_local.main(["--db", str(db_path), "--why-run", run_id]) == 0
    assert persisted_event_count(db_path) == before_count
    capsys.readouterr()


def test_trace_and_why_commands_do_not_build_runtime(monkeypatch, tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    run_id, _ = record_run_into_db(db_path)

    monkeypatch.setattr(seed_local, "build_local_app", lambda **kwargs: (_ for _ in ()).throw(AssertionError("must not build runtime")))

    assert seed_local.main(["--db", str(db_path), "--trace-run", run_id]) == 0
    assert seed_local.main(["--db", str(db_path), "--why-run", run_id]) == 0
    output = capsys.readouterr().out
    assert "Runtime Trace" in output
    assert "Seed decided to answer" in output
