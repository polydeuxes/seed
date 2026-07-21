from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text()


def test_operation_measurement_baseline_and_deviation_non_equivalences():
    text = _read("book_of_seed/07-operational-realization/execution-and-recording.md")

    assert "operation measurement != operational baseline" in text
    assert "operational baseline != predicted future duration" in text
    assert "difference from one sample != material deviation" in text
    assert "deviation != operation failure" in text
    assert "deviation != capability loss" in text
    assert "one unusual sample != changed ordinary behavior" in text
    assert "ExecutionStatus cadence != operation timing testimony" in text
    assert "does not by itself establish ordinary behavior" in text
    assert "A baseline transition is evidence-supported establishment" in text


def test_operational_measurement_preservation_and_discard_rule():
    text = _read("book_of_seed/07-operational-realization/execution-and-recording.md")

    assert "Seed need not preserve every operational measurement" in text
    assert "Non-rebuildable is not equal to preservation-required" in text
    assert "sufficient evidence or compressed standing" in text
    assert "materially sufficient understanding of operational reality" in text
    assert "within an established tolerance may be discarded" in text
    assert "does not alter or erase that understanding" in text
    assert "material deviation must preserve sufficient measurement and comparison context" in text
    assert "retain the challenge to prior understanding" in text


def test_rebuildability_does_not_reconstruct_prior_invocation():
    text = _read("book_of_seed/06-state-and-projection/projection-and-current-state.md")

    assert "A derived artifact need not be preserved" in text
    assert "Rebuildable projection is not prior invocation reconstruction" in text
    assert "rebuildable projection != prior invocation reconstruction" in text
    assert "reconstructable current condition != irrecoverable historical invocation" in text
    assert "elapsed duration of one invocation" in text
    assert "cache condition at that historical invocation" in text


def test_diagnostic_rendering_and_operator_capture_do_not_decide_seed_preservation():
    text = _read("book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md")

    assert "diagnostic rendering != Seed-consumable knowledge" in text
    assert "operator capture != Seed preservation" in text
    assert "operator omission != permission for Seed to forget" in text
    assert "Seed preservation != obligation to expose every sample externally" in text


def test_amendment_records_required_answers_and_absent_implementation():
    text = _read(
        "book_of_seed/operational_measurement_baseline_and_preservation_amendment_001.md"
    )

    assert "Seed need not preserve every operational measurement" in text
    assert "The inability to rebuild a raw measurement does not automatically require preservation" in text
    assert "One unusual sample is insufficient" in text
    assert "Diagnostic rendering is not Seed-consumable knowledge by identity" in text
    assert "No operational baseline, tolerance comparison, deviation artifact" in text
    assert "timing-based movement consumer is currently implemented" in text
    assert "`ExecutionStatus` is not operational timing testimony" in text
