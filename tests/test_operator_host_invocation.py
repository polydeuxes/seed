from __future__ import annotations

from collections import Counter
from io import BytesIO

import pytest


from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
)
from seed_runtime.events import EventLedger
from seed_runtime.material_source import (
    exact_material_result_bytes,
    read_exact_material_result,
)
from seed_runtime.witness_material_source import record_witness_material_source
from tests.operator_material_source_test_witness import (
    record_operator_material_occurrence,
)
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RECORDED_KIND,
)
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_locality_standing import (
    read_operator_locality_standing,
)
from seed_runtime.operator_invocation_locality import (
    OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND,
    record_operator_invocation_locality_responsibility_assignment,
    record_operator_invocation_locality_act_occurrence,
    record_operator_invocation_locality_result,
)
from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialOccurrence,
    SuppliedWitnessReadOccurrence,
    record_supplied_witness_material_source,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.yield_relation import read_requirements_of_yield_relation


def _supplied(
    *, output=b"\x00\xffout", error=b"same", end=b""
) -> tuple[SuppliedWitnessMaterialOccurrence, ...]:
    return (
        SuppliedWitnessMaterialOccurrence(output, "provider:0"),
        SuppliedWitnessMaterialOccurrence(error, "provider:1"),
        SuppliedWitnessMaterialOccurrence(end, "provider:2"),
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
            provenance_occurrence_positions=positions,
        )


def test_supplied_occurrence_requires_reads_to_reconstruct_its_material():
    with pytest.raises(TypeError, match="exact supplied read occurrences"):
        SuppliedWitnessMaterialOccurrence(
            b"abcd",
            "invocation output",
            read_occurrences=(
                SuppliedWitnessReadOccurrence(b"ab", "read:0", 0),
                SuppliedWitnessReadOccurrence(b"ce", "read:1", 1),
            ),
        )


def _provider(*occurrences):
    def provide(_exact_command, supply):
        for occurrence in occurrences:
            supply(occurrence)

    return provide


def test_measured_pairs_do_not_depend_on_supplied_read_partition():
    exact = b"abcdef"

    def run(read_occurrences):
        ledger = EventLedger()
        supplied = SuppliedWitnessMaterialOccurrence(
            exact,
            "invocation output",
            read_occurrences=read_occurrences,
        )
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!cat material\n"),
            operator_invocation_provider=_provider(supplied),
        )
        relation = next(
            event
            for event in ledger.list()
            if event.kind == OPERATOR_INVOCATION_LOCALITY_RECORDED_KIND
        )
        events = ledger.list_locality(
            relation.material["destination_locality_identity"]
        )
        acquisition = next(
            event
            for event in events
            if event.kind == "witness.material.source_result_recorded"
        )
        position_result = next(
            event
            for event in events
            if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        )
        return acquisition, position_result

    one_read = (
        SuppliedWitnessReadOccurrence(exact, "read:0", 0),
    )
    three_reads = (
        SuppliedWitnessReadOccurrence(b"ab", "read:0", 0),
        SuppliedWitnessReadOccurrence(b"cd", "read:1", 1),
        SuppliedWitnessReadOccurrence(b"ef", "read:2", 2),
    )

    one_acquisition, one_positions = run(one_read)
    split_acquisition, split_positions = run(three_reads)

    assert one_acquisition.exact_material == split_acquisition.exact_material == exact
    assert len(one_acquisition.material["read_occurrences"]) == 1
    assert len(split_acquisition.material["read_occurrences"]) == 3
    one_assertions = dict(one_positions.material["assertions"])
    split_assertions = dict(split_positions.material["assertions"])
    for coordinate in (
        "source_material_acquisition_occurrence_identity",
        "source_locality_identity",
        "completeness_boundary_identity",
    ):
        one_assertions.pop(coordinate)
        split_assertions.pop(coordinate)
    assert one_assertions == split_assertions
    assert one_assertions["occurrences"] == len(exact) - 1


def test_provider_cannot_append_outside_one_supplied_occurrence():
    ledger = EventLedger()

    def provider(_exact_command, supply):
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"one exact supplied result",
                "provider:guarded",
            )
        )
        record_witness_material_source(
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
            operator_invocation_provider=provider,
        )


def _acquisition_results(ledger):
    acquisition_results = []
    for event in ledger.list():
        try:
            acquisition_results.append(read_exact_material_result(ledger, event.identity))
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
    act = record_operator_invocation_locality_act_occurrence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=assignment.locality_identity
        ),
    )
    return record_operator_invocation_locality_result(
        ledger, act_occurrence_event_identity=act.identity
    )


def test_supplied_result_preserves_one_exact_prior_occurrence_reference():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    source = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"source", "provider:source"
        ),
    )
    result = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"result",
            "provider:result",
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
    function = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"opaque external function reference", "provider:function"
        ),
    )
    source = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"source", "provider:source"
        ),
        prior_supplied_occurrence_references=(function.identity,),
    )
    result = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(
            b"result",
            "provider:result",
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
        record_supplied_witness_material_source(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=SuppliedWitnessMaterialOccurrence(
                b"result",
                "provider:result",
                provenance_occurrence_positions=(0,),
            ),
        )

    assert len(ledger.list()) == before


def test_supplied_result_refuses_crossed_reordered_or_unrelated_prior_references():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    first = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(b"first", "provider:first"),
    )
    second = record_supplied_witness_material_source(
        ledger,
        operator_invocation_locality_result_event_identity=relation.identity,
        command_occurrence_reference=command.identity,
        supplied=SuppliedWitnessMaterialOccurrence(b"second", "provider:second"),
        prior_supplied_occurrence_references=(first.identity,),
    )
    unrelated = record_witness_material_source(
        ledger,
        locality_identity="unrelated",
        exact_bytes=b"unrelated",
        source_boundary="unrelated boundary",
    )
    supplied = SuppliedWitnessMaterialOccurrence(
        b"result",
        "provider:result",
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
            record_supplied_witness_material_source(
                ledger,
                operator_invocation_locality_result_event_identity=relation.identity,
                command_occurrence_reference=command.identity,
                supplied=supplied,
                prior_supplied_occurrence_references=references,
            )

    assert len(ledger.list()) == before


def test_host_provider_receives_an_acquired_exact_command_before_it_occurs():
    ledger = EventLedger()
    seen = []

    def provider(exact_command, supply):
        seen.append(exact_command)
        assert [exact_material_result_bytes(event) for event in _acquisition_results(ledger)] == [
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
        for occurrence in _supplied():
            supply(occurrence)

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls \xff\x00\n"),
        operator_invocation_provider=provider,
    )

    assert seen == [b"!ls \xff\x00\n"]
    acquisition_results = _acquisition_results(ledger)
    assert [exact_material_result_bytes(event) for event in acquisition_results] == [
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
        event.material["unknown"] == ["source_relation"]
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
    assert len(
        [
            event
            for event in ledger.list()
            if event.kind == OCCURRENCE_POSITION_RECORDED_KIND
        ]
    ) == 1
    assert len(
        [
            event
            for event in ledger.list()
            if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        ]
    ) == 4
    operator_standing = read_operator_locality_standing(
        ledger, locality_identity="locality"
    )
    witness_standing = read_operator_locality_standing(
        ledger, locality_identity=relation.material["destination_locality_identity"]
    )
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in operator_standing["material_acquisition_result_occurrences"]
    ] == [acquisition_results[0].identity]
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in witness_standing["material_acquisition_result_occurrences"]
    ] == [event.identity for event in acquisition_results[1:]]
    assert operator_standing["admission_result_occurrences"] == {}
    assert witness_standing["admission_result_occurrences"] == {}
    witness_pair_measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        and event.locality_identity
        == relation.material["destination_locality_identity"]
    )
    assert len(witness_pair_measurements) == 3
    assert {
        event.material["input_applicability_event_identity"]
        for event in witness_pair_measurements
    } == set(witness_standing["applicability_result_occurrences"])


def test_witness_material_is_durable_before_provider_resumes():
    ledger = EventLedger()
    observed = []

    def provider(_exact_command, supply):
        for occurrence in (
            SuppliedWitnessMaterialOccurrence(
                b"lower-0", "provider:output:0"
            ),
            SuppliedWitnessMaterialOccurrence(
                b"lower-1", "provider:output:1"
            ),
            SuppliedWitnessMaterialOccurrence(
                b"", "provider:completion"
            ),
        ):
            supply(occurrence)
            observed.append(
                tuple(event.exact_material for event in _acquisition_results(ledger))
            )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls\n"),
        operator_invocation_provider=provider,
    )

    assert observed == [
        (b"!ls\n", b"lower-0"),
        (b"!ls\n", b"lower-0", b"lower-1"),
        (b"!ls\n", b"lower-0", b"lower-1", b""),
    ]


def test_reused_witness_boundary_is_refused_before_second_acquisition():
    ledger = EventLedger()

    def provider(_exact_command, supply):
        supply(SuppliedWitnessMaterialOccurrence(b"first", "same"))
        supply(SuppliedWitnessMaterialOccurrence(b"second", "same"))

    with pytest.raises(ValueError, match="distinct source boundary required"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!ls\n"),
            operator_invocation_provider=provider,
        )

    assert [event.exact_material for event in _acquisition_results(ledger)] == [
        b"!ls\n",
        b"first",
    ]


def test_provider_death_leaves_the_complete_command_acquisition():
    ledger = EventLedger()

    def die(_exact_command, _supply):
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!cat path\n"),
            operator_invocation_provider=die,
        )

    assert [exact_material_result_bytes(event) for event in _acquisition_results(ledger)] == [
        b"!cat path\n"
    ]
    assert len(
        [
            event
            for event in ledger.list_locality("locality")
            if event.kind == BYTE_MEASUREMENT_RECORDED_KIND
        ]
    ) == 1


def test_provider_death_preserves_each_already_supplied_witness_occurrence():
    ledger = EventLedger()

    def die(_exact_command, supply):
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"partial", "provider:output:0"
            )
        )
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!cat path\n"),
            operator_invocation_provider=die,
        )

    assert [event.exact_material for event in _acquisition_results(ledger)] == [
        b"!cat path\n",
        b"partial",
    ]
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
            if event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
        ]
    ) == 1


def test_provider_supply_acquires_every_occurrence_without_selecting_emission():
    ledger = EventLedger()
    supplied = (
        SuppliedWitnessMaterialOccurrence(b"error", "provider:error"),
        SuppliedWitnessMaterialOccurrence(
            b"output",
            "provider:output",
            provenance_occurrence_positions=(0,),
        ),
        SuppliedWitnessMaterialOccurrence(
            b"artifact", "provider:artifact"
        ),
        SuppliedWitnessMaterialOccurrence(b"end", "provider:end"),
    )

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="locality",
        input_stream=BytesIO(b"!ls\n"),
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
    preserved_provenance = [
        event.material["provenance_occurrence_references"]
        for event in supplied_acquisition_results
    ]
    expected_base = [acquisition_results[0].identity, relation.identity]
    assert preserved_provenance == [
        expected_base,
        [*expected_base, supplied_acquisition_results[0].identity],
        expected_base,
        expected_base,
    ]
    kinds = tuple(event.kind for event in ledger.list())
    assert kinds.count(BYTE_PAIR_MEASUREMENT_RECORDED_KIND) == 4
    assert RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND not in kinds
    standing = read_operator_locality_standing(
        ledger, locality_identity=relation.material["destination_locality_identity"]
    )
    assert [
        occurrence["result_occurrence_identity"]
        for occurrence in standing["material_acquisition_result_occurrences"][-4:]
    ] == [event.identity for event in supplied_acquisition_results]


def test_repeated_exact_witness_material_does_not_repeat_measurement_work():
    ledger = EventLedger()

    def provider(_command, supply):
        supply(
            SuppliedWitnessMaterialOccurrence(
                b"tatatata",
                "provider:repeated-material",
            )
        )

    def derived_counts():
        kinds = Counter(event.kind for event in ledger.list())
        return {
            BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND: kinds[
                BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND
            ],
            BYTE_MEASUREMENT_RECORDED_KIND: kinds[BYTE_MEASUREMENT_RECORDED_KIND],
            BYTE_PAIR_MEASUREMENT_RECORDED_KIND: kinds[
                BYTE_PAIR_MEASUREMENT_RECORDED_KIND
            ],
        }

    for _position in range(2):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!opaque\n"),
            operator_invocation_provider=provider,
        )
        if _position == 0:
            first_counts = derived_counts()
            first_acquisitions = _acquisition_results(ledger)

    assert first_counts == {
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND: 2,
        BYTE_MEASUREMENT_RECORDED_KIND: 2,
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND: 1,
    }
    assert derived_counts() == first_counts
    assert len(first_acquisitions) == 2
    later_acquisitions = _acquisition_results(ledger)
    assert len(later_acquisitions) == 4


def test_missing_supplied_result_is_refused_after_command_acquisition():
    ledger = EventLedger()

    with pytest.raises(TypeError, match="exact supplied material required"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_identity="locality",
            input_stream=BytesIO(b"!ls\n"),
            operator_invocation_provider=lambda _exact, _supply: None,
        )

    assert [exact_material_result_bytes(event) for event in _acquisition_results(ledger)] == [
        b"!ls\n"
    ]


def test_equal_empty_supplied_material_remains_three_exact_occurrences():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    events = tuple(
        record_supplied_witness_material_source(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=supplied,
        )
        for supplied in _supplied(output=b"", error=b"", end=b"")
    )

    assert len(events) == 3
    assert len({event.identity for event in events}) == 3
    assert [exact_material_result_bytes(event) for event in events] == [b"", b"", b""]


def test_supplied_occurrence_requires_exact_types():
    class OtherOccurrence(SuppliedWitnessMaterialOccurrence):
        pass

    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    with pytest.raises(TypeError, match="exact supplied material required"):
        record_supplied_witness_material_source(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=OtherOccurrence(b"", "output"),
        )


def test_supplied_yield_cannot_be_replaced_by_another_occurrence():
    ledger = EventLedger()
    command = _command(ledger)
    relation = _operator_invocation_relation(ledger, command)
    output, error, _end = tuple(
        record_supplied_witness_material_source(
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
        yield_relation_event_identity=output.material["yield_relation_identity"],
        act_occurrence_event_identity=output.material[
            "act_occurrence_event_identity"
        ],
    )
    substituted = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=output.identity,
        yield_relation_event_identity=error.material["yield_relation_identity"],
        act_occurrence_event_identity=output.material[
            "act_occurrence_event_identity"
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
        yield_relation_event_identity=output.material["yield_relation_identity"],
        act_occurrence_event_identity=output.material[
            "act_occurrence_event_identity"
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
            record_supplied_witness_material_source(
                ledger,
                operator_invocation_locality_result_event_identity=relation.identity,
                command_occurrence_reference=reference,
                supplied=_supplied()[0],
            )

    command.material["source_role"] = "this Witness"
    with pytest.raises(ValueError, match="operator material occurrence"):
        record_supplied_witness_material_source(
            ledger,
            operator_invocation_locality_result_event_identity=relation.identity,
            command_occurrence_reference=command.identity,
            supplied=_supplied()[0],
        )
