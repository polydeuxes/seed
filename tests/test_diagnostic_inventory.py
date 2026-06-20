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
        "ownership_discrepancies",
        "capability_needs",
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
        "ownership_discrepancies",
        "capability_needs",
    }
    assert payload[0]["cli_flags"]


def test_recording_diagnostics_declare_diagnostic_run_scope_and_ledger_writes():
    recording_entries = [entry for entry in DIAGNOSTIC_INVENTORY if entry.supports_record]

    assert recording_entries
    assert all(entry.record_scope == "diagnostic_run" for entry in recording_entries)
    assert all(entry.writes_event_ledger for entry in recording_entries)


def test_current_diagnostics_do_not_mutate_cluster():
    assert all(not entry.mutates_cluster for entry in DIAGNOSTIC_INVENTORY)


def test_current_diagnostic_shapes_match_implementation_authority():
    assert _entry("ownership_discrepancies").supports_record
    assert _entry("knowledge_reachability").uses_repo_files
    assert _entry("capability_needs").reads_diagnostic_facts


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
