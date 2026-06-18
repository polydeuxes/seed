from __future__ import annotations

import copy
import importlib.util
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from seed_runtime.confidence import (
    build_confidence_summary,
    build_fact_confidence,
    build_fact_confidences,
    find_fact_confidence,
)
from seed_runtime.contradictions import build_contradictions
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
    source_type: str = "imported",
    confidence: float | None = None,
) -> Fact:
    data = {
        "id": fact_id,
        "subject_id": subject,
        "predicate": predicate,
        "value": value,
        "evidence_ids": evidence_ids or [],
        "source_type": source_type,
        "observed_at": _ts(),
    }
    if confidence is not None:
        data["confidence"] = confidence
    return Fact(**data)


def _evidence(evidence_id: str, event_id: str, fact: Fact) -> Evidence:
    return Evidence(
        id=evidence_id,
        workspace_id="ws",
        source="observation:test",
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


def _state(*facts: Fact) -> State:
    state = State(workspace_id="ws", last_event_id="evt-last")
    state.facts = {fact.id: fact for fact in facts}
    state.evidence = {
        evidence_id: _evidence(evidence_id, f"evt-{evidence_id}", fact)
        for fact in facts
        for evidence_id in fact.evidence_ids
    }
    return state


def _event_count(db_path: Path) -> int:
    with sqlite3.connect(str(db_path)) as connection:
        return connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]


def test_unsupported_fact_with_no_explicit_confidence_has_zero_confidence():
    fact = _fact("fact-1", "example_host_d", "status", "degraded")

    confidence = build_fact_confidence(_state(fact), fact.id)

    assert confidence is not None
    assert confidence.confidence == 0.0
    assert confidence.support_count == 0
    assert confidence.unsupported is True
    assert "unsupported" in confidence.reasons[0]


def test_one_evidence_node_has_at_least_half_confidence():
    fact = _fact("fact-1", "example_host_d", "status", "degraded", evidence_ids=["evd-1"])

    confidence = build_fact_confidence(_state(fact), fact.id)

    assert confidence is not None
    assert confidence.confidence >= 0.50
    assert confidence.support_count == 1
    assert confidence.unsupported is False


def test_two_evidence_nodes_have_strong_confidence():
    fact = _fact(
        "fact-1", "example_host_d", "status", "degraded", evidence_ids=["evd-1", "evd-2"]
    )

    confidence = build_fact_confidence(_state(fact), fact.id)

    assert confidence is not None
    assert confidence.confidence >= 0.75
    assert confidence.support_count == 2


def test_explicit_fact_confidence_is_preserved_when_higher_than_evidence():
    fact = _fact(
        "fact-1",
        "example_host_d",
        "status",
        "degraded",
        evidence_ids=["evd-1"],
        confidence=0.92,
    )

    confidence = build_fact_confidence(_state(fact), fact.id)

    assert confidence is not None
    assert confidence.confidence == 0.92
    assert "explicit fact confidence preserved" in confidence.reasons


def test_contradicted_fact_is_marked_and_confidence_is_reduced_without_resolution():
    fact_1 = _fact("fact-1", "example_host_d", "status", "healthy", evidence_ids=["evd-1", "evd-2"])
    fact_2 = _fact("fact-2", "example_host_d", "status", "degraded", evidence_ids=["evd-3", "evd-4"])
    state = _state(fact_2, fact_1)
    before_fact_ids = sorted(state.facts)

    confidences = {item.fact_id: item for item in build_fact_confidences(state)}

    assert confidences["fact-1"].contradicted is True
    assert confidences["fact-1"].contradiction_count == 1
    assert confidences["fact-1"].confidence == 0.5625
    assert "confidence reduced because fact is contradicted" in confidences["fact-1"].reasons
    assert sorted(state.facts) == before_fact_ids
    assert len(state.facts) == 2


def test_confidence_is_clamped_to_unit_interval():
    fact = _fact("fact-1", "example_host_d", "status", "degraded", confidence=1.0)

    confidence = build_fact_confidence(_state(fact), fact.id)

    assert confidence is not None
    assert 0.0 <= confidence.confidence <= 1.0


def test_summary_counts_strong_weak_unsupported_and_contradicted_facts():
    strong = _fact("strong", "a", "tag", "x", evidence_ids=["evd-1", "evd-2"])
    weak = _fact("weak", "b", "tag", "y", evidence_ids=["evd-3"])
    unsupported = _fact("unsupported", "c", "tag", "z")
    contradicted_a = _fact("contr-a", "d", "status", "up", evidence_ids=["evd-4", "evd-5"])
    contradicted_b = _fact("contr-b", "d", "status", "down", evidence_ids=["evd-6"])
    state = _state(strong, weak, unsupported, contradicted_a, contradicted_b)

    confidences = build_fact_confidences(state)
    summary = build_confidence_summary(state, confidences)

    assert summary.fact_count == 5
    assert summary.strongly_supported_count == 1
    assert summary.weakly_supported_count == 3
    assert summary.unsupported_count == 1
    assert summary.contradicted_count == 2
    assert summary.last_event_id == "evt-last"
    assert summary.projection_version == "v1"


def test_output_ordering_is_deterministic_and_state_is_not_mutated():
    state = _state(
        _fact("fact-b", "service", "runs_on", "example_host_2", evidence_ids=["evd-2"]),
        _fact("fact-a", "example_host_d", "status", "healthy"),
    )
    before = copy.deepcopy(state)

    first = build_fact_confidences(state)
    second = build_fact_confidences(state)

    assert first == second
    assert [(item.subject, item.predicate, item.fact_id) for item in first] == [
        ("example_host_d", "status", "fact-a"),
        ("service", "runs_on", "fact-b"),
    ]
    assert state == before


def test_aggregation_uses_projected_state_evidence_graph_and_contradictions_not_raw_ledger_replay():
    fact = _fact("fact-1", "example_host_d", "status", "degraded", evidence_ids=["evd-1"])
    state = _state(fact)
    graph = build_evidence_graph(state)
    contradictions = build_contradictions(state, graph)
    state.evidence = {}

    confidence = build_fact_confidence(state, fact.id, graph, contradictions)

    assert confidence is not None
    assert confidence.support_count == 1
    assert confidence.supporting_event_ids == ["evd-1", "evt-evd-1"]


def test_find_fact_confidence_matches_optional_object():
    fact = _fact("fact-1", "service", "runs_on", "example_host_b", evidence_ids=["evd-1"])
    state = _state(fact)

    assert [item.fact_id for item in find_fact_confidence(state, "service", "runs_on", "example_host_b")] == ["fact-1"]
    assert find_fact_confidence(state, "service", "runs_on", "example_host_c") == []


def test_cli_confidence_prints_summary_and_fact_list(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "service", "runs_on", "example_host_b"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--confidence"]) == 0

    output = capsys.readouterr().out
    assert "Confidence Summary" in output
    assert "Facts:" in output
    assert "Strongly Supported:" in output
    assert "Fact Confidence" in output
    assert "service runs_on example_host_b" in output


def test_cli_confidence_fact_prints_details_for_match_and_missing_fact(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "service", "runs_on", "example_host_b"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--confidence-fact", "service", "runs_on", "example_host_b"]) == 0
    output = capsys.readouterr().out
    assert "Fact" in output
    assert "service runs_on example_host_b" in output
    assert "confidence:" in output
    assert "support count:" in output
    assert "Reasons" in output
    assert "Supporting Events" in output

    assert seed_local.main(["--db", str(db_path), "--confidence-fact", "missing", "runs_on"]) == 0
    assert "No matching fact found for missing runs_on." in capsys.readouterr().out


def test_cli_confidence_commands_do_not_append_or_invoke_runtime_provider_policy_or_tools(
    tmp_path, capsys, monkeypatch
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "service", "runs_on", "example_host_b"]) == 0
    capsys.readouterr()
    before_count = _event_count(db_path)

    def fail_execution(*args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("confidence commands must be read-only")

    monkeypatch.setattr(seed_local.SQLiteEventLedger, "append", fail_execution)
    monkeypatch.setattr(seed_local, "build_local_app", fail_execution)
    monkeypatch.setattr(seed_local, "run_shell", fail_execution)
    monkeypatch.setattr(seed_local.Runtime, "handle_user_message", fail_execution)
    monkeypatch.setattr(seed_local.ToolExecutor, "execute", fail_execution)

    assert seed_local.main(["--db", str(db_path), "--confidence"]) == 0
    assert seed_local.main(["--db", str(db_path), "--confidence-fact", "service", "runs_on"]) == 0
    capsys.readouterr()
    assert _event_count(db_path) == before_count
