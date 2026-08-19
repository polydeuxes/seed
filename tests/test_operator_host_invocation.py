from __future__ import annotations

from io import BytesIO, StringIO

import pytest

FIDELITY_SUBJECT = "supplied_material_invocation"

from seed_runtime.byte_measurement import BYTE_MEASUREMENT_RECORDED_KIND
from seed_runtime.events import EventLedger
from seed_runtime.material_acquisition import (
    acquired_material_bytes,
    read_exact_material_acquisition_result,
)
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from tests.operator_material_acquisition_test_witness import (
    record_operator_material_occurrence,
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
from seed_runtime.operator_invocation_locality import (
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
    record_operator_invocation_locality_responsibility_assignment,
    record_operator_invocation_locality_act_evidence,
    record_operator_invocation_locality_result,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
    acquire_supplied_witness_material_occurrence,
)
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation


def _supplied(
    *, output=b"\x00\xffout", error=b"same", end=b""
) -> tuple[SuppliedWitnessMaterialOccurrence, ...]:
    return (
        SuppliedWitnessMaterialOccurrence(output, "provider:0", True),
        SuppliedWitnessMaterialOccurrence(error, "provider:1", True),
        SuppliedWitnessMaterialOccurrence(end, "provider:2", False),
    )


@pytest.mark.parametrize(
    "positions",
    ([], (True,), (-1,), (0, 0)),
)
def test_supplied_occurrence_requires_exact_distinct_prior_positions(positions):
    with pytest.raises(TypeError, match="exact prior supplied occurrence positions"):
        SuppliedWitnessMaterialOccurrence(
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


def test_provider_cannot_append_outside_one_supplied_occurrence():
    ledger = EventLedger()

    def provider(_exact_command, supply):
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"one exact supplied result",
                "provider:guarded",
                False,
            )
        )
        record_witness_material_acquisition(
            ledger,
            locality_identity="outside-provider-locality",
            exact_bytes=b"outside supplied material",
            source_boundary="provider side occurrence",
        )

    with pytest.raises(ValueError, match="outside supplied material"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="operator-locality",
            input_stream=BytesIO(b"!guard\n"),
            output_stream=StringIO(),
            raw_output_stream=BytesIO(),
            operator_invocation_provider=provider,
        )


def _acquisition_results(ledger):
    acquisition_results = []
    for event in ledger.list():
        try:
            acquisition_results.append(read_exact_material_acquisition_result(ledger, event.identity))
        except (TypeError, ValueError):
            pass
    return acquisition_results


def _command(ledger, *, locality="locality", exact=b"!ls\n"):
    return record_operator_material_occurrence(
        ledger,
        locality_identity=locality,
        exact=exact,
    )


def _operator_invocation_relation(ledger, command):
    assignment = record_operator_invocation_locality_responsibility_assignment(
        ledger,
        operator_material_occurrence_reference=command.identity,
        operator_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=command.locality_identity
        ),
    )
    act = record_operator_invocation_locality_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=assignment.locality_identity
        ),
    )
    return record_operator_invocation_locality_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )


def test_supplied_result_preserves_one_exact_prior_occurrence_reference():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    source = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"source", "provider:source", False
        ),
    )
    result = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
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


def test_supplied_result_preserves_function_and_source_occurrence_references():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    function = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"opaque external function reference", "provider:function", False
        ),
    )
    source = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"source", "provider:source", False
        ),
        prior_supplied_occurrence_references=(function.identity,),
    )
    result = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"result",
            "provider:result",
            False,
            provenance_occurrence_positions=(0, 1),
        ),
        prior_supplied_occurrence_references=(function.identity, source.identity),
    )

    assert result.material["provenance_occurrence_references"] == [
        command.identity,
        relation.identity,
        function.identity,
        source.identity,
    ]


def test_supplied_result_refuses_a_nonprior_occurrence_position():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    before = len(ledger.list())

    with pytest.raises(ValueError, match="exact prior supplied occurrence"):
        acquire_supplied_witness_material_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=SuppliedWitnessMaterialOccurrence(
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
    relation = _operator_invocation_relation(ledger, command)
    first = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(b"first", "provider:first", False),
    )
    second = acquire_supplied_witness_material_occurrence(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(b"second", "provider:second", False),
        prior_supplied_occurrence_references=(first.identity,),
    )
    unrelated = record_witness_material_acquisition(
        ledger,
        locality_identity="unrelated",
        exact_bytes=b"unrelated",
        source_boundary="unrelated boundary",
    )
    supplied = SuppliedWitnessMaterialOccurrence(
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
            acquire_supplied_witness_material_occurrence(
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
            "locality_standing_through_event_occurrence_identity"
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
    (
        OCCURRENCE_POSITION_RECORDED_KIND,
        OPERATOR_MATERIAL_ACQUIRE_RECORDED_KIND,
    ),
    ("operator.representation.recorded", None),
)


def test_host_provider_receives_an_acquired_exact_command_before_it_occurs():
    ledger = EventLedger()
    seen = []
    raw_output = BytesIO()

    def provider(exact_command, supply):
        seen.append(exact_command)
        assert [acquired_material_bytes(event) for event in _acquisition_results(ledger)] == [
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
    acquisition_results = _acquisition_results(ledger)
    assert [acquired_material_bytes(event) for event in acquisition_results] == [
        b"!ls \xff\x00\n",
        b"\x00\xffout",
        b"same",
        b"",
    ]
    assert [event.material["source_role"] for event in acquisition_results] == [
        "this operator",
        "this Witness",
        "this Witness",
        "this Witness",
    ]
    assert [event.material["source_boundary"] for event in acquisition_results[1:]] == [
        "provider:0",
        "provider:1",
        "provider:2",
    ]
    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    )
    assert [
        event.material["provenance_occurrence_references"]
        for event in acquisition_results[1:]
    ] == [[acquisition_results[0].identity, relation.identity]] * 3
    assert {event.locality_identity for event in acquisition_results[1:]} == {
        relation.material["destination_locality_identity"]
    }
    assert all(
        event.material["unknown"] == ["represented_relation", "source_relation"]
        for event in acquisition_results[1:]
    )
    assert len({event.material["result_identity"] for event in acquisition_results}) == 4
    assert len(
        [
            event
            for event in ledger.list()
            if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        ]
    ) == 4
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
    ) == 4
    operator_standing = read_operator_locality_standing(
        ledger, locality_identity="locality"
    )
    witness_standing = read_operator_locality_standing(
        ledger, locality_identity=relation.material["destination_locality_identity"]
    )
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in operator_standing["material_acquisition_result_occurrences"]
    ] == [acquisition_results[0].identity]
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in witness_standing["material_acquisition_result_occurrences"]
    ] == [event.identity for event in acquisition_results[1:]]
    assert operator_standing["admission_result_occurrences"] == {}
    assert witness_standing["admission_result_occurrences"] == {
        event.identity: None for event in admissions
    }
    assert len(witness_standing["applicability_result_occurrences"]) == 2
    assert {
        reference["emitted_event_identity"]
        for reference in witness_standing["representations"].values()
        if reference["emitted_event_identity"] is not None
    } == {event.identity for event in emitted}


def test_operator_emission_uses_the_current_locality_after_locality_change():
    ledger = EventLedger()

    def provider(_exact_command, supply):
        supply(
            SuppliedWitnessMaterialOccurrence(
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
        if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
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


def test_witness_material_is_durable_and_emitted_before_the_provider_resumes():
    ledger = EventLedger()
    raw_output = BytesIO()
    observed = []

    def provider(_exact_command, supply):
        for occurrence in (
            SuppliedWitnessMaterialOccurrence(
                b"lower-0", "provider:output:0", True
            ),
            SuppliedWitnessMaterialOccurrence(
                b"lower-1", "provider:output:1", True
            ),
            SuppliedWitnessMaterialOccurrence(
                b"", "provider:completion", False
            ),
        ):
            supply(occurrence)
            observed.append(
                (
                    raw_output.getvalue(),
                    tuple(event.exact_material for event in _acquisition_results(ledger)),
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


def test_reused_witness_boundary_is_refused_before_second_acquisition_or_egress():
    ledger = EventLedger()
    raw_output = BytesIO()

    def provider(_exact_command, supply):
        supply(SuppliedWitnessMaterialOccurrence(b"first", "same", True))
        supply(SuppliedWitnessMaterialOccurrence(b"second", "same", True))

    with pytest.raises(ValueError, match="distinct source boundary required"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!ls\n"),
            output_stream=StringIO(),
            raw_output_stream=raw_output,
            operator_invocation_provider=provider,
        )

    assert [event.exact_material for event in _acquisition_results(ledger)] == [
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

    assert [acquired_material_bytes(event) for event in _acquisition_results(ledger)] == [
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


def test_provider_death_preserves_each_already_supplied_witness_occurrence():
    ledger = EventLedger()
    raw_output = BytesIO()

    def die(_exact_command, supply):
        supply(
            SuppliedWitnessMaterialOccurrence(
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

    assert [event.exact_material for event in _acquisition_results(ledger)] == [
        b"!cat path\n",
        b"partial",
    ]
    assert raw_output.getvalue() == b"partial"
    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    )
    witness_events = ledger.list_locality(
        relation.material["destination_locality_identity"]
    )
    assert len(
        [
            event
            for event in witness_events
            if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        ]
    ) == 1
    assert len(
        [
            event
            for event in witness_events
            if event.kind == OCCURRENCE_POSITION_RECORDED_KIND
        ]
    ) == 1


def test_provider_declares_exact_egress_order_without_egressing_other_results():
    ledger = EventLedger()
    raw_output = BytesIO()
    supplied = (
        SuppliedWitnessMaterialOccurrence(b"error", "provider:error", True),
        SuppliedWitnessMaterialOccurrence(b"output", "provider:output", True),
        SuppliedWitnessMaterialOccurrence(
            b"artifact", "provider:artifact", False
        ),
        SuppliedWitnessMaterialOccurrence(b"end", "provider:end", False),
    )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls\n"),
        output_stream=StringIO(),
        raw_output_stream=raw_output,
        operator_invocation_provider=_provider(*supplied),
    )

    acquisition_results = _acquisition_results(ledger)
    supplied_acquisition_results = acquisition_results[1:]
    assert [event.exact_material for event in supplied_acquisition_results] == [
        b"error",
        b"output",
        b"artifact",
        b"end",
    ]
    relation = next(
        event
        for event in ledger.list()
        if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
    )
    assert [
        event.material["provenance_occurrence_references"]
        for event in supplied_acquisition_results
    ] == [[acquisition_results[0].identity, relation.identity]] * 4
    assert raw_output.getvalue() == b"erroroutput"
    supplied_identities = {event.identity for event in supplied_acquisition_results}
    assert [
        event.material["source_occurrence_reference"]
        for event in ledger.list()
        if event.kind == "operator.representation.recorded"
        and event.material["source_occurrence_reference"]
        in supplied_identities
    ] == [supplied_acquisition_results[0].identity, supplied_acquisition_results[1].identity]
    standing = read_operator_locality_standing(
        ledger, locality_identity=relation.material["destination_locality_identity"]
    )
    assert [
        occurrence["evidence_event_identity"]
        for occurrence in standing["material_acquisition_result_occurrences"][-4:]
    ] == [event.identity for event in supplied_acquisition_results]


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

    assert [acquired_material_bytes(event) for event in _acquisition_results(ledger)] == [
        b"!ls\n"
    ]


def test_equal_empty_supplied_material_remains_three_exact_occurrences():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    events = tuple(
        acquire_supplied_witness_material_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=supplied,
        )
        for supplied in _supplied(output=b"", error=b"", end=b"")
    )

    assert len(events) == 3
    assert len({event.identity for event in events}) == 3
    assert [acquired_material_bytes(event) for event in events] == [b"", b"", b""]


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
    class OtherOccurrence(SuppliedWitnessMaterialOccurrence):
        pass

    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    with pytest.raises(TypeError, match="exact supplied material required"):
        acquire_supplied_witness_material_occurrence(
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
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=b"",
            source_boundary="output",
            egress=egress,
        )


def test_supplied_yield_cannot_be_replaced_by_another_occurrence():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    output, error, _end = tuple(
        acquire_supplied_witness_material_occurrence(
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
    relation = _operator_invocation_relation(ledger, command)
    other_locality = _command(ledger, locality="other")

    for reference in ("missing", other_locality.identity):
        with pytest.raises(ValueError, match="exact operator occurrence required"):
            acquire_supplied_witness_material_occurrence(
                ledger,
                operator_invocation_locality_result_event_identity=relation.identity,
                command_occurrence_reference=reference,
                supplied=_supplied()[0],
            )

    command.material["source_role"] = "this Witness"
    with pytest.raises(ValueError, match="operator material occurrence"):
        acquire_supplied_witness_material_occurrence(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=_supplied()[0],
        )
