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

YIELD_EVIDENCE_KIND = "operator.yield.evidence_recorded"
EVENT_KIND_RESPONSIBILITIES = {
    YIELD_EVIDENCE_KIND: "02.Acts.A",
}
YIELD_LIVE_BOUNDARIES = frozenset(
    {
        "position_pair_measurement",
        "position_pair_measurement_compare",
        "assertion_yield_compare",
        "assertion_locality_movement",
        "bounded_assertion_compare",
        "locality_count_measurement",
        "failed_emission",
        "byte_measurement",
        "byte_pair_applicability",
        "byte_pair_measurement",
        "material_ingest",
        "occurrence_position_measurement",
        "preserved_material_measurement",
        "recorded_finding_yield_compare",
        "representation_result",
        "successful_emission",
    }
)
def read_yield_relation_requirements(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
    result_evidence_event_identity: str | None,
    responsible_act_evidence_event_identity: str | None,
    recorded_result_occurrence_coordinate: str = "act_occurrence_identity",
    responsible_act_occurrence_coordinate: str = "act_occurrence_identity",
) -> dict[str, bool]:
    """Read the three machine-grammar requirements of one exact Yield relation.

    The caller supplies exact occurrence identities under pressure.  Seed
    resolves the stored occurrences itself; it does not accept read
    event materials and does not re-encode the exact result.  A missing
    result-evidence occurrence makes every requirement absent.  Changing an
    unrelated event coordinate does not.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("a Yield-relation read requires one EventLedger")
    if not isinstance(recorded_result_event_identity, str) or not recorded_result_event_identity:
        raise TypeError("a Yield-relation read requires one event occurrence")
    recorded_result_event = ledger.get(recorded_result_event_identity)
    if recorded_result_event is None:
        return {
            "exact_relation": False,
            "occurrence_witness": False,
            "intact_evidence": False,
        }
    result_evidence = (
        ledger.get(result_evidence_event_identity)
        if isinstance(result_evidence_event_identity, str)
        else None
    )
    responsible_act_evidence = (
        ledger.get(responsible_act_evidence_event_identity)
        if isinstance(responsible_act_evidence_event_identity, str)
        else None
    )
    if result_evidence is None:
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

    result_occurrence = recorded_result_event.material.get(
        recorded_result_occurrence_coordinate
    )
    evidence_dimensions = result_evidence.material.get("dimensions", {})
    same_occurrence = result_occurrence == evidence_dimensions.get(
        "act_occurrence_identity"
    )
    if responsible_act_evidence is not None:
        same_occurrence = same_occurrence and result_occurrence == (
            responsible_act_evidence.material.get(
                responsible_act_occurrence_coordinate
            )
        )
    else:
        same_occurrence = False

    evidence_is_carried = (
        recorded_result_event.material.get("yield_evidence_identity") == result_evidence.identity
        and result_evidence.kind == YIELD_EVIDENCE_KIND
    )
    evidence_is_carried = evidence_is_carried and (
        recorded_result_event.exact_material == result_evidence.exact_material
    )
    result = result_evidence.material.get("result")
    result_identity = result_evidence.material.get("result_identity")
    yield_coordinates = result_evidence.material.get("yield_coordinates")
    recorded_result_coordinates = result_evidence.material.get("recorded_result_coordinates")
    exact_carried_result = False
    if (
        type(result) is dict
        and type(yield_coordinates) is list
        and type(recorded_result_coordinates) is dict
        and yield_coordinates == sorted(result)
        and set(recorded_result_coordinates) == set(result)
    ):
        carried_result = {}
        for coordinate in yield_coordinates:
            carried_at = recorded_result_coordinates.get(coordinate)
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
            and result_evidence.material.get("responsible_act_evidence_identity")
            == responsible_act_evidence.identity
            and exact_act_evidence
        )
    else:
        evidence_is_carried = False

    return {
        "exact_relation": evidence_is_carried,
        "occurrence_witness": same_occurrence,
        "intact_evidence": (
            ledger.integrity_of(result_evidence.identity) != CORRUPTED
            and (
                responsible_act_evidence is not None
                and ledger.integrity_of(responsible_act_evidence.identity) != CORRUPTED
            )
        ),
    }


def _record_yield_evidence(
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
    recorded_result_coordinates: dict[str, tuple[str, ...]] | None = None,
    result_exact_material: bytes | None = None,
) -> Event:
    """Preserve Evidence from inside an act for its already-fixed result."""

    if not isinstance(act_occurrence_identity, str) or not act_occurrence_identity:
        raise ValueError("Yield Evidence requires one exact Act occurrence identity")
    if (
        not isinstance(responsible_act_evidence_identity, str)
        or not responsible_act_evidence_identity
    ):
        raise ValueError("Yield Evidence requires exact responsible Act Evidence")
    if (
        not isinstance(responsible_act_occurrence_coordinate, str)
        or not responsible_act_occurrence_coordinate
    ):
        raise ValueError("Yield Evidence requires one exact Act occurrence coordinate")
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
            "Yield Evidence requires intact responsible Act Evidence for its occurrence"
        )
    if live_boundary not in YIELD_LIVE_BOUNDARIES:
        raise ValueError("Yield Evidence requires one declared live boundary")
    if type(result_content) is not dict:
        raise TypeError("Yield Evidence requires one exact result")
    if not isinstance(result_identity, str) or not result_identity:
        raise TypeError("Yield Evidence requires one exact result identity")
    if result_content.get("result_identity") != result_identity:
        raise ValueError("Yield Evidence result identity must be carried by its result")
    if result_exact_material is not None and type(result_exact_material) is not bytes:
        raise TypeError("Yield Evidence exact material must be exact bytes or absent")
    declared_recorded_result_coordinates = (
        {coordinate: (coordinate,) for coordinate in result_content}
        if recorded_result_coordinates is None
        else recorded_result_coordinates
    )
    if type(declared_recorded_result_coordinates) is not dict or set(
        declared_recorded_result_coordinates
    ) != set(result_content):
        raise ValueError(
            "Yield Evidence requires one carried coordinate for every result coordinate"
        )
    preserved_recorded_result_coordinates = {}
    for coordinate, carried_at in declared_recorded_result_coordinates.items():
        if type(coordinate) is not str or not coordinate:
            raise TypeError("a result coordinate must be one exact representation")
        if type(carried_at) is not tuple or not carried_at or not all(
            type(part) is str and part for part in carried_at
        ):
            raise TypeError(
                "a carried coordinate must be one nonempty tuple of exact representations"
            )
        preserved_recorded_result_coordinates[coordinate] = list(carried_at)

    return ledger.append(
        YIELD_EVIDENCE_KIND,
        {
            "responsible_act_evidence_identity": responsible_act_evidence_identity,
            "result_identity": result_identity,
            "dimensions": {
                "identity": (
                    f"yield-evidence:{act_occurrence_identity}:{result_identity}"
                ),
                "content": (
                    f"Evidence for the exact Yield from the {exact_act} occurrence "
                    f"to this exact {result_kind} result at its Act boundary"
                ),
                "exact_act": exact_act,
                "act_occurrence_identity": act_occurrence_identity,
                "occurrence_result_evidence": (
                    "preserved at the exact Act boundary after this exact "
                    "result was fixed; the result carries the relation to this"
                ),
                "responsibility": responsibility,
                "responsible_boundary": responsible_boundary,
                "authority": "unestablished",
                "evidence_scope": (
                    "establishes the exact occurrence-to-result relation at this "
                    "Act boundary; establishes no responsibility, "
                    "authorization, or occurrence beyond this boundary"
                ),
                "occurrence_preservation": (
                    "Evidence for the exact occurrence-to-result relation, "
                    "recorded; not the relation or Act occurrence by identity"
                ),
            },
            "yield_coordinates": sorted(result_content),
            "result": deepcopy(result_content),
            "recorded_result_coordinates": preserved_recorded_result_coordinates,
            "result_kind": result_kind,
            "live_boundary": live_boundary,
        },
        exact_material=result_exact_material,
        locality_identity=locality_identity,
    )
