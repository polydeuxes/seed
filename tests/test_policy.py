from seed_runtime.events import EventLedger
from seed_runtime.models import Approval, ToolSpec
from seed_runtime.policy import PolicyGate
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def tool(action, risk):
    return ToolSpec(
        name="t",
        summary="t",
        toolkit_id="tk",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
        policy_action=action,
        implementation="m:f",
        risk_class=risk,
    )


def projected_state():
    return StateProjector(EventLedger()).project("ws")


def gate_for(*actions):
    return PolicyGate(dict(actions))


def test_l1_allows():
    policy = gate_for(("safe.read", "L1"))

    decision = policy.evaluate(tool("safe.read", "L1"), projected_state())

    assert decision.outcome == "allow"
    assert decision.risk_class == "L1"


def test_l2_requires_confirmation():
    policy = gate_for(("logs.read", "L2"))

    decision = policy.evaluate(tool("logs.read", "L1"), projected_state())

    assert decision.outcome == "require_confirmation"
    assert decision.risk_class == "L2"


def test_l3_requires_approval():
    policy = gate_for(("ssh.install", "L3"))

    decision = policy.evaluate(tool("ssh.install", "L1"), projected_state())

    assert decision.outcome == "require_approval"
    assert decision.risk_class == "L3"


def test_l4_blocks():
    policy = gate_for(("database.delete", "L4"))

    decision = policy.evaluate(tool("database.delete", "L1"), projected_state())

    assert decision.outcome == "block"
    assert decision.risk_class == "L4"


def test_unknown_action_blocks():
    policy = gate_for(("known.read", "L1"))

    decision = policy.evaluate(tool("unknown.read", "L1"), projected_state())

    assert decision.outcome == "block"
    assert decision.reason == "unknown policy action is blocked by default"


def test_existing_matching_approval_allows():
    ledger = EventLedger()
    ledger.append(
        "approval.granted",
        "ws",
        {
            "approval": to_plain(
                Approval(
                    id="appr",
                    action="ssh.install",
                    scope="ent_1",
                    approved_by="user",
                )
            )
        },
    )
    state = StateProjector(ledger).project("ws")
    policy = gate_for(("ssh.install", "L3"))

    decision = policy.evaluate(tool("ssh.install", "L1"), state, scope="ent_1")

    assert decision.outcome == "allow"
    assert decision.approval_id == "appr"


def test_non_matching_approval_still_requires_approval():
    ledger = EventLedger()
    ledger.append(
        "approval.granted",
        "ws",
        {
            "approval": to_plain(
                Approval(
                    id="appr",
                    action="ssh.install",
                    scope="ent_1",
                    approved_by="user",
                )
            )
        },
    )
    state = StateProjector(ledger).project("ws")
    policy = gate_for(("ssh.install", "L3"))

    decision = policy.evaluate(tool("ssh.install", "L1"), state, scope="ent_2")

    assert decision.outcome == "require_approval"
    assert decision.approval_id is None
