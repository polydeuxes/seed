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
    assert row.first_loss == "projected_loss"


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
    assert by_candidate["storage topology"].first_loss == "projected_loss"
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
        limit=100,
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
    assert payload["metadata"]["candidate_counts"]["used"] <= 100
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
        ledger, "w", limit=100_000, all_candidates=True, max_seconds=None
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


def test_reachability_default_discovery_stops_early_and_reports_raw_seen_used():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(10_000):
        ledger.append("operator.note", "w", {"text": f"synthetic_candidate_{idx}"})

    result = build_knowledge_reachability_audit_result(
        ledger, "w", limit=500, max_seconds=None
    )
    counts = result.metadata.candidate_counts

    assert counts["used"] <= 500
    assert counts["used"] < 10_000
    assert counts["raw_seen"] < 10_000
    assert counts["limit"] == 500


def test_reachability_all_scans_all_synthetic_candidates():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for idx in range(1_000):
        ledger.append("operator.note", "w", {"text": f"all_candidate_{idx}"})

    result = build_knowledge_reachability_audit_result(
        ledger, "w", limit=100, all_candidates=True, max_seconds=None
    )

    assert result.metadata.candidate_counts["evaluated"] >= 1_000
    assert result.metadata.truncated is False


def test_reachability_read_model_substep_timing_appears():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    messages = []
    build_knowledge_reachability_audit_result(
        ledger, "w", subject="node115", progress=messages.append
    )

    for name in (
        "read_model.current_facts",
        "read_model.fact_support",
        "read_model.state_summary",
        "read_model.inquiry_orientation",
    ):
        assert any(msg.startswith(f"[reachability] start {name}") for msg in messages)
        assert any(
            msg.startswith(f"[reachability] end {name}") and "rows=" in msg
            for msg in messages
        )


def test_reachability_read_model_does_not_call_broad_builders(monkeypatch):
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )
    import seed_runtime.knowledge_reachability as kr

    def forbidden(*args, **kwargs):
        raise AssertionError("broad read-model builder called")

    monkeypatch.setattr(kr, "build_fact_view", forbidden, raising=False)
    monkeypatch.setattr(kr, "build_observation_view", forbidden, raising=False)
    monkeypatch.setattr(kr, "state_summary", forbidden, raising=False)

    ledger = EventLedger()
    for idx in range(20):
        ledger.append("operator.note", "w", {"text": f"candidate_token_{idx}"})

    result = build_knowledge_reachability_audit_result(ledger, "w", limit=10)

    assert result.metadata.algorithmic_counters["read_model_build_calls"] == 1


def test_reachability_subject_filter_avoids_broad_repo_scan(tmp_path):
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    (tmp_path / "docs").mkdir()
    (tmp_path / "seed_runtime").mkdir()
    for idx in range(100):
        (tmp_path / "docs" / f"doc_{idx}.md").write_text("content\n")
        (tmp_path / "seed_runtime" / f"module_{idx}.py").write_text("# content\n")

    result = build_knowledge_reachability_audit_result(
        EventLedger(), "w", repo_root=tmp_path, subject="node115"
    )

    assert result.metadata.scan_counts["repo files scanned"] == 0
    assert result.metadata.candidate_counts["evaluated"] == 1


def test_reachability_candidate_kind_classifies_required_examples():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    cases = {
        "Fact": "repository_concept",
        "Observation": "repository_concept",
        "Evidence": "repository_concept",
        "InferenceRule": "repository_concept",
        "CapabilityCatalog": "code_symbol",
        "RelationshipDefinition": "code_symbol",
        "confidence": "schema_field",
        "dimensions": "schema_field",
        "canonical_name": "schema_field",
        "address": "schema_field",
        "amd64": "platform_value",
        "x86_64": "platform_value",
        "vfat": "platform_value",
        "ext4": "platform_value",
        "docker0": "platform_value",
        "eno1": "platform_value",
        "evd_obs_000001": "generated_identifier",
        "fact_obs_000001": "generated_identifier",
        "cf4f3b31-e8c8-48fb-a14c-e8c185050ae6": "generated_identifier",
        "aa:bb:cc:dd:ee:ff": "network_identifier",
        "192.168.1.10": "network_identifier",
        "node.example.internal": "network_identifier",
        "shared storage candidates": "presentation_label",
        "source navigation": "presentation_label",
        "current work position": "presentation_label",
        "continuation": "presentation_label",
    }
    for candidate, expected in cases.items():
        result = build_knowledge_reachability_audit_result(
            EventLedger(), "w", subject=candidate
        )
        assert result.rows[0].candidate_kind == expected


def test_reachability_visibility_only_is_not_none_and_json_includes_kind(monkeypatch):
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )
    import seed_runtime.knowledge_reachability as kr

    monkeypatch.setattr(
        kr,
        "_build_indexes",
        lambda *args, **kwargs: kr._AuditIndexes(
            set(), set(), set(), {"source navigation"}
        ),
    )
    ledger = EventLedger()
    result = build_knowledge_reachability_audit_result(
        ledger, "w", subject="source navigation"
    )
    row = result.rows[0]
    payload = knowledge_reachability_json(result.rows, result.metadata)

    assert row.preserved is False
    assert row.projected is False
    assert row.read_model is False
    assert row.rendered is True
    assert row.first_loss == "visibility_only"
    assert payload["rows"][0]["candidate_kind"] == "presentation_label"


def test_reachability_summary_counts_and_candidate_kind_filtering():
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
    )

    ledger = EventLedger()
    for text in ("Fact", "CapabilityCatalog", "evd_obs_000001", "source navigation"):
        ledger.append("operator.note", "w", {"text": text})

    result = build_knowledge_reachability_audit_result(
        ledger, "w", all_candidates=True, max_seconds=None
    )
    kind_counts = result.metadata.candidate_kind_counts
    loss_counts = result.metadata.loss_stage_counts

    assert kind_counts is not None
    assert kind_counts["repository_concept"] >= 1
    assert kind_counts["code_symbol"] >= 1
    assert kind_counts["generated_identifier"] >= 1
    assert kind_counts["presentation_label"] >= 1
    assert loss_counts is not None
    assert sum(loss_counts.values()) == len(result.rows)

    filtered = build_knowledge_reachability_audit_result(
        ledger,
        "w",
        candidate_kind="presentation_label",
        all_candidates=True,
        max_seconds=None,
    )
    assert filtered.rows
    assert {row.candidate_kind for row in filtered.rows} == {"presentation_label"}


def test_reachability_candidate_admission_helper_preserves_sources_limits_and_read_only(tmp_path):
    from seed_runtime.knowledge_reachability import (
        build_knowledge_reachability_audit_result,
        format_knowledge_reachability_table,
    )

    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "storage-topology.md").write_text("storage topology\n")
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "seed_runtime" / "unique_runtime_module.py").write_text("# cache\n")
    ledger = EventLedger()
    ledger.append("operator.note", "w", {"text": "event_payload_candidate"})
    ledger.append(
        "fact.observed",
        "w",
        {"fact": _fact("f1", "projected-subject", "defines", "ProjectedSymbol", {"path": "seed_runtime/projected.py"})},
    )
    before_events = len(ledger.list_events("w"))

    result = build_knowledge_reachability_audit_result(
        ledger, "w", repo_root=tmp_path, all_candidates=True, max_seconds=None
    )
    payload = knowledge_reachability_json(result.rows, result.metadata)
    table = format_knowledge_reachability_table(result.rows, result.metadata)

    assert result.metadata.candidate_sources["default seeds"] > 0
    assert result.metadata.candidate_sources["event payloads"] > 0
    assert result.metadata.candidate_sources["projected state"] > 0
    assert result.metadata.candidate_sources["source-navigation terms"] > 0
    assert result.metadata.candidate_sources["docs/"] > 0
    assert result.metadata.candidate_sources["seed_runtime/"] > 0
    assert result.metadata.candidate_counts["raw_seen"] >= result.metadata.candidate_counts["used"]
    assert result.metadata.candidate_counts["limit"] == 0
    assert result.metadata.scan_counts["event payloads scanned"] > 0
    assert result.metadata.scan_counts["facts scanned"] > 0
    assert result.metadata.scan_counts["repo files scanned"] > 0
    assert result.metadata.scan_counts["symbols scanned"] > 0
    assert result.metadata.scan_counts["source-navigation terms scanned"] > 0
    assert payload["metadata"]["candidate_counts"]["used"] == result.metadata.candidate_counts["used"]
    assert "Knowledge Reachability Audit" in table
    assert len(ledger.list_events("w")) == before_events

    capped = build_knowledge_reachability_audit_result(
        ledger, "w", repo_root=tmp_path, limit=3, max_seconds=None
    )
    assert capped.metadata.truncated is True
    assert capped.metadata.reason == "limit"

    subject = build_knowledge_reachability_audit_result(
        ledger, "w", repo_root=tmp_path, subject="node115"
    )
    assert subject.metadata.scan_counts["repo files scanned"] == 0
    assert subject.metadata.candidate_counts["evaluated"] == 1


def test_reachability_index_construction_helper_preserves_index_handoff_and_metadata():
    from seed_runtime.knowledge_reachability import (
        _construct_knowledge_reachability_indexes,
        _new_counters,
        _ReachabilityTimer,
        _TokenizationCache,
        _AuditIndexes,
        build_knowledge_reachability_audit_result,
        format_knowledge_reachability_table,
    )
    from seed_runtime.state import StateProjector

    ledger = EventLedger()
    ledger.append("operator.note", "w", {"text": "preserved-only"})
    ledger.append(
        "fact.observed",
        "w",
        {"fact": _fact("f1", "node115", "defines", "IndexedSymbol", {"path": "seed_runtime/indexed.py"})},
    )
    state = StateProjector(ledger).project("w")
    counters = _new_counters()
    timings = {}
    messages = []
    indexes = _construct_knowledge_reachability_indexes(
        ledger.list_events("w"),
        state,
        timer=_ReachabilityTimer(messages.append),
        index_timings=timings,
        counters=counters,
        token_cache=_TokenizationCache(counters),
    )

    assert isinstance(indexes, _AuditIndexes)
    assert "preserved-only" in indexes.preserved_terms
    assert "node115" in indexes.projected_terms
    assert "indexedsymbol" in indexes.read_model_terms
    assert isinstance(indexes.inquiry_terms, set)
    for key in (
        "projected_entities",
        "projected_facts",
        "fact_support",
        "source_navigation.index_from_fact_support",
        "read_model",
        "inquiry_orientation",
    ):
        assert key in timings
    assert counters["state_projection_build_calls"] == 1
    assert counters["entity_projection_build_calls"] == 1
    assert counters["fact_support_index_build_calls"] == 1
    assert counters["read_model_build_calls"] == 1
    assert any(msg.startswith("[reachability] start projected_entities") for msg in messages)

    result = build_knowledge_reachability_audit_result(ledger, "w", subject="node115")
    payload = knowledge_reachability_json(result.rows, result.metadata)
    assert result.rows[0].preserved is True
    assert result.rows[0].projected is True
    assert result.rows[0].read_model is True
    assert "read_model" in payload["metadata"]["indexes"]
    assert "Knowledge Reachability Audit" in format_knowledge_reachability_table(result.rows, result.metadata)
    assert len(ledger.list_events("w")) == 2


def test_reachability_candidate_evaluation_helper_preserves_rows_order_progress_and_timeout():
    from seed_runtime.knowledge_reachability import (
        _AuditIndexes,
        _TokenizationCache,
        _ReachabilityTimer,
        _evaluate_knowledge_reachability_candidates,
        _new_counters,
        build_knowledge_reachability_audit_result,
        format_knowledge_reachability_table,
    )

    counters = _new_counters()
    messages = []
    result = _evaluate_knowledge_reachability_candidates(
        ["alpha", "node115", "source navigation"],
        {"alpha": "repository", "node115": "runtime", "source navigation": "repository"},
        _AuditIndexes({"alpha", "node115"}, {"node115"}, {"node115"}, {"source navigation"}),
        counters,
        _TokenizationCache(counters),
        timer=_ReachabilityTimer(messages.append),
        progress=messages.append,
        progress_interval_seconds=-1,
        max_seconds=None,
    )

    assert [row.candidate for row in result.rows] == ["alpha", "node115", "source navigation"]
    assert result.rows[0].candidate_kind == "unknown"
    assert result.rows[0].first_loss == "projected_loss"
    assert result.rows[1].candidate_kind == "runtime_value"
    assert result.rows[1].first_loss == "orientation_loss"
    assert result.rows[2].candidate_kind == "presentation_label"
    assert result.rows[2].first_loss == "visibility_only"
    assert any(msg.startswith("[reachability] progress evaluate") for msg in messages)

    timed = _evaluate_knowledge_reachability_candidates(
        ["alpha"],
        {"alpha": "repository"},
        _AuditIndexes(set(), set(), set(), set()),
        _new_counters(),
        _TokenizationCache(_new_counters()),
        timer=_ReachabilityTimer(None),
        max_seconds=0,
    )
    assert timed.rows == []
    assert timed.truncated is True
    assert timed.reason == "max_seconds"
    assert timed.skipped == 1

    ledger = EventLedger()
    ledger.append("operator.note", "w", {"text": "alpha beta"})
    public = build_knowledge_reachability_audit_result(ledger, "w", limit=5, progress_interval_seconds=-1)
    payload = knowledge_reachability_json(public.rows, public.metadata)
    assert [row.candidate for row in public.rows] == sorted(row.candidate for row in public.rows)
    assert public.metadata.candidate_counts["evaluated"] == len(public.rows)
    assert sum(public.metadata.loss_stage_counts.values()) == len(public.rows)
    assert payload["rows"][0]["candidate"] == public.rows[0].candidate
    assert "Knowledge Reachability Audit" in format_knowledge_reachability_table(public.rows, public.metadata)
    assert len(ledger.list_events("w")) == 1


def test_reachability_metadata_assembly_helper_preserves_public_result_metadata(tmp_path):
    from seed_runtime.knowledge_reachability import (
        _assemble_knowledge_reachability_metadata,
        _admit_knowledge_reachability_candidates,
        _construct_knowledge_reachability_indexes,
        _evaluate_knowledge_reachability_candidates,
        _new_counters,
        _ReachabilityTimer,
        _TokenizationCache,
        build_knowledge_reachability_audit_result,
        format_knowledge_reachability_table,
    )
    from seed_runtime.state import StateProjector

    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "reachability.md").write_text("storage topology\n")
    (tmp_path / "seed_runtime").mkdir()
    (tmp_path / "seed_runtime" / "metadata_symbol.py").write_text("class MetadataSymbol: pass\n")
    ledger = EventLedger()
    ledger.append("operator.note", "w", {"text": "metadata_candidate"})
    ledger.append(
        "fact.observed",
        "w",
        {"fact": _fact("f1", "node115", "defines", "MetadataSymbol", {"path": "seed_runtime/metadata_symbol.py"})},
    )
    before_events = len(ledger.list_events("w"))
    events = ledger.list_events("w")
    state = StateProjector(ledger).project("w")
    counters = _new_counters()
    token_cache = _TokenizationCache(counters)
    admission = _admit_knowledge_reachability_candidates(
        events,
        state,
        tmp_path,
        counters,
        token_cache=token_cache,
        all_candidates=True,
        limit=7,
    )
    index_timings = {}
    timings = {"load_state": 0.1234567, "discover_candidates": 0.2, "render": 0.3, "total": 0.4}
    indexes = _construct_knowledge_reachability_indexes(
        events,
        state,
        timer=_ReachabilityTimer(None, timings),
        index_timings=index_timings,
        counters=counters,
        token_cache=token_cache,
    )
    evaluation = _evaluate_knowledge_reachability_candidates(
        admission.sorted_candidates,
        admission.candidates,
        indexes,
        counters,
        token_cache,
        timer=_ReachabilityTimer(None, timings),
        max_seconds=None,
        skipped=admission.skipped,
        truncated=admission.truncated,
        reason=admission.reason,
    )
    counters["candidate_count"] = len(evaluation.rows)
    counters["raw_candidates_discovered"] = admission.discovery.raw_seen
    counters["candidates_evaluated"] = len(evaluation.rows)

    metadata = _assemble_knowledge_reachability_metadata(
        evaluation.rows,
        admission=admission,
        timings=timings,
        counters=counters,
        index_timings=index_timings,
        cache={"state": "miss", "summary": "miss", "projection": "miss"},
        skipped=evaluation.skipped,
        truncated=evaluation.truncated,
        reason=evaluation.reason,
        max_seconds=None,
    )
    payload = knowledge_reachability_json(evaluation.rows, metadata)
    table = format_knowledge_reachability_table(evaluation.rows, metadata)

    assert metadata.timings["load_state"] == 0.123457
    assert metadata.candidate_counts["raw_seen"] == admission.discovery.raw_seen
    assert metadata.candidate_counts["used"] == len(admission.sorted_candidates)
    assert metadata.candidate_counts["limit"] == 0
    assert metadata.candidate_counts["evaluated"] == len(evaluation.rows)
    assert metadata.candidate_kind_counts == payload["metadata"]["candidate_kind_counts"]
    assert metadata.loss_stage_counts == payload["metadata"]["loss_stage_counts"]
    assert metadata.algorithmic_counters["candidates_evaluated"] == len(evaluation.rows)
    assert metadata.candidate_sources["event payloads"] > 0
    assert metadata.scan_counts["event payloads scanned"] > 0
    assert metadata.cache == {"state": "miss", "summary": "miss", "projection": "miss"}
    assert "read_model" in metadata.indexes
    assert metadata.truncated is evaluation.truncated
    assert metadata.reason == evaluation.reason
    assert metadata.limit is None
    assert metadata.max_seconds is None
    assert payload["metadata"]["timing"]["load state/cache"] == metadata.timings["load_state"]
    assert payload["metadata"]["candidates"] == metadata.candidate_counts
    assert "Knowledge Reachability Audit" in table
    assert len(ledger.list_events("w")) == before_events

    public = build_knowledge_reachability_audit_result(ledger, "w", repo_root=tmp_path, subject="node115")
    public_payload = knowledge_reachability_json(public.rows, public.metadata)
    assert public_payload["metadata"]["candidate_counts"]["evaluated"] == 1
    assert "Knowledge Reachability Audit" in format_knowledge_reachability_table(public.rows, public.metadata)
    assert len(ledger.list_events("w")) == before_events


def test_reachability_json_payload_helper_preserves_aliases_shapes_and_read_only():
    from seed_runtime.knowledge_reachability import (
        KnowledgeReachabilityMetadata,
        KnowledgeReachabilityRow,
        _knowledge_reachability_json_payload,
        build_knowledge_reachability_audit_result,
    )

    rows = [
        KnowledgeReachabilityRow(
            "runtime",
            "runtime_value",
            "node115",
            True,
            True,
            False,
            False,
            False,
            "read_model_loss",
        )
    ]
    metadata = KnowledgeReachabilityMetadata(
        timings={"load_state": 1.25, "total": 2.5},
        candidate_counts={"evaluated": 1, "skipped": 0},
        candidate_kind_counts={"runtime_value": 1},
        loss_stage_counts={"read_model_loss": 1},
        algorithmic_counters={"membership_checks": 1},
        candidate_sources={"default seeds": 1},
        scan_counts={"event payloads scanned": 0},
        cache={"state": "miss"},
        indexes={"read_model": 0.5},
        truncated=True,
        reason="limit",
        limit=1,
        max_seconds=9.0,
    )
    ledger = EventLedger()
    before_events = len(ledger.list_events("w"))

    row_only = _knowledge_reachability_json_payload(rows)
    payload = _knowledge_reachability_json_payload(rows, metadata)
    public_payload = knowledge_reachability_json(rows, metadata)
    encoded = json.loads(json.dumps(payload))

    assert row_only == [
        {
            "family": "runtime",
            "candidate_kind": "runtime_value",
            "candidate": "node115",
            "preserved": True,
            "projected": True,
            "read_model": False,
            "inquiry_orientation": False,
            "rendered": False,
            "first_loss": "read_model_loss",
        }
    ]
    assert payload == public_payload
    assert set(payload) == {"metadata", "rows"}
    assert payload["rows"] == row_only
    assert payload["metadata"]["timings"] == metadata.timings
    assert payload["metadata"]["candidate_counts"] == metadata.candidate_counts
    assert payload["metadata"]["timing"]["load_state"] == 1.25
    assert payload["metadata"]["timing"]["load state/cache"] == 1.25
    assert payload["metadata"]["candidates"] == metadata.candidate_counts
    assert encoded["metadata"]["candidate_kind_counts"] == {"runtime_value": 1}
    assert encoded["metadata"]["loss_stage_counts"] == {"read_model_loss": 1}
    assert encoded["metadata"]["truncated"] is True
    assert encoded["metadata"]["reason"] == "limit"
    assert len(ledger.list_events("w")) == before_events

    result = build_knowledge_reachability_audit_result(ledger, "w", subject="node115")
    cli_like_json = json.dumps(knowledge_reachability_json(result.rows, result.metadata))
    decoded = json.loads(cli_like_json)
    assert decoded["metadata"]["timing"]["load state/cache"] == decoded["metadata"]["timings"]["load_state"]
    assert decoded["metadata"]["candidates"] == decoded["metadata"]["candidate_counts"]
    assert len(ledger.list_events("w")) == before_events


def test_reachability_table_output_helper_preserves_human_format_and_read_only():
    from seed_runtime.knowledge_reachability import (
        KnowledgeReachabilityMetadata,
        KnowledgeReachabilityRow,
        _knowledge_reachability_table_output,
        build_knowledge_reachability_audit_result,
    )

    rows = [
        KnowledgeReachabilityRow(
            "runtime",
            "runtime_value",
            "node115",
            True,
            False,
            True,
            False,
            True,
            "projected_loss",
        ),
        KnowledgeReachabilityRow(
            "repository",
            "presentation_label",
            "source navigation",
            False,
            False,
            False,
            True,
            True,
            "visibility_only",
        ),
    ]
    metadata = KnowledgeReachabilityMetadata(
        timings={"load_state": 1.2345, "total": 2.0},
        candidate_counts={"raw_seen": 2, "evaluated": 2},
        candidate_kind_counts={"runtime_value": 1, "presentation_label": 1},
        loss_stage_counts={"projected_loss": 1, "visibility_only": 1},
        truncated=True,
        reason="max_seconds",
    )
    ledger = EventLedger()
    before_events = len(ledger.list_events("w"))

    table_only = _knowledge_reachability_table_output(rows)
    full_table = _knowledge_reachability_table_output(rows, metadata)
    public_table = format_knowledge_reachability_table(rows, metadata)

    assert public_table == full_table
    assert table_only.splitlines()[0] == "Family     | Kind               | Candidate         | Preserved | Projected | Read Model | Inquiry Orientation | Rendered | First Loss     "
    assert table_only.splitlines()[1] == "---------- | ------------------ | ----------------- | --------- | --------- | ---------- | ------------------- | -------- | ---------------"
    assert "runtime    | runtime_value      | node115           | yes       | no        | yes        | no                  | yes      | projected_loss" in table_only
    assert "repository | presentation_label | source navigation | no        | no        | no         | yes                 | yes      | visibility_only" in table_only
    assert full_table.startswith("Knowledge Reachability Audit\nTiming:\n  load_state: 1.234s\n  total: 2.000s")
    assert "\nCandidates:\n  raw_seen: 2\n  evaluated: 2" in full_table
    assert "\nCandidate Kinds:\n  runtime_value: 1\n  presentation_label: 1" in full_table
    assert "\nLoss Stages:\n  projected_loss: 1\n  visibility_only: 1" in full_table
    assert "\nTruncated: true (max_seconds)\n\nFamily" in full_table
    assert full_table.endswith(table_only)
    assert len(ledger.list_events("w")) == before_events

    result = build_knowledge_reachability_audit_result(ledger, "w", subject="node115")
    cli_like_human = format_knowledge_reachability_table(result.rows, result.metadata)
    assert "Knowledge Reachability Audit" in cli_like_human
    assert "Family" in cli_like_human
    assert "node115" in cli_like_human
    assert len(ledger.list_events("w")) == before_events
