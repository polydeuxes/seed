"""Read-only validation of testimony references against external-material manifests."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

BOUNDARY_NOTES: tuple[str, ...] = (
    "Validated bindings establish material-reference integrity only.",
    "A valid span does not establish that the span supports or contradicts any claim.",
    "A matching artifact hash does not establish source authority or truth.",
    "Annotation existence does not establish annotation correctness.",
    "Bindings are not runtime Evidence, Facts, grammar verification, or capability evidence.",
    "No material interpretation, candidate ranking, or testimony evaluation occurs.",
)
VALID_STATUS = "reference_validated"


class ExternalMaterialTestimonyBindingValidationError(ValueError):
    """Deterministic referential-integrity validation failure."""


@dataclass(frozen=True)
class ExternalMaterialSourceRecord:
    source_id: str
    source_identity: str = ""
    source_kind: str = ""
    source_hash: str = ""
    source_location: str = ""
    reported_title: str = ""
    reported_creator: str = ""
    provenance: str = ""
    unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalMaterialSourceRecord":
        return cls(_required_str(data, "source_id"), _optional_str(data, "source_identity"), _optional_str(data, "source_kind"), _optional_str(data, "source_hash"), _optional_str(data, "source_location"), _optional_str(data, "reported_title"), _optional_str(data, "reported_creator"), _optional_str(data, "provenance"), _str_tuple(data.get("unknowns", ()), "unknowns"))

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self); data["unknowns"] = list(self.unknowns); return data


@dataclass(frozen=True)
class ExternalMaterialSelectedArtifactRecord:
    artifact_id: str
    parent_source_id: str
    artifact_hash: str
    artifact_location: str = ""
    line_count: int = 0
    character_count: int = 0
    selection_bounds: str = ""
    unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalMaterialSelectedArtifactRecord":
        return cls(_required_str(data, "artifact_id"), _required_str(data, "parent_source_id"), _required_str(data, "artifact_hash"), _optional_str(data, "artifact_location"), _required_int(data, "line_count"), _optional_int(data, "character_count"), _optional_str(data, "selection_bounds"), _str_tuple(data.get("unknowns", ()), "unknowns"))

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self); data["unknowns"] = list(self.unknowns); return data


@dataclass(frozen=True)
class ExternalMaterialAnnotationRecord:
    annotation_id: str
    artifact_id: str
    start_line: int
    end_line: int
    optional_start_character: int | None = None
    optional_end_character: int | None = None
    supplied_by: str = ""
    annotation_kind: str = ""
    unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalMaterialAnnotationRecord":
        return cls(_required_str(data, "annotation_id"), _required_str(data, "artifact_id"), _required_int(data, "start_line"), _required_int(data, "end_line"), _optional_nullable_int(data, "optional_start_character"), _optional_nullable_int(data, "optional_end_character"), _optional_str(data, "supplied_by"), _optional_str(data, "annotation_kind"), _str_tuple(data.get("unknowns", ()), "unknowns"))

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self); data["unknowns"] = list(self.unknowns); return data


@dataclass(frozen=True)
class ExternalMaterialManifest:
    manifest_id: str
    sources: tuple[ExternalMaterialSourceRecord, ...] = ()
    selected_artifacts: tuple[ExternalMaterialSelectedArtifactRecord, ...] = ()
    annotations: tuple[ExternalMaterialAnnotationRecord, ...] = ()
    manifest_unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalMaterialManifest":
        return cls(_required_str(data, "manifest_id"), tuple(ExternalMaterialSourceRecord.from_json_dict(x) for x in _list(data.get("sources", ()), "sources")), tuple(ExternalMaterialSelectedArtifactRecord.from_json_dict(x) for x in _list(data.get("selected_artifacts", ()), "selected_artifacts")), tuple(ExternalMaterialAnnotationRecord.from_json_dict(x) for x in _list(data.get("annotations", ()), "annotations")), _str_tuple(data.get("manifest_unknowns", ()), "manifest_unknowns"))


@dataclass(frozen=True)
class ExternalMaterialTestimonyBindingRequest:
    testimony_reference_id: str
    manifest_id: str
    source_id: str
    artifact_id: str
    expected_artifact_hash: str
    start_line: int
    end_line: int
    optional_start_character: int | None = None
    optional_end_character: int | None = None
    optional_annotation_id: str | None = None
    unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalMaterialTestimonyBindingRequest":
        ann = data.get("optional_annotation_id")
        if ann is not None and not isinstance(ann, str):
            raise ExternalMaterialTestimonyBindingValidationError("invalid_annotation_id")
        return cls(_required_str(data, "testimony_reference_id"), _required_str(data, "manifest_id"), _required_str(data, "source_id"), _required_str(data, "artifact_id"), _required_str(data, "expected_artifact_hash"), _required_int(data, "start_line"), _required_int(data, "end_line"), _optional_nullable_int(data, "optional_start_character"), _optional_nullable_int(data, "optional_end_character"), ann, _str_tuple(data.get("unknowns", ()), "unknowns"))


@dataclass(frozen=True)
class ExternalMaterialValidatedTestimonyBinding:
    testimony_reference_id: str; source_id: str; artifact_id: str; artifact_hash: str; start_line: int; end_line: int; optional_start_character: int | None; optional_end_character: int | None; optional_annotation_id: str | None; binding_status: str = VALID_STATUS; unknowns: tuple[str, ...] = ()
    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self); data["unknowns"] = list(self.unknowns); return data


@dataclass(frozen=True)
class ExternalMaterialTestimonyBindingSet:
    manifest_id: str
    bindings: tuple[ExternalMaterialValidatedTestimonyBinding, ...]
    set_unknowns: tuple[str, ...]
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    def to_json_dict(self) -> dict[str, object]:
        return {"artifact_type":"ExternalMaterialTestimonyBindingSet","manifest_id":self.manifest_id,"bindings":[b.to_json_dict() for b in self.bindings],"set_unknowns":list(self.set_unknowns),"boundary_notes":list(self.boundary_notes),"read_only":self.read_only,"writes_event_ledger":self.writes_event_ledger,"mutates_cluster":self.mutates_cluster}


def validate_external_material_testimony_bindings(manifest: ExternalMaterialManifest, requests: tuple[ExternalMaterialTestimonyBindingRequest, ...], set_unknowns: tuple[str, ...] = ()) -> ExternalMaterialTestimonyBindingSet:
    sources = {s.source_id: s for s in manifest.sources}; artifacts = {a.artifact_id: a for a in manifest.selected_artifacts}; annotations = {a.annotation_id: a for a in manifest.annotations}; seen: set[str] = set(); bindings=[]
    for r in requests:
        if r.testimony_reference_id in seen: raise ExternalMaterialTestimonyBindingValidationError("duplicate_testimony_reference_id")
        seen.add(r.testimony_reference_id)
        if r.manifest_id != manifest.manifest_id: raise ExternalMaterialTestimonyBindingValidationError("unknown_manifest")
        if r.source_id not in sources: raise ExternalMaterialTestimonyBindingValidationError("unknown_source")
        artifact = artifacts.get(r.artifact_id)
        if artifact is None: raise ExternalMaterialTestimonyBindingValidationError("unknown_artifact")
        if artifact.parent_source_id != r.source_id: raise ExternalMaterialTestimonyBindingValidationError("source_artifact_mismatch")
        if artifact.artifact_hash != r.expected_artifact_hash: raise ExternalMaterialTestimonyBindingValidationError("artifact_hash_mismatch")
        _validate_lines(r.start_line, r.end_line, artifact.line_count)
        _validate_chars(r.optional_start_character, r.optional_end_character, artifact.character_count)
        if r.optional_annotation_id is not None:
            ann = annotations.get(r.optional_annotation_id)
            if ann is None: raise ExternalMaterialTestimonyBindingValidationError("unknown_annotation")
            if ann.artifact_id != r.artifact_id: raise ExternalMaterialTestimonyBindingValidationError("annotation_artifact_mismatch")
            if not _same_span(r, ann): raise ExternalMaterialTestimonyBindingValidationError("annotation_span_mismatch")
        bindings.append(ExternalMaterialValidatedTestimonyBinding(r.testimony_reference_id, r.source_id, r.artifact_id, artifact.artifact_hash, r.start_line, r.end_line, r.optional_start_character, r.optional_end_character, r.optional_annotation_id, VALID_STATUS, r.unknowns))
    return ExternalMaterialTestimonyBindingSet(manifest.manifest_id, tuple(bindings), set_unknowns)


def external_material_testimony_binding_json(artifact: ExternalMaterialTestimonyBindingSet) -> dict[str, object]: return artifact.to_json_dict()

def format_external_material_testimony_binding(artifact: ExternalMaterialTestimonyBindingSet) -> str:
    lines=["External Material Testimony Binding Set", f"manifest_id: {artifact.manifest_id}", "coordinate_convention: one-based inclusive line bounds; optional one-based inclusive character bounds", "annotation_compatibility: exact span equality", f"read_only: {str(artifact.read_only).lower()}", f"writes_event_ledger: {str(artifact.writes_event_ledger).lower()}", f"mutates_cluster: {str(artifact.mutates_cluster).lower()}", "boundary_notes:"]
    lines += [f"- {n}" for n in artifact.boundary_notes]
    lines += ["set_unknowns:"] + ([f"- {u}" for u in artifact.set_unknowns] or ["- none supplied"])
    lines.append("bindings:")
    if not artifact.bindings: lines.append("- none supplied (zero-binding set, not failure)")
    for b in artifact.bindings:
        lines += [f"- testimony_reference_id: {b.testimony_reference_id}", f"  source_id: {b.source_id}", f"  artifact_id: {b.artifact_id}", f"  artifact_hash: {b.artifact_hash}", f"  line_bounds: {b.start_line}-{b.end_line} (one-based inclusive)", f"  character_bounds: {_char_bounds(b)}", f"  optional_annotation_id: {b.optional_annotation_id or 'none supplied'}", f"  binding_status: {b.binding_status}", f"  unknowns: {_joined(b.unknowns)}"]
    return "\n".join(lines)


def input_from_json_dict(data: dict[str, Any]) -> tuple[ExternalMaterialManifest, tuple[ExternalMaterialTestimonyBindingRequest, ...], tuple[str, ...]]:
    return ExternalMaterialManifest.from_json_dict(_dict(data.get("manifest"), "manifest")), tuple(ExternalMaterialTestimonyBindingRequest.from_json_dict(x) for x in _list(data.get("binding_requests", ()), "binding_requests")), _str_tuple(data.get("set_unknowns", ()), "set_unknowns")

def _same_span(r, a): return (r.start_line, r.end_line, r.optional_start_character, r.optional_end_character)==(a.start_line, a.end_line, a.optional_start_character, a.optional_end_character)
def _validate_lines(s,e,count):
    if s < 1 or e < 1 or e < s: raise ExternalMaterialTestimonyBindingValidationError("invalid_line_bounds")
    if count and e > count: raise ExternalMaterialTestimonyBindingValidationError("line_bounds_out_of_range")
def _validate_chars(s,e,count):
    if (s is None) != (e is None): raise ExternalMaterialTestimonyBindingValidationError("invalid_character_bounds")
    if s is not None and (s < 1 or e < 1 or e < s or (count and e > count)): raise ExternalMaterialTestimonyBindingValidationError("invalid_character_bounds")
def _required_str(d,k):
    v=d.get(k)
    if not isinstance(v,str) or not v: raise ExternalMaterialTestimonyBindingValidationError(f"{k} is required")
    return v
def _optional_str(d,k):
    v=d.get(k,"")
    if not isinstance(v,str): raise ExternalMaterialTestimonyBindingValidationError(f"{k} must be a string")
    return v
def _required_int(d,k):
    v=d.get(k)
    if not isinstance(v,int): raise ExternalMaterialTestimonyBindingValidationError(f"{k} must be an integer")
    return v
def _optional_int(d,k):
    v=d.get(k,0)
    if not isinstance(v,int): raise ExternalMaterialTestimonyBindingValidationError(f"{k} must be an integer")
    return v
def _optional_nullable_int(d,k):
    v=d.get(k)
    if v is not None and not isinstance(v,int): raise ExternalMaterialTestimonyBindingValidationError(f"{k} must be an integer or null")
    return v
def _str_tuple(v,k):
    if not isinstance(v, list | tuple): raise ExternalMaterialTestimonyBindingValidationError(f"{k} must be a list")
    if not all(isinstance(x,str) for x in v): raise ExternalMaterialTestimonyBindingValidationError(f"{k} entries must be strings")
    return tuple(v)
def _list(v,k):
    if not isinstance(v, list | tuple): raise ExternalMaterialTestimonyBindingValidationError(f"{k} must be a list")
    return v
def _dict(v,k):
    if not isinstance(v, dict): raise ExternalMaterialTestimonyBindingValidationError(f"{k} must be an object")
    return v
def _joined(values): return ", ".join(values) if values else "none supplied"
def _char_bounds(b): return f"{b.optional_start_character}-{b.optional_end_character} (one-based inclusive)" if b.optional_start_character is not None else "none supplied"
