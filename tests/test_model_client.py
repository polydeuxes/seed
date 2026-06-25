import pytest

from seed_runtime.context import DecisionInputPacket
from seed_runtime.model_client import (
    CommandTransport,
    DecisionParseError,
    DecisionPromptModelClient,
    ParsedDecisionProducer,
    StrictJSONDecisionParser,
    render_decision_prompt,
    serialize_decision_prompt,
)


class FakeTransport:
    def __init__(self, response: str) -> None:
        self.response = response
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def sample_context() -> DecisionInputPacket:
    return DecisionInputPacket(
        workspace_id="workspace-1",
        session_id="session-1",
        current_input={"event_id": "event-1", "text": "is example_host out of disk?"},
        active_goal={
            "id": "goal-1",
            "summary": "Check node health",
            "status": "active",
        },
        entities=[{"id": "entity-1", "kind": "host", "name": "example_host"}],
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
                "output_schema": {
                    "type": "object",
                    "properties": {"used_bytes": {"type": "integer"}},
                    "required": ["used_bytes"],
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


def test_render_decision_prompt_snapshot_is_compact_and_deterministic():
    prompt = render_decision_prompt(sample_context())

    assert (
        prompt
        == """TASK INSTRUCTION
Choose exactly one decision for the Seed runtime.

CURRENT INPUT
{"text":"is example_host out of disk?"}

RELEVANT STATE SUMMARY
{"active_goal":{"status":"active","summary":"Check node health"},"entities":[{"kind":"host","name":"example_host"}],"facts":[{"predicate":"disk_status","subject":"example_host","value":"unknown"}]}

VISIBLE TOOLS
[{"input_schema":{"properties":{"host":{"type":"string"}},"required":["host"],"type":"object"},"name":"docker_storage_summary","output_schema":{"properties":{"used_bytes":{"type":"integer"}},"required":["used_bytes"],"type":"object"},"risk_class":"L1","summary":"Summarize Docker disk usage for a host."}]

OPEN TOOL NEEDS
[]

ALLOWED JSON DECISION SHAPES
[{"answer":"...","kind":"answer","reason":"..."},{"kind":"ask_question","question":"...","reason":"..."},{"kind":"call_tool","reason":"...","tool_arguments":{},"tool_name":"visible_tool_name"},{"kind":"request_tool","reason":"...","tool_need":{"capability":"capability_name","name":"snake_case_name","summary":"What the missing tool should do."}},{"kind":"refuse","reason":"..."}]

STRICT OUTPUT
Output only one JSON object matching one allowed shape. Do not include prose, markdown, code fences, or multiple objects."""
    )
    assert render_decision_prompt(sample_context()) == prompt
    assert len(prompt) < 1300


def test_render_decision_prompt_includes_only_model_relevant_fields():
    prompt = render_decision_prompt(sample_context())

    assert "workspace-1" not in prompt
    assert "session-1" not in prompt
    assert "event-1" not in prompt
    assert "goal-1" not in prompt
    assert "entity-1" not in prompt
    assert "fact-1" not in prompt
    assert "policy_action" not in prompt
    assert "read_docker_storage" not in prompt


def test_render_decision_prompt_includes_open_tool_needs_without_runtime_fields():
    context = sample_context()
    context_with_need = DecisionInputPacket(
        **{
            **context.to_dict(),
            "open_tool_needs": [
                {
                    "id": "need-1",
                    "workspace_id": "workspace-1",
                    "name": "inspect_docker_storage",
                    "summary": "Inspect Docker storage on a host.",
                    "capability": "docker_storage_inspection",
                    "reason": "Current visible tools are insufficient.",
                    "status": "proposed",
                    "desired_inputs": ["host"],
                    "desired_outputs": ["storage_summary"],
                }
            ],
        }
    )

    prompt = render_decision_prompt(context_with_need)

    assert (
        '{"capability":"docker_storage_inspection","desired_inputs":["host"],'
        '"desired_outputs":["storage_summary"],"name":"inspect_docker_storage",'
        '"reason":"Current visible tools are insufficient.","summary":"Inspect Docker storage on a host."}'
        in prompt
    )
    assert "need-1" not in prompt
    assert "workspace-1" not in prompt
    assert "proposed" not in prompt


def test_serialize_decision_prompt_is_backward_compatible_alias():
    assert serialize_decision_prompt(sample_context()) == render_decision_prompt(
        sample_context()
    )


def test_serialize_decision_prompt_includes_retry_prompt_when_present():
    context = sample_context()
    retry_decision_input = DecisionInputPacket(
        **{
            **context.to_dict(),
            "retry_prompt": {"validation_errors": ["answer decisions require answer"]},
        }
    )

    prompt = serialize_decision_prompt(retry_decision_input)

    assert "\n\nCORRECTION REQUIRED\n" in prompt
    assert "answer decisions require answer" in prompt


def test_decision_prompt_model_client_sends_serialized_context_to_transport():
    transport = FakeTransport(
        '{"kind":"answer","reason":"context has it","answer":"example_host is healthy"}'
    )
    client = DecisionPromptModelClient(transport)

    raw = client.complete(sample_context())

    assert (
        raw
        == '{"kind":"answer","reason":"context has it","answer":"example_host is healthy"}'
    )
    assert len(transport.prompts) == 1
    assert "CURRENT INPUT" in transport.prompts[0]
    assert "ALLOWED JSON DECISION SHAPES" in transport.prompts[0]


def test_decision_prompt_model_client_is_injectable_into_parsed_decision_model():
    transport = FakeTransport(
        '{"kind":"call_tool","reason":"visible tool matches","tool_name":"docker_storage_summary","tool_arguments":{"host":"example_host"}}'
    )
    model = ParsedDecisionProducer(DecisionPromptModelClient(transport))

    decision = model.decide(sample_context())

    assert decision.kind == "call_tool"
    assert decision.tool_name == "docker_storage_summary"
    assert decision.tool_arguments == {"host": "example_host"}


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
