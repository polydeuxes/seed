from copy import deepcopy

import pytest

import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as direct_position_module
import seed_runtime.operator_locality_standing as standing_module
from seed_runtime.evidence_of_yield_relation import _record_evidence_of_yield_relation
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.material_ingest import ingest_material
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
    RESULT_KIND,
    _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_standing,
    _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_standing,
    get_byte_pair_occurrence_position_measurement_act_evidence,
    get_byte_pair_occurrence_position_measurement_responsibility_assignment,
    get_recorded_byte_pair_occurrence_position_measurement,
    measure_position_coordinates_of_byte_pair_occurrences,
    record_byte_pair_occurrence_position_measurement_act_evidence,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
    record_byte_pair_occurrence_position_measurement_result,
    references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
    references_to_recorded_position_coordinates_of_byte_pair_occurrences,
)
from seed_runtime.operator_locality_standing import (
    _carry_byte_pair_occurrence_position_measurement_result_into_standing,
    read_operator_locality_standing,
)


def _standing(ledger, locality):
    return read_operator_locality_standing(ledger, locality_identity=locality)


def _source(ledger, exact=b"2+2=5\n", locality="position-occurrence-position"):
    return ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=exact,
        source_role="exact supplied material",
        source_boundary="exact supplied material boundary",
    )


def _record(ledger, exact=b"2+2=5\n", locality="position-occurrence-position"):
    source = _source(ledger, exact, locality)
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
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
    return source, assignment, act, result


def test_each_input_pair_has_first_and_second_exact_position_coordinates():
    ledger = EventLedger()
    source = _source(ledger)

    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source.identity,
    )

    assert finding.occurrences == (
        (b"2+", 0, 1),
        (b"+2", 1, 2),
        (b"2=", 2, 3),
        (b"=5", 3, 4),
        (b"5\n", 4, 5),
    )
    assert finding.source_ingest_occurrence_identity == source.identity
    assert finding.completeness_boundary == (
        ledger.append_boundary_through_occurrence(source.identity)
    )


def test_same_pair_material_at_distinct_positions_remains_distinct_occurrences():
    ledger = EventLedger()
    source = _source(ledger, b"aaa")

    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source.identity,
    )

    assert finding.occurrences == ((b"aa", 0, 1), (b"aa", 1, 2))


@pytest.mark.parametrize("exact", (b"", b"x"))
def test_material_without_a_byte_pair_yields_an_exact_empty_result(exact):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, exact)

    finding = get_recorded_byte_pair_occurrence_position_measurement(
        ledger, result.identity
    )

    assert finding.occurrences == ()
    assert result.material["assertions"]["occurrences"] == 0


def test_assignment_act_yield_and_result_enter_current_standing():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    assert assignment.identity in _standing(
        ledger, locality
    )["responsibility_assignment_occurrences"]

    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    standing = _standing(ledger, locality)

    assert get_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger, assignment.identity
    ) == assignment
    assert get_byte_pair_occurrence_position_measurement_act_evidence(
        ledger, act.identity
    ) == act
    assert result.identity in standing["measurement_occurrences"]
    assert result.material["evidence_of_yield_relation_identity"] == (
        standing["measurement_occurrences"][result.identity][
            "evidence_of_yield_relation_identity"
        ]
    )


def test_act_requires_current_standing_that_carries_exact_assignment():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    before_assignment = _standing(ledger, locality)
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=before_assignment,
    )

    with pytest.raises(ValueError, match="current Locality Standing"):
        record_byte_pair_occurrence_position_measurement_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=before_assignment,
        )


def test_one_assignment_records_one_act_and_one_result():
    ledger = EventLedger()
    _source_event, assignment, act, _result = _record(ledger)

    with pytest.raises(ValueError, match="already carries an Act"):
        record_byte_pair_occurrence_position_measurement_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=_standing(
                ledger, assignment.locality_identity
            ),
        )
    with pytest.raises(ValueError, match="already carries a Yield"):
        record_byte_pair_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act.identity,
        )


def test_carried_result_skips_history_scan_only_at_its_exact_act_tip(monkeypatch):
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    finding = measure_position_coordinates_of_byte_pair_occurrences(
        ledger,
        source_ingest_occurrence_identity=source.identity,
    )
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )

    def history_scan_is_not_available(*_args, **_kwargs):
        raise AssertionError(
            "same-call result scanned prior Yield or result occurrences"
        )

    monkeypatch.setattr(ledger, "iter_locality_kind", history_scan_is_not_available)
    result = (
        direct_position_module._record_byte_pair_occurrence_position_measurement_result_from_carried_act_evidence(
            ledger,
            responsible_act_evidence=act,
            responsibility_assignment=assignment,
            finding=finding,
        )
    )
    assert result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND

    with pytest.raises(ValueError, match="intact Act Evidence"):
        (
            direct_position_module._record_byte_pair_occurrence_position_measurement_result_from_carried_act_evidence(
                ledger,
                responsible_act_evidence=act,
                responsibility_assignment=assignment,
                finding=finding,
            )
        )


def test_result_refuses_changed_assertion_coordinates():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger)
    result.material["assertions"]["dimensions"]["content"][
        "second_position"
    ] = "position"

    with pytest.raises(ValueError, match="coordinates are not exact"):
        get_recorded_byte_pair_occurrence_position_measurement(ledger, result.identity)


def test_references_preserve_every_exact_pair_occurrence():
    ledger = EventLedger()
    source, _assignment, _act, result = _record(ledger, b"aaa")

    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )

    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == ((b"aa", 0, 1), (b"aa", 1, 2))
    assert len({reference.assertion_identity for reference in references}) == 2
    assert (
        references[0].second_position_coordinate_reference
        == references[1].first_position_coordinate_reference
    )
    assert (
        references[0].first_position_coordinate_reference["identity"]
        != references[0].second_position_coordinate_reference["identity"]
    )
    assert all(
        reference.source_ingest_occurrence_identity == source.identity
        and reference.recorded_occurrence_identity == result.identity
        for reference in references
    )


def test_addressed_references_stop_after_the_last_requested_assertion(monkeypatch):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"abcdef")
    all_references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )
    calls = []
    original = direct_position_module._assertion_identity

    def counted(*args, **kwargs):
        calls.append(kwargs["first_position"])
        return original(*args, **kwargs)

    monkeypatch.setattr(direct_position_module, "_assertion_identity", counted)
    addressed = (
        references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger,
            result.identity,
            (
                all_references[0].assertion_identity,
                all_references[1].assertion_identity,
            ),
        )
    )

    assert addressed == all_references[:2]
    assert calls == [0, 0, 1, 1]


def test_full_reference_reader_does_not_construct_the_occurrence_population(
    monkeypatch,
):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"abcdef")

    def population_is_not_needed(_finding):
        raise AssertionError("full reference read constructed the occurrence population")

    monkeypatch.setattr(
        direct_position_module.FindingOfPositionCoordinatesOfBytePairOccurrences,
        "occurrences",
        property(population_is_not_needed),
    )

    references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )
    assert tuple(reference.exact_pair for reference in references) == (
        b"ab",
        b"bc",
        b"cd",
        b"de",
        b"ef",
    )


def test_exact_addressed_source_position_reads_only_its_carried_pair_references(
    monkeypatch,
):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger)
    all_references = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, result.identity
        )
    )
    addressed_position = all_references[2].second_position_coordinate_reference
    assert addressed_position == all_references[3].first_position_coordinate_reference
    calls = []
    original = direct_position_module._recorded_position_reference

    def counted(*args, **kwargs):
        calls.append(kwargs["first_position"])
        return original(*args, **kwargs)

    def full_population_is_not_needed(*_args, **_kwargs):
        raise AssertionError("addressed source position scanned the full population")

    monkeypatch.setattr(
        direct_position_module, "_recorded_position_reference", counted
    )
    monkeypatch.setattr(
        direct_position_module,
        "references_to_recorded_position_coordinates_of_byte_pair_occurrences",
        full_population_is_not_needed,
    )
    monkeypatch.setattr(
        direct_position_module,
        "references_to_addressed_recorded_position_coordinates_of_byte_pair_occurrences",
        full_population_is_not_needed,
    )

    references = (
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, addressed_position
        )
    )

    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == ((b"2=", 2, 3), (b"=5", 3, 4))
    assert all(
        addressed_position
        in (
            reference.first_position_coordinate_reference,
            reference.second_position_coordinate_reference,
        )
        for reference in references
    )
    assert calls == [2, 3]


@pytest.mark.parametrize(
    ("exact", "position", "expected"),
    (
        (b"abc", 0, ((b"ab", 0, 1),)),
        (b"abc", 2, ((b"bc", 1, 2),)),
        (b"x", 0, ()),
    ),
)
def test_addressed_source_position_preserves_exact_boundaries(
    exact, position, expected
):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, exact)
    finding = get_recorded_byte_pair_occurrence_position_measurement(
        ledger, result.identity
    )
    coordinate = direct_position_module._source_position_coordinate_reference(
        source_ingest_occurrence_identity=(
            finding.source_ingest_occurrence_identity
        ),
        source_locality_identity=finding.source_locality_identity,
        completeness_boundary_identity=finding.completeness_boundary.identity,
        position=position,
        exact_material=exact[position : position + 1],
    )

    references = (
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, coordinate
        )
    )

    assert tuple(
        (reference.exact_pair, reference.first_position, reference.second_position)
        for reference in references
    ) == expected


@pytest.mark.parametrize(
    "change",
    (
        lambda coordinate: coordinate.update(identity="forged"),
        lambda coordinate: coordinate.update(position=True),
        lambda coordinate: coordinate.update(position=-1),
        lambda coordinate: coordinate.update(exact_material=[0]),
        lambda coordinate: coordinate.update(locality_identity="another-locality"),
        lambda coordinate: coordinate.update(extra="coordinate"),
        lambda coordinate: coordinate.pop("identity"),
    ),
)
def test_addressed_source_position_refuses_a_changed_coordinate(change):
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"aaa")
    reference = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        ledger, result.identity
    )[0]
    coordinate = deepcopy(reference.second_position_coordinate_reference)
    change(coordinate)

    with pytest.raises(ValueError, match="addressed source position"):
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, coordinate
        )


def test_equal_byte_material_at_another_position_does_not_supply_the_address():
    ledger = EventLedger()
    _source_event, _assignment, _act, result = _record(ledger, b"aaa")
    references = references_to_recorded_position_coordinates_of_byte_pair_occurrences(
        ledger, result.identity
    )
    first_a = references[0].first_position_coordinate_reference
    second_a = references[0].second_position_coordinate_reference

    assert first_a["exact_material"] == second_a["exact_material"]
    assert first_a["identity"] != second_a["identity"]
    assert (
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, result.identity, second_a
        )
        == references
    )


def test_addressed_source_position_from_another_exact_result_is_refused():
    ledger = EventLedger()
    _first_source, _first_assignment, _first_act, first_result = _record(
        ledger, b"abc", "first-address-locality"
    )
    _second_source, _second_assignment, _second_act, second_result = _record(
        ledger, b"abc", "second-address-locality"
    )
    other_coordinate = (
        references_to_recorded_position_coordinates_of_byte_pair_occurrences(
            ledger, second_result.identity
        )[0].first_position_coordinate_reference
    )

    with pytest.raises(ValueError, match="exact recorded coordinate"):
        references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
            ledger, first_result.identity, other_coordinate
        )


@pytest.mark.parametrize(
    ("occurrence_boundary", "result_kind"),
    (
        ("byte_measurement", RESULT_KIND),
        ("byte_pair_occurrence_position_measurement", "another result kind"),
    ),
)
def test_result_refuses_an_intact_yield_from_another_exact_family(
    occurrence_boundary,
    result_kind,
):
    ledger = EventLedger()
    source = _source(ledger)
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, source.locality_identity),
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(
            ledger, source.locality_identity
        ),
    )
    act_read, assignment_read, finding = direct_position_module._read_act(
        ledger, act.identity
    )
    result_material = direct_position_module._result_material(
        finding, assignment_read
    )
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=direct_position_module.EXACT_ACT,
        act_occurrence_identity=assignment.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act_read.identity,
        result_kind=result_kind,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        responsibility=direct_position_module.RESPONSIBILITY,
        occurrence_boundary=occurrence_boundary,
        responsible_boundary="this Seed",
    )
    result = ledger.append(
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": act.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=act.locality_identity,
    )

    with pytest.raises(ValueError, match="exact Yield"):
        get_recorded_byte_pair_occurrence_position_measurement(ledger, result.identity)


def test_private_same_call_recorders_require_exact_carried_tip_membership(monkeypatch):
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    carried_source = _standing(ledger, locality)

    def standing_replay_is_not_available(*_args, **_kwargs):
        raise AssertionError("same-call recorder replayed current Standing")

    monkeypatch.setattr(
        standing_module,
        "read_operator_locality_standing",
        standing_replay_is_not_available,
    )
    assignment = (
        _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_standing(
            ledger,
            source_ingest_occurrence_identity=source.identity,
            locality_standing=carried_source,
        )
    )
    carried_assignment = deepcopy(carried_source)
    carried_assignment["responsibility_assignment_occurrences"][
        assignment.identity
    ] = None
    carried_assignment["through_event_occurrence_identity"] = assignment.identity
    carried_assignment["event_count"] += 1

    act = _record_byte_pair_occurrence_position_measurement_act_evidence_from_carried_standing(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=carried_assignment,
    )

    assert get_byte_pair_occurrence_position_measurement_act_evidence(
        ledger, act.identity
    ) == act

    stale_source = deepcopy(carried_source)
    stale_source["ingest_occurrences"] = []
    with pytest.raises(ValueError, match="current Locality Standing"):
        _record_byte_pair_occurrence_position_measurement_responsibility_assignment_from_carried_standing(
            ledger,
            source_ingest_occurrence_identity=source.identity,
            locality_standing=stale_source,
        )


def test_assignment_act_and_result_survive_separate_restarts(tmp_path):
    path = tmp_path / "position-occurrence-position.sqlite"
    ledger = SQLiteEventLedger(path)
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    assignment_identity = assignment.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    assignment = get_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger, assignment_identity
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    act_identity = act.identity
    ledger.close()

    ledger = SQLiteEventLedger(path)
    try:
        result = record_byte_pair_occurrence_position_measurement_result(
            ledger,
            responsible_act_evidence_event_identity=act_identity,
        )
        assert get_recorded_byte_pair_occurrence_position_measurement(
            ledger, result.identity
        ).occurrences[0] == (b"2+", 0, 1)
    finally:
        ledger.close()


def test_reopened_public_result_refuses_a_second_yield(tmp_path):
    path = tmp_path / "position-occurrence-position-duplicate.sqlite"
    ledger = SQLiteEventLedger(path)
    _source_event, _assignment, act, _result = _record(ledger)
    act_identity = act.identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        before = reopened.append_boundary()
        with pytest.raises(ValueError, match="already carries a Yield"):
            record_byte_pair_occurrence_position_measurement_result(
                reopened,
                responsible_act_evidence_event_identity=act_identity,
            )
        assert reopened.append_boundary() == before
    finally:
        reopened.close()


def test_same_call_result_carry_equals_full_standing_replay():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    before_result = _standing(ledger, locality)
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )

    carried = _carry_byte_pair_occurrence_position_measurement_result_into_standing(
        before_result,
        result,
        prior_through_event_occurrence_identity=act.identity,
    )

    assert carried == _standing(ledger, locality)


def test_refused_same_call_result_does_not_change_prior_standing():
    ledger = EventLedger()
    source = _source(ledger)
    locality = source.locality_identity
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_ingest_occurrence_identity=source.identity,
        locality_standing=_standing(ledger, locality),
    )
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality),
    )
    prior = _standing(ledger, locality)
    unchanged = deepcopy(prior)
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
    )
    malformed = deepcopy(result)
    malformed.material["unknown"] = "not one exact list"

    with pytest.raises(ValueError, match="Standing is not exact"):
        _carry_byte_pair_occurrence_position_measurement_result_into_standing(
            prior,
            malformed,
            prior_through_event_occurrence_identity=act.identity,
        )

    assert prior == unchanged


def test_result_carries_only_its_declared_measurement_coordinates():
    ledger = EventLedger()
    _source_event, assignment, _act, result = _record(ledger)

    assert result.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    assert set(result.material) == {
        "result_identity",
        "addressed_act_identity",
        "act_occurrence_identity",
        "exact_act",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "input_relation",
        "measurement_rule",
        "source_localities",
        "source_ingest_occurrence_identity",
        "completeness_boundary",
        "assertions",
        "unknown",
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    }
    assert "standing" not in assignment.material["input_relation"]
    assert "standing" not in result.material["assertions"]["dimensions"]


FIDELITY_SUBJECTS = {
    "act_evidence_responsibility_boundary_occurrence_authority_scope": (
        test_assignment_act_yield_and_result_enter_current_standing,
        test_act_requires_current_standing_that_carries_exact_assignment,
        test_one_assignment_records_one_act_and_one_result,
        test_carried_result_skips_history_scan_only_at_its_exact_act_tip,
        test_assignment_act_and_result_survive_separate_restarts,
        test_reopened_public_result_refuses_a_second_yield,
        test_same_call_result_carry_equals_full_standing_replay,
        test_refused_same_call_result_does_not_change_prior_standing,
        test_private_same_call_recorders_require_exact_carried_tip_membership,
    ),
    "yield_result_occurrence_evidence": (
        test_result_refuses_an_intact_yield_from_another_exact_family,
    ),
    "declared_measurement_result": (
        test_each_input_pair_has_first_and_second_exact_position_coordinates,
        test_same_pair_material_at_distinct_positions_remains_distinct_occurrences,
        test_material_without_a_byte_pair_yields_an_exact_empty_result,
        test_result_refuses_changed_assertion_coordinates,
        test_references_preserve_every_exact_pair_occurrence,
        test_addressed_references_stop_after_the_last_requested_assertion,
        test_full_reference_reader_does_not_construct_the_occurrence_population,
        test_exact_addressed_source_position_reads_only_its_carried_pair_references,
        test_addressed_source_position_preserves_exact_boundaries,
        test_addressed_source_position_refuses_a_changed_coordinate,
        test_equal_byte_material_at_another_position_does_not_supply_the_address,
        test_addressed_source_position_from_another_exact_result_is_refused,
        test_result_carries_only_its_declared_measurement_coordinates,
    ),
}
