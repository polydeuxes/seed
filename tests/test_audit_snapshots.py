import json
from scripts import seed_local
from seed_runtime.audit_snapshots import (
    collect_git_metadata,
    compare_audit_snapshots,
    create_audit_snapshot,
    format_audit_compare,
)


def test_snapshot_writes_observation_files(tmp_path):
    result = create_audit_snapshot(
        repo_root=tmp_path,
        kind="observation_inventory",
        payload={"predicates": [], "providers": [], "families": [], "summary": {}},
        command="seed --audit-snapshot observation_inventory",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id="2026-06-20T184233Z",
    )
    assert result.directory == tmp_path / ".audit" / "seed" / "2026-06-20T184233Z"
    assert (result.directory / "metadata.json").exists()
    assert (result.directory / "git.json").exists()
    assert (result.directory / "observation_inventory.json").exists()
    meta = json.loads((result.directory / "metadata.json").read_text())
    assert meta["kind"] == "observation_inventory"
    assert meta["event_count"] == 0


def test_snapshot_writes_ownership_files(tmp_path):
    result = create_audit_snapshot(
        repo_root=tmp_path,
        kind="ownership_discrepancies",
        payload=[],
        command="seed --audit-snapshot ownership_discrepancies",
        seed_db="seed.db",
        events=[],
        projection_version="v1",
        snapshot_id="2026-06-20T185012Z",
    )
    assert (result.directory / "metadata.json").exists()
    assert (result.directory / "git.json").exists()
    assert (result.directory / "ownership_discrepancies.json").exists()


def test_audit_is_gitignored():
    assert ".audit/" in open(".gitignore", encoding="utf-8").read().splitlines()


def test_cli_lists_saved_snapshots(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)
    create_audit_snapshot(
        repo_root=tmp_path,
        kind="observation_inventory",
        payload={"predicates": [], "providers": [], "families": [], "summary": {}},
        command="seed --audit-snapshot observation_inventory",
        seed_db=None,
        events=[],
        projection_version="v1",
        snapshot_id="2026-06-20T184233Z",
    )
    assert seed_local.main(["--audit-snapshots"]) == 0
    out = capsys.readouterr().out
    assert "Snapshot ID" in out
    assert "2026-06-20T184233Z" in out
    assert "observation_inventory" in out


def test_observation_compare_reports_predicates_and_summary(tmp_path):
    for sid, predicates, count in [
        ("2026-06-20T184233Z", ["up"], 1),
        ("2026-06-20T185012Z", ["up", "listening_socket"], 2),
    ]:
        create_audit_snapshot(
            repo_root=tmp_path,
            kind="observation_inventory",
            payload={
                "predicates": [{"predicate": p} for p in predicates],
                "providers": [],
                "families": [],
                "summary": {"predicate_count": count},
            },
            command="seed --audit-snapshot observation_inventory",
            seed_db=None,
            events=[],
            projection_version="v1",
            snapshot_id=sid,
        )
    diff = compare_audit_snapshots(tmp_path, "previous", "latest", kind="observation_inventory")
    assert diff["predicates"]["added"] == ["listening_socket"]
    assert diff["summary_changes"]["predicate_count"] == {"from": 1, "to": 2}
    text = format_audit_compare(diff)
    assert "listening_socket" in text
    assert "predicate_count: 1 -> 2" in text


def test_ownership_compare_reports_rows_and_changes(tmp_path):
    a = [{"kind": "service", "subject": "svc", "conflict": "insufficient_evidence", "confidence": 0.0, "candidate_owner": None, "capability_needs": ["local_listener"]}]
    b = [
        {"kind": "service", "subject": "svc", "conflict": "owner_not_observed", "confidence": 0.5, "candidate_owner": "node1", "capability_needs": ["listener_process_inventory"]},
        {"kind": "storage", "subject": "disk", "conflict": "missing_owner", "confidence": 0.0, "candidate_owner": None},
    ]
    create_audit_snapshot(repo_root=tmp_path, kind="ownership_discrepancies", payload=a, command="seed --audit-snapshot ownership_discrepancies", seed_db=None, events=[], projection_version="v1", snapshot_id="2026-06-20T184233Z")
    create_audit_snapshot(repo_root=tmp_path, kind="ownership_discrepancies", payload=b, command="seed --audit-snapshot ownership_discrepancies", seed_db=None, events=[], projection_version="v1", snapshot_id="2026-06-20T185012Z")
    diff = compare_audit_snapshots(tmp_path, "previous", "latest", kind="ownership_discrepancies")
    assert len(diff["added_rows"]) == 1
    assert diff["changes"]["conflict"][0]["from"] == "insufficient_evidence"
    assert diff["changes"]["confidence"][0]["to"] == 0.5
    assert diff["changes"]["candidate_owner"][0]["to"] == "node1"
    assert diff["changes"]["capability_needs"][0]["added"] == ["listener_process_inventory"]


def test_cli_audit_compare_json_is_valid(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)
    for sid, predicates in [("2026-06-20T184233Z", ["up"]), ("2026-06-20T185012Z", ["down"])]:
        create_audit_snapshot(repo_root=tmp_path, kind="observation_inventory", payload={"predicates": [{"predicate": p} for p in predicates], "providers": [], "families": [], "summary": {}}, command="seed --audit-snapshot observation_inventory", seed_db=None, events=[], projection_version="v1", snapshot_id=sid)
    assert seed_local.main(["--audit-compare", "latest", "previous", "--kind", "observation_inventory", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "observation_inventory"


def test_git_metadata_failure_is_graceful(tmp_path):
    def fail(*args, **kwargs):
        raise FileNotFoundError("git missing")
    payload = collect_git_metadata(tmp_path, runner=fail)
    assert payload["available"] is False
    assert "git missing" in payload["reason"]
