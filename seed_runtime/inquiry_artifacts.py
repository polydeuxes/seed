"""Read-only repository-visible inquiry artifact visibility."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

ArtifactClassification = Literal[
    "repository_visible", "partially_visible", "document_visible", "unknown"
]


@dataclass(frozen=True)
class InquiryArtifactVisibility:
    artifact: str
    classification: ArtifactClassification
    evidence: tuple[str, ...]
    limitations: tuple[str, ...]

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = list(self.evidence)
        data["limitations"] = list(self.limitations)
        return data


BOUNDARY: dict[str, bool] = {
    "read_only": True,
    "supports_record": False,
    "writes_event_ledger": False,
    "mutates_cluster": False,
    "infers_inquiry_movement": False,
    "creates_inquiry_graph": False,
    "infers_pressure_transformation": False,
    "performs_workflow_or_planning": False,
}

ARTIFACTS: tuple[InquiryArtifactVisibility, ...] = (
    InquiryArtifactVisibility(
        artifact="unknown",
        classification="repository_visible",
        evidence=(
            "diagnostic_inventory and diagnostic_shape_audit declare and check unknown diagnostic shape status",
            "operational_surface_classification_audit exposes unknown CLI element classification",
            "knowledge_reachability treats unknown as a candidate kind",
        ),
        limitations=("does not infer unknown inquiry movement from prose",),
    ),
    InquiryArtifactVisibility(
        artifact="boundary",
        classification="repository_visible",
        evidence=(
            "capability_relationship exposes privilege and acquisition boundaries",
            "privilege_discovery explains read-only privilege boundaries",
            "diagnostic_inventory records no recording, event-ledger, and mutation boundaries for diagnostics",
        ),
        limitations=(
            "does not promote every prose boundary into repository knowledge",
        ),
    ),
    InquiryArtifactVisibility(
        artifact="pressure",
        classification="partially_visible",
        evidence=(
            "pressure_audit ranks operational pressure from existing visibility surfaces",
            "capability_relationship includes pressure as capability relationship context",
            "selection_path and reasoning_path consume pressure audit evidence",
        ),
        limitations=(
            "operational pressure visibility is implementation-backed, but inquiry pressure transformation is not inferred",
        ),
    ),
    InquiryArtifactVisibility(
        artifact="finding",
        classification="partially_visible",
        evidence=(
            "diagnostic and audit surfaces emit read-only findings as rendered output and JSON",
            "reasoning_path exposes derivation evidence for operational conclusions",
        ),
        limitations=(
            "findings are surface outputs, not a generalized inquiry-artifact model",
        ),
    ),
    InquiryArtifactVisibility(
        artifact="supported_conclusion",
        classification="document_visible",
        evidence=(
            "investigation documents repeatedly distinguish supported conclusions from unsupported conclusions",
        ),
        limitations=(
            "no repository implementation currently models supported inquiry conclusions as artifacts",
        ),
    ),
    InquiryArtifactVisibility(
        artifact="unsupported_conclusion",
        classification="document_visible",
        evidence=(
            "investigation documents repeatedly preserve unsupported conclusions as documentation-only inquiry state",
        ),
        limitations=(
            "unsupported inquiry conclusions are not implemented as a repository-visible runtime surface",
        ),
    ),
    InquiryArtifactVisibility(
        artifact="open_question",
        classification="document_visible",
        evidence=("investigation documents preserve open questions as prose sections",),
        limitations=(
            "open questions are not implemented as workflow or planning items",
        ),
    ),
    InquiryArtifactVisibility(
        artifact="gap",
        classification="partially_visible",
        evidence=(
            "observation_domains classifies observation-domain coverage gaps from existing evidence",
            "visibility_coverage_audit reports discovered operational surfaces missing diagnostic inventory visibility",
        ),
        limitations=(
            "implementation-backed gaps are operational visibility gaps, not a general inquiry gap model",
        ),
    ),
)


def build_inquiry_artifacts() -> dict[str, Any]:
    return {"artifacts": ARTIFACTS, "boundary": BOUNDARY}


def inquiry_artifacts_json(view: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifacts": [artifact.to_json_dict() for artifact in view["artifacts"]],
        "boundary": dict(view["boundary"]),
    }


def format_inquiry_artifacts(view: dict[str, Any]) -> str:
    lines = [
        "Inquiry Artifacts Visibility",
        "",
        "Boundary: read only; no recording; no event ledger writes; no cluster mutation; no inquiry graph creation; no pressure transformation inference; no workflow or planning behavior.",
        "",
    ]
    for artifact in view["artifacts"]:
        lines.append(f"{artifact.artifact}: {artifact.classification}")
        lines.append("  evidence:")
        for evidence in artifact.evidence:
            lines.append(f"    - {evidence}")
        if artifact.limitations:
            lines.append("  limitations:")
            for limitation in artifact.limitations:
                lines.append(f"    - {limitation}")
    return "\n".join(lines)
