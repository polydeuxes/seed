from __future__ import annotations

from copy import deepcopy

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_source import record_witness_material_source
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.operator_locality_continuation import (
    LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
    LOCALITY_CONTINUATION_RECORDED_KIND,
    LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    LocalityContinuationError,
    get_recorded_locality_continuation,
    get_locality_continuation_subject_to_act_binding,
    record_locality_continuation_subject_to_act_binding,
    record_locality_continuation_act_occurrence,
    record_locality_continuation_result,
)
from seed_runtime.yield_relation import read_requirements_of_yield_relation


def _source_boundary(
    ledger: EventLedger, locality_identity: str = "source"
) -> tuple[object, str]:
    source = record_witness_material_source(
        ledger,
        locality_identity=locality_identity,
        exact_bytes=b"\x00\xffprior\n",
        source_boundary="fixture boundary",
    )
    return source, source.identity


def _binding(
    ledger: EventLedger,
    boundary: str,
    *,
    source_locality_identity: str = "source",
):
    return record_locality_continuation_subject_to_act_binding(
        ledger,
        source_locality_identity=source_locality_identity,
        source_through_event_occurrence_identity=boundary,
    )


def _act(
    ledger: EventLedger,
    boundary: str,
    *,
    source_locality_identity: str = "source",
):
    binding = _binding(
        ledger,
        boundary,
        source_locality_identity=source_locality_identity,
    )
    current_coordinates = read_operator_current_coordinates(
        ledger, locality_identity=binding.locality_identity
    )
    return record_locality_continuation_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=current_coordinates,
    )


def test_three_stage_continuation_records_exact_direct_relation_without_copying_source_coordinates():
    ledger = EventLedger()
    source, boundary = _source_boundary(ledger)

    act_occurrence = _act(ledger, boundary)
    destination = act_occurrence.locality_identity
    binding_reference = act_occurrence.material[
        "subject_to_act_binding_reference"
    ]
    binding = get_locality_continuation_subject_to_act_binding(
        ledger, binding_reference["recorded_occurrence_identity"]
    )
    after_act = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )

    assert act_occurrence.kind == LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT
    assert destination != "source"
    assert act_occurrence.exact_material is None
    assert binding.kind == (
        LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert binding.locality_identity == destination
    assert binding.material["book_clause_identity"] == "06.Locality.B"
    assert binding.identity in after_act[
        "subject_to_act_binding_occurrences"
    ]
    assert binding.material["subject_reference"][
        "source_through_event_occurrence_identity"
    ] == boundary
    assert tuple(sorted(binding.material)) == (
        "book_clause_identity",
        "exact_act_identity",
        "result_boundary_identity",
        "subject_reference",
        "unknown",
    )
    assert binding_reference == {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": "06.Locality.B",
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": binding.material["subject_reference"],
        "result_boundary_identity": binding.material[
            "result_boundary_identity"
        ],
    }
    assert len(
        {
            binding.identity,
            binding.material["exact_act_identity"],
            binding.material["result_boundary_identity"],
            act_occurrence.material["continuation_act_identity"],
            act_occurrence.material["act_occurrence_identity"],
            act_occurrence.material["locality_relation_occurrence_identity"],
        }
    ) == 5
    assert after_act["event_count"] == 2
    assert after_act["locality_continuation_relation_occurrences"] == {}
    assert after_act["subject_to_act_binding_occurrences"] == {
        binding.identity: None
    }
    assert after_act["material_result_occurrences"] == []
    assert after_act["measurement_occurrences"] == {}
    assert after_act["exact_result_occurrences"] == {}

    result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    recorded = get_recorded_locality_continuation(
        ledger, result.identity
    )
    source_reference = recorded["source_coordinate_reference"]

    assert result.kind == LOCALITY_CONTINUATION_RECORDED_KIND
    assert result.exact_material is None
    assert source_reference == {
        "source_locality_identity": "source",
        "source_through_event_occurrence_identity": source.identity,
    }
    assert recorded["locality_relation"] == {
        "first_subject": source_reference,
        "second_subject": destination,
        "relation_occurrence_identity": recorded[
            "locality_relation_occurrence_identity"
        ],
    }
    assert recorded["locality_relation_occurrence_identity"] not in {
        recorded["continuation_act_identity"],
        recorded["act_occurrence_identity"],
        recorded["result_identity"],
    }
    assert recorded["result_identity"] == binding.material[
        "result_boundary_identity"
    ]
    assert result.identity not in {
        recorded["result_identity"],
        recorded["continuation_act_identity"],
        recorded["act_occurrence_identity"],
        recorded["locality_relation_occurrence_identity"],
        binding.identity,
        binding.material["exact_act_identity"],
    }
    assert recorded["subject_to_act_binding_reference"] == binding_reference
    assert "applicability" not in recorded
    assert "priority" not in recorded
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        yield_relation_event_identity=result.material["yield_relation_identity"],
        act_occurrence_event_identity=act_occurrence.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }

    carried = advance_operator_current_coordinates(
        ledger,
        (result.material["yield_relation_identity"], result.identity),
        locality_identity=destination,
        prior=after_act,
    )
    replayed = read_operator_current_coordinates(
        ledger, locality_identity=destination
    )
    assert carried == replayed
    assert replayed["locality_continuation_relation_occurrences"] == {result.identity: None}
    assert replayed["subject_to_act_binding_occurrences"] == {
        binding.identity: None
    }
    assert replayed["material_result_occurrences"] == []
    assert replayed["measurement_occurrences"] == {}
    assert replayed["exact_result_occurrences"] == {
        result.identity: binding_reference,
    }


def test_reopened_ledger_does_not_reissue_locality_continuation_identities(tmp_path):
    path = tmp_path / "continuation.sqlite"
    ledger = SQLiteEventLedger(str(path))
    _source, boundary = _source_boundary(ledger)
    first_act = _act(ledger, boundary)
    first_result = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=first_act.identity
    )
    first_binding = get_locality_continuation_subject_to_act_binding(
        ledger,
        first_act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ],
    )
    first_identities = {
        first_act.locality_identity,
        first_binding.material["exact_act_identity"],
        first_binding.material["result_boundary_identity"],
        first_act.material["act_occurrence_identity"],
        first_act.material["locality_relation_occurrence_identity"],
    }
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    second_act = _act(ledger, boundary)
    second_result = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=second_act.identity
    )
    second_binding = get_locality_continuation_subject_to_act_binding(
        ledger,
        second_act.material["subject_to_act_binding_reference"][
            "recorded_occurrence_identity"
        ],
    )
    second_identities = {
        second_act.locality_identity,
        second_binding.material["exact_act_identity"],
        second_binding.material["result_boundary_identity"],
        second_act.material["act_occurrence_identity"],
        second_act.material["locality_relation_occurrence_identity"],
    }

    assert len(first_identities) == len(second_identities) == 5
    assert first_identities.isdisjoint(second_identities)
    assert get_recorded_locality_continuation(
        ledger, first_result.identity
    )["result_identity"] == first_binding.material["result_boundary_identity"]
    assert get_recorded_locality_continuation(
        ledger, second_result.identity
    )["result_identity"] == second_binding.material["result_boundary_identity"]


def test_act_refuses_a_binding_absent_from_current_coordinates():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    binding = _binding(ledger, boundary)
    source_coordinates = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )

    with pytest.raises(
        LocalityContinuationError, match="exact carried binding"
    ):
        record_locality_continuation_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=binding.identity,
            current_coordinates=source_coordinates,
        )


def test_durable_continuation_material_contains_no_operator_shorthand():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list_locality(act_occurrence.locality_identity)
        ]
    ).lower()

    for shorthand in ("memory", "important", "command", "cut"):
        assert shorthand not in durable


def test_later_source_occurrences_do_not_move_the_exact_source_cut():
    ledger = EventLedger()
    source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    later = record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"later",
        source_boundary="fixture boundary",
    )

    result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    reference = get_recorded_locality_continuation(
        ledger, result.identity
    )["source_coordinate_reference"]

    assert reference["source_through_event_occurrence_identity"] == source.identity
    assert reference["source_through_event_occurrence_identity"] != later.identity


def test_source_occurrence_from_another_locality_is_refused():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)

    with pytest.raises(LocalityContinuationError):
        _binding(ledger, boundary, source_locality_identity="other")


def test_missing_source_occurrence_is_refused():
    ledger = EventLedger()

    with pytest.raises(LocalityContinuationError):
        _binding(ledger, "missing")


def test_corrupted_source_occurrence_is_refused(monkeypatch):
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: CORRUPTED if identity == boundary else integrity_of(identity),
    )

    with pytest.raises(LocalityContinuationError):
        _binding(ledger, boundary)


def test_continuation_carries_only_its_direct_source_coordinates():
    ledger = EventLedger()
    _source, first_boundary = _source_boundary(ledger, "a")
    first_act = _act(
        ledger, first_boundary, source_locality_identity="a"
    )
    first_result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=first_act.identity,
    )
    first_destination = first_result.locality_identity
    second_act = _act(
        ledger,
        first_result.identity,
        source_locality_identity=first_destination,
    )
    second_result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=second_act.identity,
    )
    second_recorded = get_recorded_locality_continuation(
        ledger, second_result.identity
    )

    assert second_recorded["source_coordinate_reference"] == {
        "source_locality_identity": first_destination,
        "source_through_event_occurrence_identity": first_result.identity,
    }
    assert read_operator_current_coordinates(
        ledger, locality_identity=second_result.locality_identity
    )["locality_continuation_relation_occurrences"] == {second_result.identity: None}


def test_one_continuation_act_cannot_yield_or_record_twice():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )

    with pytest.raises(
        LocalityContinuationError, match="already carries a Yield"
    ):
        record_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "source_coordinate_reference",
        "destination_locality_identity",
        "locality_relation",
        "act_occurrence_identity",
        "locality_relation_occurrence_identity",
        "subject_to_act_binding_reference",
        "result_identity",
        "yield_relation_identity",
    ),
)
def test_changed_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    result = record_locality_continuation_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
    )
    changed = ledger.get(result.identity)
    changed.material[coordinate] = "different"

    with pytest.raises(LocalityContinuationError):
        get_recorded_locality_continuation(ledger, result.identity)


def test_equal_source_cuts_keep_distinct_occurrences_and_destinations():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    first_act = _act(ledger, boundary)
    second_act = _act(ledger, boundary)
    first = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=first_act.identity
    )
    second = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=second_act.identity
    )

    assert first_act.identity != second_act.identity
    assert first.locality_identity != second.locality_identity
    assert first.material["act_occurrence_identity"] != second.material[
        "act_occurrence_identity"
    ]
    assert first.material["locality_relation_occurrence_identity"] != second.material[
        "locality_relation_occurrence_identity"
    ]
    assert first.material["result_identity"] != second.material["result_identity"]
    assert first.material["yield_relation_identity"] != second.material[
        "yield_relation_identity"
    ]


def test_incomplete_act_occurrence_is_not_carried_as_a_relation():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)

    standing = read_operator_current_coordinates(
        ledger, locality_identity=act_occurrence.locality_identity
    )

    assert standing["locality_continuation_relation_occurrences"] == {}
    binding_identity = act_occurrence.material[
        "subject_to_act_binding_reference"
    ]["recorded_occurrence_identity"]
    assert standing["subject_to_act_binding_occurrences"] == {
        binding_identity: None
    }
    assert standing["through_event_occurrence_identity"] == act_occurrence.identity


def test_prior_relation_carrier_must_remain_one_identity_dictionary():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    act_occurrence = _act(ledger, boundary)
    result = record_locality_continuation_result(
        ledger, act_occurrence_event_identity=act_occurrence.identity
    )
    standing = read_operator_current_coordinates(
        ledger, locality_identity=result.locality_identity
    )
    broken = deepcopy(standing)
    broken["locality_continuation_relation_occurrences"] = [result.identity]

    with pytest.raises(
        ValueError, match="exact Locality continuation relations"
    ):
        advance_operator_current_coordinates(
            ledger,
            (),
            locality_identity=result.locality_identity,
            prior=broken,
        )


def test_act_occurrence_cannot_cite_another_exact_binding():
    ledger = EventLedger()
    _source, boundary = _source_boundary(ledger)
    first = _act(ledger, boundary)
    second = _act(ledger, boundary)
    changed = ledger.get(first.identity)
    changed.material["subject_to_act_binding_reference"] = dict(
        second.material["subject_to_act_binding_reference"]
    )

    with pytest.raises(LocalityContinuationError):
        record_locality_continuation_result(
            ledger,
            act_occurrence_event_identity=first.identity,
        )
