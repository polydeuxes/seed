"""Act-local Applicability of one admitted Representation to one emission Act."""

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
from seed_runtime.operator_representation_admission import (
    get_recorded_exact_material_representation_admission,
)
from seed_runtime.operator_egress import read_operator_emission_boundary


REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND = (
    "operator.representation.emission_applicability_act_evidenced"
)
REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND = (
    "operator.representation.emission_applicability_recorded"
)
REPRESENTATION_EMISSION_APPLICABILITY_BOOK_CLAUSE = "01.Standing.E.1"
REPRESENTATION_EMISSION_APPLICABILITY_ACT = (
    "Determine Applicability of one admitted exact Representation to one emission Act"
)
REPRESENTATION_EMISSION_APPLICABILITY_RESPONSIBILITY = (
    "determine exact admitted Representation input Applicability before emission participation"
)
REPRESENTATION_EMISSION_APPLICABILITY_RESULT_KIND = (
    "exact admitted Representation emission Applicability result"
)
REPRESENTATION_EMISSION_INPUT_ROLE = "exact bounded Representation"

EVENT_KIND_RESPONSIBILITIES = {
    REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND: "02.Acts.A",
    REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND: "01.Standing.E.1",
}


class RepresentationApplicabilityError(ValueError):
    """One emission Applicability boundary is absent or incoherent."""


def _identity(value: Any, message: str) -> str:
    if type(value) is not str or not value:
        raise RepresentationApplicabilityError(message)
    return value


def _admission_event_and_material(
    ledger: EventLedger, event_identity: str
) -> tuple[Event, dict[str, Any]]:
    event_identity = _identity(
        event_identity, "Applicability requires one exact Admission result"
    )
    event = ledger.get(event_identity)
    if event is None:
        raise RepresentationApplicabilityError(
            "Applicability requires one exact Admission result"
        )
    try:
        material = get_recorded_exact_material_representation_admission(
            ledger, event_identity
        )
    except (TypeError, ValueError) as error:
        raise RepresentationApplicabilityError(
            "Applicability requires one intact Admission result"
        ) from error
    return event, material


def _require_admission_standing(
    ledger: EventLedger,
    *,
    admission_event: Event,
    locality_standing: dict[str, Any],
) -> str:
    carried = (
        locality_standing.get("admission_result_occurrences")
        if type(locality_standing) is dict
        else None
    )
    boundary_identity = (
        locality_standing.get("as_of_event_identity")
        if type(locality_standing) is dict
        else None
    )
    if (
        type(carried) is not dict
        or carried.get(admission_event.identity, object()) is not None
        or locality_standing.get("locality_identity")
        != admission_event.locality_identity
        or type(boundary_identity) is not str
        or not boundary_identity
    ):
        raise RepresentationApplicabilityError(
            "Applicability requires exact current Admission Standing"
        )
    identities = (
        (admission_event.identity,)
        if admission_event.identity == boundary_identity
        else (admission_event.identity, boundary_identity)
    )
    try:
        boundary = ledger.occurrences_in_append_order(
            identities, locality_identity=admission_event.locality_identity
        )[-1]
    except (TypeError, ValueError) as error:
        raise RepresentationApplicabilityError(
            "Applicability Standing does not carry its Admission"
        ) from error
    if ledger.integrity_of(boundary.identity) == CORRUPTED:
        raise RepresentationApplicabilityError(
            "Applicability Standing boundary is corrupted"
        )
    return boundary_identity


def _act_material(
    *,
    admission_event: Event,
    admission: dict[str, Any],
    standing_boundary_identity: str,
    applicability_act_identity: str,
    applicability_act_occurrence_identity: str,
    applicability_result_identity: str,
) -> dict[str, Any]:
    return {
        "applicability_act_identity": applicability_act_identity,
        "applicability_act_occurrence_identity": (
            applicability_act_occurrence_identity
        ),
        "result_boundary_identity": applicability_result_identity,
        "act": REPRESENTATION_EMISSION_APPLICABILITY_ACT,
        "responsibility": REPRESENTATION_EMISSION_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "assigned_by_responsibility": (
            "exact bounded Representation emission Responsibility"
        ),
        "admission_result_event_identity": admission_event.identity,
        "admission_result_identity": admission["result_identity"],
        "candidate_result_event_identity": admission["candidate_reference"][
            "recorded_occurrence_identity"
        ],
        "representation_reference": deepcopy(admission["representation_reference"]),
        "input_identity": admission["candidate_reference"]["result_identity"],
        "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
        "downstream_act_identity": admission["emission_act_identity"],
        "downstream_act_occurrence_identity": admission[
            "emission_act_occurrence_identity"
        ],
        "downstream_result_boundary_identity": admission[
            "emission_result_boundary_identity"
        ],
        "destination_operator_boundary_identity": admission[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_locality_identity": admission[
            "destination_operator_locality_identity"
        ],
        "standing_boundary_identity": standing_boundary_identity,
        "scope": deepcopy(admission["scope"]),
        "authority": deepcopy(admission["authority"]),
        "evidence_scope": (
            "Evidence bounded to this exact admitted Representation input-to-emission-Act relation"
        ),
    }


def record_representation_emission_applicability_act_evidence(
    ledger: EventLedger,
    *,
    admission_result_event_identity: str,
    locality_standing: dict[str, Any],
    destination_operator_boundary,
) -> Event:
    """Validate no result yet; freeze the exact admitted input relation."""

    admission_event, admission = _admission_event_and_material(
        ledger, admission_result_event_identity
    )
    (
        _output_stream,
        destination_operator_boundary_identity,
        destination_operator_locality_identity,
    ) = read_operator_emission_boundary(destination_operator_boundary)
    if (
        destination_operator_boundary_identity
        != admission["destination_operator_boundary_identity"]
        or destination_operator_locality_identity
        != admission["destination_operator_locality_identity"]
    ):
        raise RepresentationApplicabilityError(
            "Applicability requires its exact admitted destination"
        )
    standing_boundary_identity = _require_admission_standing(
        ledger,
        admission_event=admission_event,
        locality_standing=locality_standing,
    )
    identities = (
        new_identity("representation_emission_applicability_act"),
        new_identity("representation_emission_applicability_act_occurrence"),
        new_identity("representation_emission_applicability_result"),
    )
    if len(set(identities)) != len(identities):
        raise RepresentationApplicabilityError(
            "Applicability identities are compressed"
        )
    return ledger.append(
        REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND,
        _act_material(
            admission_event=admission_event,
            admission=admission,
            standing_boundary_identity=standing_boundary_identity,
            applicability_act_identity=identities[0],
            applicability_act_occurrence_identity=identities[1],
            applicability_result_identity=identities[2],
        ),
        locality_identity=admission_event.locality_identity,
    )


def get_representation_emission_applicability_act_evidence(
    ledger: EventLedger, event_identity: str
) -> Event:
    event = ledger.get(
        _identity(event_identity, "Applicability requires one Act Evidence occurrence")
    )
    if (
        event is None
        or event.kind
        != REPRESENTATION_EMISSION_APPLICABILITY_ACT_EVIDENCE_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationApplicabilityError(
            "Applicability Act Evidence is absent or corrupted"
        )
    material = event.material
    admission_event, admission = _admission_event_and_material(
        ledger, material.get("admission_result_event_identity")
    )
    identities = (
        material.get("applicability_act_identity"),
        material.get("applicability_act_occurrence_identity"),
        material.get("result_boundary_identity"),
    )
    if (
        any(type(identity) is not str or not identity for identity in identities)
        or len(set(identities)) != len(identities)
    ):
        raise RepresentationApplicabilityError(
            "Applicability Act identities are not exact"
        )
    expected = _act_material(
        admission_event=admission_event,
        admission=admission,
        standing_boundary_identity=material.get("standing_boundary_identity"),
        applicability_act_identity=identities[0],
        applicability_act_occurrence_identity=identities[1],
        applicability_result_identity=identities[2],
    )
    boundary = ledger.get(material.get("standing_boundary_identity"))
    if (
        event.locality_identity != admission_event.locality_identity
        or material != expected
        or boundary is None
        or boundary.locality_identity != event.locality_identity
        or ledger.integrity_of(boundary.identity) == CORRUPTED
    ):
        raise RepresentationApplicabilityError(
            "Applicability Act Evidence is not exact"
        )
    ordered = (
        (admission_event.identity, event.identity)
        if admission_event.identity == boundary.identity
        else (admission_event.identity, boundary.identity, event.identity)
    )
    try:
        ledger.occurrences_in_append_order(
            ordered, locality_identity=event.locality_identity
        )
    except ValueError as error:
        raise RepresentationApplicabilityError(
            "Applicability Act does not follow its Admission Standing"
        ) from error
    return event


def _result_material(act: Event) -> dict[str, Any]:
    material = act.material
    return {
        "result_identity": material["result_boundary_identity"],
        "applicability_act_identity": material["applicability_act_identity"],
        "applicability_act_occurrence_identity": material[
            "applicability_act_occurrence_identity"
        ],
        "exact_act": REPRESENTATION_EMISSION_APPLICABILITY_ACT,
        "responsibility": REPRESENTATION_EMISSION_APPLICABILITY_RESPONSIBILITY,
        "responsible_boundary": "this Seed",
        "assigned_by_responsibility": material["assigned_by_responsibility"],
        "admission_result_event_identity": material[
            "admission_result_event_identity"
        ],
        "admission_result_identity": material["admission_result_identity"],
        "candidate_result_event_identity": material[
            "candidate_result_event_identity"
        ],
        "representation_reference": deepcopy(material["representation_reference"]),
        "input_identity": material["input_identity"],
        "input_role": material["input_role"],
        "downstream_act_identity": material["downstream_act_identity"],
        "downstream_act_occurrence_identity": material[
            "downstream_act_occurrence_identity"
        ],
        "downstream_result_boundary_identity": material[
            "downstream_result_boundary_identity"
        ],
        "destination_operator_boundary_identity": material[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_locality_identity": material[
            "destination_operator_locality_identity"
        ],
        "standing_boundary_identity": material["standing_boundary_identity"],
        "scope": deepcopy(material["scope"]),
        "authority": deepcopy(material["authority"]),
        "participants_and_roles": [
            {
                "subject": material["representation_reference"][
                    "representation_identity"
                ],
                "role": material["input_role"],
            }
        ],
        "provenance_occurrence_references": [
            material["representation_reference"]["representation_event_identity"],
            material["candidate_result_event_identity"],
            material["admission_result_event_identity"],
        ],
        "standing": "applicable",
        "support_relation_standing": "admitted",
        "validation": {
            "exact_material_Admission": True,
            "current_Admission_Standing": True,
            "same_Representation": True,
            "same_destination_operator_boundary": True,
            "same_destination_operator_Locality": True,
            "same_emission_Act_occurrence": True,
            "same_emission_result_boundary": True,
        },
        "currentness": "current through exact Admission Standing boundary",
        "known_loss": [],
        "conflicts": [],
        "unknown": [],
        "negative_authority": [
            "Applicability establishes no Participation",
            "Applicability establishes no emission result or input support",
        ],
    }


def _recorded_result_material(
    result: dict[str, Any],
    *,
    responsible_act_evidence_identity: str,
    evidence_of_yield_relation_identity: str,
) -> dict[str, Any]:
    return {
        "result_identity": result["result_identity"],
        "applicability_act_identity": result["applicability_act_identity"],
        "applicability_act_occurrence_identity": result[
            "applicability_act_occurrence_identity"
        ],
        "exact_act": result["exact_act"],
        "responsibility": result["responsibility"],
        "responsible_boundary": result["responsible_boundary"],
        "assigned_by_responsibility": result["assigned_by_responsibility"],
        "admission_result_event_identity": result[
            "admission_result_event_identity"
        ],
        "admission_result_identity": result["admission_result_identity"],
        "candidate_result_event_identity": result[
            "candidate_result_event_identity"
        ],
        "representation_reference": deepcopy(result["representation_reference"]),
        "input_identity": result["input_identity"],
        "input_role": result["input_role"],
        "downstream_act_identity": result["downstream_act_identity"],
        "downstream_act_occurrence_identity": result[
            "downstream_act_occurrence_identity"
        ],
        "downstream_result_boundary_identity": result[
            "downstream_result_boundary_identity"
        ],
        "destination_operator_boundary_identity": result[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_locality_identity": result[
            "destination_operator_locality_identity"
        ],
        "standing_boundary_identity": result["standing_boundary_identity"],
        "scope": deepcopy(result["scope"]),
        "authority": deepcopy(result["authority"]),
        "participants_and_roles": deepcopy(result["participants_and_roles"]),
        "provenance_occurrence_references": list(
            result["provenance_occurrence_references"]
        ),
        "standing": result["standing"],
        "support_relation_standing": result["support_relation_standing"],
        "validation": deepcopy(result["validation"]),
        "currentness": result["currentness"],
        "known_loss": list(result["known_loss"]),
        "conflicts": list(result["conflicts"]),
        "unknown": list(result["unknown"]),
        "negative_authority": list(result["negative_authority"]),
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
            == act.material["applicability_act_occurrence_identity"]
        ):
            raise RepresentationApplicabilityError(
                "Applicability Act already carries a Yield"
            )


def record_representation_emission_applicability_result(
    ledger: EventLedger, *, responsible_act_evidence_event_identity: str
) -> Event:
    act = get_representation_emission_applicability_act_evidence(
        ledger, responsible_act_evidence_event_identity
    )
    _refuse_second_yield(ledger, act)
    result = _result_material(act)
    evidence = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=act.locality_identity,
        exact_act=REPRESENTATION_EMISSION_APPLICABILITY_ACT,
        act_occurrence_identity=act.material[
            "applicability_act_occurrence_identity"
        ],
        responsible_act_evidence_identity=act.identity,
        result_kind=REPRESENTATION_EMISSION_APPLICABILITY_RESULT_KIND,
        result_identity=result["result_identity"],
        result_content=result,
        responsibility=REPRESENTATION_EMISSION_APPLICABILITY_RESPONSIBILITY,
        live_boundary="representation_emission_applicability",
        responsible_boundary="this Seed",
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )
    return ledger.append(
        REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND,
        _recorded_result_material(
            result,
            responsible_act_evidence_identity=act.identity,
            evidence_of_yield_relation_identity=evidence.identity,
        ),
        locality_identity=act.locality_identity,
    )


def get_recorded_representation_emission_applicability(
    ledger: EventLedger, event_identity: str
) -> dict[str, Any]:
    event = ledger.get(
        _identity(event_identity, "Applicability requires one result occurrence")
    )
    if (
        event is None
        or event.kind != REPRESENTATION_EMISSION_APPLICABILITY_RECORDED_KIND
        or event.exact_material is not None
        or ledger.integrity_of(event.identity) == CORRUPTED
    ):
        raise RepresentationApplicabilityError(
            "Applicability result is absent or corrupted"
        )
    act = get_representation_emission_applicability_act_evidence(
        ledger, event.material.get("responsible_act_evidence_identity")
    )
    result = _result_material(act)
    expected = _recorded_result_material(
        result,
        responsible_act_evidence_identity=act.identity,
        evidence_of_yield_relation_identity=event.material.get(
            "evidence_of_yield_relation_identity"
        ),
    )
    if event.locality_identity != act.locality_identity or event.material != expected:
        raise RepresentationApplicabilityError(
            "Applicability result is not exact"
        )
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=event.material[
            "evidence_of_yield_relation_identity"
        ],
        responsible_act_evidence_event_identity=act.identity,
        recorded_result_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
        responsible_act_occurrence_coordinate=(
            "applicability_act_occurrence_identity"
        ),
    )
    if not all(requirements.values()):
        raise RepresentationApplicabilityError(
            "Applicability carries no exact Yield"
        )
    return deepcopy(event.material)


def representation_emission_applicability_occurrence_references(
    ledger: EventLedger, event_identity: str
) -> tuple[str, str, str]:
    event = ledger.get(event_identity)
    result = get_recorded_representation_emission_applicability(
        ledger, event_identity
    )
    act = ledger.get(result["responsible_act_evidence_identity"])
    identities = (
        act.identity,
        result["evidence_of_yield_relation_identity"],
        event.identity,
    )
    try:
        ledger.occurrences_in_append_order(
            identities, locality_identity=event.locality_identity
        )
    except (TypeError, ValueError) as error:
        raise RepresentationApplicabilityError(
            "Applicability occurrences are not in exact order"
        ) from error
    return identities
