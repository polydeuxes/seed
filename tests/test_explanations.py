from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.explanations import ExplanationBuilder
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

NOW = datetime(2026, 6, 4, 12, 0, tzinfo=timezone.utc)


def _fact(
    fact_id: str,
    subject: str,
    predicate: str,
    value: object,
    *,
    source_type: str = "provider",
    confidence: float = 0.9,
    evidence_ids: list[str] | None = None,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        source_type=source_type,
        confidence=confidence,
        evidence_ids=evidence_ids or [],
        observed_at=NOW,
    )


def _state(
    facts: list[Fact],
    *,
    ledger: EventLedger | None = None,
):
    ledger = ledger or EventLedger()
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(
        ledger,
    ).project("ws")


def test_observed_fact_explanation_includes_provenance():
    state = _state([_fact("fact_obs_1", "node", "os", "linux", evidence_ids=["evd_1"])])

    explanation = ExplanationBuilder(state).why("node", "os")

    belief = explanation.current_beliefs[0]
    fact = belief.facts[0]
    assert belief.supporting_fact_ids == ["fact_obs_1"]
    assert belief.evidence_ids == ["evd_1"]
    assert fact.source_type == "provider"
    assert fact.observed_confidence == 0.9
    assert fact.observed_at == NOW.isoformat()


def test_inferred_fact_explanation_recurses_to_observed_source():
    state = _state(
        [_fact("fact_obs_down", "node:9100", "availability_status", "down")]
    )

    explanation = ExplanationBuilder(state).why("node:9100", "health_status")

    inferred = explanation.current_beliefs[0].facts[0]
    assert inferred.inference_rule_id == "availability_down_health_degraded"
    assert inferred.source_fact_id == "fact_obs_down"
    assert inferred.source_fact is not None
    assert inferred.source_fact.observed_confidence == 0.9


def test_endpoint_scoped_explanation_resolves_only_endpoint():
    state = _state(
        [
            _fact("fact_alias_ip", "node115", "alias", "192.168.254.115"),
            _fact(
                "fact_alias_endpoint",
                "192.168.254.115",
                "alias",
                "192.168.254.115:9100",
            ),
            _fact("fact_status", "192.168.254.115:9100", "availability_status", "down"),
        ]
    )

    explanation = ExplanationBuilder(state).why(
        "192.168.254.115:9100", "health_status"
    )

    observed_source = explanation.current_beliefs[0].facts[0].source_fact
    assert observed_source is not None
    assert observed_source.entity_resolution == ["192.168.254.115:9100"]


def test_ambiguous_runtime_explanation_returns_competing_supported_values():
    state = _state(
        [
            _fact("fact_docker", "jellyfin", "runtime", "docker"),
            _fact("fact_systemd", "jellyfin", "runtime", "systemd"),
        ]
    )

    explanation = ExplanationBuilder(state).why("jellyfin", "runtime")

    assert explanation.status == "ambiguous"
    assert explanation.current_beliefs == []
    assert {item.value for item in explanation.competing_beliefs} == {
        "docker",
        "systemd",
    }
    assert explanation.conflict is not None


def test_multi_valued_alias_explanation_returns_all_current_values():
    state = _state(
        [
            _fact("fact_alias_a", "node", "alias", "node.example"),
            _fact("fact_alias_b", "node", "alias", "10.0.0.1"),
        ]
    )

    explanation = ExplanationBuilder(state).why("node", "alias")

    assert explanation.status == "current"
    assert {item.value for item in explanation.current_beliefs} == {
        "node.example",
        "10.0.0.1",
    }


def test_explanation_survives_sqlite_reopen(tmp_path):
    path = tmp_path / "seed.sqlite"
    ledger = SQLiteEventLedger(str(path))
    ledger.append(
        "fact.observed",
        "ws",
        {
            "fact": to_plain(
                _fact("fact_obs_1", "node", "os", "linux", evidence_ids=["evd_1"])
            )
        },
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    state = StateProjector(reopened).project("ws")
    reopened.close()

    belief = ExplanationBuilder(state).why("node", "os").current_beliefs[0]
    assert belief.supporting_fact_ids == ["fact_obs_1"]
    assert belief.evidence_ids == ["evd_1"]


def test_recursive_explanation_chain_traverses_preserved_source_facts():
    observed = _fact("fact_a", "node", "a", "yes")
    inferred_b = Fact(
        id="fact_b",
        subject_id="node",
        predicate="b",
        value="yes",
        observed_at=NOW,
        inferred=True,
        confidence=0.8,
        source_fact_id="fact_a",
        inference_rule_id="a_to_b",
    )
    inferred_c = Fact(
        id="fact_c",
        subject_id="node",
        predicate="c",
        value="yes",
        observed_at=NOW,
        inferred=True,
        confidence=0.7,
        source_fact_id="fact_b",
        inference_rule_id="b_to_c",
    )
    state = _state([observed, inferred_b, inferred_c])

    explanation = ExplanationBuilder(state).why("node", "c")

    c_fact = explanation.current_beliefs[0].facts[0]
    assert c_fact.inference_rule_id == "b_to_c"
    assert c_fact.source_fact is not None
    assert c_fact.source_fact.inference_rule_id == "a_to_b"
    assert c_fact.source_fact.source_fact is not None
    assert c_fact.source_fact.source_fact.fact_id == "fact_a"


def test_confidence_cap_explanation_identifies_applied_rule_cap():
    state = _state(
        [_fact("fact_runtime", "jellyfin", "runtime", "docker", confidence=0.95)]
    )

    explanation = ExplanationBuilder(state).why("jellyfin", "managed_by")

    inferred = explanation.current_beliefs[0].facts[0]
    assert inferred.inferred_confidence == 0.6
    assert inferred.confidence_cap == 0.6
