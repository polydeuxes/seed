import json
import subprocess
import sys

from seed_runtime.implementation_trait_characterization import (
    build_implementation_trait_characterization,
    implementation_trait_characterization_json,
)

REQUIRED = {
    "uses_projected_state": "evidence_source",
    "uses_repo_files": "evidence_source",
    "uses_static_inventory": "evidence_source",
    "uses_live_observation": "evidence_source",
    "uses_event_ledger": "evidence_source",
    "uses_runtime_input": "evidence_source",
    "reads_diagnostic_facts": "evidence_source",
    "evidence": "evidence_source",
    "read_only": "operational_boundary",
    "records": "operational_boundary",
    "supports_record": "operational_boundary",
    "record_scope": "operational_boundary",
    "writes_event_ledger": "operational_boundary",
    "mutates_cluster": "operational_boundary",
    "executes_observation": "operational_boundary",
    "permission_creation": "operational_boundary",
    "provider_acquisition": "operational_boundary",
    "bounded_status": "dispatchability",
    "dispatch_surface": "dispatchability",
    "required_surface_args": "dispatchability",
    "supports_json": "implementation_capability",
    "json_support": "implementation_capability",
    "json_capable": "implementation_capability",
    "registered": "implementation_capability",
    "category": "implementation_capability",
    "consumer_kind": "implementation_capability",
    "emits_diagnostic_facts": "implementation_capability",
    "emits_cluster_facts": "implementation_capability",
}


def _by_trait():
    return {row.trait: row for row in build_implementation_trait_characterization()}


def test_required_example_traits_are_classified_from_exposed_surfaces():
    rows = _by_trait()
    for trait, concern in REQUIRED.items():
        assert trait in rows
        assert rows[trait].concern == concern
        assert rows[trait].exposed_by
        assert rows[trait].implementation_meaning
        assert rows[trait].implementation_reason


def test_required_examples_have_no_unclassified_traits():
    rows = _by_trait()
    assert [trait for trait in REQUIRED if rows[trait].concern == "unclassified"] == []


def test_concern_counts_include_required_concerns():
    payload = implementation_trait_characterization_json()
    counts = payload["concern_counts"]
    assert counts["evidence_source"] >= 8
    assert counts["operational_boundary"] >= 9
    assert counts["dispatchability"] >= 3
    assert counts["implementation_capability"] >= 8


def test_cli_human_output():
    completed = subprocess.run(
        [sys.executable, "scripts/seed_local.py", "--implementation-trait-characterization"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "Implementation Trait Characterization" in completed.stdout
    assert "uses_projected_state" in completed.stdout
    assert "concern: evidence_source" in completed.stdout


def test_cli_json_output():
    completed = subprocess.run(
        [sys.executable, "scripts/seed_local.py", "--implementation-trait-characterization", "--json"],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    rows = {item["trait"]: item for item in payload["items"]}
    assert rows["mutates_cluster"]["concern"] == "operational_boundary"
    assert "concern_counts" in payload


def test_surface_boundary_row_is_read_only():
    rows = _by_trait()
    assert rows["read_only"].concern == "operational_boundary"
    assert rows["read_only"].exposed_by == ("--projected-state-consumers",)
    assert rows["records"].concern == "operational_boundary"
    assert rows["writes_event_ledger"].concern == "operational_boundary"
    assert rows["mutates_cluster"].concern == "operational_boundary"
    assert rows["executes_observation"].concern == "operational_boundary"
    assert rows["provider_acquisition"].concern == "operational_boundary"
    assert rows["permission_creation"].concern == "operational_boundary"
