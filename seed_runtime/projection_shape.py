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
        authority_boundary="explanatory-only",
    ),
    ProjectionShapeStage(
        stage="measurement_evidence_scan",
        consumes=("facts",),
        produces=("measurement_evidence_id_set",),
        influences=("measurement_provenance_pruning",),
        does_not_influence=(),
        authority_boundary="projection-boundary",
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
                f"    Consumes:{_format_values(stage.consumes)}",
                f"    Produces:{_format_values(stage.produces)}",
                f"    Influences:{_format_values(stage.influences)}",
            ]
        )
        if stage.does_not_influence:
            lines.append(
                f"    Does Not Influence:{_format_values(stage.does_not_influence)}"
            )
        lines.extend(
            [
                f"    Authority Boundary: {stage.authority_boundary}",
                f"    Confidence: {stage.confidence}",
            ]
        )
    return "\n".join(lines)


def build_projection_stage_definition(stage_name: str) -> dict[str, object]:
    """Return a read-only identity and boundary explanation for one ProjectionStage."""

    stage = next((item for item in PROJECTION_SHAPE_STAGES if item.stage == stage_name), None)
    if stage is None:
        return {
            "projection_stage_definition": {
                "status": "unknown",
                "stage": stage_name,
                "stage_identifier": stage_name,
                "registered_stage": False,
                "evidence_source": "projection_shape_stage_registry",
                "implementation_reason": "unknown projection stage; no projection shape stage declaration exists",
            }
        }

    return {
        "projection_stage_definition": {
            "status": "known",
            "stage": stage.stage,
            "stage_identifier": stage.stage,
            "registered_stage": True,
            "evidence_source": "projection_shape_stage_registry",
            "implementation_reason": "identity recovered from the declared projection shape stage registration",
            "projection_stage_boundary": {
                "authority_boundary": stage.authority_boundary,
                "does_not_influence": list(stage.does_not_influence),
            },
        }
    }


def projection_stage_definition_json(stage_name: str) -> dict[str, object]:
    return build_projection_stage_definition(stage_name)


def build_projection_stage_explanation(stage_name: str) -> dict[str, object]:
    """Compose existing ProjectionStage explanation fields without adding evidence."""

    definition = build_projection_stage_definition(stage_name)[
        "projection_stage_definition"
    ]
    explanation: dict[str, object] = {
        "projection_stage_definition": definition,
    }
    if "projection_stage_boundary" in definition:
        explanation["projection_stage_boundary"] = definition[
            "projection_stage_boundary"
        ]
    return {"projection_stage_explanation": explanation}


def projection_stage_explanation_json(stage_name: str) -> dict[str, object]:
    return build_projection_stage_explanation(stage_name)


def format_projection_stage_explanation(stage_name: str) -> str:
    explanation = build_projection_stage_explanation(stage_name)[
        "projection_stage_explanation"
    ]
    definition = explanation["projection_stage_definition"]
    lines = [
        f"ProjectionStage explanation: {definition['stage']}",
        "  projection_stage_definition:",
        f"    status: {definition['status']}",
        f"    stage_identifier: {definition['stage_identifier']}",
        f"    registered_stage: {str(definition['registered_stage']).lower()}",
    ]
    boundary = explanation.get("projection_stage_boundary")
    if isinstance(boundary, dict):
        lines.extend(
            [
                "  projection_stage_boundary:",
                f"    authority_boundary: {boundary['authority_boundary']}",
                f"    does_not_influence:{_format_values(tuple(boundary.get('does_not_influence', [])))}",
            ]
        )
    lines.extend(
        [
            f"    implementation_reason: {definition['implementation_reason']}",
            f"    evidence_source: {definition['evidence_source']}",
        ]
    )
    return "\n".join(lines)


def format_projection_stage_definition(stage_name: str) -> str:
    definition = build_projection_stage_definition(stage_name)[
        "projection_stage_definition"
    ]
    return "\n".join(
        [
            f"ProjectionStage definition: {definition['stage']}",
            f"  status: {definition['status']}",
            f"  stage_identifier: {definition['stage_identifier']}",
            f"  registered_stage: {str(definition['registered_stage']).lower()}",
            *_format_projection_stage_boundary_lines(definition),
            f"  implementation_reason: {definition['implementation_reason']}",
            f"  evidence_source: {definition['evidence_source']}",
        ]
    )


def _format_projection_stage_boundary_lines(definition: dict[str, object]) -> list[str]:
    boundary = definition.get("projection_stage_boundary")
    if not isinstance(boundary, dict):
        return []
    does_not_influence = boundary.get("does_not_influence", [])
    if not isinstance(does_not_influence, list):
        does_not_influence = []
    return [
        "  projection_stage_boundary:",
        f"    authority_boundary: {boundary['authority_boundary']}",
        f"    does_not_influence:{_format_values(tuple(does_not_influence))}",
    ]


def _format_values(values: tuple[str, ...]) -> str:
    if not values:
        return " none"
    if len(values) == 1:
        return f" {values[0]}"
    return "\n" + "\n".join(f"      - {value}" for value in values)
