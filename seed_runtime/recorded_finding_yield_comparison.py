"""A bounded Compare of a recorded finding and its Yield Evidence.

This Compare has one recorded finding and its named Yield Evidence as participants.
Within that boundary it may find agreement, a coordinate difference, or
Unknown. It does not certify this Seed, declare completion, map responsible
boundaries, score results, expose a public diagnostic, or grant correction
Authority.

**What this compares.** One recorded recurrence Measurement finding and the
Yield Evidence that finding names. `#2517` established that represented
relation for recurrence only: a measuring act preserves exact Yield Evidence,
and the result carries the reference. Positional Measurement has not
adopted that yield witness and is outside this comparator's scope. The
evidence is not the yielding occurrence by identity. The expectation is exact
and local — *the recorded result is the result named by its Yield Evidence* —
and the witness is the recorded event itself.

**What it does not do.** It establishes no movement. `06.Standing.B` establishes that
making an Assertion available at another locality does not revise its Standing,
establish Applicability, or require another Act. A coordinate difference here
keeps whatever Standing it had; this comparison establishes only its own result.

The Compare does not traverse Input Support or revise its input occurrences.
"""

from __future__ import annotations

from dataclasses import dataclass

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    PreservedMaterialMeasurementError,
    RECURRENCE_RESULT_KIND,
)
from seed_runtime.yield_evidence import (
    YIELD_EVIDENCE_KIND,
    _record_yield_evidence,
    read_yield_relation_requirements,
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
        "result_identity",
        "downstream_act_identity",
        "act_occurrence_identity",
        "dimensions",
        "constitutional_subject",
        "compared_relation",
        "recorded_finding_reference",
        "yield_evidence",
        "evidence_and_provenance",
        "authority_boundary",
        "crossings",
        "conflicts",
        "unknowns",
        "limits",
    }
)
COMPARISON_RECORDING_COORDINATES = frozenset(
    {
        "responsible_act_evidence_identity",
        "yield_evidence_identity",
        "occurrence_preservation",
    }
)
COMPARISON_OCCURRENCE_PRESERVATION = (
    "recorded finding Yield comparison durably recorded with exact result Yield Evidence"
)


class RecordedFindingYieldComparisonError(ValueError):
    """The recorded-finding Yield Compare cannot be performed as declared."""


@dataclass(frozen=True)
class RecordedFindingYieldComparison:
    """One exact Compare result carried by one recording occurrence."""

    recorded_occurrence_identity: str
    yield_evidence_identity: str
    source_finding_event_identity: str
    standing: str

    @property
    def reference(self) -> dict[str, str]:
        """Return its exact recording-occurrence reference."""

        return {"recorded_occurrence_identity": self.recorded_occurrence_identity}


def get_recorded_finding_yield_comparison(
    ledger: EventLedger, event_identity: str
) -> RecordedFindingYieldComparison | None:
    """Return an exact occurrence-bound Compare result when evidenced."""

    event = ledger.get(event_identity)
    if event is None:
        return None
    if event.kind != FINDING_YIELD_COMPARISON_KIND:
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} is {event.kind}, not a recorded finding Yield comparison"
        )
    if ledger.integrity_of(event_identity) == CORRUPTED:
        raise RecordedFindingYieldComparisonError(
            "a corrupted occurrence cannot expose a finding Yield comparison"
        )
    material = event.material
    if set(material) != COMPARISON_RESULT_COORDINATES | COMPARISON_RECORDING_COORDINATES:
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} does not preserve the exact Compare result and "
            "recording coordinate surfaces"
        )
    if material.get("occurrence_preservation") != COMPARISON_OCCURRENCE_PRESERVATION:
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} does not preserve the Compare recording occurrence"
        )
    evidence_identity = material.get("yield_evidence_identity")
    if not isinstance(evidence_identity, str) or not evidence_identity:
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} names no exact yield Evidence occurrence"
        )
    evidence = ledger.get(evidence_identity)
    if evidence is None or evidence.kind != YIELD_EVIDENCE_KIND:
        raise RecordedFindingYieldComparisonError(
            f"{evidence_identity} is not preserved yield Evidence"
        )
    if ledger.integrity_of(evidence_identity) == CORRUPTED:
        raise RecordedFindingYieldComparisonError(
            "corrupted Yield Evidence cannot expose a Compare result"
        )
    if (
        evidence.material.get("result_kind")
        != FINDING_YIELD_COMPARISON_RESULT_KIND
        or evidence.material.get("yield_coordinates")
        != sorted(COMPARISON_RESULT_COORDINATES)
        or evidence.material.get("dimensions", {}).get("act_occurrence_identity")
        != material.get("act_occurrence_identity")
    ):
        raise RecordedFindingYieldComparisonError(
            "the named yield Evidence does not describe the exact "
            "Compare result contract"
        )
    exact_result = {name: material[name] for name in COMPARISON_RESULT_COORDINATES}
    if evidence.material.get("result") != exact_result:
        raise RecordedFindingYieldComparisonError(
            "the named Yield Evidence carries a different Compare result"
        )
    act_evidence_identity = material.get("responsible_act_evidence_identity")
    if not isinstance(act_evidence_identity, str) or not act_evidence_identity:
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} names no exact responsible Act Evidence occurrence"
        )
    act_evidence = ledger.get(act_evidence_identity)
    if (
        act_evidence is None
        or act_evidence.kind != FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND
    ):
        raise RecordedFindingYieldComparisonError(
            f"{act_evidence_identity} is not responsible Act Evidence for this Compare"
        )
    if not all(
        read_yield_relation_requirements(
            ledger,
            recorded_result_event_identity=event.identity,
            result_evidence_event_identity=evidence.identity,
            responsible_act_evidence_event_identity=act_evidence.identity,
        ).values()
    ):
        raise RecordedFindingYieldComparisonError(
            "the Compare Event does not bind its exact Act and result Evidence"
        )
    dimensions = material.get("dimensions")
    source_identity = material.get("recorded_finding_reference")
    standing = dimensions.get("standing") if isinstance(dimensions, dict) else None
    if (
        not isinstance(source_identity, str)
        or not source_identity
        or standing
        not in {
            AGREES_WITH_YIELD_EVIDENCE,
            DIFFERS_FROM_YIELD_EVIDENCE,
            COMPARISON_UNKNOWN,
        }
        or not isinstance(dimensions, dict)
        or dimensions.get("identity") != f"finding-yield-comparison:{source_identity}"
        or dimensions.get("exact_act") != "bounded finding Yield Compare"
        or dimensions.get("responsibility")
        != FINDING_YIELD_COMPARISON_RESPONSIBILITY
        or dimensions.get("scope_locality")
        != (f"locality:{event.locality_identity}" if event.locality_identity is not None else None)
    ):
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} carries an incoherent Compare result shell"
        )
    return RecordedFindingYieldComparison(
        recorded_occurrence_identity=event.identity,
        yield_evidence_identity=evidence.identity,
        source_finding_event_identity=source_identity,
        standing=standing,
    )


def _provenance(event: Event) -> dict[str, object]:
    """The exact occurrence coordinates available to this comparison."""

    return {
        "event_identity": event.identity,
        "event_kind": event.kind,
        "locality_identity": event.locality_identity,
    }


def _crossing(kind: str, material: str) -> dict[str, str]:
    return {"kind": kind, "material": material}


def compare_recorded_finding_yield(ledger: EventLedger, event_identity: str) -> Event:
    """Compare one recorded recurrence finding and its Yield Evidence."""

    recorded = ledger.get(event_identity)
    if recorded is None or recorded.kind != MEASUREMENT_RECORDED_KIND:
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} is not a recorded measurement finding, and this "
            "comparison compares one against its yield evidence"
        )
    if recorded.material.get("measurement_distinction") != "recurrence":
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} is not a recorded recurrence Measurement finding; "
            "this comparison does not apply recurrence's yield-evidence "
            "expectation to an unmigrated Measurement representation"
        )
    recorded_integrity = ledger.integrity_of(event_identity)
    if recorded_integrity == CORRUPTED:
        raise RecordedFindingYieldComparisonError(
            f"{event_identity} is corrupted, so it cannot serve as this comparison's "
            "recorded finding"
        )

    crossings: list[dict[str, str]] = []
    conflicts: list[str] = []
    unknowns = [
        "whether the finding agrees with its Yield Evidence in any coordinate "
        "this Compare did not bring under its Scope"
    ]
    unresolved = False
    named = recorded.material.get("yield_evidence_identity")
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
                evidence.material.get("result_kind")
                != RECURRENCE_RESULT_KIND
            ):
                crossings.append(
                    _crossing(
                        UNSUPPORTED_COORDINATE,
                        "the named yield evidence carries a different "
                        "kind of result",
                    )
                )
            else:
                result = evidence.material.get("result")
                coordinates = evidence.material.get("yield_coordinates")
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
                                    "the named yield evidence does not carry "
                                    "this exact recorded content",
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
    downstream_act_identity = new_identity("finding_yield_comparison_act")
    act_occurrence_identity = new_identity("finding_yield_comparison_act_occurrence")
    result_identity = new_identity("finding_yield_comparison_result")
    result_material = {
        "result_identity": result_identity,
        "downstream_act_identity": downstream_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "dimensions": {
                "identity": f"finding-yield-comparison:{event_identity}",
                "content": (
                    "a recorded measurement finding compared against the "
                    "yield evidence it names"
                ),
                "standing": standing,
                "exact_act": "bounded finding Yield Compare",
                "responsibility": FINDING_YIELD_COMPARISON_RESPONSIBILITY,
                "authority": authority_boundary,
                "scope_locality": (
                    f"locality:{recorded.locality_identity}"
                    if recorded.locality_identity is not None
                    else None
                ),
            },
        "constitutional_subject": (
                "the recorded finding's represented relation to the yield "
                "evidence it names"
            ),
        "compared_relation": (
                "the recorded finding names preserved yield evidence, and "
                "that evidence carries this exact recorded content"
            ),
        "recorded_finding_reference": event_identity,
        "yield_evidence": named,
        "evidence_and_provenance": {
                "recorded_finding": _provenance(recorded),
                "yield_evidence": (
                    _provenance(evidence)
                    if evidence is not None
                    else None
                ),
        },
        "authority_boundary": authority_boundary,
        "crossings": crossings,
        "conflicts": conflicts,
        "unknowns": unknowns,
        "limits": [
                "This establishes no movement (06.Standing.B); availability is "
                "not movement.",
                "This establishes no Responsibility or responsible boundary.",
                "Agreement within these coordinates says nothing beyond them.",
        ],
    }
    responsible_act_evidence = ledger.append(
        FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": downstream_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "bounded finding Yield Compare",
            "responsibility": FINDING_YIELD_COMPARISON_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": authority_boundary,
            "evidence_scope": (
                "Evidence for this exact finding Yield Compare occurrence only"
            ),
        },
        locality_identity=recorded.locality_identity,
    )
    yield_evidence = _record_yield_evidence(
        ledger,
        locality_identity=recorded.locality_identity,
        exact_act="bounded finding Yield Compare",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind=FINDING_YIELD_COMPARISON_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=FINDING_YIELD_COMPARISON_RESPONSIBILITY,
        live_boundary="recorded_finding_yield_compare",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        FINDING_YIELD_COMPARISON_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "yield_evidence_identity": yield_evidence.identity,
            "occurrence_preservation": COMPARISON_OCCURRENCE_PRESERVATION,
        },
        locality_identity=recorded.locality_identity,
    )
