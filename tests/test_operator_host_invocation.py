from __future__ import annotations

from io import BytesIO, StringIO

import pytest

FIDELITY_SUBJECT = "supplied_material_invocation"

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
from seed_runtime.operator_system_locality import (
    OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND,
    record_operator_system_locality_responsibility_assignment,
    record_operator_system_locality_act_evidence,
    record_operator_system_locality_result,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedSystemMaterialOccurrence,
    ingest_supplied_invocation_occurrence,
)
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation


def _supplied(
    *, output=b"\x00\xffout", error=b"same", end=b""
) -> tuple[SuppliedSystemMaterialOccurrence, ...]:
    return (
        SuppliedSystemMaterialOccurrence(output, "provider:0", True),
        SuppliedSystemMaterialOccurrence(error, "provider:1", True),
        SuppliedSystemMaterialOccurrence(end, "provider:2", False),
    )


@pytest.mark.parametrize(
    "positions",
    ([], (True,), (-1,), (0, 0)),
)
def test_supplied_occurrence_requires_exact_distinct_prior_positions(positions):
    with pytest.raises(TypeError, match="exact prior supplied occurrence positions"):
        SuppliedSystemMaterialOccurrence(
            b"result",
            "provider:result",
            False,
            provenance_occurrence_positions=positions,
        )


def _provider(*occurrences):
    def provide(_exact_command, supply):
        for occurrence in occurrences:
            supply(occurrence)

    return provide


def _ingests(ledger):
    return [
        event
        for event in ledger.list()
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


def _operator_system_relation(ledger, command):
    assignment = record_operator_system_locality_responsibility_assignment(
        ledger,
        operator_material_occurrence_reference=command.identity,
        operator_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=command.locality_identity
        ),
    )
    act = record_operator_system_locality_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
    )
    return record_operator_system_locality_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )


def test_supplied_result_preserves_one_exact_prior_occurrence_reference():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_system_relation(ledger, command)
    source = ingest_supplied_invocation_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedSystemMaterialOccurrence(
            b"source", "provider:source", False
        ),
    )
    result = ingest_supplied_invocation_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedSystemMaterialOccurrence(
            b"result",
            "provider:result",
            False,
            provenance_occurrence_positions=(0,),
        ),
        prior_supplied_occurrence_references=(source.identity,),
    )

    assert result.material["provenance_occurrence_references"] == [
        command.identity,
        relation.identity,
        source.identity,
    ]


def test_supplied_result_refuses_a_nonprior_occurrence_position():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_system_relation(ledger, command)
    before = len(ledger.list())

    with pytest.raises(ValueError, match="exact prior supplied occurrence"):
        ingest_supplied_invocation_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=SuppliedSystemMaterialOccurrence(
                b"result",
                "provider:result",
                False,
                provenance_occurrence_positions=(0,),
            ),
        )

    assert len(ledger.list()) == before


def test_supplied_result_refuses_crossed_reordered_or_unrelated_prior_references():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_system_relation(ledger, command)
    first = ingest_supplied_invocation_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedSystemMaterialOccurrence(b"first", "provider:first", False),
    )
    second = ingest_supplied_invocation_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedSystemMaterialOccurrence(b"second", "provider:second", False),
        prior_supplied_occurrence_references=(first.identity,),
    )
    unrelated = ingest_material(
        ledger,
        locality_identity="unrelated",
        exact_bytes=b"unrelated",
        source_role="system",
        source_boundary="unrelated boundary",
    )
    supplied = SuppliedSystemMaterialOccurrence(
        b"result",
        "provider:result",
        False,
        provenance_occurrence_positions=(0,),
    )
    before = len(ledger.list())

    for references in (
        (second.identity, first.identity),
        (unrelated.identity,),
        (command.identity,),
        ("missing",),
    ):
        with pytest.raises(ValueError, match="exact prior supplied occurrence"):
            ingest_supplied_invocation_occurrence(
                ledger,
                operator_invocation_locality_result_event_identity=relation.identity,
                command_occurrence_reference=command.identity,
                supplied=supplied,
                prior_supplied_occurrence_references=references,
            )

    assert len(ledger.list()) == before


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
    (OCCURRENCE_POSITION_RECORDED_KIND, MATERIAL_INGEST_OCCURRED_KIND),
    (
        OPERATOR_SYSTEM_LOCALITY_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        None,
    ),
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
    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND
    )
    assert [
        event.material["provenance_occurrence_references"]
        for event in ingests[1:]
    ] == [[ingests[0].identity, relation.identity]] * 3
    assert {event.locality_identity for event in ingests[1:]} == {
        relation.material["destination_locality_identity"]
    }
    assert all(
        event.material["unknown"] == ["represented_relation", "source_relation"]
        for event in ingests[1:]
    )
    assert len({event.material["result_identity"] for event in ingests}) == 4
    assert len(
        [
            event
            for event in ledger.list()
            if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        ]
    ) == 2
    emitted = [
        event
        for event in ledger.list()
        if event.kind == "operator.representation.emitted"
    ]
    assert len(emitted) == 2
    admissions = [
        event
        for event in ledger.list()
        if event.kind
        == "operator.representation.exact_material_admission_recorded"
    ]
    assert len(admissions) == 2
    assert {
        event.material["destination_operator_locality_identity"]
        for event in admissions
    } == {"locality"}
    assert len(
        [
            event
            for event in ledger.list()
            if event.kind == OCCURRENCE_POSITION_RECORDED_KIND
        ]
    ) == 2
    operator_standing = read_operator_locality_standing(
        ledger, locality_identity="locality"
    )
    system_standing = read_operator_locality_standing(
        ledger, locality_identity=relation.material["destination_locality_identity"]
    )
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in operator_standing["ingest_occurrences"]
    ] == [ingests[0].identity]
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in system_standing["ingest_occurrences"]
    ] == [event.identity for event in ingests[1:]]
    assert operator_standing["admission_result_occurrences"] == {}
    assert system_standing["admission_result_occurrences"] == {
        event.identity: None for event in admissions
    }
    assert len(system_standing["applicability_result_occurrences"]) == 2
    assert {
        reference["emitted_event_identity"]
        for reference in system_standing["representations"].values()
        if reference["emitted_event_identity"] is not None
    } == {event.identity for event in emitted}


def test_operator_emission_uses_the_current_locality_after_locality_change():
    ledger = EventLedger()

    def provider(_exact_command, supply):
        supply(
            SuppliedSystemMaterialOccurrence(
                b"one result",
                "provider:result",
                True,
            )
        )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="initial",
        input_stream=BytesIO(b"/locality\n!ls\n"),
        output_stream=StringIO(),
        raw_output_stream=BytesIO(),
        operator_invocation_provider=provider,
    )

    admissions = [
        event
        for event in ledger.list()
        if event.kind
        == "operator.representation.exact_material_admission_recorded"
    ]
    assert len(admissions) == 1
    admission = admissions[0]
    assert admission.locality_identity != "initial"
    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND
    )
    assert admission.locality_identity == relation.locality_identity
    assert admission.material["destination_operator_locality_identity"] == (
        relation.material["operator_locality_identity"]
    )
    emitted = [
        event
        for event in ledger.list()
        if event.kind == "operator.representation.emitted"
    ]
    assert len(emitted) == 1
    assert emitted[0].locality_identity == admission.locality_identity


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


def test_reused_system_boundary_is_refused_before_second_ingest_or_egress():
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
    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_SYSTEM_LOCALITY_RECORDED_KIND
    )
    assert [
        event.material["provenance_occurrence_references"]
        for event in supplied_ingests
    ] == [[ingests[0].identity, relation.identity]] * 4
    assert raw_output.getvalue() == b"erroroutput"
    supplied_identities = {event.identity for event in supplied_ingests}
    assert [
        event.material["source_occurrence_reference"]
        for event in ledger.list()
        if event.kind == "operator.representation.recorded"
        and event.material["source_occurrence_reference"]
        in supplied_identities
    ] == [supplied_ingests[0].identity, supplied_ingests[1].identity]
    standing = read_operator_locality_standing(
        ledger, locality_identity=relation.material["destination_locality_identity"]
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
    relation = _operator_system_relation(ledger, command)
    events = tuple(
        ingest_supplied_invocation_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
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
    relation = _operator_system_relation(ledger, command)
    with pytest.raises(TypeError, match="exact supplied material required"):
        ingest_supplied_invocation_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
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
    relation = _operator_system_relation(ledger, command)
    output, error, _end = tuple(
        ingest_supplied_invocation_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=supplied,
        )
        for supplied in _supplied()
    )

    exact = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=output.identity,
        evidence_of_yield_relation_event_identity=output.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=output.material[
            "responsible_act_evidence_identity"
        ],
    )
    substituted = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=output.identity,
        evidence_of_yield_relation_event_identity=error.material["evidence_of_yield_relation_identity"],
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
    different_command = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=output.identity,
        evidence_of_yield_relation_event_identity=output.material["evidence_of_yield_relation_identity"],
        responsible_act_evidence_event_identity=output.material[
            "responsible_act_evidence_identity"
        ],
    )
    assert not all(different_command.values())


def test_supplied_result_refuses_missing_different_or_corrupted_command():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_system_relation(ledger, command)
    other_locality = _command(ledger, locality="other")

    for reference in ("missing", other_locality.identity):
        with pytest.raises(ValueError, match="exact operator occurrence required"):
            ingest_supplied_invocation_occurrence(
                ledger,
                operator_invocation_locality_result_event_identity=relation.identity,
                command_occurrence_reference=reference,
                supplied=_supplied()[0],
            )

    command.material["source_role"] = "system"
    with pytest.raises(ValueError, match="operator material occurrence"):
        ingest_supplied_invocation_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=_supplied()[0],
        )
