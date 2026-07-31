"""Bounded formation of exact, source-addressable operator ingress material."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from seed_runtime.contextual_interpretation_warrant_set import (
    ContextualInterpretationWarrantSetError,
    ExactOperatorMaterial,
    SourceSpan,
)
from seed_runtime.events import EventLedger
from seed_runtime.models import Event


class OperatorIngressAddressableMaterialError(ValueError):
    """The supplied occurrence cannot lawfully form addressable material."""


UNKNOWNS = (
    "communicative meaning Unknown",
    "operator intent Unknown",
    "operator goal Unknown",
    "Seed-question applicability Unknown",
    "next-consumer applicability Unknown",
)
AUTHORITY_LIMITS = (
    "addressability and exact-material carriage only",
    "decoder success establishes representation availability, not interpretation or competency",
    "no interpretation candidate, warrant, selection, applicability, admission, goal, Demand, movement, authorization, or execution",
)


def _stable_id(prefix: str, value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return f"{prefix}:{hashlib.sha256(encoded.encode()).hexdigest()}"


def addressable_material_projection_id(material: ExactOperatorMaterial) -> str:
    """Return the canonical identity owned by the addressable-material boundary."""
    return _stable_id("operator-ingress-addressable-material", asdict(material))


def operator_material_full_span_id(*, ingress_event_ref: str, exact_text: str) -> str:
    """Return the addressable-material owner's canonical full-span identity."""
    return _stable_id("operator-material-full-span", (ingress_event_ref, exact_text))


@dataclass(frozen=True)
class OperatorIngressAddressableMaterial:
    artifact_type: str
    material_projection_id: str
    ingress_event_ref: str
    raw_material_event_ref: str
    representation_examination_event_ref: str
    exact_operator_material: ExactOperatorMaterial
    source_role: str
    provenance: tuple[str, ...]
    scope: tuple[str, ...]
    known_loss: tuple[str, ...]
    unknowns: tuple[str, ...]
    authority_limits: tuple[str, ...]
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_state: bool = False
    mutates_cluster: bool = False

    def __post_init__(self) -> None:
        self._validate_intrinsic_invariants()

    def _validate_intrinsic_invariants(self) -> None:
        if self.artifact_type != "operator_ingress_addressable_material":
            _refuse("wrong addressable material artifact_type")
        for name in (
            "material_projection_id",
            "ingress_event_ref",
            "raw_material_event_ref",
            "representation_examination_event_ref",
            "source_role",
        ):
            _exact_string(getattr(self, name), name)
        for name in (
            "provenance",
            "scope",
            "known_loss",
            "unknowns",
            "authority_limits",
        ):
            _intrinsic_string_tuple(getattr(self, name), name)
        if not isinstance(self.exact_operator_material, ExactOperatorMaterial):
            _refuse("exact_operator_material must be ExactOperatorMaterial")
        if self.read_only is not True or any(
            value is not False
            for value in (
                self.writes_event_ledger,
                self.mutates_state,
                self.mutates_cluster,
            )
        ):
            _refuse("addressable material must be read-only and non-mutating")
        if self.provenance != (
            self.raw_material_event_ref,
            self.representation_examination_event_ref,
            self.ingress_event_ref,
        ):
            _refuse(
                "addressable provenance must preserve exact raw, examination, ingress order"
            )
        material = self.exact_operator_material
        _intrinsic_string(material.material_ref, "exact material material_ref")
        _intrinsic_string(material.exact_text, "exact material exact_text", empty=True)
        _intrinsic_string_tuple(material.provenance, "exact material provenance")
        if (
            material.material_ref != self.ingress_event_ref
            or material.provenance != self.provenance
        ):
            _refuse("exact material standing does not match addressable standing")
        if type(material.source_spans) is not tuple or len(material.source_spans) != 1:
            _refuse("exact material must have one canonical full source span")
        span = material.source_spans[0]
        if not isinstance(span, SourceSpan):
            _refuse("source span must be a SourceSpan")
        _intrinsic_string(span.span_ref, "source span span_ref")
        _intrinsic_string(span.source_ref, "source span source_ref")
        _intrinsic_int(span.start, "source span start")
        _intrinsic_int(span.end, "source span end")
        _intrinsic_string(span.exact_text, "source span exact_text", empty=True)
        if span.span_ref != operator_material_full_span_id(
            ingress_event_ref=self.ingress_event_ref, exact_text=material.exact_text
        ):
            _refuse("full source span identity is forged")
        if (span.source_ref, span.start, span.end, span.exact_text) != (
            self.ingress_event_ref,
            0,
            len(material.exact_text),
            material.exact_text,
        ):
            _refuse("source span must cover the complete exact material")
        if self.material_projection_id != addressable_material_projection_id(material):
            _refuse("material projection identity is forged or stale")

    def to_json_dict(self) -> dict[str, object]:
        """Return the single JSON-safe projection representation."""
        return asdict(self)

    @classmethod
    def from_json_dict(
        cls, value: dict[str, object]
    ) -> OperatorIngressAddressableMaterial:
        """Recover the frozen artifact from its projection representation."""
        if not isinstance(value, dict):
            _refuse("addressable material must be an object")
        material_value = value.get("exact_operator_material")
        if not isinstance(material_value, dict):
            raise OperatorIngressAddressableMaterialError(
                "exact material must be an object"
            )
        spans = material_value.get("source_spans")
        if not isinstance(spans, (list, tuple)):
            raise OperatorIngressAddressableMaterialError(
                "source spans must be a sequence"
            )
        rebuilt_spans = []
        for span in spans:
            if not isinstance(span, dict):
                _refuse("source span must be an object")
            try:
                rebuilt_spans.append(
                    SourceSpan(
                        span_ref=_exact_string(span.get("span_ref"), "span_ref"),
                        source_ref=_exact_string(span.get("source_ref"), "source_ref"),
                        start=_exact_int(span.get("start"), "span start"),
                        end=_exact_int(span.get("end"), "span end"),
                        exact_text=_exact_string(
                            span.get("exact_text"), "span text", empty=True
                        ),
                    )
                )
            except ContextualInterpretationWarrantSetError as error:
                _refuse(str(error))
        try:
            material = ExactOperatorMaterial(
                material_ref=_exact_string(
                    material_value.get("material_ref"), "material_ref"
                ),
                exact_text=_exact_string(
                    material_value.get("exact_text"), "exact_text", empty=True
                ),
                source_spans=tuple(rebuilt_spans),
                provenance=_string_tuple(
                    material_value.get("provenance"), "material provenance"
                ),
            )
        except ContextualInterpretationWarrantSetError as error:
            _refuse(str(error))
        return cls(
            artifact_type=_exact_string(value.get("artifact_type"), "artifact_type"),
            material_projection_id=_exact_string(
                value.get("material_projection_id"), "material_projection_id"
            ),
            ingress_event_ref=_exact_string(
                value.get("ingress_event_ref"), "ingress_event_ref"
            ),
            raw_material_event_ref=_exact_string(
                value.get("raw_material_event_ref"), "raw_material_event_ref"
            ),
            representation_examination_event_ref=_exact_string(
                value.get("representation_examination_event_ref"),
                "representation_examination_event_ref",
            ),
            exact_operator_material=material,
            source_role=_exact_string(value.get("source_role"), "source_role"),
            provenance=_string_tuple(value.get("provenance"), "provenance"),
            scope=_string_tuple(value.get("scope"), "scope"),
            known_loss=_string_tuple(value.get("known_loss"), "known_loss"),
            unknowns=_string_tuple(value.get("unknowns"), "unknowns"),
            authority_limits=_string_tuple(
                value.get("authority_limits"), "authority_limits"
            ),
            read_only=_exact_bool(value.get("read_only"), "read_only"),
            writes_event_ledger=_exact_bool(
                value.get("writes_event_ledger"), "writes_event_ledger"
            ),
            mutates_state=_exact_bool(value.get("mutates_state"), "mutates_state"),
            mutates_cluster=_exact_bool(
                value.get("mutates_cluster"), "mutates_cluster"
            ),
        )


def _refuse(message: str) -> None:
    raise OperatorIngressAddressableMaterialError(message)


def _exact_string(value: object, name: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value):
        _refuse(f"{name} must be a string")
    return value


def _exact_bool(value: object, name: str) -> bool:
    if type(value) is not bool:
        _refuse(f"{name} must be a boolean")
    return value


def _exact_int(value: object, name: str) -> int:
    if type(value) is not int:
        _refuse(f"{name} must be an integer")
    return value


def _string_tuple(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(item, str) for item in value
    ):
        _refuse(f"{name} must be a sequence of strings")
    return tuple(value)


def _intrinsic_string_tuple(value: object, name: str) -> None:
    if type(value) is not tuple or not all(type(item) is str for item in value):
        _refuse(f"{name} must be an exact tuple of strings")


def _intrinsic_string(value: object, name: str, *, empty: bool = False) -> None:
    if type(value) is not str or (not empty and not value):
        _refuse(f"{name} must be an exact string")


def _intrinsic_int(value: object, name: str) -> None:
    if type(value) is not int:
        _refuse(f"{name} must be an exact integer")


def validate_operator_ingress_addressable_material(
    artifact: OperatorIngressAddressableMaterial,
) -> None:
    """Validate the complete frozen artifact without consulting the ledger."""
    if not isinstance(artifact, OperatorIngressAddressableMaterial):
        _refuse("artifact must be OperatorIngressAddressableMaterial")
    artifact._validate_intrinsic_invariants()


def form_operator_ingress_addressable_material(
    *, ingress_occurrence: Event, ledger: EventLedger
) -> OperatorIngressAddressableMaterial:
    """Form exact material from one verified, decoded initial-ingress occurrence."""
    payload = ingress_occurrence.payload
    if ingress_occurrence.kind != "operator.ingress.common_grammar.ingress_occurred":
        _refuse("a decoded ingress occurrence is required")
    if payload.get("ingress_kind") not in {"text", "empty"}:
        _refuse("ingress framing must be text or empty")
    exact_text = payload.get("decoded_text")
    if not isinstance(exact_text, str):
        _refuse("exact decoded_text is required")
    attempt = payload.get("attempt_ref")
    raw_ref = payload.get("raw_material_event_id")
    examination_ref = payload.get("representation_examination_event_id")
    if not all(
        isinstance(ref, str) and ref for ref in (attempt, raw_ref, examination_ref)
    ):
        _refuse("complete attempt and representation lineage is required")
    if payload.get("lineage") != [raw_ref, examination_ref]:
        _refuse("lineage must preserve capture followed by examination")
    dimensions = payload.get("dimensions")
    if not isinstance(dimensions, dict) or dimensions.get("authority_warrant") != (
        "occurrence-only; meaning Unknown"
    ):
        _refuse("occurrence-only authority with meaning Unknown is required")
    recorded = ledger.get(ingress_occurrence.id)
    if recorded is None or recorded != ingress_occurrence:
        _refuse("the supplied ingress occurrence is not the recorded occurrence")
    raw = ledger.get(raw_ref)
    examination = ledger.get(examination_ref)
    common = (ingress_occurrence.workspace_id, ingress_occurrence.session_id, attempt)
    if raw is None or (
        raw.kind != "operator.ingress.common_grammar.raw_material_captured"
        or raw.payload.get("material_role") != "initial_ingress"
        or (raw.workspace_id, raw.session_id, raw.payload.get("attempt_ref")) != common
    ):
        _refuse("initial raw-material lineage is missing or foreign")
    if examination is None or (
        examination.kind != "operator.ingress.common_grammar.representation_examined"
        or examination.payload.get("material_role") != "initial_ingress"
        or examination.payload.get("capture_event_id") != raw.id
        or examination.payload.get("decoder_succeeded") is not True
        or examination.payload.get("decoder_outcome") != "decoded"
        or (
            examination.workspace_id,
            examination.session_id,
            examination.payload.get("attempt_ref"),
        )
        != common
    ):
        _refuse("successful initial representation examination is missing or foreign")

    provenance = (raw.id, examination.id, ingress_occurrence.id)
    span_ref = operator_material_full_span_id(
        ingress_event_ref=ingress_occurrence.id, exact_text=exact_text
    )
    exact_material = ExactOperatorMaterial(
        material_ref=ingress_occurrence.id,
        exact_text=exact_text,
        source_spans=(
            SourceSpan(
                span_ref=span_ref,
                source_ref=ingress_occurrence.id,
                start=0,
                end=len(exact_text),
                exact_text=exact_text,
            ),
        ),
        provenance=provenance,
    )
    projection_id = addressable_material_projection_id(exact_material)
    return OperatorIngressAddressableMaterial(
        artifact_type="operator_ingress_addressable_material",
        material_projection_id=projection_id,
        ingress_event_ref=ingress_occurrence.id,
        raw_material_event_ref=raw.id,
        representation_examination_event_ref=examination.id,
        exact_operator_material=exact_material,
        source_role="operator-origin material at the preserved ingress boundary",
        provenance=provenance,
        scope=(
            f"workspace:{ingress_occurrence.workspace_id}",
            f"session:{ingress_occurrence.session_id}",
            f"attempt:{attempt}",
        ),
        known_loss=tuple(payload.get("known_loss", ())),
        unknowns=UNKNOWNS,
        authority_limits=AUTHORITY_LIMITS,
    )
