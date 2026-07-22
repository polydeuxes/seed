import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from seed_runtime.models import ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation
from seed_runtime.state import State


SCRIPT_PATH = Path("scripts/seed_local.py")


def load_seed_local_module():
    spec = importlib.util.spec_from_file_location("seed_local", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _assert_default_state_summary_has_no_storage_detail(output: str) -> None:
    forbidden = [
        "filesystems:",
        "bytes free/total",
        "showing root filesystems only",
        "detail bounded",
        "storage topology:",
        "cluster mount groups",
        "shared storage candidates",
        "storage topology ambiguities",
    ]
    for text in forbidden:
        assert text not in output


def test_cli_state_summary_rejects_storage_projection_sections():
    seed_local = load_seed_local_module()

    output = seed_local.format_state_summary(
        {
            "entity_count": 0,
            "fact_count": 0,
            "durable_fact_count": 0,
            "measurement_current_sample_count": 0,
            "conflict_count": 0,
            "stale_fact_count": 0,
            "graph_issue_warning_count": 0,
            "graph_issue_error_count": 0,
            "observation_source_counts": {},
            "availability": {"up": 0, "down": 0, "unknown": 0},
            "filesystems": [
                {
                    "host": "example_host_100:9100",
                    "mountpoint": "/mnt/example_host_205/sda1",
                    "free": 10,
                    "total": 100,
                }
            ],
            "cluster_mount_groups": [
                {
                    "mountpoint": "/mnt/example_host_205/sda1",
                    "visible_endpoint_count": 2,
                    "visible_endpoints": [
                        "example_host_100:9100",
                        "example_host_101:9100",
                    ],
                }
            ],
            "shared_storage_candidates": [
                {
                    "mountpaths": ["/mnt/example_host_205/sda1"],
                    "visible_endpoint_count": 2,
                    "visible_endpoints": [
                        "example_host_100:9100",
                        "example_host_101:9100",
                    ],
                    "evidence": ["matching total bytes", "matching device"],
                    "confidence": "medium",
                    "boundary": (
                        "candidate shared storage != shared storage fact; "
                        "candidate shared storage != ownership; "
                        "candidate shared storage != topology authority"
                    ),
                }
            ],
            "storage_topology_ambiguities": [
                {
                    "subject": "/mnt/example_host_205/sda1",
                    "materiality": "medium",
                    "reasons": ["mountpath visible on 2 endpoints"],
                    "candidate_interpretations": [
                        "multi-endpoint mount visibility",
                        "historical-node-style naming",
                    ],
                    "boundary": (
                        "ambiguity != fact; "
                        "ambiguity != ownership; "
                        "ambiguity != storage identity; "
                        "ambiguity != resolved topology"
                    ),
                }
            ],
        }
    )

    _assert_default_state_summary_has_no_storage_detail(output)


def test_cli_state_summary_rejects_bounded_filesystem_detail():
    seed_local = load_seed_local_module()
    filesystems = []
    for index in range(12):
        filesystems.append(
            {
                "host": f"node{index:03d}:9100",
                "mountpoint": "/",
                "free": index,
                "total": 100 + index,
            }
        )
    for index in range(3):
        filesystems.append(
            {
                "host": f"node{index:03d}:9100",
                "mountpoint": f"/boot/firmware{index}",
                "free": 10 + index,
                "total": 200 + index,
            }
        )
    for index in range(4):
        filesystems.append(
            {
                "host": f"node{index:03d}:9100",
                "mountpoint": f"/mnt/example_host_20{index}/sda1",
                "free": 20 + index,
                "total": 300 + index,
            }
        )
    for index in range(2):
        filesystems.append(
            {
                "host": f"node{index:03d}:9100",
                "mountpoint": f"/srv/data{index}",
                "free": 30 + index,
                "total": 400 + index,
            }
        )

    output = seed_local.format_state_summary(
        {
            "entity_count": 0,
            "fact_count": 0,
            "durable_fact_count": 0,
            "measurement_current_sample_count": 0,
            "conflict_count": 0,
            "stale_fact_count": 0,
            "graph_issue_warning_count": 0,
            "graph_issue_error_count": 0,
            "observation_source_counts": {},
            "availability": {"up": 0, "down": 0, "unknown": 0},
            "filesystems": filesystems,
            "cluster_mount_groups": [],
            "shared_storage_candidates": [],
            "storage_topology_ambiguities": [],
        }
    )

    _assert_default_state_summary_has_no_storage_detail(output)


def test_cli_state_summary_rejects_storage_topology_counts():
    seed_local = load_seed_local_module()

    summary = {
        "entity_count": 0,
        "fact_count": 0,
        "durable_fact_count": 0,
        "measurement_current_sample_count": 0,
        "conflict_count": 0,
        "stale_fact_count": 0,
        "graph_issue_warning_count": 0,
        "graph_issue_error_count": 0,
        "observation_source_counts": {},
        "availability": {"up": 0, "down": 0, "unknown": 0},
        "filesystems": [],
        "cluster_mount_groups": [
            {"mountpoint": f"/mnt/example_host_20{index}/sda1"} for index in range(3)
        ],
        "shared_storage_candidates": [
            {"mountpaths": ["/srv/high"], "confidence": "high"},
            {"mountpaths": ["/srv/medium-a"], "confidence": "medium"},
            {"mountpaths": ["/srv/medium-b"], "confidence": "medium"},
            {"mountpaths": ["/srv/low"], "confidence": "low"},
        ],
        "storage_topology_ambiguities": [
            {"subject": "/srv/high", "materiality": "high"},
            {"subject": "/srv/medium-a", "materiality": "medium"},
            {"subject": "/srv/medium-b", "materiality": "medium"},
            {"subject": "/srv/low", "materiality": "low"},
        ],
    }

    output = seed_local.format_state_summary(summary)

    _assert_default_state_summary_has_no_storage_detail(output)


def test_cli_state_summary_rejects_precomputed_storage_topology_counts():
    seed_local = load_seed_local_module()

    output = seed_local.format_state_summary(
        {
            "entity_count": 0,
            "fact_count": 0,
            "durable_fact_count": 0,
            "measurement_current_sample_count": 0,
            "conflict_count": 0,
            "stale_fact_count": 0,
            "graph_issue_warning_count": 0,
            "graph_issue_error_count": 0,
            "observation_source_counts": {},
            "availability": {"up": 0, "down": 0, "unknown": 0},
            "filesystems": [],
            "cluster_mount_groups": [
                {"mountpoint": f"/mnt/node{index}/sda1"} for index in range(31)
            ],
            "shared_storage_candidates": [
                {"mountpaths": [f"/mnt/node{index}/sda1"], "confidence": "low"}
                for index in range(42)
            ],
            "storage_topology_ambiguities": [
                {"subject": f"/mnt/node{index}/sda1", "materiality": "low"}
                for index in range(187)
            ],
            "storage_topology_summary": {
                "cluster_mount_group_count": 31,
                "shared_storage_candidate_count": 42,
                "shared_storage_candidate_confidence_counts": {"low": 42},
                "storage_topology_ambiguity_count": 187,
                "storage_topology_ambiguity_materiality_counts": {
                    "medium": 12,
                    "low": 175,
                },
            },
        }
    )

    _assert_default_state_summary_has_no_storage_detail(output)


def test_parser_no_longer_exposes_generic_http_or_model_selection():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--events", "--db", ".seed-local.sqlite"]
    )

    assert args.events is True
    assert args.db == ".seed-local.sqlite"
    assert args.message == []
    assert not hasattr(args, "http")
    assert not hasattr(args, "host")
    assert not hasattr(args, "port")
    assert not hasattr(args, "raw")
    assert not hasattr(args, "raw_only")
    assert not hasattr(args, "plan")
    assert not hasattr(args, "model")



def test_parser_excludes_execution_proposal_and_authorization_surfaces():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()
    args = parser.parse_args(["--db", ".seed-local.sqlite", "--events"])

    assert not hasattr(args, "proposal")
    assert not hasattr(args, "authorize_proposal")
    assert not hasattr(args, "authorize_execution")
    assert not hasattr(args, "grant_method")
    assert not hasattr(args, "ttl_seconds")

    help_text = parser.format_help()
    assert "--proposal" not in help_text
    assert "--authorize-proposal" not in help_text
    assert "execution proposal" not in help_text
    assert "execution authorization" not in help_text

def test_cli_fact_creates_observation_fact_through_ingestor(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--fact", "web_service", "runtime", "docker"]) == 0

    output = capsys.readouterr().out
    assert "fact_id: fact_obs_" in output
    assert "subject: web_service" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "source_type: user" in output
    assert "confidence: 1.0" in output


def test_parser_accepts_observation_ingestion_options():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        [
            "--observe",
            "web_service",
            "runtime",
            "docker",
            "--source-type",
            "discovery",
            "--confidence",
            "0.81",
        ]
    )

    assert args.observe == [["web_service", "runtime", "docker"]]
    assert args.source_type == "discovery"
    assert args.confidence == 0.81


def test_parser_accepts_json_observation_ingestion_option():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(["--observe-json", "inventory.json"])

    assert args.observe_json == "inventory.json"


def test_parser_accepts_observe_timings_flag():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--observe-local-host", "--observe-timings"]
    )

    assert args.observe_timings is True


def test_cli_observe_json_ingests_imported_observations(tmp_path, capsys):
    seed_local = load_seed_local_module()
    json_path = tmp_path / "observations.json"
    json_path.write_text(
        '{"observations":[{"subject":"web_service","predicate":"runtime",'
        '"value":"docker","confidence":0.95}]}',
        encoding="utf-8",
    )

    assert seed_local.main(["--observe-json", str(json_path)]) == 0

    output = capsys.readouterr().out
    assert "fact_id: fact_obs_" in output
    assert "subject: web_service" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "source_type: imported" in output
    assert "confidence: 0.95" in output


def test_parser_accepts_json_observation_export_option():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--export-observations-json", "inventory.json"]
    )

    assert args.export_observations_json == "inventory.json"


def test_cli_export_observations_json_writes_inventory(tmp_path, capsys):
    seed_local = load_seed_local_module()
    output_path = tmp_path / "observations.json"

    assert (
        seed_local.main(
            [
                "--observe",
                "web_service",
                "runtime",
                "docker",
                "--source-type",
                "discovery",
                "--confidence",
                "0.81",
                "--export-observations-json",
                str(output_path),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert "exported 1 observation(s)" in output
    assert payload == {
        "observations": [
            {
                "confidence": 0.81,
                "observed_at": payload["observations"][0]["observed_at"],
                "predicate": "runtime",
                "source_type": "discovery",
                "subject": "web_service",
                "value": "docker",
            }
        ]
    }


def test_parser_accepts_repeatable_fact_seed_options():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        [
            "--fact",
            "web_service",
            "runtime",
            "docker",
            "--fact",
            "plex",
            "runtime",
            "systemd",
            "restart",
            "web_service?",
        ]
    )

    assert args.fact == [
        ["web_service", "runtime", "docker"],
        ["plex", "runtime", "systemd"],
    ]
    assert args.message == ["restart", "web_service?"]


def test_dev_fact_cli_rejects_secret_field_names():
    seed_local = load_seed_local_module()

    for field in ("password", "passphrase", "token", "private_key"):
        with pytest.raises(ValueError, match="secret field"):
            seed_local.parse_dev_fact(["example_host", field, "not-accepted"])


def test_dev_fact_cli_rejects_json_values_with_secret_fields():
    seed_local = load_seed_local_module()

    with pytest.raises(ValueError, match="secret field"):
        seed_local.parse_dev_fact(["example_host", "auth", '{"token": "not-accepted"}'])


def test_parser_supports_fact_projection_queries():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()

    support_args = parser.parse_args(["--fact-support", "web_service", "runtime"])
    best_args = parser.parse_args(["--best-fact", "web_service", "runtime"])
    conflicts_args = parser.parse_args(["--fact-conflicts"])
    refreshes_args = parser.parse_args(["--stale-fact-refreshes"])
    summary_args = parser.parse_args(["--state-build"])
    summary_debug_args = parser.parse_args(["--state-build-cache-debug"])
    current_facts_debug_args = parser.parse_args(["--current-facts-cache-debug"])
    filtered_current_facts_debug_args = parser.parse_args(
        ["--current-selection", "web_service", "runtime", "--current-facts-cache-debug"]
    )

    history_args = parser.parse_args(
        [
            "--fact-support",
            "example_host",
            "up",
            "--include-history",
        ]
    )
    history_alias_args = parser.parse_args(
        [
            "--fact-support",
            "example_host",
            "up",
            "--history",
        ]
    )

    assert support_args.fact_support == ["web_service", "runtime"]
    assert history_args.include_history is True
    assert history_alias_args.include_history is True
    assert best_args.best_fact == ["web_service", "runtime"]
    assert conflicts_args.fact_conflicts is True
    assert refreshes_args.stale_fact_refreshes is True
    assert summary_args.state_build is True
    assert summary_debug_args.state_build_cache_debug is True
    assert current_facts_debug_args.current_facts_cache_debug is True
    assert current_facts_debug_args.current_selection is None
    assert filtered_current_facts_debug_args.current_facts_cache_debug is True
    assert filtered_current_facts_debug_args.current_selection == ["web_service", "runtime"]



def test_parser_current_selection_boundary_rejects_current_facts():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()

    args = parser.parse_args(["--current-selection", "web_service", "runtime"])

    assert args.current_selection == ["web_service", "runtime"]
    for argv in (["--current-selection"], ["--current-selection", "only-one"], ["--current-facts"], ["--current-facts", "a", "b"]):
        with pytest.raises(SystemExit):
            parser.parse_args(argv)


def test_cli_current_selection_emits_diagnostic_contract(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-selection.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", "192.0.2.115")],
    )

    assert seed_local.main(["--db", str(db_path), "--current-selection", "example_host", "alias"]) == 0

    output = capsys.readouterr().out
    assert "Current-Selection Diagnostic" in output
    assert "does not establish Fact standing" in output
    assert output.rstrip().endswith("192.0.2.115")

def test_cli_state_summary_cache_debug_without_db_reports_unavailable(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--state-build-cache-debug"]) == 0

    output = capsys.readouterr().out
    assert "State Build Cache Debug" in output
    assert "- status: ineligible" in output
    assert "- reason: --db is required for persisted read-model caches" in output
    assert "State-build cache:\n- status: unavailable" in output
    assert "Projection cache:\n- status: unavailable" in output


def test_cli_state_summary_cache_debug_does_not_ingest_or_execute(
    tmp_path, monkeypatch, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-debug.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        seed_local.ObservationIngestor(ledger).ingest(
            seed_local.Observation(
                id="obs_debug_host",
                source_type="user",
                observed_at=seed_local.utc_now(),
                subject="debug-host",
                predicate="os",
                value="linux",
            ),
            "local",
        )
        before = len(ledger.list_events("local"))
    finally:
        ledger.close()

    monkeypatch.setattr(
        seed_local,
        "seed_dev_state_from_args",
        lambda args, ledger: pytest.fail("state-build cache debug must not ingest"),
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--state-build-cache-debug",
                "--fact",
                "ignored",
                "os",
                "x",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "State-build cache:\n- status: miss" in output
    assert "Projection replay / build subphase timings:" in output
    assert "- event replay:" in output
    assert "- finalization: fact support construction:" in output
    assert "Projection/build structure counts:" in output
    assert "- facts:" in output
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        assert len(ledger.list_events("local")) == before
    finally:
        ledger.close()


def test_cli_state_summary_cache_debug_reports_warm_summary_hit(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-debug-warm.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        seed_local.ObservationIngestor(ledger).ingest(
            seed_local.Observation(
                id="obs_debug_warm",
                source_type="user",
                observed_at=seed_local.utc_now(),
                subject="warm-host",
                predicate="os",
                value="linux",
            ),
            "local",
        )
    finally:
        ledger.close()

    assert seed_local.main(["--db", str(db_path), "--state-build-cache-debug"]) == 0
    cold_output = capsys.readouterr().out
    assert "State-build cache:\n- status: miss" in cold_output

    assert seed_local.main(["--db", str(db_path), "--state-build-cache-debug"]) == 0
    warm_output = capsys.readouterr().out
    assert "State-build cache:\n- status: hit" in warm_output
    assert "Projection cache:\n- status: skipped" in warm_output
    assert "Projection replay / build subphase timings:" not in warm_output


def test_state_summary_cache_debug_separates_visibility_from_projection_diagnostics(tmp_path):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-debug-boundary.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        seed_local.ObservationIngestor(ledger).ingest(
            seed_local.Observation(
                id="obs_debug_boundary",
                source_type="user",
                observed_at=seed_local.utc_now(),
                subject="boundary-host",
                predicate="os",
                value="linux",
            ),
            "local",
        )
    finally:
        ledger.close()

    args = seed_local.build_parser().parse_args(
        ["--db", str(db_path), "--state-build-cache-debug"]
    )

    report = seed_local.state_summary_cache_debug_from_args(args)

    assert report.visibility.summary_cache_status == report.summary_cache_status
    assert (
        report.projection_diagnostics.state_cache_status == report.state_cache_status
    )
    assert report.projection_diagnostics.projection_timings == report.projection_timings
    assert (
        report.projection_diagnostics.projection_counters
        == report.projection_counters
    )
    assert not hasattr(report.visibility, "state_cache_status")
    assert not hasattr(report.visibility, "projection_timings")


def test_state_summary_cache_debug_assembly_consumes_cache_evidence():
    seed_local = load_seed_local_module()

    visibility = seed_local._StateBuildVisibilityPayload(
        cache_eligible=True,
        cache_ineligible_reason=None,
        summary_cache_status="hit",
        current_last_event_id="event-1",
        cached_summary_last_event_id="summary-event-1",
        notes=["summary cache satisfied the request"],
    )
    projection_diagnostics = seed_local._ProjectionCacheDiagnosticPayload(
        state_cache_status="skipped",
        cached_state_last_event_id=None,
        projection_timings=[],
        projection_counters={},
    )
    cache_evidence = seed_local._StateBuildCacheDebugCacheEvidence(
        visibility=visibility,
        projection_diagnostics=projection_diagnostics,
    )

    projection_evidence = seed_local._StateBuildCacheDebugProjectionEvidence(
        projection_diagnostics=projection_diagnostics
    )
    read_model_evidence = seed_local._StateBuildCacheDebugReadModelEvidence(
        summary_source="summary snapshot",
        summary_snapshot_published=False,
    )

    timing_evidence = seed_local._StateBuildCacheDebugTimingEvidence(
        timings=[("total runtime", 0.2)]
    )

    assembly = seed_local._StateBuildCacheDebugEvidenceAssembly.from_evidence_streams(
        cache_evidence,
        projection_evidence,
        read_model_evidence,
        timing_evidence,
    )
    compatible_assembly = (
        seed_local._StateBuildCacheDebugEvidenceAssembly.from_cache_evidence(
            cache_evidence,
            read_model_evidence=read_model_evidence,
            timing_evidence=timing_evidence,
        )
    )

    assert assembly.visibility is visibility
    assert assembly.projection_diagnostics is projection_diagnostics
    assert assembly.read_model_evidence is read_model_evidence
    assert assembly.timings == [("total runtime", 0.2)]
    assert compatible_assembly.projection_diagnostics is projection_diagnostics
    assert compatible_assembly.read_model_evidence is read_model_evidence


def test_state_summary_cache_debug_timing_evidence_preserves_collected_labels(
    monkeypatch,
):
    seed_local = load_seed_local_module()

    perf_counter_values = iter([12.5])
    monkeypatch.setattr(
        seed_local.time, "perf_counter", lambda: next(perf_counter_values)
    )

    timing_evidence = (
        seed_local._StateBuildCacheDebugTimingEvidence.from_collected_timings(
            [
                ("projection store open", 0.01),
                ("state summary snapshot lookup", 0.02),
                ("projection replay / build", 0.03),
            ],
            started=10.0,
        )
    )

    assert timing_evidence.timings == [
        ("projection store open", 0.01),
        ("state summary snapshot lookup", 0.02),
        ("projection replay / build", 0.03),
        ("total runtime", 2.5),
    ]


def test_state_summary_cache_debug_projection_evidence_from_selection():
    seed_local = load_seed_local_module()

    projection_diagnostics = seed_local.ProjectionBuildDiagnostics(
        timings=[("projection replay / build", 0.1)], counters={"events": 1}
    )
    projection_selection = seed_local._ProjectionDiagnosticSelection.from_payload(
        projection_diagnostics.payload
    )

    projection_evidence = (
        seed_local._StateBuildCacheDebugProjectionEvidence.from_diagnostic_selection(
            state_cache_status="miss",
            cached_state_last_event_id="event-1",
            projection_selection=projection_selection,
        )
    )

    assert projection_evidence.projection_diagnostics.state_cache_status == "miss"
    assert (
        projection_evidence.projection_diagnostics.cached_state_last_event_id
        == "event-1"
    )
    assert projection_evidence.projection_diagnostics.projection_timings == [
        ("projection replay / build", 0.1)
    ]
    assert projection_evidence.projection_diagnostics.projection_counters == {
        "events": 1
    }


def test_state_summary_cache_debug_evidence_consumes_evidence_assembly():
    seed_local = load_seed_local_module()

    visibility = seed_local._StateBuildVisibilityPayload(
        cache_eligible=True,
        cache_ineligible_reason=None,
        summary_cache_status="miss",
        current_last_event_id="event-1",
        cached_summary_last_event_id=None,
        notes=["note"],
    )
    projection_diagnostics = seed_local._ProjectionCacheDiagnosticPayload(
        state_cache_status="miss",
        cached_state_last_event_id=None,
        projection_timings=[("projection replay / build", 0.1)],
        projection_counters={"events": 1},
    )
    read_model_evidence = seed_local._StateBuildCacheDebugReadModelEvidence(
        summary_source="constructed read model",
        summary_snapshot_published=True,
    )
    assembly = seed_local._StateBuildCacheDebugEvidenceAssembly(
        visibility=visibility,
        projection_diagnostics=projection_diagnostics,
        read_model_evidence=read_model_evidence,
        timings=[("total runtime", 0.2)],
    )

    evidence = seed_local._StateBuildCacheDebugEvidence.from_assembly(assembly)

    assert evidence.visibility is visibility
    assert evidence.projection_diagnostics is projection_diagnostics
    assert evidence.read_model_evidence is read_model_evidence
    assert evidence.timings == [("total runtime", 0.2)]


def test_state_summary_cache_debug_report_consumes_debug_evidence():
    seed_local = load_seed_local_module()

    evidence = seed_local._StateBuildCacheDebugEvidence(
        visibility=seed_local._StateBuildVisibilityPayload(
            cache_eligible=True,
            cache_ineligible_reason=None,
            summary_cache_status="miss",
            current_last_event_id="event-1",
            cached_summary_last_event_id=None,
            notes=["note"],
        ),
        projection_diagnostics=seed_local._ProjectionCacheDiagnosticPayload(
            state_cache_status="miss",
            cached_state_last_event_id=None,
            projection_timings=[("projection replay / build", 0.1)],
            projection_counters={"events": 1},
        ),
        read_model_evidence=seed_local._StateBuildCacheDebugReadModelEvidence(
            summary_source="constructed read model",
            summary_snapshot_published=True,
        ),
        timings=[("total runtime", 0.2)],
    )

    payload = seed_local._StateBuildCacheDebugReportPayload.from_evidence(evidence)
    report = seed_local.StateSummaryCacheDebugReport.from_payload(payload)
    compatible_report = seed_local.StateSummaryCacheDebugReport.from_evidence(evidence)

    assert payload.visibility is evidence.visibility
    assert payload.projection_diagnostics is evidence.projection_diagnostics
    assert payload.timings == evidence.timings
    assert report.visibility is payload.visibility
    assert report.projection_diagnostics is payload.projection_diagnostics
    assert report.timings == payload.timings
    assert report.summary_cache_status == "miss"
    assert report.state_cache_status == "miss"
    assert compatible_report.visibility is evidence.visibility
    assert compatible_report.projection_diagnostics is evidence.projection_diagnostics
    assert compatible_report.timings == evidence.timings


def test_cli_state_summary_cache_debug_does_not_change_normal_summary_output(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-debug-normal.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        seed_local.ObservationIngestor(ledger).ingest(
            seed_local.Observation(
                id="obs_normal_summary",
                source_type="user",
                observed_at=seed_local.utc_now(),
                subject="normal-host",
                predicate="os",
                value="linux",
            ),
            "local",
        )
    finally:
        ledger.close()

    assert seed_local.main(["--db", str(db_path), "--state-build"]) == 0
    before = capsys.readouterr().out
    assert seed_local.main(["--db", str(db_path), "--state-build-cache-debug"]) == 0
    capsys.readouterr()
    assert seed_local.main(["--db", str(db_path), "--state-build"]) == 0
    after = capsys.readouterr().out
    assert "  state-build cache: miss" in before
    assert "  state-build cache: hit" in after
    assert before.count("State Build") == 1
    assert after.count("State Build") == 1
    assert "Projected State:" in before


def test_cli_state_summary_reports_projected_world_model_without_ingestion(
    tmp_path, monkeypatch, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    ingestor = seed_local.ObservationIngestor(ledger)
    now = seed_local.utc_now()

    observations = [
        seed_local.Observation(
            id="obs_host_up_old",
            source_type="discovery",
            observed_at=now - seed_local.timedelta(minutes=2),
            subject="host-up",
            predicate="availability_status",
            value="down",
        ),
        seed_local.Observation(
            id="obs_host_up_current",
            source_type="discovery",
            observed_at=now - seed_local.timedelta(minutes=1),
            subject="host-up",
            predicate="availability_status",
            value="up",
        ),
        seed_local.Observation(
            id="obs_host_down",
            source_type="discovery",
            observed_at=now,
            subject="host-down",
            predicate="availability_status",
            value="down",
        ),
        seed_local.Observation(
            id="obs_alias",
            source_type="user",
            observed_at=now,
            subject="host-up",
            predicate="alias",
            value="10.0.0.10",
        ),
        seed_local.Observation(
            id="obs_runtime_docker",
            source_type="user",
            observed_at=now,
            subject="host-up",
            predicate="runtime",
            value="docker",
        ),
        seed_local.Observation(
            id="obs_runtime_systemd",
            source_type="user",
            observed_at=now,
            subject="host-up",
            predicate="runtime",
            value="systemd",
        ),
        seed_local.Observation(
            id="obs_stale_os",
            source_type="imported",
            observed_at=now - seed_local.timedelta(days=2),
            subject="old-host",
            predicate="os",
            value="linux",
            expires_at=now - seed_local.timedelta(days=1),
        ),
        seed_local.Observation(
            id="obs_filesystem_free",
            source_type="discovery",
            observed_at=now,
            subject="10.0.0.10",
            predicate="filesystem_free_bytes",
            value=40,
            dimensions={"mountpoint": "/", "device": "/dev/sda1"},
        ),
        seed_local.Observation(
            id="obs_filesystem_total",
            source_type="discovery",
            observed_at=now,
            subject="10.0.0.10",
            predicate="filesystem_total_bytes",
            value=100,
            dimensions={"mountpoint": "/", "device": "/dev/sda1"},
        ),
    ]
    try:
        for observation in observations:
            ingestor.ingest(observation, "local")
    finally:
        ledger.close()

    monkeypatch.setattr(
        seed_local,
        "seed_dev_state_from_args",
        lambda args, ledger: pytest.fail("state summary must not ingest"),
    )


    assert (
        seed_local.main(
            ["--db", str(db_path), "--state-build", "--fact", "ignored", "os", "x"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "entities: 3" in output
    assert "facts: 8" in output
    assert "durable facts: 4" in output
    assert "measurement current samples: 4" in output
    assert "conflicts: 1" in output
    assert "stale facts: 1" in output
    assert "Observation Sources:" in output
    assert "  discovery: 4" in output
    assert "  imported: 1" in output
    assert "  user: 3" in output
    assert output.count("State Build") == 1
    assert "Projected State:" in output
    assert "Fact Accounting:" in output
    assert "top entities by kind:" not in output
    assert "top entities:" not in output
    assert "    host-up (aliases: 1 total; facts: 3)" not in output
    assert "10.0.0.10; facts" not in output
    assert "availability by scope:" not in output
    assert "availability:" not in output
    _assert_default_state_summary_has_no_storage_detail(output)


def test_format_state_summary_does_not_render_top_entity_compatibility_fields():
    seed_local = load_seed_local_module()

    output = seed_local.format_state_summary(
        {
            "entity_count": 3,
            "fact_count": 2,
            "durable_fact_count": 2,
            "measurement_current_sample_count": 0,
            "conflict_count": 0,
            "stale_fact_count": 0,
            "graph_issue_warning_count": 0,
            "graph_issue_error_count": 0,
            "observation_source_counts": {},
            "top_entities_by_kind": {
                "hosts": [{"name": "example_host", "alias_count": 0, "fact_count": 1}],
                "services": [{"name": "api", "alias_count": 0, "fact_count": 1}],
                "endpoints": {"total": 1, "up": 0, "down": 1, "unknown": 0},
                "storage": [{"name": "pool-a", "alias_count": 0, "fact_count": 1}],
            },
            "top_entities": [
                {"name": "legacy-host", "alias_count": 0, "fact_count": 1}
            ],
            "availability_by_scope": {
                "endpoint_scrape_availability": {"up": 0, "down": 1, "unknown": 0},
                "host_availability": {"up": 0, "down": 0, "unknown": 1},
                "service_availability": {"up": 1, "down": 0, "unknown": 0},
            },
        }
    )

    assert "top entities by kind:" not in output
    assert "top entities:" not in output
    assert "example_host" not in output
    assert "api" not in output
    assert "pool-a" not in output
    assert "legacy-host" not in output
    assert "availability by scope:" not in output
    assert "availability:" not in output


def test_cli_state_summary_counts_local_observation_without_availability_as_unknown(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-local-observation.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "local_observation_status", "observed")],
    )

    assert seed_local.main(["--db", str(db_path), "--state-build"]) == 0

    output = capsys.readouterr().out
    assert "entities: 1" in output
    assert "availability by scope:" not in output
    assert "availability:" not in output


def test_cli_state_summary_counts_host_availability_up(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-up.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "availability_status", "up")],
    )

    assert seed_local.main(["--db", str(db_path), "--state-build"]) == 0

    output = capsys.readouterr().out
    assert "entities: 1" in output
    assert "availability by scope:" not in output
    assert "availability:" not in output


def test_cli_state_summary_counts_host_availability_down(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-down.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "availability_status", "down")],
    )

    assert seed_local.main(["--db", str(db_path), "--state-build"]) == 0

    output = capsys.readouterr().out
    assert "entities: 1" in output
    assert "availability by scope:" not in output
    assert "availability:" not in output


def test_cli_state_summary_keeps_endpoint_availability_separate_from_host(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-endpoint-availability.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "alias", "192.0.2.115"),
            ("example_host", "local_observation_status", "observed"),
            ("192.0.2.115:9100", "availability_status", "up"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--state-build"]) == 0

    output = capsys.readouterr().out
    assert "entities: 2" in output
    assert "availability by scope:" not in output
    assert "availability:" not in output


def test_cli_state_summary_no_longer_renders_legacy_top_entities(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-many-aliases.sqlite"
    aliases = [f"172.17.0.{index}" for index in range(1, 6)]
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", alias) for alias in aliases],
    )

    assert seed_local.main(["--db", str(db_path), "--state-build"]) == 0

    output = capsys.readouterr().out
    assert "top entities by kind:" not in output
    assert "top entities:" not in output
    assert "example_host (aliases: 5 total; facts: 5)" not in output
    for alias in aliases:
        assert alias not in output


def test_cli_current_facts_and_fact_support_keep_raw_alias_evidence(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "state-summary-raw-alias-evidence.sqlite"
    aliases = ["192.0.2.115", "192.168.254.116"]
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", alias) for alias in aliases],
    )

    assert (
        seed_local.main(
            ["--db", str(db_path), "--current-selection", "example_host", "alias"]
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines()[-len(aliases):] == aliases

    assert (
        seed_local.main(
            ["--db", str(db_path), "--fact-support", "example_host", "alias"]
        )
        == 0
    )
    support_output = capsys.readouterr().out
    assert "value: 192.0.2.115" in support_output
    assert "value: 192.168.254.116" in support_output


def test_cli_cache_debug_commands_are_standalone_views(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--state-build-cache-debug"]) == 0
    state_summary_output = capsys.readouterr().out

    assert seed_local.main(["--current-facts-cache-debug"]) == 0
    current_facts_output = capsys.readouterr().out

    assert "State Build Cache Debug" in state_summary_output
    assert "Current Facts Timing" in current_facts_output


def test_cli_current_facts_cache_debug_renders_timing_section(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-facts-debug.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", "example_host.local")],
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--current-facts-cache-debug",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "example_host alias example_host.local" in output
    assert "Current Facts Timing" in output
    assert "Cache:\n- state cache: miss" in output
    assert "- projection store open:" in output
    assert "- cache metadata lookup + cached projection row load:" in output
    assert "- state cache miss path (full projection rebuild):" in output
    assert "- full projection rebuild:" in output
    assert "- event replay:" in output
    assert "- projection replay:" not in output
    assert "- snapshot save:" in output
    assert "- read-model build:" in output
    assert "- render:" in output
    assert "- total:" in output


def test_current_facts_timing_interpretation_keeps_measurements_unchanged():
    seed_local = load_seed_local_module()
    status = seed_local.StateCacheStatus(
        cache_hit=False,
        projection_version="test",
        snapshot_last_event_id="event-1",
        current_last_event_id="event-2",
        incremental_replay=True,
        events_applied=1,
    )
    diagnostics = seed_local.ProjectionBuildDiagnostics(
        timings=[("event replay", 0.125)]
    )

    interpretation = seed_local._CurrentFactsTimingInterpretation.from_cache_evidence(
        status, diagnostics
    )

    assert interpretation.cache_visibility.cache_status == "miss"
    assert (
        interpretation.cache_visibility.state_path_label
        == "state cache miss path (incremental event replay)"
    )
    assert interpretation.projection_timings == (("event replay", 0.125),)
    assert diagnostics.timings == [("event replay", 0.125)]


def test_current_facts_timing_diagnostic_payload_preserves_interpreted_evidence():
    seed_local = load_seed_local_module()
    interpretation = seed_local._CurrentFactsTimingInterpretation(
        cache_visibility=seed_local._CurrentFactsCacheVisibility(
            cache_status="miss",
            state_path_label="state cache miss path (incremental event replay)",
        ),
        projection_timings=(("event replay", 0.125),),
    )

    payload = seed_local._CurrentFactsTimingDiagnosticPayload.from_timing_interpretation(
        interpretation, 0.25
    )

    assert payload.cache_status == "miss"
    assert payload.timings == (
        ("state cache miss path (incremental event replay)", 0.25),
        ("event replay", 0.125),
    )


def test_current_facts_timing_presentation_formats_preserved_diagnostics():
    seed_local = load_seed_local_module()
    report = seed_local.CurrentFactsTimingReport(
        visibility=seed_local._CurrentFactsVisibilityPayload("example output"),
        diagnostics=seed_local._CurrentFactsDiagnosticPayload(
            "miss",
            [
                ("state cache miss path (incremental event replay)", 0.25),
                ("event replay", 0.125),
            ],
        ),
    )

    presentation = seed_local._CurrentFactsTimingPresentation.from_report(report)

    assert presentation.cache_status == "miss"
    assert presentation.timings == (
        ("state cache miss path (incremental event replay)", 0.25),
        ("event replay", 0.125),
    )
    assert presentation.format() == seed_local._format_current_facts_timing_report(report)
    assert presentation.format() == (
        "Current Facts Timing\n"
        "\n"
        "Cache:\n"
        "- state cache: miss\n"
        "\n"
        "Timings:\n"
        "- state cache miss path (incremental event replay): 0.250000s\n"
        "- event replay: 0.125000s"
    )
    assert not hasattr(presentation, "output")


def test_current_facts_cache_debug_keeps_visibility_payload_separate_from_diagnostics(
    tmp_path,
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-facts-debug-boundary.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", "example_host.local")],
    )
    args = seed_local.build_parser().parse_args(
        ["--db", str(db_path), "--current-facts-cache-debug"]
    )
    seed_local.validate_lifecycle_args(args, seed_local.build_parser())

    report = seed_local._current_facts_timing_from_args(args)

    assert report.output == report.visibility.output
    assert "example_host alias example_host.local" in report.visibility.output
    assert report.cache_status == report.diagnostics.cache_status
    assert report.timings == report.diagnostics.timings
    assert not hasattr(report.visibility, "timings")
    assert not hasattr(report.diagnostics, "output")


def test_cli_current_facts_cache_debug_warm_hit_labels_cached_projection_load(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-facts-debug-warm-hit.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", "example_host.local")],
    )

    assert seed_local.main(["--db", str(db_path), "--current-facts-cache-debug"]) == 0
    capsys.readouterr()

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        before_events = len(ledger.list_events("local"))
    finally:
        ledger.close()

    assert seed_local.main(["--db", str(db_path), "--current-facts-cache-debug"]) == 0

    output = capsys.readouterr().out
    assert "Cache:\n- state cache: hit" in output
    assert "- ledger open:" in output
    assert "- cache metadata lookup + cached projection row load:" in output
    assert "- cached projection load/materialize:" in output
    assert (
        "- state cache hit path (metadata validation + cached projection load):"
        in output
    )
    assert "- full projection rebuild:" not in output
    assert "- projection replay:" not in output
    assert "- read-model build:" in output
    assert "- stdout/output time:" in output

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        assert len(ledger.list_events("local")) == before_events
    finally:
        ledger.close()


def test_cli_current_facts_cache_debug_filtered_reports_fact_index_timing(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-facts-debug-fact-index.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", "example_host.local")],
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--current-selection",
                "example_host",
                "alias",
                "--current-facts-cache-debug",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert output.split("\n\nCurrent Facts Timing\n", 1)[0].endswith("\n\nexample_host.local")
    assert "- fact-index cache lookup/load:" in output
    assert "- fact-index build/load:" in output
    assert "- query/filter + render:" in output


def test_cli_current_facts_cache_debug_standalone_does_not_change_facts_returned(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-facts-debug-same-facts.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "alias", "192.0.2.115"),
            ("example_host", "alias", "192.168.254.116"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--current-selection", "example_host", "alias"]) == 0
    normal_output = capsys.readouterr().out

    assert "192.0.2.115" in normal_output
    assert "192.168.254.116" in normal_output


def test_cli_current_facts_cache_debug_filtered_legacy_behavior_remains_unchanged(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-facts-debug-filtered-legacy.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "alias", "192.0.2.115"),
            ("example_host", "alias", "192.168.254.116"),
        ],
    )

    assert (
        seed_local.main(
            ["--db", str(db_path), "--current-selection", "example_host", "alias"]
        )
        == 0
    )
    normal_output = capsys.readouterr().out

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--current-selection",
                "example_host",
                "alias",
                "--current-facts-cache-debug",
            ]
        )
        == 0
    )
    debug_output = capsys.readouterr().out
    debug_facts = debug_output.split("\n\nCurrent Facts Timing\n", 1)[0] + "\n"

    assert normal_output.endswith("\n\n192.0.2.115\n192.168.254.116\n")
    assert debug_facts == normal_output


def test_cli_fact_support_prints_projected_grouped_values(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact",
                "web_service",
                "runtime",
                "systemd",
                "--fact-support",
                "web_service",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: docker" in output
    assert "value: systemd" in output
    assert "aggregate_confidence: 0.9775" in output
    assert "aggregate_confidence: 0.85" in output
    assert "supporting_fact_ids: fact_obs_" in output
    assert "source_types: user" in output
    assert "first_observed:" in output
    assert "latest_observed:" in output


def test_cli_measurement_fact_support_hides_old_samples_by_default(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "example_host",
                "up",
                "0",
                "--fact",
                "example_host",
                "up",
                "1",
                "--fact-support",
                "example_host",
                "up",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: 1" in output
    assert "value: 0" not in output
    assert "support_kind: current_sample" in output
    assert "historical samples hidden" not in output


def test_cli_measurement_fact_support_include_history_shows_all_samples(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "example_host",
                "up",
                "0",
                "--fact",
                "example_host",
                "up",
                "1",
                "--fact",
                "example_host",
                "up",
                "1",
                "--fact-support",
                "example_host",
                "up",
                "--include-history",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: 0" in output
    assert output.count("value: 1") == 2
    assert output.count("support_kind: current_sample") == 3
    assert "historical samples hidden" not in output


def test_cli_availability_status_history_visibility_does_not_change_current(capsys):
    seed_local = load_seed_local_module()
    facts = [
        "--fact",
        "example_host",
        "availability_status",
        "up",
        "--fact",
        "example_host",
        "availability_status",
        "down",
    ]

    assert (
        seed_local.main(
            [*facts, "--fact-support", "example_host", "availability_status"]
        )
        == 0
    )
    default_output = capsys.readouterr().out
    assert "value: down" in default_output
    assert "value: up" not in default_output

    assert (
        seed_local.main(
            [
                *facts,
                "--fact-support",
                "example_host",
                "availability_status",
                "--include-history",
            ]
        )
        == 0
    )
    history_output = capsys.readouterr().out
    assert "value: up" in history_output
    assert "value: down" in history_output

    assert (
        seed_local.main([*facts, "--best-fact", "example_host", "availability_status"])
        == 0
    )
    best_output = capsys.readouterr().out
    assert "value: down" in best_output
    assert "value: up" not in best_output


def test_cli_durable_runtime_fact_support_still_shows_all_conflicting_values(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact",
                "web_service",
                "runtime",
                "systemd",
                "--fact-support",
                "web_service",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: docker" in output
    assert "value: systemd" in output
    assert output.count("support_kind: aggregate") == 2
    assert "historical samples hidden" not in output


def test_cli_best_fact_prints_projected_current_belief(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact",
                "web_service",
                "runtime",
                "systemd",
                "--best-fact",
                "web_service",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: web_service" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "confidence: 0.9775" in output
    assert "reason: best-supported current belief" in output
    assert "support_count: 2" in output


def test_cli_fact_conflicts_prints_projected_active_conflicts_and_winner(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact",
                "web_service",
                "runtime",
                "systemd",
                "--fact-conflicts",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: web_service" in output
    assert "predicate: runtime" in output
    assert "values: docker, systemd" in output
    assert "winning_value: docker" in output
    assert "winning_fact_id: fact_obs_" in output
    assert "conflicting_fact_ids: fact_obs_" in output
    assert "reason: multiple values for web_service/runtime" in output


def test_parser_supports_fact_expiry_options():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()

    expires_args = parser.parse_args(
        [
            "--fact",
            "web_service",
            "runtime",
            "docker",
            "--fact-expires-at",
            "2026-01-01T00:00:00+00:00",
        ]
    )
    ttl_args = parser.parse_args(
        [
            "--fact",
            "web_service",
            "runtime",
            "docker",
            "--fact-ttl-seconds",
            "60",
        ]
    )

    assert expires_args.fact_expires_at == "2026-01-01T00:00:00+00:00"
    assert ttl_args.fact_ttl_seconds == 60


def test_cli_fact_ttl_can_expire_seeded_fact(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--best-fact",
                "web_service",
                "runtime",
            ]
        )
        == 0
    )

    assert (
        capsys.readouterr().out.strip() == "no current belief for web_service runtime"
    )


def test_cli_fact_expires_at_keeps_unexpired_seeded_fact(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact-expires-at",
                "2999-01-01T00:00:00+00:00",
                "--best-fact",
                "web_service",
                "runtime",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: web_service" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output


def test_cli_expired_fact_hidden_by_default(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--fact-support",
                "web_service",
                "runtime",
            ]
        )
        == 0
    )

    assert capsys.readouterr().out.strip().endswith("no fact support for web_service runtime")


def test_cli_expired_fact_visible_with_include_expired(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--fact-support",
                "web_service",
                "runtime",
                "--include-expired",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "value: docker" in output
    assert "expired: true" in output
    assert "expires_at:" in output


def test_cli_stale_facts_prints_expired_facts(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--stale-facts",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: web_service" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "source_type: user" in output
    assert "confidence: 1.0" in output
    assert "expired: true" in output
    assert "expires_at:" in output


def test_cli_stale_fact_refreshes_recommend_service_inspection_for_runtime(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--fact-ttl-seconds",
                "0",
                "--stale-fact-refreshes",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: web_service" in output
    assert "predicate: runtime" in output
    assert "value: docker" in output
    assert "recommended_capability: service_inspection" in output
    assert "reason: predicate 'runtime' maps to 'service_inspection'" in output


def test_cli_stale_fact_refreshes_recommend_environment_inventory_for_host(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "host",
                "example_host",
                "--fact-ttl-seconds",
                "0",
                "--stale-fact-refreshes",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "subject: web_service" in output
    assert "predicate: host" in output
    assert "value: example_host" in output
    assert "recommended_capability: environment_inventory" in output
    assert "reason: predicate 'host' maps to 'environment_inventory'" in output


def test_cli_stale_fact_refreshes_fall_back_to_knowledge_lookup(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "unknown_predicate",
                "mystery",
                "--fact-ttl-seconds",
                "0",
                "--stale-fact-refreshes",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "predicate: unknown_predicate" in output
    assert "value: mystery" in output
    assert "recommended_capability: knowledge_lookup" in output
    assert "reason: predicate 'unknown_predicate' maps to 'knowledge_lookup'" in output


def test_parser_accepts_json_observation_diff_option():
    seed_local = load_seed_local_module()
    args = seed_local.build_parser().parse_args(
        ["--diff-observations-json", "inventory.json"]
    )

    assert args.diff_observations_json == "inventory.json"


def test_cli_diff_observations_json_does_not_ingest_inventory(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.db"
    json_path = tmp_path / "observations.json"
    json_path.write_text(
        '{"observations":[{"subject":"web_service","predicate":"runtime",'
        '"value":"docker"}]}',
        encoding="utf-8",
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--diff-observations-json",
                str(json_path),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "new_facts: 1" in output
    assert "matching_facts: 0" in output
    assert (
        seed_local.main(
            ["--db", str(db_path), "--fact-support", "web_service", "runtime"]
        )
        == 0
    )
    support_output = capsys.readouterr().out
    assert "no fact support for web_service runtime" in support_output


def test_cli_observe_local_host_prints_count_and_summary(monkeypatch, capsys):
    seed_local = load_seed_local_module()

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            return [
                seed_local.Observation(
                    id="obs_cli_local",
                    source_type="discovery",
                    observed_at=seed_local.utc_now(),
                    subject="node-a",
                    predicate="os",
                    value="linux",
                )
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--observe-local-host"]) == 0

    output = capsys.readouterr().out
    assert "ingested 1 observation(s)" in output
    assert "subject: node-a" in output
    assert "predicate: os" in output
    assert "source_type: discovery" in output


def test_cli_observe_local_host_timings_are_comparable_and_non_semantic(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            return [
                seed_local.Observation(
                    id="obs_cli_local_timing",
                    source_type="discovery",
                    observed_at=seed_local.utc_now(),
                    subject="node-a",
                    predicate="os",
                    value="linux",
                )
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)
    plain_db = tmp_path / "plain.sqlite"
    timing_db = tmp_path / "timing.sqlite"

    assert seed_local.main(["--db", str(plain_db), "--observe-local-host"]) == 0
    plain_output = capsys.readouterr().out
    assert "Observation ingestion timings:" not in plain_output

    assert (
        seed_local.main(
            ["--db", str(timing_db), "--observe-local-host", "--observe-timings"]
        )
        == 0
    )
    timing_output = capsys.readouterr().out
    assert "Observation ingestion timings:" in timing_output
    assert "source collection:" in timing_output
    assert "normalization:" in timing_output
    assert "event generation + ledger write:" in timing_output
    assert "total observations: 1" in timing_output
    assert "total events: 3" in timing_output

    plain_events = seed_local.SQLiteEventLedger(str(plain_db)).list_events()
    timing_events = seed_local.SQLiteEventLedger(str(timing_db)).list_events()
    assert [event.kind for event in timing_events] == [
        event.kind for event in plain_events
    ]


def test_cli_observe_local_host_quiet_output_suppresses_rendering_only(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "quiet-local.sqlite"
    collected = {"count": 0}

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            collected["count"] += 1
            return [
                seed_local.Observation(
                    id="obs_cli_local_quiet",
                    source_type="discovery",
                    observed_at=seed_local.utc_now(),
                    subject="node-a",
                    predicate="os",
                    value="linux",
                )
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert (
        seed_local.main(
            ["--db", str(db_path), "--observe-local-host", "--quiet-output"]
        )
        == 0
    )
    captured = capsys.readouterr()

    assert collected["count"] == 1
    assert captured.out == ""
    assert "Collecting fake-local-host observations" in captured.err
    assert "Collected 1 observations." in captured.err
    assert "Normalizing fake-local-host observations" in captured.err
    assert "Normalized 1 observations." in captured.err
    assert "Ingesting fake-local-host observations" in captured.err
    assert "Writing events" in captured.err
    assert "Done." in captured.err

    assert (
        seed_local.main(["--db", str(db_path), "--current-selection", "node-a", "os"]) == 0
    )
    facts_output = capsys.readouterr().out
    assert "linux" in facts_output

    assert seed_local.main(["--db", str(db_path), "--events"]) == 0
    events_output = capsys.readouterr().out
    assert "observation.observed" in events_output
    assert "evidence.observed" in events_output
    assert "fact.observed" in events_output


def test_cli_observe_repository_source_quiet_output_suppresses_rendering_only(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "quiet-repository-source.sqlite"
    repo_path = tmp_path / "repo"
    source_dir = repo_path / "seed_runtime"
    source_dir.mkdir(parents=True)
    (source_dir / "state.py").write_text(
        "from seed_runtime.projection_store import project_state_with_cache\n"
        "class StateProjector:\n"
        "    pass\n",
        encoding="utf-8",
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-repository-source",
                str(repo_path),
                "--quiet-output",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()

    assert captured.out == ""
    assert "Collecting repository_source observations" in captured.err
    assert "Normalizing repository_source observations" in captured.err
    assert "Ingesting repository_source observations" in captured.err
    assert "Writing events" in captured.err
    assert "Done." in captured.err

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--current-selection",
                "seed_runtime.state",
                "defines",
            ]
        )
        == 0
    )
    facts_output = capsys.readouterr().out
    assert "seed_runtime.state.StateProjector" in facts_output

    assert seed_local.main(["--db", str(db_path), "--events"]) == 0
    events_output = capsys.readouterr().out
    assert "observation.observed" in events_output
    assert "evidence.observed" in events_output
    assert "fact.observed" in events_output


def test_cli_local_network_facts_appear_in_current_facts_and_impact(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            observed_at = seed_local.utc_now()
            return [
                seed_local.Observation(
                    id="obs_network_interface",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="network_interface",
                    value="eth0",
                    dimensions={"interface": "eth0"},
                ),
                seed_local.Observation(
                    id="obs_network_role",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="interface_role",
                    value="primary",
                    dimensions={"interface": "eth0"},
                ),
                seed_local.Observation(
                    id="obs_network_ip",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="ip_address",
                    value="192.168.2.5",
                    dimensions={"interface": "eth0", "address_family": "ipv4"},
                ),
                seed_local.Observation(
                    id="obs_docker_interface",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="network_interface",
                    value="docker0",
                    dimensions={"interface": "docker0"},
                ),
                seed_local.Observation(
                    id="obs_docker_role",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="interface_role",
                    value="container",
                    dimensions={"interface": "docker0"},
                ),
                seed_local.Observation(
                    id="obs_docker_ip",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="ip_address",
                    value="172.17.0.1",
                    dimensions={"interface": "docker0", "address_family": "ipv4"},
                ),
                seed_local.Observation(
                    id="obs_network_ipv6_global",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="ip_address",
                    value="2001:db8::5",
                    dimensions={"interface": "eth0", "address_family": "ipv6"},
                ),
                seed_local.Observation(
                    id="obs_network_ipv6_link_local",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="ip_address",
                    value="fe80::5",
                    dimensions={"interface": "eth0", "address_family": "ipv6"},
                ),
                seed_local.Observation(
                    id="obs_network_gateway",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="default_gateway",
                    value="192.168.2.1",
                    dimensions={"interface": "eth0", "address_family": "ipv4"},
                ),
                seed_local.Observation(
                    id="obs_network_dns",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="dns_resolver",
                    value="1.1.1.1",
                    dimensions={"source": "/etc/resolv.conf"},
                ),
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--db", str(db_path), "--observe-local-host"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--current-selection", "example_host", "ip_address"]) == 0
    current_output = capsys.readouterr().out
    assert "192.168.2.5 (address_family=ipv4, interface=eth0)" in current_output
    assert "2001:db8::5 (address_family=ipv6, interface=eth0)" in current_output
    assert "fe80::5 (address_family=ipv6, interface=eth0)" in current_output
    assert "172.17.0.1 (address_family=ipv4, interface=docker0)" in current_output

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0
    impact_output = capsys.readouterr().out
    assert "availability_status: unknown" in impact_output
    assert "local network configuration:" in impact_output
    assert "aliases:\n- none" in impact_output
    assert "- primary/default-route interface eth0:" in impact_output
    assert "  ipv4: 192.168.2.5" in impact_output
    assert "  ipv6_global: 2001:db8::5" in impact_output
    assert "  ipv6_link_local: fe80::5" in impact_output
    assert "  default_gateway_ipv4: 192.168.2.1" in impact_output
    assert "default_gateway=2001:db8::5" not in impact_output
    assert (
        "- virtual/container/vpn interfaces: 1 collapsed (container=1)" in impact_output
    )
    assert "docker0: 172.17.0.1" not in impact_output
    assert (
        "- reachability/availability: not inferred from local network facts"
        in impact_output
    )
    assert "- dns_resolver (source=/etc/resolv.conf): 1.1.1.1" in impact_output


def test_cli_mount_facts_appear_in_current_facts_and_impact(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "mounts.sqlite"

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            observed_at = seed_local.utc_now()
            return [
                seed_local.Observation(
                    id="obs_mount_point",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="mount_point",
                    value="/",
                    dimensions={"mount_point": "/"},
                ),
                seed_local.Observation(
                    id="obs_filesystem_type",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="filesystem_type",
                    value="ext4",
                    dimensions={"mount_point": "/"},
                ),
                seed_local.Observation(
                    id="obs_mounted_device",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="mounted_device",
                    value="/dev/sda1",
                    dimensions={"mount_point": "/"},
                ),
                seed_local.Observation(
                    id="obs_mount_option_rw",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="mount_option",
                    value="rw",
                    dimensions={"mount_point": "/", "mount_option": "rw"},
                ),
                seed_local.Observation(
                    id="obs_mount_option_relatime",
                    source_type="discovery",
                    observed_at=observed_at,
                    subject="example_host",
                    predicate="mount_option",
                    value="relatime",
                    dimensions={"mount_point": "/", "mount_option": "relatime"},
                ),
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--db", str(db_path), "--observe-local-host"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--db", str(db_path), "--current-selection", "example_host", "mount_option"]) == 0
    current_output = capsys.readouterr().out
    assert "rw (mount_option=rw, mount_point=/)" in current_output
    assert "relatime (mount_option=relatime, mount_point=/)" in current_output

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0
    impact_output = capsys.readouterr().out
    assert "mounts:" in impact_output
    assert "- /: device=/dev/sda1 type=ext4" in impact_output
    assert "  options: relatime, rw" in impact_output
    assert (
        "- health/availability/reachability: not inferred from mount facts"
        in impact_output
    )
    assert "availability_status: unknown" in impact_output
    assert "reachability_status" not in impact_output


def test_format_mount_impact_renders_runtime_mount_groups():
    seed_local = load_seed_local_module()
    observed_at = seed_local.utc_now()

    def mount_facts(index, mount_point, device, fs_type, options=("rw",)):
        return [
            seed_local.Fact(
                id=f"fact_mount_point_{index}",
                subject_id="example_host",
                predicate="mount_point",
                value=mount_point,
                dimensions={"mount_point": mount_point},
                source_type="discovery",
                observed_at=observed_at,
            ),
            seed_local.Fact(
                id=f"fact_mount_device_{index}",
                subject_id="example_host",
                predicate="mounted_device",
                value=device,
                dimensions={"mount_point": mount_point},
                source_type="discovery",
                observed_at=observed_at,
            ),
            seed_local.Fact(
                id=f"fact_mount_type_{index}",
                subject_id="example_host",
                predicate="filesystem_type",
                value=fs_type,
                dimensions={"mount_point": mount_point},
                source_type="discovery",
                observed_at=observed_at,
            ),
            *(
                seed_local.Fact(
                    id=f"fact_mount_option_{index}_{option}",
                    subject_id="example_host",
                    predicate="mount_option",
                    value=option,
                    dimensions={"mount_point": mount_point, "mount_option": option},
                    source_type="discovery",
                    observed_at=observed_at,
                )
                for option in options
            ),
        ]

    facts = []
    for index, mount in enumerate(
        [
            ("/var/lib/docker/overlay2/a/merged", "overlay", "overlay"),
            ("/var/lib/docker/overlay2/b/merged", "overlay", "overlay"),
            ("/run/docker/netns/abc", "nsfs", "nsfs"),
            ("/proc", "proc", "proc"),
            ("/run/credentials/systemd-sysusers.service", "ramfs", "ramfs"),
            ("/", "/dev/mapper/root", "ext4"),
            ("/mnt/merged", "mergerfs", "fuse.mergerfs"),
        ]
    ):
        facts.extend(mount_facts(index, *mount))

    output = "\n".join(seed_local._format_mount_impact(facts))

    assert output.index("- /: device=/dev/mapper/root type=ext4") < output.index(
        "- /mnt/merged: device=mergerfs type=fuse.mergerfs"
    )
    assert "- docker overlay mounts: 2 collapsed" in output
    assert "- docker netns mounts: 1 collapsed" in output
    assert "- system/pseudo mounts: 1 collapsed" in output
    assert "- systemd credential mounts: 1 collapsed" in output
    assert "- full mount evidence: use --fact-support" in output
    assert "- health/availability/reachability: not inferred from mount facts" in output
    assert "/var/lib/docker/overlay2/a/merged" not in output
    assert "/run/docker/netns/abc" not in output
    assert "- /proc:" not in output


def test_cli_events_without_message_lists_persisted_events_and_exits(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe",
                "example_host",
                "architecture",
                "x86_64",
            ]
        )
        == 0
    )
    capsys.readouterr()


    assert seed_local.main(["--db", str(db_path), "--events"]) == 0

    output = capsys.readouterr().out
    assert "Events: 3" in output
    assert "kind=observation.observed" in output
    assert "kind=evidence.observed" in output
    assert "evidence_id=evd_obs_" in output
    assert "kind=fact.observed" in output
    assert output.count("subject=example_host predicate=architecture") == 2


def test_sqlite_observation_reopen_projects_best_fact_and_fact_support(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    class FakeLocalSource:
        source_type = "discovery"
        name = "fake-local-host"

        def collect(self):
            return [
                seed_local.Observation(
                    id="obs_cli_local_architecture",
                    source_type="discovery",
                    observed_at=seed_local.utc_now(),
                    subject="example_host",
                    predicate="architecture",
                    value="x86_64",
                )
            ]

    monkeypatch.setattr(seed_local, "LocalHostObservationSource", FakeLocalSource)

    assert seed_local.main(["--db", str(db_path), "--observe-local-host"]) == 0
    ingest_output = capsys.readouterr().out
    assert "subject: example_host" in ingest_output
    assert "predicate: architecture" in ingest_output
    assert "value: x86_64" in ingest_output

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        events = ledger.list_events(seed_local.DEFAULT_WORKSPACE)
        assert [event.kind for event in events] == [
            "observation.observed",
            "evidence.observed",
            "fact.observed",
        ]
        persisted_fact_payload = events[-1].payload["fact"]
        assert persisted_fact_payload["subject_id"] == "example_host"
        assert persisted_fact_payload["predicate"] == "architecture"
        assert persisted_fact_payload["value"] == "x86_64"

        state = seed_local.StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
        projected_best = state.get_best_fact("example_host", "architecture")
        assert projected_best is not None
        assert projected_best.value == "x86_64"
        projected_support = state.get_fact_support("example_host", "architecture")
        assert projected_support is not None
        assert projected_support.value == "x86_64"
        assert projected_support.supporting_fact_ids == [projected_best.id]
    finally:
        ledger.close()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", "example_host", "architecture"]
        )
        == 0
    )
    best_output = capsys.readouterr().out
    assert "subject: example_host" in best_output
    assert "predicate: architecture" in best_output
    assert "value: x86_64" in best_output
    assert "no current belief" not in best_output

    assert (
        seed_local.main(
            ["--db", str(db_path), "--fact-support", "example_host", "architecture"]
        )
        == 0
    )
    support_output = capsys.readouterr().out
    assert "value: x86_64" in support_output
    assert "supporting_fact_ids: fact_obs_" in support_output
    assert "source_types: discovery" in support_output


def test_best_fact_accepts_short_hostname_for_persisted_fqdn_observation(tmp_path):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        seed_local.ingest_observations(
            ledger,
            seed_local.DEFAULT_WORKSPACE,
            [
                seed_local.DevObservationSeed(
                    "example_host.example.test",
                    "architecture",
                    "x86_64",
                    source_type="discovery",
                )
            ],
        )
    finally:
        ledger.close()

    reopened = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(reopened).project(
            seed_local.DEFAULT_WORKSPACE
        )
        assert state.get_best_fact("example_host", "architecture").value == "x86_64"
        assert state.get_fact_support("example_host", "architecture").value == "x86_64"
    finally:
        reopened.close()


def test_ingest_observations_batches_consecutive_cli_observations():
    seed_local = load_seed_local_module()

    class CountingLedger(seed_local.EventLedger):
        def __init__(self):
            super().__init__()
            self.append_many_calls = 0

        def append_many(self, events):
            self.append_many_calls += 1
            return super().append_many(events)

    ledger = CountingLedger()

    facts = seed_local.ingest_observations(
        ledger,
        seed_local.DEFAULT_WORKSPACE,
        [
            seed_local.DevObservationSeed(
                "example_host",
                "architecture",
                "x86_64",
                source_type="discovery",
            ),
            seed_local.DevObservationSeed(
                "example_host",
                "runtime",
                "docker",
                source_type="discovery",
            ),
        ],
    )

    assert len(facts) == 2
    assert ledger.append_many_calls == 1
    assert [
        event.kind for event in ledger.list_events(seed_local.DEFAULT_WORKSPACE)
    ] == [
        "observation.observed",
        "evidence.observed",
        "fact.observed",
        "observation.observed",
        "evidence.observed",
        "fact.observed",
    ]


def _patch_fake_prometheus_source(monkeypatch, seed_local):
    class FakePrometheusSource:
        source_type = "provider"

        def __init__(self, base_url, *, timeout_seconds):
            self.name = f"fake-prometheus:{base_url}"
            self.base_url = base_url
            self.timeout_seconds = timeout_seconds

        def collect(self):
            observed_at = seed_local.utc_now()
            return [
                seed_local.Observation(
                    id="obs_cli_prometheus_up_a",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-a:9100",
                    predicate="up",
                    value=1,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {"instance": "node-a:9100"},
                    },
                ),
                seed_local.Observation(
                    id="obs_cli_prometheus_avail_a_root",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-a:9100",
                    predicate="filesystem_avail_bytes",
                    value=100,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {
                            "instance": "node-a:9100",
                            "mountpoint": "/",
                        },
                    },
                ),
                seed_local.Observation(
                    id="obs_cli_prometheus_size_a_data",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-a:9100",
                    predicate="filesystem_size_bytes",
                    value=200,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {
                            "instance": "node-a:9100",
                            "mountpoint": "/data",
                        },
                    },
                ),
                seed_local.Observation(
                    id="obs_cli_prometheus_up_b",
                    source_type="provider",
                    observed_at=observed_at,
                    subject="node-b:9100",
                    predicate="up",
                    value=0,
                    metadata={
                        "source_name": "prometheus",
                        "metric_labels": {"instance": "node-b:9100"},
                    },
                ),
            ]

    monkeypatch.setattr(seed_local, "PrometheusObservationSource", FakePrometheusSource)


def test_cli_observe_prometheus_prints_summary_by_default(monkeypatch, capsys):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)

    assert (
        seed_local.main(
            [
                "--observe-prometheus",
                "http://prom.example:9090",
                "--observe-timeout",
                "3",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 8 observation(s)" in output
    assert "hosts/instances discovered: node-a:9100, node-b:9100" in output
    assert "counts by predicate:" in output
    assert "- availability_status: 2" in output
    assert "- filesystem_avail_bytes: 1" in output
    assert "- filesystem_free_bytes: 1" in output
    assert "- filesystem_size_bytes: 1" in output
    assert "- filesystem_total_bytes: 1" in output
    assert "- up: 2" in output
    assert "fact_id:" not in output


def test_cli_observe_prometheus_verbose_prints_every_fact(monkeypatch, capsys):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)

    assert (
        seed_local.main(
            [
                "--observe-prometheus",
                "http://prom.example:9090",
                "--verbose-observations",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 8 observation(s)" in output
    assert "fact_id: fact_obs_" in output
    assert "subject: node-a:9100" in output
    assert "subject: node-b:9100" in output
    assert "predicate: availability_status" in output
    assert "predicate: filesystem_avail_bytes" in output
    assert "predicate: filesystem_free_bytes" in output
    assert "predicate: filesystem_total_bytes" in output
    assert "hosts/instances discovered:" not in output


@pytest.mark.parametrize(
    ("instance", "expected"), [("node-a:9100", "up"), ("node-b:9100", "down")]
)
def test_cli_observe_prometheus_supports_canonical_availability_best_fact(
    monkeypatch, tmp_path, capsys, instance, expected
):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-prometheus",
                "http://prom.example:9090",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", instance, "availability_status"]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert f"subject: {instance}" in output
    assert "predicate: availability_status" in output
    assert f"value: {expected}" in output


def test_cli_observe_prometheus_instance_filter_limits_ingestion(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-prometheus",
                "http://prom.example:9090",
                "--prometheus-instance",
                "node-b:9100",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 2 observation(s)" in output
    assert "hosts/instances discovered: node-b:9100" in output
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()
    assert {fact.subject_id for fact in state.facts.values()} == {"node-b:9100"}
    assert {(fact.predicate, fact.value) for fact in state.facts.values()} == {
        ("up", 0),
        ("availability_status", "down"),
        ("health_status", "degraded"),
    }


def test_cli_observe_prometheus_mountpoint_filter_limits_ingestion(
    monkeypatch, tmp_path, capsys
):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-prometheus",
                "http://prom.example:9090",
                "--prometheus-mountpoint",
                "/data",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "ingested 2 observation(s)" in output
    assert "hosts/instances discovered: node-a:9100" in output
    assert "- filesystem_size_bytes: 1" in output
    assert "- filesystem_total_bytes: 1" in output
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(ledger).project(seed_local.DEFAULT_WORKSPACE)
    finally:
        ledger.close()
    facts = list(state.facts.values())
    assert len(facts) == 2
    assert {fact.subject_id for fact in facts} == {"node-a:9100"}
    assert {fact.predicate for fact in facts} == {
        "filesystem_size_bytes",
        "filesystem_total_bytes",
    }


def test_cli_alias_to_endpoint_does_not_resolve_host_best_fact_after_sqlite_reopen(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "192.0.2.115:9100",
                "up",
                "1",
                "--alias",
                "example_host",
                "192.0.2.115:9100",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(["--db", str(db_path), "--best-fact", "example_host", "up"])
        == 0
    )
    assert capsys.readouterr().out == "no current belief for example_host up\n"

    assert (
        seed_local.main(["--db", str(db_path), "--best-fact", "192.0.2.115:9100", "up"])
        == 0
    )
    output = capsys.readouterr().out
    assert "subject: 192.0.2.115:9100" in output
    assert "predicate: up" in output
    assert "value: 1" in output

    reopened = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(reopened).project(
            seed_local.DEFAULT_WORKSPACE
        )
        support = state.get_fact_support("192.0.2.115:9100", "up")
        best = state.get_best_fact("192.0.2.115:9100", "up")
        host_best = state.get_best_fact("example_host", "up")
    finally:
        reopened.close()

    assert host_best is None
    assert best is not None
    assert best.subject_id == "192.0.2.115:9100"
    assert support is not None
    assert support.supporting_fact_ids == [best.id]


def test_cli_alias_does_not_flatten_endpoint_availability_best_fact(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "192.0.2.115:9100",
                "availability_status",
                "down",
                "--alias",
                "example_host",
                "192.0.2.115:9100",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", "example_host", "availability_status"]
        )
        == 0
    )
    assert capsys.readouterr().out == (
        "no current belief for example_host availability_status\n"
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--best-fact",
                "192.0.2.115:9100",
                "availability_status",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "subject: 192.0.2.115:9100" in output
    assert "predicate: availability_status" in output
    assert "value: down" in output


def test_cli_alias_records_alias_observation_fact(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--alias", "example_host", "192.0.2.115:9100"]) == 0

    output = capsys.readouterr().out
    assert "subject: example_host" in output
    assert "predicate: alias" in output
    assert "value: 192.0.2.115:9100" in output


def _group_member_fact(seed_local, fact_id, value, dimensions):
    return seed_local.Fact(
        id=fact_id,
        subject_id="example_host",
        predicate="group_member",
        value=value,
        dimensions=dimensions,
        source_type="discovery",
        observed_at=seed_local.utc_now(),
    )


def test_cli_current_facts_render_dimensions_for_group_member_facts():
    seed_local = load_seed_local_module()
    state = seed_local.State(workspace_id="ws")
    state.facts = {
        "fact_sudo": _group_member_fact(
            seed_local,
            "fact_sudo",
            "user",
            {"username": "user", "groupname": "sudo", "gid": "27"},
        ),
        "fact_docker": _group_member_fact(
            seed_local,
            "fact_docker",
            "user",
            {"username": "user", "gid": "999", "groupname": "docker"},
        ),
    }

    output = seed_local.format_current_facts(state, "example_host", "group_member")

    assert output.splitlines()[-2:] == [
        "user (gid=27, groupname=sudo, username=user)",
        "user (gid=999, groupname=docker, username=user)",
    ]


def test_cli_current_facts_dimensionless_output_is_unchanged():
    seed_local = load_seed_local_module()
    state = seed_local.State(workspace_id="ws")
    observed_at = seed_local.utc_now()
    state.facts = {
        "fact_alias_1": seed_local.Fact(
            id="fact_alias_1",
            subject_id="example_host",
            predicate="alias",
            value="example_host.local",
            source_type="imported",
            observed_at=observed_at,
        ),
        "fact_alias_2": seed_local.Fact(
            id="fact_alias_2",
            subject_id="example_host",
            predicate="alias",
            value="192.168.1.115",
            source_type="imported",
            observed_at=observed_at,
        ),
    }

    assert seed_local.format_current_facts(state, "example_host", "alias").endswith(
        "\n\n192.168.1.115\nexample_host.local"
    )


def test_cli_fact_support_renders_dimensions_for_group_member_facts():
    seed_local = load_seed_local_module()
    observed_at = seed_local.utc_now()
    supports = [
        seed_local.FactSupport(
            subject="example_host",
            predicate="group_member",
            value="user",
            dimensions={"username": "user", "groupname": "sudo", "gid": "27"},
            supporting_fact_ids=["fact_sudo"],
            source_types=["discovery"],
            confidence=0.95,
            observed_at=observed_at,
            latest_observed_at=observed_at,
        ),
        seed_local.FactSupport(
            subject="example_host",
            predicate="group_member",
            value="user",
            dimensions={"username": "user", "gid": "999", "groupname": "docker"},
            supporting_fact_ids=["fact_docker"],
            source_types=["discovery"],
            confidence=0.95,
            observed_at=observed_at,
            latest_observed_at=observed_at,
        ),
    ]

    output = seed_local.format_fact_supports(supports, "example_host", "group_member")

    assert "value: user\ndimensions: gid=27, groupname=sudo, username=user" in output
    assert "value: user\ndimensions: gid=999, groupname=docker, username=user" in output


def test_cli_fact_support_dimensionless_output_has_no_dimensions_line():
    seed_local = load_seed_local_module()
    observed_at = seed_local.utc_now()
    supports = [
        seed_local.FactSupport(
            subject="node",
            predicate="up",
            value=1,
            supporting_fact_ids=["fact_up_new"],
            source_types=["provider"],
            confidence=0.85,
            observed_at=observed_at,
            latest_observed_at=observed_at,
            predicate_semantics="measurement",
            support_kind="current_sample",
        )
    ]

    output = seed_local.format_fact_supports(supports, "node", "up")

    assert "value: 1\nsemantics: measurement" in output
    assert "dimensions:" not in output


def test_cli_fact_support_marks_measurement_current_sample():
    seed_local = load_seed_local_module()
    supports = [
        seed_local.FactSupport(
            subject="node",
            predicate="up",
            value=1,
            supporting_fact_ids=["fact_up_new"],
            source_types=["provider"],
            confidence=0.85,
            observed_at=seed_local.datetime(2026, 1, 1),
            latest_observed_at=seed_local.datetime(2026, 1, 1),
            predicate_semantics="measurement",
            support_kind="current_sample",
        )
    ]

    output = seed_local.format_fact_supports(supports, "node", "up")

    assert "semantics: measurement" in output
    assert "support_kind: current_sample" in output


def test_cli_observe_ansible_inventory_ingests_identity_observations(tmp_path, capsys):
    seed_local = load_seed_local_module()
    inventory_path = tmp_path / "inventory.ini"
    inventory_path.write_text(
        "[nodegroup]\nexample_host ansible_host=192.0.2.115\n", encoding="utf-8"
    )

    assert seed_local.main(["--observe-ansible-inventory", str(inventory_path)]) == 0

    output = capsys.readouterr().out
    assert "subject: example_host" in output
    assert "predicate: hostname" in output
    assert "predicate: ip_address" in output
    assert "predicate: alias" in output
    assert "predicate: group" in output


def test_cli_ansible_inventory_and_prometheus_support_best_fact(
    tmp_path, monkeypatch, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "seed.sqlite"
    inventory_path = tmp_path / "inventory.yaml"
    inventory_path.write_text(
        """all:
  hosts:
    example_host:
      ansible_host: 192.0.2.115
""",
        encoding="utf-8",
    )

    class FakePrometheusSource:
        source_type = "provider"
        name = "prometheus"

        def __init__(self, base_url, timeout_seconds=5.0):
            self.base_url = base_url
            self.timeout_seconds = timeout_seconds

        def collect(self):
            from datetime import datetime, timezone
            from seed_runtime.observations import Observation

            return [
                Observation(
                    id="obs_cli_ansible_prometheus",
                    source_type="provider",
                    observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    subject="192.0.2.115:9100",
                    predicate="up",
                    value=0,
                    confidence=0.95,
                    metadata={"source_name": "prometheus"},
                )
            ]

    monkeypatch.setattr(seed_local, "PrometheusObservationSource", FakePrometheusSource)

    assert (
        seed_local.main(
            ["--db", str(db_path), "--observe-ansible-inventory", str(inventory_path)]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        seed_local.main(
            ["--db", str(db_path), "--observe-prometheus", "http://prom.example:9090"]
        )
        == 0
    )
    capsys.readouterr()

    reopened = seed_local.SQLiteEventLedger(str(db_path))
    try:
        state = seed_local.StateProjector(reopened).project(
            seed_local.DEFAULT_WORKSPACE
        )
    finally:
        reopened.close()
    assert any(
        fact.subject_id == "example_host"
        and fact.predicate == "alias"
        and fact.value == "192.0.2.115:9100"
        for fact in state.facts.values()
    )

    assert (
        seed_local.main(
            ["--db", str(db_path), "--best-fact", "example_host", "availability_status"]
        )
        == 0
    )
    assert capsys.readouterr().out == (
        "no current belief for example_host availability_status\n"
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--best-fact",
                "192.0.2.115:9100",
                "availability_status",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "subject: 192.0.2.115:9100" in output
    assert "predicate: availability_status" in output
    assert "value: down" in output


def test_cli_entity_type_projection_queries():
    seed_local = load_seed_local_module()
    parser = seed_local.build_parser()

    assert parser.parse_args(["--entity-types"]).entity_types is True
    assert (
        parser.parse_args(["--entity-type", "example_host"]).entity_type
        == "example_host"
    )
    state = seed_local.State(workspace_id="ws")
    assert (
        seed_local.format_entity_types(state, "example_host") == "example_host: unknown"
    )


def _persist_impact_facts(seed_local, db_path, facts):
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        for index, (subject, predicate, value) in enumerate(facts):
            fact = seed_local.Fact(
                id=f"fact_impact_{index}",
                subject_id=subject,
                predicate=predicate,
                value=value,
                source_type="imported",
                confidence=0.9,
                evidence_ids=[],
                observed_at=seed_local.utc_now(),
            )
            ledger.append(
                "fact.observed",
                seed_local.DEFAULT_WORKSPACE,
                {"fact": seed_local.to_plain(fact)},
            )
    finally:
        ledger.close()


def test_cli_impact_reports_local_observation_without_availability(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-local-observation.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "local_observation_status", "observed"),
            ("example_host", "os", "linux"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0

    output = capsys.readouterr().out
    assert "local_observation_status: observed" in output
    assert "availability_status: unknown" in output
    assert "endpoint availability by role:\n- none" in output


def test_cli_impact_keeps_endpoint_alias_availability_on_endpoint(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-alias.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "os", "linux"),
            ("example_host", "alias", "192.0.2.115:9100"),
            ("192.0.2.115:9100", "availability_status", "up"),
            ("example_host", "group", "servers"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "192.0.2.115:9100"]) == 0

    output = capsys.readouterr().out
    assert "entity: 192.0.2.115:9100" in output
    assert "entity types: endpoint" in output
    assert "aliases:\n- none" in output
    assert "availability_status: up" in output
    assert "groups/member_of: none" in output


def test_cli_impact_reports_service_running_on_host_as_dependent(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-dependent.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "os", "linux"), ("web_service", "runs_on", "example_host")],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0

    assert "dependents: web_service" in capsys.readouterr().out


def test_cli_impact_includes_active_conflicts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-conflict.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("web_service", "runtime", "docker"), ("web_service", "runtime", "systemd")],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "web_service"]) == 0

    output = capsys.readouterr().out
    assert "active conflicts:" in output
    assert "- runtime: values=docker, systemd; winning=none" in output


def test_cli_current_facts_and_impact_keep_all_aliases_without_conflict(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "multi-alias.sqlite"
    aliases = [
        "192.0.2.115",
        "192.0.2.115:9100",
        "192.0.2.115:9200",
    ]
    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", alias) for alias in aliases],
    )

    assert (
        seed_local.main(
            ["--db", str(db_path), "--current-selection", "example_host", "alias"]
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines()[-len(aliases):] == aliases

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0
    output = capsys.readouterr().out
    assert "aliases:\n" + "\n".join(f"- {alias}" for alias in aliases) in output
    assert "- alias:" not in output


def test_cli_impact_formats_systemd_resolved_stub_and_upstream(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-dns.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "os", "linux"),
            ("example_host", "dns_resolver", "127.0.0.53"),
            ("example_host", "dns_resolver_stub", "127.0.0.53"),
            ("example_host", "dns_resolver_upstream", "1.1.1.1"),
            ("example_host", "dns_resolver_upstream", "2001:4860:4860::8888"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0

    output = capsys.readouterr().out
    assert "- dns_resolver_stub: 127.0.0.53" in output
    assert "- dns_resolver_upstream:\n  - 1.1.1.1\n  - 2001:4860:4860::8888" in output
    assert "dns works" not in output


def test_cli_impact_formats_unknown_upstream_when_only_stub_known(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-dns-stub-only.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "os", "linux"),
            ("example_host", "dns_resolver", "127.0.0.53"),
            ("example_host", "dns_resolver_stub", "127.0.0.53"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0

    output = capsys.readouterr().out
    assert "- dns_resolver_stub: 127.0.0.53" in output
    assert "- dns_resolver_upstream: unknown" in output
    assert "availability_status: unknown" in output
    assert (
        "- reachability/availability: not inferred from local network facts" in output
    )


def test_cli_impact_omits_ip_address_aliases_unless_explicit_alias(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-ip-alias-cleanup.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "os", "linux"),
            ("example_host", "ip_address", "192.0.2.115"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0

    output = capsys.readouterr().out
    aliases_section = output.split("availability_status:", 1)[0]
    assert "aliases:\n- none" in aliases_section
    assert "- 192.0.2.115" not in aliases_section

    _persist_impact_facts(
        seed_local,
        db_path,
        [("example_host", "alias", "192.0.2.115")],
    )
    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0
    output = capsys.readouterr().out
    assert "aliases:\n- 192.0.2.115" in output


def test_cli_impact_includes_graph_warnings(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-warning.sqlite"
    _persist_impact_facts(seed_local, db_path, [("mystery", "group", "servers")])

    assert seed_local.main(["--db", str(db_path), "--impact", "mystery"]) == 0

    output = capsys.readouterr().out
    assert "graph issues:" in output
    assert "- warning: mystery member_of servers" in output
    assert "subject type is unknown; expected host" in output


def test_cli_impact_collapses_duplicate_monitored_by_warnings(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-duplicate-warning.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "prometheus_instance", "example_host:9100"),
            ("example_host", "prometheus_instance", "example_host:8080"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0

    output = capsys.readouterr().out
    warning = "- warning: example_host monitored_by prometheus"
    assert output.count(warning) == 1


def test_cli_impact_does_not_ingest_or_execute(tmp_path, capsys, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-read-only.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "example_host",
                "os",
                "linux",
                "--impact",
                "example_host",
                "restart",
                "example_host",
            ]
        )
        == 0
    )
    assert "entity types: unknown" in capsys.readouterr().out

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        assert ledger.list_events(seed_local.DEFAULT_WORKSPACE) == []
    finally:
        ledger.close()


def test_cli_show_inference_catalog_displays_rules(capsys):
    seed_local = load_seed_local_module()

    assert seed_local.main(["--show-inference-catalog"]) == 0

    output = capsys.readouterr().out
    assert "deterministic inference rules:" in output
    assert "docker_runtime_managed_by" in output
    assert "runtime=docker -> managed_by=docker_container_lifecycle" in output
    assert "availability_down_health_degraded" in output


def test_cli_inferred_facts_displays_projection_provenance(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "web_service",
                "runtime",
                "docker",
                "--inferred-facts",
                "web_service",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "managed_by: docker_container_lifecycle" in output
    assert "source_fact_id=" in output
    assert "inference_rule_id=docker_runtime_managed_by" in output


def test_cli_why_displays_recursive_endpoint_health_inference(capsys):
    seed_local = load_seed_local_module()

    assert (
        seed_local.main(
            [
                "--fact",
                "example_host",
                "alias",
                "192.0.2.115",
                "--fact",
                "192.0.2.115",
                "alias",
                "192.0.2.115:9100",
                "--fact",
                "192.0.2.115:9100",
                "availability_status",
                "down",
                "--why",
                "192.0.2.115:9100",
                "health_status",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Current belief:" in output
    assert "health_status=degraded" in output
    assert "inference_rule: availability_down_health_degraded" in output
    assert "derived_from: availability_status=down" in output


def test_cli_impact_groups_endpoint_availability_by_role(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-endpoint-roles.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "os", "linux"),
            ("example_host", "alias", "192.0.2.115:9100"),
            ("example_host", "alias", "192.0.2.115:9200"),
            ("192.0.2.115:9100", "endpoint_role", "node-exporter"),
            ("192.0.2.115:9100", "availability_status", "down"),
            ("192.0.2.115:9200", "endpoint_role", "cadvisor"),
            ("192.0.2.115:9200", "availability_status", "up"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0

    output = capsys.readouterr().out
    assert "availability_status: unknown" in output
    assert "endpoint availability by role:\n- none" in output


def test_cli_unhealthy_keeps_current_down_endpoint_under_endpoint_identity(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-endpoints.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "os", "linux"),
            ("example_host", "alias", "192.0.2.115:9100"),
            ("192.0.2.115:9100", "endpoint_role", "node-exporter"),
            ("192.0.2.115:9100", "availability_status", "down"),
            ("example_host_b:9100", "endpoint_role", "node-exporter"),
            ("example_host_b:9100", "availability_status", "up"),
            ("host-down-is-not-an-endpoint", "os", "linux"),
            ("host-down-is-not-an-endpoint", "availability_status", "down"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--unhealthy"]) == 0

    output = capsys.readouterr().out
    assert (
        "unhealthy endpoints:\n192.0.2.115:9100:\n  - node-exporter down 192.0.2.115:9100"
        in output
    )
    assert "example_host_b:9100" not in output
    assert "host-down-is-not-an-endpoint" not in output
    assert "graph errors:" in output
    assert "graph warnings:" not in output


def test_cli_down_alias_uses_current_measurement_sample(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-current-sample.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host:9100", "availability_status", "down"),
            ("example_host:9100", "availability_status", "up"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--down"]) == 0

    assert "example_host:9100" not in capsys.readouterr().out


def test_cli_unhealthy_shows_errors_and_optionally_warnings(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-graph-issues.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "os", "linux"),
            ("workers", "group", "team"),
            ("workers", "runs_on", "example_host"),
            ("mystery", "group", "servers"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--unhealthy"]) == 0
    output = capsys.readouterr().out
    assert "graph errors:" in output
    assert "- error: workers member_of team" in output
    assert "graph warnings:" not in output
    assert "mystery member_of servers" not in output

    assert (
        seed_local.main(["--db", str(db_path), "--unhealthy", "--include-warnings"])
        == 0
    )
    output = capsys.readouterr().out
    assert "graph warnings:" in output
    assert "- warning: mystery member_of servers" in output


def test_cli_graph_issue_output_prints_hint_when_present(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "graph-issue-hint.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [("e1f9104e9a8d", "prometheus_instance", "e1f9104e9a8d:9100")],
    )

    assert seed_local.main(["--db", str(db_path), "--graph-issues"]) == 0

    output = capsys.readouterr().out
    assert (
        "hint: Add inventory or alias evidence if this monitored endpoint should map to a known host."
        in output
    )
    assert "source_fact_ids: fact_impact_0" in output


def test_cli_unhealthy_does_not_ingest_or_execute(tmp_path, capsys, monkeypatch):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "unhealthy-read-only.sqlite"

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--fact",
                "example_host:9100",
                "availability_status",
                "down",
                "--unhealthy",
                "restart",
                "example_host",
            ]
        )
        == 0
    )
    assert "unhealthy endpoints:\n- none" in capsys.readouterr().out

    ledger = seed_local.SQLiteEventLedger(str(db_path))
    try:
        assert ledger.list_events(seed_local.DEFAULT_WORKSPACE) == []
    finally:
        ledger.close()


def test_cli_impact_includes_identity_section_without_availability_or_reachability(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-identity.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "hostname", "example_host"),
            ("example_host", "machine_id", "0123456789abcdef0123456789abcdef"),
            ("example_host", "boot_id", "11111111-2222-3333-4444-555555555555"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0
    output = capsys.readouterr().out

    assert "identity:\n" in output
    assert "- hostname: example_host" in output
    assert "- machine_id: 0123456789abcdef0123456789abcdef" in output
    assert "- boot_id: 11111111-2222-3333-4444-555555555555" in output
    assert "- availability/reachability: not inferred from identity facts" in output
    assert "availability_status: unknown" in output
    assert "reachability_status" not in output


def test_cli_current_facts_exposes_identity_facts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-identity.sqlite"
    _persist_impact_facts(
        seed_local,
        db_path,
        [
            ("example_host", "hostname", "example_host"),
            ("example_host", "machine_id", "0123456789abcdef0123456789abcdef"),
            ("example_host", "boot_id", "11111111-2222-3333-4444-555555555555"),
        ],
    )

    assert seed_local.main(["--db", str(db_path), "--current-selection", "example_host", "hostname"]) == 0
    output = capsys.readouterr().out

    assert output.rstrip().endswith("example_host")


def test_cli_observe_prometheus_timings_use_test_double(monkeypatch, capsys):
    seed_local = load_seed_local_module()
    _patch_fake_prometheus_source(monkeypatch, seed_local)

    assert (
        seed_local.main(
            [
                "--observe-prometheus",
                "http://prom.example:9090",
                "--observe-timings",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Observation ingestion timings:" in output
    assert "source collection:" in output
    assert "normalization:" in output
    assert "event generation + ledger write:" in output
    assert "total observations: 8" in output


def test_cli_observe_repository_source_ingests_queryable_relationships(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "repository-source.sqlite"
    repo_path = tmp_path / "repo"
    source_dir = repo_path / "seed_runtime"
    source_dir.mkdir(parents=True)
    (source_dir / "state.py").write_text(
        "from seed_runtime.projection_store import project_state_with_cache\n"
        "class StateProjector:\n"
        "    pass\n",
        encoding="utf-8",
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-repository-source",
                str(repo_path),
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "predicate: imports" in output
    assert "predicate: defines" in output

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--current-selection",
                "seed_runtime.state",
                "defines",
            ]
        )
        == 0
    )
    assert "seed_runtime.state.StateProjector" in capsys.readouterr().out


def test_cli_observe_repository_source_timings_include_source_counters(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "repository-source-timings.sqlite"
    repo_path = tmp_path / "repo"
    source_dir = repo_path / "seed_runtime"
    source_dir.mkdir(parents=True)
    (source_dir / "state.py").write_text(
        "import json\n" "def project():\n" "    return json.dumps({})\n",
        encoding="utf-8",
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-repository-source",
                str(repo_path),
                "--observe-timings",
                "--quiet-output",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "Observation ingestion timings:" in output
    assert "files_scanned: 1" in output
    assert "files_skipped: 0" in output
    assert "definitions_imports_extracted:" in output
    assert "source collection:" in output
    assert "normalization:" in output
    assert "event generation + ledger write:" in output


def test_cli_repository_current_facts_filter_matches_broad_relationship_facts(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "repository-current-facts.sqlite"
    repo_path = tmp_path / "repo"
    source_dir = repo_path / "tests"
    source_dir.mkdir(parents=True)
    (source_dir / "test_toolkit_validator.py").write_text(
        "from seed_runtime.toolkit import CandidateStore, ToolNeed\n"
        "from seed_runtime.validator import ToolkitValidator\n"
        "\n"
        "def test_validator_accepts_generated_stub_candidate():\n"
        "    pass\n"
        "\n"
        "def test_validator_fails_candidate_tests_that_exceed_timeout():\n"
        "    pass\n",
        encoding="utf-8",
    )

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--observe-repository-source",
                str(repo_path),
            ]
        )
        == 0
    )
    capsys.readouterr()

    expected_defines = [
        "tests.test_toolkit_validator.test_validator_accepts_generated_stub_candidate "
        "(path=tests/test_toolkit_validator.py)",
        "tests.test_toolkit_validator.test_validator_fails_candidate_tests_that_exceed_timeout "
        "(path=tests/test_toolkit_validator.py)",
    ]
    expected_imports = [
        "CandidateStore (path=tests/test_toolkit_validator.py)",
        "ToolNeed (path=tests/test_toolkit_validator.py)",
        "ToolkitValidator (path=tests/test_toolkit_validator.py)",
    ]

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--current-selection",
                "tests.test_toolkit_validator",
                "defines",
            ]
        )
        == 0
    )
    filtered_defines = capsys.readouterr().out.splitlines()
    assert filtered_defines[-len(expected_defines):] == expected_defines

    assert (
        seed_local.main(
            [
                "--db",
                str(db_path),
                "--current-selection",
                "tests.test_toolkit_validator",
                "imports",
            ]
        )
        == 0
    )
    filtered_imports = capsys.readouterr().out.splitlines()
    assert filtered_imports[-len(expected_imports):] == expected_imports


def test_cli_current_facts_broken_pipe_exits_without_traceback(tmp_path):
    db_path = tmp_path / "broken-pipe.sqlite"
    process = subprocess.run(
        f"{sys.executable} {SCRIPT_PATH} --db {db_path} "
        "--fact example_host alias example_host.local --current-selection example_host alias | head -1",
        shell=True,
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        check=False,
    )

    assert process.returncode == 0
    assert "BrokenPipeError" not in process.stderr
    assert "Traceback" not in process.stderr


def _persist_storage_impact_facts(seed_local, db_path):
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    facts = [
        ("example_host", "block_device", "sda", {"device": "sda"}),
        ("example_host", "block_device", "nvme0n1", {"device": "nvme0n1"}),
        ("example_host", "partition", "sda1", {"device": "sda1", "parent": "sda"}),
        (
            "example_host",
            "partition",
            "nvme0n1p1",
            {"device": "nvme0n1p1", "parent": "nvme0n1"},
        ),
        (
            "example_host",
            "block_device_parent",
            "sda",
            {"device": "sda1", "parent": "sda"},
        ),
        (
            "example_host",
            "block_device_size_bytes",
            1073741824,
            {"device": "sda1", "parent": "sda"},
        ),
        ("example_host", "block_device_rotational", "true", {"device": "sda"}),
        ("example_host", "block_device_removable", "false", {"device": "sda"}),
        ("example_host", "block_device_model", "Fast Disk", {"device": "sda"}),
        ("example_host", "block_device_vendor", "SEED", {"device": "sda"}),
        ("example_host", "mount_point", "/", {"mount_point": "/"}),
        ("example_host", "mounted_device", "/dev/sda1", {"mount_point": "/"}),
    ]
    try:
        for index, (subject, predicate, value, dimensions) in enumerate(facts):
            fact = seed_local.Fact(
                id=f"fact_storage_impact_{index}",
                subject_id=subject,
                predicate=predicate,
                value=value,
                source_type="discovery",
                confidence=0.9,
                evidence_ids=[],
                observed_at=seed_local.utc_now(),
                dimensions=dimensions,
            )
            ledger.append(
                "fact.observed",
                seed_local.DEFAULT_WORKSPACE,
                {"fact": seed_local.to_plain(fact)},
            )
    finally:
        ledger.close()


def _persist_listener_impact_facts(seed_local, db_path):
    ledger = seed_local.SQLiteEventLedger(str(db_path))
    facts = [
        (
            "example_host",
            "listening_endpoint",
            "tcp 0.0.0.0:22",
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "example_host",
            "listening_protocol",
            "tcp",
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "example_host",
            "listening_address",
            "0.0.0.0",
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "example_host",
            "listening_port",
            22,
            {
                "protocol": "tcp",
                "address": "0.0.0.0",
                "port": "22",
                "address_family": "ipv4",
            },
        ),
        (
            "example_host",
            "listening_endpoint",
            "udp 127.0.0.1:53",
            {
                "protocol": "udp",
                "address": "127.0.0.1",
                "port": "53",
                "address_family": "ipv4",
            },
        ),
    ]
    try:
        for index, (subject, predicate, value, dimensions) in enumerate(facts):
            fact = seed_local.Fact(
                id=f"fact_listener_impact_{index}",
                subject_id=subject,
                predicate=predicate,
                value=value,
                source_type="discovery",
                confidence=0.9,
                evidence_ids=[],
                observed_at=seed_local.utc_now(),
                dimensions=dimensions,
            )
            ledger.append(
                "fact.observed",
                seed_local.DEFAULT_WORKSPACE,
                {"fact": seed_local.to_plain(fact)},
            )
    finally:
        ledger.close()


def test_cli_current_facts_exposes_listener_facts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-listeners.sqlite"
    _persist_listener_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--current-selection", "example_host", "listening_endpoint"]) == 0
    output = capsys.readouterr().out

    assert "tcp 0.0.0.0:22" in output
    assert "udp 127.0.0.1:53" in output


def test_cli_impact_includes_compact_listener_endpoints_without_inference(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-listeners.sqlite"
    _persist_listener_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0
    output = capsys.readouterr().out

    assert "listening endpoints:" in output
    assert "- tcp 0.0.0.0:22" in output
    assert "- udp 127.0.0.1:53" in output
    assert (
        "- availability/reachability/health/ownership: not inferred from listener facts"
        in output
    )
    assert "availability_status: unknown" in output
    assert "reachability_status" not in output
    assert "endpoint_health" not in output
    assert "process_owner" not in output
    assert "service_owner" not in output


def test_cli_current_facts_exposes_storage_topology_facts(tmp_path, capsys):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "current-storage.sqlite"
    _persist_storage_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--current-selection", "example_host", "block_device"]) == 0
    output = capsys.readouterr().out

    assert "sda (device=sda)" in output
    assert "nvme0n1 (device=nvme0n1)" in output


def test_cli_impact_includes_compact_storage_topology_without_health_inference(
    tmp_path, capsys
):
    seed_local = load_seed_local_module()
    db_path = tmp_path / "impact-storage.sqlite"
    _persist_storage_impact_facts(seed_local, db_path)

    assert seed_local.main(["--db", str(db_path), "--impact", "example_host"]) == 0
    output = capsys.readouterr().out

    assert "storage topology:" in output
    assert "- devices:" in output
    assert "  - sda" in output
    assert "  - nvme0n1" in output
    assert "- partitions:" in output
    assert "  - sda1" in output
    assert "  - nvme0n1p1" in output
    assert "- parent relationships:" in output
    assert "  - sda1 -> sda" in output
    assert "- mount relationships:" in output
    assert "  - /dev/sda1 -> /" in output
    assert (
        "- health/availability/filesystem-health: not inferred from storage facts"
        in output
    )
    assert "availability_status: unknown" in output
    assert "storage_health" not in output
    assert "filesystem_health" not in output


def test_cli_reachability_debug_writes_diagnostics_to_stderr_and_json_to_stdout(
    tmp_path,
):
    db_path = tmp_path / "reachability.sqlite"
    process = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--db",
            str(db_path),
            "--knowledge-reachability-audit",
            "--knowledge-reachability-audit-json",
            "--knowledge-reachability-audit-debug",
            "--knowledge-reachability-audit-limit",
            "1",
        ],
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        check=False,
    )

    assert process.returncode == 0
    decoded = json.loads(process.stdout)
    assert "[reachability]" not in process.stdout
    assert "[reachability] start load_state" in process.stderr
    assert "[reachability] end load_state" in process.stderr
    assert "state cache miss" in process.stderr
    assert "candidate sources:" in process.stderr
    assert decoded["metadata"]["timings"]["load_state"] >= 0
    assert "candidate_sources" in decoded["metadata"]
