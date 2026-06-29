from datetime import datetime, timedelta, timezone

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.serialization import to_plain
from seed_runtime.models import Approval, Entity, Fact, Goal, ToolNeed, utc_now
from seed_runtime.state import ProjectionBuildDiagnostics, StateProjector
import seed_runtime.state as state_module


def test_event_application_recovers_affected_scope_before_state_mutation():
    ledger = EventLedger()
    workspace_id = "ws_scope_visibility"
    fact = Fact(
        id="fact_scope",
        subject_id="host_1",
        predicate="os",
        value="linux",
        evidence_ids=["evt_source"],
        observed_at=utc_now(),
    )
    event = ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})

    recovered = state_module._recover_affected_scope(event)
    before_state = StateProjector(EventLedger()).project(workspace_id)

    assert recovered == state_module._AffectedScope(
        collection="facts", identity="fact_scope", subject_id="host_1"
    )
    assert "fact_scope" not in before_state.facts

    after_state = StateProjector(ledger).project(workspace_id)

    assert after_state.facts["fact_scope"] == fact


def test_affected_scope_recovery_covers_update_events_without_applying_them():
    ledger = EventLedger()
    workspace_id = "ws_scope_updates"

    need_event = ledger.append(
        "tool_need.status_changed",
        workspace_id,
        {"tool_need_id": "need_scope", "status": "satisfied"},
    )
    plan_event = ledger.append(
        "action_plan.accepted",
        workspace_id,
        {"action_plan_id": "plan_scope", "status": "accepted"},
    )

    assert state_module._recover_affected_scope(need_event) == state_module._AffectedScope(
        collection="tool_needs", identity="need_scope"
    )
    assert state_module._recover_affected_scope(plan_event) == state_module._AffectedScope(
        collection="action_plans", identity="plan_scope"
    )
    assert StateProjector(ledger).project(workspace_id).tool_needs == {}
    assert StateProjector(ledger).project(workspace_id).action_plans == {}


def test_projector_rebuilds_state_deterministically():
    ledger = EventLedger()
    workspace_id = "ws_1"
    entity = Entity(id="ent_1", kind="host", name="example_host")
    fact = Fact(
        id="fact_1",
        subject_id="ent_1",
        predicate="ssh.running",
        value=False,
        evidence_ids=["evt_source"],
        observed_at=utc_now(),
    )
    goal = Goal(id="goal_1", workspace_id=workspace_id, summary="Make SSH work")
    need = ToolNeed(
        id="need_1",
        workspace_id=workspace_id,
        name="install_ssh_server",
        summary="Install SSH",
        capability="ssh_access",
        reason="missing tool",
    )
    approval = Approval(
        id=new_id("appr"), action="ssh.install", scope="ent_1", approved_by="user"
    )

    ledger.append("entity.upserted", workspace_id, {"entity": to_plain(entity)})
    ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})
    ledger.append("goal.created", workspace_id, {"goal": to_plain(goal)})
    ledger.append("tool_need.created", workspace_id, {"tool_need": to_plain(need)})
    ledger.append("approval.granted", workspace_id, {"approval": to_plain(approval)})

    first = StateProjector(ledger).project(workspace_id)
    second = StateProjector(ledger).project(workspace_id)

    assert first == second
    assert first.entities["ent_1"].name == "example_host"
    assert first.facts["fact_1"].value is False
    assert first.goals["goal_1"].status == "active"
    assert first.open_tool_needs[0].name == "install_ssh_server"
    assert first.has_approval("ssh.install", "ent_1") is not None


def test_fact_replay_defers_relationship_projection_until_finalization(monkeypatch):
    ledger = EventLedger()
    workspace_id = "ws_deferred_relationship_projection"
    observed_at = utc_now()
    facts = [
        Fact(
            id="fact_group",
            subject_id="example_host",
            predicate="group",
            value="servers",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_alias",
            subject_id="example_host",
            predicate="alias",
            value="192.0.2.115",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_host",
            subject_id="web_service",
            predicate="host",
            value="example_host",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
    ]
    for fact in facts:
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})

    legacy_calls = 0
    catalog_calls = 0
    original_legacy = state_module._project_entity_relationships
    original_catalog = state_module._project_catalog_relationships

    def count_legacy(*args, **kwargs):
        nonlocal legacy_calls
        legacy_calls += 1
        return original_legacy(*args, **kwargs)

    def count_catalog(*args, **kwargs):
        nonlocal catalog_calls
        catalog_calls += 1
        return original_catalog(*args, **kwargs)

    monkeypatch.setattr(state_module, "_project_entity_relationships", count_legacy)
    monkeypatch.setattr(state_module, "_project_catalog_relationships", count_catalog)
    diagnostics = ProjectionBuildDiagnostics()

    state = StateProjector(ledger).project(workspace_id, diagnostics=diagnostics)

    assert legacy_calls == 1
    assert catalog_calls == 1
    assert [
        (relationship.subject, relationship.predicate, relationship.object)
        for relationship in state.entity_relationships
    ] == [
        ("example_host", "group", "servers"),
        ("example_host", "alias", "192.0.2.115"),
        ("web_service", "host", "example_host"),
    ]
    assert [
        (relationship.subject, relationship.relationship, relationship.object)
        for relationship in state.relationships
    ] == [
        ("example_host", "alias_of", "192.0.2.115"),
        ("example_host", "member_of", "servers"),
        ("web_service", "runs_on", "example_host"),
    ]
    timing_names = [name for name, _elapsed in diagnostics.timings]
    assert "event replay" in timing_names
    assert "finalization: legacy relationship projection" in timing_names
    assert "finalization: catalog relationship projection" in timing_names
    assert "event replay: legacy relationship refresh after fact" not in timing_names
    assert "event replay: catalog relationship refresh after fact" not in timing_names


def test_has_approval_compares_expiration_against_utc_now():
    ledger = EventLedger()
    workspace_id = "ws_utc_approval"
    approval = Approval(
        id=new_id("appr"),
        action="ssh.install",
        scope="ent_1",
        approved_by="user",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    expired = Approval(
        id=new_id("appr"),
        action="ssh.install",
        scope="ent_2",
        approved_by="user",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=5),
    )

    ledger.append("approval.granted", workspace_id, {"approval": to_plain(approval)})
    ledger.append("approval.granted", workspace_id, {"approval": to_plain(expired)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.has_approval("ssh.install", "ent_1") == approval
    assert state.has_approval("ssh.install", "ent_2") is None


def test_projector_projects_entity_relationships_from_string_facts():
    ledger = EventLedger()
    workspace_id = "ws_relationships"
    observed_at = utc_now()
    facts = [
        Fact(
            id="fact_host",
            subject_id="web_service",
            predicate="host",
            value="example_host",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_runtime",
            subject_id="web_service",
            predicate="runtime",
            value="docker",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_container",
            subject_id="web_service",
            predicate="container",
            value="web_service",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_running",
            subject_id="web_service",
            predicate="running",
            value=True,
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
    ]

    for fact in facts:
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})

    state = StateProjector(ledger).project(workspace_id)

    assert [
        (relationship.subject, relationship.predicate, relationship.object)
        for relationship in state.entity_relationships
    ] == [
        ("web_service", "host", "example_host"),
        ("web_service", "runtime", "docker"),
        ("web_service", "container", "web_service"),
        ("web_service", "managed_by", "docker_container_lifecycle"),
    ]


def test_entity_relationship_query_helpers_return_deduped_matches():
    ledger = EventLedger()
    workspace_id = "ws_relationship_queries"
    observed_at = utc_now()
    facts = [
        Fact(
            id="fact_host",
            subject_id="web_service",
            predicate="host",
            value="example_host",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_runtime",
            subject_id="web_service",
            predicate="runtime",
            value="docker",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_runtime_duplicate",
            subject_id="web_service",
            predicate="runtime",
            value="docker",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_runtime_other",
            subject_id="grafana",
            predicate="runtime",
            value="docker",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
    ]

    for fact in facts:
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.find_related("web_service", "host") == ["example_host"]
    assert state.find_entities("runtime", "docker") == ["web_service", "grafana"]
    assert [
        (relationship.subject, relationship.predicate, relationship.object)
        for relationship in state.get_entity_relationships("example_host")
    ] == [("web_service", "host", "example_host")]


def _observed_fact(
    fact_id: str,
    subject_id: str,
    predicate: str,
    value: object,
    observed_at: datetime,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject_id,
        predicate=predicate,
        value=value,
        evidence_ids=["evt_source"],
        observed_at=observed_at,
    )


def test_runtime_docker_infers_managed_by_docker_container_lifecycle():
    ledger = EventLedger()
    workspace_id = "ws_infer_docker"
    observed_at = utc_now()
    runtime = _observed_fact(
        "fact_runtime_docker", "web_service", "runtime", "docker", observed_at
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(runtime)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.observed_facts == {runtime.id: runtime}
    assert state.find_related("web_service", "managed_by") == [
        "docker_container_lifecycle"
    ]
    inferred = state.inferred_facts[
        "fact_inferred_web_service_managed_by_docker_container_lifecycle"
    ]
    assert inferred.inferred is True
    assert inferred.subject_id == "web_service"
    assert inferred.predicate == "managed_by"
    assert inferred.value == "docker_container_lifecycle"


def test_runtime_systemd_infers_managed_by_systemctl_cli():
    ledger = EventLedger()
    workspace_id = "ws_infer_systemd"
    observed_at = utc_now()
    runtime = _observed_fact(
        "fact_runtime_systemd", "sshd", "runtime", "systemd", observed_at
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(runtime)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.find_related("sshd", "managed_by") == ["systemctl_cli"]
    inferred = state.inferred_facts["fact_inferred_sshd_managed_by_systemctl_cli"]
    assert inferred.inferred is True


def test_observed_managed_by_fact_wins_over_inferred_managed_by():
    ledger = EventLedger()
    workspace_id = "ws_observed_wins"
    observed_at = utc_now()
    runtime = _observed_fact(
        "fact_runtime_docker", "web_service", "runtime", "docker", observed_at
    )
    managed_by = _observed_fact(
        "fact_managed_by_custom", "web_service", "managed_by", "custom_cli", observed_at
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(runtime)})
    ledger.append("fact.observed", workspace_id, {"fact": to_plain(managed_by)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.inferred_facts == {}
    assert state.find_related("web_service", "managed_by") == ["custom_cli"]
    assert state.facts[managed_by.id] == managed_by
    assert state.facts[managed_by.id].inferred is False


def test_get_best_fact_prefers_observed_fact_over_tied_inferred_fact():
    observed_at = utc_now()
    state = StateProjector(EventLedger()).project("ws_empty")
    observed = Fact(
        id="fact_observed",
        subject_id="svc",
        predicate="managed_by",
        value="custom_cli",
        observed_at=observed_at,
        confidence=0.6,
    )
    inferred = Fact(
        id="fact_inferred",
        subject_id="svc",
        predicate="managed_by",
        value="docker_container_lifecycle",
        observed_at=observed_at,
        confidence=0.6,
        inferred=True,
    )
    state.facts = {observed.id: observed, inferred.id: inferred}

    assert state.get_best_fact("svc", "managed_by") == observed


def test_get_best_fact_selects_highest_confidence_fact():
    observed_at = utc_now()
    state = StateProjector(EventLedger()).project("ws_empty")
    lower = Fact(
        id="fact_lower",
        subject_id="svc",
        predicate="runtime",
        value="docker",
        observed_at=observed_at,
        source_type="provider",
        confidence=0.85,
    )
    higher = Fact(
        id="fact_higher",
        subject_id="svc",
        predicate="runtime",
        value="systemd",
        observed_at=observed_at,
        source_type="discovery",
        confidence=0.95,
    )
    state.facts = {lower.id: lower, higher.id: higher}

    assert state.get_best_fact("svc", "runtime") == higher


def test_relationship_query_helpers_preserve_provenance_when_requested():
    ledger = EventLedger()
    workspace_id = "ws_relationship_provenance"
    observed_at = utc_now()
    fact = Fact(
        id="fact_host",
        subject_id="web_service",
        predicate="host",
        value="example_host",
        evidence_ids=["evd_1"],
        observed_at=observed_at,
        source_type="discovery",
        confidence=0.95,
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})
    state = StateProjector(ledger).project(workspace_id)

    assert state.find_related("web_service", "host", include_provenance=True) == [
        {
            "object": "example_host",
            "fact_id": "fact_host",
            "source_type": "discovery",
            "confidence": 0.95,
            "observed_at": observed_at,
            "evidence_ids": ["evd_1"],
            "inferred": False,
        }
    ]
    assert state.find_entities("host", "example_host", include_provenance=True) == [
        {
            "subject": "web_service",
            "fact_id": "fact_host",
            "source_type": "discovery",
            "confidence": 0.95,
            "observed_at": observed_at,
            "evidence_ids": ["evd_1"],
            "inferred": False,
        }
    ]


def test_inferred_confidence_is_capped_by_source_fact_confidence():
    ledger = EventLedger()
    workspace_id = "ws_inference_confidence_cap"
    observed_at = utc_now()
    runtime = Fact(
        id="fact_runtime_docker",
        subject_id="web_service",
        predicate="runtime",
        value="docker",
        observed_at=observed_at,
        source_type="provider",
        confidence=0.4,
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(runtime)})
    state = StateProjector(ledger).project(workspace_id)

    inferred = state.inferred_facts[
        "fact_inferred_web_service_managed_by_docker_container_lifecycle"
    ]
    assert inferred.source_type == "inferred"
    assert inferred.confidence == 0.4
    assert inferred.confidence <= runtime.confidence


def _projected_state(facts: list[Fact], workspace_id: str = "ws_fact_conflicts"):
    ledger = EventLedger()
    for fact in facts:
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})
    return StateProjector(ledger).project(workspace_id)


def _projected_conflicts(facts: list[Fact]):
    return _projected_state(facts).fact_conflicts


def test_fact_conflicts_no_conflict_for_single_value():
    observed_at = utc_now()
    conflicts = _projected_conflicts(
        [
            Fact(
                id="fact_runtime_docker_1",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_runtime_docker_2",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                confidence=0.95,
            ),
        ]
    )

    assert conflicts == []


def test_fact_conflicts_detects_docker_vs_systemd_equal_confidence_without_winner():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="web_service",
                predicate="runtime",
                value="systemd",
                observed_at=observed_at,
            ),
        ]
    )

    conflict = next(
        conflict for conflict in state.fact_conflicts if conflict.predicate == "runtime"
    )
    assert conflict.subject == "web_service"
    assert conflict.predicate == "runtime"
    assert conflict.values == ["docker", "systemd"]
    assert conflict.winning_value is None
    assert conflict.best_fact_id is None
    assert conflict.conflicting_fact_ids == [
        "fact_runtime_docker",
        "fact_runtime_systemd",
    ]
    assert state.get_best_fact("web_service", "runtime") is None
    assert "multiple values" in conflict.reason


def test_ambiguous_runtime_does_not_infer_managed_by():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.95,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="web_service",
                predicate="runtime",
                value="systemd",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.95,
            ),
        ],
        workspace_id="ws_ambiguous_runtime_no_infer",
    )

    assert state.find_related("web_service", "managed_by") == []
    assert state.inferred_facts == {}


def test_fact_conflicts_two_docker_supports_win_over_one_systemd():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_runtime_docker_1",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.8,
                evidence_ids=["evd_docker_1"],
            ),
            Fact(
                id="fact_runtime_docker_2",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.8,
                evidence_ids=["evd_docker_2"],
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="web_service",
                predicate="runtime",
                value="systemd",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.8,
                evidence_ids=["evd_systemd"],
            ),
        ],
        workspace_id="ws_two_docker_one_systemd",
    )

    conflict = next(
        conflict for conflict in state.fact_conflicts if conflict.predicate == "runtime"
    )
    assert conflict.winning_value == "docker"
    assert conflict.best_fact_id in {"fact_runtime_docker_1", "fact_runtime_docker_2"}
    assert conflict.conflicting_fact_ids == ["fact_runtime_systemd"]
    assert state.get_best_fact("web_service", "runtime").value == "docker"


def test_discovery_docker_wins_over_lower_confidence_user_systemd():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="discovery",
                confidence=0.95,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="web_service",
                predicate="runtime",
                value="systemd",
                observed_at=observed_at,
                source_type="user",
                confidence=0.9,
            ),
        ],
        workspace_id="ws_discovery_docker_user_systemd",
    )

    conflict = next(
        conflict for conflict in state.fact_conflicts if conflict.predicate == "runtime"
    )
    assert conflict.winning_value == "docker"
    assert conflict.best_fact_id == "fact_runtime_docker"
    assert conflict.conflicting_fact_ids == ["fact_runtime_systemd"]
    assert state.get_best_fact("web_service", "runtime").value == "docker"


def test_fact_conflicts_selects_highest_confidence_as_best():
    observed_at = utc_now()
    conflicts = _projected_conflicts(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                confidence=0.8,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="web_service",
                predicate="runtime",
                value="systemd",
                observed_at=observed_at,
                confidence=0.95,
            ),
        ]
    )

    assert conflicts[0].best_fact_id == "fact_runtime_systemd"
    assert conflicts[0].conflicting_fact_ids == ["fact_runtime_docker"]


def test_fact_conflicts_lower_confidence_inferred_fact_loses_to_observed_fact():
    observed_at = utc_now()
    state = StateProjector(EventLedger()).project("ws_empty")
    observed = Fact(
        id="fact_observed_runtime",
        subject_id="web_service",
        predicate="runtime",
        value="docker",
        observed_at=observed_at,
        confidence=0.9,
    )
    inferred = Fact(
        id="fact_inferred_runtime",
        subject_id="web_service",
        predicate="runtime",
        value="systemd",
        observed_at=observed_at,
        confidence=0.6,
        inferred=True,
    )
    state.facts = {observed.id: observed, inferred.id: inferred}

    from seed_runtime.state import _project_fact_conflicts

    state.fact_conflicts = _project_fact_conflicts(state)

    assert state.fact_conflicts[0].best_fact_id == "fact_observed_runtime"
    assert state.fact_conflicts[0].conflicting_fact_ids == ["fact_inferred_runtime"]


def test_fact_conflicts_preserves_provenance():
    observed_at = utc_now()
    conflicts = _projected_conflicts(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="web_service",
                predicate="runtime",
                value="docker",
                evidence_ids=["evd_docker"],
                observed_at=observed_at,
                confidence=0.95,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="web_service",
                predicate="runtime",
                value="systemd",
                evidence_ids=["evd_systemd"],
                observed_at=observed_at,
                confidence=0.9,
            ),
        ]
    )

    conflict = conflicts[0]
    assert conflict.best_fact_id == "fact_runtime_docker"
    assert conflict.conflicting_fact_ids == ["fact_runtime_systemd"]


def test_alias_observation_does_not_resolve_endpoint_fact_to_host_subject():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_alias_example_host_instance",
                subject_id="example_host",
                predicate="alias",
                value="192.0.2.115:9100",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_prometheus_up",
                subject_id="192.0.2.115:9100",
                predicate="up",
                value=1,
                observed_at=observed_at,
                source_type="provider",
                confidence=0.95,
            ),
        ],
        workspace_id="ws_alias_best_fact",
    )

    assert state.get_best_fact("example_host", "up") is None
    best = state.get_best_fact("192.0.2.115:9100", "up")
    assert best is not None
    assert best.id == "fact_prometheus_up"
    assert state.entity_aliases == []


def test_prometheus_instance_observation_does_not_resolve_endpoint_fact_to_host():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_prometheus_instance",
                subject_id="example_host",
                predicate="prometheus_instance",
                value="192.0.2.115:9100",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_prometheus_up",
                subject_id="192.0.2.115:9100",
                predicate="up",
                value=1,
                observed_at=observed_at,
                source_type="provider",
                confidence=0.95,
            ),
        ],
        workspace_id="ws_prometheus_instance_best_fact",
    )

    assert state.get_best_fact("example_host", "up") is None
    assert state.get_best_fact("192.0.2.115:9100", "up").id == "fact_prometheus_up"


def test_exact_subject_query_can_disable_alias_resolution():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_alias_example_host_instance",
                subject_id="example_host",
                predicate="alias",
                value="192.0.2.115:9100",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_prometheus_up",
                subject_id="192.0.2.115:9100",
                predicate="up",
                value=1,
                observed_at=observed_at,
            ),
        ],
        workspace_id="ws_alias_exact_mode",
    )

    assert state.get_best_fact("192.0.2.115:9100", "up") is not None
    assert state.get_best_fact("example_host", "up", resolve_aliases=False) is None


def test_unrelated_ip_does_not_merge_without_explicit_alias():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_alias_example_host_instance",
                subject_id="example_host",
                predicate="alias",
                value="192.0.2.115:9100",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_unrelated_up",
                subject_id="192.168.254.116:9100",
                predicate="up",
                value=1,
                observed_at=observed_at,
            ),
        ],
        workspace_id="ws_alias_no_unrelated_merge",
    )

    assert state.get_best_fact("example_host", "up") is None


def test_endpoint_and_host_measurements_remain_separate_without_identity_alias():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_alias_example_host_instance",
                subject_id="example_host",
                predicate="alias",
                value="192.0.2.115:9100",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_node_up",
                subject_id="example_host",
                predicate="up",
                value=0,
                observed_at=observed_at,
                source_type="user",
                confidence=0.7,
            ),
            Fact(
                id="fact_prometheus_up",
                subject_id="192.0.2.115:9100",
                predicate="up",
                value=1,
                observed_at=observed_at,
                source_type="provider",
                confidence=0.95,
            ),
        ],
        workspace_id="ws_alias_conflicts",
    )

    assert not any(conflict.predicate == "up" for conflict in state.fact_conflicts)
    assert "fact_node_up" in state.facts
    assert state.get_best_fact("example_host", "up").id == "fact_node_up"
    assert (
        state.get_best_fact("192.0.2.115:9100", "up").id
        == "fact_prometheus_up"
    )


def test_projector_derives_entity_types_from_facts_and_relationships():
    ledger = EventLedger()
    workspace_id = "ws_entity_types"
    observed_at = utc_now()

    def fact(fact_id, subject, predicate, value):
        return Fact(
            id=fact_id,
            subject_id=subject,
            predicate=predicate,
            value=value,
            evidence_ids=[],
            observed_at=observed_at,
        )

    facts = [
        fact("fact_ansible", "example_host", "ansible_host", "192.168.1.115"),
        fact("fact_ip", "example_host", "ip_address", "192.168.1.115"),
        fact("fact_os", "example_host", "os", "linux"),
        fact("fact_group", "example_host", "group", "servers"),
        fact("fact_runs", "web_service", "runs_on", "example_host"),
        fact("fact_monitor", "example_host", "prometheus_instance", "example_host:9100"),
        fact("fact_capability", "example_host", "provides", "ssh_access"),
        fact("fact_endpoint", "192.168.1.115:8096", "status", "up"),
    ]
    for observed_fact in facts:
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(observed_fact)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.get_current_entity_types("example_host") == ["host"]
    assert state.get_current_entity_types("servers") == ["group"]
    assert state.get_current_entity_types("web_service") == ["service"]
    assert state.get_current_entity_types("prometheus") == ["monitoring_system"]
    assert state.get_current_entity_types("ssh_access") == ["capability"]
    assert state.get_current_entity_types("192.168.1.115:8096") == ["endpoint"]
    assert any(
        assertion.source_fact_id == "fact_os"
        for assertion in state.get_entity_type_assertions("example_host")
    )
    assert any(
        assertion.source_relationship_id
        for assertion in state.get_entity_type_assertions("servers")
    )


def test_equal_confidence_equal_support_entity_types_remain_ambiguous():
    ledger = EventLedger()
    workspace_id = "ws_entity_type_ambiguity"
    observed_at = utc_now()
    facts = [
        Fact(
            id="fact_host",
            subject_id="api:8080",
            predicate="os",
            value="linux",
            evidence_ids=[],
            observed_at=observed_at,
            confidence=0.8,
        ),
        Fact(
            id="fact_endpoint",
            subject_id="api:8080",
            predicate="status",
            value="up",
            evidence_ids=[],
            observed_at=observed_at,
            confidence=0.8,
        ),
    ]
    for fact in facts:
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.get_current_entity_types("api:8080") == ["endpoint", "host"]


def test_entity_type_selection_uses_confidence_then_support_count():
    ledger = EventLedger()
    workspace_id = "ws_entity_type_support"
    observed_at = utc_now()
    facts = [
        Fact(
            id="fact_host",
            subject_id="worker",
            predicate="os",
            value="linux",
            evidence_ids=[],
            observed_at=observed_at,
            confidence=0.8,
        ),
        Fact(
            id="fact_service_a",
            subject_id="worker",
            predicate="runs_on",
            value="node-a",
            evidence_ids=[],
            observed_at=observed_at,
            confidence=0.8,
        ),
        Fact(
            id="fact_service_b",
            subject_id="worker",
            predicate="runs_on",
            value="node-b",
            evidence_ids=[],
            observed_at=observed_at,
            confidence=0.8,
        ),
    ]
    for fact in facts:
        ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.get_current_entity_types("worker") == ["service"]
