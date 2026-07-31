"""Preserve attributed interpretation-candidate testimony for exact ingress material."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from seed_runtime.contextual_interpretation_warrant_set import (
    ContextualInterpretationWarrantSetError,
    InterpretationCandidate,
)
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


def _refuse(message: str) -> None:
    raise OperatorIngressInterpretationCandidateSetError(message)


def _string(value: object, name: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value):
        _refuse(f"{name} must be a string")
    return value


def _intrinsic_string_tuple(value: object, name: str) -> None:
    if type(value) is not tuple or not all(isinstance(item, str) for item in value):
        _refuse(f"{name} must be an exact tuple of strings")


def _json_mapping(value: object, name: str) -> dict[str, object]:
    if not isinstance(value, dict):
        _refuse(f"{name} must be an object")
    return value


def _json_sequence(value: object, name: str) -> list[object] | tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        _refuse(f"{name} must be a sequence")
    return value


def _json_string_tuple(value: object, name: str) -> tuple[str, ...]:
    sequence = _json_sequence(value, name)
    if not all(isinstance(item, str) for item in sequence):
        _refuse(f"{name} must contain only strings")
    return tuple(sequence)


def _boolean(value: object, name: str) -> bool:
    if type(value) is not bool:
        _refuse(f"{name} must be a boolean")
    return value


def _validate_supplier_coordinates(value: object) -> None:
    candidate = getattr(value, "candidate", None)
    if not isinstance(candidate, InterpretationCandidate):
        _refuse("candidate must be an InterpretationCandidate")
    _string(candidate.candidate_ref, "candidate_ref")
    _string(candidate.label, "candidate label", empty=True)
    _intrinsic_string_tuple(candidate.source_span_refs, "source_span_refs")
    _string(candidate.proposed_meaning, "proposed_meaning", empty=True)
    _string(value.attributed_supplier, "attributed_supplier")
    _intrinsic_string_tuple(value.supplier_provenance, "supplier_provenance")
    if value.formation_occurrence_ref is not None:
        _string(value.formation_occurrence_ref, "formation_occurrence_ref")
    for name in (
        "declared_scope",
        "known_loss",
        "supplied_unknowns",
        "conflicts",
        "supplied_authority_limits",
    ):
        _intrinsic_string_tuple(getattr(value, name), name)


def _derived_preservation_unknowns(
    candidate: InterpretationCandidate, formation_occurrence_ref: str | None
) -> tuple[str, ...]:
    findings = []
    if formation_occurrence_ref is None:
        findings.append(FORMATION_UNKNOWN)
    if not candidate.source_span_refs:
        findings.append(SOURCE_RELATION_UNKNOWN)
    if candidate.proposed_meaning == "":
        findings.append(PROPOSITION_UNKNOWN)
    return tuple(findings)


@dataclass(frozen=True)
class SuppliedInterpretationCandidateTestimony:
    candidate: InterpretationCandidate
    attributed_supplier: str
    supplier_provenance: tuple[str, ...]
    formation_occurrence_ref: str | None
    declared_scope: tuple[str, ...]
    known_loss: tuple[str, ...]
    supplied_unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    supplied_authority_limits: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_supplier_coordinates(self)


@dataclass(frozen=True)
class AttributedInterpretationCandidateTestimony:
    candidate: InterpretationCandidate
    attributed_supplier: str
    supplier_provenance: tuple[str, ...]
    formation_occurrence_ref: str | None
    declared_scope: tuple[str, ...]
    known_loss: tuple[str, ...]
    supplied_unknowns: tuple[str, ...]
    preservation_unknowns: tuple[str, ...]
    conflicts: tuple[str, ...]
    supplied_authority_limits: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_supplier_coordinates(self)
        _intrinsic_string_tuple(self.preservation_unknowns, "preservation_unknowns")
        if self.preservation_unknowns != _derived_preservation_unknowns(
            self.candidate, self.formation_occurrence_ref
        ):
            _refuse("preservation_unknowns do not match repository-derived findings")


def candidate_set_identity_payload(
    *,
    addressable_material: OperatorIngressAddressableMaterial,
    candidate_testimonies: tuple[AttributedInterpretationCandidateTestimony, ...],
    supplied_set_unknowns: tuple[str, ...],
    preservation_set_unknowns: tuple[str, ...],
    set_conflicts: tuple[str, ...],
    boundary_notes: tuple[str, ...],
    preservation_authority_limits: tuple[str, ...],
    convention: str,
) -> dict[str, object]:
    return {
        "addressable_material": asdict(addressable_material),
        "candidate_testimonies": [asdict(item) for item in candidate_testimonies],
        "supplied_set_unknowns": supplied_set_unknowns,
        "preservation_set_unknowns": preservation_set_unknowns,
        "set_conflicts": set_conflicts,
        "boundary_notes": boundary_notes,
        "preservation_authority_limits": preservation_authority_limits,
        "convention": convention,
    }


def candidate_set_id_from_fields(**fields: object) -> str:
    encoded = json.dumps(
        candidate_set_identity_payload(**fields),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return (
        "operator-ingress-interpretation-candidate-set:"
        + hashlib.sha256(encoded.encode()).hexdigest()
    )


@dataclass(frozen=True)
class OperatorIngressInterpretationCandidateSet:
    artifact_type: str
    candidate_set_id: str
    addressable_material: OperatorIngressAddressableMaterial
    candidate_testimonies: tuple[AttributedInterpretationCandidateTestimony, ...]
    supplied_set_unknowns: tuple[str, ...]
    preservation_set_unknowns: tuple[str, ...]
    set_conflicts: tuple[str, ...]
    boundary_notes: tuple[str, ...]
    preservation_authority_limits: tuple[str, ...]
    convention: str = CONVENTION
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_state: bool = False
    mutates_cluster: bool = False

    def __post_init__(self) -> None:
        self._validate_intrinsic_invariants()

    def _validate_intrinsic_invariants(self) -> None:
        if self.artifact_type != ARTIFACT_TYPE:
            _refuse("wrong artifact_type")
        if self.convention != CONVENTION:
            _refuse("wrong convention")
        if self.boundary_notes != BOUNDARY_NOTES:
            _refuse("v1 boundary_notes are repository-owned")
        if self.preservation_authority_limits != REQUIRED_AUTHORITY_LIMITS:
            _refuse("v1 preservation authority limits are repository-owned")
        for name in (
            "candidate_testimonies",
            "supplied_set_unknowns",
            "preservation_set_unknowns",
            "set_conflicts",
            "boundary_notes",
            "preservation_authority_limits",
        ):
            value = getattr(self, name)
            if name == "candidate_testimonies":
                if type(value) is not tuple:
                    _refuse("candidate testimonies must be an exact tuple")
            else:
                _intrinsic_string_tuple(value, name)
        try:
            validate_operator_ingress_addressable_material(self.addressable_material)
        except OperatorIngressAddressableMaterialError as error:
            _refuse(str(error))
        if self.read_only is not True or any(
            item is not False
            for item in (
                self.writes_event_ledger,
                self.mutates_state,
                self.mutates_cluster,
            )
        ):
            _refuse("candidate set must be read-only and non-mutating")
        expected_set_unknowns = (
            () if self.candidate_testimonies else (NO_CANDIDATES_UNKNOWN,)
        )
        if self.preservation_set_unknowns != expected_set_unknowns:
            _refuse("preservation_set_unknowns do not match candidate-set findings")
        refs: set[str] = set()
        spans = {
            span.span_ref
            for span in self.addressable_material.exact_operator_material.source_spans
        }
        for testimony in self.candidate_testimonies:
            if not isinstance(testimony, AttributedInterpretationCandidateTestimony):
                _refuse(
                    "candidate testimonies must contain attributed testimony objects"
                )
            testimony.__post_init__()
            candidate = testimony.candidate
            if candidate.candidate_ref in refs:
                _refuse("candidate refs must be nonempty and unique")
            refs.add(candidate.candidate_ref)
            if any(ref not in spans for ref in candidate.source_span_refs):
                _refuse("candidate references a foreign source span")
        _string(self.candidate_set_id, "candidate_set_id")
        expected_id = candidate_set_id_from_fields(
            addressable_material=self.addressable_material,
            candidate_testimonies=self.candidate_testimonies,
            supplied_set_unknowns=self.supplied_set_unknowns,
            preservation_set_unknowns=self.preservation_set_unknowns,
            set_conflicts=self.set_conflicts,
            boundary_notes=self.boundary_notes,
            preservation_authority_limits=self.preservation_authority_limits,
            convention=self.convention,
        )
        if self.candidate_set_id != expected_id:
            _refuse("candidate_set_id is forged or stale")

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_json_dict(
        cls, value: dict[str, object]
    ) -> OperatorIngressInterpretationCandidateSet:
        mapping = _json_mapping(value, "candidate set")
        try:
            addressable = OperatorIngressAddressableMaterial.from_json_dict(
                _json_mapping(
                    mapping.get("addressable_material"), "addressable material"
                )
            )
            testimonies = tuple(
                _attributed_testimony_from_json(item)
                for item in _json_sequence(
                    mapping.get("candidate_testimonies"), "candidate testimonies"
                )
            )
        except (
            OperatorIngressAddressableMaterialError,
            ContextualInterpretationWarrantSetError,
        ) as error:
            _refuse(str(error))
        return cls(
            artifact_type=_string(mapping.get("artifact_type"), "artifact_type"),
            candidate_set_id=_string(
                mapping.get("candidate_set_id"), "candidate_set_id"
            ),
            addressable_material=addressable,
            candidate_testimonies=testimonies,
            supplied_set_unknowns=_json_string_tuple(
                mapping.get("supplied_set_unknowns"), "supplied_set_unknowns"
            ),
            preservation_set_unknowns=_json_string_tuple(
                mapping.get("preservation_set_unknowns"), "preservation_set_unknowns"
            ),
            set_conflicts=_json_string_tuple(
                mapping.get("set_conflicts"), "set_conflicts"
            ),
            boundary_notes=_json_string_tuple(
                mapping.get("boundary_notes"), "boundary_notes"
            ),
            preservation_authority_limits=_json_string_tuple(
                mapping.get("preservation_authority_limits"),
                "preservation_authority_limits",
            ),
            convention=_string(mapping.get("convention"), "convention"),
            read_only=_boolean(mapping.get("read_only"), "read_only"),
            writes_event_ledger=_boolean(
                mapping.get("writes_event_ledger"), "writes_event_ledger"
            ),
            mutates_state=_boolean(mapping.get("mutates_state"), "mutates_state"),
            mutates_cluster=_boolean(mapping.get("mutates_cluster"), "mutates_cluster"),
        )


def _attributed_testimony_from_json(
    raw: object,
) -> AttributedInterpretationCandidateTestimony:
    value = _json_mapping(raw, "candidate testimony")
    candidate_value = _json_mapping(value.get("candidate"), "candidate")
    try:
        candidate = InterpretationCandidate(
            candidate_ref=_string(
                candidate_value.get("candidate_ref"), "candidate_ref"
            ),
            label=_string(candidate_value.get("label"), "candidate label", empty=True),
            source_span_refs=_json_string_tuple(
                candidate_value.get("source_span_refs"), "source_span_refs"
            ),
            proposed_meaning=_string(
                candidate_value.get("proposed_meaning"), "proposed_meaning", empty=True
            ),
        )
    except ContextualInterpretationWarrantSetError as error:
        _refuse(str(error))
    formation = value.get("formation_occurrence_ref")
    if formation is not None:
        _string(formation, "formation_occurrence_ref")
    return AttributedInterpretationCandidateTestimony(
        candidate=candidate,
        attributed_supplier=_string(
            value.get("attributed_supplier"), "attributed_supplier"
        ),
        supplier_provenance=_json_string_tuple(
            value.get("supplier_provenance"), "supplier_provenance"
        ),
        formation_occurrence_ref=formation,
        declared_scope=_json_string_tuple(
            value.get("declared_scope"), "declared_scope"
        ),
        known_loss=_json_string_tuple(value.get("known_loss"), "known_loss"),
        supplied_unknowns=_json_string_tuple(
            value.get("supplied_unknowns"), "supplied_unknowns"
        ),
        preservation_unknowns=_json_string_tuple(
            value.get("preservation_unknowns"), "preservation_unknowns"
        ),
        conflicts=_json_string_tuple(value.get("conflicts"), "conflicts"),
        supplied_authority_limits=_json_string_tuple(
            value.get("supplied_authority_limits"), "supplied_authority_limits"
        ),
    )


def preserve_operator_ingress_interpretation_candidates(
    *,
    addressable_material: OperatorIngressAddressableMaterial,
    candidate_testimonies: tuple[SuppliedInterpretationCandidateTestimony, ...],
    supplied_set_unknowns: tuple[str, ...] = (),
    set_conflicts: tuple[str, ...] = (),
) -> OperatorIngressInterpretationCandidateSet:
    """Preserve supplied testimony without generating or examining interpretation."""
    try:
        validate_operator_ingress_addressable_material(addressable_material)
    except OperatorIngressAddressableMaterialError as error:
        _refuse(str(error))
    if type(candidate_testimonies) is not tuple:
        _refuse("candidate testimonies must be an exact tuple")
    _intrinsic_string_tuple(supplied_set_unknowns, "supplied_set_unknowns")
    _intrinsic_string_tuple(set_conflicts, "set_conflicts")
    preserved = []
    for supplied in candidate_testimonies:
        if not isinstance(supplied, SuppliedInterpretationCandidateTestimony):
            _refuse("candidate testimonies must contain supplied testimony objects")
        supplied.__post_init__()
        preserved.append(
            AttributedInterpretationCandidateTestimony(
                candidate=supplied.candidate,
                attributed_supplier=supplied.attributed_supplier,
                supplier_provenance=supplied.supplier_provenance,
                formation_occurrence_ref=supplied.formation_occurrence_ref,
                declared_scope=supplied.declared_scope,
                known_loss=supplied.known_loss,
                supplied_unknowns=supplied.supplied_unknowns,
                preservation_unknowns=_derived_preservation_unknowns(
                    supplied.candidate, supplied.formation_occurrence_ref
                ),
                conflicts=supplied.conflicts,
                supplied_authority_limits=supplied.supplied_authority_limits,
            )
        )
    attributed = tuple(preserved)
    preservation_set_unknowns = () if attributed else (NO_CANDIDATES_UNKNOWN,)
    identity_fields = dict(
        addressable_material=addressable_material,
        candidate_testimonies=attributed,
        supplied_set_unknowns=supplied_set_unknowns,
        preservation_set_unknowns=preservation_set_unknowns,
        set_conflicts=set_conflicts,
        boundary_notes=BOUNDARY_NOTES,
        preservation_authority_limits=REQUIRED_AUTHORITY_LIMITS,
        convention=CONVENTION,
    )
    return OperatorIngressInterpretationCandidateSet(
        artifact_type=ARTIFACT_TYPE,
        candidate_set_id=candidate_set_id_from_fields(**identity_fields),
        **identity_fields,
    )
