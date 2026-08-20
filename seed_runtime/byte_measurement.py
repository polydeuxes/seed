"""Measure exact bytes across complete bounded acquisition_result occurrences.

This is the first acquisition boundary that does not receive its measured
subjects from a caller.  The subjects are the literal byte values carried by
the exact material linked from every acquisition_result occurrence in the declared
Localities through one recorded ledger boundary.

One byte value receives one count Assertion.  Recurrence is a separate
Assertion and exists only where the total count exceeds one.  The same byte
material establishes no character, word, position pair, grammar, or represented
relation.
"""

from __future__ import annotations


from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.event import Event
from seed_runtime.identities import new_identity
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.material_acquisition import (
    MaterialAcquisitionError,
    acquired_material_bytes,
    iter_exact_material_acquisition_results,
)
from seed_runtime.witness_material_acquisition import WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND


ACQUISITION_OCCURRED_KIND = WITNESS_MATERIAL_ACQUISITION_RECORDED_KIND
BYTE_MEASUREMENT_RECORDED_KIND = "operator.measurement.byte_counts_recorded"
BYTE_MEASUREMENT_RESULT_KIND = "exact byte-count Measurement results"
BYTE_PAIR_MEASUREMENT_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_counts_recorded"
)
BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_responsibility_assignment_recorded"
)
BYTE_PAIR_MEASUREMENT_RESULT_KIND = "exact byte-position-pair count Measurement results"
RESPONSIBILITY_UNESTABLISHED = "unestablished"
BYTE_OCCURRENCE_PRESERVATION = (
    "byte Measurement results recorded after Yield"
)
BYTE_PAIR_OCCURRENCE_PRESERVATION = (
    "byte-position-pair Measurement results recorded after Yield"
)
BYTE_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "addressed_act_identity",
        "act_occurrence_identity",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "measurement_rule",
        "source_localities",
        "completeness_boundary",
        "assertions",
    }
)
BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND = (
    "operator.measurement.byte_responsible_act_evidenced"
)
BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.measurement.byte_responsibility_assignment_recorded"
)
BYTE_PAIR_RESULT_COORDINATES = BYTE_RESULT_COORDINATES | {
    "addressed_act_identity",
    "act_occurrence_identity",
    "responsibility",
    "responsible_boundary",
    "source_assertion_reference",
    "source_movement_event_identity",
    "input_applicability",
    "input_applicability_event_identity",
    "input_role",
}
BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND = (
    "operator.measurement.byte_position_pair_responsible_act_evidenced"
)
BYTE_PAIR_APPLICABILITY_RECORDED_KIND = (
    "operator.measurement.byte_position_pair_input_applicability_recorded"
)
BYTE_PAIR_APPLICABILITY_RESULT_KIND = "byte-position-pair input Applicability result"
BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "dimensions",
        "exact_act",
        "responsibility",
        "responsible_boundary",
        "responsibility_assignment_reference",
        "applicability_act_identity",
        "applicability_act_occurrence_identity",
        "addressed_act_identity",
        "input_assertion_reference",
        "input_movement_event_identity",
        "input_role",
        "applicability",
    }
)
BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.measurement.byte_position_pair_applicability_act_evidenced"
)
ASSERTION_LOCALITY_MOVEMENT_KIND = "operator.assertion.locality_movement_recorded"
ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND = (
    "operator.assertion.locality_movement_responsibility_assignment_recorded"
)
ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND = (
    "operator.assertion.locality_movement_act_evidenced"
)
ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND = "Assertion Locality movement result"
EVENT_KIND_RESPONSIBILITIES = {
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Source.D",
    BYTE_MEASUREMENT_RECORDED_KIND: "01.Source.D",
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND: "01.Source.D",
    BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Source.D",
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND: "02.Acts.A",
    BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND: "02.Acts.A",
    BYTE_PAIR_APPLICABILITY_RECORDED_KIND: "01.Standing.E.1",
    BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND: "03.Movement.A",
    ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND: "02.Acts.A",
    ASSERTION_LOCALITY_MOVEMENT_KIND: "03.Movement.A",
}
ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY = (
    "make one exact preserved Assertion available in another Locality and "
    "preserve its identity, Standing, and carried limits"
)
BYTE_MEASUREMENT_RULE = (
    "each exact byte in exact recorded material acquisition material with the same exact byte "
    "material"
)
BYTE_PAIR_MEASUREMENT_RULE = (
    "each exact byte-pair occurrence in source order within one exact recorded material acquisition "
    "material occurrence with the same exact pair material and source order"
)
MEASUREMENT_EVIDENCE_SCOPE = (
    "exact byte-count Measurement Evidence; bounded byte Standing; source "
    "exact Standing coordinates preserved"
)
SOURCE_SET_EVIDENCE_SCOPE = (
    "exact bounded source-material Measurement Evidence"
)
PAIR_MEASUREMENT_EVIDENCE_SCOPE = (
    "declared exact-source ordered byte-position-pair Measurement Evidence; exact "
    "measured pair and order; bounded pair Standing; exact source Standing coordinates preserved"
)
BYTE_PAIR_RESULT_BOUNDARY = (
    "establish exact counts of byte-pair occurrences in source order within the exact "
    "bounded source material"
)
BYTE_PAIR_INPUT_ROLE = "exact bounded source material for position-byte Measurement"
SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY = "this Seed"
BYTE_MEASUREMENT_RESPONSIBILITY = (
    "perform the bounded exact-byte Measurement and Yield the findings "
    "established by its exact source occurrences, rule, Scope, Authority, and limits"
)
BYTE_PAIR_MEASUREMENT_RESPONSIBILITY = (
    "Yield exact byte-position-pair findings from an applicable exact bounded "
    "source material within its Scope, provenance, occurrence references, "
    "Authority, Unknown, and limits"
)
BYTE_PAIR_MEASUREMENT_AUTHORITY = "bounded repository authority"
BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY = (
    "determine Applicability of one exact source-material-set Assertion to one "
    "exact byte-position-pair Measurement Act"
)
BYTE_PAIR_APPLICABILITY_AUTHORITY = (
    "determine Applicability of this exact proposed input to this exact addressed "
    "Act; establishes no Applicability for another Act; the resulting Standing, "
    "not this authority, determines participation"
)
BYTE_PAIR_UNKNOWN = (
    "what this ordered byte position pair participates in or represents: Unknown",
)
BYTE_PAIR_LIMITS = (
    "an exact byte-position-pair count or recurrence bounded by the exact measured "
    "pair and order",
)
MEASURED_ASSERTION_RESPONSIBILITY = (
    "preserve this measured Assertion's carried Standing coordinates"
)
ASSERTION_RESPONSIBILITIES = {
    MEASURED_ASSERTION_RESPONSIBILITY: "01.Standing.D.1",
}


class ByteMeasurementError(ValueError):
    """The exact byte Measurement could not be performed as declared."""


def _require_exact_result_yield(
    ledger: EventLedger,
    event: Any,
    evidence: Any,
    act_evidence: Any,
    *,
    result_name: str,
    occurrence_coordinate: str = "act_occurrence_identity",
) -> None:
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=evidence.identity,
        responsible_act_evidence_event_identity=act_evidence.identity,
        recorded_result_occurrence_coordinate=occurrence_coordinate,
        responsible_act_occurrence_coordinate=occurrence_coordinate,
    )
    if not all(requirements.values()):
        raise ByteMeasurementError(
            f"{event.identity} names no exact {result_name} yield Evidence"
        )


def _yield_immediately_precedes_result(
    ledger: EventLedger, evidence: Event, result: Event
) -> bool:
    try:
        prefix = ledger.list(
            through=ledger.append_boundary_through_occurrence(result.identity)
        )
    except (TypeError, ValueError):
        return False
    return len(prefix) >= 2 and prefix[-2] == evidence and prefix[-1] == result


@dataclass(frozen=True)
class MeasuredByteCount:
    representation: int
    occurrences_carrying: int
    count: int


@dataclass(frozen=True)
class MeasuredByteInputs:
    source_localities: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    counts: tuple[MeasuredByteCount, ...]


@dataclass(frozen=True)
class MeasuredBytePairCount:
    representation: tuple[int, int]
    occurrences_carrying: int
    count: int


@dataclass(frozen=True)
class MeasuredBytePairInputs:
    source_localities: tuple[str, ...]
    completeness_boundary: EventLedgerBoundary
    source_material: tuple[dict[str, str], ...]
    source_assertion_reference: dict[str, str]
    source_movement_event_identity: str | None
    input_applicability: dict[str, Any]
    addressed_act_identity: str
    act_occurrence_identity: str
    counts: tuple[MeasuredBytePairCount, ...]


@dataclass(frozen=True)
class RecordedByteAssertion:
    assertion_identity: str
    recorded_occurrence_identity: str
    representation: int | None
    result: str
    _material_json: str
    _support_assertion_refs_json: str
    locality_movement_event_identity: str | None = None

    @property
    def material(self) -> dict[str, Any]:
        """Return one detached copy of the recorded JSON representation."""

        return json.loads(self._material_json)

    @property
    def support_assertion_references(self) -> tuple[dict[str, str], ...]:
        """Return detached occurrence-bound local support addresses."""

        return tuple(json.loads(self._support_assertion_refs_json))

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }


@dataclass(frozen=True)
class RecordedAssertionCarriedByLocalityMovement:
    """One exact Assertion carried by a Locality movement result."""

    recorded_occurrence_identity: str
    assertion_identity: str
    locality_movement_event_identity: str
    _source_assertion_coordinates_json: str

    @property
    def source_assertion_reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }

    @property
    def source_assertion_coordinates(self) -> dict[str, Any]:
        return json.loads(self._source_assertion_coordinates_json)


@dataclass(frozen=True)
class _RecordedPositionAssertionForLocalityMovement:
    recorded_occurrence_identity: str
    assertion_identity: str
    _source_assertion_coordinates_json: str

    @property
    def assertion_reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }

    @property
    def source_assertion_coordinates(self) -> dict[str, Any]:
        return json.loads(self._source_assertion_coordinates_json)


@dataclass(frozen=True)
class _RecordedPathComparisonFindingAssertionForLocalityMovement:
    recorded_occurrence_identity: str
    assertion_identity: str
    _source_assertion_coordinates_json: str

    @property
    def assertion_reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }

    @property
    def source_assertion_coordinates(self) -> dict[str, Any]:
        return json.loads(self._source_assertion_coordinates_json)


_AssertionLocalityMovementSource = (
    RecordedByteAssertion
    | _RecordedPositionAssertionForLocalityMovement
    | _RecordedPathComparisonFindingAssertionForLocalityMovement
)


@dataclass(frozen=True)
class RecordedBytePairAssertion:
    assertion_identity: str
    recorded_occurrence_identity: str
    representation: tuple[int, int] | None
    result: str
    _material_json: str
    _support_assertion_refs_json: str

    @property
    def material(self) -> dict[str, Any]:
        return json.loads(self._material_json)

    @property
    def support_assertion_references(self) -> tuple[dict[str, str], ...]:
        return tuple(json.loads(self._support_assertion_refs_json))

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }


@dataclass(frozen=True)
class _RecordedBytePairFinding:
    assertion_identity: str
    recorded_occurrence_identity: str
    representation: tuple[int, int]
    result: str
    _content_coordinates: tuple[int, int, int] | bool
    _local_support_assertion_identities: tuple[str, ...]

    @property
    def content(self) -> dict[str, int | bool]:
        if self.result == "recurrence":
            return {"recurrence_established": self._content_coordinates}
        input_count, occurrences_carrying, count = self._content_coordinates
        return {
            "input_count": input_count,
            "occurrences_carrying": occurrences_carrying,
            "count": count,
        }

    @property
    def reference(self) -> dict[str, str]:
        return {
            "recorded_occurrence_identity": self.recorded_occurrence_identity,
            "assertion_identity": self.assertion_identity,
        }


@dataclass(frozen=True)
class _RecordedBytePairMeasurementReading:
    results: tuple[RecordedBytePairAssertion, ...] | tuple[_RecordedBytePairFinding, ...]
    assignment: Event
    source: RecordedByteAssertion


@dataclass(frozen=True)
class _PairMeasurementReplayOccurrence:
    event: Event
    material: dict[str, Any]
    exact_material: bytes | None
    locality_identity: str | None


@dataclass
class _PairMeasurementReplayReading:
    assignment: Event
    source: RecordedByteAssertion
    assignment_occurrence: _PairMeasurementReplayOccurrence
    source_occurrence: _PairMeasurementReplayOccurrence
    movement_occurrence: _PairMeasurementReplayOccurrence | None
    applicability_act_occurrence: _PairMeasurementReplayOccurrence | None = None
    applicability_result_occurrence: _PairMeasurementReplayOccurrence | None = None
    measurement_act_occurrence: _PairMeasurementReplayOccurrence | None = None


def _canonical(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


_BYTE_PAIR_MEASUREMENT_RULE_JSON = _canonical(BYTE_PAIR_MEASUREMENT_RULE)


def _identity(
    *, result: str, subject: dict[str, Any], scope: dict[str, Any], content: Any
) -> str:
    carried = {"result": result, "subject": subject, "scope": scope, "content": content}
    return "byte-measurement:" + hashlib.sha256(
        _canonical(carried).encode("utf-8")
    ).hexdigest()


def _pair_assertion_identity(
    *,
    result: str,
    representation: tuple[int, int],
    canonical_scope: str,
    content: dict[str, Any],
) -> str:
    """Hash the fixed pair-Assertion JSON shape without rebuilding that shape."""

    first, second = representation
    canonical_subject = (
        '{"measurement_rule":'
        + _BYTE_PAIR_MEASUREMENT_RULE_JSON
        + f',"representation":[{first},{second}]}}'
    )
    if result == "recurrence":
        canonical_content = '{"recurrence_established":true}'
        canonical_result = '"recurrence"'
    else:
        canonical_content = (
            f'{{"count":{content["count"]},'
            f'"input_count":{content["input_count"]},'
            f'"occurrences_carrying":{content["occurrences_carrying"]}}}'
        )
        canonical_result = '"count"'
    carried = (
        '{"content":'
        + canonical_content
        + ',"result":'
        + canonical_result
        + ',"scope":'
        + canonical_scope
        + ',"subject":'
        + canonical_subject
        + "}"
    )
    return "byte-measurement:" + hashlib.sha256(carried.encode("utf-8")).hexdigest()


def _recorded_input_assertion_standing(
    ledger: EventLedger,
    source: RecordedByteAssertion,
    *,
    measurement_locality_identity: str,
) -> tuple[RecordedByteAssertion, dict[str, str | None]]:
    """Resolve the exact result occurrence carrying one proposed input.

    The Assertion's detached material is not Standing.  Its intact Measurement
    result occurrence is the Standing carrier; an exact movement occurrence
    preserves that Standing when the addressed Act has another Locality.
    """

    if type(source) is not RecordedByteAssertion:
        raise ByteMeasurementError(
            "byte-position-pair Applicability requires one recorded byte Assertion"
        )
    if source.locality_movement_event_identity is None:
        source_event = ledger.get(source.recorded_occurrence_identity)
        readings = assertions_of_recorded_byte_measurement(
            ledger, source.recorded_occurrence_identity
        )
        exact = next(
            (
                reading
                for reading in readings or ()
                if reading.assertion_identity == source.assertion_identity
            ),
            None,
        )
        if (
            source_event is None
            or source_event.locality_identity != measurement_locality_identity
        ):
            exact = None
    else:
        exact = _validate_moved_byte_assertion(
            ledger, source.locality_movement_event_identity
        )
        movement = ledger.get(source.locality_movement_event_identity)
        if (
            movement is None
            or movement.locality_identity != measurement_locality_identity
        ):
            exact = None
    if (
        exact is None
        or exact.result != "exact_source_material_set"
        or exact.reference != source.reference
        or exact.locality_movement_event_identity
        != source.locality_movement_event_identity
    ):
        raise ByteMeasurementError(
            "byte-position-pair Applicability requires exact input Standing"
        )
    return exact, {
        "recorded_measurement_result_occurrence_identity": (
            exact.recorded_occurrence_identity
        ),
        "assertion_identity": exact.assertion_identity,
        "locality_movement_result_occurrence_identity": (
            exact.locality_movement_event_identity
        ),
    }


def _pair_input_applicability(
    ledger: EventLedger,
    source: RecordedByteAssertion,
    *,
    assignment: Event,
    measurement_locality_identity: str,
) -> dict[str, Any]:
    """Determine this source Assertion's use by this exact pair Measurement."""

    source, input_standing = _recorded_input_assertion_standing(
        ledger,
        source,
        measurement_locality_identity=measurement_locality_identity,
    )
    return _pair_input_applicability_from_exact_source(
        source,
        assignment=assignment,
        measurement_locality_identity=measurement_locality_identity,
        input_standing=input_standing,
    )


def _pair_input_applicability_from_exact_source(
    source: RecordedByteAssertion,
    *,
    assignment: Event,
    measurement_locality_identity: str,
    input_standing: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    """Build Applicability from an already validated exact source carrier."""

    if input_standing is None:
        input_standing = {
            "recorded_measurement_result_occurrence_identity": (
                source.recorded_occurrence_identity
            ),
            "assertion_identity": source.assertion_identity,
            "locality_movement_result_occurrence_identity": (
                source.locality_movement_event_identity
            ),
        }
    material = source.material
    scope = material["assertion_scope"]
    content = {
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "addressed_act": "declared byte-position-pair Measurement",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _pair_measurement_assignment_reference(assignment)
        ),
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
    }
    if (
        material["dimensions"].get("authority") != "unestablished"
        or material["dimensions"].get("evidence_scope")
        != SOURCE_SET_EVIDENCE_SCOPE
    ):
        standing = "Unknown"
        basis = "the input carries no recognized Evidence scope for this exact source-material use"
        applicability_scope = scope
        source_provenance = material["dimensions"]["source_provenance"]
        input_authority = material["dimensions"]["authority"]
        input_unknown = material["unknown"]
        input_limits = material["limits"]
        negative_authority = {
            "carried": True,
            "value": input_limits,
            "treatment": "preserved as limits on this exact use",
        }
    else:
        standing = "applicable"
        basis = "exact bounded source material matches this Act and result boundary"
        applicability_scope = scope
        source_provenance = material["dimensions"]["source_provenance"]
        input_authority = material["dimensions"]["authority"]
        input_unknown = material["unknown"]
        input_limits = material["limits"]
        negative_authority = {
            "carried": True,
            "value": input_limits,
            "treatment": "preserved as limits on this exact use",
        }
    identity = "byte-pair-applicability:" + hashlib.sha256(
        _canonical(
            {
                "content": content,
                "scope": applicability_scope,
                "measurement_locality": measurement_locality_identity,
                "standing": standing,
            }
        ).encode("utf-8")
    ).hexdigest()
    return {
        "dimensions": {
            "identity": identity,
            "content": content,
            "standing": standing,
            "source_provenance": source_provenance,
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        },
        "result": "input_applicability",
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "addressed_act_occurrence_identity": None,
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _pair_measurement_assignment_reference(assignment)
        ),
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "addressed_act": "declared byte-position-pair Measurement",
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "measurement_locality": measurement_locality_identity,
        "scope_locality": applicability_scope,
        "input_standing": input_standing,
        "input_authority": input_authority,
        "input_unknown": input_unknown,
        "input_limits": input_limits,
        "conflicts": [basis] if standing == "conflicting" else [],
        "coordinate_treatment": {
            "support_relation_standing": {
                "carried": False,
                "treatment": "not established by Applicability",
            },
            "known_loss": {"carried": False, "treatment": "not represented by input"},
            "current_Standing": {
                "carried": False,
                "treatment": "not required for this historical bounded source material",
            },
            "negative_authority": negative_authority,
        },
        "unknown": [
            "what any byte or byte position pair represents: Unknown",
            *([basis] if standing == "Unknown" else []),
        ],
        "limits": [
            "Applicability to this Measurement is not Applicability for another Act, "
            "admission, represented relation, or authority for another use"
        ],
    }


def _acquired_bytes(ledger: EventLedger, occurrence) -> bytes:
    if ledger.integrity_of(occurrence.identity) == CORRUPTED:
        raise ByteMeasurementError(
            f"{occurrence.identity} is not an intact material acquisition occurrence"
        )
    try:
        return acquired_material_bytes(occurrence)
    except MaterialAcquisitionError as exc:
        raise ByteMeasurementError(str(exc)) from exc


def _exact_material_acquisition_results(
    ledger: EventLedger,
    locality_identity: str,
    *,
    through: EventLedgerBoundary,
):
    try:
        yield from iter_exact_material_acquisition_results(
            ledger,
            locality_identity,
            through=through,
        )
    except MaterialAcquisitionError as exc:
        raise ByteMeasurementError(
            "source carries a material-acquisition result without intact physiology"
        ) from exc


def measure_byte_counts(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
) -> MeasuredByteInputs:
    """Count every exact byte in every declared Locality through one boundary."""

    localities = tuple(dict.fromkeys(source_localities))
    if not localities or any(not isinstance(item, str) or not item for item in localities):
        raise ByteMeasurementError(
            "byte Measurement requires exact declared source Localities"
        )
    boundary = ledger.append_boundary()
    return _measure_byte_counts_through(
        ledger,
        localities=localities,
        boundary=boundary,
    )


def _measure_byte_counts_through(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
) -> MeasuredByteInputs:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_material: set[str] = set()
    carrying = [0] * 256
    totals = [0] * 256
    for locality in localities:
        for acquisition_result in _exact_material_acquisition_results(
            ledger, locality, through=boundary
        ):
            exact = _acquired_bytes(ledger, acquisition_result)
            if acquisition_result.identity in seen_material:
                raise ByteMeasurementError(
                    "one material acquisition occurrence cannot enter a byte Measurement twice"
                )
            seen_material.add(acquisition_result.identity)
            source_material.append({"material_acquisition_occurrence_identity": acquisition_result.identity})
            for value, count in Counter(exact).items():
                carrying[value] += 1
                totals[value] += count
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no acquisition_result through the Measurement boundary"
        )
    counts = tuple(
        MeasuredByteCount(
            representation=value,
            occurrences_carrying=carrying[value],
            count=totals[value],
        )
        for value in range(256)
        if totals[value] > 0
    )
    return MeasuredByteInputs(
        source_localities=localities,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        counts=counts,
    )


def _prepare_pair_source(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    measurement_locality_identity: str,
) -> tuple[RecordedByteAssertion, dict[str, Any], dict[str, Any]]:
    """Read one source before its act-local Applicability determination."""

    if (
        not isinstance(measurement_locality_identity, str)
        or not measurement_locality_identity
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires an exact Act Locality"
        )
    read = assertions_of_recorded_byte_measurement(
        ledger, source_measurement_event_identity
    )
    if read is None:
        raise ByteMeasurementError("byte-position-pair Measurement requires a source")
    source = next(
        (item for item in read if item.result == "exact_source_material_set"),
        None,
    )
    if source is None:
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires an exact source-material-set Assertion"
        )
    source = _move_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_locality=measurement_locality_identity,
    )
    material = source.material
    scope = material["assertion_scope"]
    content = material["dimensions"]["content"]
    return source, scope, content


def _movement_assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }


def _source_assertion_reference(
    source: _AssertionLocalityMovementSource,
) -> dict[str, str]:
    if type(source) is RecordedByteAssertion:
        return source.reference
    return source.assertion_reference


def _source_assertion_authority(
    source: _AssertionLocalityMovementSource,
) -> Any:
    if type(source) is RecordedByteAssertion:
        return source.material["dimensions"]["authority"]
    coordinates = source.source_assertion_coordinates
    if type(source) is _RecordedPositionAssertionForLocalityMovement:
        return coordinates["dimensions"]["authority"]
    return coordinates["authority"]


def _source_assertion_coordinates(
    source: _AssertionLocalityMovementSource,
) -> dict[str, Any]:
    if type(source) is RecordedByteAssertion:
        return source.material
    return source.source_assertion_coordinates


def _source_assertion_from_reference(
    ledger: EventLedger, reference: Any
) -> tuple[_AssertionLocalityMovementSource, Event]:
    if type(reference) is not dict or set(reference) != {
        "recorded_occurrence_identity",
        "assertion_identity",
    }:
        raise ByteMeasurementError("Assertion movement carries no exact source")
    source_event = ledger.get(reference["recorded_occurrence_identity"])
    if source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("Assertion movement source cannot be read")
    if source_event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
        source_results = assertions_of_recorded_byte_measurement(
            ledger, source_event.identity
        )
        source = next(
            (
                item
                for item in source_results or ()
                if item.assertion_identity == reference["assertion_identity"]
            ),
            None,
        )
        if source is not None:
            return source, source_event

    from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
        BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
        _recorded_position_assertion_coordinates_for_locality_movement,
    )

    if source_event.kind == BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND:
        try:
            coordinates = _recorded_position_assertion_coordinates_for_locality_movement(
                ledger,
                result_event_identity=source_event.identity,
                assertion_identity=reference["assertion_identity"],
            )
        except ValueError:
            pass
        else:
            return _RecordedPositionAssertionForLocalityMovement(
                recorded_occurrence_identity=source_event.identity,
                assertion_identity=reference["assertion_identity"],
                _source_assertion_coordinates_json=_canonical(coordinates),
            ), source_event

    from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
        _recorded_path_comparison_finding_assertion_coordinates_for_locality_movement,
    )

    if (
        source_event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        try:
            coordinates = _recorded_path_comparison_finding_assertion_coordinates_for_locality_movement(
                ledger,
                result_event_identity=source_event.identity,
                assertion_identity=reference["assertion_identity"],
            )
        except ValueError:
            pass
        else:
            return _RecordedPathComparisonFindingAssertionForLocalityMovement(
                recorded_occurrence_identity=source_event.identity,
                assertion_identity=reference["assertion_identity"],
                _source_assertion_coordinates_json=_canonical(coordinates),
            ), source_event
    raise ByteMeasurementError("Assertion movement source cannot be read")


def _source_measurement_standing_coordinates(source_event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": source_event.identity,
        "result_identity": source_event.material["result_identity"],
        "act_occurrence_identity": source_event.material["act_occurrence_identity"],
        "responsible_act_evidence_identity": source_event.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": source_event.material[
            "evidence_of_yield_relation_identity"
        ],
    }


def _source_assertion_is_carried(
    source_event: Event, locality_standing: dict[str, Any]
) -> bool:
    from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
        COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    )

    if (
        source_event.kind
        == COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND
    ):
        return (
            locality_standing.get("comparison_result_occurrences", {}).get(
                source_event.identity, object()
            )
            is None
        )
    return locality_standing.get("measurement_occurrences", {}).get(
        source_event.identity
    ) == _source_measurement_standing_coordinates(source_event)


def _require_current_movement_source_standing(
    ledger: EventLedger,
    *,
    source_event: Event,
    locality_standing: dict[str, Any],
) -> str:
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    current = read_operator_locality_standing(
        ledger, locality_identity=source_event.locality_identity
    )
    boundary = locality_standing.get("through_event_occurrence_identity")
    if (
        locality_standing != current
        or type(boundary) is not str
        or not boundary
        or not _source_assertion_is_carried(source_event, locality_standing)
    ):
        raise ByteMeasurementError(
            "Assertion movement assignment requires exact current source Standing"
        )
    return boundary


def _require_current_movement_destination_standing(
    ledger: EventLedger,
    *,
    destination_locality: str,
    locality_standing: dict[str, Any],
    assignment_identity: str | None = None,
) -> str | None:
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    current = read_operator_locality_standing(
        ledger, locality_identity=destination_locality
    )
    boundary = locality_standing.get("through_event_occurrence_identity")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    if (
        locality_standing != current
        or locality_standing.get("locality_identity") != destination_locality
        or (boundary is not None and (type(boundary) is not str or not boundary))
        or (
            assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(assignment_identity, object()) is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement requires exact current destination Standing"
        )
    return boundary


def _movement_assignment_material(
    *,
    source: _AssertionLocalityMovementSource,
    source_event: Event,
    source_locality: str,
    destination_locality: str,
    source_standing_boundary_identity: str,
    destination_standing_boundary_identity: str | None,
    assignment_identity: str,
    assignment_subject_identity: str,
    movement_act_identity: str,
    movement_act_occurrence_identity: str,
    movement_result_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "movement_act_identity": movement_act_identity,
        "movement_act_occurrence_identity": movement_act_occurrence_identity,
        "movement_result_identity": movement_result_identity,
        "book_clause_identity": "03.Movement.A",
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "source_assertion_reference": _source_assertion_reference(source),
        "source_assertion_coordinates": _source_assertion_coordinates(source),
        "source_locality": source_locality,
        "destination_locality": destination_locality,
        "source_standing_boundary_identity": source_standing_boundary_identity,
        "destination_standing_boundary_identity": (
            destination_standing_boundary_identity
        ),
        "determination": (
            "the exact preserved Assertion available in another Locality"
        ),
        "scope": {
            "source_assertion_reference": _source_assertion_reference(source),
            "source_standing_boundary_identity": source_standing_boundary_identity,
            "destination_standing_boundary_identity": (
                destination_standing_boundary_identity
            ),
        },
        "authority": _source_assertion_authority(source),
        "limits": [
            "assignment is bounded to the exact source Assertion and source and "
            "destination Standing boundaries"
        ],
        "unknown": ["what the exact Assertion represents: Unknown"],
    }


def _require_exact_movement_assignment_and_source(
    ledger: EventLedger, assignment: Event
) -> tuple[_AssertionLocalityMovementSource, Event]:
    if (
        type(assignment) is not Event
        or assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or assignment.locality_identity is None
        or ledger.get(assignment.identity) != assignment
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "Assertion movement requires an exact Responsibility assignment"
        )
    source, source_event = _source_assertion_from_reference(
        ledger, assignment.material.get("source_assertion_reference")
    )
    identity_coordinates = (
        "assignment_identity",
        "assignment_subject_identity",
        "movement_act_identity",
        "movement_act_occurrence_identity",
        "movement_result_identity",
    )
    identities = {
        coordinate: assignment.material.get(coordinate)
        for coordinate in identity_coordinates
    }
    source_boundary = assignment.material.get("source_standing_boundary_identity")
    destination_boundary = assignment.material.get(
        "destination_standing_boundary_identity"
    )
    if (
        type(source_boundary) is not str
        or not source_boundary
        or any(
            type(identity) is not str or not identity
            for identity in identities.values()
        )
        or len(set(identities.values())) != len(identities)
        or assignment.material
        != _movement_assignment_material(
            source=source,
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=assignment.locality_identity,
            source_standing_boundary_identity=source_boundary,
            destination_standing_boundary_identity=destination_boundary,
            **identities,
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement requires an exact source and assignment"
        )
    return source, source_event


def record_assertion_locality_movement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    destination_locality: str,
    source_locality_standing: dict[str, Any],
    destination_locality_standing: dict[str, Any],
) -> Event:
    """Record the exact Responsibility assignment for one Assertion movement."""

    if type(destination_locality) is not str or not destination_locality:
        raise ByteMeasurementError("Assertion movement requires a destination Locality")
    exact_source, source_event = _source_assertion_from_reference(
        ledger, source.reference
    )
    if exact_source != source:
        raise ByteMeasurementError("Assertion movement requires its exact source")
    if source_event.locality_identity == destination_locality:
        raise ByteMeasurementError("same-Locality Assertion requires no movement")
    source_boundary = _require_current_movement_source_standing(
        ledger,
        source_event=source_event,
        locality_standing=source_locality_standing,
    )
    destination_boundary = _require_current_movement_destination_standing(
        ledger,
        destination_locality=destination_locality,
        locality_standing=destination_locality_standing,
    )
    identities = {
        "assignment_identity": new_identity("assertion_locality_movement_assignment"),
        "assignment_subject_identity": new_identity(
            "assertion_locality_movement_assignment_subject"
        ),
        "movement_act_identity": new_identity("assertion_locality_movement_act"),
        "movement_act_occurrence_identity": new_identity(
            "assertion_locality_movement_occurrence"
        ),
        "movement_result_identity": new_identity(
            "assertion_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("Assertion movement lifecycle identities collapsed")
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
        _movement_assignment_material(
            source=source,
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_standing_boundary_identity=source_boundary,
            destination_standing_boundary_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def _read_assertion_locality_movement_responsibility_assignment(
    ledger: EventLedger,
    assignment_event_identity: str,
    *,
    prior_destination_standing: dict[str, Any] | None = None,
) -> tuple[Event, _AssertionLocalityMovementSource, Event]:
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or assignment.locality_identity is None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment is absent or corrupted"
        )
    material = assignment.material
    source, source_event = _source_assertion_from_reference(
        ledger, material.get("source_assertion_reference")
    )
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "assignment_identity",
            "assignment_subject_identity",
            "movement_act_identity",
            "movement_act_occurrence_identity",
            "movement_result_identity",
        )
    }
    source_boundary = material.get("source_standing_boundary_identity")
    destination_boundary = material.get("destination_standing_boundary_identity")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(source_boundary) is not str
        or not source_boundary
        or (
            destination_boundary is not None
            and (type(destination_boundary) is not str or not destination_boundary)
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment carries malformed coordinates"
        )
    expected = _movement_assignment_material(
        source=source,
        source_event=source_event,
        source_locality=source_event.locality_identity,
        destination_locality=assignment.locality_identity,
        source_standing_boundary_identity=source_boundary,
        destination_standing_boundary_identity=destination_boundary,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment coordinates are not exact"
        )
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing_through,
    )

    try:
        source_standing = read_operator_locality_standing_through(
            ledger,
            locality_identity=source_event.locality_identity,
            through_event_occurrence_identity=source_boundary,
        )
        if prior_destination_standing is None:
            prior_destination_standing = read_operator_locality_standing_through(
                ledger,
                locality_identity=assignment.locality_identity,
                through_event_occurrence_identity=destination_boundary,
            )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment has no exact Standing"
        ) from error
    if not _source_assertion_is_carried(source_event, source_standing):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment has no exact source Standing"
        )
    prior_destination_boundary = prior_destination_standing.get(
        "through_event_occurrence_identity"
    )
    carried_assignments = prior_destination_standing.get(
        "responsibility_assignment_occurrences"
    )
    destination_boundary_is_exact = prior_destination_boundary == destination_boundary
    assignment_is_carried_later = bool(
        type(prior_destination_boundary) is str
        and prior_destination_boundary
        and type(carried_assignments) is dict
        and carried_assignments.get(assignment.identity, object()) is None
    )
    if (
        prior_destination_standing.get("locality_identity")
        != assignment.locality_identity
        or not (destination_boundary_is_exact or assignment_is_carried_later)
    ):
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment has no exact destination Standing"
        )
    order = (assignment.identity,)
    if destination_boundary is not None:
        order = (destination_boundary, assignment.identity)
    if assignment_is_carried_later and prior_destination_boundary != assignment.identity:
        order = (*order, prior_destination_boundary)
    try:
        ledger.occurrences_in_append_order(
            order, locality_identity=assignment.locality_identity
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "Assertion movement Responsibility assignment order is false"
        ) from error
    return assignment, source, source_event


def get_assertion_locality_movement_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    return _read_assertion_locality_movement_responsibility_assignment(
        ledger, assignment_event_identity
    )[0]


def _movement_act_material(assignment: Event) -> dict[str, Any]:
    return {
        "act": "Assertion Locality movement",
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": _movement_assignment_reference(
            assignment
        ),
        "movement_act_identity": assignment.material["movement_act_identity"],
        "movement_act_occurrence_identity": assignment.material[
            "movement_act_occurrence_identity"
        ],
        "source_assertion_reference": assignment.material[
            "source_assertion_reference"
        ],
        "source_locality": assignment.material["source_locality"],
        "destination_locality": assignment.locality_identity,
        "locality_relation": {
            "first_subject": assignment.material["source_assertion_reference"],
            "second_subject": assignment.locality_identity,
            "relation_occurrence_identity": assignment.material[
                "movement_act_occurrence_identity"
            ],
        },
        "authority": assignment.material["authority"],
        "evidence_scope": "Evidence for this exact Assertion Locality movement",
    }


def record_assertion_locality_movement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    assignment, _source, _source_event = (
        _read_assertion_locality_movement_responsibility_assignment(
            ledger, responsibility_assignment_event_identity
        )
    )
    _require_current_movement_destination_standing(
        ledger,
        destination_locality=assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        assignment_identity=assignment.identity,
    )
    for prior in ledger.iter_locality_kind(
        assignment.locality_identity,
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
    ):
        if prior.material.get("responsibility_assignment_reference") == (
            _movement_assignment_reference(assignment)
        ):
            raise ByteMeasurementError(
                "Assertion movement Responsibility assignment already carries an Act"
            )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
        _movement_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _record_assertion_locality_movement_act_from_carried_standing(
    ledger: EventLedger,
    *,
    assignment: Event,
    destination_standing: dict[str, Any],
) -> Event:
    try:
        _require_exact_movement_assignment_and_source(ledger, assignment)
    except (ByteMeasurementError, TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "Assertion movement Act requires an exact source and assignment"
        ) from error
    if (
        assignment.kind
        != ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND
        or ledger.get(assignment.identity) != assignment
        or ledger.integrity_of(assignment.identity) == CORRUPTED
        or destination_standing.get("locality_identity")
        != assignment.locality_identity
        or destination_standing.get("through_event_occurrence_identity")
        != assignment.identity
        or destination_standing.get(
            "responsibility_assignment_occurrences", {}
        ).get(assignment.identity, object())
        is not None
        or ledger.append_boundary_through_occurrence(assignment.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "Assertion movement Act requires exact carried assignment Standing"
        )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND,
        _movement_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def _read_assertion_locality_movement_act_evidence(
    ledger: EventLedger,
    act_evidence_event_identity: str,
    *,
    prior_destination_standing: dict[str, Any] | None = None,
) -> tuple[Event, Event, _AssertionLocalityMovementSource]:
    act = ledger.get(act_evidence_event_identity)
    if (
        act is None
        or act.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
        or ledger.integrity_of(act.identity) == CORRUPTED
    ):
        raise ByteMeasurementError("Assertion movement Act Evidence is absent or corrupted")
    reference = act.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise ByteMeasurementError("Assertion movement Act carries no exact assignment")
    assignment, source, _source_event = (
        _read_assertion_locality_movement_responsibility_assignment(
            ledger,
            reference.get("recorded_occurrence_identity"),
            prior_destination_standing=prior_destination_standing,
        )
    )
    if (
        reference != _movement_assignment_reference(assignment)
        or act.locality_identity != assignment.locality_identity
        or act.material != _movement_act_material(assignment)
    ):
        raise ByteMeasurementError("Assertion movement Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, act.identity),
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError("Assertion movement Act order is false") from error
    return act, assignment, source


def _movement_result_material(
    assignment: Event,
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["movement_result_identity"],
        "movement_act_identity": assignment.material["movement_act_identity"],
        "movement_act_occurrence_identity": assignment.material[
            "movement_act_occurrence_identity"
        ],
        "responsibility": ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": _movement_assignment_reference(
            assignment
        ),
        "source_assertion_reference": assignment.material[
            "source_assertion_reference"
        ],
        "source_assertion_coordinates": assignment.material[
            "source_assertion_coordinates"
        ],
        "assertion_identity": assignment.material["source_assertion_reference"][
            "assertion_identity"
        ],
        "source_locality": assignment.material["source_locality"],
        "destination_locality": assignment.locality_identity,
        "locality_relation": {
            "first_subject": assignment.material["source_assertion_reference"],
            "second_subject": assignment.locality_identity,
            "relation_occurrence_identity": assignment.material[
                "movement_act_occurrence_identity"
            ],
        },
        "preserved_coordinates": [
            "Evidence",
            "Authority",
            "Scope",
            "Unknown",
            "limits",
            "Standing",
        ],
        "authority": assignment.material["authority"],
        "movement_scope": (
            "Locality movement bounded to this exact Assertion; establishes no "
            "different identity or Standing"
        ),
    }


def record_assertion_locality_movement_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act, assignment, _source = _read_assertion_locality_movement_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    for kind in (
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        ASSERTION_LOCALITY_MOVEMENT_KIND,
    ):
        for prior in ledger.iter_locality_kind(assignment.locality_identity, kind):
            if prior.material.get("responsible_act_evidence_identity") == act.identity:
                raise ByteMeasurementError(
                    "Assertion movement Act already carries a Yield or result"
                )
    return _append_assertion_locality_movement_result(
        ledger, act=act, assignment=assignment
    )


def _append_assertion_locality_movement_result(
    ledger: EventLedger, *, act: Event, assignment: Event
) -> Event:
    result_material = _movement_result_material(assignment)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=assignment.locality_identity,
        exact_act="Assertion Locality movement",
        act_occurrence_identity=assignment.material[
            "movement_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=act.identity,
        result_kind=ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND,
        result_identity=assignment.material["movement_result_identity"],
        result_content=result_material,
        responsibility=ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY,
        occurrence_boundary="assertion_locality_movement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        responsible_act_occurrence_coordinate="movement_act_occurrence_identity",
        coordinates_of_recorded_result={key: (key,) for key in result_material},
    )
    _require_exact_movement_assignment_and_source(ledger, assignment)
    if (
        ledger.get(act.identity) != act
        or ledger.integrity_of(act.identity) == CORRUPTED
        or act.material != _movement_act_material(assignment)
        or ledger.get(evidence.identity) != evidence
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(evidence.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "Assertion movement result requires exact source, Act, and Yield Evidence"
        )
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_KIND,
        {
            **_movement_result_material(assignment),
            "responsible_act_evidence_identity": act.identity,
            "evidence_of_yield_relation_identity": evidence.identity,
        },
        locality_identity=assignment.locality_identity,
    )


def _record_assertion_locality_movement_result_from_carried_act(
    ledger: EventLedger,
    *,
    act: Event,
    assignment: Event,
    destination_standing: dict[str, Any] | None = None,
) -> Event:
    if destination_standing is not None:
        try:
            _require_exact_movement_assignment_and_source(ledger, assignment)
        except (ByteMeasurementError, TypeError, ValueError) as error:
            raise ByteMeasurementError(
                "Assertion movement result requires an exact source and Act"
            ) from error
        if act.material != _movement_act_material(assignment):
            raise ByteMeasurementError(
                "Assertion movement result requires an exact source and Act"
            )
    if (
        ledger.get(act.identity) != act
        or act.kind != ASSERTION_LOCALITY_MOVEMENT_ACT_EVIDENCE_KIND
        or ledger.integrity_of(act.identity) == CORRUPTED
        or act.locality_identity != assignment.locality_identity
        or act.material != _movement_act_material(assignment)
        or ledger.append_boundary_through_occurrence(act.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "Assertion movement result requires its exact carried Act at the append tip"
        )
    return _append_assertion_locality_movement_result(
        ledger, act=act, assignment=assignment
    )


def _move_byte_assertion_to_locality(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    destination_locality: str,
) -> RecordedByteAssertion:
    """Preserve one Assertion movement without copying the Assertion."""

    source_event = ledger.get(source.recorded_occurrence_identity)
    if source_event is None:
        raise ByteMeasurementError("Assertion locality movement requires its source")
    if source_event.locality_identity == destination_locality:
        return source
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    assignment = record_assertion_locality_movement_responsibility_assignment(
        ledger,
        source=source,
        destination_locality=destination_locality,
        source_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=source_event.locality_identity
        ),
        destination_locality_standing=read_operator_locality_standing(
            ledger, locality_identity=destination_locality
        ),
    )
    act = record_assertion_locality_movement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=destination_locality
        ),
    )
    movement = record_assertion_locality_movement_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    exact = _validate_moved_byte_assertion(ledger, movement.identity)
    if exact is None:
        raise ByteMeasurementError("Assertion locality movement is absent")
    return exact


def move_recorded_byte_assertion_to_locality(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    destination_locality: str,
) -> RecordedByteAssertion:
    return _move_byte_assertion_to_locality(
        ledger,
        source=source,
        destination_locality=destination_locality,
    )


def _move_assertion_reference_to_locality(
    ledger: EventLedger,
    *,
    source_assertion_reference: dict[str, str],
    destination_locality: str,
) -> RecordedAssertionCarriedByLocalityMovement:
    """Carry one exact supported Assertion through one 03.Movement.A occurrence."""

    source, source_event = _source_assertion_from_reference(
        ledger, source_assertion_reference
    )
    if type(source) is RecordedByteAssertion:
        raise ByteMeasurementError(
            "this movement road requires a position or path-comparison Assertion"
        )
    if source_event.locality_identity == destination_locality:
        raise ByteMeasurementError("same-Locality Assertion requires no movement")
    from seed_runtime.operator_locality_standing import (
        _carry_assertion_locality_movement_act_into_standing,
        _carry_assertion_locality_movement_assignment_into_standing,
        _carry_assertion_locality_movement_result_into_standing,
        read_operator_locality_standing,
    )

    source_standing = read_operator_locality_standing(
        ledger, locality_identity=source_event.locality_identity
    )
    _require_current_movement_source_standing(
        ledger, source_event=source_event, locality_standing=source_standing
    )
    destination_standing = read_operator_locality_standing(
        ledger, locality_identity=destination_locality
    )
    _require_current_movement_destination_standing(
        ledger,
        destination_locality=destination_locality,
        locality_standing=destination_standing,
    )
    assignment = _record_movement_assignment_from_carried_standings(
        ledger,
        source=source,
        source_event=source_event,
        source_standing=source_standing,
        destination_locality=destination_locality,
        destination_standing=destination_standing,
    )
    destination_standing = (
        _carry_assertion_locality_movement_assignment_into_standing(
            ledger,
            destination_standing,
            assignment,
            source=source,
            source_event=source_event,
            source_standing=source_standing,
        )
    )
    act = _record_assertion_locality_movement_act_from_carried_standing(
        ledger,
        assignment=assignment,
        destination_standing=destination_standing,
    )
    destination_standing = _carry_assertion_locality_movement_act_into_standing(
        ledger,
        destination_standing,
        act,
        responsibility_assignment=assignment,
    )
    movement = _record_assertion_locality_movement_result_from_carried_act(
        ledger,
        act=act,
        assignment=assignment,
        destination_standing=destination_standing,
    )
    _destination_standing, carried = (
        _carry_assertion_locality_movement_result_into_standing(
            ledger,
            destination_standing,
            movement,
            responsible_act_evidence=act,
            responsibility_assignment=assignment,
            source=source,
        )
    )
    if type(carried) is not RecordedAssertionCarriedByLocalityMovement:
        raise ByteMeasurementError(
            "Assertion Locality movement carries no exact result"
        )
    return carried


def _record_movement_assignment_from_carried_standings(
    ledger: EventLedger,
    *,
    source: _AssertionLocalityMovementSource,
    source_event: Event,
    source_standing: dict[str, Any],
    destination_locality: str,
    destination_standing: dict[str, Any],
) -> Event:
    source_boundary = source_standing.get("through_event_occurrence_identity")
    destination_boundary = destination_standing.get(
        "through_event_occurrence_identity"
    )
    if (
        source_standing.get("locality_identity") != source_event.locality_identity
        or type(source_boundary) is not str
        or not source_boundary
        or not _source_assertion_is_carried(source_event, source_standing)
        or destination_standing.get("locality_identity") != destination_locality
        or (
            destination_boundary is not None
            and (
                type(destination_boundary) is not str
                or not destination_boundary
            )
        )
    ):
        raise ByteMeasurementError(
            "Assertion movement assignment requires exact carried source and destination Standing"
        )
    identities = {
        "assignment_identity": new_identity(
            "assertion_locality_movement_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "assertion_locality_movement_assignment_subject"
        ),
        "movement_act_identity": new_identity("assertion_locality_movement_act"),
        "movement_act_occurrence_identity": new_identity(
            "assertion_locality_movement_occurrence"
        ),
        "movement_result_identity": new_identity(
            "assertion_locality_movement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError("Assertion movement lifecycle identities collapsed")
    return ledger.append(
        ASSERTION_LOCALITY_MOVEMENT_RESPONSIBILITY_ASSIGNMENT_KIND,
        _movement_assignment_material(
            source=source,
            source_event=source_event,
            source_locality=source_event.locality_identity,
            destination_locality=destination_locality,
            source_standing_boundary_identity=source_boundary,
            destination_standing_boundary_identity=destination_boundary,
            **identities,
        ),
        locality_identity=destination_locality,
    )


def move_recorded_byte_assertions_to_locality(
    ledger: EventLedger,
    *,
    sources: tuple[RecordedByteAssertion, ...],
    destination_locality: str,
) -> tuple[RecordedByteAssertion, ...]:
    """Move one exact result's Assertions in one bounded same-call lifecycle."""

    if not sources:
        return ()
    source_event_identity = sources[0].recorded_occurrence_identity
    if any(
        source.recorded_occurrence_identity != source_event_identity
        for source in sources
    ):
        raise ByteMeasurementError(
            "bounded Assertion movement requires one exact source result"
        )
    source_event = ledger.get(source_event_identity)
    if source_event is None or source_event.locality_identity is None:
        raise ByteMeasurementError("Assertion locality movement requires its source")
    if source_event.locality_identity == destination_locality:
        return sources
    exact_sources = {
        source.assertion_identity: source
        for source in assertions_of_recorded_byte_measurement(
            ledger, source_event_identity
        )
        or ()
    }
    if any(exact_sources.get(source.assertion_identity) != source for source in sources):
        raise ByteMeasurementError(
            "bounded Assertion movement requires each exact source Assertion"
        )
    from seed_runtime.operator_locality_standing import (
        _carry_assertion_locality_movement_act_into_standing,
        _carry_assertion_locality_movement_assignment_into_standing,
        _carry_assertion_locality_movement_result_into_standing,
        read_operator_locality_standing,
    )

    source_standing = read_operator_locality_standing(
        ledger, locality_identity=source_event.locality_identity
    )
    _require_current_movement_source_standing(
        ledger, source_event=source_event, locality_standing=source_standing
    )
    destination_standing = read_operator_locality_standing(
        ledger, locality_identity=destination_locality
    )
    _require_current_movement_destination_standing(
        ledger,
        destination_locality=destination_locality,
        locality_standing=destination_standing,
    )
    moved = []
    for source in sources:
        assignment = _record_movement_assignment_from_carried_standings(
            ledger,
            source=source,
            source_event=source_event,
            source_standing=source_standing,
            destination_locality=destination_locality,
            destination_standing=destination_standing,
        )
        destination_standing = (
            _carry_assertion_locality_movement_assignment_into_standing(
                ledger,
                destination_standing,
                assignment,
                source=source,
                source_event=source_event,
                source_standing=source_standing,
            )
        )
        act = _record_assertion_locality_movement_act_from_carried_standing(
            ledger,
            assignment=assignment,
            destination_standing=destination_standing,
        )
        destination_standing = _carry_assertion_locality_movement_act_into_standing(
            ledger,
            destination_standing,
            act,
            responsibility_assignment=assignment,
        )
        movement = _record_assertion_locality_movement_result_from_carried_act(
            ledger,
            act=act,
            assignment=assignment,
            destination_standing=destination_standing,
        )
        destination_standing, exact = (
            _carry_assertion_locality_movement_result_into_standing(
                ledger,
                destination_standing,
                movement,
                responsible_act_evidence=act,
                responsibility_assignment=assignment,
                source=source,
            )
        )
        moved.append(exact)
    return tuple(moved)


def _assertion_carried_by_locality_movement_result(
    *,
    movement: Event,
    responsibility_assignment: Event,
    source: _AssertionLocalityMovementSource,
) -> RecordedByteAssertion | RecordedAssertionCarriedByLocalityMovement:
    """Carry the source Assertion with one exact validated movement result."""

    if (
        movement.material.get("responsibility_assignment_reference")
        != _movement_assignment_reference(responsibility_assignment)
        or responsibility_assignment.material.get("source_assertion_reference")
        != _source_assertion_reference(source)
        or movement.material.get("source_assertion_reference")
        != _source_assertion_reference(source)
    ):
        raise ByteMeasurementError(
            "Assertion locality movement carries no exact source"
        )
    if type(source) is RecordedByteAssertion:
        return RecordedByteAssertion(
            assertion_identity=source.assertion_identity,
            recorded_occurrence_identity=source.recorded_occurrence_identity,
            representation=source.representation,
            result=source.result,
            _material_json=_canonical(source.material),
            _support_assertion_refs_json=_canonical(
                list(source.support_assertion_references)
            ),
            locality_movement_event_identity=movement.identity,
        )
    return RecordedAssertionCarriedByLocalityMovement(
        recorded_occurrence_identity=source.recorded_occurrence_identity,
        assertion_identity=source.assertion_identity,
        locality_movement_event_identity=movement.identity,
        _source_assertion_coordinates_json=_canonical(
            _source_assertion_coordinates(source)
        ),
    )


def _validate_moved_byte_assertion(
    ledger: EventLedger,
    movement_event_identity: str,
    *,
    prior_destination_standing: dict[str, Any] | None = None,
) -> RecordedByteAssertion | RecordedAssertionCarriedByLocalityMovement | None:
    movement = ledger.get(movement_event_identity)
    if movement is None or movement.kind != ASSERTION_LOCALITY_MOVEMENT_KIND:
        return None
    if ledger.integrity_of(movement.identity) == CORRUPTED:
        raise ByteMeasurementError("Assertion locality movement is corrupted")
    act_evidence, assignment, source = (
        _read_assertion_locality_movement_act_evidence(
            ledger,
            movement.material.get("responsible_act_evidence_identity"),
            prior_destination_standing=prior_destination_standing,
        )
    )
    if (
        movement.locality_identity != assignment.locality_identity
        or movement.material.get("responsibility_assignment_reference")
        != _movement_assignment_reference(assignment)
    ):
        raise ByteMeasurementError(
            "Assertion locality movement carries no exact assignment"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=movement.identity,
        evidence_of_yield_relation_event_identity=movement.material.get("evidence_of_yield_relation_identity"),
        responsible_act_evidence_event_identity=movement.material.get(
            "responsible_act_evidence_identity"
        ),
        recorded_result_occurrence_coordinate="movement_act_occurrence_identity",
        responsible_act_occurrence_coordinate="movement_act_occurrence_identity",
    )
    yield_evidence = ledger.get(
        movement.material.get("evidence_of_yield_relation_identity")
    )
    if (
        not all(requirements.values())
        or yield_evidence is None
        or yield_evidence.material.get("result_kind")
        != ASSERTION_LOCALITY_MOVEMENT_RESULT_KIND
        or yield_evidence.material.get("occurrence_boundary")
        != "assertion_locality_movement"
    ):
        raise ByteMeasurementError("Assertion movement Evidence of Yield relation is not exact")
    expected = {
        **_movement_result_material(assignment),
        "responsible_act_evidence_identity": act_evidence.identity,
        "evidence_of_yield_relation_identity": movement.material.get(
            "evidence_of_yield_relation_identity"
        ),
    }
    if movement.material != expected:
        raise ByteMeasurementError("Assertion locality movement is not exact")
    return _assertion_carried_by_locality_movement_result(
        movement=movement,
        responsibility_assignment=assignment,
        source=source,
    )


def _measure_byte_position_pair_counts_through(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
    source_assertion_reference: dict[str, str],
    source_movement_event_identity: str | None,
    input_applicability: dict[str, Any],
    addressed_act_identity: str,
    act_occurrence_identity: str,
) -> MeasuredBytePairInputs:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )

    source_material: list[dict[str, str]] = []
    seen_material: set[str] = set()
    totals: dict[bytes, int] = {}
    carrying: dict[bytes, int] = {}
    for locality in localities:
        for acquisition_result in _exact_material_acquisition_results(
            ledger, locality, through=boundary
        ):
            if ledger.integrity_of(acquisition_result.identity) == CORRUPTED:
                raise ByteMeasurementError(
                    "corrupted acquisition_result cannot participate in byte-position-pair Measurement"
                )
            exact = _acquired_bytes(ledger, acquisition_result)
            if acquisition_result.identity in seen_material:
                raise ByteMeasurementError(
                    "one material acquisition occurrence cannot enter a pair Measurement twice"
                )
            seen_material.add(acquisition_result.identity)
            source_material.append({"material_acquisition_occurrence_identity": acquisition_result.identity})
            seen: set[bytes] = set()
            for index in range(len(exact) - 1):
                pair = exact[index : index + 2]
                totals[pair] = totals.get(pair, 0) + 1
                seen.add(pair)
            for pair in seen:
                carrying[pair] = carrying.get(pair, 0) + 1
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no acquisition_result through the Measurement boundary"
        )
    counts = tuple(
        MeasuredBytePairCount(
            representation=(pair[0], pair[1]),
            occurrences_carrying=carrying[pair],
            count=totals[pair],
        )
        for pair in totals
    )
    return MeasuredBytePairInputs(
        source_localities=localities,
        completeness_boundary=boundary,
        source_material=tuple(source_material),
        source_assertion_reference=source_assertion_reference,
        source_movement_event_identity=source_movement_event_identity,
        input_applicability=input_applicability,
        addressed_act_identity=addressed_act_identity,
        act_occurrence_identity=act_occurrence_identity,
        counts=counts,
    )


def _assertions(measured: MeasuredByteInputs) -> list[dict[str, Any]]:
    scope = {
        "source_localities": list(measured.source_localities),
    }
    source_subject = {"measurement_rule": BYTE_MEASUREMENT_RULE}
    source_content = {
        "source_material": list(measured.source_material),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
    }
    source_identity = _identity(
        result="exact_source_material_set",
        subject=source_subject,
        scope=scope,
        content=source_content,
    )
    results: list[dict[str, Any]] = [
        {
            "dimensions": {
                "identity": source_identity,
                "content": source_content,
                "source_provenance": (
                    "complete declared material acquisition through one boundary"
                ),
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": "unestablished",
                "evidence_scope": SOURCE_SET_EVIDENCE_SCOPE,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": "exact_source_material_set",
            "assertion_subject": source_subject,
            "assertion_scope": scope,
            "input_support": {
                "occurrence_references": [
                    item["material_acquisition_occurrence_identity"]
                    for item in measured.source_material
                ],
                "local_assertion_references": [],
            },
            "conflicts": "Unknown",
            "unknown": ["what the exact source bytes represent: Unknown"],
            "limits": [
                "exact source-material set bounded by source occurrences and "
                "completeness boundary"
            ],
        }
    ]

    def assertion(
        *,
        result: str,
        item: MeasuredByteCount,
        content: dict[str, Any],
        provenance: str,
        local_support_references: list[str],
    ):
        subject = {
            "representation": item.representation,
            "measurement_rule": BYTE_MEASUREMENT_RULE,
        }
        identity = _identity(result=result, subject=subject, scope=scope, content=content)
        return {
            "dimensions": {
                "identity": identity,
                "content": content,
                "source_provenance": provenance,
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": "unestablished",
                "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "input_support": {
                "occurrence_references": [],
                "local_assertion_references": local_support_references,
            },
            "conflicts": "Unknown",
            "unknown": ["what this byte participates in or represents: Unknown"],
            "limits": [
                "exact byte count or recurrence bounded by source occurrences and "
                "Measurement rule"
            ],
        }

    for item in measured.counts:
        count_content = {
            "input_count": len(measured.source_material),
            "occurrences_carrying": item.occurrences_carrying,
            "count": item.count,
        }
        count = assertion(
            result="count",
            item=item,
            content=count_content,
            provenance="the exact source-material-set Assertion carried here",
            local_support_references=[source_identity],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    provenance="the exact count Assertion carried here",
                    local_support_references=[count["dimensions"]["identity"]],
                )
            )
    return results


def _byte_measurement_source_material(
    ledger: EventLedger,
    *,
    localities: tuple[str, ...],
    boundary: EventLedgerBoundary,
) -> tuple[dict[str, str], ...]:
    missing = [
        locality
        for locality in localities
        if not ledger.has_locality(locality, through=boundary)
    ]
    if missing:
        raise ByteMeasurementError(
            "declared source Localities are absent through the Measurement boundary: "
            + ", ".join(missing)
        )
    source_material = []
    seen_material = set()
    from seed_runtime.operator_material_acquisition import (
        read_operator_material_acquire_locality_relation_requirements,
    )

    for locality in localities:
        for acquisition_result in _exact_material_acquisition_results(
            ledger, locality, through=boundary
        ):
            _acquired_bytes(ledger, acquisition_result)
            if not all(
                read_operator_material_acquire_locality_relation_requirements(
                    ledger,
                    recorded_result_event_identity=acquisition_result.identity,
                ).values()
            ):
                # Exact acquisition availability does not supply the Locality
                # occurrence and Evidence required by 01.Source.D.
                continue
            if acquisition_result.identity in seen_material:
                raise ByteMeasurementError(
                    "one material acquisition occurrence cannot enter a byte Measurement twice"
                )
            seen_material.add(acquisition_result.identity)
            source_material.append(
                {"material_acquisition_occurrence_identity": acquisition_result.identity}
            )
    if not source_material:
        raise ByteMeasurementError(
            "declared source Localities contain no exact material result with "
            "material-to-this-Seed Locality occurrence and Evidence through the "
            "Measurement boundary"
        )
    return tuple(source_material)


def _byte_measurement_assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }


def _byte_measurement_assignment_material(
    *,
    source_localities: tuple[str, ...],
    source_material: tuple[dict[str, str], ...],
    completeness_boundary_identity: str,
    standing_boundary_identity: str | None,
    assignment_identity: str,
    assignment_subject_identity: str,
    measurement_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "measurement_act_identity": measurement_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "measurement_rule": BYTE_MEASUREMENT_RULE,
        "source_localities": list(source_localities),
        "source_occurrence_references": [
            dict(reference) for reference in source_material
        ],
        "completeness_boundary_identity": completeness_boundary_identity,
        "standing_boundary_identity": standing_boundary_identity,
        "scope": {
            "recording_standing_boundary_identity": standing_boundary_identity,
            "source_localities": list(source_localities),
            "completeness_boundary_identity": completeness_boundary_identity,
        },
        "authority": "unestablished",
        "limits": [
            "assignment is bounded to the exact declared source Localities, "
            "material acquisition occurrences, and completeness boundary"
        ],
        "unknown": ["what the exact source material represents: Unknown"],
    }


def _require_current_byte_measurement_standing(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
) -> str | None:
    if type(locality_standing) is not dict:
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    from seed_runtime.operator_locality_standing import (
        read_operator_locality_standing,
    )

    current = read_operator_locality_standing(
        ledger, locality_identity=recording_locality_identity
    )
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    boundary = locality_standing.get("through_event_occurrence_identity")
    if (
        locality_standing != current
        or locality_standing.get("locality_identity")
        != recording_locality_identity
        or (boundary is not None and (type(boundary) is not str or not boundary))
        or (
            required_assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(required_assignment_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    return boundary


def _require_carried_byte_measurement_standing_at_tip(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
) -> str:
    if type(locality_standing) is not dict:
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    boundary = locality_standing.get("through_event_occurrence_identity")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    if (
        locality_standing.get("locality_identity")
        != recording_locality_identity
        or type(boundary) is not str
        or not boundary
        or (
            required_assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(required_assignment_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    event = ledger.get(boundary)
    locality_events = (
        ledger.list_locality(recording_locality_identity)
        if event is not None
        else ()
    )
    if (
        event is None
        or event.locality_identity != recording_locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or not locality_events
        or locality_events[-1].identity != boundary
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact current Locality Standing"
        )
    return boundary


def _prepare_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
) -> tuple[tuple[str, ...], EventLedgerBoundary, tuple[dict[str, str], ...]]:
    if (
        type(recording_locality_identity) is not str
        or not recording_locality_identity
    ):
        raise ByteMeasurementError(
            "byte Measurement recording requires an exact Locality"
        )
    localities = tuple(dict.fromkeys(source_localities))
    if (
        not localities
        or any(type(locality) is not str or not locality for locality in localities)
    ):
        raise ByteMeasurementError(
            "byte Measurement requires exact declared source Localities"
        )
    boundary = ledger.append_boundary()
    source_material = _byte_measurement_source_material(
        ledger, localities=localities, boundary=boundary
    )
    return localities, boundary, source_material


def _append_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_localities: tuple[str, ...],
    source_material: tuple[dict[str, str], ...],
    completeness_boundary_identity: str,
    standing_boundary_identity: str | None,
    recording_locality_identity: str,
) -> Event:
    identities = {
        "assignment_identity": new_identity("byte_measurement_assignment"),
        "assignment_subject_identity": new_identity(
            "byte_measurement_assignment_subject"
        ),
        "measurement_act_identity": new_identity("byte_measurement_act"),
        "act_occurrence_identity": new_identity("byte_measurement_occurrence"),
        "measurement_result_identity": new_identity("byte_measurement_result"),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError(
            "byte Measurement lifecycle identities collapsed"
        )
    return ledger.append(
        BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _byte_measurement_assignment_material(
            source_localities=source_localities,
            source_material=source_material,
            completeness_boundary_identity=completeness_boundary_identity,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=recording_locality_identity,
    )


def record_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    """Record one exact-byte Measurement Responsibility assignment."""

    localities, boundary, source_material = (
        _prepare_byte_measurement_responsibility_assignment(
            ledger,
            source_localities=source_localities,
            recording_locality_identity=recording_locality_identity,
        )
    )
    standing_boundary_identity = _require_current_byte_measurement_standing(
        ledger,
        recording_locality_identity=recording_locality_identity,
        locality_standing=locality_standing,
    )
    if ledger.append_boundary() != boundary:
        raise ByteMeasurementError(
            "byte Measurement global recording boundary changed before assignment"
        )
    return _append_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=boundary.identity,
        standing_boundary_identity=standing_boundary_identity,
        recording_locality_identity=recording_locality_identity,
    )


def _record_byte_measurement_responsibility_assignment_from_carried_standing(
    ledger: EventLedger,
    *,
    source_localities: Iterable[str],
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    localities, boundary, source_material = (
        _prepare_byte_measurement_responsibility_assignment(
            ledger,
            source_localities=source_localities,
            recording_locality_identity=recording_locality_identity,
        )
    )
    standing_boundary_identity = (
        _require_carried_byte_measurement_standing_at_tip(
            ledger,
            recording_locality_identity=recording_locality_identity,
            locality_standing=locality_standing,
        )
    )
    if ledger.append_boundary() != boundary:
        raise ByteMeasurementError(
            "byte Measurement global recording boundary changed before assignment"
        )
    return _append_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=boundary.identity,
        standing_boundary_identity=standing_boundary_identity,
        recording_locality_identity=recording_locality_identity,
    )


def _read_byte_measurement_responsibility_assignment(
    ledger: EventLedger,
    assignment_event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, tuple[str, ...], EventLedgerBoundary, tuple[dict[str, str], ...]]:
    if type(assignment_event_identity) is not str or not assignment_event_identity:
        raise ByteMeasurementError(
            "byte Measurement requires one exact Responsibility assignment"
        )
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(assignment.locality_identity) is not str
        or not assignment.locality_identity
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment is absent or corrupted"
        )
    material = assignment.material
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "assignment_identity",
            "assignment_subject_identity",
            "measurement_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    localities_value = material.get("source_localities")
    completeness_boundary_identity = material.get(
        "completeness_boundary_identity"
    )
    standing_boundary_identity = material.get("standing_boundary_identity")
    if (
        any(type(identity) is not str or not identity for identity in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(localities_value) is not list
        or not localities_value
        or any(type(locality) is not str or not locality for locality in localities_value)
        or len(set(localities_value)) != len(localities_value)
        or type(completeness_boundary_identity) is not str
        or not completeness_boundary_identity
        or (
            standing_boundary_identity is not None
            and (
                type(standing_boundary_identity) is not str
                or not standing_boundary_identity
            )
        )
    ):
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment carries malformed coordinates"
        )
    localities = tuple(localities_value)
    boundary = EventLedgerBoundary(completeness_boundary_identity)
    source_material = _byte_measurement_source_material(
        ledger, localities=localities, boundary=boundary
    )
    expected = _byte_measurement_assignment_material(
        source_localities=localities,
        source_material=source_material,
        completeness_boundary_identity=completeness_boundary_identity,
        standing_boundary_identity=standing_boundary_identity,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment coordinates are not exact"
        )
    if prior_standing is None:
        from seed_runtime.operator_locality_standing import (
            _operator_standing_validation_context,
            read_operator_locality_standing_through,
        )

        prior_standing = _operator_standing_validation_context(
            ledger, locality_identity=assignment.locality_identity
        )
        if prior_standing is None:
            try:
                prior_standing = read_operator_locality_standing_through(
                    ledger,
                    locality_identity=assignment.locality_identity,
                    through_event_occurrence_identity=standing_boundary_identity,
                )
            except (TypeError, ValueError) as error:
                raise ByteMeasurementError(
                    "byte Measurement Responsibility assignment has no exact prior Standing"
                ) from error
    carried_assignments = prior_standing.get(
        "responsibility_assignment_occurrences"
    )
    prior_boundary_identity = prior_standing.get(
        "through_event_occurrence_identity"
    )
    boundary_is_exact = prior_boundary_identity == standing_boundary_identity
    assignment_is_carried_later = bool(
        type(prior_boundary_identity) is str
        and prior_boundary_identity
        and type(carried_assignments) is dict
        and carried_assignments.get(assignment.identity, object()) is None
    )
    if (
        prior_standing.get("locality_identity") != assignment.locality_identity
        or not (boundary_is_exact or assignment_is_carried_later)
    ):
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment has no exact prior Standing"
        )
    if boundary_is_exact:
        order = (assignment.identity,)
        if standing_boundary_identity is not None:
            order = (standing_boundary_identity, assignment.identity)
    elif prior_boundary_identity == assignment.identity:
        order = (assignment.identity,)
    else:
        order = (assignment.identity, prior_boundary_identity)
        if standing_boundary_identity is not None:
            order = (
                standing_boundary_identity,
                assignment.identity,
                prior_boundary_identity,
            )
    try:
        ledger.occurrences_in_append_order(
            order, locality_identity=assignment.locality_identity
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "byte Measurement Responsibility assignment order is false"
        ) from error
    return assignment, localities, boundary, source_material


def get_byte_measurement_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    return _read_byte_measurement_responsibility_assignment(
        ledger, assignment_event_identity
    )[0]


def _byte_measurement_act_evidence_material(
    assignment: Event,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": assignment.material[
            "measurement_act_identity"
        ],
        "act_occurrence_identity": assignment.material[
            "act_occurrence_identity"
        ],
        "act": "declared exact-byte Measurement",
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _byte_measurement_assignment_reference(assignment)
        ),
        "source_localities": list(assignment.material["source_localities"]),
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence bounded to this exact responsible Measurement "
            "occurrence; establishes no responsibility"
        ),
    }


def _append_byte_measurement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    assignment: Event,
) -> Event:
    for prior_act in ledger.iter_locality_kind(
        assignment.locality_identity,
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    ):
        if (
            prior_act.material.get("responsibility_assignment_reference")
            == _byte_measurement_assignment_reference(assignment)
            or prior_act.material.get("act_occurrence_identity")
            == assignment.material["act_occurrence_identity"]
        ):
            raise ByteMeasurementError(
                "byte Measurement Responsibility assignment already carries an Act"
            )
    return ledger.append(
        BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
        _byte_measurement_act_evidence_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def record_byte_measurement_responsible_act_evidence(
    ledger: EventLedger,
    *,
    responsibility_assignment_event_identity: str,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    """Record Evidence for one exact assigned byte Measurement Act."""

    assignment, _localities, _boundary, _source_material = (
        _read_byte_measurement_responsibility_assignment(
            ledger, responsibility_assignment_event_identity
        )
    )
    _require_current_byte_measurement_standing(
        ledger,
        recording_locality_identity=assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=assignment.identity,
    )
    return _append_byte_measurement_responsible_act_evidence(
        ledger,
        assignment=assignment,
    )


def _record_byte_measurement_responsible_act_evidence_from_carried_standing(
    ledger: EventLedger,
    *,
    responsibility_assignment: Event,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    if (
        type(responsibility_assignment) is not Event
        or responsibility_assignment.kind
        != BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or ledger.integrity_of(responsibility_assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement requires its exact carried assignment"
        )
    exact_assignment, _localities, _boundary, _source_material = (
        _read_byte_measurement_responsibility_assignment(
            ledger,
            responsibility_assignment.identity,
            prior_standing=responsibility_assignment_standing,
        )
    )
    if exact_assignment != responsibility_assignment:
        raise ByteMeasurementError(
            "byte Measurement requires its exact carried assignment"
        )
    _require_carried_byte_measurement_standing_at_tip(
        ledger,
        recording_locality_identity=responsibility_assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=responsibility_assignment.identity,
    )
    return _append_byte_measurement_responsible_act_evidence(
        ledger,
        assignment=responsibility_assignment,
    )


def _measurement_of_responsible_act_evidence(
    ledger: EventLedger,
    responsible_act_evidence_event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Any, Event, MeasuredByteInputs]:
    event = ledger.get(responsible_act_evidence_event_identity)
    if (
        event is None
        or event.kind != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement Yield requires one exact responsible Act Evidence occurrence"
        )
    material = event.material
    assignment_reference = material.get("responsibility_assignment_reference")
    if (
        type(assignment_reference) is not dict
        or set(assignment_reference)
        != {
            "recorded_occurrence_identity",
            "assignment_identity",
            "assignment_subject_identity",
        }
        or type(event.locality_identity) is not str
        or not event.locality_identity
    ):
        raise ByteMeasurementError(
            "byte Measurement responsible Act Evidence carries malformed coordinates"
        )
    assignment, localities, boundary, _source_material = (
        _read_byte_measurement_responsibility_assignment(
            ledger,
            assignment_reference.get("recorded_occurrence_identity"),
            prior_standing=prior_standing,
        )
    )
    measured = _measure_byte_counts_through(
        ledger,
        localities=localities,
        boundary=boundary,
    )
    expected = _byte_measurement_act_evidence_material(assignment)
    if (
        assignment_reference
        != _byte_measurement_assignment_reference(assignment)
        or event.locality_identity != assignment.locality_identity
        or material != expected
    ):
        raise ByteMeasurementError(
            "byte Measurement responsible Act Evidence is not exact"
        )
    return event, assignment, measured


def _require_byte_measurement_act_without_result(
    ledger: EventLedger, act_evidence: Event
) -> None:
    for kind in (
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        BYTE_MEASUREMENT_RECORDED_KIND,
    ):
        for event in ledger.iter_locality_kind(act_evidence.locality_identity, kind):
            if (
                event.material.get("responsible_act_evidence_identity")
                == act_evidence.identity
            ):
                raise ByteMeasurementError(
                    "byte Measurement responsible Act occurrence already has a Yield or result"
                )


def _record_byte_measurement_result_from_exact_inputs(
    ledger: EventLedger,
    *,
    responsible_act_evidence: Event,
    assignment: Event,
    measured: MeasuredByteInputs,
) -> Event:
    result_identity = assignment.material["measurement_result_identity"]
    result_material = {
        "result_identity": result_identity,
        "dimensions": {
                "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source-material-set, byte count, and recurrence Assertions"
                ),
                "source_provenance": "complete declared material acquisition through one boundary",
                "authority": "unestablished",
                "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
        },
        "exact_act": "declared exact-byte Measurement",
        "addressed_act_identity": responsible_act_evidence.material[
            "addressed_act_identity"
        ],
        "act_occurrence_identity": responsible_act_evidence.material[
            "act_occurrence_identity"
        ],
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _byte_measurement_assignment_reference(assignment)
        ),
        "measurement_rule": BYTE_MEASUREMENT_RULE,
        "source_localities": list(measured.source_localities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "assertions": _assertions(measured),
    }
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=responsible_act_evidence.locality_identity,
        exact_act="declared exact-byte Measurement",
        act_occurrence_identity=responsible_act_evidence.material[
            "act_occurrence_identity"
        ],
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind=BYTE_MEASUREMENT_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=BYTE_MEASUREMENT_RESPONSIBILITY,
        occurrence_boundary="byte_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    return ledger.append(
        BYTE_MEASUREMENT_RECORDED_KIND,
        {
            **result_material,
            "evidence_of_yield_relation_identity": evidence.identity,
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "occurrence_preservation": BYTE_OCCURRENCE_PRESERVATION,
        },
        locality_identity=responsible_act_evidence.locality_identity,
    )


def record_byte_measurement_result(
    ledger: EventLedger,
    *,
    responsible_act_evidence_event_identity: str,
):
    """Record the Yield and result of one exact evidenced byte Measurement Act."""

    supplied = ledger.get(responsible_act_evidence_event_identity)
    if (
        supplied is None
        or supplied.kind != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(supplied.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte Measurement Yield requires one exact responsible Act Evidence occurrence"
        )
    _require_byte_measurement_act_without_result(ledger, supplied)

    responsible_act_evidence, assignment, measured = (
        _measurement_of_responsible_act_evidence(
            ledger, supplied.identity
        )
    )

    return _record_byte_measurement_result_from_exact_inputs(
        ledger,
        responsible_act_evidence=responsible_act_evidence,
        assignment=assignment,
        measured=measured,
    )


def _record_byte_measurement_result_from_carried_act_evidence(
    ledger: EventLedger,
    *,
    responsible_act_evidence: Event,
    responsibility_assignment: Event,
    locality_standing: dict[str, Any],
) -> Event:
    if (
        type(responsible_act_evidence) is not Event
        or type(responsibility_assignment) is not Event
        or ledger.get(responsible_act_evidence.identity)
        != responsible_act_evidence
        or responsible_act_evidence.kind
        != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires exact carried lifecycle occurrences"
        )
    exact_act, exact_assignment, measured = (
        _measurement_of_responsible_act_evidence(
            ledger,
            responsible_act_evidence.identity,
            prior_standing=locality_standing,
        )
    )
    if (
        exact_act != responsible_act_evidence
        or exact_assignment != responsibility_assignment
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires exact carried lifecycle occurrences"
        )
    if (
        ledger.get(responsible_act_evidence.identity) != responsible_act_evidence
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "byte Measurement result requires its exact Act at the append tip"
        )
    return _record_byte_measurement_result_from_exact_inputs(
        ledger,
        responsible_act_evidence=responsible_act_evidence,
        assignment=responsibility_assignment,
        measured=measured,
    )


def _assertions_of_recorded_byte_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[RecordedByteAssertion, ...] | None:
    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_identity} is not a byte Measurement occurrence")
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot return byte results")
    material = event.material
    if set(material) != BYTE_RESULT_COORDINATES | {
        "evidence_of_yield_relation_identity",
        "responsible_act_evidence_identity",
        "occurrence_preservation",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact byte result and recording surfaces"
        )
    if (
        material.get("occurrence_preservation") != BYTE_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared exact-byte Measurement"
        or material.get("responsibility") != BYTE_MEASUREMENT_RESPONSIBILITY
        or material.get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or not isinstance(material.get("addressed_act_identity"), str)
        or not material["addressed_act_identity"]
        or not isinstance(material.get("act_occurrence_identity"), str)
        or not material["act_occurrence_identity"]
        or material["addressed_act_identity"] == material["act_occurrence_identity"]
        or material.get("dimensions")
        != {
            "identity": "byte-count-measurement-occurrence",
                "content": (
                    "exact source-material-set, byte count, and recurrence Assertions"
                ),
            "source_provenance": (
                "complete declared material acquisition through one boundary"
            ),
            "authority": "unestablished",
            "evidence_scope": MEASUREMENT_EVIDENCE_SCOPE,
        }
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact Measurement and "
            "recording-occurrence Evidence"
        )
    evidence_identity = material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if (
        evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_MEASUREMENT_RESULT_KIND
        or evidence.material.get("coordinates_of_carried_result")
        != [coordinate for coordinate in material if coordinate in BYTE_RESULT_COORDINATES]
        or evidence.material.get("dimensions", {}).get("responsibility")
        != BYTE_MEASUREMENT_RESPONSIBILITY
        or evidence.material.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["act_occurrence_identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact byte Measurement yield Evidence"
        )
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    act_evidence = ledger.get(act_evidence_identity) if isinstance(act_evidence_identity, str) else None
    expected_act_evidence = {
        "addressed_act_identity": material["addressed_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": "declared exact-byte Measurement",
        "responsibility": BYTE_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": material[
            "responsibility_assignment_reference"
        ],
        "source_localities": material["source_localities"],
        "authority": "unestablished",
        "evidence_scope": (
            "Evidence bounded to this exact responsible Measurement "
            "occurrence; establishes no responsibility"
        ),
    }
    if (
        act_evidence is None
        or act_evidence.kind != BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND
        or act_evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(act_evidence.identity) == CORRUPTED
        or act_evidence.material != expected_act_evidence
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact responsible byte Measurement occurrence Evidence"
        )
    _validated_act, assignment, measured = (
        _measurement_of_responsible_act_evidence(
            ledger,
            act_evidence.identity,
            prior_standing=prior_standing,
        )
    )
    _require_exact_result_yield(
        ledger,
        event,
        evidence,
        act_evidence,
        result_name="byte Measurement",
    )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_localities")
    if (
        material.get("measurement_rule") != BYTE_MEASUREMENT_RULE
        or not isinstance(boundary_value, dict)
        or set(boundary_value) != {"identity"}
        or not isinstance(boundary_value["identity"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact byte Measurement boundary"
        )
    if (
        material.get("responsibility_assignment_reference")
        != _byte_measurement_assignment_reference(assignment)
        or measured.completeness_boundary.identity != boundary_value["identity"]
        or list(measured.source_localities) != localities_value
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not establish its Seed-native Measurement boundary"
        )
    expected = _assertions(measured)
    if material.get("assertions") != expected:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the results of its complete bounded source read"
        )
    read = []
    for assertion in expected:
        local_identities = assertion["input_support"]["local_assertion_references"]
        read.append(
            RecordedByteAssertion(
                assertion_identity=assertion["dimensions"]["identity"],
                recorded_occurrence_identity=event.identity,
                representation=assertion["assertion_subject"].get("representation"),
                result=assertion["result"],
                _material_json=_canonical(assertion),
                _support_assertion_refs_json=_canonical(
                    [
                        {
                            "recorded_occurrence_identity": event.identity,
                            "assertion_identity": local_identity,
                        }
                        for local_identity in local_identities
                    ]
                ),
            )
        )
    return tuple(read)


def assertions_of_recorded_byte_measurement(
    ledger: EventLedger, event_identity: str
) -> tuple[RecordedByteAssertion, ...] | None:
    """Read the exact byte results after replaying their bounded source read."""

    return _assertions_of_recorded_byte_measurement(
        ledger, event_identity
    )


def _pair_assertions(measured: MeasuredBytePairInputs) -> list[dict[str, Any]]:
    scope = {
        "source_localities": list(measured.source_localities),
    }
    results: list[dict[str, Any]] = []

    def assertion(
        *,
        result: str,
        item: MeasuredBytePairCount,
        content: dict[str, Any],
        provenance: str,
        local_support_references: list[str],
        source_support_references: list[dict[str, str]],
    ) -> dict[str, Any]:
        subject = {
            "representation": list(item.representation),
            "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
        }
        identity = _identity(result=result, subject=subject, scope=scope, content=content)
        return {
            "dimensions": {
                "identity": identity,
                "content": content,
                "source_provenance": provenance,
                "responsibility": MEASURED_ASSERTION_RESPONSIBILITY,
                "authority": "unestablished",
                "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
            },
            "subject_kind": "assertion",
            "responsible_boundary": "this recorded assertion",
            "result": result,
            "assertion_subject": subject,
            "assertion_scope": scope,
            "input_support": {
                "assertion_references": source_support_references,
                "local_assertion_references": local_support_references,
            },
            "conflicts": "Unknown",
            "unknown": list(BYTE_PAIR_UNKNOWN),
            "limits": list(BYTE_PAIR_LIMITS),
        }

    for item in measured.counts:
        count = assertion(
            result="count",
            item=item,
            content={
                "input_count": len(measured.source_material),
                "occurrences_carrying": item.occurrences_carrying,
                "count": item.count,
            },
            provenance="the exact source-material-set Assertion referenced here",
            local_support_references=[],
            source_support_references=[measured.source_assertion_reference],
        )
        results.append(count)
        if item.count > 1:
            results.append(
                assertion(
                    result="recurrence",
                    item=item,
                    content={"recurrence_established": True},
                    provenance="the exact count Assertion carried here",
                    local_support_references=[count["dimensions"]["identity"]],
                    source_support_references=[],
                )
            )
    return results


def _pair_measurement_assignment_reference(assignment: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": assignment.identity,
        "assignment_identity": assignment.material["assignment_identity"],
        "assignment_subject_identity": assignment.material[
            "assignment_subject_identity"
        ],
    }


def _pair_measurement_assignment_material(
    *,
    source: RecordedByteAssertion,
    scope: dict[str, Any],
    content: dict[str, Any],
    recording_locality_identity: str,
    standing_boundary_identity: str,
    assignment_identity: str,
    assignment_subject_identity: str,
    applicability_act_identity: str,
    applicability_act_occurrence_identity: str,
    applicability_result_identity: str,
    measurement_act_identity: str,
    measurement_act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": (
            applicability_act_occurrence_identity
        ),
        "applicability_result_identity": applicability_result_identity,
        "measurement_act_identity": measurement_act_identity,
        "measurement_act_occurrence_identity": measurement_act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
        "source_assertion_reference": source.reference,
        "source_movement_event_identity": source.locality_movement_event_identity,
        "source_localities": list(scope["source_localities"]),
        "source_occurrence_references": list(content["source_material"]),
        "completeness_boundary_identity": content["completeness_boundary"][
            "identity"
        ],
        "standing_boundary_identity": standing_boundary_identity,
        "recording_locality_identity": recording_locality_identity,
        "scope": {
            "recording_standing_boundary_identity": standing_boundary_identity,
            "recording_locality_identity": recording_locality_identity,
            "source_localities": list(scope["source_localities"]),
            "completeness_boundary_identity": content["completeness_boundary"][
                "identity"
            ],
        },
        "authority": BYTE_PAIR_MEASUREMENT_AUTHORITY,
        "input_authority": source.material["dimensions"]["authority"],
        "limits": [
            "assignment is bounded to the exact source Assertion, Locality, "
            "completeness boundary, rule, Applicability, and Measurement result"
        ],
        "unknown": [
            "what measured byte position pair represents: Unknown"
        ],
    }


def _require_exact_pair_measurement_assignment_event(
    ledger: EventLedger,
    assignment: Event,
    source: RecordedByteAssertion,
) -> None:
    """Validate one recorded assignment against its already validated source."""

    if (
        type(assignment) is not Event
        or type(source) is not RecordedByteAssertion
        or ledger.get(assignment.identity) != assignment
        or assignment.kind
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or assignment.locality_identity is None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment is not exact"
        )
    material = assignment.material
    identity_keys = (
        "assignment_identity",
        "assignment_subject_identity",
        "applicability_act_identity",
        "applicability_act_occurrence_identity",
        "applicability_result_identity",
        "measurement_act_identity",
        "measurement_act_occurrence_identity",
        "measurement_result_identity",
    )
    identities = {key: material.get(key) for key in identity_keys}
    boundary = material.get("standing_boundary_identity")
    if (
        source.reference != material.get("source_assertion_reference")
        or source.locality_movement_event_identity
        != material.get("source_movement_event_identity")
        or type(boundary) is not str
        or not boundary
        or any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or material
        != _pair_measurement_assignment_material(
            source=source,
            scope=source.material["assertion_scope"],
            content=source.material["dimensions"]["content"],
            recording_locality_identity=assignment.locality_identity,
            standing_boundary_identity=boundary,
            **identities,
        )
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment coordinates are not exact"
        )


def _pair_source_is_carried(
    source: RecordedByteAssertion,
    locality_standing: dict[str, Any],
    *,
    assignment_identity: str | None = None,
) -> bool:
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    if assignment_identity is not None:
        return (
            type(assignments) is dict
            and assignments.get(assignment_identity, object()) is None
        )
    if source.locality_movement_event_identity is not None:
        movements = locality_standing.get(
            "assertion_locality_movement_occurrences"
        )
        return (
            type(movements) is dict
            and source.locality_movement_event_identity in movements
        )
    carried = locality_standing.get("measurement_occurrences")
    return (
        type(carried) is dict
        and source.recorded_occurrence_identity in carried
    )


def _require_carried_pair_measurement_standing_at_tip(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
    required_assignment_identity: str | None = None,
    required_applicability_identity: str | None = None,
) -> str:
    boundary = locality_standing.get("through_event_occurrence_identity")
    assignments = locality_standing.get("responsibility_assignment_occurrences")
    applicability = locality_standing.get("applicability_result_occurrences")
    event = ledger.get(boundary) if type(boundary) is str else None
    if (
        locality_standing.get("locality_identity") != recording_locality_identity
        or type(boundary) is not str
        or not boundary
        or event is None
        or event.locality_identity != recording_locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary)
        != ledger.append_boundary()
        or not _pair_source_is_carried(
            source,
            locality_standing,
            assignment_identity=required_assignment_identity,
        )
        or (
            required_assignment_identity is not None
            and (
                type(assignments) is not dict
                or assignments.get(required_assignment_identity, object()) is not None
            )
        )
        or (
            required_applicability_identity is not None
            and (
                type(applicability) is not dict
                or applicability.get(required_applicability_identity, object())
                is not None
            )
        )
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement requires exact carried Standing at the append tip"
        )
    return boundary


def _append_pair_measurement_responsibility_assignment(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    scope: dict[str, Any],
    content: dict[str, Any],
    recording_locality_identity: str,
    standing_boundary_identity: str,
) -> Event:
    identities = {
        "assignment_identity": new_identity("byte_position_pair_measurement_assignment"),
        "assignment_subject_identity": new_identity(
            "byte_position_pair_measurement_assignment_subject"
        ),
        "applicability_act_identity": new_identity("byte_pair_applicability_act"),
        "applicability_act_occurrence_identity": new_identity(
            "byte_pair_applicability_occurrence"
        ),
        "applicability_result_identity": new_identity(
            "byte_pair_applicability_result"
        ),
        "measurement_act_identity": new_identity("byte_position_pair_measurement_act"),
        "measurement_act_occurrence_identity": new_identity(
            "byte_position_pair_measurement_occurrence"
        ),
        "measurement_result_identity": new_identity(
            "byte_position_pair_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ByteMeasurementError(
            "byte-position-pair Measurement lifecycle identities collapsed"
        )
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _pair_measurement_assignment_material(
            source=source,
            scope=scope,
            content=content,
            recording_locality_identity=recording_locality_identity,
            standing_boundary_identity=standing_boundary_identity,
            **identities,
        ),
        locality_identity=recording_locality_identity,
    )


def _prior_standing_for_pair_measurement_assignment(
    ledger: EventLedger,
    *,
    assignment: Event,
    boundary: str,
) -> dict[str, Any]:
    from seed_runtime.operator_locality_standing import (
        _operator_standing_validation_context,
        read_operator_locality_standing_through,
    )

    prior_standing = _operator_standing_validation_context(
        ledger, locality_identity=assignment.locality_identity
    )
    if prior_standing is not None:
        return prior_standing
    try:
        return read_operator_locality_standing_through(
            ledger,
            locality_identity=assignment.locality_identity,
            through_event_occurrence_identity=boundary,
        )
    except (TypeError, ValueError) as error:
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment has no exact prior Standing"
        ) from error


def _read_pair_measurement_responsibility_assignment(
    ledger: EventLedger,
    assignment_event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, RecordedByteAssertion, dict[str, Any], dict[str, Any]]:
    assignment = ledger.get(assignment_event_identity)
    if (
        assignment is None
        or assignment.kind
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or assignment.locality_identity is None
        or ledger.integrity_of(assignment.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment is absent or corrupted"
        )
    material = assignment.material
    identity_keys = (
        "assignment_identity",
        "assignment_subject_identity",
        "applicability_act_identity",
        "applicability_act_occurrence_identity",
        "applicability_result_identity",
        "measurement_act_identity",
        "measurement_act_occurrence_identity",
        "measurement_result_identity",
    )
    identities = {key: material.get(key) for key in identity_keys}
    reference = material.get("source_assertion_reference")
    movement_identity = material.get("source_movement_event_identity")
    boundary = material.get("standing_boundary_identity")
    if type(boundary) is not str or not boundary:
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment carries no Standing boundary"
        )
    if movement_identity is None:
        if prior_standing is None:
            prior_standing = _prior_standing_for_pair_measurement_assignment(
                ledger, assignment=assignment, boundary=boundary
            )
        readings = _assertions_of_recorded_byte_measurement(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
            prior_standing=prior_standing,
        )
        source = next(
            (
                reading
                for reading in readings or ()
                if reading.assertion_identity
                == reference.get("assertion_identity")
            ),
            None,
        ) if type(reference) is dict else None
    elif type(movement_identity) is str and movement_identity:
        source = _validate_moved_byte_assertion(ledger, movement_identity)
    else:
        source = None
    if (
        source is None
        or source.reference != reference
        or source.locality_movement_event_identity != movement_identity
        or any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment carries no exact source or lifecycle"
        )
    scope = source.material["assertion_scope"]
    content = source.material["dimensions"]["content"]
    expected = _pair_measurement_assignment_material(
        source=source,
        scope=scope,
        content=content,
        recording_locality_identity=assignment.locality_identity,
        standing_boundary_identity=boundary,
        **identities,
    )
    if material != expected:
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment coordinates are not exact"
        )
    if prior_standing is None:
        prior_standing = _prior_standing_for_pair_measurement_assignment(
            ledger, assignment=assignment, boundary=boundary
        )
    standing_boundary = prior_standing.get("through_event_occurrence_identity")
    assignments = prior_standing.get("responsibility_assignment_occurrences")
    boundary_is_exact = standing_boundary == boundary
    assignment_is_carried = bool(
        type(assignments) is dict
        and assignments.get(assignment.identity, object()) is None
    )
    if (
        prior_standing.get("locality_identity") != assignment.locality_identity
        or not _pair_source_is_carried(
            source,
            prior_standing,
            assignment_identity=(assignment.identity if assignment_is_carried else None),
        )
        or not (boundary_is_exact or assignment_is_carried)
    ):
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment has no exact prior Standing"
        )
    order = (boundary, assignment.identity)
    if assignment_is_carried and standing_boundary != assignment.identity:
        order = (*order, standing_boundary)
    try:
        ledger.occurrences_in_append_order(
            tuple(dict.fromkeys(order)),
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "byte-position-pair Measurement assignment order is false"
        ) from error
    return assignment, source, scope, content


def get_byte_position_pair_measurement_responsibility_assignment(
    ledger: EventLedger, assignment_event_identity: str
) -> Event:
    return _read_pair_measurement_responsibility_assignment(
        ledger, assignment_event_identity
    )[0]


def _pair_applicability_act_material(
    assignment: Event, source: RecordedByteAssertion
) -> dict[str, Any]:
    return {
        "applicability_act_identity": assignment.material[
            "applicability_act_identity"
        ],
        "applicability_act_occurrence_identity": assignment.material[
            "applicability_act_occurrence_identity"
        ],
        "act": "input Applicability determination",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _pair_measurement_assignment_reference(assignment)
        ),
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        "evidence_scope": (
            "Evidence for this exact input Applicability determination occurrence"
        ),
    }


def _require_exact_pair_applicability_act_event(
    ledger: EventLedger,
    event: Event,
    *,
    assignment: Event,
    source: RecordedByteAssertion,
) -> None:
    _require_exact_pair_measurement_assignment_event(ledger, assignment, source)
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND
        or event.locality_identity != assignment.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != _pair_applicability_act_material(assignment, source)
    ):
        raise ByteMeasurementError("pair Applicability Act Evidence is not exact")


def _record_pair_input_applicability_act_from_carried_assignment(
    ledger: EventLedger,
    *,
    assignment: Event,
    source: RecordedByteAssertion,
    responsibility_assignment_standing: dict[str, Any],
) -> Event:
    _require_exact_pair_measurement_assignment_event(ledger, assignment, source)
    _require_carried_pair_measurement_standing_at_tip(
        ledger,
        source=source,
        recording_locality_identity=assignment.locality_identity,
        locality_standing=responsibility_assignment_standing,
        required_assignment_identity=assignment.identity,
    )
    if responsibility_assignment_standing[
        "through_event_occurrence_identity"
    ] != assignment.identity:
        raise ByteMeasurementError(
            "pair Applicability Act requires its assignment at the append tip"
        )
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND,
        _pair_applicability_act_material(assignment, source),
        locality_identity=assignment.locality_identity,
    )


def _pair_applicability_result_material(
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_assertion: dict[str, Any],
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["applicability_result_identity"],
        "dimensions": {
            "identity": applicability_assertion["dimensions"]["identity"],
            "content": "exact source-Assertion to addressed-Act Applicability",
            "standing": applicability_assertion["dimensions"]["standing"],
            "source_provenance": applicability_assertion["dimensions"]["source_provenance"],
            "authority": BYTE_PAIR_APPLICABILITY_AUTHORITY,
        },
        "exact_act": "input Applicability determination",
        "responsibility": BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _pair_measurement_assignment_reference(assignment)
        ),
        "applicability_act_identity": applicability_assertion["applicability_act_identity"],
        "applicability_act_occurrence_identity": applicability_assertion[
            "applicability_act_occurrence_identity"
        ],
        "addressed_act_identity": applicability_assertion["addressed_act_identity"],
        "input_assertion_reference": source.reference,
        "input_movement_event_identity": source.locality_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "applicability": applicability_assertion,
    }


def _require_exact_pair_applicability_result_event(
    ledger: EventLedger,
    event: Event,
    *,
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_act_evidence: Event,
) -> dict[str, Any]:
    _require_exact_pair_applicability_act_event(
        ledger,
        applicability_act_evidence,
        assignment=assignment,
        source=source,
    )
    expected_applicability = _pair_input_applicability_from_exact_source(
        source,
        assignment=assignment,
        measurement_locality_identity=assignment.locality_identity,
    )
    expected_material = {
        **_pair_applicability_result_material(
            assignment, source, expected_applicability
        ),
        "evidence_of_yield_relation_identity": event.material.get(
            "evidence_of_yield_relation_identity"
        ),
        "responsible_act_evidence_identity": applicability_act_evidence.identity,
    }
    evidence = ledger.get(event.material.get("evidence_of_yield_relation_identity"))
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=(
                event.material.get("evidence_of_yield_relation_identity")
            ),
            responsible_act_evidence_event_identity=applicability_act_evidence.identity,
            recorded_result_occurrence_coordinate=(
                "applicability_act_occurrence_identity"
            ),
            responsible_act_occurrence_coordinate=(
                "applicability_act_occurrence_identity"
            ),
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_APPLICABILITY_RECORDED_KIND
        or event.locality_identity != assignment.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != expected_material
        or evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_PAIR_APPLICABILITY_RESULT_KIND
        or evidence.material.get("occurrence_boundary")
        != "byte_pair_applicability"
        or not all(requirements.values())
        or not _yield_immediately_precedes_result(ledger, evidence, event)
    ):
        raise ByteMeasurementError("pair Applicability result is not exact")
    return expected_applicability


def _record_pair_input_applicability_result_from_carried_act(
    ledger: EventLedger,
    *,
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_act_evidence: Event,
    applicability_assertion: dict[str, Any],
) -> Event:
    _require_exact_pair_applicability_act_event(
        ledger,
        applicability_act_evidence,
        assignment=assignment,
        source=source,
    )
    expected_applicability = _pair_input_applicability_from_exact_source(
        source,
        assignment=assignment,
        measurement_locality_identity=assignment.locality_identity,
    )
    if (
        applicability_assertion != expected_applicability
        or ledger.append_boundary_through_occurrence(
            applicability_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Applicability result requires its exact Act at the append tip"
        )
    result_material = _pair_applicability_result_material(
        assignment, source, applicability_assertion
    )
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=assignment.locality_identity,
        exact_act="input Applicability determination",
        act_occurrence_identity=assignment.material[
            "applicability_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=applicability_act_evidence.identity,
        result_kind=BYTE_PAIR_APPLICABILITY_RESULT_KIND,
        result_identity=assignment.material["applicability_result_identity"],
        result_content=result_material,
        responsibility=BYTE_PAIR_INPUT_APPLICABILITY_RESPONSIBILITY,
        occurrence_boundary="byte_pair_applicability",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        responsible_act_occurrence_coordinate="applicability_act_occurrence_identity",
    )
    if (
        ledger.get(evidence.identity) != evidence
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(evidence.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Applicability result requires its exact Yield at the append tip"
        )
    recorded_material = {
        **_pair_applicability_result_material(
            assignment, source, applicability_assertion
        ),
        "evidence_of_yield_relation_identity": evidence.identity,
        "responsible_act_evidence_identity": applicability_act_evidence.identity,
    }
    return ledger.append(
        BYTE_PAIR_APPLICABILITY_RECORDED_KIND,
        recorded_material,
        locality_identity=assignment.locality_identity,
    )


def _read_pair_applicability_act_evidence(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, Event, RecordedByteAssertion]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "pair Applicability Act Evidence is absent or corrupted"
        )
    reference = event.material.get("responsibility_assignment_reference")
    assignment, source, _scope, _content = (
        _read_pair_measurement_responsibility_assignment(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
            prior_standing=prior_standing,
        )
    )
    if (
        reference != _pair_measurement_assignment_reference(assignment)
        or event.locality_identity != assignment.locality_identity
        or event.material != _pair_applicability_act_material(assignment, source)
    ):
        raise ByteMeasurementError("pair Applicability Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "pair Applicability Act does not follow its assignment"
        ) from error
    return event, assignment, source


def _read_recorded_pair_input_applicability(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Read one historical input Applicability result without redetermining it."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
        raise ByteMeasurementError(f"{event_identity} is not pair-input Applicability")
    if ledger.integrity_of(event.identity) == CORRUPTED:
        raise ByteMeasurementError("corrupted Applicability cannot be read")
    material = event.material
    if set(material) != BYTE_PAIR_APPLICABILITY_RESULT_COORDINATES | {
        "evidence_of_yield_relation_identity",
        "responsible_act_evidence_identity",
    }:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact Applicability result surface"
        )
    assignment_reference = material.get("responsibility_assignment_reference")
    assignment, source, _scope, _content = (
        _read_pair_measurement_responsibility_assignment(
            ledger,
            assignment_reference.get("recorded_occurrence_identity")
            if type(assignment_reference) is dict
            else None,
            prior_standing=prior_standing,
        )
    )
    act_evidence = ledger.get(material.get("responsible_act_evidence_identity"))
    if (
        assignment_reference
        != _pair_measurement_assignment_reference(assignment)
        or event.locality_identity != assignment.locality_identity
        or material.get("result_identity")
        != assignment.material["applicability_result_identity"]
        or act_evidence is None
    ):
        raise ByteMeasurementError(
            f"{event_identity} carries no exact pair Measurement assignment"
        )
    applicability = _require_exact_pair_applicability_result_event(
        ledger,
        event,
        assignment=assignment,
        source=source,
        applicability_act_evidence=act_evidence,
    )
    return json.loads(_canonical(applicability))
def get_recorded_pair_input_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any] | None:
    return _read_recorded_pair_input_applicability(
        ledger, event_identity
    )


def _pair_measurement_act_material(
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_event: Event,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material[
            "measurement_act_occurrence_identity"
        ],
        "act": "declared byte-position-pair Measurement",
        "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _pair_measurement_assignment_reference(assignment)
        ),
        "result_boundary": BYTE_PAIR_RESULT_BOUNDARY,
        "input_applicability_identity": applicability_event.material["dimensions"][
            "identity"
        ],
        "input_applicability_event_identity": applicability_event.identity,
        "input_assertion_reference": source.reference,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "authority": BYTE_PAIR_MEASUREMENT_AUTHORITY,
        "evidence_scope": (
            "Evidence bounded to this exact responsible Measurement occurrence; "
            "establishes no responsibility or authority for another Act"
        ),
    }


def _require_exact_pair_measurement_act_event(
    ledger: EventLedger,
    event: Event,
    *,
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_event: Event,
    applicability_act_evidence: Event,
) -> None:
    _require_exact_pair_applicability_result_event(
        ledger,
        applicability_event,
        assignment=assignment,
        source=source,
        applicability_act_evidence=applicability_act_evidence,
    )
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND
        or event.locality_identity != assignment.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material
        != _pair_measurement_act_material(assignment, source, applicability_event)
    ):
        raise ByteMeasurementError("pair Measurement Act Evidence is not exact")


def _record_pair_measurement_act_from_carried_applicability(
    ledger: EventLedger,
    *,
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_event: Event,
    locality_standing: dict[str, Any],
) -> Event:
    applicability_act_evidence = ledger.get(
        applicability_event.material.get("responsible_act_evidence_identity")
    )
    if (
        applicability_act_evidence is None
        or applicability_act_evidence.kind
        != BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND
    ):
        raise ByteMeasurementError(
            "pair Measurement Act requires exact recorded assignment and Applicability"
        )
    _require_exact_pair_applicability_result_event(
        ledger,
        applicability_event,
        assignment=assignment,
        source=source,
        applicability_act_evidence=applicability_act_evidence,
    )
    _require_carried_pair_measurement_standing_at_tip(
        ledger,
        source=source,
        recording_locality_identity=assignment.locality_identity,
        locality_standing=locality_standing,
        required_assignment_identity=assignment.identity,
        required_applicability_identity=applicability_event.identity,
    )
    if (
        locality_standing["through_event_occurrence_identity"]
        != applicability_event.identity
        or applicability_event.material["dimensions"]["standing"] != "applicable"
    ):
        raise ByteMeasurementError(
            "pair Measurement Act requires exact applicable Standing at the append tip"
        )
    return ledger.append(
        BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND,
        _pair_measurement_act_material(assignment, source, applicability_event),
        locality_identity=assignment.locality_identity,
    )


def _read_pair_measurement_act_evidence(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[Event, Event, RecordedByteAssertion, Event]:
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "pair Measurement Act Evidence is absent or corrupted"
        )
    reference = event.material.get("responsibility_assignment_reference")
    assignment, source, _scope, _content = (
        _read_pair_measurement_responsibility_assignment(
            ledger,
            reference.get("recorded_occurrence_identity")
            if type(reference) is dict
            else None,
            prior_standing=prior_standing,
        )
    )
    applicability = ledger.get(
        event.material.get("input_applicability_event_identity")
    )
    applicability_act = (
        ledger.get(applicability.material.get("responsible_act_evidence_identity"))
        if applicability is not None
        else None
    )
    applicability_material = None
    if applicability is not None and applicability_act is not None:
        applicability_material = _require_exact_pair_applicability_result_event(
            ledger,
            applicability,
            assignment=assignment,
            source=source,
            applicability_act_evidence=applicability_act,
        )
    if (
        reference != _pair_measurement_assignment_reference(assignment)
        or applicability is None
        or applicability_material != applicability.material.get("applicability")
        or applicability.material.get("responsibility_assignment_reference")
        != reference
        or applicability.material.get("dimensions", {}).get("standing")
        != "applicable"
        or event.locality_identity != assignment.locality_identity
        or event.material
        != _pair_measurement_act_material(assignment, source, applicability)
    ):
        raise ByteMeasurementError("pair Measurement Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, applicability.identity, event.identity),
            locality_identity=assignment.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "pair Measurement Act does not follow exact Applicability"
        ) from error
    return event, assignment, source, applicability


def _pair_measurement_result_material(
    measured: MeasuredBytePairInputs,
    *,
    assignment: Event,
    applicability_event: Event,
) -> dict[str, Any]:
    return {
        "result_identity": assignment.material["measurement_result_identity"],
        "dimensions": {
            "identity": "byte-position-pair-count-measurement-occurrence",
            "content": "byte-position-pair count and recurrence Assertions",
            "source_provenance": "the recorded source-material-set Assertion",
            "authority": "unestablished",
            "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
        },
        "exact_act": "declared byte-position-pair Measurement",
        "addressed_act_identity": assignment.material["measurement_act_identity"],
        "act_occurrence_identity": assignment.material[
            "measurement_act_occurrence_identity"
        ],
        "responsibility": BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        "responsible_boundary": SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
        "responsibility_assignment_reference": (
            _pair_measurement_assignment_reference(assignment)
        ),
        "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
        "source_assertion_reference": measured.source_assertion_reference,
        "source_movement_event_identity": measured.source_movement_event_identity,
        "input_role": BYTE_PAIR_INPUT_ROLE,
        "input_applicability": measured.input_applicability,
        "input_applicability_event_identity": applicability_event.identity,
        "source_localities": list(measured.source_localities),
        "completeness_boundary": {
            "identity": measured.completeness_boundary.identity
        },
        "assertions": _pair_assertions(measured),
    }


def _record_pair_measurement_result_from_carried_act(
    ledger: EventLedger,
    *,
    responsible_act_evidence: Event,
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_event: Event,
    applicability_act_evidence: Event,
    locality_standing: dict[str, Any],
) -> Event:
    _require_exact_pair_measurement_act_event(
        ledger,
        responsible_act_evidence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act_evidence,
    )
    _require_carried_pair_measurement_standing_at_tip(
        ledger,
        source=source,
        recording_locality_identity=assignment.locality_identity,
        locality_standing=locality_standing,
        required_assignment_identity=assignment.identity,
        required_applicability_identity=applicability_event.identity,
    )
    if (
        responsible_act_evidence.kind != BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or responsible_act_evidence.material
        != _pair_measurement_act_material(
            assignment,
            source,
            applicability_event,
        )
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement result requires its exact Act at the append tip"
        )
    scope = source.material["assertion_scope"]
    content = source.material["dimensions"]["content"]
    measured = _measure_byte_position_pair_counts_through(
        ledger,
        localities=tuple(scope["source_localities"]),
        boundary=EventLedgerBoundary(content["completeness_boundary"]["identity"]),
        source_assertion_reference=source.reference,
        source_movement_event_identity=source.locality_movement_event_identity,
        input_applicability=applicability_event.material["applicability"],
        addressed_act_identity=assignment.material["measurement_act_identity"],
        act_occurrence_identity=assignment.material[
            "measurement_act_occurrence_identity"
        ],
    )
    if (
        ledger.get(responsible_act_evidence.identity) != responsible_act_evidence
        or ledger.integrity_of(responsible_act_evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(
            responsible_act_evidence.identity
        )
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement result requires its exact Act at the append tip"
        )
    result_material = _pair_measurement_result_material(
        measured,
        assignment=assignment,
        applicability_event=applicability_event,
    )
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=assignment.locality_identity,
        exact_act="declared byte-position-pair Measurement",
        act_occurrence_identity=assignment.material[
            "measurement_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind=BYTE_PAIR_MEASUREMENT_RESULT_KIND,
        result_identity=assignment.material["measurement_result_identity"],
        result_content=result_material,
        responsibility=BYTE_PAIR_MEASUREMENT_RESPONSIBILITY,
        occurrence_boundary="byte_pair_measurement",
        responsible_boundary=SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY,
    )
    if (
        ledger.get(evidence.identity) != evidence
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or ledger.append_boundary_through_occurrence(evidence.identity)
        != ledger.append_boundary()
    ):
        raise ByteMeasurementError(
            "pair Measurement result requires its exact Yield at the append tip"
        )
    recorded_material = {
        **_pair_measurement_result_material(
            measured,
            assignment=assignment,
            applicability_event=applicability_event,
        ),
        "evidence_of_yield_relation_identity": evidence.identity,
        "responsible_act_evidence_identity": responsible_act_evidence.identity,
        "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
    }
    return ledger.append(
        BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
        recorded_material,
        locality_identity=assignment.locality_identity,
    )


def _require_exact_pair_measurement_result_event(
    ledger: EventLedger,
    event: Event,
    *,
    responsible_act_evidence: Event,
    assignment: Event,
    source: RecordedByteAssertion,
    applicability_event: Event,
    applicability_act_evidence: Event,
) -> None:
    _require_exact_pair_measurement_act_event(
        ledger,
        responsible_act_evidence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act_evidence,
    )
    scope = source.material["assertion_scope"]
    content = source.material["dimensions"]["content"]
    measured = _measure_byte_position_pair_counts_through(
        ledger,
        localities=tuple(scope["source_localities"]),
        boundary=EventLedgerBoundary(content["completeness_boundary"]["identity"]),
        source_assertion_reference=source.reference,
        source_movement_event_identity=source.locality_movement_event_identity,
        input_applicability=applicability_event.material["applicability"],
        addressed_act_identity=assignment.material["measurement_act_identity"],
        act_occurrence_identity=assignment.material[
            "measurement_act_occurrence_identity"
        ],
    )
    evidence = ledger.get(event.material.get("evidence_of_yield_relation_identity"))
    expected = {
        **_pair_measurement_result_material(
            measured,
            assignment=assignment,
            applicability_event=applicability_event,
        ),
        "evidence_of_yield_relation_identity": (
            event.material.get("evidence_of_yield_relation_identity")
        ),
        "responsible_act_evidence_identity": responsible_act_evidence.identity,
        "occurrence_preservation": BYTE_PAIR_OCCURRENCE_PRESERVATION,
    }
    try:
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=(
                event.material.get("evidence_of_yield_relation_identity")
            ),
            responsible_act_evidence_event_identity=responsible_act_evidence.identity,
        )
    except (TypeError, ValueError):
        requirements = {}
    if (
        type(event) is not Event
        or ledger.get(event.identity) != event
        or event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or event.locality_identity != assignment.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
        or event.material != expected
        or evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or evidence.locality_identity != event.locality_identity
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind") != BYTE_PAIR_MEASUREMENT_RESULT_KIND
        or evidence.material.get("occurrence_boundary") != "byte_pair_measurement"
        or not all(requirements.values())
        or not _yield_immediately_precedes_result(ledger, evidence, event)
    ):
        raise ByteMeasurementError(
            "pair Measurement result or Yield is not exact"
        )


def _pair_measurement_replay_occurrence(
    ledger: EventLedger,
    event: Event,
    *,
    expected_material: dict[str, Any] | None = None,
) -> _PairMeasurementReplayOccurrence:
    material = (
        deepcopy(event.material)
        if expected_material is None
        else expected_material
    )
    recorded = ledger.get(event.identity) if type(event) is Event else None
    if (
        recorded is None
        or recorded != event
        or recorded.material != material
        or recorded.exact_material != event.exact_material
        or recorded.locality_identity != event.locality_identity
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "pair Measurement replay occurrence is absent, changed, or corrupted"
        )
    return _PairMeasurementReplayOccurrence(
        event=event,
        material=material,
        exact_material=event.exact_material,
        locality_identity=event.locality_identity,
    )


def _require_exact_pair_measurement_replay_occurrence(
    ledger: EventLedger,
    occurrence: _PairMeasurementReplayOccurrence,
) -> None:
    recorded = ledger.get(occurrence.event.identity)
    if (
        recorded is None
        or recorded != occurrence.event
        or recorded.material != occurrence.material
        or recorded.exact_material != occurrence.exact_material
        or recorded.locality_identity != occurrence.locality_identity
        or ledger.integrity_of(occurrence.event.identity) == CORRUPTED
    ):
        raise ByteMeasurementError(
            "pair Measurement replay occurrence changed after validation"
        )


def _pair_measurement_replay_reading(
    ledger: EventLedger,
    *,
    assignment: Event,
    source: RecordedByteAssertion,
) -> _PairMeasurementReplayReading:
    """Retain one exact family reading for this replay call only."""

    assignment_material = deepcopy(assignment.material)
    source_event = ledger.get(source.recorded_occurrence_identity)
    movement_event = (
        ledger.get(source.locality_movement_event_identity)
        if source.locality_movement_event_identity is not None
        else None
    )
    if source_event is None or (
        source.locality_movement_event_identity is not None
        and movement_event is None
    ):
        raise ByteMeasurementError(
            "pair Measurement replay source is absent"
        )
    reading = _PairMeasurementReplayReading(
        assignment=assignment,
        source=source,
        assignment_occurrence=_pair_measurement_replay_occurrence(
            ledger,
            assignment,
            expected_material=assignment_material,
        ),
        source_occurrence=_pair_measurement_replay_occurrence(
            ledger, source_event
        ),
        movement_occurrence=(
            _pair_measurement_replay_occurrence(ledger, movement_event)
            if movement_event is not None
            else None
        ),
    )
    _require_exact_pair_measurement_assignment_event(
        ledger, assignment, source
    )
    return reading


def _require_exact_pair_measurement_replay_reading(
    ledger: EventLedger,
    reading: _PairMeasurementReplayReading,
) -> None:
    if reading.assignment is not reading.assignment_occurrence.event:
        raise ByteMeasurementError(
            "pair Measurement replay reading was substituted"
        )
    occurrences = (
        reading.assignment_occurrence,
        reading.source_occurrence,
        reading.movement_occurrence,
        reading.applicability_act_occurrence,
        reading.applicability_result_occurrence,
        reading.measurement_act_occurrence,
    )
    for occurrence in occurrences:
        if occurrence is not None:
            _require_exact_pair_measurement_replay_occurrence(
                ledger, occurrence
            )
    _require_exact_pair_measurement_assignment_event(
        ledger, reading.assignment, reading.source
    )


def _advance_pair_measurement_replay_reading(
    ledger: EventLedger,
    reading: _PairMeasurementReplayReading,
    event: Event,
) -> _PairMeasurementReplayReading:
    """Validate one later phase from one exact same-call family reading."""

    event_material = deepcopy(event.material)
    _require_exact_pair_measurement_replay_reading(ledger, reading)
    event_occurrence = _pair_measurement_replay_occurrence(
        ledger,
        event,
        expected_material=event_material,
    )
    if event.locality_identity != reading.assignment.locality_identity:
        raise ByteMeasurementError(
            "pair Measurement replay phase entered another Locality"
        )
    if event.kind == BYTE_PAIR_APPLICABILITY_ACT_EVIDENCE_KIND:
        if reading.applicability_act_occurrence is not None:
            raise ByteMeasurementError(
                "pair Measurement replay duplicated Applicability Act"
            )
        _require_exact_pair_applicability_act_event(
            ledger,
            event,
            assignment=reading.assignment,
            source=reading.source,
        )
        reading.applicability_act_occurrence = event_occurrence
    elif event.kind == BYTE_PAIR_APPLICABILITY_RECORDED_KIND:
        act = reading.applicability_act_occurrence
        if act is None or reading.applicability_result_occurrence is not None:
            raise ByteMeasurementError(
                "pair Measurement replay has no exact Applicability Act"
            )
        _require_exact_pair_applicability_result_event(
            ledger,
            event,
            assignment=reading.assignment,
            source=reading.source,
            applicability_act_evidence=act.event,
        )
        reading.applicability_result_occurrence = event_occurrence
    elif event.kind == BYTE_PAIR_RESPONSIBLE_ACT_EVIDENCE_KIND:
        act = reading.applicability_act_occurrence
        applicability = reading.applicability_result_occurrence
        if (
            act is None
            or applicability is None
            or reading.measurement_act_occurrence is not None
        ):
            raise ByteMeasurementError(
                "pair Measurement replay has no exact Applicability result"
            )
        _require_exact_pair_measurement_act_event(
            ledger,
            event,
            assignment=reading.assignment,
            source=reading.source,
            applicability_event=applicability.event,
            applicability_act_evidence=act.event,
        )
        reading.measurement_act_occurrence = event_occurrence
    elif event.kind == BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        act = reading.applicability_act_occurrence
        applicability = reading.applicability_result_occurrence
        measurement_act = reading.measurement_act_occurrence
        if act is None or applicability is None or measurement_act is None:
            raise ByteMeasurementError(
                "pair Measurement replay has no exact Measurement Act"
            )
        _require_exact_pair_measurement_result_event(
            ledger,
            event,
            responsible_act_evidence=measurement_act.event,
            assignment=reading.assignment,
            source=reading.source,
            applicability_event=applicability.event,
            applicability_act_evidence=act.event,
        )
    else:
        raise ByteMeasurementError("pair Measurement replay phase is not exact")
    ordered = tuple(
        occurrence.event.identity
        for occurrence in (
            reading.assignment_occurrence,
            reading.applicability_act_occurrence,
            reading.applicability_result_occurrence,
            reading.measurement_act_occurrence,
        )
        if occurrence is not None
    )
    if event.identity not in ordered:
        ordered = (*ordered, event.identity)
    try:
        resolved = ledger.occurrences_in_append_order(
            ordered,
            locality_identity=reading.assignment.locality_identity,
        )
    except ValueError as error:
        raise ByteMeasurementError(
            "pair Measurement replay phase order is false"
        ) from error
    if tuple(occurrence.identity for occurrence in resolved) != ordered:
        raise ByteMeasurementError(
            "pair Measurement replay phase order is false"
        )
    return reading


def _record_byte_position_pair_count_layer_from_carried_standing(
    ledger: EventLedger,
    *,
    source: RecordedByteAssertion,
    scope: dict[str, Any],
    content: dict[str, Any],
    recording_locality_identity: str,
    standing: dict[str, Any],
) -> tuple[Event, dict[str, Any]]:
    from seed_runtime.operator_locality_standing import (
        _carry_pair_applicability_act_into_standing,
        _carry_pair_applicability_result_into_standing,
        _carry_pair_measurement_act_into_standing,
        _carry_pair_measurement_assignment_into_standing,
        _carry_pair_measurement_result_into_standing,
    )

    boundary = _require_carried_pair_measurement_standing_at_tip(
        ledger,
        source=source,
        recording_locality_identity=recording_locality_identity,
        locality_standing=standing,
    )
    assignment = _append_pair_measurement_responsibility_assignment(
        ledger,
        source=source,
        scope=scope,
        content=content,
        recording_locality_identity=recording_locality_identity,
        standing_boundary_identity=boundary,
    )
    standing = _carry_pair_measurement_assignment_into_standing(
        ledger,
        standing,
        assignment,
        source,
        prior_through_event_occurrence_identity=boundary,
    )
    applicability = _pair_input_applicability(
        ledger,
        source,
        assignment=assignment,
        measurement_locality_identity=recording_locality_identity,
    )
    applicability_act = (
        _record_pair_input_applicability_act_from_carried_assignment(
            ledger,
            assignment=assignment,
            source=source,
            responsibility_assignment_standing=standing,
        )
    )
    standing = _carry_pair_applicability_act_into_standing(
        ledger,
        standing,
        applicability_act,
        assignment=assignment,
        source=source,
        prior_through_event_occurrence_identity=assignment.identity,
    )
    applicability_event = _record_pair_input_applicability_result_from_carried_act(
        ledger,
        assignment=assignment,
        source=source,
        applicability_act_evidence=applicability_act,
        applicability_assertion=applicability,
    )
    standing = _carry_pair_applicability_result_into_standing(
        ledger,
        standing,
        applicability_event,
        assignment=assignment,
        source=source,
        applicability_act_evidence=applicability_act,
        prior_through_event_occurrence_identity=applicability_act.identity,
    )
    if applicability["dimensions"]["standing"] != "applicable":
        return applicability_event, standing
    responsible_act_evidence = (
        _record_pair_measurement_act_from_carried_applicability(
            ledger,
            assignment=assignment,
            source=source,
            applicability_event=applicability_event,
            locality_standing=standing,
        )
    )
    standing = _carry_pair_measurement_act_into_standing(
        ledger,
        standing,
        responsible_act_evidence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act,
        prior_through_event_occurrence_identity=applicability_event.identity,
    )
    result = _record_pair_measurement_result_from_carried_act(
        ledger,
        responsible_act_evidence=responsible_act_evidence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act,
        locality_standing=standing,
    )
    standing = _carry_pair_measurement_result_into_standing(
        ledger,
        standing,
        result,
        responsible_act_evidence=responsible_act_evidence,
        assignment=assignment,
        source=source,
        applicability_event=applicability_event,
        applicability_act_evidence=applicability_act,
        prior_through_event_occurrence_identity=responsible_act_evidence.identity,
    )
    return result, standing


def _record_byte_position_pair_count_layer_from_carried_locality_standing(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    recording_locality_identity: str,
    locality_standing: dict[str, Any],
) -> tuple[Event, dict[str, Any]]:
    source, scope, content = _prepare_pair_source(
        ledger,
        source_measurement_event_identity=source_measurement_event_identity,
        measurement_locality_identity=recording_locality_identity,
    )
    _require_carried_pair_measurement_standing_at_tip(
        ledger,
        source=source,
        recording_locality_identity=recording_locality_identity,
        locality_standing=locality_standing,
    )
    return _record_byte_position_pair_count_layer_from_carried_standing(
        ledger,
        source=source,
        scope=scope,
        content=content,
        recording_locality_identity=recording_locality_identity,
        standing=locality_standing,
    )


def record_byte_position_pair_count_layer(
    ledger: EventLedger,
    *,
    source_measurement_event_identity: str,
    recording_locality_identity: str,
):
    """Record exact byte-position-pair counts without crossing append boundaries."""

    if not isinstance(recording_locality_identity, str) or not recording_locality_identity:
        raise ByteMeasurementError(
            "byte-position-pair Measurement recording requires an exact Locality"
        )
    source, scope, content = _prepare_pair_source(
        ledger,
        source_measurement_event_identity=source_measurement_event_identity,
        measurement_locality_identity=recording_locality_identity,
    )
    from seed_runtime.operator_locality_standing import read_operator_locality_standing

    standing = read_operator_locality_standing(
        ledger, locality_identity=recording_locality_identity
    )
    result, _standing = _record_byte_position_pair_count_layer_from_carried_standing(
        ledger,
        source=source,
        scope=scope,
        content=content,
        recording_locality_identity=recording_locality_identity,
        standing=standing,
    )
    return result


def _validated_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    findings_only: bool,
    prior_standing: dict[str, Any] | None = None,
) -> _RecordedBytePairMeasurementReading | None:
    """Validate one exact pair result and return its requested reading surface."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND:
        raise ByteMeasurementError(
            f"{event_identity} is not a byte-position-pair Measurement occurrence"
        )
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise ByteMeasurementError("a corrupted occurrence cannot return pair results")
    material = event.material
    exact_surface = BYTE_PAIR_RESULT_COORDINATES | {
        "evidence_of_yield_relation_identity",
        "responsible_act_evidence_identity",
        "occurrence_preservation",
    }
    if set(material) != exact_surface:
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact pair result and recording surfaces"
        )
    assignment_reference = material.get("responsibility_assignment_reference")
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    act_evidence, assignment, source, applicability_event = (
        _read_pair_measurement_act_evidence(
            ledger,
            act_evidence_identity,
            prior_standing=prior_standing,
        )
    )
    if (
        assignment_reference
        != _pair_measurement_assignment_reference(assignment)
        or event.locality_identity != assignment.locality_identity
        or material.get("result_identity")
        != assignment.material["measurement_result_identity"]
        or material.get("source_assertion_reference") != source.reference
        or material.get("source_movement_event_identity")
        != source.locality_movement_event_identity
        or material.get("input_applicability_event_identity")
        != applicability_event.identity
    ):
        raise ByteMeasurementError(
            f"{event_identity} carries no exact pair Measurement assignment"
        )
    expected_dimensions = {
        "identity": "byte-position-pair-count-measurement-occurrence",
        "content": (
            "byte-position-pair count and recurrence Assertions"
        ),
        "source_provenance": "the recorded source-material-set Assertion",
        "authority": "unestablished",
        "evidence_scope": PAIR_MEASUREMENT_EVIDENCE_SCOPE,
    }
    if (
        material.get("occurrence_preservation") != BYTE_PAIR_OCCURRENCE_PRESERVATION
        or material.get("exact_act") != "declared byte-position-pair Measurement"
        or material.get("responsibility") != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or not isinstance(material.get("addressed_act_identity"), str)
        or not material["addressed_act_identity"]
        or not isinstance(material.get("act_occurrence_identity"), str)
        or not material["act_occurrence_identity"]
        or material["addressed_act_identity"] == material["act_occurrence_identity"]
        or material.get("dimensions") != expected_dimensions
        or material.get("measurement_rule") != BYTE_PAIR_MEASUREMENT_RULE
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not preserve its exact pair Measurement Assertion"
        )
    evidence_identity = material.get("evidence_of_yield_relation_identity")
    evidence = ledger.get(evidence_identity) if isinstance(evidence_identity, str) else None
    if (
        evidence is None
        or evidence.kind != RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
        or ledger.integrity_of(evidence.identity) == CORRUPTED
        or evidence.material.get("result_kind")
        != BYTE_PAIR_MEASUREMENT_RESULT_KIND
        or evidence.material.get("occurrence_boundary") != "byte_pair_measurement"
        or evidence.material.get("coordinates_of_carried_result")
        != [
            coordinate
            for coordinate in material
            if coordinate in BYTE_PAIR_RESULT_COORDINATES
        ]
        or evidence.material.get("dimensions", {}).get("responsibility")
        != BYTE_PAIR_MEASUREMENT_RESPONSIBILITY
        or evidence.material.get("dimensions", {}).get("responsible_boundary")
        != SEED_NATIVE_MEASUREMENT_RESPONSIBLE_BOUNDARY
        or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != material["act_occurrence_identity"]
        or not _yield_immediately_precedes_result(ledger, evidence, event)
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact byte-position-pair yield Evidence"
        )
    carried_applicability = material.get("input_applicability")
    applicability_dimensions = (
        carried_applicability.get("dimensions")
        if isinstance(carried_applicability, dict)
        else None
    )
    applicability_identity = (
        applicability_dimensions.get("identity")
        if isinstance(applicability_dimensions, dict)
        else None
    )
    if not isinstance(applicability_identity, str) or not applicability_identity:
        raise ByteMeasurementError(f"{event_identity} carries no exact input Applicability")
    if (
        act_evidence.material
        != _pair_measurement_act_material(assignment, source, applicability_event)
    ):
        raise ByteMeasurementError(
            f"{event_identity} names no exact responsible pair Measurement occurrence Evidence"
        )
    _require_exact_result_yield(
        ledger,
        event,
        evidence,
        act_evidence,
        result_name="byte-position-pair",
    )
    boundary_value = material.get("completeness_boundary")
    localities_value = material.get("source_localities")
    if (
        not isinstance(boundary_value, dict)
        or set(boundary_value) != {"identity"}
        or not isinstance(boundary_value["identity"], str)
        or not isinstance(localities_value, list)
        or not localities_value
        or any(not isinstance(item, str) or not item for item in localities_value)
        or len(set(localities_value)) != len(localities_value)
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry the exact pair Measurement boundary"
        )
    source_reference = material.get("source_assertion_reference")
    if (
        not isinstance(source_reference, dict)
        or set(source_reference) != {"recorded_occurrence_identity", "assertion_identity"}
        or not all(isinstance(value, str) and value for value in source_reference.values())
    ):
        raise ByteMeasurementError(f"{event_identity} carries no exact source Assertion")
    if source.reference != source_reference or event.locality_identity is None:
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source Assertion"
        )
    source_material = source.material
    source_scope = source_material["assertion_scope"]
    source_content = source_material["dimensions"]["content"]
    if (
        localities_value != source_scope["source_localities"]
        or boundary_value != source_content["completeness_boundary"]
        or assignment.material.get("source_localities") != localities_value
        or assignment.material.get("completeness_boundary_identity")
        != boundary_value["identity"]
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not carry its exact input source boundary"
        )
    applicability_event_identity = material.get("input_applicability_event_identity")
    if (
        applicability_event_identity != applicability_event.identity
        or applicability_event.material.get("applicability")
        != material.get("input_applicability")
    ):
        raise ByteMeasurementError(
            f"{event_identity} does not name its exact recorded input Applicability"
        )
    expected_scope = {
        "source_localities": localities_value,
    }
    assertions = material.get("assertions")
    if not isinstance(assertions, list):
        raise ByteMeasurementError(f"{event_identity} carries no pair result Assertions")
    by_pair: dict[tuple[int, int], dict[str, dict[str, Any]]] = {}
    exact_keys = {
        "dimensions",
        "subject_kind",
        "responsible_boundary",
        "result",
        "assertion_subject",
        "assertion_scope",
        "input_support",
        "conflicts",
        "unknown",
        "limits",
    }
    canonical_scope = _canonical(expected_scope)
    for assertion in assertions:
        if not isinstance(assertion, dict) or set(assertion) != exact_keys:
            raise ByteMeasurementError(f"{event_identity} carries a malformed pair Assertion")
        subject = assertion.get("assertion_subject")
        result = assertion.get("result")
        dimensions = assertion.get("dimensions")
        representation = (
            subject.get("representation") if isinstance(subject, dict) else None
        )
        if (
            type(representation) is not list
            or len(representation) != 2
            or any(
                type(value) is not int or not 0 <= value <= 255
                for value in representation
            )
            or subject
            != {
                "representation": representation,
                "measurement_rule": BYTE_PAIR_MEASUREMENT_RULE,
            }
            or result not in {"count", "recurrence"}
            or assertion.get("assertion_scope") != expected_scope
            or assertion.get("subject_kind") != "assertion"
            or assertion.get("responsible_boundary") != "this recorded assertion"
            or assertion.get("conflicts") != "Unknown"
            or not isinstance(dimensions, dict)
            or set(dimensions)
                != {
                    "identity",
                    "content",
                    "source_provenance",
                    "responsibility",
                    "authority",
                    "evidence_scope",
                }
            or dimensions.get("responsibility") != MEASURED_ASSERTION_RESPONSIBILITY
            or dimensions.get("authority") != "unestablished"
            or dimensions.get("evidence_scope") != PAIR_MEASUREMENT_EVIDENCE_SCOPE
            or assertion.get("unknown") != list(BYTE_PAIR_UNKNOWN)
            or assertion.get("limits")
            != list(BYTE_PAIR_LIMITS)
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair Assertion")
        content = dimensions.get("content")
        fixed_content_shape = (
            result == "recurrence"
            and content == {"recurrence_established": True}
        ) or (
            result == "count"
            and type(content) is dict
            and set(content) == {"input_count", "occurrences_carrying", "count"}
            and all(type(value) is int for value in content.values())
        )
        expected_identity = (
            _pair_assertion_identity(
                result=result,
                representation=tuple(representation),
                canonical_scope=canonical_scope,
                content=content,
            )
            if fixed_content_shape
            else _identity(
                result=result,
                subject=subject,
                scope=expected_scope,
                content=content,
            )
        )
        if dimensions.get("identity") != expected_identity:
            raise ByteMeasurementError(f"{event_identity} carries a false pair Assertion identity")
        group = by_pair.setdefault(tuple(representation), {})
        if result in group:
            raise ByteMeasurementError(f"{event_identity} duplicates one pair result")
        group[result] = assertion
    for group in by_pair.values():
        count = group.get("count")
        if count is None:
            raise ByteMeasurementError(f"{event_identity} carries recurrence without count")
        count_content = count["dimensions"]["content"]
        if (
            not isinstance(count_content, dict)
            or set(count_content)
            != {"input_count", "occurrences_carrying", "count"}
            or any(type(value) is not int or value <= 0 for value in count_content.values())
            or count_content["occurrences_carrying"] > count_content["input_count"]
            or count_content["occurrences_carrying"] > count_content["count"]
            or count["input_support"]
            != {"assertion_references": [source_reference], "local_assertion_references": []}
            or count["dimensions"]["source_provenance"]
            != "the exact source-material-set Assertion referenced here"
        ):
            raise ByteMeasurementError(f"{event_identity} carries an unlawful pair count")
        recurrence = group.get("recurrence")
        if (recurrence is not None) != (count_content["count"] > 1):
            raise ByteMeasurementError(f"{event_identity} carries the wrong recurrence boundary")
        if recurrence is not None and (
            recurrence["dimensions"]["content"] != {"recurrence_established": True}
            or recurrence["dimensions"]["source_provenance"]
            != "the exact count Assertion carried here"
            or recurrence["input_support"]
            != {
                "assertion_references": [],
                "local_assertion_references": [count["dimensions"]["identity"]],
            }
        ):
            raise ByteMeasurementError(f"{event_identity} carries unlawful recurrence support")
    validated_results = []
    for assertion in assertions:
        if findings_only:
            content = assertion["dimensions"]["content"]
            content_coordinates: tuple[int, int, int] | bool
            if assertion["result"] == "recurrence":
                content_coordinates = content["recurrence_established"]
            else:
                content_coordinates = (
                    content["input_count"],
                    content["occurrences_carrying"],
                    content["count"],
                )
            validated_results.append(
                _RecordedBytePairFinding(
                    assertion_identity=assertion["dimensions"]["identity"],
                    recorded_occurrence_identity=event.identity,
                    representation=tuple(
                        assertion["assertion_subject"]["representation"]
                    ),
                    result=assertion["result"],
                    _content_coordinates=content_coordinates,
                    _local_support_assertion_identities=tuple(
                        assertion["input_support"][
                            "local_assertion_references"
                        ]
                    ),
                )
            )
            continue
        support = assertion["input_support"]
        support_references = list(support["assertion_references"])
        support_references.extend(
            {
                "recorded_occurrence_identity": event.identity,
                "assertion_identity": local_identity,
            }
            for local_identity in support["local_assertion_references"]
        )
        validated_results.append(RecordedBytePairAssertion(
            assertion_identity=assertion["dimensions"]["identity"],
            recorded_occurrence_identity=event.identity,
            representation=tuple(assertion["assertion_subject"]["representation"]),
            result=assertion["result"],
            _material_json=_canonical(assertion),
            _support_assertion_refs_json=_canonical(support_references),
        ))
    return _RecordedBytePairMeasurementReading(
        results=tuple(validated_results),
        assignment=assignment,
        source=source,
    )


def _read_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    findings_only: bool,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[RecordedBytePairAssertion, ...] | tuple[_RecordedBytePairFinding, ...] | None:
    reading = _validated_recorded_byte_position_pair_measurement(
        ledger,
        event_identity,
        findings_only=findings_only,
        prior_standing=prior_standing,
    )
    return reading.results if reading is not None else None


def assertions_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> tuple[RecordedBytePairAssertion, ...] | None:
    """Read the exact pair result without performing Measurement again."""

    reading = _read_recorded_byte_position_pair_measurement(
        ledger, event_identity, findings_only=False
    )
    return reading


def _findings_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger,
    event_identity: str,
    *,
    prior_standing: dict[str, Any] | None = None,
) -> tuple[_RecordedBytePairFinding, ...] | None:
    """Read only exact finding coordinates after the same full validation."""

    reading = _read_recorded_byte_position_pair_measurement(
        ledger,
        event_identity,
        findings_only=True,
        prior_standing=prior_standing,
    )
    return reading


def byte_position_pair_measurement_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, ...]:
    """Return the exact ordered Applicability and Measurement occurrences."""

    assertions = assertions_of_recorded_byte_position_pair_measurement(
        ledger, event_identity
    )
    if type(assertions) is not tuple:
        raise ByteMeasurementError("pair Measurement result is absent")
    result = ledger.get(event_identity)
    assert result is not None
    applicability_identity = result.material["input_applicability_event_identity"]
    applicability = ledger.get(applicability_identity)
    if applicability is None:
        raise ByteMeasurementError(
            "pair Measurement carries no exact Applicability result"
        )
    get_recorded_pair_input_applicability(ledger, applicability.identity)
    references = (
        applicability.material["responsible_act_evidence_identity"],
        applicability.material["evidence_of_yield_relation_identity"],
        applicability.identity,
        result.material["responsible_act_evidence_identity"],
        result.material["evidence_of_yield_relation_identity"],
        result.identity,
    )
    ordered = ledger.occurrences_in_append_order(
        references, locality_identity=result.locality_identity
    )
    if tuple(event.identity for event in ordered) != references:
        raise ByteMeasurementError(
            "pair Applicability and Measurement occurrences are not ordered"
        )
    return references


def input_applicability_of_recorded_byte_position_pair_measurement(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any] | None:
    """Validate the exact input-to-Act Applicability Assertion."""

    read = assertions_of_recorded_byte_position_pair_measurement(ledger, event_identity)
    if read is None:
        return None
    event = ledger.get(event_identity)
    return json.loads(_canonical(event.material["input_applicability"]))
