from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.models import Entity, Fact, Goal, ToolNeed, utc_now, Approval


def test_projector_rebuilds_state_deterministically():
    ledger = EventLedger()
    workspace_id = "ws_1"
    entity = Entity(id="ent_1", kind="host", name="node-1")
    fact = Fact(id="fact_1", subject_id="ent_1", predicate="ssh.running", value=False, source_event_id="evt_source", observed_at=utc_now())
    goal = Goal(id="goal_1", workspace_id=workspace_id, summary="Make SSH work")
    need = ToolNeed(id="need_1", workspace_id=workspace_id, name="install_ssh_server", summary="Install SSH", capability="ssh_access", reason="missing tool")
    approval = Approval(id=new_id("appr"), action="ssh.install", scope="ent_1", approved_by="user")

    ledger.append("entity.upserted", workspace_id, {"entity": to_plain(entity)})
    ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})
    ledger.append("goal.created", workspace_id, {"goal": to_plain(goal)})
    ledger.append("tool_need.created", workspace_id, {"tool_need": to_plain(need)})
    ledger.append("approval.granted", workspace_id, {"approval": to_plain(approval)})

    first = StateProjector(ledger).project(workspace_id)
    second = StateProjector(ledger).project(workspace_id)

    assert first == second
    assert first.entities["ent_1"].name == "node-1"
    assert first.facts["fact_1"].value is False
    assert first.goals["goal_1"].status == "active"
    assert first.open_tool_needs[0].name == "install_ssh_server"
    assert first.has_approval("ssh.install", "ent_1") is not None
