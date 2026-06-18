from __future__ import annotations

import copy
import importlib.util
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from seed_runtime.capability_inventory import build_capability_inventory
from seed_runtime.contradictions import build_contradictions
from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact
from seed_runtime.integrity_summary import (
    DEFAULT_INTEGRITY_SUMMARY_CAVEATS,
    ProjectionIntegritySummary,
    build_projection_integrity_summary,
)
from seed_runtime.models import ToolNeed, ToolSpec
from seed_runtime.serialization import to_plain
from seed_runtime.state import GraphValidationIssue, State, StateProjector
from seed_runtime.events import EventLedger

SCRIPT_PATH = Path("scripts/seed_local.py")
BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _fact(
    fact_id: str,
    subject: str,
    predicate: str,
    value: object,
    *,
    evidence_ids: list[str] | None = None,
    expires_at: datetime | None = None,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        evidence_ids=evidence_ids or [],
        source_type="discovery",
        confidence=0.9,
        observed_at=BASE_TIME,
        expires_at=expires_at,
    )


def _evidence(evidence_id: str, fact: Fact) -> Evidence:
    return Evidence(
        id=evidence_id,
        workspace_id="ws",
        source="observation:tests",
        kind="observation",
        observed_at=BASE_TIME,
        payload={
            "source_event_id": f"evt-{evidence_id}",
            "subject": fact.subject_id,
            "predicate": fact.predicate,
            "value": fact.value,
        },
        confidence=0.9,
    )


def _tool(capability: str) -> ToolSpec:
    return ToolSpec(
        name=capability,
        summary=f"{capability} tool",
        input_schema={},
        output_schema={},
        policy_action=capability,
        implementation="tests:no_execute",
        toolkit_id="tests",
        risk_class="L1",
    )


def _need(capability: str) -> ToolNeed:
    return ToolNeed(
        id=f"need_{capability}",
        workspace_id="ws",
        name=f"Need {capability}",
        summary=f"Need {capability}",
        capability=capability,
        reason="test inventory universe",
    )


def _project(ledger: EventLedger) -> State:
    return StateProjector(ledger).project("ws")


def _event_count(db_path: Path) -> int:
    with sqlite3.connect(str(db_path)) as connection:
        return connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]


def test_empty_projection_integrity_summary_has_zero_counts_and_caveats():
    summary = build_projection_integrity_summary(State(workspace_id="ws"))

    assert summary == ProjectionIntegritySummary(
        unsupported_fact_count=0,
        fact_conflict_count=0,
        contradiction_count=0,
        graph_issue_count=0,
        stale_fact_count=0,
        refresh_recommendation_count=0,
        verified_capability_count=0,
        unverified_capability_count=0,
        stale_capability_count=0,
        unknown_capability_count=0,
        provider_reported_capability_count=0,
        caveats=list(DEFAULT_INTEGRITY_SUMMARY_CAVEATS),
        projection_version="v1",
        last_event_id=None,
    )


def test_summary_aggregates_conflicts_contradictions_graph_and_stale_signals():
    expired_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    unsupported = _fact("fact-unsupported", "svc", "owner", "ops")
    supported = _fact("fact-supported", "svc", "runtime", "docker", evidence_ids=["evd-1"])
    conflict_a = _fact("fact-conflict-a", "svc", "status", "healthy", evidence_ids=["evd-a"])
    conflict_b = _fact("fact-conflict-b", "svc", "status", "degraded", evidence_ids=["evd-b"])
    stale = _fact("fact-stale", "svc", "host", "example_host_1", expires_at=expired_at)
    state = State(workspace_id="ws", last_event_id="evt-last")
    state.facts = {
        fact.id: fact
        for fact in [unsupported, supported, conflict_a, conflict_b, stale]
    }
    state.evidence = {
        "evd-1": _evidence("evd-1", supported),
        "evd-a": _evidence("evd-a", conflict_a),
        "evd-b": _evidence("evd-b", conflict_b),
    }
    state.graph_issues = [
        GraphValidationIssue(
            id="issue-1",
            severity="warning",
            subject="svc",
            relationship="runs_on",
            object="example_host_1",
            relationship_ids=["rel-1"],
            source_fact_ids=["fact-supported"],
            reason="test graph issue",
            hint=None,
            expected_subject_types=["service"],
            actual_subject_types=["unknown"],
            expected_object_types=["host"],
            actual_object_types=["unknown"],
        )
    ]

    summary = build_projection_integrity_summary(state)

    assert summary.unsupported_fact_count == 2
    assert summary.fact_conflict_count == 1
    assert summary.contradiction_count == 1
    assert summary.graph_issue_count == 1
    assert summary.stale_fact_count == 1
    assert summary.refresh_recommendation_count == 1
    assert summary.last_event_id == "evt-last"


def test_summary_aggregates_capability_inventory_states():
    ledger = EventLedger()
    ledger.append("tool.registered", "ws", {"tool": to_plain(_tool("unverified_cap"))})
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(_need("verified_cap"))})
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(_need("provider_cap"))})
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(_need("unknown_cap"))})
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(_need("stale_cap"))})
    expired_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    for capability, value, expires_at in [
        ("verified_cap", "verified", None),
        ("provider_cap", "provider_reported", None),
        ("unknown_cap", "ambiguous", None),
        ("stale_cap", "verified", expired_at),
    ]:
        ledger.append(
            "fact.observed",
            "ws",
            {
                "fact": to_plain(
                    _fact(
                        f"fact_{capability}",
                        capability,
                        "capability_verified",
                        value,
                        expires_at=expires_at,
                    )
                )
            },
        )
    state = _project(ledger)

    summary = build_projection_integrity_summary(
        state, capability_inventory=build_capability_inventory(state, now=BASE_TIME)
    )

    assert summary.verified_capability_count == 1
    assert summary.unverified_capability_count == 1
    assert summary.stale_capability_count == 1
    assert summary.unknown_capability_count == 1
    assert summary.provider_reported_capability_count == 1


def test_summary_is_deterministic_and_read_only():
    state = State(workspace_id="ws")
    state.facts = {
        "b": _fact("b", "svc", "status", "healthy"),
        "a": _fact("a", "svc", "status", "degraded"),
    }
    before = copy.deepcopy(state)

    first = build_projection_integrity_summary(state)
    second = build_projection_integrity_summary(state)

    assert first == second
    assert state == before


def test_summary_can_reuse_existing_structures_without_rebuilding(monkeypatch):
    state = State(workspace_id="ws")
    fact_a = _fact("a", "svc", "status", "healthy")
    fact_b = _fact("b", "svc", "status", "degraded")
    state.facts = {fact_a.id: fact_a, fact_b.id: fact_b}
    contradictions = build_contradictions(state)

    monkeypatch.setattr(
        "seed_runtime.integrity_summary.build_contradictions",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("rebuilt contradictions")),
    )

    summary = build_projection_integrity_summary(state, contradictions=contradictions)

    assert summary.contradiction_count == 1


def test_integrity_summary_cli_output_is_read_only_and_concise(tmp_path, capsys, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert seed_local.main(["--db", str(db_path), "--observe", "svc", "owner", "ops"]) == 0
    capsys.readouterr()
    before_count = _event_count(db_path)

    def fail_runtime(*args, **kwargs):  # pragma: no cover - should never be called
        raise AssertionError("integrity summary must not enter Runtime")

    monkeypatch.setattr(seed_local, "build_local_app", fail_runtime)
    monkeypatch.setattr(seed_local, "run_shell", fail_runtime)

    assert seed_local.main(["--db", str(db_path), "--integrity-summary"]) == 0

    output = capsys.readouterr().out
    assert "Integrity Summary" in output
    assert "Unsupported facts: 0" in output
    assert "Fact conflicts: 0" in output
    assert "Capabilities" in output
    assert "Refresh recommendations: 0" in output
    assert _event_count(db_path) == before_count


def test_integrity_summary_navigation_hints_reference_existing_inventory_commands():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()
    existing_options = {
        option
        for action in parser._actions
        for option in action.option_strings
    }
    summary = ProjectionIntegritySummary(
        unsupported_fact_count=12,
        fact_conflict_count=3,
        contradiction_count=1,
        graph_issue_count=4,
        stale_fact_count=8,
        refresh_recommendation_count=5,
        verified_capability_count=14,
        unverified_capability_count=6,
        stale_capability_count=2,
        unknown_capability_count=1,
        provider_reported_capability_count=7,
        caveats=[],
        projection_version="v1",
        last_event_id="evt-last",
    )

    output = seed_local.format_projection_integrity_summary(summary)
    navigation_commands = [
        "--unsupported-facts",
        "--fact-conflicts",
        "--contradictions",
        "--graph-issues",
        "--stale-facts",
        "--stale-fact-refreshes",
        "--capability-status",
    ]

    for command in navigation_commands:
        assert command in existing_options
        assert f"See: {command}" in output


def test_integrity_summary_navigation_output_is_deterministic():
    seed_local = load_seed_local_module()
    summary = build_projection_integrity_summary(State(workspace_id="ws"))

    first = seed_local.format_projection_integrity_summary(summary)
    second = seed_local.format_projection_integrity_summary(summary)

    assert first == second


def test_integrity_summary_navigation_hints_are_shown_for_empty_state():
    seed_local = load_seed_local_module()
    output = seed_local.format_projection_integrity_summary(
        build_projection_integrity_summary(State(workspace_id="ws"))
    )

    assert "Unsupported facts: 0\nSee: --unsupported-facts" in output
    assert "Fact conflicts: 0\nSee: --fact-conflicts" in output
    assert "Contradictions: 0\nSee: --contradictions" in output
    assert "Graph issues: 0\nSee: --graph-issues" in output
    assert "Stale facts: 0\nSee: --stale-facts" in output
    assert "Refresh recommendations: 0\nSee: --stale-fact-refreshes" in output
    assert "See: --capability-status" in output


def test_integrity_summary_navigation_does_not_change_summary_semantics():
    seed_local = load_seed_local_module()
    state = State(workspace_id="ws")
    fact_a = _fact("a", "svc", "status", "healthy")
    fact_b = _fact("b", "svc", "status", "degraded")
    state.facts = {fact_a.id: fact_a, fact_b.id: fact_b}

    before = build_projection_integrity_summary(state)
    seed_local.format_projection_integrity_summary(before)
    after = build_projection_integrity_summary(state)

    assert after == before
