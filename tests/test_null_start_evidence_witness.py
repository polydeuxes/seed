"""Exact material acquisition Evidence from an empty ledger."""

from __future__ import annotations

from io import StringIO
import json

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_acquisition import (
    acquired_material_bytes,
    iter_exact_material_acquisition_results,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation
from tests.binary_input import binary_input


E1 = "hello"
E2 = "learn proficient english language"
E3 = "# Nouns\n\nA noun is a word.\n\n# Verbs\n\nA verb is a word."


def run_null_start() -> list:
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input("\n".join([E1, E2, E3]) + "\n"),
        output_stream=StringIO(),
    )
    return ledger.list()


def represent_null_start_evidence(events=None) -> str:
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
    run_persistent_operator_console(
        ledger=result,
        locality_identity="s",
        input_stream=binary_input("\n".join([E1, E2, E3]) + "\n"),
        output_stream=StringIO(),
    )
    return result


def _acquisition_results(ledger: EventLedger):
    return list(iter_exact_material_acquisition_results(ledger, "s"))


def test_one_acquisition_result_occurs_for_each_delivered_line(ledger):
    acquisition_results = _acquisition_results(ledger)

    assert len(acquisition_results) == 2 + len(E3.split("\n"))


def test_each_material_acquisition_carries_the_operator_role(ledger):
    acquisition_results = _acquisition_results(ledger)

    assert all(event.material["source_role"] == "this operator" for event in acquisition_results)


def test_each_material_acquisition_preserves_exact_bytes(ledger):
    exact = [acquired_material_bytes(event) for event in _acquisition_results(ledger)]

    assert exact[0] == (E1 + "\n").encode()
    assert exact[1] == (E2 + "\n").encode()
    assert (E3 + "\n").encode() not in exact


def test_each_material_acquisition_binds_its_exact_act_and_evidence_of_yield_relation(ledger):
    for acquisition_result in _acquisition_results(ledger):
        assert all(
            read_requirements_of_yield_relation(
                ledger,
                recorded_result_event_identity=acquisition_result.identity,
                evidence_of_yield_relation_event_identity=acquisition_result.material["evidence_of_yield_relation_identity"],
                responsible_act_evidence_event_identity=acquisition_result.material[
                    "responsible_act_evidence_identity"
                ],
            ).values()
        )


def test_material_acquisition_does_not_assert_a_represented_relation(ledger):
    for acquisition_result in _acquisition_results(ledger):
        assert "represented_material" not in acquisition_result.material
        assert acquisition_result.material["unknown"] == [
            "represented_relation",
            "source_relation",
        ]
        assert acquisition_result.material["provenance_occurrence_references"] == []
        assert "exact material result" in acquisition_result.material["dimensions"][
            "evidence_scope"
        ]


def test_material_acquisition_evidence_is_inspectable(ledger):
    represented = represent_null_start_evidence(ledger.list())

    assert "operator.material.acquire_recorded" in represented
    assert "responsible_act_evidence_identity" in represented
    assert "evidence_of_yield_relation_identity" in represented


def test_material_acquisition_exact_material_is_inspectable(ledger):
    acquisition_results = _acquisition_results(ledger)

    assert all(type(event.exact_material) is bytes for event in acquisition_results)




if __name__ == "__main__":  # pragma: no cover
    print(represent_null_start_evidence())
