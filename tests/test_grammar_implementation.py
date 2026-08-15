import ast
import json
import re
from tests.binary_input import binary_input
from io import BytesIO, StringIO
from pathlib import Path

from seed_runtime.byte_measurement import (
    BYTE_PAIR_INPUT_ROLE,
    _identity,
    _validate_moved_byte_assertion,
    assertions_of_recorded_byte_measurement,
    get_recorded_pair_input_applicability,
    record_adjacent_byte_pair_count_layer,
    record_byte_count_layer,
)
from seed_runtime.adjacency_pair_measurement import (
    measure_after,
    record_adjacency_pair_measurement_compare,
    record_adjacency_pair_measurements,
    record_emitted_representation_adjacency,
)
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.ids import new_id
from seed_runtime.material_ingest import ingest_material
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_command import AddressedOperatorCommand, OperatorCommandFrame
from seed_runtime.operator_checkpoint import (
    ADDRESSED_REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    open_operator_checkpoint,
)
from tests.material_fixture_console import run_material_fixture_console
from seed_runtime.operator_representation import (
    REPRESENTATION_EMISSION_INPUT_ROLE,
    emit_operator_representation,
    record_operator_representation,
)
from seed_runtime.preserved_material_measurement import (
    INGEST_OCCURRED_KIND,
    DeclaredMeasurement,
    measure_recurrence,
    ingest_occurrences,
    record_measurement_finding,
)
from seed_runtime.recorded_finding_yield_comparison import (
    compare_recorded_finding_yield,
)
from seed_runtime.assertion_comparison import (
    assertions_of_recorded_assertion_comparison,
    compare_assertion_yields,
    record_assertion_yield_comparison,
)
from seed_runtime.bounded_assertion_comparison import (
    compare_preserved_findings,
    record_comparison_finding,
)
from seed_runtime.recurrence_measurement import (
    assertions_of_recorded_measurement,
    measure_locality_counts,
    record_measured_count,
)
from seed_runtime.yield_evidence import YIELD_LIVE_BOUNDARIES
from seed_runtime.yield_evidence import read_yield_edge_requirements


GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed/grammar.json"
RUNTIME = Path(__file__).resolve().parents[1] / "seed_runtime"

EXACT = "exact"
INAPPLICABLE = "inapplicable"
UNKNOWN = "Unknown"
MISSING = "missing"
CONTRADICTION = "contradiction"


class _IntegrityAdversaryLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self._corrupted_ids: set[str] = set()

    def mark_corrupted(self, event_id: str) -> None:
        self._corrupted_ids.add(event_id)

    def integrity_of(self, event_id: str) -> str:
        if event_id in self._corrupted_ids:
            return CORRUPTED
        return super().integrity_of(event_id)


def _clause(clause_id: str) -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["clauses"][clause_id]


def _witness_grammar() -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["implementation_witness"]


def _content_locality_witness(
    content: dict, *, locality, occurrence_id: str
) -> str:
    if locality is None:
        return MISSING
    return (
        EXACT
        if locality.id == occurrence_id and locality.payload == content
        else MISSING
    )


def _assertion_locality_witness(bundle: dict, *, occurrence_id: str) -> str:
    requirements = _assertion_locality_requirements(
        bundle, occurrence_id=occurrence_id
    )
    return EXACT if all(requirements.values()) else MISSING


def _assertion_locality_requirements(
    bundle: dict, *, occurrence_id: str
) -> dict[str, bool]:
    assertion = bundle["source_assertion"]
    event = bundle["event"]
    carried = [
        item
        for item in event.payload.get("assertions", [])
        if item.get("dimensions", {}).get("identity") == assertion.assertion_id
    ]
    exact_relation = carried == [assertion.payload]
    exact_occurrence = (
        event.id == occurrence_id
        == assertion.recorded_occurrence_id
    )
    intact = bundle["ledger"].integrity_of(event.id) != CORRUPTED
    return {
        "exact_relation": exact_relation,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": intact,
    }


def _source_assertion():
    road = _byte_measurement_road()
    return road["source_assertion"]


def _byte_measurement_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_id="source",
        input_stream=binary_input("ta\n"),
        output_stream=StringIO(),
    )
    measurement = record_byte_count_layer(
        ledger,
        source_locality_ids=("source",),
        recording_locality_id="byte-measurement",
    )
    assertion = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, measurement.id)
        if item.result == "exact_source_material_set"
    )
    return {
        "ledger": ledger,
        "event": measurement,
        "source_assertion": assertion,
        "act_evidence": ledger.get(measurement.payload["responsible_act_evidence_id"]),
        "content_evidence": ledger.get(measurement.payload["yield_evidence_id"]),
    }


def _recorded_applicability() -> dict:
    # RecordedByteAssertion deliberately carries no ledger handle. Recreate the
    # live road so every relation can be checked through its own occurrences.
    ledger = _IntegrityAdversaryLedger()
    run_persistent_operator_console(
        ledger=ledger,
        locality_id="source",
        input_stream=binary_input("ta\n"),
        output_stream=StringIO(),
    )
    byte_measurement = record_byte_count_layer(
        ledger,
        source_locality_ids=("source",),
        recording_locality_id="byte-measurement",
    )
    pair_measurement = record_adjacent_byte_pair_count_layer(
        ledger,
        source_measurement_event_id=byte_measurement.id,
        recording_locality_id="measurement",
    )
    event = ledger.get(pair_measurement.payload["input_applicability_event_id"])
    read = get_recorded_pair_input_applicability(ledger, event.id)
    movement = ledger.get(read["input_movement_event_id"])
    return {
        "ledger": ledger,
        "applicability": read,
        "event": event,
        "act_evidence": ledger.get(event.payload["responsible_act_evidence_id"]),
        "content_evidence": ledger.get(event.payload["yield_evidence_id"]),
        "movement": movement,
        "movement_act_evidence": ledger.get(
            movement.payload["movement_act_evidence_event_id"]
        ),
        "movement_content_evidence": ledger.get(
            movement.payload["yield_evidence_id"]
        ),
        "pair_event": pair_measurement,
        "pair_act_evidence": ledger.get(
            pair_measurement.payload["responsible_act_evidence_id"]
        ),
        "pair_content_evidence": ledger.get(
            pair_measurement.payload["yield_evidence_id"]
        ),
    }


def _assertion_locality_movement_yield_road() -> dict:
    source = _recorded_applicability()
    return {
        "ledger": source["ledger"],
        "event": source["movement"],
        "act_evidence": source["movement_act_evidence"],
        "content_evidence": source["movement_content_evidence"],
        "recorded_result_occurrence_coordinate": "movement_act_occurrence_id",
        "act_evidence_occurrence_coordinate": "movement_act_occurrence_id",
    }


def _emission_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_id="emission",
        locality_standing={"as_of_event_id": None},
    )
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    event = ledger.get(representation["emitted_event_id"])
    return {
        "ledger": ledger,
        "event": event,
        "attempt": ledger.get(representation["emission_attempt_event_id"]),
        "attempt_locality_evidence": ledger.get(
            representation["emission_attempt_locality_evidence_id"]
        ),
        "act_evidence": ledger.get(
            event.payload["responsible_act_evidence_id"]
        ),
        "locality_evidence": ledger.get(event.payload["locality_evidence_id"]),
        "content_evidence": ledger.get(event.payload["yield_evidence_id"]),
    }


def _failed_emission_yield_road() -> dict:
    class PartialOutput(StringIO):
        def write(self, value):
            super().write(value[:-1])
            return len(value) - 1

    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_id="failed-emission",
        locality_standing={"as_of_event_id": None},
    )
    try:
        emit_operator_representation(
            ledger,
            representation=representation,
            output_stream=PartialOutput(),
        )
    except ValueError:
        pass
    event = ledger.get(representation["emission_outcome_event_id"])
    return _yield_bundle(ledger, event)


def _repeated_emission_attempt_road() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_id="repeated-emission-attempt",
        locality_standing={"as_of_event_id": None},
    )
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    first_attempt = ledger.get(representation["emission_attempt_event_id"])
    first_evidence = ledger.get(
        representation["emission_attempt_locality_evidence_id"]
    )
    first_event = ledger.get(representation["emitted_event_id"])
    first_act_evidence = ledger.get(
        first_event.payload["responsible_act_evidence_id"]
    )
    first_locality_evidence = ledger.get(
        first_event.payload["locality_evidence_id"]
    )
    first_yield_evidence = ledger.get(first_event.payload["yield_evidence_id"])
    emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    second_attempt = ledger.get(representation["emission_attempt_event_id"])
    second_evidence = ledger.get(
        representation["emission_attempt_locality_evidence_id"]
    )
    second_event = ledger.get(representation["emitted_event_id"])
    second_act_evidence = ledger.get(
        second_event.payload["responsible_act_evidence_id"]
    )
    second_locality_evidence = ledger.get(
        second_event.payload["locality_evidence_id"]
    )
    second_yield_evidence = ledger.get(second_event.payload["yield_evidence_id"])
    return (
        {
            "ledger": ledger,
            "attempt": first_attempt,
            "attempt_locality_evidence": first_evidence,
            "event": first_event,
            "act_evidence": first_act_evidence,
            "locality_evidence": first_locality_evidence,
            "content_evidence": first_yield_evidence,
        },
        {
            "ledger": ledger,
            "attempt": second_attempt,
            "attempt_locality_evidence": second_evidence,
            "event": second_event,
            "act_evidence": second_act_evidence,
            "locality_evidence": second_locality_evidence,
            "content_evidence": second_yield_evidence,
        },
    )


def _representation_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    representation = record_operator_representation(
        ledger,
        locality_id="representation",
        locality_standing={"as_of_event_id": None},
    )
    event = ledger.get(representation["representation_event_id"])
    return {
        "ledger": ledger,
        "event": event,
        "act_evidence": ledger.get(event.payload["responsible_act_evidence_id"]),
        "locality_evidence": ledger.get(event.payload["locality_evidence_id"]),
        "content_evidence": ledger.get(event.payload["yield_evidence_id"]),
    }


def _repeated_representation_road() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()

    def record() -> dict:
        representation = record_operator_representation(
            ledger,
            locality_id="repeated-representation",
            locality_standing={"as_of_event_id": None},
        )
        event = ledger.get(representation["representation_event_id"])
        return {
            "ledger": ledger,
            "event": event,
            "act_evidence": ledger.get(
                event.payload["responsible_act_evidence_id"]
            ),
            "locality_evidence": ledger.get(
                event.payload["locality_evidence_id"]
            ),
            "content_evidence": ledger.get(event.payload["yield_evidence_id"]),
        }

    return record(), record()


def _assertion_compare_input_locality_roads() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()
    run_material_fixture_console(
        ledger=ledger,
        locality_id="assertion-compare-source",
        input_stream=binary_input("a word\n"),
        output_stream=StringIO(),
    )
    sources = ingest_occurrences(
        ledger,
        locality_id="assertion-compare-source",
    )
    finding_event = record_measurement_finding(
        ledger,
        locality_id="assertion-compare-source",
        finding=measure_after(sources, "a", counting_scope="one source"),
    )
    counted = measure_locality_counts(
        ledger,
        bounded_localities=("assertion-compare-source",),
    )[0]
    first = record_measured_count(
        ledger,
        locality_id="assertion-compare-source",
        finding=counted,
    )
    second = record_measured_count(
        ledger,
        locality_id="assertion-compare-source",
        finding=counted,
    )
    first_count = next(
        item for item in assertions_of_recorded_measurement(first)
        if item.result == "count"
    )
    second_count = next(
        item for item in assertions_of_recorded_measurement(second)
        if item.result == "count"
    )
    comparison = compare_assertion_yields(
        ledger, (first_count.reference, second_count.reference)
    )

    def record() -> dict:
        event = record_assertion_yield_comparison(
            ledger,
            locality_id="assertion-compare-target",
            comparison=comparison,
        )
        evidence = ledger.get(event.payload["input_locality_evidence_ids"][0])
        return {
            "ledger": ledger,
            "event": event,
            "act_evidence": ledger.get(
                event.payload["responsible_act_evidence_id"]
            ),
            "content_evidence": ledger.get(event.payload["yield_evidence_id"]),
            "locality_evidence": evidence,
        }

    return record(), record()


def _assertion_yield_compare_road() -> dict:
    return _assertion_compare_input_locality_roads()[0]


def _bounded_assertion_compare_yield_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    for locality_id, material in (("first", "a b\n"), ("second", "a c\n")):
        run_material_fixture_console(
            ledger=ledger,
            locality_id=locality_id,
            input_stream=binary_input(material),
            output_stream=StringIO(),
        )
    findings = []
    for locality_id in ("first", "second"):
        occurrences = ingest_occurrences(ledger, locality_id=locality_id)
        findings.append(
            record_measurement_finding(
                ledger,
                locality_id=locality_id,
                finding=measure_after(
                    occurrences, "a", counting_scope="one exact locality"
                ),
            )
        )
    event = record_comparison_finding(
        ledger,
        locality_id="comparison",
        finding=compare_preserved_findings(
            ledger, tuple(finding.id for finding in findings)
        ),
    )
    return _yield_bundle(ledger, event)


def _locality_count_yield_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    run_material_fixture_console(
        ledger=ledger,
        locality_id="count-source",
        input_stream=binary_input("a b\n"),
        output_stream=StringIO(),
    )
    occurrences = ingest_occurrences(ledger, locality_id="count-source")
    record_measurement_finding(
        ledger,
        locality_id="count-source",
        finding=measure_after(
            occurrences, "a", counting_scope="one exact locality"
        ),
    )
    finding = measure_locality_counts(
        ledger, bounded_localities=("count-source",)
    )[0]
    event = record_measured_count(
        ledger,
        locality_id="count-result",
        finding=finding,
    )
    return _yield_bundle(ledger, event)


def _bounded_compare_input_locality_roads() -> tuple[dict, dict]:
    exact = _bounded_assertion_compare_yield_road()
    event = exact["event"]
    first = {
        **exact,
        "locality_evidence": exact["ledger"].get(
            event.payload["input_locality_evidence_ids"][0]
        ),
    }
    alternate = _bounded_assertion_compare_yield_road()
    alternate_event = alternate["event"]
    second = {
        **alternate,
        "locality_evidence": alternate["ledger"].get(
            alternate_event.payload["input_locality_evidence_ids"][0]
        ),
    }
    return first, second


def _bounded_compare_input_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    first_subject = evidence.payload.get("first_subject")
    second_subject = evidence.payload.get("second_subject")
    return {
        "exact_relation": (
            first_subject in event.payload.get("input_event_ids", [])
            and evidence.id in event.payload.get("input_locality_evidence_ids", [])
        ),
        "occurrence_witness": (
            isinstance(second_subject, dict)
            and second_subject.get("downstream_act_id")
            == event.payload.get("downstream_act_id")
            and second_subject.get("act_occurrence_id")
            == event.payload.get("act_occurrence_id")
        ),
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _bounded_compare_input_locality_cases() -> dict[str, str]:
    exact, alternate = _bounded_compare_input_locality_roads()
    missing = dict(exact)
    missing["locality_evidence"] = exact["locality_evidence"].model_copy(deep=True)
    missing["locality_evidence"].payload["first_subject"] = "missing-input"
    wrong_occurrence = dict(exact)
    wrong_occurrence["locality_evidence"] = alternate["locality_evidence"]
    corrupted, _ = _bounded_compare_input_locality_roads()
    corrupted["ledger"].mark_corrupted(corrupted["locality_evidence"].id)
    unrelated = dict(exact)
    unrelated["event"] = exact["event"].model_copy(deep=True)
    unrelated["event"].payload["boundary_notes"] = []

    def witness(bundle: dict) -> str:
        requirements = _bounded_compare_input_locality_requirements(bundle)
        return EXACT if all(requirements.values()) else MISSING

    return {
        "exact": witness(exact),
        "edge_missing": witness(missing),
        "wrong_occurrence": witness(wrong_occurrence),
        "corrupted_evidence": witness(corrupted),
        "unrelated_occurrence": witness(unrelated),
    }


def _assertion_compare_input_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    first_subject = evidence.payload.get("first_subject")
    second_subject = evidence.payload.get("second_subject")
    exact_relation = (
        first_subject in event.payload.get("inputs", [])
        and evidence.id in event.payload.get("input_locality_evidence_ids", [])
    )
    exact_occurrence = (
        isinstance(second_subject, dict)
        and second_subject.get("downstream_act_id")
        == event.payload.get("downstream_act_id")
        and second_subject.get("act_occurrence_id")
        == event.payload.get("act_occurrence_id")
    )
    return {
        "exact_relation": exact_relation,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _assertion_compare_input_locality_cases() -> dict[str, str]:
    exact, alternate = _assertion_compare_input_locality_roads()
    missing = dict(exact)
    missing_evidence = exact["locality_evidence"].model_copy(deep=True)
    missing_evidence.payload["first_subject"] = {
        "recorded_occurrence_reference": "not-an-input",
        "assertion_id": "not-an-input",
    }
    missing["locality_evidence"] = missing_evidence
    wrong_occurrence = dict(exact)
    wrong_evidence = exact["locality_evidence"].model_copy(deep=True)
    wrong_evidence.payload["second_subject"] = dict(
        alternate["locality_evidence"].payload["second_subject"]
    )
    wrong_occurrence["locality_evidence"] = wrong_evidence
    corrupted, _ = _assertion_compare_input_locality_roads()
    corrupted["ledger"].mark_corrupted(corrupted["locality_evidence"].id)
    unrelated = dict(exact)
    unrelated_event = exact["event"].model_copy(deep=True)
    unrelated_event.payload["assertions"] = list(
        reversed(unrelated_event.payload["assertions"])
    )
    unrelated["event"] = unrelated_event

    def witness(bundle: dict) -> str:
        return (
            EXACT
            if all(_assertion_compare_input_locality_requirements(bundle).values())
            else MISSING
        )

    return {
        "exact": witness(exact),
        "edge_missing": witness(missing),
        "wrong_occurrence": witness(wrong_occurrence),
        "corrupted_evidence": witness(corrupted),
        "unrelated_occurrence": witness(unrelated),
    }


def _checkpoint_locality_roads() -> tuple[dict, dict]:
    ledger = _IntegrityAdversaryLedger()

    def record(locality_id: str) -> dict:
        representation = record_operator_representation(
            ledger,
            locality_id=locality_id,
            locality_standing={"as_of_event_id": None},
        )
        addressed = AddressedOperatorCommand(
            command_id=new_id("operator_command"),
            locality_id=locality_id,
            addressed_at_representation_event_id=representation[
                "representation_event_id"
            ],
            frame=OperatorCommandFrame(
                exact_bytes=b"/checkpoint material\n",
                name=b"checkpoint",
                arguments=b"material",
            ),
        )
        checkpoint_result = open_operator_checkpoint(ledger, addressed)
        evidence = ledger.get(checkpoint_result.locality_evidence_event_id)
        checkpoint = ledger.get(
            addressed.addressed_at_representation_event_id
        )
        return {
            "ledger": ledger,
            "event": evidence,
            "addressed": addressed,
            "checkpoint": checkpoint,
        }

    return record("checkpoint-road-one"), record("checkpoint-road-two")


def _checkpoint_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    addressed = bundle["addressed"]
    checkpoint = bundle["checkpoint"]
    if addressed is None or checkpoint is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        event.payload.get("first_subject") == addressed.command_id
        and event.payload.get("addressed_identity") == addressed.command_id
        and event.payload.get("second_subject") == checkpoint.id
    )
    occurrence_witness = (
        event.payload.get("representation_reference") == checkpoint.id
        and addressed.addressed_at_representation_event_id == checkpoint.id
        and checkpoint.kind == "operator.representation.recorded"
        and addressed.locality_id == checkpoint.locality_id
        and event.locality_id != checkpoint.locality_id
    )
    return {
        "exact_relation": exact_relation,
        "occurrence_witness": occurrence_witness,
        "intact_evidence": all(
            bundle["ledger"].integrity_of(item.id) != CORRUPTED
            for item in (event, checkpoint)
        ),
    }


def _checkpoint_locality_cases() -> dict[str, str]:
    exact, alternate = _checkpoint_locality_roads()
    missing = dict(exact)
    missing["event"] = exact["event"].model_copy(deep=True)
    missing["event"].payload["second_subject"] = "missing-checkpoint"
    wrong_occurrence = dict(exact)
    wrong_occurrence["checkpoint"] = alternate["checkpoint"]
    corrupted, _ = _checkpoint_locality_roads()
    corrupted["ledger"].mark_corrupted(corrupted["event"].id)
    unrelated = dict(exact)
    unrelated["addressed"] = AddressedOperatorCommand(
        command_id=exact["addressed"].command_id,
        locality_id=exact["addressed"].locality_id,
        addressed_at_representation_event_id=(
            exact["addressed"].addressed_at_representation_event_id
        ),
        frame=OperatorCommandFrame(
            exact_bytes=b"/checkpoint other\n",
            name=b"checkpoint",
            arguments=b"other",
        ),
    )

    def witness(bundle: dict) -> str:
        return EXACT if all(_checkpoint_locality_requirements(bundle).values()) else MISSING

    return {
        "exact": witness(exact),
        "edge_missing": witness(missing),
        "wrong_occurrence": witness(wrong_occurrence),
        "corrupted_evidence": witness(corrupted),
        "unrelated_occurrence": witness(unrelated),
    }


def _yield_bundle(ledger, event) -> dict:
    act_evidence_id = event.payload.get("responsible_act_evidence_id")
    locality_evidence_id = event.payload.get("locality_evidence_id")
    return {
        "ledger": ledger,
        "event": event,
        "act_evidence": (
            ledger.get(act_evidence_id) if isinstance(act_evidence_id, str) else None
        ),
        "content_evidence": ledger.get(event.payload["yield_evidence_id"]),
        "locality_evidence": (
            ledger.get(locality_evidence_id)
            if isinstance(locality_evidence_id, str)
            else None
        ),
    }


def _preserved_material_yield_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    ledger.append(
        INGEST_OCCURRED_KIND,
        {"represented_material": "the cat"},
        locality_id="preserved-material-yield",
    )
    occurrences = ingest_occurrences(
        ledger, locality_id="preserved-material-yield"
    )
    finding = measure_recurrence(
        occurrences,
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact token equality",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        yield_in=(ledger, "w", "preserved-material-yield"),
    )
    event = record_measurement_finding(
        ledger,
        locality_id="preserved-material-yield",
        finding=finding,
    )
    bundle = _yield_bundle(ledger, event)
    bundle["yield_coordinate_paths"] = {
        "material_provenance": ("dimensions", "source_provenance")
    }
    return bundle


def _material_ingest_yield_road() -> dict:
    ledger = _IntegrityAdversaryLedger()
    event = ingest_material(
        ledger,
        locality_id="material-ingest-yield",
        exact_bytes=b"\x00\xffmaterial\n",
        source_role="system",
        source_boundary="supplied byte boundary",
    )
    return _yield_bundle(ledger, event)


def _recorded_finding_compare_yield_road() -> dict:
    source = _preserved_material_yield_road()
    event = compare_recorded_finding_yield(
        source["ledger"], source["event"].id
    )
    return _yield_bundle(source["ledger"], event)


def _adjacent_measurement_yield_road(*, compare: bool = False) -> dict:
    ledger = _IntegrityAdversaryLedger()
    for text in ("L a b R", "X a b Y"):
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": text},
            locality_id="adjacent-measurement-yield",
        )
    occurrences = ingest_occurrences(
        ledger, locality_id="adjacent-measurement-yield"
    )
    finding = record_measurement_finding(
        ledger,
        locality_id="adjacent-measurement-yield",
        finding=measure_after(occurrences, "a", counting_scope="exact fixture"),
    )
    first = record_adjacency_pair_measurements(
        ledger,
        locality_id="adjacent-measurement-yield",
        finding_event_id=finding.id,
    )
    if not compare:
        return _yield_bundle(ledger, first)
    representation = record_operator_representation(
        ledger,
        locality_id="adjacent-measurement-yield",
        locality_standing={"as_of_event_id": None},
    )
    first_emission = emit_operator_representation(
        ledger, representation=representation, output_stream=StringIO()
    )
    first_emission_event_id = first_emission["emitted_event_id"]
    second_emission = emit_operator_representation(
        ledger, representation=representation, output_stream=StringIO()
    )
    first = record_emitted_representation_adjacency(
        ledger, emission_event_id=first_emission_event_id
    )
    second = record_emitted_representation_adjacency(
        ledger, emission_event_id=second_emission["emitted_event_id"]
    )
    event = record_adjacency_pair_measurement_compare(
        ledger,
        locality_id="adjacent-measurement-yield",
        measurement_event_ids=(first.id, second.id),
    )
    return _yield_bundle(ledger, event)


def _assertion_witness(bundle: dict) -> dict[str, str]:
    assertion = bundle["source_assertion"]
    event = bundle["event"]
    content_evidence = bundle["content_evidence"]
    payload = assertion.payload
    dimensions = payload["dimensions"]
    expected_identity = _identity(
        result=payload["result"],
        subject=payload["assertion_subject"],
        scope=payload["assertion_scope"],
        content=dimensions["content"],
    )
    carried_assertion = next(
        (
            item
            for item in event.payload["assertions"]
            if item["dimensions"]["identity"] == assertion.assertion_id
        ),
        None,
    )
    evidence_edge = (
        assertion.recorded_occurrence_id == event.id
        and carried_assertion == payload
        and content_evidence is not None
        and event.payload.get("yield_evidence_id") == content_evidence.id
        and "assertions" in content_evidence.payload.get("yield_coordinates", [])
    )
    return {
        "identity": (
            EXACT if dimensions.get("identity") == expected_identity else CONTRADICTION
        ),
        # Evidence remains on the occurrence/result edge. It is read
        # through the exact locality, not copied from support_basis.
        "Evidence": EXACT if evidence_edge else MISSING,
        "provenance": EXACT if dimensions.get("source_provenance") else MISSING,
        "Scope": EXACT if payload.get("assertion_scope") else MISSING,
        "Authority": EXACT if dimensions.get("authority") else MISSING,
        "conflicts": UNKNOWN if payload.get("conflicts") == "Unknown" else MISSING,
        "limits": EXACT if payload.get("limits") else MISSING,
        "Unknowns": EXACT if payload.get("unknowns") else MISSING,
        "Standing": EXACT if dimensions.get("standing") else MISSING,
    }


def _applicability_witness(bundle: dict) -> dict[str, str]:
    applicability = bundle["applicability"]
    event = bundle["event"]
    act_evidence = bundle["act_evidence"]
    content_evidence = bundle["content_evidence"]
    content = applicability["dimensions"]["content"]
    treatment = applicability["coordinate_treatment"]
    input_edge = (
        act_evidence is not None
        and event.payload.get("input_assertion_reference")
        == applicability.get("input_assertion_reference")
        == act_evidence.payload.get("input_assertion_reference")
    )
    act_edge = (
        act_evidence is not None
        and event.payload.get("downstream_act_id")
        == applicability.get("downstream_act_id")
        == act_evidence.payload.get("downstream_act_id")
    )
    occurrence_edge = (
        act_evidence is not None
        and event.payload.get("applicability_act_occurrence_id")
        == applicability.get("applicability_act_occurrence_id")
        == act_evidence.payload.get("applicability_act_occurrence_id")
    )
    carried_result = (
        content_evidence is not None
        and event.payload.get("yield_evidence_id") == content_evidence.id
        and event.payload["dimensions"].get("standing")
        == applicability["dimensions"].get("standing")
    )
    return {
        "input_identity": EXACT if input_edge else MISSING,
        "exact_Act": EXACT if act_edge else MISSING,
        "subject": EXACT if content.get("downstream_act") else MISSING,
        "result_boundary": EXACT if applicability.get("result_boundary") else MISSING,
        "Scope": EXACT if applicability.get("scope_locality") else MISSING,
        "locality": EXACT if applicability.get("measurement_locality") else MISSING,
        "Authority": EXACT if applicability["dimensions"].get("authority") else MISSING,
        # The relation endpoints already identify the exact input role and the
        # exact addressed-Act role; no extra participant noun is supplied.
        "participants_and_roles": EXACT if input_edge and act_edge else MISSING,
        "provenance": (
            EXACT
            if applicability["dimensions"].get("source_provenance")
            else MISSING
        ),
        "Standing": (
            EXACT if carried_result else MISSING
        ),
        "support_relation_Standing": (
            INAPPLICABLE
            if treatment.get("support_relation_standing", {}).get("treatment")
            == "not established by Applicability"
            else MISSING
        ),
        "currentness": (
            INAPPLICABLE
            if treatment.get("currentness", {}).get("treatment")
            == "not required for this historical bounded source material"
            else MISSING
        ),
        "occurrence_identity": (
            EXACT if occurrence_edge else MISSING
        ),
        "known_loss": (
            UNKNOWN
            if treatment.get("known_loss", {}).get("treatment")
            == "not represented by input"
            else MISSING
        ),
        "conflicts": EXACT if "conflicts" in applicability else MISSING,
        "Unknowns": EXACT if applicability.get("unknowns") else MISSING,
        "negative_Authority": (
            EXACT if treatment.get("negative_authority") else MISSING
        ),
    }


def _occurrence_result_witness(bundle: dict) -> str:
    requirements = _occurrence_result_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _occurrence_result_requirements(bundle: dict) -> dict[str, bool]:
    ledger = bundle["ledger"]
    result_evidence = bundle["content_evidence"]
    responsible_act_evidence = bundle.get("act_evidence")

    def record_if_supplied_representation_changed(event):
        if event is None:
            return None
        stored = ledger.get(event.id)
        if stored == event:
            return event.id
        recorded = event.model_copy(
            deep=True,
            update={"id": new_id("yield_edge_pressure")},
        )
        ledger.append_many([recorded])
        return recorded.id

    result_evidence_id = record_if_supplied_representation_changed(result_evidence)
    responsible_act_evidence_id = record_if_supplied_representation_changed(
        responsible_act_evidence
    )

    event = bundle["event"].model_copy(deep=True)
    if (
        result_evidence is not None
        and result_evidence_id != result_evidence.id
        and event.payload.get("yield_evidence_id") == result_evidence.id
    ):
        event.payload["yield_evidence_id"] = result_evidence_id
    if (
        responsible_act_evidence is not None
        and responsible_act_evidence_id != responsible_act_evidence.id
        and event.payload.get("responsible_act_evidence_id")
        == responsible_act_evidence.id
    ):
        event.payload["responsible_act_evidence_id"] = (
            responsible_act_evidence_id
        )
    event_id = record_if_supplied_representation_changed(event)

    return read_yield_edge_requirements(
        ledger,
        recorded_result_event_id=event_id,
        result_evidence_event_id=result_evidence_id,
        responsible_act_evidence_event_id=responsible_act_evidence_id,
        recorded_result_occurrence_coordinate=bundle.get(
            "recorded_result_occurrence_coordinate", "act_occurrence_id"
        ),
        responsible_act_occurrence_coordinate=bundle.get(
            "act_evidence_occurrence_coordinate", "act_occurrence_id"
        ),
    )


def _emission_locality_witness(bundle: dict) -> str:
    requirements = _emission_locality_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    event_relation = event.payload.get("locality_relation")
    evidence_relation = evidence.payload.get("locality_relation")
    exact_relation = bool(
        isinstance(event_relation, dict)
        and isinstance(evidence_relation, dict)
        and event_relation.get("first_subject")
        == evidence_relation.get("first_subject")
        == event.payload.get("representation_reference")
        == evidence.payload.get("representation_reference")
        and event_relation.get("second_subject")
        == evidence_relation.get("second_subject")
        == event.payload.get("act_occurrence_id")
        == evidence.payload.get("act_occurrence_id")
        and event.payload.get("representation_event_id")
        == evidence.payload.get("representation_event_id")
        and event.payload.get("emitted_representation")
        == evidence.payload.get("carried_content")
    )
    exact_occurrence = bool(
        isinstance(event_relation, dict)
        and isinstance(evidence_relation, dict)
        and event_relation.get("relation_occurrence_id")
        == evidence_relation.get("relation_occurrence_id")
    )
    evidence_is_carried = event.payload.get("locality_evidence_id") == evidence.id
    return {
        "exact_relation": exact_relation and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _emission_attempt_locality_witness(bundle: dict) -> str:
    requirements = _emission_attempt_locality_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_attempt_locality_requirements(bundle: dict) -> dict[str, bool]:
    attempt = bundle["attempt"]
    evidence = bundle["attempt_locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        attempt.payload.get("representation")
        == evidence.payload.get("carried_content")
    )
    exact_occurrence = attempt.id == evidence.payload.get("attempt_event_id")
    exact_subject = (
        attempt.payload.get("representation_reference")
        == evidence.payload.get("representation_reference")
    )
    return {
        "exact_relation": exact_relation and exact_subject,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _emission_participation_witness(bundle: dict) -> str:
    requirements = _emission_participation_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _emission_participation_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["act_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_relation = (
        event.payload.get("representation_reference")
        == evidence.payload.get("representation_reference")
        and event.payload.get("input_role")
        == evidence.payload.get("input_role")
        == REPRESENTATION_EMISSION_INPUT_ROLE
    )
    exact_occurrence = (
        event.payload.get("act_occurrence_id")
        == evidence.payload.get("act_occurrence_id")
    )
    evidence_is_carried = (
        event.payload.get("responsible_act_evidence_id") == evidence.id
    )
    return {
        "exact_relation": exact_relation and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _representation_locality_witness(bundle: dict) -> str:
    requirements = _representation_locality_requirements(bundle)
    return EXACT if all(requirements.values()) else MISSING


def _representation_locality_requirements(bundle: dict) -> dict[str, bool]:
    event = bundle["event"]
    evidence = bundle["locality_evidence"]
    if evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    content = evidence.payload.get("carried_content")
    exact_content = isinstance(content, dict) and all(
        event.payload.get(key) == value for key, value in content.items()
    )
    exact_occurrence = (
        event.payload.get("act_occurrence_id")
        == evidence.payload.get("act_occurrence_id")
    )
    evidence_is_carried = event.payload.get("locality_evidence_id") == evidence.id
    return {
        "exact_relation": exact_content and evidence_is_carried,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(evidence.id) != CORRUPTED
        ),
    }


def _structural_edge_fidelity_cases() -> dict[str, dict[str, str]]:
    locality = _byte_measurement_road()
    alternate_locality = _byte_measurement_road()
    corrupted_locality = _byte_measurement_road()
    corrupted_locality["ledger"].mark_corrupted(corrupted_locality["event"].id)
    missing_locality = dict(locality)
    missing_event = locality["event"].model_copy(deep=True)
    missing_event.payload["assertions"] = [
        item
        for item in missing_event.payload["assertions"]
        if item["dimensions"]["identity"]
        != locality["source_assertion"].assertion_id
    ]
    missing_locality["event"] = missing_event
    unrelated_locality = dict(locality)
    unrelated_event = locality["event"].model_copy(deep=True)
    unrelated_event.payload["yield_evidence_id"] = "other-yield-evidence"
    unrelated_locality["event"] = unrelated_event

    participation = _recorded_applicability()
    alternate_participation = _recorded_applicability()
    corrupted_participation = _recorded_applicability()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["pair_act_evidence"].id
    )
    missing_participation = dict(participation)
    missing_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    missing_participation_evidence.payload["input_role"] = "different-role"
    missing_participation["pair_act_evidence"] = missing_participation_evidence
    wrong_participation = dict(participation)
    wrong_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    wrong_participation_evidence.payload["act_occurrence_id"] = (
        alternate_participation["pair_event"].payload["act_occurrence_id"]
    )
    wrong_participation["pair_act_evidence"] = wrong_participation_evidence
    unrelated_participation = dict(participation)
    unrelated_participation_event = participation["pair_event"].model_copy(
        deep=True
    )
    unrelated_participation_event.payload["yield_evidence_id"] = (
        "other-yield-evidence"
    )
    unrelated_participation["pair_event"] = unrelated_participation_event

    yielded = _byte_measurement_road()
    alternate_yield = _byte_measurement_road()
    corrupted_yield = _byte_measurement_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    missing_yield = dict(yielded)
    missing_yield_event = yielded["event"].model_copy(deep=True)
    missing_yield_event.payload["yield_evidence_id"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(yielded)
    wrong_yield_act_evidence = yielded["act_evidence"].model_copy(deep=True)
    wrong_yield_content_evidence = yielded["content_evidence"].model_copy(deep=True)
    alternate_yield_occurrence = alternate_yield["event"].payload[
        "act_occurrence_id"
    ]
    wrong_yield_act_evidence.payload["act_occurrence_id"] = (
        alternate_yield_occurrence
    )
    wrong_yield_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_yield_occurrence
    )
    wrong_yield["act_evidence"] = wrong_yield_act_evidence
    wrong_yield["content_evidence"] = wrong_yield_content_evidence
    unrelated_yield = dict(yielded)
    unrelated_yield_event = yielded["event"].model_copy(deep=True)
    unrelated_yield_event.payload["occurrence_preservation"] = (
        "different neighboring locality coordinate"
    )
    unrelated_yield["event"] = unrelated_yield_event

    return {
        "locality": {
            "exact": _assertion_locality_witness(
                locality,
                occurrence_id=locality["event"].id,
            ),
            "edge_missing": _assertion_locality_witness(
                missing_locality,
                occurrence_id=locality["event"].id,
            ),
            "wrong_occurrence": _assertion_locality_witness(
                locality,
                occurrence_id=alternate_locality["event"].id,
            ),
            "corrupted_evidence": _assertion_locality_witness(
                corrupted_locality,
                occurrence_id=corrupted_locality["event"].id,
            ),
            "unrelated_occurrence": _assertion_locality_witness(
                unrelated_locality,
                occurrence_id=locality["event"].id,
            ),
        },
        "participation": {
            "exact": _participation_witness(
                participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "edge_missing": _participation_witness(
                missing_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "wrong_occurrence": _participation_witness(
                wrong_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "corrupted_evidence": _participation_witness(
                corrupted_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
            "unrelated_occurrence": _participation_witness(
                unrelated_participation, role=BYTE_PAIR_INPUT_ROLE
            ),
        },
        "yield": {
            "exact": _occurrence_result_witness(yielded),
            "edge_missing": _occurrence_result_witness(missing_yield),
            "wrong_occurrence": _occurrence_result_witness(wrong_yield),
            "corrupted_evidence": _occurrence_result_witness(corrupted_yield),
            "unrelated_occurrence": _occurrence_result_witness(unrelated_yield),
        },
    }


def _successful_emission_requirement_bundles() -> dict[str, dict[str, dict]]:
    emission, alternate = _repeated_emission_attempt_road()

    missing_locality = dict(emission)
    missing_locality_evidence = emission["locality_evidence"].model_copy(deep=True)
    missing_locality_evidence.payload["carried_content"] = "different content"
    missing_locality["locality_evidence"] = missing_locality_evidence
    wrong_locality = dict(emission)
    wrong_locality_evidence = emission["locality_evidence"].model_copy(deep=True)
    wrong_locality_evidence.payload["locality_relation"][
        "relation_occurrence_id"
    ] = alternate["locality_evidence"].payload["locality_relation"][
        "relation_occurrence_id"
    ]
    wrong_locality["locality_evidence"] = wrong_locality_evidence
    unrelated_locality = dict(emission)
    unrelated_locality_event = emission["event"].model_copy(deep=True)
    unrelated_locality_event.payload["yield_evidence_id"] = "other-yield-evidence"
    unrelated_locality["event"] = unrelated_locality_event
    corrupted_locality = _emission_road()
    corrupted_locality["ledger"].mark_corrupted(
        corrupted_locality["locality_evidence"].id
    )

    missing_participation = dict(emission)
    missing_act_evidence = emission["act_evidence"].model_copy(deep=True)
    missing_act_evidence.payload["input_role"] = "different-role"
    missing_participation["act_evidence"] = missing_act_evidence
    wrong_participation = dict(emission)
    wrong_participation_event = emission["event"].model_copy(deep=True)
    wrong_participation_event.payload["responsible_act_evidence_id"] = alternate[
        "act_evidence"
    ].id
    wrong_participation["event"] = wrong_participation_event
    wrong_participation["act_evidence"] = alternate["act_evidence"]
    unrelated_participation = dict(emission)
    unrelated_participation_event = emission["event"].model_copy(deep=True)
    unrelated_participation_event.payload["locality_evidence_id"] = (
        "other-locality-evidence"
    )
    unrelated_participation["event"] = unrelated_participation_event
    corrupted_participation = _emission_road()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["act_evidence"].id
    )

    missing_yield = dict(emission)
    missing_yield_event = emission["event"].model_copy(deep=True)
    missing_yield_event.payload["yield_evidence_id"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(emission)
    wrong_yield_event = emission["event"].model_copy(deep=True)
    wrong_yield_event.payload["responsible_act_evidence_id"] = alternate[
        "act_evidence"
    ].id
    wrong_yield_event.payload["yield_evidence_id"] = alternate[
        "content_evidence"
    ].id
    wrong_yield["event"] = wrong_yield_event
    wrong_yield["act_evidence"] = alternate["act_evidence"]
    wrong_yield["content_evidence"] = alternate["content_evidence"]
    unrelated_yield = dict(emission)
    unrelated_yield_event = emission["event"].model_copy(deep=True)
    unrelated_yield_event.payload["input_role"] = "other-role"
    unrelated_yield["event"] = unrelated_yield_event
    corrupted_yield = _emission_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    return {
        "locality": {
            "exact": emission,
            "edge_missing": missing_locality,
            "wrong_occurrence": wrong_locality,
            "corrupted_evidence": corrupted_locality,
            "unrelated_occurrence": unrelated_locality,
        },
        "participation": {
            "exact": emission,
            "edge_missing": missing_participation,
            "wrong_occurrence": wrong_participation,
            "corrupted_evidence": corrupted_participation,
            "unrelated_occurrence": unrelated_participation,
        },
        "yield": {
            "exact": emission,
            "edge_missing": missing_yield,
            "wrong_occurrence": wrong_yield,
            "corrupted_evidence": corrupted_yield,
            "unrelated_occurrence": unrelated_yield,
        },
    }


def _emission_structural_edge_fidelity_cases() -> dict[str, dict[str, str]]:
    bundles = _successful_emission_requirement_bundles()
    witnesses = {
        "locality": _emission_locality_witness,
        "participation": _emission_participation_witness,
        "yield": _occurrence_result_witness,
    }
    return {
        edge: {case: witnesses[edge](bundle) for case, bundle in cases.items()}
        for edge, cases in bundles.items()
    }


def _yield_requirement_bundles(
    exact: dict,
    alternate: dict,
    corrupted: dict,
    *,
    unrelated_value,
) -> dict[str, dict]:
    missing = dict(exact)
    missing_event = exact["event"].model_copy(deep=True)
    missing_event.payload["yield_evidence_id"] = "missing-yield-evidence"
    missing["event"] = missing_event

    wrong_occurrence = dict(exact)
    wrong_act_evidence = (
        exact["act_evidence"].model_copy(deep=True)
        if exact.get("act_evidence") is not None
        else None
    )
    wrong_content_evidence = exact["content_evidence"].model_copy(deep=True)
    recorded_result_occurrence_coordinate = exact.get(
        "recorded_result_occurrence_coordinate", "act_occurrence_id"
    )
    act_evidence_occurrence_coordinate = exact.get(
        "act_evidence_occurrence_coordinate", "act_occurrence_id"
    )
    alternate_occurrence = alternate["event"].payload[
        recorded_result_occurrence_coordinate
    ]
    if wrong_act_evidence is not None:
        wrong_act_evidence.payload[act_evidence_occurrence_coordinate] = (
            alternate_occurrence
        )
    wrong_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_occurrence
    )
    if wrong_act_evidence is not None:
        wrong_occurrence["act_evidence"] = wrong_act_evidence
    wrong_occurrence["content_evidence"] = wrong_content_evidence

    unrelated = dict(exact)
    unrelated_event = exact["event"].model_copy(
        deep=True, update={"id": unrelated_value}
    )
    unrelated["event"] = unrelated_event

    corrupted["ledger"].mark_corrupted(corrupted["content_evidence"].id)
    return {
        "exact": exact,
        "edge_missing": missing,
        "wrong_occurrence": wrong_occurrence,
        "corrupted_evidence": corrupted,
        "unrelated_occurrence": unrelated,
    }


def _byte_pair_yield_requirement_bundles() -> dict[str, dict[str, dict]]:
    applicability = _recorded_applicability()
    alternate_applicability = _recorded_applicability()
    corrupted_applicability = _recorded_applicability()
    for bundle in (
        applicability,
        alternate_applicability,
        corrupted_applicability,
    ):
        bundle["recorded_result_occurrence_coordinate"] = (
            "applicability_act_occurrence_id"
        )
        bundle["act_evidence_occurrence_coordinate"] = (
            "applicability_act_occurrence_id"
        )

    pair = {
        "ledger": applicability["ledger"],
        "event": applicability["pair_event"],
        "act_evidence": applicability["pair_act_evidence"],
        "content_evidence": applicability["pair_content_evidence"],
    }
    alternate_pair = {
        "ledger": alternate_applicability["ledger"],
        "event": alternate_applicability["pair_event"],
        "act_evidence": alternate_applicability["pair_act_evidence"],
        "content_evidence": alternate_applicability["pair_content_evidence"],
    }
    corrupted_pair_source = _recorded_applicability()
    corrupted_pair = {
        "ledger": corrupted_pair_source["ledger"],
        "event": corrupted_pair_source["pair_event"],
        "act_evidence": corrupted_pair_source["pair_act_evidence"],
        "content_evidence": corrupted_pair_source["pair_content_evidence"],
    }

    return {
        "byte_pair_applicability": _yield_requirement_bundles(
            applicability,
            alternate_applicability,
            corrupted_applicability,
            unrelated_value=alternate_applicability["event"].id,
        ),
        "byte_pair_measurement": _yield_requirement_bundles(
            pair,
            alternate_pair,
            corrupted_pair,
            unrelated_value=alternate_pair["event"].id,
        ),
    }


def _remaining_yield_requirement_bundles() -> dict[str, dict[str, dict]]:
    roads = {
        "adjacency_pair_measurement": _adjacent_measurement_yield_road,
        "adjacency_pair_measurement_compare": (
            lambda: _adjacent_measurement_yield_road(compare=True)
        ),
        "assertion_yield_compare": _assertion_yield_compare_road,
        "assertion_locality_movement": _assertion_locality_movement_yield_road,
        "bounded_assertion_compare": _bounded_assertion_compare_yield_road,
        "locality_count_measurement": _locality_count_yield_road,
        "failed_emission_outcome": _failed_emission_yield_road,
        "material_ingest": _material_ingest_yield_road,
        "preserved_material_measurement": _preserved_material_yield_road,
        "recorded_finding_yield_compare": _recorded_finding_compare_yield_road,
    }
    boundaries = {}
    for boundary, road in roads.items():
        exact = road()
        alternate = road()
        corrupted = road()
        boundaries[boundary] = _yield_requirement_bundles(
            exact,
            alternate,
            corrupted,
            unrelated_value=alternate["event"].id,
        )
    return boundaries


def _locality_requirement_bundles(
    exact: dict, alternate: dict, corrupted: dict
) -> dict[str, dict]:
    missing = dict(exact)
    missing_evidence = exact["locality_evidence"].model_copy(deep=True)
    carried_content = missing_evidence.payload["carried_content"]
    if isinstance(carried_content, dict):
        missing_evidence.payload["carried_content"] = {
            **carried_content,
            next(iter(carried_content)): "different-carried-coordinate",
        }
    else:
        missing_evidence.payload["carried_content"] = "different-carried-content"
    missing["locality_evidence"] = missing_evidence

    wrong_occurrence = dict(exact)
    wrong_evidence = exact["locality_evidence"].model_copy(deep=True)
    wrong_evidence.payload["act_occurrence_id"] = alternate["event"].payload[
        "act_occurrence_id"
    ]
    wrong_occurrence["locality_evidence"] = wrong_evidence

    corrupted["ledger"].mark_corrupted(corrupted["locality_evidence"].id)
    unrelated = dict(exact)
    unrelated["event"] = exact["event"].model_copy(
        deep=True, update={"id": alternate["event"].id}
    )
    return {
        "exact": exact,
        "edge_missing": missing,
        "wrong_occurrence": wrong_occurrence,
        "corrupted_evidence": corrupted,
        "unrelated_occurrence": unrelated,
    }


def _remaining_locality_requirement_bundles() -> dict[str, dict[str, dict]]:
    roads = {
        "adjacency_pair_measurement": _adjacent_measurement_yield_road,
        "adjacency_pair_measurement_compare": (
            lambda: _adjacent_measurement_yield_road(compare=True)
        ),
    }
    return {
        boundary: _locality_requirement_bundles(road(), road(), road())
        for boundary, road in roads.items()
    }


def _additional_live_structural_edge_fidelity_cases() -> dict[
    tuple[str, str], dict[str, str]
]:
    representation, alternate_representation = _repeated_representation_road()
    missing_representation_locality = dict(representation)
    missing_representation_locality_evidence = representation[
        "locality_evidence"
    ].model_copy(deep=True)
    missing_representation_locality_evidence.payload["carried_content"][
        "representation_result"
    ] = "different result"
    missing_representation_locality[
        "locality_evidence"
    ] = missing_representation_locality_evidence
    wrong_representation_locality = dict(representation)
    wrong_representation_locality_evidence = representation[
        "locality_evidence"
    ].model_copy(deep=True)
    wrong_representation_locality_evidence.payload["act_occurrence_id"] = (
        alternate_representation["event"].payload["act_occurrence_id"]
    )
    wrong_representation_locality[
        "locality_evidence"
    ] = wrong_representation_locality_evidence
    corrupted_representation_locality = _representation_road()
    corrupted_representation_locality["ledger"].mark_corrupted(
        corrupted_representation_locality["locality_evidence"].id
    )
    unrelated_representation_locality = dict(representation)
    unrelated_representation_event = representation["event"].model_copy(deep=True)
    unrelated_representation_event.payload["yield_evidence_id"] = "other-yield"
    unrelated_representation_locality["event"] = unrelated_representation_event

    missing_representation_yield = dict(representation)
    missing_representation_yield_event = representation["event"].model_copy(
        deep=True
    )
    missing_representation_yield_event.payload["yield_evidence_id"] = (
        "missing-yield-evidence"
    )
    missing_representation_yield["event"] = missing_representation_yield_event
    wrong_representation_yield = dict(representation)
    wrong_representation_act_evidence = representation["act_evidence"].model_copy(
        deep=True
    )
    wrong_representation_content_evidence = representation[
        "content_evidence"
    ].model_copy(deep=True)
    alternate_occurrence = alternate_representation["event"].payload[
        "act_occurrence_id"
    ]
    wrong_representation_act_evidence.payload["act_occurrence_id"] = (
        alternate_occurrence
    )
    wrong_representation_content_evidence.payload["dimensions"][
        "act_occurrence_id"
    ] = alternate_occurrence
    wrong_representation_yield["act_evidence"] = wrong_representation_act_evidence
    wrong_representation_yield[
        "content_evidence"
    ] = wrong_representation_content_evidence
    corrupted_representation_yield = _representation_road()
    corrupted_representation_yield["ledger"].mark_corrupted(
        corrupted_representation_yield["content_evidence"].id
    )
    unrelated_representation_yield = dict(representation)
    unrelated_representation_yield_event = representation["event"].model_copy(
        deep=True
    )
    unrelated_representation_yield_event.payload["locality_evidence_id"] = (
        "other-locality"
    )
    unrelated_representation_yield["event"] = unrelated_representation_yield_event

    attempt, alternate_attempt = _repeated_emission_attempt_road()
    missing_attempt = dict(attempt)
    changed_relation_payload = dict(attempt["attempt_locality_evidence"].payload)
    changed_relation_payload["carried_content"] = "different carried content"
    missing_attempt["attempt_locality_evidence"] = attempt["ledger"].append(
        attempt["attempt_locality_evidence"].kind,
        changed_relation_payload,
        locality_id="repeated-emission-attempt",
    )
    wrong_attempt = dict(attempt)
    wrong_attempt["attempt_locality_evidence"] = alternate_attempt[
        "attempt_locality_evidence"
    ]
    corrupted_attempt, _ = _repeated_emission_attempt_road()
    corrupted_attempt["ledger"].mark_corrupted(
        corrupted_attempt["attempt_locality_evidence"].id
    )
    unrelated_attempt = dict(attempt)
    unrelated_attempt_event = attempt["attempt"].model_copy(deep=True)
    unrelated_attempt_event.payload["yield_evidence_id"] = "unrelated-yield"
    unrelated_attempt["attempt"] = unrelated_attempt_event

    return {
        ("locality", "representation_result"): {
            "exact": _representation_locality_witness(representation),
            "edge_missing": _representation_locality_witness(
                missing_representation_locality
            ),
            "wrong_occurrence": _representation_locality_witness(
                wrong_representation_locality
            ),
            "corrupted_evidence": _representation_locality_witness(
                corrupted_representation_locality
            ),
            "unrelated_occurrence": _representation_locality_witness(
                unrelated_representation_locality
            ),
        },
        ("yield", "representation_result"): {
            "exact": _occurrence_result_witness(representation),
            "edge_missing": _occurrence_result_witness(
                missing_representation_yield
            ),
            "wrong_occurrence": _occurrence_result_witness(
                wrong_representation_yield
            ),
            "corrupted_evidence": _occurrence_result_witness(
                corrupted_representation_yield
            ),
            "unrelated_occurrence": _occurrence_result_witness(
                unrelated_representation_yield
            ),
        },
        ("locality", "emission_attempt"): {
            "exact": _emission_attempt_locality_witness(attempt),
            "edge_missing": _emission_attempt_locality_witness(missing_attempt),
            "wrong_occurrence": _emission_attempt_locality_witness(wrong_attempt),
            "corrupted_evidence": _emission_attempt_locality_witness(
                corrupted_attempt
            ),
            "unrelated_occurrence": _emission_attempt_locality_witness(
                unrelated_attempt
            ),
        },
    }


def _live_structural_edge_fidelity_cases() -> dict[
    tuple[str, str], dict[str, str]
]:
    primary_boundaries = {
        "locality": "byte_measurement",
        "participation": "byte_pair_measurement",
        "yield": "byte_measurement",
    }
    registered = {
        (edge, primary_boundaries[edge]): cases
        for edge, cases in _structural_edge_fidelity_cases().items()
    }
    registered.update(
        {
            (edge, "successful_emission"): cases
            for edge, cases in _emission_structural_edge_fidelity_cases().items()
        }
    )
    registered.update(_additional_live_structural_edge_fidelity_cases())
    registered[("locality", "assertion_movement")] = _locality_fidelity_cases()
    registered[("locality", "assertion_compare_input")] = (
        _assertion_compare_input_locality_cases()
    )
    registered[("locality", "bounded_compare_input")] = (
        _bounded_compare_input_locality_cases()
    )
    registered[("locality", "operator_checkpoint")] = (
        _checkpoint_locality_cases()
    )
    registered.update(
        {
            ("yield", boundary): {
                case: _occurrence_result_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in _byte_pair_yield_requirement_bundles().items()
        }
    )
    registered.update(
        {
            ("yield", boundary): {
                case: _occurrence_result_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in _remaining_yield_requirement_bundles().items()
        }
    )
    registered.update(
        {
            ("locality", boundary): {
                case: _representation_locality_witness(bundle)
                for case, bundle in cases.items()
            }
            for boundary, cases in _remaining_locality_requirement_bundles().items()
        }
    )
    return registered


def test_primary_edge_measurements_preserve_their_live_boundaries():
    registered = _live_structural_edge_fidelity_cases()

    assert ("locality", "byte_measurement") in registered
    assert ("participation", "byte_pair_measurement") in registered
    assert ("yield", "byte_measurement") in registered
    assert ("locality", "assertion_movement") in registered


def _structural_edge_implementation_specs() -> dict[str, dict]:
    requirements = {
        "exact_relation": "edge_missing",
        "occurrence_witness": "wrong_occurrence",
        "intact_evidence": "corrupted_evidence",
    }
    return {
        "locality": {
            "from": "first_subject",
            "to": "second_subject",
            "requires": requirements,
        },
        "participation": {
            "from": "subject",
            "to": "Act_occurrence",
            "coordinate": "role",
            "requires": requirements,
        },
        "yield": {
            "from": "Act_occurrence",
            "to": "result",
            "preserves": ["Act_occurrence_identity", "result_identity"],
            "equal_result_content_establishes_identity": False,
            "requires": requirements,
        },
    }


def _assert_structural_edge_anatomy(grammar: dict, specs: dict[str, dict]) -> None:
    assert set(specs) == set(grammar["structural_edges"])
    relation_families = grammar["implementation_witness"]["relation_audit"][
        "families"
    ]
    for edge, declared in grammar["structural_edges"].items():
        witnessed = specs[edge]
        declared_anatomy = {
            key: value
            for key, value in declared.items()
            if key not in {"book_clause", "requires"}
        }
        witnessed_anatomy = {
            key: value for key, value in witnessed.items() if key != "requires"
        }
        assert witnessed_anatomy == declared_anatomy
        assert list(witnessed["requires"]) == declared["requires"]
        assert declared["requires"] == relation_families[edge]


def _act_occurrence_witness(bundle: dict) -> dict[str, str]:
    event = bundle["event"]
    act_evidence = bundle["act_evidence"]
    assignment = event.payload["responsibility_assignment_evidence"]
    joined = (
        act_evidence is not None
        and event.payload["downstream_act_id"]
        == act_evidence.payload["downstream_act_id"]
        and event.payload["act_occurrence_id"]
        == act_evidence.payload["act_occurrence_id"]
        and event.payload["responsibility"]
        == act_evidence.payload["responsibility"]
        and event.payload["responsible_boundary"]
        == act_evidence.payload["responsible_boundary"]
        and assignment
        == act_evidence.payload.get("responsibility_assignment_evidence")
    )
    return {
        "Responsibility": EXACT if joined else MISSING,
        "Responsibility_assignment_Standing": (
            EXACT if joined and assignment.get("standing") == "assigned" else MISSING
        ),
        "responsible_boundary": EXACT if joined else MISSING,
        "exact_Act": EXACT if joined else MISSING,
        "Act_occurrence": EXACT if joined else MISSING,
        "occurrence_Evidence": (
            EXACT
            if joined
            and event.payload["responsible_act_evidence_id"] == act_evidence.id
            else MISSING
        ),
        "Authority": (
            EXACT if joined and act_evidence.payload.get("authority") else MISSING
        ),
        "Scope": (
            EXACT
            if event.locality_id is not None
            and assignment.get("completeness_boundary")
            else MISSING
        ),
        "limits": (
            EXACT if event.payload["dimensions"].get("authority") else MISSING
        ),
    }


def _locality_requirements(bundle: dict) -> dict[str, bool]:
    ledger = bundle["ledger"]
    movement = bundle["movement"]
    act_evidence = bundle["movement_act_evidence"]
    relation = movement.payload.get("locality_relation")
    evidence_relation = (
        act_evidence.payload.get("locality_relation")
        if act_evidence is not None
        else None
    )
    return {
        "exact_relation": bool(
            isinstance(relation, dict)
            and isinstance(evidence_relation, dict)
            and relation.get("first_subject")
            == evidence_relation.get("first_subject")
            == movement.payload.get("source_assertion_reference")
            and relation.get("second_subject")
            == evidence_relation.get("second_subject")
            == movement.payload.get("destination_locality")
        ),
        "occurrence_witness": bool(
            isinstance(relation, dict)
            and isinstance(evidence_relation, dict)
            and relation.get("relation_occurrence_id")
            == evidence_relation.get("relation_occurrence_id")
            == movement.payload.get("movement_act_occurrence_id")
        ),
        "intact_evidence": bool(
            act_evidence is not None
            and movement.payload.get("movement_act_evidence_event_id")
            == act_evidence.id
            and ledger.integrity_of(act_evidence.id) != CORRUPTED
        ),
    }


def _locality_witness(bundle: dict) -> str:
    return EXACT if all(_locality_requirements(bundle).values()) else MISSING


def _locality_fidelity_cases() -> dict[str, str]:
    exact = _recorded_applicability()

    edge_missing = _recorded_applicability()
    edge_missing["movement"].payload["locality_relation"]["second_subject"] = (
        "another bounded subject"
    )

    wrong_occurrence = _recorded_applicability()
    source_occurrence = wrong_occurrence["ledger"].get(
        wrong_occurrence["movement"].payload["source_assertion_reference"][
            "recorded_occurrence_id"
        ]
    )
    wrong_occurrence["movement_act_evidence"].payload["locality_relation"][
        "relation_occurrence_id"
    ] = source_occurrence.id

    corrupted_evidence = _recorded_applicability()
    corrupted_evidence["ledger"].mark_corrupted(
        corrupted_evidence["movement_act_evidence"].id
    )

    unrelated_occurrence = _recorded_applicability()
    unrelated_occurrence["movement"].payload["movement_scope"] = "another description"

    return {
        "exact": _locality_witness(exact),
        "edge_missing": _locality_witness(edge_missing),
        "wrong_occurrence": _locality_witness(wrong_occurrence),
        "corrupted_evidence": _locality_witness(corrupted_evidence),
        "unrelated_occurrence": _locality_witness(unrelated_occurrence),
    }


def _participation_witness(bundle: dict, *, role: str) -> str:
    requirements = _participation_requirements(bundle, role=role)
    return EXACT if all(requirements.values()) else MISSING


def _participation_requirements(bundle: dict, *, role: str) -> dict[str, bool]:
    applicability = bundle["applicability"]
    pair = bundle["pair_event"]
    act_evidence = bundle["pair_act_evidence"]
    if act_evidence is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    exact_subject = (
        applicability["input_assertion_reference"]
        == pair.payload["source_assertion_reference"]
        == act_evidence.payload["input_assertion_reference"]
    )
    exact_role = (
        role
        == applicability["input_role"]
        == pair.payload["input_role"]
        == act_evidence.payload["input_role"]
    )
    exact_occurrence = (
        pair.payload["act_occurrence_id"]
        == act_evidence.payload["act_occurrence_id"]
    )
    applicable_to_act = (
        applicability["dimensions"]["standing"] == "applicable"
        and applicability["downstream_act_id"] == pair.payload["downstream_act_id"]
        and applicability["dimensions"]["identity"]
        == act_evidence.payload["input_applicability_identity"]
    )
    return {
        "exact_relation": exact_subject and exact_role and applicable_to_act,
        "occurrence_witness": exact_occurrence,
        "intact_evidence": (
            bundle["ledger"].integrity_of(act_evidence.id) != CORRUPTED
        ),
    }


def test_implementation_witness_discriminates_content_and_locality():
    grammar = _witness_grammar()
    ledger = EventLedger()
    content = {"a": 1, "b": 2}

    first = ledger.append("test.locality", dict(content), locality_id="s")
    second = ledger.append("test.locality", dict(content), locality_id="t")
    assert first.payload == second.payload
    assert first.locality_id != second.locality_id

    changed_content = ledger.append(
        "test.locality", {"a": 1, "b": 3}, locality_id="s"
    )
    assert first.payload != changed_content.payload
    assert first.locality_id == changed_content.locality_id

    assert grammar["discriminators"] == ["content", "locality"]
    assert grammar["non_equivalence"] == [
        ["content", "locality"],
    ]


def test_fidelity_is_this_seeds_bounded_machine_comparison():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    assert grammar["fidelity"] == {
        "book_clause": "01.Source.C",
        "subject": "this_Seed",
        "expectation": "machine_grammar",
        "comparison": "deterministic_tests",
        "witness": "live_implementation",
        "result": "bounded_Fidelity_finding",
        "does_not_establish": "global_certification",
    }


def test_every_structural_edge_has_live_fidelity_cases():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    cases = _structural_edge_fidelity_cases()
    specs = _structural_edge_implementation_specs()
    expected = grammar["implementation_witness"]["fidelity_cases"]

    _assert_structural_edge_anatomy(grammar, specs)
    assert set(cases) == set(grammar["structural_edges"])
    assert all(set(edge_cases) == set(expected) for edge_cases in cases.values())
    assert cases == {
        edge: expected for edge in grammar["structural_edges"]
    }
    for edge, spec in specs.items():
        for adversary in spec["requires"].values():
            assert cases[edge][adversary] == MISSING


def test_emission_instantiates_each_edge_it_carries_at_its_boundary():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    cases = _emission_structural_edge_fidelity_cases()
    expected = grammar["implementation_witness"]["fidelity_cases"]

    assert set(cases) == {"locality", "participation", "yield"}
    assert set(cases) == set(grammar["structural_edges"])
    assert cases == {edge: expected for edge in cases}


def test_every_registered_live_edge_instantiation_obeys_the_full_fidelity_matrix():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    expected = grammar["implementation_witness"]["fidelity_cases"]
    registered = _live_structural_edge_fidelity_cases()

    assert registered
    assert {edge for edge, _boundary in registered} == set(
        grammar["structural_edges"]
    )
    assert all(cases == expected for cases in registered.values())
    assert ("locality", "representation_result") in registered
    assert ("locality", "emission_attempt") in registered
    assert {
        boundary for edge, boundary in registered if edge == "yield"
    } == set(YIELD_LIVE_BOUNDARIES)


def test_every_yield_evidence_site_declares_its_live_boundary():
    declared: list[str] = []
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name):
                continue
            if node.func.id != "_record_yield_evidence":
                continue
            boundary = next(
                (keyword.value for keyword in node.keywords if keyword.arg == "live_boundary"),
                None,
            )
            assert isinstance(boundary, ast.Constant), (
                f"{path.name}:{node.lineno} must declare one literal live_boundary"
            )
            assert isinstance(boundary.value, str) and boundary.value
            declared.append(boundary.value)

    assert len(declared) == len(set(declared))
    assert set(declared) == set(YIELD_LIVE_BOUNDARIES)


def test_byte_pair_yield_adversaries_change_one_requirement_each():
    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
    }
    boundaries = _byte_pair_yield_requirement_bundles()

    assert {
        boundary: {
            case: tuple(_occurrence_result_requirements(bundle).values())
            for case, bundle in cases.items()
        }
        for boundary, cases in boundaries.items()
    } == {boundary: expected for boundary in boundaries}


def test_remaining_yield_adversaries_change_one_requirement_each():
    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
    }
    boundaries = _remaining_yield_requirement_bundles()

    assert {
        boundary: {
            case: tuple(_occurrence_result_requirements(bundle).values())
            for case, bundle in cases.items()
        }
        for boundary, cases in boundaries.items()
    } == {boundary: expected for boundary in boundaries}


def test_remaining_locality_adversaries_change_one_requirement_each():
    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
    }
    boundaries = _remaining_locality_requirement_bundles()
    assert {
        boundary: {
            case: tuple(_representation_locality_requirements(bundle).values())
            for case, bundle in cases.items()
        }
        for boundary, cases in boundaries.items()
    } == {boundary: expected for boundary in boundaries}


def test_emission_attempt_locality_adversaries_change_one_requirement_each():
    exact, alternate = _repeated_emission_attempt_road()
    wrong_occurrence = dict(exact)
    wrong_occurrence["attempt_locality_evidence"] = alternate[
        "attempt_locality_evidence"
    ]

    missing_relation = dict(exact)
    different = dict(exact["attempt_locality_evidence"].payload)
    different["carried_content"] = "different carried content"
    missing_relation["attempt_locality_evidence"] = exact["ledger"].append(
        exact["attempt_locality_evidence"].kind,
        different,
        locality_id="repeated-emission-attempt",
    )

    corrupted, _ = _repeated_emission_attempt_road()
    corrupted["ledger"].mark_corrupted(
        corrupted["attempt_locality_evidence"].id
    )

    unrelated = dict(exact)
    unrelated_attempt = exact["attempt"].model_copy(deep=True)
    unrelated_attempt.payload["yield_evidence_id"] = "unrelated-yield"
    unrelated["attempt"] = unrelated_attempt

    assert _emission_attempt_locality_requirements(exact) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_attempt_locality_requirements(missing_relation) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_attempt_locality_requirements(wrong_occurrence) == {
        "exact_relation": True,
        "occurrence_witness": False,
        "intact_evidence": True,
    }
    assert _emission_attempt_locality_requirements(corrupted) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": False,
    }
    assert _emission_attempt_locality_requirements(unrelated) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_successful_emission_adversaries_change_one_requirement_each():
    bundles = _successful_emission_requirement_bundles()
    requirement_witnesses = {
        "locality": _emission_locality_requirements,
        "participation": _emission_participation_requirements,
        "yield": _occurrence_result_requirements,
    }
    expected = {
        "exact": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
        "edge_missing": {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
        "wrong_occurrence": {
            "exact_relation": True,
            "occurrence_witness": False,
            "intact_evidence": True,
        },
        "corrupted_evidence": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": False,
        },
        "unrelated_occurrence": {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        },
    }

    assert {
        edge: {
            case: requirement_witnesses[edge](bundle)
            for case, bundle in cases.items()
        }
        for edge, cases in bundles.items()
    } == {edge: expected for edge in bundles}


def test_representation_result_adversaries_change_one_requirement_each():
    exact, alternate = _repeated_representation_road()

    missing_locality = dict(exact)
    missing_locality_evidence = exact["locality_evidence"].model_copy(deep=True)
    missing_locality_evidence.payload["carried_content"][
        "representation_result"
    ] = "different result"
    missing_locality["locality_evidence"] = missing_locality_evidence
    wrong_locality = dict(exact)
    wrong_locality_evidence = exact["locality_evidence"].model_copy(deep=True)
    wrong_locality_evidence.payload["act_occurrence_id"] = alternate[
        "event"
    ].payload["act_occurrence_id"]
    wrong_locality["locality_evidence"] = wrong_locality_evidence
    corrupted_locality = _representation_road()
    corrupted_locality["ledger"].mark_corrupted(
        corrupted_locality["locality_evidence"].id
    )
    unrelated_locality = dict(exact)
    unrelated_event = exact["event"].model_copy(deep=True)
    unrelated_event.payload["yield_evidence_id"] = "different-yield-evidence"
    unrelated_locality["event"] = unrelated_event

    missing_yield = dict(exact)
    missing_yield_event = exact["event"].model_copy(deep=True)
    missing_yield_event.payload["yield_evidence_id"] = "missing-yield-evidence"
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(exact)
    wrong_act_evidence = exact["act_evidence"].model_copy(deep=True)
    wrong_content_evidence = exact["content_evidence"].model_copy(deep=True)
    alternate_occurrence = alternate["event"].payload["act_occurrence_id"]
    wrong_act_evidence.payload["act_occurrence_id"] = alternate_occurrence
    wrong_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["content_evidence"] = wrong_content_evidence
    corrupted_yield = _representation_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    unrelated_yield = dict(exact)
    unrelated_yield_event = exact["event"].model_copy(deep=True)
    unrelated_yield_event.payload["locality_evidence_id"] = "different-locality"
    unrelated_yield["event"] = unrelated_yield_event

    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
    }
    bundles = {
        "locality": {
            "exact": exact,
            "edge_missing": missing_locality,
            "wrong_occurrence": wrong_locality,
            "corrupted_evidence": corrupted_locality,
            "unrelated_occurrence": unrelated_locality,
        },
        "yield": {
            "exact": exact,
            "edge_missing": missing_yield,
            "wrong_occurrence": wrong_yield,
            "corrupted_evidence": corrupted_yield,
            "unrelated_occurrence": unrelated_yield,
        },
    }
    witnesses = {
        "locality": _representation_locality_requirements,
        "yield": _occurrence_result_requirements,
    }

    assert {
        edge: {
            case: tuple(witnesses[edge](bundle).values())
            for case, bundle in cases.items()
        }
        for edge, cases in bundles.items()
    } == {edge: expected for edge in bundles}


def test_byte_measurement_adversaries_change_one_requirement_each():
    locality = _byte_measurement_road()
    alternate_locality = _byte_measurement_road()
    missing_locality = dict(locality)
    missing_event = locality["event"].model_copy(deep=True)
    missing_event.payload["assertions"] = []
    missing_locality["event"] = missing_event
    corrupted_locality = _byte_measurement_road()
    corrupted_locality["ledger"].mark_corrupted(corrupted_locality["event"].id)
    unrelated_locality = dict(locality)
    unrelated_event = locality["event"].model_copy(deep=True)
    unrelated_event.payload["yield_evidence_id"] = "different-yield-evidence"
    unrelated_locality["event"] = unrelated_event

    participation = _recorded_applicability()
    alternate_participation = _recorded_applicability()
    missing_participation = dict(participation)
    missing_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    missing_participation_evidence.payload["input_role"] = "different-role"
    missing_participation["pair_act_evidence"] = missing_participation_evidence
    wrong_participation = dict(participation)
    wrong_participation_evidence = participation[
        "pair_act_evidence"
    ].model_copy(deep=True)
    wrong_participation_evidence.payload["act_occurrence_id"] = (
        alternate_participation["pair_event"].payload["act_occurrence_id"]
    )
    wrong_participation["pair_act_evidence"] = wrong_participation_evidence
    corrupted_participation = _recorded_applicability()
    corrupted_participation["ledger"].mark_corrupted(
        corrupted_participation["pair_act_evidence"].id
    )
    unrelated_participation = dict(participation)
    unrelated_pair = participation["pair_event"].model_copy(deep=True)
    unrelated_pair.payload["yield_evidence_id"] = "different-yield-evidence"
    unrelated_participation["pair_event"] = unrelated_pair

    yielded = _byte_measurement_road()
    alternate_yield = _byte_measurement_road()
    missing_yield = dict(yielded)
    missing_yield_event = yielded["event"].model_copy(deep=True)
    missing_yield_event.payload["yield_evidence_id"] = (
        "missing-yield-evidence"
    )
    missing_yield["event"] = missing_yield_event
    wrong_yield = dict(yielded)
    wrong_act_evidence = yielded["act_evidence"].model_copy(deep=True)
    wrong_content_evidence = yielded["content_evidence"].model_copy(deep=True)
    alternate_occurrence = alternate_yield["event"].payload["act_occurrence_id"]
    wrong_act_evidence.payload["act_occurrence_id"] = alternate_occurrence
    wrong_content_evidence.payload["dimensions"]["act_occurrence_id"] = (
        alternate_occurrence
    )
    wrong_yield["act_evidence"] = wrong_act_evidence
    wrong_yield["content_evidence"] = wrong_content_evidence
    corrupted_yield = _byte_measurement_road()
    corrupted_yield["ledger"].mark_corrupted(
        corrupted_yield["content_evidence"].id
    )
    unrelated_yield = dict(yielded)
    unrelated_yield_event = yielded["event"].model_copy(deep=True)
    unrelated_yield_event.payload["occurrence_preservation"] = "different"
    unrelated_yield["event"] = unrelated_yield_event

    expected = {
        "exact": (True, True, True),
        "edge_missing": (False, True, True),
        "wrong_occurrence": (True, False, True),
        "corrupted_evidence": (True, True, False),
        "unrelated_occurrence": (True, True, True),
    }
    actual = {
        "locality": {
            "exact": _assertion_locality_requirements(
                locality, occurrence_id=locality["event"].id
            ),
            "edge_missing": _assertion_locality_requirements(
                missing_locality, occurrence_id=locality["event"].id
            ),
            "wrong_occurrence": _assertion_locality_requirements(
                locality, occurrence_id=alternate_locality["event"].id
            ),
            "corrupted_evidence": _assertion_locality_requirements(
                corrupted_locality,
                occurrence_id=corrupted_locality["event"].id,
            ),
            "unrelated_occurrence": _assertion_locality_requirements(
                unrelated_locality, occurrence_id=locality["event"].id
            ),
        },
        "participation": {
            case: _participation_requirements(bundle, role=BYTE_PAIR_INPUT_ROLE)
            for case, bundle in {
                "exact": participation,
                "edge_missing": missing_participation,
                "wrong_occurrence": wrong_participation,
                "corrupted_evidence": corrupted_participation,
                "unrelated_occurrence": unrelated_participation,
            }.items()
        },
        "yield": {
            case: _occurrence_result_requirements(bundle)
            for case, bundle in {
                "exact": yielded,
                "edge_missing": missing_yield,
                "wrong_occurrence": wrong_yield,
                "corrupted_evidence": corrupted_yield,
                "unrelated_occurrence": unrelated_yield,
            }.items()
        },
    }

    assert {
        edge: {case: tuple(requirements.values()) for case, requirements in cases.items()}
        for edge, cases in actual.items()
    } == {edge: expected for edge in actual}


def test_attempt_and_success_have_distinct_locality_relations_for_the_same_text():
    emission = _emission_road()
    alternate = _emission_road()
    wrong_attempt = dict(emission)
    wrong_attempt["attempt_locality_evidence"] = alternate[
        "attempt_locality_evidence"
    ]
    success_evidence_in_attempt_slot = dict(emission)
    success_evidence_in_attempt_slot["attempt_locality_evidence"] = emission[
        "locality_evidence"
    ]

    assert emission["attempt"].payload["representation"] == emission[
        "event"
    ].payload["emitted_representation"]
    assert _emission_attempt_locality_witness(emission) == EXACT
    assert _emission_attempt_locality_witness(wrong_attempt) == MISSING
    assert (
        _emission_attempt_locality_witness(success_evidence_in_attempt_slot)
        == MISSING
    )


def test_successful_emission_locality_binds_the_exact_representation():
    exact = _emission_road()
    different = dict(exact)
    evidence = exact["locality_evidence"].model_copy(deep=True)
    evidence.payload["representation_reference"] = "another-representation"
    evidence.payload["locality_relation"]["first_subject"] = (
        "another-representation"
    )
    different["locality_evidence"] = evidence

    assert _emission_locality_requirements(exact) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _emission_locality_requirements(different) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def test_representation_act_has_an_exact_yield_edge_without_asserting_participation():
    representation = _representation_road()
    alternate = _representation_road()
    missing = dict(representation)
    missing["content_evidence"] = None
    wrong_occurrence = dict(representation)
    wrong_occurrence["content_evidence"] = alternate["content_evidence"]
    missing_locality = dict(representation)
    missing_locality["locality_evidence"] = None
    wrong_locality = dict(representation)
    wrong_locality["locality_evidence"] = alternate["locality_evidence"]

    assert _representation_locality_witness(representation) == EXACT
    assert _representation_locality_witness(missing_locality) == MISSING
    assert _representation_locality_witness(wrong_locality) == MISSING
    assert _occurrence_result_witness(representation) == EXACT
    assert _occurrence_result_witness(missing) == MISSING
    assert _occurrence_result_witness(wrong_occurrence) == MISSING
    assert "input_role" not in representation["event"].payload


def test_changed_structural_edge_anatomy_is_detected():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    grammar["structural_edges"]["yield"]["from"] = "result"

    try:
        _assert_structural_edge_anatomy(
            grammar, _structural_edge_implementation_specs()
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("reversed Yield anatomy escaped implementation Fidelity")


def test_content_and_locality_endpoints_do_not_establish_locality_relation():
    ledger = EventLedger()
    content = {"subject": "x", "standing": "Unknown"}
    locality = ledger.append("test.locality", dict(content), locality_id="s")

    assert (
        _content_locality_witness(
            content, locality=locality, occurrence_id=locality.id
        )
        == EXACT
    )
    second_locality = ledger.append(
        "test.locality", dict(content), locality_id="s"
    )
    assert content
    assert second_locality.payload == locality.payload
    assert second_locality.id != locality.id
    assert (
        _content_locality_witness(
            content,
            locality=second_locality,
            occurrence_id=locality.id,
        )
        == MISSING
    )


def test_assertion_clause_is_checked_against_a_live_byte_assertion():
    clause = _clause("01.Standing.D.1")
    witness = _assertion_witness(_byte_measurement_road())

    assert set(witness) == {"identity", *clause["responsibility"]["coordinates"]}
    assert witness == {
        "identity": EXACT,
        "Evidence": EXACT,
        "provenance": EXACT,
        "Scope": EXACT,
        "Authority": EXACT,
        "conflicts": UNKNOWN,
        "limits": EXACT,
        "Unknowns": EXACT,
        "Standing": EXACT,
    }


def test_asserted_content_identity_includes_scope_but_not_locality():
    ledger = EventLedger()
    for locality_id in ("source-one", "source-two"):
        run_persistent_operator_console(
            ledger=ledger,
            locality_id=locality_id,
            input_stream=binary_input("t\n"),
            output_stream=StringIO(),
        )

    first = record_byte_count_layer(
        ledger,
        source_locality_ids=("source-one",),
        recording_locality_id="measurement-one",
    )
    repeated = record_byte_count_layer(
        ledger,
        source_locality_ids=("source-one",),
        recording_locality_id="measurement-two",
    )
    other_scope = record_byte_count_layer(
        ledger,
        source_locality_ids=("source-two",),
        recording_locality_id="measurement-three",
    )

    def count_assertion(event):
        return next(
            assertion
            for assertion in event.payload["assertions"]
            if assertion["result"] == "count"
            and assertion["assertion_subject"].get("byte_hex") == "74"
        )

    first_assertion = count_assertion(first)
    repeated_assertion = count_assertion(repeated)
    other_scope_assertion = count_assertion(other_scope)
    assert first_assertion["dimensions"]["content"] == repeated_assertion[
        "dimensions"
    ]["content"]
    assert first_assertion["dimensions"]["identity"] == repeated_assertion[
        "dimensions"
    ]["identity"]
    assert first.id != repeated.id
    assert first_assertion["dimensions"]["content"] == other_scope_assertion[
        "dimensions"
    ]["content"]
    assert first_assertion["assertion_scope"] != other_scope_assertion[
        "assertion_scope"
    ]
    assert first_assertion["dimensions"]["identity"] != other_scope_assertion[
        "dimensions"
    ]["identity"]


def test_applicability_clause_is_checked_against_a_live_pair_determination():
    clause = _clause("01.Standing.E.1")
    witness = _applicability_witness(_recorded_applicability())

    assert set(witness) == set(clause["coordinates"])
    assert witness == {
        "input_identity": EXACT,
        "exact_Act": EXACT,
        "subject": EXACT,
        "result_boundary": EXACT,
        "Scope": EXACT,
        "locality": EXACT,
        "Authority": EXACT,
        "participants_and_roles": EXACT,
        "provenance": EXACT,
        "Standing": EXACT,
        "support_relation_Standing": INAPPLICABLE,
        "currentness": INAPPLICABLE,
        "occurrence_identity": EXACT,
        "known_loss": UNKNOWN,
        "conflicts": EXACT,
        "Unknowns": EXACT,
        "negative_Authority": EXACT,
    }


def test_input_is_an_open_act_local_role_before_participation():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    bundle = _recorded_applicability()
    applicability = bundle["applicability"]

    assert grammar["input_role"] == {
        "kind": "Act_local_role",
        "preserves_subject_identity": True,
        "distinct_from": [
            "subject",
            "locality",
            "Applicability",
            "Admission",
            "participation",
            "input_to_result_support",
        ],
    }
    assert applicability["input_role"] == BYTE_PAIR_INPUT_ROLE
    assert applicability["downstream_act_occurrence_id"] is None


def test_participation_requires_exact_subject_role_and_act_occurrence():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    bundle = _recorded_applicability()

    assert grammar["structural_edges"]["participation"] == {
        "book_clause": "01.Standing.E.1",
        "from": "subject",
        "to": "Act_occurrence",
        "coordinate": "role",
        "requires": ["exact_relation", "occurrence_witness", "intact_evidence"],
    }
    assert _participation_witness(bundle, role=BYTE_PAIR_INPUT_ROLE) == EXACT
    assert _participation_witness(bundle, role="some other role") == MISSING

    assert bundle["applicability"]["dimensions"]["standing"] == "applicable"
    assert bundle["pair_event"].payload["act_occurrence_id"]
    bundle["pair_act_evidence"] = None
    assert _participation_witness(bundle, role=BYTE_PAIR_INPUT_ROLE) == MISSING


def test_unjoined_endpoints_do_not_witness_an_input_to_act_relation():
    grammar = _witness_grammar()
    bundle = _recorded_applicability()
    bundle["act_evidence"] = None
    witness = _applicability_witness(bundle)

    assert bundle["applicability"]["input_assertion_reference"]
    assert bundle["applicability"]["downstream_act_id"]
    assert bundle["applicability"]["applicability_act_occurrence_id"]
    assert grammar["relation_audit"] == {
        "endpoint_presence_establishes_relation": False,
        "families": {
            "candidate_participation": ["exact_relation", "occurrence_witness"],
            "participation": [
                "exact_relation",
                "occurrence_witness",
                "intact_evidence",
            ],
            "locality": [
                "exact_relation",
                "occurrence_witness",
                "intact_evidence",
            ],
            "yield": ["exact_relation", "occurrence_witness", "intact_evidence"],
        },
    }
    assert witness["input_identity"] == MISSING
    assert witness["exact_Act"] == MISSING
    assert witness["occurrence_identity"] == MISSING


def test_locality_relation_clause_is_checked_against_the_live_pair_road():
    clause = _clause("06.Standing.B")
    bundle = _recorded_applicability()
    relation = bundle["movement"].payload["locality_relation"]

    assert clause["identity"] == [
        "first_subject",
        "second_subject",
        "relation_occurrence",
    ]
    assert clause["requires"] == list(_locality_requirements(bundle))
    assert relation["first_subject"] == bundle["movement"].payload[
        "source_assertion_reference"
    ]
    assert relation["second_subject"] == bundle["movement"].payload[
        "destination_locality"
    ]
    assert _locality_witness(bundle) == EXACT


def test_locality_fans_out_orthogonal_adversaries_for_each_live_road():
    exact = _recorded_applicability()

    edge_missing = _recorded_applicability()
    edge_missing["movement"].payload["locality_relation"]["second_subject"] = (
        "another bounded subject"
    )

    wrong_occurrence = _recorded_applicability()
    source_occurrence = wrong_occurrence["ledger"].get(
        wrong_occurrence["movement"].payload["source_assertion_reference"][
            "recorded_occurrence_id"
        ]
    )
    wrong_occurrence["movement_act_evidence"].payload["locality_relation"][
        "relation_occurrence_id"
    ] = source_occurrence.id

    corrupted_evidence = _recorded_applicability()
    corrupted_evidence["ledger"].mark_corrupted(
        corrupted_evidence["movement_act_evidence"].id
    )

    unrelated_occurrence = _recorded_applicability()
    unrelated_occurrence["movement"].payload["movement_scope"] = "another description"

    cases = {
        "exact": exact,
        "edge_missing": edge_missing,
        "wrong_occurrence": wrong_occurrence,
        "corrupted_evidence": corrupted_evidence,
        "unrelated_occurrence": unrelated_occurrence,
    }
    assert {name: _locality_witness(case) for name, case in cases.items()} == {
        "exact": EXACT,
        "edge_missing": MISSING,
        "wrong_occurrence": MISSING,
        "corrupted_evidence": MISSING,
        "unrelated_occurrence": EXACT,
    }
    assert _locality_requirements(edge_missing) == {
        "exact_relation": False,
        "occurrence_witness": True,
        "intact_evidence": True,
    }
    assert _locality_requirements(wrong_occurrence) == {
        "exact_relation": True,
        "occurrence_witness": False,
        "intact_evidence": True,
    }
    assert _locality_requirements(corrupted_evidence) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": False,
    }


def test_occurrence_and_result_endpoints_do_not_establish_their_relation():
    bundle = _byte_measurement_road()
    assert _occurrence_result_witness(bundle) == EXACT

    event = bundle["event"]
    assert event.payload["act_occurrence_id"]
    assert event.payload["assertions"]
    bundle["content_evidence"] = None
    assert _occurrence_result_witness(bundle) == MISSING


def test_yield_edge_read_has_no_result_reencoding_surface():
    bundle = _byte_measurement_road()
    import seed_runtime.yield_evidence as yield_module

    assert not hasattr(yield_module, "yield_commitment")
    assert _occurrence_result_requirements(bundle) == {
        "exact_relation": True,
        "occurrence_witness": True,
        "intact_evidence": True,
    }


def _live_yield_exact_bundles() -> dict[str, dict]:
    bundles = {
        "byte_measurement": _byte_measurement_road(),
        "representation_result": _representation_road(),
        "successful_emission": _successful_emission_requirement_bundles()[
            "yield"
        ]["exact"],
    }
    bundles.update(
        {
            boundary: cases["exact"]
            for boundary, cases in _byte_pair_yield_requirement_bundles().items()
        }
    )
    bundles.update(
        {
            boundary: cases["exact"]
            for boundary, cases in _remaining_yield_requirement_bundles().items()
        }
    )
    assert set(bundles) == set(YIELD_LIVE_BOUNDARIES)
    return bundles


def _different_preservable_value(value):
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is float:
        return value + 1.0
    if type(value) is str:
        return value + "-different"
    if type(value) is list:
        return [*value, None]
    if type(value) is dict:
        different = dict(value)
        coordinate = "different"
        while coordinate in different:
            coordinate += "-different"
        different[coordinate] = None
        return different
    if value is None:
        return "different"
    raise TypeError(f"unpreservable yielded coordinate: {type(value).__name__}")


def _change_one_carried_yield_coordinate(bundle: dict) -> dict:
    different = dict(bundle)
    event = bundle["event"].model_copy(deep=True)
    evidence = bundle["content_evidence"]
    occurrence_coordinate = bundle.get(
        "recorded_result_occurrence_coordinate", "act_occurrence_id"
    )
    for coordinate in evidence.payload["yield_coordinates"]:
        carried_at = evidence.payload["recorded_result_coordinates"][coordinate]
        if carried_at == [occurrence_coordinate]:
            continue
        containing = event.payload
        for part in carried_at[:-1]:
            containing = containing[part]
        containing[carried_at[-1]] = _different_preservable_value(
            containing[carried_at[-1]]
        )
        different["event"] = event
        return different
    raise AssertionError("the Yield result has no non-occurrence coordinate")


def test_every_live_recorded_yield_result_is_bound_to_its_exact_evidence_result():
    for boundary, exact in _live_yield_exact_bundles().items():
        assert _occurrence_result_requirements(exact) == {
            "exact_relation": True,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        changed_result = _change_one_carried_yield_coordinate(exact)
        assert _occurrence_result_requirements(changed_result) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary

        missing_reference = dict(exact)
        missing_reference_event = exact["event"].model_copy(deep=True)
        missing_reference_event.payload["yield_evidence_id"] = (
            "missing-yield-evidence"
        )
        missing_reference["event"] = missing_reference_event
        assert _occurrence_result_requirements(missing_reference) == {
            "exact_relation": False,
            "occurrence_witness": True,
            "intact_evidence": True,
        }, boundary


def test_exact_act_clause_is_checked_against_live_byte_measurement():
    clause = _clause("02.Acts.A")
    bundle = _byte_measurement_road()
    witness = _act_occurrence_witness(bundle)

    assert set(witness) == set(clause["responsibility"]["coordinates"])
    assert set(witness.values()) == {EXACT}
    assert bundle["event"].payload["downstream_act_id"] != bundle["event"].payload[
        "act_occurrence_id"
    ]
    assert _occurrence_result_witness(bundle) == EXACT


def test_act_and_occurrence_ids_do_not_establish_their_relation():
    bundle = _byte_measurement_road()
    event = bundle["event"]
    assert event.payload["downstream_act_id"]
    assert event.payload["act_occurrence_id"]
    bundle["act_evidence"] = None
    witness = _act_occurrence_witness(bundle)

    assert witness["exact_Act"] == MISSING
    assert witness["Act_occurrence"] == MISSING
    assert witness["occurrence_Evidence"] == MISSING


def test_responsibility_coordinates_do_not_establish_assignment_standing():
    bundle = _byte_measurement_road()
    assignment = dict(
        bundle["event"].payload["responsibility_assignment_evidence"]
    )
    assignment.pop("standing")
    bundle["event"].payload["responsibility_assignment_evidence"] = assignment
    bundle["act_evidence"].payload["responsibility_assignment_evidence"] = dict(
        assignment
    )

    witness = _act_occurrence_witness(bundle)
    assert witness["Responsibility"] == EXACT
    assert witness["responsible_boundary"] == EXACT
    assert witness["Responsibility_assignment_Standing"] == MISSING


def test_runtime_authority_does_not_carry_evidence_scope_prose():
    contaminated = {}
    pattern = re.compile(
        r'"authority"\s*:\s*(?:"[^"\n]*(?:Evidence|evidence|evidences)|'
        r'\([^)]{0,400}(?:Evidence|evidence|evidences))',
        re.MULTILINE,
    )
    for path in sorted(RUNTIME.glob("*.py")):
        matches = [match.group(0) for match in pattern.finditer(path.read_text())]
        if matches:
            contaminated[path.name] = matches

    assert contaminated == {}


def test_each_dimensions_call_separates_authority_from_its_evidence_scope():
    """Every road through the shared dimensions bottleneck is observed."""

    observed = []
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_dimensions"
            ):
                continue
            keywords = {item.arg: item.value for item in node.keywords}
            observed.append((path.name, node.lineno))
            authority = keywords.get("authority")
            assert isinstance(authority, ast.Constant), (path, node.lineno)
            assert authority.value == "unestablished", (path, node.lineno)
            assert "evidence_scope" in keywords, (path, node.lineno)

    assert observed


LOCALITY_BOUNDARY_BY_KIND = {
    "operator.assertion.compare_input_locality_evidenced": (
        "assertion_compare_input"
    ),
    "operator.measurement.comparison_input_locality_evidenced": (
        "bounded_compare_input"
    ),
    "operator.addressed_representation.locality_evidenced": "operator_checkpoint",
    "operator.measurement.adjacency_pair_measurement_locality_evidenced": (
        "adjacency_pair_measurement"
    ),
    "operator.measurement.adjacency_pair_measurement_compare_locality_evidenced": (
        "adjacency_pair_measurement_compare"
    ),
    "operator.representation.locality_evidenced": "representation_result",
    "operator.representation.emission_attempt_locality_evidenced": (
        "emission_attempt"
    ),
    "operator.representation.emission_locality_evidenced": (
        "successful_emission"
    ),
}
LOCALITY_BOUNDARIES_EVIDENCED_BY_OCCURRENCE = {
    "byte_measurement",
    "assertion_movement",
}


def _declared_kind_constants(family: str) -> dict[str, list[str]]:
    """Every module-level kind constant naming this edge, found by read code.

    Independent discovery, as with Yield: the registry above is not
    asked what exists, the runtime is. A boundary that stops declaring itself,
    or a new one that never registers, both surface here.
    """

    found: dict[str, list[str]] = {}
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not isinstance(node.value, ast.Constant):
                continue
            if not isinstance(node.value.value, str):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if family not in target.id:
                    continue
                found.setdefault(node.value.value, []).append(path.name)
    return found


def test_every_locality_evidence_kind_is_declared_once_and_registered():
    """The Yield discovery pattern, applied to the second structural edge."""

    discovered = _declared_kind_constants("LOCALITY_EVIDENCE_KIND")

    duplicated = {
        kind: modules for kind, modules in discovered.items() if len(modules) > 1
    }
    assert not duplicated, (
        "\nOne locality kind, declared by more than one module. The writer and "
        "the reader then hold separate contracts that drift silently:\n"
        + "\n".join(f"  {kind} -- {', '.join(m)}" for kind, m in duplicated.items())
    )

    assert set(discovered) == set(LOCALITY_BOUNDARY_BY_KIND), (
        "\nLive locality boundaries and the registry disagree.\n"
        f"  only live:     {sorted(set(discovered) - set(LOCALITY_BOUNDARY_BY_KIND))}\n"
        f"  only registry: {sorted(set(LOCALITY_BOUNDARY_BY_KIND) - set(discovered))}"
    )
    registered = _live_structural_edge_fidelity_cases()
    assert {
        boundary for edge, boundary in registered if edge == "locality"
    } == (
        set(LOCALITY_BOUNDARY_BY_KIND.values())
        | LOCALITY_BOUNDARIES_EVIDENCED_BY_OCCURRENCE
    )


# Every module recording a `scope_locality` dimension. 06.Standing.B makes
# locality a coordinate in its own right, and 01.Standing.E.1 enumerates Scope
# and locality separately among the coordinates Applicability is determined
# for. This compound field carries both in one string. A regression boundary,
# not approval.
SCOPE_LOCALITY_COMPOUND_SITES = 21


def test_no_new_site_compounds_scope_with_locality():
    """The count of sites compounding Scope with locality may fall, never rise."""

    sites = sum(
        path.read_text(encoding="utf-8").count("scope_locality")
        for path in sorted(RUNTIME.glob("*.py"))
    )
    assert sites <= SCOPE_LOCALITY_COMPOUND_SITES, (
        f"\n{sites} sites compound Scope with locality, up from "
        f"{SCOPE_LOCALITY_COMPOUND_SITES}. 06.Standing.B carries locality as "
        "its own coordinate; a new site glues it to Scope again."
    )


# Every live structural-edge witness, and where its Evidence comes from.
#
# A dedicated Evidence event species is not what makes an edge live: Evidence
# may be the event occurrence itself, a responsible Act evidence occurrence,
# or a dedicated one. grammar.json requires exact_relation, occurrence_witness,
# and intact_evidence, and names no species for them.
STRUCTURAL_EDGE_EVIDENCE = {
    "_checkpoint_locality_requirements": (
        "locality",
        "a command-to-checkpoint locality-evidence occurrence",
    ),
    "_assertion_compare_input_locality_requirements": (
        "locality",
        "an Assertion-to-Compare locality-evidence occurrence",
    ),
    "_bounded_compare_input_locality_requirements": (
        "locality",
        "a finding-to-Compare locality-evidence occurrence",
    ),
    "_locality_requirements": (
        "locality",
        "the responsible movement Evidence occurrence",
    ),
    "_assertion_locality_requirements": ("locality", "the event occurrence itself"),
    "_emission_locality_requirements": ("locality", "a locality-evidence occurrence"),
    "_emission_attempt_locality_requirements": (
        "locality",
        "an emission-attempt locality-evidence occurrence",
    ),
    "_representation_locality_requirements": (
        "locality",
        "a representation locality-evidence occurrence",
    ),
    "_emission_participation_requirements": (
        "participation",
        "the responsible emission Act evidence occurrence",
    ),
    "_participation_requirements": (
        "participation",
        "the responsible pair Act evidence occurrence",
    ),
    "_occurrence_result_requirements": ("yield", "a Yield-evidence occurrence"),
}


def _requirement_witnesses() -> set[str]:
    """Every live edge witness, found by read this module rather than listing it."""

    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    return {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name.startswith("_")
        and node.name.endswith("_requirements")
    }


def test_every_live_edge_witness_names_its_edge_and_its_evidence():
    """Independent discovery equated with the registry, for all three edges."""

    assert _requirement_witnesses() == set(STRUCTURAL_EDGE_EVIDENCE), (
        "\nLive edge witnesses and the registry disagree.\n"
        f"  only live:     {sorted(_requirement_witnesses() - set(STRUCTURAL_EDGE_EVIDENCE))}\n"
        f"  only registry: {sorted(set(STRUCTURAL_EDGE_EVIDENCE) - _requirement_witnesses())}"
    )

    edges = json.loads(GRAMMAR.read_text(encoding="utf-8"))["structural_edges"]
    for witness, (edge, evidence) in STRUCTURAL_EDGE_EVIDENCE.items():
        assert edge in edges, f"{witness} names {edge}, which is not a structural edge"
        assert evidence, witness


def test_each_structural_edge_has_a_live_witness():
    """Each structural edge grammar.json declares has a live witness."""

    edges = json.loads(GRAMMAR.read_text(encoding="utf-8"))["structural_edges"]
    witnessed = {edge for edge, _ in STRUCTURAL_EDGE_EVIDENCE.values()}
    assert witnessed == set(edges)


def test_every_live_edge_witness_returns_its_edge_required_coordinates():
    """The vector each witness reports is the one its edge declares."""

    edges = json.loads(GRAMMAR.read_text(encoding="utf-8"))["structural_edges"]
    yielded = _occurrence_result_requirements(_byte_measurement_road())
    assert set(yielded) == set(edges["yield"]["requires"])

    # The remaining witnesses are still developer-read through Python AST.
    # Yield is deliberately absent here: its required coordinates were read
    # from Seed's live result above, not read from function syntax.
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name not in STRUCTURAL_EDGE_EVIDENCE:
            continue
        if node.name == "_occurrence_result_requirements":
            continue
        edge, _ = STRUCTURAL_EDGE_EVIDENCE[node.name]
        required = set(edges[edge]["requires"])
        reported = {
            key.value
            for sub in ast.walk(node)
            if isinstance(sub, ast.Dict)
            for key in sub.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, str)
        }
        assert required <= reported, (
            f"{node.name} witnesses {edge}, which requires {sorted(required)}; "
            f"it reports {sorted(reported)}"
        )
