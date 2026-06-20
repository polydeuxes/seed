from datetime import datetime, timezone
import json

from seed_runtime.events import EventLedger
from seed_runtime.knowledge_reachability import (
    build_knowledge_reachability_audit,
    format_knowledge_reachability_table,
    knowledge_reachability_json,
)


def _fact(fid, subject, predicate, value, dimensions=None):
    return {
        "id": fid,
        "subject_id": subject,
        "predicate": predicate,
        "value": value,
        "dimensions": dimensions or {},
        "evidence_ids": [],
        "source_type": "discovery",
        "confidence": 0.9,
        "observed_at": datetime(2026, 1, 1, tzinfo=timezone.utc).isoformat(),
    }


def test_reachability_table_and_json_include_stage_columns():
    ledger = EventLedger()
    ledger.append(
        "fact.observed", "w", {"fact": _fact("fact_1", "node115", "up", True)}
    )

    rows = build_knowledge_reachability_audit(ledger, "w", subject="node115")

    assert rows[0].preserved is True
    assert rows[0].projected is True
    assert rows[0].read_model is True
    assert rows[0].rendered is True
    table = format_knowledge_reachability_table(rows)
    assert "Family" in table
    assert "First Loss" in table
    payload = knowledge_reachability_json(rows)
    assert payload[0]["candidate"] == "node115"


def test_reachability_detects_first_loss_at_projection_for_preserved_only_concept():
    ledger = EventLedger()
    ledger.append(
        "operator.note",
        "w",
        {"text": "repository concept current work position is preserved only"},
    )

    row = build_knowledge_reachability_audit(
        ledger, "w", subject="current work position"
    )[0]

    assert row.preserved is True
    assert row.projected is False
    assert row.first_loss == "Projected"


def test_reachability_integration_fixture_finds_distinct_loss_stages(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "source-navigation.md").write_text("source navigation\n")
    ledger = EventLedger()
    ledger.append(
        "fact.observed", "w", {"fact": _fact("fact_runtime", "node115", "up", True)}
    )
    ledger.append("operator.note", "w", {"text": "storage topology preserved mention"})
    ledger.append(
        "fact.observed",
        "w",
        {
            "fact": _fact(
                "fact_projected", "projection-cache", "contains", "state build"
            )
        },
    )
    ledger.append(
        "fact.observed",
        "w",
        {
            "fact": _fact(
                "fact_symbol",
                "seed_runtime.source_navigation",
                "defines",
                "seed_runtime.source_navigation.build_source_navigation",
                {"path": "seed_runtime/source_navigation.py"},
            )
        },
    )

    rows = build_knowledge_reachability_audit(ledger, "w", repo_root=tmp_path)
    by_candidate = {row.candidate: row for row in rows}

    assert by_candidate["node115"].first_loss == "none"
    assert by_candidate["storage topology"].first_loss == "Projected"
    assert by_candidate["state build"].projected is True
    assert by_candidate["source navigation"].family == "repository"
    assert any(
        row.read_model for row in rows if "build_source_navigation" in row.candidate
    )
