from copy import deepcopy
import importlib.util
import sqlite3
import sys
from pathlib import Path

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.models import Entity, Fact, Goal, ToolNeed, ToolSpec, utc_now
from seed_runtime.observations import Observation
from seed_runtime.serialization import to_plain
from seed_runtime.state import GraphValidationIssue, State, StateProjector
from seed_runtime.state_views import (
    CapabilityView,
    FactView,
    IssueView,
    ObservationView,
    RequirementView,
    StateSummary,
    build_capability_view,
    build_fact_view,
    build_issue_view,
    build_observation_view,
    build_requirement_view,
    build_state_summary,
)

SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local_state_views", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _state() -> State:
    observed_at = utc_now()
    state = State(workspace_id="ws", last_event_id="evt_last", projection_version="v1")
    state.entities["node214"] = Entity(id="node214", kind="host", name="node214")
    state.facts["fact_runtime"] = Fact(
        id="fact_runtime",
        subject_id="jellyfin",
        predicate="runs_on",
        value="node214",
        evidence_ids=["evd_runtime"],
        confidence=0.91,
        observed_at=observed_at,
    )
    state.observations["obs_runtime"] = Observation(
        id="obs_runtime",
        source_type="discovery",
        observed_at=observed_at,
        subject="jellyfin",
        predicate="runs_on",
        value="node214",
    )
    state.goals["goal_backup"] = Goal(
        id="goal_backup",
        workspace_id="ws",
        summary="backup_restore required",
        status="active",
        created_from_event_id="evt_goal",
    )
    state.tool_needs["need_backup"] = ToolNeed(
        id="need_backup",
        workspace_id="ws",
        name="backup_restore",
        summary="Need backup restore",
        capability="backup_restore",
        reason="missing capability",
        requested_by_event_id="evt_need",
        status="proposed",
    )
    state.tools["docker"] = ToolSpec(
        name="docker",
        summary="Docker provider",
        toolkit_id="docker",
        input_schema={},
        output_schema={},
        policy_action="docker",
        implementation="tests:noop",
        risk_class="L1",
    )
    state.graph_issues.append(
        GraphValidationIssue(
            id="issue_storage",
            severity="error",
            subject="node214",
            relationship="storage",
            object="inconsistent",
            relationship_ids=["rel_storage"],
            source_fact_ids=["fact_runtime"],
            reason="storage inconsistency",
            hint=None,
            expected_subject_types=["host"],
            actual_subject_types=["host"],
            expected_object_types=["volume"],
            actual_object_types=["unknown"],
        )
    )
    return state


def test_fact_view_builds_correctly_from_projected_state():
    views = build_fact_view(_state())

    assert views == [
        FactView(
            fact_id="fact_runtime",
            subject="jellyfin",
            predicate="runs_on",
            object="node214",
            confidence=0.91,
            supporting_event_ids=["evd_runtime"],
        )
    ]


def test_observation_view_builds_correctly_from_projected_state():
    views = build_observation_view(_state())

    assert views == [
        ObservationView(
            observation_id="obs_runtime",
            observation_type="discovery",
            summary="jellyfin runs_on node214",
            supporting_event_ids=["obs_runtime"],
        )
    ]


def test_requirement_view_builds_correctly_from_projected_state():
    assert build_requirement_view(_state()) == [
        RequirementView(
            requirement_id="goal_backup",
            requirement_name="backup_restore required",
            status="active",
            supporting_event_ids=["evt_goal"],
        )
    ]


def test_capability_view_builds_correctly_from_projected_state():
    assert build_capability_view(_state()) == [
        CapabilityView(
            capability_id="need_backup",
            capability_name="backup_restore",
            status="proposed",
            supporting_event_ids=["evt_need"],
        ),
        CapabilityView(
            capability_id="docker",
            capability_name="docker",
            status="registered",
            supporting_event_ids=[],
        ),
    ]


def test_issue_view_builds_correctly_from_projected_state():
    assert build_issue_view(_state()) == [
        IssueView(
            issue_id="issue_storage",
            summary="node214 storage inconsistent: storage inconsistency",
            severity="high",
            supporting_event_ids=["fact_runtime", "rel_storage"],
        )
    ]


def test_state_summary_reports_correct_counts():
    assert build_state_summary(_state()) == StateSummary(
        facts_count=1,
        observations_count=1,
        requirements_count=1,
        capabilities_count=2,
        issues_count=1,
        last_event_id="evt_last",
        projection_version="v1",
    )


def test_state_views_are_deterministic():
    state = _state()

    assert build_fact_view(state) == build_fact_view(state)
    assert build_observation_view(state) == build_observation_view(state)
    assert build_requirement_view(state) == build_requirement_view(state)
    assert build_capability_view(state) == build_capability_view(state)
    assert build_issue_view(state) == build_issue_view(state)
    assert build_state_summary(state) == build_state_summary(state)


def test_state_views_do_not_mutate_state():
    state = _state()
    before = deepcopy(state)

    build_fact_view(state)
    build_observation_view(state)
    build_requirement_view(state)
    build_capability_view(state)
    build_issue_view(state)
    build_state_summary(state)

    assert state == before


def test_state_views_use_projected_state_without_raw_events():
    state = State(workspace_id="ws", last_event_id="evt_projected")
    state.facts["fact_projected"] = Fact(
        id="fact_projected",
        subject_id="svc",
        predicate="runtime",
        value="docker",
        evidence_ids=[],
        observed_at=utc_now(),
    )

    assert build_fact_view(state)[0].fact_id == "fact_projected"
    assert build_state_summary(state).last_event_id == "evt_projected"


def _event_count(db_path):
    with sqlite3.connect(db_path) as connection:
        return connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]


def _seed_db(db_path):
    ledger = SQLiteEventLedger(str(db_path))
    try:
        fact = Fact(
            id="fact_cli",
            subject_id="docker",
            predicate="available",
            value=True,
            evidence_ids=[],
            observed_at=utc_now(),
        )
        observation = Observation(
            id="obs_cli",
            source_type="user",
            observed_at=utc_now(),
            subject="docker",
            predicate="available",
            value=True,
        )
        goal = Goal(id="goal_cli", workspace_id="local", summary="keep docker available")
        need = ToolNeed(
            id="need_cli",
            workspace_id="local",
            name="docker_check",
            summary="Need docker checks",
            capability="docker_inspection",
            reason="current state",
        )
        ledger.append("observation.observed", "local", {"observation": to_plain(observation)})
        ledger.append("fact.observed", "local", {"fact": to_plain(fact)})
        ledger.append("goal.created", "local", {"goal": to_plain(goal)})
        ledger.append("tool_need.created", "local", {"tool_need": to_plain(need)})
    finally:
        ledger.close()


def test_cli_state_view_commands_do_not_append_events(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-views.sqlite"
    _seed_db(db_path)
    before = _event_count(db_path)

    commands = [
        ["--state-summary"],
        ["--current-facts"],
        ["--current-observations"],
        ["--current-requirements"],
        ["--current-capabilities"],
        ["--current-issues"],
    ]
    for command in commands:
        assert seed_local.main(["--db", str(db_path), *command]) == 0
        assert _event_count(db_path) == before

    output = capsys.readouterr().out
    assert "State Summary" in output
    assert "Current Facts" in output
    assert "Current Observations" in output
    assert "Current Requirements" in output
    assert "Current Capabilities" in output
    assert "Current Issues" in output


def test_cli_state_view_commands_do_not_invoke_runtime_provider_policy_or_tools(tmp_path, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-views-no-runtime.sqlite"
    _seed_db(db_path)

    def explode(*args, **kwargs):  # pragma: no cover - must not be called
        raise AssertionError("state view CLI must not build or invoke runtime behavior")

    monkeypatch.setattr(seed_local, "build_local_app", explode)

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0
    assert seed_local.main(["--db", str(db_path), "--current-facts"]) == 0
