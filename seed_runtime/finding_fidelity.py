"""A bounded comparison of a recorded finding and its production evidence.

`01.External.D` grants this and states its conditions: a Fidelity finding is
produced only by a bounded comparison bringing constitutional grammar, a
bounded expectation, and an implementation witness under a declared seam or
scope. Within that scope it may find the witness faithful, an unfaithful
boundary crossing, mixed, or Unknown, and it must not become global
certification, a completion declaration, an owner map, a score, a registry, a
public diagnostic, or correction authority.

**What this compares.** One recorded recurrence Measurement finding and the
production evidence that finding names. `#2517` established that represented
relation for recurrence only: a measuring act preserves evidence of what it
produced, and the result carries the reference. Positional Measurement has not
adopted that production witness and is outside this comparator's scope. The
evidence is not the producing occurrence by identity. The expectation is exact
and local — *the recorded result is the result its production evidence
concerns* — and the witness is the recorded event itself.

**What it does not do.** It revises nothing. `06.Standing.B` establishes that
making an Assertion available at another locality does not revise its Standing,
establish Applicability, or require another Act. A finding found unfaithful here
keeps whatever Standing it had; this comparison establishes only its own result.

**It does not walk anything.** A fidelity finding concerning one recorded
finding is available to whatever Act has it participate, and each later act determines its
own applicability for its own inputs — `01.Standing.E.1`. Walking the support
basis and premise edges and revising what is found there would be that
determination made centrally, for exact Acts that never made it. The edges are
recorded and a later responsible act may follow them; this act does not.
"""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_CONVENTION,
    MEASUREMENT_RECORDED_KIND,
    PreservedMaterialMeasurementError,
    RECURRENCE_RESULT_KIND,
    RESPONSIBILITY_UNRECOVERED,
)
from seed_runtime.production_evidence import (
    PRODUCTION_EVIDENCE_KIND,
    _record_production_evidence,
    production_commitment,
)

FIDELITY_FINDING_KIND = "operator.fidelity.finding_recorded"
FIDELITY_RESULT_KIND = "finding Fidelity finding"
FIDELITY_CONVENTION = "recorded_recurrence_finding_fidelity_v1"

FAITHFUL_WITHIN_SCOPE = "faithful within scope"
UNFAITHFUL_CROSSING = "unfaithful boundary crossing"
FIDELITY_UNKNOWN = "Unknown"

ERASURE = "erasure"
INVENTION = "invention"

FIDELITY_RESULT_COORDINATES = frozenset(
    {
        "dimensions",
        "constitutional_subject",
        "bounded_expectation",
        "implementation_witness",
        "production_evidence",
        "evidence_and_provenance",
        "authority_boundary",
        "preserved_invariants",
        "observed_crossings",
        "conflicts",
        "unknowns",
        "lawful_stopping_point",
        "revises",
        "forbidden_inferences",
    }
)
FIDELITY_RECORDING_COORDINATES = frozenset(
    {"production_evidence_id", "occurrence_preservation"}
)
FIDELITY_OCCURRENCE_PRESERVATION = (
    "Fidelity finding durably recorded after its exact result was produced"
)


class FindingFidelityError(ValueError):
    """A fidelity comparison cannot be performed as declared."""


@dataclass(frozen=True)
class RecordedFidelityFinding:
    """One exact Fidelity result recovered from its recording occurrence.

    Constructing this representation does not establish that recovery occurred.
    A later Act must resolve its recorded-occurrence reference through the
    ledger rather than trust the dataclass by shape.
    """

    recorded_occurrence_id: str
    production_evidence_id: str
    source_finding_event_id: str
    standing: str

    @property
    def reference(self) -> dict[str, str]:
        """Address this durable recording occurrence for later re-recovery.

        This is not a reference to the producing Act occurrence or to the
        production-Evidence occurrence. Those identities remain distinct.
        """

        return {"recorded_occurrence_id": self.recorded_occurrence_id}


def get_recorded_fidelity_finding(
    ledger: EventLedger, event_id: str
) -> RecordedFidelityFinding | None:
    """Recover one occurrence-bound Fidelity result without using it.

    Recovery establishes that the occurrence carries the exact result its
    production Evidence commits to. It does not decide this finding's
    Applicability to any later Act, traverse its source finding, or revise
    anything.
    """

    event = ledger.get(event_id)
    if event is None:
        return None
    if event.kind != FIDELITY_FINDING_KIND:
        raise FindingFidelityError(
            f"{event_id} is {event.kind}, not a recorded Fidelity finding"
        )
    if ledger.integrity_of(event_id) == CORRUPTED:
        raise FindingFidelityError(
            "a corrupted occurrence cannot expose a Fidelity finding"
        )
    payload = event.payload
    if set(payload) != FIDELITY_RESULT_COORDINATES | FIDELITY_RECORDING_COORDINATES:
        raise FindingFidelityError(
            f"{event_id} does not preserve the exact Fidelity result and "
            "recording coordinate surfaces"
        )
    if payload.get("occurrence_preservation") != FIDELITY_OCCURRENCE_PRESERVATION:
        raise FindingFidelityError(
            f"{event_id} does not preserve the Fidelity recording occurrence"
        )
    evidence_id = payload.get("production_evidence_id")
    if not isinstance(evidence_id, str) or not evidence_id:
        raise FindingFidelityError(
            f"{event_id} names no exact production Evidence occurrence"
        )
    evidence = ledger.get(evidence_id)
    if evidence is None or evidence.kind != PRODUCTION_EVIDENCE_KIND:
        raise FindingFidelityError(
            f"{evidence_id} is not preserved production Evidence"
        )
    if ledger.integrity_of(evidence_id) == CORRUPTED:
        raise FindingFidelityError(
            "corrupted production Evidence cannot expose a Fidelity finding"
        )
    if evidence.workspace_id != event.workspace_id:
        raise FindingFidelityError(
            "a Fidelity finding and its production Evidence must belong to "
            "the same workspace"
        )
    if (
        evidence.payload.get("production_convention") != FIDELITY_CONVENTION
        or evidence.payload.get("produced_result_kind") != FIDELITY_RESULT_KIND
        or evidence.payload.get("production_coordinates")
        != sorted(FIDELITY_RESULT_COORDINATES)
    ):
        raise FindingFidelityError(
            "the named production Evidence does not describe the exact "
            "Fidelity result contract"
        )
    produced = {name: payload[name] for name in FIDELITY_RESULT_COORDINATES}
    if evidence.payload.get("production_commitment") != production_commitment(
        FIDELITY_CONVENTION, produced
    ):
        raise FindingFidelityError(
            "the named production Evidence concerns a different Fidelity result"
        )
    dimensions = payload.get("dimensions")
    source_id = payload.get("implementation_witness")
    standing = dimensions.get("standing") if isinstance(dimensions, dict) else None
    if (
        not isinstance(source_id, str)
        or not source_id
        or standing
        not in {FAITHFUL_WITHIN_SCOPE, UNFAITHFUL_CROSSING, FIDELITY_UNKNOWN}
        or not isinstance(dimensions, dict)
        or dimensions.get("identity") != f"fidelity:{source_id}"
        or dimensions.get("producing_act") != "bounded fidelity comparison"
        or dimensions.get("responsibility") != RESPONSIBILITY_UNRECOVERED
        or dimensions.get("scope_workspace") != event.workspace_id
        or dimensions.get("scope_locality")
        != (f"session:{event.session_id}" if event.session_id is not None else None)
    ):
        raise FindingFidelityError(
            f"{event_id} carries an incoherent Fidelity result shell"
        )
    return RecordedFidelityFinding(
        recorded_occurrence_id=event.id,
        production_evidence_id=evidence.id,
        source_finding_event_id=source_id,
        standing=standing,
    )


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
    """Compare one recorded recurrence finding and its production evidence.

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
    if recorded.payload.get("measurement_form") != "recurrence":
        raise FindingFidelityError(
            f"{event_id} is not a recorded recurrence Measurement finding; "
            "this comparison does not apply recurrence's production-evidence "
            "expectation to an unmigrated Measurement form"
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
            elif evidence.workspace_id != recorded.workspace_id:
                unresolved = True
                unknowns.append(
                    "the named production evidence belongs to a different "
                    "workspace, and no warranted cross-workspace movement is "
                    "available to this comparison"
                )
            elif evidence.kind != PRODUCTION_EVIDENCE_KIND:
                observed.append(
                    _crossing(
                        INVENTION,
                        "the named occurrence is represented as production "
                        "evidence, but its recorded kind does not represent "
                        "production evidence",
                    )
                )
            elif (
                evidence.payload.get("produced_result_kind")
                != RECURRENCE_RESULT_KIND
                or evidence.payload.get("production_convention")
                != MEASUREMENT_CONVENTION
            ):
                observed.append(
                    _crossing(
                        INVENTION,
                        "the named production evidence concerns a different "
                        "kind of result or production convention",
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
                    except PreservedMaterialMeasurementError:
                        observed.append(
                            _crossing(
                                ERASURE,
                                "the recorded finding omits at least one exact "
                                "coordinate its production evidence commits to",
                            )
                        )
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
    result_payload = {
        "dimensions": {
                "identity": f"fidelity:{event_id}",
                "content": (
                    "a recorded measurement finding compared against the "
                    "production evidence it names"
                ),
                "standing": standing,
                "producing_act": "bounded fidelity comparison",
                "responsibility": RESPONSIBILITY_UNRECOVERED,
                "authority": authority_boundary,
                "scope_workspace": recorded.workspace_id,
                "scope_locality": (
                    f"session:{recorded.session_id}"
                    if recorded.session_id is not None
                    else None
                ),
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
                "relation and stop; do not traverse provenance references or determine "
                "downstream applicability, admission, input support, or "
                "revision"
        ),
        "revises": [],
        "forbidden_inferences": [
                "This revises nothing (06.Standing.B); availability is not "
                "revision.",
                "This establishes no responsibility and names no owner.",
                "Faithful within this scope is not faithful generally.",
                "A crossing observed here is not a crossing observed of "
                "whatever this finding stood on.",
        ],
    }
    production_evidence = _record_production_evidence(
        ledger,
        workspace_id=recorded.workspace_id,
        session_id=recorded.session_id,
        convention=FIDELITY_CONVENTION,
        producing_act="bounded Fidelity comparison",
        produced_result_kind=FIDELITY_RESULT_KIND,
        result_identity=f"fidelity:{event_id}",
        produced_content=result_payload,
        responsibility=RESPONSIBILITY_UNRECOVERED,
    )
    return ledger.append(
        FIDELITY_FINDING_KIND,
        recorded.workspace_id,
        {
            **result_payload,
            "production_evidence_id": production_evidence.id,
            "occurrence_preservation": FIDELITY_OCCURRENCE_PRESERVATION,
        },
        session_id=recorded.session_id,
    )
