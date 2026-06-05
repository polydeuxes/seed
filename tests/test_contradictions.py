from __future__ import annotations

import copy
import importlib.util
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from seed_runtime.contradictions import (
    build_contradiction_summary,
    build_contradictions,
    find_contradictions_for_fact,
)
from seed_runtime.evidence import Evidence
from seed_runtime.evidence_graph import build_evidence_graph
from seed_runtime.facts import Fact
from seed_runtime.state import State

SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _ts(offset: int = 0) -> datetime:
    return datetime(2026, 1, 1, 0, 0, offset, tzinfo=timezone.utc)


def _fact(
    fact_id: str,
    subject: str,
    predicate: str,
    value: object,
    *,
    evidence_ids: list[str] | None = None,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        evidence_ids=evidence_ids or [],
        source_type="discovery",
        confidence=0.9,
        observed_at=_ts(),
    )


def _evidence(evidence_id: str, event_id: str, fact: Fact) -> Evidence:
    return Evidence(
        id=evidence_id,
        workspace_id="ws",
        source="observation:discovery",
        kind="observation",
        observed_at=_ts(),
        payload={
            "source_event_id": event_id,
            "subject": fact.subject_id,
            "predicate": fact.predicate,
            "value": fact.value,
        },
        confidence=0.9,
    )


def _contradictory_state() -> State:
    state = State(workspace_id="ws", last_event_id="evt-2")
    fact_1 = _fact("fact-1", "node214", "status", "healthy", evidence_ids=["evd-1"])
    fact_2 = _fact("fact-2", "node214", "status", "degraded", evidence_ids=["evd-2"])
    state.facts = {fact_2.id: fact_2, fact_1.id: fact_1}
    state.evidence = {
        "evd-1": _evidence("evd-1", "evt-1", fact_1),
        "evd-2": _evidence("evd-2", "evt-2", fact_2),
    }
    return state


def _event_count(db_path: Path) -> int:
    with sqlite3.connect(str(db_path)) as connection:
        return connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]


def test_detects_contradiction_for_exclusive_predicate_with_different_values():
    contradictions = build_contradictions(_contradictory_state())

    assert len(contradictions) == 1
    contradiction = contradictions[0]
    assert contradiction.subject == "node214"
    assert contradiction.predicate == "status"
    assert contradiction.fact_ids == ["fact-2", "fact-1"]
    assert contradiction.values == ["degraded", "healthy"]
    assert contradiction.severity == "high"
    assert contradiction.reason == "exclusive predicate has multiple values"


def test_does_not_flag_duplicate_identical_facts():
    state = State(workspace_id="ws")
    state.facts = {
        "fact-a": _fact("fact-a", "node214", "status", "healthy"),
        "fact-b": _fact("fact-b", "node214", "status", "healthy"),
    }

    assert build_contradictions(state) == []


def test_does_not_flag_non_exclusive_predicates_by_default():
    state = State(workspace_id="ws")
    state.facts = {
        "fact-a": _fact("fact-a", "node214", "tag", "blue"),
        "fact-b": _fact("fact-b", "node214", "tag", "green"),
    }

    assert build_contradictions(state) == []
    assert build_contradictions(state, exclusive_predicates={"tag"})[0].predicate == "tag"


def test_attaches_evidence_per_conflicting_fact_when_graph_is_supplied():
    state = _contradictory_state()
    graph = build_evidence_graph(state)

    contradiction = build_contradictions(state, graph)[0]

    assert sorted(contradiction.evidence_by_fact_id) == ["fact-1", "fact-2"]
    assert contradiction.evidence_by_fact_id["fact-1"].supporting_event_ids == ["evd-1", "evt-1"]
    assert contradiction.evidence_by_fact_id["fact-2"].supporting_event_ids == ["evd-2", "evt-2"]
    assert contradiction.supporting_event_ids == ["evd-1", "evd-2", "evt-1", "evt-2"]


def test_summary_counts_contradictions_and_severity_buckets_correctly():
    state = _contradictory_state()
    contradictions = build_contradictions(state)

    summary = build_contradiction_summary(state, contradictions)

    assert summary.contradiction_count == 1
    assert summary.affected_fact_count == 2
    assert summary.high_severity_count == 1
    assert summary.medium_severity_count == 0
    assert summary.low_severity_count == 0
    assert summary.last_event_id == "evt-2"
    assert summary.projection_version == "v1"


def test_find_contradictions_for_fact_returns_relevant_contradictions():
    state = _contradictory_state()

    assert [item.subject for item in find_contradictions_for_fact(state, "fact-1")] == ["node214"]
    assert find_contradictions_for_fact(state, "missing") == []


def test_output_ordering_is_deterministic():
    state = _contradictory_state()
    service_a = _fact("fact-a", "service", "runs_on", "node1")
    service_b = _fact("fact-b", "service", "runs_on", "node2")
    state.facts[service_b.id] = service_b
    state.facts[service_a.id] = service_a

    first = build_contradictions(state)
    second = build_contradictions(state)

    assert first == second
    assert [(item.subject, item.predicate) for item in first] == [
        ("node214", "status"),
        ("service", "runs_on"),
    ]


def test_contradiction_detection_does_not_mutate_state():
    state = _contradictory_state()
    before = copy.deepcopy(state)

    build_contradictions(state)
    build_contradiction_summary(state)
    find_contradictions_for_fact(state, "fact-1")

    assert state == before


def test_contradiction_detection_uses_projected_state_and_evidence_graph_not_raw_ledger_replay():
    state = _contradictory_state()
    graph = build_evidence_graph(state)
    state.evidence = {}

    contradiction = build_contradictions(state, graph)[0]

    assert sorted(contradiction.evidence_by_fact_id) == ["fact-1", "fact-2"]
    assert contradiction.supporting_event_ids == ["evd-1", "evd-2", "evt-1", "evt-2"]


def test_cli_contradictions_prints_summary_and_conflict_details(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "node214", "status", "healthy"]) == 0
    assert seed_local.main(["--db", str(db_path), "--observe", "node214", "status", "degraded"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--contradictions"]) == 0

    output = capsys.readouterr().out
    assert "Contradictions" in output
    assert "Count: 1" in output
    assert "Affected Facts: 2" in output
    assert "High Severity: 1" in output
    assert "* node214 status" in output
    assert "severity: high" in output
    assert "reason: exclusive predicate has multiple values" in output
    assert "values: degraded, healthy" in output
    assert "facts:" in output
    assert "supporting events:" in output


def test_cli_contradiction_command_does_not_append_events(tmp_path, capsys, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "node214", "status", "healthy"]) == 0
    assert seed_local.main(["--db", str(db_path), "--observe", "node214", "status", "degraded"]) == 0
    capsys.readouterr()
    before_count = _event_count(db_path)

    def fail_append(*args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("--contradictions must not append events")

    monkeypatch.setattr(seed_local.SQLiteEventLedger, "append", fail_append)

    assert seed_local.main(["--db", str(db_path), "--contradictions"]) == 0
    capsys.readouterr()
    assert _event_count(db_path) == before_count


def test_cli_contradiction_command_does_not_invoke_runtime_provider_policy_or_tools(
    tmp_path, capsys, monkeypatch
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "node214", "status", "healthy"]) == 0
    assert seed_local.main(["--db", str(db_path), "--observe", "node214", "status", "degraded"]) == 0
    capsys.readouterr()

    def fail_execution(*args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("--contradictions must be read-only")

    monkeypatch.setattr(seed_local, "build_local_app", fail_execution)
    monkeypatch.setattr(seed_local, "run_shell", fail_execution)
    monkeypatch.setattr(seed_local.RuntimeLoop, "run", fail_execution)
    monkeypatch.setattr(seed_local.EchoTool, "execute", fail_execution)

    assert seed_local.main(["--db", str(db_path), "--contradictions"]) == 0
    output = capsys.readouterr().out
    assert "Contradictions" in output
