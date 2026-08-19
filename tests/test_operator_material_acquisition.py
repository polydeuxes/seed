from __future__ import annotations

from copy import deepcopy
from io import BytesIO, StringIO

import pytest

FIDELITY_SUBJECT = "operator_material_acquisition_witness"

from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.operator_material_acquisition import (
    OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND,
    OPERATOR_MATERIAL_ACQUIRE_LOCALITY_RELATION_OCCURRENCE_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
    OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OperatorMaterialAcquireError,
    get_operator_material_acquire_responsibility_assignment,
    get_recorded_operator_material_acquire,
    read_operator_material_acquire_locality_relation_requirements,
    record_operator_material_acquire_responsibility_assignment,
    record_operator_material_acquire_responsible_act_evidence,
    record_operator_material_acquire_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.operator_representation import record_operator_representation
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation


def _context(ledger, locality_identity="source"):
    standing = read_operator_locality_standing(
        ledger, locality_identity=locality_identity
    )
    representation = record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=standing,
    )
    standing = advance_operator_locality_standing(
        ledger,
        representation["recorded_occurrence_references"],
        locality_identity=locality_identity,
        prior=standing,
    )
    return standing, representation


def _assignment(ledger, standing, representation, locality_identity="source"):
    return record_operator_material_acquire_responsibility_assignment(
        ledger,
        locality_identity=locality_identity,
        addressed_representation_event_identity=representation[
            "representation_event_identity"
        ],
        locality_standing=standing,
    )


def _act(ledger, assignment):
    standing = read_operator_locality_standing(
        ledger, locality_identity=assignment.locality_identity
    )
    return record_operator_material_acquire_responsible_act_evidence(
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
    standing, representation = _context(ledger)
    assignment = _assignment(ledger, standing, representation)
    after_assignment = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    act_evidence = record_operator_material_acquire_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=after_assignment,
    )
    before_result = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    result = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
        boundary_material=_boundary(),
    )
    recorded = get_recorded_operator_material_acquire(ledger, result.identity)

    assert assignment.kind == (
        OPERATOR_MATERIAL_ACQUIRE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
    )
    assert act_evidence.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND
    assert result.kind == OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND
    assert assignment.exact_material is act_evidence.exact_material is None
    assert result.exact_material == b"\x00\xffraw\n"
    assert assignment.material["book_clause_identity"] == "01.Source.G"
    assert assignment.identity in after_assignment[
        "responsibility_assignment_occurrences"
    ]
    assert recorded["result_identity"] == assignment.material[
        "result_boundary_identity"
    ]
    assert recorded["source_standing_reference"] == {
        "locality_identity": "source",
        "locality_standing_through_event_occurrence_identity": standing[
            "through_event_occurrence_identity"
        ],
        "addressed_representation_event_identity": representation[
            "representation_event_identity"
        ],
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
    assert recorded["locality_evidence_identity"] == result.identity
    assert recorded["result_identity"] != result.identity
    assert read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=result.identity,
        evidence_of_yield_relation_event_identity=result.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=act_evidence.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
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
            act_evidence.identity,
            result.identity,
            result.material["evidence_of_yield_relation_identity"],
        }
    ) == 10

    carried = advance_operator_locality_standing(
        ledger,
        (result.material["evidence_of_yield_relation_identity"], result.identity),
        locality_identity="source",
        prior=before_result,
    )
    replayed = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    assert carried == replayed
    assert replayed["responsibility_assignment_occurrences"][assignment.identity] is None
    assert replayed["operator_material_acquire_act_occurrences"] == {
        act_evidence.identity: None
    }
    assert replayed["exact_result_occurrences"][result.identity] is None


def test_empty_boundary_leaves_assignment_and_act_without_result_or_yield():
    ledger = EventLedger()
    standing, representation = _context(ledger)
    assignment = _assignment(ledger, standing, representation)
    act_evidence = _act(ledger, assignment)
    before = tuple(ledger.list())

    with pytest.raises(
        OperatorMaterialAcquireError, match="establishes no acquire result"
    ):
        record_operator_material_acquire_result(
            ledger,
            responsible_act_evidence_event_identity=act_evidence.identity,
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
        output_stream=StringIO(),
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
            if event.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND
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
        output_stream=StringIO(),
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
        if event.kind == OPERATOR_MATERIAL_ACQUIRE_ACT_EVIDENCE_KIND
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
        if result.material["responsible_act_evidence_identity"] == acts[-1].identity
    ]


def test_equal_raw_results_keep_distinct_occurrences_and_scopes():
    ledger = EventLedger()
    standing, representation = _context(ledger)
    results = []
    assignments = []
    acts = []
    for _ in range(2):
        assignment = _assignment(ledger, standing, representation)
        act = _act(ledger, assignment)
        result = record_operator_material_acquire_result(
            ledger,
            responsible_act_evidence_event_identity=act.identity,
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
    standing, representation = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, representation))
    record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
        boundary_material=_boundary(b"first"),
    )

    with pytest.raises(OperatorMaterialAcquireError, match="already carries a Yield"):
        record_operator_material_acquire_result(
            ledger,
            responsible_act_evidence_event_identity=act.identity,
            boundary_material=_boundary(b"second"),
        )


def test_assignment_refuses_different_locality_and_changed_cut():
    ledger = EventLedger()
    standing, representation = _context(ledger)
    different_locality = dict(standing)
    different_locality["locality_identity"] = "elsewhere"
    with pytest.raises(OperatorMaterialAcquireError, match="different"):
        _assignment(ledger, different_locality, representation)

    changed = dict(standing)
    changed["through_event_occurrence_identity"] = "missing"
    with pytest.raises(OperatorMaterialAcquireError, match="current Standing"):
        _assignment(ledger, changed, representation)


def test_assignment_refuses_cross_locality_and_reversed_standing_boundaries():
    ledger = EventLedger()
    standing, representation = _context(ledger)

    changed_cut = dict(standing)
    changed_cut["through_event_occurrence_identity"] = ledger.append(
        "other.locality.occurrence", locality_identity="elsewhere"
    ).identity
    with pytest.raises(OperatorMaterialAcquireError, match="current Standing"):
        _assignment(ledger, changed_cut, representation)

    representation_identity = representation["representation_event_identity"]
    earlier = next(
        event
        for event in ledger.list_locality("source")
        if event.identity != representation_identity
    )
    reversed_boundary = dict(standing)
    reversed_boundary["through_event_occurrence_identity"] = earlier.identity
    with pytest.raises(OperatorMaterialAcquireError, match="current Standing"):
        _assignment(ledger, reversed_boundary, representation)


def test_assignment_refuses_a_corrupted_standing_boundary(monkeypatch):
    ledger = EventLedger()
    standing, representation = _context(ledger)
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
        _assignment(ledger, changed, representation)


def test_addressed_representation_can_be_the_exact_standing_boundary():
    ledger = EventLedger()
    standing, representation = _context(ledger)
    same_boundary = dict(standing)
    same_boundary["through_event_occurrence_identity"] = representation[
        "representation_event_identity"
    ]

    assignment = _assignment(ledger, same_boundary, representation)

    assert assignment.material["source_standing_reference"][
        "locality_standing_through_event_occurrence_identity"
    ] == representation["representation_event_identity"]


def test_act_refuses_assignment_not_carried_by_supplied_standing():
    ledger = EventLedger()
    standing, representation = _context(ledger)
    assignment = _assignment(ledger, standing, representation)

    with pytest.raises(OperatorMaterialAcquireError, match="carried assignment"):
        record_operator_material_acquire_responsible_act_evidence(
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
        "evidence_occurrence_reference",
        "authority",
        "standing",
        "limits",
        "unknown",
    ),
)
def test_changed_assignment_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, representation = _context(ledger)
    assignment = _assignment(ledger, standing, representation)
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
        "locality_evidence_identity",
        "known_loss",
        "authority",
        "standing",
        "limits",
        "unknown",
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    ),
)
def test_changed_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, representation = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, representation))
    result = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    ledger.get(result.identity).material[coordinate] = "different"

    with pytest.raises((OperatorMaterialAcquireError, TypeError, ValueError)):
        get_recorded_operator_material_acquire(ledger, result.identity)


@pytest.mark.parametrize(
    ("coordinate", "changed"),
    (
        (
            "first_subject",
            {
                "recorded_occurrence_identity": "another occurrence",
                "coordinate": "exact_material",
            },
        ),
        ("relation", "another relation"),
        ("second_subject", "another bounded subject"),
        ("relation_occurrence_identity", "another occurrence"),
    ),
)
def test_locality_relation_refuses_each_changed_coordinate(coordinate, changed):
    ledger = EventLedger()
    standing, representation = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, representation))
    result = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    ledger.get(result.identity).material["locality_relation"][coordinate] = changed

    requirements = read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    )

    assert not all(requirements.values())
    with pytest.raises(OperatorMaterialAcquireError):
        get_recorded_operator_material_acquire(ledger, result.identity)


def test_locality_relation_refuses_a_different_or_corrupted_evidence_occurrence(
    monkeypatch,
):
    ledger = EventLedger()
    standing, representation = _context(ledger)
    act = _act(ledger, _assignment(ledger, standing, representation))
    result = record_operator_material_acquire_result(
        ledger,
        responsible_act_evidence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    result.material["locality_evidence_identity"] = act.identity

    assert read_operator_material_acquire_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    ) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": False,
    }

    result.material["locality_evidence_identity"] = result.identity
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
        "intact_evidence": False,
    }


def test_prior_acquire_act_carrier_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    standing, representation = _context(ledger)
    assignment = _assignment(ledger, standing, representation)
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


def test_assignment_and_act_survive_a_durable_restart_before_raw_result(tmp_path):
    path = tmp_path / "acquire.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, representation = _context(ledger)
    assignment = _assignment(ledger, standing, representation)
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
        responsible_act_evidence_event_identity=act.identity,
        boundary_material=_boundary(b"after restart\x00"),
    )
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    assert get_recorded_operator_material_acquire(ledger, result.identity)[
        "result_identity"
    ] == assignment.material["result_boundary_identity"]
    ledger.close()


def test_assignment_survives_alone_and_a_later_carried_cut_can_record_its_act(
    tmp_path,
):
    path = tmp_path / "assignment-only.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, representation = _context(ledger)
    assignment = _assignment(ledger, standing, representation)
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    after_assignment = read_operator_locality_standing(
        ledger, locality_identity="source"
    )
    assert after_assignment["responsibility_assignment_occurrences"] == {
        assignment.identity: None
    }
    assert after_assignment["operator_material_acquire_act_occurrences"] == {}

    interleaved_representation = record_operator_representation(
        ledger,
        locality_identity="source",
        locality_standing=after_assignment,
    )
    carried = advance_operator_locality_standing(
        ledger,
        interleaved_representation["recorded_occurrence_references"],
        locality_identity="source",
        prior=after_assignment,
    )
    act = record_operator_material_acquire_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=carried,
    )

    assert act.material["responsibility_assignment_reference"][
        "recorded_occurrence_identity"
    ] == assignment.identity
    assert [
        event.identity
        for event in ledger.occurrences_in_append_order(
            (assignment.identity, interleaved_representation[
                "representation_event_identity"
            ], act.identity),
            locality_identity="source",
        )
    ] == [
        assignment.identity,
        interleaved_representation["representation_event_identity"],
        act.identity,
    ]
    ledger.close()


def test_durable_material_contains_no_later_control_words():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"ordinary\n"),
        output_stream=StringIO(),
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
