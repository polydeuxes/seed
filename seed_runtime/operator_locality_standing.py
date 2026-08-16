"""Deterministic Locality Standing read over preserved ingest events."""

from __future__ import annotations


from bisect import bisect_left
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND
from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    assertions_of_recorded_byte_measurement,
)
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_RECORDED_KIND,
    get_recorded_occurrence_position_measurement,
)

# The writer of these occurrences declares their kinds. A reader declaring its
# own copy would be a second contract, free to drift from the first.
from seed_runtime.operator_representation import (
    REPRESENTATION_RECORDED_KIND as _REPRESENTATION_RECORDED_KIND,
    REPRESENTATION_ACT_EVIDENCE_KIND as _REPRESENTATION_ACT_EVIDENCE_KIND,
    REPRESENTATION_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_ATTEMPT_KIND as _REPRESENTATION_EMISSION_ATTEMPT_KIND,
    REPRESENTATION_EMITTED_KIND as _REPRESENTATION_EMITTED_KIND,
    REPRESENTATION_EMISSION_FAILURE_KIND as _REPRESENTATION_EMISSION_FAILURE_KIND,
    REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND as _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
)

_SUBJECT_BY_KIND = {
    MATERIAL_INGEST_OCCURRED_KIND: "ingest_occurrence",
}
_MEASUREMENT_ACT_EVIDENCE_KINDS = {
    BYTE_MEASUREMENT_RESPONSIBLE_ACT_EVIDENCE_KIND,
    OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
}
_MEASUREMENT_RECORDED_KINDS = {
    BYTE_MEASUREMENT_RECORDED_KIND,
    OCCURRENCE_POSITION_RECORDED_KIND,
}
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    *_MEASUREMENT_ACT_EVIDENCE_KINDS,
    *_MEASUREMENT_RECORDED_KINDS,
    _REPRESENTATION_RECORDED_KIND,
    _REPRESENTATION_ACT_EVIDENCE_KIND,
    _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_ATTEMPT_KIND,
    _REPRESENTATION_EMITTED_KIND,
    _REPRESENTATION_EMISSION_FAILURE_KIND,
    _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
}


def _record_distinct(collected: list[str], value: str) -> None:
    """Keep one sorted, distinct sequence in place.

    The returned coordinate is a sorted list of distinct strings, as it has
    always been.  Adding a value already present does nothing, so an advance
    that yields no new value costs nothing.
    """

    index = bisect_left(collected, value)
    if index == len(collected) or collected[index] != value:
        collected.insert(index, value)


def read_operator_locality_standing(
    ledger: EventLedger, *, locality_identity: str
) -> dict[str, Any]:
    """Project bounded Locality-local Standing by replaying the whole Locality.

    Equivalent to advancing from no prior Standing over every recorded event.
    `#2376` established that advancing from a prior Standing over only the
    occurrences after its boundary yields the same result, so a caller that
    already holds its Standing and knows what it just recorded should use
    :func:`advance_operator_locality_standing` instead of replaying.
    """

    return advance_operator_locality_standing(
        ledger,
        (
            event.identity
            for event in ledger.list_locality(locality_identity)
        ),
        locality_identity=locality_identity,
    )


def advance_operator_locality_standing(
    ledger: EventLedger,
    event_identities: Iterable[str],
    *,
    locality_identity: str,
    prior: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Advance bounded Locality-local Standing over exact ledger occurrences.

    With no `prior`, this reads the supplied identities from an empty Standing.
    With a `prior`, it begins from the accumulators already established there.
    The ledger verifies each supplied identity's Locality and their append order.
    The caller supplies the bounded identities; this function does not infer an
    omitted occurrence.

    The caller supplies exact identities from the responsible Act that recorded
    them. The ledger resolves those identities rather than accepting supplied
    occurrence representations.

    Every accumulator the live event kinds read is seeded from `prior`, and the
    per-event branches and refusals below are the same ones replay uses. Those
    refusals consult accumulated Standing rather than the ledger, which is why
    seeding preserves them (`#2376`).

    **The advance has as input `prior`.** Its accumulators are taken over rather
    than copied, and the returned Standing shares them. A caller that needs the
    earlier Standing to stay as it was must project it again; there is no
    snapshot here.

    That is not defensive weakness, it is the point. Standing grows with the
    Locality, so copying it per advance would cost the Locality event count every
    time and reinstate the quadratic this replaced. The console holds one
    Standing, hands it forward, and keeps no earlier one.

    The result is fully recomputable
    from the ledger and is not itself recorded: it returns only standings,
    limits, and Unknowns the Locality's events already carry.  An empty
    coordinate is absence of record, not negative standing and not Unknown.
    No Yield is established for represented relation candidates here; each preserved ingest keeps
    the authority its own event recorded.
    """
    events = ledger.occurrences_in_append_order(
        event_identities,
        locality_identity=locality_identity,
    )
    scope = f"locality:{locality_identity}"
    ingest_occurrences: list[dict[str, Any]] = []
    representations: dict[str, dict[str, Any]] = {}
    # Kept sorted and distinct in place rather than as a set sorted on return.
    # A set would have to be rebuilt from the prior list and re-sorted on every
    # advance, which costs the accumulated size each time.  These coordinates
    # do not grow on the five live kinds today, but acquisition would make them
    # grow, and the prior-transfer rule has to hold for every accumulator that
    # can.
    known_loss: list[str] = []
    unknowns: list[str] = []
    conflicts: list[str] = []
    as_of_event_identity: str | None = None
    event_count = 0

    if prior is not None:
        # Every accumulator the live event kinds read, taken over from the
        # Standing that already input the earlier occurrences.  Not copied:
        # see the shared-accumulator note above.
        ingest_occurrences = prior["ingest_occurrences"]
        representations = prior["representations"]
        known_loss = prior["known_loss"]
        unknowns = prior["unknowns"]
        conflicts = prior["conflicts"]
        as_of_event_identity = prior["as_of_event_identity"]
        event_count = prior["event_count"]

    for event in events:
        if event.locality_identity != locality_identity:
            continue
        if not (
            event.kind == MATERIAL_INGEST_OCCURRED_KIND
            or event.kind.startswith("operator.representation.")
            or event.kind in _MEASUREMENT_ACT_EVIDENCE_KINDS
            or event.kind in _MEASUREMENT_RECORDED_KINDS
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-ingest event: {event.kind}")
        event_count += 1
        as_of_event_identity = event.identity
        for key, collected in (
            ("known_loss", known_loss),
            ("unknowns", unknowns),
            ("conflicts", conflicts),
        ):
            for value in event.material.get(key, ()):
                _record_distinct(collected, value)
        if event.kind in _MEASUREMENT_ACT_EVIDENCE_KINDS:
            continue
        if event.kind == BYTE_MEASUREMENT_RECORDED_KIND:
            assertions_of_recorded_byte_measurement(ledger, event.identity)
            continue
        if event.kind == OCCURRENCE_POSITION_RECORDED_KIND:
            get_recorded_occurrence_position_measurement(ledger, event.identity)
            continue
        if event.kind in {
            _REPRESENTATION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
        }:
            continue
        if event.kind == _REPRESENTATION_RECORDED_KIND:
            material = event.material
            if material["result_identity"] in representations:
                raise ValueError(
                    "duplicate Representation identity: "
                    f"{material['result_identity']}"
                )
            representations[material["result_identity"]] = {
                "representation_identity": material["result_identity"],
                "representation_event_identity": event.identity,
                "emission_attempt_event_identity": None,
                "emission_attempt_locality_evidence_identity": None,
                "emission_failure_event_identity": None,
                "emitted_event_identity": None,
                "representation_result": material["representation_result"],
                "emission_text": material["emission_text"],
                "alternative_material": material["alternative_material"],
                "coordinate_binding": material["coordinate_binding"],
                "locality_standing_as_of_event_identity": material[
                    "locality_standing_as_of_event_identity"
                ],
                "scope": material["dimensions"]["scope_locality"],
                "provenance": material["dimensions"]["source_provenance"],
                "known_loss": material["known_loss"],
                "unknowns": material["unknowns"],
                "conflicts": material["conflicts"],
            }
            continue
        if event.kind in {
            _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
        }:
            # These Events preserve exact relation Evidence. They do not add or
            # revise Locality Standing by identity.
            continue
        if event.kind == _REPRESENTATION_EMISSION_ATTEMPT_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission attempt without recorded representation event: "
                    f"{representation_reference}"
                )
            representations[representation_reference]["emission_attempt_event_identity"] = event.identity
            continue
        if event.kind == _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "emission-attempt Locality Evidence without recorded Representation: "
                    f"{representation_reference}"
                )
            if event.material["attempt_event_identity"] != representations[
                representation_reference
            ]["emission_attempt_event_identity"]:
                raise ValueError(
                    "emission-attempt Locality Evidence names another attempt"
                )
            representations[representation_reference][
                "emission_attempt_locality_evidence_identity"
            ] = event.identity
            continue
        if event.kind == _REPRESENTATION_EMITTED_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission without recorded representation event: "
                    f"{representation_reference}"
                )
            if (
                event.material["representation_event_identity"]
                != representations[representation_reference]["representation_event_identity"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded "
                    "representation Act occurrence"
                )
            if (
                event.material["attempt_reference"]
                != representations[representation_reference]["emission_attempt_event_identity"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded attempt"
                )
            representations[representation_reference]["emitted_event_identity"] = event.identity
            continue
        if event.kind == _REPRESENTATION_EMISSION_FAILURE_KIND:
            representation_reference = event.material["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission failure without recorded representation event: "
                    f"{representation_reference}"
                )
            if (
                event.material["attempt_reference"]
                != representations[representation_reference]["emission_attempt_event_identity"]
            ):
                raise ValueError(
                    "representation emission failure does not name its recorded attempt"
                )
            representations[representation_reference]["emission_failure_event_identity"] = event.identity
            continue
        ingest_reference = event.material["dimensions"]["identity"]
        occurrence = {
            "subject_reference": ingest_reference,
            "standing": "preserved",
            "authority": event.material["dimensions"]["authority"],
            "evidence_event_identity": event.identity,
            "source_role": event.material["source_role"],
        }
        if isinstance(event.material.get("represented_material"), str):
            occurrence["represented_material"] = event.material[
                "represented_material"
            ]
        ingest_occurrences.append(occurrence)

    return {
        "locality_identity": locality_identity,
        "as_of_event_identity": as_of_event_identity,
        "event_count": event_count,
        "ingest_occurrences": ingest_occurrences,
        "representations": representations,
        # No "current" Representation is projected.  Emission order is
        # preserved in `representations`, which retains representation Act and
        # emission occurrences in append order; naming one of them current
        # would assert present relevance that no occurrence establishes.
        # Exactly the relation standings recorded by Locality events.  No
        # current event kind records one, so this stays empty until a
        # responsible occurrence does; emptiness is absence of record only.
        "recorded_relation_standings": [],
        "known_loss": known_loss,
        "unknowns": unknowns,
        "conflicts": conflicts,
    }
