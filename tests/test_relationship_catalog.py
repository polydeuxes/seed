from datetime import datetime, timezone

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.facts import Fact
from seed_runtime.observations import Observation, ObservationIngestor
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


def _project_observation(observation: Observation):
    ledger = EventLedger()
    ObservationIngestor(ledger).ingest(observation, "ws")
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
        "belongs_to_domain",
        "defines",
        "depends_on",
        "member_of",
        "monitored_by",
        "provides",
        "related_to",
        "runs_on",
    ]
    assert {
        entry.relationship: entry.relationship_kind
        for entry in catalog.list_relationships()
    } == {
        "alias_of": "identity",
        "belongs_to_domain": "grouping",
        "defines": "topology",
        "depends_on": "dependency",
        "member_of": "grouping",
        "monitored_by": "dependency",
        "provides": "dependency",
        "related_to": "topology",
        "runs_on": "hosting",
    }
    assert catalog.get("member_of").derived_from_predicates == ["group"]
    assert catalog.get("depends_on").subject_type == "document"
    assert catalog.get("depends_on").object_type == "document"
    assert catalog.get("related_to").derived_from_predicates == ["related"]
    assert catalog.get("belongs_to_domain").object_type == "domain"
    assert catalog.get("defines").object_type == "concept"
    assert catalog.get("alias_of").derived_from_predicates == [
        "alias",
        "hostname",
        "ip_address",
        "ansible_host",
    ]
    assert catalog.get("provides").derived_from_predicates == [
        "provides",
        "endpoint_role",
    ]


def test_group_alias_prometheus_and_host_facts_do_not_alias_endpoint_instances():
    state = _project(
        _fact("fact_group", "example_host", "group", "servers"),
        _fact("fact_alias", "example_host", "alias", "192.0.2.115"),
        _fact("fact_prom", "example_host", "prometheus_instance", "192.0.2.115:9100"),
        _fact("fact_host", "web_service", "host", "example_host"),
    )

    assert [
        (edge.subject, edge.relationship, edge.object)
        for edge in state.get_relationships()
    ] == [
        ("example_host", "alias_of", "192.0.2.115"),
        ("example_host", "member_of", "servers"),
        ("web_service", "runs_on", "example_host"),
        ("example_host", "monitored_by", "prometheus"),
    ]


def test_self_alias_facts_are_retained_without_projecting_relationships():
    state = _project(
        _fact("fact_hostname", "example_host_f", "hostname", "example_host_f"),
        _fact("fact_self_alias", "example_host_f", "alias", "example_host_f"),
        _fact("fact_ip_alias", "example_host_f", "alias", "192.0.2.200"),
    )

    assert set(state.facts) == {"fact_hostname", "fact_self_alias", "fact_ip_alias"}
    assert [
        (edge.subject, edge.relationship, edge.object)
        for edge in state.get_relationships()
    ] == [("example_host_f", "alias_of", "192.0.2.200")]
    assert seed_local.state_summary(state)["graph_issue_count"] == 0


def test_relationship_preserves_source_fact_provenance_and_is_deterministic():
    fact = _fact("fact_group", "example_host", "group", "servers")

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
        _fact("fact_group_1", "example_host", "group", "servers"),
        _fact("fact_group_2", "example_host_e", "group", "servers"),
        _fact("fact_host", "web_service", "host", "example_host"),
    )

    assert len(state.get_relationships(relationship="member_of")) == 2
    assert state.find_related("web_service", "runs_on") == ["example_host"]
    assert state.find_subjects("member_of", "servers") == ["example_host", "example_host_e"]
    assert state.get_relationships(subject="example_host", object="servers")[0].relationship == "member_of"
    assert [
        edge.relationship for edge in state.get_relationships(relationship_kind="hosting")
    ] == ["runs_on"]


def test_dependency_traversal_uses_relationship_semantics():
    state = _project(
        _fact("fact_alias", "example_host", "alias", "primary-host"),
        _fact("fact_group", "example_host", "group", "servers"),
        _fact("fact_host", "web_service", "host", "example_host"),
        _fact("fact_prom", "example_host", "prometheus_instance", "example_host:9100"),
    )

    assert state.find_dependencies("web_service") == ["example_host", "prometheus"]
    assert state.find_dependents("prometheus") == ["example_host", "web_service"]
    assert "primary-host" not in state.find_dependencies("example_host")
    assert "servers" not in state.find_dependencies("example_host")


def test_sqlite_reopen_preserves_relationship_projection(tmp_path):
    path = tmp_path / "relationships.sqlite"
    ledger = SQLiteEventLedger(str(path))
    fact = _fact("fact_group", "example_host", "group", "servers")
    ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    expected = StateProjector(ledger).project("ws").get_relationships()
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        actual = StateProjector(reopened).project("ws").get_relationships()
    finally:
        reopened.close()

    assert actual == expected
    assert actual[0].relationship_kind == "grouping"


def test_state_summary_optionally_includes_relationship_count():
    state = _project(_fact("fact_group", "example_host", "group", "servers"))

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
        {"fact": to_plain(_fact("fact_group", "example_host", "group", "servers"))},
    )
    ledger.append(
        "fact.observed",
        seed_local.DEFAULT_WORKSPACE,
        {"fact": to_plain(_fact("fact_host", "web_service", "host", "example_host"))},
    )
    ledger.close()

    assert seed_local.main(
        [
            "--db",
            str(path),
            "--relationships",
            "--relationship-subject",
            "example_host",
            "--relationship",
            "member_of",
            "--relationship-object",
            "servers",
        ]
    ) == 0

    assert capsys.readouterr().out == "example_host member_of servers\n"


def test_endpoint_role_projects_provides_relationship_for_non_prometheus_facts():
    state = _project(
        _fact(
            "fact_endpoint_role",
            "192.0.2.115:9100",
            "endpoint_role",
            "node-exporter",
        )
    )

    assert [
        (edge.subject, edge.relationship, edge.object)
        for edge in state.get_relationships()
    ] == [("192.0.2.115:9100", "provides", "node-exporter")]
    assert state.get_current_entity_types("192.0.2.115:9100") == ["endpoint"]
    assert state.get_current_entity_types("node-exporter") == ["capability"]
    assert state.get_graph_issues() == []


def test_endpoint_role_projects_provides_relationship_for_non_prometheus_observations():
    state = _project_observation(
        Observation(
            id="obs_custom_endpoint_role",
            source_type="provider",
            observed_at=NOW,
            subject="192.0.2.115:9100",
            predicate="endpoint_role",
            value="node-exporter",
            metadata={"source_name": "custom_inventory"},
        )
    )

    assert [
        (edge.subject, edge.relationship, edge.object)
        for edge in state.get_relationships()
    ] == [("192.0.2.115:9100", "provides", "node-exporter")]
    assert state.get_current_entity_types("192.0.2.115:9100") == ["endpoint"]
    assert state.get_current_entity_types("node-exporter") == ["capability"]
    assert state.get_graph_issues() == []


def test_prometheus_instance_does_not_project_monitored_by_for_prometheus_observations():
    state = _project_observation(
        Observation(
            id="obs_prometheus_instance",
            source_type="provider",
            observed_at=NOW,
            subject="example_host",
            predicate="prometheus_instance",
            value="192.0.2.115:9100",
            metadata={"source_name": "prometheus"},
        )
    )

    assert [
        (fact.subject_id, fact.predicate, fact.value) for fact in state.facts.values()
    ] == [("example_host", "prometheus_instance", "192.0.2.115:9100")]
    assert state.get_relationships() == []
    assert state.get_graph_issues() == []


def test_non_prometheus_instance_facts_still_project_existing_monitored_by_relationship():
    state = _project(
        _fact("fact_prom", "example_host", "prometheus_instance", "example_host:9100")
    )

    assert [
        (edge.subject, edge.relationship, edge.object)
        for edge in state.get_relationships()
    ] == [("example_host", "monitored_by", "prometheus")]


def test_prometheus_endpoint_role_does_not_project_provides_relationship():
    state = _project_observation(
        Observation(
            id="obs_prometheus_endpoint_role",
            source_type="provider",
            observed_at=NOW,
            subject="192.0.2.115:9100",
            predicate="endpoint_role",
            value="node-exporter",
            metadata={"source_name": "prometheus"},
        )
    )

    assert [
        (fact.subject_id, fact.predicate, fact.value) for fact in state.facts.values()
    ] == [("192.0.2.115:9100", "endpoint_role", "node-exporter")]
    assert state.get_relationships() == []
    assert state.get_current_entity_types("192.0.2.115:9100") == ["endpoint"]
    assert state.get_entity_type_assertions("node-exporter") == []
    assert state.get_graph_issues() == []
