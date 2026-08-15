"""Deterministic Locality Standing read over preserved ingest events."""

from __future__ import annotations


from bisect import bisect_left
from typing import Any, Iterable

from seed_runtime.events import EventLedger
from seed_runtime.event import Event
from seed_runtime.material_ingest import MATERIAL_INGEST_OCCURRED_KIND

# The writer of these occurrences declares their kinds. A reader declaring its
# own copy would be a second contract, free to drift from the first.
from seed_runtime.operator_representation import (
    REPRESENTATION_RECORDED_KIND as _REPRESENTATION_RECORDED_KIND,
    REPRESENTATION_ACT_EVIDENCE_KIND as _REPRESENTATION_ACT_EVIDENCE_KIND,
    REPRESENTATION_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_ATTEMPT_KIND as _REPRESENTATION_EMISSION_ATTEMPT_KIND,
    REPRESENTATION_EMITTED_KIND as _REPRESENTATION_EMITTED_KIND,
    REPRESENTATION_EMISSION_OUTCOME_KIND as _REPRESENTATION_EMISSION_OUTCOME_KIND,
    REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND as _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
    REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND as _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
)

_SUBJECT_BY_KIND = {
    MATERIAL_INGEST_OCCURRED_KIND: "ingest_occurrence",
}
_SUPPORTED_KINDS = {
    *_SUBJECT_BY_KIND,
    _REPRESENTATION_RECORDED_KIND,
    _REPRESENTATION_ACT_EVIDENCE_KIND,
    _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
    _REPRESENTATION_EMISSION_ATTEMPT_KIND,
    _REPRESENTATION_EMITTED_KIND,
    _REPRESENTATION_EMISSION_OUTCOME_KIND,
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
    ledger: EventLedger, *, locality_id: str
) -> dict[str, Any]:
    """Project bounded Locality-local Standing by replaying the whole Locality.

    Equivalent to advancing from no prior Standing over every recorded event.
    `#2376` established that advancing from a prior Standing over only the
    occurrences after its boundary yields the same result, so a caller that
    already holds its Standing and knows what it just recorded should use
    :func:`advance_operator_locality_standing` instead of replaying.
    """

    return advance_operator_locality_standing(
        ledger.list_locality(locality_id),
        locality_id=locality_id,
    )


def advance_operator_locality_standing(
    events: Iterable[Event],
    *,
    locality_id: str,
    prior: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Advance bounded Locality-local Standing over an exact sequence of events.

    With no `prior`, this reads from nothing and `events` must be the whole
    Locality. With a `prior`, `events` must be exactly the applicable
    occurrences recorded after `prior["as_of_event_id"]`, in append order; the
    prefix it already input is not revisited.

    The caller supplies those occurrences. Nothing here searches a ledger for
    them, because a responsible act that just recorded an occurrence already
    holds it.

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

    Accepts as input only Ingest and ``operator.representation.*``
    events stamped with this exact Locality, in append order. The result is fully recomputable
    from the ledger and is not itself recorded: it exposes only standings,
    limits, and Unknowns the Locality's events already carry.  An empty
    coordinate is absence of record, not negative standing and not Unknown.
    Represented relation candidates are never yielded here; each preserved ingest keeps
    the authority its own event recorded.
    """
    scope = f"locality:{locality_id}"
    ingests: dict[str, dict[str, Any]] = {}
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
    as_of_event_id: str | None = None
    event_count = 0

    if prior is not None:
        # Every accumulator the live event kinds read, taken over from the
        # Standing that already input the earlier occurrences.  Not copied:
        # see the shared-accumulator note above.
        ingests = prior["ingests"]
        ingest_occurrences = prior["ingest_occurrences"]
        representations = prior["representations"]
        known_loss = prior["known_loss"]
        unknowns = prior["unknowns"]
        conflicts = prior["conflicts"]
        as_of_event_id = prior["as_of_event_id"]
        event_count = prior["event_count"]

    for event in events:
        if event.locality_id != locality_id:
            continue
        if not (
            event.kind == MATERIAL_INGEST_OCCURRED_KIND
            or event.kind.startswith("operator.representation.")
        ):
            continue
        if event.kind not in _SUPPORTED_KINDS:
            raise ValueError(f"unsupported operator-ingest event: {event.kind}")
        event_count += 1
        as_of_event_id = event.id
        for key, collected in (
            ("known_loss", known_loss),
            ("unknowns", unknowns),
            ("conflicts", conflicts),
        ):
            for value in event.payload.get(key, ()):
                _record_distinct(collected, value)
        if event.kind in {
            _REPRESENTATION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_LOCALITY_EVIDENCE_KIND,
        }:
            continue
        if event.kind == _REPRESENTATION_RECORDED_KIND:
            payload = event.payload
            if payload["representation_reference"] in representations:
                raise ValueError(
                    "duplicate representation reference: "
                    f"{payload['representation_reference']}"
                )
            representations[payload["representation_reference"]] = {
                "representation_id": payload["representation_reference"],
                "representation_event_id": event.id,
                "emission_attempt_event_id": None,
                "emission_attempt_locality_evidence_id": None,
                "emission_outcome_event_id": None,
                "emitted_event_id": None,
                "representation_result": payload["representation_result"],
                "emission_text": payload["emission_text"],
                "alternative_material": payload["alternative_material"],
                "coordinate_binding": payload["coordinate_binding"],
                "locality_standing_as_of_event_id": payload[
                    "locality_standing_as_of_event_id"
                ],
                "scope": payload["dimensions"]["scope_locality"],
                "provenance": payload["dimensions"]["source_provenance"],
                "known_loss": payload["known_loss"],
                "unknowns": payload["unknowns"],
                "conflicts": payload["conflicts"],
            }
            continue
        if event.kind in {
            _REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
            _REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
        }:
            # These Events preserve exact edge Evidence. They do not add or
            # revise Locality Standing by identity.
            continue
        if event.kind == _REPRESENTATION_EMISSION_ATTEMPT_KIND:
            representation_reference = event.payload["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission attempt without recorded representation event: "
                    f"{representation_reference}"
                )
            representations[representation_reference]["emission_attempt_event_id"] = event.id
            continue
        if event.kind == _REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND:
            representation_reference = event.payload["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "emission-attempt Locality Evidence without recorded Representation: "
                    f"{representation_reference}"
                )
            if event.payload["attempt_event_id"] != representations[
                representation_reference
            ]["emission_attempt_event_id"]:
                raise ValueError(
                    "emission-attempt Locality Evidence names another attempt"
                )
            representations[representation_reference][
                "emission_attempt_locality_evidence_id"
            ] = event.id
            continue
        if event.kind == _REPRESENTATION_EMITTED_KIND:
            representation_reference = event.payload["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission without recorded representation event: "
                    f"{representation_reference}"
                )
            if (
                event.payload["representation_event_id"]
                != representations[representation_reference]["representation_event_id"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded "
                    "representation Act occurrence"
                )
            if (
                event.payload["attempt_reference"]
                != representations[representation_reference]["emission_attempt_event_id"]
            ):
                raise ValueError(
                    "representation emission does not name its recorded attempt"
                )
            representations[representation_reference]["emitted_event_id"] = event.id
            representations[representation_reference]["emission_outcome_event_id"] = event.id
            continue
        if event.kind == _REPRESENTATION_EMISSION_OUTCOME_KIND:
            representation_reference = event.payload["representation_reference"]
            if representation_reference not in representations:
                raise ValueError(
                    "representation emission outcome without recorded representation event: "
                    f"{representation_reference}"
                )
            if (
                event.payload["attempt_reference"]
                != representations[representation_reference]["emission_attempt_event_id"]
            ):
                raise ValueError(
                    "representation emission outcome does not name its recorded attempt"
                )
            representations[representation_reference]["emission_outcome_event_id"] = event.id
            continue
        ingest_reference = event.payload["dimensions"]["identity"]
        ingest = ingests.setdefault(
            ingest_reference,
            {"event_ids": [], "ingest_occurrence": None},
        )
        ingest["event_ids"].append(event.id)
        occurrence = {
            "ingest_reference": ingest_reference,
            "subject_reference": ingest_reference,
            "standing": "preserved",
            "authority": event.payload["dimensions"]["authority"],
            "evidence_event_id": event.id,
            "source_role": event.payload["source_role"],
            "content": event.payload["dimensions"]["content"],
        }
        if isinstance(event.payload.get("represented_material"), str):
            occurrence["represented_material"] = event.payload[
                "represented_material"
            ]
        ingest["ingest_occurrence"] = occurrence
        ingest_occurrences.append(occurrence)

    return {
        "locality_id": locality_id,
        "as_of_event_id": as_of_event_id,
        "event_count": event_count,
        "ingests": ingests,
        "ingest_occurrences": ingest_occurrences,
        "representations": representations,
        # No "current" Representation is projected.  Emission order is
        # addressable from `representations`, which preserves representation Act and
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
