from __future__ import annotations

from datetime import datetime

from seed_runtime.events import EventLedger
from seed_runtime.observation_sources import (
    ObservationCollectionService,
    RepositorySourceObservationSource,
)
from seed_runtime.observations import ObservationIngestor
from seed_runtime.source_navigation import build_source_navigation, format_source_navigation
from seed_runtime.state import StateProjector

BASE_TIME = datetime(2024, 1, 1, 0, 0, 0)


def _project_repository(tmp_path, *, twice: bool = False):
    runtime_dir = tmp_path / "seed_runtime"
    runtime_dir.mkdir(exist_ok=True)
    (runtime_dir / "state_summary_views.py").write_text(
        "from seed_runtime.state_views import build_state_summary\n"
        "def state_summary(state):\n"
        "    return build_state_summary(state)\n",
        encoding="utf-8",
    )
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    (scripts_dir / "seed_local.py").write_text(
        "from seed_runtime.state_summary_views import state_summary\n"
        "from seed_runtime.observation_sources import PrometheusObservationSource\n",
        encoding="utf-8",
    )
    ledger = EventLedger()
    service = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    )
    source = RepositorySourceObservationSource(
        tmp_path,
        observed_at=BASE_TIME,
        include_roots=("seed_runtime", "scripts"),
    )
    service.collect(source, "ws")
    if twice:
        service.collect(source, "ws")
    return StateProjector(ledger).project("ws")


def test_short_symbol_lookup_finds_expected_definition(tmp_path):
    view = build_source_navigation(_project_repository(tmp_path), "state_summary")

    assert [row.value for row in view.definitions] == [
        "seed_runtime.state_summary_views.state_summary"
    ]
    assert view.definitions[0].path == "seed_runtime/state_summary_views.py"


def test_qualified_symbol_lookup_returns_exact_match(tmp_path):
    view = build_source_navigation(
        _project_repository(tmp_path),
        "seed_runtime.state_summary_views.state_summary",
    )

    assert [row.value for row in view.definitions] == [
        "seed_runtime.state_summary_views.state_summary"
    ]
    assert not view.imports


def test_module_lookup_returns_grouped_definitions_and_imports(tmp_path):
    view = build_source_navigation(_project_repository(tmp_path), "scripts.seed_local")

    assert not view.definitions
    assert [row.value for row in view.imports] == [
        "PrometheusObservationSource",
        "state_summary",
    ]
    assert {row.path for row in view.imports} == {"scripts/seed_local.py"}


def test_path_lookup_returns_grouped_definitions_and_imports(tmp_path):
    view = build_source_navigation(
        _project_repository(tmp_path), "seed_runtime/state_summary_views.py"
    )

    assert [row.value for row in view.definitions] == [
        "seed_runtime.state_summary_views.state_summary"
    ]
    assert [row.value for row in view.imports] == ["build_state_summary"]


def test_repeated_observation_keeps_navigation_rows_stable_and_support_valid(tmp_path):
    first = build_source_navigation(_project_repository(tmp_path), "state_summary")
    second = build_source_navigation(
        _project_repository(tmp_path, twice=True), "state_summary"
    )

    assert [row.value for row in second.definitions] == [
        row.value for row in first.definitions
    ]
    assert second.definitions[0].support_count == 2
    assert second.definitions[0].representative_fact_id is not None


def test_navigation_query_is_read_only(tmp_path):
    state = _project_repository(tmp_path)
    before = (
        len(state.observations),
        len(state.evidence),
        len(state.facts),
        list(state.fact_supports),
    )

    view = build_source_navigation(state, "state_summary")
    rendered = format_source_navigation(view)

    assert "Source Navigation" in rendered
    assert (
        len(state.observations),
        len(state.evidence),
        len(state.facts),
        list(state.fact_supports),
    ) == before
