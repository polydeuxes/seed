"""Implementation-local Constitutional View Selection boundary.

Selection consumes only deterministic question and capability projections, performs
exact comparison, preserves unsupported uncertainty, and produces one immutable
SelectedConstitutionalViews artifact for Constitutional View Composition.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable
from typing import Any

from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion
from seed_runtime.constitutional_fidelity_view import (
    ConstitutionalFidelityView,
    build_constitutional_fidelity_view,
)
from seed_runtime.constitutional_governance_view import (
    ConstitutionalGovernanceView,
    build_constitutional_governance_view,
)
from seed_runtime.constitutional_process_view import (
    ConstitutionalProcessView,
    build_constitutional_process_view,
)
from seed_runtime.constitutional_view_composition import (
    CompositionOutputFormat,
    ConstitutionalViewCompositionRequest,
    constitutional_view_composition_request,
)
from seed_runtime.read_model_ownership import (
    CONSTITUTIONAL_READ_MODEL_CONTRACTS,
    ConstitutionalReadModelContract,
    ReadModelViewRegistration,
    constitutional_read_model_registration,
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


def _selection_keys_from_bounded_question(
    bounded_question: BoundedConstitutionalQuestion,
) -> tuple[str, ...]:
    """Return only exact caller-declared selection keys, without interpretation."""

    keys: list[str] = []
    for field_name, field_value in bounded_question.caller_supplied_fields:
        if field_name.startswith("selection_key:"):
            key = field_name.removeprefix("selection_key:")
            if key:
                keys.append(key)
        elif field_name == "selection_key" and field_value:
            keys.append(field_value)
    return tuple(dict.fromkeys(keys))


def project_constitutional_question(
    bounded_question: BoundedConstitutionalQuestion,
) -> ConstitutionalQuestionProjection:
    """Deterministically project one bounded question for Selection.

    Projection preserves the bounded-question identity, carries only exact
    caller-declared selection keys, and maps bounded-question uncertainty and
    unknowns into Selection's existing uncertainty channel. It performs no
    capability projection, view selection, composition, persistence, ledger
    write, cluster mutation, semantic matching, or natural-language inference.
    """

    uncertainty = (
        *bounded_question.uncertainty,
        *(f"unknown: {unknown}" for unknown in bounded_question.unknowns),
    )
    return ConstitutionalQuestionProjection(
        bounded_question_id=bounded_question.bounded_question_id,
        selection_keys=_selection_keys_from_bounded_question(bounded_question),
        uncertainty=uncertainty,
        read_only=bounded_question.read_only,
        mutates_cluster=bounded_question.mutates_cluster,
        writes_event_ledger=bounded_question.writes_event_ledger,
    )


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




ConstitutionalCapabilitySource = (
    ConstitutionalProcessView | ConstitutionalGovernanceView | ConstitutionalFidelityView
)


_CONSTITUTIONAL_VIEW_BUILDERS: dict[str, Callable[[], ConstitutionalCapabilitySource]] = {
    "constitutional_process": build_constitutional_process_view,
    "constitutional_governance": build_constitutional_governance_view,
    "constitutional_fidelity": build_constitutional_fidelity_view,
}


def _capability_keys_from_source(view: ConstitutionalCapabilitySource) -> tuple[str, ...]:
    """Return exact implementation-supported keys exposed by a view artifact."""

    keys: list[str] = []
    if isinstance(view, ConstitutionalProcessView) and view.stages:
        keys.append("process")
    if isinstance(view, ConstitutionalGovernanceView) and view.relationships:
        keys.append("governance")
    if isinstance(view, ConstitutionalFidelityView) and view.classifications:
        keys.append("fidelity")
    return tuple(dict.fromkeys(keys))


def _projection_for_capability_source(
    *,
    contract: ConstitutionalReadModelContract,
    registration: ReadModelViewRegistration,
    view: ConstitutionalCapabilitySource | None,
) -> ConstitutionalCapabilityProjection:
    """Project one registered constitutional source without mutating its owners."""

    if view is None:
        return ConstitutionalCapabilityProjection(
            registered_view_name=registration.name,
            capability_keys=(),
            compatibility_answer="Unknown.",
            read_only=contract.read_only and registration.read_only,
            mutates_cluster=contract.mutates_cluster,
            writes_event_ledger=contract.writes_event_ledger,
        )

    return ConstitutionalCapabilityProjection(
        registered_view_name=registration.name,
        capability_keys=_capability_keys_from_source(view),
        compatibility_answer=getattr(view, "compatibility_answer", "Unknown."),
        read_only=contract.read_only and registration.read_only and view.read_only,
        mutates_cluster=contract.mutates_cluster or view.mutates_cluster,
        writes_event_ledger=contract.writes_event_ledger or view.writes_event_ledger,
    )


def project_constitutional_capabilities(
    contracts: tuple[ConstitutionalReadModelContract, ...] = CONSTITUTIONAL_READ_MODEL_CONTRACTS,
    registrations: tuple[ReadModelViewRegistration, ...] | None = None,
    view_builders: dict[str, Callable[[], ConstitutionalCapabilitySource]] = _CONSTITUTIONAL_VIEW_BUILDERS,
) -> tuple[ConstitutionalCapabilityProjection, ...]:
    """Regenerate deterministic capability projections from registered sources only.

    The helper consumes existing constitutional read-model contracts, their
    existing registrations, and immutable constitutional view builders. It
    preserves exact capability keys exposed by those view artifact types and
    performs no Selection, Composition, persistence, ledger writes, cluster
    mutation, registration repair, semantic inference, or operator-testimony
    interpretation.
    """

    registration_by_name = {
        registration.name: registration for registration in registrations or ()
    }
    projections: list[ConstitutionalCapabilityProjection] = []
    seen_names: set[str] = set()

    for contract in contracts:
        registration = registration_by_name.get(
            contract.name, constitutional_read_model_registration(contract)
        )
        if registration.name in seen_names:
            continue
        seen_names.add(registration.name)

        builder = view_builders.get(contract.name)
        view = builder() if builder is not None else None
        projections.append(
            _projection_for_capability_source(
                contract=contract, registration=registration, view=view
            )
        )

    return tuple(projections)


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
