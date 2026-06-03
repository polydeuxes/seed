import importlib.util
import sys
from pathlib import Path

import pytest

from seed_runtime.intent_classifier import IntentDecisionModel, IntentPromptModelClient


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
    assert isinstance(app.runtime.model, IntentDecisionModel)
    assert [tool.name for tool in app.context_composer.registry.list_tools()] == ["echo"]
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
    assert "tool.call.started" in output
    assert "tool.call.completed" in output


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


def test_fact_seed_appends_evidence_and_fact_before_user_message():
    seed_local = load_seed_local_module()
    app = seed_local.build_local_app()

    app.seed_facts([seed_local.DevFactSeed("jellyfin", "runtime", "docker")])
    result = app.run("echo hello")

    event_kinds = [event["kind"] for event in result["events"]]
    assert event_kinds[:3] == [
        "evidence.observed",
        "fact.observed",
        "input.user_message",
    ]

    state = app.projector.project(app.workspace_id)
    fact = next(iter(state.facts.values()))
    evidence = next(iter(state.evidence.values()))
    assert fact.subject_id == "jellyfin"
    assert fact.predicate == "runtime"
    assert fact.value == "docker"
    assert fact.evidence_ids == [evidence.id]
    assert evidence.payload == {
        "subject_id": "jellyfin",
        "predicate": "runtime",
        "value": "docker",
        "index": 1,
    }


def test_cli_fact_seed_influences_service_recommendation_ranking(monkeypatch, capsys):
    seed_local = load_seed_local_module()

    monkeypatch.setattr(
        seed_local.IntentPromptModelClient,
        "complete",
        lambda self, context: (
            '{"intent":"missing_tool","reason":"needs service tool","arguments":{}}'
        ),
    )

    assert seed_local.main(
        ["--fact", "jellyfin", "runtime", "docker", "restart jellyfin?"]
    ) == 0

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

    assert seed_local.main(
        ["--fact", "jellyfin", "runtime", "docker", "--plan", "restart jellyfin?"]
    ) == 0

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
        "missing:\n- target_host_known\n- provider_registered\n- approval_present"
        in output
    )
    assert "preconditions:" in output
    assert "- id: target_host_known\n  satisfied: false" in output
    assert "reason: no host entity or target host fact is present" in output
    assert "tool.call" not in output
    assert "approved" not in output.lower()


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
