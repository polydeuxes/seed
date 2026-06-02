from datetime import datetime, timedelta, timezone

from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.serialization import to_plain
from seed_runtime.models import Approval, Entity, Fact, Goal, ToolNeed, utc_now
from seed_runtime.state import StateProjector


def test_projector_rebuilds_state_deterministically():
    ledger = EventLedger()
    workspace_id = "ws_1"
    entity = Entity(id="ent_1", kind="host", name="node-1")
    fact = Fact(id="fact_1", subject_id="ent_1", predicate="ssh.running", value=False, evidence_ids=["evt_source"], observed_at=utc_now())
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


def test_has_approval_compares_expiration_against_utc_now():
    ledger = EventLedger()
    workspace_id = "ws_utc_approval"
    approval = Approval(
        id=new_id("appr"),
        action="ssh.install",
        scope="ent_1",
        approved_by="user",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
    )
    expired = Approval(
        id=new_id("appr"),
        action="ssh.install",
        scope="ent_2",
        approved_by="user",
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=5),
    )

    ledger.append("approval.granted", workspace_id, {"approval": to_plain(approval)})
    ledger.append("approval.granted", workspace_id, {"approval": to_plain(expired)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.has_approval("ssh.install", "ent_1") == approval
    assert state.has_approval("ssh.install", "ent_2") is None
