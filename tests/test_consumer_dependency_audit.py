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
    assert (
        seed_local.main(["--consumer-audit", "--predicate", "ip_address", "--json"])
        == 0
    )
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
    (tmp_path / "seed_runtime" / "state.py").write_text(
        'if fact.predicate == "fixture_predicate": pass', encoding="utf-8"
    )
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
    (tmp_path / "seed_runtime" / "state.py").write_text(
        '"wide_predicate"', encoding="utf-8"
    )
    (tmp_path / "seed_runtime" / "state_views.py").write_text(
        '"wide_predicate"', encoding="utf-8"
    )
    (tmp_path / "seed_runtime" / "ownership_discrepancies.py").write_text(
        '"wide_predicate"', encoding="utf-8"
    )
    audit = build_consumer_audit(tmp_path, predicate_filter="wide_predicate")
    row = audit.items[0]
    assert row.consumer_count == 4
    assert audit.summary["multi_consumer_items"] == 1
    assert row.highlight == "widely used"


def test_filtering_by_diagnostic(capsys):
    assert (
        seed_local.main(
            ["--consumer-audit", "--diagnostic", "ownership_discrepancies", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert [item["item"] for item in payload["items"]] == ["ownership_discrepancies"]
    assert payload["items"][0]["kind"] == "diagnostic"


def test_empty_behavior_is_sane(capsys):
    assert (
        seed_local.main(
            ["--consumer-audit", "--predicate", "definitely_missing_predicate"]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "Items scanned: 0" in output
    assert "No items matched" in output


def test_storage_canonical_predicate_consumers_are_not_orphaned():
    audit = build_consumer_audit(predicate_filter="filesystem_avail_bytes")
    row = audit.items[0]
    assert row.orphaned is False
    assert row.consumer_count > 0
    assert "read_models" in row.consumers
    assert "state_build" in row.consumers


def test_storage_consumer_audit_json_reflects_corrected_counts():
    audit = build_consumer_audit(predicate_filter="filesystem_avail_bytes")
    payload = audit.to_json_dict()
    row = payload["items"][0]
    assert row["item"] == "filesystem_avail_bytes"
    assert row["orphaned"] is False
    assert row["consumer_count"] == len(row["consumers"])
    assert row["consumer_count"] > 0


def test_storage_consumer_audit_human_output_remains_valid():
    audit = build_consumer_audit(predicate_filter="filesystem_avail_bytes")
    output = format_consumer_audit(audit)
    assert "Consumer Dependency Audit" in output
    assert "Item: filesystem_avail_bytes" in output
    assert "Orphaned: no" in output
    assert "  read_models" in output


def test_consumer_audit_uses_canonical_mapping_without_prefix_matches(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "predicate_catalog").mkdir()
    (tmp_path / "predicate_catalog" / "core.json").write_text(
        json.dumps(
            {
                "predicates": [
                    {
                        "predicate": "storage_free_bytes",
                        "kind": "measurement",
                        "value_type": "integer",
                        "cardinality": "single",
                    }
                ],
                "mappings": [
                    {
                        "source_name": "fixture",
                        "predicate": "raw_storage_avail_bytes",
                        "canonical_predicate": "storage_free_bytes",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "seed_runtime" / "observation_sources.py").write_text(
        """class FixtureObservationSource:
    source_type = "fixture"
    def collect(self):
        return [
            Observation(subject="h", predicate="raw_storage_avail_bytes", object=1),
            Observation(subject="h", predicate="raw_storage_avail_bytes_extra", object=1),
            Observation(subject="h", predicate="unused_storage_avail_bytes", object=1),
        ]
""",
        encoding="utf-8",
    )
    (tmp_path / "seed_runtime" / "state_summary_views.py").write_text(
        'if fact.predicate == "storage_free_bytes": pass\n', encoding="utf-8"
    )

    mapped = build_consumer_audit(
        tmp_path, predicate_filter="raw_storage_avail_bytes"
    ).items[0]
    prefix = build_consumer_audit(
        tmp_path, predicate_filter="raw_storage_avail_bytes_extra"
    ).items[0]
    unused = build_consumer_audit(
        tmp_path, predicate_filter="unused_storage_avail_bytes"
    ).items[0]

    assert mapped.orphaned is False
    assert mapped.consumers == ("read_models", "state_build")
    assert prefix.orphaned is True
    assert unused.orphaned is True
