from seed_runtime.events import EventLedger
from seed_runtime.execution import ToolExecutor
from seed_runtime.models import Entity, Fact, ToolNeed, utc_now
from seed_runtime.registry import ToolRegistry
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def _executor_with_inventory():
    ledger = EventLedger()
    registry = ToolRegistry()
    registry.load_manifest("toolkits/core/echo/toolkit.yaml")
    registry.load_manifest("toolkits/generated/environment_inventory/toolkit.yaml")
    projector = StateProjector(ledger)
    return ledger, ToolExecutor(ledger, registry, projector)


def test_environment_inventory_lists_registered_model_visible_tools():
    ledger, executor = _executor_with_inventory()

    result = executor.execute("ws", "ses", "list_registered_tools", {})

    assert result.kind == "tool_result"
    tools = result.payload["output"]["tools"]
    assert {tool["name"] for tool in tools} >= {
        "echo",
        "list_registered_tools",
        "list_open_tool_needs",
        "list_known_entities",
        "list_known_facts",
    }
    assert {tool["risk_class"] for tool in tools} == {"L1"}
    assert "tool.call.completed" in [event.kind for event in ledger.list_events("ws")]


def test_environment_inventory_lists_open_tool_needs_only_from_state():
    ledger, executor = _executor_with_inventory()
    open_need = ToolNeed(
        id="need_open",
        workspace_id="ws",
        name="network_inventory",
        summary="Inventory approved network targets",
        capability="network_inventory",
        reason="Need a future network discovery tool",
        desired_inputs=["scope"],
        desired_outputs=["hosts"],
    )
    closed_need = ToolNeed(
        id="need_closed",
        workspace_id="ws",
        name="host_notes",
        summary="Record notes about hosts",
        capability="host_notes",
        reason="Already registered",
        status="registered",
    )
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(open_need)})
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(closed_need)})

    result = executor.execute("ws", "ses", "list_open_tool_needs", {})

    assert result.kind == "tool_result"
    assert result.payload["output"]["tool_needs"] == [to_plain(open_need)]


def test_environment_inventory_lists_known_entities_and_facts_from_state():
    ledger, executor = _executor_with_inventory()
    entity = Entity(
        id="ent_1",
        kind="host",
        name="example_host",
        aliases=["primary"],
        attributes={"source": "user"},
        confidence=0.9,
    )
    fact = Fact(
        id="fact_1",
        subject_id="ent_1",
        predicate="ssh.running",
        value=False,
        evidence_ids=["evt_source"],
        observed_at=utc_now(),
        confidence=0.8,
    )
    ledger.append("entity.upserted", "ws", {"entity": to_plain(entity)})
    ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})

    entities = executor.execute("ws", "ses", "list_known_entities", {})
    facts = executor.execute("ws", "ses", "list_known_facts", {})

    assert entities.kind == "tool_result"
    assert entities.payload["output"]["entities"] == [to_plain(entity)]
    assert facts.kind == "tool_result"
    assert facts.payload["output"]["facts"] == [to_plain(fact)]
