from __future__ import annotations

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    record_byte_pair_occurrence_position_measurement_act_evidence,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
    record_byte_pair_occurrence_position_measurement_result,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.variable_extent_recurrence import (
    get_recorded_corresponding_coordinate_material_measurement,
    get_recorded_variable_extent,
    get_recorded_variable_extent_recurrence,
    iter_recurrent_coordinate_material_findings,
    record_corresponding_coordinate_material_measurements,
    record_variable_extent_steps,
)
import seed_runtime.variable_extent_recurrence as variable_extent_recurrence
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)


def _direct_result(ledger, *, locality, exact):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact variable extent material boundary",
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality
    )
    assignment = (
        record_byte_pair_occurrence_position_measurement_responsibility_assignment(
            ledger,
            source_material_acquisition_occurrence_identity=source.identity,
            locality_standing=standing,
        )
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    return record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )


def _target_surface():
    return [
        {"first_role": 0, "second_role": 1, "result": "difference"},
        {"first_role": 0, "second_role": 2, "result": "same-content"},
        {"first_role": 1, "second_role": 2, "result": "difference"},
    ]


def _target_group(ledger, recurrence_result):
    recurrence = get_recorded_variable_extent_recurrence(
        ledger, recurrence_result.identity
    )
    matching = tuple(
        finding
        for finding in recurrence["findings"]
        if finding["subject"]["complete_compare_findings"] == _target_surface()
    )
    assert len(matching) == 1
    return matching[0]


def _measurement_for_group(ledger, measurements, group):
    matching = tuple(
        get_recorded_corresponding_coordinate_material_measurement(
            ledger, measurement.result_occurrence.identity
        )
        for measurement in measurements
        if measurement.recurrence_finding_reference == group["finding_reference"]
    )
    assert len(matching) == 1
    return matching[0]


def _step_at(run, coordinate_count):
    matching = tuple(
        step for step in run.steps if step.coordinate_count == coordinate_count
    )
    assert len(matching) == 1
    return matching[0]


def test_recurrence_exhausts_source_and_reuses_prior_compare_work():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="variable-extent-positive",
        exact=b"a+aa+a",
    )

    run = record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
    )

    assert tuple(step.coordinate_count for step in run.steps[:2]) == (2, 3)
    assert run.exhausted is True
    assert all(step.new_event_count > 0 for step in run.steps)
    assert direct.identity in run.locality_standing["measurement_occurrences"]
    direct_act = ledger.get(direct.material["responsible_act_evidence_identity"])
    assert run.locality_standing["exact_result_occurrences"][direct.identity] == (
        direct_act.material["responsibility_assignment_reference"]
    )

    final_recurrence = get_recorded_variable_extent_recurrence(
        ledger, run.steps[-1].recurrence_result_occurrence.identity
    )
    recurrent_final_groups = tuple(
        finding
        for finding in final_recurrence["findings"]
        if "recurrence" in finding
    )
    assert recurrent_final_groups == ()

    result_kinds = {
        variable_extent_recurrence.COMPARE_APPLICABILITY_RESULT_KIND,
        variable_extent_recurrence.COMPARE_RESULT_KIND,
        variable_extent_recurrence.EXTENT_MEASUREMENT_RESULT_KIND,
        variable_extent_recurrence.RECURRENCE_MEASUREMENT_RESULT_KIND,
    }
    produced_results = tuple(
        event
        for event in ledger.list_locality("variable-extent-positive")
        if event.kind in result_kinds
    )
    assert produced_results
    for result in produced_results:
        act = ledger.get(result.material["responsible_act_evidence_identity"])
        reference = act.material["responsibility_assignment_reference"]
        assignment = ledger.get(reference["recorded_occurrence_identity"])
        assert run.locality_standing["exact_result_occurrences"][result.identity] == (
            reference
        )
        assert (
            run.locality_standing["responsibility_assignment_occurrences"].get(
                assignment.identity, object()
            )
            is None
        )
        if result.kind == variable_extent_recurrence.COMPARE_APPLICABILITY_RESULT_KIND:
            assert (
                run.locality_standing["applicability_result_occurrences"].get(
                    result.identity, object()
                )
                is None
            )
        elif result.kind == variable_extent_recurrence.COMPARE_RESULT_KIND:
            assert (
                run.locality_standing["comparison_result_occurrences"].get(
                    result.identity, object()
                )
                is None
            )
        else:
            assert result.identity in run.locality_standing[
                "measurement_occurrences"
            ]
        assert assignment.material["subject"] == act.material["coordinates"]["subject"]
        assert assignment.material["result_boundary_identity"] == result.material[
            "result_identity"
        ]

    by_length_and_start = {}
    for step in run.steps:
        for event in step.extent_result_occurrences:
            reading = get_recorded_variable_extent(ledger, event.identity)
            start = reading["source_position_coordinates"][0]["position"]
            by_length_and_start[step.coordinate_count, start] = reading

    length_two = by_length_and_start[2, 0]
    length_three = by_length_and_start[3, 0]
    assert length_three["compare_result_references"][:1] == length_two[
        "compare_result_references"
    ]
    assert len(length_three["new_compare_result_references"]) == 2

    target_recurrence = _step_at(run, 3).recurrence_result_occurrence
    group = _target_group(ledger, target_recurrence)
    assert "recurrence" in group
    assert group["count"] == 2
    assert tuple(
        get_recorded_variable_extent(
            ledger, reference["recorded_occurrence_reference"]
        )["source_position_coordinates"][0]["position"]
        for reference in group["support_result_references"]
    ) == (0, 3)

    # This explicit producer-result to consumer call is the remaining
    # hand-written continuation. It supplies the complete recurrence result;
    # the consumer chooses no group, role, or value from it.
    coordinate_run = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=target_recurrence.identity,
        locality_standing=run.locality_standing,
    )
    measurements = coordinate_run.measurements
    target_measurement = _measurement_for_group(ledger, measurements, group)
    assert all(
        measurement.result_occurrence.identity
        in coordinate_run.locality_standing["measurement_occurrences"]
        for measurement in measurements
    )
    assert all(
        coordinate_run.locality_standing["exact_result_occurrences"][
            measurement.result_occurrence.identity
        ]
        == ledger.get(
            measurement.result_occurrence.material[
                "responsible_act_evidence_identity"
            ]
        ).material["responsibility_assignment_reference"]
        for measurement in measurements
    )
    assert all(
        ledger.get(
            ledger.get(
                measurement.result_occurrence.material[
                    "responsible_act_evidence_identity"
                ]
            ).material["responsibility_assignment_reference"][
                "recorded_occurrence_identity"
            ]
        ).identity
        in coordinate_run.locality_standing[
            "responsibility_assignment_occurrences"
        ]
        for measurement in measurements
    )
    assert coordinate_run.locality_standing == read_operator_locality_standing(
        ledger, locality_identity="variable-extent-positive"
    )
    recurrent = {
        (
            finding["subject"]["coordinate_role"],
            bytes(finding["subject"]["exact_material"]),
        ): finding
        for finding in target_measurement["findings"]
        if "recurrence" in finding
    }

    assert recurrent[1, b"+"]["count"] == 2
    assert tuple(
        (finding["subject"]["coordinate_role"], finding["count"])
        for finding in iter_recurrent_coordinate_material_findings(
            ledger, measurements
        )
        if finding["finding_reference"] in {
            recurrent[1, b"+"]["finding_reference"],
        }
    ) == ((1, 2),)


def test_same_internal_surface_does_not_create_varying_literal_recurrence():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="variable-extent-control",
        exact=b"a+aa-a",
    )
    run = record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
    )
    target_recurrence = _step_at(run, 3).recurrence_result_occurrence
    group = _target_group(ledger, target_recurrence)
    assert "recurrence" in group
    assert group["count"] == 2

    coordinate_run = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=target_recurrence.identity,
        locality_standing=run.locality_standing,
    )
    measurements = coordinate_run.measurements
    target_measurement = _measurement_for_group(ledger, measurements, group)
    varying_roles = tuple(
        finding
        for finding in target_measurement["findings"]
        if finding["subject"]["coordinate_role"] == 1
    )

    assert {
        (finding["subject"]["coordinate_role"], bytes(finding["subject"]["exact_material"]))
        for finding in varying_roles
    } == {
        (1, b"+"),
        (1, b"-"),
    }
    assert all(finding["count"] == 1 for finding in varying_roles)
    assert all("recurrence" not in finding for finding in varying_roles)


def test_changed_extent_coordinate_is_refused():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="variable-extent-integrity",
        exact=b"aba",
    )
    run = record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
    )
    result = ledger.get(run.steps[0].extent_result_occurrences[0].identity)
    act = ledger.get(result.material["responsible_act_evidence_identity"])
    assignment = ledger.get(
        act.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    exact_result_boundary = assignment.material["result_boundary_identity"]
    assignment.material["result_boundary_identity"] = "changed-result-boundary"
    try:
        get_recorded_variable_extent(ledger, result.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed Responsibility ownership was accepted")
    assignment.material["result_boundary_identity"] = exact_result_boundary

    yielded = ledger.get(result.material["evidence_of_yield_relation_identity"])
    exact_yield_occurrence = yielded.material["dimensions"][
        "act_occurrence_identity"
    ]
    yielded.material["dimensions"]["act_occurrence_identity"] = "changed-yield"
    try:
        read_operator_locality_standing(
            ledger, locality_identity="variable-extent-integrity"
        )
    except ValueError:
        pass
    else:
        raise AssertionError("changed Yield was accepted into current Standing")
    yielded.material["dimensions"][
        "act_occurrence_identity"
    ] = exact_yield_occurrence

    result.material["coordinates"]["source_position_coordinates"][0][
        "exact_material"
    ] = [ord("x")]

    try:
        get_recorded_variable_extent(ledger, result.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed extent coordinate was accepted")


def test_bounded_variable_extent_recording_reuses_validated_direct_coordinates(
    monkeypatch,
):
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="variable-extent-bounded-validation",
        exact=b"a+aa+a",
    )
    calls = 0
    exact_reader = (
        variable_extent_recurrence.source_position_coordinate_references_of_recorded_position_measurement
    )

    def counted_reader(ledger, result_event_identity):
        nonlocal calls
        calls += 1
        return exact_reader(ledger, result_event_identity)

    monkeypatch.setattr(
        variable_extent_recurrence,
        "source_position_coordinate_references_of_recorded_position_measurement",
        counted_reader,
    )

    record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
    )

    # The recording boundary and its bounded Standing advance each validate
    # the direct result. Sibling Compare/Measurement results reuse those exact
    # validated coordinates instead of reconstructing the source population.
    assert calls == 2


def test_interior_coordinate_set_survives_unrelated_surrounding_material():
    readings = []
    for locality, exact, start in (
        ("variable-extent-isolated", b"aba", 0),
        ("variable-extent-surrounded", b"xabay", 1),
    ):
        ledger = EventLedger()
        direct = _direct_result(ledger, locality=locality, exact=exact)
        run = record_variable_extent_steps(
            ledger,
            direct_result_event_identity=direct.identity,
        )
        matching = []
        for event in _step_at(run, 3).extent_result_occurrences:
            reading = get_recorded_variable_extent(ledger, event.identity)
            if reading["source_position_coordinates"][0]["position"] == start:
                matching.append(reading)
        assert len(matching) == 1
        readings.append(matching[0])

    assert tuple(
        bytes(coordinate["exact_material"])
        for coordinate in readings[0]["source_position_coordinates"]
    ) == (b"a", b"b", b"a")
    assert readings[0]["complete_compare_findings"] == readings[1][
        "complete_compare_findings"
    ]


def test_variable_extent_results_and_coordinate_measurements_survive_restart(tmp_path):
    database = tmp_path / "variable-extent.sqlite"
    ledger = SQLiteEventLedger(str(database))
    direct = _direct_result(
        ledger,
        locality="variable-extent-restart",
        exact=b"aba",
    )
    run = record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
    )
    coordinate_run = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=(
            run.steps[0].recurrence_result_occurrence.identity
        ),
        locality_standing=run.locality_standing,
    )
    measurements = coordinate_run.measurements
    extent_identity = run.steps[-1].extent_result_occurrences[0].identity
    recurrence_identity = run.steps[0].recurrence_result_occurrence.identity
    measurement_identities = tuple(
        measurement.result_occurrence.identity for measurement in measurements
    )
    expected_extent = get_recorded_variable_extent(ledger, extent_identity)
    expected_recurrence = get_recorded_variable_extent_recurrence(
        ledger, recurrence_identity
    )
    expected_measurements = tuple(
        get_recorded_corresponding_coordinate_material_measurement(ledger, identity)
        for identity in measurement_identities
    )
    expected_ownership = coordinate_run.locality_standing[
        "exact_result_occurrences"
    ]
    ledger.close()

    reopened = SQLiteEventLedger(str(database))
    try:
        assert get_recorded_variable_extent(reopened, extent_identity) == expected_extent
        assert (
            get_recorded_variable_extent_recurrence(reopened, recurrence_identity)
            == expected_recurrence
        )
        assert tuple(
            get_recorded_corresponding_coordinate_material_measurement(
                reopened, identity
            )
            for identity in measurement_identities
        ) == expected_measurements
        assert read_operator_locality_standing(
            reopened, locality_identity="variable-extent-restart"
        )["exact_result_occurrences"] == expected_ownership
    finally:
        reopened.close()


PYTEST_ADMISSION = (
    test_recurrence_exhausts_source_and_reuses_prior_compare_work,
    test_same_internal_surface_does_not_create_varying_literal_recurrence,
    test_changed_extent_coordinate_is_refused,
    test_bounded_variable_extent_recording_reuses_validated_direct_coordinates,
    test_interior_coordinate_set_survives_unrelated_surrounding_material,
    test_variable_extent_results_and_coordinate_measurements_survive_restart,
)
