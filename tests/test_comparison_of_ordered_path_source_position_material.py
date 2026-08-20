from __future__ import annotations

import pytest

from seed_runtime.comparison_of_ordered_path_source_position_material import (
    COMPARE_RESULT_KIND,
    get_recorded_ordered_path_source_position_material_comparison,
    record_ordered_path_source_position_material_comparison,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    record_byte_pair_occurrence_position_measurement_act_evidence,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
    record_byte_pair_occurrence_position_measurement_result,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    ordered_source_position_coordinates_beside_ordered_relation_path_assertion,
)
from tests.test_measurement_of_shared_position_of_byte_pair_occurrences import (
    _direct_d2,
    _record_d2_shared_path,
    _standing,
)
from seed_runtime.ordered_path_source_position_continuation import (
    yield_ordered_path_source_position_continuations,
)
from tests.operator_material_acquisition_test_witness import (
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


def _comparison(ledger, *, locality, exact, position=1):
    path = _path(ledger, locality=locality, exact=exact, position=position)
    recorded = record_ordered_path_source_position_material_comparison(
        ledger,
        path_result_event_identity=path.identity,
        locality_standing=_standing(ledger, locality),
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
        record_byte_pair_occurrence_position_measurement_responsibility_assignment(
            ledger,
            source_material_acquisition_occurrence_identity=source.identity,
            locality_standing=_standing(ledger, locality),
        )
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    return result


def test_path_first_and_final_equal_material_yield_same_content():
    ledger = EventLedger()
    path, recorded = _comparison(
        ledger, locality="ordered-path-endpoint-same", exact=b"2+2=5\n"
    )

    reading = get_recorded_ordered_path_source_position_material_comparison(
        ledger, recorded.result_occurrence.identity
    )
    _assertion, positions = (
        ordered_source_position_coordinates_beside_ordered_relation_path_assertion(
            ledger, path.identity
        )
    )

    assert recorded.result_occurrence.kind == COMPARE_RESULT_KIND
    assert tuple(position["position"] for position in positions) == (0, 1, 2)
    assert reading["finding"]["result"] == "same-content"
    assert reading["finding"]["subject"][
        "first_source_position_coordinate"
    ] == positions[0]
    assert reading["finding"]["subject"][
        "second_source_position_coordinate"
    ] == positions[2]
    assert reading["finding"]["subject"][
        "first_source_position_coordinate"
    ]["exact_material"] == [ord("2")]
    assert reading["finding"]["subject"][
        "second_source_position_coordinate"
    ]["exact_material"] == [ord("2")]
    assert recorded.result_occurrence.identity in recorded.locality_standing[
        "comparison_result_occurrences"
    ]


def test_path_first_and_final_different_material_yield_difference():
    ledger = EventLedger()
    _path_result, recorded = _comparison(
        ledger, locality="ordered-path-endpoint-difference", exact=b"abc"
    )

    reading = get_recorded_ordered_path_source_position_material_comparison(
        ledger, recorded.result_occurrence.identity
    )

    assert reading["finding"]["result"] == "difference"
    assert reading["finding"]["subject"][
        "first_source_position_coordinate"
    ]["exact_material"] == [ord("a")]
    assert reading["finding"]["subject"][
        "second_source_position_coordinate"
    ]["exact_material"] == [ord("c")]


def test_endpoint_comparison_refuses_a_changed_path_coordinate():
    ledger = EventLedger()
    _path_result, recorded = _comparison(
        ledger, locality="ordered-path-endpoint-refusal", exact=b"aba"
    )
    result = ledger.get(recorded.result_occurrence.identity)
    result.material["finding"]["subject"]["second_source_position_coordinate"][
        "exact_material"
    ] = [ord("x")]

    with pytest.raises(ValueError):
        get_recorded_ordered_path_source_position_material_comparison(
            ledger, result.identity
        )


def test_endpoint_comparison_survives_sqlite_restart(tmp_path):
    database = tmp_path / "ordered-path-endpoint-compare.sqlite"
    ledger = SQLiteEventLedger(str(database))
    _path_result, recorded = _comparison(
        ledger, locality="ordered-path-endpoint-restart", exact=b"aba"
    )
    identity = recorded.result_occurrence.identity
    expected = get_recorded_ordered_path_source_position_material_comparison(
        ledger, identity
    )
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    try:
        assert get_recorded_ordered_path_source_position_material_comparison(
            reopened, identity
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
            locality_standing=_standing(ledger, locality),
        )
    )

    assert tuple(
        continuation.source_position_coordinate["position"]
        for continuation in continuations
    ) == tuple(range(6))
    assert sum(
        continuation.ordered_path_result is not None
        for continuation in continuations
    ) == 4
    assert sum(
        continuation.comparison_result is not None
        for continuation in continuations
    ) == 4
    findings = {
        continuation.source_position_coordinate["position"]: (
            continuation.comparison_result.material["finding"]["result"]
            if continuation.comparison_result is not None
            else None
        )
        for continuation in continuations
    }
    assert findings == {
        0: None,
        1: "same-content",
        2: "difference",
        3: "difference",
        4: "difference",
        5: None,
    }


def test_one_source_position_continuation_yields_before_its_siblings():
    ledger = EventLedger()
    locality = "ordered-path-source-position-independent-continuations"
    direct = _direct_position_result(ledger, locality=locality, exact=b"abc")
    continuations = yield_ordered_path_source_position_continuations(
        ledger,
        direct_result_event_identity=direct.identity,
        locality_standing=_standing(ledger, locality),
    )

    first = next(continuations)
    assert first.source_position_coordinate["position"] == 0
    assert first.ordered_path_result is None
    events_after_first = len(ledger.list_events())

    second = next(continuations)
    assert len(ledger.list_events()) > events_after_first
    assert second.source_position_coordinate["position"] == 1
    assert second.ordered_path_result is not None
    assert second.comparison_result.material["finding"]["result"] == "difference"


PYTEST_ADMISSION = (
    test_path_first_and_final_equal_material_yield_same_content,
    test_path_first_and_final_different_material_yield_difference,
    test_endpoint_comparison_refuses_a_changed_path_coordinate,
    test_endpoint_comparison_survives_sqlite_restart,
    test_each_exact_source_position_continues_without_a_chosen_subject,
    test_one_source_position_continuation_yields_before_its_siblings,
)
