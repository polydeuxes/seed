from datetime import datetime, timezone

from scripts import seed_local
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.models import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

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


def test_self_alias_is_warning_while_other_aliases_are_loose():
    state = _project(
        _fact("self_alias", "node", "alias", "node"),
        _fact("other_alias", "node", "alias", "node.example"),
    )

    assert len(state.graph_issues) == 1
    assert state.graph_issues[0].severity == "warning"
    assert state.graph_issues[0].relationship == "alias_of"
    assert "aliases an entity to itself" in state.graph_issues[0].reason


def test_unknown_entity_type_is_warning():
    state = _project(_fact("membership", "mystery", "group", "servers"))

    assert len(state.graph_issues) == 1
    assert state.graph_issues[0].severity == "warning"
    assert state.graph_issues[0].actual_subject_types == ["unknown"]


def test_ambiguous_entity_type_is_warning():
    state = _project(
        _fact("host_type", "api:8080", "os", "linux"),
        _fact("endpoint_type", "api:8080", "status", "up"),
        _fact("capability", "api:8080", "provides", "http"),
    )

    assert len(state.graph_issues) == 1
    assert state.graph_issues[0].severity == "warning"
    assert state.graph_issues[0].actual_subject_types == ["endpoint", "host"]


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

    state = _project(_fact("membership", "mystery", "group", "servers"))
    summary = seed_local.state_summary(state)
    assert summary["graph_issue_count"] == 1
    assert "graph issues: 1" in seed_local.format_state_summary(summary)
