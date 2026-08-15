from tests.binary_input import binary_input
from io import StringIO
import hashlib
import json

import pytest

from seed_runtime.byte_measurement import (
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
    BYTE_PAIR_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_RESULT_COORDINATES,
    BYTE_MEASUREMENT_RULE,
    ByteMeasurementError,
    RESPONSIBILITY_UNESTABLISHED,
    SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    _measure_byte_counts_through,
    _identity,
    _pair_input_applicability,
    get_recorded_pair_input_applicability,
    assertions_of_recorded_byte_measurement,
    assertions_of_recorded_adjacent_byte_pair_measurement,
    input_applicability_of_recorded_adjacent_byte_pair_measurement,
    measure_byte_counts,
    record_byte_count_layer,
    record_adjacent_byte_pair_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.event import Event
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.yield_evidence import YIELD_EVIDENCE_KIND
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingest_material,
)


def _ledger(text="猫\n狗\n"):
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=binary_input(text + ""),
        output_stream=StringIO(),
    )
    return ledger


def _byte_source(ledger):
    return record_byte_count_layer(
        ledger,
        source_locality_identities=("source",),
        recording_locality_identity="byte-measurement",
    )


def test_exact_bytes_supply_the_measured_subjects_without_whitespace():
    measured = measure_byte_counts(
        _ledger(), source_locality_identities=("source",)
    )
    counts = {item.representation: item for item in measured.counts}

    # UTF-8 猫 = e7 8c ab and 狗 = e7 8b 97.  No character boundary is used or
    # asserted; these are the exact bytes Seed recorded.
    assert counts[231].count == 2
    assert counts[140].count == 1
    assert counts[171].count == 1
    assert counts[139].count == 1
    assert counts[151].count == 1
    assert counts[10].count == 2
    assert len(measured.source_material) == 2


def test_the_complete_declared_localities_supply_the_inputs():
    measured = measure_byte_counts(
        _ledger("a\nb\n"), source_locality_identities=("source",)
    )
    assert len(measured.source_material) == 2
    assert all(
        set(item) == {"ingest_occurrence_identity"}
        for item in measured.source_material
    )
    assert measured.completeness_boundary.identity


def test_count_and_recurrence_are_distinct_results():
    event = record_byte_count_layer(
        _ledger("ab\n"),
        source_locality_identities=("source",),
        recording_locality_identity="measurement",
    )
    by_byte = {}
    for assertion in event.material["assertions"]:
        representation = assertion["assertion_subject"].get("representation")
        if representation is not None:
            by_byte.setdefault(representation, []).append(assertion)

    assert [item["result"] for item in by_byte[97]] == ["count"]
    assert by_byte[97][0]["dimensions"]["content"]["count"] == 1
    # The newline occurs once too. No positive singleton is called recurrence.
    assert [item["result"] for item in by_byte[10]] == ["count"]


def test_recurrence_exists_only_above_one():
    event = record_byte_count_layer(
        _ledger("aa\n"),
        source_locality_identities=("source",),
        recording_locality_identity="measurement",
    )
    results = [
        item["result"]
        for item in event.material["assertions"]
        if item["assertion_subject"].get("representation") == 97
    ]
    assert results == ["count", "recurrence"]


def test_the_rule_is_mechanics_not_an_unchecked_callable():
    event = record_byte_count_layer(
        _ledger("the cat\n"),
        source_locality_identities=("source",),
        recording_locality_identity="measurement",
    )
    assert event.material["measurement_rule"] == BYTE_MEASUREMENT_RULE
    assert event.kind == BYTE_MEASUREMENT_RECORDED_KIND
    assert "zebra" not in str(event.material)


def test_recorded_results_replay_the_complete_bounded_source_read():
    ledger = _ledger("猫\n狗\n")
    event = record_byte_count_layer(
        ledger,
        source_locality_identities=("source",),
        recording_locality_identity="measurement",
    )
    read = assertions_of_recorded_byte_measurement(ledger, event.identity)
    assert read
    assert all(item.recorded_occurrence_identity == event.identity for item in read)
    evidence = ledger.get(event.material["yield_evidence_identity"])
    assert evidence.kind == YIELD_EVIDENCE_KIND
    assert evidence.material["dimensions"]["act_occurrence_identity"] == event.material[
        "act_occurrence_identity"
    ]
    assert "occurrence_preservation" not in evidence.material["yield_coordinates"]

    count = next(
        item
        for item in read
        if item.representation == 231 and item.result == "count"
    )
    assert count.material["dimensions"]["content"] == {
        "input_count": 2,
        "occurrences_carrying": 2,
        "count": 2,
    }
    assert count.material["assertion_scope"] == {
        "source_locality_identities": ["source"],
    }
    assert count.material["dimensions"]["source_provenance"]
    assert count.material["dimensions"]["authority"] == "unestablished"
    assert count.material["dimensions"]["evidence_scope"]
    assert count.material["unknowns"]
    assert count.material["conflicts"] == "Unknown"
    assert count.material["limits"]
    assert count.support_assertion_references == (
        {
            "recorded_occurrence_identity": event.identity,
            "assertion_identity": event.material["assertions"][0]["dimensions"]["identity"],
        },
    )

    detached_material = count.material
    detached_material["dimensions"]["standing"] = "unsupported"
    assert count.material["dimensions"]["standing"] == "measured"

    detached_references = count.support_assertion_references
    detached_references[0]["assertion_identity"] = "unsupported"
    assert count.support_assertion_references[0]["assertion_identity"] != "unsupported"

    # Read preserves exact durable JSON kinds. It does not protect the
    # result by transmuting lists to tuples or dicts to proxy objects.
    represented = Event(
        identity="re-represented",
        kind="test.representation",
        material=count.material,
    )
    assert type(represented.material) is dict
    assert type(represented.material["assertion_scope"]["source_locality_identities"]) is list


def test_a_self_consistent_truncated_source_assertion_is_refused():
    ledger = _ledger("a\nb\n")
    event = record_byte_count_layer(
        ledger,
        source_locality_identities=("source",),
        recording_locality_identity="measurement",
    )
    assertions = event.material["assertions"]
    source = assertions[0]
    source["dimensions"]["content"]["source_material"] = source["dimensions"][
        "content"
    ]["source_material"][:1]
    evidence = ledger.get(event.material["yield_evidence_identity"])
    evidence.material["result"] = {
        name: event.material[name] for name in BYTE_RESULT_COORDINATES
    }
    with pytest.raises(ByteMeasurementError, match="complete bounded source read"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_recording_occurrence_evidence_is_validated_exactly():
    ledger = _ledger("a\n")
    event = record_byte_count_layer(
        ledger,
        source_locality_identities=("source",),
        recording_locality_identity="measurement",
    )
    event.material["occurrence_preservation"] = "something else"
    with pytest.raises(ByteMeasurementError, match="recording-occurrence Evidence"):
        assertions_of_recorded_byte_measurement(ledger, event.identity)


def test_ingest_after_the_measurement_boundary_cannot_enter_the_measurement():
    ledger = EventLedger()
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"a",
        source_role="operator",
        source_boundary="first boundary",
    )
    boundary = ledger.append_boundary()
    ingest_material(
        ledger,
        locality_identity="source",
        exact_bytes=b"b",
        source_role="system",
        source_boundary="second boundary",
    )
    measured = _measure_byte_counts_through(
        ledger,
        localities=("source",),
        boundary=boundary,
    )
    assert {item.representation: item.count for item in measured.counts} == {97: 1}


def test_a_missing_declared_locality_is_refused():
    with pytest.raises(ByteMeasurementError, match="absent"):
        measure_byte_counts(
            _ledger(), source_locality_identities=("missing",)
        )


def test_ingest_must_match_its_exact_byte_coordinates():
    ledger = _ledger("a\n")
    ingest = next(
        ledger.iter_locality_kind("source", MATERIAL_INGEST_OCCURRED_KIND)
    )
    object.__setattr__(ingest, "exact_material", None)
    with pytest.raises(ByteMeasurementError, match="carries no exact bytes"):
        measure_byte_counts(
            ledger, source_locality_identities=("source",)
        )


def test_repeated_locality_coordinate_does_not_repeat_one_ingest():
    ledger = _ledger("a\n")
    once = measure_byte_counts(
        ledger, source_locality_identities=("source",)
    )
    repeated = measure_byte_counts(
        ledger, source_locality_identities=("source", "source")
    )
    assert repeated == once


def test_every_overlapping_adjacent_byte_pair_is_measured():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["representation"]): item["dimensions"]["content"]
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    assert counts[(116, 97)]["count"] == 4
    assert counts[(97, 116)]["count"] == 3
    assert counts[(97, 10)]["count"] == 1


def test_adjacent_pairs_never_cross_ingest_boundaries():
    ledger = _ledger("a\nb\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["representation"]): item["dimensions"]["content"][
            "count"
        ]
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    assert counts == {(97, 10): 1, (98, 10): 1}
    assert (10, 98) not in counts


def test_adjacency_pair_measurement_remains_byte_not_character_based():
    ledger = _ledger("猫\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    counts = {
        tuple(item["assertion_subject"]["representation"])
        for item in event.material["assertions"]
        if item["result"] == "count"
    }

    # UTF-8 bytes e7 8c ab plus the recorded newline. These are adjacent bytes,
    # not a Assertion that any pair is a character.
    assert counts == {(231, 140), (140, 171), (171, 10)}


def test_pair_count_and_recurrence_are_separate_results():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assert event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
    by_pair = {}
    for assertion in event.material["assertions"]:
        representation = assertion["assertion_subject"].get("representation")
        if representation is not None:
            by_pair.setdefault(tuple(representation), []).append(assertion)

    assert [item["result"] for item in by_pair[(116, 97)]] == ["count", "recurrence"]
    assert [item["result"] for item in by_pair[(97, 10)]] == ["count"]
    assert by_pair[(116, 97)][1]["input_support"]["local_assertion_identities"] == [
        by_pair[(116, 97)][0]["dimensions"]["identity"]
    ]
    moved_reference = by_pair[(116, 97)][0]["input_support"]["assertion_references"][0]
    original = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source.identity)
        if item.result == "exact_source_material_set"
    )
    assert moved_reference["assertion_identity"] == original.assertion_identity
    assert moved_reference["recorded_occurrence_identity"] == original.recorded_occurrence_identity
    assert event.material["source_movement_event_identity"] != original.recorded_occurrence_identity
    applicability = input_applicability_of_recorded_adjacent_byte_pair_measurement(
        ledger, event.identity
    )
    assert applicability["dimensions"]["standing"] == "applicable"
    assert applicability["input_assertion_reference"] == event.material["source_assertion_reference"]
    assert applicability["result_boundary"]
    assert applicability["downstream_act"] == "declared adjacent-byte-pair Measurement"
    assert applicability["measurement_locality"] == "measurement"
    assert applicability["input_unknowns"]
    assert applicability["input_limits"]
    assert applicability["conflicts"] == []
    assert applicability["coordinate_treatment"]["support_relation_standing"] == {
        "carried": False,
        "treatment": "not established by Applicability",
    }


def test_recorded_pair_results_replay_the_complete_bounded_source_read():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    read = assertions_of_recorded_adjacent_byte_pair_measurement(
        ledger, event.identity
    )
    assert read
    assert all(item.recorded_occurrence_identity == event.identity for item in read)
    assert {item.representation for item in read if item.representation} == {
        (116, 97),
        (97, 116),
        (97, 10),
    }
    count = next(
        item
        for item in read
        if item.representation == (116, 97) and item.result == "count"
    )
    detached = count.material
    detached["dimensions"]["standing"] = "unsupported"
    assert count.material["dimensions"]["standing"] == "measured"
    assert count.support_assertion_references[0]["recorded_occurrence_identity"] == source.identity
    movement = ledger.get(event.material["source_movement_event_identity"])
    assert movement.material["source_assertion_reference"]["recorded_occurrence_identity"] == source.identity
    assert movement.material["assertion_identity"] == count.support_assertion_references[0]["assertion_identity"]
    assert movement.material["source_locality"] == "byte-measurement"
    assert movement.material["destination_locality"] == "measurement"
    assert movement.material["movement_act_identity"] != movement.material[
        "movement_act_occurrence_identity"
    ]
    act_evidence = ledger.get(movement.material["responsible_act_evidence_identity"])
    assert act_evidence.material["movement_act_identity"] == movement.material[
        "movement_act_identity"
    ]
    assert act_evidence.material["movement_act_occurrence_identity"] == movement.material[
        "movement_act_occurrence_identity"
    ]
    assert "dimensions" not in movement.material


def test_pair_validation_refuses_a_self_consistent_truncated_result_inputs():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    event.material["assertions"] = event.material["assertions"][:-1]
    evidence = ledger.get(event.material["yield_evidence_identity"])
    evidence.material["result"] = {
        name: event.material[name] for name in BYTE_PAIR_RESULT_COORDINATES
    }

    with pytest.raises(ByteMeasurementError, match="recurrence boundary"):
        assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.identity)


@pytest.mark.parametrize(
    "representation",
    (
        [116],
        [116, 256],
        [116, "97"],
        "7461",
        (116, 97),
        [116, 97, 10],
        [True, 97],
    ),
)
def test_pair_validation_requires_one_exact_ordered_representation(representation):
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    assertion = event.material["assertions"][0]
    assertion["assertion_subject"]["representation"] = representation
    assertion["dimensions"]["identity"] = _identity(
        result=assertion["result"],
        subject=assertion["assertion_subject"],
        scope=assertion["assertion_scope"],
        content=assertion["dimensions"]["content"],
    )
    ledger.get(event.material["yield_evidence_identity"]).material["result"] = {
        name: event.material[name] for name in BYTE_PAIR_RESULT_COORDINATES
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair Assertion"):
        assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.identity)


def test_pair_validation_does_not_perform_the_pair_measurement_again(monkeypatch):
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("the pair Measurement occurred again")

    monkeypatch.setattr(
        "seed_runtime.byte_measurement._measure_adjacent_byte_pair_counts_through",
        forbidden,
    )
    monkeypatch.setattr(
        "seed_runtime.byte_measurement._pair_input_applicability", forbidden
    )
    assert assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.identity)


def test_pair_validation_refuses_unsupported_input_applicability():
    ledger = _ledger("tatatata\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    event.material["input_applicability"]["result_boundary"] = "some other use"
    evidence = ledger.get(event.material["yield_evidence_identity"])
    evidence.material["result"] = {
        name: event.material[name] for name in BYTE_PAIR_RESULT_COORDINATES
    }

    with pytest.raises(ByteMeasurementError, match="historical input Applicability"):
        assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.identity)


def test_zero_observed_pairs_is_a_lawful_addressable_result():
    ledger = _ledger("\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert event.material["assertions"] == []
    assert assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.identity) == ()


def test_applicability_identity_is_bound_to_one_exact_downstream_act():
    ledger = _ledger("ta\n")
    source_event = _byte_source(ledger)
    source = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source_event.identity)
        if item.result == "exact_source_material_set"
    )
    first = _pair_input_applicability(
        source,
        downstream_act_identity="pair-act-1",
        applicability_act_identity="applicability-act-1",
        applicability_act_occurrence_identity="applicability-occurrence-1",
        measurement_locality_identity="measurement",
    )
    second = _pair_input_applicability(
        source,
        downstream_act_identity="pair-act-2",
        applicability_act_identity="applicability-act-2",
        applicability_act_occurrence_identity="applicability-occurrence-2",
        measurement_locality_identity="measurement",
    )

    assert first["dimensions"]["identity"] != second["dimensions"]["identity"]
    assert first["responsibility"]
    assert first["responsibility"] != first["assigned_by_responsibility"]
    assert first["downstream_act_identity"] == "pair-act-1"
    assert first["downstream_act_occurrence_identity"] is None


def test_pair_applicability_has_unknown_and_conflicting_outcomes():
    ledger = _ledger("ta\n")
    source_event = _byte_source(ledger)
    source = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, source_event.identity)
        if item.result == "exact_source_material_set"
    )
    carried = source.material
    carried["dimensions"]["authority"] = "unrecognized"
    unknown_source = type(source)(
        assertion_identity=source.assertion_identity,
        recorded_occurrence_identity=source.recorded_occurrence_identity,
        representation=source.representation,
        result=source.result,
        _material_json=json.dumps(carried),
        _support_assertion_refs_json="[]",
    )
    unknown = _pair_input_applicability(
        unknown_source,
        downstream_act_identity="pair-act-unknown-authority",
        applicability_act_identity="applicability-act-unknown",
        applicability_act_occurrence_identity="applicability-occurrence-unknown",
        measurement_locality_identity="measurement",
    )
    conflicting_material = source.material
    conflicting_material["dimensions"]["standing"] = "reported"
    conflicting_source = type(source)(
        assertion_identity=source.assertion_identity,
        recorded_occurrence_identity=source.recorded_occurrence_identity,
        representation=source.representation,
        result=source.result,
        _material_json=json.dumps(conflicting_material),
        _support_assertion_refs_json="[]",
    )
    conflicting = _pair_input_applicability(
        conflicting_source,
        downstream_act_identity="pair-act-conflicting-standing",
        applicability_act_identity="applicability-act-conflicting",
        applicability_act_occurrence_identity="applicability-occurrence-conflicting",
        measurement_locality_identity="measurement",
    )

    assert unknown["dimensions"]["standing"] == "Unknown"
    assert len(unknown["unknowns"]) == 2
    assert conflicting["dimensions"]["standing"] == "conflicting"
    assert len(conflicting["conflicts"]) == 1
    assert conflicting["input_standing"] == "reported"
    assert conflicting["input_assertion_reference"] == source.reference
    assert conflicting["downstream_act_occurrence_identity"] is None


def test_seed_native_measurement_and_result_assertions_keep_distinct_responsibilities():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    result = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    applicability = get_recorded_pair_input_applicability(
        ledger, result.material["input_applicability_event_identity"]
    )

    assert result.material["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    assert applicability["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    assert source.material["responsibility"] != result.material["responsibility"]
    assert source.material["responsible_boundary"] == (
        SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
    )
    for assertion in result.material["assertions"]:
        assert assertion["dimensions"]["responsibility"] != result.material["responsibility"]


def test_seed_native_responsibility_is_earned_from_preserved_occurrences():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    assignment = source.material["responsibility_assignment_evidence"]
    source_set = next(
        assertion
        for assertion in source.material["assertions"]
        if assertion["result"] == "exact_source_material_set"
    )

    assert assignment["responsible_boundary"] == "this Seed"
    assert assignment["source_occurrence_references"] == source_set["dimensions"][
        "content"
    ]["source_material"]
    assert assignment["completeness_boundary"] == source.material[
        "completeness_boundary"
    ]["identity"]
    yield_evidence = ledger.get(source.material["yield_evidence_identity"])
    assert yield_evidence.material["dimensions"]["responsible_boundary"] == (
        "this Seed"
    )


def test_locality_movement_assignment_is_earned_from_the_exact_source():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    pair = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    movement = ledger.get(pair.material["source_movement_event_identity"])
    assignment = movement.material["responsibility_assignment_evidence"]

    assert assignment == {
        "responsible_boundary": "this Seed",
        "standing": "assigned",
        "source_assertion_reference": movement.material["source_assertion_reference"],
        "source_locality": "byte-measurement",
        "destination_locality": "measurement",
        "determination": "the exact preserved Assertion moved between Localities",
    }


def test_pair_act_identity_is_not_its_occurrence_identity():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    result = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )

    assert result.material["downstream_act_identity"] != result.material["act_occurrence_identity"]
    assert result.material["input_applicability"]["downstream_act_identity"] == (
        result.material["downstream_act_identity"]
    )
    assert result.material["input_applicability"]["downstream_act_occurrence_identity"] is None


def test_pair_validation_refuses_more_carrying_occurrences_than_total_pairs():
    ledger = _ledger("ta\n")
    source = _byte_source(ledger)
    event = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_identity=source.identity,
        recording_locality_identity="measurement",
    )
    count = next(
        assertion
        for assertion in event.material["assertions"]
        if assertion["assertion_subject"]["representation"] == [116, 97]
    )
    count["dimensions"]["content"] = {
        "input_count": 2,
        "occurrences_carrying": 2,
        "count": 1,
    }
    count["dimensions"]["identity"] = _identity(
        result="count",
        subject=count["assertion_subject"],
        scope=count["assertion_scope"],
        content=count["dimensions"]["content"],
    )
    ledger.get(event.material["yield_evidence_identity"]).material["result"] = {
        name: event.material[name] for name in BYTE_PAIR_RESULT_COORDINATES
    }

    with pytest.raises(ByteMeasurementError, match="unlawful pair count"):
        assertions_of_recorded_adjacent_byte_pair_measurement(ledger, event.identity)
