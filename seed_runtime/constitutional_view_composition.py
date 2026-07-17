"""Read-only Constitutional View Composition over registered constitutional views."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from seed_runtime.constitutional_fidelity_view import (
    build_constitutional_fidelity_view,
    constitutional_fidelity_view_json,
)
from seed_runtime.constitutional_governance_view import (
    build_constitutional_governance_view,
    constitutional_governance_view_json,
)
from seed_runtime.constitutional_process_view import (
    build_constitutional_process_view,
    constitutional_process_view_json,
)
from seed_runtime.read_model_ownership import CONSTITUTIONAL_READ_MODEL_CONTRACTS
from seed_runtime.serialization import to_plain

CompositionOutputFormat = Literal["human", "json"]


@dataclass(frozen=True)
class ConstitutionalViewCompositionRequest:
    """Minimum explicit request for bounded constitutional view composition.

    The request owns only explicit registered-view selection, purpose labeling,
    output-format intent, and optional upstream selection limits. It does not
    select views heuristically, discover evidence, reason at runtime, recover
    authority, plan, orchestrate, or mutate repository state.
    """

    requested_views: tuple[str, ...]
    composition_purpose: str
    output_format: CompositionOutputFormat
    bounded_question_id: str | None = None
    selection_uncertainty: tuple[str, ...] = ()
    selection_read_only_boundaries: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConstitutionalContributingView:
    """One already registered constitutional view consumed by composition."""

    name: str
    cli_flag: str
    inventory_name: str
    shape_audit_name: str
    artifact: dict[str, Any]
    evidence: tuple[str, ...]
    unknowns: tuple[str, ...]
    explicit_refusals: tuple[str, ...]


@dataclass(frozen=True)
class ConstitutionalViewCompositionArtifact:
    """One immutable bounded explanation composed from requested views."""

    name: str
    request: ConstitutionalViewCompositionRequest
    contributing_views: tuple[ConstitutionalContributingView, ...]
    bounded_summary: str
    correlated_existing_evidence: tuple[str, ...]
    preserved_selection_uncertainty: tuple[str, ...]
    preserved_unknowns: tuple[str, ...]
    preserved_refusals: tuple[str, ...]
    compatibility_answer: str
    read_only_boundaries: tuple[str, ...]
    read_only: bool = True
    mutates_cluster: bool = False
    writes_event_ledger: bool = False


_BUILDERS = {
    "constitutional_process": (build_constitutional_process_view, constitutional_process_view_json),
    "constitutional_governance": (build_constitutional_governance_view, constitutional_governance_view_json),
    "constitutional_fidelity": (build_constitutional_fidelity_view, constitutional_fidelity_view_json),
}


def constitutional_view_composition_request(
    *,
    requested_views: tuple[str, ...],
    composition_purpose: str = "bounded_explanation",
    output_format: CompositionOutputFormat = "human",
    bounded_question_id: str | None = None,
    selection_uncertainty: tuple[str, ...] = (),
    selection_read_only_boundaries: tuple[str, ...] = (),
) -> ConstitutionalViewCompositionRequest:
    """Build the bounded explicit composition request."""

    return ConstitutionalViewCompositionRequest(
        requested_views=tuple(requested_views),
        composition_purpose=composition_purpose,
        output_format=output_format,
        bounded_question_id=bounded_question_id,
        selection_uncertainty=tuple(selection_uncertainty),
        selection_read_only_boundaries=tuple(selection_read_only_boundaries),
    )


def build_constitutional_view_composition(
    request: ConstitutionalViewCompositionRequest,
) -> ConstitutionalViewCompositionArtifact:
    """Compose explicitly requested registered constitutional views read-only."""

    contracts = {contract.name: contract for contract in CONSTITUTIONAL_READ_MODEL_CONTRACTS}
    unknown_requested = tuple(
        name for name in request.requested_views if name not in contracts or name not in _BUILDERS
    )
    if unknown_requested:
        supported = ", ".join(sorted(contracts))
        raise ValueError(
            "constitutional view composition only accepts registered constitutional views; "
            f"unsupported: {', '.join(unknown_requested)}; supported: {supported}"
        )

    contributing_views: list[ConstitutionalContributingView] = []
    evidence: list[str] = []
    unknowns: list[str] = []
    refusals: list[str] = []
    compatibility_answers: list[str] = []

    for view_name in request.requested_views:
        contract = contracts[view_name]
        builder, json_renderer = _BUILDERS[view_name]
        view = builder()
        payload = json_renderer(view)
        contributing_views.append(
            ConstitutionalContributingView(
                name=view_name,
                cli_flag=contract.cli_flag,
                inventory_name=contract.inventory_name,
                shape_audit_name=contract.shape_audit_name,
                artifact=payload,
                evidence=tuple(payload.get("composition", ())),
                unknowns=tuple(payload.get("unknowns", ())),
                explicit_refusals=tuple(payload.get("explicit_refusals", ())),
            )
        )
        evidence.extend(payload.get("composition", ()))
        unknowns.extend(f"{view_name}: {item}" for item in payload.get("unknowns", ()))
        refusals.extend(
            f"{view_name}: {item}" for item in payload.get("explicit_refusals", ())
        )
        compatibility_answers.append(str(payload.get("compatibility_answer", "Unknown.")))

    return ConstitutionalViewCompositionArtifact(
        name="Constitutional View Composition",
        request=request,
        contributing_views=tuple(contributing_views),
        bounded_summary=(
            "Composes only the explicitly requested registered constitutional read-model "
            "views into one bounded explanation without adding authority, resolving Unknowns, "
            "discovering evidence, planning, orchestration, or repository mutation."
        ),
        correlated_existing_evidence=tuple(dict.fromkeys(evidence)),
        preserved_selection_uncertainty=request.selection_uncertainty,
        preserved_unknowns=tuple((*request.selection_uncertainty, *unknowns)),
        preserved_refusals=tuple(refusals),
        compatibility_answer="No." if all(answer == "No." for answer in compatibility_answers) else "Unknown.",
        read_only_boundaries=(
            "registered constitutional read models only",
            "explicit requested view selection only",
            "preserve upstream selection uncertainty without resolving it",
            "preserve bounded question identity only when supplied by handoff",
            "immutable read-only artifacts only",
            "correlate existing evidence only",
            "preserve contributing Unknowns",
            "preserve contributing explicit refusals",
            "no runtime reasoning",
            "no evidence discovery",
            "no constitutional authority",
            "no implementation authority",
            "no recording",
            "no event-ledger writes",
            "no cluster mutation",
        ),
    )


def constitutional_view_composition_json(
    artifact: ConstitutionalViewCompositionArtifact,
) -> dict[str, Any]:
    """Return deterministic JSON-ready Constitutional View Composition data."""

    return to_plain(artifact)


def format_constitutional_view_composition(
    artifact: ConstitutionalViewCompositionArtifact,
) -> str:
    """Render Constitutional View Composition for humans."""

    lines = [
        artifact.name,
        "",
        f"Compatibility answer: {artifact.compatibility_answer}",
        f"Read-only: {str(artifact.read_only).lower()}",
        f"Writes event ledger: {str(artifact.writes_event_ledger).lower()}",
        f"Mutates cluster: {str(artifact.mutates_cluster).lower()}",
        f"Purpose: {artifact.request.composition_purpose}",
        f"Requested views: {', '.join(artifact.request.requested_views)}",
        f"Bounded question id: {artifact.request.bounded_question_id or 'none'}",
        "",
        "Bounded summary",
        "",
        artifact.bounded_summary,
        "",
        "Contributing views",
        "",
    ]
    for view in artifact.contributing_views:
        lines.append(f"* {view.name}: {view.cli_flag}; evidence: {', '.join(view.evidence)}")
    lines.extend(["", "Correlated existing evidence", ""])
    lines.extend(f"* {item}" for item in artifact.correlated_existing_evidence)
    lines.extend(["", "Preserved selection uncertainty", ""])
    lines.extend(f"* {item}" for item in artifact.preserved_selection_uncertainty)
    lines.extend(["", "Preserved Unknowns", ""])
    lines.extend(f"* {item}" for item in artifact.preserved_unknowns)
    lines.extend(["", "Preserved refusals", ""])
    lines.extend(f"* {item}" for item in artifact.preserved_refusals)
    lines.extend(["", "Read-only boundaries", ""])
    lines.extend(f"* {item}" for item in artifact.read_only_boundaries)
    return "\n".join(lines)
