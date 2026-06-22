import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.capability_needs import CapabilityNeedEntry
from seed_runtime.capability_relationship import build_capability_relationship
from seed_runtime.state import State

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location(
        "seed_local_capability_relationship", SCRIPT_PATH
    )
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


def test_capability_relationship_human_multi_capability_visibility(monkeypatch, capsys):
    monkeypatch.setattr(
        "seed_runtime.capability_relationship.build_capability_needs",
        lambda state: [
            _need("listener_process_inventory", ("svc-a", "svc-b", "svc-c")),
            _need("container_port_mapping", ("svc-d",)),
        ],
    )
    seed_local = load_seed_local()

    assert seed_local.main(["--capability-relationship"]) == 0
    output = capsys.readouterr().out

    assert "Capability Relationship" in output
    assert "listener_process_inventory" in output
    assert "container_port_mapping" in output
    assert "partial_non_root" in output
    assert "docker_group_or_root" in output
    assert "service ownership attribution" in output
    assert "container port-to-service attribution" in output
    assert "3 affected subjects" in output
    assert "1 affected subjects" in output
    assert "Attainability:" in output and "unknown" in output
    assert "Expectation:" in output and "unknown" in output
    assert "not acquisition guidance" in output


def test_capability_relationship_json_single_capability_boundary(monkeypatch, capsys):
    monkeypatch.setattr(
        "seed_runtime.capability_relationship.build_capability_needs",
        lambda state: [
            _need("listener_process_inventory", ("svc-a", "svc-b")),
            _need("container_inventory", ("svc-c",)),
        ],
    )
    seed_local = load_seed_local()

    assert (
        seed_local.main(["--capability-relationship", "container_inventory", "--json"])
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["boundary"] == {
        "read_only": True,
        "writes_event_ledger": False,
        "mutates_cluster": False,
    }
    assert len(payload["capabilities"]) == 1
    relationship = payload["capabilities"][0]
    assert relationship["capability"] == "container_inventory"
    assert relationship["current_access"] == "docker_group_or_root"
    assert relationship["operational_benefit"] == "container ownership attribution"
    assert relationship["pressure"] == 1
    assert relationship["attainability"] == "unknown"
    assert relationship["expectation"] == "unknown"
    assert relationship["reasoning"]
    assert "deployment intent not observed" in relationship["known_limitations"]


def test_capability_relationship_is_read_only_and_no_ledger_writes(
    monkeypatch, tmp_path, capsys
):
    monkeypatch.setattr(
        "seed_runtime.capability_relationship.build_capability_needs",
        lambda state: [_need("listener_process_inventory")],
    )
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"

    assert seed_local.main(["--db", str(db), "--capability-relationship"]) == 0

    ledger = seed_local.SQLiteEventLedger(str(db))
    try:
        assert ledger.list_events(seed_local.DEFAULT_WORKSPACE) == []
    finally:
        ledger.close()

    state = State(workspace_id="ws")
    before = (dict(state.facts), dict(state.evidence), list(state.open_tool_needs))
    audit = build_capability_relationship(state)
    after = (dict(state.facts), dict(state.evidence), list(state.open_tool_needs))
    assert before == after
    assert audit.read_only is True
    assert audit.writes_event_ledger is False
    assert audit.mutates_cluster is False
