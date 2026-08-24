from __future__ import annotations

from copy import deepcopy
from io import BytesIO

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.byte_measurement import BYTE_MEASUREMENT_RECORDED_KIND
from seed_runtime.material_acquisition import (
    MaterialAcquisitionError,
    iter_exact_material_acquisition_results,
    read_exact_material_acquisition_result,
)
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND, record_witness_material_acquisition
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_material_acquisition import (
    OPERATOR_MATERIAL_ACQUIRE_ACT_OCCURRENCE_EVENT,
    OPERATOR_MATERIAL_ACQUIRE_LOCALITY_RELATION_OCCURRENCE_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OperatorMaterialAcquireError,
    get_operator_material_acquire_responsibility_assignment,
    get_recorded_operator_material_acquire,
    read_operator_material_acquire_locality_relation_requirements,
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_act_occurrence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.yield_relation import read_requirements_of_yield_relation


def _context(ledger, locality_identity="source"):
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    return standing, standing["through_event_occurrence_identity"]


def _assignment(ledger, standing, standing_boundary, locality_identity="source"):
    assert standing_boundary == standing["through_event_occurrence_identity"]
    return record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )


def _act(ledger, assignment):
    standing = read_operator_locality_standing(
        ledger, locality_identity=assignment.locality_identity
    )
    return record_operator_material_acquire_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )


def _boundary(exact=b"\x00\xffraw\n"):
    return OperatorBoundaryMaterial(
        exact_bytes=exact,
        eof=exact == b"",
        material_boundary="fixture exact byte boundary",
        known_loss=("material before this fixture boundary is not available",),
    )


def test_one_read_records_distinct_assignment_act_yield_and_exact_raw_result():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    assignment = _assignment(ledger, standing, standing_boundary)
    after_assignment = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    act_occurrence = record_operator_material_acquire_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=after_assignment,
    )
    before_result = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    result = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
        boundary_material=_boundary(),
    )
    recorded = get_recorded_operator_material_acquire(ledger, result.identity)

    assert assignment.kind == (
        OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    )
    assert act_occurrence.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_OCCURRENCE_EVENT
    assert result.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    assert assignment.exact_material is act_occurrence.exact_material is None
    assert result.exact_material == b"\x00\xffraw\n"
    assert assignment.material["book_clause_identity"] == "01.Source.G"
    assert "locality_relation" not in assignment.material
    assert assignment.material["unknown"] == [
        "what exact material the operator boundary supplies: Unknown"
    ]
    assert assignment.identity in after_assignment[
        "responsibility_assignment_occurrences"
    ]
    assert recorded["result_identity"] == assignment.material[
        "result_boundary_identity"
    ]
    assert recorded["source_standing_reference"] == {
        "locality_identity": "source",
        "standing_boundary_event_identity": standing_boundary,
    }
    assert recorded["scope"] == assignment.material["scope"]
    assert OPERATOR_MATERIAL_ACQUIRE_LOCALITY_RELATION_OCCURRENCE_KIND == (
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    )
    assert recorded["locality_relation"] == {
        "first_subject": {
            "recorded_occurrence_identity": result.identity,
            "coordinate": "exact_material",
        },
        "relation": "locality",
        "second_subject": "this Seed",
        "relation_occurrence_identity": result.identity,
    }
    assert recorded["locality_relation_occurrence_identity"] == result.identity
    assert recorded["result_identity"] != result.identity
    assert read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": True,
    }
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
    assert len(
        {
            assignment.identity,
            assignment.material["assignment_identity"],
            assignment.material["assignment_subject_identity"],
            assignment.material["scope"]["scope_identity"],
            assignment.material["acquire_act_identity"],
            assignment.material["act_occurrence_identity"],
            assignment.material["result_boundary_identity"],
            act_occurrence.identity,
            result.identity,
            result.material["yield_relation_identity"],
        }
    ) == 10

    carried = advance_operator_locality_standing(
        ledger,
        (result.material["yield_relation_identity"], result.identity),
        locality_identity="source",
        prior=before_result,
    )
    replayed = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    assert carried == replayed
    assert replayed["responsibility_assignment_occurrences"][assignment.identity] is None
    assert replayed["operator_material_acquire_act_occurrences"] == {
        act_occurrence.identity: None
    }
    assert replayed["exact_result_occurrences"][result.identity] == (
        act_occurrence.material["responsibility_assignment_reference"]
    )
    assert replayed["material_locality_relation_occurrences"] == {
        result.identity: {
            "locality_relation": deepcopy(recorded["locality_relation"]),
        }
    }


def test_empty_boundary_leaves_assignment_and_act_without_result_or_yield():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    assignment = _assignment(ledger, standing, standing_boundary)
    act_occurrence = _act(ledger, assignment)
    before = tuple(ledger.list())

    with pytest.raises(
        OperatorMaterialAcquireError, match="establishes no acquire result"
    ):
        record_operator_material_acquire_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
            boundary_material=_boundary(b""),
        )

    assert tuple(ledger.list()) == before
    assert not [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    ]


def test_console_empty_input_records_one_unfinished_boundary_occurrence():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(),
    )

    assert len(
        [
            event
            for event in ledger.list()
            if event.kind
            == OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        ]
    ) == 1
    assert len(
        [
            event
            for event in ledger.list()
            if event.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_OCCURRENCE_EVENT
        ]
    ) == 1
    assert not [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    ]


def test_console_records_one_fresh_occurrence_per_read_including_final_empty_read():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"first\nsecond\n"),
    )
    assignments = [
        event
        for event in ledger.list()
        if event.kind
        == OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    ]
    acts = [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_OCCURRENCE_EVENT
    ]
    results = [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    ]

    assert len(assignments) == len(acts) == 3
    assert len(results) == 2
    assert [result.exact_material for result in results] == [b"first\n", b"second\n"]
    assert len(
        {
            assignment.material["act_occurrence_identity"]
            for assignment in assignments
        }
    ) == 3
    assert not [
        result
        for result in results
        if result.material["act_occurrence_identity"] == acts[-1].identity
    ]


def test_ordinary_operator_material_is_the_exact_acquisition_measurement_source():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"Hello\n"),
    )
    acquired = [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    ]
    assert len(acquired) == 1
    standing = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    assert standing["material_locality_relation_occurrences"] == {
        acquired[0].identity: {
            "locality_relation": deepcopy(
                acquired[0].material["locality_relation"]
            ),
        }
    }
    acquisition_results = [
        event
        for event in ledger.list()
        if event.kind == WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
    ]
    assert acquisition_results == []
    assert read_exact_material_acquisition_result(ledger, acquired[0].identity) == acquired[0]
    assert acquired[0].exact_material == b"Hello\n"
    assert acquired[0].material["provenance_occurrence_references"] == []
    position_results = [
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
    ]
    byte_results = [
        event
        for event in ledger.list()
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    ]
    assert len(position_results) == len(byte_results) == 1
    assert position_results[0].material["source_material_acquisition_occurrence_identity"] == (
        acquired[0].identity
    )
    assert byte_results[0].material["assertions"][0]["dimensions"]["content"][
        "source_material"
    ] == [{"material_acquisition_occurrence_identity": acquired[0].identity}]


def test_operator_result_kind_without_source_g_physiology_is_not_acquisition():
    ledger = EventLedger()
    claimed = ledger.append(
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
        {
            "source_role": "this operator",
            "unknown": ["represented_relation", "source_relation"],
        },
        exact_material=b"claimed O1",
        locality_identity="source",
    )

    with pytest.raises(MaterialAcquisitionError, match="intact physiology"):
        read_exact_material_acquisition_result(ledger, claimed.identity)


def test_exact_acquisition_families_merge_only_their_append_order():
    ledger = EventLedger()
    first = record_witness_material_acquisition(
        ledger,
        locality_identity="source",
        exact_bytes=b"first supplied material",
        source_boundary="first boundary",
    )
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"operator material\n"),
    )
    operator = next(
        event
        for event in ledger.list_locality("source")
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    )
    last = record_witness_material_acquisition(
        ledger,
        locality_identity="source",
        exact_bytes=b"last supplied material",
        source_boundary="last boundary",
    )

    assert [
        event.identity
        for event in iter_exact_material_acquisition_results(ledger, "source")
    ] == [first.identity, operator.identity, last.identity]


def test_equal_raw_results_keep_distinct_occurrences_and_scopes():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    results = []
    assignments = []
    acts = []
    for _ in range(2):
        assignment = _assignment(ledger, standing, standing_boundary)
        act = _act(ledger, assignment)
        result = record_operator_material_acquire_result(
            ledger,
            act_occurrence_event_identity=act.identity,
            boundary_material=_boundary(b"same\x00\xff"),
        )
        assignments.append(assignment)
        acts.append(act)
        results.append(result)
        standing = read_operator_locality_standing(
            ledger, locality_identity="source"
        )

    assert results[0].exact_material == results[1].exact_material
    assert results[0].identity != results[1].identity
    assert results[0].material["locality_relation"]["first_subject"] != results[
        1
    ].material["locality_relation"]["first_subject"]
    assert results[0].material["locality_relation"][
        "relation_occurrence_identity"
    ] != results[1].material["locality_relation"]["relation_occurrence_identity"]
    assert results[0].material["result_identity"] != results[1].material[
        "result_identity"
    ]
    assert acts[0].material["act_occurrence_identity"] != acts[1].material[
        "act_occurrence_identity"
    ]
    assert assignments[0].material["scope"]["scope_identity"] != assignments[
        1
    ].material["scope"]["scope_identity"]


def test_one_acquire_act_cannot_yield_twice():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, standing_boundary))
    record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(b"first"),
    )

    with pytest.raises(OperatorMaterialAcquireError, match="already carries a Yield"):
        record_operator_material_acquire_result(
            ledger,
            act_occurrence_event_identity=act.identity,
            boundary_material=_boundary(b"second"),
        )


def test_assignment_refuses_different_locality_and_changed_cut():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    different_locality = dict(standing)
    different_locality["locality_identity"] = "elsewhere"
    with pytest.raises(OperatorMaterialAcquireError, match="different"):
        _assignment(ledger, different_locality, standing_boundary)

    changed = dict(standing)
    changed["through_event_occurrence_identity"] = "missing"
    with pytest.raises(OperatorMaterialAcquireError, match="current Standing"):
        _assignment(ledger, changed, standing_boundary)


def test_assignment_refuses_a_cross_locality_standing_boundary():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)

    changed_cut = dict(standing)
    changed_cut["through_event_occurrence_identity"] = ledger.append(
        "other.locality.occurrence", locality_identity="elsewhere"
    ).identity
    with pytest.raises(OperatorMaterialAcquireError, match="current Standing"):
        _assignment(ledger, changed_cut, standing_boundary)

def test_assignment_refuses_a_corrupted_standing_boundary(monkeypatch):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    boundary_identity = ledger.append(
        "standing.boundary.fixture", locality_identity="source"
    ).identity
    changed = dict(standing)
    changed["through_event_occurrence_identity"] = boundary_identity
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED if identity == boundary_identity else integrity_of(identity)
        ),
    )

    with pytest.raises(OperatorMaterialAcquireError, match="current Standing"):
        _assignment(ledger, changed, standing_boundary)


def test_act_refuses_assignment_not_carried_by_supplied_standing():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    assignment = _assignment(ledger, standing, standing_boundary)

    with pytest.raises(OperatorMaterialAcquireError, match="carried assignment"):
        record_operator_material_acquire_act_occurrence(
            ledger,
            responsibility_assignment_event_identity=assignment.identity,
            responsibility_assignment_standing=standing,
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "assignment_identity",
        "assignment_subject_identity",
        "book_clause_identity",
        "acquire_act_identity",
        "act_occurrence_identity",
        "result_boundary_identity",
        "source_standing_reference",
        "scope",
        "standing_boundary_occurrence_reference",
        "standing",
        "limits",
        "unknown",
    ),
)
def test_changed_assignment_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    assignment = _assignment(ledger, standing, standing_boundary)
    changed = ledger.get(assignment.identity)
    if coordinate in {
        "assignment_identity",
        "assignment_subject_identity",
        "acquire_act_identity",
        "act_occurrence_identity",
    }:
        changed.material[coordinate] = changed.material["result_boundary_identity"]
    else:
        changed.material[coordinate] = "different"

    with pytest.raises((OperatorMaterialAcquireError, TypeError, ValueError)):
        get_operator_material_acquire_responsibility_assignment(
            ledger, assignment.identity
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "result_identity",
        "act_occurrence_identity",
        "responsibility_assignment_reference",
        "source_standing_reference",
        "scope",
        "source_boundary",
        "locality_relation",
        "locality_relation_occurrence_identity",
        "known_loss",
        "standing",
        "limits",
        "unknown",
        "act_occurrence_identity",
        "yield_relation_identity",
    ),
)
def test_changed_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, standing_boundary))
    result = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    ledger.get(result.identity).material[coordinate] = "different"

    with pytest.raises((OperatorMaterialAcquireError, TypeError, ValueError)):
        get_recorded_operator_material_acquire(ledger, result.identity)


@pytest.mark.parametrize(
    ("coordinate", "changed", "expected_requirements"),
    (
        (
            "first_subject",
            {
                "recorded_occurrence_identity": "another occurrence",
                "coordinate": "exact_material",
            },
            {
                "exact_relation": False,
                "occurrence_witness": True,
                "intact_occurrence": True,
            },
        ),
        (
            "relation",
            "another relation",
            {
                "exact_relation": False,
                "occurrence_witness": True,
                "intact_occurrence": True,
            },
        ),
        (
            "second_subject",
            "another bounded subject",
            {
                "exact_relation": False,
                "occurrence_witness": True,
                "intact_occurrence": True,
            },
        ),
        (
            "relation_occurrence_identity",
            "another occurrence",
            {
                "exact_relation": True,
                "occurrence_witness": False,
                "intact_occurrence": True,
            },
        ),
    ),
)
def test_locality_relation_refuses_each_changed_coordinate(
    coordinate,
    changed,
    expected_requirements,
):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, standing_boundary))
    result = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    ledger.get(result.identity).material["locality_relation"][coordinate] = changed

    requirements = read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    )

    assert requirements == expected_requirements
    with pytest.raises(OperatorMaterialAcquireError):
        get_recorded_operator_material_acquire(ledger, result.identity)


def test_locality_relation_refuses_a_different_or_corrupted_relation_occurrence(
    monkeypatch,
):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, standing_boundary))
    result = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    result.material["locality_relation_occurrence_identity"] = act.identity

    assert read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": False,
    }

    result.material["locality_relation_occurrence_identity"] = result.identity
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED if identity == result.identity else integrity_of(identity)
        ),
    )
    assert read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": False,
    }


def test_a_self_reference_without_o1_physiology_is_not_a_locality_relation():
    ledger = EventLedger()
    result = ledger.append(
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
        {},
        exact_material=b"material\n",
        locality_identity="source",
    )
    result.material.update(
        {
            "responsible_boundary": "this Seed",
            "source_boundary": "fixture boundary",
            "locality_relation": {
                "first_subject": {
                    "recorded_occurrence_identity": result.identity,
                    "coordinate": "exact_material",
                },
                "relation": "locality",
                "second_subject": "this Seed",
                "relation_occurrence_identity": result.identity,
            },
            "locality_relation_occurrence_identity": result.identity,
        }
    )

    assert read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": False,
    }


def test_prior_acquire_act_carrier_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    assignment = _assignment(ledger, standing, standing_boundary)
    _act(ledger, assignment)
    prior = read_operator_locality_standing(ledger, locality_identity="source")
    broken = deepcopy(prior)
    broken["operator_material_acquire_act_occurrences"] = []

    with pytest.raises(ValueError, match="acquire Act occurrences"):
        advance_operator_locality_standing(
            ledger,
            (),
            locality_identity="source",
            prior=broken,
        )


def test_prior_acquire_locality_relations_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, standing_boundary))
    result = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    prior = read_operator_locality_standing(ledger, locality_identity="source")
    assert result.identity in prior[
        "material_locality_relation_occurrences"
    ]
    broken = deepcopy(prior)
    broken["material_locality_relation_occurrences"] = []

    with pytest.raises(ValueError, match="material Locality relation occurrences"):
        advance_operator_locality_standing(
            ledger,
            (),
            locality_identity="source",
            prior=broken,
        )


def test_assignment_and_act_survive_a_durable_restart_before_raw_result(tmp_path):
    path = tmp_path / "acquire.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, standing_boundary = _context(ledger)
    assignment = _assignment(ledger, standing, standing_boundary)
    act = _act(ledger, assignment)
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    before = read_operator_locality_standing(ledger, locality_identity="source")
    assert before["responsibility_assignment_occurrences"][assignment.identity] is None
    assert before["operator_material_acquire_act_occurrences"] == {
        act.identity: None
    }
    result = record_operator_material_acquire_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(b"after restart\x00"),
    )
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    assert get_recorded_operator_material_acquire(ledger, result.identity)[
        "result_identity"
    ] == assignment.material["result_boundary_identity"]
    ledger.close()


def test_assignment_survives_alone_and_its_carried_standing_can_record_its_act(
    tmp_path,
):
    path = tmp_path / "assignment-only.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, standing_boundary = _context(ledger)
    assignment = _assignment(ledger, standing, standing_boundary)
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    after_assignment = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    assert after_assignment["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert after_assignment["operator_material_acquire_act_occurrences"] == {}

    act = record_operator_material_acquire_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=after_assignment,
    )

    assert act.material["responsibility_assignment_reference"][
        "recorded_occurrence_identity"
    ] == assignment.identity
    assert [
        event.identity
        for event in ledger.occurrences_in_append_order(
            (assignment.identity, act.identity),
            locality_identity="source",
        )
    ] == [
        assignment.identity,
        act.identity,
    ]
    ledger.close()


def test_durable_material_contains_no_later_control_words():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"ordinary\n"),
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list()
            if event.kind.startswith("operator.material.acquire")
        ]
    ).lower()

    for absent in ("session", "exit", "quit", "stop"):
        assert absent not in durable


PYTEST_ADMISSION = (
    test_one_read_records_distinct_assignment_act_yield_and_exact_raw_result,
    test_empty_boundary_leaves_assignment_and_act_without_result_or_yield,
    test_console_empty_input_records_one_unfinished_boundary_occurrence,
    test_console_records_one_fresh_occurrence_per_read_including_final_empty_read,
    test_ordinary_operator_material_is_the_exact_acquisition_measurement_source,
    test_operator_result_kind_without_source_g_physiology_is_not_acquisition,
    test_exact_acquisition_families_merge_only_their_append_order,
    test_equal_raw_results_keep_distinct_occurrences_and_scopes,
    test_one_acquire_act_cannot_yield_twice,
    test_assignment_refuses_different_locality_and_changed_cut,
    test_assignment_refuses_a_cross_locality_standing_boundary,
    test_assignment_refuses_a_corrupted_standing_boundary,
    test_act_refuses_assignment_not_carried_by_supplied_standing,
    test_changed_assignment_coordinates_are_refused,
    test_changed_result_coordinates_are_refused,
    test_locality_relation_refuses_each_changed_coordinate,
    test_locality_relation_refuses_a_different_or_corrupted_relation_occurrence,
    test_a_self_reference_without_o1_physiology_is_not_a_locality_relation,
    test_prior_acquire_act_carrier_must_remain_an_identity_dictionary,
    test_prior_acquire_locality_relations_must_remain_an_identity_dictionary,
    test_assignment_and_act_survive_a_durable_restart_before_raw_result,
    test_assignment_survives_alone_and_its_carried_standing_can_record_its_act,
    test_durable_material_contains_no_later_control_words,
)
