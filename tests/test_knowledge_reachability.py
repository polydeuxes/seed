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


def test_reachability_builds_state_once_for_multi_candidate_audit(monkeypatch):
    import seed_runtime.knowledge_reachability as kr

    calls = 0
    original_project = kr.StateProjector.project

    def counted_project(self, workspace_id):
        nonlocal calls
        calls += 1
        return original_project(self, workspace_id)

    monkeypatch.setattr(kr.StateProjector, "project", counted_project)
    ledger = EventLedger()
    for idx in range(3):
        ledger.append(
            "fact.observed",
            "w",
            {"fact": _fact(f"fact_{idx}", f"node{idx}", "mentions", f"token{idx}")},
        )

    rows = build_knowledge_reachability_audit(ledger, "w", limit=10)

    assert len(rows) > 1
    assert calls == 1


def test_reachability_default_candidate_evaluation_is_capped():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(10):
        ledger.append("operator.note", "w", {"text": f"candidate_token_{idx}"})

    result = build_knowledge_reachability_audit_result(ledger, "w", limit=3)

    assert result.metadata.candidates["evaluated"] == 3
    assert result.metadata.candidates["skipped"] > 0
    assert result.metadata.truncated is True
    assert result.metadata.reason == "limit"


def test_reachability_all_disables_candidate_cap():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(10):
        ledger.append("operator.note", "w", {"text": f"candidate_token_{idx}"})

    result = build_knowledge_reachability_audit_result(
        ledger, "w", limit=3, all_candidates=True
    )

    assert (
        result.metadata.candidates["evaluated"]
        == result.metadata.candidates["discovered"]
    )
    assert result.metadata.truncated is False


def test_reachability_json_includes_timing_metadata_and_valid_json():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    ledger.append(
        "fact.observed", "w", {"fact": _fact("fact_1", "node115", "up", True)}
    )

    result = build_knowledge_reachability_audit_result(ledger, "w", subject="node115")
    encoded = json.dumps(knowledge_reachability_json(result.rows, result.metadata))
    decoded = json.loads(encoded)

    assert "metadata" in decoded
    assert "timing" in decoded["metadata"]
    assert "load state/cache" in decoded["metadata"]["timing"]
    assert decoded["metadata"]["candidates"]["evaluated"] == 1


def test_reachability_progress_callback_keeps_json_payload_clean():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(3):
        ledger.append("operator.note", "w", {"text": f"candidate_token_{idx}"})
    progress_messages = []

    result = build_knowledge_reachability_audit_result(
        ledger,
        "w",
        limit=3,
        progress=progress_messages.append,
        progress_interval_seconds=-1,
    )
    encoded = json.dumps(knowledge_reachability_json(result.rows, result.metadata))

    assert progress_messages
    assert "evaluated" in progress_messages[0]
    assert json.loads(encoded)["metadata"]["candidates"]["evaluated"] == 3


def test_reachability_max_seconds_marks_truncated_results():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(5):
        ledger.append("operator.note", "w", {"text": f"candidate_token_{idx}"})

    result = build_knowledge_reachability_audit_result(
        ledger, "w", limit=5, max_seconds=0
    )

    assert result.metadata.truncated is True
    assert result.metadata.reason == "max_seconds"
    assert result.metadata.candidates["evaluated"] == 0
    assert result.metadata.candidates["skipped"] >= 5


def test_reachability_observability_records_required_metadata(tmp_path):
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "runtime-note.md").write_text("runtime note\n")
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "seed_runtime" / "state_views.py").write_text("# symbol\n")
    ledger = EventLedger()
    ledger.append("operator.note", "w", {"text": "event_payload_candidate"})
    messages = []

    result = build_knowledge_reachability_audit_result(
        ledger,
        "w",
        repo_root=tmp_path,
        limit=2,
        progress=messages.append,
        progress_interval_seconds=-1,
    )
    payload = knowledge_reachability_json(result.rows, result.metadata)

    for phase in (
        "load_state",
        "discover_candidates",
        "build_indexes",
        "evaluate",
        "render",
        "total",
    ):
        assert phase in payload["metadata"]["timings"]
    assert payload["metadata"]["candidate_counts"]["capped"] == 2
    assert payload["metadata"]["candidate_sources"]["default seeds"] > 0
    assert payload["metadata"]["candidate_sources"]["event payloads"] > 0
    assert payload["metadata"]["candidate_sources"]["docs/"] > 0
    assert payload["metadata"]["candidate_sources"]["seed_runtime/"] > 0
    assert "event payloads scanned" in payload["metadata"]["scan_counts"]
    assert payload["metadata"]["cache"]["state"] in {"hit", "miss"}
    assert messages.index(
        "[reachability] start load_state state_cache=miss evaluated=0"
    ) < next(
        idx
        for idx, msg in enumerate(messages)
        if msg.startswith("[reachability] end load_state")
    )
    assert any(msg.startswith("[reachability] progress evaluate") for msg in messages)
    assert json.loads(json.dumps(payload))["metadata"]["candidate_sources"]


def test_reachability_hot_loop_counters_do_not_scale_builders_with_candidates():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(25):
        ledger.append("operator.note", "w", {"text": f"candidate_token_{idx}"})
    for idx in range(10):
        ledger.append(
            "fact.observed",
            "w",
            {
                "fact": _fact(
                    f"fact_{idx}",
                    f"module{idx}",
                    "defines",
                    f"module{idx}.Symbol{idx}",
                    {"path": f"seed_runtime/module{idx}.py"},
                )
            },
        )

    result = build_knowledge_reachability_audit_result(ledger, "w", limit=20)
    counters = result.metadata.algorithmic_counters

    assert counters is not None
    assert counters["source_navigation_build_calls"] == 0
    assert counters["source_navigation_query_calls"] == 0
    assert counters["orientation_build_calls"] == 1
    assert counters["fact_support_index_build_calls"] == 1
    assert counters["read_model_build_calls"] == 1
    assert counters["fact_supports_scanned"] < counters["candidates_evaluated"] * 10
    assert counters["normalizations"] <= counters["candidates_evaluated"] * 4


def test_reachability_scale_uses_indexed_evaluation_for_large_candidate_set():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(100_000):
        ledger.append("operator.note", "w", {"text": f"scale_candidate_{idx}"})
    for idx in range(1_000):
        ledger.append(
            "fact.observed",
            "w",
            {
                "fact": _fact(
                    f"scale_fact_{idx}",
                    f"scale_module_{idx}",
                    "defines" if idx % 2 == 0 else "imports",
                    f"scale_module_{idx}.ScaleSymbol{idx}",
                    {"path": f"seed_runtime/scale_module_{idx}.py"},
                )
            },
        )

    result = build_knowledge_reachability_audit_result(
        ledger, "w", limit=100_000, max_seconds=None
    )
    counters = result.metadata.algorithmic_counters

    assert counters is not None
    assert counters["raw_candidates_discovered"] >= 100_000
    assert counters["candidates_evaluated"] >= 100_000
    assert counters["source_navigation_build_calls"] == 0
    assert counters["source_navigation_query_calls"] == 0
    assert counters["orientation_build_calls"] == 1
    assert counters["fact_support_index_build_calls"] == 1
    assert counters["source_navigation_rows_scanned"] == 1_000
    assert counters["membership_checks"] <= counters["candidates_evaluated"] * 5
