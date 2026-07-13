"""Deterministic end-to-end constitutional pipeline invocation.

This module owns only ordered invocation and typed handoff between the existing
constitutional pipeline stages. It preserves explicit caller inputs and returns
stage artifacts for inspection without interpreting unrestricted language,
discovering capabilities, persisting state, writing ledgers, or mutating cluster
state.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable, Mapping
from typing import Any

from seed_runtime.bounded_constitutional_question import (
    BoundedConstitutionalQuestion,
    produce_bounded_constitutional_question,
)
from seed_runtime.constitutional_view_composition import (
    CompositionOutputFormat,
    ConstitutionalViewCompositionArtifact,
    ConstitutionalViewCompositionRequest,
    build_constitutional_view_composition,
)
from seed_runtime.constitutional_view_selection import (
    ConstitutionalCapabilityProjection,
    ConstitutionalCapabilitySource,
    ConstitutionalQuestionProjection,
    SelectedConstitutionalViews,
    project_constitutional_capabilities,
    project_constitutional_question,
    select_constitutional_views,
    selected_constitutional_views_to_composition_request,
)
from seed_runtime.read_model_ownership import (
    CONSTITUTIONAL_READ_MODEL_CONTRACTS,
    ConstitutionalReadModelContract,
    ReadModelViewRegistration,
)
from seed_runtime.serialization import to_plain


@dataclass(frozen=True)
class ConstitutionalPipelineRequest:
    """Explicit immutable request for one constitutional pipeline invocation.

    The request mirrors the bounded-question producer's explicit inputs and the
    existing composition adapter's explicit formatting inputs. Optional immutable
    capability sources are accepted for deterministic tests or callers that need
    to supply already-known registration evidence; the invocation does not
    discover, repair, or infer capability evidence.
    """

    operator_inquiry: str
    inquiry_provenance: str
    bounded_question: str
    constitutional_intent: str
    scope_status: str
    uncertainty: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    bounded_question_id: str | None = None
    caller_supplied_fields: tuple[tuple[str, str], ...] = ()
    capability_contracts: tuple[ConstitutionalReadModelContract, ...] = CONSTITUTIONAL_READ_MODEL_CONTRACTS
    capability_registrations: tuple[ReadModelViewRegistration, ...] | None = None
    capability_view_builders: Mapping[str, Callable[[], ConstitutionalCapabilitySource]] | None = None
    composition_purpose: str = "bounded_explanation"
    output_format: CompositionOutputFormat = "human"




@dataclass(frozen=True)
class ConstitutionalPipelineProvenanceExplanation:
    """Deterministic explanation assembled from completed pipeline artifacts only."""

    bounded_question_id: str
    inquiry_provenance: str
    operator_inquiry_testimony: str
    question_selection_keys: tuple[str, ...]
    available_capability_keys: tuple[tuple[str, tuple[str, ...]], ...]
    matched_keys: tuple[str, ...]
    unsupported_question_keys: tuple[str, ...]
    selected_views: tuple[str, ...]
    unselected_or_unavailable_views: tuple[str, ...]
    selection_uncertainty: tuple[str, ...]
    empty_selection_explanation: str
    composition_contributors: tuple[str, ...]
    composition_unknowns: tuple[str, ...]
    composition_refusals: tuple[str, ...]
    read_only: bool
    writes_event_ledger: bool
    mutates_cluster: bool
    testimony_boundary: str = "operator testimony is preserved as evidence, not established fact"
    explanation_boundary: str = (
        "provenance explanation reports existing typed handoffs only; it does not "
        "perform projection, selection, composition, verification, persistence, or mutation"
    )


def explain_constitutional_pipeline_provenance(
    result: ConstitutionalPipelineResult,
) -> ConstitutionalPipelineProvenanceExplanation:
    """Explain why completed pipeline artifacts produced the selected views.

    The explanation reads only the artifacts already present on one completed
    ``ConstitutionalPipelineResult``. It performs no pipeline stages, capability
    discovery, semantic matching, persistence, event-ledger write, or cluster
    mutation.
    """

    question_keys = result.question_projection.selection_keys
    capability_keys_by_view = tuple(
        (capability.registered_view_name, capability.capability_keys)
        for capability in result.capability_projection
    )
    flat_capability_keys = {
        key
        for capability in result.capability_projection
        for key in capability.capability_keys
    }
    matched_keys = tuple(key for key in question_keys if key in flat_capability_keys)
    unsupported_keys = tuple(key for key in question_keys if key not in flat_capability_keys)
    unknown_capabilities = tuple(
        capability.registered_view_name
        for capability in result.capability_projection
        if capability.compatibility_answer == "Unknown." and not capability.capability_keys
    )

    unselected_or_unavailable: list[str] = []
    if not question_keys:
        unselected_or_unavailable.append("absent: no explicit question selection key was supplied")
    for key in unsupported_keys:
        reason = f"unsupported: {key} did not match any projected capability key"
        if unknown_capabilities:
            reason += "; missing capability evidence: " + ", ".join(unknown_capabilities)
        unselected_or_unavailable.append(reason)
    for capability_name in unknown_capabilities:
        unselected_or_unavailable.append(
            f"unknown: {capability_name} projected no capability keys because capability evidence was Unknown"
        )

    empty_selection_explanation = ""
    if not result.selection.selected_view_names:
        if not question_keys:
            empty_selection_explanation = "No explicit selection key was supplied; empty selection is not verified irrelevance."
        elif unsupported_keys:
            empty_selection_explanation = "No selected view was produced because explicit keys did not match projected capability keys; this is not verified irrelevance."
        elif result.selection.selection_uncertainty:
            empty_selection_explanation = "Selection preserved uncertainty and produced no selected view; this is not verified irrelevance."
        else:
            empty_selection_explanation = "Selection produced no selected view from the completed artifacts; this is not verified irrelevance."

    stage_read_only = (
        result.bounded_question.read_only,
        result.question_projection.read_only,
        *(capability.read_only for capability in result.capability_projection),
        result.selection.read_only,
        result.composition.read_only,
    )
    stage_writes_event_ledger = (
        result.bounded_question.writes_event_ledger,
        result.question_projection.writes_event_ledger,
        *(capability.writes_event_ledger for capability in result.capability_projection),
        result.selection.writes_event_ledger,
        result.composition.writes_event_ledger,
    )
    stage_mutates_cluster = (
        result.bounded_question.mutates_cluster,
        result.question_projection.mutates_cluster,
        *(capability.mutates_cluster for capability in result.capability_projection),
        result.selection.mutates_cluster,
        result.composition.mutates_cluster,
    )

    return ConstitutionalPipelineProvenanceExplanation(
        bounded_question_id=result.bounded_question.bounded_question_id,
        inquiry_provenance=result.bounded_question.inquiry_provenance,
        operator_inquiry_testimony=result.bounded_question.operator_inquiry,
        question_selection_keys=question_keys,
        available_capability_keys=capability_keys_by_view,
        matched_keys=matched_keys,
        unsupported_question_keys=unsupported_keys,
        selected_views=result.selection.selected_view_names,
        unselected_or_unavailable_views=tuple(unselected_or_unavailable),
        selection_uncertainty=result.selection.selection_uncertainty,
        empty_selection_explanation=empty_selection_explanation,
        composition_contributors=tuple(view.name for view in result.composition.contributing_views),
        composition_unknowns=result.composition.preserved_unknowns,
        composition_refusals=result.composition.preserved_refusals,
        read_only=all(stage_read_only),
        writes_event_ledger=any(stage_writes_event_ledger),
        mutates_cluster=any(stage_mutates_cluster),
    )


@dataclass(frozen=True)
class ConstitutionalPipelineResult:
    """Inspectable immutable result preserving each existing stage artifact."""

    bounded_question: BoundedConstitutionalQuestion
    question_projection: ConstitutionalQuestionProjection
    capability_projection: tuple[ConstitutionalCapabilityProjection, ...]
    selection: SelectedConstitutionalViews
    composition_request: ConstitutionalViewCompositionRequest
    composition: ConstitutionalViewCompositionArtifact


def invoke_constitutional_pipeline(
    request: ConstitutionalPipelineRequest,
) -> ConstitutionalPipelineResult:
    """Invoke the existing constitutional stages in deterministic order."""

    bounded_question = produce_bounded_constitutional_question(
        operator_inquiry=request.operator_inquiry,
        inquiry_provenance=request.inquiry_provenance,
        bounded_question=request.bounded_question,
        constitutional_intent=request.constitutional_intent,
        scope_status=request.scope_status,
        uncertainty=request.uncertainty,
        unknowns=request.unknowns,
        bounded_question_id=request.bounded_question_id,
        caller_supplied_fields=dict(request.caller_supplied_fields),
    )
    question_projection = project_constitutional_question(bounded_question)
    if request.capability_view_builders is None:
        capability_projection = project_constitutional_capabilities(
            request.capability_contracts,
            request.capability_registrations,
        )
    else:
        capability_projection = project_constitutional_capabilities(
            request.capability_contracts,
            request.capability_registrations,
            dict(request.capability_view_builders),
        )
    selection = select_constitutional_views(
        question_projection=question_projection,
        capability_projections=capability_projection,
    )
    composition_request = selected_constitutional_views_to_composition_request(
        selection,
        composition_purpose=request.composition_purpose,
        output_format=request.output_format,
    )
    composition = build_constitutional_view_composition(composition_request)

    return ConstitutionalPipelineResult(
        bounded_question=bounded_question,
        question_projection=question_projection,
        capability_projection=capability_projection,
        selection=selection,
        composition_request=composition_request,
        composition=composition,
    )


def constitutional_pipeline_result_json(
    result: ConstitutionalPipelineResult,
) -> dict[str, Any]:
    """Return deterministic JSON-ready data for the complete pipeline result."""

    payload = to_plain(result)
    payload["provenance_explanation"] = to_plain(explain_constitutional_pipeline_provenance(result))
    return payload


def format_constitutional_pipeline_result(result: ConstitutionalPipelineResult) -> str:
    """Render the complete constitutional pipeline result for humans."""

    explanation = explain_constitutional_pipeline_provenance(result)
    lines = [
        "Constitutional Pipeline",
        "",
        "Operator input testimony",
        "",
        f"Operator inquiry supplied: {result.bounded_question.operator_inquiry}",
        f"Inquiry provenance: {result.bounded_question.inquiry_provenance}",
        f"Testimony status: {result.bounded_question.testimony_status}",
        "",
        "Bounded question",
        "",
        f"ID: {result.bounded_question.bounded_question_id}",
        f"Question: {result.bounded_question.bounded_question}",
        f"Constitutional intent: {result.bounded_question.constitutional_intent}",
        f"Scope status: {result.bounded_question.scope_status}",
        f"Uncertainty: {', '.join(result.bounded_question.uncertainty) or 'none'}",
        f"Unknowns: {', '.join(result.bounded_question.unknowns) or 'none'}",
        "",
        "Question projection",
        "",
        f"Selection keys: {', '.join(result.question_projection.selection_keys) or 'none'}",
        f"Read-only: {str(result.question_projection.read_only).lower()}",
        f"Writes event ledger: {str(result.question_projection.writes_event_ledger).lower()}",
        f"Mutates cluster: {str(result.question_projection.mutates_cluster).lower()}",
        "",
        "Capability projection",
        "",
    ]
    for capability in result.capability_projection:
        lines.append(
            f"* {capability.registered_view_name}: keys={', '.join(capability.capability_keys) or 'none'}; "
            f"compatibility={capability.compatibility_answer}; read_only={str(capability.read_only).lower()}; "
            f"writes_event_ledger={str(capability.writes_event_ledger).lower()}; "
            f"mutates_cluster={str(capability.mutates_cluster).lower()}"
        )
    lines.extend([
        "",
        "Selected constitutional views",
        "",
        f"Selected views: {', '.join(result.selection.selected_view_names) or 'none'}",
        f"Selection uncertainty: {', '.join(result.selection.selection_uncertainty) or 'none'}",
        f"Compatibility answer: {result.selection.compatibility_answer}",
        f"Read-only: {str(result.selection.read_only).lower()}",
        f"Writes event ledger: {str(result.selection.writes_event_ledger).lower()}",
        f"Mutates cluster: {str(result.selection.mutates_cluster).lower()}",
        "",
        "Composition result",
        "",
        f"Requested views: {', '.join(result.composition_request.requested_views) or 'none'}",
        f"Purpose: {result.composition_request.composition_purpose}",
        f"Compatibility answer: {result.composition.compatibility_answer}",
        f"Read-only: {str(result.composition.read_only).lower()}",
        f"Writes event ledger: {str(result.composition.writes_event_ledger).lower()}",
        f"Mutates cluster: {str(result.composition.mutates_cluster).lower()}",
        "",
        "Provenance explanation",
        "",
        "Why these views were selected",
        f"Question selection keys: {', '.join(explanation.question_selection_keys) or 'none'}",
        "Available capability keys: "
        + (
            "; ".join(
                f"{name}=[{', '.join(keys) or 'none'}]"
                for name, keys in explanation.available_capability_keys
            )
            or "none"
        ),
        f"Matched keys: {', '.join(explanation.matched_keys) or 'none'}",
        f"Selected views explained by exact matches: {', '.join(explanation.selected_views) or 'none'}",
        "",
        "Why requested keys were unsupported",
    ])
    lines.extend(f"* {item}" for item in explanation.unselected_or_unavailable_views)
    if not explanation.unselected_or_unavailable_views:
        lines.append("* none")
    if explanation.empty_selection_explanation:
        lines.append(f"* {explanation.empty_selection_explanation}")
    lines.extend([
        "",
        "Remaining uncertainty",
    ])
    lines.extend(f"* {item}" for item in explanation.selection_uncertainty)
    if not explanation.selection_uncertainty:
        lines.append("* none")
    lines.extend([
        "",
        "Composition contributors",
    ])
    lines.extend(f"* {item}" for item in explanation.composition_contributors)
    if not explanation.composition_contributors:
        lines.append("* none")
    lines.extend([
        "",
        "Preserved Unknowns",
        "",
    ])
    lines.extend(f"* {item}" for item in result.composition.preserved_unknowns)
    if not result.composition.preserved_unknowns:
        lines.append("* none")
    lines.extend(["", "Preserved refusals", ""])
    lines.extend(f"* {item}" for item in result.composition.preserved_refusals)
    if not result.composition.preserved_refusals:
        lines.append("* none")
    lines.extend(["", "Boundary", "", "* operator inquiry is reported as supplied testimony, not established fact", "* no event-ledger writes", "* no cluster mutation"])
    return "\n".join(lines)
