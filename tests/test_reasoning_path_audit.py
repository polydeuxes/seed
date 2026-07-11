import importlib.util
import json
import sys
from pathlib import Path

from seed_runtime.events import SQLiteEventLedger
from seed_runtime.state import StateProjector

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "seed_local.py"


def load_seed_local():
    spec = importlib.util.spec_from_file_location(
        "seed_local_reasoning_path", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def ingest(seed_local, db_path, *observations):
    argv = ["--db", str(db_path), "--quiet-output"]
    for subject, predicate, value in observations:
        argv.extend(["--observe", subject, predicate, value])
    assert seed_local.main(argv) == 0


def test_reasoning_path_renders_evidence_conclusions_consumers_and_story(
    tmp_path, capsys
):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db),
                "--reasoning-path",
                "capability",
                "listener_process_inventory",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out

    assert "Reasoning Path" in output
    assert "Observed Evidence:" in output
    assert "ownership_discrepancies" in output
    assert "Intermediate Conclusions:" in output
    assert "ownership attribution incomplete" in output
    assert "Derived Conclusions:" in output
    assert "listener_process_inventory capability need" in output
    assert "Consumers:" in output
    assert "capability_needs" in output
    assert "pressure_audit" in output
    assert "Story Impact:" in output
    assert "operational_story" in output


def test_reasoning_path_json_is_valid_and_read_only(tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )
    ledger = SQLiteEventLedger(db)
    try:
        before = len(ledger.list_events("default"))
    finally:
        ledger.close()
    capsys.readouterr()

    assert (
        seed_local.main(
            [
                "--db",
                str(db),
                "--reasoning-path",
                "ownership",
                "owner_not_observed",
                "--json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    ledger = SQLiteEventLedger(db)
    try:
        after = len(ledger.list_events("default"))
    finally:
        ledger.close()

    assert payload["subject"] == "owner_not_observed"
    assert payload["evidence"]
    assert payload["intermediate_conclusions"]
    assert payload["derived_conclusions"]
    assert payload["consumers"]
    assert payload["story_impact"]
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_cluster"] is False
    assert after == before


def test_reasoning_path_preserves_conclusions_and_lineage_at_compatibility_handoff(
    tmp_path, capsys
):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(
        seed_local,
        db,
        ("api", "prometheus_target", "127.0.0.1:9100"),
        ("node-a", "listening_socket", "tcp 127.0.0.1:9100"),
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            [
                "--db",
                str(db),
                "--reasoning-path",
                "capability",
                "listener_process_inventory",
                "--json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["intermediate_conclusions"]
    assert payload["derived_conclusions"]
    assert payload["evidence"]
    assert payload["consumers"]
    assert payload["story_impact"]
    assert all("evidence" not in item for item in payload["derived_conclusions"])
    assert all("consumers" not in item for item in payload["derived_conclusions"])
    assert all("story_impact" not in item for item in payload["derived_conclusions"])


def test_reasoning_path_projects_supporting_evidence_at_compatibility_handoff():
    from seed_runtime.reasoning_path_audit import (
        _DerivationLineagePayload,
        _DerivationSupportingEvidencePayload,
        _DerivedConclusionPayload,
        _reasoning_path_from_payloads,
    )

    supporting_evidence = [{"surface": "ownership_discrepancies", "finding": "x"}]
    audit = _reasoning_path_from_payloads(
        "capability",
        "listener_process_inventory",
        conclusions=_DerivedConclusionPayload(
            intermediate_conclusions=[{"conclusion": "ownership attribution incomplete"}],
            derived_conclusions=[
                {"conclusion": "listener_process_inventory capability need"}
            ],
        ),
        supporting_evidence=_DerivationSupportingEvidencePayload(
            evidence=supporting_evidence
        ),
        lineage=_DerivationLineagePayload(
            consumers=[{"surface": "capability_needs"}],
            story_impact=[{"surface": "operational_story"}],
            unknowns=[],
        ),
    )

    assert audit.evidence == supporting_evidence
    assert audit.consumers == [{"surface": "capability_needs"}]
    assert audit.story_impact == [{"surface": "operational_story"}]
    assert audit.to_json_dict()["evidence"] == supporting_evidence


def test_reasoning_path_supporting_evidence_payload_owns_source_row_projection():
    from types import SimpleNamespace

    from seed_runtime.reasoning_path_audit import (
        _DerivationSupportingEvidencePayload,
        _reasoning_path_supporting_evidence_payload,
    )

    payload = _reasoning_path_supporting_evidence_payload(
        [
            SimpleNamespace(
                subject="api",
                conflict="owner_not_observed",
                reason="socket has no owner observation",
                evidence_count=2,
            ),
            SimpleNamespace(
                subject="worker",
                conflict="",
                reason="candidate observed from relationship evidence",
                evidence_count=1,
            ),
        ]
    )

    assert isinstance(payload, _DerivationSupportingEvidencePayload)
    assert payload.evidence == [
        {
            "surface": "ownership_discrepancies",
            "subject": "api",
            "finding": "owner_not_observed",
            "reason": "socket has no owner observation",
            "evidence_count": 2,
        },
        {
            "surface": "ownership_discrepancies",
            "subject": "worker",
            "finding": "ownership_candidate",
            "reason": "candidate observed from relationship evidence",
            "evidence_count": 1,
        },
    ]


def test_reasoning_path_unknown_and_empty_state_are_explicit(tmp_path, capsys):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db),
                "--reasoning-path",
                "capability",
                "not_a_known_conclusion",
                "--json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["evidence"] == []
    assert payload["derived_conclusions"] == []
    assert payload["unknowns"] == [
        {"area": "derivation", "reason": "no derivation evidence currently available"}
    ]
    assert payload["boundary"]["records_facts"] is False


def test_reasoning_path_does_not_mutate_projected_state(tmp_path):
    seed_local = load_seed_local()
    db = tmp_path / "seed.sqlite"
    ingest(seed_local, db, ("api", "prometheus_target", "127.0.0.1:9100"))
    ledger = SQLiteEventLedger(db)
    try:
        before = StateProjector(ledger).project("default").facts.copy()
    finally:
        ledger.close()

    assert (
        seed_local.main(["--db", str(db), "--reasoning-path", "pressure", "capability"])
        == 0
    )

    ledger = SQLiteEventLedger(db)
    try:
        after = StateProjector(ledger).project("default").facts.copy()
    finally:
        ledger.close()
    assert after == before


def test_reasoning_path_registered_in_visibility_contracts():
    from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
    from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit

    entry = next(item for item in DIAGNOSTIC_INVENTORY if item.name == "reasoning_path")
    assert entry.cli_flags == ("--reasoning-path",)
    assert entry.supports_json
    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster

    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "reasoning_path"
    ]
    assert rows
    assert all(row.status == "consistent" for row in rows)


def test_reasoning_path_lineage_owns_typed_unknown_before_public_handoff():
    from seed_runtime.reasoning_path_audit import (
        _DerivationLineagePayload,
        _DerivationSupportingEvidencePayload,
        _DerivedConclusionPayload,
        _reasoning_path_from_payloads,
    )
    from seed_runtime.typed_unknowns import preserve_typed_unknown

    typed_unknown = preserve_typed_unknown(
        unknown_type="Evidence Gap",
        area="derivation",
        reason="no derivation evidence currently available",
    )
    lineage = _DerivationLineagePayload(
        consumers=[], story_impact=[], unknowns=[typed_unknown]
    )

    audit = _reasoning_path_from_payloads(
        "capability",
        "not_a_known_conclusion",
        conclusions=_DerivedConclusionPayload([], []),
        supporting_evidence=_DerivationSupportingEvidencePayload([]),
        lineage=lineage,
    )

    assert lineage.unknowns == [typed_unknown]
    assert lineage.unknowns[0].unknown_type == "Evidence Gap"
    assert audit.unknowns == [
        {"area": "derivation", "reason": "no derivation evidence currently available"}
    ]
