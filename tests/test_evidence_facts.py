from seed_runtime.base import SeedModel
from seed_runtime.context import ContextComposer
from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.models import utc_now
from seed_runtime.registry import ToolRegistry
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector


def test_evidence_backed_fact_projects_with_provenance():
    ledger = EventLedger()
    workspace_id = "ws_evidence"
    observed_at = utc_now()
    evidence = Evidence(
        id="evd_1",
        workspace_id=workspace_id,
        source="host_notes",
        kind="host.note",
        observed_at=observed_at,
        payload={"host": "node-1", "ssh_running": False},
        confidence=0.9,
    )
    fact = Fact(
        id="fact_1",
        subject_id="ent_1",
        predicate="ssh.running",
        value=False,
        evidence_ids=[evidence.id],
        observed_at=observed_at,
        confidence=evidence.confidence,
    )

    ledger.append("evidence.observed", workspace_id, {"evidence": to_plain(evidence)})
    ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})

    state = StateProjector(ledger).project(workspace_id)

    assert state.evidence[evidence.id] == evidence
    assert state.facts[fact.id].evidence_ids == [evidence.id]
    assert state.facts[fact.id].confidence == evidence.confidence


def test_evidence_and_fact_share_seed_model_conventions():
    assert issubclass(Evidence, SeedModel)
    assert issubclass(Fact, SeedModel)


def test_context_includes_evidence_backed_facts():
    ledger = EventLedger()
    workspace_id = "ws_evidence"
    observed_at = utc_now()
    evidence = Evidence(
        id="evd_1",
        workspace_id=workspace_id,
        source="host_notes",
        kind="host.note",
        observed_at=observed_at,
        payload={"host": "node-1", "ssh_running": False},
    )
    fact = Fact(
        id="fact_1",
        subject_id="ent_1",
        predicate="ssh.running",
        value=False,
        evidence_ids=[evidence.id],
        observed_at=observed_at,
    )

    ledger.append("evidence.observed", workspace_id, {"evidence": to_plain(evidence)})
    ledger.append("fact.observed", workspace_id, {"fact": to_plain(fact)})
    input_event = ledger.append("input.user_message", workspace_id, {"text": "status?"})
    state = StateProjector(ledger).project(workspace_id)

    packet = ContextComposer(ToolRegistry()).compose(
        workspace_id, None, input_event, state
    )

    assert packet.facts == [
        {
            "id": "fact_1",
            "subject_id": "ent_1",
            "predicate": "ssh.running",
            "value": False,
            "evidence_ids": ["evd_1"],
            "observed_at": observed_at,
            "expires_at": None,
            "source_type": "user",
            "confidence": 0.9,
            "inferred": False,
            "evidence": [
                {
                    "id": "evd_1",
                    "workspace_id": workspace_id,
                    "source": "host_notes",
                    "kind": "host.note",
                    "observed_at": observed_at,
                    "payload": {"host": "node-1", "ssh_running": False},
                    "confidence": 1.0,
                }
            ],
        }
    ]
