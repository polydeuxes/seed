"""Read-only capability verification promotion-readiness inspection.

This module joins evidence-derived capability candidates with acquired
verification evidence to explain whether a future capability verification
promotion would be supportable. It does not create ``capability_verified``
facts, select capabilities, evaluate policy, invoke tools, plan, or execute.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from seed_runtime.capability_candidates import (
    CapabilityCandidate,
    CapabilityCandidateEvidence,
    build_capability_candidates,
)
from seed_runtime.fact_index import DerivedFactIndex
from seed_runtime.state import State
from seed_runtime.verification_evidence import (
    VerificationEvidence,
    build_verification_evidence,
)

_PROMOTION_READINESS_BOUNDARY_NOTES = (
    "promotion_readiness_not_promotion",
    "promotion_readiness_not_capability_verified",
    "capability_candidate_not_verified_capability",
    "verification_evidence_not_capability_verified",
    "capability_verified_not_capability_selection",
    "capability_verified_not_execution_authority",
    "capability_verified_not_execution_decision",
    "capability_verified_not_tool_invocation",
    "observed_binary_not_permission",
    "no_capability_verified_fact_creation",
    "no_inventory_modification",
    "no_capability_selection",
    "no_policy_evaluation",
    "no_tool_execution",
    "read_only_inspection",
)


@dataclass(frozen=True)
class _CapabilityVerificationPayload:
    """Implementation-local verification payload before promotion admission checks."""

    candidate: str
    candidate_support: list[CapabilityCandidateEvidence] = field(default_factory=list)
    verification_support: list[VerificationEvidence] = field(default_factory=list)


@dataclass(frozen=True)
class CapabilityPromotionReadiness:
    """Promotion-readiness support for one capability candidate."""

    candidate: str
    candidate_support: list[CapabilityCandidateEvidence] = field(default_factory=list)
    verification_support: list[VerificationEvidence] = field(default_factory=list)
    promotion_readiness: str = "unsupported"
    rationale: str = ""
    boundary_notes: list[str] = field(
        default_factory=lambda: list(_PROMOTION_READINESS_BOUNDARY_NOTES)
    )


@dataclass(frozen=True)
class CapabilityPromotionReadinessInspection:
    """Read-only candidate plus verification evidence promotion-readiness result."""

    readiness: list[CapabilityPromotionReadiness] = field(default_factory=list)
    filter: str | None = None
    boundary: str = "capability_promotion_readiness_inspection_only"
    notes: list[str] = field(
        default_factory=lambda: list(_PROMOTION_READINESS_BOUNDARY_NOTES)
    )


def build_capability_promotion_readiness_inspection(
    state: State,
    *,
    filter_text: str | None = None,
    path_env: str | None = None,
    fact_index: DerivedFactIndex | None = None,
) -> CapabilityPromotionReadinessInspection:
    """Inspect whether candidates have support for future verification promotion.

    The candidate universe comes from evidence-derived capability candidates.
    Verification support comes from read-only local PATH metadata inspection. A
    candidate is ``supported`` only when both candidate support and verification
    support are present. This function never writes facts or events and never
    promotes readiness into ``capability_verified``.
    """

    candidate_inspection = build_capability_candidates(
        state, filter_text=filter_text, fact_index=fact_index
    )
    verification_by_candidate: dict[str, list[VerificationEvidence]] = {}
    for evidence in build_verification_evidence(
        state,
        filter_text=filter_text,
        path_env=path_env,
        candidate_inspection=candidate_inspection,
    ).evidence:
        verification_by_candidate.setdefault(evidence.candidate, []).append(evidence)

    readiness = [
        _readiness_for_candidate(
            candidate,
            verification_by_candidate.get(candidate.candidate, []),
        )
        for candidate in candidate_inspection.candidates
    ]
    return CapabilityPromotionReadinessInspection(
        readiness=readiness, filter=filter_text
    )


def _readiness_for_candidate(
    candidate: CapabilityCandidate,
    verification_support: list[VerificationEvidence],
) -> CapabilityPromotionReadiness:
    verification_payload = _verification_payload_for_candidate(
        candidate, verification_support
    )
    return _promotion_readiness_from_verification_payload(verification_payload)


def _verification_payload_for_candidate(
    candidate: CapabilityCandidate,
    verification_support: list[VerificationEvidence],
) -> _CapabilityVerificationPayload:
    return _CapabilityVerificationPayload(
        candidate=candidate.candidate,
        candidate_support=list(candidate.supporting_evidence),
        verification_support=list(verification_support),
    )


def _promotion_readiness_from_verification_payload(
    verification_payload: _CapabilityVerificationPayload,
) -> CapabilityPromotionReadiness:
    if verification_payload.candidate_support and verification_payload.verification_support:
        return CapabilityPromotionReadiness(
            candidate=verification_payload.candidate,
            candidate_support=list(verification_payload.candidate_support),
            verification_support=list(verification_payload.verification_support),
            promotion_readiness="supported",
            rationale=(
                "candidate support is present and verification evidence is present, so "
                "a future capability verification promotion would be supportable by "
                "the inspected evidence; this inspection does not promote, create "
                "capability_verified facts, select, authorize, evaluate policy, or execute"
            ),
        )
    return CapabilityPromotionReadiness(
        candidate=verification_payload.candidate,
        candidate_support=list(verification_payload.candidate_support),
        verification_support=list(verification_payload.verification_support),
        promotion_readiness="unsupported",
        rationale=(
            "candidate support is present but required verification support is missing, "
            "so capability verification promotion is not supportable from the inspected "
            "evidence; no capability_verified fact is created"
        ),
    )
