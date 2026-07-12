import json

from scripts import seed_local
from seed_runtime.emitter_attribution_audit import (
    ClassifiedEvidence,
    build_emitter_attribution_audit,
    emitter_attribution_audit_json,
    format_emitter_attribution_audit,
    _classify_unknown_emitter_attribution,
    _collect_emitter_attribution_implementation_evidence,
    _known_emitter_attributed_rows,
    _unknown_emitter_attribution_item,
    UnknownEmitterAttribution,
)
from seed_runtime.emitter_consumer_audit import EmitterConsumerItem
from seed_runtime.events import EventLedger


def test_emitter_attribution_audit_renders(capsys):
    assert seed_local.main(["--emitter-attribution-audit"]) == 0
    out = capsys.readouterr().out
    assert "Emitter Attribution Audit" in out
    assert "Reason:" in out


def test_emitter_attribution_audit_json_valid(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "items" in data
    assert "summary" in data
    assert data["items"][0]["event"]


def test_attributed_emitters_are_reported():
    audit = build_emitter_attribution_audit()
    assert any(
        item.status == "attributed" and item.emitter != "unknown"
        for item in audit.items
    )


def test_known_emitter_attributed_row_construction_preserves_base_fields():
    base_item = EmitterConsumerItem(
        emitter="alpha",
        emits=("alpha.created",),
        consumers=("projection builders", "diagnostics and audits"),
        status="consumed",
        evidence=("seed_runtime/alpha.py:4", ""),
        emission_type="domain_emission",
    )

    rows = _known_emitter_attributed_rows(base_item)

    assert len(rows) == 1
    row = rows[0]
    assert row.event == "alpha.created"
    assert row.emitter == "alpha"
    assert row.status == "attributed"
    assert (
        row.reason
        == "direct event emission evidence is attributed by the emitter/consumer audit"
    )
    assert row.consumers == ("projection builders", "diagnostics and audits")
    assert row.evidence == ("seed_runtime/alpha.py:4",)
    assert row.emission_type == "domain_emission"
    assert row.confidence == "high"
    assert row.attribution_evidence == (
        ClassifiedEvidence("direct_emitter", "seed_runtime/alpha.py:4"),
    )
    assert row.supporting_references == ()


def test_known_emitter_attributed_rows_preserve_public_outputs_and_read_only_boundary(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "alpha.py").write_text(
        'def emit(self):\n'
        '    ledger.append("alpha.created", "s", {})\n',
        encoding="utf-8",
    )
    (runtime / "state.py").write_text(
        'def consume(event):\n'
        '    return event.kind == "alpha.created"\n',
        encoding="utf-8",
    )
    ledger = EventLedger()
    before = ledger.list_events()

    audit = build_emitter_attribution_audit(tmp_path)

    assert before == ledger.list_events() == []
    assert audit.summary == {
        "items_scanned": 1,
        "attributed": 1,
        "dynamic": 0,
        "indirect": 0,
        "discovery_gap": 0,
        "missing": 0,
        "unknown": 0,
    }
    data = emitter_attribution_audit_json(audit)
    item = data["items"][0]
    assert item["event"] == "alpha.created"
    assert item["emitter"] == "alpha"
    assert item["status"] == "attributed"
    assert item["reason"] == (
        "direct event emission evidence is attributed by the emitter/consumer audit"
    )
    assert item["consumers"] == ["projection builders"]
    assert item["evidence"] == ["seed_runtime/alpha.py:2"]
    assert item["emission_type"] == "domain_emission"
    assert item["confidence"] == "high"
    assert item["attribution_evidence"] == [
        {"category": "direct_emitter", "location": "seed_runtime/alpha.py:2"}
    ]
    rendered = format_emitter_attribution_audit(audit)
    assert "Event: alpha.created" in rendered
    assert "Emitter: alpha" in rendered
    assert "Status: attributed" in rendered
    assert (
        "Reason: direct event emission evidence is attributed by the emitter/consumer audit"
        in rendered
    )
    assert "Confidence: high" in rendered
    assert "direct_emitter: seed_runtime/alpha.py:2" in rendered


def test_unknown_emitter_attribution_item_construction_preserves_recovered_fields():
    base_item = EmitterConsumerItem(
        emitter="unknown",
        emits=("workflow.done",),
        consumers=("projection builders", "diagnostics and audits"),
        status="consumed",
        evidence=("seed_runtime/state.py:2",),
        emission_type="domain_emission",
    )
    attribution = UnknownEmitterAttribution(
        status="indirect",
        reason="classification reason from recovered artifact",
        emitter="unknown",
        confidence="medium",
        attribution_evidence=(
            ClassifiedEvidence("indirect_emitter", "seed_runtime/workflow.py:3"),
        ),
        supporting_references=(
            ClassifiedEvidence("event_constructor", "seed_runtime/events.py:7"),
            ClassifiedEvidence("diagnostic_reference", "seed_runtime/audit.py:11"),
        ),
    )

    row = _unknown_emitter_attribution_item(base_item, "workflow.done", attribution)

    assert row.event == "workflow.done"
    assert row.emitter == "unknown"
    assert row.status == "indirect"
    assert row.reason == "classification reason from recovered artifact"
    assert row.consumers == ("projection builders", "diagnostics and audits")
    assert row.evidence == (
        "seed_runtime/workflow.py:3",
        "seed_runtime/events.py:7",
        "seed_runtime/audit.py:11",
    )
    assert row.emission_type == "domain_emission"
    assert row.confidence == "medium"
    assert row.attribution_evidence == (
        ClassifiedEvidence("indirect_emitter", "seed_runtime/workflow.py:3"),
    )
    assert row.supporting_references == (
        ClassifiedEvidence("event_constructor", "seed_runtime/events.py:7"),
        ClassifiedEvidence("diagnostic_reference", "seed_runtime/audit.py:11"),
    )

def test_unknown_emitters_are_reported():
    audit = build_emitter_attribution_audit()
    assert any(item.emitter == "unknown" for item in audit.items)


def test_discovery_gap_explanations_appear_for_consumed_literal_without_emit(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "gap.event"\n'
    )
    audit = build_emitter_attribution_audit(tmp_path)
    item = next(item for item in audit.items if item.event == "gap.event")
    assert item.status == "discovery_gap"
    assert "no direct emit call" in item.reason


def test_workflow_events_appear_when_implementation_evidence_exists(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "pending_action.completed"\n'
    )
    (runtime / "pending_actions.py").write_text(
        'from seed_runtime.events import Event\ndef helper(kind):\n    return Event(kind=kind, subject="s", predicate="p", object="o")\n'
    )
    audit = build_emitter_attribution_audit(tmp_path)
    item = next(
        item for item in audit.items if item.event == "pending_action.completed"
    )
    assert item.status == "dynamic"
    assert "workflow event" in item.reason


def test_empty_state_builder_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    audit = build_emitter_attribution_audit(tmp_path)
    assert audit.items == ()
    assert audit.summary["items_scanned"] == 0


def test_emitter_attribution_audit_does_not_write_event_ledger_or_mutate_cluster():
    ledger = EventLedger()
    before = ledger.list_events()
    audit = build_emitter_attribution_audit()
    after = ledger.list_events()
    assert before == after == []
    assert audit.metadata["discovery"]


def test_attribution_excludes_rendered_messages_from_default_counts():
    audit = build_emitter_attribution_audit()
    events = {item.event for item in audit.items}
    assert (
        "No deterministic related material found in projected read models."
        not in events
    )
    assert "No supportable lexical overlap was found." not in events
    assert (
        "Guardrail: diagnostic only; no ownership facts are inferred or written."
        not in events
    )
    assert all(item.emission_type == "domain_emission" for item in audit.items)
    assert audit.summary["attributed"] == sum(
        item.status == "attributed" and item.emission_type == "domain_emission"
        for item in audit.items
    )


def test_action_plan_events_remain_attributed():
    audit = build_emitter_attribution_audit()
    item = next(item for item in audit.items if item.event == "action_plan.created")
    assert item.status == "attributed"
    assert item.emitter == "action_plan"
    assert item.emission_type == "domain_emission"


def test_attribution_include_rendered_classifies_guardrail_messages(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--include-rendered"]) == 0
    out = capsys.readouterr().out
    assert (
        "Guardrail: diagnostic only; no ownership facts are inferred or written." in out
    )
    assert "Emission type: guardrail_text" in out


def test_attribution_json_reports_domain_classification(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert {item["emission_type"] for item in data["items"]} == {"domain_emission"}


def test_unknown_emitter_attribution_rows_preserve_public_outputs_and_read_only_boundary(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind in {"gap.event", "aaa.event"}\n',
        encoding="utf-8",
    )
    (runtime / "references.py").write_text(
        'REFERENCE = "gap.event"\n',
        encoding="utf-8",
    )
    ledger = EventLedger()
    before = ledger.list_events()

    audit = build_emitter_attribution_audit(tmp_path)

    assert before == ledger.list_events() == []
    assert audit.summary == {
        "items_scanned": 2,
        "attributed": 0,
        "dynamic": 0,
        "indirect": 0,
        "discovery_gap": 2,
        "missing": 0,
        "unknown": 0,
    }
    assert [item.event for item in audit.items] == ["aaa.event", "gap.event"]
    assert [item.status for item in audit.items] == ["discovery_gap", "discovery_gap"]

    data = emitter_attribution_audit_json(audit)
    gap = data["items"][1]
    assert gap["event"] == "gap.event"
    assert gap["emitter"] == "unknown"
    assert gap["status"] == "discovery_gap"
    assert gap["reason"] == (
        "event literal is present in implementation evidence and consumed, but no direct emit call is attributed by current discovery"
    )
    assert gap["consumers"] == ["projection builders"]
    assert gap["evidence"] == [
        "seed_runtime/state.py:2",
        "seed_runtime/references.py:1",
    ]
    assert gap["emission_type"] == "domain_emission"
    assert gap["confidence"] == "low"
    assert gap["attribution_evidence"] == []
    assert gap["supporting_references"] == [
        {"category": "projection_consumer", "location": "seed_runtime/state.py:2"},
        {"category": "string_reference", "location": "seed_runtime/references.py:1"},
    ]

    rendered = format_emitter_attribution_audit(audit)
    assert "Items scanned: 2" in rendered
    assert "Discovery Gap: 2" in rendered
    assert "Missing: 0" in rendered
    assert "Event: gap.event" in rendered
    assert "Emitter: unknown" in rendered
    assert "Status: discovery_gap" in rendered
    assert "Confidence: low" in rendered
    assert "Supporting references: 2" in rendered

def test_direct_append_literal_attributes_unknown_emitter_candidate(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "workflow.py").write_text(
        'def emit(self):\n    self._require_ledger().append("workflow.done", "s", {})\n',
        encoding="utf-8",
    )
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "workflow.done"\n',
        encoding="utf-8",
    )

    audit = build_emitter_attribution_audit(tmp_path)
    item = next(item for item in audit.items if item.event == "workflow.done")

    assert item.status == "attributed"
    assert item.confidence == "high"
    assert item.emitter == "workflow"
    assert item.attribution_evidence[0].category == "direct_emitter"


def test_dynamic_construction_does_not_override_direct_emitter_evidence(tmp_path):
    runtime = tmp_path / "seed_runtime"
    scripts = tmp_path / "scripts"
    runtime.mkdir()
    scripts.mkdir()
    (runtime / "action_plans.py").write_text(
        "from seed_runtime.events import Event\n"
        "def emit(self, kind):\n"
        '    Event(kind=kind, subject="s", predicate="p", object="o")\n'
        '    self._require_ledger().append("action_plan.accepted", "s", {})\n',
        encoding="utf-8",
    )
    (runtime / "state.py").write_text(
        'def consume(event):\n    return event.kind == "action_plan.accepted"\n',
        encoding="utf-8",
    )

    audit = build_emitter_attribution_audit(tmp_path)
    item = next(item for item in audit.items if item.event == "action_plan.accepted")

    assert item.status == "attributed"
    assert item.confidence == "high"
    assert any(e.category == "direct_emitter" for e in item.attribution_evidence)
    assert any(e.category == "event_constructor" for e in item.supporting_references)


def test_action_plan_lifecycle_events_are_attributed_from_direct_evidence():
    audit = build_emitter_attribution_audit()

    for event in (
        "action_plan.accepted",
        "action_plan.approved",
        "action_plan.rejected",
        "action_plan.superseded",
    ):
        item = next(item for item in audit.items if item.event == event)
        assert item.status == "attributed"
        assert item.emitter == "action_plan"
        assert item.confidence == "high"
        assert any(e.category == "direct_emitter" for e in item.attribution_evidence)
        assert item.supporting_references


def test_attribution_json_distinguishes_driving_evidence_from_references(capsys):
    assert seed_local.main(["--emitter-attribution-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    item = next(i for i in data["items"] if i["event"] == "action_plan.accepted")

    assert item["confidence"] == "high"
    assert item["attribution_evidence"]
    assert item["attribution_evidence"][0]["category"] == "direct_emitter"
    assert "supporting_references" in item



def test_unknown_emitter_classification_preserves_returned_fields():
    direct = (ClassifiedEvidence("direct_emitter", "seed_runtime/workflow.py:2"),)
    indirect = (ClassifiedEvidence("indirect_emitter", "seed_runtime/pending_actions.py:4"),)
    diagnostic = (ClassifiedEvidence("diagnostic_reference", "seed_runtime/audit.py:5"),)
    string_ref = (ClassifiedEvidence("string_reference", "seed_runtime/other.py:6"),)
    dynamic = (ClassifiedEvidence("event_constructor", "seed_runtime/events.py:7"),)

    attributed = _classify_unknown_emitter_attribution("workflow.done", direct, dynamic)
    assert attributed.status == "attributed"
    assert attributed.reason.startswith("direct emitter evidence")
    assert attributed.emitter == "workflow"
    assert attributed.confidence == "high"
    assert attributed.attribution_evidence == direct
    assert attributed.supporting_references == dynamic

    workflow_dynamic_with_refs = _classify_unknown_emitter_attribution(
        "pending_action.completed", diagnostic, dynamic
    )
    assert workflow_dynamic_with_refs.status == "dynamic"
    assert workflow_dynamic_with_refs.reason.startswith("workflow event")
    assert workflow_dynamic_with_refs.emitter == "unknown"
    assert workflow_dynamic_with_refs.confidence == "low"
    assert workflow_dynamic_with_refs.attribution_evidence == dynamic
    assert workflow_dynamic_with_refs.supporting_references == diagnostic

    indirect_result = _classify_unknown_emitter_attribution(
        "custom.event", indirect + string_ref, dynamic
    )
    assert indirect_result.status == "indirect"
    assert indirect_result.reason.startswith("event is visible through workflow helper")
    assert indirect_result.emitter == "unknown"
    assert indirect_result.confidence == "medium"
    assert indirect_result.attribution_evidence == indirect
    assert indirect_result.supporting_references == string_ref + dynamic

    discovery_gap = _classify_unknown_emitter_attribution("custom.event", string_ref, ())
    assert discovery_gap.status == "discovery_gap"
    assert discovery_gap.reason.startswith("event literal is present")
    assert discovery_gap.emitter == "unknown"
    assert discovery_gap.confidence == "low"
    assert discovery_gap.attribution_evidence == ()
    assert discovery_gap.supporting_references == string_ref

    workflow_dynamic_only = _classify_unknown_emitter_attribution(
        "action_plan.created", (), dynamic
    )
    assert workflow_dynamic_only.status == "dynamic"
    assert workflow_dynamic_only.attribution_evidence == dynamic
    assert workflow_dynamic_only.supporting_references == ()

    missing = _classify_unknown_emitter_attribution("custom.event", (), ())
    assert missing.status == "missing"
    assert missing.reason.startswith("event is consumed")
    assert missing.emitter == "unknown"
    assert missing.confidence == "none"
    assert missing.attribution_evidence == ()
    assert missing.supporting_references == ()



def test_implementation_evidence_collection_preserves_sources_and_ordering(tmp_path):
    runtime = tmp_path / "seed_runtime"
    runtime.mkdir()
    (runtime / "alpha.py").write_text(
        'from seed_runtime.events import Event\n'
        'def dynamic(kind):\n'
        '    Event(kind=kind, subject="s", predicate="p", object="o")\n'
        'def direct(self):\n'
        '    ledger.append("alpha.created", "s", {})\n'
        'def literal(event):\n'
        '    return event.kind == "alpha.created"\n',
        encoding="utf-8",
    )
    (runtime / "zeta.py").write_text(
        'def dynamic_append(self, kind):\n'
        '    self._require_ledger().append(kind, "s", {})\n'
        'def literal():\n'
        '    return "zeta.reference"\n',
        encoding="utf-8",
    )
    evidence = _collect_emitter_attribution_implementation_evidence(tmp_path)

    alpha_refs = evidence.literal_references["alpha.created"]
    assert [(e.category, e.location) for e in alpha_refs] == sorted(
        (e.category, e.location) for e in alpha_refs
    )
    assert ("direct_emitter", "seed_runtime/alpha.py:5") in [
        (e.category, e.location) for e in alpha_refs
    ]
    assert any(e.category == "string_reference" for e in alpha_refs)
    assert evidence.literal_references["zeta.reference"] == (
        ClassifiedEvidence("string_reference", "seed_runtime/zeta.py:4"),
    )
    assert evidence.dynamic_event_construction == tuple(
        sorted(evidence.dynamic_event_construction, key=lambda e: (e.category, e.location))
    )
    assert evidence.dynamic_event_construction == (
        ClassifiedEvidence("event_constructor", "seed_runtime/alpha.py:3"),
        ClassifiedEvidence("event_constructor", "seed_runtime/zeta.py:2"),
    )
