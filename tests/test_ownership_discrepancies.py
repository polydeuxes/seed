import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.state import StateProjector

SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local_ownership", SCRIPT_PATH)
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


def run_json(seed_local, db_path, capsys, subject=None):
    capsys.readouterr()
    argv = ["--db", str(db_path), "--ownership-discrepancies", "--json"]
    if subject:
        argv.extend(["--subject", subject])
    assert seed_local.main(argv) == 0
    return json.loads(capsys.readouterr().out)


def test_local_disk_mounted_only_on_node115_has_owner_without_conflict(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("/mnt/sda1", "mountpoint", "/mnt/sda1"),
        ("/mnt/sda1", "host", "node115"),
    )

    rows = run_json(seed_local, db, capsys, "/mnt/sda1")

    assert rows[0]["candidate_owner"] == "node115"
    assert rows[0]["conflict"] is None
    assert rows[0]["evidence"]
    assert rows[0]["label"] == "candidate"


def test_remote_mount_uses_source_owner_not_consumer(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("/mnt/media", "mountpoint", "/mnt/media"),
        ("/mnt/media", "host", "node200"),
        ("/mnt/media", "mount_source", "node115:/srv/media"),
    )

    rows = run_json(seed_local, db, capsys, "/mnt/media")

    assert rows[0]["candidate_owner"] == "node115"
    assert rows[0]["conflict"] == "remote_export_attribution_missing"
    assert "export attribution remains unverified" in rows[0]["reason"]
    assert all(ref["role"] != "ownership_fact_written" for ref in rows[0]["evidence"])


def test_same_mount_visible_on_multiple_nodes_reports_ambiguity(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("fs_a", "mountpoint", "/shared"),
        ("fs_a", "host", "node115"),
        ("fs_b", "mountpoint", "/shared"),
        ("fs_b", "host", "node200"),
    )

    rows = run_json(seed_local, db, capsys, "fs_a")

    assert rows[0]["conflict"] in {
        "multiple_candidate_owners",
        "shared_visibility_not_ownership",
    }


def test_service_listening_on_node115_has_candidate_owner(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("web", "listens_on", "node115:8080"))

    rows = run_json(seed_local, db, capsys, "web")

    assert rows[0]["kind"] == "service"
    assert rows[0]["candidate_owner"] == "node115"


def test_prometheus_target_without_host_or_process_is_insufficient(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("api", "prometheus_target", "10.0.0.7:9100"))

    rows = run_json(seed_local, db, capsys, "api")

    assert rows[0]["conflict"] == "insufficient_evidence"
    assert rows[0]["candidate_owner"] is None


def test_prometheus_target_with_local_listener_moves_to_attribution_need(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
        ("node-a", "listener_attribution_status", "unprivileged_socket_only"),
    )

    rows = run_json(seed_local, db, capsys, "api")

    assert rows[0]["candidate_owner"] == "node-a"
    assert rows[0]["conflict"] == "owner_not_observed"
    assert "Local listener evidence confirms" in rows[0]["reason"]
    assert any(ref["role"] == "local_listener_confirmed" for ref in rows[0]["evidence"])


def test_unrecorded_owner_not_observed_listener_gap_surfaces_capability_need(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
        ("node-a", "listener_attribution_status", "unprivileged_socket_only"),
    )

    ownership_rows = run_json(seed_local, db, capsys, "api")

    assert ownership_rows[0]["candidate_owner"] == "node-a"
    assert ownership_rows[0]["conflict"] == "owner_not_observed"
    assert ownership_rows[0]["confidence"] == 0.55
    assert seed_local.main(["--db", str(db), "--capability-needs", "--json"]) == 0
    needs = json.loads(capsys.readouterr().out)
    capabilities = {item["capability"]: item for item in needs}
    assert "listener_process_inventory" in capabilities
    assert capabilities["listener_process_inventory"]["subjects"] == ["api"]
    assert "listener_process_inventory" in capabilities[
        "listener_process_inventory"
    ]["needed_evidence"]

    state = StateProjector(SQLiteEventLedger(db)).project("local")
    entity_facts = [
        fact
        for fact in state.facts.values()
        if not fact.subject_id.startswith("diagnostic_run:")
    ]
    assert all("owner" not in fact.predicate for fact in entity_facts)


def test_local_listener_does_not_infer_container_ownership_and_records_attribution_needs(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )

    rows = run_json(seed_local, db, capsys, "api")
    assert all(
        ref["role"] != "process_or_container_observed" for ref in rows[0]["evidence"]
    )
    assert (
        seed_local.main(["--db", str(db), "--ownership-discrepancies", "--record"]) == 0
    )
    capsys.readouterr()
    assert seed_local.main(["--db", str(db), "--capability-needs", "--json"]) == 0
    needs = json.loads(capsys.readouterr().out)
    capabilities = {item["capability"] for item in needs}
    assert {
        "listener_process_inventory",
        "container_port_mapping",
        "container_inventory",
    }.issubset(capabilities)


def test_no_ownership_evidence_reports_missing_owner(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"

    rows = run_json(seed_local, db, capsys, "node115")

    assert rows[0]["conflict"] == "missing_owner"
    assert rows[0]["candidate_owner"] is None


def test_ownership_discrepancies_without_record_does_not_modify_event_count(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("api", "prometheus_target", "10.0.0.7:9100"))
    before = len(SQLiteEventLedger(db).list("local"))

    assert seed_local.main(["--db", str(db), "--ownership-discrepancies"]) == 0

    assert "insufficient_evidence" in capsys.readouterr().out
    after = len(SQLiteEventLedger(db).list("local"))
    assert after == before


def test_ownership_discrepancies_record_appends_diagnostic_run_scoped_facts(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("node116", "prometheus_target", "10.0.0.7:9100"))
    before_events = SQLiteEventLedger(db).list("local")

    assert (
        seed_local.main(["--db", str(db), "--ownership-discrepancies", "--record"]) == 0
    )

    capsys.readouterr()
    appended = SQLiteEventLedger(db).list("local")[len(before_events) :]
    facts = [
        event.payload["fact"] for event in appended if event.kind == "fact.inferred"
    ]
    assert facts
    run_subjects = {fact["subject_id"] for fact in facts}
    assert len(run_subjects) == 1
    assert next(iter(run_subjects)).startswith("diagnostic_run:")
    assert {"node116", "node115", "service", "filesystem"}.isdisjoint(run_subjects)
    assert any(
        f["predicate"] == "diagnostic_name" and f["value"] == "ownership_discrepancies"
        for f in facts
    )
    assert any(
        f["predicate"] == "needed_evidence" and f["value"] == "local_listener"
        for f in facts
    )
    assert any(
        f["predicate"] == "candidate_capability"
        and f["value"] == "tcp_listen_inventory"
        for f in facts
    )
    assert any(
        f["predicate"] == "privilege_level"
        and f["value"] == "non_root_partial_root_full"
        for f in facts
    )


def test_capability_needs_view_retrieves_recorded_needs_and_filters(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("node116", "prometheus_target", "10.0.0.7:9100"))
    assert (
        seed_local.main(["--db", str(db), "--ownership-discrepancies", "--record"]) == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            [
                "--db",
                str(db),
                "--capability-needs",
                "--subject",
                "node116",
                "--diagnostic",
                "ownership_discrepancies",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Capability Needs" in output
    assert "tcp_listen_inventory" in output
    assert "subjects: 1" in output
    assert "ownership_discrepancies" in output


def test_capability_needs_json_output_is_valid(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("node116", "prometheus_target", "10.0.0.7:9100"))
    assert (
        seed_local.main(["--db", str(db), "--ownership-discrepancies", "--record"]) == 0
    )
    capsys.readouterr()

    assert seed_local.main(["--db", str(db), "--capability-needs", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    tcp = next(item for item in payload if item["capability"] == "tcp_listen_inventory")
    assert tcp["subjects"] == ["node116"]
    assert tcp["diagnostics"] == ["ownership_discrepancies"]
    assert "local_listener" in tcp["needed_evidence"]


def test_recorded_diagnostic_needs_do_not_affect_inference_validation_or_ownership_facts(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("node116", "prometheus_target", "10.0.0.7:9100"))
    before_state = StateProjector(SQLiteEventLedger(db)).project("local")
    before_rows = run_json(seed_local, db, capsys, "node116")
    before_issues = [
        (i.subject, i.relationship, i.object, i.reason)
        for i in before_state.get_graph_issues()
    ]

    assert (
        seed_local.main(["--db", str(db), "--ownership-discrepancies", "--record"]) == 0
    )
    capsys.readouterr()

    after_state = StateProjector(SQLiteEventLedger(db)).project("local")
    after_rows = run_json(seed_local, db, capsys, "node116")
    after_issues = [
        (i.subject, i.relationship, i.object, i.reason)
        for i in after_state.get_graph_issues()
    ]
    assert after_rows == before_rows
    assert after_issues == before_issues
    entity_facts = [
        fact
        for fact in after_state.facts.values()
        if not fact.subject_id.startswith("diagnostic_run:")
    ]
    assert all("owner" not in fact.predicate for fact in entity_facts)
    assert all("capability" not in fact.predicate for fact in entity_facts)


def test_remote_mount_source_host_increases_confidence_preserves_uncertainty_and_records_needs(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("/mnt/node205/sda1", "mount_point", "/mnt/node205/sda1"),
        ("/mnt/node205/sda1", "host", "consumer"),
        ("/mnt/node205/sda1", "mount_source", "node205:/mnt/sda1"),
        ("/mnt/node205/sda1", "mount_source_host", "node205"),
        ("/mnt/node205/sda1", "mount_source_path", "/mnt/sda1"),
        (
            "/mnt/node205/sda1",
            "mount_attribution_status",
            "remote_source_observed_export_unattributed",
        ),
    )

    rows = run_json(seed_local, db, capsys, "/mnt/node205/sda1")

    assert rows[0]["candidate_owner"] == "node205"
    assert rows[0]["confidence"] > 0.72
    assert rows[0]["conflict"] == "remote_export_attribution_missing"
    assert "export attribution remains unverified" in rows[0]["reason"]
    assert all("owner" not in ref["predicate"] for ref in rows[0]["evidence"])
    assert any(
        ref["role"] == "remote_mount_source_host_observed"
        for ref in rows[0]["evidence"]
    )

    assert (
        seed_local.main(["--db", str(db), "--ownership-discrepancies", "--record"]) == 0
    )
    capsys.readouterr()
    assert seed_local.main(["--db", str(db), "--capability-needs", "--json"]) == 0
    needs = json.loads(capsys.readouterr().out)
    capabilities = {item["capability"] for item in needs}
    assert {
        "nfs_export_inventory",
        "smb_share_inventory",
        "remote_storage_export_inventory",
    } <= capabilities

    state = StateProjector(SQLiteEventLedger(db)).project("local")
    entity_facts = [
        fact
        for fact in state.facts.values()
        if not fact.subject_id.startswith("diagnostic_run:")
    ]
    assert all("owner" not in fact.predicate for fact in entity_facts)
