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
