from __future__ import annotations

from copy import deepcopy

import pytest

from seed_runtime.comparison_of_ordered_path_source_position_material import (
    COMPARE_RESULT_KIND,
    get_recorded_ordered_path_source_position_material_comparison,
    yield_ordered_path_source_position_material_comparisons,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    record_byte_pair_occurrence_position_measurement_result,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    ordered_source_position_coordinates_adjacent_to_ordered_relation_path_assertion,
)
from tests.test_measurement_of_shared_position_of_byte_pair_occurrences import (
    _direct_d2,
    _record_d2_shared_path,
    _current_coordinates,
)
from seed_runtime.ordered_path_source_position_continuation import (
    yield_ordered_path_source_position_continuations,
)
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)


def _path(ledger, *, locality, exact, position=1):
    _source, _direct, determination = _direct_d2(
        ledger,
        locality=locality,
        exact=exact,
        position=position,
    )
    return _record_d2_shared_path(ledger, locality, determination)[-1]


def _comparisons(ledger, *, locality, exact, position=1):
    path = _path(ledger, locality=locality, exact=exact, position=position)
    recorded = tuple(
        yield_ordered_path_source_position_material_comparisons(
            ledger,
            path_result_event_identity=path.identity,
            locality_standing=_current_coordinates(ledger, locality),
        )
    )
    return path, recorded


def _direct_position_result(ledger, *, locality, exact):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact material boundary",
    )
    assignment = (
        record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
            ledger,
            source_material_result_occurrence_identity=source.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    )
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=assignment.identity,
        binding_current_coordinates=_current_coordinates(ledger, locality),
    )
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )
    return result


def test_every_path_ordered_pair_is_compared_without_a_chosen_pair():
    ledger = EventLedger()
    path, recorded = _comparisons(
        ledger, locality="ordered-path-pair-population", exact=b"2+2=5\n"
    )
    _assertion, positions = (
        ordered_source_position_coordinates_adjacent_to_ordered_relation_path_assertion(
            ledger, path.identity
        )
    )
    readings = tuple(
        get_recorded_ordered_path_source_position_material_comparison(
            ledger, comparison.result_occurrence.identity
        )
        for comparison in recorded
    )

    assert tuple(position["position"] for position in positions) == (0, 1, 2)
    assert tuple(reading["path_position_pair"] for reading in readings) == (
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
        and comparison.result_occurrence.identity
        in comparison.locality_standing["comparison_result_occurrences"]
        for comparison in recorded
    )


def test_three_different_path_coordinates_yield_three_differences():
    ledger = EventLedger()
    _path_result, recorded = _comparisons(
        ledger, locality="ordered-path-pair-difference", exact=b"abc"
    )
    readings = tuple(
        get_recorded_ordered_path_source_position_material_comparison(
            ledger, comparison.result_occurrence.identity
        )
        for comparison in recorded
    )

    assert tuple(reading["finding"]["result"] for reading in readings) == (
        "difference",
        "difference",
        "difference",
    )


def test_three_equal_path_coordinates_yield_three_same_content_findings():
    ledger = EventLedger()
    _path_result, recorded = _comparisons(
        ledger, locality="ordered-path-pair-same-content", exact=b"aaa"
    )

    assert tuple(
        get_recorded_ordered_path_source_position_material_comparison(
            ledger, comparison.result_occurrence.identity
        )["finding"]["result"]
        for comparison in recorded
    ) == ("same-content", "same-content", "same-content")


def test_path_pair_comparison_refuses_a_changed_path_coordinate():
    ledger = EventLedger()
    _path_result, comparisons = _comparisons(
        ledger, locality="ordered-path-pair-refusal", exact=b"aba"
    )
    recorded = comparisons[1]
    result = ledger.get(recorded.result_occurrence.identity)
    result.material["finding"]["subject"]["second_source_position_coordinate"][
        "exact_material"
    ] = [ord("x")]

    with pytest.raises(ValueError):
        get_recorded_ordered_path_source_position_material_comparison(
            ledger, result.identity
        )


def test_path_pair_comparisons_survive_sqlite_restart(tmp_path):
    database = tmp_path / "ordered-path-pair-compare.sqlite"
    ledger = SQLiteEventLedger(str(database))
    _path_result, recorded = _comparisons(
        ledger, locality="ordered-path-pair-restart", exact=b"aba"
    )
    identities = tuple(
        comparison.result_occurrence.identity for comparison in recorded
    )
    expected = tuple(
        get_recorded_ordered_path_source_position_material_comparison(
            ledger, identity
        )
        for identity in identities
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    try:
        assert tuple(
            get_recorded_ordered_path_source_position_material_comparison(
                reopened, identity
            )
            for identity in identities
        ) == expected
    finally:
        reopened.close()


def test_each_exact_source_position_continues_without_a_chosen_subject():
    ledger = EventLedger()
    locality = "ordered-path-source-position-continuation"
    direct = _direct_position_result(
        ledger, locality=locality, exact=b"2+2=5\n"
    )

    continuations = tuple(
        yield_ordered_path_source_position_continuations(
            ledger,
            direct_result_event_identity=direct.identity,
            current_coordinates=_current_coordinates(ledger, locality),
        )
    )

    assert tuple(
        dict.fromkeys(
            continuation.source_position_coordinate["position"]
            for continuation in continuations
        )
    ) == tuple(range(6))
    assert len(continuations) == 14
    assert sum(
        continuation.ordered_path_result is not None
        for continuation in continuations
    ) == 12
    assert sum(
        continuation.comparison_result is not None
        for continuation in continuations
    ) == 12
    centered_on_plus = tuple(
        continuation.comparison_result.material
        for continuation in continuations
        if continuation.source_position_coordinate["position"] == 1
    )
    assert tuple(
        material["path_position_pair"] for material in centered_on_plus
    ) == ([0, 1], [0, 2], [1, 2])
    assert tuple(
        material["finding"]["result"] for material in centered_on_plus
    ) == ("difference", "same-content", "difference")


def test_a_changed_prefix_is_refused_before_another_continuation_is_exposed():
    ledger = EventLedger()
    locality = "changed-ordered-path-source-prefix"
    direct = _direct_position_result(ledger, locality=locality, exact=b"2+2=5\n")
    source = ledger.list(
        through=ledger.append_boundary_through_occurrence(direct.identity)
    )[0]
    original_material = deepcopy(source.material)
    continuations = yield_ordered_path_source_position_continuations(
        ledger,
        direct_result_event_identity=direct.identity,
        current_coordinates=_current_coordinates(ledger, locality),
    )

    first = next(continuations)
    source.material["unknown"] = ["changed after first continuation"]
    with pytest.raises(
        ValueError,
        match="source changed during its bounded continuation",
    ):
        next(continuations)

    assert first.source_position_coordinate["position"] == 0
    source.material.clear()
    source.material.update(original_material)


def test_one_path_pair_yields_before_its_sibling_pairs():
    ledger = EventLedger()
    locality = "ordered-path-pair-independent-continuations"
    path = _path(ledger, locality=locality, exact=b"abc")
    comparisons = yield_ordered_path_source_position_material_comparisons(
        ledger,
        path_result_event_identity=path.identity,
        locality_standing=_current_coordinates(ledger, locality),
    )

    first = next(comparisons)
    assert first.result_occurrence.material["path_position_pair"] == [0, 1]
    events_after_first = len(ledger.list_events())

    second = next(comparisons)
    assert len(ledger.list_events()) > events_after_first
    assert second.result_occurrence.material["path_position_pair"] == [0, 2]
    assert first.result_occurrence.material["finding"]["result"] == "difference"
    assert second.result_occurrence.material["finding"]["result"] == "difference"
