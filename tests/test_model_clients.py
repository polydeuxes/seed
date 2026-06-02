import json
from urllib import request

import pytest

from seed_runtime.context import ContextPacket
from seed_runtime.model_client import DecisionParseError
from seed_runtime.model_clients import (
    LlamaCppDecisionModel,
    LocalChatModel,
    OllamaDecisionModel,
    build_decision_prompt,
    parse_decision_text,
)


class MockHTTPResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class UrlopenRecorder:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.requests: list[request.Request] = []
        self.timeouts: list[float] = []

    def __call__(self, http_request: request.Request, timeout: float):
        self.requests.append(http_request)
        self.timeouts.append(timeout)
        return MockHTTPResponse(self.payload)

    @property
    def last_json(self) -> dict:
        return json.loads(self.requests[-1].data.decode("utf-8"))


def echo_context() -> ContextPacket:
    return ContextPacket(
        workspace_id="workspace-1",
        session_id="session-1",
        current_input={"event_id": "event-1", "text": "echo hello"},
        active_goal=None,
        entities=[],
        facts=[],
        tools=[
            {
                "name": "echo",
                "summary": "Echo a message.",
                "input_schema": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                },
                "output_schema": {"type": "object"},
                "policy_action": "echo",
                "risk_class": "L1",
            }
        ],
        open_tool_needs=[],
        decision_schema={"kinds": ["answer", "call_tool", "refuse"]},
    )


def expected_echo_decision_text() -> str:
    return json.dumps(
        {
            "kind": "call_tool",
            "reason": "echo is available and matches the request",
            "tool_name": "echo",
            "tool_arguments": {"message": "hello"},
        },
        separators=(",", ":"),
    )


def test_local_chat_model_base_shape_exposes_common_settings():
    client = LocalChatModel(
        model_name="local-small",
        endpoint_url="http://localhost:1234",
        timeout=4.5,
        temperature=0.2,
        max_tokens=128,
        num_predict=64,
    )

    assert client.model_name == "local-small"
    assert client.endpoint_url == "http://localhost:1234"
    assert client.timeout == 4.5
    assert client.temperature == 0.2
    assert client.max_tokens == 128
    assert client.num_predict == 64


def test_build_decision_prompt_renders_context_and_allowed_shape():
    prompt = build_decision_prompt(echo_context())

    assert '"text":"echo hello"' in prompt
    assert '"workspace_id":"workspace-1"' in prompt
    assert '"kind":"call_tool"' in prompt
    assert '"tool_name":"visible_tool_name"' in prompt
    assert "Return only JSON, no markdown, no prose." in prompt
    assert '"kind":"ask_question"' not in prompt


def test_parse_decision_text_accepts_first_manual_target():
    decision = parse_decision_text(expected_echo_decision_text())

    assert decision.kind == "call_tool"
    assert decision.reason == "echo is available and matches the request"
    assert decision.tool_name == "echo"
    assert decision.tool_arguments == {"message": "hello"}


@pytest.mark.parametrize(
    "text",
    [
        'Here is the decision: {"kind":"answer","reason":"ok","answer":"hi"}',
        '```json\n{"kind":"answer","reason":"ok","answer":"hi"}\n```',
        ' {"kind":"answer","reason":"ok","answer":"hi"}',
    ],
)
def test_parse_decision_text_rejects_prose_fences_and_wrappers(text: str):
    with pytest.raises(DecisionParseError):
        parse_decision_text(text)


def test_parse_decision_text_validates_kind_and_reason():
    with pytest.raises(DecisionParseError, match="kind and reason"):
        parse_decision_text('{"kind":"answer","answer":"hi"}')


def test_ollama_decision_model_posts_chat_request_and_parses_decision(monkeypatch):
    recorder = UrlopenRecorder(
        {"message": {"role": "assistant", "content": expected_echo_decision_text()}}
    )
    monkeypatch.setattr(request, "urlopen", recorder)
    model = OllamaDecisionModel(
        "llama3.2:1b",
        endpoint_url="http://ollama.local/",
        timeout=7,
        temperature=0,
        num_predict=96,
    )

    decision = model.decide(echo_context())

    assert decision.kind == "call_tool"
    assert decision.tool_arguments == {"message": "hello"}
    assert recorder.requests[0].full_url == "http://ollama.local/api/chat"
    assert recorder.timeouts == [7]
    payload = recorder.last_json
    assert payload["model"] == "llama3.2:1b"
    assert payload["stream"] is False
    assert payload["format"] == "json"
    assert payload["options"] == {"temperature": 0, "num_predict": 96}
    assert payload["messages"][0]["role"] == "user"
    assert "Return only JSON, no markdown, no prose." in payload["messages"][0]["content"]


def test_ollama_decision_model_can_use_generate_endpoint(monkeypatch):
    recorder = UrlopenRecorder({"response": expected_echo_decision_text()})
    monkeypatch.setattr(request, "urlopen", recorder)
    model = OllamaDecisionModel(
        "llama3.2:1b",
        endpoint_url="http://ollama.local",
        max_tokens=55,
        api="generate",
    )

    decision = model.decide(echo_context())

    assert decision.tool_name == "echo"
    assert recorder.requests[0].full_url == "http://ollama.local/api/generate"
    assert recorder.last_json["options"] == {"temperature": 0.0, "num_predict": 55}
    assert "prompt" in recorder.last_json


def test_llamacpp_decision_model_posts_openai_chat_request_and_parses(monkeypatch):
    recorder = UrlopenRecorder(
        {"choices": [{"message": {"content": expected_echo_decision_text()}}]}
    )
    monkeypatch.setattr(request, "urlopen", recorder)
    model = LlamaCppDecisionModel(
        "local-model",
        endpoint_url="http://llama.local",
        timeout=9,
        max_tokens=77,
    )

    decision = model.decide(echo_context())

    assert decision.kind == "call_tool"
    assert decision.tool_name == "echo"
    assert recorder.requests[0].full_url == "http://llama.local/v1/chat/completions"
    assert recorder.timeouts == [9]
    payload = recorder.last_json
    assert payload["model"] == "local-model"
    assert payload["temperature"] == 0.0
    assert payload["max_tokens"] == 77
    assert payload["response_format"] == {"type": "json_object"}
    assert payload["messages"][0]["role"] == "user"
