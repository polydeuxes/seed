from datetime import datetime, timezone
import json

from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.verification_evidence import build_verification_evidence
from seed_runtime.capability_verification import build_capability_verification_inspection

from test_seed_local_script import load_seed_local_module

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _package_fact(package: str) -> Fact:
    return Fact(
        id=f"fact_{package.replace('-', '_')}",
        subject_id="localhost",
        predicate="package_installed",
        value=package,
        evidence_ids=[f"evd_{package.replace('-', '_')}"],
        observed_at=BASE_TIME,
        source_type="discovery",
        confidence=1.0,
    )


def _project(ledger: EventLedger):
    return StateProjector(ledger).project("ws")


def test_verification_evidence_observes_path_binary(tmp_path):
    ssh = tmp_path / "ssh"
    ssh.write_text("stub", encoding="utf-8")
    ssh.chmod(0o755)
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))})

    inspection = build_verification_evidence(_project(ledger), filter_text="ssh", path_env=str(tmp_path))

    assert inspection.boundary == "verification_evidence_acquisition_only"
    assert inspection.evidence[0].candidate == "ssh_client"
    assert inspection.evidence[0].evidence_type == "binary_path_observed"
    assert inspection.evidence[0].observation_source == "local_path_inspection"
    assert inspection.evidence[0].value == str(ssh)
    assert "binary_not_invoked" in inspection.evidence[0].support_notes


def test_verification_evidence_remains_inspectable_and_supports_verification_inspection(tmp_path, monkeypatch):
    python = tmp_path / "python3"
    python.write_text("stub", encoding="utf-8")
    python.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path))
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("python3"))})

    verification = build_capability_verification_inspection(_project(ledger), filter_text="python").verifications[0]

    assert verification.candidate == "python_runtime"
    assert verification.verification_status == "unverified"
    assert verification.acquired_verification_evidence[0].value == str(python)
    assert "verification_evidence_not_capability_verification" in verification.acquired_verification_evidence[0].boundary_notes


def test_verification_evidence_cli_is_read_only_and_survives_absent_execution(monkeypatch, tmp_path, capsys):
    seed_local = load_seed_local_module()
    binary_dir = tmp_path / "bin"
    binary_dir.mkdir()
    ssh = binary_dir / "ssh"
    ssh.write_text("stub", encoding="utf-8")
    ssh.chmod(0o755)
    monkeypatch.setenv("PATH", str(binary_dir))
    db_path = tmp_path / "seed-local.sqlite"
    ledger = seed_local.SQLiteEventLedger(db_path)
    try:
        ledger.append("fact.observed", "local", {"fact": to_plain(_package_fact("openssh-client"))})
        before = len(ledger.list_events("local"))
    finally:
        ledger.close()

    assert seed_local.main(["--db", str(db_path), "--verification-evidence", "ssh"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output["boundary"] == "verification_evidence_acquisition_only"
    assert output["evidence"][0]["candidate"] == "ssh_client"
    assert output["evidence"][0]["value"] == str(ssh)
    reopened = seed_local.SQLiteEventLedger(db_path)
    try:
        assert len(reopened.list_events("local")) == before
    finally:
        reopened.close()
