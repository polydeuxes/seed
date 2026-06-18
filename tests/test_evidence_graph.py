from __future__ import annotations

import copy
import importlib.util
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from seed_runtime.evidence import Evidence
from seed_runtime.evidence_graph import (
    build_evidence_graph,
    build_evidence_summary,
    build_fact_evidence_view,
    find_evidence_for_fact,
    unsupported_fact_views,
)
from seed_runtime.facts import Fact, FactSupport
from seed_runtime.projection_store import state_from_payload, state_to_payload
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


def _state_with_supported_and_unsupported_facts() -> State:
    state = State(workspace_id="ws", last_event_id="evt_last")
    evidence = Evidence(
        id="evd_obs_1",
        workspace_id="ws",
        source="observation:discovery",
        kind="observation",
        observed_at=_ts(),
        payload={
            "source_event_id": "evt_123",
            "observation_id": "obs_1",
            "subject": "service",
            "predicate": "runs_on",
            "value": "example_host_b",
            "run_id": "run_1",
        },
        confidence=0.91,
    )
    supported = Fact(
        id="fact_supported",
        subject_id="service",
        predicate="runs_on",
        value="example_host_b",
        evidence_ids=[evidence.id],
        source_type="discovery",
        confidence=0.91,
        observed_at=_ts(),
    )
    unsupported = Fact(
        id="fact_unsupported",
        subject_id="example_host_d",
        predicate="status",
        value="degraded",
        evidence_ids=[],
        source_type="imported",
        confidence=0.70,
        observed_at=_ts(1),
    )
    state.evidence = {evidence.id: evidence}
    state.facts = {supported.id: supported, unsupported.id: unsupported}
    state.fact_supports = [
        FactSupport(
            subject="service",
            predicate="runs_on",
            value="example_host_b",
            supporting_fact_ids=[supported.id],
            source_types=["discovery"],
            confidence=0.91,
            observed_at=_ts(),
            latest_observed_at=_ts(),
        )
    ]
    return state


def test_evidence_graph_builds_nodes_and_support_links_from_fact_support_data():
    state = _state_with_supported_and_unsupported_facts()

    graph = build_evidence_graph(state)

    assert [node.evidence_id for node in graph.evidence_nodes] == ["evd_obs_1"]
    assert graph.evidence_nodes[0].evidence_type == "observation"
    assert graph.evidence_nodes[0].source_event_id == "evt_123"
    assert [(link.source_evidence_id, link.target_fact_id, link.relationship) for link in graph.evidence_links] == [
        ("evd_obs_1", "fact_supported", "supports")
    ]


def test_evidence_summary_counts_nodes_linked_facts_and_unsupported_facts():
    summary = build_evidence_summary(_state_with_supported_and_unsupported_facts())

    assert summary.evidence_count == 1
    assert summary.linked_fact_count == 1
    assert summary.unsupported_fact_count == 1
    assert summary.average_confidence == 0.91
    assert summary.last_event_id == "evt_last"
    assert summary.projection_version == "v1"


def test_fact_evidence_view_explains_supported_fact_and_reports_unsupported():
    state = _state_with_supported_and_unsupported_facts()

    supported = build_fact_evidence_view(state, "fact_supported")
    unsupported = unsupported_fact_views(state)

    assert supported is not None
    assert supported.supporting_event_ids == ["evd_obs_1", "evt_123"]
    assert "supported by 1 evidence record" in supported.explanation
    assert [view.fact_id for view in unsupported] == ["fact_unsupported"]


def test_find_evidence_for_fact_matches_optional_object():
    state = _state_with_supported_and_unsupported_facts()

    matches = find_evidence_for_fact(state, "service", "runs_on", "example_host_b")

    assert [view.fact_id for view in matches] == ["fact_supported"]
    assert find_evidence_for_fact(state, "service", "runs_on", "example_host_c") == []


def test_evidence_graph_ordering_is_deterministic_and_state_is_not_mutated():
    state = _state_with_supported_and_unsupported_facts()
    before = copy.deepcopy(state)

    first = build_evidence_graph(state)
    second = build_evidence_graph(state)

    assert first == second
    assert state == before


def test_state_snapshot_serialization_preserves_evidence_related_fields():
    state = _state_with_supported_and_unsupported_facts()

    restored = state_from_payload(state_to_payload(state))
    graph = build_evidence_graph(restored)

    assert [node.evidence_id for node in graph.evidence_nodes] == ["evd_obs_1"]
    restored_view = next(view for view in graph.fact_evidence if view.fact_id == "fact_supported")
    assert restored_view.supporting_event_ids == ["evd_obs_1", "evt_123"]


def _event_count(db_path: Path) -> int:
    with sqlite3.connect(str(db_path)) as connection:
        return connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]


def test_cli_evidence_commands_are_read_only_and_print_expected_output(tmp_path, capsys, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "service", "runs_on", "example_host_b"]) == 0
    capsys.readouterr()
    before_count = _event_count(db_path)

    def fail_runtime(*args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("evidence commands must not enter Runtime")

    monkeypatch.setattr(seed_local, "build_local_app", fail_runtime)
    monkeypatch.setattr(seed_local, "run_shell", fail_runtime)

    assert seed_local.main(["--db", str(db_path), "--evidence"]) == 0
    evidence_output = capsys.readouterr().out
    assert "Evidence Summary" in evidence_output
    assert "Evidence Nodes: 1" in evidence_output
    assert _event_count(db_path) == before_count

    assert seed_local.main(["--db", str(db_path), "--why-fact", "service", "runs_on", "example_host_b"]) == 0
    why_output = capsys.readouterr().out
    assert "Fact" in why_output
    assert "service runs_on example_host_b" in why_output
    assert "Explanation" in why_output
    assert "Evidence" in why_output
    assert _event_count(db_path) == before_count

    assert seed_local.main(["--db", str(db_path), "--unsupported-facts"]) == 0
    unsupported_output = capsys.readouterr().out
    assert "Unsupported Facts" in unsupported_output
    assert _event_count(db_path) == before_count


def test_cli_why_fact_handles_missing_fact(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "service", "runs_on", "example_host_b"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--why-fact", "missing", "runs_on"]) == 0

    assert "No matching fact found for missing runs_on." in capsys.readouterr().out
