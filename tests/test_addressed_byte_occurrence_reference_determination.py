from copy import deepcopy

import pytest

import seed_runtime.addressed_byte_occurrence_reference_determination as determination_module
import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as direct_position_module
from seed_runtime.addressed_byte_occurrence_reference_determination import (
    APPLICABILITY_BOUNDARY,
    APPLICABILITY_RESULT_KIND,
    APPLICABILITY_YIELD_RESULT_KIND,
    DETERMINATION_BOUNDARY,
    DETERMINATION_RESULT_KIND,
    DETERMINATION_YIELD_RESULT_KIND,
    AddressedByteOccurrenceReferenceDeterminationError,
    get_addressed_byte_occurrence_reference_determination_act_evidence,
    get_addressed_byte_occurrence_reference_determination_applicability_act_evidence,
    get_addressed_byte_occurrence_reference_determination_responsibility_assignment,
    get_recorded_addressed_byte_occurrence_reference_determination,
    get_recorded_addressed_byte_occurrence_reference_determination_applicability,
    record_addressed_byte_occurrence_reference_determination_act_evidence,
    record_addressed_byte_occurrence_reference_determination_applicability_act_evidence,
    record_addressed_byte_occurrence_reference_determination_applicability_result,
    record_addressed_byte_occurrence_reference_determination_responsibility_assignment,
    record_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    _source_position_coordinate_reference,
    record_byte_pair_occurrence_position_measurement_act_evidence,
    record_byte_pair_occurrence_position_measurement_responsibility_assignment,
    record_byte_pair_occurrence_position_measurement_result,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
)
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)


class CallbackEventLedger(EventLedger):
    callback = None

    def iter_locality_kind(self, locality_identity, kind):
        events = super().iter_locality_kind(locality_identity, kind)
        callback = self.callback
        if callback is not None:
            self.callback = None
            callback()
        return events


def _advance(ledger, standing, *events):
    return advance_operator_locality_standing(
        ledger,
        (event.identity for event in events),
        locality_identity=standing["locality_identity"],
        prior=standing,
    )


def _direct(ledger, exact=b"2+2=5\n", locality="addressed-byte"):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact supplied material boundary",
    )
    standing = read_operator_locality_standing(ledger, locality_identity=locality)
    assignment = record_byte_pair_occurrence_position_measurement_responsibility_assignment(
        ledger,
        source_material_acquisition_occurrence_identity=source.identity,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, assignment)
    act = record_byte_pair_occurrence_position_measurement_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(ledger, standing, act)
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    standing = _advance(ledger, standing, result)
    return source, result, standing


def _coordinate(ledger, source, exact, position):
    return _source_position_coordinate_reference(
        source_material_acquisition_occurrence_identity=source.identity,
        source_locality_identity=source.locality_identity,
        completeness_boundary_identity=(
            ledger.append_boundary_through_occurrence(source.identity).identity
        ),
        position=position,
        exact_material=exact[position : position + 1],
    )


def _through_applicability(
    ledger, exact=b"2+2=5\n", position=3, locality="addressed-byte"
):
    source, direct_result, standing = _direct(ledger, exact, locality)
    coordinate = _coordinate(ledger, source, exact, position)
    assignment = record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, assignment)
    applicability_act = record_addressed_byte_occurrence_reference_determination_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(ledger, standing, applicability_act)
    applicability = record_addressed_byte_occurrence_reference_determination_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=applicability_act.identity,
    )
    standing = _advance(ledger, standing, applicability)
    return {
        "source": source,
        "direct_result": direct_result,
        "coordinate": coordinate,
        "assignment": assignment,
        "applicability_act": applicability_act,
        "applicability": applicability,
        "standing": standing,
    }


def _record(ledger, exact=b"2+2=5\n", position=3, locality="addressed-byte"):
    recorded = _through_applicability(ledger, exact, position, locality)
    determination_act = record_addressed_byte_occurrence_reference_determination_act_evidence(
        ledger,
        applicability_result_event_identity=recorded["applicability"].identity,
        applicability_standing=recorded["standing"],
    )
    standing = _advance(ledger, recorded["standing"], determination_act)
    result = record_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_act_evidence_event_identity=determination_act.identity,
    )
    standing = _advance(ledger, standing, result)
    return {
        **recorded,
        "determination_act": determination_act,
        "result": result,
        "standing": standing,
    }


def test_interior_address_carries_every_and_only_ordered_assertion_reference():
    ledger = EventLedger()
    recorded = _record(ledger)
    expected = references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate(
        ledger,
        recorded["direct_result"].identity,
        recorded["coordinate"],
    )
    material = get_recorded_addressed_byte_occurrence_reference_determination(
        ledger, recorded["result"].identity
    )

    assert material["ordered_assertion_references"] == [
        reference.assertion_reference for reference in expected
    ]
    assert [reference.exact_pair for reference in expected] == [b"2=", b"=5"]
    applicability_finding = recorded["applicability"].material[
        "applicability_finding"
    ]
    assert applicability_finding["relation"] == "applicable_to"
    assert set(applicability_finding) == {
        "first_subject",
        "relation",
        "second_subject",
        "source_material_acquisition_occurrence_identity",
        "locality_identity",
        "completeness_boundary_identity",
        "responsibility_assignment_reference",
    }
    assert len(
        {
            recorded["assignment"].material[coordinate]
            for coordinate in determination_module._IDENTITY_COORDINATES
        }
    ) == len(determination_module._IDENTITY_COORDINATES)
    assert material["determination_rule"] == determination_module.DETERMINATION_RULE
    assert material["completeness_boundary"] == {
        "identity": recorded["coordinate"]["completeness_boundary_identity"]
    }
    assert set(material) == {
        "result_identity",
        "exact_act",
        "determination_act_identity",
        "determination_act_occurrence_identity",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "applicability_result_reference",
        "direct_pair_position_result_reference",
        "addressed_source_byte_position_coordinate_reference",
        "determination_rule",
        "completeness_boundary",
        "ordered_assertion_references",
        "limits",
        "unknown",
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    }
    assert not {"exact_pair", "first_position", "second_position"} & set(material)


@pytest.mark.parametrize(
    ("exact", "position", "expected_count"),
    ((b"ab", 0, 1), (b"ab", 1, 1), (b"x", 0, 0)),
)
def test_boundary_and_single_byte_addresses_have_exact_reference_population(
    exact, position, expected_count
):
    ledger = EventLedger()
    recorded = _record(ledger, exact=exact, position=position)
    material = get_recorded_addressed_byte_occurrence_reference_determination(
        ledger, recorded["result"].identity
    )
    assert len(material["ordered_assertion_references"]) == expected_count


def test_repeated_byte_occurrences_remain_distinct_by_position_assertion():
    ledger = EventLedger()
    recorded = _record(ledger, exact=b"aaa", position=1)
    references = recorded["result"].material["ordered_assertion_references"]
    assert len(references) == 2
    assert references[0]["assertion_identity"] != references[1]["assertion_identity"]


def test_assignment_refuses_stale_forged_and_cross_result_coordinates_atomically():
    ledger = EventLedger()
    first_source, first_result, first_standing = _direct(
        ledger, b"ab", "addressed-byte"
    )
    coordinate = _coordinate(ledger, first_source, b"ab", 0)
    stale = deepcopy(first_standing)
    extra = record_witness_material_acquisition(
        ledger,
        locality_identity="addressed-byte",
        exact_bytes=b"later",
        source_boundary="exact supplied material boundary",
    )
    current = read_operator_locality_standing(
        ledger, locality_identity="addressed-byte"
    )
    before = len(ledger.list())
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="current Standing",
    ):
        record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
            ledger,
            direct_result_event_identity=first_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            locality_standing=stale,
        )
    assert len(ledger.list()) == before

    forged = deepcopy(coordinate)
    forged["exact_material"] = [ord("z")]
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
            ledger,
            direct_result_event_identity=first_result.identity,
            addressed_source_byte_position_coordinate_reference=forged,
            locality_standing=current,
        )
    assert len(ledger.list()) == before

    second_source, second_result, second_standing = _direct(
        ledger, b"ab", "another-addressed-byte"
    )
    del second_source
    cross_before = len(ledger.list())
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
            ledger,
            direct_result_event_identity=second_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            locality_standing=second_standing,
        )
    assert len(ledger.list()) == cross_before
    assert extra is not None


def test_each_stage_reader_refuses_corrupted_prior_stage():
    ledger = EventLedger()
    recorded = _record(ledger)

    recorded["assignment"].material["scope"]["locality_identity"] = "changed"
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        get_addressed_byte_occurrence_reference_determination_applicability_act_evidence(
            ledger, recorded["applicability_act"].identity
        )


@pytest.mark.parametrize(
    ("occurrence_coordinate", "reader"),
    (
        (
            "assignment",
            get_addressed_byte_occurrence_reference_determination_responsibility_assignment,
        ),
        (
            "applicability_act",
            get_addressed_byte_occurrence_reference_determination_applicability_act_evidence,
        ),
        (
            "applicability",
            get_recorded_addressed_byte_occurrence_reference_determination_applicability,
        ),
        (
            "determination_act",
            get_addressed_byte_occurrence_reference_determination_act_evidence,
        ),
        (
            "result",
            get_recorded_addressed_byte_occurrence_reference_determination,
        ),
    ),
)
def test_each_recorded_occurrence_refuses_its_corruption(
    occurrence_coordinate, reader
):
    ledger = EventLedger()
    recorded = _record(ledger)
    event = recorded[occurrence_coordinate]
    event.material["responsibility"] = "changed responsibility"
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        reader(ledger, event.identity)


@pytest.mark.parametrize(
    ("boundary", "result_kind"),
    (
        ("changed-boundary", APPLICABILITY_YIELD_RESULT_KIND),
        (APPLICABILITY_BOUNDARY, "changed result kind"),
    ),
)
def test_applicability_refuses_wrong_yield_kind_or_boundary(boundary, result_kind):
    ledger = EventLedger()
    recorded = _record(ledger)
    evidence = ledger.get(
        recorded["applicability"].material["evidence_of_yield_relation_identity"]
    )
    evidence.material["occurrence_boundary"] = boundary
    evidence.material["result_kind"] = result_kind
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError, match="exact Yield"
    ):
        get_recorded_addressed_byte_occurrence_reference_determination_applicability(
            ledger, recorded["applicability"].identity
        )


@pytest.mark.parametrize(
    ("boundary", "result_kind"),
    (
        ("changed-boundary", DETERMINATION_YIELD_RESULT_KIND),
        (DETERMINATION_BOUNDARY, "changed result kind"),
    ),
)
def test_determination_refuses_wrong_yield_kind_or_boundary(boundary, result_kind):
    ledger = EventLedger()
    recorded = _record(ledger)
    evidence = ledger.get(
        recorded["result"].material["evidence_of_yield_relation_identity"]
    )
    evidence.material["occurrence_boundary"] = boundary
    evidence.material["result_kind"] = result_kind
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError, match="exact Yield"
    ):
        get_recorded_addressed_byte_occurrence_reference_determination(
            ledger, recorded["result"].identity
        )


def test_one_act_cannot_append_a_second_yield_or_result():
    ledger = EventLedger()
    recorded = _record(ledger)
    before = len(ledger.list())
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="already carries",
    ):
        record_addressed_byte_occurrence_reference_determination_result(
            ledger,
            determination_act_evidence_event_identity=recorded[
                "determination_act"
            ].identity,
        )
    assert len(ledger.list()) == before


def test_call_local_standing_equals_full_replay():
    ledger = EventLedger()
    recorded = _record(ledger)
    replayed = read_operator_locality_standing(
        ledger, locality_identity=recorded["source"].locality_identity
    )
    assert recorded["standing"] == replayed
    assert recorded["assignment"].identity in replayed[
        "responsibility_assignment_occurrences"
    ]
    assert recorded["applicability"].identity in replayed[
        "applicability_result_occurrences"
    ]
    assert recorded["result"].identity in replayed["measurement_occurrences"]


def test_lifecycle_is_exact_after_sqlite_restart(tmp_path):
    from seed_runtime.identities import _next_values, new_identity

    path = tmp_path / "addressed-byte.sqlite"
    ledger = SQLiteEventLedger(path)
    recorded = _record(ledger)
    result_identity = recorded["result"].identity
    locality = recorded["source"].locality_identity
    expected = deepcopy(recorded["result"].material)
    assignment_material = recorded["assignment"].material
    carried_identities = {
        "addressed_byte_occurrence_reference_assignment": assignment_material[
            "assignment_identity"
        ],
        "addressed_byte_occurrence_reference_assignment_subject": assignment_material[
            "assignment_subject_identity"
        ],
        "addressed_byte_occurrence_reference_applicability_act": assignment_material[
            "applicability_act_identity"
        ],
        "addressed_byte_occurrence_reference_applicability_act_occurrence": assignment_material[
            "applicability_act_occurrence_identity"
        ],
        "addressed_byte_occurrence_reference_applicability_result": assignment_material[
            "applicability_result_identity"
        ],
        "addressed_byte_occurrence_reference_determination_measurement_act": assignment_material[
            "determination_act_identity"
        ],
        "addressed_byte_occurrence_reference_determination_measurement_act_occurrence": assignment_material[
            "determination_act_occurrence_identity"
        ],
        "addressed_byte_occurrence_reference_determination_measurement_result": assignment_material[
            "determination_result_identity"
        ],
    }
    ledger.close()

    _next_values.clear()
    reopened = SQLiteEventLedger(path)
    assert get_recorded_addressed_byte_occurrence_reference_determination(
        reopened, result_identity
    ) == expected
    assert result_identity in read_operator_locality_standing(
        reopened, locality_identity=locality
    )["measurement_occurrences"]
    for prefix, identity in carried_identities.items():
        prior_number = int(identity.rsplit("_", 1)[1])
        assert new_identity(prefix) == f"{prefix}_{prior_number + 1:06d}"
    reopened.close()


def test_carried_lifecycle_is_exact_after_sqlite_restart(tmp_path):
    path = tmp_path / "addressed-byte-carried.sqlite"
    ledger = SQLiteEventLedger(path)
    source, direct_result, standing = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    carried, result = determination_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        locality_standing=standing,
    )
    expected = deepcopy(result.material)
    result_identity = result.identity
    locality_identity = source.locality_identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    assert get_recorded_addressed_byte_occurrence_reference_determination(
        reopened, result_identity
    ) == expected
    assert carried == read_operator_locality_standing(
        reopened, locality_identity=locality_identity
    )
    reopened.close()


def test_determination_uses_addressed_kernel_without_full_reference_scan(monkeypatch):
    ledger = EventLedger()
    source, direct_result, standing = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    calls = []
    original = determination_module.references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate

    def counted(*args, **kwargs):
        calls.append(args[1])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        determination_module,
        "references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate",
        counted,
    )
    assignment = record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        locality_standing=standing,
    )
    assert calls == [direct_result.identity, direct_result.identity]
    assert "ordered_assertion_references" not in assignment.material


def test_carried_lifecycle_reads_its_direct_source_once_and_matches_replay(
    monkeypatch,
):
    ledger = EventLedger()
    source, direct_result, standing = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    supplied_standing = deepcopy(standing)
    source_calls = []
    result_calls = []
    original_source = determination_module._source
    original_result = direct_position_module._read_result

    def counted_source(*args, **kwargs):
        source_calls.append(kwargs["result_event_identity"])
        return original_source(*args, **kwargs)

    def counted_result(*args, **kwargs):
        result_calls.append(args[1])
        return original_result(*args, **kwargs)

    monkeypatch.setattr(determination_module, "_source", counted_source)
    monkeypatch.setattr(direct_position_module, "_read_result", counted_result)

    carried, result = determination_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        locality_standing=standing,
    )

    assert source_calls == [direct_result.identity]
    assert result_calls == [direct_result.identity]
    assert standing == supplied_standing
    assert result.identity in carried["measurement_occurrences"]
    assert carried == read_operator_locality_standing(
        ledger, locality_identity=source.locality_identity
    )


def test_carried_lifecycle_requires_intact_source_material_and_preserves_supplied_standing():
    ledger = CallbackEventLedger()
    source, direct_result, standing = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    supplied_standing = deepcopy(standing)
    source_material = deepcopy(direct_result.material)

    def replace_source_material_after_reading():
        direct_result.material["unknown"] = ["later material after assignment"]

    ledger.callback = replace_source_material_after_reading
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        determination_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
            ledger,
            direct_result_event_identity=direct_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            locality_standing=standing,
        )

    assert standing == supplied_standing
    direct_result.material.clear()
    direct_result.material.update(source_material)


def test_assignment_refuses_unrelated_append_during_source_revalidation(monkeypatch):
    ledger = EventLedger()
    source, direct_result, standing = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    original = determination_module.references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate
    calls = 0

    def append_after_source_validation(*args, **kwargs):
        nonlocal calls
        references = original(*args, **kwargs)
        calls += 1
        if calls == 2:
            ledger.append(
                "test.callback.unrelated",
                {"source": "callback"},
                locality_identity=source.locality_identity,
            )
        return references

    monkeypatch.setattr(
        determination_module,
        "references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate",
        append_after_source_validation,
    )
    prior = deepcopy(standing)
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="append tip",
    ):
        record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
            ledger,
            direct_result_event_identity=direct_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            locality_standing=standing,
        )
    assert not any(
        event.kind == determination_module.RESPONSIBILITY_ASSIGNMENT_KIND
        for event in ledger.list()
    )
    assert standing == prior
    assert read_operator_locality_standing(
        ledger, locality_identity=source.locality_identity
    ) == prior


def test_act_requires_intact_retained_assignment_during_duplicate_iterator():
    ledger = CallbackEventLedger()
    source, direct_result, standing = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    assignment = record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, assignment)
    prior = deepcopy(standing)
    ledger.callback = lambda: assignment.material.__setitem__(
        "responsibility", "changed responsibility"
    )

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_applicability_act_evidence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=standing,
        )
    assert not any(
        event.kind == determination_module.APPLICABILITY_ACT_EVIDENCE_KIND
        for event in ledger.list()
    )
    assert standing == prior


def test_result_refuses_unrelated_append_during_duplicate_iterator_without_yield():
    ledger = CallbackEventLedger()
    source, direct_result, standing = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    assignment = record_addressed_byte_occurrence_reference_determination_responsibility_assignment(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, assignment)
    act = record_addressed_byte_occurrence_reference_determination_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(ledger, standing, act)
    prior = deepcopy(standing)
    before_yields = tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    )
    ledger.callback = lambda: ledger.append(
        "test.callback.unrelated",
        {"source": "callback"},
        locality_identity=source.locality_identity,
    )

    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="append tip",
    ):
        record_addressed_byte_occurrence_reference_determination_applicability_result(
            ledger, applicability_act_evidence_event_identity=act.identity
        )
    assert not any(
        event.kind == determination_module.APPLICABILITY_RESULT_KIND
        for event in ledger.list()
    )
    assert tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ) == before_yields
    assert standing == prior
    assert read_operator_locality_standing(
        ledger, locality_identity=source.locality_identity
    ) == prior


def test_determination_act_requires_intact_applicability_during_iterator():
    ledger = CallbackEventLedger()
    recorded = _through_applicability(ledger, b"abcdef", 3)
    prior = deepcopy(recorded["standing"])
    ledger.callback = lambda: recorded["applicability"].material.__setitem__(
        "responsibility", "changed responsibility"
    )

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_evidence(
            ledger,
            applicability_result_event_identity=recorded[
                "applicability"
            ].identity,
            applicability_standing=recorded["standing"],
        )
    assert not any(
        event.kind == determination_module.DETERMINATION_ACT_EVIDENCE_KIND
        for event in ledger.list()
    )
    assert recorded["standing"] == prior


def test_determination_result_refuses_iterator_append_without_yield():
    ledger = CallbackEventLedger()
    recorded = _through_applicability(ledger, b"abcdef", 3)
    act = record_addressed_byte_occurrence_reference_determination_act_evidence(
        ledger,
        applicability_result_event_identity=recorded["applicability"].identity,
        applicability_standing=recorded["standing"],
    )
    standing = _advance(ledger, recorded["standing"], act)
    prior = deepcopy(standing)
    before_yields = tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    )
    ledger.callback = lambda: ledger.append(
        "test.callback.unrelated",
        {"source": "callback"},
        locality_identity=recorded["source"].locality_identity,
    )

    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="append tip",
    ):
        record_addressed_byte_occurrence_reference_determination_result(
            ledger, determination_act_evidence_event_identity=act.identity
        )
    assert not any(
        event.kind == determination_module.DETERMINATION_RESULT_KIND
        for event in ledger.list()
    )
    assert tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ) == before_yields
    assert standing == prior
    assert read_operator_locality_standing(
        ledger, locality_identity=recorded["source"].locality_identity
    ) == prior
