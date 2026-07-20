from datetime import datetime, timezone
import json

from seed_runtime.capability_candidates import build_capability_candidates
from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.fact_index import build_fact_index
from seed_runtime.facts import Fact
from seed_runtime.projection_store import (
    FACT_INDEX_NAME,
    FACT_INDEX_VERSION,
    STATE_PROJECTION_VERSION,
    SQLiteProjectionStore,
)
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
    import seed_runtime.policy as policy_module

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


def test_capability_candidate_output_is_identical_with_fact_index():
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("git"))})
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("docker.io"))})
    state = _project(ledger)
    fact_index = build_fact_index(state, workspace_id="ws")

    without_index = build_capability_candidates(state)
    with_index = build_capability_candidates(state, fact_index=fact_index)

    assert with_index == without_index


def test_capability_candidate_inspection_consumes_fact_index():
    package_fact = _package_fact("openssh-client")

    class PackageFactIndex:
        fact_ids_by_subject_predicate = {
            "localhost": {"package_installed": [package_fact.id]}
        }

        def __init__(self):
            self.lookups: list[tuple[str, str]] = []

        def current_facts(self, state, subject, predicate, *, include_expired=False):
            self.lookups.append((subject, predicate))
            return [package_fact]

    fact_index = PackageFactIndex()

    inspection = build_capability_candidates(
        _project(EventLedger()), filter_text="ssh", fact_index=fact_index
    )

    assert [candidate.candidate for candidate in inspection.candidates] == ["ssh_client"]
    assert fact_index.lookups == [("localhost", "package_installed")]


def test_capability_candidate_index_path_is_read_only():
    ledger = EventLedger()
    ledger.append("fact.observed", "ws", {"fact": to_plain(_package_fact("curl"))})
    state = _project(ledger)
    fact_index = build_fact_index(state, workspace_id="ws")
    before_events = [event.id for event in ledger.list_events("ws")]
    before_observations = dict(state.observations)
    before_facts = dict(state.facts)

    build_capability_candidates(state, fact_index=fact_index)

    assert [event.id for event in ledger.list_events("ws")] == before_events
    assert state.observations == before_observations
    assert state.facts == before_facts


def test_capability_observation_survives_absent_execution_systems(monkeypatch):
    import seed_runtime.runtime as runtime_module

    monkeypatch.setattr(runtime_module, "Runtime", None)
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


def test_capability_candidates_cli_builds_fact_index_cache_on_miss(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "candidate-index-miss.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    try:
        event = ledger.append(
            "fact.observed",
            "local",
            {"fact": to_plain(_package_fact("openssh-client"))},
        )
    finally:
        ledger.close()

    assert (
        seed_local.main(["--db", str(db_path), "--capability-candidates", "ssh"])
        == 0
    )

    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert output["candidates"][0]["candidate"] == "ssh_client"
    assert "Fact index cache: miss" in captured.err
    assert "Building fact index..." in captured.err

    store = SQLiteProjectionStore(str(db_path))
    try:
        snapshot = store.load_derived_index_snapshot(
            "local",
            FACT_INDEX_NAME,
            FACT_INDEX_VERSION,
            state_projection_version=STATE_PROJECTION_VERSION,
            state_last_event_id=event.id,
        )
    finally:
        store.close()
    assert snapshot is not None


def test_capability_candidates_cli_uses_fact_index_cache_hit(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "candidate-index-hit.sqlite"
    ledger = SQLiteEventLedger(str(db_path))
    try:
        ledger.append(
            "fact.observed",
            "local",
            {"fact": to_plain(_package_fact("openssh-client"))},
        )
    finally:
        ledger.close()

    assert (
        seed_local.main(["--db", str(db_path), "--capability-candidates", "ssh"])
        == 0
    )
    first = capsys.readouterr()
    assert "Fact index cache: miss" in first.err

    assert (
        seed_local.main(["--db", str(db_path), "--capability-candidates", "ssh"])
        == 0
    )
    second = capsys.readouterr()

    assert "Fact index cache: hit" in second.err
    assert json.loads(second.out)["candidates"][0]["candidate"] == "ssh_client"
