import json
from pathlib import Path

from scripts import seed_local
from seed_runtime.observation_inventory import build_observation_inventory, format_observation_inventory


def test_cli_observation_inventory_renders(capsys):
    assert seed_local.main(["--observation-inventory"]) == 0
    out = capsys.readouterr().out
    assert "Observation Inventory" in out
    assert "Providers:" in out
    assert "Predicates:" in out
    assert "local_host" in out


def test_cli_observation_inventory_json_is_valid(capsys):
    assert seed_local.main(["--observation-inventory", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) >= {"providers", "predicates", "families", "summary", "metadata"}


def test_providers_and_predicates_are_discovered_from_implementation():
    inv = build_observation_inventory()
    providers = {p.name for p in inv.providers}
    predicates = {p.predicate for p in inv.predicates}
    assert "local_host" in providers
    assert "prometheus:http://example.invalid" not in providers
    assert {"os", "hostname", "up"} <= predicates


def test_inventory_is_not_backed_by_manually_maintained_static_list():
    source = Path("seed_runtime/observation_inventory.py").read_text()
    assert "local_host" not in source
    assert "PrometheusObservationSource" not in source
    assert "OBSERVATION_INVENTORY" not in source


def test_filtering_works():
    provider_inv = build_observation_inventory(provider_filter="systemd")
    assert [p.name for p in provider_inv.providers] == ["systemd"]
    predicate_inv = build_observation_inventory(predicate_filter="up")
    assert [p.predicate for p in predicate_inv.predicates] == ["up"]
    assert all(p.predicates == ("up",) for p in predicate_inv.providers)


def test_summary_counts_are_correct():
    payload = build_observation_inventory().to_json_dict()
    assert payload["summary"]["provider_count"] == len(payload["providers"])
    assert payload["summary"]["predicate_count"] == len(payload["predicates"])
    assert payload["summary"]["family_count"] == len(payload["families"])


def test_empty_inventory_behavior_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    inv = build_observation_inventory(tmp_path)
    assert inv.to_json_dict()["summary"] == {"provider_count": 0, "predicate_count": 0, "family_count": 0}
    rendered = format_observation_inventory(inv)
    assert "Providers: 0" in rendered
