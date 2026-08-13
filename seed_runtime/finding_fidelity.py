"""A bounded comparison of a recorded finding against the act that produced it.

`01.External.D` grants this and states its conditions: a Fidelity finding is
produced only by a bounded comparison bringing constitutional grammar, a
bounded expectation, and an implementation witness under a declared seam or
scope. Within that scope it may find the witness faithful, an unfaithful
boundary crossing, mixed, or Unknown, and it must not become global
certification, a completion declaration, an owner map, a score, a registry, a
public diagnostic, or correction authority.

**What this compares.** One recorded measurement finding against the production
evidence that finding names. `#2517` established that relation: a measuring act
preserves evidence of what it produced, and the result it returns carries the
reference. So the expectation is exact and local — *the recorded result is the
result its production evidence concerns* — and the witness is the recorded
event itself.

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

from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_PRODUCED_KIND,
    MEASUREMENT_RECORDED_KIND,
    RESPONSIBILITY_UNRECOVERED,
)

FIDELITY_FINDING_KIND = "operator.fidelity.finding_recorded"

FAITHFUL_WITHIN_SCOPE = "faithful within scope"
UNFAITHFUL_CROSSING = "unfaithful boundary crossing"
FIDELITY_UNKNOWN = "Unknown"

# The four crossings `01.External.D` names. A comparison reports which it
# observed, or that it observed none, rather than scoring the witness.
ERASURE = "erasure"
INVENTION = "invention"
MUTATION = "mutation"
RELOCATION_OF_AUTHORITY = "relocation of authority"


class FindingFidelityError(ValueError):
    """A fidelity comparison cannot be performed as declared."""


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
    observed: list[str] = []
    named = recorded.payload.get("production_evidence_id")
    evidence: Event | None = None
    if named is None:
        # The recorded finding claims a measurement produced it -- its
        # provenance and responsibility coordinates say so -- while naming no
        # evidence that one did.
        observed.append(INVENTION)
    else:
        evidence = ledger.get(named)
        if evidence is None or evidence.kind != MEASUREMENT_PRODUCED_KIND:
            observed.append(INVENTION)
        else:
            from seed_runtime.preserved_material_measurement import (
                _recorded_production_commitment,
            )

            if evidence.payload["production_commitment"] != (
                _recorded_production_commitment(recorded)
            ):
                observed.append(MUTATION)
    standing = FAITHFUL_WITHIN_SCOPE if not observed else UNFAITHFUL_CROSSING
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
                "authority_warrant": (
                    "this comparison within this scope only; no certification, "
                    "completion, owner map, score, or correction authority"
                ),
                "scope_locality": (
                    f"workspace:{recorded.workspace_id};"
                    f"session:{recorded.session_id}"
                ),
                "occurrence_preservation": "fidelity comparison durably recorded",
            },
            "constitutional_subject": (
                "the relation between a recorded finding and the act that "
                "produced it"
            ),
            "bounded_expectation": (
                "the recorded finding names preserved production evidence, and "
                "that evidence concerns this exact recorded content"
            ),
            "implementation_witness": event_id,
            "production_evidence": named,
            "observed_crossings": observed,
            "unknowns": [
                "whether the finding is faithful in any respect this "
                "comparison did not bring under its scope",
            ],
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
