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


def _project_dense_repository(tmp_path):
    runtime_dir = tmp_path / "seed_runtime"
    runtime_dir.mkdir(exist_ok=True)
    import_lines = "\n".join(f"from pkg.mod{i} import Import{i}" for i in range(12))
    define_lines = "\n".join(
        f"def function_{i}():\n    return Import{i % 12}\n" for i in range(12)
    )
    (runtime_dir / "dense.py").write_text(
        f"{import_lines}\n\n{define_lines}",
        encoding="utf-8",
    )
    ledger = EventLedger()
    service = ObservationCollectionService(
        ObservationIngestor(ledger), normalization_pipeline=None
    )
    source = RepositorySourceObservationSource(
        tmp_path,
        observed_at=BASE_TIME,
        include_roots=("seed_runtime",),
    )
    service.collect(source, "ws")
    return StateProjector(ledger).project("ws")


def test_symbol_lookup_rendering_remains_fully_expanded(tmp_path):
    rendered = format_source_navigation(
        build_source_navigation(_project_repository(tmp_path), "state_summary")
    )

    assert "Definitions:" in rendered
    assert "Definitions: 1 total" not in rendered
    assert "module: seed_runtime.state_summary_views" in rendered
    assert "path: seed_runtime/state_summary_views.py" in rendered
    assert "support facts: 1" in rendered
    assert "representative fact:" in rendered
    assert "representative support:" in rendered


def test_path_lookup_rendering_is_bounded(tmp_path):
    rendered = format_source_navigation(
        build_source_navigation(
            _project_dense_repository(tmp_path), "seed_runtime/dense.py"
        )
    )

    assert "Definitions: 12 total, showing 10" in rendered
    assert "Imports: 12 total, showing 10" in rendered
    assert "  seed_runtime.dense.function_7" in rendered
    assert "  seed_runtime.dense.function_8" not in rendered
    assert "  Import7" in rendered
    assert "  Import8" not in rendered
    assert rendered.count("representative fact:") == 0
    assert rendered.count("representative support:") == 0


def test_module_lookup_rendering_is_bounded(tmp_path):
    rendered = format_source_navigation(
        build_source_navigation(
            _project_dense_repository(tmp_path), "seed_runtime.dense"
        )
    )

    assert "Definitions: 12 total, showing 10" in rendered
    assert "Imports: 12 total, showing 10" in rendered
    assert "  seed_runtime.dense.function_7" in rendered
    assert "  seed_runtime.dense.function_8" not in rendered
    assert "  Import7" in rendered
    assert "  Import8" not in rendered


def test_support_metadata_remains_available_from_bounded_and_exact_views(tmp_path):
    state = _project_dense_repository(tmp_path)
    bounded = format_source_navigation(
        build_source_navigation(state, "seed_runtime/dense.py")
    )
    exact = format_source_navigation(build_source_navigation(state, "function_11"))

    assert "Support:" in bounded
    assert "support facts: 24" in bounded
    assert "representative fact/support: available in exact symbol lookup" in bounded
    assert "representative fact:" in exact
    assert "representative support:" in exact


def test_repeated_observation_rendering_stays_stable(tmp_path):
    first = format_source_navigation(
        build_source_navigation(_project_repository(tmp_path), "state_summary")
    )
    second = format_source_navigation(
        build_source_navigation(
            _project_repository(tmp_path, twice=True), "state_summary"
        )
    )

    assert "support facts: 1" in first
    assert "support facts: 2" in second
    assert "seed_runtime.state_summary_views.state_summary" in second
    assert "representative fact:" in second
