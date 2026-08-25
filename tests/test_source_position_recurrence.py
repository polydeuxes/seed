from __future__ import annotations

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
    record_byte_pair_occurrence_position_measurement_result,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.source_position_recurrence import (
    RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND,
    get_recorded_recurrent_result_material_measurement,
    get_recorded_corresponding_coordinate_material_measurement,
    get_recorded_source_position_measurement,
    get_recorded_source_position_recurrence,
    iter_recurrent_coordinate_material_findings,
    record_corresponding_coordinate_material_measurements,
    record_recurrent_result_material_measurements,
    record_source_position_measurements,
)
import seed_runtime.source_position_recurrence as source_position_recurrence
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)


def _direct_result(ledger, *, locality, exact):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact source-position material boundary",
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
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    return record_byte_pair_occurrence_position_measurement_result(
        ledger,
        act_occurrence_event_identity=act.identity,
    )


def _target_surface():
    return ["difference", "same-content", "difference"]


def _target_group(ledger, recurrence_result):
    recurrence = get_recorded_source_position_recurrence(
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


def _step_at(recording, coordinate_count):
    matching = tuple(
        step for step in recording.steps if step.coordinate_count == coordinate_count
    )
    assert len(matching) == 1
    return matching[0]


def _finding_source_positions(finding):
    return tuple(
        carried["source_position_coordinate"]["position"]
        for carried in finding["support"]
    )


def _record_material_measurements(ledger, *, locality, exact):
    direct = _direct_result(ledger, locality=locality, exact=exact)
    source_position_measurements = record_source_position_measurements(
        ledger, direct_result_event_identity=direct.identity
    )
    standing = source_position_measurements.locality_standing
    coordinate_measurements_by_recurrence = []
    material_measurements_by_recurrence = []
    for step in source_position_measurements.steps:
        recurrence_result = step.recurrence_result_occurrence
        coordinate_measurements = (
            record_corresponding_coordinate_material_measurements(
                ledger,
                recurrence_result_event_identity=recurrence_result.identity,
                locality_standing=standing,
            )
        )
        coordinate_measurements_by_recurrence.append(coordinate_measurements)
        material_measurements = record_recurrent_result_material_measurements(
            ledger,
            recurrence_result_event_identity=recurrence_result.identity,
            locality_standing=coordinate_measurements.locality_standing,
        )
        material_measurements_by_recurrence.append(material_measurements)
        standing = material_measurements.locality_standing
    return (
        source_position_measurements,
        tuple(coordinate_measurements_by_recurrence),
        tuple(material_measurements_by_recurrence),
        standing,
    )


def _material_for_group(ledger, material_measurements_by_recurrence, group):
    matching = tuple(
        measurement
        for measurements in material_measurements_by_recurrence
        for measurement in measurements.measurements
        if measurement.recurrence_finding_reference == group["finding_reference"]
    )
    assert len(matching) == 1
    event = matching[0].result_occurrence
    return event, get_recorded_recurrent_result_material_measurement(ledger, event.identity)


def test_recurrence_exhausts_source_and_reuses_prior_compare_work():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="source-position-positive",
        exact=b"a+aa+a",
    )

    recording = record_source_position_measurements(
        ledger,
        direct_result_event_identity=direct.identity,
    )

    assert tuple(step.coordinate_count for step in recording.steps[:2]) == (2, 3)
    assert recording.exhausted is True
    assert all(step.new_event_count > 0 for step in recording.steps)
    assert direct.identity in recording.locality_standing["measurement_occurrences"]
    direct_act = ledger.get(direct.material["act_occurrence_event_identity"])
    assert recording.locality_standing["exact_result_occurrences"][direct.identity] == (
        direct_act.material["responsibility_assignment_reference"]
    )

    final_recurrence = get_recorded_source_position_recurrence(
        ledger, recording.steps[-1].recurrence_result_occurrence.identity
    )
    recurrent_final_groups = tuple(
        finding
        for finding in final_recurrence["findings"]
        if "recurrence" in finding
    )
    assert recurrent_final_groups == ()

    result_kinds = {
        source_position_recurrence.COMPARE_APPLICABILITY_RESULT_KIND,
        source_position_recurrence.COMPARE_RESULT_KIND,
        source_position_recurrence.SOURCE_POSITION_MEASUREMENT_RESULT_KIND,
        source_position_recurrence.RECURRENCE_MEASUREMENT_RESULT_KIND,
    }
    produced_results = tuple(
        event
        for event in ledger.list_locality("source-position-positive")
        if event.kind in result_kinds
    )
    assert produced_results
    for result in produced_results:
        act = ledger.get(result.material["act_occurrence_event_identity"])
        reference = act.material["responsibility_assignment_reference"]
        assignment = ledger.get(reference["recorded_occurrence_identity"])
        assert recording.locality_standing["exact_result_occurrences"][result.identity] == (
            reference
        )
        assert (
            recording.locality_standing["responsibility_assignment_occurrences"].get(
                assignment.identity, object()
            )
            is None
        )
        if result.kind == source_position_recurrence.COMPARE_APPLICABILITY_RESULT_KIND:
            assert (
                recording.locality_standing["applicability_result_occurrences"].get(
                    result.identity, object()
                )
                is None
            )
        elif result.kind == source_position_recurrence.COMPARE_RESULT_KIND:
            assert (
                recording.locality_standing["comparison_result_occurrences"].get(
                    result.identity, object()
                )
                is None
            )
        else:
            assert result.identity in recording.locality_standing[
                "measurement_occurrences"
            ]
        assert assignment.material["subject"] == act.material["coordinates"]["subject"]
        assert assignment.material["rule"] == (
            source_position_recurrence._RESPONSIBILITY_RULES[assignment.kind]
        )
        assert assignment.material["result_boundary_identity"] == result.material[
            "result_identity"
        ]

    by_length_and_start = {}
    for step in recording.steps:
        for event in step.source_position_result_occurrences:
            reading = get_recorded_source_position_measurement(ledger, event.identity)
            start = reading["source_position_coordinates"][0]["position"]
            by_length_and_start[step.coordinate_count, start] = reading

    length_two = by_length_and_start[2, 0]
    length_three = by_length_and_start[3, 0]
    assert length_three["compare_result_references"][:1] == length_two[
        "compare_result_references"
    ]
    assert len(length_three["new_compare_result_references"]) == 2

    target_recurrence = _step_at(recording, 3).recurrence_result_occurrence
    group = _target_group(ledger, target_recurrence)
    assert "recurrence" in group
    assert group["count"] == 2
    assert tuple(
        get_recorded_source_position_measurement(
            ledger, reference["recorded_occurrence_reference"]
        )["source_position_coordinates"][0]["position"]
        for reference in group["support_result_references"]
    ) == (0, 3)

    # This explicit call from one result to the later Measurement is the
    # remaining hand-written continuation. It supplies the complete recurrence
    # result; the later Measurement chooses no finding, source position, or
    # value from it.
    coordinate_measurements = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=target_recurrence.identity,
        locality_standing=recording.locality_standing,
    )
    measurements = coordinate_measurements.measurements
    target_measurement = _measurement_for_group(ledger, measurements, group)
    assert all(
        measurement.result_occurrence.identity
        in coordinate_measurements.locality_standing["measurement_occurrences"]
        for measurement in measurements
    )
    assert all(
        coordinate_measurements.locality_standing["exact_result_occurrences"][
            measurement.result_occurrence.identity
        ]
        == ledger.get(
            measurement.result_occurrence.material[
                "act_occurrence_event_identity"
            ]
        ).material["responsibility_assignment_reference"]
        for measurement in measurements
    )
    assert all(
        ledger.get(
            ledger.get(
                measurement.result_occurrence.material[
                    "act_occurrence_event_identity"
                ]
            ).material["responsibility_assignment_reference"][
                "recorded_occurrence_identity"
            ]
        ).identity
        in coordinate_measurements.locality_standing[
            "responsibility_assignment_occurrences"
        ]
        for measurement in measurements
    )
    recurrent = {
        (
            _finding_source_positions(finding),
            bytes(finding["subject"]["exact_material"]),
        ): finding
        for finding in target_measurement["findings"]
        if "recurrence" in finding
    }

    assert recurrent[(1, 4), b"+"]["count"] == 2
    assert tuple(
        (_finding_source_positions(finding), finding["count"])
        for finding in iter_recurrent_coordinate_material_findings(
            ledger, measurements
        )
        if finding["finding_reference"] in {
            recurrent[(1, 4), b"+"]["finding_reference"],
        }
    ) == (((1, 4), 2),)


def test_same_compare_surface_does_not_create_common_material():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="source-position-control",
        exact=b"a+aa-a",
    )
    recording = record_source_position_measurements(
        ledger,
        direct_result_event_identity=direct.identity,
    )
    target_recurrence = _step_at(recording, 3).recurrence_result_occurrence
    group = _target_group(ledger, target_recurrence)
    assert "recurrence" in group
    assert group["count"] == 2

    coordinate_measurements = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=target_recurrence.identity,
        locality_standing=recording.locality_standing,
    )
    measurements = coordinate_measurements.measurements
    target_measurement = _measurement_for_group(ledger, measurements, group)
    varying_findings = tuple(
        finding
        for finding in target_measurement["findings"]
        if _finding_source_positions(finding) in {(1,), (4,)}
    )

    assert {
        (_finding_source_positions(finding), bytes(finding["subject"]["exact_material"]))
        for finding in varying_findings
    } == {
        ((1,), b"+"),
        ((4,), b"-"),
    }
    assert all(finding["count"] == 1 for finding in varying_findings)
    assert all("recurrence" not in finding for finding in varying_findings)


def test_changed_source_position_coordinate_is_refused():
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="source-position-integrity",
        exact=b"aba",
    )
    recording = record_source_position_measurements(
        ledger,
        direct_result_event_identity=direct.identity,
    )
    result = ledger.get(recording.steps[0].source_position_result_occurrences[0].identity)
    act = ledger.get(result.material["act_occurrence_event_identity"])
    assignment = ledger.get(
        act.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    exact_result_boundary = assignment.material["result_boundary_identity"]
    assignment.material["result_boundary_identity"] = "changed-result-boundary"
    try:
        get_recorded_source_position_measurement(ledger, result.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed Responsibility ownership was accepted")
    assignment.material["result_boundary_identity"] = exact_result_boundary

    yielded = ledger.get(result.material["yield_relation_identity"])
    exact_yield_occurrence = yielded.material["dimensions"][
        "act_occurrence_identity"
    ]
    yielded.material["dimensions"]["act_occurrence_identity"] = "changed-yield"
    try:
        read_operator_locality_standing(
            ledger, locality_identity="source-position-integrity"
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
        get_recorded_source_position_measurement(ledger, result.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed source-position coordinate was accepted")


def test_source_position_recording_reuses_validated_direct_coordinates(
    monkeypatch,
):
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="source-position-bounded-validation",
        exact=b"a+aa+a",
    )
    calls = 0
    exact_reader = (
        source_position_recurrence
        .source_position_coordinate_references_of_recorded_position_measurement
    )

    def counted_reader(ledger, result_event_identity):
        nonlocal calls
        calls += 1
        return exact_reader(ledger, result_event_identity)

    monkeypatch.setattr(
        source_position_recurrence,
        "source_position_coordinate_references_of_recorded_position_measurement",
        counted_reader,
    )

    record_source_position_measurements(
        ledger,
        direct_result_event_identity=direct.identity,
    )

    # The recording boundary and its bounded Standing advance each validate
    # the direct result. Sibling Compare/Measurement results reuse those exact
    # validated coordinates instead of reconstructing all source occurrences.
    assert calls == 2


def test_unrelated_acquired_material_does_not_change_exact_coordinates():
    readings = []
    for locality, exact, start in (
        ("source-position-isolated", b"aba", 0),
        ("source-position-with-unrelated-material", b"xabay", 1),
    ):
        ledger = EventLedger()
        direct = _direct_result(ledger, locality=locality, exact=exact)
        recording = record_source_position_measurements(
            ledger,
            direct_result_event_identity=direct.identity,
        )
        matching = []
        for event in _step_at(recording, 3).source_position_result_occurrences:
            reading = get_recorded_source_position_measurement(ledger, event.identity)
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


def test_sqlite_restart_recovers_source_position_readers(tmp_path):
    database = tmp_path / "source-position.sqlite"
    ledger = EventLedger()
    direct = _direct_result(
        ledger,
        locality="source-position-restart",
        exact=b"aba",
    )
    recording = record_source_position_measurements(
        ledger,
        direct_result_event_identity=direct.identity,
    )
    coordinate_measurements = record_corresponding_coordinate_material_measurements(
        ledger,
        recurrence_result_event_identity=(
            recording.steps[0].recurrence_result_occurrence.identity
        ),
        locality_standing=recording.locality_standing,
    )
    measurements = coordinate_measurements.measurements
    source_position_identity = recording.steps[-1].source_position_result_occurrences[0].identity
    recurrence_identity = recording.steps[0].recurrence_result_occurrence.identity
    measurement_identities = tuple(
        measurement.result_occurrence.identity for measurement in measurements
    )
    validated = {}
    expected_source_positions = get_recorded_source_position_measurement(
        ledger, source_position_identity, _validated=validated
    )
    expected_recurrence = get_recorded_source_position_recurrence(
        ledger, recurrence_identity, _validated=validated
    )
    expected_measurements = tuple(
        get_recorded_corresponding_coordinate_material_measurement(
            ledger, identity, _validated=validated
        )
        for identity in measurement_identities
    )
    durable = SQLiteEventLedger(str(database))
    durable.append_many(ledger.list())
    durable.close()

    sqlite_ledger = SQLiteEventLedger(str(database))
    try:
        validated = {}
        assert get_recorded_source_position_measurement(
            sqlite_ledger, source_position_identity, _validated=validated
        ) == expected_source_positions
        assert (
            get_recorded_source_position_recurrence(
                sqlite_ledger, recurrence_identity, _validated=validated
            )
            == expected_recurrence
        )
        assert tuple(
            get_recorded_corresponding_coordinate_material_measurement(
                sqlite_ledger, identity, _validated=validated
            )
            for identity in measurement_identities
        ) == expected_measurements
    finally:
        sqlite_ledger.close()


def test_recurrent_results_yield_one_exact_reusable_material_without_selection():
    ledger = EventLedger()
    source_position_measurements, _coordinate_measurements, material_measurements, standing = (
        _record_material_measurements(
            ledger,
            locality="recurrent-result-material-positive",
            exact=b"a+aa+a",
        )
    )
    recurrence = _step_at(source_position_measurements, 3).recurrence_result_occurrence
    group = _target_group(ledger, recurrence)

    event, reading = _material_for_group(ledger, material_measurements, group)
    assert event.kind == RECURRENT_RESULT_MATERIAL_MEASUREMENT_RESULT_KIND
    assert event.exact_material == b"a+a"
    assert bytes(reading["exact_material"]) == b"a+a"
    assert tuple(
        bytes(finding["subject"]["exact_material"])
        for finding in reading["coordinate_material_findings"]
    ) == (b"a", b"+", b"a")
    assert all(
        tuple(sorted(finding["subject"]))
        == ("exact_material", "recurrence_finding_reference")
        for finding in reading["coordinate_material_findings"]
    )
    assert reading["support_result_references"] == group[
        "support_result_references"
    ]
    assert all(
        tuple(
            coordinate["position"]
            for coordinate in support["source_position_coordinates"]
        )
        in {(0, 1, 2), (3, 4, 5)}
        for support in reading["support_occurrences"]
    )

    act = ledger.get(event.material["act_occurrence_event_identity"])
    ownership = act.material["responsibility_assignment_reference"]
    assignment = ledger.get(ownership["recorded_occurrence_identity"])
    assert standing["measurement_occurrences"][event.identity][
        "result_identity"
    ] == event.material["result_identity"]
    assert standing["exact_result_occurrences"][event.identity] == (
        ownership
    )
    assert assignment.material["subject"] == reading["subject"]
    assert assignment.material["result_boundary_identity"] == reading[
        "result_identity"
    ]


def test_exact_reusable_material_result_is_not_a_source_assertion():
    ledger = EventLedger()
    measurements, _coordinate_measurements, material_measurements, _standing = (
        _record_material_measurements(
            ledger,
            locality="candidate exact-material refusal",
            exact=b"a+aa+a",
        )
    )
    recurrence = _step_at(measurements, 3).recurrence_result_occurrence
    group = _target_group(ledger, recurrence)
    exact_material_result, _reading = _material_for_group(
        ledger, material_measurements, group
    )

    assert exact_material_result.exact_material == b"a+a"
    assert exact_material_result.material.get("assertions") is None


def test_varying_coordinate_material_yields_no_common_exact_material():
    ledger = EventLedger()
    source_position_measurements, _coordinate_measurements, material_measurements, _standing = (
        _record_material_measurements(
            ledger,
            locality="recurrent-result-material-control",
            exact=b"a+aa-a",
        )
    )
    recurrence = _step_at(source_position_measurements, 3).recurrence_result_occurrence
    group = _target_group(ledger, recurrence)

    assert all(
        measurement.recurrence_finding_reference != group["finding_reference"]
        for measurements in material_measurements
        for measurement in measurements.measurements
    )
    assert all(
        measurement.result_occurrence.exact_material not in {b"a+a", b"a-a"}
        for measurements in material_measurements
        for measurement in measurements.measurements
    )


def test_recurrent_result_material_refuses_changed_support_material_order_owner_and_yield():
    ledger = EventLedger()
    source_position_measurements, _coordinate_measurements, material_measurements, _standing = (
        _record_material_measurements(
            ledger,
            locality="recurrent-result-material-integrity",
            exact=b"a+aa+a",
        )
    )
    recurrence = _step_at(source_position_measurements, 3).recurrence_result_occurrence
    group = _target_group(ledger, recurrence)
    event, _reading = _material_for_group(ledger, material_measurements, group)

    support = event.material["coordinates"]["support_result_references"]
    event.material["coordinates"]["support_result_references"] = list(
        reversed(support)
    )
    try:
        get_recorded_recurrent_result_material_measurement(ledger, event.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed support references were accepted")
    event.material["coordinates"]["support_result_references"] = support

    material = event.material["coordinates"]["coordinate_material_findings"][1][
        "subject"
    ]["exact_material"]
    event.material["coordinates"]["coordinate_material_findings"][1]["subject"][
        "exact_material"
    ] = [ord("-")]
    try:
        get_recorded_recurrent_result_material_measurement(ledger, event.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed coordinate material was accepted")
    event.material["coordinates"]["coordinate_material_findings"][1]["subject"][
        "exact_material"
    ] = material

    findings = event.material["coordinates"]["coordinate_material_findings"]
    event.material["coordinates"]["coordinate_material_findings"] = list(
        reversed(findings)
    )
    try:
        get_recorded_recurrent_result_material_measurement(ledger, event.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed coordinate sequence was accepted")
    event.material["coordinates"]["coordinate_material_findings"] = findings

    act = ledger.get(event.material["act_occurrence_event_identity"])
    assignment = ledger.get(
        act.material["responsibility_assignment_reference"][
            "recorded_occurrence_identity"
        ]
    )
    result_boundary = assignment.material["result_boundary_identity"]
    assignment.material["result_boundary_identity"] = "changed-result-boundary"
    try:
        get_recorded_recurrent_result_material_measurement(ledger, event.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed Responsibility ownership was accepted")
    assignment.material["result_boundary_identity"] = result_boundary

    rule = assignment.material["rule"]
    assignment.material["rule"] = "changed exact rule"
    try:
        get_recorded_recurrent_result_material_measurement(ledger, event.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed Responsibility rule was accepted")
    assignment.material["rule"] = rule

    del assignment.material["rule"]
    try:
        get_recorded_recurrent_result_material_measurement(ledger, event.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("missing Responsibility rule was accepted")
    assignment.material["rule"] = rule

    yielded = ledger.get(event.material["yield_relation_identity"])
    act_occurrence = yielded.material["dimensions"]["act_occurrence_identity"]
    yielded.material["dimensions"]["act_occurrence_identity"] = "changed-yield"
    try:
        get_recorded_recurrent_result_material_measurement(ledger, event.identity)
    except ValueError:
        pass
    else:
        raise AssertionError("changed Yield was accepted")
    yielded.material["dimensions"]["act_occurrence_identity"] = act_occurrence


def test_sqlite_restart_recovers_recurrent_result_material_and_ownership(tmp_path):
    database = tmp_path / "recurrent-result-material.sqlite"
    ledger = EventLedger()
    source_position_measurements, _coordinate_measurements, material_measurements, standing = (
        _record_material_measurements(
            ledger,
            locality="recurrent-result-material-restart",
            exact=b"a+aa+a",
        )
    )
    recurrence = _step_at(source_position_measurements, 3).recurrence_result_occurrence
    group = _target_group(ledger, recurrence)
    event, expected = _material_for_group(ledger, material_measurements, group)
    expected_ownership = standing["exact_result_occurrences"][
        event.identity
    ]
    event_identity = event.identity
    durable = SQLiteEventLedger(str(database))
    durable.append_many(ledger.list())
    durable.close()

    ledger = SQLiteEventLedger(str(database))
    try:
        recorded = get_recorded_recurrent_result_material_measurement(
            ledger, event_identity
        )
        assert recorded == expected
        event = ledger.get(event_identity)
        assert event.exact_material == b"a+a"
        act = ledger.get(event.material["act_occurrence_event_identity"])
        assert act.material["responsibility_assignment_reference"] == (
            expected_ownership
        )
        assignment = ledger.get(
            expected_ownership["recorded_occurrence_identity"]
        )
        assert assignment.material["rule"] == (
            source_position_recurrence.RECURRENT_RESULT_MATERIAL_MEASUREMENT_RULE
        )
        assert assignment.material["subject"] == recorded["subject"]
        assert assignment.material["result_boundary_identity"] == (
            recorded["result_identity"]
        )
    finally:
        ledger.close()


def test_source_coordinate_not_in_support_does_not_choose_material():
    ledger = EventLedger()
    source_position_measurements, _coordinate_measurements, material_measurements, _standing = (
        _record_material_measurements(
            ledger,
            locality="recurrent-result-material-coordinate-not-in-support",
            exact=b"xa+aa+a",
        )
    )
    recurrence = _step_at(source_position_measurements, 3).recurrence_result_occurrence
    group = _target_group(ledger, recurrence)
    event, reading = _material_for_group(
        ledger, material_measurements, group
    )

    assert event.exact_material == b"a+a"
    assert tuple(
        bytes(finding["subject"]["exact_material"])
        for finding in reading["coordinate_material_findings"]
    ) == (b"a", b"+", b"a")
    assert tuple(
        coordinate["position"]
        for support in reading["support_occurrences"]
        for coordinate in support["source_position_coordinates"]
    ) == (1, 2, 3, 4, 5, 6)


PYTEST_ADMISSION = (
    test_recurrence_exhausts_source_and_reuses_prior_compare_work,
    test_same_compare_surface_does_not_create_common_material,
    test_changed_source_position_coordinate_is_refused,
    test_source_position_recording_reuses_validated_direct_coordinates,
    test_unrelated_acquired_material_does_not_change_exact_coordinates,
    test_sqlite_restart_recovers_source_position_readers,
    test_recurrent_results_yield_one_exact_reusable_material_without_selection,
    test_exact_reusable_material_result_is_not_a_source_assertion,
    test_varying_coordinate_material_yields_no_common_exact_material,
    test_recurrent_result_material_refuses_changed_support_material_order_owner_and_yield,
    test_sqlite_restart_recovers_recurrent_result_material_and_ownership,
    test_source_coordinate_not_in_support_does_not_choose_material,
)
