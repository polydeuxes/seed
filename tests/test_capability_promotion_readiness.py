from datetime import datetime, timezone
import json

from seed_runtime.capability_promotion_readiness import (
    build_capability_promotion_readiness_inspection,
)
from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

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


def _package_evidence(package: str) -> Evidence:
    return Evidence(
        id=f"evd_{package.replace('-', '_')}",
        workspace_id="ws",
        source="local_dpkg_status",
        kind="local.package.status",
        observed_at=BASE_TIME,
        payload={"package": package, "read_only": True},
        confidence=1.0,
    )


def _project(ledger: EventLedger):
    return StateProjector(ledger).project("ws")


def test_promotion_readiness_can_be_inspected_and_preserves_support(tmp_path):
    ssh = tmp_path / "ssh"
    ssh.write_text("stub", encoding="utf-8")
    ssh.chmod(0o755)
    ledger = EventLedger()
    ledger.append("evidence.observed", "ws", {"evidence": to_plain(_package_evidence("openssh-client"))})
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))})

    inspection = build_capability_promotion_readiness_inspection(
        _project(ledger), filter_text="ssh", path_env=str(tmp_path)
    )

    readiness = inspection.readiness[0]
    assert inspection.boundary == "capability_promotion_readiness_inspection_only"
    assert readiness.candidate == "ssh_client"
    assert readiness.promotion_readiness == "supported"
    assert readiness.candidate_support[0].value == "openssh-client"
    assert readiness.candidate_support[0].evidence_summaries == ["local.package.status from local_dpkg_status"]
    assert readiness.verification_support[0].evidence_type == "binary_path_observed"
    assert readiness.verification_support[0].value == str(ssh)
    assert "promotion_readiness_not_promotion" in readiness.boundary_notes


def test_promotion_readiness_reports_missing_verification_support(tmp_path):
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))})

    readiness = build_capability_promotion_readiness_inspection(
        _project(ledger), filter_text="ssh", path_env=str(tmp_path)
    ).readiness[0]

    assert readiness.candidate == "ssh_client"
    assert readiness.candidate_support[0].value == "openssh-client"
    assert readiness.verification_support == []
    assert readiness.promotion_readiness == "unsupported"
    assert "verification support is missing" in readiness.rationale


def test_promotion_readiness_does_not_create_capability_verified_facts_or_write_events(tmp_path):
    ssh = tmp_path / "ssh"
    ssh.write_text("stub", encoding="utf-8")
    ssh.chmod(0o755)
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))})
    state = _project(ledger)
    before_events = [event.id for event in ledger.list_events("ws")]
    before_facts = dict(state.facts)

    inspection = build_capability_promotion_readiness_inspection(
        state, filter_text="ssh", path_env=str(tmp_path)
    )

    assert inspection.readiness[0].promotion_readiness == "supported"
    assert [event.id for event in ledger.list_events("ws")] == before_events
    assert state.facts == before_facts
    assert not any(fact.predicate == "capability_verified" for fact in state.facts.values())
    assert "no_capability_verified_fact_creation" in inspection.notes


def test_promotion_readiness_invokes_no_tool_executor_or_policy(monkeypatch, tmp_path):
    import seed_runtime.execution as execution_module
    import seed_runtime.policy as policy_module

    git = tmp_path / "git"
    git.write_text("stub", encoding="utf-8")
    git.chmod(0o755)
    monkeypatch.setattr(
        execution_module.ToolExecutor,
        "__init__",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("ToolExecutor used")),
    )
    monkeypatch.setattr(
        policy_module.PolicyGate,
        "evaluate",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("policy evaluated")),
    )
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("git"))})

    inspection = build_capability_promotion_readiness_inspection(
        _project(ledger), path_env=str(tmp_path)
    )

    assert inspection.readiness[0].candidate == "git_client"
    assert inspection.readiness[0].promotion_readiness == "supported"
    assert "no_tool_execution" in inspection.notes
    assert "no_policy_evaluation" in inspection.notes


def test_promotion_readiness_survives_absent_execution_systems(monkeypatch, tmp_path):
    import seed_runtime.runtime as runtime_module
    import seed_runtime.execution as execution_module

    monkeypatch.setattr(runtime_module, "Runtime", None)
    monkeypatch.setattr(execution_module, "ToolExecutor", None)
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("python3"))})

    inspection = build_capability_promotion_readiness_inspection(
        _project(ledger), filter_text="python", path_env=str(tmp_path)
    )

    assert inspection.readiness[0].candidate == "python_runtime"
    assert inspection.readiness[0].promotion_readiness == "unsupported"


def test_promotion_readiness_cli_is_read_only_json_and_avoids_runtime(monkeypatch, tmp_path, capsys):
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
    monkeypatch.setattr(seed_local, "build_local_app", lambda *a, **k: (_ for _ in ()).throw(AssertionError("Runtime used")))
    monkeypatch.setattr(seed_local, "ToolExecutor", None)

    assert seed_local.main(["--db", str(db_path), "--capability-promotion-readiness", "ssh"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output["boundary"] == "capability_promotion_readiness_inspection_only"
    assert output["readiness"][0]["candidate"] == "ssh_client"
    assert output["readiness"][0]["promotion_readiness"] == "supported"
    assert output["readiness"][0]["verification_support"][0]["value"] == str(ssh)
    reopened = seed_local.SQLiteEventLedger(db_path)
    try:
        assert len(reopened.list_events("local")) == before
    finally:
        reopened.close()
