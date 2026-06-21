"""Read-only visibility for implementation-backed projection shape."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

AuthorityBoundary = Literal[
    "selection-bearing",
    "derivation-bearing",
    "validation-only",
    "explanatory-only",
    "identity-resolution",
    "projection-boundary",
    "unknown",
]


@dataclass(frozen=True)
class ProjectionShapeStage:
    stage: str
    consumes: tuple[str, ...]
    produces: tuple[str, ...]
    influences: tuple[str, ...]
    does_not_influence: tuple[str, ...]
    authority_boundary: AuthorityBoundary
    confidence: str = "implementation_backed"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        for key in ("consumes", "produces", "influences", "does_not_influence"):
            data[key] = list(data[key])
        return data


PROJECTION_SHAPE_STAGES: tuple[ProjectionShapeStage, ...] = (
    ProjectionShapeStage(
        stage="event_replay",
        consumes=("event_ledger",),
        produces=(
            "entities",
            "observations",
            "evidence",
            "facts",
            "goals",
            "tool_needs",
            "approvals",
            "execution_authorizations",
            "execution_proposals",
            "pending_actions",
            "action_plans",
            "handoff_plans",
            "tools",
        ),
        influences=("projection_finalization",),
        does_not_influence=("event_ledger",),
        authority_boundary="projection-boundary",
    ),
    ProjectionShapeStage(
        stage="alias_projection",
        consumes=("facts",),
        produces=("alias_resolver", "entity_aliases"),
        influences=(
            "measurement_retention",
            "inference",
            "fact_conflict_handling",
            "current_fact_selection",
        ),
        does_not_influence=("event_ledger",),
        authority_boundary="identity-resolution",
    ),
    ProjectionShapeStage(
        stage="measurement_retention",
        consumes=("facts", "alias_resolver", "measurement_history_limit"),
        produces=(
            "retained_projected_facts",
            "pruned_projected_measurement_provenance",
        ),
        influences=("inference", "fact_support_projection", "relationship_projection"),
        does_not_influence=("event_ledger",),
        authority_boundary="selection-bearing",
    ),
    ProjectionShapeStage(
        stage="inference",
        consumes=(
            "current_observed_facts",
            "inference_catalog",
            "predicate_catalog",
            "alias_resolver",
        ),
        produces=("inferred_facts", "facts"),
        influences=(
            "alias_projection",
            "fact_support_projection",
            "relationship_projection",
            "entity_type_assertion_projection",
        ),
        does_not_influence=("event_ledger", "observed_facts"),
        authority_boundary="derivation-bearing",
    ),
    ProjectionShapeStage(
        stage="fact_support_projection",
        consumes=("facts",),
        produces=("fact_supports",),
        influences=("current_fact_selection", "fact_conflict_handling"),
        does_not_influence=("relationship_projection",),
        authority_boundary="selection-bearing",
    ),
    ProjectionShapeStage(
        stage="legacy_relationship_projection",
        consumes=("facts",),
        produces=("entity_relationships",),
        influences=("legacy_relationship_views",),
        does_not_influence=(
            "catalog_relationship_projection",
            "graph_issue_construction",
        ),
        authority_boundary="derivation-bearing",
    ),
    ProjectionShapeStage(
        stage="catalog_relationship_projection",
        consumes=("facts", "relationship_catalog", "evidence"),
        produces=("relationships",),
        influences=("entity_type_assertion_projection", "graph_issue_construction"),
        does_not_influence=("fact_support_projection",),
        authority_boundary="derivation-bearing",
    ),
    ProjectionShapeStage(
        stage="entity_type_assertion_projection",
        consumes=("entities", "facts", "relationships", "entity_type_catalog"),
        produces=("entity_type_assertions",),
        influences=("graph_issue_construction", "entity_type_views"),
        does_not_influence=("relationship_projection", "fact_support_projection"),
        authority_boundary="derivation-bearing",
    ),
    ProjectionShapeStage(
        stage="graph_issue_construction",
        consumes=(
            "relationships",
            "entity_type_assertions",
            "relationship_catalog",
            "entity_type_catalog",
        ),
        produces=("graph_issues",),
        influences=("graph_issue_views", "unhealthy_views"),
        does_not_influence=("relationships", "entity_type_assertions", "facts"),
        authority_boundary="validation-only",
    ),
    ProjectionShapeStage(
        stage="fact_conflict_handling",
        consumes=("facts", "fact_supports", "predicate_catalog", "alias_resolver"),
        produces=("fact_conflicts",),
        influences=("fact_conflict_views", "integrity_summary"),
        does_not_influence=("facts", "relationships", "entity_type_assertions"),
        authority_boundary="validation-only",
    ),
    ProjectionShapeStage(
        stage="measurement_evidence_scan",
        consumes=("facts",),
        produces=("all_measurement_evidence_ids",),
        influences=("measurement_provenance_pruning",),
        does_not_influence=("unknown",),
        authority_boundary="unknown",
        confidence="weak_evidence_unknown_boundary",
    ),
)

BOUNDARY = {"read_only": True, "writes_event_ledger": False, "mutates_cluster": False}


def build_projection_shape() -> dict[str, object]:
    return {"stages": PROJECTION_SHAPE_STAGES, "boundary": dict(BOUNDARY)}


def projection_shape_json(shape: dict[str, object] | None = None) -> dict[str, object]:
    shape = shape or build_projection_shape()
    return {
        "stages": [stage.to_json_dict() for stage in shape["stages"]],
        "boundary": dict(shape["boundary"]),
    }


def format_projection_shape(shape: dict[str, object] | None = None) -> str:
    shape = shape or build_projection_shape()
    lines = ["Projection Shape", "Boundary:"]
    boundary = shape["boundary"]
    lines.extend(
        [
            f"  Read Only: {str(boundary['read_only']).lower()}",
            f"  Writes Event Ledger: {str(boundary['writes_event_ledger']).lower()}",
            f"  Mutates Cluster: {str(boundary['mutates_cluster']).lower()}",
            "",
            "Stages:",
        ]
    )
    for stage in shape["stages"]:
        lines.extend(
            [
                f"  Stage: {stage.stage}",
                f"    Consumes: {_join(stage.consumes)}",
                f"    Produces: {_join(stage.produces)}",
                f"    Influences: {_join(stage.influences)}",
                f"    Does Not Influence: {_join(stage.does_not_influence)}",
                f"    Authority Boundary: {stage.authority_boundary}",
                f"    Confidence: {stage.confidence}",
            ]
        )
    return "\n".join(lines)


def _join(values: tuple[str, ...]) -> str:
    return ", ".join(values) if values else "none"
