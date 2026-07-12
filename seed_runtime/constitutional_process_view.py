"""Read-only Constitutional Process View composed from existing evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from seed_runtime.serialization import to_plain

StageStatus = Literal["known", "unknown"]


@dataclass(frozen=True)
class ConstitutionalProcessStage:
    """One preserved stage in the constitutional process view."""

    name: str
    status: StageStatus
    support_level: str
    evidence: tuple[str, ...]
    summary: str


@dataclass(frozen=True)
class ConstitutionalProcessView:
    """Read-only view over the existing constitutional process evidence."""

    name: str
    compatibility_answer: str
    composition: tuple[str, ...]
    stages: tuple[ConstitutionalProcessStage, ...]
    unknowns: tuple[str, ...]
    remaining_candidate_views: tuple[str, ...]
    read_only: bool = True
    mutates_cluster: bool = False
    writes_event_ledger: bool = False


PROCESS_EVIDENCE: tuple[str, ...] = (
    "constitutional_process_reconciliation.md",
    "constitutional_question_grammar_characterization.md",
    "constitutional_grammar_topology_survey.md",
    "constitutional_grammar_cross_examination.md",
    "constitutional_grammar_district_completion_audit.md",
    "orientation_guided_recovery_methodology_characterization.md",
    "constitutional_cross_examination_admissibility_handoff_investigation.md",
    "constitutional_grammar_recovery_discipline_characterization.md",
    "constitutional_bounded_investigation_characterization.md",
    "inquiry_eligibility_characterization.md",
)


def build_constitutional_process_view() -> ConstitutionalProcessView:
    """Build the bounded Constitutional Process View without repository mutation."""

    stages = (
        ConstitutionalProcessStage(
            name="Pressure",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_process_reconciliation.md",
                "constitutional_question_grammar_characterization.md",
            ),
            summary="Possible questions appear as pressure without becoming command authority.",
        ),
        ConstitutionalProcessStage(
            name="Lawful Question",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_process_reconciliation.md",
                "constitutional_question_grammar_characterization.md",
                "inquiry_eligibility_characterization.md",
            ),
            summary="Question Grammar admits or refuses bounded inquiry under evidence, authority, unknown, stop, and confidence limits.",
        ),
        ConstitutionalProcessStage(
            name="Orientation",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_process_reconciliation.md",
                "orientation_guided_recovery_methodology_characterization.md",
            ),
            summary="Orientation receives an admitted inquiry question and locates lawful attention before recovery.",
        ),
        ConstitutionalProcessStage(
            name="Recovery",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_process_reconciliation.md",
                "constitutional_grammar_recovery_discipline_characterization.md",
            ),
            summary="Recovery changes constitutional or implementation visibility only where admitted and oriented evidence exposes a lawful boundary.",
        ),
        ConstitutionalProcessStage(
            name="Cross-Examination",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_process_reconciliation.md",
                "constitutional_grammar_cross_examination.md",
                "constitutional_cross_examination_admissibility_handoff_investigation.md",
            ),
            summary="Cross-examination tests recovered neighborhoods for dependency, artifact consumption, responsibility collapse, and required distinction.",
        ),
        ConstitutionalProcessStage(
            name="Completion Audit",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_process_reconciliation.md",
                "constitutional_grammar_district_completion_audit.md",
            ),
            summary="Completion audit decides whether the bounded district is complete for currently visible evidence while preserving adjacent pressure.",
        ),
        ConstitutionalProcessStage(
            name="Lawful Stop",
            status="known",
            support_level="Direct",
            evidence=(
                "constitutional_process_reconciliation.md",
                "constitutional_grammar_recovery_discipline_characterization.md",
            ),
            summary="Lawful stop is preserved where further movement would require unsupported recovery, invention, mutation, or overclaiming.",
        ),
    )
    return ConstitutionalProcessView(
        name="Constitutional Process View",
        compatibility_answer="No.",
        composition=PROCESS_EVIDENCE,
        stages=stages,
        unknowns=(
            "Whether every constitutional inquiry starts only as Pressure remains unknown.",
            "Whether every Recovery requires a separate Cross-Examination artifact remains unknown.",
            "Whether every Cross-Examination requires a separate Completion Audit remains unknown.",
            "Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains unknown.",
            "Whether a single named constitutional process owner exists remains unknown.",
        ),
        remaining_candidate_views=(
            "Governance View",
            "Fidelity View",
            "Observability Coverage View",
            "Provenance Coverage View",
        ),
    )


def constitutional_process_view_json(view: ConstitutionalProcessView) -> dict[str, Any]:
    """Return deterministic JSON-ready Constitutional Process View data."""

    return to_plain(view)


def format_constitutional_process_view(view: ConstitutionalProcessView) -> str:
    """Render the Constitutional Process View for humans."""

    lines = [
        view.name,
        "",
        f"Compatibility answer: {view.compatibility_answer}",
        f"Read-only: {str(view.read_only).lower()}",
        f"Writes event ledger: {str(view.writes_event_ledger).lower()}",
        f"Mutates cluster: {str(view.mutates_cluster).lower()}",
        "",
        "Stages",
        "",
    ]
    for stage in view.stages:
        evidence = ", ".join(stage.evidence)
        lines.append(
            f"* {stage.name}: {stage.status} ({stage.support_level}) - {stage.summary} Evidence: {evidence}"
        )
    lines.extend(["", "Preserved Unknowns", ""])
    lines.extend(f"* {unknown}" for unknown in view.unknowns)
    lines.extend(["", "Remaining candidate views", ""])
    lines.extend(f"* {candidate}" for candidate in view.remaining_candidate_views)
    return "\n".join(lines)
