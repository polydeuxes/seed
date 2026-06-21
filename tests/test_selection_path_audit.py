import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.state import StateProjector

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location(
        "seed_local_selection_path", SCRIPT_PATH
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


def seeded_db(tmp_path):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )
    return seed_local, db


def test_selection_path_renders(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--selection-path", "current_focus"]) == 0
    output = capsys.readouterr().out

    assert "Selection Path" in output
    assert "Selected:" in output
    assert "Candidate Set:" in output
    assert "Selection Factors:" in output
    assert "Non-selected Candidates:" in output
    assert "Boundary:" in output


def test_selection_path_json_is_valid_and_surfaces_selection_details(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db), "--selection-path", "current_focus", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["selected"]
    assert payload["candidates"]
    assert {"candidate", "score", "rank", "reason", "evidence"} <= set(
        payload["candidates"][0]
    )
    assert payload["selection_factors"]
    assert "descending score" in payload["selection_factors"][0]
    assert isinstance(payload["non_selected"], list)
    assert payload["evidence"]
    assert payload["boundary"]["records_facts"] is False
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_cluster"] is False


def test_selection_path_unknown_logic_remains_explicit(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db), "--selection-path", "not_a_selection", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["selected"] == "unknown"
    assert payload["selection_factors"] == ["unknown"]
    assert payload["unknowns"]
    assert (
        "no implementation-backed selection evidence"
        in payload["unknowns"][0]["reason"]
    )


def test_selection_path_does_not_change_operational_story_selection(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--operational-story", "--json"]) == 0
    story_before = json.loads(capsys.readouterr().out)
    assert (
        seed_local.main(
            ["--db", str(db), "--selection-path", "current_focus", "--json"]
        )
        == 0
    )
    selection = json.loads(capsys.readouterr().out)
    assert seed_local.main(["--db", str(db), "--operational-story", "--json"]) == 0
    story_after = json.loads(capsys.readouterr().out)

    assert story_after == story_before
    assert selection["outcome"]["focus"] == story_before["focus"]


def test_selection_path_does_not_write_events_or_mutate_cluster(tmp_path, capsys):
    seed_local, db = seeded_db(tmp_path)
    ledger = SQLiteEventLedger(str(db))
    try:
        before = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()

    before_state = StateProjector(SQLiteEventLedger(db)).project(
        seed_local.DEFAULT_WORKSPACE
    )
    before_facts = dict(before_state.facts)
    assert seed_local.main(["--db", str(db), "--selection-path", "current_focus"]) == 0
    capsys.readouterr()

    ledger = SQLiteEventLedger(str(db))
    try:
        after = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
        after_state = StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()

    assert [event.id for event in after] == [event.id for event in before]
    assert dict(after_state.facts) == before_facts


def test_selection_path_registered_in_visibility_contracts():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit

    entry = next(item for item in DIAGNOSTIC_INVENTORY if item.name == "selection_path")
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "selection_path"
    ]
    assert rows
    assert {row.status for row in rows} <= {"consistent"}
