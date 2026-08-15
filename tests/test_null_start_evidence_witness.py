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
from seed_runtime.yield_evidence import read_yield_edge_requirements
from tests.binary_input import binary_input


E1 = "hello"
E2 = "learn proficient english language"
E3 = "# Nouns\n\nA noun is a word.\n\n# Verbs\n\nA verb is a word."


def run_null_start() -> list:
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_id="s",
        input_stream=binary_input("\n".join([E1, E2, E3]) + "\n"),
        output_stream=StringIO(),
    )
    return ledger.list()


def represent_null_start_evidence() -> str:
    lines = []
    for position, event in enumerate(run_null_start(), start=1):
        lines.append(f"[{position}] {event.kind}  {event.id}")
        for key, value in sorted(event.payload.items()):
            lines.append(f"      {key} = {json.dumps(value, default=str)}")
    return "\n".join(lines) + "\n"


@pytest.fixture(scope="module")
def ledger() -> EventLedger:
    result = EventLedger()
    run_persistent_operator_console(
        ledger=result,
        locality_id="s",
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
    assert all(event.payload["source_role"] == "operator" for event in ingests)


def test_each_ingest_preserves_exact_bytes(ledger):
    exact = [ingested_material_bytes(event) for event in _ingests(ledger)]

    assert exact[0] == (E1 + "\n").encode()
    assert exact[1] == (E2 + "\n").encode()
    assert (E3 + "\n").encode() not in exact


def test_each_ingest_binds_its_exact_act_and_result_evidence(ledger):
    for ingest in _ingests(ledger):
        assert all(
            read_yield_edge_requirements(
                ledger,
                recorded_result_event_id=ingest.id,
                result_evidence_event_id=ingest.payload["yield_evidence_id"],
                responsible_act_evidence_event_id=ingest.payload[
                    "responsible_act_evidence_id"
                ],
            ).values()
        )


def test_ingest_does_not_assert_a_represented_relation(ledger):
    for ingest in _ingests(ledger):
        assert "represented_material" not in ingest.payload
        assert ingest.payload["provenance_occurrence_references"] == []
        assert "represented relation Unknown" in ingest.payload["dimensions"][
            "evidence_scope"
        ]


def test_ingest_evidence_is_inspectable():
    represented = represent_null_start_evidence()

    assert MATERIAL_INGEST_OCCURRED_KIND in represented
    assert "exact_bytes_hex" in represented
    assert "responsible_act_evidence_id" in represented
    assert "yield_evidence_id" in represented


if __name__ == "__main__":  # pragma: no cover
    print(represent_null_start_evidence())
