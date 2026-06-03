from datetime import datetime, timedelta, timezone

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.serialization import to_plain
from seed_runtime.models import Approval, Entity, Fact, Goal, ToolNeed, utc_now
from seed_runtime.state import StateProjector


def test_projector_rebuilds_state_deterministically():
    ledger = EventLedger()
    workspace_id = "ws_1"
    entity = Entity(id="ent_1", kind="host", name="node-1")
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
    assert first.entities["ent_1"].name == "node-1"
    assert first.facts["fact_1"].value is False
    assert first.goals["goal_1"].status == "active"
    assert first.open_tool_needs[0].name == "install_ssh_server"
    assert first.has_approval("ssh.install", "ent_1") is not None


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
            subject_id="jellyfin",
            predicate="host",
            value="node115",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_runtime",
            subject_id="jellyfin",
            predicate="runtime",
            value="docker",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_container",
            subject_id="jellyfin",
            predicate="container",
            value="jellyfin",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_running",
            subject_id="jellyfin",
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
        ("jellyfin", "host", "node115"),
        ("jellyfin", "runtime", "docker"),
        ("jellyfin", "container", "jellyfin"),
        ("jellyfin", "managed_by", "docker_container_lifecycle"),
    ]


def test_entity_relationship_query_helpers_return_deduped_matches():
    ledger = EventLedger()
    workspace_id = "ws_relationship_queries"
    observed_at = utc_now()
    facts = [
        Fact(
            id="fact_host",
            subject_id="jellyfin",
            predicate="host",
            value="node115",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_runtime",
            subject_id="jellyfin",
            predicate="runtime",
            value="docker",
            evidence_ids=["evt_source"],
            observed_at=observed_at,
        ),
        Fact(
            id="fact_runtime_duplicate",
            subject_id="jellyfin",
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

    assert state.find_related("jellyfin", "host") == ["node115"]
    assert state.find_entities("runtime", "docker") == ["jellyfin", "grafana"]
    assert [
        (relationship.subject, relationship.predicate, relationship.object)
        for relationship in state.get_entity_relationships("node115")
    ] == [("jellyfin", "host", "node115")]


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
        "fact_runtime_docker", "jellyfin", "runtime", "docker", observed_at
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(runtime)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.observed_facts == {runtime.id: runtime}
    assert state.find_related("jellyfin", "managed_by") == [
        "docker_container_lifecycle"
    ]
    inferred = state.inferred_facts[
        "fact_inferred_jellyfin_managed_by_docker_container_lifecycle"
    ]
    assert inferred.inferred is True
    assert inferred.subject_id == "jellyfin"
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
        "fact_runtime_docker", "jellyfin", "runtime", "docker", observed_at
    )
    managed_by = _observed_fact(
        "fact_managed_by_custom", "jellyfin", "managed_by", "custom_cli", observed_at
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(runtime)})
    ledger.append("fact.observed", workspace_id, {"fact": to_plain(managed_by)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.inferred_facts == {}
    assert state.find_related("jellyfin", "managed_by") == ["custom_cli"]
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
        subject_id="jellyfin",
        predicate="host",
        value="node115",
        evidence_ids=["evd_1"],
        observed_at=observed_at,
        source_type="discovery",
        confidence=0.95,
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})
    state = StateProjector(ledger).project(workspace_id)

    assert state.find_related("jellyfin", "host", include_provenance=True) == [
        {
            "object": "node115",
            "fact_id": "fact_host",
            "source_type": "discovery",
            "confidence": 0.95,
            "observed_at": observed_at,
            "evidence_ids": ["evd_1"],
            "inferred": False,
        }
    ]
    assert state.find_entities("host", "node115", include_provenance=True) == [
        {
            "subject": "jellyfin",
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
        subject_id="jellyfin",
        predicate="runtime",
        value="docker",
        observed_at=observed_at,
        source_type="provider",
        confidence=0.4,
    )

    ledger.append("fact.observed", workspace_id, {"fact": to_plain(runtime)})
    state = StateProjector(ledger).project(workspace_id)

    inferred = state.inferred_facts[
        "fact_inferred_jellyfin_managed_by_docker_container_lifecycle"
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
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_runtime_docker_2",
                subject_id="jellyfin",
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
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="jellyfin",
                predicate="runtime",
                value="systemd",
                observed_at=observed_at,
            ),
        ]
    )

    conflict = next(
        conflict for conflict in state.fact_conflicts if conflict.predicate == "runtime"
    )
    assert conflict.subject == "jellyfin"
    assert conflict.predicate == "runtime"
    assert conflict.values == ["docker", "systemd"]
    assert conflict.winning_value is None
    assert conflict.best_fact_id is None
    assert conflict.conflicting_fact_ids == [
        "fact_runtime_docker",
        "fact_runtime_systemd",
    ]
    assert state.get_best_fact("jellyfin", "runtime") is None
    assert "multiple values" in conflict.reason


def test_ambiguous_runtime_does_not_infer_managed_by():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.95,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="jellyfin",
                predicate="runtime",
                value="systemd",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.95,
            ),
        ],
        workspace_id="ws_ambiguous_runtime_no_infer",
    )

    assert state.find_related("jellyfin", "managed_by") == []
    assert state.inferred_facts == {}


def test_fact_conflicts_two_docker_supports_win_over_one_systemd():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_runtime_docker_1",
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.8,
                evidence_ids=["evd_docker_1"],
            ),
            Fact(
                id="fact_runtime_docker_2",
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="provider",
                confidence=0.8,
                evidence_ids=["evd_docker_2"],
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="jellyfin",
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
    assert state.get_best_fact("jellyfin", "runtime").value == "docker"


def test_discovery_docker_wins_over_lower_confidence_user_systemd():
    observed_at = utc_now()
    state = _projected_state(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                source_type="discovery",
                confidence=0.95,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="jellyfin",
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
    assert state.get_best_fact("jellyfin", "runtime").value == "docker"


def test_fact_conflicts_selects_highest_confidence_as_best():
    observed_at = utc_now()
    conflicts = _projected_conflicts(
        [
            Fact(
                id="fact_runtime_docker",
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                observed_at=observed_at,
                confidence=0.8,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="jellyfin",
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
        subject_id="jellyfin",
        predicate="runtime",
        value="docker",
        observed_at=observed_at,
        confidence=0.9,
    )
    inferred = Fact(
        id="fact_inferred_runtime",
        subject_id="jellyfin",
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
                subject_id="jellyfin",
                predicate="runtime",
                value="docker",
                evidence_ids=["evd_docker"],
                observed_at=observed_at,
                confidence=0.95,
            ),
            Fact(
                id="fact_runtime_systemd",
                subject_id="jellyfin",
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
