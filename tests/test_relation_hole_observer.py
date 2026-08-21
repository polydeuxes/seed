"""Exact carriage of an occurrence pair by a recorded relation.

The observer asks one question about two occurrences joined by a reference:
does some recorded relation carry both of them as its first and second
subjects?  Where the reference happens to sit is a separate reading and never
answers that question.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.observe_relation_holes import (  # noqa: E402
    _recorded_relation_for_pair,
    _recorded_relations,
    _relation_subject_positions,
    _subject_occurrences,
)


def _event(identity: str, material: dict) -> dict:
    return {"identity": identity, "kind": "test.recorded", "material": material}


def _carriage(events: list[dict], source: str, destination: str):
    known = {event["identity"] for event in events}
    population = _recorded_relations(events, known)
    first_index, second_index = _relation_subject_positions(population)
    destination_index = [
        index
        for index, event in enumerate(events)
        if event["identity"] == destination
    ][0]
    return _recorded_relation_for_pair(
        source,
        destination,
        destination_index,
        population,
        first_index,
        second_index,
    )


def _relation(first, second, relation="locality"):
    return {
        "first_subject": first,
        "second_subject": second,
        "relation": relation,
    }


def test_a_subject_carries_the_occurrence_recorded_within_it():
    known = {"evt_1", "evt_2"}
    assert _subject_occurrences("evt_1", known) == {"evt_1"}
    assert _subject_occurrences(
        {"recorded_occurrence_identity": "evt_1", "coordinate": "exact_material"},
        known,
    ) == {"evt_1"}


def test_a_string_that_is_no_recorded_occurrence_is_not_collected():
    assert _subject_occurrences("this Seed", {"evt_1"}) == set()
    assert _subject_occurrences({"locality": "this Seed"}, {"evt_1"}) == set()


def test_a_relation_carrying_both_occurrences_in_order_carries_the_pair():
    events = [
        _event("evt_1", {}),
        _event("evt_2", {"reference": "evt_1", "pair": _relation("evt_1", "evt_2")}),
    ]
    carriage, records, within_one = _carriage(events, "evt_1", "evt_2")
    assert carriage == "first_and_second_subject"
    assert within_one is False
    assert [record["subject_order"] for record in records] == ["first_and_second"]


def test_the_reverse_subject_order_is_recorded_as_itself():
    events = [
        _event("evt_1", {}),
        _event("evt_2", {"reference": "evt_1", "pair": _relation("evt_2", "evt_1")}),
    ]
    carriage, records, _within = _carriage(events, "evt_1", "evt_2")
    assert carriage == "second_and_first_subject"
    assert [record["subject_order"] for record in records] == ["second_and_first"]


def test_a_relation_recorded_in_a_third_occurrence_still_carries_the_pair():
    """The reference and the relation need not share an occurrence.

    This is the carriage the earlier reading could not see, because it only
    looked inside the occurrence holding the reference.
    """

    events = [
        _event("evt_1", {}),
        _event("evt_2", {"reference": "evt_1"}),
        _event("evt_3", {"pair": _relation("evt_1", "evt_2")}),
    ]
    carriage, records, _within = _carriage(events, "evt_1", "evt_2")
    assert carriage == "first_and_second_subject"
    assert records[0]["recorded_by_occurrence"] == "evt_3"
    assert records[0]["recorded_position"] == "later_recorded_occurrence"


def test_a_reference_inside_a_relation_coordinate_carries_no_pair():
    """Sitting within relation material is not being one of its subjects."""

    events = [
        _event("evt_1", {}),
        _event(
            "evt_2",
            {
                "pair": {
                    "first_subject": {"provenance": "evt_1"},
                    "second_subject": "this Seed",
                    "relation": "locality",
                }
            },
        ),
    ]
    carriage, _records, _within = _carriage(events, "evt_1", "evt_2")
    assert carriage == "no_recorded_relation"


def test_two_occurrences_inside_one_subject_carry_no_pair():
    """One compound subject is one subject, whatever it carries."""

    events = [
        _event("evt_1", {}),
        _event(
            "evt_2",
            {
                "reference": "evt_1",
                "pair": {
                    "first_subject": {"from": "evt_1", "through": "evt_2"},
                    "second_subject": "this Seed",
                    "relation": "locality",
                },
            },
        ),
    ]
    carriage, _records, within_one = _carriage(events, "evt_1", "evt_2")
    assert carriage == "no_recorded_relation"
    assert within_one is True


def test_an_unrelated_recorded_relation_carries_no_pair():
    events = [
        _event("evt_1", {}),
        _event("evt_2", {"reference": "evt_1"}),
        _event("evt_3", {"pair": _relation("evt_1", "evt_9")}),
    ]
    carriage, records, _within = _carriage(events, "evt_1", "evt_2")
    assert carriage == "no_recorded_relation"
    assert records == []


PYTEST_ADMISSION = (
    test_a_subject_carries_the_occurrence_recorded_within_it,
    test_a_string_that_is_no_recorded_occurrence_is_not_collected,
    test_a_relation_carrying_both_occurrences_in_order_carries_the_pair,
    test_the_reverse_subject_order_is_recorded_as_itself,
    test_a_relation_recorded_in_a_third_occurrence_still_carries_the_pair,
    test_a_reference_inside_a_relation_coordinate_carries_no_pair,
    test_two_occurrences_inside_one_subject_carry_no_pair,
    test_an_unrelated_recorded_relation_carries_no_pair,
)
