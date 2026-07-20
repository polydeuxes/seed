import json

import scripts.seed_local as seed_local
from seed_runtime.consumer_dependency_audit import (
    build_consumer_audit,
    format_consumer_audit,
    _diagnostic_audit_items,
    _matched_consumer_groups,
    _observation_predicate_audit_items,
)
from seed_runtime.observation_inventory import ObservationPredicateInventory


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


def test_observation_predicate_item_producer_preserves_boundary_behavior(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    sources = {
        "projection_builders": {"seed_runtime/state.py": '"alpha_predicate"'},
        "read_models": {"seed_runtime/state_views.py": '"beta_predicate"'},
    }
    items = _observation_predicate_audit_items(
        (
            ObservationPredicateInventory("beta_predicate", ("fixture",)),
            ObservationPredicateInventory("alpha_predicate", ("fixture",)),
        ),
        sources,
        repo_root=tmp_path,
    )

    assert [item.kind for item in items] == [
        "observation_predicate",
        "observation_predicate",
    ]
    assert [item.item for item in items] == ["beta_predicate", "alpha_predicate"]
    assert items[0].consumers == ("read_models",)
    assert items[1].consumers == ("projection_builders",)

    (tmp_path / "seed_runtime" / "state.py").write_text(
        '"alpha_predicate"', encoding="utf-8"
    )
    (tmp_path / "seed_runtime" / "state_views.py").write_text(
        '"beta_predicate"', encoding="utf-8"
    )
    (tmp_path / "seed_runtime" / "observation_sources.py").write_text(
        """class FixtureObservationSource:
    source_type = \"fixture\"
    def collect(self):
        return [
            Observation(subject=\"h\", predicate=\"beta_predicate\", object=1),
            Observation(subject=\"h\", predicate=\"alpha_predicate\", object=1),
        ]
""",
        encoding="utf-8",
    )
    audit = build_consumer_audit(tmp_path)
    observation_rows = [
        (item.kind, item.item)
        for item in audit.items
        if item.kind == "observation_predicate"
    ]
    assert observation_rows == [
        ("observation_predicate", "alpha_predicate"),
        ("observation_predicate", "beta_predicate"),
    ]
    payload = audit.to_json_dict()
    alpha_payload = next(
        item for item in payload["items"] if item["item"] == "alpha_predicate"
    )
    assert alpha_payload == {
        "item": "alpha_predicate",
        "kind": "observation_predicate",
        "consumers": ["projection_builders"],
        "consumer_count": 1,
        "orphaned": False,
        "highlight": "fragile",
    }
    output = format_consumer_audit(audit)
    assert "Item: alpha_predicate" in output
    assert "Kind: observation_predicate" in output
    assert "  projection_builders" in output
    assert not (tmp_path / "seed_events.jsonl").exists()


def test_diagnostic_item_producer_preserves_boundary_behavior(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    sources = {
        "diagnostics": {
            "seed_runtime/ownership_discrepancies.py": '"ownership_discrepancies"'
        },
        "views": {"scripts/seed_local.py": '"component_audit"'},
    }
    items = _diagnostic_audit_items(
        ("component_audit", "ownership_discrepancies"),
        sources,
        diagnostic_filter="ownership_discrepancies",
        repo_root=tmp_path,
    )

    assert len(items) == 1
    assert items[0].kind == "diagnostic"
    assert items[0].item == "ownership_discrepancies"
    assert items[0].consumers == ("diagnostics",)

    (tmp_path / "seed_runtime" / "ownership_discrepancies.py").write_text(
        '"ownership_discrepancies"', encoding="utf-8"
    )
    (tmp_path / "scripts" / "seed_local.py").write_text(
        '"component_audit"', encoding="utf-8"
    )
    audit = build_consumer_audit(tmp_path, diagnostic_filter="ownership_discrepancies")
    assert [(item.kind, item.item) for item in audit.items] == [
        ("diagnostic", "ownership_discrepancies")
    ]
    payload = audit.to_json_dict()
    assert payload["items"] == [
        {
            "item": "ownership_discrepancies",
            "kind": "diagnostic",
            "consumers": ["diagnostics"],
            "consumer_count": 1,
            "orphaned": False,
            "highlight": "fragile",
        }
    ]
    output = format_consumer_audit(audit)
    assert "Item: ownership_discrepancies" in output
    assert "Kind: diagnostic" in output
    assert "  diagnostics" in output
    assert not (tmp_path / "seed_events.jsonl").exists()


def test_matched_consumer_groups_preserves_order_exact_matches_and_orphans():
    sources = {
        "first_group": {"first.py": "unrelated"},
        "second_group": {"second.py": 'fact.predicate == "target_predicate"'},
        "third_group": {"third.py": "target-predicate"},
    }

    assert _matched_consumer_groups(sources, ("target_predicate",)) == (
        "second_group",
        "third_group",
    )
    assert _matched_consumer_groups(sources, ("missing_predicate",)) == ()


def test_audit_item_delegates_lookup_terms_and_low_level_mention_matching(tmp_path):
    (tmp_path / "predicate_catalog").mkdir()
    (tmp_path / "predicate_catalog" / "core.json").write_text(
        json.dumps(
            {
                "mappings": [
                    {
                        "predicate": "raw_storage_avail_bytes",
                        "canonical_predicate": "storage_free_bytes",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "seed_runtime").mkdir(exist_ok=True)
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / "seed_runtime" / "observation_sources.py").write_text(
        """class FixtureObservationSource:
    source_type = "fixture"
    def collect(self):
        return [Observation(subject="h", predicate="raw_storage_avail_bytes", object=1)]
""",
        encoding="utf-8",
    )
    sources = {
        "projection_builders": {"seed_runtime/state.py": "raw_storage_avail_bytes"},
        "read_models": {
            "seed_runtime/state_summary_views.py": 'fact.predicate == "storage_free_bytes"'
        },
        "diagnostics": {"seed_runtime/knowledge_reachability.py": "raw-storage-avail-bytes"},
    }
    for group_files in sources.values():
        for relative_path, content in group_files.items():
            path = tmp_path / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    audit = build_consumer_audit(tmp_path, predicate_filter="raw_storage_avail_bytes")
    row = audit.items[0]
    assert row.consumers == (
        "projection_builders",
        "read_models",
        "diagnostics",
        "state_build",
    )
    assert row.to_json_dict()["consumers"] == [
        "projection_builders",
        "read_models",
        "diagnostics",
        "state_build",
    ]
    output = format_consumer_audit(audit)
    assert "  projection_builders" in output
    assert "  read_models" in output
    assert "  diagnostics" in output
    assert "  state_build" in output
    assert not (tmp_path / "seed_events.jsonl").exists()


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


def test_listener_predicates_consumed_by_ownership_discrepancy_diagnostics():
    for predicate in (
        "listener_address",
        "listener_port",
        "listener_scope",
        "listener_attribution_status",
        "listening_process_id",
        "listening_process_name",
    ):
        row = build_consumer_audit(predicate_filter=predicate).items[0]
        assert row.orphaned is False
        assert "diagnostics" in row.consumers
