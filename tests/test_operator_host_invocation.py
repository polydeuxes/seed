from __future__ import annotations

from io import BytesIO, StringIO

import pytest

from seed_runtime.byte_measurement import BYTE_MEASUREMENT_RECORDED_KIND
from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import (
    MATERIAL_INGEST_OCCURRED_KIND,
    ingest_material,
    ingested_material_bytes,
)
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RECORDED_KIND,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    read_operator_locality_standing,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedInvocationMaterial,
    SuppliedMaterialOccurrence,
    ingest_supplied_invocation_material,
)
from seed_runtime.yield_evidence import read_yield_relation_requirements


def _supplied(
    *, output=b"\x00\xffout", error=b"same", end=b""
) -> SuppliedInvocationMaterial:
    return SuppliedInvocationMaterial(
        output_material=SuppliedMaterialOccurrence(output, "provider:0"),
        error_material=SuppliedMaterialOccurrence(error, "provider:1"),
        end_material=SuppliedMaterialOccurrence(end, "provider:2"),
    )


def _ingests(ledger):
    return [
        event
        for event in ledger.list_locality("locality")
        if event.kind == MATERIAL_INGEST_OCCURRED_KIND
    ]


def _command(ledger, *, locality="locality", exact=b"!ls\n"):
    return ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=exact,
        source_role="operator",
        source_boundary="operator boundary",
    )


def test_host_provider_receives_an_acquired_exact_command_before_it_occurs():
    ledger = EventLedger()
    seen = []
    raw_output = BytesIO()

    def provider(exact_command):
        seen.append(exact_command)
        assert [ingested_material_bytes(event) for event in _ingests(ledger)] == [
            b"!ls \xff\x00\n"
        ]
        assert len(
            [
                event
                for event in ledger.list_locality("locality")
                if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
            ]
        ) == 1
        assert len(
            [
                event
                for event in ledger.list_locality("locality")
                if event.kind == OCCURRENCE_POSITION_RECORDED_KIND
            ]
        ) == 1
        assert len(
            [
                event
                for event in ledger.list_locality("locality")
                if event.kind == "operator.representation.recorded"
            ]
        ) == 2
        return _supplied()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls \xff\x00\n"),
        output_stream=StringIO(),
        raw_output_stream=raw_output,
        host_invocation_provider=provider,
    )

    assert seen == [b"!ls \xff\x00\n"]
    assert raw_output.getvalue() == b"\x00\xffoutsame"
    ingests = _ingests(ledger)
    assert [ingested_material_bytes(event) for event in ingests] == [
        b"!ls \xff\x00\n",
        b"\x00\xffout",
        b"same",
        b"",
    ]
    assert [event.material["source_role"] for event in ingests] == [
        "operator",
        "system",
        "system",
        "system",
    ]
    assert [event.material["source_boundary"] for event in ingests[1:]] == [
        "provider:0",
        "provider:1",
        "provider:2",
    ]
    assert [
        event.material["provenance_occurrence_references"]
        for event in ingests[1:]
    ] == [[ingests[0].identity]] * 3
    assert all(
        "the asserted source relation remains Unknown" in event.material["unknowns"]
        for event in ingests[1:]
    )
    assert len({event.material["result_identity"] for event in ingests}) == 4
    assert len(
        [
            event
            for event in ledger.list_locality("locality")
            if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        ]
    ) == 2
    assert len(
        [
            event
            for event in ledger.list_locality("locality")
            if event.kind == "operator.representation.emitted"
        ]
    ) == 2
    assert len(
        [
            event
            for event in ledger.list_locality("locality")
            if event.kind == OCCURRENCE_POSITION_RECORDED_KIND
        ]
    ) == 2
    standing = read_operator_locality_standing(
        ledger, locality_identity="locality"
    )
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in standing["ingest_occurrences"]
    ] == [event.identity for event in ingests]


def test_provider_death_leaves_the_complete_command_acquisition():
    ledger = EventLedger()

    def die(_exact_command):
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!cat path\n"),
            output_stream=StringIO(),
            raw_output_stream=BytesIO(),
            host_invocation_provider=die,
        )

    assert [ingested_material_bytes(event) for event in _ingests(ledger)] == [
        b"!cat path\n"
    ]
    assert len(
        [
            event
            for event in ledger.list_locality("locality")
            if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        ]
    ) == 1
    representations = [
        event
        for event in ledger.list_locality("locality")
        if event.kind == "operator.representation.recorded"
    ]
    assert len(representations) == 2
    assert representations[-1].material[
        "locality_standing_as_of_event_identity"
    ] is not None


def test_missing_supplied_result_is_refused_after_command_acquisition():
    ledger = EventLedger()

    with pytest.raises(TypeError, match="exact supplied material required"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!ls\n"),
            output_stream=StringIO(),
            raw_output_stream=BytesIO(),
            host_invocation_provider=lambda _exact: None,
        )

    assert [ingested_material_bytes(event) for event in _ingests(ledger)] == [
        b"!ls\n"
    ]


def test_equal_empty_supplied_material_remains_three_exact_occurrences():
    ledger = EventLedger()
    command = _command(ledger)
    events = ingest_supplied_invocation_material(
        ledger,
        locality_identity="locality",
        command_occurrence_reference=command.identity,
        supplied=_supplied(output=b"", error=b"", end=b""),
    )

    assert len(events) == 3
    assert len({event.identity for event in events}) == 3
    assert [ingested_material_bytes(event) for event in events] == [b"", b"", b""]


def test_host_provider_requires_an_exact_output_boundary():
    with pytest.raises(ValueError, match="exact output boundary required"):
        run_persistent_operator_console(
            ledger=EventLedger(),
            locality_identity="locality",
            input_stream=BytesIO(b""),
            output_stream=StringIO(),
            host_invocation_provider=lambda _exact: _supplied(),
        )


def test_supplied_boundaries_and_carrier_require_exact_types():
    class OtherOccurrence(SuppliedMaterialOccurrence):
        pass

    with pytest.raises(ValueError, match="distinct source boundary required"):
        SuppliedInvocationMaterial(
            output_material=SuppliedMaterialOccurrence(b"", "same"),
            error_material=SuppliedMaterialOccurrence(b"", "same"),
            end_material=SuppliedMaterialOccurrence(b"", "end"),
        )
    with pytest.raises(TypeError, match="exact supplied material required"):
        SuppliedInvocationMaterial(
            output_material=OtherOccurrence(b"", "output"),
            error_material=SuppliedMaterialOccurrence(b"", "error"),
            end_material=SuppliedMaterialOccurrence(b"", "end"),
        )

    class OtherMaterial(SuppliedInvocationMaterial):
        pass

    ledger = EventLedger()
    command = _command(ledger)
    with pytest.raises(TypeError, match="exact supplied material required"):
        ingest_supplied_invocation_material(
            ledger,
            locality_identity="locality",
            command_occurrence_reference=command.identity,
            supplied=OtherMaterial(
                output_material=SuppliedMaterialOccurrence(b"", "output"),
                error_material=SuppliedMaterialOccurrence(b"", "error"),
                end_material=SuppliedMaterialOccurrence(b"", "end"),
            ),
        )


def test_supplied_yield_cannot_be_replaced_by_another_occurrence():
    ledger = EventLedger()
    command = _command(ledger)
    output, error, _end = ingest_supplied_invocation_material(
        ledger,
        locality_identity="locality",
        command_occurrence_reference=command.identity,
        supplied=_supplied(),
    )

    exact = read_yield_relation_requirements(
        ledger,
        recorded_result_event_identity=output.identity,
        result_evidence_event_identity=output.material["yield_evidence_identity"],
        responsible_act_evidence_event_identity=output.material[
            "responsible_act_evidence_identity"
        ],
    )
    substituted = read_yield_relation_requirements(
        ledger,
        recorded_result_event_identity=output.identity,
        result_evidence_event_identity=error.material["yield_evidence_identity"],
        responsible_act_evidence_event_identity=output.material[
            "responsible_act_evidence_identity"
        ],
    )

    assert all(exact.values())
    assert not all(substituted.values())

    another_command = _command(ledger, exact=b"!cat other\n")
    output.material["provenance_occurrence_references"] = [
        another_command.identity
    ]
    crossed = read_yield_relation_requirements(
        ledger,
        recorded_result_event_identity=output.identity,
        result_evidence_event_identity=output.material["yield_evidence_identity"],
        responsible_act_evidence_event_identity=output.material[
            "responsible_act_evidence_identity"
        ],
    )
    assert not all(crossed.values())


def test_supplied_result_refuses_missing_crossed_or_corrupted_command():
    ledger = EventLedger()
    other_locality = _command(ledger, locality="other")

    for reference in ("missing", other_locality.identity):
        with pytest.raises(ValueError, match="exact operator occurrence required"):
            ingest_supplied_invocation_material(
                ledger,
                locality_identity="locality",
                command_occurrence_reference=reference,
                supplied=_supplied(),
            )

    command = _command(ledger)
    command.material["source_role"] = "system"
    with pytest.raises(ValueError, match="exact operator occurrence required"):
        ingest_supplied_invocation_material(
            ledger,
            locality_identity="locality",
            command_occurrence_reference=command.identity,
            supplied=_supplied(),
        )
