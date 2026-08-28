"""Each addressed byte occurrence requires exact ordered result-position references."""

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
    get_addressed_byte_occurrence_reference_determination_act_occurrence,
    get_addressed_byte_occurrence_reference_determination_applicability_act_occurrence,
    get_addressed_byte_occurrence_reference_determination_subject_to_act_binding,
    get_recorded_addressed_byte_occurrence_reference_determination,
    get_recorded_addressed_byte_occurrence_reference_determination_applicability,
    record_addressed_byte_occurrence_reference_determination_act_occurrence,
    record_addressed_byte_occurrence_reference_determination_applicability_act_occurrence,
    record_addressed_byte_occurrence_reference_determination_applicability_result,
    record_addressed_byte_occurrence_reference_determination_subject_to_act_binding,
    record_addressed_byte_occurrence_reference_determination_result,
)
from seed_runtime.events import EventLedger, SQLiteEventLedger
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    _source_position_coordinate_reference,
    record_byte_pair_occurrence_position_measurement_act_occurrence,
    record_byte_pair_occurrence_position_measurement_subject_to_act_binding,
    record_byte_pair_occurrence_position_measurement_result,
    references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate,
)
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)


class InterveningActEventLedger(EventLedger):
    act_during_kind_read = None

    def iter_locality_kind(self, locality_identity, kind):
        events = super().iter_locality_kind(locality_identity, kind)
        intervening_act = self.act_during_kind_read
        if intervening_act is not None:
            self.act_during_kind_read = None
            intervening_act()
        return events


def _advance(ledger, current_coordinates, *events):
    interval = ledger.locality_occurrence_interval(
        locality_identity=current_coordinates["locality_identity"],
        after_occurrence_identity=current_coordinates[
            "through_event_occurrence_identity"
        ],
        through_occurrence_identity=events[-1].identity,
    )
    return advance_operator_current_coordinates(
        ledger,
        (event.identity for event in interval),
        locality_identity=current_coordinates["locality_identity"],
        prior=current_coordinates,
    )


def _direct(ledger, exact=b"2+2=5\n", locality="addressed-byte"):
    source = record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
        source_boundary="exact supplied material boundary",
    )
    current_coordinates = read_operator_current_coordinates(ledger, locality_identity=locality)
    determination_binding = record_byte_pair_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        source_material_result_occurrence_identity=source.identity,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(ledger, current_coordinates, determination_binding)
    act = record_byte_pair_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=determination_binding.identity,
        binding_current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(ledger, current_coordinates, act)
    result = record_byte_pair_occurrence_position_measurement_result(
        ledger, act_occurrence_event_identity=act.identity
    )
    current_coordinates = _advance(ledger, current_coordinates, result)
    return source, result, current_coordinates


def _coordinate(ledger, source, exact, position):
    return _source_position_coordinate_reference(
        source_material_result_occurrence_identity=source.identity,
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
    source, direct_result, current_coordinates = _direct(ledger, exact, locality)
    coordinate = _coordinate(ledger, source, exact, position)
    determination_binding = record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(ledger, current_coordinates, determination_binding)
    applicability_act = record_addressed_byte_occurrence_reference_determination_applicability_act_occurrence(
        ledger,
        binding_event_identity=determination_binding.identity,
        binding_current_coordinates=current_coordinates,
    )
    applicability_binding = ledger.get(
        applicability_act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )
    current_coordinates = _advance(
        ledger, current_coordinates, applicability_binding, applicability_act
    )
    applicability = record_addressed_byte_occurrence_reference_determination_applicability_result(
        ledger,
        applicability_act_occurrence_event_identity=applicability_act.identity,
    )
    current_coordinates = _advance(ledger, current_coordinates, applicability)
    return {
        "source": source,
        "direct_result": direct_result,
        "coordinate": coordinate,
        "determination_binding": determination_binding,
        "applicability_binding": applicability_binding,
        "applicability_act": applicability_act,
        "applicability": applicability,
        "current_coordinates": current_coordinates,
    }


def _record(ledger, exact=b"2+2=5\n", position=3, locality="addressed-byte"):
    recorded = _through_applicability(ledger, exact, position, locality)
    determination_act = record_addressed_byte_occurrence_reference_determination_act_occurrence(
        ledger,
        applicability_result_event_identity=recorded["applicability"].identity,
        current_coordinates=recorded["current_coordinates"],
    )
    current_coordinates = _advance(ledger, recorded["current_coordinates"], determination_act)
    result = record_addressed_byte_occurrence_reference_determination_result(
        ledger,
        determination_act_occurrence_event_identity=determination_act.identity,
    )
    current_coordinates = _advance(ledger, current_coordinates, result)
    return {
        **recorded,
        "determination_act": determination_act,
        "result": result,
        "current_coordinates": current_coordinates,
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
        "source_material_result_occurrence_identity",
        "locality_identity",
        "completeness_boundary_identity",
        "subject_to_act_binding_reference",
    }
    assert len(
        {
            binding.material[coordinate]
            for binding, coordinates in (
                (
                    recorded["determination_binding"],
                    determination_module._DETERMINATION_IDENTITY_COORDINATES,
                ),
                (
                    recorded["applicability_binding"],
                    determination_module._APPLICABILITY_IDENTITY_COORDINATES,
                ),
            )
            for coordinate in coordinates
        }
    ) == 6
    assert material["completeness_boundary"] == {
        "identity": recorded["coordinate"]["completeness_boundary_identity"]
    }
    assert set(material) == {
        "result_identity",
        "exact_act",
        "determination_act_identity",
        "determination_act_occurrence_identity",
        "subject_to_act_binding_reference",
        "applicability_result_reference",
        "direct_pair_position_result_reference",
        "addressed_source_byte_position_coordinate_reference",
        "completeness_boundary",
        "ordered_assertion_references",
        "act_occurrence_event_identity",
        "yield_relation_identity",
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
    assert tuple(reference["assertion_position"] for reference in references) == (0, 1)


def test_binding_refuses_stale_changed_and_other_result_coordinates_atomically():
    ledger = EventLedger()
    first_source, first_result, first_coordinates = _direct(
        ledger, b"ab", "addressed-byte"
    )
    coordinate = _coordinate(ledger, first_source, b"ab", 0)
    stale = deepcopy(first_coordinates)
    extra = record_witness_material_source(
        ledger,
        locality_identity="addressed-byte",
        exact_bytes=b"later",
        source_boundary="exact supplied material boundary",
    )
    current = read_operator_current_coordinates(
        ledger, locality_identity="addressed-byte"
    )
    before = len(ledger.list())
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="current coordinates",
    ):
        record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
            ledger,
            direct_result_event_identity=first_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            current_coordinates=stale,
        )
    assert len(ledger.list()) == before

    changed = deepcopy(coordinate)
    changed["exact_material"] = [ord("z")]
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
            ledger,
            direct_result_event_identity=first_result.identity,
            addressed_source_byte_position_coordinate_reference=changed,
            current_coordinates=current,
        )
    assert len(ledger.list()) == before

    second_source, second_result, second_coordinates = _direct(
        ledger, b"ab", "another-addressed-byte"
    )
    del second_source
    cross_before = len(ledger.list())
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
            ledger,
            direct_result_event_identity=second_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            current_coordinates=second_coordinates,
        )
    assert len(ledger.list()) == cross_before
    assert extra is not None


def test_each_stage_reader_refuses_corrupted_prior_stage():
    ledger = EventLedger()
    recorded = _record(ledger)

    recorded["determination_binding"].material[
        "through_event_occurrence_identity"
    ] = "changed"
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        get_addressed_byte_occurrence_reference_determination_applicability_act_occurrence(
            ledger, recorded["applicability_act"].identity
        )


@pytest.mark.parametrize(
    ("occurrence_coordinate", "reader"),
    (
        (
            "determination_binding",
            get_addressed_byte_occurrence_reference_determination_subject_to_act_binding,
        ),
        (
            "applicability_act",
            get_addressed_byte_occurrence_reference_determination_applicability_act_occurrence,
        ),
        (
            "applicability",
            get_recorded_addressed_byte_occurrence_reference_determination_applicability,
        ),
        (
            "determination_act",
            get_addressed_byte_occurrence_reference_determination_act_occurrence,
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
    event.material["result_boundary_identity"] = "changed coordinate"
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
    yield_relation = ledger.get(
        recorded["applicability"].material["yield_relation_identity"]
    )
    yield_relation.material["occurrence_boundary"] = boundary
    yield_relation.material["result_kind"] = result_kind
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
    yield_relation = ledger.get(
        recorded["result"].material["yield_relation_identity"]
    )
    yield_relation.material["occurrence_boundary"] = boundary
    yield_relation.material["result_kind"] = result_kind
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
            determination_act_occurrence_event_identity=recorded[
                "determination_act"
            ].identity,
        )
    assert len(ledger.list()) == before


def test_call_local_coordinates_equals_full_replay():
    ledger = EventLedger()
    recorded = _record(ledger)
    replayed = read_operator_current_coordinates(
        ledger, locality_identity=recorded["source"].locality_identity
    )
    assert recorded["current_coordinates"] == replayed
    assert recorded["determination_binding"].identity in replayed[
        "subject_to_act_binding_occurrences"
    ]
    assert recorded["applicability"].identity in replayed[
        "applicability_result_occurrences"
    ]
    assert recorded["result"].identity in replayed["measurement_occurrences"]


def test_lifecycle_is_exact_after_sqlite_restart(tmp_path):
    path = tmp_path / "addressed-byte.sqlite"
    ledger = SQLiteEventLedger(path)
    recorded = _record(ledger)
    result_identity = recorded["result"].identity
    locality = recorded["source"].locality_identity
    expected = deepcopy(recorded["result"].material)
    determination_binding_material = recorded["determination_binding"].material
    applicability_binding_material = recorded["applicability_binding"].material
    carried_identities = {
        "addressed_byte_occurrence_reference_applicability_act": applicability_binding_material[
            "applicability_act_identity"
        ],
        "addressed_byte_occurrence_reference_applicability_act_occurrence": applicability_binding_material[
            "applicability_act_occurrence_identity"
        ],
        "addressed_byte_occurrence_reference_applicability_result": applicability_binding_material[
            "applicability_result_identity"
        ],
        "addressed_byte_occurrence_reference_determination_measurement_act": determination_binding_material[
            "determination_act_identity"
        ],
        "addressed_byte_occurrence_reference_determination_measurement_act_occurrence": determination_binding_material[
            "determination_act_occurrence_identity"
        ],
        "addressed_byte_occurrence_reference_determination_measurement_result": determination_binding_material[
            "determination_result_identity"
        ],
    }
    ledger.close()

    reopened = SQLiteEventLedger(path)
    assert get_recorded_addressed_byte_occurrence_reference_determination(
        reopened, result_identity
    ) == expected
    assert result_identity in read_operator_current_coordinates(
        reopened, locality_identity=locality
    )["measurement_occurrences"]
    for prefix, identity in carried_identities.items():
        prior_number = int(identity.rsplit("_", 1)[1])
        assert reopened.mint_identity(prefix) == f"{prefix}_{prior_number + 1:06d}"
    reopened.close()


def test_carried_lifecycle_is_exact_after_sqlite_restart(tmp_path):
    path = tmp_path / "addressed-byte-carried.sqlite"
    ledger = SQLiteEventLedger(path)
    source, direct_result, current_coordinates = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    carried, result = determination_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        current_coordinates=current_coordinates,
    )
    expected = deepcopy(result.material)
    result_identity = result.identity
    locality_identity = source.locality_identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    assert get_recorded_addressed_byte_occurrence_reference_determination(
        reopened, result_identity
    ) == expected
    assert carried == read_operator_current_coordinates(
        reopened, locality_identity=locality_identity
    )
    reopened.close()


def test_determination_uses_addressed_kernel_without_full_reference_scan(monkeypatch):
    ledger = EventLedger()
    source, direct_result, current_coordinates = _direct(ledger, b"abcdef")
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
    determination_binding = record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        current_coordinates=current_coordinates,
    )
    assert calls == [direct_result.identity, direct_result.identity]
    assert "ordered_assertion_references" not in determination_binding.material


def test_carried_lifecycle_reads_its_direct_source_once_and_matches_replay(
    monkeypatch,
):
    ledger = EventLedger()
    source, direct_result, current_coordinates = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    supplied_coordinates = deepcopy(current_coordinates)
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

    carried, result = determination_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        current_coordinates=current_coordinates,
    )

    assert source_calls == [direct_result.identity]
    assert result_calls == [direct_result.identity]
    assert current_coordinates == supplied_coordinates
    assert result.identity in carried["measurement_occurrences"]
    assert carried == read_operator_current_coordinates(
        ledger, locality_identity=source.locality_identity
    )


def test_carried_lifecycle_requires_intact_source_material_and_preserves_supplied_coordinates():
    ledger = InterveningActEventLedger()
    source, direct_result, current_coordinates = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    supplied_coordinates = deepcopy(current_coordinates)
    source_material = deepcopy(direct_result.material)

    def replace_source_material_after_reading():
        direct_result.material["result_identity"] = (
            "later material after determination binding"
        )

    ledger.act_during_kind_read = replace_source_material_after_reading
    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        determination_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_current_coordinates(
            ledger,
            direct_result_event_identity=direct_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            current_coordinates=current_coordinates,
        )

    assert current_coordinates == supplied_coordinates
    direct_result.material.clear()
    direct_result.material.update(source_material)


def test_binding_refuses_unrelated_append_during_source_revalidation(monkeypatch):
    ledger = EventLedger()
    source, direct_result, current_coordinates = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    original = determination_module.references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate
    calls = 0

    def append_after_source_validation(*args, **kwargs):
        nonlocal calls
        references = original(*args, **kwargs)
        calls += 1
        if calls == 2:
            ledger.append(
                "test.intervening.unrelated",
                {"source": "intervening Act"},
                locality_identity=source.locality_identity,
            )
        return references

    monkeypatch.setattr(
        determination_module,
        "references_to_recorded_byte_pair_occurrences_carrying_addressed_source_position_coordinate",
        append_after_source_validation,
    )
    prior = deepcopy(current_coordinates)
    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="current append boundary",
    ):
        record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
            ledger,
            direct_result_event_identity=direct_result.identity,
            addressed_source_byte_position_coordinate_reference=coordinate,
            current_coordinates=current_coordinates,
        )
    assert not any(
        event.kind
        == determination_module.DETERMINATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        for event in ledger.list()
    )
    assert current_coordinates == prior
    assert read_operator_current_coordinates(
        ledger, locality_identity=source.locality_identity
    ) == prior


def test_act_requires_intact_retained_binding_during_duplicate_iterator():
    ledger = InterveningActEventLedger()
    source, direct_result, current_coordinates = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    determination_binding = record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(ledger, current_coordinates, determination_binding)
    prior = deepcopy(current_coordinates)
    ledger.act_during_kind_read = lambda: determination_binding.material.__setitem__(
        "result_boundary_identity", "changed coordinate"
    )

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_applicability_act_occurrence(
            ledger,
            binding_event_identity=determination_binding.identity,
            binding_current_coordinates=current_coordinates,
        )
    assert not any(
        event.kind == determination_module.APPLICABILITY_ACT_OCCURRENCE_EVENT
        for event in ledger.list()
    )
    assert current_coordinates == prior


def test_result_refuses_unrelated_append_during_duplicate_iterator_without_yield():
    ledger = InterveningActEventLedger()
    source, direct_result, current_coordinates = _direct(ledger, b"abcdef")
    coordinate = _coordinate(ledger, source, b"abcdef", 3)
    determination_binding = record_addressed_byte_occurrence_reference_determination_subject_to_act_binding(
        ledger,
        direct_result_event_identity=direct_result.identity,
        addressed_source_byte_position_coordinate_reference=coordinate,
        current_coordinates=current_coordinates,
    )
    current_coordinates = _advance(ledger, current_coordinates, determination_binding)
    act = record_addressed_byte_occurrence_reference_determination_applicability_act_occurrence(
        ledger,
        binding_event_identity=determination_binding.identity,
        binding_current_coordinates=current_coordinates,
    )
    applicability_binding = ledger.get(
        act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ]
    )
    current_coordinates = _advance(ledger, current_coordinates, applicability_binding, act)
    prior = deepcopy(current_coordinates)
    before_yields = tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_YIELD_RELATION_EVENT
    )
    ledger.act_during_kind_read = lambda: ledger.append(
        "test.intervening.unrelated",
        {"source": "intervening Act"},
        locality_identity=source.locality_identity,
    )

    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="current append boundary",
    ):
        record_addressed_byte_occurrence_reference_determination_applicability_result(
            ledger, applicability_act_occurrence_event_identity=act.identity
        )
    assert not any(
        event.kind == determination_module.APPLICABILITY_RESULT_KIND
        for event in ledger.list()
    )
    assert tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_YIELD_RELATION_EVENT
    ) == before_yields
    assert current_coordinates == prior
    assert read_operator_current_coordinates(
        ledger, locality_identity=source.locality_identity
    ) == prior


def test_determination_act_requires_intact_applicability_during_iterator():
    ledger = InterveningActEventLedger()
    recorded = _through_applicability(ledger, b"abcdef", 3)
    prior = deepcopy(recorded["current_coordinates"])
    ledger.act_during_kind_read = lambda: recorded["applicability"].material.__setitem__(
        "result_identity", "changed coordinate"
    )

    with pytest.raises(AddressedByteOccurrenceReferenceDeterminationError):
        record_addressed_byte_occurrence_reference_determination_act_occurrence(
            ledger,
            applicability_result_event_identity=recorded[
                "applicability"
            ].identity,
            current_coordinates=recorded["current_coordinates"],
        )
    assert not any(
        event.kind == determination_module.DETERMINATION_ACT_OCCURRENCE_EVENT
        for event in ledger.list()
    )
    assert recorded["current_coordinates"] == prior


def test_determination_result_refuses_iterator_append_without_yield():
    ledger = InterveningActEventLedger()
    recorded = _through_applicability(ledger, b"abcdef", 3)
    act = record_addressed_byte_occurrence_reference_determination_act_occurrence(
        ledger,
        applicability_result_event_identity=recorded["applicability"].identity,
        current_coordinates=recorded["current_coordinates"],
    )
    current_coordinates = _advance(ledger, recorded["current_coordinates"], act)
    prior = deepcopy(current_coordinates)
    before_yields = tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_YIELD_RELATION_EVENT
    )
    ledger.act_during_kind_read = lambda: ledger.append(
        "test.intervening.unrelated",
        {"source": "intervening Act"},
        locality_identity=recorded["source"].locality_identity,
    )

    with pytest.raises(
        AddressedByteOccurrenceReferenceDeterminationError,
        match="current append boundary",
    ):
        record_addressed_byte_occurrence_reference_determination_result(
            ledger, determination_act_occurrence_event_identity=act.identity
        )
    assert not any(
        event.kind == determination_module.DETERMINATION_RESULT_KIND
        for event in ledger.list()
    )
    assert tuple(
        event.identity
        for event in ledger.list()
        if event.kind == determination_module.RECORDED_YIELD_RELATION_EVENT
    ) == before_yields
    assert current_coordinates == prior
    assert read_operator_current_coordinates(
        ledger, locality_identity=recorded["source"].locality_identity
    ) == prior
