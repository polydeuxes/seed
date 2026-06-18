from datetime import datetime, timezone

from scripts import seed_local
from seed_runtime.entity_type_catalog import EntityTypeCatalog, EntityTypeDefinition
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.projection_store import (
    ProjectionSnapshot,
    SQLiteProjectionStore,
    STATE_PROJECTION_NAME,
    STATE_PROJECTION_VERSION,
    state_to_payload,
)
from seed_runtime.relationship_catalog import RelationshipCatalog
from seed_runtime.models import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import GraphValidationIssue, GraphValidator, State, StateProjector

NOW = datetime(2026, 6, 4, 12, 0, tzinfo=timezone.utc)


def _fact(fact_id: str, subject: str, predicate: str, value: str) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        source_type="imported",
        confidence=0.9,
        observed_at=NOW,
        evidence_ids=[],
    )


def _project(*facts: Fact):
    ledger = EventLedger()
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(ledger).project("ws")


def test_relationship_catalog_expected_types_exist_in_entity_type_catalog():
    relationship_catalog = RelationshipCatalog.load()
    entity_type_catalog = EntityTypeCatalog.load()

    missing = sorted(
        {
            expected_type
            for relationship in relationship_catalog.list_relationships()
            for expected_type in (relationship.subject_type, relationship.object_type)
            if expected_type != "entity" and entity_type_catalog.get(expected_type) is None
        }
    )

    assert missing == []


def test_document_concept_domain_are_loaded_entity_types():
    entity_type_catalog = EntityTypeCatalog.load()

    assert entity_type_catalog.get("document") is not None
    assert entity_type_catalog.get("concept") is not None
    assert entity_type_catalog.get("domain") is not None


def test_defines_no_longer_emits_unknown_catalog_type_when_catalog_types_exist():
    state = _project(_fact("defines_fact", "module.py", "defines", "BaseModel"))

    assert len(state.graph_issues) == 1
    issue = state.graph_issues[0]
    assert issue.relationship == "defines"
    assert "unknown catalog type" not in issue.reason
    assert issue.reason == (
        "subject type is unknown; expected document; "
        "object type is unknown; expected concept"
    )
    assert issue.expected_subject_types == ["document"]
    assert issue.expected_object_types == ["concept"]
    assert issue.actual_subject_types == ["unknown"]
    assert issue.actual_object_types == ["unknown"]


def test_unknown_catalog_type_warning_still_emits_for_true_missing_expected_type():
    relationship_catalog = RelationshipCatalog.load()
    entity_type_catalog = EntityTypeCatalog(
        EntityTypeDefinition(entity_type=name) for name in ["unknown", "concept"]
    )
    state = _project(_fact("defines_fact", "module.py", "defines", "BaseModel"))

    issues = GraphValidator(relationship_catalog, entity_type_catalog).validate(state)

    assert len(issues) == 1
    assert issues[0].reason == (
        "subject expects unknown catalog type document; "
        "object type is unknown; expected concept"
    )


def test_valid_host_member_of_group_has_no_issue():
    state = _project(
        _fact("host_type", "node", "os", "linux"),
        _fact("membership", "node", "group", "servers"),
    )

    assert state.graph_issues == []


def test_valid_service_runs_on_host_has_no_issue():
    state = _project(
        _fact("host_type", "node", "os", "linux"),
        _fact("hosting", "api", "runs_on", "node"),
    )

    assert state.graph_issues == []


def test_group_runs_on_host_is_error():
    state = _project(
        _fact("host_type", "node", "os", "linux"),
        _fact("group_type", "member", "group", "workers"),
        _fact("bad_hosting", "workers", "runs_on", "node"),
    )

    issue = next(issue for issue in state.graph_issues if issue.subject == "workers")
    assert issue.severity == "error"
    assert issue.relationship == "runs_on"
    assert issue.expected_subject_types == ["service"]
    assert issue.actual_subject_types == ["group", "service"]
    assert "subject type is group; expected service" in issue.reason


def test_self_alias_is_suppressed_without_a_graph_issue():
    state = _project(
        _fact("self_alias", "node", "alias", "node"),
        _fact("other_alias", "node", "alias", "node.example"),
    )

    assert state.graph_issues == []
    assert [
        (edge.subject, edge.relationship, edge.object)
        for edge in state.get_relationships()
    ] == [("node", "alias_of", "node.example")]
    assert "self_alias" in state.facts


def test_unknown_entity_type_is_warning():
    state = _project(_fact("membership", "mystery", "group", "servers"))

    assert len(state.graph_issues) == 1
    assert state.graph_issues[0].severity == "warning"
    assert state.graph_issues[0].actual_subject_types == ["unknown"]


def test_unknown_monitored_by_subject_is_warning():
    state = _project(
        _fact("prometheus_alias", "mystery", "prometheus_instance", "mystery:9100")
    )

    assert len(state.graph_issues) == 1
    issue = state.graph_issues[0]
    assert issue.severity == "warning"
    assert issue.subject == "mystery"
    assert issue.relationship == "monitored_by"
    assert issue.actual_subject_types == ["unknown"]
    assert issue.hint == (
        "Add inventory or alias evidence if this monitored endpoint should map to a "
        "known host."
    )


def test_other_graph_warning_has_no_hint():
    state = _project(_fact("membership", "mystery", "group", "servers"))

    assert len(state.graph_issues) == 1
    assert state.graph_issues[0].hint is None


def test_duplicate_monitored_by_warnings_collapse_and_preserve_relationship_ids():
    state = _project(
        _fact(
            "node_exporter", "example_host", "prometheus_instance", "example_host:9100"
        ),
        _fact("cadvisor", "example_host", "prometheus_instance", "example_host:8080"),
    )

    assert len(state.graph_issues) == 1
    issue = state.graph_issues[0]
    assert (issue.subject, issue.relationship, issue.object) == (
        "example_host",
        "monitored_by",
        "prometheus",
    )
    assert issue.severity == "warning"
    assert issue.reason == "subject type is unknown; expected host"
    matching_edges = [
        edge for edge in state.relationships if edge.relationship == "monitored_by"
    ]
    assert issue.relationship_ids == [edge.id for edge in matching_edges]
    assert issue.source_fact_ids == [edge.source_fact_id for edge in matching_edges]


def test_provides_accepts_any_subject_entity_type():
    state = _project(
        _fact("host_type", "api:8080", "os", "linux"),
        _fact("endpoint_type", "api:8080", "status", "up"),
        _fact("capability", "api:8080", "provides", "http"),
    )

    assert state.graph_issues == []


def test_sqlite_reopen_preserves_graph_validation_result(tmp_path):
    path = tmp_path / "graph-validation.sqlite"
    ledger = SQLiteEventLedger(str(path))
    for fact in (
        _fact("host_type", "node", "os", "linux"),
        _fact("group_type", "member", "group", "workers"),
        _fact("bad_hosting", "workers", "runs_on", "node"),
    ):
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    expected = StateProjector(ledger).project("ws").graph_issues
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        actual = StateProjector(reopened).project("ws").graph_issues
    finally:
        reopened.close()

    assert actual == expected


def test_graph_issues_cli_and_state_summary(tmp_path, capsys):
    path = tmp_path / "graph-validation-cli.sqlite"
    ledger = SQLiteEventLedger(str(path))
    ledger.append(
        "fact.observed",
        seed_local.DEFAULT_WORKSPACE,
        {"fact": to_plain(_fact("membership", "mystery", "group", "servers"))},
    )
    ledger.close()

    assert seed_local.main(["--db", str(path), "--graph-issues"]) == 0
    output = capsys.readouterr().out
    assert "warning: mystery member_of servers" in output
    assert "subject type is unknown; expected host" in output

    assert (
        seed_local.main(["--db", str(path), "--graph-issues", "--severity", "warning"])
        == 0
    )
    assert "warning: mystery member_of servers" in capsys.readouterr().out

    assert (
        seed_local.main(["--db", str(path), "--graph-issues", "--severity", "error"])
        == 0
    )
    assert capsys.readouterr().out == "no error graph issues\n"

    state = _project(_fact("membership", "mystery", "group", "servers"))
    summary = seed_local.state_summary(state)
    assert summary["graph_issue_count"] == 1
    assert summary["graph_issue_warning_count"] == 1
    assert summary["graph_issue_error_count"] == 0
    assert "graph issues: 1 warning, 0 errors" in seed_local.format_state_summary(
        summary
    )


def test_state_summary_separates_graph_warnings_and_errors():
    state = _project(
        _fact("unknown_membership", "mystery", "group", "servers"),
        _fact("host_type", "node", "os", "linux"),
        _fact("wrong_service_type", "workers", "os", "linux"),
        _fact("bad_hosting", "workers", "runs_on", "node"),
    )

    summary = seed_local.state_summary(state)

    assert summary["graph_issue_count"] == 2
    assert summary["graph_issue_warning_count"] == 1
    assert summary["graph_issue_error_count"] == 1
    assert "graph issues: 1 warning, 1 error" in seed_local.format_state_summary(
        summary
    )


def _graph_issue(
    issue_id,
    severity,
    subject,
    relationship,
    object_,
    reason,
    *,
    source_fact_ids=None,
    relationship_ids=None,
):
    return GraphValidationIssue(
        id=issue_id,
        severity=severity,
        subject=subject,
        relationship=relationship,
        object=object_,
        relationship_ids=list(relationship_ids or [f"rel-{issue_id}"]),
        source_fact_ids=list(source_fact_ids or [f"fact-{issue_id}"]),
        reason=reason,
        hint=None,
        expected_subject_types=["host"],
        actual_subject_types=["unknown"],
        expected_object_types=["group"],
        actual_object_types=["unknown"],
    )


def test_graph_issue_summary_formats_projected_state_groups_and_limits_examples():
    state = State("ws")
    state.graph_issues = [
        _graph_issue(
            "1",
            "warning",
            "node-a",
            "member_of",
            "workers",
            "subject type is unknown; expected host",
        ),
        _graph_issue(
            "2",
            "warning",
            "node-b",
            "member_of",
            "workers",
            "subject type is unknown; expected host",
        ),
        _graph_issue(
            "3",
            "warning",
            "node-c",
            "member_of",
            "workers",
            "subject type is unknown; expected host",
        ),
        _graph_issue(
            "4",
            "error",
            "svc",
            "runs_on",
            "node-a",
            "object type is unknown; expected host",
        ),
    ]

    output = seed_local.format_graph_issue_summary(
        state, category_limit=1, examples_per_category=2
    )

    assert "Graph Issue Summary" in output
    assert "- warnings: 3" in output
    assert "- errors: 1" in output
    assert "- total: 4" in output
    assert "- warning: 3" in output
    assert "- error: 1" in output
    assert (
        "warning | member_of | subject type is unknown; expected host: 3 (75.0% of total)"
        in output
    )
    assert "error | runs_on" not in output
    assert (
        "node-a member_of workers; reason: subject type is unknown; expected host"
        in output
    )
    assert (
        "node-b member_of workers; reason: subject type is unknown; expected host"
        in output
    )
    assert "node-c member_of workers" not in output
    assert "subject types: expected=host actual=unknown" in output
    assert "object types: expected=group actual=unknown" in output
    assert "counts: source_facts=1 relationships=1" in output


def test_graph_issue_summary_does_not_mutate_state():
    state = State("ws")
    state.graph_issues = [
        _graph_issue("1", "warning", "node-a", "member_of", "workers", "reason")
    ]
    before = to_plain(state.graph_issues)

    seed_local.format_graph_issue_summary(state)

    assert to_plain(state.graph_issues) == before


def test_graph_issue_summary_cli_reads_projected_state_and_is_read_only(
    tmp_path, capsys
):
    path = tmp_path / "graph-issue-summary.sqlite"
    ledger = SQLiteEventLedger(str(path))
    ledger.append(
        "fact.observed",
        seed_local.DEFAULT_WORKSPACE,
        {"fact": to_plain(_fact("membership", "mystery", "group", "servers"))},
    )
    before_events = len(ledger.list_events(seed_local.DEFAULT_WORKSPACE))
    ledger.close()

    assert (
        seed_local.main(
            [
                "--db",
                str(path),
                "--graph-issue-summary",
                "--graph-issue-limit",
                "10",
                "--graph-issue-examples",
                "3",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Graph Issue Summary" in output
    assert "- warnings: 1" in output
    assert (
        "warning | member_of | subject type is unknown; expected host: 1 (100.0% of total)"
        in output
    )
    assert (
        "mystery member_of servers; reason: subject type is unknown; expected host"
        in output
    )

    reopened = SQLiteEventLedger(str(path))
    try:
        assert len(reopened.list_events(seed_local.DEFAULT_WORKSPACE)) == before_events
    finally:
        reopened.close()


def test_existing_graph_issues_cli_output_remains_unchanged(tmp_path, capsys):
    path = tmp_path / "graph-issues-unchanged.sqlite"
    ledger = SQLiteEventLedger(str(path))
    ledger.append(
        "fact.observed",
        seed_local.DEFAULT_WORKSPACE,
        {"fact": to_plain(_fact("membership", "mystery", "group", "servers"))},
    )
    ledger.close()

    assert seed_local.main(["--db", str(path), "--graph-issues"]) == 0

    output = capsys.readouterr().out
    assert output.startswith("warning: mystery member_of servers\n")
    assert "Graph Issue Summary" not in output


def test_graph_issue_summary_cli_uses_cached_projected_state_until_rebuilt(
    tmp_path, capsys
):
    path = tmp_path / "graph-issue-summary-cache.sqlite"
    ledger = SQLiteEventLedger(str(path))
    event = ledger.append(
        "fact.observed",
        seed_local.DEFAULT_WORKSPACE,
        {"fact": to_plain(_fact("defines_fact", "module.py", "defines", "BaseModel"))},
    )
    stale_state = StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    stale_state.graph_issues[0] = GraphValidationIssue(
        **{
            **to_plain(stale_state.graph_issues[0]),
            "reason": (
                "subject expects unknown catalog type document; "
                "object expects unknown catalog type concept"
            ),
        }
    )
    store = SQLiteProjectionStore(str(path))
    try:
        store.save_snapshot(
            ProjectionSnapshot(
                workspace_id=seed_local.DEFAULT_WORKSPACE,
                projection_name=STATE_PROJECTION_NAME,
                projection_version=STATE_PROJECTION_VERSION,
                last_event_id=event.id,
                last_event_created_at=event.timestamp,
                state_payload=state_to_payload(stale_state),
                created_at=NOW,
            )
        )
    finally:
        store.close()
        ledger.close()

    assert seed_local.main(["--db", str(path), "--graph-issue-summary"]) == 0
    output = capsys.readouterr().out
    assert "unknown catalog type document" in output

    assert seed_local.main(["--db", str(path), "--rebuild-state-cache"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(path), "--graph-issue-summary"]) == 0
    output = capsys.readouterr().out
    assert "unknown catalog type" not in output
    assert "subject type is unknown; expected document" in output
