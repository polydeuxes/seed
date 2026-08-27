"""Operator material is bounded by one exact source boundary."""

from __future__ import annotations

from copy import deepcopy
from io import BytesIO

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.byte_measurement import BYTE_MEASUREMENT_RECORDED_KIND
from seed_runtime.material_source import (
    MaterialSourceError,
    iter_exact_material_results,
    read_exact_material_result,
)
from seed_runtime.witness_material_source import WITNESS_MATERIAL_SOURCE_RECORDED_KIND, record_witness_material_source
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_current_coordinates import (
    advance_operator_current_coordinates,
    read_operator_current_coordinates,
)
from seed_runtime.operator_material_source import (
    OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT,
    OPERATOR_MATERIAL_SOURCE_LOCALITY_RELATION_OCCURRENCE_KIND,
    OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
    OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
    OperatorMaterialSourceError,
    get_operator_material_source_subject_to_act_binding,
    get_recorded_operator_material_source,
    read_operator_material_source_locality_relation_requirements,
    record_operator_material_source_subject_to_act_binding,
    record_operator_material_source_act_occurrence,
    record_operator_material_source_result,
)
from seed_runtime.operator_material_boundary import OperatorBoundaryMaterial
from seed_runtime.yield_relation import read_requirements_of_yield_relation
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)


def _context(ledger, locality_identity="source"):
    standing = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    return standing, standing["through_event_occurrence_identity"]


def _binding(ledger, standing, locality_identity="source"):
    return record_operator_material_source_subject_to_act_binding(
        ledger,
        locality_identity=locality_identity,
        current_coordinates=standing,
        source_boundary="fixture exact byte boundary",
    )


def _act(ledger, binding):
    standing = read_operator_current_coordinates(
        ledger, locality_identity=binding.locality_identity
    )
    return record_operator_material_source_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=standing,
    )


def _boundary(exact=b"\x00\xffraw\n"):
    return OperatorBoundaryMaterial(
        exact_bytes=exact,
        eof=exact == b"",
        material_boundary="fixture exact byte boundary",
    )


def test_one_read_records_distinct_binding_act_yield_and_exact_raw_result():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    binding = _binding(ledger, standing)
    after_binding = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    act_occurrence = record_operator_material_source_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=after_binding,
    )
    before_result = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act_occurrence.identity,
        boundary_material=_boundary(),
    )
    recorded = get_recorded_operator_material_source(ledger, result.identity)

    assert binding.kind == (
        OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    )
    assert act_occurrence.kind == OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT
    assert result.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
    assert binding.exact_material is act_occurrence.exact_material is None
    assert result.exact_material == b"\x00\xffraw\n"
    assert tuple(sorted(binding.material)) == (
        "act",
        "act_occurrence_identity",
        "book_clause_identity",
        "current_coordinate_reference",
        "exact_act_identity",
        "result_boundary_identity",
        "subject_reference",
    )
    assert binding.identity in after_binding[
        "subject_to_act_binding_occurrences"
    ]
    assert recorded["result_identity"] == binding.material[
        "result_boundary_identity"
    ]
    assert recorded["current_coordinate_reference"] == {
        "locality_identity": "source",
        "through_event_occurrence_identity": standing_boundary,
    }
    assert OPERATOR_MATERIAL_SOURCE_LOCALITY_RELATION_OCCURRENCE_KIND == (
        OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
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
    assert read_operator_material_source_locality_relation_requirements(
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
            binding.identity,
            binding.material["exact_act_identity"],
            binding.material["act_occurrence_identity"],
            binding.material["result_boundary_identity"],
            act_occurrence.identity,
            result.identity,
            result.material["yield_relation_identity"],
        }
    ) == 7

    carried = advance_operator_current_coordinates(
        ledger,
        (result.material["yield_relation_identity"], result.identity),
        locality_identity="source",
        prior=before_result,
    )
    replayed = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    assert carried == replayed
    assert replayed["subject_to_act_binding_occurrences"][binding.identity] is None
    assert replayed["operator_material_source_act_occurrences"] == {
        act_occurrence.identity: None
    }
    assert replayed["exact_result_occurrences"][result.identity] == (
        act_occurrence.material["subject_to_act_binding_reference"]
    )
    assert replayed["material_locality_relation_occurrences"] == {
        result.identity: {
            "locality_relation": deepcopy(recorded["locality_relation"]),
        }
    }


def test_empty_boundary_leaves_binding_and_act_without_result_or_yield():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    binding = _binding(ledger, standing)
    act_occurrence = _act(ledger, binding)
    before = tuple(ledger.list())

    with pytest.raises(
        OperatorMaterialSourceError, match="establishes no material result"
    ):
        record_operator_material_source_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
            boundary_material=_boundary(b""),
        )

    assert tuple(ledger.list()) == before
    assert not [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
    ]


def test_result_refuses_material_from_another_source_boundary():
    ledger = EventLedger()
    standing, _standing_boundary = _context(ledger)
    act_occurrence = _act(ledger, _binding(ledger, standing))
    before = tuple(ledger.list())

    with pytest.raises(OperatorMaterialSourceError, match="source boundary"):
        record_operator_material_source_result(
            ledger,
            act_occurrence_event_identity=act_occurrence.identity,
            boundary_material=OperatorBoundaryMaterial(
                exact_bytes=b"material",
                eof=False,
                material_boundary="another source boundary",
            ),
        )

    assert tuple(ledger.list()) == before


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
            == OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        ]
    ) == 1
    assert len(
        [
            event
            for event in ledger.list()
            if event.kind == OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT
        ]
    ) == 1
    assert not [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
    ]


def test_console_records_one_fresh_occurrence_per_read_including_final_empty_read(
    monkeypatch,
):
    class _AlreadyMeasured(set):
        def __contains__(self, _item):
            return True

    monkeypatch.setattr(
        "seed_runtime.operator_console._recorded_byte_measurement_material_references",
        lambda _ledger: _AlreadyMeasured(),
    )
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"first\nsecond\n"),
    )
    bindings = [
        event
        for event in ledger.list()
        if event.kind
        == OPERATOR_MATERIAL_SOURCE_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
    ]
    acts = [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_SOURCE_ACT_OCCURRENCE_EVENT
    ]
    results = [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
    ]

    assert len(bindings) == len(acts) == 3
    assert len(results) == 2
    assert [result.exact_material for result in results] == [b"first\n", b"second\n"]
    assert len(
        {
            binding.material["act_occurrence_identity"]
            for binding in bindings
        }
    ) == 3
    assert not [
        result
        for result in results
        if result.material["act_occurrence_event_identity"] == acts[-1].identity
    ]


def test_ordinary_operator_material_is_the_exact_source_measurement_source():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"H"),
    )
    sources = [
        event
        for event in ledger.list()
        if event.kind == OPERATOR_MATERIAL_SOURCE_RECORDED_KIND
    ]
    assert len(sources) == 1
    standing = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    assert standing["material_locality_relation_occurrences"] == {
        sources[0].identity: {
            "locality_relation": deepcopy(
                sources[0].material["locality_relation"]
            ),
        }
    }
    source_results = [
        event
        for event in ledger.list()
        if event.kind == WITNESS_MATERIAL_SOURCE_RECORDED_KIND
    ]
    assert source_results == []
    assert read_exact_material_result(ledger, sources[0].identity) == sources[0]
    assert sources[0].exact_material == b"H"
    assert sources[0].material["source_occurrence_references"] == []
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
    assert position_results[0].material[
        "source_material_result_occurrence_identity"
    ] == (
        sources[0].identity
    )
    assert byte_results[0].material["assertions"][0]["dimensions"]["content"][
        "source_material"
    ] == [{"material_result_occurrence_identity": sources[0].identity}]


def test_operator_result_kind_without_source_g_physiology_is_not_source():
    ledger = EventLedger()
    claimed = ledger.append(
        OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
        {
            "unknown": ["represented_relation", "source_relation"],
        },
        exact_material=b"claimed O1",
        locality_identity="source",
    )

    with pytest.raises(MaterialSourceError, match="intact physiology"):
        read_exact_material_result(ledger, claimed.identity)


def test_exact_source_families_merge_only_their_append_order():
    ledger = EventLedger()
    first = record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"first supplied material",
        source_boundary="first boundary",
    )
    operator = record_operator_material_occurrence(
        ledger,
        locality_identity="source",
        exact=b"operator material\n",
    )
    last = record_witness_material_source(
        ledger,
        locality_identity="source",
        exact_bytes=b"last supplied material",
        source_boundary="last boundary",
    )

    assert [
        event.identity
        for event in iter_exact_material_results(ledger, "source")
    ] == [first.identity, operator.identity, last.identity]


def test_equal_raw_results_keep_distinct_occurrences_and_boundaries():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    results = []
    bindings = []
    acts = []
    for _ in range(2):
        binding = _binding(ledger, standing)
        act = _act(ledger, binding)
        result = record_operator_material_source_result(
            ledger,
            act_occurrence_event_identity=act.identity,
            boundary_material=_boundary(b"same\x00\xff"),
        )
        bindings.append(binding)
        acts.append(act)
        results.append(result)
        standing = read_operator_current_coordinates(
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


def test_one_source_act_cannot_yield_twice():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _binding(ledger, standing))
    record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(b"first"),
    )

    with pytest.raises(OperatorMaterialSourceError, match="already carries a Yield"):
        record_operator_material_source_result(
            ledger,
            act_occurrence_event_identity=act.identity,
            boundary_material=_boundary(b"second"),
        )


def test_binding_refuses_different_locality_and_changed_cut():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    different_locality = dict(standing)
    different_locality["locality_identity"] = "elsewhere"
    with pytest.raises(OperatorMaterialSourceError, match="different"):
        _binding(ledger, different_locality)

    changed = dict(standing)
    changed["through_event_occurrence_identity"] = "missing"
    with pytest.raises(OperatorMaterialSourceError, match="through-occurrence"):
        _binding(ledger, changed)


def test_binding_refuses_a_cross_locality_through_occurrence_boundary():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)

    changed_cut = dict(standing)
    changed_cut["through_event_occurrence_identity"] = ledger.append(
        "other.locality.occurrence", locality_identity="elsewhere"
    ).identity
    with pytest.raises(OperatorMaterialSourceError, match="through-occurrence"):
        _binding(ledger, changed_cut)

def test_binding_refuses_a_corrupted_through_occurrence_boundary(monkeypatch):
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

    with pytest.raises(OperatorMaterialSourceError, match="through-occurrence"):
        _binding(ledger, changed)


def test_act_refuses_binding_absent_from_current_coordinates():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    binding = _binding(ledger, standing)

    with pytest.raises(OperatorMaterialSourceError, match="carried binding"):
        record_operator_material_source_act_occurrence(
            ledger,
            subject_to_act_binding_event_identity=binding.identity,
            current_coordinates=standing,
        )


@pytest.mark.parametrize(
    "coordinate",
    (
        "book_clause_identity",
        "subject_reference",
        "act",
        "exact_act_identity",
        "act_occurrence_identity",
        "current_coordinate_reference",
    ),
)
def test_changed_binding_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    binding = _binding(ledger, standing)
    changed = ledger.get(binding.identity)
    if coordinate in {"exact_act_identity", "act_occurrence_identity"}:
        changed.material[coordinate] = changed.material["result_boundary_identity"]
    else:
        changed.material[coordinate] = "different"

    with pytest.raises((OperatorMaterialSourceError, TypeError, ValueError)):
        get_operator_material_source_subject_to_act_binding(
            ledger, binding.identity
        )


def test_result_refuses_a_changed_binding_result_boundary():
    ledger = EventLedger()
    current_coordinates, _through_occurrence = _context(ledger)
    binding = _binding(ledger, current_coordinates)
    act = _act(ledger, binding)
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )

    binding.material["result_boundary_identity"] = "different"

    with pytest.raises((OperatorMaterialSourceError, TypeError, ValueError)):
        get_recorded_operator_material_source(ledger, result.identity)


@pytest.mark.parametrize(
    "coordinate",
    (
        "result_identity",
        "exact_act_identity",
        "act_occurrence_identity",
        "exact_act",
        "subject_to_act_binding_reference",
        "current_coordinate_reference",
        "source_boundary",
        "locality_relation",
        "locality_relation_occurrence_identity",
        "act_occurrence_event_identity",
        "yield_relation_identity",
    ),
)
def test_changed_result_coordinates_are_refused(coordinate):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _binding(ledger, standing))
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    ledger.get(result.identity).material[coordinate] = "different"

    with pytest.raises((OperatorMaterialSourceError, TypeError, ValueError)):
        get_recorded_operator_material_source(ledger, result.identity)


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
    act = _act(ledger, _binding(ledger, standing))
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    ledger.get(result.identity).material["locality_relation"][coordinate] = changed

    requirements = read_operator_material_source_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    )

    assert requirements == expected_requirements
    with pytest.raises(OperatorMaterialSourceError):
        get_recorded_operator_material_source(ledger, result.identity)


def test_locality_relation_refuses_a_different_or_corrupted_relation_occurrence(
    monkeypatch,
):
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _binding(ledger, standing))
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    result.material["locality_relation_occurrence_identity"] = act.identity

    assert read_operator_material_source_locality_relation_requirements(
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
    assert read_operator_material_source_locality_relation_requirements(
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
        OPERATOR_MATERIAL_SOURCE_RECORDED_KIND,
        {},
        exact_material=b"material\n",
        locality_identity="source",
    )
    result.material.update(
        {
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

    assert read_operator_material_source_locality_relation_requirements(
        ledger,
        recorded_result_event_identity=result.identity,
    ) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_occurrence": False,
    }


def test_prior_source_act_carrier_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    binding = _binding(ledger, standing)
    _act(ledger, binding)
    prior = read_operator_current_coordinates(ledger, locality_identity="source")
    broken = deepcopy(prior)
    broken["operator_material_source_act_occurrences"] = []

    with pytest.raises(ValueError, match="source Act occurrences"):
        advance_operator_current_coordinates(
            ledger,
            (),
            locality_identity="source",
            prior=broken,
        )


def test_prior_source_locality_relations_must_remain_an_identity_dictionary():
    ledger = EventLedger()
    standing, standing_boundary = _context(ledger)
    act = _act(ledger, _binding(ledger, standing))
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(),
    )
    prior = read_operator_current_coordinates(ledger, locality_identity="source")
    assert result.identity in prior[
        "material_locality_relation_occurrences"
    ]
    broken = deepcopy(prior)
    broken["material_locality_relation_occurrences"] = []

    with pytest.raises(ValueError, match="material Locality relation occurrences"):
        advance_operator_current_coordinates(
            ledger,
            (),
            locality_identity="source",
            prior=broken,
        )


def test_binding_and_act_remain_addressable_after_restart_before_result(tmp_path):
    path = tmp_path / "source.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, standing_boundary = _context(ledger)
    binding = _binding(ledger, standing)
    act = _act(ledger, binding)
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    before = read_operator_current_coordinates(ledger, locality_identity="source")
    assert before["subject_to_act_binding_occurrences"][binding.identity] is None
    assert before["operator_material_source_act_occurrences"] == {
        act.identity: None
    }
    result = record_operator_material_source_result(
        ledger,
        act_occurrence_event_identity=act.identity,
        boundary_material=_boundary(b"after restart\x00"),
    )
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    assert get_recorded_operator_material_source(ledger, result.identity)[
        "result_identity"
    ] == binding.material["result_boundary_identity"]
    ledger.close()


def test_binding_alone_remains_addressable_and_can_record_its_act(
    tmp_path,
):
    path = tmp_path / "binding-only.sqlite"
    ledger = SQLiteEventLedger(str(path))
    standing, standing_boundary = _context(ledger)
    binding = _binding(ledger, standing)
    ledger.close()

    ledger = SQLiteEventLedger(str(path))
    after_binding = read_operator_current_coordinates(
        ledger, locality_identity="source"
    )
    assert after_binding["subject_to_act_binding_occurrences"] == {
        binding.identity: None
    }
    assert after_binding["operator_material_source_act_occurrences"] == {}

    act = record_operator_material_source_act_occurrence(
        ledger,
        subject_to_act_binding_event_identity=binding.identity,
        current_coordinates=after_binding,
    )

    assert act.material["subject_to_act_binding_reference"][
        "recorded_occurrence_identity"
    ] == binding.identity
    assert [
        event.identity
        for event in ledger.occurrences_in_append_order(
            (binding.identity, act.identity),
            locality_identity="source",
        )
    ] == [
        binding.identity,
        act.identity,
    ]
    ledger.close()


def test_durable_material_contains_no_later_control_words():
    ledger = EventLedger()
    record_operator_material_occurrence(
        ledger=ledger,
        locality_identity="source",
        exact=b"ordinary\n",
    )
    durable = repr(
        [
            (event.kind, event.material)
            for event in ledger.list()
            if event.kind.startswith("operator.material.source")
        ]
    ).lower()

    for absent in (
        "assignment",
        "responsibility",
        "responsible_boundary",
        "session",
        "standing",
        "exit",
        "quit",
        "stop",
    ):
        assert absent not in durable
