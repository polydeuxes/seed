"""A bounded comparison of a recorded finding and its production evidence.

`01.External.D` grants this and states its conditions: a Fidelity finding is
produced only by a bounded comparison bringing constitutional grammar, a
bounded expectation, and an implementation witness under a declared seam or
scope. Within that scope it may find the witness faithful, an unfaithful
boundary crossing, mixed, or Unknown, and it must not become global
certification, a completion declaration, an owner map, a score, a registry, a
public diagnostic, or correction authority.

**What this compares.** One recorded measurement finding and the production
evidence that finding names. `#2517` established that represented relation: a
measuring act preserves evidence of what it produced, and the result carries
the reference. The evidence is not the producing occurrence by identity. The
expectation is exact and local — *the recorded result is the result its
production evidence concerns* — and the witness is the recorded event itself.

**What it does not do.** It revises nothing. `01.Uptake.A` holds that evidence
becoming available "does not by itself change any consumer assertion, standing,
confidence, reliance, or current result", and that an upstream producer owns its
production and availability testimony, "not any consumer's applicability,
admission, Uptake, reliance, or downstream revision". A finding found unfaithful
here keeps whatever standing it had; what changes is that this comparison's
result exists and may be consumed.

**It does not walk anything.** A fidelity finding concerning one recorded
finding is available to whatever consumes it, and each later act determines its
own applicability for its own inputs — `01.Standing.E.1`. Walking the support
basis and premise edges and revising what is found there would be that
determination made centrally, for consumers that never made it. The edges are
recorded and a later responsible act may follow them; this act does not.
"""

from __future__ import annotations

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_PRODUCED_KIND,
    MEASUREMENT_RECORDED_KIND,
    PreservedMaterialMeasurementError,
    RESPONSIBILITY_UNRECOVERED,
)

FIDELITY_FINDING_KIND = "operator.fidelity.finding_recorded"

FAITHFUL_WITHIN_SCOPE = "faithful within scope"
UNFAITHFUL_CROSSING = "unfaithful boundary crossing"
FIDELITY_UNKNOWN = "Unknown"

ERASURE = "erasure"
INVENTION = "invention"


class FindingFidelityError(ValueError):
    """A fidelity comparison cannot be performed as declared."""


def _provenance(event: Event, integrity: str) -> dict[str, object]:
    """The exact occurrence coordinates available to this comparison."""

    return {
        "event_id": event.id,
        "event_kind": event.kind,
        "workspace_id": event.workspace_id,
        "session_id": event.session_id,
        "integrity": integrity,
    }


def _crossing(kind: str, observation: str) -> dict[str, str]:
    return {"kind": kind, "observation": observation}


def compare_recorded_finding(ledger: EventLedger, event_id: str) -> Event:
    """Compare one recorded finding against the production evidence it names.

    The bounded expectation, stated so it can be wrong: a recorded measurement
    finding names production evidence, that evidence is preserved, and it
    concerns this exact recorded content.
    """

    recorded = ledger.get(event_id)
    if recorded is None or recorded.kind != MEASUREMENT_RECORDED_KIND:
        raise FindingFidelityError(
            f"{event_id} is not a recorded measurement finding, and this "
            "comparison compares one against its production evidence"
        )
    recorded_integrity = ledger.integrity_of(event_id)
    if recorded_integrity == CORRUPTED:
        raise FindingFidelityError(
            f"{event_id} is corrupted, so it cannot serve as this comparison's "
            "implementation witness"
        )

    observed: list[dict[str, str]] = []
    conflicts: list[str] = []
    unknowns = [
        "whether the finding is faithful in any respect this comparison did "
        "not bring under its scope"
    ]
    unresolved = False
    named = recorded.payload.get("production_evidence_id")
    evidence: Event | None = None
    evidence_integrity: str | None = None
    if named is None:
        observed.append(
            _crossing(
                ERASURE,
                "the recorded finding does not preserve the required relation "
                "to production evidence",
            )
        )
    elif not isinstance(named, str) or not named:
        observed.append(
            _crossing(
                INVENTION,
                "the recorded finding supplies something other than an exact "
                "production-evidence occurrence identity",
            )
        )
    else:
        evidence = ledger.get(named)
        if evidence is None:
            unresolved = True
            unknowns.append(
                "the named production evidence is unavailable; absence does "
                "not establish that its occurrence or the production did not "
                "exist"
            )
        else:
            evidence_integrity = ledger.integrity_of(named)
            if evidence_integrity == CORRUPTED:
                unresolved = True
                conflicts.append(
                    "the named production-evidence occurrence is corrupted"
                )
            elif evidence.kind != MEASUREMENT_PRODUCED_KIND:
                observed.append(
                    _crossing(
                        INVENTION,
                        "the named occurrence is supplied with production-"
                        "evidence standing that its recorded kind does not carry",
                    )
                )
            else:
                commitment = evidence.payload.get("production_commitment")
                coordinates = evidence.payload.get("production_coordinates")
                if commitment is None or coordinates is None:
                    observed.append(
                        _crossing(
                            ERASURE,
                            "the production evidence omits the commitment or "
                            "coordinate boundary required to compare it",
                        )
                    )
                elif (
                    not isinstance(commitment, str)
                    or not isinstance(coordinates, list)
                    or not all(isinstance(item, str) for item in coordinates)
                    or len(set(coordinates)) != len(coordinates)
                ):
                    unresolved = True
                    unknowns.append(
                        "the production evidence does not carry an interpretable "
                        "commitment and exact coordinate boundary"
                    )
                else:
                    from seed_runtime.preserved_material_measurement import (
                        _recorded_production_commitment,
                    )

                    try:
                        recorded_commitment = _recorded_production_commitment(
                            recorded, tuple(coordinates)
                        )
                    except PreservedMaterialMeasurementError as exc:
                        observed.append(_crossing(ERASURE, str(exc)))
                    else:
                        if commitment != recorded_commitment:
                            # The mismatch proves the bounded expectation failed.
                            # It does not prove which Fidelity crossing caused it:
                            # altered content and a misplaced evidence reference
                            # produce the same witness here.
                            observed.append(
                                _crossing(
                                    FIDELITY_UNKNOWN,
                                    "the named production evidence does not "
                                    "concern this exact recorded content",
                                )
                            )
    if unresolved:
        standing = FIDELITY_UNKNOWN
    elif observed:
        standing = UNFAITHFUL_CROSSING
    else:
        standing = FAITHFUL_WITHIN_SCOPE

    authority_boundary = (
        "this comparison within this exact finding-to-production-evidence "
        "scope only; no certification, completion, owner map, score, or "
        "correction authority"
    )
    return ledger.append(
        FIDELITY_FINDING_KIND,
        recorded.workspace_id,
        {
            "dimensions": {
                "identity": f"fidelity:{event_id}",
                "content": (
                    "a recorded measurement finding compared against the "
                    "production evidence it names"
                ),
                "standing": standing,
                "producing_act": "bounded fidelity comparison",
                "producer": RESPONSIBILITY_UNRECOVERED,
                "responsibility": RESPONSIBILITY_UNRECOVERED,
                "authority_warrant": authority_boundary,
                "scope_workspace": recorded.workspace_id,
                "scope_locality": (
                    f"session:{recorded.session_id}"
                    if recorded.session_id is not None
                    else None
                ),
                "occurrence_preservation": "fidelity comparison durably recorded",
            },
            "constitutional_subject": (
                "the recorded finding's represented relation to the production "
                "evidence it names"
            ),
            "bounded_expectation": (
                "the recorded finding names preserved production evidence, and "
                "that evidence concerns this exact recorded content"
            ),
            "implementation_witness": event_id,
            "production_evidence": named,
            "evidence_and_provenance": {
                "recorded_finding": _provenance(recorded, recorded_integrity),
                "production_evidence": (
                    _provenance(evidence, evidence_integrity)
                    if evidence is not None and evidence_integrity is not None
                    else None
                ),
            },
            "authority_boundary": authority_boundary,
            "preserved_invariants": [
                "the comparison is limited to one recorded finding and the "
                "production evidence it names",
                "content equality alone does not supply a production relation",
                "the comparison does not revise its witness or traverse its "
                "support and premise relations",
            ],
            "observed_crossings": observed,
            "conflicts": conflicts,
            "unknowns": unknowns,
            "lawful_stopping_point": (
                "produce this Fidelity finding concerning this exact represented "
                "relation and stop; do not traverse lineage or determine "
                "downstream applicability, admission, Uptake, reliance, or "
                "revision"
            ),
            "revises": [],
            "forbidden_inferences": [
                "This revises nothing (01.Uptake.A); availability is not "
                "revision.",
                "This establishes no responsibility and names no owner.",
                "Faithful within this scope is not faithful generally.",
                "A crossing observed here is not a crossing observed of "
                "whatever this finding stood on.",
            ],
        },
        session_id=recorded.session_id,
    )
