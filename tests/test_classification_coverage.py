from datetime import datetime, timezone

from scripts import seed_local
from seed_runtime.classification_coverage import (
    build_classification_coverage_diagnostic,
    format_classification_coverage,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.models import Entity
from seed_runtime.models import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

NOW = datetime(2026, 6, 19, 12, 0, tzinfo=timezone.utc)


def _fact(fact_id: str, subject: str, predicate: str, value: object) -> Fact:
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


def _project(*facts: Fact, entities: list[Entity] | None = None):
    ledger = EventLedger()
    for entity in entities or []:
        ledger.append("entity.observed", "ws", {"entity": to_plain(entity)})
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(ledger).project("ws")


def test_classification_coverage_empty_state():
    diagnostic = build_classification_coverage_diagnostic(_project(), observed_at=NOW)

    assert diagnostic.entity_count == 0
    assert diagnostic.classified_entity_count == 0
    assert diagnostic.unknown_entity_count == 0
    assert diagnostic.unknown_percentage == 0.0
    assert "Entity Classification Coverage" in format_classification_coverage(diagnostic)


def test_classification_coverage_fully_classified_entities():
    state = _project(_fact("host_type", "node", "os", "linux"))
    diagnostic = build_classification_coverage_diagnostic(state, observed_at=NOW)

    assert diagnostic.entity_count == 1
    assert diagnostic.classified_entity_count == 1
    assert diagnostic.unknown_entity_count == 0
    assert diagnostic.classification_distribution["host"] == 1


def test_classification_coverage_unknown_entities_present():
    state = _project(_fact("unknown", "mystery", "custom", "value"))
    diagnostic = build_classification_coverage_diagnostic(state, observed_at=NOW)

    assert diagnostic.entity_count == 1
    assert diagnostic.classified_entity_count == 0
    assert diagnostic.unknown_entity_count == 1
    assert diagnostic.unknown_percentage == 100.0
    assert diagnostic.top_unknown_predicates == [("custom", 1)]


def test_classification_coverage_mixed_classification_coverage():
    state = _project(
        _fact("host_type", "node", "os", "linux"),
        _fact("unknown", "mystery", "custom", "value"),
    )
    diagnostic = build_classification_coverage_diagnostic(state, observed_at=NOW)

    assert diagnostic.entity_count == 2
    assert diagnostic.classified_entity_count == 1
    assert diagnostic.unknown_entity_count == 1
    assert diagnostic.unknown_percentage == 50.0


def test_classification_coverage_graph_issue_attribution():
    state = _project(
        _fact("unknown_membership", "mystery", "group", "servers"),
        _fact("host_type", "node", "os", "linux"),
        _fact("bad_hosting", "servers", "runs_on", "node"),
    )
    diagnostic = build_classification_coverage_diagnostic(state, observed_at=NOW)

    assert diagnostic.unknown_subject_graph_issue_count == 1
    assert diagnostic.unknown_object_graph_issue_count == 0
    assert diagnostic.both_unknown_graph_issue_count == 0
    assert diagnostic.concrete_mismatch_graph_issue_count == 1
    assert diagnostic.top_unknown_relationship_categories == [("grouping", 1)]
    assert diagnostic.top_unknown_graph_issue_categories


def test_classification_coverage_default_command_does_not_record(tmp_path, capsys):
    db = tmp_path / "seed.sqlite"
    seed_local.main(["--db", str(db), "--observe", "mystery", "custom", "value"])
    before = len(SQLiteEventLedger(db).list("local"))

    assert seed_local.main(["--db", str(db), "--classification-coverage"]) == 0

    output = capsys.readouterr().out
    after = len(SQLiteEventLedger(db).list("local"))
    assert "Entity Classification Coverage" in output
    assert after == before


def test_classification_coverage_record_appends_self_observation_evidence(tmp_path):
    db = tmp_path / "seed.sqlite"
    seed_local.main(["--db", str(db), "--observe", "mystery", "custom", "value"])
    before_events = SQLiteEventLedger(db).list("local")

    assert seed_local.main(["--db", str(db), "--classification-coverage", "--record"]) == 0

    after_events = SQLiteEventLedger(db).list("local")
    assert len(after_events) > len(before_events)
    observed = [event for event in after_events if event.kind == "observation.observed"]
    assert any(
        event.payload["observation"]["metadata"]["ingested_by"]
        == "scripts.seed_local --classification-coverage --record"
        for event in observed
    )
    assert any(
        event.kind == "fact.inferred"
        and event.payload["fact"]["predicate"] == "diagnostic_name"
        and event.payload["fact"]["value"] == "entity_classification_coverage"
        for event in after_events
    )
