from datetime import datetime, timedelta, timezone
import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.capability_inventory import build_capability_inventory
from seed_runtime.evidence import Evidence
from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.models import ToolNeed, ToolSpec
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector

SCRIPT_PATH = Path("scripts/seed_local.py")
BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _tool(name: str) -> ToolSpec:
    return ToolSpec(
        name=name,
        summary=f"{name} tool",
        input_schema={},
        output_schema={},
        policy_action=name,
        implementation="tests:no_execute",
        toolkit_id="tests",
        risk_class="L1",
    )


def _need(capability: str) -> ToolNeed:
    return ToolNeed(
        id=f"need_{capability}",
        workspace_id="ws",
        name=f"Need {capability}",
        summary=f"Need {capability}",
        capability=capability,
        reason="test inventory universe",
    )


def _verification_fact(
    capability: str,
    value: str = "verified",
    *,
    fact_id: str | None = None,
    evidence_id: str | None = None,
    observed_at: datetime = BASE_TIME,
    expires_at: datetime | None = None,
    source_type: str = "provider",
) -> Fact:
    return Fact(
        id=fact_id or f"fact_{capability}",
        subject_id=capability,
        predicate="capability_verified",
        value=value,
        evidence_ids=[evidence_id or f"evd_{capability}"],
        observed_at=observed_at,
        expires_at=expires_at,
        source_type=source_type,
    )


def _evidence(capability: str, *, evidence_id: str | None = None) -> Evidence:
    return Evidence(
        id=evidence_id or f"evd_{capability}",
        workspace_id="ws",
        source="provider_report",
        kind="capability.verification.report",
        observed_at=BASE_TIME,
        payload={"capability": capability},
        confidence=0.8,
    )


def _project(ledger: EventLedger):
    return StateProjector(ledger).project("ws")


def test_capability_inventory_is_read_only():
    ledger = EventLedger()
    ledger.append("tool.registered", "ws", {"tool": to_plain(_tool("web_search"))})
    state = _project(ledger)
    before_events = [event.id for event in ledger.list_events("ws")]
    before_facts = dict(state.facts)

    inventory = build_capability_inventory(state)

    assert [entry.capability for entry in inventory] == ["web_search"]
    assert [event.id for event in ledger.list_events("ws")] == before_events
    assert state.facts == before_facts


def test_capability_inventory_uses_no_tool_executor_or_runtime(monkeypatch):
    import seed_runtime.execution as execution_module
    import seed_runtime.runtime as runtime_module

    monkeypatch.setattr(
        execution_module.ToolExecutor,
        "__init__",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("ToolExecutor used")),
    )
    monkeypatch.setattr(
        runtime_module.Runtime,
        "__init__",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("Runtime used")),
    )
    ledger = EventLedger()
    ledger.append("tool.registered", "ws", {"tool": to_plain(_tool("web_search"))})
    state = _project(ledger)

    assert build_capability_inventory(state)[0].state == "unverified"


def test_verified_capability_inventory_derives_from_facts_and_evidence():
    ledger = EventLedger()
    ledger.append("evidence.observed", "ws", {"evidence": to_plain(_evidence("web_search"))})
    ledger.append("fact.observed", "ws", {"fact": to_plain(_verification_fact("web_search"))})
    state = _project(ledger)

    entry = build_capability_inventory(state, now=BASE_TIME + timedelta(seconds=30))[0]

    assert entry.capability == "web_search"
    assert entry.state == "verified"
    assert entry.supporting_facts == ["fact_web_search"]
    assert [evidence.evidence_id for evidence in entry.supporting_evidence] == [
        "evd_web_search"
    ]
    assert entry.age_seconds == 30


def test_unverified_capability_inventory_derives_from_missing_facts():
    ledger = EventLedger()
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(_need("ssh_access"))})
    state = _project(ledger)

    entry = build_capability_inventory(state)[0]

    assert entry.capability == "ssh_access"
    assert entry.state == "unverified"
    assert entry.supporting_facts == []
    assert "no capability_verified fact" in entry.reason


def test_stale_status_uses_existing_expired_fact_semantics_only():
    ledger = EventLedger()
    expired_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    fact = _verification_fact("web_search", expires_at=expired_at)
    ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    state = _project(ledger)

    entry = build_capability_inventory(state)[0]

    assert entry.state == "stale"
    assert entry.support is not None
    assert entry.support.expires_at == expired_at
    assert state.get_stale_facts()[0].id == fact.id


def test_provider_reported_state_derives_from_provider_reported_fact_value():
    ledger = EventLedger()
    ledger.append(
        "fact.observed",
        "ws",
        {"fact": to_plain(_verification_fact("weather_lookup", "provider_reported"))},
    )
    state = _project(ledger)

    assert build_capability_inventory(state)[0].state == "provider_reported"


def test_capability_inventory_ordering_is_deterministic():
    ledger = EventLedger()
    ledger.append("tool.registered", "ws", {"tool": to_plain(_tool("z_capability"))})
    ledger.append("tool_need.created", "ws", {"tool_need": to_plain(_need("a_capability"))})
    ledger.append(
        "fact.observed",
        "ws",
        {"fact": to_plain(_verification_fact("m_capability"))},
    )
    state = _project(ledger)

    assert [entry.capability for entry in build_capability_inventory(state)] == [
        "a_capability",
        "m_capability",
        "z_capability",
    ]


def test_capability_status_cli_is_read_only_json_and_avoids_runtime(monkeypatch, tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed-local.sqlite"
    ledger = seed_local.SQLiteEventLedger(db_path)
    try:
        ledger.append("tool.registered", "local", {"tool": to_plain(_tool("web_search"))})
        before = len(ledger.list_events("local"))
    finally:
        ledger.close()

    monkeypatch.setattr(
        seed_local,
        "build_local_app",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("Runtime path used")),
    )

    assert seed_local.main(["--db", str(db_path), "--capability-status"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output[0]["capability"] == "web_search"
    assert output[0]["state"] == "unverified"
    ledger = seed_local.SQLiteEventLedger(db_path)
    try:
        assert len(ledger.list_events("local")) == before
    finally:
        ledger.close()
