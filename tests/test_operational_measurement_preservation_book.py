from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text()


def test_operation_measurement_baseline_and_deviation_non_equivalences():
    text = _read("book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md")

    assert "operation measurement != operational baseline" in text
    assert "operational baseline != predicted future duration" in text
    assert "difference from one sample != material deviation" in text
    assert "deviation != operation failure" in text
    assert "deviation != capability loss" in text
    assert "one unusual sample != changed ordinary behavior" in text
    assert "ExecutionStatus cadence != operation timing testimony" in text
    assert "does not make it execution by measurement alone" in text
    assert "A baseline transition is evidence-supported establishment" in text


def test_operational_measurement_preservation_and_discard_rule():
    text = _read("book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md")

    assert "Seed need not preserve every operational measurement" in text
    assert "Non-rebuildable is not equal to preservation-required" in text
    assert "sufficient evidence or compressed standing" in text
    assert "materially sufficient understanding of operational reality" in text
    assert "within an established tolerance may be discarded" in text
    assert "does not alter or erase that understanding" in text
    assert "material deviation must preserve sufficient measurement and comparison context" in text
    assert "retain the challenge to prior understanding" in text


def test_operational_measurement_topology_non_equivalences_in_canonical_clauses():
    recording = _read("book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md")
    execution = _read("book_of_seed/07-operational-realization/execution-and-recording.md")

    assert "bounded operation != execution" in execution
    assert "operational measurement != execution" in recording
    assert "operational measurement != execution record" in recording
    assert "operational measurement != operation result" in recording
    assert "operation-instance measurement != ambient runtime observation" in recording
    assert "runtime/resource observation != operational baseline" in recording
    assert "execution status != operational measurement" in recording
    assert "diagnostic rendering != measurement ownership" in recording
    assert "non-rebuildable != preservation-required" in recording


def test_runtime_resource_observation_is_separate_from_operation_instance_measurement():
    text = _read("book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md")

    assert "Operation-instance measurement and ambient runtime/resource observation are not identical" in text
    assert "Ordinary runtime/resource observation is testimony about a process or runtime condition at an observed time" in text
    assert "without necessarily attributing the value to one bounded operation instance" in text
    assert "may support an operational measurement or baseline only through an explicit attribution and establishment boundary" in text


def test_execution_chapter_no_longer_owns_operational_measurement_or_stale_executor_anchor():
    text = _read("book_of_seed/07-operational-realization/execution-and-recording.md")

    assert "Operational measurement is a distinct form of operation testimony" not in text
    assert "Addressable boundaries for operational measurement" not in text
    assert "ToolExecutor.execute(...)" not in text
    assert "seed_runtime/execution.py::ToolExecutor" not in text
    assert "commonly realized by `ToolExecutor.execute(...)`" not in text
    assert "invoking registered Python callables" not in text


def test_concordance_indexes_measurement_without_equating_execution_or_runtime_observation():
    text = _read("book_of_seed/concordance.md")

    assert "| operational measurement | Evidence and Knowledge | [Recording and knowledge extraction]" in text
    assert "| runtime/resource observation | Evidence and Knowledge | [Recording and knowledge extraction]" in text
    assert "timing sample, elapsed duration, runtime/resource observation" not in text
    measurement_line = next(
        line for line in text.splitlines() if line.startswith("| operational measurement |")
    )
    assert "execution" not in measurement_line.lower()
    runtime_line = next(
        line for line in text.splitlines() if line.startswith("| runtime/resource observation |")
    )
    assert "operation-instance timing" not in runtime_line


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


def test_amendment_and_correction_records_required_answers_and_absent_implementation():
    amendment = _read(
        "book_of_seed/operational_measurement_baseline_and_preservation_amendment_001.md"
    )
    correction = _read("book_of_seed/operational_measurement_topology_correction_001.md")

    assert "Seed need not preserve every operational measurement" in amendment
    assert "The inability to rebuild a raw measurement does not automatically require preservation" in amendment
    assert "One unusual sample is insufficient" in amendment
    assert "Diagnostic rendering is not Seed-consumable knowledge by identity" in amendment
    assert "No operational baseline, tolerance comparison, deviation artifact" in amendment
    assert "timing-based movement consumer is currently implemented" in amendment
    assert "`ExecutionStatus` is not operational timing testimony" in amendment
    assert "Is operational measurement constitutionally identical to execution? No." in correction
    assert "Does measuring a projection, cache lookup, query, or rendering operation make it an execution? No, not by measurement alone." in correction
    assert "Is ordinary runtime/resource observation identical to an operation-instance measurement? No." in correction
    assert "Does current repository evidence support the canonical claim that Seed commonly executes registered Python callables through `ToolExecutor.execute(...)`? No." in correction
    assert "No operational timing baseline is implemented" in correction
    assert "No tolerance comparison is implemented" in correction
    assert "No deviation artifact is implemented" in correction
    assert "No baseline-transition artifact is implemented" in correction
    assert "No timing-based lawful-movement consumer is implemented" in correction
    assert "does not invalidate PR 1895's preservation rule" in correction


def test_recording_boundary_does_not_own_measurement_or_standing_establishment():
    text = _read("book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md")

    assert "operational measurement != recording" in text
    assert "measurement occurrence != recorded measurement" in text
    assert "recording measurement testimony != producing measurement testimony" in text
    assert "diagnostic rendering != measurement production" in text
    assert "diagnostic rendering != measurement preservation" in text
    assert "baseline establishment != baseline recording" in text
    assert "retained measurement series != operational baseline" in text
    assert "comparison != recording" in text
    assert "deviation recognition != deviation recording" in text
    assert "baseline transition establishment != transition recording" in text
    assert "record exists != recorded standing lawfully established" in text
    assert "non-rebuildable != preservation-required" in text


def test_canonical_clauses_protect_transient_measurement_and_record_limits():
    text = _read("book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md")

    assert "Recording may preserve already produced measurement testimony" in text
    assert "does not produce the upstream measurement" in text
    assert "measurement-production responsibility produces that operation-instance testimony" in text
    assert "A measurement occurrence may exist transiently without ever becoming a recorded measurement" in text
    assert "baseline recording may preserve the resulting standing but does not establish ordinary behavior" in text
    assert "recorded summary" in text
    assert "Comparison occurrence != recorded comparison" in text or "comparison occurrence != recorded comparison" in text
    assert "Material deviation recognition is an establishment decision" in text
    assert "recorded difference does not establish material deviation" in text
    assert "Preservation decision != standing-establishment decision" in text


def test_boundary_correction_record_required_answers_and_absences():
    text = _read("book_of_seed/operational_measurement_recording_boundary_correction_001.md")

    assert "Producing operational measurement testimony is not constitutionally identical to recording it" in text
    assert "Operational measurement testimony may exist transiently without a recording boundary" in text
    assert "Recording a set of measurements does not establish an operational baseline" in text
    assert "Recording a difference does not establish material deviation" in text
    assert "Recording repeated measurements does not establish a baseline transition" in text
    assert "Recording may preserve already established measurement, baseline, deviation, or transition standing" in text
    assert "does not invalidate PR 1895's preservation rule or PR 1896's execution correction" in text
    assert "No operational timing baseline is implemented" in text
    assert "No tolerance comparison is implemented" in text
    assert "No deviation artifact is implemented" in text
    assert "No baseline-transition artifact is implemented" in text
    assert "No timing-based lawful-movement consumer is implemented" in text
