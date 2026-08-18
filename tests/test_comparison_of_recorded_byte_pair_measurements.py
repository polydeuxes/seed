from copy import deepcopy
from io import BytesIO, StringIO

import pytest

from tests.binary_input import binary_input

import seed_runtime.byte_measurement as byte_measurement_module
import seed_runtime.comparison_of_recorded_byte_pair_measurements as comparison_module
import seed_runtime.operator_locality_standing as operator_standing_module
from seed_runtime.byte_measurement import (
    record_byte_measurement_responsibility_assignment,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
    get_byte_position_pair_measurement_responsibility_assignment,
    assertions_of_recorded_byte_position_pair_measurement,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    RecordedPairMeasurementComparisonError,
    get_recorded_pair_measurement_comparison,
    record_recorded_pair_measurement_comparison_responsibility_assignment,
    record_recorded_pair_measurement_comparison_applicability_act_evidence,
    record_recorded_pair_measurement_comparison_applicability_result,
    record_recorded_pair_measurement_comparison_act_evidence,
    record_recorded_pair_measurement_comparison_result,
    _record_recorded_pair_measurement_comparison_from_carried_measurements,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_acquisition import (
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_responsible_act_evidence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.operator_representation import (
    read_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_representation_admission import (
    REPRESENTATION_CANDIDATE_RECORDED_KIND,
)
from seed_runtime.supplied_invocation_material import SuppliedSystemMaterialOccurrence


LOCALITY = "recorded-pair-comparison-locality"


def _pair_measurement(ledger):
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(LOCALITY,),
        recording_locality_identity=LOCALITY,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        ),
    )
    act = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        ),
    )
    byte_result = record_byte_measurement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    return record_byte_position_pair_count_layer(
        ledger,
        source_measurement_event_identity=byte_result.identity,
        recording_locality_identity=LOCALITY,
    )


def _inputs():
    ledger = EventLedger()
    earlier_source = ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abab",
        source_role="system",
        source_boundary="earlier supplied occurrence",
    )
    earlier = _pair_measurement(ledger)
    added = ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abac",
        source_role="system",
        source_boundary="later supplied occurrence",
        provenance_occurrence_references=(earlier_source.identity,),
    )
    later = _pair_measurement(ledger)
    return ledger, earlier_source, added, earlier, later


def _comparison():
    ledger, earlier_source, added, earlier, later = _inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    assignment = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=standing,
    )
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    applicability_act = (
        record_recorded_pair_measurement_comparison_applicability_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            locality_standing=standing,
        )
    )
    applicability = record_recorded_pair_measurement_comparison_applicability_result(
        ledger,
        responsible_act_evidence_event_identity=applicability_act.identity,
    )
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    compare_act = record_recorded_pair_measurement_comparison_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
    )
    result = record_recorded_pair_measurement_comparison_result(
        ledger, responsible_act_evidence_event_identity=compare_act.identity
    )
    return ledger, earlier_source, added, earlier, later, assignment, applicability, result


def test_one_console_call_revalidates_only_the_pair_crossing_a_callback(
    monkeypatch,
):
    ledger, _earlier_source, _added, earlier, later = _inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    full_reads = []
    original = comparison_module._validated_recorded_byte_position_pair_measurement

    def record(*args, **kwargs):
        full_reads.append(args[1])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        comparison_module,
        "_validated_recorded_byte_position_pair_measurement",
        record,
    )
    result, standing = (
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier,
            later_measurement=later,
            locality_standing=standing,
        )
    )

    assert full_reads == [earlier.identity]
    assert result.identity in standing["comparison_result_occurrences"]
    replayed = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    assert standing == replayed
    assert full_reads.count(earlier.identity) >= 2
    assert later.identity in full_reads
    assert get_recorded_pair_measurement_comparison(
        ledger, result.identity
    ) == result.material


def test_changed_pair_crossing_a_callback_cannot_enter_compare_standing():
    ledger, _earlier_source, _added, earlier, later = _inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    standing_before = deepcopy(standing)
    event_count_before = len(ledger.list())
    earlier.material["assertions"][0]["dimensions"]["content"]["count"] += 1

    with pytest.raises(
        (RecordedPairMeasurementComparisonError, ValueError),
    ):
        _record_recorded_pair_measurement_comparison_from_carried_measurements(
            ledger,
            earlier_measurement=earlier,
            later_measurement=later,
            locality_standing=standing,
        )

    assert standing == standing_before
    assert len(ledger.list()) == event_count_before


def _operator_inputs(*, acquisition_before_earlier_measurement=False):
    ledger = EventLedger()
    earlier_source = ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abab",
        source_role="operator",
        source_boundary="earlier operator occurrence",
    )
    if acquisition_before_earlier_measurement:
        standing = read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        )
        representation = record_operator_representation(
            ledger,
            locality_identity=LOCALITY,
            locality_standing=standing,
        )
        standing = read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        )
    else:
        earlier = _pair_measurement(ledger)
        standing = read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        )
        representation = record_operator_representation(
            ledger,
            locality_identity=LOCALITY,
            locality_standing=standing,
            source_occurrence_reference=earlier.identity,
        )
        standing = read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        )
    assignment = record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=LOCALITY,
        addressed_representation_event_identity=(
            representation["representation_event_identity"]
        ),
        locality_standing=standing,
    )
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    act = record_operator_material_acquire_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    boundary = operator_boundary_material(BytesIO(b"abac\n"))
    acquired = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
        boundary_material=boundary,
    )
    if acquisition_before_earlier_measurement:
        earlier = _pair_measurement(ledger)
    added_standing = run_operator_ingest(
        ledger=ledger,
        locality_identity=LOCALITY,
        boundary_material=boundary,
        operator_material_occurrence_reference=acquired.identity,
    )
    added = ledger.get(
        added_standing["current_standing"]["ingest_occurrence"][
            "evidence_event_identity"
        ]
    )
    later = _pair_measurement(ledger)
    return ledger, earlier_source, acquired, added, earlier, later


def test_operator_acquisition_carries_the_prior_pair_measurement_into_compare():
    ledger, _source, acquired, added, earlier, later = _operator_inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)

    assignment = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=standing,
    )

    assert assignment.material["added_occurrence_reference"] == added.identity
    assert assignment.material["input_relation"] == (
        "operator material acquisition at prior Standing"
    )
    assert assignment.material[
        "operator_material_acquire_result_event_identity"
    ] == acquired.identity
    assert assignment.material[
        "operator_material_source_standing_reference"
    ] == acquired.material["source_standing_reference"]
    assert assignment.material["destination_operator_locality_identity"] == LOCALITY


def test_operator_occurrence_without_acquisition_cannot_supply_compare():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abab",
        source_role="operator",
        source_boundary="earlier operator occurrence",
    )
    earlier = _pair_measurement(ledger)
    ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abac",
        source_role="operator",
        source_boundary="later operator occurrence",
    )
    later = _pair_measurement(ledger)

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="one exact operator acquisition occurrence",
    ):
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )


def test_operator_acquisition_before_the_premise_cannot_supply_compare():
    ledger, _source, _acquired, _added, earlier, later = _operator_inputs(
        acquisition_before_earlier_measurement=True
    )

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="operator acquisition carries no exact prior Standing",
    ):
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )


def test_produced_measurements_enter_one_responsible_compare():
    ledger, earlier_source, added, earlier, later, assignment, applicability, result = (
        _comparison()
    )
    recorded = get_recorded_pair_measurement_comparison(ledger, result.identity)

    assert assignment.material["earlier_measurement_reference"][
        "recorded_occurrence_identity"
    ] == earlier.identity
    assert assignment.material["later_measurement_reference"][
        "recorded_occurrence_identity"
    ] == later.identity
    assert assignment.material["added_occurrence_reference"] == added.identity
    assert assignment.material["prior_provenance_occurrence_references"] == [
        earlier_source.identity
    ]
    assert applicability.material["standing"] == "applicable"
    assert len(recorded["participation_of_input_in_compare"]) == 2

    findings = recorded["findings"]
    count_ab = next(
        item
        for item in findings["conflicting_findings"]
        if item["subject"] == {"result": "count", "representation": [97, 98]}
    )
    assert count_ab["earlier_content"] == {
        "input_count": 1,
        "occurrences_carrying": 1,
        "count": 2,
    }
    assert count_ab["later_content"] == {
        "input_count": 2,
        "occurrences_carrying": 2,
        "count": 3,
    }
    assert any(
        item["subject"] == {"result": "recurrence", "representation": [97, 98]}
        for item in findings["same_content_findings"]
    )
    assert any(
        item["subject"] == {"result": "count", "representation": [97, 99]}
        for item in findings["findings_of_later_result"]
    )
    assert findings["unknown_findings"] == []

    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    assert result.identity in standing["comparison_result_occurrences"]


def test_same_content_finding_labels_do_not_hide_changed_content():
    ledger, *_rest, result = _comparison()
    findings = get_recorded_pair_measurement_comparison(ledger, result.identity)[
        "findings"
    ]
    conflicting_subjects = {
        (item["subject"]["result"], tuple(item["subject"]["representation"]))
        for item in findings["conflicting_findings"]
    }
    assert ("count", (97, 98)) in conflicting_subjects


def test_missing_provenance_cannot_supply_the_compare_rung():
    ledger, _source, added, earlier, later = _inputs()
    added.material["provenance_occurrence_references"] = []
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="supplied occurrence with exact provenance",
    ):
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )


def test_measurement_availability_without_standing_cannot_supply_compare():
    ledger, _source, _added, earlier, later = _inputs()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    standing["measurement_occurrences"].pop(earlier.identity)
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="each exact Measurement result in current Standing",
    ):
        record_recorded_pair_measurement_comparison_responsibility_assignment(
            ledger,
            earlier_result_event_identity=earlier.identity,
            later_result_event_identity=later.identity,
            locality_standing=standing,
        )


def test_corrupted_compare_yield_is_refused():
    ledger, *_rest, result = _comparison()
    evidence = ledger.get(result.material["evidence_of_yield_relation_identity"])
    assert evidence is not None
    evidence.material["result_identity"] = "crossed-result"
    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="exact Yield",
    ):
        get_recorded_pair_measurement_comparison(ledger, result.identity)


def test_one_result_read_validates_each_pair_measurement_once(monkeypatch):
    ledger, _first_source, _added, earlier, later, *_middle, result = _comparison()
    original = comparison_module._measurement_and_findings
    calls = []

    def counted(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(comparison_module, "_measurement_and_findings", counted)

    get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert calls == [earlier.identity, later.identity]

    get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert calls == [
        earlier.identity,
        later.identity,
        earlier.identity,
        later.identity,
    ]


def test_result_reader_preserves_its_exact_assignment_and_public_getter_delegates(
    monkeypatch,
):
    ledger, *_inputs, assignment, _applicability, result = _comparison()
    material, assignment_reading = (
        comparison_module._recorded_pair_measurement_comparison_reading(
            ledger, result.identity
        )
    )

    assert material == result.material
    assert assignment_reading[0] == assignment

    calls = []
    original = comparison_module._recorded_pair_measurement_comparison_reading

    def witnessed(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(
        comparison_module,
        "_recorded_pair_measurement_comparison_reading",
        witnessed,
    )
    assert get_recorded_pair_measurement_comparison(
        ledger, result.identity
    ) == result.material
    assert calls == [result.identity]


def test_standing_replay_carries_one_validated_assignment_across_comparison_stages(
    monkeypatch,
):
    ledger, *_rest, result = _comparison()
    calls = []
    original = (
        operator_standing_module._recorded_pair_comparison_assignment_reading
    )

    def witnessed(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(
        operator_standing_module,
        "_recorded_pair_comparison_assignment_reading",
        witnessed,
    )
    monkeypatch.setattr(comparison_module, "_assignment_reading", witnessed)

    standing = read_operator_locality_standing(
        ledger, locality_identity=LOCALITY
    )
    assignment_identity = result.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    assert result.identity in standing["comparison_result_occurrences"]
    assert calls == [assignment_identity]

    get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert calls == [assignment_identity, assignment_identity]


@pytest.mark.parametrize("callback", ("assignment", "input", "append"))
def test_standing_replay_carry_refuses_callback_change_and_leaks_no_state(
    monkeypatch, callback
):
    ledger, _source, _added, earlier, _later, assignment, _applicability, _result = (
        _comparison()
    )
    assignment_material = deepcopy(assignment.material)
    earlier_material = deepcopy(earlier.material)
    original = (
        operator_standing_module._recorded_pair_comparison_applicability_act_reading
    )
    callback_crossed = False

    def cross_after_assignment(*args, **kwargs):
        nonlocal callback_crossed
        if not callback_crossed:
            callback_crossed = True
            if callback == "assignment":
                assignment.material["responsibility"] = "changed after validation"
            elif callback == "input":
                earlier.material["measurement_rule"] = "changed after validation"
            else:
                ledger.append(
                    "test.unrelated_callback",
                    {"unknown": ["append after comparison assignment validation"]},
                    locality_identity="unrelated-callback",
                )
        return original(*args, **kwargs)

    monkeypatch.setattr(
        operator_standing_module,
        "_recorded_pair_comparison_applicability_act_reading",
        cross_after_assignment,
    )
    with pytest.raises(RecordedPairMeasurementComparisonError):
        read_operator_locality_standing(ledger, locality_identity=LOCALITY)

    assignment.material.clear()
    assignment.material.update(assignment_material)
    earlier.material.clear()
    earlier.material.update(earlier_material)
    assert read_operator_locality_standing(
        ledger, locality_identity=LOCALITY
    )["comparison_result_occurrences"]


def test_interleaved_comparisons_keep_distinct_ephemeral_assignment_readings(
    monkeypatch,
):
    ledger, _source, _added, earlier, later = _inputs()
    first = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        ),
    )
    second = record_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        earlier_result_event_identity=earlier.identity,
        later_result_event_identity=later.identity,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=LOCALITY
        ),
    )

    def finish(assignment):
        applicability_act = record_recorded_pair_measurement_comparison_applicability_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )
        applicability = record_recorded_pair_measurement_comparison_applicability_result(
            ledger,
            responsible_act_evidence_event_identity=applicability_act.identity,
        )
        act = record_recorded_pair_measurement_comparison_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity=LOCALITY
            ),
        )
        return record_recorded_pair_measurement_comparison_result(
            ledger, responsible_act_evidence_event_identity=act.identity
        )

    results = (finish(first), finish(second))
    calls = []
    original = (
        operator_standing_module._recorded_pair_comparison_assignment_reading
    )

    def witnessed(ledger, event_identity):
        calls.append(event_identity)
        return original(ledger, event_identity)

    monkeypatch.setattr(
        operator_standing_module,
        "_recorded_pair_comparison_assignment_reading",
        witnessed,
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=LOCALITY
    )

    assert all(
        result.identity in standing["comparison_result_occurrences"]
        for result in results
    )
    assert calls == [first.identity, second.identity]


def test_compare_reads_exact_findings_without_rebuilding_full_assertion_carriers(
    monkeypatch,
):
    ledger, *_rest, result = _comparison()

    def full_carrier_is_not_a_compare_input(*args, **kwargs):
        raise AssertionError("Compare rebuilt one full Assertion carrier")

    monkeypatch.setattr(
        byte_measurement_module,
        "RecordedBytePairAssertion",
        full_carrier_is_not_a_compare_input,
    )

    recorded = get_recorded_pair_measurement_comparison(ledger, result.identity)
    assert recorded["findings"]["conflicting_findings"]
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    representation = record_operator_representation(
        ledger,
        locality_identity=LOCALITY,
        locality_standing=standing,
        source_occurrence_reference=result.identity,
    )
    assert read_operator_representation(
        ledger, representation["representation_event_identity"]
    )["source_occurrence_reference"] == result.identity


def test_later_result_read_revalidates_changed_pair_measurement_evidence():
    ledger, _first_source, _added, earlier, _later, *_middle, result = _comparison()
    get_recorded_pair_measurement_comparison(ledger, result.identity)
    evidence = ledger.get(earlier.material["evidence_of_yield_relation_identity"])
    assert evidence is not None
    evidence.material["result_identity"] = "crossed-pair-result"

    with pytest.raises(
        RecordedPairMeasurementComparisonError,
        match="intact recorded byte-position-pair Measurement",
    ):
        get_recorded_pair_measurement_comparison(ledger, result.identity)


def test_supplied_occurrences_without_a_relation_do_not_create_pair_acts():
    ledger = EventLedger()

    def provider(command, supply):
        assert command == b"!opaque\n"
        supply(
            SuppliedSystemMaterialOccurrence(
                exact_bytes=b"first",
                source_boundary="first opaque occurrence",
                egress=False,
            )
        )
        supply(
            SuppliedSystemMaterialOccurrence(
                exact_bytes=b"second",
                source_boundary="second opaque occurrence",
                egress=False,
            )
        )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="operator-locality",
        input_stream=binary_input(b"!opaque\n"),
        output_stream=StringIO(),
        raw_output_stream=BytesIO(),
        operator_invocation_provider=provider,
    )

    kinds = tuple(event.kind for event in ledger.list())
    assert kinds.count("operator.measurement.byte_counts_recorded") == 3
    assert "operator.measurement.byte_position_pair_counts_recorded" not in kinds
    assert RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND not in kinds
    assert REPRESENTATION_CANDIDATE_RECORDED_KIND not in kinds


def test_preexisting_material_is_a_premise_for_later_operator_turns():
    ledger = EventLedger()
    corpus_occurrence = ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abab",
        source_role="operator",
        source_boundary="earlier corpus occurrence",
    )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"abac\nabca\n"),
        output_stream=StringIO(),
    )

    comparisons = tuple(
        event
        for event in ledger.list()
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )
    assert len(comparisons) == 2
    first_assignment = comparison_module.get_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        comparisons[0].material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ],
    )
    second_assignment = comparison_module.get_recorded_pair_measurement_comparison_responsibility_assignment(
        ledger,
        comparisons[1].material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ],
    )
    assert first_assignment.material["earlier_source_occurrence_references"] == [
        corpus_occurrence.identity
    ]
    assert second_assignment.material["earlier_measurement_reference"] == (
        first_assignment.material["later_measurement_reference"]
    )
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    addressed_sources = {
        coordinates["source_occurrence_reference"]
        for coordinates in standing["representations"].values()
    }
    assert comparisons[0].identity in addressed_sources
    assert comparisons[1].identity in addressed_sources


def test_stale_pair_measurement_is_not_reused_as_the_current_premise():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abab",
        source_role="operator",
        source_boundary="first corpus occurrence",
    )
    stale_pair = _pair_measurement(ledger)
    second_corpus_occurrence = ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abac",
        source_role="operator",
        source_boundary="second corpus occurrence",
    )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b""),
        output_stream=StringIO(),
    )

    current_pairs = tuple(
        event
        for event in ledger.list()
        if event.kind == "operator.measurement.byte_position_pair_counts_recorded"
    )
    assert len(current_pairs) == 2
    assert current_pairs[0].identity == stale_pair.identity
    current_assignment = get_byte_position_pair_measurement_responsibility_assignment(
        ledger,
        current_pairs[1].material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ],
    )
    stale_assignment = get_byte_position_pair_measurement_responsibility_assignment(
        ledger,
        stale_pair.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ],
    )
    assert current_assignment.material["source_occurrence_references"] == [
        {"ingest_occurrence_identity": stale_assignment.material[
            "source_occurrence_references"
        ][0]["ingest_occurrence_identity"]},
        {"ingest_occurrence_identity": second_corpus_occurrence.identity},
    ]


def test_operator_pair_premise_and_compare_survive_reopen(tmp_path):
    database = tmp_path / "operator-pair-compare.sqlite"
    ledger = SQLiteEventLedger(str(database))
    ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"abab",
        source_role="operator",
        source_boundary="durable corpus occurrence",
    )
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(b"abac\n"),
        output_stream=StringIO(),
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    standing = read_operator_locality_standing(
        reopened, locality_identity=LOCALITY
    )
    assert len(standing["comparison_result_occurrences"]) == 1
    comparison_identity = next(iter(standing["comparison_result_occurrences"]))
    recorded = get_recorded_pair_measurement_comparison(
        reopened, comparison_identity
    )
    assignment = comparison_module.get_recorded_pair_measurement_comparison_responsibility_assignment(
        reopened,
        recorded["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ],
    )
    assert assignment.material["added_occurrence_reference"] in {
        occurrence["evidence_event_identity"]
        for occurrence in standing["ingest_occurrences"]
    }
    reopened.close()

    resumed = SQLiteEventLedger(str(database))
    pair_count_before_resume = sum(
        event.kind == "operator.measurement.byte_position_pair_counts_recorded"
        for event in resumed.list()
    )
    run_persistent_operator_console(
        ledger=resumed,
        locality_identity=LOCALITY,
        input_stream=binary_input(b""),
        output_stream=StringIO(),
    )
    resumed_standing = read_operator_locality_standing(
        resumed, locality_identity=LOCALITY
    )
    assert sum(
        event.kind == "operator.measurement.byte_position_pair_counts_recorded"
        for event in resumed.list()
    ) == pair_count_before_resume
    last_representation = next(
        reversed(tuple(resumed_standing["representations"].values()))
    )
    assert last_representation["source_occurrence_reference"] == comparison_identity
    resumed.close()


@pytest.mark.parametrize(
    ("later_material", "expected_finding_counts"),
    (
        (b"bc\n", (0, 2)),
        (b"b", (0, 0)),
    ),
)
def test_zero_pair_premise_comparison_survives_console_and_reopen(
    tmp_path, later_material, expected_finding_counts
):
    database = tmp_path / ("zero-pair-" + str(len(later_material)) + ".sqlite")
    ledger = SQLiteEventLedger(str(database))
    ingest_material(
        ledger,
        locality_identity=LOCALITY,
        exact_bytes=b"a",
        source_role="operator",
        source_boundary="one-byte durable corpus occurrence",
    )
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=LOCALITY,
        input_stream=binary_input(later_material),
        output_stream=StringIO(),
    )
    pair_identities = tuple(
        event.identity
        for event in ledger.list()
        if event.kind == "operator.measurement.byte_position_pair_counts_recorded"
    )
    comparison = next(
        event
        for event in reversed(ledger.list())
        if event.kind == RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND
    )
    assert tuple(
        len(
            assertions_of_recorded_byte_position_pair_measurement(
                ledger, identity
            )
            or ()
        )
        for identity in pair_identities
    ) == expected_finding_counts
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    assert get_recorded_pair_measurement_comparison(
        reopened, comparison.identity
    ) == comparison.material
    pair_count = len(pair_identities)
    run_persistent_operator_console(
        ledger=reopened,
        locality_identity=LOCALITY,
        input_stream=binary_input(b""),
        output_stream=StringIO(),
    )
    assert sum(
        event.kind == "operator.measurement.byte_position_pair_counts_recorded"
        for event in reopened.list()
    ) == pair_count
    reopened.close()


def test_carried_compare_result_is_one_structured_representation_source():
    ledger, *_rest, result = _comparison()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)

    representation = record_operator_representation(
        ledger,
        locality_identity=LOCALITY,
        locality_standing=standing,
        source_occurrence_reference=result.identity,
    )
    recorded = read_operator_representation(
        ledger, representation["representation_event_identity"]
    )

    assert recorded["source_occurrence_reference"] == result.identity
    assert recorded["exact_material"] is None
    assert "representation_rule" not in recorded


def test_compare_result_absent_from_standing_is_refused_as_representation_source():
    ledger, *_rest, result = _comparison()
    standing = read_operator_locality_standing(ledger, locality_identity=LOCALITY)
    standing["comparison_result_occurrences"].pop(result.identity)

    with pytest.raises(ValueError, match="not carried by Standing"):
        record_operator_representation(
            ledger,
            locality_identity=LOCALITY,
            locality_standing=standing,
            source_occurrence_reference=result.identity,
        )


FIDELITY_SUBJECTS = {
    "assertion_standing_coordinates": (
        test_operator_acquisition_carries_the_prior_pair_measurement_into_compare,
        test_operator_occurrence_without_acquisition_cannot_supply_compare,
        test_operator_acquisition_before_the_premise_cannot_supply_compare,
        test_produced_measurements_enter_one_responsible_compare,
        test_same_content_finding_labels_do_not_hide_changed_content,
        test_missing_provenance_cannot_supply_the_compare_rung,
        test_measurement_availability_without_standing_cannot_supply_compare,
        test_corrupted_compare_yield_is_refused,
        test_one_console_call_revalidates_only_the_pair_crossing_a_callback,
        test_changed_pair_crossing_a_callback_cannot_enter_compare_standing,
        test_one_result_read_validates_each_pair_measurement_once,
        test_result_reader_preserves_its_exact_assignment_and_public_getter_delegates,
        test_compare_reads_exact_findings_without_rebuilding_full_assertion_carriers,
        test_later_result_read_revalidates_changed_pair_measurement_evidence,
        test_supplied_occurrences_without_a_relation_do_not_create_pair_acts,
        test_preexisting_material_is_a_premise_for_later_operator_turns,
        test_stale_pair_measurement_is_not_reused_as_the_current_premise,
        test_operator_pair_premise_and_compare_survive_reopen,
        test_zero_pair_premise_comparison_survives_console_and_reopen,
        test_carried_compare_result_is_one_structured_representation_source,
        test_compare_result_absent_from_standing_is_refused_as_representation_source,
    ),
}
