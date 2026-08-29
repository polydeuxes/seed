"""Every same-position Measurement position is addressed by Compare."""

from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.comparison_of_shared_position_source_position_material import (
    APPLICABILITY_ACT_KIND,
    APPLICABILITY_RESULT_KIND,
    APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    COMPARE_RESULT_KIND,
    get_recorded_shared_position_source_position_material_comparison,
    yield_shared_position_source_position_material_comparisons,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    record_byte_pair_occurrence_position_measurement_result,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    source_position_coordinates_of_shared_position_result,
)
from tests.test_measurement_of_shared_position_of_byte_pair_occurrences import (
    _direct_d2,
    _record_d2_shared_position,
    _current_coordinates,
)
from seed_runtime.source_position_determination_and_comparison import (
    yield_source_position_determinations_and_comparisons,
)
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.yield_relation import RECORDED_YIELD_RELATION_EVENT


def _shared_position(ledger, *, locality, exact, position=1):
    _source, _direct, determination = _direct_d2(
        ledger,
        locality=locality,
        exact=exact,
        position=position,
    )
    return _record_d2_shared_position(ledger, locality, determination)[-1]


def _comparisons(ledger, *, locality, exact, position=1):
    shared_position = _shared_position(ledger, locality=locality, exact=exact, position=position)
    recorded = tuple(
        yield_shared_position_source_position_material_comparisons(
            ledger,
            shared_position_measurement_result_event_identity=shared_position.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    )
    return shared_position, recorded


def _direct_position_result(ledger, *, locality, exact):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact material boundary",
    )
    binding = (
        record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding.identity,
        binding_current_coordinates=_current_coordinates(ledger, locality),
    )
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    return result


def test_every_source_position_pair_is_compared_without_a_chosen_pair():
    ledger = EventLedger()
    shared_position, recorded = _comparisons(
        ledger, locality="shared-position-pair-population", exact=b"2+2=5\n"
    )
    _assertion, positions = (
        source_position_coordinates_of_shared_position_result(
            ledger, shared_position.identity
        )
    )
    readings = tuple(
        get_recorded_shared_position_source_position_material_comparison(
            ledger, comparison.result_occurrence.identity
        )
        for comparison in recorded
    )

    assert tuple(position["position"] for position in positions) == (0, 1, 2)
    assert tuple(reading["source_position_pair"] for reading in readings) == (
        [0, 1],
        [0, 2],
        [1, 2],
    )
    assert tuple(reading["finding"]["result"] for reading in readings) == (
        "difference",
        "same-content",
        "difference",
    )
    assert tuple(
        (
            reading["finding"]["subject"][
                "first_source_position_coordinate"
            ]["exact_material"],
            reading["finding"]["subject"][
                "second_source_position_coordinate"
            ]["exact_material"],
        )
        for reading in readings
    ) == (
        ([ord("2")], [ord("+")]),
        ([ord("2")], [ord("2")]),
        ([ord("+")], [ord("2")]),
    )
    assert all(
        comparison.result_occurrence.kind == COMPARE_RESULT_KIND
        and "yield_relation_identity" not in comparison.result_occurrence.material
        and comparison.result_occurrence.identity
        in comparison.current_coordinates["comparison_result_occurrences"]
        for comparison in recorded
    )
    assert not tuple(
        event
        for event in ledger.iter_locality_kind(
            "shared-position-pair-population", RECORDED_YIELD_RELATION_EVENT
        )
        if event.material.get("occurrence_boundary")
        == "comparison_of_shared_position_source_position_material_compare"
    )
    applicability_results = tuple(
        ledger.iter_locality_kind(
            "shared-position-pair-population", APPLICABILITY_RESULT_KIND
        )
    )
    assert applicability_results == ()
    assert not tuple(
        event
        for event in ledger.list_locality("shared-position-pair-population")
        if event.kind
        in {
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
            APPLICABILITY_ACT_KIND,
            APPLICABILITY_RESULT_KIND,
        }
    )
    assert not tuple(
        event
        for event in ledger.iter_locality_kind(
            "shared-position-pair-population", RECORDED_YIELD_RELATION_EVENT
        )
        if event.material.get("occurrence_boundary")
        == "comparison_of_shared_position_source_position_material_applicability"
    )
    binding_occurrences = tuple(
        ledger.get(identity)
        for identity in recorded[-1].current_coordinates[
            "subject_to_act_binding_occurrences"
        ]
        if ledger.get(identity).kind
        in {
            COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
            APPLICABILITY_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
        }
    )
    assert tuple(event.kind for event in binding_occurrences) == (
        COMPARE_SUBJECT_TO_ACT_BINDING_RECORDED_EVENT,
    ) * 3
    assert all(
        "applicability_result_event_identity"
        not in comparison.result_occurrence.material
        for comparison in recorded
    )


def test_repeated_compare_result_is_refused_without_applicability():
    ledger = EventLedger()
    _shared_position_result, recorded = _comparisons(
        ledger, locality="repeated-compare-result", exact=b"2+2=5\n"
    )
    comparison_result = recorded[0].result_occurrence
    ledger.append(
        COMPARE_RESULT_KIND,
        deepcopy(comparison_result.material),
        locality_identity=comparison_result.locality_identity,
    )

    with pytest.raises(ValueError, match="single exact result"):
        get_recorded_shared_position_source_position_material_comparison(
            ledger, comparison_result.identity
        )


def test_three_different_source_position_coordinates_yield_three_differences():
    ledger = EventLedger()
    _shared_position_result, recorded = _comparisons(
        ledger, locality="shared-position-pair-difference", exact=b"abc"
    )
    readings = tuple(
        get_recorded_shared_position_source_position_material_comparison(
            ledger, comparison.result_occurrence.identity
        )
        for comparison in recorded
    )

    assert tuple(reading["finding"]["result"] for reading in readings) == (
        "difference",
        "difference",
        "difference",
    )


def test_three_equal_source_position_coordinates_yield_three_same_content_findings():
    ledger = EventLedger()
    _shared_position_result, recorded = _comparisons(
        ledger, locality="shared-position-pair-same-content", exact=b"aaa"
    )

    assert tuple(
        get_recorded_shared_position_source_position_material_comparison(
            ledger, comparison.result_occurrence.identity
        )["finding"]["result"]
        for comparison in recorded
    ) == ("same-content", "same-content", "same-content")


def test_source_position_pair_comparison_refuses_a_changed_source_position_coordinate():
    ledger = EventLedger()
    _shared_position_result, comparisons = _comparisons(
        ledger, locality="shared-position-pair-refusal", exact=b"aba"
    )
    recorded = comparisons[1]
    result = ledger.get(recorded.result_occurrence.identity)
    result.material["finding"]["subject"]["second_source_position_coordinate"][
        "exact_material"
    ] = [ord("x")]

    with pytest.raises(ValueError):
        get_recorded_shared_position_source_position_material_comparison(
            ledger, result.identity
        )


def test_source_position_pair_comparisons_survive_sqlite_restart(tmp_path):
    database = tmp_path / "shared-position-pair-compare.sqlite"
    ledger = SQLiteEventLedger(str(database))
    with ledger.batched():
        shared_position = _shared_position(
            ledger, locality="shared-position-pair-restart", exact=b"aba"
        )
        recorded = (
            next(
                yield_shared_position_source_position_material_comparisons(
                    ledger,
                    shared_position_measurement_result_event_identity=shared_position.identity,
                    current_coordinates=_current_coordinates(
                        ledger, "shared-position-pair-restart"
                    ),
                )
            ),
        )
    identities = tuple(
        comparison.result_occurrence.identity for comparison in recorded
    )
    expected = tuple(
        get_recorded_shared_position_source_position_material_comparison(
            ledger, identity
        )
        for identity in identities
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    try:
        assert tuple(
            get_recorded_shared_position_source_position_material_comparison(
                reopened, identity
            )
            for identity in identities
        ) == expected
    finally:
        reopened.close()


def test_each_exact_source_position_is_determined_without_a_chosen_subject():
    ledger = EventLedger()
    locality = "shared-position-source-position-determination"
    direct = _direct_position_result(
        ledger, locality=locality, exact=b"aba"
    )

    results = tuple(
        yield_source_position_determinations_and_comparisons(
            ledger,
            direct_result_event_identity=direct.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    )

    assert tuple(
        dict.fromkeys(
            result.source_position_coordinate["position"]
            for result in results
        )
    ) == tuple(range(3))
    assert len(results) == 5
    assert sum(
        result.shared_position_result is not None
        for result in results
    ) == 3
    assert sum(
        result.comparison_result is not None
        for result in results
    ) == 3
    centered_on_plus = tuple(
        result.comparison_result.material
        for result in results
        if result.source_position_coordinate["position"] == 1
    )
    assert tuple(
        material["source_position_pair"] for material in centered_on_plus
    ) == ([0, 1], [0, 2], [1, 2])
    assert tuple(
        material["finding"]["result"] for material in centered_on_plus
    ) == ("difference", "same-content", "difference")


def test_a_changed_prefix_is_refused_before_another_result_is_exposed():
    ledger = EventLedger()
    locality = "changed-shared-position-source-prefix"
    direct = _direct_position_result(ledger, locality=locality, exact=b"aba")
    source = ledger.list(
        through=ledger.append_boundary_through_occurrence(direct.identity)
    )[0]
    original_material = deepcopy(source.material)
    results = yield_source_position_determinations_and_comparisons(
        ledger,
        direct_result_event_identity=direct.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )

    first = next(results)
    source.material["unknown"] = ["changed after first result"]
    with pytest.raises(ValueError):
        next(results)

    assert first.source_position_coordinate["position"] == 0
    source.material.clear()
    source.material.update(original_material)


def test_one_source_position_pair_yields_before_its_sibling_pairs():
    ledger = EventLedger()
    locality = "shared-position-pair-independent-recording"
    shared_position = _shared_position(ledger, locality=locality, exact=b"abc")
    comparisons = yield_shared_position_source_position_material_comparisons(
        ledger,
        shared_position_measurement_result_event_identity=shared_position.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )

    first = next(comparisons)
    assert first.result_occurrence.material["source_position_pair"] == [0, 1]
    events_after_first = len(ledger.list_events())

    second = next(comparisons)
    assert len(ledger.list_events()) > events_after_first
    assert second.result_occurrence.material["source_position_pair"] == [0, 2]
    assert first.result_occurrence.material["finding"]["result"] == "difference"
    assert second.result_occurrence.material["finding"]["result"] == "difference"
