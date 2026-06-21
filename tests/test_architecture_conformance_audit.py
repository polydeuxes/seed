import json

from scripts import seed_local
from seed_runtime.architecture_conformance_audit import (
    ArchitectureEvidence,
    OperationalEvidence,
    _finding,
    build_architecture_conformance_audit,
    format_architecture_conformance_audit,
)
from seed_runtime.events import EventLedger


def test_architecture_conformance_audit_renders(capsys):
    assert seed_local.main(["--architecture-conformance-audit"]) == 0
    out = capsys.readouterr().out
    assert "Architecture Conformance Audit" in out
    assert "Findings:" in out
    assert "Architecture evidence:" in out
    assert "Operational evidence:" in out


def test_architecture_conformance_audit_json_valid(capsys):
    assert seed_local.main(["--architecture-conformance-audit", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "findings" in data
    assert "summary" in data
    assert data["summary"]["read_only"] is True


def test_aligned_findings_can_be_reported():
    finding = _finding(
        "event",
        (ArchitectureEvidence("event", "docs/architecture.md", "architecture reference mentions event"),),
        (OperationalEvidence("event", "operational_graph", "node event:x", "high"),),
    )
    assert finding.classification == "aligned"
    assert finding.architecture_evidence
    assert finding.operational_evidence


def test_drift_findings_can_be_reported():
    finding = _finding(
        "projection",
        (ArchitectureEvidence("projection", "docs/architecture.md", "architecture says projection creates view"),),
        (OperationalEvidence("projection", "operational_graph", "projection relationship carrier observed", "high"),),
    )
    assert finding.classification == "drift"


def test_underspecified_findings_can_be_reported():
    finding = _finding(
        "surface",
        (),
        (OperationalEvidence("surface", "operational_graph", "node surface:x", "high"),),
    )
    assert finding.classification == "underspecified"


def test_emergent_structure_findings_can_be_reported():
    finding = _finding(
        "consumer",
        (),
        (
            OperationalEvidence("consumer", "operational_graph", "relationship one", "high"),
            OperationalEvidence("consumer", "operational_graph", "relationship two", "high"),
        ),
    )
    assert finding.classification == "emergent_structure"


def test_unknown_findings_can_be_reported():
    finding = _finding(
        "authorization",
        (ArchitectureEvidence("authorization", "docs/architecture.md", "architecture reference mentions authorization"),),
        (OperationalEvidence("authorization", "operational_graph", "indirect relationship", "low"),),
    )
    assert finding.classification == "unknown"


def test_architecture_and_operational_evidence_are_shown():
    finding = _finding(
        "event",
        (ArchitectureEvidence("event", "docs/architecture.md", "architecture reference mentions event"),),
        (OperationalEvidence("event", "operational_graph", "node event:x", "high"),),
    )
    output = format_architecture_conformance_audit(
        build_architecture_conformance_audit(architecture_evidence=finding.architecture_evidence)
    )
    assert "Architecture evidence:" in output
    assert "Operational evidence:" in output


def test_architecture_conformance_empty_state_is_sane(tmp_path):
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "scripts").mkdir()
    audit = build_architecture_conformance_audit(tmp_path)
    assert audit.findings == ()
    assert "No architecture or operational evidence" in format_architecture_conformance_audit(audit)


def test_architecture_conformance_does_not_write_event_ledger_or_mutate_cluster():
    ledger = EventLedger()
    before = ledger.list_events()
    audit = build_architecture_conformance_audit()
    after = ledger.list_events()
    assert before == after == []
    assert audit.metadata["writes_event_ledger"] is False
    assert audit.metadata["mutates_cluster"] is False
    assert audit.metadata["records_diagnostics"] is False
