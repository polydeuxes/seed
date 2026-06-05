from copy import deepcopy
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

from seed_runtime.confidence import FactConfidence, build_fact_confidences
from seed_runtime.context_views import (
    ContextFact,
    ContextIssue,
    ContextSummary,
    build_context_summary,
    build_decision_context_view,
    select_context_facts,
)
from seed_runtime.contradictions import build_contradictions
from seed_runtime.evidence import Evidence
from seed_runtime.evidence_graph import build_evidence_graph
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.models import Fact, Goal, ToolNeed, utc_now
from seed_runtime.serialization import to_plain
from seed_runtime.state import State

SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local_context_views", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _evidence(evidence_id: str, event_id: str) -> Evidence:
    return Evidence(
        id=evidence_id,
        workspace_id="ws",
        source="test",
        kind="user_input",
        observed_at=utc_now(),
        payload={"summary": evidence_id},
        confidence=1.0,
    )


def _fact(fact_id: str, subject: str, predicate: str, value, evidence_ids=None, **extra) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        evidence_ids=list(evidence_ids or []),
        observed_at=utc_now(),
        **extra,
    )


def _state() -> State:
    state = State(workspace_id="ws", last_event_id="evt_last", projection_version="v1")
    for evidence_id in ["evd_a", "evd_b", "evd_c", "evd_d", "evd_e"]:
        state.evidence[evidence_id] = _evidence(evidence_id, f"evt_{evidence_id}")
    state.facts["fact_high"] = _fact(
        "fact_high",
        "service-a",
        "runs_on",
        "node-1",
        ["evd_a", "evd_b"],
        confidence=0.96,
    )
    state.facts["fact_weak"] = _fact(
        "fact_weak", "service-b", "enabled", True, ["evd_c"]
    )
    state.facts["fact_status_active"] = _fact(
        "fact_status_active", "service-c", "status", "active", ["evd_d"]
    )
    state.facts["fact_status_down"] = _fact(
        "fact_status_down", "service-c", "status", "down", ["evd_e"]
    )
    state.facts["fact_unsupported"] = _fact(
        "fact_unsupported", "service-z", "hostname", "unknown"
    )
    state.goals["goal_restore"] = Goal(
        id="goal_restore",
        workspace_id="ws",
        summary="restore service-a",
        status="active",
        created_from_event_id="evt_goal",
    )
    state.tool_needs["need_restore"] = ToolNeed(
        id="need_restore",
        workspace_id="ws",
        name="restore",
        summary="restore capability needed",
        capability="service_management",
        reason="service needs management",
        requested_by_event_id="evt_need",
        status="proposed",
    )
    return state


def test_context_view_includes_supported_facts():
    view = build_decision_context_view(_state())

    assert {fact.fact_id for fact in view.facts} >= {
        "fact_high",
        "fact_weak",
        "fact_status_active",
        "fact_status_down",
    }


def test_unsupported_facts_excluded_by_default():
    view = build_decision_context_view(_state())

    assert "fact_unsupported" not in [fact.fact_id for fact in view.facts]


def test_contradicted_facts_retained_and_marked():
    view = build_decision_context_view(_state())
    facts_by_id = {fact.fact_id: fact for fact in view.facts}

    assert facts_by_id["fact_status_active"].contradicted is True
    assert facts_by_id["fact_status_down"].contradicted is True
    assert any(issue.issue_id.startswith("contradiction-") for issue in view.issues)


def test_confidence_values_preserved_from_confidence_aggregation():
    state = _state()
    confidence_by_id = {item.fact_id: item for item in build_fact_confidences(state)}
    view = build_decision_context_view(state)
    facts_by_id = {fact.fact_id: fact for fact in view.facts}

    assert facts_by_id["fact_high"].confidence == confidence_by_id["fact_high"].confidence
    assert (
        facts_by_id["fact_status_active"].confidence
        == confidence_by_id["fact_status_active"].confidence
    )


def test_deterministic_ordering():
    first = build_decision_context_view(_state())
    second = build_decision_context_view(_state())

    assert first == second
    assert [fact.fact_id for fact in first.facts] == [
        "fact_high",
        "fact_weak",
        "fact_status_active",
        "fact_status_down",
    ]


def test_summary_counts_correct():
    view = build_decision_context_view(_state())

    assert view.summary == ContextSummary(
        facts_count=4,
        issues_count=1,
        contradicted_fact_count=2,
        strongly_supported_count=1,
        weakly_supported_count=3,
        unsupported_count=0,
    )


def test_context_view_does_not_mutate_state():
    state = _state()
    before = deepcopy(state)

    build_decision_context_view(state)

    assert state == before


def test_context_view_uses_projected_knowledge_layers_supplied_by_caller():
    state = _state()
    graph = build_evidence_graph(state)
    contradictions = build_contradictions(state, graph)
    supplied_confidences = [
        FactConfidence(
            fact_id="synthetic_from_confidence_layer",
            subject="synthetic",
            predicate="available",
            object=True,
            confidence=0.88,
            support_count=3,
            contradiction_count=0,
            unsupported=False,
            contradicted=False,
        )
    ]

    view = build_decision_context_view(
        state,
        evidence_graph=graph,
        contradictions=contradictions,
        fact_confidences=supplied_confidences,
    )

    assert view.facts == [
        ContextFact(
            fact_id="synthetic_from_confidence_layer",
            subject="synthetic",
            predicate="available",
            object=True,
            confidence=0.88,
            contradicted=False,
            evidence_count=3,
        )
    ]
    assert view.summary.facts_count == 1


def test_select_context_facts_can_include_unsupported_when_requested():
    confidences = build_fact_confidences(_state())

    facts = select_context_facts(confidences, include_unsupported=True)

    assert facts[-1].fact_id == "fact_unsupported"
    assert build_context_summary(facts, []).unsupported_count == 1


def _event_count(db_path: Path) -> int:
    with sqlite3.connect(db_path) as conn:
        return conn.execute("select count(*) from events").fetchone()[0]


def _seed_db(db_path: Path) -> None:
    ledger = SQLiteEventLedger(db_path)
    try:
        observed_at = utc_now()
        evidence = Evidence(
            id="evd_cli",
            workspace_id="default",
            source="test",
            kind="user_input",
            observed_at=observed_at,
            payload={"summary": "cli evidence"},
        )
        fact = Fact(
            id="fact_cli",
            subject_id="service-cli",
            predicate="runs_on",
            value="node-cli",
            evidence_ids=["evd_cli"],
            observed_at=observed_at,
        )
        ledger.append("evidence.observed", "local", {"evidence": to_plain(evidence)})
        ledger.append("fact.observed", "local", {"fact": to_plain(fact)})
    finally:
        ledger.close()


def test_cli_decision_context_output_works_and_is_read_only(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "context-view.sqlite"
    _seed_db(db_path)
    before = _event_count(db_path)

    assert seed_local.main(["--db", str(db_path), "--decision-context"]) == 0

    assert _event_count(db_path) == before
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["facts"] == [
        {
            "fact_id": "fact_cli",
            "subject": "service-cli",
            "predicate": "runs_on",
            "object": "node-cli",
            "confidence": 0.5,
            "contradicted": False,
            "evidence_count": 1,
        }
    ]
    assert payload["summary"]["facts_count"] == 1


def test_cli_decision_context_does_not_invoke_runtime_provider_policy_or_tools(
    tmp_path, monkeypatch
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "context-view-no-runtime.sqlite"
    _seed_db(db_path)

    def explode(*args, **kwargs):  # pragma: no cover - must not be called
        raise AssertionError("decision context must not execute runtime behavior")

    monkeypatch.setattr(seed_local, "build_local_app", explode)
    monkeypatch.setattr(seed_local.EchoTool, "execute", explode)
    monkeypatch.setattr(seed_local.RuntimeLoop, "run", explode)

    assert seed_local.main(["--db", str(db_path), "--decision-context"]) == 0
