"""Continue one exact prior Locality Standing boundary at another Locality.

This boundary establishes one direct Locality relation and bounded
availability only.  It does not copy the prior Locality's occurrences or
Standing accumulators, make any carried subject applicable to another Act,
establish priority, or follow another continuation transitively.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.yield_relation import (
    RECORDED_YIELD_RELATION_EVENT,
    _record_yield_relation,
    read_requirements_of_yield_relation,
)


STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT = (
    "operator.standing.locality_continuation_act_occurrence_recorded"
)
STANDING_LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND = (
    "operator.standing.locality_continuation_subject_to_act_binding_recorded"
)
STANDING_LOCALITY_CONTINUATION_RECORDED_KIND = (
    "operator.standing.locality_continuation_recorded"
)
STANDING_LOCALITY_CONTINUATION_RESULT_KIND = (
    "Standing Locality relation result"
)
STANDING_LOCALITY_CONTINUATION_ACT = "Standing Locality relation"
STANDING_LOCALITY_CONTINUATION_INPUT_ROLE = (
    "exact prior Locality Standing boundary"
)
EVENT_KIND_RESPONSIBILITIES = {
    STANDING_LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND: (
        "06.Locality.B"
    ),
    STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT: "02.Acts.A",
    STANDING_LOCALITY_CONTINUATION_RECORDED_KIND: "06.Locality.A",
}
STANDING_LOCALITY_CONTINUATION_ASSIGNMENT_BOOK_CLAUSE = "06.Locality.B"


class StandingLocalityContinuationError(ValueError):
    """One exact Standing Locality continuation could not be established."""


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise StandingLocalityContinuationError(message)
    return value


def _source_standing_reference(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    standing_boundary_event_identity: str,
) -> dict[str, str | None]:
    """Resolve one intact exact source Standing boundary."""

    _require_identity(
        source_locality_identity,
        "Standing Locality continuation requires one exact source Locality",
    )
    _require_identity(
        standing_boundary_event_identity,
        "Standing Locality continuation requires one exact Standing boundary",
    )
    source_boundary = ledger.get(standing_boundary_event_identity)
    if (
        source_boundary is None
        or source_boundary.locality_identity != source_locality_identity
        or ledger.integrity_of(source_boundary.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation requires one intact source boundary"
        )
    occurrences = ledger.list_locality(source_locality_identity)
    positions = {event.identity: position for position, event in enumerate(occurrences)}
    if positions.get(standing_boundary_event_identity) is None:
        raise StandingLocalityContinuationError(
            "the source Standing boundary is absent from its source Locality"
        )
    return {
        "source_locality_identity": source_locality_identity,
        "source_standing_through_event_occurrence_identity": (
            standing_boundary_event_identity
        ),
    }


def _participation(
    source_standing_reference: dict[str, str | None],
    *,
    act_occurrence_identity: str,
) -> dict[str, Any]:
    return {
        "subject_reference": deepcopy(source_standing_reference),
        "role": STANDING_LOCALITY_CONTINUATION_INPUT_ROLE,
        "act_occurrence_identity": act_occurrence_identity,
    }


def _binding_material(
    *,
    exact_act_identity: str,
    result_boundary_identity: str,
    source_standing_reference: dict[str, str | None],
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "book_clause_identity": (
            STANDING_LOCALITY_CONTINUATION_ASSIGNMENT_BOOK_CLAUSE
        ),
        "exact_act_identity": exact_act_identity,
        "subject_reference": deepcopy(source_standing_reference),
        "destination_locality_identity": destination_locality_identity,
        "scope": {
            "source_locality_identity": source_standing_reference[
                "source_locality_identity"
            ],
            "source_standing_through_event_occurrence_identity": source_standing_reference[
                "source_standing_through_event_occurrence_identity"
            ],
            "destination_locality_identity": destination_locality_identity,
        },
        "result_boundary_identity": result_boundary_identity,
        "unknown": [
            "Applicability of every carried subject to another Act: Unknown"
        ],
    }


def _binding_reference(binding: Event) -> dict[str, Any]:
    return {
        "recorded_occurrence_identity": binding.identity,
        "book_clause_identity": binding.material["book_clause_identity"],
        "exact_act_identity": binding.material["exact_act_identity"],
        "subject_reference": deepcopy(binding.material["subject_reference"]),
        "result_boundary_identity": binding.material[
            "result_boundary_identity"
        ],
    }


def _act_occurrence_material(
    *,
    continuation_act_identity: str,
    act_occurrence_identity: str,
    locality_relation_occurrence_identity: str,
    subject_to_act_binding_reference: dict[str, Any],
    source_standing_reference: dict[str, str | None],
    destination_locality_identity: str,
) -> dict[str, Any]:
    return {
        "continuation_act_identity": continuation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "locality_relation_occurrence_identity": (
            locality_relation_occurrence_identity
        ),
        "act": STANDING_LOCALITY_CONTINUATION_ACT,
        "subject_to_act_binding_reference": dict(
            subject_to_act_binding_reference
        ),
        "source_standing_reference": deepcopy(source_standing_reference),
        "destination_locality_identity": destination_locality_identity,
        "participation": _participation(
            source_standing_reference,
            act_occurrence_identity=act_occurrence_identity,
        ),
    }


def _result_material(
    *,
    result_identity: str,
    continuation_act_identity: str,
    act_occurrence_identity: str,
    locality_relation_occurrence_identity: str,
    subject_to_act_binding_reference: dict[str, Any],
    source_standing_reference: dict[str, str | None],
    destination_locality_identity: str,
) -> dict[str, Any]:
    participation = _participation(
        source_standing_reference,
        act_occurrence_identity=act_occurrence_identity,
    )
    return {
        "result_identity": result_identity,
        "continuation_act_identity": continuation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "locality_relation_occurrence_identity": (
            locality_relation_occurrence_identity
        ),
        "exact_act": STANDING_LOCALITY_CONTINUATION_ACT,
        "subject_to_act_binding_reference": dict(
            subject_to_act_binding_reference
        ),
        "source_standing_reference": deepcopy(source_standing_reference),
        "destination_locality_identity": destination_locality_identity,
        "participation": participation,
        "locality_relation": {
            "first_subject": deepcopy(source_standing_reference),
            "second_subject": destination_locality_identity,
            "relation_occurrence_identity": locality_relation_occurrence_identity,
        },
        "unknown": [
            "Applicability of every carried subject to another Act: Unknown"
        ],
    }


def _recorded_result_material(
    result_material: dict[str, Any],
    *,
    act_occurrence_event_identity: str,
    yield_relation_identity: str,
) -> dict[str, Any]:
    """Carry every result coordinate at one literal durable address."""

    return {
        "result_identity": result_material["result_identity"],
        "continuation_act_identity": result_material[
            "continuation_act_identity"
        ],
        "act_occurrence_identity": result_material["act_occurrence_identity"],
        "locality_relation_occurrence_identity": result_material[
            "locality_relation_occurrence_identity"
        ],
        "exact_act": result_material["exact_act"],
        "subject_to_act_binding_reference": result_material[
            "subject_to_act_binding_reference"
        ],
        "source_standing_reference": result_material[
            "source_standing_reference"
        ],
        "destination_locality_identity": result_material[
            "destination_locality_identity"
        ],
        "participation": result_material["participation"],
        "locality_relation": result_material["locality_relation"],
        "unknown": result_material["unknown"],
        "act_occurrence_event_identity": act_occurrence_event_identity,
        "yield_relation_identity": yield_relation_identity,
    }


def record_standing_locality_continuation_subject_to_act_binding(
    ledger: EventLedger,
    *,
    source_locality_identity: str,
    standing_boundary_event_identity: str,
) -> Event:
    """Bind one source-boundary Locality relation to its exact Act."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Standing Locality continuation requires one EventLedger")
    source_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_locality_identity,
        standing_boundary_event_identity=standing_boundary_event_identity,
    )
    destination_locality_identity = new_identity("standing_locality")
    if ledger.has_locality(destination_locality_identity):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation requires one fresh destination Locality"
        )
    exact_act_identity = new_identity("standing_locality_continuation_act")
    result_boundary_identity = new_identity(
        "standing_locality_continuation_result_boundary"
    )
    return ledger.append(
        STANDING_LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND,
        _binding_material(
            exact_act_identity=exact_act_identity,
            result_boundary_identity=result_boundary_identity,
            source_standing_reference=source_reference,
            destination_locality_identity=destination_locality_identity,
        ),
        locality_identity=destination_locality_identity,
    )


def record_standing_locality_continuation_act_occurrence(
    ledger: EventLedger,
    *,
    subject_to_act_binding_event_identity: str,
    current_coordinates: dict[str, Any],
) -> Event:
    """Record one Act from one exact carried subject-to-Act binding."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("Standing Locality continuation requires one EventLedger")
    binding = get_standing_locality_continuation_subject_to_act_binding(
        ledger, subject_to_act_binding_event_identity
    )
    if type(current_coordinates) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act requires current coordinates"
        )
    binding_occurrences = current_coordinates.get(
        "subject_to_act_binding_occurrences"
    )
    if (
        current_coordinates.get("locality_identity") != binding.locality_identity
        or type(binding_occurrences) is not dict
        or binding.identity not in binding_occurrences
        or binding_occurrences[binding.identity] is not None
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act requires its exact carried binding"
        )
    standing_boundary = current_coordinates.get(
        "through_event_occurrence_identity"
    )
    standing_boundary_event = ledger.get(standing_boundary)
    if (
        type(standing_boundary) is not str
        or not standing_boundary
        or standing_boundary_event is None
        or standing_boundary_event.locality_identity != binding.locality_identity
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act requires one exact current-coordinate boundary"
        )
    if standing_boundary != binding.identity:
        try:
            ledger.occurrences_in_append_order(
                (binding.identity, standing_boundary),
                locality_identity=binding.locality_identity,
            )
        except ValueError as error:
            raise StandingLocalityContinuationError(
                "Standing Locality continuation Act requires its prior binding occurrence"
            ) from error

    source_reference = binding.material["subject_reference"]
    destination_locality_identity = binding.locality_identity
    continuation_act_identity = binding.material["exact_act_identity"]
    act_occurrence_identity = new_identity(
        "standing_locality_continuation_occurrence"
    )
    locality_relation_occurrence_identity = new_identity(
        "standing_locality_continuation_relation_occurrence"
    )
    return ledger.append(
        STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT,
        _act_occurrence_material(
            continuation_act_identity=continuation_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            locality_relation_occurrence_identity=(
                locality_relation_occurrence_identity
            ),
            subject_to_act_binding_reference=_binding_reference(binding),
            source_standing_reference=source_reference,
            destination_locality_identity=destination_locality_identity,
        ),
        locality_identity=destination_locality_identity,
    )


def _validated_act_occurrence(
    ledger: EventLedger, act_occurrence_event_identity: str
) -> Event:
    _require_identity(
        act_occurrence_event_identity,
        "Standing Locality continuation result requires one exact Act occurrence identity",
    )
    act_occurrence = ledger.get(act_occurrence_event_identity)
    if (
        act_occurrence is None
        or act_occurrence.kind != STANDING_LOCALITY_CONTINUATION_ACT_OCCURRENCE_EVENT
        or type(act_occurrence.locality_identity) is not str
        or not act_occurrence.locality_identity
        or act_occurrence.exact_material is not None
        or ledger.integrity_of(act_occurrence.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation result requires intact Act occurrence"
        )
    material = act_occurrence.material
    source_reference = material.get("source_standing_reference")
    if type(source_reference) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence carries no exact source boundary"
        )
    expected_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_reference.get("source_locality_identity"),
        standing_boundary_event_identity=source_reference.get(
            "source_standing_through_event_occurrence_identity"
        ),
    )
    if source_reference != expected_reference:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence carries another source boundary"
        )
    continuation_act_identity = material.get("continuation_act_identity")
    act_occurrence_identity = material.get("act_occurrence_identity")
    locality_relation_occurrence_identity = material.get(
        "locality_relation_occurrence_identity"
    )
    binding_reference = material.get("subject_to_act_binding_reference")
    if type(binding_reference) is not dict:
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence carries no exact subject-to-Act binding"
        )
    binding = get_standing_locality_continuation_subject_to_act_binding(
        ledger, binding_reference.get("recorded_occurrence_identity")
    )
    if (
        type(continuation_act_identity) is not str
        or not continuation_act_identity
        or type(act_occurrence_identity) is not str
        or not act_occurrence_identity
        or continuation_act_identity == act_occurrence_identity
        or type(locality_relation_occurrence_identity) is not str
        or not locality_relation_occurrence_identity
        or locality_relation_occurrence_identity
        in {continuation_act_identity, act_occurrence_identity}
        or len(
            {
                binding.identity,
                binding.material["result_boundary_identity"],
                continuation_act_identity,
                act_occurrence_identity,
                locality_relation_occurrence_identity,
            }
        )
        != 5
        or binding_reference != _binding_reference(binding)
        or binding.locality_identity != act_occurrence.locality_identity
        or binding.material["subject_reference"] != expected_reference
        or binding.material["destination_locality_identity"]
        != act_occurrence.locality_identity
        or material.get("destination_locality_identity")
        != act_occurrence.locality_identity
        or material
        != _act_occurrence_material(
            continuation_act_identity=continuation_act_identity,
            act_occurrence_identity=act_occurrence_identity,
            locality_relation_occurrence_identity=(
                locality_relation_occurrence_identity
            ),
            subject_to_act_binding_reference=binding_reference,
            source_standing_reference=expected_reference,
            destination_locality_identity=act_occurrence.locality_identity,
        )
    ):
        raise StandingLocalityContinuationError(
            "Standing Locality continuation Act occurrence is not exact"
        )
    return act_occurrence


def record_standing_locality_continuation_result(
    ledger: EventLedger,
    *,
    act_occurrence_event_identity: str,
) -> Event:
    """Record the Yield and direct Locality relation for one recorded Act."""

    act_occurrence = _validated_act_occurrence(
        ledger, act_occurrence_event_identity
    )
    material = act_occurrence.material
    locality_identity = act_occurrence.locality_identity
    act_occurrence_identity = material["act_occurrence_identity"]
    for prior_yield in ledger.iter_locality_kind(
        locality_identity, RECORDED_YIELD_RELATION_EVENT
    ):
        dimensions = prior_yield.material.get("dimensions")
        if (
            prior_yield.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
            or (
                type(dimensions) is dict
                and dimensions.get("act_occurrence_identity")
                == act_occurrence_identity
            )
        ):
            raise StandingLocalityContinuationError(
                "the Standing Locality continuation Act already carries a Yield"
            )
    for prior_result in ledger.iter_locality_kind(
        locality_identity, STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
    ):
        if (
            prior_result.material.get("act_occurrence_event_identity")
            == act_occurrence.identity
            or prior_result.material.get("act_occurrence_identity")
            == act_occurrence_identity
        ):
            raise StandingLocalityContinuationError(
                "the Standing Locality continuation Act already carries a result"
            )

    result_identity = material["subject_to_act_binding_reference"][
        "result_boundary_identity"
    ]
    result_material = _result_material(
        result_identity=result_identity,
        continuation_act_identity=material["continuation_act_identity"],
        act_occurrence_identity=act_occurrence_identity,
        locality_relation_occurrence_identity=material[
            "locality_relation_occurrence_identity"
        ],
        subject_to_act_binding_reference=material[
            "subject_to_act_binding_reference"
        ],
        source_standing_reference=material["source_standing_reference"],
        destination_locality_identity=locality_identity,
    )
    yield_relation = _record_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act=STANDING_LOCALITY_CONTINUATION_ACT,
        act_occurrence_identity=act_occurrence_identity,
        act_occurrence_event_identity=act_occurrence.identity,
        result_kind=STANDING_LOCALITY_CONTINUATION_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        occurrence_boundary="standing_locality_continuation",
    )
    return ledger.append(
        STANDING_LOCALITY_CONTINUATION_RECORDED_KIND,
        _recorded_result_material(
            result_material,
            act_occurrence_event_identity=act_occurrence.identity,
            yield_relation_identity=yield_relation.identity,
        ),
        locality_identity=locality_identity,
    )


def get_recorded_standing_locality_continuation(
    ledger: EventLedger, recorded_result_event_identity: str
) -> dict[str, Any]:
    """Read one direct continuation relation through its exact relation."""

    _require_identity(
        recorded_result_event_identity,
        "Standing Locality continuation read requires one exact result occurrence",
    )
    event = ledger.get(recorded_result_event_identity)
    if (
        event is None
        or event.kind != STANDING_LOCALITY_CONTINUATION_RECORDED_KIND
        or type(event.locality_identity) is not str
        or not event.locality_identity
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation result is absent or corrupted"
        )
    act_occurrence = _validated_act_occurrence(
        ledger, event.material.get("act_occurrence_event_identity")
    )
    result_identity = event.material.get("result_identity")
    expected = _result_material(
        result_identity=result_identity,
        continuation_act_identity=act_occurrence.material[
            "continuation_act_identity"
        ],
        act_occurrence_identity=act_occurrence.material["act_occurrence_identity"],
        locality_relation_occurrence_identity=act_occurrence.material[
            "locality_relation_occurrence_identity"
        ],
        subject_to_act_binding_reference=act_occurrence.material[
            "subject_to_act_binding_reference"
        ],
        source_standing_reference=act_occurrence.material[
            "source_standing_reference"
        ],
        destination_locality_identity=event.locality_identity,
    )
    expected_event_material = _recorded_result_material(
        expected,
        act_occurrence_event_identity=act_occurrence.identity,
        yield_relation_identity=event.material.get("yield_relation_identity"),
    )
    if (
        type(result_identity) is not str
        or not result_identity
        or act_occurrence.locality_identity != event.locality_identity
        or event.material != expected_event_material
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation result coordinates are not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        yield_relation_event_identity=event.material["yield_relation_identity"],
        act_occurrence_event_identity=act_occurrence.identity,
    )
    if not all(requirements.values()):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation carries no exact Yield relation"
        )
    return deepcopy(event.material)


def get_standing_locality_continuation_subject_to_act_binding(
    ledger: EventLedger, recorded_binding_event_identity: str
) -> Event:
    """Read one exact subject-to-Act binding occurrence."""

    _require_identity(
        recorded_binding_event_identity,
        "Standing Locality continuation requires one exact binding occurrence",
    )
    binding = ledger.get(recorded_binding_event_identity)
    if (
        binding is None
        or binding.kind
        != STANDING_LOCALITY_CONTINUATION_SUBJECT_TO_ACT_BINDING_RECORDED_KIND
        or type(binding.locality_identity) is not str
        or not binding.locality_identity
        or binding.exact_material is not None
        or ledger.integrity_of(binding.identity) == CORRUPTED
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation binding is absent or corrupted"
        )
    material = binding.material
    source_reference = material.get("subject_reference")
    if type(source_reference) is not dict:
        raise StandingLocalityContinuationError(
            "the binding carries no exact source boundary"
        )
    expected_reference = _source_standing_reference(
        ledger,
        source_locality_identity=source_reference.get("source_locality_identity"),
        standing_boundary_event_identity=source_reference.get(
            "source_standing_through_event_occurrence_identity"
        ),
    )
    exact_act_identity = material.get("exact_act_identity")
    result_boundary_identity = material.get("result_boundary_identity")
    if (
        type(exact_act_identity) is not str
        or not exact_act_identity
        or type(result_boundary_identity) is not str
        or not result_boundary_identity
        or exact_act_identity == result_boundary_identity
        or source_reference != expected_reference
        or material
        != _binding_material(
            exact_act_identity=exact_act_identity,
            result_boundary_identity=result_boundary_identity,
            source_standing_reference=expected_reference,
            destination_locality_identity=binding.locality_identity,
        )
    ):
        raise StandingLocalityContinuationError(
            "the Standing Locality continuation binding is not exact"
        )
    return binding
