import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.state import State, StateProjector

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location(
        "seed_local_operational_story", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def ingest(seed_local, db_path, *observations):
    argv = ["--db", str(db_path), "--quiet-output"]
    for subject, predicate, value in observations:
        argv.extend(["--observe", subject, predicate, value])
    assert seed_local.main(argv) == 0


def test_operational_story_renders_and_json_is_valid(tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )

    assert seed_local.main(["--db", str(db), "--operational-story"]) == 0
    output = capsys.readouterr().out
    assert "Operational Story" in output
    assert "Current Focus:" in output
    assert "Primary Pressure:" in output
    assert "Current Investigation Path:" in output

    assert seed_local.main(["--db", str(db), "--operational-story", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["boundary"]["records_facts"] is False
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_cluster"] is False
    assert isinstance(payload["investigation_path"], list)


def test_operational_story_incorporates_surfaces(tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--operational-story", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    text = json.dumps(payload)

    assert payload["pressure"]["score"] > 0
    assert payload["pressure"]["category"]
    assert any(
        c["capability"] == "listener_process_inventory"
        for c in payload["capabilities"]
    )
    assert any(c["access_level"] == "partial_non_root" for c in payload["constraints"])
    assert any(c["area"] == "Listener Attribution" for c in payload["correlation_gaps"])
    assert payload["impact"]["overall"] in {"unknown", "improved", "regressed", "unchanged"}
    assert "capability_pressure" in text
    assert any(u["area"] == "impact" for u in payload["unknowns"])


def test_operational_story_empty_state_is_sane(monkeypatch, tmp_path):
    from seed_runtime.impact_audit import ImpactAudit
    from seed_runtime.operational_story import build_operational_story, format_operational_story
    from seed_runtime.pressure_audit import PressureAudit
    from seed_runtime.privilege_discovery import PrivilegeDiscoveryAudit
    from seed_runtime.correlation_audit import CorrelationAudit

    monkeypatch.setattr(
        "seed_runtime.operational_story.build_pressure_audit",
        lambda state, repo_root=None: PressureAudit(()),
    )
    monkeypatch.setattr(
        "seed_runtime.operational_story.build_capability_needs", lambda state: []
    )
    monkeypatch.setattr(
        "seed_runtime.operational_story.build_privilege_discovery",
        lambda state: PrivilegeDiscoveryAudit(()),
    )
    monkeypatch.setattr(
        "seed_runtime.operational_story.build_correlation_audit",
        lambda state, repo_root=None: CorrelationAudit((), {}),
    )
    monkeypatch.setattr(
        "seed_runtime.operational_story.build_impact_audit",
        lambda repo_root: ImpactAudit({}, [], "unknown", [], []),
    )

    story = build_operational_story(State(workspace_id="ws"), repo_root=tmp_path)
    output = format_operational_story(story)
    assert "no current pressure focus identified" in output
    assert "none observed" in output
    assert "Unknowns:" in output


def test_operational_story_does_not_write_events_or_mutate_cluster(tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("api", "prometheus_target", "127.0.0.1:9100"))
    ledger = SQLiteEventLedger(str(db))
    try:
        before = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()

    before_state = StateProjector(SQLiteEventLedger(db)).project(seed_local.DEFAULT_WORKSPACE)
    before_facts = dict(before_state.facts)
    assert seed_local.main(["--db", str(db), "--operational-story"]) == 0
    capsys.readouterr()

    ledger = SQLiteEventLedger(str(db))
    try:
        after = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
        after_state = StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()
    assert [event.id for event in after] == [event.id for event in before]
    assert dict(after_state.facts) == before_facts


def test_operational_story_registered_in_visibility_contract():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit

    entry = next(
        item for item in DIAGNOSTIC_INVENTORY if item.name == "operational_story"
    )
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "operational_story"
    ]
    assert rows
    assert {row.status for row in rows} <= {"consistent"}
