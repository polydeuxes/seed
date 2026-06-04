from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.facts import Fact
from seed_runtime.relationship_catalog import RelationshipCatalog
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from scripts import seed_local


NOW = datetime(2026, 6, 4, 12, 0, tzinfo=timezone.utc)


def _project(*facts: Fact):
    ledger = EventLedger()
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(ledger).project("ws")


def _fact(fact_id: str, subject: str, predicate: str, value: str) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        source_type="imported",
        confidence=0.91,
        observed_at=NOW,
        evidence_ids=["evidence_1"],
    )


def test_core_catalog_contains_initial_relationship_vocabulary():
    catalog = RelationshipCatalog.load()

    assert [entry.relationship for entry in catalog.list_relationships()] == [
        "alias_of",
        "member_of",
        "monitored_by",
        "provides",
        "runs_on",
    ]
    assert catalog.get("member_of").derived_from_predicates == ["group"]


def test_group_alias_prometheus_and_host_facts_create_relationships():
    state = _project(
        _fact("fact_group", "node115", "group", "servers"),
        _fact("fact_alias", "node115", "alias", "192.168.254.115"),
        _fact("fact_prom", "node115", "prometheus_instance", "192.168.254.115:9100"),
        _fact("fact_host", "jellyfin", "host", "node115"),
    )

    assert [
        (edge.subject, edge.relationship, edge.object)
        for edge in state.get_relationships()
    ] == [
        ("node115", "alias_of", "192.168.254.115"),
        ("node115", "member_of", "servers"),
        ("jellyfin", "runs_on", "node115"),
        ("node115", "alias_of", "192.168.254.115:9100"),
        ("node115", "monitored_by", "prometheus"),
    ]


def test_relationship_preserves_source_fact_provenance_and_is_deterministic():
    fact = _fact("fact_group", "node115", "group", "servers")

    first = _project(fact).get_relationships()[0]
    second = _project(fact).get_relationships()[0]

    assert first == second
    assert first.source_fact_id == fact.id
    assert first.source_type == fact.source_type
    assert first.confidence == fact.confidence
    assert first.observed_at == fact.observed_at
    assert first.metadata["evidence_ids"] == ["evidence_1"]


def test_relationship_query_helpers_filter_edges():
    state = _project(
        _fact("fact_group_1", "node115", "group", "servers"),
        _fact("fact_group_2", "node210", "group", "servers"),
        _fact("fact_host", "jellyfin", "host", "node115"),
    )

    assert len(state.get_relationships(relationship="member_of")) == 2
    assert state.find_related("jellyfin", "runs_on") == ["node115"]
    assert state.find_subjects("member_of", "servers") == ["node115", "node210"]
    assert state.get_relationships(subject="node115", object="servers")[0].relationship == "member_of"


def test_sqlite_reopen_preserves_relationship_projection(tmp_path):
    path = tmp_path / "relationships.sqlite"
    ledger = SQLiteEventLedger(str(path))
    fact = _fact("fact_group", "node115", "group", "servers")
    ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    expected = StateProjector(ledger).project("ws").get_relationships()
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        actual = StateProjector(reopened).project("ws").get_relationships()
    finally:
        reopened.close()

    assert actual == expected


def test_state_summary_optionally_includes_relationship_count():
    state = _project(_fact("fact_group", "node115", "group", "servers"))

    assert "relationship_count" not in seed_local.state_summary(state)
    summary = seed_local.state_summary(state, include_relationship_count=True)

    assert summary["relationship_count"] == 1
    assert "relationships: 1" in seed_local.format_state_summary(summary)


def test_cli_relationship_filters_print_projected_edges(tmp_path, capsys):
    path = tmp_path / "relationships-cli.sqlite"
    ledger = SQLiteEventLedger(str(path))
    ledger.append(
        "fact.observed",
        seed_local.DEFAULT_WORKSPACE,
        {"fact": to_plain(_fact("fact_group", "node115", "group", "servers"))},
    )
    ledger.append(
        "fact.observed",
        seed_local.DEFAULT_WORKSPACE,
        {"fact": to_plain(_fact("fact_host", "jellyfin", "host", "node115"))},
    )
    ledger.close()

    assert seed_local.main(
        [
            "--db",
            str(path),
            "--relationships",
            "--relationship-subject",
            "node115",
            "--relationship",
            "member_of",
            "--relationship-object",
            "servers",
        ]
    ) == 0

    assert capsys.readouterr().out == "node115 member_of servers\n"
