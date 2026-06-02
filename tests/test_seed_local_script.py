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
    assert "- Identify target host for service." in output
    assert "- Confirm container name." in output
    assert "- Verify Docker access." in output
    assert "- Request approval before restart." in output
    assert "tool.call.started" not in output
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
