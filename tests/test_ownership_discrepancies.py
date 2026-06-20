import importlib.util
import json
import sys
from pathlib import Path

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
    assert rows[0]["conflict"] is None
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


def test_no_ownership_evidence_reports_missing_owner(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db = tmp_path / "seed.sqlite"

    rows = run_json(seed_local, db, capsys, "node115")

    assert rows[0]["conflict"] == "missing_owner"
    assert rows[0]["candidate_owner"] is None
