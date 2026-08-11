import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.consumer_dependency_audit import ConsumerAudit
from seed_runtime.correlation_audit import (
    build_correlation_audit,
    format_correlation_audit,
)
from seed_runtime.events import SQLiteEventLedger
from seed_runtime.state import State, StateProjector

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location("seed_local_correlation", SCRIPT_PATH)
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


def test_correlation_audit_renders_and_json_is_valid(tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
        ("node-a", "listener_attribution_status", "process_observed"),
        ("node-a", "listening_process_id", "123"),
        ("node-a", "listening_process_name", "node_exporter"),
    )

    assert seed_local.main(["--db", str(db), "--correlation-audit"]) == 0
    output = capsys.readouterr().out
    assert "Correlation Audit" in output
    assert "Listener Attribution" in output
    assert "Candidate Boundary:" in output

    assert seed_local.main(["--db", str(db), "--correlation-audit", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert isinstance(payload["findings"], list)
    assert payload["metadata"]["records_facts"] is False
    assert payload["metadata"]["mutates_cluster"] is False


def test_listener_process_evidence_with_unresolved_ownership_reports_correlation_gap(
    tmp_path, capsys
):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
        ("node-a", "listener_attribution_status", "process_observed"),
        ("node-a", "listening_process_id", "123"),
        ("node-a", "listening_process_name", "node_exporter"),
    )
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--correlation-audit", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    listener = next(
        f for f in payload["findings"] if f["area"] == "Listener Attribution"
    )
    assert listener["evidence_present"]["listener_process_facts"] == 2
    assert listener["observed_result"]["owner_not_observed_rows"] == 1
    assert "process attribution exists" in listener["assessment"]
    assert listener["candidate_boundary"] == "service identity correlation"


def test_correlation_findings_remain_explanatory_and_do_not_infer_ownership(
    tmp_path, capsys
):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
        ("node-a", "listener_attribution_status", "process_observed"),
        ("node-a", "listening_process_name", "node_exporter"),
    )
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--correlation-audit", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    text = json.dumps(payload).lower()
    assert "implement service identity model" not in text
    assert "does_not_infer_ownership" in text
    assert "candidate_owner" not in text

    state = StateProjector(SQLiteEventLedger(db)).project("local")
    entity_facts = [
        fact
        for fact in state.facts.values()
        if not fact.subject_id.startswith("diagnostic_run:")
    ]
    assert all("owner" not in fact.predicate for fact in entity_facts)


def test_correlation_audit_empty_state_is_sane(monkeypatch):
    monkeypatch.setattr(
        "seed_runtime.correlation_audit.build_consumer_audit",
        lambda root: ConsumerAudit(items=(), metadata={}),
    )
    audit = build_correlation_audit(State(workspace_id="ws"), repo_root=ROOT)
    assert audit.findings == ()
    assert "(none)" in format_correlation_audit(audit)


def test_correlation_audit_does_not_write_events_or_mutate_cluster(tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("api", "prometheus_target", "127.0.0.1:9100"))
    ledger = SQLiteEventLedger(str(db))
    try:
        before = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()

    assert seed_local.main(["--db", str(db), "--correlation-audit"]) == 0
    capsys.readouterr()

    ledger = SQLiteEventLedger(str(db))
    try:
        after = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()
    assert [event.id for event in after] == [event.id for event in before]


def test_correlation_audit_registered_in_visibility_contract():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit

    entry = next(
        item for item in DIAGNOSTIC_INVENTORY if item.name == "correlation_audit"
    )
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False

    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "correlation_audit"
    ]
    assert rows
    assert {row.status for row in rows} <= {"consistent"}
