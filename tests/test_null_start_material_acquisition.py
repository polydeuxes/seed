"""Exact material acquisition from an empty ledger."""

from __future__ import annotations

import json

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_source import (
    exact_material_result_bytes,
    iter_exact_material_results,
)
from seed_runtime.yield_relation import read_requirements_of_yield_relation
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)


E1 = "hello"
E2 = "learn proficient english language"
E3 = "# Nouns\n\nA noun is a word.\n\n# Verbs\n\nA verb is a word."


def run_null_start() -> list:
    ledger = EventLedger()
    _record_material(ledger)
    return ledger.list()


def exact_null_start_occurrences(events=None) -> str:
    lines = []
    for position, event in enumerate(
        run_null_start() if events is None else events,
        start=1,
    ):
        lines.append(f"[{position}] {event.kind}  {event.identity}")
        for key, value in sorted(event.material.items()):
            lines.append(f"      {key} = {json.dumps(value, default=str)}")
    return "\n".join(lines) + "\n"


@pytest.fixture(scope="module")
def ledger() -> EventLedger:
    result = EventLedger()
    _record_material(result)
    return result


def _record_material(ledger: EventLedger) -> None:
    material = "\n".join([E1, E2, E3]) + "\n"
    for position, line in enumerate(material.splitlines(keepends=True)):
        record_operator_material_occurrence(
            ledger,
            exact=line.encode(),
            locality_identity="s",
            source_boundary=f"operator boundary {position}",
        )


def _acquisition_results(ledger: EventLedger):
    return list(iter_exact_material_results(ledger, "s"))


def test_one_acquisition_result_occurs_for_each_delivered_line(ledger):
    acquisition_results = _acquisition_results(ledger)

    assert len(acquisition_results) == 2 + len(E3.split("\n"))


def test_each_material_acquisition_carries_the_operator_role(ledger):
    acquisition_results = _acquisition_results(ledger)

    assert all(event.material["source_role"] == "this operator" for event in acquisition_results)


def test_each_material_acquisition_preserves_exact_bytes(ledger):
    exact = [exact_material_result_bytes(event) for event in _acquisition_results(ledger)]

    assert exact[0] == (E1 + "\n").encode()
    assert exact[1] == (E2 + "\n").encode()
    assert (E3 + "\n").encode() not in exact


def test_each_material_acquisition_binds_its_exact_act_and_yield_relation(ledger):
    for acquisition_result in _acquisition_results(ledger):
        assert all(
            read_requirements_of_yield_relation(
                ledger,
                recorded_result_event_identity=acquisition_result.identity,
                yield_relation_event_identity=acquisition_result.material["yield_relation_identity"],
                act_occurrence_event_identity=acquisition_result.material[
                    "act_occurrence_event_identity"
                ],
            ).values()
        )


def test_material_acquisition_does_not_assert_a_source_relation(ledger):
    for acquisition_result in _acquisition_results(ledger):
        assert acquisition_result.material["unknown"] == ["source_relation"]
        assert acquisition_result.material["provenance_occurrence_references"] == []


def test_material_acquisition_occurrences_are_exactly_addressable(ledger):
    occurrences = exact_null_start_occurrences(ledger.list())

    assert "operator.material.source_recorded" in occurrences
    assert "act_occurrence_identity" in occurrences
    assert "yield_relation_identity" in occurrences


def test_material_acquisition_exact_material_is_inspectable(ledger):
    acquisition_results = _acquisition_results(ledger)

    assert all(type(event.exact_material) is bytes for event in acquisition_results)




if __name__ == "__main__":  # pragma: no cover
    print(exact_null_start_occurrences())
