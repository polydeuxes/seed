"""Bounded formation of exact, source-addressable operator ingress material."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from seed_runtime.contextual_interpretation_warrant_set import (
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

    def to_json_dict(self) -> dict[str, object]:
        """Return the single JSON-safe projection representation."""
        return asdict(self)

    @classmethod
    def from_json_dict(
        cls, value: dict[str, object]
    ) -> OperatorIngressAddressableMaterial:
        """Recover the frozen artifact from its projection representation."""
        material_value = value["exact_operator_material"]
        if not isinstance(material_value, dict):
            raise OperatorIngressAddressableMaterialError(
                "exact material must be an object"
            )
        spans = material_value.get("source_spans")
        if not isinstance(spans, (list, tuple)):
            raise OperatorIngressAddressableMaterialError(
                "source spans must be a sequence"
            )
        material = ExactOperatorMaterial(
            material_ref=str(material_value["material_ref"]),
            exact_text=str(material_value["exact_text"]),
            source_spans=tuple(SourceSpan(**span) for span in spans),
            provenance=tuple(material_value.get("provenance", ())),
        )
        return cls(
            artifact_type=str(value["artifact_type"]),
            material_projection_id=str(value["material_projection_id"]),
            ingress_event_ref=str(value["ingress_event_ref"]),
            raw_material_event_ref=str(value["raw_material_event_ref"]),
            representation_examination_event_ref=str(
                value["representation_examination_event_ref"]
            ),
            exact_operator_material=material,
            source_role=str(value["source_role"]),
            provenance=tuple(value["provenance"]),
            scope=tuple(value["scope"]),
            known_loss=tuple(value["known_loss"]),
            unknowns=tuple(value["unknowns"]),
            authority_limits=tuple(value["authority_limits"]),
            read_only=bool(value["read_only"]),
            writes_event_ledger=bool(value["writes_event_ledger"]),
            mutates_state=bool(value["mutates_state"]),
            mutates_cluster=bool(value["mutates_cluster"]),
        )


def _refuse(message: str) -> None:
    raise OperatorIngressAddressableMaterialError(message)


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
    span_ref = _stable_id(
        "operator-material-full-span", (ingress_occurrence.id, exact_text)
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
    projection_id = _stable_id(
        "operator-ingress-addressable-material", asdict(exact_material)
    )
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
