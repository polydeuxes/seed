import pytest

from seed_runtime.context import ContextPacket
from seed_runtime.model_client import (
    CommandTransport,
    DecisionParseError,
    DecisionPromptModelClient,
    ParsedDecisionModel,
    StrictJSONDecisionParser,
    serialize_decision_prompt,
)


class FakeTransport:
    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def sample_context() -> ContextPacket:
    return ContextPacket(
        workspace_id="workspace-1",
        session_id="session-1",
        current_input={"event_id": "event-1", "text": "is node-1 out of disk?"},
        active_goal={
            "id": "goal-1",
            "summary": "Check node health",
            "status": "active",
        },
        entities=[{"id": "entity-1", "kind": "host", "name": "node-1"}],
        facts=[
            {
                "id": "fact-1",
                "subject_id": "entity-1",
                "predicate": "disk_status",
                "value": "unknown",
            }
        ],
        tools=[
            {
                "name": "docker_storage_summary",
                "summary": "Summarize Docker disk usage for a host.",
                "input_schema": {
                    "type": "object",
                    "properties": {"host": {"type": "string"}},
                    "required": ["host"],
                },
                "policy_action": "read_docker_storage",
                "risk_class": "L1",
            }
        ],
        open_tool_needs=[],
        decision_schema={
            "kinds": ["answer", "ask_question", "call_tool", "request_tool", "refuse"]
        },
    )


def test_strict_json_decision_parser_accepts_decision_object():
    decision = StrictJSONDecisionParser().parse(
        '{"kind":"answer","reason":"done","answer":"hello"}'
    )
    assert decision.kind == "answer"
    assert decision.answer == "hello"


def test_strict_json_decision_parser_rejects_prose():
    with pytest.raises(DecisionParseError):
        StrictJSONDecisionParser().parse('Here is the decision: {"kind":"answer"}')


def test_serialize_decision_prompt_uses_stable_small_model_sections():
    prompt = serialize_decision_prompt(sample_context())

    assert prompt.startswith("TASK\nChoose one decision for the Seed runtime.")
    assert "\n\nCURRENT INPUT\n" in prompt
    assert "\n\nSTATE\n" in prompt
    assert "\n\nTOOLS\n" in prompt
    assert "\n\nOUTPUT JSON SCHEMA\n" in prompt
    assert '"text": "is node-1 out of disk?"' in prompt
    assert '"name": "docker_storage_summary"' in prompt
    assert "Return only one JSON object" in prompt


def test_serialize_decision_prompt_includes_retry_prompt_when_present():
    context = sample_context()
    retry_context = ContextPacket(
        **{
            **context.to_dict(),
            "retry_prompt": {"validation_errors": ["answer decisions require answer"]},
        }
    )

    prompt = serialize_decision_prompt(retry_context)

    assert "\n\nCORRECTION REQUIRED\n" in prompt
    assert "answer decisions require answer" in prompt


def test_decision_prompt_model_client_sends_serialized_context_to_transport():
    transport = FakeTransport(
        '{"kind":"answer","reason":"context has it","answer":"node-1 is healthy"}'
    )
    client = DecisionPromptModelClient(transport)

    raw = client.complete(sample_context())

    assert (
        raw
        == '{"kind":"answer","reason":"context has it","answer":"node-1 is healthy"}'
    )
    assert len(transport.prompts) == 1
    assert "CURRENT INPUT" in transport.prompts[0]
    assert "OUTPUT JSON SCHEMA" in transport.prompts[0]


def test_decision_prompt_model_client_is_injectable_into_parsed_decision_model():
    transport = FakeTransport(
        '{"kind":"call_tool","reason":"visible tool matches","tool_name":"docker_storage_summary","tool_arguments":{"host":"node-1"}}'
    )
    model = ParsedDecisionModel(DecisionPromptModelClient(transport))

    decision = model.decide(sample_context())

    assert decision.kind == "call_tool"
    assert decision.tool_name == "docker_storage_summary"
    assert decision.tool_arguments == {"host": "node-1"}


def test_command_transport_writes_prompt_to_stdin_and_returns_stdout():
    transport = CommandTransport(
        [
            "python",
            "-c",
            'import sys; prompt=sys.stdin.read(); print(\'{\\"kind\\":\\"answer\\",\\"reason\\":\\"saw %s chars\\",\\"answer\\":\\"ok\\"}\' % len(prompt))',
        ]
    )

    raw = transport.complete("hello")

    assert raw.strip() == '{"kind":"answer","reason":"saw 5 chars","answer":"ok"}'
