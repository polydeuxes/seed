"""Bounded Compare over two productions of one canonical Assertion.

Canonical Assertion identity establishes the shared subject.  Distinct
producing Event identities establish that there are two production
occurrences.  Compare reports literal sameness and difference across carried
fidelity coordinates; it establishes no conflict, preference, truth, meaning,
or reason to revise either Assertion.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from itertools import combinations
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.event import Event
from seed_runtime.ids import new_id
from seed_runtime.adjacent_pair_measurement import (
    INGRESS_OCCURRED_KIND,
    RecordedAdjacentPairResultAssertion,
    _validate_result_assertion_ingress,
    assertion_of_recorded_adjacent_pair_result,
    get_recorded_adjacent_pair_result_assertion,
    iter_recorded_adjacent_pair_result_assertions,
)
from seed_runtime.recurrence_measurement import (
    RecordedMeasuredAssertion,
    get_recorded_measured_assertion,
)


class AssertionComparisonError(ValueError):
    """The bounded Assertion comparison could not be instantiated."""


@dataclass(frozen=True)
class AssertionProductionInput:
    assertion_id: str
    producing_event_id: str
    integrity: str


@dataclass(frozen=True)
class AssertionCoordinateDistinction:
    coordinate: str
    same: bool
    present: tuple[bool, bool]
    values: tuple[Any, Any]


@dataclass(frozen=True)
class AssertionProductionComparison:
    assertion_id: str
    inputs: tuple[AssertionProductionInput, AssertionProductionInput]
    distinctions: tuple[AssertionCoordinateDistinction, ...]
    act: str = "Compare"
    owner: str = "this bounded comparison occurrence"
    responsibility: str = (
        "preserve each input's carried fidelity coordinates and report literal "
        "sameness, difference, and absence only"
    )


@dataclass(frozen=True)
class PositionalResultInput:
    """One exact occurrence-bound positional result consumed by Compare."""

    assertion_id: str
    producing_event_id: str
    integrity: str


@dataclass(frozen=True)
class PositionalResultCoordinateDistinction:
    """One literal carried-coordinate result of Compare."""

    coordinate: str
    same: bool
    present: tuple[bool, bool]
    values: tuple[Any, Any]


@dataclass(frozen=True)
class PositionalResultComparison:
    """Unrecorded Compare over two Assertions with one exact subject."""

    subject: dict[str, Any]
    inputs: tuple[PositionalResultInput, PositionalResultInput]
    distinctions: tuple[PositionalResultCoordinateDistinction, ...]
    act: str = "Compare"
    owner: str = "this bounded comparison occurrence"
    responsibility: str = (
        "preserve each positional result Assertion as carried and report literal "
        "coordinate sameness, difference, and absence only"
    )


ASSERTION_PRODUCTION_COMPARISON_RECORDED_KIND = (
    "operator.assertion.production_comparison_recorded"
)
POSITIONAL_RESULT_COMPARISON_RECORDED_KIND = (
    "operator.assertion.positional_result_comparison_recorded"
)

COMPARISON_ASSERTION_FIDELITY_RESPONSIBILITY = (
    "preserve the fidelity of this comparison Assertion's Standing to its "
    "carried coordinates"
)
POSITIONAL_RESULT_COMPARISON_PROVENANCE = (
    "the two exact positional result Assertion productions carried in support_basis"
)
POSITIONAL_RESULT_COMPARISON_AUTHORITY = (
    "literal comparison evidence only; establishes no relation, similarity, "
    "recurrence, conflict, meaning, preference, revision, or strengthening"
)
POSITIONAL_RESULT_COMPARISON_UNKNOWNS = (
    "whether this literal result is Applicable to any later Act remains Unknown",
)
POSITIONAL_RESULT_COMPARISON_FORBIDDEN_INFERENCES = (
    "literal sameness is not similarity, relation, or recurrence",
    "literal difference is not conflict",
    "recording does not establish Applicability, admission, consumption, "
    "Uptake, or Standing movement",
)


@dataclass(frozen=True)
class RecordedAssertionProductionDistinction:
    """One addressable coordinate result inside its producing Compare occurrence."""

    assertion_id: str
    producing_event_id: str
    coordinate: str
    payload: dict[str, Any]

    @property
    def reference(self) -> dict[str, str]:
        return {
            "producing_event_id": self.producing_event_id,
            "assertion_id": self.assertion_id,
        }


@dataclass(frozen=True)
class RecordedPositionalResultDistinction:
    """One addressable coordinate result of a positional-result Compare."""

    assertion_id: str
    producing_event_id: str
    coordinate: str
    payload: dict[str, Any]

    @property
    def reference(self) -> dict[str, str]:
        return {
            "producing_event_id": self.producing_event_id,
            "assertion_id": self.assertion_id,
        }


COORDINATES: dict[str, tuple[str, ...]] = {
    "standing": ("dimensions", "standing"),
    "source_provenance": ("dimensions", "source_provenance"),
    "responsibility": ("dimensions", "responsibility"),
    "authority_warrant": ("dimensions", "authority_warrant"),
    "scope": ("assertion_scope",),
    "support_basis": ("support_basis",),
    "completeness_boundary": ("completeness_boundary",),
    "completeness_scope": ("completeness_scope",),
    "unknowns": ("unknowns",),
    "forbidden_inferences": ("forbidden_inferences",),
}

POSITIONAL_RESULT_COORDINATES: dict[str, tuple[str, ...]] = {
    "positions_measured": ("dimensions", "content", "positions_measured"),
    "occupancies": ("dimensions", "content", "occupancies"),
    "standing": ("dimensions", "standing"),
    "source_provenance": ("dimensions", "source_provenance"),
    "responsibility": ("dimensions", "responsibility"),
    "authority_warrant": ("dimensions", "authority_warrant"),
    "scope": ("assertion_scope",),
    "support_basis": ("support_basis",),
    "completeness_boundary": ("completeness_boundary",),
    "completeness_scope": ("completeness_scope",),
    "unknowns": ("unknowns",),
    "forbidden_inferences": ("forbidden_inferences",),
}


def _read(payload: dict[str, Any], path: tuple[str, ...]) -> tuple[bool, Any]:
    value: Any = payload
    for coordinate in path:
        if not isinstance(value, dict) or coordinate not in value:
            return False, None
        value = value[coordinate]
    return True, value


def _exactly_same(left: Any, right: Any) -> bool:
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":")
    )


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _distinction_assertion_identity(
    *,
    compared_assertion_id: str,
    inputs: Iterable[dict[str, str]],
    workspace_id: str,
    session_id: str,
    coordinate: str,
    present: Iterable[bool],
    values: Iterable[Any],
    same: bool,
) -> str:
    identity = {
        "compared_assertion_id": compared_assertion_id,
        "inputs": list(inputs),
        "workspace_id": workspace_id,
        "session_id": session_id,
        "coordinate": coordinate,
        "present": list(present),
        "values": list(values),
        "same": same,
    }
    return "assertion-production-distinction:" + hashlib.sha256(
        _canonical_json(identity).encode("utf-8")
    ).hexdigest()


def _positional_result_distinction_identity(
    *,
    subject: dict[str, Any],
    inputs: Iterable[dict[str, str]],
    workspace_id: str,
    session_id: str,
    coordinate: str,
    present: Iterable[bool],
    values: Iterable[Any],
    same: bool,
) -> str:
    identity = {
        "compared_subject": subject,
        "inputs": list(inputs),
        "workspace_id": workspace_id,
        "session_id": session_id,
        "coordinate": coordinate,
        "present": list(present),
        "values": list(values),
        "same": same,
    }
    return "positional-result-distinction:" + hashlib.sha256(
        _canonical_json(identity).encode("utf-8")
    ).hexdigest()


def compare_assertion_productions(
    ledger: EventLedger, references: Iterable[dict[str, str]]
) -> AssertionProductionComparison:
    """Compare two exact productions of the same canonical Assertion."""

    refs = tuple(references)
    if len(refs) != 2:
        raise AssertionComparisonError(
            f"Assertion production Compare consumes exactly two inputs; {len(refs)} supplied"
        )
    required = {"producing_event_id", "assertion_id"}
    if any(set(reference) != required for reference in refs):
        raise AssertionComparisonError(
            "each input must be one exact producing-event and Assertion identity pair"
        )
    if refs[0] == refs[1] or refs[0]["producing_event_id"] == refs[1]["producing_event_id"]:
        raise AssertionComparisonError(
            "one producing occurrence cannot be compared with itself"
        )
    if refs[0]["assertion_id"] != refs[1]["assertion_id"]:
        raise AssertionComparisonError(
            "Assertion production Compare requires one canonical Assertion identity"
        )

    recovered: list[RecordedMeasuredAssertion] = []
    inputs = []
    for reference in refs:
        assertion = get_recorded_measured_assertion(
            ledger,
            producing_event_id=reference["producing_event_id"],
            assertion_id=reference["assertion_id"],
        )
        if assertion is None:
            raise AssertionComparisonError(
                "an Assertion reference does not resolve to its producing occurrence"
            )
        integrity = ledger.integrity_of(assertion.producing_event_id)
        if integrity == CORRUPTED:
            raise AssertionComparisonError(
                "a corrupted producing occurrence cannot participate in Compare"
            )
        recovered.append(assertion)
        inputs.append(
            AssertionProductionInput(
                assertion_id=assertion.assertion_id,
                producing_event_id=assertion.producing_event_id,
                integrity=integrity,
            )
        )

    distinctions = []
    for coordinate, path in COORDINATES.items():
        read = tuple(_read(assertion.payload, path) for assertion in recovered)
        present = (read[0][0], read[1][0])
        values = (read[0][1], read[1][1])
        distinctions.append(
            AssertionCoordinateDistinction(
                coordinate=coordinate,
                same=present[0] == present[1] and _exactly_same(*values),
                present=present,
                values=values,
            )
        )
    return AssertionProductionComparison(
        assertion_id=refs[0]["assertion_id"],
        inputs=(inputs[0], inputs[1]),
        distinctions=tuple(distinctions),
    )


def compare_positional_result_assertions(
    ledger: EventLedger, references: Iterable[dict[str, str]]
) -> PositionalResultComparison:
    """Compare two exact result Assertions sharing one literal subject.

    Subject equality supplies comparability only. It establishes no relation,
    similarity, recurrence, conflict, preference, meaning, or reason for either
    Assertion's Standing to move.
    """

    refs = tuple(references)
    if len(refs) != 2:
        raise AssertionComparisonError(
            f"positional result Compare consumes exactly two inputs; {len(refs)} supplied"
        )
    required = {"producing_event_id", "assertion_id"}
    if any(set(reference) != required for reference in refs):
        raise AssertionComparisonError(
            "each input must be one exact producing-event and Assertion identity pair"
        )
    if refs[0] == refs[1] or refs[0]["producing_event_id"] == refs[1]["producing_event_id"]:
        raise AssertionComparisonError(
            "one positional result production cannot be compared with itself"
        )

    recovered: list[RecordedAdjacentPairResultAssertion] = []
    integrities = []
    for reference in refs:
        assertion = get_recorded_adjacent_pair_result_assertion(
            ledger,
            producing_event_id=reference["producing_event_id"],
            assertion_id=reference["assertion_id"],
        )
        if assertion is None:
            raise AssertionComparisonError(
                "a positional result Assertion reference does not resolve to its "
                "producing occurrence"
            )
        integrity = ledger.integrity_of(assertion.producing_event_id)
        recovered.append(assertion)
        integrities.append(integrity)

    return _compare_recovered_positional_result_assertions(
        recovered, integrities=integrities
    )


def _compare_recovered_positional_result_assertions(
    assertions: Iterable[RecordedAdjacentPairResultAssertion],
    *,
    integrities: Iterable[str],
) -> PositionalResultComparison:
    """Compare Assertions already recovered inside one bounded occurrence."""

    recovered = tuple(assertions)
    integrity_values = tuple(integrities)
    if len(recovered) != 2 or len(integrity_values) != 2:
        raise AssertionComparisonError("a recovered positional Compare requires two inputs")
    inputs = tuple(
        PositionalResultInput(
            assertion_id=assertion.assertion_id,
            producing_event_id=assertion.producing_event_id,
            integrity=integrity,
        )
        for assertion, integrity in zip(recovered, integrity_values)
    )
    subjects = tuple(assertion.payload["assertion_subject"] for assertion in recovered)
    if not _exactly_same(subjects[0], subjects[1]):
        raise AssertionComparisonError(
            "positional result Compare requires one exact carried Assertion subject"
        )

    distinctions = []
    for coordinate, path in POSITIONAL_RESULT_COORDINATES.items():
        read = tuple(_read(assertion.payload, path) for assertion in recovered)
        present = (read[0][0], read[1][0])
        values = (read[0][1], read[1][1])
        distinctions.append(
            PositionalResultCoordinateDistinction(
                coordinate=coordinate,
                same=present[0] == present[1] and _exactly_same(*values),
                present=present,
                values=values,
            )
        )
    return PositionalResultComparison(
        subject=dict(subjects[0]),
        inputs=(inputs[0], inputs[1]),
        distinctions=tuple(distinctions),
    )


def _positional_result_assertions_by_subject(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: "EventLedgerBoundary",
) -> dict[str, list[dict[str, str]]]:
    """Validate the population while retaining only compact references."""

    grouped: dict[str, list[dict[str, str]]] = {}
    for assertion in iter_recorded_adjacent_pair_result_assertions(
        ledger,
        workspace_id=workspace_id,
        session_ids=session_ids,
        through=through,
    ):
        subject_key = _canonical_json(assertion.payload["assertion_subject"])
        grouped.setdefault(subject_key, []).append(assertion.reference)
    return grouped


def iter_positional_result_comparison_inputs(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: "EventLedgerBoundary",
) -> Iterator[tuple[dict[str, str], dict[str, str]]]:
    """Form every unordered production pair sharing one exact subject.

    The caller fixes the eligible append extent. Equal carried subjects supply
    comparability; no count, threshold, ranking, result value, or semantic
    category admits or excludes a production. Compare is not performed here.
    """

    by_subject = _positional_result_assertions_by_subject(
        ledger,
        workspace_id=workspace_id,
        session_ids=session_ids,
        through=through,
    )
    for references in by_subject.values():
        yield from combinations(references, 2)


def record_positional_result_comparison(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    comparison: PositionalResultComparison,
) -> Event:
    """Preserve each literal positional-result Compare output separately."""

    input_refs = tuple(
        {
            "producing_event_id": item.producing_event_id,
            "assertion_id": item.assertion_id,
        }
        for item in comparison.inputs
    )
    verified = compare_positional_result_assertions(ledger, input_refs)
    if comparison != verified:
        raise AssertionComparisonError(
            "the supplied positional-result comparison does not match its inputs"
        )
    return ledger.append(
        POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
        workspace_id,
        _positional_result_comparison_payload(
            workspace_id=workspace_id,
            session_id=session_id,
            comparison=comparison,
        ),
        session_id=session_id,
    )


def _positional_result_comparison_payload(
    *,
    workspace_id: str,
    session_id: str,
    comparison: PositionalResultComparison,
) -> dict[str, Any]:
    """Represent a comparison already reproduced from validated inputs."""

    input_refs = tuple(
        {
            "producing_event_id": item.producing_event_id,
            "assertion_id": item.assertion_id,
        }
        for item in comparison.inputs
    )
    assertions = []
    for distinction in comparison.distinctions:
        content = {
            "coordinate": distinction.coordinate,
            "present": list(distinction.present),
            "values": list(distinction.values),
            "same": distinction.same,
        }
        identity = _positional_result_distinction_identity(
            subject=comparison.subject,
            inputs=input_refs,
            workspace_id=workspace_id,
            session_id=session_id,
            **content,
        )
        assertions.append(
            {
                "dimensions": {
                    "identity": identity,
                    "content": content,
                    "standing": "compared",
                    "source_provenance": POSITIONAL_RESULT_COMPARISON_PROVENANCE,
                    "responsibility": COMPARISON_ASSERTION_FIDELITY_RESPONSIBILITY,
                    "authority_warrant": POSITIONAL_RESULT_COMPARISON_AUTHORITY,
                    "scope_locality": "the exact assertion_scope carried here",
                    "occurrence_preservation": (
                        "distinct Compare result preserved by its producing occurrence"
                    ),
                },
                "subject_kind": "assertion",
                "responsibility_owner": "this recorded assertion",
                "result": "positional_result_coordinate_distinction",
                "assertion_subject": {
                    "compared_subject": dict(comparison.subject),
                    "coordinate": distinction.coordinate,
                },
                "assertion_scope": {
                    "workspace_id": workspace_id,
                    "session_id": session_id,
                    "compared_productions": list(input_refs),
                },
                "support_basis": {"assertion_refs": list(input_refs)},
                "unknowns": list(POSITIONAL_RESULT_COMPARISON_UNKNOWNS),
                "forbidden_inferences": list(
                    POSITIONAL_RESULT_COMPARISON_FORBIDDEN_INFERENCES
                ),
            }
        )
    return {
            "dimensions": {
                "identity": "positional-result-comparison-occurrence",
                "content": f"{len(assertions)} distinct comparison Assertions recorded",
                "standing": "recorded",
                "source_provenance": "two occurrence-bound positional result Assertions",
                "authority_warrant": "literal Compare results only",
                "scope_locality": f"workspace:{workspace_id};session:{session_id}",
                "occurrence_preservation": "comparison occurrence durably recorded",
            },
            "producing_act": "Compare",
            "owner": comparison.owner,
            "responsibility": comparison.responsibility,
            "compared_subject": dict(comparison.subject),
            "inputs": list(input_refs),
            "assertions": assertions,
        }


def assertions_of_recorded_positional_result_comparison(
    event: Event,
) -> tuple[RecordedPositionalResultDistinction, ...]:
    """Recover and verify every output of one recorded positional Compare."""

    if event.kind != POSITIONAL_RESULT_COMPARISON_RECORDED_KIND:
        raise AssertionComparisonError(
            f"{event.id} is not a positional-result Compare occurrence"
        )
    stated = event.payload.get("assertions")
    outer_inputs = event.payload.get("inputs")
    compared_subject = event.payload.get("compared_subject")
    required_ref = {"producing_event_id", "assertion_id"}
    if (
        not isinstance(stated, list)
        or len(stated) != len(POSITIONAL_RESULT_COORDINATES)
        or not isinstance(compared_subject, dict)
        or not isinstance(outer_inputs, list)
        or len(outer_inputs) != 2
        or any(
            not isinstance(reference, dict)
            or set(reference) != required_ref
            or not all(isinstance(value, str) and value for value in reference.values())
            for reference in outer_inputs
        )
        or outer_inputs[0]["producing_event_id"]
        == outer_inputs[1]["producing_event_id"]
    ):
        raise AssertionComparisonError(
            f"{event.id} does not carry one bounded positional-result Compare"
        )

    recovered = []
    seen_identities = set()
    seen_coordinates = set()
    for assertion in stated:
        dimensions = assertion.get("dimensions") if isinstance(assertion, dict) else None
        content = dimensions.get("content") if isinstance(dimensions, dict) else None
        identity = dimensions.get("identity") if isinstance(dimensions, dict) else None
        subject = assertion.get("assertion_subject") if isinstance(assertion, dict) else None
        scope = assertion.get("assertion_scope") if isinstance(assertion, dict) else None
        support = assertion.get("support_basis") if isinstance(assertion, dict) else None
        refs = support.get("assertion_refs") if isinstance(support, dict) else None
        if (
            assertion.get("subject_kind") != "assertion"
            or assertion.get("responsibility_owner") != "this recorded assertion"
            or assertion.get("result") != "positional_result_coordinate_distinction"
            or not isinstance(dimensions, dict)
            or dimensions.get("standing") != "compared"
            or dimensions.get("source_provenance")
            != POSITIONAL_RESULT_COMPARISON_PROVENANCE
            or dimensions.get("responsibility")
            != COMPARISON_ASSERTION_FIDELITY_RESPONSIBILITY
            or dimensions.get("authority_warrant")
            != POSITIONAL_RESULT_COMPARISON_AUTHORITY
            or dimensions.get("scope_locality")
            != "the exact assertion_scope carried here"
            or dimensions.get("occurrence_preservation")
            != "distinct Compare result preserved by its producing occurrence"
            or not isinstance(content, dict)
            or set(content) != {"coordinate", "present", "values", "same"}
            or not isinstance(identity, str)
            or not identity
            or not isinstance(subject, dict)
            or not isinstance(scope, dict)
            or refs != outer_inputs
            or subject.get("compared_subject") != compared_subject
            or scope
            != {
                "workspace_id": event.workspace_id,
                "session_id": event.session_id,
                "compared_productions": outer_inputs,
            }
            or assertion.get("unknowns")
            != list(POSITIONAL_RESULT_COMPARISON_UNKNOWNS)
            or assertion.get("forbidden_inferences")
            != list(POSITIONAL_RESULT_COMPARISON_FORBIDDEN_INFERENCES)
        ):
            raise AssertionComparisonError(
                f"{event.id} carries an incoherent positional Compare result"
            )
        coordinate = content["coordinate"]
        present = content["present"]
        values = content["values"]
        same = content["same"]
        if (
            coordinate not in POSITIONAL_RESULT_COORDINATES
            or subject.get("coordinate") != coordinate
            or not isinstance(present, list)
            or len(present) != 2
            or not all(isinstance(value, bool) for value in present)
            or not isinstance(values, list)
            or len(values) != 2
            or not isinstance(same, bool)
            or same != (present[0] == present[1] and _exactly_same(*values))
        ):
            raise AssertionComparisonError(
                f"{event.id} carries an unlawful positional Compare result"
            )
        canonical = _positional_result_distinction_identity(
            subject=compared_subject,
            inputs=outer_inputs,
            workspace_id=event.workspace_id,
            session_id=event.session_id,
            coordinate=coordinate,
            present=present,
            values=values,
            same=same,
        )
        if identity != canonical or identity in seen_identities or coordinate in seen_coordinates:
            raise AssertionComparisonError(
                f"{event.id} carries duplicate or noncanonical positional Compare output"
            )
        seen_identities.add(identity)
        seen_coordinates.add(coordinate)
        recovered.append(
            RecordedPositionalResultDistinction(
                assertion_id=identity,
                producing_event_id=event.id,
                coordinate=coordinate,
                payload=assertion,
            )
        )
    if seen_coordinates != set(POSITIONAL_RESULT_COORDINATES):
        raise AssertionComparisonError(
            f"{event.id} does not carry every positional Compare coordinate"
        )
    return tuple(recovered)


def get_recorded_positional_result_distinction(
    ledger: EventLedger, *, producing_event_id: str, assertion_id: str
) -> RecordedPositionalResultDistinction | None:
    """Resolve one result only after reproducing its bounded Compare."""

    event = ledger.get(producing_event_id)
    if event is None:
        return None
    recovered = _recover_recorded_positional_result_comparison(ledger, event)
    for result in recovered:
        if result.assertion_id == assertion_id:
            return result
    return None


def _recover_recorded_positional_result_comparison(
    ledger: EventLedger,
    event: Event,
) -> tuple[RecordedPositionalResultDistinction, ...]:
    """Recover one Compare from an Event returned by this ledger.

    This private helper's caller must obtain ``event`` from ``ledger`` in the
    current bounded read.  Public recovery remains occurrence-id based so an
    arbitrary Event carrying the same id cannot borrow the ledger row's
    integrity standing.
    """

    if ledger.integrity_of(event.id) == CORRUPTED:
        raise AssertionComparisonError(
            "a corrupted Compare occurrence cannot expose result Assertions"
        )
    recovered = assertions_of_recorded_positional_result_comparison(event)
    comparison = compare_positional_result_assertions(ledger, event.payload["inputs"])
    _require_recorded_positional_comparison_matches(event, recovered, comparison)
    return recovered


def _require_recorded_positional_comparison_matches(
    event: Event,
    recovered: tuple[RecordedPositionalResultDistinction, ...],
    comparison: PositionalResultComparison,
) -> None:
    """Require the carried occurrence and outputs to equal the replayed Act."""

    if (
        event.payload.get("producing_act") != comparison.act
        or event.payload.get("owner") != comparison.owner
        or event.payload.get("responsibility") != comparison.responsibility
        or event.payload["compared_subject"] != comparison.subject
    ):
        raise AssertionComparisonError(
            "the recorded Compare occurrence does not match its replayed Act"
        )
    expected = {
        distinction.coordinate: {
            "coordinate": distinction.coordinate,
            "present": list(distinction.present),
            "values": list(distinction.values),
            "same": distinction.same,
        }
        for distinction in comparison.distinctions
    }
    for result in recovered:
        if result.payload["dimensions"]["content"] != expected[result.coordinate]:
            raise AssertionComparisonError(
                "a recorded positional Compare result does not match its inputs"
            )


def iter_recorded_positional_result_distinctions(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_ids: Iterable[str],
    through: "EventLedgerBoundary",
) -> Iterator[RecordedPositionalResultDistinction]:
    """Validate and stream a bounded population of recorded Compare outputs.

    Each occurrence-bound positional input receives its complete ingress proof
    once in this frozen invocation. Later uses retain only that compact
    validated reference, then rehydrate and structurally verify the Assertion.
    """

    validated_inputs: set[tuple[str, str]] = set()
    ingress_ids_by_boundary: dict[tuple[str, str], tuple[str, ...]] = {}
    for session_id in tuple(dict.fromkeys(session_ids)):
        for event in ledger.iter_session_kind(
            workspace_id,
            session_id,
            POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
            through=through,
        ):
            recovered_results = assertions_of_recorded_positional_result_comparison(
                event
            )
            recovered_inputs = []
            integrities = []
            for reference in event.payload["inputs"]:
                ref = (
                    reference["producing_event_id"],
                    reference["assertion_id"],
                )
                producing_event = ledger.get(ref[0])
                if producing_event is None:
                    raise AssertionComparisonError(
                        "a positional result input is no longer recoverable"
                    )
                integrity = ledger.integrity_of(ref[0])
                if integrity == CORRUPTED:
                    raise AssertionComparisonError(
                        "a corrupted positional result cannot supply Compare"
                    )
                assertion = assertion_of_recorded_adjacent_pair_result(producing_event)
                if assertion.assertion_id != ref[1]:
                    raise AssertionComparisonError(
                        "a positional result input reference changed"
                    )
                if ref not in validated_inputs:
                    cache_key = (
                        producing_event.session_id,
                        assertion.completeness_boundary.commitment,
                    )
                    recovered_ingress_ids = ingress_ids_by_boundary.get(cache_key)
                    if recovered_ingress_ids is None:
                        recovered_ingress_ids = tuple(
                            ledger.iter_session_kind_ids(
                                workspace_id,
                                producing_event.session_id,
                                INGRESS_OCCURRED_KIND,
                                through=assertion.completeness_boundary,
                            )
                        )
                        ingress_ids_by_boundary[cache_key] = recovered_ingress_ids
                    _validate_result_assertion_ingress(
                        ledger,
                        producing_event,
                        assertion,
                        recovered_ingress_ids=recovered_ingress_ids,
                    )
                    validated_inputs.add(ref)
                recovered_inputs.append(assertion)
                integrities.append(integrity)
            comparison = _compare_recovered_positional_result_assertions(
                recovered_inputs, integrities=integrities
            )
            _require_recorded_positional_comparison_matches(
                event, recovered_results, comparison
            )
            yield from recovered_results


def record_positional_result_comparison_layer(
    ledger: EventLedger,
    *,
    workspace_id: str,
    source_session_ids: Iterable[str],
    recording_session_id: str,
) -> int:
    """Form, perform, and record one fixed layer of lawful Comparisons.

    One captured append prefix fixes the eligible result Assertions. Every
    unordered pair sharing an exact carried subject is compared and recorded;
    results written here cannot become inputs to this same invocation.
    """

    sessions = tuple(dict.fromkeys(source_session_ids))
    if not sessions or any(not isinstance(value, str) or not value for value in sessions):
        raise AssertionComparisonError(
            "a positional comparison layer requires exact declared source sessions"
        )
    if not isinstance(recording_session_id, str) or not recording_session_id:
        raise AssertionComparisonError(
            "a positional comparison layer requires an exact recording session"
        )
    boundary = ledger.capture_boundary()
    missing = [
        session_id
        for session_id in sessions
        if not ledger.has_session(workspace_id, session_id, through=boundary)
    ]
    if missing:
        raise AssertionComparisonError(
            "declared source sessions are absent through the layer boundary: "
            + ", ".join(missing)
        )

    by_subject = _positional_result_assertions_by_subject(
        ledger,
        workspace_id=workspace_id,
        session_ids=sessions,
        through=boundary,
    )
    batch_size = 128
    pending = []
    recorded = 0
    for references in by_subject.values():
        recovered = []
        for reference in references:
            event = ledger.get(reference["producing_event_id"])
            if event is None:
                raise AssertionComparisonError(
                    "a validated positional result production is no longer recoverable"
                )
            assertion = assertion_of_recorded_adjacent_pair_result(event)
            if assertion.assertion_id != reference["assertion_id"]:
                raise AssertionComparisonError(
                    "a validated positional result reference changed during the layer"
                )
            recovered.append(assertion)
        for left, right in combinations(recovered, 2):
            comparison = _compare_recovered_positional_result_assertions(
                (left, right),
                integrities=(
                    ledger.integrity_of(left.producing_event_id),
                    ledger.integrity_of(right.producing_event_id),
                ),
            )
            pending.append(
                Event(
                    id=new_id("evt"),
                    kind=POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
                    workspace_id=workspace_id,
                    session_id=recording_session_id,
                    payload=_positional_result_comparison_payload(
                        workspace_id=workspace_id,
                        session_id=recording_session_id,
                        comparison=comparison,
                    ),
                )
            )
            if len(pending) == batch_size:
                ledger.append_many(pending)
                recorded += len(pending)
                pending.clear()
    if pending:
        ledger.append_many(pending)
        recorded += len(pending)
    return recorded


def record_assertion_production_comparison(
    ledger: EventLedger,
    *,
    workspace_id: str,
    session_id: str,
    comparison: AssertionProductionComparison,
) -> Event:
    """Preserve each literal Compare result without performing its Uptake."""

    input_refs = tuple(
        {
            "producing_event_id": item.producing_event_id,
            "assertion_id": item.assertion_id,
        }
        for item in comparison.inputs
    )
    verified = compare_assertion_productions(ledger, input_refs)
    if comparison != verified:
        raise AssertionComparisonError(
            "the supplied comparison does not match its occurrence-bound inputs"
        )
    assertions = []
    for distinction in comparison.distinctions:
        content = {
            "coordinate": distinction.coordinate,
            "present": list(distinction.present),
            "values": list(distinction.values),
            "same": distinction.same,
        }
        identity = _distinction_assertion_identity(
            compared_assertion_id=comparison.assertion_id,
            inputs=input_refs,
            workspace_id=workspace_id,
            session_id=session_id,
            **content,
        )
        assertions.append(
            {
                "dimensions": {
                    "identity": identity,
                    "content": content,
                    "standing": "compared",
                    "source_provenance": (
                        "the two exact occurrence-bound productions carried in "
                        "support_basis"
                    ),
                    "responsibility": COMPARISON_ASSERTION_FIDELITY_RESPONSIBILITY,
                    "authority_warrant": (
                        "literal comparison evidence only; establishes no conflict, "
                        "meaning, preference, revision, or strengthening"
                    ),
                    "scope_locality": "the exact assertion_scope carried here",
                    "occurrence_preservation": (
                        "distinct Compare result preserved by its producing occurrence"
                    ),
                },
                "subject_kind": "assertion",
                "responsibility_owner": "this recorded assertion",
                "result": "assertion_production_coordinate_distinction",
                "assertion_subject": {
                    "compared_assertion_id": comparison.assertion_id,
                    "coordinate": distinction.coordinate,
                },
                "assertion_scope": {
                    "workspace_id": workspace_id,
                    "session_id": session_id,
                    "compared_productions": list(input_refs),
                },
                "support_basis": {"assertion_refs": list(input_refs)},
                "unknowns": [
                    "whether a literal difference is Applicable to either input "
                    "Assertion remains Unknown",
                    "whether any consumer will admit or consume this result remains "
                    "Unknown",
                ],
                "forbidden_inferences": [
                    "literal difference is not conflict",
                    "new availability does not revise either compared Assertion",
                    "recording does not establish Applicability, admission, "
                    "consumption, or Uptake",
                ],
            }
        )
    return ledger.append(
        ASSERTION_PRODUCTION_COMPARISON_RECORDED_KIND,
        workspace_id,
        {
            "dimensions": {
                "identity": "assertion-production-comparison-occurrence",
                "content": f"{len(assertions)} distinct comparison Assertions recorded",
                "standing": "recorded",
                "source_provenance": "two occurrence-bound Assertion productions",
                "authority_warrant": "literal Compare results only",
                "scope_locality": f"workspace:{workspace_id};session:{session_id}",
                "occurrence_preservation": "comparison occurrence durably recorded",
            },
            "producing_act": "Compare",
            "owner": comparison.owner,
            "responsibility": comparison.responsibility,
            "inputs": list(input_refs),
            "assertions": assertions,
        },
        session_id=session_id,
    )


def assertions_of_recorded_assertion_comparison(
    event: Event,
) -> tuple[RecordedAssertionProductionDistinction, ...]:
    """Recover and verify every addressable result of one recorded Compare."""

    if event.kind != ASSERTION_PRODUCTION_COMPARISON_RECORDED_KIND:
        raise AssertionComparisonError(
            f"{event.id} is {event.kind}, not an Assertion production Compare occurrence"
        )
    stated = event.payload.get("assertions")
    outer_inputs = event.payload.get("inputs")
    if not isinstance(stated, list):
        raise AssertionComparisonError(
            f"{event.id} does not preserve its distinct comparison Assertions"
        )
    required_ref = {"producing_event_id", "assertion_id"}
    if (
        not isinstance(outer_inputs, list)
        or len(outer_inputs) != 2
        or any(
            not isinstance(reference, dict)
            or set(reference) != required_ref
            or not all(isinstance(value, str) and value for value in reference.values())
            for reference in outer_inputs
        )
        or outer_inputs[0]["producing_event_id"]
        == outer_inputs[1]["producing_event_id"]
        or outer_inputs[0]["assertion_id"] != outer_inputs[1]["assertion_id"]
    ):
        raise AssertionComparisonError(
            f"{event.id} does not carry two distinct productions of one Assertion"
        )
    if len(stated) != len(COORDINATES):
        raise AssertionComparisonError(
            f"{event.id} does not carry every distinct Compare result"
        )
    recovered = []
    seen = set()
    seen_coordinates = set()
    for assertion in stated:
        dimensions = assertion.get("dimensions") if isinstance(assertion, dict) else None
        content = dimensions.get("content") if isinstance(dimensions, dict) else None
        identity = dimensions.get("identity") if isinstance(dimensions, dict) else None
        subject = assertion.get("assertion_subject") if isinstance(assertion, dict) else None
        scope = assertion.get("assertion_scope") if isinstance(assertion, dict) else None
        support = assertion.get("support_basis") if isinstance(assertion, dict) else None
        input_refs = support.get("assertion_refs") if isinstance(support, dict) else None
        if (
            assertion.get("subject_kind") != "assertion"
            or assertion.get("result") != "assertion_production_coordinate_distinction"
            or not isinstance(content, dict)
            or not isinstance(subject, dict)
            or not isinstance(scope, dict)
            or not isinstance(input_refs, list)
            or input_refs != outer_inputs
            or scope.get("compared_productions") != input_refs
            or not isinstance(scope.get("workspace_id"), str)
            or not isinstance(scope.get("session_id"), str)
            or scope.get("workspace_id") != event.workspace_id
            or scope.get("session_id") != event.session_id
            or subject.get("compared_assertion_id")
            != outer_inputs[0]["assertion_id"]
            or subject.get("coordinate") != content.get("coordinate")
        ):
            raise AssertionComparisonError(
                f"{event.id} carries an incoherent comparison Assertion"
            )
        required_content = {"coordinate", "present", "values", "same"}
        if set(content) != required_content:
            raise AssertionComparisonError(
                f"{event.id} carries an incomplete comparison result"
            )
        coordinate = content["coordinate"]
        present = content["present"]
        values = content["values"]
        same = content["same"]
        if (
            coordinate not in COORDINATES
            or coordinate in seen_coordinates
            or not isinstance(present, list)
            or len(present) != 2
            or not all(isinstance(value, bool) for value in present)
            or not isinstance(values, list)
            or len(values) != 2
            or not isinstance(same, bool)
            or same
            != (present[0] == present[1] and _exactly_same(values[0], values[1]))
        ):
            raise AssertionComparisonError(
                f"{event.id} carries a result outside the Compare output contract"
            )
        seen_coordinates.add(coordinate)
        canonical = _distinction_assertion_identity(
            compared_assertion_id=subject["compared_assertion_id"],
            inputs=input_refs,
            workspace_id=scope.get("workspace_id"),
            session_id=scope.get("session_id"),
            coordinate=content["coordinate"],
            present=content["present"],
            values=content["values"],
            same=content["same"],
        )
        if identity != canonical or identity in seen:
            raise AssertionComparisonError(
                f"{event.id} carries a comparison Assertion with invalid identity"
            )
        seen.add(identity)
        recovered.append(
            RecordedAssertionProductionDistinction(
                assertion_id=identity,
                producing_event_id=event.id,
                coordinate=content["coordinate"],
                payload=assertion,
            )
        )
    if seen_coordinates != set(COORDINATES):
        raise AssertionComparisonError(
            f"{event.id} does not carry the exact Compare coordinate set"
        )
    return tuple(recovered)
