"""A bounded Compare of a recorded finding and its Yield Evidence.

This Compare concerns one recorded finding and the Yield Evidence it names.
Within that boundary it may find agreement, a coordinate difference, or
Unknown. It does not certify this Seed, declare completion, map responsible
boundaries, score results, expose a public diagnostic, or grant correction
Authority.

**What this compares.** One recorded recurrence Measurement finding and the
Yield Evidence that finding names. `#2517` established that represented
relation for recurrence only: a measuring act preserves evidence of what it
yielded, and the result carries the reference. Positional Measurement has not
adopted that yield witness and is outside this comparator's scope. The
evidence is not the yielding occurrence by identity. The expectation is exact
and local — *the recorded result is the result its yield evidence
concerns* — and the witness is the recorded event itself.

**What it does not do.** It revises nothing. `06.Standing.B` establishes that
making an Assertion available at another locality does not revise its Standing,
establish Applicability, or require another Act. A coordinate difference here
keeps whatever Standing it had; this comparison establishes only its own result.

**It does not walk anything.** A Compare result concerning one recorded
finding is available to whatever Act has it participate, and each later act determines its
own applicability for its own inputs — `01.Standing.E.1`. Walking the support
support and premise edges and revising what is found there would be that
determination made centrally, for exact Acts that never made it. The edges are
recorded and a later responsible act may follow them; this act does not.
"""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.ids import new_id
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    PreservedMaterialMeasurementError,
    RECURRENCE_RESULT_KIND,
)
from seed_runtime.yield_evidence import (
    YIELD_EVIDENCE_KIND,
    _record_yield_evidence,
    read_yield_edge_requirements,
)

FINDING_YIELD_COMPARISON_KIND = "operator.measurement.finding_yield_compared"
FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND = (
    "operator.measurement.finding_yield_comparison_act_evidenced"
)
FINDING_YIELD_COMPARISON_RESULT_KIND = "recorded finding Yield comparison"
EVENT_KIND_RESPONSIBILITIES = {
    FINDING_YIELD_COMPARISON_KIND: "02.Acts.A",
    FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND: "02.Acts.A",
}
FINDING_YIELD_COMPARISON_RESPONSIBILITY = (
    "Compare one recorded finding with the exact Yield Evidence it names"
)

AGREES_WITH_YIELD_EVIDENCE = "agrees within compared coordinates"
DIFFERS_FROM_YIELD_EVIDENCE = "differs within compared coordinates"
COMPARISON_UNKNOWN = "Unknown"

ERASURE = "erasure"
UNSUPPORTED_COORDINATE = "unsupported coordinate"

COMPARISON_RESULT_COORDINATES = frozenset(
    {
        "downstream_act_id",
        "act_occurrence_id",
        "dimensions",
        "constitutional_subject",
        "compared_relation",
        "recorded_finding_reference",
        "yield_evidence",
        "evidence_and_provenance",
        "authority_boundary",
        "preserved_invariants",
        "crossings",
        "conflicts",
        "unknowns",
        "lawful_stopping_point",
        "revises",
        "limits",
    }
)
COMPARISON_RECORDING_COORDINATES = frozenset(
    {
        "responsible_act_evidence_id",
        "yield_evidence_id",
        "occurrence_preservation",
    }
)
COMPARISON_OCCURRENCE_PRESERVATION = (
    "recorded finding Yield comparison durably recorded after its exact result was yielded"
)


class RecordedFindingYieldComparisonError(ValueError):
    """The recorded-finding Yield Compare cannot be performed as declared."""


@dataclass(frozen=True)
class RecordedFindingYieldComparison:
    """One exact Compare result carried by one recording occurrence."""

    recorded_occurrence_id: str
    yield_evidence_id: str
    source_finding_event_id: str
    standing: str

    @property
    def reference(self) -> dict[str, str]:
        """Return its exact recording-occurrence reference."""

        return {"recorded_occurrence_id": self.recorded_occurrence_id}


def get_recorded_finding_yield_comparison(
    ledger: EventLedger, event_id: str
) -> RecordedFindingYieldComparison | None:
    """Return an exact occurrence-bound Compare result when evidenced."""

    event = ledger.get(event_id)
    if event is None:
        return None
    if event.kind != FINDING_YIELD_COMPARISON_KIND:
        raise RecordedFindingYieldComparisonError(
            f"{event_id} is {event.kind}, not a recorded finding Yield comparison"
        )
    if ledger.integrity_of(event_id) == CORRUPTED:
        raise RecordedFindingYieldComparisonError(
            "a corrupted occurrence cannot expose a finding Yield comparison"
        )
    payload = event.payload
    if set(payload) != COMPARISON_RESULT_COORDINATES | COMPARISON_RECORDING_COORDINATES:
        raise RecordedFindingYieldComparisonError(
            f"{event_id} does not preserve the exact Compare result and "
            "recording coordinate surfaces"
        )
    if payload.get("occurrence_preservation") != COMPARISON_OCCURRENCE_PRESERVATION:
        raise RecordedFindingYieldComparisonError(
            f"{event_id} does not preserve the Compare recording occurrence"
        )
    evidence_id = payload.get("yield_evidence_id")
    if not isinstance(evidence_id, str) or not evidence_id:
        raise RecordedFindingYieldComparisonError(
            f"{event_id} names no exact yield Evidence occurrence"
        )
    evidence = ledger.get(evidence_id)
    if evidence is None or evidence.kind != YIELD_EVIDENCE_KIND:
        raise RecordedFindingYieldComparisonError(
            f"{evidence_id} is not preserved yield Evidence"
        )
    if ledger.integrity_of(evidence_id) == CORRUPTED:
        raise RecordedFindingYieldComparisonError(
            "corrupted Yield Evidence cannot expose a Compare result"
        )
    if (
        evidence.payload.get("result_kind")
        != FINDING_YIELD_COMPARISON_RESULT_KIND
        or evidence.payload.get("yield_coordinates")
        != sorted(COMPARISON_RESULT_COORDINATES)
        or evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != payload.get("act_occurrence_id")
    ):
        raise RecordedFindingYieldComparisonError(
            "the named yield Evidence does not describe the exact "
            "Compare result contract"
        )
    yielded = {name: payload[name] for name in COMPARISON_RESULT_COORDINATES}
    if evidence.payload.get("result") != yielded:
        raise RecordedFindingYieldComparisonError(
            "the named Yield Evidence concerns a different Compare result"
        )
    act_evidence_id = payload.get("responsible_act_evidence_id")
    if not isinstance(act_evidence_id, str) or not act_evidence_id:
        raise RecordedFindingYieldComparisonError(
            f"{event_id} names no exact responsible Act Evidence occurrence"
        )
    act_evidence = ledger.get(act_evidence_id)
    if (
        act_evidence is None
        or act_evidence.kind != FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND
    ):
        raise RecordedFindingYieldComparisonError(
            f"{act_evidence_id} is not responsible Act Evidence for this Compare"
        )
    if not all(
        read_yield_edge_requirements(
            ledger,
            recorded_result_event_id=event.id,
            result_evidence_event_id=evidence.id,
            responsible_act_evidence_event_id=act_evidence.id,
        ).values()
    ):
        raise RecordedFindingYieldComparisonError(
            "the Compare Event does not bind its exact Act and result Evidence"
        )
    dimensions = payload.get("dimensions")
    source_id = payload.get("recorded_finding_reference")
    standing = dimensions.get("standing") if isinstance(dimensions, dict) else None
    if (
        not isinstance(source_id, str)
        or not source_id
        or standing
        not in {
            AGREES_WITH_YIELD_EVIDENCE,
            DIFFERS_FROM_YIELD_EVIDENCE,
            COMPARISON_UNKNOWN,
        }
        or not isinstance(dimensions, dict)
        or dimensions.get("identity") != f"finding-yield-comparison:{source_id}"
        or dimensions.get("exact_act") != "bounded finding Yield Compare"
        or dimensions.get("responsibility")
        != FINDING_YIELD_COMPARISON_RESPONSIBILITY
        or dimensions.get("scope_locality")
        != (f"locality:{event.locality_id}" if event.locality_id is not None else None)
    ):
        raise RecordedFindingYieldComparisonError(
            f"{event_id} carries an incoherent Compare result shell"
        )
    return RecordedFindingYieldComparison(
        recorded_occurrence_id=event.id,
        yield_evidence_id=evidence.id,
        source_finding_event_id=source_id,
        standing=standing,
    )


def _provenance(event: Event, integrity: str) -> dict[str, object]:
    """The exact occurrence coordinates available to this comparison."""

    return {
        "event_id": event.id,
        "event_kind": event.kind,
        "locality_id": event.locality_id,
        "integrity": integrity,
    }


def _crossing(kind: str, material: str) -> dict[str, str]:
    return {"kind": kind, "material": material}


def compare_recorded_finding_yield(ledger: EventLedger, event_id: str) -> Event:
    """Compare one recorded recurrence finding and its Yield Evidence."""

    recorded = ledger.get(event_id)
    if recorded is None or recorded.kind != MEASUREMENT_RECORDED_KIND:
        raise RecordedFindingYieldComparisonError(
            f"{event_id} is not a recorded measurement finding, and this "
            "comparison compares one against its yield evidence"
        )
    if recorded.payload.get("measurement_distinction") != "recurrence":
        raise RecordedFindingYieldComparisonError(
            f"{event_id} is not a recorded recurrence Measurement finding; "
            "this comparison does not apply recurrence's yield-evidence "
            "expectation to an unmigrated Measurement representation"
        )
    recorded_integrity = ledger.integrity_of(event_id)
    if recorded_integrity == CORRUPTED:
        raise RecordedFindingYieldComparisonError(
            f"{event_id} is corrupted, so it cannot serve as this comparison's "
            "recorded finding"
        )

    crossings: list[dict[str, str]] = []
    conflicts: list[str] = []
    unknowns = [
        "whether the finding agrees with its Yield Evidence in any coordinate "
        "this Compare did not bring under its Scope"
    ]
    unresolved = False
    named = recorded.payload.get("yield_evidence_id")
    evidence: Event | None = None
    evidence_integrity: str | None = None
    if named is None:
        crossings.append(
            _crossing(
                ERASURE,
                "the recorded finding does not preserve the required relation "
                "to yield evidence",
            )
        )
    elif not isinstance(named, str) or not named:
        crossings.append(
            _crossing(
                UNSUPPORTED_COORDINATE,
                "the recorded finding supplies something other than an exact "
                "yield-evidence occurrence identity",
            )
        )
    else:
        evidence = ledger.get(named)
        if evidence is None:
            unresolved = True
            unknowns.append(
                "the named yield evidence is unavailable; absence does "
                "not establish that its occurrence or the yield did not "
                "exist"
            )
        else:
            evidence_integrity = ledger.integrity_of(named)
            if evidence_integrity == CORRUPTED:
                unresolved = True
                conflicts.append(
                    "the named yield-evidence occurrence is corrupted"
                )
            elif evidence.kind != YIELD_EVIDENCE_KIND:
                crossings.append(
                    _crossing(
                        UNSUPPORTED_COORDINATE,
                        "the named occurrence is represented as yield "
                        "evidence, but its recorded kind does not represent "
                        "yield evidence",
                    )
                )
            elif (
                evidence.payload.get("result_kind")
                != RECURRENCE_RESULT_KIND
            ):
                crossings.append(
                    _crossing(
                        UNSUPPORTED_COORDINATE,
                        "the named yield evidence concerns a different "
                        "kind of result",
                    )
                )
            else:
                result = evidence.payload.get("result")
                coordinates = evidence.payload.get("yield_coordinates")
                if result is None or coordinates is None:
                    crossings.append(
                        _crossing(
                            ERASURE,
                            "the yield evidence omits the result or "
                            "coordinate boundary required to compare it",
                        )
                    )
                elif (
                    not isinstance(result, dict)
                    or not isinstance(coordinates, list)
                    or not all(isinstance(item, str) for item in coordinates)
                    or len(set(coordinates)) != len(coordinates)
                ):
                    unresolved = True
                    unknowns.append(
                        "the yield evidence does not carry an exact result "
                        "and coordinate boundary"
                    )
                else:
                    from seed_runtime.preserved_material_measurement import (
                        _recorded_yield_result,
                    )

                    try:
                        recorded_result = _recorded_yield_result(
                            recorded, tuple(coordinates)
                        )
                    except PreservedMaterialMeasurementError:
                        crossings.append(
                            _crossing(
                                ERASURE,
                                "the recorded finding omits at least one exact "
                                "coordinate its Yield Evidence carries",
                            )
                        )
                    else:
                        if result != recorded_result:
                            # The mismatch proves the compared relation differs.
                            # It does not prove which coordinate caused it:
                            # altered content and a misplaced evidence reference
                            # yield the same witness here.
                            crossings.append(
                                _crossing(
                                    COMPARISON_UNKNOWN,
                                    "the named yield evidence does not "
                                    "concern this exact recorded content",
                                )
                            )
    if unresolved:
        standing = COMPARISON_UNKNOWN
    elif crossings:
        standing = DIFFERS_FROM_YIELD_EVIDENCE
    else:
        standing = AGREES_WITH_YIELD_EVIDENCE

    authority_boundary = (
        "this comparison within this exact finding-to-yield-evidence "
        "scope only; no certification, completion, responsible-boundary map, score, or "
        "correction authority"
    )
    downstream_act_id = new_id("finding_yield_comparison_act")
    act_occurrence_id = new_id("finding_yield_comparison_act_occurrence")
    result_payload = {
        "downstream_act_id": downstream_act_id,
        "act_occurrence_id": act_occurrence_id,
        "dimensions": {
                "identity": f"finding-yield-comparison:{event_id}",
                "content": (
                    "a recorded measurement finding compared against the "
                    "yield evidence it names"
                ),
                "standing": standing,
                "exact_act": "bounded finding Yield Compare",
                "responsibility": FINDING_YIELD_COMPARISON_RESPONSIBILITY,
                "authority": authority_boundary,
                "scope_locality": (
                    f"locality:{recorded.locality_id}"
                    if recorded.locality_id is not None
                    else None
                ),
            },
        "constitutional_subject": (
                "the recorded finding's represented relation to the yield "
                "evidence it names"
            ),
        "compared_relation": (
                "the recorded finding names preserved yield evidence, and "
                "that evidence concerns this exact recorded content"
            ),
        "recorded_finding_reference": event_id,
        "yield_evidence": named,
        "evidence_and_provenance": {
                "recorded_finding": _provenance(recorded, recorded_integrity),
                "yield_evidence": (
                    _provenance(evidence, evidence_integrity)
                    if evidence is not None and evidence_integrity is not None
                    else None
                ),
        },
        "authority_boundary": authority_boundary,
        "preserved_invariants": [
                "the comparison is limited to one recorded finding and the "
                "yield evidence it names",
                "content equality alone does not supply a yield relation",
                "the comparison does not revise its witness or traverse its "
                "support and premise relations",
        ],
        "crossings": crossings,
        "conflicts": conflicts,
        "unknowns": unknowns,
        "lawful_stopping_point": (
                "yield this Compare result concerning this exact represented "
                "relation and stop; do not traverse provenance references or determine "
                "downstream applicability, admission, input support, or "
                "revision"
        ),
        "revises": [],
        "limits": [
                "This revises nothing (06.Standing.B); availability is not "
                "revision.",
                "This establishes no Responsibility or responsible boundary.",
                "Agreement within these coordinates says nothing beyond them.",
                "A crossing represented here is not a crossing concerning "
                "whatever this finding stood on.",
        ],
    }
    responsible_act_evidence = ledger.append(
        FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND,
        {
            "downstream_act_id": downstream_act_id,
            "act_occurrence_id": act_occurrence_id,
            "act": "bounded finding Yield Compare",
            "responsibility": FINDING_YIELD_COMPARISON_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": authority_boundary,
            "evidence_scope": (
                "Evidence concerning this exact finding Yield Compare occurrence only"
            ),
        },
        locality_id=recorded.locality_id,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_id=recorded.locality_id,
        exact_act="bounded finding Yield Compare",
        act_occurrence_id=act_occurrence_id,
        result_kind=FINDING_YIELD_COMPARISON_RESULT_KIND,
        result_identity=f"finding-yield-comparison:{event_id}",
        result_content=result_payload,
        responsibility=FINDING_YIELD_COMPARISON_RESPONSIBILITY,
        live_boundary="recorded_finding_yield_compare",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        FINDING_YIELD_COMPARISON_KIND,
        {
            **result_payload,
            "responsible_act_evidence_id": responsible_act_evidence.id,
            "yield_evidence_id": yield_evidence.id,
            "occurrence_preservation": COMPARISON_OCCURRENCE_PRESERVATION,
        },
        locality_id=recorded.locality_id,
    )
