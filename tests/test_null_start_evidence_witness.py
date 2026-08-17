"""Exact Ingest Evidence from an empty ledger."""

from __future__ import annotations

from io import StringIO
import json

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingested_material_bytes,
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


def represent_null_start_evidence() -> str:
    lines = []
    for position, event in enumerate(run_null_start(), start=1):
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


def _ingests(ledger: EventLedger):
    return [
        event
        for event in ledger.list_locality("s")
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ]


def test_one_ingest_occurs_for_each_delivered_line(ledger):
    ingests = _ingests(ledger)

    assert len(ingests) == 2 + len(E3.split("\n"))


def test_each_ingest_carries_the_operator_role(ledger):
    ingests = _ingests(ledger)

    assert all(event.material["source_role"] == "operator" for event in ingests)


def test_each_ingest_preserves_exact_bytes(ledger):
    exact = [ingested_material_bytes(event) for event in _ingests(ledger)]

    assert exact[0] == (E1 + "\n").encode()
    assert exact[1] == (E2 + "\n").encode()
    assert (E3 + "\n").encode() not in exact


def test_each_ingest_binds_its_exact_act_and_evidence_of_yield_relation(ledger):
    for ingest in _ingests(ledger):
        assert all(
            read_requirements_of_yield_relation(
                ledger,
                recorded_result_event_identity=ingest.identity,
                evidence_of_yield_relation_event_identity=ingest.material["evidence_of_yield_relation_identity"],
                responsible_act_evidence_event_identity=ingest.material[
                    "responsible_act_evidence_identity"
                ],
            ).values()
        )


def test_ingest_does_not_assert_a_represented_relation(ledger):
    for ingest in _ingests(ledger):
        assert "represented_material" not in ingest.material
        assert ingest.material["unknown"] == [
            "represented_relation",
            "source_relation",
        ]
        (provenance_reference,) = ingest.material[
            "provenance_occurrence_references"
        ]
        supplied_occurrence = ledger.get(provenance_reference)
        assert supplied_occurrence is not None
        assert supplied_occurrence.locality_identity == ingest.locality_identity
        assert supplied_occurrence.exact_material == ingest.exact_material
        assert "represented relation Unknown" in ingest.material["dimensions"][
            "evidence_scope"
        ]


def test_ingest_evidence_is_inspectable():
    represented = represent_null_start_evidence()

    assert MATERIAL_INGEST_OCCURRED_KIND in represented
    assert "responsible_act_evidence_identity" in represented
    assert "evidence_of_yield_relation_identity" in represented


def test_ingest_exact_material_is_inspectable():
    ingests = [
        event
        for event in run_null_start()
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ]

    assert all(type(event.exact_material) is bytes for event in ingests)


FIDELITY_SUBJECTS = {
    "operator_material_ingest_occurrence": (
        test_one_ingest_occurs_for_each_delivered_line,
    ),
    "operator_material_ingest_role": (test_each_ingest_carries_the_operator_role,),
    "material_ingest_exact_material": (test_each_ingest_preserves_exact_bytes,),
    "material_ingest_act_yield_relation": (
        test_each_ingest_binds_its_exact_act_and_evidence_of_yield_relation,
    ),
    "material_ingest_representation_distinction": (
        test_ingest_does_not_assert_a_represented_relation,
    ),
    "material_ingest_evidence_visibility": (test_ingest_evidence_is_inspectable,),
    "material_ingest_exact_material_visibility": (
        test_ingest_exact_material_is_inspectable,
    ),
}


if __name__ == "__main__":  # pragma: no cover
    print(represent_null_start_evidence())
