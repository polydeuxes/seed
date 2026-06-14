from datetime import datetime, timezone
import json

from seed_runtime.capability_candidates import build_capability_candidates
from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

from test_seed_local_script import load_seed_local_module

BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _package_fact(
    package: str, *, fact_id: str | None = None, evidence_id: str | None = None
) -> Fact:
    return Fact(
        id=fact_id or f"fact_{package.replace('-', '_').replace('.', '_')}",
        subject_id="localhost",
        predicate="package_installed",
        value=package,
        evidence_ids=[
            evidence_id or f"evd_{package.replace('-', '_').replace('.', '_')}"
        ],
        observed_at=BASE_TIME,
        source_type="discovery",
        confidence=1.0,
    )


def _evidence(package: str, *, evidence_id: str | None = None) -> Evidence:
    return Evidence(
        id=evidence_id or f"evd_{package.replace('-', '_').replace('.', '_')}",
        workspace_id="ws",
        source="local_dpkg_status",
        kind="local.package.status",
        observed_at=BASE_TIME,
        payload={"package": package, "read_only": True},
        confidence=1.0,
    )


def _project(ledger: EventLedger):
    return StateProjector(ledger).project("ws")


def test_observed_package_evidence_produces_capability_candidate():
    ledger = EventLedger()
    ledger.append(
        "fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))}
    )
    state = _project(ledger)

    inspection = build_capability_candidates(state)

    assert [candidate.candidate for candidate in inspection.candidates] == ["ssh_client"]
    assert inspection.candidates[0].confidence == "supported_by_observed_package"
    assert inspection.boundary == "capability_candidate_preservation_only"


def test_capability_candidate_preserves_supporting_evidence():
    ledger = EventLedger()
    ledger.append(
        "evidence.observed", "ws", {"evidence": to_plain(_evidence("python3"))}
    )
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("python3"))})
    state = _project(ledger)

    candidate = build_capability_candidates(state).candidates[0]

    assert candidate.candidate == "python_runtime"
    assert candidate.supporting_evidence[0].fact_id == "fact_python3"
    assert candidate.supporting_evidence[0].predicate == "package_installed"
    assert candidate.supporting_evidence[0].value == "python3"
    assert candidate.supporting_evidence[0].evidence_ids == ["evd_python3"]
    assert candidate.supporting_evidence[0].evidence_summaries


def test_capability_candidates_do_not_become_execution_decisions():
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("git"))})
    state = _project(ledger)

    inspection = build_capability_candidates(state)

    assert "capability_candidate_not_execution_decision" in inspection.notes
    assert "no_capability_selection" in inspection.notes
    assert state.execution_proposals == {}
    assert state.pending_actions == {}
    assert state.action_plans == {}


def test_capability_candidates_do_not_invoke_tool_executor_or_policy(monkeypatch):
    import seed_runtime.execution as execution_module
    import seed_runtime.policy as policy_module

    monkeypatch.setattr(
        execution_module.ToolExecutor,
        "__init__",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("ToolExecutor used")
        ),
    )
    monkeypatch.setattr(
        policy_module.PolicyGate,
        "evaluate",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("policy evaluated")
        ),
    )
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("curl"))})

    inspection = build_capability_candidates(_project(ledger))

    assert inspection.candidates[0].candidate == "http_client"
    assert "no_tool_execution" in inspection.notes
    assert "no_policy_evaluation" in inspection.notes


def test_capability_candidates_are_inspectable_and_filterable():
    ledger = EventLedger()
    ledger.append(
        "fact.observed", "ws", {"fact": to_plain(_package_fact("openssh-client"))}
    )
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("docker.io"))})
    state = _project(ledger)

    inspection = build_capability_candidates(state, filter_text="ssh")

    assert [candidate.candidate for candidate in inspection.candidates] == ["ssh_client"]
    assert inspection.filter == "ssh"


def test_capability_candidates_are_read_only():
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("docker.io"))})
    state = _project(ledger)
    before_events = [event.id for event in ledger.list_events("ws")]
    before_facts = dict(state.facts)

    build_capability_candidates(state)

    assert [event.id for event in ledger.list_events("ws")] == before_events
    assert state.facts == before_facts


def test_capability_observation_survives_absent_execution_systems(monkeypatch):
    import seed_runtime.runtime as runtime_module
    import seed_runtime.execution as execution_module

    monkeypatch.setattr(runtime_module, "Runtime", None)
    monkeypatch.setattr(execution_module, "ToolExecutor", None)
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("git"))})

    assert (
        build_capability_candidates(_project(ledger)).candidates[0].candidate
        == "git_client"
    )


def test_capability_candidates_cli_is_read_only_json_and_avoids_runtime(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    ledger = seed_local.SQLiteEventLedger(db_path)
    try:
        ledger.append(
            "fact.observed",
            "local",
            {"fact": to_plain(_package_fact("openssh-client"))},
        )
        before = len(ledger.list_events("local"))
    finally:
        ledger.close()

    monkeypatch.setattr(
        seed_local,
        "build_local_app",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("Runtime path used")
        ),
    )
    monkeypatch.setattr(
        seed_local,
        "ToolExecutor",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("ToolExecutor used")
        ),
    )

    assert (
        seed_local.main(["--db", str(db_path), "--capability-candidates", "ssh"])
        == 0
    )

    output = json.loads(capsys.readouterr().out)
    assert output["boundary"] == "capability_candidate_preservation_only"
    assert output["candidates"][0]["candidate"] == "ssh_client"
    assert (
        output["candidates"][0]["supporting_evidence"][0]["value"]
        == "openssh-client"
    )
    assert "no_tool_execution" in output["notes"]

    reopened = seed_local.SQLiteEventLedger(db_path)
    try:
        assert len(reopened.list_events("local")) == before
    finally:
        reopened.close()
