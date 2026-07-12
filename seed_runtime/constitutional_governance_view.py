"""Read-only Constitutional Governance View composed from existing evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from seed_runtime.serialization import to_plain

RelationshipStatus = Literal["known", "unknown"]


@dataclass(frozen=True)
class ConstitutionalGovernanceRelationship:
    """One preserved governance relationship in the constitutional governance view."""

    name: str
    status: RelationshipStatus
    support_level: str
    evidence: tuple[str, ...]
    summary: str


@dataclass(frozen=True)
class ConstitutionalGovernanceView:
    """Read-only view over existing constitutional governance evidence."""

    name: str
    compatibility_answer: str
    composition: tuple[str, ...]
    relationships: tuple[ConstitutionalGovernanceRelationship, ...]
    unknowns: tuple[str, ...]
    explicit_refusals: tuple[str, ...]
    remaining_candidate_views: tuple[str, ...]
    read_only: bool = True
    mutates_cluster: bool = False
    writes_event_ledger: bool = False


GOVERNANCE_EVIDENCE: tuple[str, ...] = (
    "constitutional_governance_investigation.md",
    "constitutional_question_grammar_characterization.md",
    "constitutional_relationship_grammar_survey.md",
    "external_grammar_structural_recovery_characterization.md",
    "constitutional_process_reconciliation.md",
    "constitutional_fidelity_characterization.md",
)


def build_constitutional_governance_view() -> ConstitutionalGovernanceView:
    """Build the bounded Constitutional Governance View without repository mutation."""

    relationships = (
        ConstitutionalGovernanceRelationship(
            name="Question Grammar governs later Process movement",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_governance_investigation.md",
                "constitutional_question_grammar_characterization.md",
                "constitutional_process_reconciliation.md",
            ),
            summary="Question Grammar constrains and locally authorizes the Lawful Question stage while refusing to become Orientation or Recovery.",
        ),
        ConstitutionalGovernanceRelationship(
            name="Relationship Grammar governs connective use",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_governance_investigation.md",
                "constitutional_relationship_grammar_survey.md",
            ),
            summary="Relationship Grammar authorizes only repository-supported connective classifications and preserves boundaries without participant ownership.",
        ),
        ConstitutionalGovernanceRelationship(
            name="External Grammar governs representation intake",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_governance_investigation.md",
                "external_grammar_structural_recovery_characterization.md",
            ),
            summary="External Grammar constrains later constitutional work to consume bounded recovered structures with provenance instead of raw representation authority.",
        ),
        ConstitutionalGovernanceRelationship(
            name="Constitutional Process governs bounded movement",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_governance_investigation.md",
                "constitutional_process_reconciliation.md",
            ),
            summary="Process preserves supported movement and lawful stop boundaries without becoming a runtime pipeline, hierarchy, or universal sequence.",
        ),
        ConstitutionalGovernanceRelationship(
            name="Constitutional Fidelity governs lawful realization",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_governance_investigation.md",
                "constitutional_fidelity_characterization.md",
            ),
            summary="Fidelity constrains realization by testing preservation of recovered authority while refusing to create or own that authority.",
        ),
    )
    return ConstitutionalGovernanceView(
        name="Constitutional Governance View",
        compatibility_answer="No.",
        composition=GOVERNANCE_EVIDENCE,
        relationships=relationships,
        unknowns=(
            "Whether there is a distinct constitutional governance owner remains Unknown.",
            "Whether every recovery requires a separate cross-examination artifact remains Unknown.",
            "Whether every cross-examination requires a separate completion audit remains Unknown.",
            "Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains Unknown.",
            "Whether Question Grammar and Inquiry Navigation are distinct competencies remains Unknown.",
            "Whether a common owner exists for external-representation recovery families remains Unknown and currently unsupported.",
            "Whether governance relationships require any implementation topology remains Unknown because implementation was not inspected.",
        ),
        explicit_refusals=(
            "governance execution",
            "governance ownership",
            "constitutional recovery",
            "implementation recovery",
            "hierarchy",
            "runtime governance",
            "repository mutation",
        ),
        remaining_candidate_views=(
            "Fidelity View",
            "Observability Coverage View",
            "Provenance Coverage View",
        ),
    )


def constitutional_governance_view_json(view: ConstitutionalGovernanceView) -> dict[str, Any]:
    """Return deterministic JSON-ready Constitutional Governance View data."""

    return to_plain(view)


def format_constitutional_governance_view(view: ConstitutionalGovernanceView) -> str:
    """Render the Constitutional Governance View for humans."""

    lines = [
        view.name,
        "",
        f"Compatibility answer: {view.compatibility_answer}",
        f"Read-only: {str(view.read_only).lower()}",
        f"Writes event ledger: {str(view.writes_event_ledger).lower()}",
        f"Mutates cluster: {str(view.mutates_cluster).lower()}",
        "",
        "Governance relationships",
        "",
    ]
    for relationship in view.relationships:
        evidence = ", ".join(relationship.evidence)
        lines.append(
            f"* {relationship.name}: {relationship.status} ({relationship.support_level}) - {relationship.summary} Evidence: {evidence}"
        )
    lines.extend(["", "Preserved Unknowns", ""])
    lines.extend(f"* {unknown}" for unknown in view.unknowns)
    lines.extend(["", "Explicit refusals", ""])
    lines.extend(f"* {refusal}" for refusal in view.explicit_refusals)
    lines.extend(["", "Remaining candidate views", ""])
    lines.extend(f"* {candidate}" for candidate in view.remaining_candidate_views)
    return "\n".join(lines)
