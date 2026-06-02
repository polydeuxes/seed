from seed_runtime.events import EventLedger
from seed_runtime.models import Approval, ToolSpec
from seed_runtime.policy import PolicyGate
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def tool(action, risk):
    return ToolSpec(name="t", summary="t", toolkit_id="tk", input_schema={"type": "object"}, output_schema={"type": "object"}, policy_action=action, implementation="m:f", risk_class=risk)


def test_l1_allows():
    state = StateProjector(EventLedger()).project("ws")
    assert PolicyGate().evaluate(tool("safe.read", "L1"), state).outcome == "allow"


def test_l3_requires_approval_then_allows():
    ledger = EventLedger()
    ledger.append("approval.granted", "ws", {"approval": to_plain(Approval(id="appr", action="ssh.install", scope="ent_1", approved_by="user"))})
    state = StateProjector(ledger).project("ws")

    assert PolicyGate().evaluate(tool("ssh.install", "L3"), state, scope="ent_1").outcome == "allow"
    assert PolicyGate().evaluate(tool("ssh.install", "L3"), state, scope="ent_2").outcome == "require_approval"


def test_l4_blocks():
    state = StateProjector(EventLedger()).project("ws")
    assert PolicyGate().evaluate(tool("dangerous", "L4"), state).outcome == "block"
