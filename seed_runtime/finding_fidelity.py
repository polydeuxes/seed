"""A bounded comparison of a recorded finding and its yield evidence.

`01.Source.D` grants this and states its conditions: a Fidelity finding is
yielded only by a bounded comparison bringing constitutional grammar, a
bounded expectation, and an implementation witness under a declared seam or
scope. Within that scope it may find the witness faithful, an unfaithful
boundary crossing, mixed, or Unknown, and it must not become global
certification, a completion declaration, a responsible-boundary map, a score, a registry, a
public diagnostic, or correction authority.

**What this compares.** One recorded recurrence Measurement finding and the
yield evidence that finding names. `#2517` established that represented
relation for recurrence only: a measuring act preserves evidence of what it
yielded, and the result carries the reference. Positional Measurement has not
adopted that yield witness and is outside this comparator's scope. The
evidence is not the yielding occurrence by identity. The expectation is exact
and local — *the recorded result is the result its yield evidence
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
from seed_runtime.ids import new_id
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_CONVENTION,
    MEASUREMENT_RECORDED_KIND,
    PreservedMaterialMeasurementError,
    RECURRENCE_RESULT_KIND,
    RESPONSIBILITY_UNESTABLISHED,
)
from seed_runtime.yield_evidence import (
    YIELD_EVIDENCE_KIND,
    _record_yield_evidence,
    yield_commitment,
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
        "target_act_id",
        "act_occurrence_id",
        "dimensions",
        "constitutional_subject",
        "bounded_expectation",
        "implementation_witness",
        "yield_evidence",
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
    {"yield_evidence_id", "occurrence_preservation"}
)
FIDELITY_OCCURRENCE_PRESERVATION = (
    "Fidelity finding durably recorded after its exact result was yielded"
)


class FindingFidelityError(ValueError):
    """A fidelity comparison cannot be performed as declared."""


@dataclass(frozen=True)
class RecordedFidelityFinding:
    """One exact Fidelity result reconstructed from its recording occurrence.

    Constructing this representation does not establish that reconstruction occurred.
    A later Act must resolve its recorded-occurrence reference through the
    ledger rather than trust the dataclass by shape.
    """

    recorded_occurrence_id: str
    yield_evidence_id: str
    source_finding_event_id: str
    standing: str

    @property
    def reference(self) -> dict[str, str]:
        """Address this durable recording occurrence for later re-reconstruction.

        This is not a reference to the yielding Act occurrence or to the
        yield-Evidence occurrence. Those identities remain distinct.
        """

        return {"recorded_occurrence_id": self.recorded_occurrence_id}


def get_recorded_fidelity_finding(
    ledger: EventLedger, event_id: str
) -> RecordedFidelityFinding | None:
    """Reconstruct one occurrence-bound Fidelity result without using it.

    Reconstruction establishes that the occurrence carries the exact result its
    yield Evidence commits to. It does not decide this finding's
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
    evidence_id = payload.get("yield_evidence_id")
    if not isinstance(evidence_id, str) or not evidence_id:
        raise FindingFidelityError(
            f"{event_id} names no exact yield Evidence occurrence"
        )
    evidence = ledger.get(evidence_id)
    if evidence is None or evidence.kind != YIELD_EVIDENCE_KIND:
        raise FindingFidelityError(
            f"{evidence_id} is not preserved yield Evidence"
        )
    if ledger.integrity_of(evidence_id) == CORRUPTED:
        raise FindingFidelityError(
            "corrupted yield Evidence cannot expose a Fidelity finding"
        )
    if evidence.workspace_id != event.workspace_id:
        raise FindingFidelityError(
            "a Fidelity finding and its yield Evidence must belong to "
            "the same workspace"
        )
    if (
        evidence.payload.get("yield_convention") != FIDELITY_CONVENTION
        or evidence.payload.get("yielded_result_kind") != FIDELITY_RESULT_KIND
        or evidence.payload.get("yield_coordinates")
        != sorted(FIDELITY_RESULT_COORDINATES)
        or evidence.payload.get("dimensions", {}).get("act_occurrence_id")
        != payload.get("act_occurrence_id")
    ):
        raise FindingFidelityError(
            "the named yield Evidence does not describe the exact "
            "Fidelity result contract"
        )
    yielded = {name: payload[name] for name in FIDELITY_RESULT_COORDINATES}
    if evidence.payload.get("yield_commitment") != yield_commitment(
        FIDELITY_CONVENTION, yielded
    ):
        raise FindingFidelityError(
            "the named yield Evidence concerns a different Fidelity result"
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
        or dimensions.get("yielding_act") != "bounded fidelity comparison"
        or dimensions.get("responsibility") != RESPONSIBILITY_UNESTABLISHED
        or dimensions.get("scope_workspace") != event.workspace_id
        or dimensions.get("scope_locality")
        != (f"session:{event.session_id}" if event.session_id is not None else None)
    ):
        raise FindingFidelityError(
            f"{event_id} carries an incoherent Fidelity result shell"
        )
    return RecordedFidelityFinding(
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
        "workspace_id": event.workspace_id,
        "session_id": event.session_id,
        "integrity": integrity,
    }


def _crossing(kind: str, observation: str) -> dict[str, str]:
    return {"kind": kind, "observation": observation}


def compare_recorded_finding(ledger: EventLedger, event_id: str) -> Event:
    """Compare one recorded recurrence finding and its yield evidence.

    The bounded expectation, stated so it can be wrong: a recorded measurement
    finding names yield evidence, that evidence is preserved, and it
    concerns this exact recorded content.
    """

    recorded = ledger.get(event_id)
    if recorded is None or recorded.kind != MEASUREMENT_RECORDED_KIND:
        raise FindingFidelityError(
            f"{event_id} is not a recorded measurement finding, and this "
            "comparison compares one against its yield evidence"
        )
    if recorded.payload.get("measurement_form") != "recurrence":
        raise FindingFidelityError(
            f"{event_id} is not a recorded recurrence Measurement finding; "
            "this comparison does not apply recurrence's yield-evidence "
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
    named = recorded.payload.get("yield_evidence_id")
    evidence: Event | None = None
    evidence_integrity: str | None = None
    if named is None:
        observed.append(
            _crossing(
                ERASURE,
                "the recorded finding does not preserve the required relation "
                "to yield evidence",
            )
        )
    elif not isinstance(named, str) or not named:
        observed.append(
            _crossing(
                INVENTION,
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
            elif evidence.workspace_id != recorded.workspace_id:
                unresolved = True
                unknowns.append(
                    "the named yield evidence belongs to a different "
                    "workspace, and no established cross-workspace movement is "
                    "available to this comparison"
                )
            elif evidence.kind != YIELD_EVIDENCE_KIND:
                observed.append(
                    _crossing(
                        INVENTION,
                        "the named occurrence is represented as yield "
                        "evidence, but its recorded kind does not represent "
                        "yield evidence",
                    )
                )
            elif (
                evidence.payload.get("yielded_result_kind")
                != RECURRENCE_RESULT_KIND
                or evidence.payload.get("yield_convention")
                != MEASUREMENT_CONVENTION
            ):
                observed.append(
                    _crossing(
                        INVENTION,
                        "the named yield evidence concerns a different "
                        "kind of result or yield convention",
                    )
                )
            else:
                commitment = evidence.payload.get("yield_commitment")
                coordinates = evidence.payload.get("yield_coordinates")
                if commitment is None or coordinates is None:
                    observed.append(
                        _crossing(
                            ERASURE,
                            "the yield evidence omits the commitment or "
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
                        "the yield evidence does not carry an interpretable "
                        "commitment and exact coordinate boundary"
                    )
                else:
                    from seed_runtime.preserved_material_measurement import (
                        _recorded_yield_commitment,
                    )

                    try:
                        recorded_commitment = _recorded_yield_commitment(
                            recorded, tuple(coordinates)
                        )
                    except PreservedMaterialMeasurementError:
                        observed.append(
                            _crossing(
                                ERASURE,
                                "the recorded finding omits at least one exact "
                                "coordinate its yield evidence commits to",
                            )
                        )
                    else:
                        if commitment != recorded_commitment:
                            # The mismatch proves the bounded expectation failed.
                            # It does not prove which Fidelity crossing caused it:
                            # altered content and a misplaced evidence reference
                            # yield the same witness here.
                            observed.append(
                                _crossing(
                                    FIDELITY_UNKNOWN,
                                    "the named yield evidence does not "
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
        "this comparison within this exact finding-to-yield-evidence "
        "scope only; no certification, completion, responsible-boundary map, score, or "
        "correction authority"
    )
    target_act_id = new_id("fidelity_comparison_act")
    act_occurrence_id = new_id("fidelity_comparison_act_occurrence")
    result_payload = {
        "target_act_id": target_act_id,
        "act_occurrence_id": act_occurrence_id,
        "dimensions": {
                "identity": f"fidelity:{event_id}",
                "content": (
                    "a recorded measurement finding compared against the "
                    "yield evidence it names"
                ),
                "standing": standing,
                "yielding_act": "bounded fidelity comparison",
                "responsibility": RESPONSIBILITY_UNESTABLISHED,
                "authority": authority_boundary,
                "scope_workspace": recorded.workspace_id,
                "scope_locality": (
                    f"session:{recorded.session_id}"
                    if recorded.session_id is not None
                    else None
                ),
            },
        "constitutional_subject": (
                "the recorded finding's represented relation to the yield "
                "evidence it names"
            ),
        "bounded_expectation": (
                "the recorded finding names preserved yield evidence, and "
                "that evidence concerns this exact recorded content"
            ),
        "implementation_witness": event_id,
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
        "observed_crossings": observed,
        "conflicts": conflicts,
        "unknowns": unknowns,
        "lawful_stopping_point": (
                "yield this Fidelity finding concerning this exact represented "
                "relation and stop; do not traverse provenance references or determine "
                "downstream applicability, admission, input support, or "
                "revision"
        ),
        "revises": [],
        "forbidden_inferences": [
                "This revises nothing (06.Standing.B); availability is not "
                "revision.",
                "This establishes no Responsibility or responsible boundary.",
                "Faithful within this scope is not faithful generally.",
                "A crossing observed here is not a crossing observed of "
                "whatever this finding stood on.",
        ],
    }
    yield_evidence = _record_yield_evidence(
        ledger,
        workspace_id=recorded.workspace_id,
        session_id=recorded.session_id,
        convention=FIDELITY_CONVENTION,
        yielding_act="bounded Fidelity comparison",
        act_occurrence_id=act_occurrence_id,
        yielded_result_kind=FIDELITY_RESULT_KIND,
        result_identity=f"fidelity:{event_id}",
        yielded_content=result_payload,
        responsibility=RESPONSIBILITY_UNESTABLISHED,
    )
    return ledger.append(
        FIDELITY_FINDING_KIND,
        recorded.workspace_id,
        {
            **result_payload,
            "yield_evidence_id": yield_evidence.id,
            "occurrence_preservation": FIDELITY_OCCURRENCE_PRESERVATION,
        },
        session_id=recorded.session_id,
    )
