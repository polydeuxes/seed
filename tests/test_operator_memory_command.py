from __future__ import annotations

from io import BytesIO

import pytest


from seed_runtime.events import EventLedger
from seed_runtime.material_acquisition import read_exact_material_acquisition_result
from seed_runtime.operator_command import (
    AddressedOperatorCommand,
    OperatorCommandFrame,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_memory_command import (
    OperatorMemoryRequest,
    request_operator_memory,
)
from seed_runtime.operator_standing_continuation import (
    STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
    get_recorded_standing_locality_continuation,
)


def _command(exact_bytes: bytes, arguments: bytes = b""):
    return AddressedOperatorCommand(
        command_identity="command",
        locality_identity="source",
        addressed_at_representation_event_identity="representation",
        frame=OperatorCommandFrame(
            exact_bytes=exact_bytes,
            name=b"memory",
            arguments=arguments,
        ),
    )


@pytest.mark.parametrize("exact", (b"/memory", b"/memory\n", b"/memory\r\n"))
def test_memory_request_is_only_exact_argument_free_control(exact):
    assert request_operator_memory(_command(exact)) == OperatorMemoryRequest()


@pytest.mark.parametrize(
    ("exact", "arguments"),
    (
        (b"/memory important\n", b"important"),
        (b"/memory material\n", b"material"),
        (b"/memory \n", b""),
        (b"/memory\t\n", b""),
    ),
)
def test_memory_request_refuses_every_payload(exact, arguments):
    with pytest.raises(ValueError, match="accepts no material"):
        request_operator_memory(_command(exact, arguments))


def test_console_memory_creates_and_switches_to_one_fresh_destination():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"before\n/memory\nafter\n"),
    )
    acts = [
        event
        for event in ledger.list()
        if event.kind == STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT
    ]
    results = [
        event
        for event in ledger.list()
        if event.kind == STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    ]

    assert len(acts) == len(results) == 1
    act = acts[0]
    result = results[0]
    assert act.locality_identity == result.locality_identity != "source"
    assert act.exact_material is None
    recorded = get_recorded_standing_locality_continuation(
        ledger, result.identity
    )
    addressed = ledger.get(
        recorded["source_standing_reference"][
            "addressed_representation_event_identity"
        ]
    )
    assert addressed.locality_identity == "source"
    assert recorded["source_standing_reference"][
        "source_standing_through_event_occurrence_identity"
    ] == addressed.material["locality_standing_through_event_occurrence_identity"]
    acquisition_results = []
    for event in ledger.list():
        try:
            acquisition_results.append(
                read_exact_material_acquisition_result(ledger, event.identity)
            )
        except (TypeError, ValueError):
            pass
    assert [event.locality_identity for event in acquisition_results] == [
        "source",
        "source",
        result.locality_identity,
    ]
    assert [event.exact_material for event in acquisition_results] == [
        b"before\n",
        b"/memory\n",
        b"after\n",
    ]
    destination_representations = [
        event
        for event in ledger.list_locality(result.locality_identity)
        if event.kind == "operator.representation.recorded"
    ]
    assignment_identity = act.material["responsibility_assignment_reference"][
        "recorded_occurrence_identity"
    ]
    assert [
        event.material["locality_standing_through_event_occurrence_identity"]
        for event in destination_representations[:3]
    ] == [assignment_identity, act.identity, result.identity]


def test_memory_does_not_change_checkpoint_species_or_copy_source_occurrences():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="source",
        input_stream=BytesIO(b"one\ntwo\n/memory\n"),
    )
    result = next(
        event
        for event in ledger.list()
        if event.kind == STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    )
    destination = ledger.list_locality(result.locality_identity)
    source_identities = {
        event.identity for event in ledger.list_locality("source")
    }
    recorded = get_recorded_standing_locality_continuation(
        ledger, result.identity
    )

    assert not [
        event
        for event in ledger.list()
        if event.kind == "operator.addressed_representation.locality_recorded"
    ]
    assert {
        recorded["source_standing_reference"][
            "addressed_representation_event_identity"
        ],
        recorded["source_standing_reference"][
            "source_standing_through_event_occurrence_identity"
        ],
    } <= source_identities
    for event in destination:
        with pytest.raises(ValueError):
            read_exact_material_acquisition_result(ledger, event.identity)


PYTEST_ADMISSION = (
    test_memory_request_is_only_exact_argument_free_control,
    test_memory_request_refuses_every_payload,
    test_console_memory_creates_and_switches_to_one_fresh_destination,
    test_memory_does_not_change_checkpoint_species_or_copy_source_occurrences,
)
