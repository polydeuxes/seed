import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.capability_needs import CapabilityNeedEntry
from seed_runtime.privilege_discovery import (
    build_privilege_discovery,
    format_privilege_discovery,
)
from seed_runtime.state import State

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location("seed_local_privilege", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _need(capability: str, subjects=("svc-a", "svc-b")):
    return CapabilityNeedEntry(
        capability=capability,
        subjects=set(subjects),
        diagnostics={"ownership_discrepancies"},
        needed_evidence={capability},
        diagnostic_runs={"current_projection"},
    )


def test_privilege_discovery_renders_capability_access_pressure_and_guidance(monkeypatch, capsys):
    seed_local = load_seed_local()
    monkeypatch.setattr(
        "seed_runtime.privilege_discovery.build_capability_needs",
        lambda state: [
            _need("listener_process_inventory"),
            _need("container_inventory", ("svc-c",)),
        ],
    )

    assert seed_local.main(["--privilege-discovery"]) == 0
    output = capsys.readouterr().out

    assert "Privilege Discovery" in output
    assert "listener_process_inventory" in output
    assert "partial_non_root" in output
    assert "2 affected subjects" in output
    assert "service ownership attribution" in output
    assert "attempt non-root attribution first" in output
    assert "container_inventory" in output
    assert "docker_group_or_root" in output
    assert "requires docker-group or root visibility" in output


def test_privilege_discovery_json_is_valid_and_includes_boundary_fields(monkeypatch, capsys):
    seed_local = load_seed_local()
    monkeypatch.setattr(
        "seed_runtime.privilege_discovery.build_capability_needs",
        lambda state: [_need("container_port_mapping")],
    )

    assert seed_local.main(["--privilege-discovery", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["boundary"] == "privilege_discovery_visibility_only"
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["capabilities"][0]["name"] == "container_port_mapping"
    assert payload["capabilities"][0]["access_level"] == "docker_group_or_root"
    assert payload["capabilities"][0]["pressure"] == 2
    assert payload["capabilities"][0]["operational_benefit"]
    assert payload["capabilities"][0]["suggested_next_step"]


def test_privilege_discovery_empty_state_is_sane_and_read_only(monkeypatch, tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    monkeypatch.setattr(
        "seed_runtime.privilege_discovery.build_capability_needs", lambda state: []
    )

    assert seed_local.main(["--db", str(db), "--privilege-discovery"]) == 0
    output = capsys.readouterr().out
    assert "No unavailable capability needs" in output
    assert "no sudo" in output

    ledger = seed_local.SQLiteEventLedger(str(db))
    try:
        assert ledger.list_events(seed_local.DEFAULT_WORKSPACE) == []
    finally:
        ledger.close()

    state = State(workspace_id="ws")
    before = (dict(state.facts), dict(state.evidence), list(state.open_tool_needs))
    audit = build_privilege_discovery(state)
    after = (dict(state.facts), dict(state.evidence), list(state.open_tool_needs))
    assert before == after
    assert audit.mutates_cluster is False
    assert audit.writes_event_ledger is False


def test_unknown_capability_need_still_appears_with_unknown_access(monkeypatch):
    monkeypatch.setattr(
        "seed_runtime.privilege_discovery.build_capability_needs",
        lambda state: [_need("new_probe")],
    )

    audit = build_privilege_discovery(State(workspace_id="ws"))
    rendered = format_privilege_discovery(audit)

    assert audit.capabilities[0].name == "new_probe"
    assert audit.capabilities[0].access_level == "unknown"
    assert "inspect implementation evidence" in rendered
