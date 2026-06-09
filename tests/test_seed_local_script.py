import importlib.util
import json
import sys
from pathlib import Path

import pytest

from seed_runtime.models import ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State

from seed_runtime.intent_classifier import IntentDecisionModel, IntentPromptModelClient
from seed_runtime.runtime import Runtime

SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_local_app_uses_intent_classifier_path_and_loads_echo_toolkit():
    seed_local = load_seed_local_module()

    app = seed_local.build_local_app(model="qwen2.5:3b", timeout_seconds=12.0)

    assert isinstance(app.model_client, IntentPromptModelClient)
    assert isinstance(app.runtime, Runtime)
    assert isinstance(app.runtime.model, IntentDecisionModel)
    assert [tool.name for tool in app.context_composer.registry.list_tools()] == [
        "echo"
    ]
    assert app.model_client.transport.extra_payload == {
        "model": "qwen2.5:3b",
        "stream": False,
        "format": "json",
    }
    assert app.model_client.transport.url == "http://localhost:11434/api/generate"
    assert app.model_client.transport.timeout_seconds == 12.0


def test_one_shot_echo_uses_deterministic_fallback_without_ollama():
    seed_local = load_seed_local_module()
    app = seed_local.build_local_app()

    result = app.run("echo hello")

    assert result["response"]["kind"] == "tool_result"
    assert result["response"]["payload"]["output"]["message"] == "hello"
    assert [event["kind"] for event in result["events"]] == [
        "input.user_message",
        "model.decision.proposed",
        "tool.call.started",
        "tool.call.completed",
        "evidence.observed",
    ]
    assert result["events"][0]["session_id"] == app.session_id


def test_normal_cli_missing_tool_records_open_tool_need_and_recommendations(
    monkeypatch,
):
    seed_local = load_seed_local_module()
    app = seed_local.build_local_app()

    monkeypatch.setattr(
        app.model_client,
        "complete",
        lambda context: (
            '{"intent":"missing_tool","reason":"needs service tool","arguments":{}}'
        ),
    )

    result = app.run("restart jellyfin?")

    assert result["response"]["kind"] == "tool_need"
    assert (
        result["response"]["payload"]["tool_need"]["capability"] == "service_management"
    )
    assert isinstance(result["response"]["payload"]["recommendations"], list)
    state = app.projector.project(app.workspace_id)
    assert [need.capability for need in state.open_tool_needs] == ["service_management"]


def test_normal_cli_answer_uses_runtime():
    seed_local = load_seed_local_module()
    app = seed_local.build_local_app()

    result = app.run("What is Docker?")

    assert result["response"]["kind"] == "answer"
    assert "Docker" in result["response"]["message"]
    assert [event["kind"] for event in result["events"]] == [
        "input.user_message",
        "model.decision.proposed",
        "response.answer",
    ]


def test_runtime_tool_output_evidence_appears_in_projected_state():
    seed_local = load_seed_local_module()
    app = seed_local.build_local_app()

    app.run("echo evidence")

    state = app.projector.project(app.workspace_id)
    assert len(state.evidence) == 1
    evidence = next(iter(state.evidence.values()))
    assert evidence.source == "tool:echo"
    assert evidence.payload["message"] == "evidence"


def test_old_runtime_module_remains_available():
    seed_local = load_seed_local_module()

    assert seed_local.Runtime is Runtime
    assert Path("seed_runtime/runtime.py").exists()


def test_parser_supports_required_modes_and_model_selection():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        [
            "--http",
            "--events",
            "--raw",
            "--raw-only",
            "--plan",
            "--preconditions",
            "plan_cli",
            "--db",
            ".seed-local.sqlite",
            "--model",
            "qwen2.5:3b",
            "install",
            "docker",
        ]
    )

    assert args.http is True
    assert args.events is True
    assert args.raw is True
    assert args.raw_only is True
    assert args.plan is True
    assert args.preconditions == "plan_cli"
    assert args.db == ".seed-local.sqlite"
    assert args.model == "qwen2.5:3b"
    assert args.message == ["install", "docker"]


def test_parser_supports_execution_proposal_generation():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--db", ".seed-local.sqlite", "--proposal", "plan_cli"]
    )

    assert args.db == ".seed-local.sqlite"
    assert args.proposal == "plan_cli"


def test_cli_default_prints_concise_summary_without_event_ledger(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["echo hello"]) == 0

    output = capsys.readouterr().out
    assert "Tool echo completed." in output
    assert "Output:" in output
    assert "tool.call.started" not in output
    assert "Events:" not in output


def test_format_response_summary_lists_tool_need_recommendations():
    seed_local = load_seed_local_module()

    summary = seed_local.format_response_summary(
        {
            "response": {
                "kind": "tool_need",
                "message": "Recorded tool need weather_lookup.",
                "payload": {
                    "tool_need": {"capability": "weather_lookup"},
                    "recommendations": [
                        {
                            "provider": "open_meteo",
                            "score": 55,
                            "reasons": ["catalog default"],
                        },
                        {
                            "provider": "wttr",
                            "score": 50,
                            "reasons": ["provider matches known runtime: api"],
                        },
                    ],
                },
            }
        }
    )

    assert summary == (
        "Recorded tool need weather_lookup.\n"
        "Recommendations:\n"
        "1. open_meteo (score=55)\n"
        "   - catalog default\n"
        "\n"
        "2. wttr (score=50)\n"
        "   - provider matches known runtime: api"
    )


def test_format_response_summary_omits_empty_recommendations_for_unknown_capability():
    seed_local = load_seed_local_module()

    summary = seed_local.format_response_summary(
        {
            "response": {
                "kind": "tool_need",
                "message": "Recorded tool need custom_workflow.",
                "payload": {
                    "tool_need": {"capability": "custom_workflow"},
                    "recommendations": [],
                },
            }
        }
    )

    assert summary == "Recorded tool need custom_workflow."


def test_cli_events_includes_full_event_ledger(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--events", "echo hello"]) == 0

    output = capsys.readouterr().out
    assert "Tool echo completed." in output
    assert "Events:" in output
    assert "tool.call.completed" in output
    assert "model.decision.proposed" in output


def test_cli_raw_continues_through_runtime(monkeypatch, capsys):
    seed_local = load_seed_local_module()

    monkeypatch.setattr(seed_local.LocalSeedApp, "raw", lambda self, text: "RAW INTENT")

    assert seed_local.main(["--raw", "echo hello"]) == 0

    output = capsys.readouterr().out
    assert "Raw model output:\nRAW INTENT" in output
    assert "Tool echo completed." in output
    assert "Output:" in output


def test_cli_raw_only_prints_raw_output_and_exits(monkeypatch, capsys):
    seed_local = load_seed_local_module()

    monkeypatch.setattr(seed_local.LocalSeedApp, "raw", lambda self, text: "RAW INTENT")

    def fail_run(self, text):
        pytest.fail("--raw-only should not run the runtime")

    monkeypatch.setattr(seed_local.LocalSeedApp, "run", fail_run)

    assert seed_local.main(["--raw-only", "echo hello"]) == 0

    assert capsys.readouterr().out == "RAW INTENT\n"


def test_raw_preview_does_not_append_to_runtime_ledger(monkeypatch):
    seed_local = load_seed_local_module()
    app = seed_local.build_local_app()

    monkeypatch.setattr(app.model_client, "complete", lambda context: "RAW INTENT")

    assert app.raw("install docker") == "RAW INTENT"
    assert app.ledger.list(app.workspace_id) == []


def test_fact_seed_ingests_observation_evidence_and_fact_before_user_message():
    seed_local = load_seed_local_module()
    app = seed_local.build_local_app()

    app.seed_facts([seed_local.DevFactSeed("jellyfin", "runtime", "docker")])
    result = app.run("echo hello")

    event_kinds = [event["kind"] for event in result["events"]]
    assert event_kinds[:4] == [
        "observation.observed",
        "evidence.observed",
        "fact.observed",
        "input.user_message",
    ]

    state = app.projector.project(app.workspace_id)
    observation = next(iter(state.observations.values()))
    fact = next(iter(state.facts.values()))
    evidence = next(iter(state.evidence.values()))
    assert fact.subject_id == "jellyfin"
    assert fact.predicate == "runtime"
    assert fact.value == "docker"
    assert fact.evidence_ids == [evidence.id]
    assert fact.source_type == "user"
    assert fact.confidence == 1.0
    assert fact.observed_at == observation.observed_at
    assert evidence.payload == {
        "observation_id": observation.id,
        "source_type": "user",
        "subject": "jellyfin",
        "predicate": "runtime",
        "value": "docker",
        "metadata": {"ingested_by": "scripts.seed_local --fact"},
        "dimensions": {},
        "expires_at": None,
    }


def test_cli_fact_creates_observation_fact_through_ingestor(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--fact", "jellyfin", "runtime", "docker"]) == 0

    output = capsys.readouterr().out
    assert "fact_id: fact_obs_" in output
    assert "subject: jellyfin" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "source_type: user" in output
    assert "confidence: 1.0" in output


def test_observe_and_fact_produce_equivalent_projected_facts():
    seed_local = load_seed_local_module()

    fact_app = seed_local.build_local_app()
    observe_app = seed_local.build_local_app()

    fact_app.seed_facts([seed_local.DevFactSeed("jellyfin", "runtime", "docker")])
    observe_app.observe(
        [seed_local.DevObservationSeed("jellyfin", "runtime", "docker")]
    )

    fact_state = fact_app.projector.project(fact_app.workspace_id)
    observe_state = observe_app.projector.project(observe_app.workspace_id)
    fact_best = fact_state.get_best_fact("jellyfin", "runtime")
    observe_best = observe_state.get_best_fact("jellyfin", "runtime")
    fact_support = fact_state.get_fact_support("jellyfin", "runtime")
    observe_support = observe_state.get_fact_support("jellyfin", "runtime")

    assert fact_best is not None
    assert observe_best is not None
    assert fact_best.subject_id == observe_best.subject_id == "jellyfin"
    assert fact_best.predicate == observe_best.predicate == "runtime"
    assert fact_best.value == observe_best.value == "docker"
    assert fact_best.source_type == observe_best.source_type == "user"
    assert fact_best.confidence == observe_best.confidence == 1.0
    assert fact_support is not None
    assert observe_support is not None
    assert fact_support.value == observe_support.value == "docker"
    assert fact_support.confidence == observe_support.confidence == 0.85
    assert fact_support.source_types == observe_support.source_types == ["user"]


def test_cli_fact_seed_influences_service_recommendation_ranking(monkeypatch, capsys):
    seed_local = load_seed_local_module()

    monkeypatch.setattr(
        seed_local.IntentPromptModelClient,
        "complete",
        lambda self, context: (
            '{"intent":"missing_tool","reason":"needs service tool","arguments":{}}'
        ),
    )

    assert (
        seed_local.main(
            ["--fact", "jellyfin", "runtime", "docker", "restart jellyfin?"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "1. docker_container_lifecycle" in output
    assert "2. systemctl_cli" in output
    assert output.index("1. docker_container_lifecycle") < output.index(
        "2. systemctl_cli"
    )
    assert "known runtime: docker" in output


def test_cli_plan_prints_non_executable_top_recommendation_plan(monkeypatch, capsys):
    seed_local = load_seed_local_module()

    monkeypatch.setattr(
        seed_local.IntentPromptModelClient,
        "complete",
        lambda self, context: (
            '{"intent":"missing_tool","reason":"needs service tool","arguments":{}}'
        ),
    )

    assert (
        seed_local.main(
            ["--fact", "jellyfin", "runtime", "docker", "--plan", "restart jellyfin?"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "1. docker_container_lifecycle" in output
    assert "Plan:\nPropose using docker_container_lifecycle" in output
    assert "action_plan_id: plan_" in output
    assert "- Identify target host for service." in output
    assert "- Confirm container name." in output
    assert "- Verify Docker access." in output
    assert "- Request approval before restart." in output
    assert "tool.call.started" not in output
    assert "action_plan.created" not in output
    assert "approved" not in output.lower()


def test_parser_accepts_observation_ingestion_options():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        [
            "--observe",
            "jellyfin",
            "runtime",
            "docker",
            "--source-type",
            "discovery",
            "--confidence",
            "0.81",
        ]
    )

    assert args.observe == [["jellyfin", "runtime", "docker"]]
    assert args.source_type == "discovery"
    assert args.confidence == 0.81


def test_parser_accepts_json_observation_ingestion_option():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(["--observe-json", "inventory.json"])

    assert args.observe_json == "inventory.json"


def test_cli_observe_json_ingests_imported_observations(tmp_path, capsys):
    seed_local = load_seed_local_module()
    json_path = tmp_path / "observations.json"
    json_path.write_text(
        '{"observations":[{"subject":"jellyfin","predicate":"runtime",'
        '"value":"docker","confidence":0.95}]}',
        encoding="utf-8",
    )

    assert seed_local.main(["--observe-json", str(json_path)]) == 0

    output = capsys.readouterr().out
    assert "fact_id: fact_obs_" in output
    assert "subject: jellyfin" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "source_type: imported" in output
    assert "confidence: 0.95" in output


def test_parser_accepts_json_observation_export_option():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--export-observations-json", "inventory.json"]
    )

    assert args.export_observations_json == "inventory.json"


def test_cli_export_observations_json_writes_inventory(tmp_path, capsys):
    seed_local = load_seed_local_module()
    output_path = tmp_path / "observations.json"

    assert (
        seed_local.main(
            [
                "--observe",
                "jellyfin",
                "runtime",
                "docker",
                "--source-type",
                "discovery",
                "--confidence",
                "0.81",
                "--export-observations-json",
                str(output_path),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert "exported 1 observation(s)" in output
    assert payload == {
        "observations": [
            {
                "confidence": 0.81,
                "observed_at": payload["observations"][0]["observed_at"],
                "predicate": "runtime",
                "source_type": "discovery",
                "subject": "jellyfin",
                "value": "docker",
            }
        ]
    }


def test_parser_accepts_repeatable_fact_seed_options():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        [
            "--fact",
            "jellyfin",
            "runtime",
            "docker",
            "--fact",
            "plex",
            "runtime",
            "systemd",
            "restart",
            "jellyfin?",
        ]
    )

    assert args.fact == [
        ["jellyfin", "runtime", "docker"],
        ["plex", "runtime", "systemd"],
    ]
    assert args.message == ["restart", "jellyfin?"]


def seed_cli_action_plan(
    seed_local,
    db_path,
    plan_id="plan_cli",
    *,
    provider="open_meteo",
    capability="weather_lookup",
    risk_class="L1",
    requires_approval=False,
):
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    ledger.append(
        "action_plan.created",
        "local",
        {
            "action_plan": {
                "id": plan_id,
                "tool_need_id": "need_cli",
                "provider": provider,
                "capability": capability,
                "summary": f"Propose using {provider}",
                "steps": ["Determine location."],
                "risk_class": risk_class,
                "requires_approval": requires_approval,
                "status": "proposed",
                "rejection_reason": None,
                "replacement_plan_id": None,
                "executable": False,
            }
        },
        session_id="local",
    )
    ledger.close()


def test_parser_supports_execution_proposal_authorization_grant():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        [
            "--db",
            ".seed-local.sqlite",
            "--authorize-proposal",
            "eprop_cli",
            "--grant-method",
            "interactive_prompt",
            "--ttl-seconds",
            "300",
        ]
    )

    assert args.db == ".seed-local.sqlite"
    assert args.authorize_proposal == "eprop_cli"
    assert args.grant_method == "interactive_prompt"
    assert args.ttl_seconds == 300


def test_cli_authorize_execution_grants_for_accepted_plan_without_executing(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )
    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--fact",
                "jellyfin",
                "host",
                "node115",
                "--fact",
                "jellyfin",
                "container",
                "jellyfin",
                "--proposal",
                "plan_cli",
            ]
        )
        == 0
    )
    proposal_output = capsys.readouterr().out
    proposal_id = next(
        line.split(": ", 1)[1]
        for line in proposal_output.splitlines()
        if line.startswith("execution_proposal_id: ")
    )
    assert seed_local.main(["--db", str(db_path), "--accept-plan", "plan_cli"]) == 0
    capsys.readouterr()

    def fail_load_manifest(self, path):
        pytest.fail("authorize-proposal must not register tools")

    monkeypatch.setattr(seed_local.ToolRegistry, "load_manifest", fail_load_manifest)

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--authorize-proposal",
                proposal_id,
                "--grant-method",
                "interactive_prompt",
                "--ttl-seconds",
                "300",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "execution_authorization_id: auth_" in output
    assert f"execution_proposal_id: {proposal_id}" in output
    assert "action_plan_id: plan_cli" in output
    assert "tool_name: docker_container_lifecycle" in output
    assert "arguments_fingerprint: sha256:" in output
    assert "expires_at: " in output
    assert "secret_seen_by_seed: false" in output
    assert "tool.call" not in output

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        events = ledger.list_events("local")
    finally:
        ledger.close()
    kinds = [event.kind for event in events]
    assert "tool.call.started" not in kinds
    assert "tool.call.completed" not in kinds


def test_cli_authorize_proposal_requires_accepted_plan(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )
    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--fact",
                "jellyfin",
                "host",
                "node115",
                "--fact",
                "jellyfin",
                "container",
                "jellyfin",
                "--proposal",
                "plan_cli",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    proposal_id = next(
        line.split(": ", 1)[1]
        for line in output.splitlines()
        if line.startswith("execution_proposal_id: ")
    )

    with pytest.raises(seed_local.ActionPlanTransitionError, match="only accepted"):
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--authorize-proposal",
                proposal_id,
            ]
        )


def test_cli_authorize_proposal_rejects_direct_tool_arguments(tmp_path):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path)

    with pytest.raises(SystemExit):
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--authorize-proposal",
                "eprop_cli",
                "--tool-arguments-json",
                '{"token": "not-accepted"}',
            ]
        )


def test_cli_preconditions_prints_inspect_only_report_without_registering_tools(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    def fail_load_manifest(self, path):
        pytest.fail("precondition reports must not register tools")

    monkeypatch.setattr(seed_local.ToolRegistry, "load_manifest", fail_load_manifest)

    assert seed_local.main(["--db", str(db_path), "--preconditions", "plan_cli"]) == 0

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "executable: false" in output
    assert (
        "missing:\n- target_host_known\n- provider_registered\n- execution_authorization_present"
        in output
    )
    assert "preconditions:" in output
    assert "- id: target_host_known\n  satisfied: false" in output
    assert (
        "reason: no host entity, entity host fact, or target host fact is present"
        in output
    )
    assert "tool.call" not in output
    assert "approved" not in output.lower()


def test_cli_proposal_missing_plan_prints_reason_without_traceback(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"

    assert seed_local.main(["--db", str(db_path), "--proposal", "plan_missing"]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "missing_reason: plan not found" in captured.err
    assert "action_plan_id: plan_missing" in captured.err
    assert "Traceback" not in captured.err


def test_cli_proposal_reports_provider_tool_not_registered(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L1",
        requires_approval=False,
    )

    assert seed_local.main(["--db", str(db_path), "--proposal", "plan_cli"]) == 0

    output = capsys.readouterr().out
    assert "missing_reason: provider/tool not registered" in output
    assert "provider_registered" in output


def test_cli_proposal_reports_preconditions_missing(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--proposal",
                "plan_cli",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "missing_reason: preconditions missing" in output
    assert "target_host_known" in output


def test_cli_proposal_reports_service_host_missing(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        ledger.append(
            "entity.upserted",
            "local",
            {"entity": {"id": "host_1", "kind": "host", "name": "node-1"}},
        )
    finally:
        ledger.close()

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--fact",
                "svc",
                "container",
                "web",
                "--proposal",
                "plan_cli",
            ]
        )
        == 1
    )

    captured = capsys.readouterr()
    assert "missing_reason: service host missing" in captured.err
    assert "Traceback" not in captured.err


def test_cli_proposal_reports_unsupported_provider(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="systemd_service_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "systemd_service_lifecycle",
                "--fact",
                "svc",
                "host",
                "node-1",
                "--fact",
                "svc",
                "container",
                "web",
                "--proposal",
                "plan_cli",
            ]
        )
        == 1
    )

    captured = capsys.readouterr()
    assert "missing_reason: provider unsupported" in captured.err
    assert "Traceback" not in captured.err


def test_cli_proposal_reports_container_name_missing(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--fact",
                "svc",
                "host",
                "node-1",
                "--proposal",
                "plan_cli",
            ]
        )
        == 1
    )

    captured = capsys.readouterr()
    assert "missing_reason: container name missing" in captured.err
    assert "Traceback" not in captured.err


def test_cli_proposal_reports_builder_returned_none(monkeypatch, tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    monkeypatch.setattr(
        seed_local.ExecutionProposalService,
        "_tool_call_for_plan",
        lambda self, action_plan, state: None,
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--fact",
                "svc",
                "host",
                "node-1",
                "--fact",
                "svc",
                "container",
                "web",
                "--proposal",
                "plan_cli",
            ]
        )
        == 1
    )

    captured = capsys.readouterr()
    assert "missing_reason: proposal builder returned None" in captured.err
    assert "Traceback" not in captured.err


def test_cli_proposal_prints_missing_preconditions_without_creating_proposal(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    def fail_load_manifest(self, path):
        pytest.fail("proposal reports must not register tools")

    monkeypatch.setattr(seed_local.ToolRegistry, "load_manifest", fail_load_manifest)

    assert seed_local.main(["--db", str(db_path), "--proposal", "plan_cli"]) == 0

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "executable: false" in output
    assert (
        "missing:\n- target_host_known\n- provider_registered\n"
        "- execution_authorization_present" in output
    )
    assert "execution_proposal_id:" not in output
    assert "tool.call" not in output

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        kinds = [event.kind for event in ledger.list_events("local")]
    finally:
        ledger.close()
    assert "execution_proposal.created" not in kinds
    assert "tool.call.started" not in kinds
    assert "tool.call.completed" not in kinds


def test_cli_proposal_creates_concrete_non_executable_proposal_without_executing(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    def fail_load_manifest(self, path):
        pytest.fail("proposal generation must not register tools")

    monkeypatch.setattr(seed_local.ToolRegistry, "load_manifest", fail_load_manifest)

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--fact",
                "jellyfin",
                "host",
                "node115",
                "--fact",
                "jellyfin",
                "container",
                "jellyfin",
                "--proposal",
                "plan_cli",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "execution_proposal_id: eprop_" in output
    assert "action_plan_id: plan_cli" in output
    assert "provider: docker_container_lifecycle" in output
    assert "tool_name: docker_container_lifecycle" in output
    assert (
        'tool_arguments: {"action": "restart", "container": "jellyfin", "host": "node115"}'
        in output
    )
    assert "arguments_fingerprint: sha256:" in output
    assert "executable: false" in output
    assert "tool.call" not in output

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        events = ledger.list_events("local")
    finally:
        ledger.close()
    kinds = [event.kind for event in events]
    assert "execution_proposal.created" in kinds
    assert "tool.call.started" not in kinds
    assert "tool.call.completed" not in kinds
    proposal_event = next(
        event for event in events if event.kind == "execution_proposal.created"
    )
    assert proposal_event.payload["execution_proposal"]["executable"] is False


def test_cli_preconditions_reports_satisfied_preconditions(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path)
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    ledger.append(
        "tool.registered",
        "local",
        {
            "tool": {
                "name": "open_meteo",
                "summary": "Weather lookup.",
                "toolkit_id": "open_meteo",
                "input_schema": {},
                "output_schema": {},
                "policy_action": "weather_lookup.open_meteo",
                "implementation": "toolkits.generated.weather:lookup",
                "risk_class": "L1",
            }
        },
    )
    ledger.close()

    assert seed_local.main(["--db", str(db_path), "--preconditions", "plan_cli"]) == 0

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "executable: true" in output
    assert "missing:\n- none" in output
    assert "- id: provider_registered\n  satisfied: true" in output
    assert "registered tool is available: open_meteo" in output


def test_cli_accept_plan_prints_accepted_without_registering_tools(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path)

    def fail_load_manifest(self, path):
        pytest.fail("lifecycle commands must not register tools")

    monkeypatch.setattr(seed_local.ToolRegistry, "load_manifest", fail_load_manifest)

    assert seed_local.main(["--db", str(db_path), "--accept-plan", "plan_cli"]) == 0

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "status: accepted" in output
    assert "tool.call" not in output
    assert "approved" not in output.lower()


def test_cli_accept_plan_prints_clean_error_for_already_accepted_plan(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path, plan_id="plan_000001")
    assert seed_local.main(["--db", str(db_path), "--accept-plan", "plan_000001"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--accept-plan", "plan_000001"]) == 0

    output = capsys.readouterr().out
    assert output == (
        "action_plan_id: plan_000001\n"
        "status: accepted\n"
        "error: invalid transition accepted -> accepted\n"
    )


def test_cli_reject_plan_prints_rejected_and_reason(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path)

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--reject-plan",
                "plan_cli",
                "--reason",
                "Use another provider",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "status: rejected" in output
    assert "rejection_reason: Use another provider" in output


def test_cli_supersede_plan_prints_superseded_and_replacement_id(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path)

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--supersede-plan",
                "plan_cli",
                "--replacement-plan",
                "plan_replacement",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "status: superseded" in output
    assert "replacement_plan_id: plan_replacement" in output


def test_parser_accepts_registered_provider_and_fact_examples():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        [
            "--db",
            ".seed-local.sqlite",
            "--registered-provider",
            "docker_container_lifecycle",
            "--fact",
            "jellyfin",
            "host",
            "node115",
            "--preconditions",
            "plan_000001",
        ]
    )

    assert args.registered_provider == ["docker_container_lifecycle"]
    assert args.fact == [["jellyfin", "host", "node115"]]
    assert args.preconditions == "plan_000001"


def test_cli_preconditions_satisfy_provider_and_host_but_not_approval(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--registered-provider",
                "docker_container_lifecycle",
                "--fact",
                "jellyfin",
                "host",
                "node115",
                "--preconditions",
                "plan_cli",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "executable: false" in output
    assert "missing:\n- execution_authorization_present" in output
    assert "- id: target_host_known\n  satisfied: true" in output
    assert "entity host fact is present" in output
    assert "- id: provider_registered\n  satisfied: true" in output
    assert "registered tool is available: docker_container_lifecycle" in output
    assert "- id: execution_authorization_present\n  satisfied: false" in output
    assert "no current execution authorization is present" in output
    assert "tool.call" not in output
    assert "approved" not in output.lower()


def test_cli_preconditions_target_host_fact_satisfies_host_requirement(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(
        seed_local,
        db_path,
        provider="docker_container_lifecycle",
        capability="service_management",
        risk_class="L3",
        requires_approval=True,
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "jellyfin",
                "target_host",
                "node115",
                "--preconditions",
                "plan_cli",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "- id: target_host_known\n  satisfied: true" in output
    assert "target host fact is present" in output
    assert "- provider_registered" in output
    assert "- execution_authorization_present" in output


def test_cli_approve_plan_prints_approved_without_executing_or_registering(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path)
    assert seed_local.main(["--db", str(db_path), "--accept-plan", "plan_cli"]) == 0
    capsys.readouterr()

    def fail_load_manifest(self, path):
        pytest.fail("approve-plan must not register tools")

    monkeypatch.setattr(seed_local.ToolRegistry, "load_manifest", fail_load_manifest)

    assert seed_local.main(["--db", str(db_path), "--approve-plan", "plan_cli"]) == 0

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "status: accepted" in output
    assert "approved: true" in output
    assert "tool.call" not in output

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        kinds = [event.kind for event in ledger.list_events("local")]
    finally:
        ledger.close()
    assert "action_plan.approved" in kinds
    assert "pending_action.approved" not in kinds
    assert "tool.registered" not in kinds


def test_cli_approve_plan_prints_clean_error_for_proposed_plan(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    seed_cli_action_plan(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--approve-plan", "plan_cli"]) == 0

    output = capsys.readouterr().out
    assert "action_plan_id: plan_cli" in output
    assert "status: proposed" in output
    assert "error: invalid transition proposed -> approved" in output


def test_dev_fact_cli_rejects_secret_field_names():
    seed_local = load_seed_local_module()

    for field in ("password", "passphrase", "token", "private_key"):
        with pytest.raises(ValueError, match="secret field"):
            seed_local.parse_dev_fact(["node-1", field, "not-accepted"])


def test_dev_fact_cli_rejects_json_values_with_secret_fields():
    seed_local = load_seed_local_module()

    with pytest.raises(ValueError, match="secret field"):
        seed_local.parse_dev_fact(["node-1", "auth", '{"token": "not-accepted"}'])


def test_parser_supports_handoff_generation():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--db", ".seed-local.sqlite", "--handoff", "plan_cli"]
    )

    assert args.db == ".seed-local.sqlite"
    assert args.handoff == "plan_cli"


def test_handoff_cli_function_prints_non_executable_plan_for_accepted_action_plan(
    tmp_path,
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    setup_args = seed_local.build_parser().parse_args(
        [
            "--db",
            str(db_path),
            "--workspace",
            "ws",
            "--session",
            "ses",
            "--handoff",
            "placeholder",
        ]
    )
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        service = seed_local.ActionPlanService(ledger)
        plan = service.create_plan(
            ToolNeed(
                id="need_service",
                workspace_id="ws",
                name="restart_jellyfin",
                capability="service_management",
                summary="Restart Jellyfin",
                reason="User asked",
            ),
            RankedRecommendation(
                provider="docker_container_lifecycle",
                summary="Use Docker lifecycle operations.",
                kind="local_cli",
                source="docker",
                risk_class="L3",
                notes="Requires approval.",
                score=100,
                reasons=[],
                reasoning=[],
            ),
            State(workspace_id="ws"),
        )
        service.accept_plan("ws", plan.id)
    finally:
        ledger.close()

    setup_args.handoff = plan.id
    result = seed_local.handoff_plan(setup_args)
    output = seed_local.format_handoff_plan(result)

    assert "handoff_plan" in result
    assert "handoff_plan_id: handoff_" in output
    assert "provider: docker_container_lifecycle" in output
    assert "backend_type: ansible" in output
    assert "operation: service.manage" in output
    assert "policy_summary: risk_class=L3" in output
    assert "secret_boundary: Seed passes only this non-secret plan boundary" in output


def test_parser_supports_fact_projection_queries():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()

    support_args = parser.parse_args(["--fact-support", "jellyfin", "runtime"])
    best_args = parser.parse_args(["--best-fact", "jellyfin", "runtime"])
    conflicts_args = parser.parse_args(["--fact-conflicts"])
    refreshes_args = parser.parse_args(["--stale-fact-refreshes"])
    summary_args = parser.parse_args(["--state-summary"])

    history_args = parser.parse_args(
        [
            "--fact-support",
            "node115",
            "up",
            "--include-history",
        ]
    )
    history_alias_args = parser.parse_args(
        [
            "--fact-support",
            "node115",
            "up",
            "--history",
        ]
    )

    assert support_args.fact_support == ["jellyfin", "runtime"]
    assert history_args.include_history is True
    assert history_alias_args.include_history is True
    assert best_args.best_fact == ["jellyfin", "runtime"]
    assert conflicts_args.fact_conflicts is True
    assert refreshes_args.stale_fact_refreshes is True
    assert summary_args.state_summary is True


def test_cli_state_summary_reports_projected_world_model_without_ingestion(
    tmp_path, monkeypatch, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    ingestor = seed_local.ObservationIngestor(ledger)
    now = seed_local.utc_now()

    observations = [
        seed_local.Observation(
            id="obs_host_up_old",
            source_type="discovery",
            observed_at=now - seed_local.timedelta(minutes=2),
            subject="host-up",
            predicate="availability_status",
            value="down",
        ),
        seed_local.Observation(
            id="obs_host_up_current",
            source_type="discovery",
            observed_at=now - seed_local.timedelta(minutes=1),
            subject="host-up",
            predicate="availability_status",
            value="up",
        ),
        seed_local.Observation(
            id="obs_host_down",
            source_type="discovery",
            observed_at=now,
            subject="host-down",
            predicate="availability_status",
            value="down",
        ),
        seed_local.Observation(
            id="obs_alias",
            source_type="user",
            observed_at=now,
            subject="host-up",
            predicate="alias",
            value="10.0.0.10",
        ),
        seed_local.Observation(
            id="obs_runtime_docker",
            source_type="user",
            observed_at=now,
            subject="host-up",
            predicate="runtime",
            value="docker",
        ),
        seed_local.Observation(
            id="obs_runtime_systemd",
            source_type="user",
            observed_at=now,
            subject="host-up",
            predicate="runtime",
            value="systemd",
        ),
        seed_local.Observation(
            id="obs_stale_os",
            source_type="imported",
            observed_at=now - seed_local.timedelta(days=2),
            subject="old-host",
            predicate="os",
            value="linux",
            expires_at=now - seed_local.timedelta(days=1),
        ),
        seed_local.Observation(
            id="obs_filesystem_free",
            source_type="discovery",
            observed_at=now,
            subject="10.0.0.10",
            predicate="filesystem_free_bytes",
            value=40,
            dimensions={"mountpoint": "/", "device": "/dev/sda1"},
        ),
        seed_local.Observation(
            id="obs_filesystem_total",
            source_type="discovery",
            observed_at=now,
            subject="10.0.0.10",
            predicate="filesystem_total_bytes",
            value=100,
            dimensions={"mountpoint": "/", "device": "/dev/sda1"},
        ),
    ]
    try:
        for observation in observations:
            ingestor.ingest(observation, "local")
    finally:
        ledger.close()

    monkeypatch.setattr(
        seed_local,
        "seed_dev_state_from_args",
        lambda args, ledger: pytest.fail("state summary must not ingest"),
    )

    monkeypatch.setattr(
        seed_local,
        "build_local_app",
        lambda *args, **kwargs: pytest.fail("state summary must not execute"),
    )

    assert (
        seed_local.main(
            ["--db", str(db_path), "--state-summary", "--fact", "ignored", "os", "x"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "entities: 3" in output
    assert "facts: 8" in output
    assert "durable facts: 4" in output
    assert "measurement current samples: 4" in output
    assert "conflicts: 1" in output
    assert "stale facts: 1" in output
    assert "  discovery: 4" in output
    assert "  imported: 1" in output
    assert "  user: 3" in output
    assert "host-up (aliases: 1 total; facts: 6)" in output
    assert "10.0.0.10; facts" not in output
    assert "  up: 1" in output
    assert "  down: 1" in output
    assert "  unknown: 1" in output
    assert "host-up /: 40/100 bytes free/total" in output


def test_cli_state_summary_counts_local_observation_without_availability_as_unknown(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-local-observation.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "local_observation_status", "observed")],
    )

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0

    output = capsys.readouterr().out
    assert "entities: 1" in output
    assert "availability:\n  up: 0\n  down: 0\n  unknown: 1" in output


def test_cli_state_summary_counts_host_availability_up(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-up.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "availability_status", "up")],
    )

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0

    output = capsys.readouterr().out
    assert "entities: 1" in output
    assert "availability:\n  up: 1\n  down: 0\n  unknown: 0" in output


def test_cli_state_summary_counts_host_availability_down(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-down.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "availability_status", "down")],
    )

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0

    output = capsys.readouterr().out
    assert "entities: 1" in output
    assert "availability:\n  up: 0\n  down: 1\n  unknown: 0" in output


def test_cli_state_summary_keeps_endpoint_availability_separate_from_host(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-endpoint-availability.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "alias", "192.168.254.115"),
            ("node115", "local_observation_status", "observed"),
            ("192.168.254.115:9100", "availability_status", "up"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0

    output = capsys.readouterr().out
    assert "entities: 2" in output
    assert "availability:\n  up: 1\n  down: 0\n  unknown: 1" in output


def test_cli_state_summary_top_entities_summarizes_alias_count(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-many-aliases.sqlite"
    aliases = [f"172.17.0.{index}" for index in range(1, 6)]
    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "alias", alias) for alias in aliases],
    )

    assert seed_local.main(["--db", str(db_path), "--state-summary"]) == 0

    output = capsys.readouterr().out
    assert "node115 (aliases: 5 total; facts: 5)" in output
    for alias in aliases:
        assert alias not in output


def test_cli_current_facts_and_fact_support_keep_raw_alias_evidence(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-raw-alias-evidence.sqlite"
    aliases = ["192.168.254.115", "192.168.254.116"]
    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "alias", alias) for alias in aliases],
    )

    assert (
        seed_local.main(["--db", str(db_path), "--current-facts", "node115", "alias"])
        == 0
    )
    assert capsys.readouterr().out.splitlines() == aliases

    assert (
        seed_local.main(["--db", str(db_path), "--fact-support", "node115", "alias"])
        == 0
    )
    support_output = capsys.readouterr().out
    assert "value: 192.168.254.115" in support_output
    assert "value: 192.168.254.116" in support_output


def test_cli_fact_support_prints_projected_grouped_values(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "systemd",
                "--fact-support",
                "jellyfin",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: docker" in output
    assert "value: systemd" in output
    assert "aggregate_confidence: 0.9775" in output
    assert "aggregate_confidence: 0.85" in output
    assert "supporting_fact_ids: fact_obs_" in output
    assert "source_types: user" in output
    assert "first_observed:" in output
    assert "latest_observed:" in output


def test_cli_measurement_fact_support_hides_old_samples_by_default(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "node115",
                "up",
                "0",
                "--fact",
                "node115",
                "up",
                "1",
                "--fact-support",
                "node115",
                "up",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: 1" in output
    assert "value: 0" not in output
    assert "support_kind: current_sample" in output
    assert "historical samples hidden" not in output


def test_cli_measurement_fact_support_include_history_shows_all_samples(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "node115",
                "up",
                "0",
                "--fact",
                "node115",
                "up",
                "1",
                "--fact",
                "node115",
                "up",
                "1",
                "--fact-support",
                "node115",
                "up",
                "--include-history",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: 0" in output
    assert output.count("value: 1") == 2
    assert output.count("support_kind: current_sample") == 3
    assert "historical samples hidden" not in output


def test_cli_availability_status_history_visibility_does_not_change_current(capsys):
    seed_local = load_seed_local_module()
    facts = [
        "--fact",
        "node115",
        "availability_status",
        "up",
        "--fact",
        "node115",
        "availability_status",
        "down",
    ]

    assert (
        seed_local.main([*facts, "--fact-support", "node115", "availability_status"])
        == 0
    )
    default_output = capsys.readouterr().out
    assert "value: down" in default_output
    assert "value: up" not in default_output

    assert (
        seed_local.main(
            [
                *facts,
                "--fact-support",
                "node115",
                "availability_status",
                "--include-history",
            ]
        )
        == 0
    )
    history_output = capsys.readouterr().out
    assert "value: up" in history_output
    assert "value: down" in history_output

    assert (
        seed_local.main([*facts, "--best-fact", "node115", "availability_status"]) == 0
    )
    best_output = capsys.readouterr().out
    assert "value: down" in best_output
    assert "value: up" not in best_output


def test_cli_durable_runtime_fact_support_still_shows_all_conflicting_values(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "systemd",
                "--fact-support",
                "jellyfin",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: docker" in output
    assert "value: systemd" in output
    assert output.count("support_kind: aggregate") == 2
    assert "historical samples hidden" not in output


def test_cli_best_fact_prints_projected_current_belief(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "systemd",
                "--best-fact",
                "jellyfin",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: jellyfin" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "confidence: 0.9775" in output
    assert "reason: best-supported current belief" in output
    assert "support_count: 2" in output


def test_cli_fact_conflicts_prints_projected_active_conflicts_and_winner(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact",
                "jellyfin",
                "runtime",
                "systemd",
                "--fact-conflicts",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: jellyfin" in output
    assert "predicate: runtime" in output
    assert "values: docker, systemd" in output
    assert "winning_value: docker" in output
    assert "winning_fact_id: fact_obs_" in output
    assert "conflicting_fact_ids: fact_obs_" in output
    assert "reason: multiple values for jellyfin/runtime" in output


def test_parser_supports_fact_expiry_options():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()

    expires_args = parser.parse_args(
        [
            "--fact",
            "jellyfin",
            "runtime",
            "docker",
            "--fact-expires-at",
            "2026-01-01T00:00:00+00:00",
        ]
    )
    ttl_args = parser.parse_args(
        [
            "--fact",
            "jellyfin",
            "runtime",
            "docker",
            "--fact-ttl-seconds",
            "60",
        ]
    )

    assert expires_args.fact_expires_at == "2026-01-01T00:00:00+00:00"
    assert ttl_args.fact_ttl_seconds == 60


def test_cli_fact_ttl_can_expire_seeded_fact(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--best-fact",
                "jellyfin",
                "runtime",
            ]
        )
        == 0
    )

    assert capsys.readouterr().out.strip() == "no current belief for jellyfin runtime"


def test_cli_fact_expires_at_keeps_unexpired_seeded_fact(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact-expires-at",
                "2999-01-01T00:00:00+00:00",
                "--best-fact",
                "jellyfin",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: jellyfin" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output


def test_cli_expired_fact_hidden_by_default(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--fact-support",
                "jellyfin",
                "runtime",
            ]
        )
        == 0
    )

    assert capsys.readouterr().out.strip() == "no fact support for jellyfin runtime"


def test_cli_expired_fact_visible_with_include_expired(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--fact-support",
                "jellyfin",
                "runtime",
                "--include-expired",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: docker" in output
    assert "expired: true" in output
    assert "expires_at:" in output


def test_cli_stale_facts_prints_expired_facts(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--stale-facts",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: jellyfin" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "source_type: user" in output
    assert "confidence: 1.0" in output
    assert "expired: true" in output
    assert "expires_at:" in output


def test_cli_stale_fact_refreshes_recommend_service_inspection_for_runtime(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--stale-fact-refreshes",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: jellyfin" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "recommended_capability: service_inspection" in output
    assert "reason: predicate 'runtime' maps to 'service_inspection'" in output


def test_cli_stale_fact_refreshes_recommend_environment_inventory_for_host(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "host",
                "node115",
                "--fact-ttl-seconds",
                "0",
                "--stale-fact-refreshes",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: jellyfin" in output
    assert "predicate: host" in output
    assert "value: node115" in output
    assert "recommended_capability: environment_inventory" in output
    assert "reason: predicate 'host' maps to 'environment_inventory'" in output


def test_cli_stale_fact_refreshes_fall_back_to_knowledge_lookup(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "jellyfin",
                "unknown_predicate",
                "mystery",
                "--fact-ttl-seconds",
                "0",
                "--stale-fact-refreshes",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "predicate: unknown_predicate" in output
    assert "value: mystery" in output
    assert "recommended_capability: knowledge_lookup" in output
    assert "reason: predicate 'unknown_predicate' maps to 'knowledge_lookup'" in output


def test_parser_accepts_json_observation_diff_option():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--diff-observations-json", "inventory.json"]
    )

    assert args.diff_observations_json == "inventory.json"


def test_cli_diff_observations_json_does_not_ingest_inventory(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.db"
    json_path = tmp_path / "observations.json"
    json_path.write_text(
        '{"observations":[{"subject":"jellyfin","predicate":"runtime",'
        '"value":"docker"}]}',
        encoding="utf-8",
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--diff-observations-json",
                str(json_path),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "new_facts: 1" in output
    assert "matching_facts: 0" in output
    assert (
        seed_local.main(["--db", str(db_path), "--fact-support", "jellyfin", "runtime"])
        == 0
    )
    support_output = capsys.readouterr().out
    assert "no fact support for jellyfin runtime" in support_output


def test_cli_observe_local_host_prints_count_and_summary(monkeypatch, capsys):
    seed_local = load_seed_local_module()

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            return [
                seed_local.Observation(
                    id="obs_cli_local",
                    source_type="discovery",
                    observed_at=seed_local.utc_now(),
                    subject="node-a",
                    predicate="os",
                    value="linux",
                )
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--observe-local-host"]) == 0

    output = capsys.readouterr().out
    assert "ingested 1 observation(s)" in output
    assert "subject: node-a" in output
    assert "predicate: os" in output
    assert "source_type: discovery" in output


def test_cli_local_network_facts_appear_in_current_facts_and_impact(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            observed_at = seed_local.utc_now()
            return [
                seed_local.Observation(
                    id="obs_network_interface",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="network_interface",
                    value="eth0",
                    dimensions={"interface": "eth0"},
                ),
                seed_local.Observation(
                    id="obs_network_role",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="interface_role",
                    value="primary",
                    dimensions={"interface": "eth0"},
                ),
                seed_local.Observation(
                    id="obs_network_ip",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="ip_address",
                    value="192.168.2.5",
                    dimensions={"interface": "eth0", "address_family": "ipv4"},
                ),
                seed_local.Observation(
                    id="obs_docker_interface",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="network_interface",
                    value="docker0",
                    dimensions={"interface": "docker0"},
                ),
                seed_local.Observation(
                    id="obs_docker_role",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="interface_role",
                    value="container",
                    dimensions={"interface": "docker0"},
                ),
                seed_local.Observation(
                    id="obs_docker_ip",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="ip_address",
                    value="172.17.0.1",
                    dimensions={"interface": "docker0", "address_family": "ipv4"},
                ),
                seed_local.Observation(
                    id="obs_network_ipv6_global",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="ip_address",
                    value="2001:db8::5",
                    dimensions={"interface": "eth0", "address_family": "ipv6"},
                ),
                seed_local.Observation(
                    id="obs_network_ipv6_link_local",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="ip_address",
                    value="fe80::5",
                    dimensions={"interface": "eth0", "address_family": "ipv6"},
                ),
                seed_local.Observation(
                    id="obs_network_gateway",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="default_gateway",
                    value="192.168.2.1",
                    dimensions={"interface": "eth0", "address_family": "ipv4"},
                ),
                seed_local.Observation(
                    id="obs_network_dns",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="dns_resolver",
                    value="1.1.1.1",
                    dimensions={"source": "/etc/resolv.conf"},
                ),
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--db", str(db_path), "--observe-local-host"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--current-facts"]) == 0
    current_output = capsys.readouterr().out
    assert "* node115 network_interface eth0" in current_output
    assert "* node115 ip_address 192.168.2.5" in current_output
    assert "* node115 ip_address 2001:db8::5" in current_output
    assert "* node115 ip_address fe80::5" in current_output
    assert "* node115 network_interface docker0" in current_output
    assert "* node115 ip_address 172.17.0.1" in current_output
    assert "* node115 default_gateway 192.168.2.1" in current_output
    assert "* node115 dns_resolver 1.1.1.1" in current_output

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0
    impact_output = capsys.readouterr().out
    assert "availability_status: unknown" in impact_output
    assert "local network configuration:" in impact_output
    assert "aliases:\n- none" in impact_output
    assert "- primary/default-route interface eth0:" in impact_output
    assert "  ipv4: 192.168.2.5" in impact_output
    assert "  ipv6_global: 2001:db8::5" in impact_output
    assert "  ipv6_link_local: fe80::5" in impact_output
    assert "  default_gateway_ipv4: 192.168.2.1" in impact_output
    assert "default_gateway=2001:db8::5" not in impact_output
    assert (
        "- virtual/container/vpn interfaces: 1 collapsed (container=1)" in impact_output
    )
    assert "docker0: 172.17.0.1" not in impact_output
    assert (
        "- reachability/availability: not inferred from local network facts"
        in impact_output
    )
    assert "- dns_resolver (source=/etc/resolv.conf): 1.1.1.1" in impact_output


def test_cli_mount_facts_appear_in_current_facts_and_impact(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "mounts.sqlite"

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            observed_at = seed_local.utc_now()
            return [
                seed_local.Observation(
                    id="obs_mount_point",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="mount_point",
                    value="/",
                    dimensions={"mount_point": "/"},
                ),
                seed_local.Observation(
                    id="obs_filesystem_type",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="filesystem_type",
                    value="ext4",
                    dimensions={"mount_point": "/"},
                ),
                seed_local.Observation(
                    id="obs_mounted_device",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="mounted_device",
                    value="/dev/sda1",
                    dimensions={"mount_point": "/"},
                ),
                seed_local.Observation(
                    id="obs_mount_option_rw",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="mount_option",
                    value="rw",
                    dimensions={"mount_point": "/", "mount_option": "rw"},
                ),
                seed_local.Observation(
                    id="obs_mount_option_relatime",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="node115",
                    predicate="mount_option",
                    value="relatime",
                    dimensions={"mount_point": "/", "mount_option": "relatime"},
                ),
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--db", str(db_path), "--observe-local-host"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--current-facts"]) == 0
    current_output = capsys.readouterr().out
    assert "* node115 mount_point /" in current_output
    assert "* node115 filesystem_type ext4" in current_output
    assert "* node115 mounted_device /dev/sda1" in current_output
    assert "* node115 mount_option rw" in current_output

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0
    impact_output = capsys.readouterr().out
    assert "mounts:" in impact_output
    assert "- /: device=/dev/sda1 type=ext4" in impact_output
    assert "  options: relatime, rw" in impact_output
    assert (
        "- health/availability/reachability: not inferred from mount facts"
        in impact_output
    )
    assert "availability_status: unknown" in impact_output
    assert "reachability_status" not in impact_output


def test_format_mount_impact_renders_runtime_mount_groups():
    seed_local = load_seed_local_module()
    observed_at = seed_local.utc_now()

    def mount_facts(index, mount_point, device, fs_type, options=("rw",)):
        return [
            seed_local.Fact(
                id=f"fact_mount_point_{index}",
                subject_id="node115",
                predicate="mount_point",
                value=mount_point,
                dimensions={"mount_point": mount_point},
                source_type="discovery",
                observed_at=observed_at,
            ),
            seed_local.Fact(
                id=f"fact_mount_device_{index}",
                subject_id="node115",
                predicate="mounted_device",
                value=device,
                dimensions={"mount_point": mount_point},
                source_type="discovery",
                observed_at=observed_at,
            ),
            seed_local.Fact(
                id=f"fact_mount_type_{index}",
                subject_id="node115",
                predicate="filesystem_type",
                value=fs_type,
                dimensions={"mount_point": mount_point},
                source_type="discovery",
                observed_at=observed_at,
            ),
            *(
                seed_local.Fact(
                    id=f"fact_mount_option_{index}_{option}",
                    subject_id="node115",
                    predicate="mount_option",
                    value=option,
                    dimensions={"mount_point": mount_point, "mount_option": option},
                    source_type="discovery",
                    observed_at=observed_at,
                )
                for option in options
            ),
        ]

    facts = []
    for index, mount in enumerate(
        [
            ("/var/lib/docker/overlay2/a/merged", "overlay", "overlay"),
            ("/var/lib/docker/overlay2/b/merged", "overlay", "overlay"),
            ("/run/docker/netns/abc", "nsfs", "nsfs"),
            ("/proc", "proc", "proc"),
            ("/run/credentials/systemd-sysusers.service", "ramfs", "ramfs"),
            ("/", "/dev/mapper/root", "ext4"),
            ("/mnt/merged", "mergerfs", "fuse.mergerfs"),
        ]
    ):
        facts.extend(mount_facts(index, *mount))

    output = "\n".join(seed_local._format_mount_impact(facts))

    assert output.index("- /: device=/dev/mapper/root type=ext4") < output.index(
        "- /mnt/merged: device=mergerfs type=fuse.mergerfs"
    )
    assert "- docker overlay mounts: 2 collapsed" in output
    assert "- docker netns mounts: 1 collapsed" in output
    assert "- system/pseudo mounts: 1 collapsed" in output
    assert "- systemd credential mounts: 1 collapsed" in output
    assert "- full mount evidence: use --current-facts" in output
    assert "- health/availability/reachability: not inferred from mount facts" in output
    assert "/var/lib/docker/overlay2/a/merged" not in output
    assert "/run/docker/netns/abc" not in output
    assert "- /proc:" not in output


def test_cli_events_without_message_lists_persisted_events_and_exits(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert (
        seed_local.main(
            ["--db", str(db_path), "--observe", "node115", "architecture", "x86_64"]
        )
        == 0
    )
    capsys.readouterr()

    def fail_shell(*args, **kwargs):
        pytest.fail(
            "--events without a message should list events instead of shell mode"
        )

    monkeypatch.setattr(seed_local, "run_shell", fail_shell)

    assert seed_local.main(["--db", str(db_path), "--events"]) == 0

    output = capsys.readouterr().out
    assert "Events: 3" in output
    assert "kind=observation.observed" in output
    assert "kind=evidence.observed" in output
    assert "evidence_id=evd_obs_" in output
    assert "kind=fact.observed" in output
    assert output.count("subject=node115 predicate=architecture") == 2


def test_sqlite_observation_reopen_projects_best_fact_and_fact_support(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            return [
                seed_local.Observation(
                    id="obs_cli_local_architecture",
                    source_type="discovery",
                    observed_at=seed_local.utc_now(),
                    subject="node115",
                    predicate="architecture",
                    value="x86_64",
                )
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--db", str(db_path), "--observe-local-host"]) == 0
    ingest_output = capsys.readouterr().out
    assert "subject: node115" in ingest_output
    assert "predicate: architecture" in ingest_output
    assert "value: x86_64" in ingest_output

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        events = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
        assert [event.kind for event in events] == [
            "observation.observed",
            "evidence.observed",
            "fact.observed",
        ]
        persisted_fact_payload = events[-1].payload["fact"]
        assert persisted_fact_payload["subject_id"] == "node115"
        assert persisted_fact_payload["predicate"] == "architecture"
        assert persisted_fact_payload["value"] == "x86_64"

        state = seed_local.StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
        projected_best = state.get_best_fact("node115", "architecture")
        assert projected_best is not None
        assert projected_best.value == "x86_64"
        projected_support = state.get_fact_support("node115", "architecture")
        assert projected_support is not None
        assert projected_support.value == "x86_64"
        assert projected_support.supporting_fact_ids == [projected_best.id]
    finally:
        ledger.close()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", "node115", "architecture"]
        )
        == 0
    )
    best_output = capsys.readouterr().out
    assert "subject: node115" in best_output
    assert "predicate: architecture" in best_output
    assert "value: x86_64" in best_output
    assert "no current belief" not in best_output

    assert (
        seed_local.main(
            ["--db", str(db_path), "--fact-support", "node115", "architecture"]
        )
        == 0
    )
    support_output = capsys.readouterr().out
    assert "value: x86_64" in support_output
    assert "supporting_fact_ids: fact_obs_" in support_output
    assert "source_types: discovery" in support_output


def test_best_fact_accepts_short_hostname_for_persisted_fqdn_observation(tmp_path):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        seed_local.ingest_observations(
            ledger,
            seed_local.DEFAULT_WORKSPACE,
            [
                seed_local.DevObservationSeed(
                    "node115.example.test",
                    "architecture",
                    "x86_64",
                    source_type="discovery",
                )
            ],
        )
    finally:
        ledger.close()

    reopened = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(reopened).project(
            seed_local.DEFAULT_WORKSPACE
        )
        assert state.get_best_fact("node115", "architecture").value == "x86_64"
        assert state.get_fact_support("node115", "architecture").value == "x86_64"
    finally:
        reopened.close()


def _patch_fake_prometheus_source(monkeypatch, seed_local):
    class FakePrometheusSource:
        source_type = "provider"

        def __init__(self, base_url, *, timeout_seconds):
            self.name = f"fake-prometheus:{base_url}"
            self.base_url = base_url
            self.timeout_seconds = timeout_seconds

        def collect(self):
            observed_at = seed_local.utc_now()
            return [
                seed_local.Observation(
                    id="obs_cli_prometheus_up_a",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-a:9100",
                    predicate="up",
                    value=1,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {"instance": "node-a:9100"},
                    },
                ),
                seed_local.Observation(
                    id="obs_cli_prometheus_avail_a_root",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-a:9100",
                    predicate="filesystem_avail_bytes",
                    value=100,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {
                            "instance": "node-a:9100",
                            "mountpoint": "/",
                        },
                    },
                ),
                seed_local.Observation(
                    id="obs_cli_prometheus_size_a_data",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-a:9100",
                    predicate="filesystem_size_bytes",
                    value=200,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {
                            "instance": "node-a:9100",
                            "mountpoint": "/data",
                        },
                    },
                ),
                seed_local.Observation(
                    id="obs_cli_prometheus_up_b",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-b:9100",
                    predicate="up",
                    value=0,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {"instance": "node-b:9100"},
                    },
                ),
            ]

    monkeypatch.setattr(seed_local, "PrometheusObservationSource", FakePrometheusSource)


def test_cli_observe_prometheus_prints_summary_by_default(monkeypatch, capsys):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)

    assert (
        seed_local.main(
            [
                "--observe-prometheus",
                "http://prom.example:9090",
                "--observe-timeout",
                "3",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 8 observation(s)" in output
    assert "hosts/instances discovered: node-a:9100, node-b:9100" in output
    assert "counts by predicate:" in output
    assert "- availability_status: 2" in output
    assert "- filesystem_avail_bytes: 1" in output
    assert "- filesystem_free_bytes: 1" in output
    assert "- filesystem_size_bytes: 1" in output
    assert "- filesystem_total_bytes: 1" in output
    assert "- up: 2" in output
    assert "fact_id:" not in output


def test_cli_observe_prometheus_verbose_prints_every_fact(monkeypatch, capsys):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)

    assert (
        seed_local.main(
            [
                "--observe-prometheus",
                "http://prom.example:9090",
                "--verbose-observations",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 8 observation(s)" in output
    assert "fact_id: fact_obs_" in output
    assert "subject: node-a:9100" in output
    assert "subject: node-b:9100" in output
    assert "predicate: availability_status" in output
    assert "predicate: filesystem_avail_bytes" in output
    assert "predicate: filesystem_free_bytes" in output
    assert "predicate: filesystem_total_bytes" in output
    assert "hosts/instances discovered:" not in output


@pytest.mark.parametrize(
    ("instance", "expected"), [("node-a:9100", "up"), ("node-b:9100", "down")]
)
def test_cli_observe_prometheus_supports_canonical_availability_best_fact(
    monkeypatch, tmp_path, capsys, instance, expected
):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-prometheus",
                "http://prom.example:9090",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", instance, "availability_status"]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert f"subject: {instance}" in output
    assert "predicate: availability_status" in output
    assert f"value: {expected}" in output


def test_cli_observe_prometheus_instance_filter_limits_ingestion(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-prometheus",
                "http://prom.example:9090",
                "--prometheus-instance",
                "node-b:9100",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 2 observation(s)" in output
    assert "hosts/instances discovered: node-b:9100" in output
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()
    assert {fact.subject_id for fact in state.facts.values()} == {"node-b:9100"}
    assert {(fact.predicate, fact.value) for fact in state.facts.values()} == {
        ("up", 0),
        ("availability_status", "down"),
        ("health_status", "degraded"),
    }


def test_cli_observe_prometheus_mountpoint_filter_limits_ingestion(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-prometheus",
                "http://prom.example:9090",
                "--prometheus-mountpoint",
                "/data",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 2 observation(s)" in output
    assert "hosts/instances discovered: node-a:9100" in output
    assert "- filesystem_size_bytes: 1" in output
    assert "- filesystem_total_bytes: 1" in output
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()
    facts = list(state.facts.values())
    assert len(facts) == 2
    assert {fact.subject_id for fact in facts} == {"node-a:9100"}
    assert {fact.predicate for fact in facts} == {
        "filesystem_size_bytes",
        "filesystem_total_bytes",
    }


def test_cli_alias_resolves_best_fact_after_sqlite_reopen(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "192.168.254.115:9100",
                "up",
                "1",
                "--alias",
                "node115",
                "192.168.254.115:9100",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--best-fact", "node115", "up"]) == 0
    output = capsys.readouterr().out
    assert "subject: 192.168.254.115:9100" in output
    assert "predicate: up" in output
    assert "value: 1" in output

    reopened = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(reopened).project(
            seed_local.DEFAULT_WORKSPACE
        )
        support = state.get_fact_support("node115", "up")
        best = state.get_best_fact("node115", "up")
    finally:
        reopened.close()

    assert best is not None
    assert best.subject_id == "192.168.254.115:9100"
    assert support is not None
    assert support.supporting_fact_ids == [best.id]


def test_cli_alias_does_not_flatten_endpoint_availability_best_fact(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "192.168.254.115:9100",
                "availability_status",
                "down",
                "--alias",
                "node115",
                "192.168.254.115:9100",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", "node115", "availability_status"]
        )
        == 0
    )
    assert capsys.readouterr().out == (
        "no current belief for node115 availability_status\n"
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--best-fact",
                "192.168.254.115:9100",
                "availability_status",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "subject: 192.168.254.115:9100" in output
    assert "predicate: availability_status" in output
    assert "value: down" in output


def test_cli_alias_records_alias_observation_fact(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--alias", "node115", "192.168.254.115:9100"]) == 0

    output = capsys.readouterr().out
    assert "subject: node115" in output
    assert "predicate: alias" in output
    assert "value: 192.168.254.115:9100" in output


def _group_member_fact(seed_local, fact_id, value, dimensions):
    return seed_local.Fact(
        id=fact_id,
        subject_id="node115",
        predicate="group_member",
        value=value,
        dimensions=dimensions,
        source_type="discovery",
        observed_at=seed_local.utc_now(),
    )


def test_cli_current_facts_render_dimensions_for_group_member_facts():
    seed_local = load_seed_local_module()
    state = seed_local.State(workspace_id="ws")
    state.facts = {
        "fact_sudo": _group_member_fact(
            seed_local,
            "fact_sudo",
            "user",
            {"username": "user", "groupname": "sudo", "gid": "27"},
        ),
        "fact_docker": _group_member_fact(
            seed_local,
            "fact_docker",
            "user",
            {"username": "user", "gid": "999", "groupname": "docker"},
        ),
    }

    output = seed_local.format_current_facts(state, "node115", "group_member")

    assert output.splitlines() == [
        "user (gid=27, groupname=sudo, username=user)",
        "user (gid=999, groupname=docker, username=user)",
    ]


def test_cli_current_facts_dimensionless_output_is_unchanged():
    seed_local = load_seed_local_module()
    state = seed_local.State(workspace_id="ws")
    observed_at = seed_local.utc_now()
    state.facts = {
        "fact_alias_1": seed_local.Fact(
            id="fact_alias_1",
            subject_id="node115",
            predicate="alias",
            value="node115.local",
            source_type="imported",
            observed_at=observed_at,
        ),
        "fact_alias_2": seed_local.Fact(
            id="fact_alias_2",
            subject_id="node115",
            predicate="alias",
            value="192.168.1.115",
            source_type="imported",
            observed_at=observed_at,
        ),
    }

    assert seed_local.format_current_facts(state, "node115", "alias") == (
        "192.168.1.115\nnode115.local"
    )


def test_cli_fact_support_renders_dimensions_for_group_member_facts():
    seed_local = load_seed_local_module()
    observed_at = seed_local.utc_now()
    supports = [
        seed_local.FactSupport(
            subject="node115",
            predicate="group_member",
            value="user",
            dimensions={"username": "user", "groupname": "sudo", "gid": "27"},
            supporting_fact_ids=["fact_sudo"],
            source_types=["discovery"],
            confidence=0.95,
            observed_at=observed_at,
            latest_observed_at=observed_at,
        ),
        seed_local.FactSupport(
            subject="node115",
            predicate="group_member",
            value="user",
            dimensions={"username": "user", "gid": "999", "groupname": "docker"},
            supporting_fact_ids=["fact_docker"],
            source_types=["discovery"],
            confidence=0.95,
            observed_at=observed_at,
            latest_observed_at=observed_at,
        ),
    ]

    output = seed_local.format_fact_supports(supports, "node115", "group_member")

    assert "value: user\ndimensions: gid=27, groupname=sudo, username=user" in output
    assert "value: user\ndimensions: gid=999, groupname=docker, username=user" in output


def test_cli_fact_support_dimensionless_output_has_no_dimensions_line():
    seed_local = load_seed_local_module()
    observed_at = seed_local.utc_now()
    supports = [
        seed_local.FactSupport(
            subject="node",
            predicate="up",
            value=1,
            supporting_fact_ids=["fact_up_new"],
            source_types=["provider"],
            confidence=0.85,
            observed_at=observed_at,
            latest_observed_at=observed_at,
            predicate_semantics="measurement",
            support_kind="current_sample",
        )
    ]

    output = seed_local.format_fact_supports(supports, "node", "up")

    assert "value: 1\nsemantics: measurement" in output
    assert "dimensions:" not in output


def test_cli_fact_support_marks_measurement_current_sample():
    seed_local = load_seed_local_module()
    supports = [
        seed_local.FactSupport(
            subject="node",
            predicate="up",
            value=1,
            supporting_fact_ids=["fact_up_new"],
            source_types=["provider"],
            confidence=0.85,
            observed_at=seed_local.datetime(2026, 1, 1),
            latest_observed_at=seed_local.datetime(2026, 1, 1),
            predicate_semantics="measurement",
            support_kind="current_sample",
        )
    ]

    output = seed_local.format_fact_supports(supports, "node", "up")

    assert "semantics: measurement" in output
    assert "support_kind: current_sample" in output


def test_cli_observe_ansible_inventory_ingests_identity_observations(tmp_path, capsys):
    seed_local = load_seed_local_module()
    inventory_path = tmp_path / "inventory.ini"
    inventory_path.write_text(
        "[nodegroup]\nnode115 ansible_host=192.168.254.115\n", encoding="utf-8"
    )

    assert seed_local.main(["--observe-ansible-inventory", str(inventory_path)]) == 0

    output = capsys.readouterr().out
    assert "subject: node115" in output
    assert "predicate: hostname" in output
    assert "predicate: ip_address" in output
    assert "predicate: alias" in output
    assert "predicate: group" in output


def test_cli_ansible_inventory_and_prometheus_support_best_fact(
    tmp_path, monkeypatch, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    inventory_path = tmp_path / "inventory.yaml"
    inventory_path.write_text(
        """all:
  hosts:
    node115:
      ansible_host: 192.168.254.115
""",
        encoding="utf-8",
    )

    class FakePrometheusSource:
        source_type = "provider"
        name = "prometheus"

        def __init__(self, base_url, timeout_seconds=5.0):
            self.base_url = base_url
            self.timeout_seconds = timeout_seconds

        def collect(self):
            from datetime import datetime, timezone
            from seed_runtime.observations import Observation

            return [
                Observation(
                    id="obs_cli_ansible_prometheus",
                    source_type="provider",
                    observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    subject="192.168.254.115:9100",
                    predicate="up",
                    value=0,
                    confidence=0.95,
                    metadata={"source_name": "prometheus"},
                )
            ]

    monkeypatch.setattr(seed_local, "PrometheusObservationSource", FakePrometheusSource)

    assert (
        seed_local.main(
            ["--db", str(db_path), "--observe-ansible-inventory", str(inventory_path)]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--observe-prometheus", "http://prom.example:9090"]
        )
        == 0
    )
    capsys.readouterr()

    reopened = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(reopened).project(
            seed_local.DEFAULT_WORKSPACE
        )
    finally:
        reopened.close()
    assert any(
        fact.subject_id == "node115"
        and fact.predicate == "alias"
        and fact.value == "192.168.254.115:9100"
        for fact in state.facts.values()
    )

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", "node115", "availability_status"]
        )
        == 0
    )
    assert capsys.readouterr().out == (
        "no current belief for node115 availability_status\n"
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--best-fact",
                "192.168.254.115:9100",
                "availability_status",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "subject: 192.168.254.115:9100" in output
    assert "predicate: availability_status" in output
    assert "value: down" in output


def test_cli_entity_type_projection_queries():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()

    assert parser.parse_args(["--entity-types"]).entity_types is True
    assert parser.parse_args(["--entity-type", "node115"]).entity_type == "node115"
    state = seed_local.State(workspace_id="ws")
    assert seed_local.format_entity_types(state, "node115") == "node115: unknown"


def _persist_impact_facts(seed_local, db_path, facts):
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        for index, (subject, predicate, value) in enumerate(facts):
            fact = seed_local.Fact(
                id=f"fact_impact_{index}",
                subject_id=subject,
                predicate=predicate,
                value=value,
                source_type="imported",
                confidence=0.9,
                evidence_ids=[],
                observed_at=seed_local.utc_now(),
            )
            ledger.append(
                "fact.observed",
                seed_local.DEFAULT_WORKSPACE,
                {"fact": seed_local.to_plain(fact)},
            )
    finally:
        ledger.close()


def test_cli_impact_reports_local_observation_without_availability(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-local-observation.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "local_observation_status", "observed"),
            ("node115", "os", "linux"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0

    output = capsys.readouterr().out
    assert "local_observation_status: observed" in output
    assert "availability_status: unknown" in output
    assert "endpoint availability by role:\n- none" in output


def test_cli_impact_resolves_host_alias_and_reports_availability(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-alias.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "os", "linux"),
            ("node115", "alias", "192.168.254.115:9100"),
            ("192.168.254.115:9100", "availability_status", "up"),
            ("node115", "group", "servers"),
        ],
    )

    assert (
        seed_local.main(["--db", str(db_path), "--impact", "192.168.254.115:9100"]) == 0
    )

    output = capsys.readouterr().out
    assert "entity: node115" in output
    assert "entity types: host" in output
    assert "aliases:\n- 192.168.254.115:9100" in output
    assert "availability_status: unknown" in output
    assert "endpoint availability by role:\n- 192.168.254.115:9100: up" in output
    assert "groups/member_of: servers" in output


def test_cli_impact_reports_service_running_on_host_as_dependent(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-dependent.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "os", "linux"), ("jellyfin", "runs_on", "node115")],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0

    assert "dependents: jellyfin" in capsys.readouterr().out


def test_cli_impact_includes_active_conflicts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-conflict.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("jellyfin", "runtime", "docker"), ("jellyfin", "runtime", "systemd")],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "jellyfin"]) == 0

    output = capsys.readouterr().out
    assert "active conflicts:" in output
    assert "- runtime: values=docker, systemd; winning=none" in output


def test_cli_current_facts_and_impact_keep_all_aliases_without_conflict(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "multi-alias.sqlite"
    aliases = [
        "192.168.254.115",
        "192.168.254.115:9100",
        "192.168.254.115:9200",
    ]
    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "alias", alias) for alias in aliases],
    )

    assert (
        seed_local.main(["--db", str(db_path), "--current-facts", "node115", "alias"])
        == 0
    )
    assert capsys.readouterr().out.splitlines() == aliases

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0
    output = capsys.readouterr().out
    assert "aliases:\n" + "\n".join(f"- {alias}" for alias in aliases) in output
    assert "- alias:" not in output


def test_cli_impact_formats_systemd_resolved_stub_and_upstream(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-dns.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "os", "linux"),
            ("node115", "dns_resolver", "127.0.0.53"),
            ("node115", "dns_resolver_stub", "127.0.0.53"),
            ("node115", "dns_resolver_upstream", "1.1.1.1"),
            ("node115", "dns_resolver_upstream", "2001:4860:4860::8888"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0

    output = capsys.readouterr().out
    assert "- dns_resolver_stub: 127.0.0.53" in output
    assert "- dns_resolver_upstream:\n  - 1.1.1.1\n  - 2001:4860:4860::8888" in output
    assert "dns works" not in output


def test_cli_impact_formats_unknown_upstream_when_only_stub_known(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-dns-stub-only.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "os", "linux"),
            ("node115", "dns_resolver", "127.0.0.53"),
            ("node115", "dns_resolver_stub", "127.0.0.53"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0

    output = capsys.readouterr().out
    assert "- dns_resolver_stub: 127.0.0.53" in output
    assert "- dns_resolver_upstream: unknown" in output
    assert "availability_status: unknown" in output
    assert (
        "- reachability/availability: not inferred from local network facts" in output
    )


def test_cli_impact_omits_ip_address_aliases_unless_explicit_alias(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-ip-alias-cleanup.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "os", "linux"),
            ("node115", "ip_address", "192.168.254.115"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0

    output = capsys.readouterr().out
    aliases_section = output.split("availability_status:", 1)[0]
    assert "aliases:\n- none" in aliases_section
    assert "- 192.168.254.115" not in aliases_section

    _persist_impact_facts(
        seed_local,
        db_path,
        [("node115", "alias", "192.168.254.115")],
    )
    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0
    output = capsys.readouterr().out
    assert "aliases:\n- 192.168.254.115" in output


def test_cli_impact_includes_graph_warnings(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-warning.sqlite"
    _persist_impact_facts(seed_local, db_path, [("mystery", "group", "servers")])

    assert seed_local.main(["--db", str(db_path), "--impact", "mystery"]) == 0

    output = capsys.readouterr().out
    assert "graph issues:" in output
    assert "- warning: mystery member_of servers" in output
    assert "subject type is unknown; expected host" in output


def test_cli_impact_collapses_duplicate_monitored_by_warnings(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-duplicate-warning.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "prometheus_instance", "node115:9100"),
            ("node115", "prometheus_instance", "node115:8080"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0

    output = capsys.readouterr().out
    warning = "- warning: node115 monitored_by prometheus"
    assert output.count(warning) == 1


def test_cli_impact_does_not_ingest_or_execute(tmp_path, capsys, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-read-only.sqlite"
    monkeypatch.setattr(
        seed_local,
        "build_local_app",
        lambda **_kwargs: (_ for _ in ()).throw(AssertionError("runtime was built")),
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "node115",
                "os",
                "linux",
                "--impact",
                "node115",
                "restart",
                "node115",
            ]
        )
        == 0
    )
    assert "entity types: unknown" in capsys.readouterr().out

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        assert ledger.list_events(seed_local.DEFAULT_WORKSPACE) == []
    finally:
        ledger.close()


def test_cli_show_inference_catalog_displays_rules(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--show-inference-catalog"]) == 0

    output = capsys.readouterr().out
    assert "deterministic inference rules:" in output
    assert "docker_runtime_managed_by" in output
    assert "runtime=docker -> managed_by=docker_container_lifecycle" in output
    assert "availability_down_health_degraded" in output


def test_cli_inferred_facts_displays_projection_provenance(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            ["--fact", "jellyfin", "runtime", "docker", "--inferred-facts", "jellyfin"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "managed_by: docker_container_lifecycle" in output
    assert "source_fact_id=" in output
    assert "inference_rule_id=docker_runtime_managed_by" in output


def test_cli_why_displays_recursive_endpoint_health_inference(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "node115",
                "alias",
                "192.168.254.115",
                "--fact",
                "192.168.254.115",
                "alias",
                "192.168.254.115:9100",
                "--fact",
                "192.168.254.115:9100",
                "availability_status",
                "down",
                "--why",
                "192.168.254.115:9100",
                "health_status",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Current belief:" in output
    assert "health_status=degraded" in output
    assert "inference_rule: availability_down_health_degraded" in output
    assert "derived_from: availability_status=down" in output


def test_cli_impact_groups_endpoint_availability_by_role(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-endpoint-roles.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "os", "linux"),
            ("node115", "alias", "192.168.254.115:9100"),
            ("node115", "alias", "192.168.254.115:9200"),
            ("192.168.254.115:9100", "endpoint_role", "node-exporter"),
            ("192.168.254.115:9100", "availability_status", "down"),
            ("192.168.254.115:9200", "endpoint_role", "cadvisor"),
            ("192.168.254.115:9200", "availability_status", "up"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0

    output = capsys.readouterr().out
    assert "availability_status: unknown" in output
    assert "endpoint availability by role:" in output
    assert "- node-exporter: down (192.168.254.115:9100)" in output
    assert "- cadvisor: up (192.168.254.115:9200)" in output


def test_cli_unhealthy_groups_current_down_endpoint_under_aliased_host_with_role(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-endpoints.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "os", "linux"),
            ("node115", "alias", "192.168.254.115:9100"),
            ("192.168.254.115:9100", "endpoint_role", "node-exporter"),
            ("192.168.254.115:9100", "availability_status", "down"),
            ("node116:9100", "endpoint_role", "node-exporter"),
            ("node116:9100", "availability_status", "up"),
            ("host-down-is-not-an-endpoint", "os", "linux"),
            ("host-down-is-not-an-endpoint", "availability_status", "down"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--unhealthy"]) == 0

    output = capsys.readouterr().out
    assert (
        "unhealthy endpoints:\nnode115:\n  - node-exporter down 192.168.254.115:9100"
        in output
    )
    assert "node116:9100" not in output
    assert "host-down-is-not-an-endpoint" not in output
    assert "graph errors:" in output
    assert "graph warnings:" not in output


def test_cli_down_alias_uses_current_measurement_sample(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-current-sample.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115:9100", "availability_status", "down"),
            ("node115:9100", "availability_status", "up"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--down"]) == 0

    assert "node115:9100" not in capsys.readouterr().out


def test_cli_unhealthy_shows_errors_and_optionally_warnings(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-graph-issues.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "os", "linux"),
            ("workers", "group", "team"),
            ("workers", "runs_on", "node115"),
            ("mystery", "group", "servers"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--unhealthy"]) == 0
    output = capsys.readouterr().out
    assert "graph errors:" in output
    assert "- error: workers member_of team" in output
    assert "graph warnings:" not in output
    assert "mystery member_of servers" not in output

    assert (
        seed_local.main(["--db", str(db_path), "--unhealthy", "--include-warnings"])
        == 0
    )
    output = capsys.readouterr().out
    assert "graph warnings:" in output
    assert "- warning: mystery member_of servers" in output


def test_cli_graph_issue_output_prints_hint_when_present(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "graph-issue-hint.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("e1f9104e9a8d", "prometheus_instance", "e1f9104e9a8d:9100")],
    )

    assert seed_local.main(["--db", str(db_path), "--graph-issues"]) == 0

    output = capsys.readouterr().out
    assert (
        "hint: Add inventory or alias evidence if this monitored endpoint should map to a known host."
        in output
    )
    assert "source_fact_ids: fact_impact_0" in output


def test_cli_unhealthy_does_not_ingest_or_execute(tmp_path, capsys, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-read-only.sqlite"
    monkeypatch.setattr(
        seed_local,
        "build_local_app",
        lambda **_kwargs: (_ for _ in ()).throw(AssertionError("runtime was built")),
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "node115:9100",
                "availability_status",
                "down",
                "--unhealthy",
                "restart",
                "node115",
            ]
        )
        == 0
    )
    assert "unhealthy endpoints:\n- none" in capsys.readouterr().out

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        assert ledger.list_events(seed_local.DEFAULT_WORKSPACE) == []
    finally:
        ledger.close()


def test_cli_impact_includes_identity_section_without_availability_or_reachability(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-identity.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "hostname", "node115"),
            ("node115", "machine_id", "0123456789abcdef0123456789abcdef"),
            ("node115", "boot_id", "11111111-2222-3333-4444-555555555555"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0
    output = capsys.readouterr().out

    assert "identity:\n" in output
    assert "- hostname: node115" in output
    assert "- machine_id: 0123456789abcdef0123456789abcdef" in output
    assert "- boot_id: 11111111-2222-3333-4444-555555555555" in output
    assert "- availability/reachability: not inferred from identity facts" in output
    assert "availability_status: unknown" in output
    assert "reachability_status" not in output


def test_cli_current_facts_exposes_identity_facts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-identity.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("node115", "hostname", "node115"),
            ("node115", "machine_id", "0123456789abcdef0123456789abcdef"),
            ("node115", "boot_id", "11111111-2222-3333-4444-555555555555"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--current-facts"]) == 0
    output = capsys.readouterr().out

    assert "* node115 hostname node115" in output
    assert "* node115 machine_id 0123456789abcdef0123456789abcdef" in output
    assert "* node115 boot_id 11111111-2222-3333-4444-555555555555" in output


def _persist_storage_impact_facts(seed_local, db_path):
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    facts = [
        ("node115", "block_device", "sda", {"device": "sda"}),
        ("node115", "block_device", "nvme0n1", {"device": "nvme0n1"}),
        ("node115", "partition", "sda1", {"device": "sda1", "parent": "sda"}),
        (
            "node115",
            "partition",
            "nvme0n1p1",
            {"device": "nvme0n1p1", "parent": "nvme0n1"},
        ),
        (
            "node115",
            "block_device_parent",
            "sda",
            {"device": "sda1", "parent": "sda"},
        ),
        (
            "node115",
            "block_device_size_bytes",
            1073741824,
            {"device": "sda1", "parent": "sda"},
        ),
        ("node115", "block_device_rotational", "true", {"device": "sda"}),
        ("node115", "block_device_removable", "false", {"device": "sda"}),
        ("node115", "block_device_model", "Fast Disk", {"device": "sda"}),
        ("node115", "block_device_vendor", "SEED", {"device": "sda"}),
        ("node115", "mount_point", "/", {"mount_point": "/"}),
        ("node115", "mounted_device", "/dev/sda1", {"mount_point": "/"}),
    ]
    try:
        for index, (subject, predicate, value, dimensions) in enumerate(facts):
            fact = seed_local.Fact(
                id=f"fact_storage_impact_{index}",
                subject_id=subject,
                predicate=predicate,
                value=value,
                source_type="discovery",
                confidence=0.9,
                evidence_ids=[],
                observed_at=seed_local.utc_now(),
                dimensions=dimensions,
            )
            ledger.append(
                "fact.observed",
                seed_local.DEFAULT_WORKSPACE,
                {"fact": seed_local.to_plain(fact)},
            )
    finally:
        ledger.close()


def _persist_listener_impact_facts(seed_local, db_path):
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    facts = [
        (
            "node115",
            "listening_endpoint",
            "tcp 0.0.0.0:22",
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "node115",
            "listening_protocol",
            "tcp",
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "node115",
            "listening_address",
            "0.0.0.0",
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "node115",
            "listening_port",
            22,
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "node115",
            "listening_endpoint",
            "udp 127.0.0.1:53",
            {
                "protocol": "udp",
                "address": "127.0.0.1",
                "port": "53",
                "address_family": "ipv4",
            },
        ),
    ]
    try:
        for index, (subject, predicate, value, dimensions) in enumerate(facts):
            fact = seed_local.Fact(
                id=f"fact_listener_impact_{index}",
                subject_id=subject,
                predicate=predicate,
                value=value,
                source_type="discovery",
                confidence=0.9,
                evidence_ids=[],
                observed_at=seed_local.utc_now(),
                dimensions=dimensions,
            )
            ledger.append(
                "fact.observed",
                seed_local.DEFAULT_WORKSPACE,
                {"fact": seed_local.to_plain(fact)},
            )
    finally:
        ledger.close()


def test_cli_current_facts_exposes_listener_facts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-listeners.sqlite"
    _persist_listener_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--current-facts"]) == 0
    output = capsys.readouterr().out

    assert "* node115 listening_endpoint tcp 0.0.0.0:22" in output
    assert "* node115 listening_protocol tcp" in output
    assert "* node115 listening_address 0.0.0.0" in output
    assert "* node115 listening_port 22" in output
    assert "* node115 listening_endpoint udp 127.0.0.1:53" in output


def test_cli_impact_includes_compact_listener_endpoints_without_inference(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-listeners.sqlite"
    _persist_listener_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0
    output = capsys.readouterr().out

    assert "listening endpoints:" in output
    assert "- tcp 0.0.0.0:22" in output
    assert "- udp 127.0.0.1:53" in output
    assert (
        "- availability/reachability/health/ownership: not inferred from listener facts"
        in output
    )
    assert "availability_status: unknown" in output
    assert "reachability_status" not in output
    assert "endpoint_health" not in output
    assert "process_owner" not in output
    assert "service_owner" not in output


def test_cli_current_facts_exposes_storage_topology_facts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-storage.sqlite"
    _persist_storage_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--current-facts"]) == 0
    output = capsys.readouterr().out

    assert "* node115 block_device sda" in output
    assert "* node115 partition sda1" in output
    assert "* node115 block_device_size_bytes 1073741824" in output
    assert "* node115 block_device_rotational true" in output
    assert "* node115 block_device_removable false" in output
    assert "* node115 block_device_model Fast Disk" in output
    assert "* node115 block_device_vendor SEED" in output
    assert "* node115 block_device_parent sda" in output


def test_cli_impact_includes_compact_storage_topology_without_health_inference(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-storage.sqlite"
    _persist_storage_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--impact", "node115"]) == 0
    output = capsys.readouterr().out

    assert "storage topology:" in output
    assert "- devices:" in output
    assert "  - sda" in output
    assert "  - nvme0n1" in output
    assert "- partitions:" in output
    assert "  - sda1" in output
    assert "  - nvme0n1p1" in output
    assert "- parent relationships:" in output
    assert "  - sda1 -> sda" in output
    assert "- mount relationships:" in output
    assert "  - /dev/sda1 -> /" in output
    assert (
        "- health/availability/filesystem-health: not inferred from storage facts"
        in output
    )
    assert "availability_status: unknown" in output
    assert "storage_health" not in output
    assert "filesystem_health" not in output
