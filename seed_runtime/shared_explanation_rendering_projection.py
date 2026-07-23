"""Shared read-only rendering projection for one stage-owned explanation."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

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
    explanation: Any,
) -> SharedExplanationRenderingProjection:
    raise TypeError("shared rendering projection requires one known stage-local explanation")

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
