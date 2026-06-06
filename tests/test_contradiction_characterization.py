from __future__ import annotations

import copy
from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.explanations import ExplanationBuilder
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import GraphValidationIssue, StateProjector

NOW = datetime(2026, 6, 6, 12, 0, tzinfo=timezone.utc)
PAST = datetime(2000, 1, 1, tzinfo=timezone.utc)
FUTURE = datetime(2100, 1, 1, tzinfo=timezone.utc)


def _fact(
    fact_id: str,
    subject: str,
    predicate: str,
    value: object,
    *,
    observed_at: datetime = NOW,
    confidence: float = 0.9,
    source_type: str = "provider",
    evidence_ids: list[str] | None = None,
    expires_at: datetime | None = None,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        observed_at=observed_at,
        confidence=confidence,
        source_type=source_type,
        evidence_ids=evidence_ids or [],
        expires_at=expires_at,
    )


def _project(facts: list[Fact], *, measurement_history_limit: int = 1):
    ledger = EventLedger()
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(
        ledger, measurement_history_limit=measurement_history_limit
    ).project("ws")


def test_durable_single_cardinality_conflict_preserves_competing_facts_and_supports():
    state = _project(
        [
            _fact("fact_runtime_docker", "jellyfin", "runtime", "docker"),
            _fact("fact_runtime_systemd", "jellyfin", "runtime", "systemd"),
        ]
    )

    conflicts = state.get_fact_conflicts()

    assert len(conflicts) == 1
    conflict = conflicts[0]
    assert conflict.subject == "jellyfin"
    assert conflict.predicate == "runtime"
    assert conflict.values == ["docker", "systemd"]
    assert conflict.winning_value is None
    assert conflict.best_fact_id is None
    assert conflict.conflicting_fact_ids == [
        "fact_runtime_docker",
        "fact_runtime_systemd",
    ]
    assert set(state.facts) == {"fact_runtime_docker", "fact_runtime_systemd"}
    assert {
        (support.value, tuple(support.supporting_fact_ids))
        for support in state.get_fact_supports("jellyfin", "runtime")
    } == {
        ("docker", ("fact_runtime_docker",)),
        ("systemd", ("fact_runtime_systemd",)),
    }


def test_multi_cardinality_predicates_do_not_conflict_solely_due_to_multiple_values():
    state = _project(
        [
            _fact("fact_alias", "node1", "alias", "node1.example"),
            _fact("fact_ip", "node1", "ip_address", "10.0.0.1"),
            _fact("fact_ip_2", "node1", "ip_address", "10.0.0.2"),
            _fact("fact_group_a", "node1", "group", "web"),
            _fact("fact_group_b", "node1", "group", "blue"),
        ]
    )

    assert state.get_fact_conflicts() == []
    assert [fact.value for fact in state.get_current_facts("node1", "ip_address")] == [
        "10.0.0.1",
        "10.0.0.2",
    ]
    assert {fact.value for fact in state.get_current_facts("node1", "group")} == {
        "web",
        "blue",
    }
    assert state.get_current_facts("node1", "alias")[0].value == "node1.example"


def test_measurements_use_latest_current_sample_without_fact_conflict_and_keep_debug_history_when_configured():
    older = _fact(
        "fact_fs_old",
        "node1",
        "filesystem_free_bytes",
        100,
        observed_at=datetime(2026, 6, 6, 10, 0, tzinfo=timezone.utc),
        evidence_ids=["evd_old"],
    )
    newer = _fact(
        "fact_fs_new",
        "node1",
        "filesystem_free_bytes",
        50,
        observed_at=datetime(2026, 6, 6, 11, 0, tzinfo=timezone.utc),
        evidence_ids=["evd_new"],
    )

    default_state = _project([older, newer])
    debug_state = _project([older, newer], measurement_history_limit=2)

    assert list(default_state.facts) == ["fact_fs_new"]
    assert set(debug_state.facts) == {"fact_fs_old", "fact_fs_new"}
    assert debug_state.get_fact_conflicts() == []
    support = debug_state.get_fact_support("node1", "filesystem_free_bytes")
    assert support is not None
    assert support.value == 50
    assert support.supporting_fact_ids == ["fact_fs_new"]
    assert support.predicate_semantics == "measurement"
    assert support.support_kind == "current_sample"
    assert debug_state.get_best_fact("node1", "filesystem_free_bytes").id == "fact_fs_new"


def test_expired_facts_are_stale_excluded_from_default_conflicts_and_visible_with_include_expired():
    state = _project(
        [
            _fact(
                "fact_runtime_expired",
                "jellyfin",
                "runtime",
                "docker",
                expires_at=PAST,
            ),
            _fact(
                "fact_runtime_current",
                "jellyfin",
                "runtime",
                "systemd",
                expires_at=FUTURE,
            ),
        ]
    )

    assert state.get_fact_conflicts() == []
    assert state.get_best_fact("jellyfin", "runtime").id == "fact_runtime_current"
    assert [fact.id for fact in state.get_stale_facts()] == ["fact_runtime_expired"]
    recommendations = state.get_stale_fact_refresh_recommendations()
    assert [item.fact_id for item in recommendations] == ["fact_runtime_expired"]
    assert recommendations[0].recommended_capability == "service_inspection"

    include_expired_conflicts = state.get_fact_conflicts(include_expired=True)
    assert len(include_expired_conflicts) == 1
    assert include_expired_conflicts[0].values == ["docker", "systemd"]


def test_why_explanation_exposes_active_fact_conflict_without_truth_arbitration():
    state = _project(
        [
            _fact("fact_runtime_docker", "jellyfin", "runtime", "docker"),
            _fact("fact_runtime_systemd", "jellyfin", "runtime", "systemd"),
        ]
    )

    explanation = ExplanationBuilder(state).why("jellyfin", "runtime")

    assert explanation.status == "ambiguous"
    assert explanation.current_beliefs == []
    assert {belief.value for belief in explanation.competing_beliefs} == {
        "docker",
        "systemd",
    }
    assert explanation.conflict is not None
    assert explanation.conflict.best_fact_id is None
    assert explanation.conflict.winning_value is None
    assert explanation.conflict.conflicting_fact_ids == [
        "fact_runtime_docker",
        "fact_runtime_systemd",
    ]


def test_graph_validation_reports_invalid_topology_without_mutating_projected_graph_or_facts():
    state = _project(
        [
            _fact("host_type", "node1", "os", "linux"),
            _fact("group_type", "member1", "group", "workers"),
            _fact("bad_hosting", "workers", "runs_on", "node1"),
        ]
    )

    issue = next(issue for issue in state.graph_issues if issue.subject == "workers")

    assert isinstance(issue, GraphValidationIssue)
    assert issue.severity == "error"
    assert issue.relationship == "runs_on"
    assert "subject type is group; expected service" in issue.reason
    assert [edge.source_fact_id for edge in state.get_relationships("workers", "runs_on")] == [
        "bad_hosting"
    ]
    assert {"host_type", "group_type", "bad_hosting"}.issubset(state.facts)


def test_projected_fact_conflict_inventory_is_read_only():
    state = _project(
        [
            _fact("fact_runtime_docker", "jellyfin", "runtime", "docker"),
            _fact("fact_runtime_systemd", "jellyfin", "runtime", "systemd"),
        ]
    )
    before = copy.deepcopy(state)

    inventory = state.get_fact_conflicts()

    assert [item.predicate for item in inventory] == ["runtime"]
    assert state == before
