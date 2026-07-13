"""Implementation-local Constitutional View Selection boundary.

Selection consumes only deterministic question and capability projections, performs
exact comparison, preserves unsupported uncertainty, and produces one immutable
SelectedConstitutionalViews artifact for Constitutional View Composition.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from seed_runtime.constitutional_view_composition import (
    CompositionOutputFormat,
    ConstitutionalViewCompositionRequest,
    constitutional_view_composition_request,
)
from seed_runtime.serialization import to_plain


@dataclass(frozen=True)
class ConstitutionalQuestionProjection:
    """Deterministic selection input projected from a bounded question.

    The projection preserves only the bounded-question identity and exact
    already-projected selection keys. It does not carry a raw question, reason
    semantically, discover evidence, plan, orchestrate, or mutate state.
    """

    bounded_question_id: str
    selection_keys: tuple[str, ...]
    uncertainty: tuple[str, ...] = ()
    read_only: bool = True
    mutates_cluster: bool = False
    writes_event_ledger: bool = False


@dataclass(frozen=True)
class ConstitutionalCapabilityProjection:
    """Deterministic selection input projected from one registered view.

    The projection preserves the registered view name and exact already-projected
    capability keys. It does not expose the immutable constitutional view itself
    and does not author constitutional knowledge.
    """

    registered_view_name: str
    capability_keys: tuple[str, ...]
    compatibility_answer: str = "No."
    read_only: bool = True
    mutates_cluster: bool = False
    writes_event_ledger: bool = False


@dataclass(frozen=True)
class SelectedConstitutionalViews:
    """Single immutable artifact owned by ConstitutionalViewSelection."""

    bounded_question_id: str
    selected_view_names: tuple[str, ...]
    selection_uncertainty: tuple[str, ...]
    compatibility_answer: str
    read_only_boundaries: tuple[str, ...]
    read_only: bool = True
    mutates_cluster: bool = False
    writes_event_ledger: bool = False


def select_constitutional_views(
    *,
    question_projection: ConstitutionalQuestionProjection,
    capability_projections: tuple[ConstitutionalCapabilityProjection, ...],
) -> SelectedConstitutionalViews:
    """Select registered view names by deterministic exact-key comparison only."""

    question_keys = set(question_projection.selection_keys)
    selected: list[str] = []
    unsupported_keys = set(question_projection.selection_keys)
    uncertainty = list(question_projection.uncertainty)
    compatibility_answers: list[str] = []

    for capability in capability_projections:
        matched = question_keys.intersection(capability.capability_keys)
        if matched:
            selected.append(capability.registered_view_name)
            unsupported_keys.difference_update(matched)
            compatibility_answers.append(capability.compatibility_answer)

    if unsupported_keys:
        uncertainty.extend(
            f"unsupported selection key: {key}" for key in sorted(unsupported_keys)
        )
    if not selected:
        uncertainty.append("no registered constitutional view matched deterministic projection keys")

    boundary_flags = (
        question_projection.read_only,
        not question_projection.mutates_cluster,
        not question_projection.writes_event_ledger,
        *(
            flag
            for capability in capability_projections
            for flag in (
                capability.read_only,
                not capability.mutates_cluster,
                not capability.writes_event_ledger,
            )
        ),
    )

    return SelectedConstitutionalViews(
        bounded_question_id=question_projection.bounded_question_id,
        selected_view_names=tuple(dict.fromkeys(selected)),
        selection_uncertainty=tuple(uncertainty),
        compatibility_answer=(
            "No."
            if compatibility_answers and all(answer == "No." for answer in compatibility_answers)
            else "Unknown."
        ),
        read_only_boundaries=(
            "question projection input only",
            "capability projection input only",
            "exact deterministic key comparison only",
            "preserve unsupported selection uncertainty",
            "registered view names only",
            "no raw question consumption",
            "no immutable constitutional view consumption",
            "no semantic reasoning",
            "no ranking",
            "no heuristics",
            "no planning",
            "no orchestration",
            "no evidence discovery",
            "no constitutional recovery",
            "no repository mutation",
            "no event-ledger writes",
            "no cluster mutation",
        ),
        read_only=all(boundary_flags),
        mutates_cluster=False,
        writes_event_ledger=False,
    )


def selected_constitutional_views_to_composition_request(
    artifact: SelectedConstitutionalViews,
    *,
    composition_purpose: str = "bounded_explanation",
    output_format: CompositionOutputFormat = "human",
) -> ConstitutionalViewCompositionRequest:
    """Wire SelectedConstitutionalViews directly into the existing Composition request."""

    return constitutional_view_composition_request(
        requested_views=artifact.selected_view_names,
        composition_purpose=composition_purpose,
        output_format=output_format,
    )


def selected_constitutional_views_json(
    artifact: SelectedConstitutionalViews,
) -> dict[str, Any]:
    """Return deterministic JSON-ready SelectedConstitutionalViews data."""

    return to_plain(artifact)
