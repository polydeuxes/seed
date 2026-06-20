import json

import scripts.seed_local as seed_local
from seed_runtime.consumer_dependency_audit import (
    build_consumer_audit,
    format_consumer_audit,
)


def test_consumer_audit_renders(capsys):
    assert seed_local.main(["--consumer-audit", "--predicate", "ip_address"]) == 0
    output = capsys.readouterr().out
    assert "Consumer Dependency Audit" in output
    assert "Item: ip_address" in output
    assert "Consumer Count:" in output


def test_consumer_audit_json_is_valid(capsys):
    assert seed_local.main(["--consumer-audit", "--predicate", "ip_address", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert {"summary", "items", "metadata"} <= set(payload)
    assert payload["items"][0]["item"] == "ip_address"


def test_consumers_are_discovered_from_implementation_fixture(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "seed_runtime" / "observation_sources.py").write_text(
        """class FixtureObservationSource:
    source_type = "fixture"
    def collect(self):
        return [Observation(subject="h", predicate="fixture_predicate", object="x")]
""",
        encoding="utf-8",
    )
    (tmp_path / "seed_runtime" / "state.py").write_text('if fact.predicate == "fixture_predicate": pass', encoding="utf-8")
    audit = build_consumer_audit(tmp_path, predicate_filter="fixture_predicate")
    row = audit.items[0]
    assert row.consumers == ("projection_builders",)
    assert row.consumer_count == 1
    assert row.highlight == "fragile"


def test_orphaned_detection_works_for_fixture(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "seed_runtime" / "observation_sources.py").write_text(
        """class FixtureObservationSource:
    source_type = "fixture"
    def collect(self):
        return [Observation(subject="h", predicate="orphan_predicate", object="x")]
""",
        encoding="utf-8",
    )
    audit = build_consumer_audit(tmp_path, predicate_filter="orphan_predicate")
    row = audit.items[0]
    assert row.consumer_count == 0
    assert row.orphaned is True
    assert "Orphaned: yes" in format_consumer_audit(audit)


def test_consumer_counts_are_correct_for_multiconsumer_fixture(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "seed_runtime" / "observation_sources.py").write_text(
        """class FixtureObservationSource:
    source_type = "fixture"
    def collect(self):
        return [Observation(subject="h", predicate="wide_predicate", object="x")]
""",
        encoding="utf-8",
    )
    (tmp_path / "seed_runtime" / "state.py").write_text('"wide_predicate"', encoding="utf-8")
    (tmp_path / "seed_runtime" / "state_views.py").write_text('"wide_predicate"', encoding="utf-8")
    (tmp_path / "seed_runtime" / "ownership_discrepancies.py").write_text('"wide_predicate"', encoding="utf-8")
    audit = build_consumer_audit(tmp_path, predicate_filter="wide_predicate")
    row = audit.items[0]
    assert row.consumer_count == 4
    assert audit.summary["multi_consumer_items"] == 1
    assert row.highlight == "widely used"


def test_filtering_by_diagnostic(capsys):
    assert seed_local.main(["--consumer-audit", "--diagnostic", "ownership_discrepancies", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [item["item"] for item in payload["items"]] == ["ownership_discrepancies"]
    assert payload["items"][0]["kind"] == "diagnostic"


def test_empty_behavior_is_sane(capsys):
    assert seed_local.main(["--consumer-audit", "--predicate", "definitely_missing_predicate"]) == 0
    output = capsys.readouterr().out
    assert "Items scanned: 0" in output
    assert "No items matched" in output
