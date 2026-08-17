"""Candidate and Admission boundaries for one exact Representation emission."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from seed_runtime.event import Event
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.evidence_of_yield_relation import (
    RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND,
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)
from seed_runtime.operator_egress import read_operator_emission_boundary


REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.representation.candidate_responsibility_assignment_recorded"
)
REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND = (
    "operator.representation.candidate_act_evidenced"
)
REPRESENTATION_CANDIDATE_RECORDED_KIND = (
    "operator.representation.candidate_recorded"
)
EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND = (
    "operator.representation.exact_material_admission_responsibility_assignment_recorded"
)
EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND = (
    "operator.representation.exact_material_admission_act_evidenced"
)
EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND = (
    "operator.representation.exact_material_admission_recorded"
)

REPRESENTATION_CANDIDATE_BOOK_CLAUSE = "01.Source.E"
REPRESENTATION_ADMISSION_BOOK_CLAUSE = "01.Standing.E"
REPRESENTATION_CANDIDATE_ACT = (
    "Preserve one exact Representation as candidate for one emission Act"
)
REPRESENTATION_CANDIDATE_RESPONSIBILITY = (
    "preserve one exact Representation candidate for one operator Locality"
)
REPRESENTATION_ADMISSION_ACT = (
    "Determine Admission of one exact Representation candidate to one exact material operator Locality"
)
REPRESENTATION_ADMISSION_RESPONSIBILITY = (
    "determine Admission of one exact Representation candidate to one exact material operator Locality"
)
REPRESENTATION_CANDIDATE_RESULT_KIND = "exact Representation candidate result"
REPRESENTATION_ADMISSION_RESULT_KIND = "exact Representation Admission result"
REPRESENTATION_EMISSION_INPUT_ROLE = "exact bounded Representation"

EVENT_KIND_RESPONSIBILITIES = {
    REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Source.E",
    REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND: "02.Acts.A",
    REPRESENTATION_CANDIDATE_RECORDED_KIND: "01.Source.E",
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND: "01.Standing.E",
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND: "02.Acts.A",
    EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND: "01.Standing.E",
}


class RepresentationAdmissionError(ValueError):
    """One Representation Candidate or Admission boundary is not exact."""


def exact_material_representation_rule_is_applicable_to_boundary_rule(
    representation_rule: Any, boundary_rule: Any
) -> bool:
    """Read the one currently declared exact-material emission rule pair."""

    from seed_runtime.operator_egress import EXACT_MATERIAL_WRITE_BOUNDARY_RULE
    from seed_runtime.operator_representation import (
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
    )

    return (
        type(representation_rule) is str
        and representation_rule == EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
        and type(boundary_rule) is str
        and boundary_rule == EXACT_MATERIAL_WRITE_BOUNDARY_RULE
    )


def _require_identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise RepresentationAdmissionError(message)
    return value


def _authority(book_clause_identity: str, limit: str) -> dict[str, str]:
    return {
        "source": "active Book",
        "book_clause_identity": book_clause_identity,
        "standing": "bounded",
        "limit": limit,
    }


def _representation_reference(
    ledger: EventLedger,
    *,
    representation_event_identity: str,
) -> dict[str, str | None]:
    from seed_runtime.operator_representation import read_operator_representation

    try:
        representation = read_operator_representation(
            ledger, representation_event_identity
        )
    except (TypeError, ValueError) as error:
        raise RepresentationAdmissionError(
            "candidate requires one intact Representation"
        ) from error
    reference = {
        "representation_event_identity": representation[
            "representation_event_identity"
        ],
        "representation_identity": representation["representation_identity"],
        "representation_act_identity": representation[
            "representation_act_identity"
        ],
        "representation_act_occurrence_identity": representation[
            "act_occurrence_identity"
        ],
        "source_occurrence_reference": representation[
            "source_occurrence_reference"
        ],
        "source_locality_identity": representation["locality_identity"],
        "representation_source_standing_boundary_identity": representation[
            "locality_standing_as_of_event_identity"
        ],
    }
    if "representation_rule" in representation:
        reference["representation_rule"] = representation["representation_rule"]
    return reference


def _require_representation_standing(
    ledger: EventLedger,
    *,
    representation_reference: dict[str, str | None],
    locality_standing: dict[str, Any],
) -> str:
    if type(locality_standing) is not dict:
        raise RepresentationAdmissionError(
            "candidate requires exact Locality Standing"
        )
    locality_identity = representation_reference["source_locality_identity"]
    boundary_identity = locality_standing.get("as_of_event_identity")
    representations = locality_standing.get("representations")
    if (
        locality_standing.get("locality_identity") != locality_identity
        or type(representations) is not dict
        or type(boundary_identity) is not str
        or not boundary_identity
    ):
        raise RepresentationAdmissionError(
            "candidate requires its exact Representation Standing"
        )
    carried = representations.get(
        representation_reference["representation_identity"]
    )
    if (
        type(carried) is not dict
        or carried.get("representation_event_identity")
        != representation_reference["representation_event_identity"]
    ):
        raise RepresentationAdmissionError(
            "candidate requires its exact carried Representation"
        )
    identities = (
        (boundary_identity,)
        if boundary_identity
        == representation_reference["representation_event_identity"]
        else (
            representation_reference["representation_event_identity"],
            boundary_identity,
        )
    )
    try:
        boundary = ledger.occurrences_in_append_order(
            identities, locality_identity=locality_identity
        )[-1]
    except (TypeError, ValueError) as error:
        raise RepresentationAdmissionError(
            "candidate Representation is outside its Standing boundary"
        ) from error
    if ledger.integrity_of(boundary.identity) == CORRUPTED:
        raise RepresentationAdmissionError(
            "candidate Standing boundary is corrupted"
        )
    return boundary_identity


def _scope(
    *,
    scope_identity: str,
    source_locality_identity: str,
    representation_source_standing_boundary_identity: str | None,
    assignment_standing_boundary_identity: str,
    destination_operator_boundary_identity: str,
    destination_operator_boundary_rule: str,
    destination_operator_locality_identity: str,
    emission_act_identity: str,
    emission_act_occurrence_identity: str,
    emission_result_boundary_identity: str,
) -> dict[str, str | None]:
    return {
        "scope_identity": scope_identity,
        "source_locality_identity": source_locality_identity,
        "representation_source_standing_boundary_identity": (
            representation_source_standing_boundary_identity
        ),
        "assignment_standing_boundary_identity": (
            assignment_standing_boundary_identity
        ),
        "destination_operator_boundary_identity": (
            destination_operator_boundary_identity
        ),
        "destination_operator_boundary_rule": destination_operator_boundary_rule,
        "destination_operator_locality_identity": (
            destination_operator_locality_identity
        ),
        "emission_act_identity": emission_act_identity,
        "emission_act_occurrence_identity": emission_act_occurrence_identity,
        "emission_result_boundary_identity": emission_result_boundary_identity,
    }


def _assignment_reference(event: Event) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "assignment_identity": event.material["assignment_identity"],
        "assignment_subject_identity": event.material[
            "assignment_subject_identity"
        ],
        "book_clause_identity": event.material["book_clause_identity"],
        "scope_identity": event.material["scope"]["scope_identity"],
        "result_boundary_identity": event.material["result_boundary_identity"],
    }


def _candidate_assignment_material(
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    candidate_act_identity: str,
    candidate_act_occurrence_identity: str,
    candidate_result_boundary_identity: str,
    scope_identity: str,
    representation_reference: dict[str, str | None],
    assignment_standing_boundary_identity: str,
    destination_operator_boundary_identity: str,
    destination_operator_boundary_rule: str,
    destination_operator_locality_identity: str,
    emission_act_identity: str,
    emission_act_occurrence_identity: str,
    emission_result_boundary_identity: str,
) -> dict[str, Any]:
    scope = _scope(
        scope_identity=scope_identity,
        source_locality_identity=representation_reference[
            "source_locality_identity"
        ],
        representation_source_standing_boundary_identity=(
            representation_reference[
                "representation_source_standing_boundary_identity"
            ]
        ),
        assignment_standing_boundary_identity=assignment_standing_boundary_identity,
        destination_operator_boundary_identity=(
            destination_operator_boundary_identity
        ),
        destination_operator_boundary_rule=destination_operator_boundary_rule,
        destination_operator_locality_identity=(
            destination_operator_locality_identity
        ),
        emission_act_identity=emission_act_identity,
        emission_act_occurrence_identity=emission_act_occurrence_identity,
        emission_result_boundary_identity=emission_result_boundary_identity,
    )
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": REPRESENTATION_CANDIDATE_BOOK_CLAUSE,
        "responsible_boundary": "this Seed",
        "responsibility": REPRESENTATION_CANDIDATE_RESPONSIBILITY,
        "candidate_act_identity": candidate_act_identity,
        "act_occurrence_identity": candidate_act_occurrence_identity,
        "result_boundary_identity": candidate_result_boundary_identity,
        "representation_reference": deepcopy(representation_reference),
        "representation_source_standing_boundary_identity": (
            representation_reference[
                "representation_source_standing_boundary_identity"
            ]
        ),
        "assignment_standing_boundary_identity": assignment_standing_boundary_identity,
        "destination_operator_boundary_identity": (
            destination_operator_boundary_identity
        ),
        "destination_operator_boundary_rule": destination_operator_boundary_rule,
        "destination_operator_locality_identity": (
            destination_operator_locality_identity
        ),
        "emission_act_identity": emission_act_identity,
        "emission_act_occurrence_identity": emission_act_occurrence_identity,
        "emission_result_boundary_identity": emission_result_boundary_identity,
        "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
        "scope": scope,
        "evidence_occurrence_reference": representation_reference[
            "representation_event_identity"
        ],
        "authority": _authority(
            REPRESENTATION_CANDIDATE_BOOK_CLAUSE,
            "preservation bounded to this candidate and emission Act",
        ),
        "standing": "assigned",
        "limits": [
            "candidate identity establishes no Admission",
            "candidate identity establishes no Participation or emission",
        ],
        "unknown": [],
    }


def record_representation_candidate_responsibility_assignment(
    ledger: EventLedger,
    *,
    representation_event_identity: str,
    locality_standing: dict[str, Any],
    destination_operator_boundary,
) -> Event:
    """Assign one bounded Candidate occurrence for one emission Act."""

    if not isinstance(ledger, EventLedger):
        raise TypeError("candidate requires one EventLedger")
    (
        _output_stream,
        destination_operator_boundary_identity,
        destination_operator_locality_identity,
        destination_operator_boundary_rule,
    ) = read_operator_emission_boundary(destination_operator_boundary)
    representation_reference = _representation_reference(
        ledger, representation_event_identity=representation_event_identity
    )
    assignment_standing_boundary_identity = _require_representation_standing(
        ledger,
        representation_reference=representation_reference,
        locality_standing=locality_standing,
    )
    identities = {
        "assignment_identity": new_identity("representation_candidate_assignment"),
        "assignment_subject_identity": new_identity(
            "representation_candidate_assignment_subject"
        ),
        "candidate_act_identity": new_identity("representation_candidate_act"),
        "candidate_act_occurrence_identity": new_identity(
            "representation_candidate_act_occurrence"
        ),
        "candidate_result_boundary_identity": new_identity(
            "representation_candidate_result"
        ),
        "scope_identity": new_identity("representation_candidate_scope"),
        "emission_act_identity": new_identity(
            "operator_representation_emission_act"
        ),
        "emission_act_occurrence_identity": new_identity(
            "operator_representation_emission_occurrence"
        ),
        "emission_result_boundary_identity": new_identity(
            "operator_representation_emission_result"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise RepresentationAdmissionError("candidate identities are compressed")
    return ledger.append(
        REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _candidate_assignment_material(
            **identities,
            representation_reference=representation_reference,
            assignment_standing_boundary_identity=(
                assignment_standing_boundary_identity
            ),
            destination_operator_boundary_identity=(
                destination_operator_boundary_identity
            ),
            destination_operator_boundary_rule=destination_operator_boundary_rule,
            destination_operator_locality_identity=(
                destination_operator_locality_identity
            ),
        ),
        locality_identity=representation_reference["source_locality_identity"],
    )


def get_representation_candidate_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    event_identity = _require_identity(
        event_identity, "candidate requires one assignment occurrence"
    )
    event = ledger.get(event_identity)
    if (
        event is None
        or event.kind
        != REPRESENTATION_CANDIDATE_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or type(event.locality_identity) is not str
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationAdmissionError("candidate assignment is absent or corrupted")
    material = event.material
    representation_reference = material.get("representation_reference")
    scope = material.get("scope")
    if type(representation_reference) is not dict or type(scope) is not dict:
        raise RepresentationAdmissionError("candidate assignment coordinates are not exact")
    exact_reference = _representation_reference(
        ledger,
        representation_event_identity=representation_reference.get(
            "representation_event_identity"
        ),
    )
    identities = (
        material.get("assignment_identity"),
        material.get("assignment_subject_identity"),
        material.get("candidate_act_identity"),
        material.get("act_occurrence_identity"),
        material.get("result_boundary_identity"),
        scope.get("scope_identity"),
        material.get("emission_act_identity"),
        material.get("emission_act_occurrence_identity"),
        material.get("emission_result_boundary_identity"),
    )
    if (
        any(type(identity) is not str or not identity for identity in identities)
        or len(set(identities)) != len(identities)
        or representation_reference != exact_reference
        or event.locality_identity != exact_reference["source_locality_identity"]
    ):
        raise RepresentationAdmissionError("candidate assignment identities are not exact")
    expected = _candidate_assignment_material(
        assignment_identity=identities[0],
        assignment_subject_identity=identities[1],
        candidate_act_identity=identities[2],
        candidate_act_occurrence_identity=identities[3],
        candidate_result_boundary_identity=identities[4],
        scope_identity=identities[5],
        representation_reference=exact_reference,
        assignment_standing_boundary_identity=material.get(
            "assignment_standing_boundary_identity"
        ),
        destination_operator_boundary_identity=material.get(
            "destination_operator_boundary_identity"
        ),
        destination_operator_boundary_rule=material.get(
            "destination_operator_boundary_rule"
        ),
        destination_operator_locality_identity=material.get(
            "destination_operator_locality_identity"
        ),
        emission_act_identity=identities[6],
        emission_act_occurrence_identity=identities[7],
        emission_result_boundary_identity=identities[8],
    )
    if material != expected:
        raise RepresentationAdmissionError("candidate assignment is not exact")
    boundary = ledger.get(material["assignment_standing_boundary_identity"])
    if (
        boundary is None
        or boundary.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
    ):
        raise RepresentationAdmissionError("candidate Standing boundary is not exact")
    source_identities = (
        (boundary.identity, event.identity)
        if representation_reference["representation_event_identity"]
        == boundary.identity
        else (
            representation_reference["representation_event_identity"],
            boundary.identity,
            event.identity,
        )
    )
    try:
        ledger.occurrences_in_append_order(
            source_identities,
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RepresentationAdmissionError(
            "candidate assignment does not follow its source Standing"
        ) from error
    return event


def _candidate_act_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "candidate_act_identity": material["candidate_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": REPRESENTATION_CANDIDATE_ACT,
        "responsibility": REPRESENTATION_CANDIDATE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "representation_reference": deepcopy(material["representation_reference"]),
        "representation_source_standing_boundary_identity": material[
            "representation_source_standing_boundary_identity"
        ],
        "assignment_standing_boundary_identity": material[
            "assignment_standing_boundary_identity"
        ],
        "destination_operator_boundary_identity": material[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": material[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": material[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": material["emission_act_identity"],
        "emission_act_occurrence_identity": material[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": material[
            "emission_result_boundary_identity"
        ],
        "input_role": material["input_role"],
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "evidence_scope": "Evidence bounded to this exact Candidate occurrence",
    }


def record_representation_candidate_act_evidence(
    ledger: EventLedger,
    *,
    assignment_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    assignment = get_representation_candidate_responsibility_assignment(
        ledger, assignment_event_identity
    )
    carried = (
        locality_standing.get("responsibility_assignment_occurrences")
        if type(locality_standing) is dict
        else None
    )
    if (
        type(carried) is not dict
        or carried.get(assignment.identity, object()) is not None
        or locality_standing.get("locality_identity")
        != assignment.locality_identity
    ):
        raise RepresentationAdmissionError(
            "Candidate Act requires its exact carried assignment"
        )
    return ledger.append(
        REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND,
        _candidate_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def get_representation_candidate_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _require_identity(event_identity, "candidate requires one Act Evidence occurrence")
    )
    if (
        event is None
        or event.kind != REPRESENTATION_CANDIDATE_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationAdmissionError("Candidate Act Evidence is absent or corrupted")
    reference = event.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise RepresentationAdmissionError("Candidate Act carries no assignment")
    assignment = get_representation_candidate_responsibility_assignment(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        event.locality_identity != assignment.locality_identity
        or reference != _assignment_reference(assignment)
        or event.material != _candidate_act_material(assignment)
    ):
        raise RepresentationAdmissionError("Candidate Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RepresentationAdmissionError(
            "Candidate Act does not follow its assignment"
        ) from error
    return event


def _candidate_result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["responsibility_assignment_reference"][
            "result_boundary_identity"
        ],
        "candidate_act_identity": material["candidate_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": REPRESENTATION_CANDIDATE_ACT,
        "responsibility": REPRESENTATION_CANDIDATE_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "representation_reference": deepcopy(material["representation_reference"]),
        "representation_source_standing_boundary_identity": material[
            "representation_source_standing_boundary_identity"
        ],
        "assignment_standing_boundary_identity": material[
            "assignment_standing_boundary_identity"
        ],
        "destination_operator_boundary_identity": material[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": material[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": material[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": material["emission_act_identity"],
        "emission_act_occurrence_identity": material[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": material[
            "emission_result_boundary_identity"
        ],
        "input_role": material["input_role"],
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "standing": "candidate",
        "limits": [
            "Candidate is not Admission",
            "Candidate is not Participation or emission",
        ],
        "unknown": [],
    }


def _recorded_candidate_result_material(
    result: dict[str, Any],
    *,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "candidate_act_identity": result["candidate_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            result["responsibility_assignment_reference"]
        ),
        "representation_reference": deepcopy(result["representation_reference"]),
        "representation_source_standing_boundary_identity": result[
            "representation_source_standing_boundary_identity"
        ],
        "assignment_standing_boundary_identity": result[
            "assignment_standing_boundary_identity"
        ],
        "destination_operator_boundary_identity": result[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": result[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": result[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": result["emission_act_identity"],
        "emission_act_occurrence_identity": result[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": result[
            "emission_result_boundary_identity"
        ],
        "input_role": result["input_role"],
        "scope": deepcopy(result["scope"]),
        "authority": deepcopy(result["authority"]),
        "standing": result["standing"],
        "limits": list(result["limits"]),
        "unknown": list(result["unknown"]),
        "responsible_act_evidence_identity": responsible_act_evidence_identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
    }


def _refuse_second_yield(ledger: EventLedger, act: Event) -> None:
    for evidence in ledger.iter_locality_kind(
        act.locality_identity, RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
    ):
        if (
            evidence.material.get("responsible_act_evidence_identity")
            == act.identity
            or evidence.material.get("dimensions", {}).get(
                "act_occurrence_identity"
            )
            == act.material["act_occurrence_identity"]
        ):
            raise RepresentationAdmissionError("Act already carries a Yield")


def record_representation_candidate_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act = get_representation_candidate_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    _refuse_second_yield(ledger, act)
    result = _candidate_result_material(act)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=REPRESENTATION_CANDIDATE_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=REPRESENTATION_CANDIDATE_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=REPRESENTATION_CANDIDATE_RESPONSIBILITY,
        live_boundary="representation_candidate",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        REPRESENTATION_CANDIDATE_RECORDED_KIND,
        _recorded_candidate_result_material(
            result,
            responsible_act_evidence_identity=act.identity,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_representation_candidate(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = ledger.get(
        _require_identity(event_identity, "candidate requires one result occurrence")
    )
    if (
        event is None
        or event.kind != REPRESENTATION_CANDIDATE_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationAdmissionError("Candidate result is absent or corrupted")
    act = get_representation_candidate_act_evidence(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    result = _candidate_result_material(act)
    expected = _recorded_candidate_result_material(
        result,
        responsible_act_evidence_identity=act.identity,
        evidence_of_yield_relation_identity=event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise RepresentationAdmissionError("Candidate result is not exact")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material[
            "evidence_of_yield_relation_identity"
        ],
        responsible_act_evidence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise RepresentationAdmissionError("Candidate carries no exact Yield")
    return deepcopy(event.material)


def _candidate_reference(event: Event, material: dict[str, Any]) -> dict[str, str]:
    return {
        "recorded_occurrence_identity": event.identity,
        "result_identity": material["result_identity"],
        "representation_event_identity": material["representation_reference"][
            "representation_event_identity"
        ],
        "destination_operator_boundary_identity": material[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": material[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": material[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": material["emission_act_identity"],
        "emission_act_occurrence_identity": material[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": material[
            "emission_result_boundary_identity"
        ],
    }


def _admission_assignment_material(
    *,
    assignment_identity: str,
    assignment_subject_identity: str,
    admission_act_identity: str,
    admission_act_occurrence_identity: str,
    admission_result_boundary_identity: str,
    scope_identity: str,
    candidate_event: Event,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    return {
        "assignment_identity": assignment_identity,
        "assignment_subject_identity": assignment_subject_identity,
        "book_clause_identity": REPRESENTATION_ADMISSION_BOOK_CLAUSE,
        "responsible_boundary": "this Seed",
        "responsibility": REPRESENTATION_ADMISSION_RESPONSIBILITY,
        "admission_act_identity": admission_act_identity,
        "act_occurrence_identity": admission_act_occurrence_identity,
        "result_boundary_identity": admission_result_boundary_identity,
        "candidate_reference": _candidate_reference(candidate_event, candidate),
        "representation_reference": deepcopy(candidate["representation_reference"]),
        "destination_operator_boundary_identity": candidate[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": candidate[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": candidate[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": candidate["emission_act_identity"],
        "emission_act_occurrence_identity": candidate[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": candidate[
            "emission_result_boundary_identity"
        ],
        "input_role": candidate["input_role"],
        "scope": {
            **deepcopy(candidate["scope"]),
            "scope_identity": scope_identity,
            "candidate_result_identity": candidate["result_identity"],
            "admission_result_boundary_identity": admission_result_boundary_identity,
        },
        "evidence_occurrence_reference": candidate_event.identity,
        "authority": _authority(
            REPRESENTATION_ADMISSION_BOOK_CLAUSE,
            "Admission bounded to this candidate and destination operator Locality",
        ),
        "standing": "assigned",
        "limits": [
            "Admission establishes no Participation by identity",
            "Admission to one operator Locality is not Admission to another",
        ],
        "unknown": [],
    }


def record_exact_material_representation_admission_responsibility_assignment(
    ledger: EventLedger,
    *,
    candidate_result_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    candidate_event = ledger.get(candidate_result_event_identity)
    if candidate_event is None:
        raise RepresentationAdmissionError("Admission requires one Candidate result")
    candidate = get_recorded_representation_candidate(
        ledger, candidate_result_event_identity
    )
    carried = (
        locality_standing.get("candidate_result_occurrences")
        if type(locality_standing) is dict
        else None
    )
    if (
        locality_standing.get("locality_identity")
        != candidate_event.locality_identity
        or type(carried) is not dict
        or carried.get(candidate_event.identity, object()) is not None
    ):
        raise RepresentationAdmissionError(
            "Admission requires exact Candidate Standing"
        )
    identities = {
        "assignment_identity": new_identity(
            "exact_material_representation_admission_assignment"
        ),
        "assignment_subject_identity": new_identity(
            "exact_material_representation_admission_assignment_subject"
        ),
        "admission_act_identity": new_identity(
            "exact_material_representation_admission_act"
        ),
        "admission_act_occurrence_identity": new_identity(
            "exact_material_representation_admission_act_occurrence"
        ),
        "admission_result_boundary_identity": new_identity(
            "exact_material_representation_admission_result"
        ),
        "scope_identity": new_identity(
            "exact_material_representation_admission_scope"
        ),
    }
    if len(set(identities.values())) != len(identities):
        raise RepresentationAdmissionError("Admission identities are compressed")
    return ledger.append(
        EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
        _admission_assignment_material(
            **identities,
            candidate_event=candidate_event,
            candidate=candidate,
        ),
        locality_identity=candidate_event.locality_identity,
    )


def get_exact_material_representation_admission_responsibility_assignment(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _require_identity(event_identity, "Admission requires one assignment occurrence")
    )
    if (
        event is None
        or event.kind
        != EXACT_MATERIAL_REPRESENTATION_ADMISSION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationAdmissionError("Admission assignment is absent or corrupted")
    material = event.material
    candidate_reference = material.get("candidate_reference")
    if type(candidate_reference) is not dict:
        raise RepresentationAdmissionError("Admission assignment carries no Candidate")
    candidate_event = ledger.get(candidate_reference.get("recorded_occurrence_identity"))
    if candidate_event is None:
        raise RepresentationAdmissionError("Admission Candidate is absent")
    candidate = get_recorded_representation_candidate(
        ledger, candidate_event.identity
    )
    scope = material.get("scope")
    identities = (
        material.get("assignment_identity"),
        material.get("assignment_subject_identity"),
        material.get("admission_act_identity"),
        material.get("act_occurrence_identity"),
        material.get("result_boundary_identity"),
        scope.get("scope_identity") if type(scope) is dict else None,
    )
    if any(type(identity) is not str or not identity for identity in identities):
        raise RepresentationAdmissionError("Admission assignment identities are not exact")
    expected = _admission_assignment_material(
        assignment_identity=identities[0],
        assignment_subject_identity=identities[1],
        admission_act_identity=identities[2],
        admission_act_occurrence_identity=identities[3],
        admission_result_boundary_identity=identities[4],
        scope_identity=identities[5],
        candidate_event=candidate_event,
        candidate=candidate,
    )
    if (
        len(set(identities)) != len(identities)
        or event.locality_identity != candidate_event.locality_identity
        or material != expected
    ):
        raise RepresentationAdmissionError("Admission assignment is not exact")
    try:
        ledger.occurrences_in_append_order(
            (candidate_event.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RepresentationAdmissionError(
            "Admission assignment does not follow its Candidate"
        ) from error
    return event


def _admission_act_material(assignment: Event) -> dict[str, Any]:
    material = assignment.material
    return {
        "admission_act_identity": material["admission_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "act": REPRESENTATION_ADMISSION_ACT,
        "responsibility": REPRESENTATION_ADMISSION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": _assignment_reference(assignment),
        "candidate_reference": deepcopy(material["candidate_reference"]),
        "representation_reference": deepcopy(material["representation_reference"]),
        "destination_operator_boundary_identity": material[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": material[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": material[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": material["emission_act_identity"],
        "emission_act_occurrence_identity": material[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": material[
            "emission_result_boundary_identity"
        ],
        "input_role": material["input_role"],
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "evidence_scope": "Evidence bounded to this exact Admission occurrence",
    }


def record_exact_material_representation_admission_act_evidence(
    ledger: EventLedger,
    *,
    assignment_event_identity: str,
    locality_standing: dict[str, Any],
) -> Event:
    assignment = get_exact_material_representation_admission_responsibility_assignment(
        ledger, assignment_event_identity
    )
    carried = (
        locality_standing.get("responsibility_assignment_occurrences")
        if type(locality_standing) is dict
        else None
    )
    if (
        type(carried) is not dict
        or carried.get(assignment.identity, object()) is not None
        or locality_standing.get("locality_identity")
        != assignment.locality_identity
    ):
        raise RepresentationAdmissionError(
            "Admission Act requires its exact carried assignment"
        )
    return ledger.append(
        EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND,
        _admission_act_material(assignment),
        locality_identity=assignment.locality_identity,
    )


def get_exact_material_representation_admission_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _require_identity(event_identity, "Admission requires one Act Evidence occurrence")
    )
    if (
        event is None
        or event.kind != EXACT_MATERIAL_REPRESENTATION_ADMISSION_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationAdmissionError("Admission Act Evidence is absent or corrupted")
    reference = event.material.get("responsibility_assignment_reference")
    if type(reference) is not dict:
        raise RepresentationAdmissionError("Admission Act carries no assignment")
    assignment = get_exact_material_representation_admission_responsibility_assignment(
        ledger, reference.get("recorded_occurrence_identity")
    )
    if (
        event.locality_identity != assignment.locality_identity
        or reference != _assignment_reference(assignment)
        or event.material != _admission_act_material(assignment)
    ):
        raise RepresentationAdmissionError("Admission Act Evidence is not exact")
    try:
        ledger.occurrences_in_append_order(
            (assignment.identity, event.identity),
            locality_identity=event.locality_identity,
        )
    except ValueError as error:
        raise RepresentationAdmissionError(
            "Admission Act does not follow its assignment"
        ) from error
    return event


def _admission_result_material(act: Event) -> dict[str, Any]:
    material = act.material
    representation_rule = material["representation_reference"].get(
        "representation_rule"
    )
    boundary_rule = material["destination_operator_boundary_rule"]
    return {
        "result_identity": material["responsibility_assignment_reference"][
            "result_boundary_identity"
        ],
        "admission_act_identity": material["admission_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "exact_act": REPRESENTATION_ADMISSION_ACT,
        "responsibility": REPRESENTATION_ADMISSION_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "responsibility_assignment_reference": deepcopy(
            material["responsibility_assignment_reference"]
        ),
        "candidate_reference": deepcopy(material["candidate_reference"]),
        "representation_reference": deepcopy(material["representation_reference"]),
        "destination_operator_boundary_identity": material[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": material[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": material[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": material["emission_act_identity"],
        "emission_act_occurrence_identity": material[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": material[
            "emission_result_boundary_identity"
        ],
        "input_role": material["input_role"],
        "admission_relation": {
            "first_subject": material["candidate_reference"]["result_identity"],
            "relation": "admitted_to",
            "second_subject": material[
                "destination_operator_locality_identity"
            ],
        },
        "representation_rule_to_boundary_rule_relation": {
            "first_subject": representation_rule,
            "relation": "applicable_to",
            "second_subject": boundary_rule,
        },
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "standing": "admitted",
        "limits": [
            "Admission establishes no Participation by identity",
            "Admission establishes no emission boundary result",
        ],
        "unknown": [],
    }


def _recorded_admission_result_material(
    result: dict[str, Any],
    *,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "admission_act_identity": result["admission_act_identity"],
        "act_occurrence_identity": result["act_occurrence_identity"],
        "exact_act": result["exact_act"],
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
        "responsibility_assignment_reference": deepcopy(
            result["responsibility_assignment_reference"]
        ),
        "candidate_reference": deepcopy(result["candidate_reference"]),
        "representation_reference": deepcopy(result["representation_reference"]),
        "destination_operator_boundary_identity": result[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": result[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": result[
            "destination_operator_locality_identity"
        ],
        "emission_act_identity": result["emission_act_identity"],
        "emission_act_occurrence_identity": result[
            "emission_act_occurrence_identity"
        ],
        "emission_result_boundary_identity": result[
            "emission_result_boundary_identity"
        ],
        "input_role": result["input_role"],
        "admission_relation": deepcopy(result["admission_relation"]),
        "representation_rule_to_boundary_rule_relation": deepcopy(
            result["representation_rule_to_boundary_rule_relation"]
        ),
        "scope": deepcopy(result["scope"]),
        "authority": deepcopy(result["authority"]),
        "standing": result["standing"],
        "limits": list(result["limits"]),
        "unknown": list(result["unknown"]),
        "responsible_act_evidence_identity": responsible_act_evidence_identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
    }


def record_exact_material_representation_admission_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act = get_exact_material_representation_admission_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    _refuse_second_yield(ledger, act)
    from seed_runtime.operator_representation import read_operator_representation

    representation = read_operator_representation(
        ledger, act.material["representation_reference"]["representation_event_identity"]
    )
    if (
        type(representation["exact_material"]) is not bytes
        or not exact_material_representation_rule_is_applicable_to_boundary_rule(
            representation.get("representation_rule"),
            act.material.get("destination_operator_boundary_rule"),
        )
    ):
        raise RepresentationAdmissionError(
            "operator Locality cannot admit a Representation without exact material under an applicable Representation and destination boundary rule pair"
        )
    result = _admission_result_material(act)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=REPRESENTATION_ADMISSION_ACT,
        act_occurrence_identity=act.material["act_occurrence_identity"],
        responsible_act_evidence_identity=act.identity,
        result_kind=REPRESENTATION_ADMISSION_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=REPRESENTATION_ADMISSION_RESPONSIBILITY,
        live_boundary="representation_admission",
        responsible_boundary="this Seed",
    )
    return ledger.append(
        EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND,
        _recorded_admission_result_material(
            result,
            responsible_act_evidence_identity=act.identity,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_exact_material_representation_admission(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = ledger.get(
        _require_identity(event_identity, "Admission requires one result occurrence")
    )
    if (
        event is None
        or event.kind != EXACT_MATERIAL_REPRESENTATION_ADMISSION_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationAdmissionError("Admission result is absent or corrupted")
    act = get_exact_material_representation_admission_act_evidence(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    result = _admission_result_material(act)
    expected = _recorded_admission_result_material(
        result,
        responsible_act_evidence_identity=act.identity,
        evidence_of_yield_relation_identity=event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise RepresentationAdmissionError("Admission result is not exact")
    candidate = get_recorded_representation_candidate(
        ledger, result["candidate_reference"]["recorded_occurrence_identity"]
    )
    if candidate["result_identity"] != result["candidate_reference"]["result_identity"]:
        raise RepresentationAdmissionError("Admission carries another Candidate")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material[
            "evidence_of_yield_relation_identity"
        ],
        responsible_act_evidence_event_identity=act.identity,
    )
    if not all(requirements.values()):
        raise RepresentationAdmissionError("Admission carries no exact Yield")
    return deepcopy(event.material)


def exact_material_representation_admission_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, ...]:
    """Resolve the exact Candidate and Admission lifecycle in append order."""

    admission_event = ledger.get(event_identity)
    admission = get_recorded_exact_material_representation_admission(
        ledger, event_identity
    )
    candidate_event = ledger.get(
        admission["candidate_reference"]["recorded_occurrence_identity"]
    )
    candidate = get_recorded_representation_candidate(
        ledger, candidate_event.identity
    )
    candidate_act = ledger.get(candidate["responsible_act_evidence_identity"])
    admission_act = ledger.get(admission["responsible_act_evidence_identity"])
    candidate_assignment_identity = candidate_act.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    admission_assignment_identity = admission_act.material[
        "responsibility_assignment_reference"
    ]["recorded_occurrence_identity"]
    identities = (
        candidate_assignment_identity,
        candidate_act.identity,
        candidate["evidence_of_yield_relation_identity"],
        candidate_event.identity,
        admission_assignment_identity,
        admission_act.identity,
        admission["evidence_of_yield_relation_identity"],
        admission_event.identity,
    )
    try:
        ledger.occurrences_in_append_order(
            identities, locality_identity=admission_event.locality_identity
        )
    except (TypeError, ValueError) as error:
        raise RepresentationAdmissionError(
            "Candidate and Admission occurrences are not in exact order"
        ) from error
    return identities
