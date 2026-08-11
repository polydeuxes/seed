import json

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.investigation_path_audit import build_investigation_path_audit


def _surface_names(domain: str) -> list[str]:
    return [step.name for step in build_investigation_path_audit(domain).surfaces]


def test_cli_investigation_path_renders(capsys):
    assert seed_local.main(["--investigation-path", "ownership"]) == 0

    output = capsys.readouterr().out

    assert "Investigation Path" in output
    assert "Domain: ownership" in output
    assert "Relevant Surfaces" in output
    assert "Suggested Order" in output


def test_cli_investigation_path_json_emits_valid_json(capsys):
    assert seed_local.main(["--investigation-path", "ownership", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["domain"] == "ownership"
    assert payload["surfaces"]
    assert payload["surfaces"][0]["order"] == 1
    assert {"name", "reason", "order"} <= set(payload["surfaces"][0])


def test_ownership_path_includes_ownership_relevant_surfaces():
    names = _surface_names("ownership")

    assert names[:3] == [
        "ownership_discrepancies",
        "capability_needs",
        "privilege_discovery",
    ]
    assert "correlation_audit" in names
    assert "impact_audit" in names


def test_capability_path_includes_capability_relevant_surfaces():
    names = _surface_names("capability")

    assert names[:2] == ["capability_needs", "privilege_discovery"]
    assert "pressure_audit" in names


def test_pressure_path_includes_pressure_relevant_surfaces():
    names = _surface_names("pressure")

    assert names[:3] == ["pressure_audit", "capability_needs", "privilege_discovery"]
    assert "impact_audit" in names


def test_correlation_path_includes_correlation_relevant_surfaces():
    names = _surface_names("correlation")

    assert names[0] == "correlation_audit"
    assert "consumer_audit" in names
    assert "observation_utilization" in names


def test_unknown_domain_behaves_sanely(capsys):
    assert seed_local.main(["--investigation-path", "unknown-domain"]) == 1

    output = capsys.readouterr().out

    assert "No investigation path is registered" in output
    assert "Known Domains" in output


def test_investigation_path_has_no_event_ledger_writes_or_cluster_mutation():
    entry = next(
        entry for entry in DIAGNOSTIC_INVENTORY if entry.name == "investigation_path"
    )

    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster
