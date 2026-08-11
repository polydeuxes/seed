"""Read-only mechanical line and nonblank-region projection for bounded external text."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any

from seed_runtime.external_material_testimony_binding import (
    ExternalMaterialManifest,
)

PROJECTION_CONVENTION = "external_material_structural_projection_v1"
BOUNDARY_NOTES: tuple[str, ...] = (
    "Lines and regions are mechanical projections of exact supplied text.",
    "A line boundary is not a semantic boundary.",
    "A nonblank contiguous region is not a paragraph, section, heading, rule, example, or exercise.",
    "No prose comprehension, grammar inference, semantic labeling, candidate generation, or normalized similarity occurs.",
    "Raw case, punctuation, whitespace, and newline distinctions remain unnormalized.",
    "This projection is not runtime Evidence, Fact, or grammar verification.",
)


class ExternalMaterialStructuralProjectionError(ValueError):
    """Deterministic structural projection validation failure."""


@dataclass(frozen=True)
class ExternalMaterialStructuralProjectionRequest:
    manifest_id: str
    source_id: str
    artifact_id: str
    expected_artifact_hash: str
    encoding: str
    exact_text: str
    unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalMaterialStructuralProjectionRequest":
        return cls(
            _required_str(data, "manifest_id"),
            _required_str(data, "source_id"),
            _required_str(data, "artifact_id"),
            _required_str(data, "expected_artifact_hash"),
            _required_str(data, "encoding"),
            _required_text(data, "exact_text"),
            _str_tuple(data.get("unknowns", ()), "unknowns"),
        )


@dataclass(frozen=True)
class ExternalMaterialProjectedLine:
    line_id: str
    line_number: int
    character_start: int
    character_end: int
    character_count: int
    is_blank: bool
    has_line_terminator: bool
    text: str
    unknowns: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self); data["unknowns"] = list(self.unknowns); return data


@dataclass(frozen=True)
class ExternalMaterialProjectedNonblankRegion:
    region_id: str
    start_line: int
    end_line: int
    line_ids: tuple[str, ...]
    line_count: int
    unknowns: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self); data["line_ids"] = list(self.line_ids); data["unknowns"] = list(self.unknowns); return data


@dataclass(frozen=True)
class ExternalMaterialStructuralProjection:
    manifest_id: str
    source_id: str
    artifact_id: str
    artifact_hash: str
    encoding: str
    lines: tuple[ExternalMaterialProjectedLine, ...]
    nonblank_regions: tuple[ExternalMaterialProjectedNonblankRegion, ...]
    projection_unknowns: tuple[str, ...] = ()
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    projection_convention: str = PROJECTION_CONVENTION
    coordinate_convention: str = "one-based inclusive line numbers; zero-based half-open character offsets over the exact Python string; line terminators are counted in line character ranges"
    line_splitting_convention: str = "empty text has zero physical lines; otherwise splitlines(keepends=True) defines physical lines without adding a synthetic final line"

    def to_json_dict(self) -> dict[str, object]:
        return {
            "artifact_type": "ExternalMaterialStructuralProjection",
            "manifest_id": self.manifest_id,
            "source_id": self.source_id,
            "artifact_id": self.artifact_id,
            "artifact_hash": self.artifact_hash,
            "encoding": self.encoding,
            "projection_convention": self.projection_convention,
            "coordinate_convention": self.coordinate_convention,
            "line_splitting_convention": self.line_splitting_convention,
            "lines": [l.to_json_dict() for l in self.lines],
            "nonblank_regions": [r.to_json_dict() for r in self.nonblank_regions],
            "projection_unknowns": list(self.projection_unknowns),
            "boundary_notes": list(self.boundary_notes),
            "read_only": self.read_only,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


def project_external_material_structure(manifest: ExternalMaterialManifest, request: ExternalMaterialStructuralProjectionRequest) -> ExternalMaterialStructuralProjection:
    if request.manifest_id != manifest.manifest_id:
        raise ExternalMaterialStructuralProjectionError("unknown_manifest")
    sources = {s.source_id: s for s in manifest.sources}
    artifacts = {a.artifact_id: a for a in manifest.selected_artifacts}
    if request.source_id not in sources:
        raise ExternalMaterialStructuralProjectionError("unknown_source")
    artifact = artifacts.get(request.artifact_id)
    if artifact is None:
        raise ExternalMaterialStructuralProjectionError("unknown_artifact")
    if artifact.parent_source_id != request.source_id:
        raise ExternalMaterialStructuralProjectionError("source_artifact_mismatch")
    if artifact.artifact_hash != request.expected_artifact_hash:
        raise ExternalMaterialStructuralProjectionError("artifact_hash_mismatch")
    try:
        encoded = request.exact_text.encode(request.encoding)
    except LookupError as exc:
        raise ExternalMaterialStructuralProjectionError("unsupported_encoding") from exc
    except UnicodeEncodeError as exc:
        raise ExternalMaterialStructuralProjectionError("text_encode_failure") from exc
    actual_hash = sha256(encoded).hexdigest()
    if actual_hash != artifact.artifact_hash:
        raise ExternalMaterialStructuralProjectionError("artifact_hash_mismatch")
    pieces = request.exact_text.splitlines(keepends=True) if request.exact_text else []
    if len(pieces) != artifact.line_count:
        raise ExternalMaterialStructuralProjectionError("line_count_mismatch")
    if len(request.exact_text) != artifact.character_count:
        raise ExternalMaterialStructuralProjectionError("character_count_mismatch")
    lines = _project_lines(request, pieces)
    regions = _project_regions(request, lines)
    return ExternalMaterialStructuralProjection(request.manifest_id, request.source_id, request.artifact_id, artifact.artifact_hash, request.encoding, tuple(lines), tuple(regions), request.unknowns)


def external_material_structural_projection_json(projection: ExternalMaterialStructuralProjection) -> dict[str, object]:
    return projection.to_json_dict()


def format_external_material_structural_projection(projection: ExternalMaterialStructuralProjection) -> str:
    out = ["External Material Structural Projection", f"manifest_id: {projection.manifest_id}", f"source_id: {projection.source_id}", f"artifact_id: {projection.artifact_id}", f"artifact_hash: {projection.artifact_hash}", f"encoding: {projection.encoding}", f"projection_convention: {projection.projection_convention}", f"coordinate_convention: {projection.coordinate_convention}", f"line_splitting_convention: {projection.line_splitting_convention}", f"read_only: {str(projection.read_only).lower()}", f"writes_event_ledger: {str(projection.writes_event_ledger).lower()}", f"mutates_cluster: {str(projection.mutates_cluster).lower()}", "boundary_notes:"]
    out += [f"- {n}" for n in projection.boundary_notes]
    out += ["lines:"]
    out += ["- none (empty artifact)"] if not projection.lines else [f"- {l.line_id}: line {l.line_number}, chars {l.character_start}-{l.character_end}, count {l.character_count}, blank={str(l.is_blank).lower()}, terminator={str(l.has_line_terminator).lower()}" for l in projection.lines]
    out += ["nonblank_regions:"]
    out += ["- none"] if not projection.nonblank_regions else [f"- {r.region_id}: lines {r.start_line}-{r.end_line}, line_count {r.line_count}, line_ids {', '.join(r.line_ids)}" for r in projection.nonblank_regions]
    return "\n".join(out)


def input_from_json_dict(data: dict[str, Any]) -> tuple[ExternalMaterialManifest, ExternalMaterialStructuralProjectionRequest]:
    if not isinstance(data, dict): raise ExternalMaterialStructuralProjectionError("input must be an object")
    manifest = ExternalMaterialManifest.from_json_dict(_dict(data.get("manifest"), "manifest"))
    request = ExternalMaterialStructuralProjectionRequest.from_json_dict(_dict(data.get("projection_request"), "projection_request"))
    return manifest, request


def _project_lines(request, pieces):
    out=[]; pos=0
    for number, piece in enumerate(pieces, 1):
        has_term = piece.endswith(("\n", "\r"))
        content = piece[:-2] if piece.endswith("\r\n") else (piece[:-1] if has_term else piece)
        end = pos + len(piece)
        out.append(ExternalMaterialProjectedLine(_stable_id("line", request, f"{number}:{pos}:{end}"), number, pos, end, len(piece), content.strip()=="", has_term, piece, ()))
        pos=end
    return out


def _project_regions(request, lines):
    regions=[]; current=[]
    for line in lines:
        if line.is_blank:
            if current: regions.append(_region(request, current)); current=[]
        else:
            current.append(line)
    if current: regions.append(_region(request, current))
    return regions


def _region(request, lines):
    start, end = lines[0].line_number, lines[-1].line_number
    line_ids = tuple(l.line_id for l in lines)
    return ExternalMaterialProjectedNonblankRegion(_stable_id("region", request, f"{start}:{end}:{','.join(line_ids)}"), start, end, line_ids, len(lines), ())


def _stable_id(kind, request, coordinates):
    seed = "|".join((PROJECTION_CONVENTION, kind, request.manifest_id, request.source_id, request.artifact_id, request.expected_artifact_hash, coordinates))
    return f"external_material_{kind}:" + sha256(seed.encode("utf-8")).hexdigest()[:24]


def _required_str(d,k):
    v=d.get(k)
    if not isinstance(v,str) or not v: raise ExternalMaterialStructuralProjectionError(f"{k} is required")
    return v

def _required_text(d,k):
    v=d.get(k)
    if not isinstance(v,str): raise ExternalMaterialStructuralProjectionError(f"{k} must be a string")
    return v

def _str_tuple(v,k):
    if not isinstance(v, list | tuple) or not all(isinstance(x,str) for x in v): raise ExternalMaterialStructuralProjectionError(f"{k} must be a list of strings")
    return tuple(v)

def _dict(v,k):
    if not isinstance(v, dict): raise ExternalMaterialStructuralProjectionError(f"{k} must be an object")
    return v
