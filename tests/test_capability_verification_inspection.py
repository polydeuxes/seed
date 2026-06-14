from datetime import datetime, timezone
import json

from seed_runtime.capability_verification import build_capability_verification_inspection
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


def _verification_fact(capability: str, value: str = "verified") -> Fact:
    return Fact(
        id=f"fact_{capability}_verified",
        subject_id=capability,
        predicate="capability_verified",
        value=value,
        evidence_ids=[f"evd_{capability}_verified"],
        observed_at=BASE_TIME,
        source_type="provider",
        confidence=0.9,
    )


def _verification_evidence(capability: str) -> Evidence:
    return Evidence(
        id=f"evd_{capability}_verified",
        workspace_id="ws",
        source="capability_report",
        kind="capability.verification.report",
        observed_at=BASE_TIME,
        payload={"capability": capability, "read_only": True},
        confidence=0.9,
    )


def _project(ledger: EventLedger):
    return StateProjector(ledger).project("ws")


def test_capability_candidates_can_be_inspected_for_verification_status():
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))})

    inspection = build_capability_verification_inspection(_project(ledger), filter_text="ssh")

    assert inspection.boundary == "capability_verification_inspection_only"
    assert inspection.verifications[0].candidate == "ssh_client"
    assert inspection.verifications[0].verification_status == "unverified"


def test_capability_verification_preserves_candidate_and_verification_evidence():
    ledger = EventLedger()
    ledger.append("evidence.observed", "ws", {"evidence": to_plain(_package_evidence("python3"))})
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("python3"))})
    ledger.append("evidence.observed", "ws", {"evidence": to_plain(_verification_evidence("python_runtime"))})
    ledger.append("fact.observed", "ws", {"fact": to_plain(_verification_fact("python_runtime"))})

    verification = build_capability_verification_inspection(_project(ledger)).verifications[0]

    assert verification.candidate == "python_runtime"
    assert verification.verification_status == "verified"
    assert verification.supporting_evidence[0].value == "python3"
    assert verification.verification_supporting_facts == ["fact_python_runtime_verified"]
    assert verification.verification_supporting_evidence[0].evidence_id == "evd_python_runtime_verified"


def test_verification_does_not_become_selection_permission_or_execution_authority():
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))})
    ledger.append("fact.observed", "ws", {"fact": to_plain(_verification_fact("ssh_client"))})
    state = _project(ledger)

    inspection = build_capability_verification_inspection(state)

    assert inspection.verifications[0].verification_status == "verified"
    assert "verified_capability_not_capability_selection" in inspection.notes
    assert "verified_capability_not_permission" in inspection.notes
    assert "verified_capability_not_execution_authority" in inspection.notes
    assert state.execution_proposals == {}
    assert state.pending_actions == {}
    assert state.action_plans == {}


def test_verification_invokes_no_tool_executor_or_policy(monkeypatch):
    import seed_runtime.execution as execution_module
    import seed_runtime.policy as policy_module

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

    inspection = build_capability_verification_inspection(_project(ledger))

    assert inspection.verifications[0].candidate == "git_client"
    assert "no_tool_execution" in inspection.notes
    assert "no_policy_evaluation" in inspection.notes


def test_verification_is_read_only_and_survives_absent_execution_systems(monkeypatch):
    import seed_runtime.runtime as runtime_module
    import seed_runtime.execution as execution_module

    monkeypatch.setattr(runtime_module, "Runtime", None)
    monkeypatch.setattr(execution_module, "ToolExecutor", None)
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("git"))})
    state = _project(ledger)
    before_events = [event.id for event in ledger.list_events("ws")]
    before_facts = dict(state.facts)

    inspection = build_capability_verification_inspection(state)

    assert inspection.verifications[0].verification_status == "unverified"
    assert [event.id for event in ledger.list_events("ws")] == before_events
    assert state.facts == before_facts


def test_capability_verification_cli_is_read_only_json_and_avoids_runtime(monkeypatch, tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    ledger = seed_local.SQLiteEventLedger(db_path)
    try:
        ledger.append("fact.observed", "local", {"fact": to_plain(_package_fact("openssh-client"))})
        ledger.append("fact.observed", "local", {"fact": to_plain(_verification_fact("ssh_client"))})
        before = len(ledger.list_events("local"))
    finally:
        ledger.close()

    monkeypatch.setattr(
        seed_local,
        "build_local_app",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("Runtime path used")),
    )
    monkeypatch.setattr(
        seed_local,
        "ToolExecutor",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("ToolExecutor used")),
    )

    assert seed_local.main(["--db", str(db_path), "--capability-verification", "ssh"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output["boundary"] == "capability_verification_inspection_only"
    assert output["verifications"][0]["candidate"] == "ssh_client"
    assert output["verifications"][0]["verification_status"] == "verified"
    assert "verified_capability_not_permission" in output["notes"]

    reopened = seed_local.SQLiteEventLedger(db_path)
    try:
        assert len(reopened.list_events("local")) == before
    finally:
        reopened.close()
