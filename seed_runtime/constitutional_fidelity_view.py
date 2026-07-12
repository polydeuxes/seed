"""Read-only Constitutional Fidelity View composed from completed evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from seed_runtime.serialization import to_plain

ClassificationStatus = Literal["known", "unknown"]


@dataclass(frozen=True)
class ConstitutionalFidelityClassification:
    """One bounded fidelity classification from the completed evidence corpus."""

    name: str
    status: ClassificationStatus
    support_level: str
    evidence: tuple[str, ...]
    summary: str


@dataclass(frozen=True)
class ConstitutionalFidelityView:
    """Read-only view over the completed Constitutional Fidelity evidence corpus."""

    name: str
    compatibility_answer: str
    summary: str
    composition: tuple[str, ...]
    classifications: tuple[ConstitutionalFidelityClassification, ...]
    recurring_constitutional_discipline: tuple[str, ...]
    unknowns: tuple[str, ...]
    explicit_refusals: tuple[str, ...]
    read_only_boundaries: tuple[str, ...]
    remaining_candidate_views: tuple[str, ...]
    read_only: bool = True
    mutates_cluster: bool = False
    writes_event_ledger: bool = False


FIDELITY_EVIDENCE: tuple[str, ...] = (
    "constitutional_fidelity_characterization.md",
)


def build_constitutional_fidelity_view() -> ConstitutionalFidelityView:
    """Build the bounded Constitutional Fidelity View without repository mutation."""

    classifications = (
        ConstitutionalFidelityClassification(
            name="constitutional authority",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Constitutional authority is determined only by completed constitutional evidence; Fidelity preserves that authority without creating it.",
        ),
        ConstitutionalFidelityClassification(
            name="lawful implementation realization",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Implementation realization is lawful only while it preserves recovered constitutional authority and keeps implementation ownership tied to implementation evidence.",
        ),
        ConstitutionalFidelityClassification(
            name="implementation freedom",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Structural symmetry is neither required nor sufficient; implementation-local freedoms remain lawful when they do not redefine admission, recovery, completion, knowledge, mutation, or stop authority.",
        ),
        ConstitutionalFidelityClassification(
            name="compatibility-only structures",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Compatibility mechanics are lawful while neutral and boundary-preserving, and become unlawful when they decide constitutional authority.",
        ),
        ConstitutionalFidelityClassification(
            name="orchestration-only structures",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Orchestration mechanics are lawful while neutral and boundary-preserving, and cannot become required topology, runtime stages, or authority owners.",
        ),
        ConstitutionalFidelityClassification(
            name="constitutional boundary preservation",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Pressure, admission, orientation, recovery, cross-examination, completion, lawful stop, diagnostic read-only boundaries, presentation vocabulary limits, and Unknown preservation remain protected during realization.",
        ),
        ConstitutionalFidelityClassification(
            name="explicit refusals",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Fidelity refuses implementation owners, implementation slices, constitutional owners, engines, projection grammar, symmetry mapping tables, architecture layers, runtime stages, handoff objects, durable cluster truth from diagnostics, and authority from convenience.",
        ),
        ConstitutionalFidelityClassification(
            name="preserved Unknowns",
            status="known",
            support_level="Direct",
            evidence=FIDELITY_EVIDENCE,
            summary="Unsupported conclusions remain Unknown rather than becoming authority, implementation ownership, topology, projection grammar, or fidelity-specific comparison obligations.",
        ),
    )
    return ConstitutionalFidelityView(
        name="Constitutional Fidelity View",
        compatibility_answer="No.",
        summary="Constitutional Fidelity is the boundary-preserving discipline for lawful realization: completed constitutional evidence authorizes constitutional responsibility, implementation evidence authorizes implementation ownership, and Fidelity guards against collapse between the two.",
        composition=FIDELITY_EVIDENCE,
        classifications=classifications,
        recurring_constitutional_discipline=(
            "Constitutional authority is determined only by completed constitutional evidence.",
            "Implementation ownership is determined only by implementation evidence.",
            "Structural symmetry is neither required nor sufficient.",
            "Implementation realization is lawful only when constitutional authority is preserved.",
            "Implementation-only mechanics remain neutral until they claim, erase, mutate, or relocate constitutional authority.",
            "Compatibility and orchestration remain lawful while preserving constitutional boundaries.",
            "Unsupported conclusions remain Unknown rather than becoming authority.",
        ),
        unknowns=(
            "Whether Asymmetrical Question Construction is a distinct constitutional responsibility or only pressure inside or adjacent to admission remains Unknown.",
            "Whether future implementation should introduce question construction before exact QuestionFamily admission remains Unknown.",
            "Whether bounded ask should ever require inquiry orientation before selected dispatch remains Unknown.",
            "Whether a shared implementation Recovery artifact should ever exist between bounded eligibility and selected answering surfaces remains Unknown.",
            "Whether Cross-Examination and Completion Audit should ever become distinct implementation-visible responsibilities outside diagnostic shape audit remains Unknown.",
            "Whether stop/refusal surfaces should ever be inventoried independently across CLI, admission, orientation, dispatch, and downstream surfaces remains Unknown.",
            "Whether Projection Grammar is recoverable as its own constitutional grammar remains Unknown; reviewed evidence preserves it as explanatory pressure.",
            "Whether Constitutional Fidelity should ever become an implementation-backed public surface remains Unknown.",
            "Whether Relationship Grammar or External Grammar require future fidelity-specific comparison remains Unknown because the characterization did not inspect unrelated constitutional districts.",
        ),
        explicit_refusals=(
            "constitutional recovery",
            "implementation recovery",
            "ownership recovery",
            "implementation mutation",
            "repository mutation",
            "runtime evaluation",
            "fidelity enforcement",
            "architectural redesign",
            "projection recovery",
        ),
        read_only_boundaries=(
            "render only",
            "summarize only",
            "classify only",
            "correlate only",
            "expose preserved Unknowns only",
            "no recording",
            "no event-ledger writes",
            "no cluster mutation",
        ),
        remaining_candidate_views=(
            "Observability Coverage View",
            "Provenance Coverage View",
        ),
    )


def constitutional_fidelity_view_json(view: ConstitutionalFidelityView) -> dict[str, Any]:
    """Return deterministic JSON-ready Constitutional Fidelity View data."""

    return to_plain(view)


def format_constitutional_fidelity_view(view: ConstitutionalFidelityView) -> str:
    """Render the Constitutional Fidelity View for humans."""

    lines = [
        view.name,
        "",
        f"Compatibility answer: {view.compatibility_answer}",
        f"Read-only: {str(view.read_only).lower()}",
        f"Writes event ledger: {str(view.writes_event_ledger).lower()}",
        f"Mutates cluster: {str(view.mutates_cluster).lower()}",
        "",
        "Summary",
        "",
        view.summary,
        "",
        "Classifications",
        "",
    ]
    for classification in view.classifications:
        evidence = ", ".join(classification.evidence)
        lines.append(
            f"* {classification.name}: {classification.status} ({classification.support_level}) - {classification.summary} Evidence: {evidence}"
        )
    lines.extend(["", "Recurring constitutional discipline", ""])
    lines.extend(f"* {item}" for item in view.recurring_constitutional_discipline)
    lines.extend(["", "Preserved Unknowns", ""])
    lines.extend(f"* {unknown}" for unknown in view.unknowns)
    lines.extend(["", "Explicit refusals", ""])
    lines.extend(f"* {refusal}" for refusal in view.explicit_refusals)
    lines.extend(["", "Read-only boundaries", ""])
    lines.extend(f"* {boundary}" for boundary in view.read_only_boundaries)
    lines.extend(["", "Remaining candidate views", ""])
    lines.extend(f"* {candidate}" for candidate in view.remaining_candidate_views)
    return "\n".join(lines)
