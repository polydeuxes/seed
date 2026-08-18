"""Record and emit bounded Representations."""

from __future__ import annotations

from typing import Any

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RECORDED_KIND,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND,
    _findings_of_recorded_byte_position_pair_measurement,
    assertions_of_recorded_byte_measurement,
)
from seed_runtime.events import CORRUPTED, Event, EventLedger
from seed_runtime.identities import new_identity
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RECORDED_KIND,
    get_recorded_occurrence_position_measurement,
)
from seed_runtime.measurement_of_recurrent_byte_pair_occurrence_position import (
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND,
    get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position,
)
from seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences import (
    SHARED_POSITION_MEASUREMENT_RESULT_KIND,
    get_recorded_shared_position_measurement,
)
from seed_runtime.comparison_of_recorded_byte_pair_measurements import (
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND,
    get_recorded_pair_measurement_comparison,
)
from seed_runtime.comparison_of_ordered_relation_path_with_recorded_pair_findings import (
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND,
    get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings,
)
from seed_runtime.operator_egress import (
    ExactMaterialEgressFailure,
    emit_exact_material,
)
from seed_runtime.evidence_of_yield_relation import (
    _record_evidence_of_yield_relation,
    read_requirements_of_yield_relation,
)

REPRESENTATION_RECORDED_KIND = "operator.representation.recorded"

REPRESENTATION_EMISSION_ATTEMPT_KIND = "operator.representation.emission_attempt_recorded"
REPRESENTATION_EMITTED_KIND = "operator.representation.emitted"
REPRESENTATION_BOUNDARY_FAILURE_KIND = "operator.representation.boundary_failure_recorded"
REPRESENTATION_BOUNDARY_FAILURE_ACT_EVIDENCE_KIND = (
    "operator.representation.boundary_failure_act_evidenced"
)
REPRESENTATION_ACT_EVIDENCE_KIND = "operator.representation.act_evidenced"
REPRESENTATION_LOCALITY_EVIDENCE_KIND = (
    "operator.representation.locality_evidenced"
)
REPRESENTATION_RESPONSIBILITY = (
    "yield one bounded Representation from the exact carried Locality coordinates"
)
EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE = (
    "preserve exact material of source result"
)
REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND = (
    "operator.representation.emission_act_evidenced"
)
REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND = (
    "operator.representation.emission_locality_evidenced"
)
REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND = (
    "operator.representation.emission_attempt_locality_evidenced"
)
REPRESENTATION_EMISSION_INPUT_ROLE = "exact bounded Representation"
REPRESENTATION_EXACT_MATERIAL_EMISSION_RESPONSIBILITY = (
    "emit one exact Representation result"
)
REPRESENTATION_EMISSION_RESULT_KIND = "Representation emission boundary result"
REPRESENTATION_BOUNDARY_FAILURE_RESULT_KIND = "Representation boundary failure result"
REPRESENTATION_BOUNDARY_FAILURE_RESPONSIBILITY = (
    "preserve one exact Representation boundary failure occurrence"
)
EVENT_KIND_RESPONSIBILITIES = {
    REPRESENTATION_RECORDED_KIND: "01.Source.A",
    REPRESENTATION_EMISSION_ATTEMPT_KIND: "02.Acts.A",
    REPRESENTATION_EMITTED_KIND: "02.Acts.A",
    REPRESENTATION_ACT_EVIDENCE_KIND: "02.Acts.A",
    REPRESENTATION_LOCALITY_EVIDENCE_KIND: "06.Locality.A",
    REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND: "02.Acts.A",
    REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND: "06.Locality.A",
    REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND: "06.Locality.A",
    REPRESENTATION_BOUNDARY_FAILURE_KIND: "02.Acts.A",
    REPRESENTATION_BOUNDARY_FAILURE_ACT_EVIDENCE_KIND: "02.Acts.A",
}

_MEASUREMENT_READERS = {
    BYTE_MEASUREMENT_RECORDED_KIND: assertions_of_recorded_byte_measurement,
    BYTE_PAIR_MEASUREMENT_RECORDED_KIND: (
        _findings_of_recorded_byte_position_pair_measurement
    ),
    OCCURRENCE_POSITION_RECORDED_KIND: get_recorded_occurrence_position_measurement,
    RECORDING_OCCURRENCE_OF_RESULT_OF_MEASUREMENT_OF_RECURRENT_BYTE_PAIR_OCCURRENCE_POSITION_KIND: (
        get_recorded_result_of_measurement_of_recurrent_byte_pair_occurrence_position
    ),
    SHARED_POSITION_MEASUREMENT_RESULT_KIND: (
        get_recorded_shared_position_measurement
    ),
}

_STRUCTURED_RESULT_READERS = {
    RECORDED_PAIR_MEASUREMENT_COMPARISON_RESULT_KIND: (
        get_recorded_pair_measurement_comparison
    ),
    COMPARISON_OF_ORDERED_RELATION_PATH_WITH_RECORDED_PAIR_FINDINGS_RESULT_KIND: (
        get_recorded_comparison_of_ordered_relation_path_with_recorded_pair_findings
    ),
}


def _dimensions(
    *, identity, content, source, responsibility, authority, scope, occurrence,
    evidence_scope=None,
):
    dimensions = {
        "identity": identity,
        "content": content,
        "source_provenance": source,
        "responsibility": responsibility,
        "authority": authority,
        "scope_locality": scope,
        "occurrence_preservation": occurrence,
    }
    if evidence_scope is not None:
        dimensions["evidence_scope"] = evidence_scope
    return dimensions


def _validate_standing_boundary(
    ledger: EventLedger,
    *,
    locality_identity: str,
    through_event_occurrence_identity: str | None,
    source_occurrence_reference: str | None,
    representation_event_identity: str | None = None,
    carried_pair_measurement: Event | None = None,
    carried_standing_boundary: Event | None = None,
) -> None:
    """Require the represented source to belong to the exact Standing prefix."""

    if through_event_occurrence_identity is None:
        if source_occurrence_reference is not None:
            raise ValueError(
                "Representation source occurrence is outside its Standing boundary"
            )
        return
    if type(through_event_occurrence_identity) is not str or not through_event_occurrence_identity:
        raise ValueError("Representation requires one exact Standing boundary")
    boundary_event = (
        carried_standing_boundary
        if carried_standing_boundary is not None
        and carried_standing_boundary.identity
        == through_event_occurrence_identity
        else ledger.get(through_event_occurrence_identity)
    )
    if (
        boundary_event is None
        or boundary_event.locality_identity != locality_identity
        or (
            boundary_event is not carried_standing_boundary
            and ledger.integrity_of(through_event_occurrence_identity)
            == CORRUPTED
        )
    ):
        raise ValueError("Representation Standing boundary is not exact")
    if (
        source_occurrence_reference is not None
        and source_occurrence_reference != through_event_occurrence_identity
    ):
        try:
            ledger.occurrences_in_append_order(
                (source_occurrence_reference, through_event_occurrence_identity),
                locality_identity=locality_identity,
            )
        except ValueError as error:
            raise ValueError(
                "Representation source occurrence is outside its Standing boundary"
            ) from error
    if representation_event_identity is not None:
        try:
            ledger.occurrences_in_append_order(
                (through_event_occurrence_identity, representation_event_identity),
                locality_identity=locality_identity,
            )
        except ValueError as error:
            raise ValueError(
                "Representation does not follow its exact Standing boundary"
            ) from error


def _record_operator_representation(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    source_occurrence_reference: str | None = None,
    carried_pair_measurement: Event | None = None,
    carried_standing_boundary: Event | None = None,
) -> dict[str, Any]:
    """Record one exact bounded Representation and its Act occurrence."""
    through_event_occurrence_identity = locality_standing["through_event_occurrence_identity"]
    exact_material = _exact_source_material(
        ledger,
        locality_identity=locality_identity,
        locality_standing=locality_standing,
        source_occurrence_reference=source_occurrence_reference,
        carried_pair_measurement=carried_pair_measurement,
    )
    _validate_standing_boundary(
        ledger,
        locality_identity=locality_identity,
        through_event_occurrence_identity=through_event_occurrence_identity,
        source_occurrence_reference=source_occurrence_reference,
        carried_pair_measurement=carried_pair_measurement,
        carried_standing_boundary=carried_standing_boundary,
    )
    representation_identity = new_identity("operator_representation")
    representation_act_identity = new_identity("operator_representation_act")
    act_occurrence_identity = new_identity("operator_representation_act_occurrence")
    scope = f"locality:{locality_identity}"
    representation_result = (
        "bounded representation of one exact Locality Standing boundary"
    )
    content = "bounded Representation of one exact Locality Standing boundary"
    occurrence = "Representation Act occurrence recorded"
    known_loss: list[str] = []
    result_material = {
        "result_identity": representation_identity,
        "representation_act_identity": representation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "source_occurrence_reference": source_occurrence_reference,
        "representation_result": representation_result,
        "locality_standing_through_event_occurrence_identity": through_event_occurrence_identity,
        "known_loss": known_loss,
        "unknown": [],
        "conflicts": [],
    }
    if exact_material is not None:
        result_material["representation_rule"] = (
            EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
        )
    responsible_act_evidence = ledger.append(
        REPRESENTATION_ACT_EVIDENCE_KIND,
        {
            "representation_act_identity": representation_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "bounded Representation Act",
            "responsibility": REPRESENTATION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence bounded to this exact Representation Act occurrence"
            ),
        },
        locality_identity=locality_identity,
    )
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=locality_identity,
        exact_act="bounded Representation Act",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind="bounded Representation",
        result_identity=representation_identity,
        result_content=result_material,
        responsibility=REPRESENTATION_RESPONSIBILITY,
        live_boundary="representation_result",
        responsible_boundary="this Seed",
        result_exact_material=exact_material,
    )
    locality_evidence = ledger.append(
        REPRESENTATION_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_identity": act_occurrence_identity,
            "content_kind": "bounded Representation",
            "carried_content": result_material,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence bounded to this exact Representation-to-occurrence Locality"
            ),
        },
        exact_material=exact_material,
        locality_identity=locality_identity,
    )
    representation_event = ledger.append(
        REPRESENTATION_RECORDED_KIND,
        {
            **result_material,
            "dimensions": _dimensions(
                identity=act_occurrence_identity,
                content=content,
                source=through_event_occurrence_identity,
                responsibility=REPRESENTATION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "bounded to this Representation Act occurrence; establishes no input "
                    "support or response treatment"
                ),
                scope=scope,
                occurrence=occurrence,
            ),
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "evidence_of_yield_relation_identity": evidence_of_yield_relation.identity,
            "locality_evidence_identity": locality_evidence.identity,
        },
        exact_material=exact_material,
        locality_identity=locality_identity,
    )
    representation = {
        "representation_identity": representation_identity,
        "representation_act_identity": representation_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "locality_identity": locality_identity,
        "representation_result": representation_result,
        "responsible_act_evidence_identity": responsible_act_evidence.identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation.identity,
        "locality_evidence_identity": locality_evidence.identity,
        "representation_event_identity": representation_event.identity,
        "source_occurrence_reference": source_occurrence_reference,
        "recorded_occurrence_references": (
            responsible_act_evidence.identity,
            evidence_of_yield_relation.identity,
            locality_evidence.identity,
            representation_event.identity,
        ),
        "emission_attempt_event_identity": None,
        "emission_attempt_locality_evidence_identity": None,
        "emission_act_evidence_identity": None,
        "emission_locality_evidence_identity": None,
        "emission_evidence_of_yield_relation_identity": None,
        "boundary_failure_act_evidence_identity": None,
        "boundary_failure_evidence_of_yield_relation_identity": None,
        "boundary_failure_event_identity": None,
        "emitted_event_identity": None,
        "locality_standing_through_event_occurrence_identity": through_event_occurrence_identity,
        "exact_material": exact_material,
        "known_loss": known_loss,
        "unknown": [],
        "conflicts": [],
    }
    if exact_material is not None:
        representation["representation_rule"] = (
            EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
        )
    return representation


def record_operator_representation(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    source_occurrence_reference: str | None = None,
) -> dict[str, Any]:
    return _record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=locality_standing,
        source_occurrence_reference=source_occurrence_reference,
    )


def _record_operator_representation_from_recorded_pair_measurement(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    pair_measurement: Event,
    carried_standing_boundary: Event | None = None,
) -> dict[str, Any]:
    """Address the pair result produced and carried by this console call."""

    if (
        type(pair_measurement) is not Event
        or type(locality_standing) is not dict
        or pair_measurement.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
        or pair_measurement.locality_identity != locality_identity
        or pair_measurement.identity
        not in locality_standing.get("measurement_occurrences", {})
    ):
        raise ValueError("Representation requires its just-carried pair Measurement")
    through = locality_standing.get("through_event_occurrence_identity")
    boundary = (
        pair_measurement
        if through == pair_measurement.identity
        else carried_standing_boundary
    )
    if (
        type(boundary) is not Event
        or boundary.identity != through
        or boundary.locality_identity != locality_identity
    ):
        raise ValueError("Representation requires its just-carried Standing boundary")
    return _record_operator_representation(
        ledger,
        locality_identity=locality_identity,
        locality_standing=locality_standing,
        source_occurrence_reference=pair_measurement.identity,
        carried_pair_measurement=pair_measurement,
        carried_standing_boundary=boundary,
    )


def _exact_source_material(
    ledger: EventLedger,
    *,
    locality_identity: str,
    locality_standing: dict[str, Any],
    source_occurrence_reference: str | None,
    carried_pair_measurement: Event | None = None,
) -> bytes | None:
    if source_occurrence_reference is None:
        return None
    if type(source_occurrence_reference) is not str or not source_occurrence_reference:
        raise ValueError("Representation requires one exact source occurrence")
    source = (
        carried_pair_measurement
        if carried_pair_measurement is not None
        else ledger.get(source_occurrence_reference)
    )
    if source is None:
        raise ValueError("Representation source occurrence is missing")
    if source.locality_identity != locality_identity:
        raise ValueError("Representation source occurrence has a distinct Locality")
    exact_result_occurrences = locality_standing.get("exact_result_occurrences", {})
    if type(exact_result_occurrences) is not dict:
        raise ValueError("Representation requires exact carried result occurrences")
    if (
        source is not carried_pair_measurement
        and ledger.integrity_of(source.identity) == CORRUPTED
    ):
        raise ValueError("Representation source occurrence is corrupted")
    measurement_occurrences = locality_standing.get("measurement_occurrences", {})
    if type(measurement_occurrences) is not dict:
        raise ValueError("Representation requires exact carried Measurement results")
    if source.identity in measurement_occurrences:
        measurement_reference = measurement_occurrences[source.identity]
        expected_reference = {
            "recorded_occurrence_identity": source.identity,
            "result_identity": source.material.get("result_identity"),
            "act_occurrence_identity": source.material.get(
                "act_occurrence_identity"
            ),
            "responsible_act_evidence_identity": source.material.get(
                "responsible_act_evidence_identity"
            ),
            "evidence_of_yield_relation_identity": source.material.get(
                "evidence_of_yield_relation_identity"
            ),
        }
        if (
            type(measurement_reference) is not dict
            or measurement_reference != expected_reference
        ):
            raise ValueError("Representation source Measurement is not exact")
        if source is carried_pair_measurement:
            if (
                source.kind != BYTE_PAIR_MEASUREMENT_RECORDED_KIND
                or source.exact_material is not None
            ):
                raise ValueError("Representation source Measurement is not exact")
            return None
        reader = _MEASUREMENT_READERS.get(source.kind)
        if reader is None:
            raise ValueError(
                "Representation source is not a declared Measurement result"
            )
        structured_result = reader(ledger, source.identity)
        if structured_result is None:
            raise ValueError("Representation source Measurement is missing")
        requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=source.identity,
            evidence_of_yield_relation_event_identity=expected_reference[
                "evidence_of_yield_relation_identity"
            ],
            responsible_act_evidence_event_identity=expected_reference[
                "responsible_act_evidence_identity"
            ],
        )
        if not all(requirements.values()) or source.exact_material is not None:
            raise ValueError("Representation source Measurement Yield is not exact")
        return None
    if source.kind in _MEASUREMENT_READERS:
        raise ValueError("Representation source Measurement is not carried by Standing")
    comparison_result_occurrences = locality_standing.get(
        "comparison_result_occurrences", {}
    )
    if type(comparison_result_occurrences) is not dict:
        raise ValueError("Representation requires exact carried Compare results")
    if source.identity in comparison_result_occurrences:
        if comparison_result_occurrences.get(source.identity, object()) is not None:
            raise ValueError("Representation source Compare result is not exact")
        reader = _STRUCTURED_RESULT_READERS.get(source.kind)
        structured_result = (
            reader(ledger, source.identity) if reader is not None else None
        )
        if structured_result is None or source.exact_material is not None:
            raise ValueError("Representation source Compare result is not exact")
        return None
    if source.kind in _STRUCTURED_RESULT_READERS:
        raise ValueError("Representation source Compare result is not carried by Standing")
    if source.identity not in exact_result_occurrences:
        raise ValueError("Representation source occurrence is not carried by Standing")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=source.identity,
        evidence_of_yield_relation_event_identity=source.material.get("evidence_of_yield_relation_identity"),
        responsible_act_evidence_event_identity=source.material.get(
            "responsible_act_evidence_identity"
        ),
    )
    if not all(requirements.values()) or type(source.exact_material) is not bytes:
        raise ValueError("Representation source Yield is not exact")
    return source.exact_material


def read_operator_representation(
    ledger: EventLedger, representation_event_identity: str
) -> dict[str, Any]:
    event = ledger.get(representation_event_identity)
    if event is None or event.kind != REPRESENTATION_RECORDED_KIND:
        raise ValueError("the addressed occurrence is not a recorded Representation")
    material = event.material
    act_evidence = ledger.get(material.get("responsible_act_evidence_identity"))
    locality_evidence = ledger.get(material.get("locality_evidence_identity"))
    evidence_of_yield_relation_identity = material.get("evidence_of_yield_relation_identity")
    if (
        ledger.integrity_of(event.identity) == CORRUPTED
        or act_evidence is None
        or act_evidence.kind != REPRESENTATION_ACT_EVIDENCE_KIND
        or locality_evidence is None
        or locality_evidence.kind != REPRESENTATION_LOCALITY_EVIDENCE_KIND
        or ledger.integrity_of(locality_evidence.identity) == CORRUPTED
    ):
        raise ValueError("the recorded Representation Evidence is not exact")
    requirements = read_requirements_of_yield_relation(
        ledger,
        recorded_result_event_identity=event.identity,
        evidence_of_yield_relation_event_identity=evidence_of_yield_relation_identity,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )
    if not all(requirements.values()):
        raise ValueError("the recorded Representation Yield is not exact")
    source_occurrence_reference = material.get("source_occurrence_reference")
    _validate_standing_boundary(
        ledger,
        locality_identity=event.locality_identity,
        through_event_occurrence_identity=material.get(
            "locality_standing_through_event_occurrence_identity"
        ),
        source_occurrence_reference=source_occurrence_reference,
        representation_event_identity=event.identity,
    )
    if source_occurrence_reference is not None:
        source = ledger.get(source_occurrence_reference)
        if (
            source is None
            or source.locality_identity != event.locality_identity
            or ledger.integrity_of(source.identity) == CORRUPTED
        ):
            raise ValueError("the recorded Representation source is not exact")
        reader = _MEASUREMENT_READERS.get(source.kind)
        if reader is None:
            reader = _STRUCTURED_RESULT_READERS.get(source.kind)
        structured_source_result = (
            reader(ledger, source.identity) if reader is not None else None
        )
        if structured_source_result is not None:
            if (
                event.exact_material is not None
                or source.exact_material is not None
                or "representation_rule" in material
            ):
                raise ValueError("the recorded Representation source is not exact")
        elif (
            type(source.exact_material) is not bytes
            or source.exact_material != event.exact_material
            or material.get("representation_rule")
            != EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
        ):
            raise ValueError("the recorded Representation source is not exact")
        source_requirements = read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=source.identity,
            evidence_of_yield_relation_event_identity=source.material.get("evidence_of_yield_relation_identity"),
            responsible_act_evidence_event_identity=source.material.get(
                "responsible_act_evidence_identity"
            ),
        )
        if not all(source_requirements.values()):
            raise ValueError("the recorded Representation source Yield is not exact")
    exact_result = ledger.get(evidence_of_yield_relation_identity).material.get("result")
    if (
        type(exact_result) is not dict
        or locality_evidence.material.get("carried_content") != exact_result
        or locality_evidence.material.get("act_occurrence_identity")
        != material.get("act_occurrence_identity")
        or act_evidence.material.get("act_occurrence_identity")
        != material.get("act_occurrence_identity")
        or act_evidence.material.get("representation_act_identity")
        != material.get("representation_act_identity")
        or event.locality_identity != locality_evidence.locality_identity
        or event.locality_identity != act_evidence.locality_identity
    ):
        raise ValueError("the recorded Representation coordinates are not exact")
    representation = {
        "representation_identity": material["result_identity"],
        "representation_act_identity": material["representation_act_identity"],
        "act_occurrence_identity": material["act_occurrence_identity"],
        "locality_identity": event.locality_identity,
        "representation_result": material["representation_result"],
        "responsible_act_evidence_identity": act_evidence.identity,
        "evidence_of_yield_relation_identity": evidence_of_yield_relation_identity,
        "locality_evidence_identity": locality_evidence.identity,
        "representation_event_identity": event.identity,
        "recorded_occurrence_references": (
            act_evidence.identity,
            evidence_of_yield_relation_identity,
            locality_evidence.identity,
            event.identity,
        ),
        "source_occurrence_reference": source_occurrence_reference,
        "locality_standing_through_event_occurrence_identity": material[
            "locality_standing_through_event_occurrence_identity"
        ],
        "exact_material": event.exact_material,
    }
    if "representation_rule" in material:
        representation["representation_rule"] = material["representation_rule"]
    return representation


def emit_operator_representation_material(
    ledger: EventLedger,
    *,
    representation: dict[str, Any],
    admission_result_event_identity: str,
    applicability_result_event_identity: str,
    locality_standing: dict[str, Any],
    output_boundary,
) -> dict[str, Any]:
    """Emit one exact Representation admitted to one operator Locality."""

    from seed_runtime.operator_representation_admission import (
        get_recorded_exact_material_representation_admission,
        exact_material_representation_admission_occurrence_references,
    )
    from seed_runtime.operator_representation_applicability import (
        get_recorded_representation_emission_applicability,
        representation_emission_applicability_occurrence_references,
    )

    admission = get_recorded_exact_material_representation_admission(
        ledger, admission_result_event_identity
    )
    applicability = get_recorded_representation_emission_applicability(
        ledger, applicability_result_event_identity
    )
    from seed_runtime.operator_egress import read_operator_emission_boundary

    (
        output_stream,
        destination_operator_boundary_identity,
        destination_operator_locality_identity,
        destination_operator_boundary_rule,
    ) = read_operator_emission_boundary(output_boundary)
    carried_admissions = (
        locality_standing.get("admission_result_occurrences")
        if type(locality_standing) is dict
        else None
    )
    carried_applicability = (
        locality_standing.get("applicability_result_occurrences")
        if type(locality_standing) is dict
        else None
    )
    if (
        type(carried_admissions) is not dict
        or carried_admissions.get(admission_result_event_identity, object())
        is not None
        or type(carried_applicability) is not dict
        or carried_applicability.get(
            applicability_result_event_identity, object()
        )
        is not None
        or locality_standing.get("locality_identity")
        != admission["scope"]["source_locality_identity"]
        or destination_operator_boundary_identity
        != admission["destination_operator_boundary_identity"]
        or destination_operator_boundary_rule
        != admission["destination_operator_boundary_rule"]
        or destination_operator_locality_identity
        != admission["destination_operator_locality_identity"]
        or applicability["admission_result_event_identity"]
        != admission_result_event_identity
        or applicability["standing"] != "applicable"
        or applicability["downstream_act_identity"]
        != admission["emission_act_identity"]
        or applicability["downstream_act_occurrence_identity"]
        != admission["emission_act_occurrence_identity"]
        or applicability["destination_operator_boundary_rule"]
        != admission["destination_operator_boundary_rule"]
        or applicability["representation_rule_to_boundary_rule_relation"]
        != admission["representation_rule_to_boundary_rule_relation"]
    ):
        raise ValueError(
            "emission requires one exact carried Admission, Applicability, and destination"
        )

    recorded = read_operator_representation(
        ledger, representation.get("representation_event_identity")
    )
    exact_material = recorded["exact_material"]
    if type(exact_material) is not bytes:
        raise ValueError("the recorded Representation carries no exact material")
    for coordinate in (
        "representation_identity",
        "representation_event_identity",
        "locality_identity",
        "exact_material",
    ):
        if representation.get(coordinate) != recorded[coordinate]:
            raise ValueError(
                "the supplied Representation differs from its recorded material"
            )
    if (
        admission["representation_reference"]["representation_event_identity"]
        != recorded["representation_event_identity"]
        or admission["representation_reference"]["representation_identity"]
        != recorded["representation_identity"]
    ):
        raise ValueError("Admission addresses another Representation")
    for prior_attempt in ledger.iter_locality_kind(
        representation["locality_identity"], REPRESENTATION_EMISSION_ATTEMPT_KIND
    ):
        if (
            prior_attempt.material.get("admission_result_event_identity")
            == admission_result_event_identity
            or prior_attempt.material.get("act_occurrence_identity")
            == admission["emission_act_occurrence_identity"]
        ):
            raise ValueError("Admission already participated in an emission attempt")
    representation["recorded_occurrence_references"] = (
        *recorded["recorded_occurrence_references"],
        *exact_material_representation_admission_occurrence_references(
            ledger, admission_result_event_identity
        ),
        *representation_emission_applicability_occurrence_references(
            ledger, applicability_result_event_identity
        ),
    )
    emission_act_identity = admission["emission_act_identity"]
    act_occurrence_identity = admission["emission_act_occurrence_identity"]
    result_identity = admission["emission_result_boundary_identity"]
    scope = f"locality:{representation['locality_identity']}"
    attempt_event = ledger.append(
        REPRESENTATION_EMISSION_ATTEMPT_KIND,
        {
            "representation_reference": representation["representation_identity"],
            "representation_event_identity": representation[
                "representation_event_identity"
            ],
            "emission_act_identity": emission_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "admission_result_event_identity": admission_result_event_identity,
            "input_applicability_event_identity": (
                applicability_result_event_identity
            ),
            "candidate_result_event_identity": admission["candidate_reference"][
                "recorded_occurrence_identity"
            ],
            "destination_operator_boundary_identity": admission[
                "destination_operator_boundary_identity"
            ],
            "destination_operator_boundary_rule": admission[
                "destination_operator_boundary_rule"
            ],
            "destination_operator_locality_identity": admission[
                "destination_operator_locality_identity"
            ],
            "dimensions": _dimensions(
                identity=f"emission-attempt:{representation['representation_identity']}",
                content="exact Representation for the declared emission boundary",
                source=representation["representation_event_identity"],
                responsibility=REPRESENTATION_EXACT_MATERIAL_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "bounded to this attempt occurrence; establishes no output-boundary "
                    "acceptance or downstream effect"
                ),
                scope=scope,
                occurrence="emission attempt occurrence recorded before output",
            ),
            "known_loss": [],
            "unknown": [
                "output-boundary acceptance remains Unknown until Evidence establishes it",
                "effects beyond the output boundary remain Unknown",
            ],
            "conflicts": [],
            "provenance_occurrence_references": [
                representation["representation_event_identity"]
            ],
        },
        exact_material=exact_material,
        locality_identity=representation["locality_identity"],
    )
    representation["emission_attempt_event_identity"] = attempt_event.identity
    representation["recorded_occurrence_references"] += (attempt_event.identity,)
    attempt_locality_evidence = ledger.append(
        REPRESENTATION_EMISSION_ATTEMPT_LOCALITY_EVIDENCE_KIND,
        {
            "representation_reference": representation["representation_identity"],
            "attempt_event_identity": attempt_event.identity,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence bounded to the exact Representation-to-emission-attempt Locality"
            ),
        },
        exact_material=exact_material,
        locality_identity=representation["locality_identity"],
    )
    representation["emission_attempt_locality_evidence_identity"] = (
        attempt_locality_evidence.identity
    )
    representation["recorded_occurrence_references"] += (
        attempt_locality_evidence.identity,
    )

    # The exact attempt and its Locality Evidence are durable before bytes can
    # leave Seed. Process death after this flush remains an attempt with an
    # Unknown boundary result; it is not manufactured into a failure result.
    ledger.flush()

    try:
        written = emit_exact_material(output_stream, exact_material)
    except ExactMaterialEgressFailure as failure:
        _record_exact_material_boundary_failure(
            ledger,
            representation=representation,
            attempt_event_identity=attempt_event.identity,
            emitted_event_identity=None,
            scope=scope,
            reported_count=failure.reported_count,
            error=failure.error,
        )
        if failure.error is not None:
            raise failure.error from failure
        raise ValueError(
            "output boundary did not accept the exact representation"
        ) from failure
    except Exception as error:
        _record_exact_material_boundary_failure(
            ledger,
            representation=representation,
            attempt_event_identity=attempt_event.identity,
            emitted_event_identity=None,
            scope=scope,
            reported_count=None,
            error=error,
        )
        raise

    locality_relation = {
        "first_subject": representation["representation_identity"],
        "second_subject": act_occurrence_identity,
        "relation_occurrence_identity": new_identity(
            "operator_representation_emission_locality_occurrence"
        ),
    }
    boundary_result = {"accepted_count": written}
    result_content = {
        "result_identity": result_identity,
        "result": boundary_result,
    }
    result_material = {
        "emission_act_identity": emission_act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "representation_reference": representation["representation_identity"],
        "representation_event_identity": representation[
            "representation_event_identity"
        ],
        "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
        "admission_result_event_identity": admission_result_event_identity,
        "input_applicability_event_identity": applicability_result_event_identity,
        "candidate_result_event_identity": admission["candidate_reference"][
            "recorded_occurrence_identity"
        ],
        "destination_operator_boundary_identity": admission[
            "destination_operator_boundary_identity"
        ],
        "destination_operator_boundary_rule": admission[
            "destination_operator_boundary_rule"
        ],
        "destination_operator_locality_identity": admission[
            "destination_operator_locality_identity"
        ],
        "locality_relation": locality_relation,
        "boundary_result": boundary_result,
        **result_content,
    }
    responsible_act_evidence = ledger.append(
        REPRESENTATION_EMISSION_ACT_EVIDENCE_KIND,
        {
            "emission_act_identity": emission_act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "exact bounded Representation emission",
            "responsibility": REPRESENTATION_EXACT_MATERIAL_EMISSION_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "representation_reference": representation["representation_identity"],
            "representation_event_identity": representation[
                "representation_event_identity"
            ],
            "input_role": REPRESENTATION_EMISSION_INPUT_ROLE,
            "admission_result_event_identity": admission_result_event_identity,
            "input_applicability_event_identity": (
                applicability_result_event_identity
            ),
            "candidate_result_event_identity": admission["candidate_reference"][
                "recorded_occurrence_identity"
            ],
            "destination_operator_boundary_identity": admission[
                "destination_operator_boundary_identity"
            ],
            "destination_operator_boundary_rule": admission[
                "destination_operator_boundary_rule"
            ],
            "destination_operator_locality_identity": admission[
                "destination_operator_locality_identity"
            ],
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence bounded to this exact emission Act occurrence and "
                "the Representation participating in its exact input role; establishes no other role"
            ),
        },
        locality_identity=representation["locality_identity"],
    )
    locality_evidence = ledger.append(
        REPRESENTATION_EMISSION_LOCALITY_EVIDENCE_KIND,
        {
            "act_occurrence_identity": act_occurrence_identity,
            "representation_reference": representation["representation_identity"],
            "representation_event_identity": representation[
                "representation_event_identity"
            ],
            "locality_relation": locality_relation,
            "authority": "unestablished",
            "evidence_scope": (
                "Evidence bounded to the exact Representation-to-emission-occurrence Locality"
            ),
        },
        exact_material=exact_material,
        locality_identity=representation["locality_identity"],
    )
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=representation["locality_identity"],
        exact_act="exact bounded Representation emission",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=responsible_act_evidence.identity,
        result_kind=REPRESENTATION_EMISSION_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_content,
        result_exact_material=exact_material,
        responsibility=REPRESENTATION_EXACT_MATERIAL_EMISSION_RESPONSIBILITY,
        live_boundary="successful_emission",
        responsible_boundary="this Seed",
    )
    emitted_event = ledger.append(
        REPRESENTATION_EMITTED_KIND,
        {
            "attempt_reference": attempt_event.identity,
            **result_material,
            "dimensions": _dimensions(
                identity=act_occurrence_identity,
                content="exact Representation emitted at the declared boundary",
                source=representation["representation_event_identity"],
                responsibility=REPRESENTATION_EXACT_MATERIAL_EMISSION_RESPONSIBILITY,
                authority="unestablished",
                evidence_scope=(
                    "bounded to this emission occurrence; effects beyond the output "
                    "boundary require separate Evidence"
                ),
                scope=scope,
                occurrence="emission occurrence recorded",
            ),
            "responsible_act_evidence_identity": responsible_act_evidence.identity,
            "locality_evidence_identity": locality_evidence.identity,
            "evidence_of_yield_relation_identity": evidence_of_yield_relation.identity,
            "known_loss": [],
            "unknown": [],
            "conflicts": [],
            "provenance_occurrence_references": [
                representation["representation_event_identity"],
                admission_result_event_identity,
                applicability_result_event_identity,
                attempt_event.identity,
            ],
        },
        exact_material=exact_material,
        locality_identity=representation["locality_identity"],
    )
    representation["emission_act_evidence_identity"] = (
        responsible_act_evidence.identity
    )
    representation["emission_locality_evidence_identity"] = locality_evidence.identity
    representation["emission_evidence_of_yield_relation_identity"] = evidence_of_yield_relation.identity
    representation["emitted_event_identity"] = emitted_event.identity
    representation["recorded_occurrence_references"] += (
        responsible_act_evidence.identity,
        locality_evidence.identity,
        evidence_of_yield_relation.identity,
        emitted_event.identity,
    )
    # The exact write acceptance and its Yield are durable before a later host
    # flush is invoked.  A flush exception is a distinct boundary occurrence;
    # it cannot revise the already-recorded emission into nonoccurrence.
    ledger.flush()
    flush = getattr(output_stream, "flush", None)
    if flush is not None:
        try:
            flush_result = flush()
            if flush_result is not None:
                raise ValueError("output boundary flush did not report completion")
        except Exception as error:
            _record_exact_material_boundary_failure(
                ledger,
                representation=representation,
                attempt_event_identity=attempt_event.identity,
                emitted_event_identity=emitted_event.identity,
                scope=scope,
                reported_count=written,
                error=error,
            )
            raise
    return representation


def _record_exact_material_boundary_failure(
    ledger: EventLedger,
    *,
    representation: dict[str, Any],
    attempt_event_identity: str,
    emitted_event_identity: str | None,
    scope: str,
    reported_count: int | None,
    error: Exception | None,
):
    """Preserve one boundary failure without revising accepted emission."""

    unknown = [
        "output-boundary result remains Unknown",
        "effects beyond the output boundary remain Unknown",
    ]
    act_identity = new_identity("operator_representation_boundary_failure_act")
    act_occurrence_identity = new_identity(
        "operator_representation_boundary_failure_act_occurrence"
    )
    result_identity = new_identity("operator_representation_boundary_failure_result")
    result_material = {
        "result_identity": result_identity,
        "downstream_act_identity": act_identity,
        "act_occurrence_identity": act_occurrence_identity,
        "attempt_reference": attempt_event_identity,
        "representation_reference": representation["representation_identity"],
        "representation_event_identity": representation[
            "representation_event_identity"
        ],
        "emitted_event_identity": emitted_event_identity,
        "dimensions": _dimensions(
            identity=f"boundary-failure:{attempt_event_identity}",
            content="Representation boundary failure occurrence",
            source=attempt_event_identity,
            responsibility=REPRESENTATION_BOUNDARY_FAILURE_RESPONSIBILITY,
            authority="unestablished",
            evidence_scope=(
                "bounded to this failure occurrence; establishes no downstream effect "
                "and no acceptance beyond the reported result"
            ),
            scope=scope,
            occurrence="boundary failure occurrence recorded",
        ),
        "reported_count": reported_count,
        "error": repr(error) if error is not None else None,
        "known_loss": [],
        "unknown": unknown,
        "conflicts": [],
        "provenance_occurrence_references": [
            representation["representation_event_identity"],
            attempt_event_identity,
        ],
    }
    act_evidence = ledger.append(
        REPRESENTATION_BOUNDARY_FAILURE_ACT_EVIDENCE_KIND,
        {
            "downstream_act_identity": act_identity,
            "act_occurrence_identity": act_occurrence_identity,
            "act": "Representation boundary failure after exact write invocation",
            "responsibility": REPRESENTATION_BOUNDARY_FAILURE_RESPONSIBILITY,
            "responsible_boundary": "this Seed",
            "authority": "unestablished",
            "evidence_scope": (
                "bounded to this exact Representation boundary failure occurrence"
            ),
        },
        locality_identity=representation["locality_identity"],
    )
    evidence_of_yield_relation = _record_evidence_of_yield_relation(
        ledger,
        locality_identity=representation["locality_identity"],
        exact_act="Representation boundary failure after exact write invocation",
        act_occurrence_identity=act_occurrence_identity,
        responsible_act_evidence_identity=act_evidence.identity,
        result_kind=REPRESENTATION_BOUNDARY_FAILURE_RESULT_KIND,
        result_identity=result_identity,
        result_content=result_material,
        responsibility=REPRESENTATION_BOUNDARY_FAILURE_RESPONSIBILITY,
        live_boundary="failed_boundary",
        responsible_boundary="this Seed",
        coordinates_of_recorded_result={key: (key,) for key in result_material},
    )
    failed_event = ledger.append(
        REPRESENTATION_BOUNDARY_FAILURE_KIND,
        {
            **result_material,
            "responsible_act_evidence_identity": act_evidence.identity,
            "evidence_of_yield_relation_identity": evidence_of_yield_relation.identity,
        },
        locality_identity=representation["locality_identity"],
    )
    representation["boundary_failure_act_evidence_identity"] = act_evidence.identity
    representation["boundary_failure_evidence_of_yield_relation_identity"] = evidence_of_yield_relation.identity
    representation["boundary_failure_event_identity"] = failed_event.identity
    representation["recorded_occurrence_references"] += (
        act_evidence.identity,
        evidence_of_yield_relation.identity,
        failed_event.identity,
    )
    return failed_event
