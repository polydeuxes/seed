"""Preserve attributed interpretation-candidate testimony for exact ingress material."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json

from seed_runtime.contextual_interpretation_warrant_set import (
    ExactOperatorMaterial,
    InterpretationCandidate,
    SourceSpan,
)
from seed_runtime.operator_ingress_addressable_material import (
    OperatorIngressAddressableMaterial,
)

CONVENTION = "operator_ingress_interpretation_candidate_set_v1"
FORMATION_UNKNOWN = "candidate formation occurrence Unknown"
NO_CANDIDATES_UNKNOWN = "no interpretation candidate testimony presently supplied"
PROPOSITION_UNKNOWN = "candidate proposition unavailable"
REQUIRED_AUTHORITY_LIMITS = (
    "proposes one possible interpretation only",
    "does not warrant its proposed meaning",
    "does not establish operator intent, goal, question, command, request, or treatment",
    "does not establish selection, applicability, admission, BOGE standing, Demand, movement, authorization, execution, or truth",
)
BOUNDARY_NOTES = (
    "Candidate testimony is attributed external or caller-supplied grammar, not Seed-generated meaning.",
    "Preservation does not evaluate, warrant, rank, select, apply, admit, or act on a candidate.",
    "A unique candidate is not a selected or warranted candidate; multiple candidates are not an ambiguity resolution.",
)


class OperatorIngressInterpretationCandidateSetError(ValueError):
    """The supplied material or candidate testimony cannot be preserved lawfully."""


@dataclass(frozen=True)
class AttributedInterpretationCandidateTestimony:
    candidate: InterpretationCandidate
    attributed_supplier: str
    supplier_provenance: tuple[str, ...]
    formation_occurrence_ref: str | None
    declared_scope: tuple[str, ...]
    known_loss: tuple[str, ...]
    unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    authority_limits: tuple[str, ...]


@dataclass(frozen=True)
class OperatorIngressInterpretationCandidateSet:
    artifact_type: str
    candidate_set_id: str
    addressable_material_projection_id: str
    ingress_event_ref: str
    exact_operator_material: ExactOperatorMaterial
    candidate_testimonies: tuple[AttributedInterpretationCandidateTestimony, ...]
    set_unknowns: tuple[str, ...]
    set_conflicts: tuple[str, ...]
    boundary_notes: tuple[str, ...]
    convention: str = CONVENTION
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_state: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, object]:
        """Return the artifact's single JSON-safe representation."""
        return asdict(self)

    @classmethod
    def from_json_dict(
        cls, value: dict[str, object]
    ) -> OperatorIngressInterpretationCandidateSet:
        """Recover an artifact from its exact JSON-safe representation."""
        material_value = _mapping(
            value.get("exact_operator_material"), "exact material"
        )
        material = ExactOperatorMaterial(
            material_ref=_string(material_value.get("material_ref"), "material_ref"),
            exact_text=_string(
                material_value.get("exact_text"), "exact_text", empty=True
            ),
            source_spans=tuple(
                SourceSpan(**_mapping(span, "source span"))
                for span in _sequence(
                    material_value.get("source_spans"), "source spans"
                )
            ),
            provenance=tuple(
                _sequence(material_value.get("provenance", ()), "material provenance")
            ),
        )
        testimonies = []
        for raw in _sequence(
            value.get("candidate_testimonies"), "candidate testimonies"
        ):
            testimony = _mapping(raw, "candidate testimony")
            candidate_value = _mapping(testimony.get("candidate"), "candidate")
            candidate = InterpretationCandidate(
                candidate_ref=_string(
                    candidate_value.get("candidate_ref"), "candidate_ref"
                ),
                label=_string(
                    candidate_value.get("label"), "candidate label", empty=True
                ),
                source_span_refs=tuple(
                    _sequence(
                        candidate_value.get("source_span_refs"),
                        "candidate source spans",
                    )
                ),
                proposed_meaning=_string(
                    candidate_value.get("proposed_meaning"),
                    "proposed meaning",
                    empty=True,
                ),
            )
            formation = testimony.get("formation_occurrence_ref")
            if formation is not None and not isinstance(formation, str):
                _refuse("formation_occurrence_ref must be a string or None")
            testimonies.append(
                AttributedInterpretationCandidateTestimony(
                    candidate=candidate,
                    attributed_supplier=_string(
                        testimony.get("attributed_supplier"), "attributed supplier"
                    ),
                    supplier_provenance=tuple(testimony["supplier_provenance"]),
                    formation_occurrence_ref=formation,
                    declared_scope=tuple(testimony["declared_scope"]),
                    known_loss=tuple(testimony["known_loss"]),
                    unknowns=tuple(testimony["unknowns"]),
                    conflicts=tuple(testimony["conflicts"]),
                    authority_limits=tuple(testimony["authority_limits"]),
                )
            )
        return cls(
            artifact_type=_string(value.get("artifact_type"), "artifact_type"),
            candidate_set_id=_string(value.get("candidate_set_id"), "candidate_set_id"),
            addressable_material_projection_id=_string(
                value.get("addressable_material_projection_id"),
                "material projection id",
            ),
            ingress_event_ref=_string(
                value.get("ingress_event_ref"), "ingress event ref"
            ),
            exact_operator_material=material,
            candidate_testimonies=tuple(testimonies),
            set_unknowns=tuple(value["set_unknowns"]),
            set_conflicts=tuple(value["set_conflicts"]),
            boundary_notes=tuple(value["boundary_notes"]),
            convention=_string(value.get("convention"), "convention"),
            read_only=bool(value["read_only"]),
            writes_event_ledger=bool(value["writes_event_ledger"]),
            mutates_state=bool(value["mutates_state"]),
            mutates_cluster=bool(value["mutates_cluster"]),
        )


def _refuse(message: str) -> None:
    raise OperatorIngressInterpretationCandidateSetError(message)


def _mapping(value: object, name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        _refuse(f"{name} must be an object")
    return value


def _sequence(value: object, name: str) -> list[object] | tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        _refuse(f"{name} must be a sequence")
    return value


def _string(value: object, name: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value):
        _refuse(f"{name} must be a{' possibly empty' if empty else ' nonempty'} string")
    return value


def _append_once(values: tuple[str, ...], required: tuple[str, ...]) -> tuple[str, ...]:
    return values + tuple(value for value in required if value not in values)


def _validate_material(addressable: OperatorIngressAddressableMaterial) -> None:
    if addressable.artifact_type != "operator_ingress_addressable_material":
        _refuse("operator_ingress_addressable_material is required")
    if not addressable.read_only or any(
        (
            addressable.writes_event_ledger,
            addressable.mutates_state,
            addressable.mutates_cluster,
        )
    ):
        _refuse("addressable material must be read-only and non-mutating")
    material = addressable.exact_operator_material
    if material.material_ref != addressable.ingress_event_ref:
        _refuse("exact material must reference the ingress event")
    if material.provenance != addressable.provenance:
        _refuse("exact material must preserve addressable provenance")
    seen: set[str] = set()
    for span in material.source_spans:
        if span.span_ref in seen:
            _refuse("source span refs must be unique")
        seen.add(span.span_ref)
        if span.source_ref != material.material_ref:
            _refuse("source span belongs to foreign material")
        if (
            span.start < 0
            or span.end < span.start
            or span.end > len(material.exact_text)
        ):
            _refuse("source span offsets exceed exact material")
        if material.exact_text[span.start : span.end] != span.exact_text:
            _refuse("source span text does not match exact material")


def preserve_operator_ingress_interpretation_candidates(
    *,
    addressable_material: OperatorIngressAddressableMaterial,
    candidate_testimonies: tuple[AttributedInterpretationCandidateTestimony, ...],
    set_unknowns: tuple[str, ...] = (),
    set_conflicts: tuple[str, ...] = (),
) -> OperatorIngressInterpretationCandidateSet:
    """Preserve supplied testimony without generating or examining interpretation."""
    _validate_material(addressable_material)
    material = addressable_material.exact_operator_material
    spans = {span.span_ref: span for span in material.source_spans}
    refs: set[str] = set()
    preserved = []
    for testimony in candidate_testimonies:
        candidate = testimony.candidate
        if not candidate.candidate_ref:
            _refuse("candidate_ref must be nonempty")
        if candidate.candidate_ref in refs:
            _refuse("candidate refs must be unique")
        refs.add(candidate.candidate_ref)
        if not testimony.attributed_supplier:
            _refuse("candidate testimony requires supplier attribution")
        for span_ref in candidate.source_span_refs:
            if span_ref not in spans:
                _refuse("candidate references a foreign source span")
        unknowns = testimony.unknowns
        if testimony.formation_occurrence_ref is None:
            unknowns = _append_once(unknowns, (FORMATION_UNKNOWN,))
        if candidate.proposed_meaning == "":
            unknowns = _append_once(unknowns, (PROPOSITION_UNKNOWN,))
        preserved.append(
            replace(
                testimony,
                unknowns=unknowns,
                authority_limits=_append_once(
                    testimony.authority_limits, REQUIRED_AUTHORITY_LIMITS
                ),
            )
        )
    result_unknowns = set_unknowns
    if not preserved:
        result_unknowns = _append_once(result_unknowns, (NO_CANDIDATES_UNKNOWN,))
    identity = {
        "addressable_material_projection_id": addressable_material.material_projection_id,
        "exact_operator_material": asdict(material),
        "candidate_testimonies": [asdict(value) for value in preserved],
        "set_unknowns": result_unknowns,
        "set_conflicts": set_conflicts,
        "convention": CONVENTION,
    }
    encoded = json.dumps(
        identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    candidate_set_id = (
        "operator-ingress-interpretation-candidate-set:"
        + hashlib.sha256(encoded.encode()).hexdigest()
    )
    return OperatorIngressInterpretationCandidateSet(
        artifact_type="operator_ingress_interpretation_candidate_set",
        candidate_set_id=candidate_set_id,
        addressable_material_projection_id=addressable_material.material_projection_id,
        ingress_event_ref=addressable_material.ingress_event_ref,
        exact_operator_material=material,
        candidate_testimonies=tuple(preserved),
        set_unknowns=result_unknowns,
        set_conflicts=set_conflicts,
        boundary_notes=BOUNDARY_NOTES,
    )
