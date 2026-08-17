"""Evidence for one exact Yield relation.

This does not establish Responsibility. It preserves, from inside
an act after that act has fixed its result, Evidence committing to the exact
result coordinates. The resulting Event is Evidence for the exact
occurrence-to-result relation; it is neither that relation nor either endpoint by identity.

The helper is private implementation plumbing, not the guarantee. The result's
carried relation to this Evidence distinguishes a result with exact Yield from an
identical caller-supplied representation. A public entry point that
accepts arbitrary result content would instead create a second recorder able to
manufacture that relation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger

RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND = "operator.evidence_of_yield_relation_recorded"
EVENT_KIND_RESPONSIBILITIES = {
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND: "02.Acts.A",
}
LIVE_BOUNDARIES_OF_YIELD_RELATION = frozenset(
    {
        "assertion_locality_movement",
        "failed_emission",
        "byte_measurement",
        "byte_pair_applicability",
        "byte_pair_measurement",
        "material_ingest",
        "occurrence_position_measurement",
        "measurement_of_recurrent_byte_pair_occurrence_position",
        "operator_material_acquire",
        "representation_result",
        "recorded_standing_boundary_locality_relation",
        "standing_boundary_reference",
        "standing_locality_continuation",
        "successful_emission",
    }
)
def read_requirements_of_evidence_carried_by_result_occurrence(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
    evidence_of_yield_relation_event_identity: str | None,
    recorded_result_occurrence_coordinate: str = "act_occurrence_identity",
) -> dict[str, bool]:
    """Read Evidence carried by a result occurrence separately from the Yield relation.

    The recording occurrence carries the exact Evidence occurrence by identity.
    The Evidence occurrence in turn names the Act occurrence whose result is
    recorded.  Neither equal result content nor endpoint presence substitutes
    for this carried relation.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("an Evidence-carried-by-result-occurrence read requires one EventLedger")
    if (
        type(recorded_result_event_identity) is not str
        or not recorded_result_event_identity
    ):
        raise TypeError("an Evidence-carried-by-result-occurrence read requires one result occurrence")
    if (
        type(evidence_of_yield_relation_event_identity) is not str
        or not evidence_of_yield_relation_event_identity
    ):
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    if (
        type(recorded_result_occurrence_coordinate) is not str
        or not recorded_result_occurrence_coordinate
    ):
        raise TypeError("the carried result occurrence coordinate must be exact")

    recorded_result_event = ledger.get(recorded_result_event_identity)
    evidence_of_yield_relation = ledger.get(
        evidence_of_yield_relation_event_identity
    )
    if recorded_result_event is None or evidence_of_yield_relation is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }

    exact_relation = (
        recorded_result_event.material.get(
            "evidence_of_yield_relation_identity"
        )
        == evidence_of_yield_relation.identity
        and evidence_of_yield_relation.kind
        == RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    )
    occurrence_witness = (
        recorded_result_event.locality_identity
        == evidence_of_yield_relation.locality_identity
        and recorded_result_event.material.get(
            recorded_result_occurrence_coordinate
        )
        == evidence_of_yield_relation.material.get("dimensions", {}).get(
            "act_occurrence_identity"
        )
    )
    if occurrence_witness:
        try:
            ledger.occurrences_in_append_order(
                (
                    evidence_of_yield_relation.identity,
                    recorded_result_event.identity,
                ),
                locality_identity=recorded_result_event.locality_identity,
            )
        except (TypeError, ValueError):
            occurrence_witness = False

    return {
        "exact_relation": exact_relation,
        "occurrence_witness": occurrence_witness,
        "intact_evidence": (
            ledger.integrity_of(evidence_of_yield_relation.identity)
            != CORRUPTED
        ),
    }


def read_requirements_of_yield_relation(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
    evidence_of_yield_relation_event_identity: str | None,
    responsible_act_evidence_event_identity: str | None,
    recorded_result_occurrence_coordinate: str = "act_occurrence_identity",
    responsible_act_occurrence_coordinate: str = "act_occurrence_identity",
) -> dict[str, bool]:
    """Read the three witness-grammar requirements of one exact Yield relation.

    The caller supplies exact occurrence identities under pressure.  Seed
    resolves the stored occurrences itself; it does not accept read
    event materials and does not re-encode the exact result.  A missing
    result-evidence occurrence makes every requirement absent.  Changing an
    unrelated event coordinate does not.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("a Yield relation read requires one EventLedger")
    if not isinstance(recorded_result_event_identity, str) or not recorded_result_event_identity:
        raise TypeError("a Yield relation read requires one event occurrence")
    recorded_result_event = ledger.get(recorded_result_event_identity)
    if recorded_result_event is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    evidence_of_yield_relation = (
        ledger.get(evidence_of_yield_relation_event_identity)
        if isinstance(evidence_of_yield_relation_event_identity, str)
        else None
    )
    responsible_act_evidence = (
        ledger.get(responsible_act_evidence_event_identity)
        if isinstance(responsible_act_evidence_event_identity, str)
        else None
    )
    if evidence_of_yield_relation is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    if not isinstance(recorded_result_occurrence_coordinate, str) or not (
        recorded_result_occurrence_coordinate
    ):
        raise TypeError("the event occurrence coordinate must be exact")
    if not isinstance(responsible_act_occurrence_coordinate, str) or not (
        responsible_act_occurrence_coordinate
    ):
        raise TypeError("the responsible-Act occurrence coordinate must be exact")

    act_occurrence_identity_of_recorded_result = recorded_result_event.material.get(
        recorded_result_occurrence_coordinate
    )
    evidence_dimensions = evidence_of_yield_relation.material.get("dimensions", {})
    same_occurrence = act_occurrence_identity_of_recorded_result == evidence_dimensions.get(
        "act_occurrence_identity"
    )
    if responsible_act_evidence is not None:
        same_occurrence = same_occurrence and act_occurrence_identity_of_recorded_result == (
            responsible_act_evidence.material.get(
                responsible_act_occurrence_coordinate
            )
        )
    else:
        same_occurrence = False

    evidence_is_carried = (
        recorded_result_event.material.get("evidence_of_yield_relation_identity") == evidence_of_yield_relation.identity
        and evidence_of_yield_relation.kind == RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    )
    evidence_is_carried = evidence_is_carried and (
        recorded_result_event.exact_material == evidence_of_yield_relation.exact_material
    )
    result = evidence_of_yield_relation.material.get("result")
    result_identity = evidence_of_yield_relation.material.get("result_identity")
    coordinates_of_carried_result = evidence_of_yield_relation.material.get("coordinates_of_carried_result")
    coordinates_of_recorded_result = evidence_of_yield_relation.material.get("coordinates_of_recorded_result")
    exact_carried_result = False
    if (
        type(result) is dict
        and type(coordinates_of_carried_result) is list
        and type(coordinates_of_recorded_result) is dict
        and coordinates_of_carried_result == list(result)
        and set(coordinates_of_recorded_result) == set(result)
    ):
        carried_result = {}
        for coordinate in coordinates_of_carried_result:
            carried_at = coordinates_of_recorded_result.get(coordinate)
            if type(carried_at) is not list or not carried_at or not all(
                type(part) is str and part for part in carried_at
            ):
                break
            value = recorded_result_event.material
            for part in carried_at:
                if type(value) is not dict or part not in value:
                    break
                value = value[part]
            else:
                carried_result[coordinate] = value
                continue
            break
        else:
            exact_carried_result = carried_result == result
    evidence_is_carried = (
        evidence_is_carried
        and exact_carried_result
        and isinstance(result_identity, str)
        and result_identity
        and type(result) is dict
        and result.get("result_identity") == result_identity
        and recorded_result_event.material.get("result_identity") == result_identity
    )
    if responsible_act_evidence is not None:
        exact_act_evidence = (
            evidence_dimensions.get("exact_act")
            == responsible_act_evidence.material.get("act")
            and evidence_dimensions.get("responsibility")
            == responsible_act_evidence.material.get("responsibility")
            and evidence_dimensions.get("responsible_boundary")
            == responsible_act_evidence.material.get("responsible_boundary")
        )
        evidence_is_carried = evidence_is_carried and (
            recorded_result_event.material.get("responsible_act_evidence_identity")
            == responsible_act_evidence.identity
            and evidence_of_yield_relation.material.get("responsible_act_evidence_identity")
            == responsible_act_evidence.identity
            and exact_act_evidence
        )
    else:
        evidence_is_carried = False

    return {
        "exact_relation": evidence_is_carried,
        "occurrence_witness": same_occurrence,
        "intact_evidence": (
            ledger.integrity_of(evidence_of_yield_relation.identity) != CORRUPTED
            and (
                responsible_act_evidence is not None
                and ledger.integrity_of(responsible_act_evidence.identity) != CORRUPTED
            )
        ),
    }


def _record_evidence_of_yield_relation(
    ledger: EventLedger,
    *,
    locality_identity: str | None,
    exact_act: str,
    act_occurrence_identity: str,
    responsible_act_evidence_identity: str,
    result_kind: str,
    result_identity: str,
    result_content: dict[str, Any],
    responsibility: str,
    live_boundary: str,
    responsible_boundary: str = "unestablished",
    responsible_act_occurrence_coordinate: str = "act_occurrence_identity",
    coordinates_of_recorded_result: dict[str, tuple[str, ...]] | None = None,
    result_exact_material: bytes | None = None,
) -> Event:
    """Preserve Evidence from inside an act for its already-fixed result."""

    if not isinstance(act_occurrence_identity, str) or not act_occurrence_identity:
        raise ValueError("Evidence of Yield relation requires one exact Act occurrence identity")
    if (
        not isinstance(responsible_act_evidence_identity, str)
        or not responsible_act_evidence_identity
    ):
        raise ValueError("Evidence of Yield relation requires exact responsible Act Evidence")
    if (
        not isinstance(responsible_act_occurrence_coordinate, str)
        or not responsible_act_occurrence_coordinate
    ):
        raise ValueError("Evidence of Yield relation requires one exact Act occurrence coordinate")
    responsible_act_evidence = ledger.get(responsible_act_evidence_identity)
    if (
        responsible_act_evidence is None
        or responsible_act_evidence.material.get(responsible_act_occurrence_coordinate)
        != act_occurrence_identity
        or responsible_act_evidence.material.get("act") != exact_act
        or responsible_act_evidence.material.get("responsibility") != responsibility
        or responsible_act_evidence.material.get("responsible_boundary")
        != responsible_boundary
        or ledger.integrity_of(responsible_act_evidence_identity) == CORRUPTED
    ):
        raise ValueError(
            "Evidence of Yield relation requires intact responsible Act Evidence for its occurrence"
        )
    if live_boundary not in LIVE_BOUNDARIES_OF_YIELD_RELATION:
        raise ValueError("Evidence of Yield relation requires one declared live boundary")
    if type(result_content) is not dict:
        raise TypeError("Evidence of Yield relation requires one exact result")
    if not isinstance(result_identity, str) or not result_identity:
        raise TypeError("Evidence of Yield relation requires one exact result identity")
    if result_content.get("result_identity") != result_identity:
        raise ValueError("Evidence of Yield relation result identity must be carried by its result")
    if result_exact_material is not None and type(result_exact_material) is not bytes:
        raise TypeError("Evidence of Yield relation exact material must be exact bytes or absent")
    declared_coordinates_of_recorded_result = (
        {coordinate: (coordinate,) for coordinate in result_content}
        if coordinates_of_recorded_result is None
        else coordinates_of_recorded_result
    )
    if type(declared_coordinates_of_recorded_result) is not dict or set(
        declared_coordinates_of_recorded_result
    ) != set(result_content):
        raise ValueError(
            "Evidence of Yield relation requires one carried coordinate for every result coordinate"
        )
    preserved_coordinates_of_recorded_result = {}
    for coordinate, carried_at in declared_coordinates_of_recorded_result.items():
        if type(coordinate) is not str or not coordinate:
            raise TypeError("a result coordinate must be one exact representation")
        if type(carried_at) is not tuple or not carried_at or not all(
            type(part) is str and part for part in carried_at
        ):
            raise TypeError(
                "a carried coordinate must be one nonempty tuple of exact representations"
            )
        preserved_coordinates_of_recorded_result[coordinate] = list(carried_at)

    return ledger.append(
        RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
        {
            "responsible_act_evidence_identity": responsible_act_evidence_identity,
            "result_identity": result_identity,
            "dimensions": {
                "identity": (
                    f"yield-evidence:{act_occurrence_identity}:{result_identity}"
                ),
                "exact_act": exact_act,
                "act_occurrence_identity": act_occurrence_identity,
                "responsibility": responsibility,
                "responsible_boundary": responsible_boundary,
                "authority": "unestablished",
            },
            "coordinates_of_carried_result": list(result_content),
            "result": deepcopy(result_content),
            "coordinates_of_recorded_result": preserved_coordinates_of_recorded_result,
            "result_kind": result_kind,
            "live_boundary": live_boundary,
        },
        exact_material=result_exact_material,
        locality_identity=locality_identity,
    )
