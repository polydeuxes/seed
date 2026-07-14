"""Read-only raw line/region length features for external material structural projections."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any

from seed_runtime.external_material_structural_projection import (
    ExternalMaterialProjectedLine,
    ExternalMaterialProjectedNonblankRegion,
    ExternalMaterialStructuralProjection,
)

FEATURE_CONVENTION = "external_material_surface_feature_projection_v1"
FEATURE_CONVENTION_NOTES: tuple[str, ...] = (
    "Line numbers remain one-based.",
    "Character counts use Python string characters.",
    "Raw line text is not copied into this artifact.",
    "Content-character count excludes only the recorded line terminator.",
    "All other whitespace remains counted.",
    "Region sequences preserve physical line order.",
    "No normalization or interpretation occurs.",
)
BOUNDARY_NOTES: tuple[str, ...] = (
    "Surface features are deterministic measurements of an existing structural projection.",
    "Content-character count excludes only the recorded line terminator.",
    "No case, punctuation, whitespace, or Unicode normalization occurs.",
    "Line-length and region-length arrangements do not establish semantic structure.",
    "A recurring feature arrangement does not establish correspondence or shared responsibility.",
    "This projection does not identify headings, rules, examples, exercises, code, prose, or grammar.",
    "This projection is not runtime Evidence, Fact, candidate verification, or capability evidence.",
)


class ExternalMaterialSurfaceFeatureProjectionError(ValueError):
    """Deterministic surface-feature projection validation failure."""


@dataclass(frozen=True)
class ExternalMaterialLineSurfaceFeature:
    line_id: str
    line_number: int
    raw_character_count: int
    content_character_count: int
    line_terminator_character_count: int
    is_blank: bool
    has_line_terminator: bool
    unknowns: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self); data["unknowns"] = list(self.unknowns); return data


@dataclass(frozen=True)
class ExternalMaterialRegionSurfaceFeature:
    region_id: str
    line_ids: tuple[str, ...]
    line_count: int
    raw_line_character_count_sequence: tuple[int, ...]
    content_character_count_sequence: tuple[int, ...]
    total_raw_character_count: int
    total_content_character_count: int
    unknowns: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["line_ids"] = list(self.line_ids)
        data["raw_line_character_count_sequence"] = list(self.raw_line_character_count_sequence)
        data["content_character_count_sequence"] = list(self.content_character_count_sequence)
        data["unknowns"] = list(self.unknowns)
        return data


@dataclass(frozen=True)
class ExternalMaterialSurfaceFeatureProjection:
    manifest_id: str
    source_id: str
    artifact_id: str
    artifact_hash: str
    structural_projection_identity: str
    feature_convention: str
    line_features: tuple[ExternalMaterialLineSurfaceFeature, ...]
    region_features: tuple[ExternalMaterialRegionSurfaceFeature, ...]
    projection_unknowns: tuple[str, ...] = ()
    feature_convention_notes: tuple[str, ...] = FEATURE_CONVENTION_NOTES
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, object]:
        return {
            "artifact_type": "ExternalMaterialSurfaceFeatureProjection",
            "manifest_id": self.manifest_id,
            "source_id": self.source_id,
            "artifact_id": self.artifact_id,
            "artifact_hash": self.artifact_hash,
            "structural_projection_identity": self.structural_projection_identity,
            "feature_convention": self.feature_convention,
            "feature_convention_notes": list(self.feature_convention_notes),
            "line_features": [f.to_json_dict() for f in self.line_features],
            "region_features": [f.to_json_dict() for f in self.region_features],
            "projection_unknowns": list(self.projection_unknowns),
            "boundary_notes": list(self.boundary_notes),
            "read_only": self.read_only,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


def project_external_material_surface_features(structural_projection: ExternalMaterialStructuralProjection) -> ExternalMaterialSurfaceFeatureProjection:
    _validate_structural_projection(structural_projection)
    line_features = tuple(_line_feature(line) for line in structural_projection.lines)
    by_id = {feature.line_id: feature for feature in line_features}
    region_features = tuple(_region_feature(region, by_id) for region in structural_projection.nonblank_regions)
    return ExternalMaterialSurfaceFeatureProjection(
        structural_projection.manifest_id,
        structural_projection.source_id,
        structural_projection.artifact_id,
        structural_projection.artifact_hash,
        _structural_identity(structural_projection),
        FEATURE_CONVENTION,
        line_features,
        region_features,
        structural_projection.projection_unknowns,
    )


def external_material_surface_feature_projection_json(projection: ExternalMaterialSurfaceFeatureProjection) -> dict[str, object]:
    return projection.to_json_dict()


def format_external_material_surface_feature_projection(projection: ExternalMaterialSurfaceFeatureProjection) -> str:
    out = [
        "External Material Surface Feature Projection",
        f"manifest_id: {projection.manifest_id}",
        f"source_id: {projection.source_id}",
        f"artifact_id: {projection.artifact_id}",
        f"artifact_hash: {projection.artifact_hash}",
        f"structural_projection_identity: {projection.structural_projection_identity}",
        f"feature_convention: {projection.feature_convention}",
        f"read_only: {str(projection.read_only).lower()}",
        f"writes_event_ledger: {str(projection.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(projection.mutates_cluster).lower()}",
        "feature_convention_notes:",
    ]
    out += [f"- {n}" for n in projection.feature_convention_notes]
    out += ["boundary_notes:"] + [f"- {n}" for n in projection.boundary_notes]
    out += ["line_features:"]
    out += ["- none (empty artifact)"] if not projection.line_features else [
        f"- {f.line_id}: line {f.line_number}, raw {f.raw_character_count}, content {f.content_character_count}, terminator {f.line_terminator_character_count}, blank={str(f.is_blank).lower()}, has_line_terminator={str(f.has_line_terminator).lower()}"
        for f in projection.line_features
    ]
    out += ["region_features:"]
    out += ["- none"] if not projection.region_features else [
        f"- {f.region_id}: line_count {f.line_count}, line_ids {', '.join(f.line_ids)}, raw_sequence {list(f.raw_line_character_count_sequence)}, content_sequence {list(f.content_character_count_sequence)}, total_raw {f.total_raw_character_count}, total_content {f.total_content_character_count}"
        for f in projection.region_features
    ]
    return "\n".join(out)


def structural_projection_from_json_dict(data: dict[str, Any]) -> ExternalMaterialStructuralProjection:
    if not isinstance(data, dict):
        raise ExternalMaterialSurfaceFeatureProjectionError("input must be an object")
    if data.get("artifact_type") != "ExternalMaterialStructuralProjection":
        raise ExternalMaterialSurfaceFeatureProjectionError("artifact_type must be ExternalMaterialStructuralProjection")
    lines = tuple(_line_from_json(item) for item in _list(data.get("lines"), "lines"))
    regions = tuple(_region_from_json(item) for item in _list(data.get("nonblank_regions"), "nonblank_regions"))
    return ExternalMaterialStructuralProjection(
        _str(data, "manifest_id"), _str(data, "source_id"), _str(data, "artifact_id"), _str(data, "artifact_hash"), _str(data, "encoding"),
        lines, regions, tuple(_str_list(data.get("projection_unknowns", []), "projection_unknowns")),
    )


def _line_feature(line: ExternalMaterialProjectedLine) -> ExternalMaterialLineSurfaceFeature:
    terminator = _terminator_length(line.text, line.has_line_terminator)
    content_count = line.character_count - terminator
    if content_count < 0 or line.character_count != len(line.text):
        raise ExternalMaterialSurfaceFeatureProjectionError("line_character_count_mismatch")
    return ExternalMaterialLineSurfaceFeature(line.line_id, line.line_number, line.character_count, content_count, terminator, line.is_blank, line.has_line_terminator, line.unknowns)


def _region_feature(region: ExternalMaterialProjectedNonblankRegion, by_id: dict[str, ExternalMaterialLineSurfaceFeature]) -> ExternalMaterialRegionSurfaceFeature:
    features = tuple(by_id[line_id] for line_id in region.line_ids)
    raw = tuple(f.raw_character_count for f in features)
    content = tuple(f.content_character_count for f in features)
    return ExternalMaterialRegionSurfaceFeature(region.region_id, region.line_ids, region.line_count, raw, content, sum(raw), sum(content), region.unknowns)


def _terminator_length(text: str, has_line_terminator: bool) -> int:
    if not has_line_terminator:
        return 0
    if text.endswith("\r\n"):
        return 2
    if text.endswith("\n") or text.endswith("\r"):
        return 1
    raise ExternalMaterialSurfaceFeatureProjectionError("line_terminator_not_found")


def _validate_structural_projection(projection: ExternalMaterialStructuralProjection) -> None:
    seen_lines: set[str] = set()
    line_positions: dict[str, int] = {}
    for pos, line in enumerate(projection.lines):
        if line.line_id in seen_lines:
            raise ExternalMaterialSurfaceFeatureProjectionError("duplicate_line_id")
        seen_lines.add(line.line_id); line_positions[line.line_id] = pos
    seen_regions: set[str] = set()
    for region in projection.nonblank_regions:
        if region.region_id in seen_regions:
            raise ExternalMaterialSurfaceFeatureProjectionError("duplicate_region_id")
        seen_regions.add(region.region_id)
        if region.line_count != len(region.line_ids):
            raise ExternalMaterialSurfaceFeatureProjectionError("region_line_count_mismatch")
        previous = -1
        for line_id in region.line_ids:
            if line_id not in line_positions:
                raise ExternalMaterialSurfaceFeatureProjectionError("unknown_region_line_id")
            current = line_positions[line_id]
            if current <= previous:
                raise ExternalMaterialSurfaceFeatureProjectionError("nondeterministic_region_line_order")
            previous = current


def _structural_identity(projection: ExternalMaterialStructuralProjection) -> str:
    seed = "|".join((FEATURE_CONVENTION, projection.manifest_id, projection.source_id, projection.artifact_id, projection.artifact_hash, projection.projection_convention))
    return "external_material_structural_projection:" + sha256(seed.encode("utf-8")).hexdigest()[:24]


def _line_from_json(data: Any) -> ExternalMaterialProjectedLine:
    if not isinstance(data, dict): raise ExternalMaterialSurfaceFeatureProjectionError("line must be an object")
    return ExternalMaterialProjectedLine(_str(data,"line_id"), _int(data,"line_number"), _int(data,"character_start"), _int(data,"character_end"), _int(data,"character_count"), _bool(data,"is_blank"), _bool(data,"has_line_terminator"), _str_any(data,"text"), tuple(_str_list(data.get("unknowns", []), "unknowns")))


def _region_from_json(data: Any) -> ExternalMaterialProjectedNonblankRegion:
    if not isinstance(data, dict): raise ExternalMaterialSurfaceFeatureProjectionError("region must be an object")
    return ExternalMaterialProjectedNonblankRegion(_str(data,"region_id"), _int(data,"start_line"), _int(data,"end_line"), tuple(_str_list(data.get("line_ids"), "line_ids")), _int(data,"line_count"), tuple(_str_list(data.get("unknowns", []), "unknowns")))


def _str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value: raise ExternalMaterialSurfaceFeatureProjectionError(f"{key} is required")
    return value

def _str_any(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str): raise ExternalMaterialSurfaceFeatureProjectionError(f"{key} must be a string")
    return value

def _int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    if not isinstance(value, int): raise ExternalMaterialSurfaceFeatureProjectionError(f"{key} must be an integer")
    return value

def _bool(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool): raise ExternalMaterialSurfaceFeatureProjectionError(f"{key} must be a boolean")
    return value

def _list(value: Any, key: str) -> list[Any]:
    if not isinstance(value, list): raise ExternalMaterialSurfaceFeatureProjectionError(f"{key} must be a list")
    return value

def _str_list(value: Any, key: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value): raise ExternalMaterialSurfaceFeatureProjectionError(f"{key} must be a list of strings")
    return value
