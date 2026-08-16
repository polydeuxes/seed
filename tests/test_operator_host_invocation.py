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
from seed_runtime.operator_material_acquisition import (
    OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedSystemMaterialOccurrence,
    ingest_supplied_invocation_occurrence,
)
from seed_runtime.yield_evidence import read_yield_relation_requirements


def _supplied(
    *, output=b"\x00\xffout", error=b"same", end=b""
) -> tuple[SuppliedSystemMaterialOccurrence, ...]:
    return (
        SuppliedSystemMaterialOccurrence(output, "provider:0", True),
        SuppliedSystemMaterialOccurrence(error, "provider:1", True),
        SuppliedSystemMaterialOccurrence(end, "provider:2", False),
    )


def _provider(*occurrences):
    def provide(_exact_command, supply):
        for occurrence in occurrences:
            supply(occurrence)

    return provide


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


def _represented_boundary_kinds(ledger):
    represented = []
    for event in ledger.list_locality("locality"):
        if event.kind != "operator.representation.recorded":
            continue
        standing_boundary = event.material[
            "locality_standing_as_of_event_identity"
        ]
        source_reference = event.material["source_occurrence_reference"]
        represented.append(
            (
                (
                    None
                    if standing_boundary is None
                    else ledger.get(standing_boundary).kind
                ),
                (
                    None
                    if source_reference is None
                    else ledger.get(source_reference).kind
                ),
            )
        )
    return tuple(represented)


_COMPLETE_COMMAND_REPRESENTED_BOUNDARIES = (
    (None, None),
    (
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
    ),
    (OCCURRENCE_POSITION_RECORDED_KIND, None),
)


def test_host_provider_receives_an_acquired_exact_command_before_it_occurs():
    ledger = EventLedger()
    seen = []
    raw_output = BytesIO()

    def provider(exact_command, supply):
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
        assert (
            _represented_boundary_kinds(ledger)
            == _COMPLETE_COMMAND_REPRESENTED_BOUNDARIES
        )
        for occurrence in _supplied():
            supply(occurrence)

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls \xff\x00\n"),
        output_stream=StringIO(),
        raw_output_stream=raw_output,
        operator_invocation_provider=provider,
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
        event.material["unknowns"] == ["represented_relation", "source_relation"]
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


def test_system_material_is_durable_and_emitted_before_the_provider_resumes():
    ledger = EventLedger()
    raw_output = BytesIO()
    observed = []

    def provider(_exact_command, supply):
        for occurrence in (
            SuppliedSystemMaterialOccurrence(
                b"lower-0", "provider:output:0", True
            ),
            SuppliedSystemMaterialOccurrence(
                b"lower-1", "provider:output:1", True
            ),
            SuppliedSystemMaterialOccurrence(
                b"", "provider:completion", False
            ),
        ):
            supply(occurrence)
            observed.append(
                (
                    raw_output.getvalue(),
                    tuple(event.exact_material for event in _ingests(ledger)),
                )
            )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls\n"),
        output_stream=StringIO(),
        raw_output_stream=raw_output,
        operator_invocation_provider=provider,
    )

    assert observed == [
        (b"lower-0", (b"!ls\n", b"lower-0")),
        (b"lower-0lower-1", (b"!ls\n", b"lower-0", b"lower-1")),
        (
            b"lower-0lower-1",
            (b"!ls\n", b"lower-0", b"lower-1", b""),
        ),
    ]


def test_crossed_system_boundary_is_refused_before_a_second_ingest_or_egress():
    ledger = EventLedger()
    raw_output = BytesIO()

    def provider(_exact_command, supply):
        supply(SuppliedSystemMaterialOccurrence(b"first", "same", True))
        supply(SuppliedSystemMaterialOccurrence(b"second", "same", True))

    with pytest.raises(ValueError, match="distinct source boundary required"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!ls\n"),
            output_stream=StringIO(),
            raw_output_stream=raw_output,
            operator_invocation_provider=provider,
        )

    assert [event.exact_material for event in _ingests(ledger)] == [
        b"!ls\n",
        b"first",
    ]
    assert raw_output.getvalue() == b"first"


def test_provider_death_leaves_the_complete_command_acquisition():
    ledger = EventLedger()

    def die(_exact_command, _supply):
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!cat path\n"),
            output_stream=StringIO(),
            raw_output_stream=BytesIO(),
            operator_invocation_provider=die,
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
    assert (
        _represented_boundary_kinds(ledger)
        == _COMPLETE_COMMAND_REPRESENTED_BOUNDARIES
    )


def test_provider_death_preserves_each_already_supplied_system_occurrence():
    ledger = EventLedger()
    raw_output = BytesIO()

    def die(_exact_command, supply):
        supply(
            SuppliedSystemMaterialOccurrence(
                b"partial", "provider:output:0", True
            )
        )
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!cat path\n"),
            output_stream=StringIO(),
            raw_output_stream=raw_output,
            operator_invocation_provider=die,
        )

    assert [event.exact_material for event in _ingests(ledger)] == [
        b"!cat path\n",
        b"partial",
    ]
    assert raw_output.getvalue() == b"partial"


def test_provider_declares_exact_egress_order_without_egressing_other_results():
    ledger = EventLedger()
    raw_output = BytesIO()
    supplied = (
        SuppliedSystemMaterialOccurrence(b"error", "provider:error", True),
        SuppliedSystemMaterialOccurrence(b"output", "provider:output", True),
        SuppliedSystemMaterialOccurrence(
            b"artifact", "provider:artifact", False
        ),
        SuppliedSystemMaterialOccurrence(b"end", "provider:end", False),
    )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls\n"),
        output_stream=StringIO(),
        raw_output_stream=raw_output,
        operator_invocation_provider=_provider(*supplied),
    )

    ingests = _ingests(ledger)
    supplied_ingests = ingests[1:]
    assert [event.exact_material for event in supplied_ingests] == [
        b"error",
        b"output",
        b"artifact",
        b"end",
    ]
    assert [
        event.material["provenance_occurrence_references"]
        for event in supplied_ingests
    ] == [[ingests[0].identity]] * 4
    assert raw_output.getvalue() == b"erroroutput"
    supplied_identities = {event.identity for event in supplied_ingests}
    assert [
        event.material["source_occurrence_reference"]
        for event in ledger.list_locality("locality")
        if event.kind == "operator.representation.recorded"
        and event.material["source_occurrence_reference"]
        in supplied_identities
    ] == [supplied_ingests[0].identity, supplied_ingests[1].identity]
    standing = read_operator_locality_standing(
        ledger, locality_identity="locality"
    )
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in standing["ingest_occurrences"][-4:]
    ] == [event.identity for event in supplied_ingests]


def test_missing_supplied_result_is_refused_after_command_acquisition():
    ledger = EventLedger()

    with pytest.raises(TypeError, match="exact supplied material required"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!ls\n"),
            output_stream=StringIO(),
            raw_output_stream=BytesIO(),
            operator_invocation_provider=lambda _exact, _supply: None,
        )

    assert [ingested_material_bytes(event) for event in _ingests(ledger)] == [
        b"!ls\n"
    ]


def test_equal_empty_supplied_material_remains_three_exact_occurrences():
    ledger = EventLedger()
    command = _command(ledger)
    events = tuple(
        ingest_supplied_invocation_occurrence(
            ledger,
            locality_identity="locality",
            command_occurrence_reference=command.identity,
            supplied=supplied,
        )
        for supplied in _supplied(output=b"", error=b"", end=b"")
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
            operator_invocation_provider=_provider(*_supplied()),
        )


def test_supplied_occurrence_requires_exact_types():
    class OtherOccurrence(SuppliedSystemMaterialOccurrence):
        pass

    ledger = EventLedger()
    command = _command(ledger)
    with pytest.raises(TypeError, match="exact supplied material required"):
        ingest_supplied_invocation_occurrence(
            ledger,
            locality_identity="locality",
            command_occurrence_reference=command.identity,
            supplied=OtherOccurrence(b"", "output", True),
        )


@pytest.mark.parametrize(
    "egress",
    (
        0,
        1,
        None,
        "yes",
    ),
)
def test_supplied_occurrence_requires_an_exact_egress_distinction(egress):
    with pytest.raises(TypeError, match="exact egress distinction required"):
        SuppliedSystemMaterialOccurrence(
            exact_bytes=b"",
            source_boundary="output",
            egress=egress,
        )


def test_supplied_yield_cannot_be_replaced_by_another_occurrence():
    ledger = EventLedger()
    command = _command(ledger)
    output, error, _end = tuple(
        ingest_supplied_invocation_occurrence(
            ledger,
            locality_identity="locality",
            command_occurrence_reference=command.identity,
            supplied=supplied,
        )
        for supplied in _supplied()
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
            ingest_supplied_invocation_occurrence(
                ledger,
                locality_identity="locality",
                command_occurrence_reference=reference,
                supplied=_supplied()[0],
            )

    command = _command(ledger)
    command.material["source_role"] = "system"
    with pytest.raises(ValueError, match="exact operator occurrence required"):
        ingest_supplied_invocation_occurrence(
            ledger,
            locality_identity="locality",
            command_occurrence_reference=command.identity,
            supplied=_supplied()[0],
        )
