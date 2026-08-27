from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger, EventLedgerBoundary
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)

OCCURRENCE_POSITION_RECORDED_KIND = (
    "operator.measurement.locality_occurrence_position_recorded"
)
OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.measurement.locality_occurrence_position_subject_to_act_binding_recorded"
)
OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT = (
    "operator.measurement.locality_occurrence_position_act_occurrence_recorded"
)
OCCURRENCE_POSITION_RESULT_KIND = "occurrence position Measurement result"
OCCURRENCE_POSITION_ACT = "occurrence position Measurement"
OCCURRENCE_POSITION_RESULT_COORDINATES = frozenset(
    {
        "result_identity",
        "addressed_act_identity",
        "act_occurrence_identity",
        "exact_act",
        "subject_to_act_binding_reference",
        "source_localities",
        "completeness_boundary",
        "assertions",
    }
)
EVENT_KIND_BOOK_CLAUSES = {
    OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: "01.Source.D",
    OCCURRENCE_POSITION_RECORDED_KIND: "01.Source.D",
    OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
}


@dataclass(frozen=True)
class OccurrencePositionFinding:
    """Exact occurrence positions within one Locality and append boundary."""

    source_locality_identity: str
    completeness_boundary: EventLedgerBoundary
    occurrences: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source_locality_identity, str) or not (
            self.source_locality_identity
        ):
            raise ValueError(
                "one exact source Locality is required"
            )
        if not isinstance(self.completeness_boundary, EventLedgerBoundary):
            raise ValueError(
                "one exact append boundary is required"
            )
        identities = []
        for expected_position, occurrence in enumerate(self.occurrences):
            if (
                type(occurrence) is not tuple
                or len(occurrence) != 2
                or not isinstance(occurrence[0], str)
                or not occurrence[0]
                or type(occurrence[1]) is not int
                or occurrence[1] != expected_position
            ):
                raise ValueError(
                    "each exact occurrence requires its measured position"
                )
            identities.append(occurrence[0])
        if len(set(identities)) != len(identities):
            raise ValueError(
                "one occurrence cannot occupy more than one measured position"
            )

def measure_occurrence_position(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    through: EventLedgerBoundary | None = None,
) -> OccurrencePositionFinding:
    """Measure every occurrence position in one Locality through one boundary."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("occurrence position Measurement requires one EventLedger")
    if not isinstance(source_locality_identity, str) or not source_locality_identity:
        raise ValueError(
            "one exact source Locality is required"
        )
    boundary = through or ledger.append_boundary()
    return _measure_occurrence_position_through(
        ledger,
        source_locality_identity=source_locality_identity,
        boundary=boundary,
    )


def _measure_occurrence_position_through(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    boundary: EventLedgerBoundary,
) -> OccurrencePositionFinding:
    occurrences = ledger.list_locality(
        source_locality_identity,
        through=boundary,
    )
    if any(ledger.integrity_of(event.identity) == CORRUPTED for event in occurrences):
        raise ValueError(
            "occurrence position Measurement requires intact occurrences"
        )
    return OccurrencePositionFinding(
        source_locality_identity=source_locality_identity,
        completeness_boundary=boundary,
        occurrences=tuple(
            (event.identity, position)
            for position, event in enumerate(occurrences)
        ),
    )


def _occurrence_position_result_material(
    finding: OccurrencePositionFinding,
    *,
    binding: Event,
    assertions: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "result_identity": binding.material["measurement_result_identity"],
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "exact_act": OCCURRENCE_POSITION_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "source_localities": [finding.source_locality_identity],
        "completeness_boundary": {
            "identity": finding.completeness_boundary.identity,
        },
        "assertions": assertions,
    }


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": binding.material["subject_reference"],
        "result_boundary_identity": binding.material[
            "result_boundary_identity"
        ],
    }


def _binding_material(
    finding: OccurrencePositionFinding,
    *,
    through_event_occurrence_identity: str | None,
    exact_act_identity: str,
    act_occurrence_identity: str,
    measurement_result_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": {
            "source_occurrence_references": [
                {"occurrence_identity": identity}
                for identity, _position in finding.occurrences
            ],
        },
        "exact_act_identity": exact_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "measurement_result_identity": measurement_result_identity,
        "result_boundary_identity": measurement_result_identity,
        "book_clause_identity": "01.Source.D",
        "source_locality_identity": finding.source_locality_identity,
        "completeness_boundary_identity": finding.completeness_boundary.identity,
        "through_event_occurrence_identity": through_event_occurrence_identity,
    }


def _position_assertions(
    finding: OccurrencePositionFinding,
) -> list[dict[str, Any]]:
    assertions = []
    for occurrence_identity, position in finding.occurrences:
        boundary = {"identity": finding.completeness_boundary.identity}
        subject = {"occurrence_identity": occurrence_identity}
        content = {
            "position": position,
            "completeness_boundary": boundary,
        }
        assertions.append(
            {
                "dimensions": {
                    "identity": occurrence_identity,
                    "content": content,
                },
                "result": "position",
                "assertion_subject": subject,
            }
        )
    return assertions


def _exact_occurrence_position_finding(
    ledger: EventLedger,
    finding: OccurrencePositionFinding,
) -> None:
    if not isinstance(ledger, EventLedger):
        raise TypeError("occurrence position Measurement requires one EventLedger")
    if type(finding) is not OccurrencePositionFinding:
        raise TypeError(
            "occurrence position recording requires one exact finding"
        )
    source_occurrences = ledger.list_locality(
        finding.source_locality_identity,
        through=finding.completeness_boundary,
    )
    if len(source_occurrences) != len(finding.occurrences):
        raise ValueError(
            "the supplied occurrence position finding differs from the exact boundary"
        )
    for position, occurrence in enumerate(source_occurrences):
        if ledger.integrity_of(occurrence.identity) == CORRUPTED:
            raise ValueError(
                "occurrence position Measurement requires intact occurrences"
            )
        if finding.occurrences[position] != (occurrence.identity, position):
            raise ValueError(
                "the supplied occurrence position finding differs from the exact boundary"
            )


def _occurrence_position_act_occurrence_material(
    finding: OccurrencePositionFinding,
    *,
    binding: Event,
) -> dict[str, Any]:
    return {
        "addressed_act_identity": binding.material["exact_act_identity"],
        "act_occurrence_identity": binding.material["act_occurrence_identity"],
        "act": OCCURRENCE_POSITION_ACT,
        "subject_to_act_binding_reference": _binding_reference(binding),
        "source_locality_identity": finding.source_locality_identity,
    }


def _require_current_coordinates(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
    required_binding_identity: str | None = None,
) -> str | None:
    if type(current_coordinates) is not dict:
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    # Imported here because the current-coordinate reader imports this module's event
    # contract. Recording is runtime work after both modules are initialized.
    from seed_runtime.operator_current_coordinates import (
        read_operator_current_coordinates,
    )

    current = read_operator_current_coordinates(
        ledger, locality_identity=locality_identity
    )
    carried = current_coordinates.get("subject_to_act_binding_occurrences")
    if (
        current_coordinates != current
        or current_coordinates.get("locality_identity") != locality_identity
        or (
            required_binding_identity is not None
            and (
                type(carried) is not dict
                or carried.get(required_binding_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    if boundary is not None and (type(boundary) is not str or not boundary):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    return boundary


def _require_carried_current_coordinates_at_append_boundary(
    ledger: EventLedger,
    *,
    locality_identity: str,
    current_coordinates: dict[str, Any],
    required_binding_identity: str | None = None,
) -> str | None:
    """Read same-call coordinates at the current append boundary."""

    if type(current_coordinates) is not dict:
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    boundary = current_coordinates.get("through_event_occurrence_identity")
    carried = current_coordinates.get("subject_to_act_binding_occurrences")
    if (
        current_coordinates.get("locality_identity") != locality_identity
        or boundary is None
        or type(boundary) is not str
        or not boundary
        or (
            required_binding_identity is not None
            and (
                type(carried) is not dict
                or carried.get(required_binding_identity, object()) is not None
            )
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    event = ledger.get(boundary)
    if (
        event is None
        or event.locality_identity != locality_identity
        or ledger.integrity_of(boundary) == CORRUPTED
        or ledger.append_boundary_through_occurrence(boundary)
        != ledger.append_boundary()
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    return boundary


def _record_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    current_coordinates: dict[str, Any],
    carried: bool,
) -> Event:
    if type(recording_locality_identity) is not str or not recording_locality_identity:
        raise ValueError("occurrence position recording requires one exact Locality")
    if carried:
        if (
            type(finding) is not OccurrencePositionFinding
            or finding.source_locality_identity != recording_locality_identity
            or finding.completeness_boundary != ledger.append_boundary()
        ):
            raise ValueError(
                "occurrence position Measurement requires exact current coordinates"
            )
    else:
        _exact_occurrence_position_finding(ledger, finding)
    require_coordinates = (
        _require_carried_current_coordinates_at_append_boundary
        if carried
        else _require_current_coordinates
    )
    through_event_occurrence_identity = require_coordinates(
        ledger,
        locality_identity=recording_locality_identity,
        current_coordinates=current_coordinates,
    )
    if (
        carried
        and (
            not finding.occurrences
            or finding.occurrences[-1][0] != through_event_occurrence_identity
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires exact current coordinates"
        )
    identities = {
        "exact_act_identity": ledger.mint_identity(
            "occurrence_position_measurement_act"
        ),
        "act_occurrence_identity": ledger.mint_identity(
            "occurrence_position_measurement_occurrence"
        ),
        "measurement_result_identity": ledger.mint_identity(
            "occurrence_position_measurement_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise ValueError("occurrence position Measurement identities collapsed")
    return ledger.append(
        OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identities,
        ),
        locality_identity=recording_locality_identity,
    )


def record_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record one exact Book-backed subject-to-Act binding occurrence."""

    return _record_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        recording_locality_identity=recording_locality_identity,
        finding=finding,
        current_coordinates=current_coordinates,
        carried=False,
    )


def _record_occurrence_position_measurement_subject_to_act_binding_from_current_coordinates(
    ledger: EventLedger,
    *,
    recording_locality_identity: str,
    finding: OccurrencePositionFinding,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record a finding produced from exact same-call coordinates."""

    return _record_occurrence_position_measurement_subject_to_act_binding(
        ledger,
        recording_locality_identity=recording_locality_identity,
        finding=finding,
        current_coordinates=current_coordinates,
        carried=True,
    )


def _read_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
) -> tuple[Event, OccurrencePositionFinding]:
    if type(binding_event_identity) is not str or not binding_event_identity:
        raise ValueError(
            "occurrence position Measurement requires one binding occurrence"
        )
    binding = ledger.get(binding_event_identity)
    if (
        binding is None
        or binding.kind
        != OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or type(binding.locality_identity) is not str
        or not binding.locality_identity
        or binding.exact_material is not None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position Measurement binding is absent or corrupted"
        )
    material = binding.material
    identities = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "exact_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    source_locality_identity = material.get("source_locality_identity")
    completeness_boundary_identity = material.get(
        "completeness_boundary_identity"
    )
    through_event_occurrence_identity = material.get(
        "through_event_occurrence_identity"
    )
    if (
        any(type(value) is not str or not value for value in identities.values())
        or len(set(identities.values())) != len(identities)
        or type(source_locality_identity) is not str
        or not source_locality_identity
        or type(completeness_boundary_identity) is not str
        or not completeness_boundary_identity
        or (
            through_event_occurrence_identity is not None
            and (
                type(through_event_occurrence_identity) is not str
                or not through_event_occurrence_identity
            )
        )
    ):
        raise ValueError(
            "occurrence position Measurement binding coordinates are not exact"
        )
    try:
        finding = _measure_occurrence_position_through(
            ledger,
            source_locality_identity=source_locality_identity,
            boundary=EventLedgerBoundary(completeness_boundary_identity),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "occurrence position Measurement binding coordinates are not exact"
        ) from error
    if material != _binding_material(
        finding,
        through_event_occurrence_identity=through_event_occurrence_identity,
        **identities,
    ):
        raise ValueError(
            "occurrence position Measurement binding coordinates are not exact"
        )
    if through_event_occurrence_identity is not None:
        boundary = ledger.get(through_event_occurrence_identity)
        if (
            boundary is None
            or boundary.locality_identity != binding.locality_identity
            or ledger.integrity_of(boundary.identity) == CORRUPTED
        ):
            raise ValueError(
                "occurrence position Measurement binding has no exact through-occurrence boundary"
            )
        try:
            ledger.occurrences_in_append_order(
                (through_event_occurrence_identity, binding.identity),
                locality_identity=binding.locality_identity,
            )
        except ValueError as error:
            raise ValueError(
                "occurrence position Measurement binding has false occurrence order"
            ) from error
    return binding, finding


def get_occurrence_position_measurement_subject_to_act_binding(
    ledger: EventLedger,
    binding_event_identity: str,
) -> Event:
    """Read one exact occurrence-position subject-to-Act binding."""

    binding, _finding = (
        _read_occurrence_position_measurement_subject_to_act_binding(
            ledger, binding_event_identity
        )
    )
    return binding


def _record_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    binding_event_identity: str,
    current_coordinates: dict[str, Any],
    carried: bool,
) -> Event:
    binding, finding = (
        _read_occurrence_position_measurement_subject_to_act_binding(
            ledger, binding_event_identity
        )
    )
    require_coordinates = (
        _require_carried_current_coordinates_at_append_boundary
        if carried
        else _require_current_coordinates
    )
    require_coordinates(
        ledger,
        locality_identity=binding.locality_identity,
        current_coordinates=current_coordinates,
        required_binding_identity=binding.identity,
    )
    for prior_act in ledger.iter_locality_kind(
        binding.locality_identity,
        OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    ):
        if (
            prior_act.material.get("subject_to_act_binding_reference")
            == _binding_reference(binding)
            or prior_act.material.get("act_occurrence_identity")
            == binding.material["act_occurrence_identity"]
        ):
            raise ValueError(
                "the occurrence position binding already carries an Act"
            )
    return ledger.append(
        OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
        _occurrence_position_act_occurrence_material(
            finding,
            binding=binding,
        ),
        locality_identity=binding.locality_identity,
    )


def record_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    *,
    binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record the Act occurrence before its Yield and result."""

    return _record_occurrence_position_measurement_act_occurrence(
        ledger,
        binding_event_identity=binding_event_identity,
        current_coordinates=current_coordinates,
        carried=False,
    )


def _require_carried_occurrence_position_binding(
    ledger: EventLedger,
    *,
    binding: Event,
    finding: OccurrencePositionFinding,
) -> None:
    if (
        type(binding) is not Event
        or type(finding) is not OccurrencePositionFinding
        or binding.kind
        != OCCURRENCE_POSITION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or binding.exact_material is not None
        or binding.locality_identity
        != finding.source_locality_identity
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position Measurement requires its exact carried binding"
        )
    material = binding.material
    identity_coordinates = {
        coordinate: material.get(coordinate)
        for coordinate in (
            "exact_act_identity",
            "act_occurrence_identity",
            "measurement_result_identity",
        )
    }
    through_event_occurrence_identity = material.get(
        "through_event_occurrence_identity"
    )
    if (
        any(
            type(identity) is not str or not identity
            for identity in identity_coordinates.values()
        )
        or len(set(identity_coordinates.values())) != len(identity_coordinates)
        or material
        != _binding_material(
            finding,
            through_event_occurrence_identity=through_event_occurrence_identity,
            **identity_coordinates,
        )
    ):
        raise ValueError(
            "occurrence position Measurement requires its exact carried binding"
        )


def _record_occurrence_position_measurement_act_occurrence_from_current_coordinates(
    ledger: EventLedger,
    *,
    binding: Event,
    finding: OccurrencePositionFinding,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record the Act from the just-carried exact binding occurrence."""

    _require_carried_occurrence_position_binding(
        ledger,
        binding=binding,
        finding=finding,
    )
    _require_carried_current_coordinates_at_append_boundary(
        ledger,
        locality_identity=binding.locality_identity,
        current_coordinates=current_coordinates,
        required_binding_identity=binding.identity,
    )
    for prior_act in ledger.iter_locality_kind(
        binding.locality_identity,
        OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
    ):
        if (
            prior_act.material.get("subject_to_act_binding_reference")
            == _binding_reference(binding)
            or prior_act.material.get("act_occurrence_identity")
            == binding.material["act_occurrence_identity"]
        ):
            raise ValueError(
                "the occurrence position binding already carries an Act"
            )
    return ledger.append(
        OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT,
        _occurrence_position_act_occurrence_material(
            finding,
            binding=binding,
        ),
        locality_identity=binding.locality_identity,
    )


def _read_occurrence_position_measurement_act_occurrence(
    ledger: EventLedger,
    act_occurrence_event_identity: str,
) -> tuple[Event, Event, OccurrencePositionFinding]:
    if type(act_occurrence_event_identity) is not str or not act_occurrence_event_identity:
        raise ValueError(
            "occurrence position result requires one exact Act occurrence identity"
        )
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act occurrence"
        )
    reference = act_occurrence.material.get("subject_to_act_binding_reference")
    if type(reference) is not dict:
        raise ValueError(
            "occurrence position result requires its exact intact Act occurrence"
        )
    try:
        binding, finding = (
            _read_occurrence_position_measurement_subject_to_act_binding(
                ledger, reference.get("recorded_occurrence_identity")
            )
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "occurrence position result requires its exact intact Act occurrence"
        ) from error
    if (
        binding.locality_identity != act_occurrence.locality_identity
        or reference != _binding_reference(binding)
        or act_occurrence.material
        != _occurrence_position_act_occurrence_material(
            finding,
            binding=binding,
        )
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act occurrence"
        )
    try:
        ledger.occurrences_in_append_order(
            (binding.identity, act_occurrence.identity),
            locality_identity=act_occurrence.locality_identity,
        )
    except ValueError as error:
        raise ValueError(
            "occurrence position Act occurrence requires its prior binding"
        ) from error
    return act_occurrence, binding, finding


def _refuse_existing_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    act_occurrence_identity: str,
) -> None:
    for prior_yield in ledger.iter_locality_kind(
        act_occurrence.locality_identity,
        RECORDED_YIELD_RELATION_EVENT,
    ):
        dimensions = prior_yield.material.get("dimensions")
        if (
            prior_yield.material.get("act_occurrence_identity")
            == act_occurrence.identity
            or (
                type(dimensions) is dict
                and dimensions.get("act_occurrence_identity")
                == act_occurrence_identity
            )
        ):
            raise ValueError(
                "the occurrence position Measurement Act already carries a Yield"
            )
    for prior_result in ledger.iter_locality_kind(
        act_occurrence.locality_identity,
        OCCURRENCE_POSITION_RECORDED_KIND,
    ):
        if (
            prior_result.material.get("act_occurrence_identity")
            == act_occurrence.identity
            or prior_result.material.get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise ValueError(
                "the occurrence position Measurement Act already carries a result"
            )


def _record_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    binding: Event,
    finding: OccurrencePositionFinding,
) -> Event:
    act_occurrence_identity = binding.material["act_occurrence_identity"]

    assertions = _position_assertions(finding)
    result_material = _occurrence_position_result_material(
        finding,
        binding=binding,
        assertions=assertions,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=act_occurrence.locality_identity,
        exact_act=OCCURRENCE_POSITION_ACT,
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=OCCURRENCE_POSITION_RESULT_KIND,
        result_identity=result_material["result_identity"],
        result_content=result_material,
        occurrence_boundary="occurrence_position_measurement",
    )
    recorded_material = {
        "result_identity": result_material["result_identity"],
        "addressed_act_identity": result_material["addressed_act_identity"],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "exact_act": result_material["exact_act"],
        "subject_to_act_binding_reference": result_material[
            "subject_to_act_binding_reference"
        ],
        "source_localities": result_material["source_localities"],
        "completeness_boundary": result_material["completeness_boundary"],
        "assertions": result_material["assertions"],
        "act_occurrence_event_identity": act_occurrence.identity,
        "yield_relation_identity": yield_relation.identity,
    }
    return ledger.append(
        OCCURRENCE_POSITION_RECORDED_KIND,
        recorded_material,
        locality_identity=act_occurrence.locality_identity,
    )


def record_occurrence_position_measurement_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the Yield and result of one exact recorded Measurement Act."""

    act_occurrence, binding, finding = (
        _read_occurrence_position_measurement_act_occurrence(
            ledger, act_occurrence_event_identity
        )
    )
    _refuse_existing_occurrence_position_measurement_result(
        ledger,
        act_occurrence=act_occurrence,
        act_occurrence_identity=binding.material["act_occurrence_identity"],
    )
    return _record_occurrence_position_measurement_result(
        ledger,
        act_occurrence=act_occurrence,
        binding=binding,
        finding=finding,
    )


def _record_occurrence_position_measurement_result_from_carried_act_occurrence(
    ledger: EventLedger,
    *,
    act_occurrence: Event,
    binding: Event,
    finding: OccurrencePositionFinding,
) -> Event:
    """Record the result from the just-produced exact Act occurrence."""

    _require_carried_occurrence_position_binding(
        ledger,
        binding=binding,
        finding=finding,
    )
    if (
        type(act_occurrence) is not Event
        or act_occurrence.kind != OCCURRENCE_POSITION_ACT_OCCURRENCE_EVENT
        or act_occurrence.exact_material is not None
        or act_occurrence.locality_identity
        != binding.locality_identity
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
        or act_occurrence.material
        != _occurrence_position_act_occurrence_material(
            finding,
            binding=binding,
        )
        or ledger.append_boundary_through_occurrence(
            act_occurrence.identity
        )
        != ledger.append_boundary()
    ):
        raise ValueError(
            "occurrence position result requires its exact intact Act occurrence"
        )
    return _record_occurrence_position_measurement_result(
        ledger,
        act_occurrence=act_occurrence,
        binding=binding,
        finding=finding,
    )


def get_recorded_occurrence_position_measurement(
    ledger: EventLedger,
    event_identity: str,
) -> OccurrencePositionFinding:
    """Read one recorded occurrence-position Measurement through its exact relation."""

    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind != OCCURRENCE_POSITION_RECORDED_KIND
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise ValueError(
            "the occurrence position Measurement result is absent or corrupted"
        )
    material = event.material
    if set(material) != OCCURRENCE_POSITION_RESULT_COORDINATES | {
        "act_occurrence_identity",
        "act_occurrence_event_identity",
        "yield_relation_identity",
    }:
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        )
    source_localities = material.get("source_localities")
    boundary = material.get("completeness_boundary")
    if (
        material.get("exact_act") != OCCURRENCE_POSITION_ACT
        or type(source_localities) is not list
        or len(source_localities) != 1
        or type(source_localities[0]) is not str
        or not source_localities[0]
        or type(boundary) is not dict
        or set(boundary) != {"identity"}
        or type(boundary["identity"]) is not str
        or not boundary["identity"]
        or type(material.get("assertions")) is not list
        or type(material.get("result_identity")) is not str
        or not material["result_identity"]
        or type(material.get("addressed_act_identity")) is not str
        or not material["addressed_act_identity"]
        or type(material.get("act_occurrence_identity")) is not str
        or not material["act_occurrence_identity"]
        or material["addressed_act_identity"]
        == material["act_occurrence_identity"]
    ):
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        )
    try:
        finding = _measure_occurrence_position_through(
            ledger,
            source_locality_identity=source_localities[0],
            boundary=EventLedgerBoundary(boundary["identity"]),
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "the occurrence position Measurement carries malformed coordinates"
        ) from error
    assertions = _position_assertions(finding)
    if material["assertions"] != assertions:
        raise ValueError(
            "the occurrence position Measurement carries malformed Assertions"
        )

    yield_relation_identity = material.get(
        "yield_relation_identity"
    )
    try:
        act_occurrence, binding, bound_finding = (
                _read_occurrence_position_measurement_act_occurrence(
                    ledger, material.get("act_occurrence_event_identity")
                )
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "the occurrence position Measurement carries no exact Act occurrence"
        ) from error
    if (
        act_occurrence.locality_identity != event.locality_identity
        or bound_finding != finding
        or material.get("subject_to_act_binding_reference")
        != _binding_reference(binding)
    ):
        raise ValueError(
            "the occurrence position Measurement carries no exact Act occurrence"
        )
    result_material = _occurrence_position_result_material(
        bound_finding,
        binding=binding,
        assertions=assertions,
    )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=(
            yield_relation_identity
            if isinstance(yield_relation_identity, str)
            else None
        ),
        act_occurrence_event_identity=act_occurrence.identity,
    )
    if not all(requirements.values()):
        raise ValueError(
            "the occurrence position Measurement carries no exact Yield relation"
        )
    carried = {
        key: value
        for key, value in material.items()
            if key
                not in {
                    "act_occurrence_event_identity",
                    "yield_relation_identity",
                }
    }
    if carried != result_material:
        raise ValueError(
            "the occurrence position Measurement result differs from its coordinates"
        )
    return finding
