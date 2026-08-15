"""Private physiology for Evidence concerning one exact yielded result.

This does not establish Responsibility. It preserves, from inside
an act after that act has fixed its result, Evidence committing to the exact
coordinates yielded. The resulting Event is Evidence concerning the exact
occurrence-to-result edge; it is neither that edge nor either endpoint by identity.

The helper is private implementation plumbing, not the guarantee. The result's
carried relation to this Evidence distinguishes a yielded result from an
identical caller-supplied representation. Exposing a public entry point that
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
        "adjacency_pair_measurement",
        "adjacency_pair_measurement_compare",
        "assertion_yield_compare",
        "assertion_locality_movement",
        "bounded_assertion_compare",
        "locality_count_measurement",
        "failed_emission_outcome",
        "byte_measurement",
        "byte_pair_applicability",
        "byte_pair_measurement",
        "material_ingest",
        "preserved_material_measurement",
        "recorded_finding_yield_compare",
        "representation_result",
        "successful_emission",
    }
)
def read_yield_edge_requirements(
    ledger: EventLedger,
    *,
    recorded_result_event_identity: str,
    result_evidence_event_identity: str | None,
    responsible_act_evidence_event_identity: str | None = None,
    recorded_result_occurrence_coordinate: str = "act_occurrence_identity",
    responsible_act_occurrence_coordinate: str = "act_occurrence_identity",
) -> dict[str, bool]:
    """Read the three machine-grammar requirements of one exact Yield edge.

    The caller supplies exact occurrence identities under pressure.  Seed
    resolves the stored occurrences itself; it does not accept read
    event payloads and does not re-encode the yielded result.  A missing
    result-evidence occurrence makes every requirement absent.  Changing an
    unrelated event coordinate does not.
    """

    if not isinstance(ledger, EventLedger):
        raise TypeError("a Yield-edge read requires one EventLedger")
    if not isinstance(recorded_result_event_identity, str) or not recorded_result_event_identity:
        raise TypeError("a Yield-edge read requires one event occurrence")
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
    responsible_act_evidence_required = isinstance(
        responsible_act_evidence_event_identity, str
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

    result_occurrence = recorded_result_event.payload.get(
        recorded_result_occurrence_coordinate
    )
    evidence_dimensions = result_evidence.payload.get("dimensions", {})
    same_occurrence = result_occurrence == evidence_dimensions.get(
        "act_occurrence_identity"
    )
    if responsible_act_evidence is not None:
        same_occurrence = same_occurrence and result_occurrence == (
            responsible_act_evidence.payload.get(
                responsible_act_occurrence_coordinate
            )
        )
    elif responsible_act_evidence_required:
        same_occurrence = False

    evidence_is_carried = (
        recorded_result_event.payload.get("yield_evidence_identity") == result_evidence.identity
        and result_evidence.kind == YIELD_EVIDENCE_KIND
    )
    result = result_evidence.payload.get("result")
    yield_coordinates = result_evidence.payload.get("yield_coordinates")
    recorded_result_coordinates = result_evidence.payload.get("recorded_result_coordinates")
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
            value = recorded_result_event.payload
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
    evidence_is_carried = evidence_is_carried and exact_carried_result
    if responsible_act_evidence is not None:
        evidence_is_carried = evidence_is_carried and (
            recorded_result_event.payload.get("responsible_act_evidence_identity")
            == responsible_act_evidence.identity
        )
    elif responsible_act_evidence_required:
        evidence_is_carried = False

    return {
        "exact_relation": evidence_is_carried,
        "occurrence_witness": same_occurrence,
        "intact_evidence": (
            ledger.integrity_of(result_evidence.identity) != CORRUPTED
            and (
                (
                    responsible_act_evidence is None
                    and not responsible_act_evidence_required
                )
                or (
                    responsible_act_evidence is not None
                    and ledger.integrity_of(responsible_act_evidence.identity) != CORRUPTED
                )
            )
        ),
    }


def _record_yield_evidence(
    ledger: EventLedger,
    *,
    locality_identity: str | None,
    exact_act: str,
    act_occurrence_identity: str,
    result_kind: str,
    result_identity: str,
    result_content: dict[str, Any],
    responsibility: str,
    live_boundary: str,
    responsible_boundary: str = "unestablished",
    recorded_result_coordinates: dict[str, tuple[str, ...]] | None = None,
) -> Event:
    """Preserve Evidence from inside an act for its already-fixed result."""

    if not isinstance(act_occurrence_identity, str) or not act_occurrence_identity:
        raise ValueError("Yield Evidence requires one exact Act occurrence identity")
    if live_boundary not in YIELD_LIVE_BOUNDARIES:
        raise ValueError("Yield Evidence requires one declared live boundary")
    if type(result_content) is not dict:
        raise TypeError("Yield Evidence requires one exact yielded result")
    declared_recorded_result_coordinates = (
        {coordinate: (coordinate,) for coordinate in result_content}
        if recorded_result_coordinates is None
        else recorded_result_coordinates
    )
    if type(declared_recorded_result_coordinates) is not dict or set(
        declared_recorded_result_coordinates
    ) != set(result_content):
        raise ValueError(
            "Yield Evidence requires one carried coordinate for every yielded coordinate"
        )
    preserved_recorded_result_coordinates = {}
    for coordinate, carried_at in declared_recorded_result_coordinates.items():
        if type(coordinate) is not str or not coordinate:
            raise TypeError("a yielded coordinate must be one exact representation")
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
            "dimensions": {
                "identity": (
                    f"yield-evidence:{act_occurrence_identity}:{result_identity}"
                ),
                "content": (
                    f"evidence that {exact_act} yielded this exact "
                    f"{result_kind} at its exact Act boundary"
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
                    "establishes the exact occurrence-to-result edge at this "
                    "Act boundary; establishes no responsibility, "
                    "authorization, or successful return from "
                    "an enclosing call"
                ),
                "occurrence_preservation": (
                    "Evidence concerning the exact occurrence-to-result edge, "
                    "durably recorded; not the edge or Act occurrence by identity"
                ),
            },
            "yield_coordinates": sorted(result_content),
            "result": deepcopy(result_content),
            "recorded_result_coordinates": preserved_recorded_result_coordinates,
            "result_kind": result_kind,
            "live_boundary": live_boundary,
        },
        locality_identity=locality_identity,
    )
