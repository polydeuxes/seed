import json

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import (
    DIAGNOSTIC_INVENTORY,
    DiagnosticInventoryEntry,
    format_diagnostic_inventory,
)


def _entry(name: str) -> DiagnosticInventoryEntry:
    return next(entry for entry in DIAGNOSTIC_INVENTORY if entry.name == name)


def test_cli_diagnostic_inventory_lists_known_diagnostics(capsys):
    assert seed_local.main(["--diagnostic-inventory"]) == 0

    output = capsys.readouterr().out

    assert "Diagnostic" in output
    for name in [
        "classification_coverage",
        "graph_issue_summary",
        "knowledge_reachability",
        "documentation_structure",
        "ownership_discrepancies",
        "capability_needs",
        "observation_utilization",
        "architecture_conformance_audit",
        "operational_graph",
        "operational_graph_confidence",
        "operational_graph_taxonomy",
        "consumer_audit",
        "emitter_attribution_audit",
        "current_facts_cache_debug",
        "investigation_path",
    ]:
        assert name in output


def test_cli_diagnostic_inventory_json_emits_valid_json(capsys):
    assert seed_local.main(["--diagnostic-inventory", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert isinstance(payload, list)
    assert {entry["name"] for entry in payload} >= {
        "classification_coverage",
        "graph_issue_summary",
        "knowledge_reachability",
        "documentation_structure",
        "ownership_discrepancies",
        "capability_needs",
        "observation_utilization",
        "architecture_conformance_audit",
        "operational_graph",
        "operational_graph_confidence",
        "operational_graph_taxonomy",
        "consumer_audit",
        "emitter_attribution_audit",
        "current_facts_cache_debug",
        "investigation_path",
    }
    assert payload[0]["cli_flags"]


def test_recording_diagnostics_declare_diagnostic_run_scope_and_ledger_writes():
    recording_entries = [
        entry for entry in DIAGNOSTIC_INVENTORY if entry.supports_record
    ]

    assert recording_entries
    assert all(entry.record_scope == "diagnostic_run" for entry in recording_entries)
    assert all(entry.writes_event_ledger for entry in recording_entries)


def test_current_diagnostics_do_not_mutate_cluster():
    assert all(not entry.mutates_cluster for entry in DIAGNOSTIC_INVENTORY)


def test_current_diagnostic_shapes_match_implementation_authority():
    assert _entry("documentation_structure").cli_flags == (
        "--documentation-structure",
        "--document",
        "--missing-front-matter",
        "--missing-trailing-newline",
        "--empty-sections",
        "--sections",
        "--links",
        "--code-fences",
        "--recurrence",
        "--rare",
        "--missing-common-sections",
        "--outliers",
        "--skeletons",
        "--where",
        "--membership",
        "--limit",
        "--top",
        "--summary-only",
        "--min-count",
        "--max-count",
    )
    assert _entry("documentation_structure").uses_repo_files
    assert (
        "exact section-label structural membership"
        in _entry("documentation_structure").description
    )
    assert (
        "without parsing code contents" in _entry("documentation_structure").description
    )
    assert _entry("documentation_structure").supports_json
    assert not _entry("documentation_structure").supports_record
    assert _entry("documentation_structure").record_scope == "none"
    assert not _entry("documentation_structure").writes_event_ledger
    assert not _entry("documentation_structure").mutates_cluster
    assert _entry("ownership_discrepancies").supports_record
    assert _entry("knowledge_reachability").uses_repo_files
    assert _entry("capability_needs").reads_diagnostic_facts
    assert _entry("current_facts_cache_debug").cli_flags == (
        "--current-facts-cache-debug",
    )
    assert not _entry("current_facts_cache_debug").writes_event_ledger
    assert not _entry("current_facts_cache_debug").mutates_cluster
    assert _entry("investigation_path").cli_flags == ("--investigation-path",)
    assert _entry("investigation_path").supports_json
    assert not _entry("investigation_path").writes_event_ledger
    assert not _entry("investigation_path").mutates_cluster
    assert _entry("architecture_conformance_audit").cli_flags == (
        "--architecture-conformance-audit",
    )
    assert _entry("architecture_conformance_audit").supports_json
    assert not _entry("architecture_conformance_audit").supports_record
    assert _entry("architecture_conformance_audit").record_scope == "none"
    assert not _entry("architecture_conformance_audit").writes_event_ledger
    assert not _entry("architecture_conformance_audit").mutates_cluster
    assert _entry("operational_graph").cli_flags == ("--operational-graph",)
    assert _entry("operational_graph").supports_json
    assert not _entry("operational_graph").supports_record
    assert _entry("operational_graph").record_scope == "none"
    assert not _entry("operational_graph").writes_event_ledger
    assert not _entry("operational_graph").mutates_cluster
    assert _entry("operational_graph_confidence").cli_flags == (
        "--operational-graph-confidence",
        "--exclude-aggregate",
    )
    assert _entry("operational_graph_taxonomy").cli_flags == (
        "--operational-graph-taxonomy",
    )
    assert _entry("operational_graph_taxonomy").supports_json
    assert not _entry("operational_graph_taxonomy").supports_record
    assert _entry("operational_graph_taxonomy").record_scope == "none"
    assert not _entry("operational_graph_taxonomy").writes_event_ledger
    assert not _entry("operational_graph_taxonomy").mutates_cluster
    assert _entry("operational_graph_confidence").supports_json
    assert not _entry("operational_graph_confidence").supports_record
    assert _entry("operational_graph_confidence").record_scope == "none"
    assert not _entry("operational_graph_confidence").writes_event_ledger
    assert not _entry("operational_graph_confidence").mutates_cluster


def test_inventory_rendering_is_generated_from_registry_data():
    rendered = format_diagnostic_inventory(
        (
            DiagnosticInventoryEntry(
                name="synthetic_probe",
                cli_flags=("--synthetic-probe",),
                uses_projected_state=False,
                uses_repo_files=True,
                supports_json=True,
                supports_record=True,
                record_scope="diagnostic_run",
                emits_diagnostic_facts=True,
                emits_cluster_facts=False,
                writes_event_ledger=True,
                mutates_cluster=False,
                reads_diagnostic_facts=True,
                description="Synthetic registry entry used to prove generated rendering.",
            ),
        )
    )

    assert "synthetic_probe" in rendered
    assert "--synthetic-probe" in rendered
    assert "diagnostic_run" in rendered
    assert "writes_event_ledger=true" in rendered
    assert "reads_diagnostic_facts=true" in rendered


def test_container_ownership_authority_inventory_entry_declares_boundary():
    entry = _entry("container_ownership_authority")

    assert entry.cli_flags == ("--container-ownership-authority",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.uses_projected_state is True
    assert entry.uses_repo_files is False
    assert entry.reads_diagnostic_facts is True
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False


def test_projected_state_consumers_registered_in_diagnostic_inventory():
    entry = _entry("projected_state_consumers")

    assert entry.cli_flags == ("--projected-state-consumers",)
    assert entry.supports_json
    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.uses_projected_state
    assert not entry.uses_repo_files
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster


def test_implementation_trait_characterization_registered_in_diagnostic_inventory():
    entry = _entry("implementation_trait_characterization")

    assert entry.cli_flags == ("--implementation-trait-characterization",)
    assert entry.supports_json
    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.uses_projected_state
    assert not entry.uses_repo_files
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster
    assert not entry.emits_diagnostic_facts
    assert not entry.emits_cluster_facts



def test_diagnostic_surface_definition_json_includes_identity_explanation(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-definition", "diagnostic_shape_audit", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    definition = payload["diagnostic_surface_definition"]

    assert definition["status"] == "known"
    assert definition["diagnostic_name"] == "diagnostic_shape_audit"
    assert definition["cli_flags"] == ["--diagnostic-shape-audit"]
    assert definition["description"] == _entry("diagnostic_shape_audit").description
    assert definition["supports_json"] is True
    assert definition["supports_record"] is False
    assert definition["record_scope"] == "none"
    assert definition["diagnostic_surface_boundary"] == {
        "status": "known",
        "statements": [
            "read-only",
            "does not record",
            "record_scope=none",
            "does not write event ledger",
            "does not mutate cluster",
            "does not use projected state",
            "does not use repository files",
            "does not emit diagnostic facts",
            "does not emit cluster facts",
            "does not read diagnostic facts",
        ],
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "boundary recovered from declared diagnostic inventory fields",
    }
    assert definition["diagnostic_surface_consumption"] == {
        "status": "known",
        "declared_consumption": {
            "uses_projected_state": False,
            "uses_repo_files": False,
            "reads_diagnostic_facts": False,
        },
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "consumption recovered from declared diagnostic inventory fields",
    }
    assert definition["diagnostic_inventory_registration"] == "present"
    assert definition["shape_registration_status"] == "present"


def test_diagnostic_surface_definition_human_renders_identity_explanation(capsys):
    assert seed_local.main(["--diagnostic-surface-definition", "diagnostic_shape_audit"]) == 0

    output = capsys.readouterr().out

    assert "DiagnosticSurface definition: diagnostic_shape_audit" in output
    assert "  status: known" in output
    assert "  cli_flags: --diagnostic-shape-audit" in output
    assert f"  description: {_entry('diagnostic_shape_audit').description}" in output
    assert "  supports_json: true" in output
    assert "  supports_record: false" in output
    assert "  record_scope: none" in output
    assert (
        "  diagnostic_surface_boundary: read-only; does not record; "
        "record_scope=none; does not write event ledger; does not mutate cluster; "
        "does not use projected state; does not use repository files; "
        "does not emit diagnostic facts; does not emit cluster facts; "
        "does not read diagnostic facts"
    ) in output
    assert (
        "  diagnostic_surface_consumption: uses_projected_state=false; "
        "uses_repo_files=false; reads_diagnostic_facts=false"
    ) in output
    assert "  diagnostic_inventory_registration: present" in output
    assert "  shape_registration_status: present" in output


def test_diagnostic_surface_definition_unknown_is_bounded(capsys):
    assert seed_local.main(["--diagnostic-surface-definition", "missing_surface", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["diagnostic_surface_definition"] == {
        "status": "unknown",
        "diagnostic_name": "missing_surface",
        "cli_flags": [],
        "description": "unknown",
        "supports_json": "unknown",
        "supports_record": "unknown",
        "record_scope": "unknown",
        "diagnostic_surface_boundary": {
            "status": "unknown",
            "statements": [],
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
        },
        "diagnostic_surface_consumption": {
            "status": "unknown",
            "declared_consumption": {},
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
        },
        "diagnostic_inventory_registration": "absent",
        "shape_registration_status": "unknown",
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
    }


def test_diagnostic_surface_definition_does_not_change_inventory_output(capsys):
    assert seed_local.main(["--diagnostic-inventory", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert isinstance(payload, list)
    assert "diagnostic_surface_definition" not in payload[0]
    assert _entry("diagnostic_surface_definition").supports_json is True
    assert _entry("diagnostic_surface_definition").record_scope == "none"
    assert not _entry("diagnostic_surface_definition").mutates_cluster
    assert "diagnostic_surface_boundary" not in payload[0]
    assert "diagnostic_surface_consumption" not in payload[0]


def test_diagnostic_surface_consumption_json_uses_inventory_declarations(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-definition", "privilege_discovery", "--json"]
        )
        == 0
    )

    definition = json.loads(capsys.readouterr().out)["diagnostic_surface_definition"]

    assert definition["diagnostic_surface_consumption"] == {
        "status": "known",
        "declared_consumption": {
            "uses_projected_state": True,
            "uses_repo_files": False,
            "reads_diagnostic_facts": True,
        },
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "consumption recovered from declared diagnostic inventory fields",
    }


def test_diagnostic_surface_definition_guardrails_exclude_runtime_planning_and_inference(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-definition", "diagnostic_shape_audit", "--json"]
        )
        == 0
    )

    rendered = json.dumps(json.loads(capsys.readouterr().out)).lower()

    for forbidden in [
        "runtime execution",
        "diagnostic execution",
        "planner behavior",
        "semantic interpretation",
        "implementation inference",
        "consumption inference",
        "future execution",
        "new relationship concepts",
    ]:
        assert forbidden not in rendered
