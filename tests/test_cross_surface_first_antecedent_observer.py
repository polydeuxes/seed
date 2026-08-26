from __future__ import annotations

import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from observe_cross_surface_first_antecedent import observe  # noqa: E402


def test_live_measurement_reaches_every_first_aperture_material_and_stops():
    finding = observe()

    assert finding["source_count"] == 4
    assert finding["all_distinct_source_bytes_have_count_findings"] is True
    assert finding["all_projection_apertures_have_count_findings"] is True
    assert finding["all_results_have_exact_current_coordinates"] is True
    assert finding["projection_observer_ledger_occurrence_count"] == 0
    assert finding["known_loss"] is None

    assert all(
        source["binding_precedes_Act_Yield_and_result"]
        for source in finding["sources"]
    )
