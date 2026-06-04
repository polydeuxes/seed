from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.explanations import ExplanationBuilder
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

NOW = datetime(2026, 6, 4, tzinfo=timezone.utc)


def _fact(
    fact_id: str,
    subject: str,
    predicate: str,
    value: object,
    *,
    source_type: str = "provider",
    confidence: float = 0.85,
    evidence_ids: list[str] | None = None,
    inferred: bool = False,
    inference_rule_id: str | None = None,
    source_fact_id: str | None = None,
    confidence_cap: float | None = None,
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
        inferred=inferred,
        inference_rule_id=inference_rule_id,
        source_fact_id=source_fact_id,
        confidence_cap=confidence_cap,
    )


def _state(*facts: Fact):
    ledger = EventLedger()
    for fact in facts:
        ledger.append(
            "fact.inferred" if fact.inferred else "fact.observed",
            "ws",
            {"fact": to_plain(fact)},
        )
    return StateProjector(ledger).project("ws")


def test_observed_fact_explanation():
    fact = _fact(
        "fact_obs_1",
        "node115",
        "architecture",
        "x86_64",
        confidence=0.82,
        evidence_ids=["evd_1"],
    )

    explanation = ExplanationBuilder(_state(fact)).why("node115", "architecture")

    assert explanation.status == "current"
    support = explanation.current_beliefs[0].facts[0]
    assert support.fact_id == "fact_obs_1"
    assert support.evidence_ids == ["evd_1"]
    assert support.source_type == "provider"
    assert support.confidence == 0.82
    assert support.observed_at == NOW


def test_inferred_fact_explanation_includes_rule_and_source_fact():
    runtime = _fact("fact_runtime", "jellyfin", "runtime", "docker", confidence=0.9)

    explanation = ExplanationBuilder(_state(runtime)).why("jellyfin", "managed_by")

    support = explanation.current_beliefs[0].facts[0]
    assert support.inference_rule_id == "runtime_docker_managed_by_container_lifecycle"
    assert support.inference_rule is not None
    assert support.inference_rule.target_predicate == "managed_by"
    assert support.source_fact_id == runtime.id
    assert support.source_fact is not None
    assert support.source_fact.predicate == "runtime"
    assert support.source_fact.value == "docker"


def test_alias_resolved_explanation_has_resolution_chain():
    facts = [
        _fact("fact_alias_ip", "node115", "alias", "192.168.254.115"),
        _fact(
            "fact_alias_endpoint",
            "192.168.254.115",
            "alias",
            "192.168.254.115:9100",
        ),
        _fact(
            "fact_availability",
            "192.168.254.115:9100",
            "availability_status",
            "down",
        ),
    ]

    explanation = ExplanationBuilder(_state(*facts)).why(
        "node115", "availability_status"
    )

    assert explanation.current_beliefs[0].facts[0].resolution_chain == [
        "node115",
        "192.168.254.115",
        "192.168.254.115:9100",
    ]


def test_ambiguous_runtime_explanation_returns_competing_supported_values():
    explanation = ExplanationBuilder(
        _state(
            _fact("fact_docker", "jellyfin", "runtime", "docker"),
            _fact("fact_systemd", "jellyfin", "runtime", "systemd"),
        )
    ).why("jellyfin", "runtime")

    assert explanation.status == "ambiguous"
    assert explanation.current_beliefs == []
    assert [belief.value for belief in explanation.competing_beliefs] == [
        "docker",
        "systemd",
    ]
    assert explanation.conflicts[0].winning_value is None


def test_multi_valued_alias_explanation_returns_all_values_and_support():
    explanation = ExplanationBuilder(
        _state(
            _fact("fact_alias_ip", "node115", "alias", "192.168.254.115"),
            _fact(
                "fact_alias_endpoint",
                "node115",
                "alias",
                "192.168.254.115:9100",
            ),
        )
    ).why("node115", "alias")

    assert explanation.status == "current"
    assert [belief.value for belief in explanation.current_beliefs] == [
        "192.168.254.115",
        "192.168.254.115:9100",
    ]
    assert [belief.supporting_fact_ids for belief in explanation.current_beliefs] == [
        ["fact_alias_ip"],
        ["fact_alias_endpoint"],
    ]


def test_explanation_survives_sqlite_reopen(tmp_path):
    path = tmp_path / "seed.sqlite"
    ledger = SQLiteEventLedger(str(path))
    ledger.append(
        "fact.observed",
        "ws",
        {
            "fact": to_plain(
                _fact(
                    "fact_persisted",
                    "node115",
                    "architecture",
                    "x86_64",
                    evidence_ids=["evd_persisted"],
                )
            )
        },
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        explanation = ExplanationBuilder(StateProjector(reopened).project("ws")).why(
            "node115", "architecture"
        )
    finally:
        reopened.close()

    assert explanation.current_beliefs[0].supporting_fact_ids == ["fact_persisted"]
    assert explanation.current_beliefs[0].facts[0].evidence_ids == ["evd_persisted"]


def test_recursive_explanation_chain():
    observed = _fact("fact_observed", "svc", "a", "one")
    first = _fact(
        "fact_first",
        "svc",
        "b",
        "two",
        source_type="inferred",
        confidence=0.6,
        inferred=True,
        inference_rule_id="a_to_b",
        source_fact_id=observed.id,
    )
    second = _fact(
        "fact_second",
        "svc",
        "c",
        "three",
        source_type="inferred",
        confidence=0.6,
        inferred=True,
        inference_rule_id="b_to_c",
        source_fact_id=first.id,
    )

    explanation = ExplanationBuilder(_state(observed, first, second)).why("svc", "c")

    root = explanation.current_beliefs[0].facts[0]
    assert root.source_fact is not None
    assert root.source_fact.fact_id == first.id
    assert root.source_fact.source_fact is not None
    assert root.source_fact.source_fact.fact_id == observed.id


def test_confidence_cap_explanation():
    runtime = _fact("fact_runtime", "jellyfin", "runtime", "docker", confidence=0.9)

    explanation = ExplanationBuilder(_state(runtime)).why("jellyfin", "managed_by")

    inferred = explanation.current_beliefs[0].facts[0]
    assert inferred.confidence == 0.6
    assert inferred.confidence_cap == 0.6
    assert inferred.source_fact is not None
    assert inferred.source_fact.confidence == 0.9


def test_cli_why_formats_ambiguous_values_and_support(capsys):
    from scripts import seed_local

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "systemd",
                "--why",
                "jellyfin",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "No current belief." in output
    assert "Competing supported values:\n\ndocker\nsystemd" in output
    assert "supporting_fact_ids:" in output
    assert "Conflicts:" in output
