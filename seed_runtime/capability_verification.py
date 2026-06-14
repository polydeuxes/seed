"""Read-only capability candidate verification inspection.

This module joins evidence-derived capability candidates to existing projected
``capability_verified`` facts. It preserves verification status for inspection
only; it does not select capabilities, evaluate policy, invoke tools, plan, or
execute anything.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from seed_runtime.capability_candidates import CapabilityCandidate, build_capability_candidates
from seed_runtime.capability_inventory import CapabilityInventoryEntry, build_capability_inventory
from seed_runtime.state import State
from seed_runtime.verification_evidence import VerificationEvidence, build_verification_evidence

_VERIFICATION_BOUNDARY_NOTES = (
    "capability_candidate_not_verified_capability",
    "verified_capability_not_capability_selection",
    "verified_capability_not_execution_authority",
    "verified_capability_not_execution_decision",
    "verified_capability_not_tool_invocation",
    "verified_capability_not_permission",
    "no_capability_selection",
    "no_policy_evaluation",
    "no_tool_execution",
    "read_only_inspection",
)


@dataclass(frozen=True)
class CapabilityVerification:
    """Verification status for one preserved capability candidate."""

    candidate: str
    verification_status: str
    supporting_evidence: list[object] = field(default_factory=list)
    verification_supporting_facts: list[str] = field(default_factory=list)
    verification_supporting_evidence: list[object] = field(default_factory=list)
    acquired_verification_evidence: list[VerificationEvidence] = field(default_factory=list)
    rationale: str = ""
    boundary_notes: list[str] = field(default_factory=lambda: list(_VERIFICATION_BOUNDARY_NOTES))


@dataclass(frozen=True)
class CapabilityVerificationInspection:
    """Read-only candidate-to-verification inspection result."""

    verifications: list[CapabilityVerification] = field(default_factory=list)
    filter: str | None = None
    boundary: str = "capability_verification_inspection_only"
    notes: list[str] = field(default_factory=lambda: list(_VERIFICATION_BOUNDARY_NOTES))


def build_capability_verification_inspection(
    state: State, *, filter_text: str | None = None, now: datetime | None = None
) -> CapabilityVerificationInspection:
    """Inspect candidate verification status from projected State only.

    The candidate universe comes from evidence-derived capability candidates.
    Verification status comes only from existing capability inventory semantics,
    which are themselves backed by projected ``capability_verified`` facts. A
    package-observed candidate without a ``capability_verified`` fact remains
    unverified because candidate evidence is not verification authority.
    """

    candidate_inspection = build_capability_candidates(state, filter_text=filter_text)
    verification_evidence_by_candidate: dict[str, list[VerificationEvidence]] = {}
    for evidence in build_verification_evidence(state, filter_text=filter_text).evidence:
        verification_evidence_by_candidate.setdefault(evidence.candidate, []).append(evidence)

    inventory_by_capability: dict[str, CapabilityInventoryEntry] = {
        entry.capability: entry
        for entry in build_capability_inventory(
            state, now=now or datetime.now(timezone.utc)
        )
    }
    verifications = [
        _verification_for_candidate(
            candidate,
            inventory_by_capability.get(candidate.candidate),
            verification_evidence_by_candidate.get(candidate.candidate, []),
        )
        for candidate in candidate_inspection.candidates
    ]
    return CapabilityVerificationInspection(
        verifications=verifications,
        filter=filter_text,
    )


def _verification_for_candidate(
    candidate: CapabilityCandidate,
    inventory_entry: CapabilityInventoryEntry | None,
    acquired_evidence: list[VerificationEvidence],
) -> CapabilityVerification:
    if inventory_entry is None:
        return CapabilityVerification(
            candidate=candidate.candidate,
            verification_status="unverified",
            supporting_evidence=list(candidate.supporting_evidence),
            acquired_verification_evidence=list(acquired_evidence),
            rationale=(
                "candidate evidence is preserved, but no projected capability_verified "
                "fact exists for this candidate; verification remains separate from "
                "candidate preservation, selection, permission, and execution"
            ),
        )
    return CapabilityVerification(
        candidate=candidate.candidate,
        verification_status=inventory_entry.state,
        supporting_evidence=list(candidate.supporting_evidence),
        verification_supporting_facts=list(inventory_entry.supporting_facts),
        verification_supporting_evidence=list(inventory_entry.supporting_evidence),
        acquired_verification_evidence=list(acquired_evidence),
        rationale=(
            f"candidate evidence is preserved and verification status is derived from "
            f"existing capability inventory: {inventory_entry.reason}; this does not "
            f"grant selection, permission, policy approval, or execution authority"
        ),
    )
