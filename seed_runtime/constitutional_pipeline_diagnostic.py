"""Read-only diagnostic observation for the complete constitutional pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from seed_runtime.constitutional_pipeline import (
    ConstitutionalPipelineRequest,
    ConstitutionalPipelineResult,
    invoke_constitutional_pipeline,
)
from seed_runtime.serialization import to_plain

StageStatus = Literal["complete", "empty", "unsupported", "unknown", "refused"]


@dataclass(frozen=True)
class ConstitutionalPipelineStageDiagnostic:
    pipeline_stage: str
    status: StageStatus
    artifact_identity: str
    key_count: int = 0
    selected_view_count: int = 0
    unknown_count: int = 0
    refusal_count: int = 0
    uncertainty: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    refusals: tuple[str, ...] = ()
    selected_views: tuple[str, ...] = ()
    unsupported_keys: tuple[str, ...] = ()
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    authority_claim: bool = False


@dataclass(frozen=True)
class ConstitutionalPipelineDiagnosticResult:
    name: str
    pipeline_request: ConstitutionalPipelineRequest
    pipeline_result: ConstitutionalPipelineResult
    stages: tuple[ConstitutionalPipelineStageDiagnostic, ...]
    stage_order: tuple[str, ...]
    selected_views: tuple[str, ...]
    no_view_selection_reasons: tuple[str, ...]
    composition_compatibility_answer: str
    pipeline_read_only: bool
    event_ledger_status: str
    cluster_mutation_status: str
    recordability: str
    testimony_boundary: str
    diagnostic_boundary: str
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False


def build_constitutional_pipeline_diagnostic(
    request: ConstitutionalPipelineRequest,
) -> ConstitutionalPipelineDiagnosticResult:
    """Invoke the existing pipeline once and classify its returned artifacts."""

    return constitutional_pipeline_diagnostic_from_result(
        request=request,
        result=invoke_constitutional_pipeline(request),
    )


def constitutional_pipeline_diagnostic_from_result(
    *,
    request: ConstitutionalPipelineRequest,
    result: ConstitutionalPipelineResult,
) -> ConstitutionalPipelineDiagnosticResult:
    """Classify an existing complete pipeline result without re-running stages."""

    stages = (
        _bounded_question_stage(result),
        _question_projection_stage(result),
        _capability_projection_stage(result),
        _selection_stage(result),
        _composition_request_stage(result),
        _composition_stage(result),
    )
    pipeline_read_only = all(stage.read_only for stage in stages)
    writes_event_ledger = any(stage.writes_event_ledger for stage in stages)
    mutates_cluster = any(stage.mutates_cluster for stage in stages)
    no_view_reasons = tuple(
        item for item in result.selection.selection_uncertainty
        if item.startswith("unsupported selection key:")
        or item == "no registered constitutional view matched deterministic projection keys"
    )
    return ConstitutionalPipelineDiagnosticResult(
        name="constitutional_pipeline_diagnostic",
        pipeline_request=request,
        pipeline_result=result,
        stages=stages,
        stage_order=tuple(stage.pipeline_stage for stage in stages),
        selected_views=result.selection.selected_view_names,
        no_view_selection_reasons=no_view_reasons,
        composition_compatibility_answer=result.composition.compatibility_answer,
        pipeline_read_only=pipeline_read_only,
        event_ledger_status="writes_event_ledger=true" if writes_event_ledger else "no event-ledger writes",
        cluster_mutation_status="mutates_cluster=true" if mutates_cluster else "no cluster mutation",
        recordability="read-only non-recording diagnostic; record_scope=none",
        testimony_boundary="operator testimony is preserved as evidence, not established fact",
        diagnostic_boundary="observes typed pipeline artifacts only; does not own stage algorithms or constitutional authority",
        read_only=pipeline_read_only,
        writes_event_ledger=writes_event_ledger,
        mutates_cluster=mutates_cluster,
    )


def _bounded_question_stage(result: ConstitutionalPipelineResult) -> ConstitutionalPipelineStageDiagnostic:
    artifact = result.bounded_question
    status: StageStatus = "unknown" if artifact.unknowns else "complete"
    return ConstitutionalPipelineStageDiagnostic(
        pipeline_stage="bounded_question",
        status=status,
        artifact_identity=artifact.bounded_question_id,
        uncertainty=artifact.uncertainty,
        unknowns=artifact.unknowns,
        unknown_count=len(artifact.unknowns),
        read_only=artifact.read_only,
        writes_event_ledger=artifact.writes_event_ledger,
        mutates_cluster=artifact.mutates_cluster,
    )


def _question_projection_stage(result: ConstitutionalPipelineResult) -> ConstitutionalPipelineStageDiagnostic:
    artifact = result.question_projection
    status: StageStatus = "empty" if not artifact.selection_keys else "complete"
    return ConstitutionalPipelineStageDiagnostic(
        pipeline_stage="question_projection",
        status=status,
        artifact_identity=artifact.bounded_question_id,
        key_count=len(artifact.selection_keys),
        uncertainty=artifact.uncertainty,
        read_only=artifact.read_only,
        writes_event_ledger=artifact.writes_event_ledger,
        mutates_cluster=artifact.mutates_cluster,
    )


def _capability_projection_stage(result: ConstitutionalPipelineResult) -> ConstitutionalPipelineStageDiagnostic:
    projections = result.capability_projection
    unknowns = tuple(p.registered_view_name for p in projections if p.compatibility_answer == "Unknown.")
    key_count = sum(len(p.capability_keys) for p in projections)
    status: StageStatus = "unknown" if unknowns else ("empty" if key_count == 0 else "complete")
    return ConstitutionalPipelineStageDiagnostic(
        pipeline_stage="capability_projection",
        status=status,
        artifact_identity=f"capability_projections:{len(projections)}",
        key_count=key_count,
        unknowns=unknowns,
        unknown_count=len(unknowns),
        read_only=all(p.read_only for p in projections),
        writes_event_ledger=any(p.writes_event_ledger for p in projections),
        mutates_cluster=any(p.mutates_cluster for p in projections),
    )


def _selection_stage(result: ConstitutionalPipelineResult) -> ConstitutionalPipelineStageDiagnostic:
    artifact = result.selection
    unsupported = tuple(
        item.removeprefix("unsupported selection key: ")
        for item in artifact.selection_uncertainty
        if item.startswith("unsupported selection key: ")
    )
    if artifact.selected_view_names:
        status: StageStatus = "complete"
    elif unsupported:
        status = "unsupported"
    else:
        status = "empty"
    return ConstitutionalPipelineStageDiagnostic(
        pipeline_stage="selection",
        status=status,
        artifact_identity=artifact.bounded_question_id,
        selected_view_count=len(artifact.selected_view_names),
        uncertainty=artifact.selection_uncertainty,
        selected_views=artifact.selected_view_names,
        unsupported_keys=unsupported,
        read_only=artifact.read_only,
        writes_event_ledger=artifact.writes_event_ledger,
        mutates_cluster=artifact.mutates_cluster,
    )


def _composition_request_stage(result: ConstitutionalPipelineResult) -> ConstitutionalPipelineStageDiagnostic:
    artifact = result.composition_request
    return ConstitutionalPipelineStageDiagnostic(
        pipeline_stage="composition_request",
        status="empty" if not artifact.requested_views else "complete",
        artifact_identity=f"purpose:{artifact.composition_purpose}",
        selected_view_count=len(artifact.requested_views),
        selected_views=artifact.requested_views,
    )


def _composition_stage(result: ConstitutionalPipelineResult) -> ConstitutionalPipelineStageDiagnostic:
    artifact = result.composition
    if artifact.preserved_refusals:
        status: StageStatus = "refused"
    elif artifact.preserved_unknowns or artifact.compatibility_answer == "Unknown.":
        status = "unknown"
    elif not artifact.contributing_views:
        status = "empty"
    else:
        status = "complete"
    return ConstitutionalPipelineStageDiagnostic(
        pipeline_stage="composition",
        status=status,
        artifact_identity=artifact.name,
        selected_view_count=len(artifact.contributing_views),
        unknown_count=len(artifact.preserved_unknowns),
        refusal_count=len(artifact.preserved_refusals),
        unknowns=artifact.preserved_unknowns,
        refusals=artifact.preserved_refusals,
        read_only=artifact.read_only,
        writes_event_ledger=artifact.writes_event_ledger,
        mutates_cluster=artifact.mutates_cluster,
    )


def constitutional_pipeline_diagnostic_json(
    result: ConstitutionalPipelineDiagnosticResult,
) -> dict[str, Any]:
    return to_plain(result)


def format_constitutional_pipeline_diagnostic(
    result: ConstitutionalPipelineDiagnosticResult,
) -> str:
    lines = [
        "Constitutional Pipeline Diagnostic",
        "",
        "Boundary",
        f"- recordability: {result.recordability}",
        f"- event ledger: {result.event_ledger_status}",
        f"- cluster mutation: {result.cluster_mutation_status}",
        f"- testimony: {result.testimony_boundary}",
        f"- diagnostic: {result.diagnostic_boundary}",
        "",
        "Stages",
        "Pipeline stage | Status | Artifact / counts | Uncertainty / Unknown / refusal summary | Read-only / ledger / mutation",
    ]
    for stage in result.stages:
        summary = []
        if stage.key_count:
            summary.append(f"keys={stage.key_count}")
        summary.append(f"selected_views={stage.selected_view_count}")
        summary.append(f"unknowns={stage.unknown_count}")
        summary.append(f"refusals={stage.refusal_count}")
        detail = []
        if stage.uncertainty:
            detail.append("uncertainty=" + "; ".join(stage.uncertainty))
        if stage.unknowns:
            detail.append("unknown=" + "; ".join(stage.unknowns))
        if stage.refusals:
            detail.append("refused=" + "; ".join(stage.refusals))
        if stage.unsupported_keys:
            detail.append("unsupported_keys=" + ", ".join(stage.unsupported_keys))
        lines.append(
            f"{stage.pipeline_stage} | {stage.status} | {stage.artifact_identity}; "
            f"{', '.join(summary)} | {(' | '.join(detail) or 'none')} | "
            f"read_only={str(stage.read_only).lower()} "
            f"writes_event_ledger={str(stage.writes_event_ledger).lower()} "
            f"mutates_cluster={str(stage.mutates_cluster).lower()}"
        )
    lines.extend([
        "",
        f"Selected views: {', '.join(result.selected_views) or 'none'}",
        f"No-view selection reasons: {', '.join(result.no_view_selection_reasons) or 'none'}",
        f"Composition compatibility answer: {result.composition_compatibility_answer}",
        f"Pipeline read-only: {str(result.pipeline_read_only).lower()}",
    ])
    return "\n".join(lines)
