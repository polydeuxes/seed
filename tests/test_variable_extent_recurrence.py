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
        {"first_role": 0, "second_role": 3, "result": "difference"},
        {"first_role": 1, "second_role": 3, "result": "difference"},
        {"first_role": 2, "second_role": 3, "result": "difference"},
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


def test_two_extensions_reuse_prior_compare_work_and_expose_literal_recurrence():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="variable-extent-positive",
        exact=b"2+2=\n3+3=\n4+4=",
    )

    run = record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
        extension_count=2,
    )

    assert tuple(step.coordinate_count for step in run.steps) == (2, 3, 4)
    assert all(step.new_event_count > 0 for step in run.steps)

    by_length_and_start = {}
    for step in run.steps:
        for event in step.extent_result_occurrences:
            reading = get_recorded_variable_extent(ledger, event.identity)
            start = reading["source_position_coordinates"][0]["position"]
            by_length_and_start[step.coordinate_count, start] = reading

    length_two = by_length_and_start[2, 0]
    length_three = by_length_and_start[3, 0]
    length_four = by_length_and_start[4, 0]
    assert length_three["compare_result_references"][:1] == length_two[
        "compare_result_references"
    ]
    assert len(length_three["new_compare_result_references"]) == 2
    assert length_four["compare_result_references"][:3] == length_three[
        "compare_result_references"
    ]
    assert len(length_four["new_compare_result_references"]) == 3

    final_recurrence = run.steps[-1].recurrence_result_occurrence
    group = _target_group(ledger, final_recurrence)
    assert "recurrence" in group
    assert group["count"] == 3
    assert tuple(
        get_recorded_variable_extent(
            ledger, reference["recorded_occurrence_reference"]
        )["source_position_coordinates"][0]["position"]
        for reference in group["support_result_references"]
    ) == (0, 5, 10)

    # This explicit producer-result to consumer call is the remaining
    # hand-written continuation. It supplies the complete recurrence result;
    # the consumer chooses no group, role, or value from it.
    coordinate_run = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=final_recurrence.identity,
        locality_standing=run.locality_standing,
    )
    measurements = coordinate_run.measurements
    target_measurement = _measurement_for_group(ledger, measurements, group)
    assert all(
        measurement.result_occurrence.identity
        in coordinate_run.locality_standing["measurement_occurrences"]
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

    assert recurrent[1, b"+"]["count"] == 3
    assert recurrent[3, b"="]["count"] == 3
    assert all(
        "recurrence" not in finding
        for finding in target_measurement["findings"]
        if finding["subject"]["coordinate_role"] in {0, 2}
    )
    assert tuple(
        (finding["subject"]["coordinate_role"], finding["count"])
        for finding in iter_recurrent_coordinate_material_findings(
            ledger, measurements
        )
        if finding["finding_reference"] in {
            recurrent[1, b"+"]["finding_reference"],
            recurrent[3, b"="]["finding_reference"],
        }
    ) == ((1, 3), (3, 3))


def test_same_internal_surface_does_not_create_varying_literal_recurrence():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="variable-extent-control",
        exact=b"2+2=\n3-3#\n4x4?",
    )
    run = record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
        extension_count=2,
    )
    final_recurrence = run.steps[-1].recurrence_result_occurrence
    group = _target_group(ledger, final_recurrence)
    assert "recurrence" in group
    assert group["count"] == 3

    coordinate_run = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=final_recurrence.identity,
        locality_standing=run.locality_standing,
    )
    measurements = coordinate_run.measurements
    target_measurement = _measurement_for_group(ledger, measurements, group)
    varying_roles = tuple(
        finding
        for finding in target_measurement["findings"]
        if finding["subject"]["coordinate_role"] in {1, 3}
    )

    assert {
        (finding["subject"]["coordinate_role"], bytes(finding["subject"]["exact_material"]))
        for finding in varying_roles
    } == {
        (1, b"+"),
        (1, b"-"),
        (1, b"x"),
        (3, b"="),
        (3, b"#"),
        (3, b"?"),
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
        extension_count=0,
    )
    result = ledger.get(run.steps[0].extent_result_occurrences[0].identity)
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
        exact=b"2+2=\n3+3=\n4+4=",
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
        extension_count=2,
    )

    # The recording boundary and its bounded Standing advance each validate
    # the direct result. Sibling Compare/Measurement results reuse those exact
    # validated coordinates instead of reconstructing the source population.
    assert calls == 2


def test_variable_extent_results_and_coordinate_measurements_survive_restart(tmp_path):
    database = tmp_path / "variable-extent.sqlite"
    ledger = SQLiteEventLedger(str(database))
    direct = _direct_result(
        ledger,
        locality="variable-extent-restart",
        exact=b"aba\naca",
    )
    run = record_variable_extent_steps(
        ledger,
        direct_result_event_identity=direct.identity,
        extension_count=1,
    )
    coordinate_run = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=(
            run.steps[-1].recurrence_result_occurrence.identity
        ),
        locality_standing=run.locality_standing,
    )
    measurements = coordinate_run.measurements
    extent_identity = run.steps[-1].extent_result_occurrences[0].identity
    recurrence_identity = run.steps[-1].recurrence_result_occurrence.identity
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
    finally:
        reopened.close()


PYTEST_ADMISSION = (
    test_two_extensions_reuse_prior_compare_work_and_expose_literal_recurrence,
    test_same_internal_surface_does_not_create_varying_literal_recurrence,
    test_changed_extent_coordinate_is_refused,
    test_bounded_variable_extent_recording_reuses_validated_direct_coordinates,
    test_variable_extent_results_and_coordinate_measurements_survive_restart,
)
