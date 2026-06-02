import importlib.util
import sys
from pathlib import Path

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
        ["--http", "--raw", "--model", "qwen2.5:3b", "install", "docker"]
    )

    assert args.http is True
    assert args.raw is True
    assert args.model == "qwen2.5:3b"
    assert args.message == ["install", "docker"]
