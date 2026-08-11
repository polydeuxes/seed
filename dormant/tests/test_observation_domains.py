import json

from scripts import seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.observation_domains import build_observation_domains
from seed_runtime.state import State


def _domain(report, name):
    return next(entry for entry in report.domains if entry.domain == name)


def test_cli_observation_domains_renders_human_readable(capsys):
    assert seed_local.main(["--observation-domains"]) == 0
    out = capsys.readouterr().out
    assert "Observation Domains" in out
    assert "Domain:" in out
    assert "Classification:" in out
    assert "Gap Type:" in out
    assert "Boundary: read_only=true writes_event_ledger=false mutates_cluster=false" in out


def test_cli_observation_domains_json_is_valid(capsys):
    assert seed_local.main(["--observation-domains", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) == {"domains", "boundary"}
    assert payload["boundary"] == {
        "read_only": True,
        "writes_event_ledger": False,
        "mutates_cluster": False,
    }
    assert {"domain", "classification", "gap_type", "pressure", "evidence"} <= set(
        payload["domains"][0]
    )


def test_domain_classification_visibility_includes_observed_domain():
    report = build_observation_domains(State(workspace_id="test"))
    observed = [d for d in report.domains if d.classification == "observed"]
    assert observed
    assert any("observation family observed" in " ".join(d.evidence) for d in observed)


def test_partially_observed_listener_domain_visibility(capsys):
    assert seed_local.main(["--observation-domains", "local_listeners"]) == 0
    out = capsys.readouterr().out
    assert "Domain: local_listeners" in out
    assert "Classification: partially_observed" in out
    assert "Pressure: listener_process_inventory" in out


def test_unobserved_container_domain_visibility(capsys):
    assert seed_local.main(["--observation-domains", "container_runtime"]) == 0
    out = capsys.readouterr().out
    assert "Domain: container_runtime" in out
    assert "Classification: unobserved" in out
    assert "Pressure: container_inventory" in out
    assert "container_port_mapping" in out


def test_unknown_domain_handling(capsys):
    assert seed_local.main(["--observation-domains", "does_not_exist"]) == 0
    out = capsys.readouterr().out
    assert "Domain: does_not_exist" in out
    assert "Classification: unknown" in out
    assert "Gap Type: unknown" in out


def test_gap_type_and_pressure_to_domain_visibility():
    report = build_observation_domains(State(workspace_id="test"))
    listener = _domain(report, "local_listeners")
    assert listener.gap_type == "missing_evidence_inside_observed_domain"
    assert "listener_process_inventory" in listener.pressure
    container = _domain(report, "container_runtime")
    assert container.gap_type == "missing_observation_domain"
    assert {"container_inventory", "container_port_mapping"} <= set(container.pressure)


def test_observation_domains_boundary_is_read_only():
    report = build_observation_domains(State(workspace_id="test"))
    assert report.boundary["read_only"] is True
    assert report.boundary["writes_event_ledger"] is False
    assert report.boundary["mutates_cluster"] is False


def test_observation_domains_visibility_registration():
    entry = next(e for e in DIAGNOSTIC_INVENTORY if e.name == "observation_domains")
    assert entry.cli_flags == ("--observation-domains",)
    assert entry.supports_json
    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster
    assert entry.reads_diagnostic_facts


def test_observation_domains_shape_registration_consistency():
    rows = [r for r in build_diagnostic_shape_audit() if r.diagnostic == "observation_domains"]
    assert rows
    assert {row.status for row in rows} == {"consistent"}
