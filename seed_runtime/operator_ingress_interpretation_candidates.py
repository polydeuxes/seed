"""Preserve attributed interpretation-candidate testimony for exact ingress material."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json

from seed_runtime.contextual_interpretation_warrant_set import InterpretationCandidate
from seed_runtime.operator_ingress_addressable_material import (
    OperatorIngressAddressableMaterial,
    OperatorIngressAddressableMaterialError,
    validate_operator_ingress_addressable_material,
)

CONVENTION = "operator_ingress_interpretation_candidate_set_v1"
ARTIFACT_TYPE = "operator_ingress_interpretation_candidate_set"
FORMATION_UNKNOWN = "candidate formation occurrence Unknown"
SOURCE_RELATION_UNKNOWN = "candidate source-material relation unavailable"
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
    supplied_authority_limits: tuple[str, ...]


@dataclass(frozen=True)
class OperatorIngressInterpretationCandidateSet:
    artifact_type: str
    candidate_set_id: str
    addressable_material: OperatorIngressAddressableMaterial
    candidate_testimonies: tuple[AttributedInterpretationCandidateTestimony, ...]
    set_unknowns: tuple[str, ...]
    set_conflicts: tuple[str, ...]
    boundary_notes: tuple[str, ...]
    # Uniform limits belong to this preservation responsibility, not its suppliers.
    preservation_authority_limits: tuple[str, ...]
    convention: str = CONVENTION
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_state: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_json_dict(
        cls, value: dict[str, object]
    ) -> OperatorIngressInterpretationCandidateSet:
        mapping = _mapping(value, "candidate set")
        if mapping.get("artifact_type") != ARTIFACT_TYPE:
            _refuse("wrong artifact_type")
        if mapping.get("convention") != CONVENTION:
            _refuse("wrong convention")
        try:
            addressable = OperatorIngressAddressableMaterial.from_json_dict(
                _mapping(mapping.get("addressable_material"), "addressable material")
            )
        except OperatorIngressAddressableMaterialError as error:
            _refuse(str(error))
        testimonies = tuple(
            _testimony_from_json(item)
            for item in _sequence(
                mapping.get("candidate_testimonies"), "candidate testimonies"
            )
        )
        result = cls(
            artifact_type=ARTIFACT_TYPE,
            candidate_set_id=_string(
                mapping.get("candidate_set_id"), "candidate_set_id"
            ),
            addressable_material=addressable,
            candidate_testimonies=testimonies,
            set_unknowns=_string_tuple(mapping.get("set_unknowns"), "set_unknowns"),
            set_conflicts=_string_tuple(mapping.get("set_conflicts"), "set_conflicts"),
            boundary_notes=_string_tuple(
                mapping.get("boundary_notes"), "boundary_notes"
            ),
            preservation_authority_limits=_string_tuple(
                mapping.get("preservation_authority_limits"),
                "preservation_authority_limits",
            ),
            convention=CONVENTION,
            read_only=_boolean(mapping.get("read_only"), "read_only"),
            writes_event_ledger=_boolean(
                mapping.get("writes_event_ledger"), "writes_event_ledger"
            ),
            mutates_state=_boolean(mapping.get("mutates_state"), "mutates_state"),
            mutates_cluster=_boolean(mapping.get("mutates_cluster"), "mutates_cluster"),
        )
        _validate_set(result)
        if result.candidate_set_id != _candidate_set_id(result):
            _refuse("candidate_set_id is forged or stale")
        return result


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
        _refuse(f"{name} must be a string")
    return value


def _string_tuple(value: object, name: str) -> tuple[str, ...]:
    sequence = _sequence(value, name)
    if not all(isinstance(item, str) for item in sequence):
        _refuse(f"{name} must contain only strings")
    return tuple(sequence)


def _boolean(value: object, name: str) -> bool:
    if type(value) is not bool:
        _refuse(f"{name} must be a boolean")
    return value


def _append_unknown(values: tuple[str, ...], value: str) -> tuple[str, ...]:
    return values if value in values else values + (value,)


def _testimony_from_json(raw: object) -> AttributedInterpretationCandidateTestimony:
    value = _mapping(raw, "candidate testimony")
    candidate_value = _mapping(value.get("candidate"), "candidate")
    candidate = InterpretationCandidate(
        candidate_ref=_string(candidate_value.get("candidate_ref"), "candidate_ref"),
        label=_string(candidate_value.get("label"), "candidate label", empty=True),
        source_span_refs=_string_tuple(
            candidate_value.get("source_span_refs"), "source_span_refs"
        ),
        proposed_meaning=_string(
            candidate_value.get("proposed_meaning"), "proposed_meaning", empty=True
        ),
    )
    formation = value.get("formation_occurrence_ref")
    if formation is not None:
        _string(formation, "formation_occurrence_ref")
    testimony = AttributedInterpretationCandidateTestimony(
        candidate=candidate,
        attributed_supplier=_string(
            value.get("attributed_supplier"), "attributed_supplier"
        ),
        supplier_provenance=_string_tuple(
            value.get("supplier_provenance"), "supplier_provenance"
        ),
        formation_occurrence_ref=formation,
        declared_scope=_string_tuple(value.get("declared_scope"), "declared_scope"),
        known_loss=_string_tuple(value.get("known_loss"), "known_loss"),
        unknowns=_string_tuple(value.get("unknowns"), "unknowns"),
        conflicts=_string_tuple(value.get("conflicts"), "conflicts"),
        supplied_authority_limits=_string_tuple(
            value.get("supplied_authority_limits"), "supplied_authority_limits"
        ),
    )
    _validate_testimony(testimony)
    return testimony


def _identity_payload(
    value: OperatorIngressInterpretationCandidateSet,
) -> dict[str, object]:
    return {
        "addressable_material": asdict(value.addressable_material),
        "candidate_testimonies": [asdict(item) for item in value.candidate_testimonies],
        "preservation_authority_limits": value.preservation_authority_limits,
        "set_unknowns": value.set_unknowns,
        "set_conflicts": value.set_conflicts,
        "boundary_notes": value.boundary_notes,
        "convention": value.convention,
    }


def _candidate_set_id(value: OperatorIngressInterpretationCandidateSet) -> str:
    encoded = json.dumps(
        _identity_payload(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return (
        "operator-ingress-interpretation-candidate-set:"
        + hashlib.sha256(encoded.encode()).hexdigest()
    )


def _validate_material(addressable: OperatorIngressAddressableMaterial) -> None:
    try:
        validate_operator_ingress_addressable_material(addressable)
    except OperatorIngressAddressableMaterialError as error:
        _refuse(str(error))


def _validate_testimony(value: object) -> None:
    if not isinstance(value, AttributedInterpretationCandidateTestimony):
        _refuse("candidate testimonies must contain testimony objects")
    candidate = value.candidate
    if not isinstance(candidate, InterpretationCandidate):
        _refuse("candidate must be an InterpretationCandidate")
    _string(candidate.candidate_ref, "candidate_ref")
    _string(candidate.label, "candidate label", empty=True)
    _string_tuple(candidate.source_span_refs, "source_span_refs")
    _string(candidate.proposed_meaning, "proposed_meaning", empty=True)
    _string(value.attributed_supplier, "attributed_supplier")
    _string_tuple(value.supplier_provenance, "supplier_provenance")
    if value.formation_occurrence_ref is not None:
        _string(value.formation_occurrence_ref, "formation_occurrence_ref")
    _string_tuple(value.declared_scope, "declared_scope")
    _string_tuple(value.known_loss, "known_loss")
    _string_tuple(value.unknowns, "unknowns")
    _string_tuple(value.conflicts, "conflicts")
    _string_tuple(value.supplied_authority_limits, "supplied_authority_limits")


def _typed_testimony(
    value: AttributedInterpretationCandidateTestimony,
) -> AttributedInterpretationCandidateTestimony:
    """Copy validated testimony into the exact frozen coordinate shapes."""
    candidate = replace(
        value.candidate, source_span_refs=tuple(value.candidate.source_span_refs)
    )
    return replace(
        value,
        candidate=candidate,
        supplier_provenance=tuple(value.supplier_provenance),
        declared_scope=tuple(value.declared_scope),
        known_loss=tuple(value.known_loss),
        unknowns=tuple(value.unknowns),
        conflicts=tuple(value.conflicts),
        supplied_authority_limits=tuple(value.supplied_authority_limits),
    )


def _validate_set(value: OperatorIngressInterpretationCandidateSet) -> None:
    if value.artifact_type != ARTIFACT_TYPE:
        _refuse("wrong artifact_type")
    if value.convention != CONVENTION:
        _refuse("wrong convention")
    if value.boundary_notes != BOUNDARY_NOTES:
        _refuse("v1 boundary_notes are repository-owned")
    if value.preservation_authority_limits != REQUIRED_AUTHORITY_LIMITS:
        _refuse("v1 preservation authority limits are repository-owned")
    _string_tuple(value.set_unknowns, "set_unknowns")
    _string_tuple(value.set_conflicts, "set_conflicts")
    _sequence(value.candidate_testimonies, "candidate testimonies")
    _validate_material(value.addressable_material)
    if value.read_only is not True or any(
        item is not False
        for item in (
            value.writes_event_ledger,
            value.mutates_state,
            value.mutates_cluster,
        )
    ):
        _refuse("candidate set must be read-only and non-mutating")
    refs: set[str] = set()
    spans = {
        span.span_ref
        for span in value.addressable_material.exact_operator_material.source_spans
    }
    for testimony in value.candidate_testimonies:
        _validate_testimony(testimony)
        candidate = testimony.candidate
        if not candidate.candidate_ref or candidate.candidate_ref in refs:
            _refuse("candidate refs must be nonempty and unique")
        refs.add(candidate.candidate_ref)
        if any(ref not in spans for ref in candidate.source_span_refs):
            _refuse("candidate references a foreign source span")


def preserve_operator_ingress_interpretation_candidates(
    *,
    addressable_material: OperatorIngressAddressableMaterial,
    candidate_testimonies: tuple[AttributedInterpretationCandidateTestimony, ...],
    set_unknowns: tuple[str, ...] = (),
    set_conflicts: tuple[str, ...] = (),
) -> OperatorIngressInterpretationCandidateSet:
    """Preserve supplied testimony without generating or examining interpretation."""
    _validate_material(addressable_material)
    _sequence(candidate_testimonies, "candidate testimonies")
    set_unknowns = _string_tuple(set_unknowns, "set_unknowns")
    set_conflicts = _string_tuple(set_conflicts, "set_conflicts")
    preserved = []
    for supplied in candidate_testimonies:
        _validate_testimony(supplied)
        supplied = _typed_testimony(supplied)
        unknowns = supplied.unknowns
        if supplied.formation_occurrence_ref is None:
            unknowns = _append_unknown(unknowns, FORMATION_UNKNOWN)
        if not supplied.candidate.source_span_refs:
            unknowns = _append_unknown(unknowns, SOURCE_RELATION_UNKNOWN)
        if supplied.candidate.proposed_meaning == "":
            unknowns = _append_unknown(unknowns, PROPOSITION_UNKNOWN)
        preserved.append(replace(supplied, unknowns=unknowns))
    if not preserved:
        set_unknowns = _append_unknown(set_unknowns, NO_CANDIDATES_UNKNOWN)
    result = OperatorIngressInterpretationCandidateSet(
        artifact_type=ARTIFACT_TYPE,
        candidate_set_id="pending",
        addressable_material=addressable_material,
        candidate_testimonies=tuple(preserved),
        set_unknowns=set_unknowns,
        set_conflicts=set_conflicts,
        boundary_notes=BOUNDARY_NOTES,
        preservation_authority_limits=REQUIRED_AUTHORITY_LIMITS,
    )
    _validate_set(result)
    return replace(result, candidate_set_id=_candidate_set_id(result))
