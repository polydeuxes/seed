"""Shared read-only rendering projection for one stage-owned explanation."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from seed_runtime.operator_authority_scope_binding import MinimumLawfulAdvancementExplanation
from seed_runtime.representation_grammar_applicability import (
    RepresentationGrammarApplicabilityAdvancementExplanation,
)

PROJECTION_CONVENTION = "shared_explanation_rendering_projection_v1"


@dataclass(frozen=True)
class SharedExplanationRenderingProjection:
    artifact_type: str
    source_explanation_identity: str
    source_artifact_owner: str
    source_explanation_type: str
    producer: str
    attempted_movement: str
    source_state: str
    source_reason: str
    preserved_unknowns: tuple[str, ...]
    preserved_conflicts: tuple[str, ...]
    prohibited_downstream_movement: tuple[str, ...]
    explanation_boundary: str
    stage_owned_material: dict[str, Any]
    single_explanation_boundary: str = (
        "Consumes exactly one already-produced stage-local explanation; does not "
        "compare, aggregate, order, or compose explanations."
    )
    rendering_boundary: str = (
        "Shared field names are display labels only; all constitutional meaning "
        "remains authored and owned by the source stage."
    )
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    projection_convention: str = PROJECTION_CONVENTION

    def to_json_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


def _tuple(xs: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(xs)


def project_shared_explanation_rendering(
    explanation: MinimumLawfulAdvancementExplanation
    | RepresentationGrammarApplicabilityAdvancementExplanation,
) -> SharedExplanationRenderingProjection:
    if isinstance(explanation, MinimumLawfulAdvancementExplanation):
        stage_owned_material: dict[str, Any] = {
            "established": explanation.established,
            "first_missing_boundary": explanation.first_missing_boundary,
            "movement_blocked": explanation.movement_blocked,
            "authority_resolvable": explanation.authority_resolvable,
            "reconsideration_transition": explanation.reconsideration_transition,
        }
    elif isinstance(explanation, RepresentationGrammarApplicabilityAdvancementExplanation):
        stage_owned_material = {
            "examined_grammar": explanation.examined_grammar,
            "examined_demand": explanation.examined_demand,
            "examined_mechanism": explanation.examined_mechanism,
            "examined_contract": explanation.examined_contract,
            "established_applicability_evidence": _tuple(explanation.established_applicability_evidence),
            "next_handoff_boundary": explanation.next_handoff_boundary,
            "handoff_permitted": explanation.handoff_permitted,
            "authority_treatment": explanation.authority_treatment,
            "reconsideration_evidence": _tuple(explanation.reconsideration_evidence),
            "known_loss": _tuple(explanation.preserved_known_loss),
            "provenance": _tuple(explanation.preserved_provenance),
            "compatibility_boundary_changed": explanation.compatibility_boundary_changed,
        }
    else:
        raise TypeError("shared rendering projection requires one known stage-local explanation")

    return SharedExplanationRenderingProjection(
        artifact_type="SharedExplanationRenderingProjection",
        source_explanation_identity=explanation.explanation_id,
        source_artifact_owner=explanation.producer,
        source_explanation_type=explanation.artifact_type,
        producer="SharedExplanationRenderingProjection",
        attempted_movement=explanation.attempted_movement,
        source_state=explanation.source_state,
        source_reason=explanation.source_reason,
        preserved_unknowns=_tuple(explanation.preserved_unknowns),
        preserved_conflicts=_tuple(explanation.preserved_conflicts),
        prohibited_downstream_movement=_tuple(explanation.prohibited_downstream_movement),
        explanation_boundary=explanation.explanation_boundary,
        stage_owned_material=stage_owned_material,
        read_only=explanation.read_only,
        writes_event_ledger=explanation.writes_event_ledger,
        mutates_cluster=explanation.mutates_cluster,
    )


def shared_explanation_rendering_json(p: SharedExplanationRenderingProjection) -> dict[str, Any]:
    return p.to_json_dict()


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def format_shared_explanation_rendering(p: SharedExplanationRenderingProjection) -> str:
    lines = [
        "Shared Explanation Rendering Projection",
        f"source_explanation_identity: {p.source_explanation_identity}",
        f"source_artifact_owner: {p.source_artifact_owner}",
        f"source_explanation_type: {p.source_explanation_type}",
        f"producer: {p.producer}",
        f"attempted_movement: {p.attempted_movement}",
        f"source_state: {p.source_state}",
        f"source_reason: {p.source_reason}",
        f"explanation_boundary: {p.explanation_boundary}",
        f"single_explanation_boundary: {p.single_explanation_boundary}",
        f"rendering_boundary: {p.rendering_boundary}",
        f"read_only: {str(p.read_only).lower()}",
        f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(p.mutates_cluster).lower()}",
    ]
    for label, vals in (
        ("preserved_unknowns", p.preserved_unknowns),
        ("preserved_conflicts", p.preserved_conflicts),
        ("prohibited_downstream_movement", p.prohibited_downstream_movement),
    ):
        lines.append(label + ":")
        lines += [f"- {x}" for x in vals] or ["- none"]
    lines.append("stage_owned_material:")
    for key, value in p.stage_owned_material.items():
        if isinstance(value, tuple):
            lines.append(f"  {key}:")
            lines += [f"  - {x}" for x in value] or ["  - none"]
        else:
            lines.append(f"  {key}: {_format_value(value)}")
    return "\n".join(lines)
