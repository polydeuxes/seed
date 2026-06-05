from seed_runtime.decision_journal import DecisionJournal, context_hash
from seed_runtime.events import EventLedger
from seed_runtime.runtime_loop import RuntimeContext
from seed_runtime.state import State


def test_decision_journal_appends_eventledger_event_not_mutable_store():
    ledger = EventLedger()
    journal = DecisionJournal(ledger)

    event = journal.append_record(
        workspace_id="ws",
        run_id="run-1",
        decision_kind="answer",
        reason="because",
        context_hash="abc123",
        policy_allowed=True,
        outcome="answered",
    )

    assert event.kind == "decision.recorded"
    assert ledger.list_events("ws") == [event]
    assert not hasattr(journal, "save")
    assert not hasattr(journal, "update")
    assert not hasattr(journal, "records")
    assert journal.ledger is ledger


def test_context_hash_is_deterministic_for_equivalent_context():
    first = RuntimeContext(
        workspace_id="ws",
        run_id="run-1",
        state=State(workspace_id="ws"),
        current_input={"metadata": {"b": 2, "a": 1}, "text": "hello"},
        tools=[{"risk_class": "L1", "name": "echo"}],
    )
    second = RuntimeContext(
        workspace_id="ws",
        run_id="run-1",
        state=State(workspace_id="ws"),
        current_input={"text": "hello", "metadata": {"a": 1, "b": 2}},
        tools=[{"name": "echo", "risk_class": "L1"}],
    )

    assert context_hash(first) == context_hash(second)
