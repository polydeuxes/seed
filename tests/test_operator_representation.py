from tests.binary_input import binary_input
from io import BytesIO, StringIO

import pytest
from tests.representation_admission import admit_representation

FIDELITY_SUBJECT = "exact_Representation_occurrence"

from seed_runtime.byte_measurement import (
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    record_byte_measurement_responsibility_assignment,
    assertions_of_recorded_byte_measurement,
    record_byte_measurement_responsible_act_evidence,
    record_byte_measurement_result,
    record_byte_position_pair_count_layer,
)
from seed_runtime.events import CORRUPTED, EventLedger
from seed_runtime.operator_representation import (
    EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
    emit_operator_representation_material,
    read_operator_representation,
    record_operator_representation,
)
from seed_runtime.material_ingest import ingest_material, is_exact_ingest_result
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.occurrence_position_measurement import (
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    get_recorded_occurrence_position_measurement,
    measure_occurrence_position,
    record_occurrence_position_measurement_responsibility_assignment,
    record_occurrence_position_measurement_responsible_act_evidence,
    record_occurrence_position_measurement_result,
)
from seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences import (
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
from seed_runtime.evidence_of_yield_relation import read_requirements_of_yield_relation
from seed_runtime.operator_representation_admission import RepresentationAdmissionError
from seed_runtime.operator_console import run_persistent_operator_console

_BYTE_MEASUREMENT_KINDS = (
    BYTE_MEASUREMENT_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    "operator.measurement.byte_responsible_act_evidenced",
    "operator.evidence_of_yield_relation_recorded",
    "operator.measurement.byte_counts_recorded",
)
_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KINDS = (
    BYTE_PAIR_OCCURRENCE_POSITION_ASSIGNMENT_KIND,
    BYTE_PAIR_OCCURRENCE_POSITION_ACT_EVIDENCE_KIND,
    "operator.evidence_of_yield_relation_recorded",
    BYTE_PAIR_OCCURRENCE_POSITION_RESULT_KIND,
)
_OCCURRENCE_POSITION_MEASUREMENT_KINDS = (
    OCCURRENCE_POSITION_RESPONSIBILITY_ASSIGNMENT_RECORDED_KIND,
    "operator.measurement.locality_occurrence_position_act_evidenced",
    "operator.evidence_of_yield_relation_recorded",
    "operator.measurement.locality_occurrence_position_recorded",
)
_REPRESENTATION_RELATION_EVIDENCE_KINDS = (
    "operator.representation.act_evidenced",
    "operator.evidence_of_yield_relation_recorded",
    "operator.representation.locality_evidenced",
)
_OPERATOR_MATERIAL_ACQUIRE_BEGIN_KINDS = (
    "operator.material.acquire_responsibility_assignment_recorded",
    "operator.material.acquire_act_evidenced",
)
_OPERATOR_MATERIAL_ACQUIRE_RESULT_KINDS = (
    "operator.evidence_of_yield_relation_recorded",
    "operator.material.acquire_recorded",
)


def _one_material_console_kinds():
    return [
        *_REPRESENTATION_RELATION_EVIDENCE_KINDS,
        "operator.representation.recorded",
        *_OPERATOR_MATERIAL_ACQUIRE_BEGIN_KINDS,
        *_OPERATOR_MATERIAL_ACQUIRE_RESULT_KINDS,
        *_REPRESENTATION_RELATION_EVIDENCE_KINDS,
        "operator.representation.recorded",
        *_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KINDS,
        *_BYTE_MEASUREMENT_KINDS,
        *_OCCURRENCE_POSITION_MEASUREMENT_KINDS,
        *_REPRESENTATION_RELATION_EVIDENCE_KINDS,
        "operator.representation.recorded",
        *_OPERATOR_MATERIAL_ACQUIRE_BEGIN_KINDS,
    ]


class DictSubclass(dict):
    pass


def _run_console(text, *, locality="s"):
    ledger = EventLedger()
    output = StringIO()
    run_persistent_operator_console(
        ledger=ledger,
        locality_identity=locality,
        input_stream=binary_input(text),
        output_stream=output,
    )
    return ledger, output.getvalue()


def _standing(ledger, *, locality="s"):
    return read_operator_locality_standing(
        ledger, locality_identity=locality
    )


def _byte_measurement(ledger, *, locality="s"):
    ingest_material(
        ledger,
        locality_identity=locality,
        exact_bytes=b"aba",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    assignment = record_byte_measurement_responsibility_assignment(
        ledger,
        source_localities=(locality,),
        recording_locality_identity=locality,
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    responsible_act_evidence = record_byte_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=read_operator_locality_standing(
            ledger, locality_identity=locality
        ),
    )
    return record_byte_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=responsible_act_evidence.identity,
    )


def _structured_measurement(ledger, kind, *, locality="s"):
    byte = _byte_measurement(ledger, locality=locality)
    if kind == "pair":
        return record_byte_position_pair_count_layer(
            ledger,
            source_measurement_event_identity=byte.identity,
            recording_locality_identity=locality,
        )
    finding = measure_occurrence_position(
        ledger, source_locality_identity=locality
    )
    assignment = record_occurrence_position_measurement_responsibility_assignment(
        ledger,
        recording_locality_identity=locality,
        finding=finding,
        locality_standing=_standing(ledger, locality=locality),
    )
    act_evidence = record_occurrence_position_measurement_responsible_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=_standing(ledger, locality=locality),
    )
    return record_occurrence_position_measurement_result(
        ledger,
        responsible_act_evidence_event_identity=act_evidence.identity,
    )


def _record_fixture_representation(ledger, *, locality="s"):
    return record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=_standing(ledger, locality=locality),
    )


def _recorded_representation(ledger, *, locality="s"):
    representation = record_operator_representation(
        ledger,
        locality_identity=locality,
        locality_standing=_standing(ledger, locality=locality),
    )
    return representation, ledger.get(representation["representation_event_identity"])


def test_representation_reader_reads_the_exact_recorded_representation():
    ledger = EventLedger()
    representation, event = _recorded_representation(ledger)

    recorded = read_operator_representation(ledger, event.identity)

    assert recorded == {
        "representation_identity": representation["representation_identity"],
        "representation_act_identity": representation["representation_act_identity"],
        "act_occurrence_identity": representation["act_occurrence_identity"],
        "locality_identity": representation["locality_identity"],
        "representation_result": representation["representation_result"],
        "responsible_act_evidence_identity": representation[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": representation["evidence_of_yield_relation_identity"],
        "locality_evidence_identity": representation[
            "locality_evidence_identity"
        ],
        "representation_event_identity": representation["representation_event_identity"],
        "recorded_occurrence_references": representation[
            "recorded_occurrence_references"
        ],
        "source_occurrence_reference": None,
        "locality_standing_through_event_occurrence_identity": None,
        "exact_material": None,
    }
    assert ledger.occurrences_in_append_order(
        recorded["recorded_occurrence_references"],
        locality_identity="s",
    )


def test_representation_carries_exact_material_without_claiming_meaning():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    event = ledger.get(representation["representation_event_identity"])
    evidence = ledger.get(event.material["evidence_of_yield_relation_identity"])

    assert event.exact_material == b"hello"
    assert evidence.exact_material == b"hello"
    assert event.material["source_occurrence_reference"] == source.identity
    assert event.material["representation_rule"] == (
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
    )


def test_representation_refuses_a_changed_exact_material_rule():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    event = ledger.get(representation["representation_event_identity"])
    event.material["representation_rule"] = "other"

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_empty_exact_material_carries_its_rule_through_emission():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"",
        source_role="operator",
        source_boundary="empty fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    output = BytesIO()
    admission, applicability, standing, boundary = admit_representation(
        ledger,
        representation,
        output_stream=output,
    )

    emitted = emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )

    recorded = read_operator_representation(
        ledger, representation["representation_event_identity"]
    )
    emission = ledger.get(emitted["emitted_event_identity"])
    assert recorded["exact_material"] == b""
    assert recorded["representation_rule"] == (
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
    )
    assert emission.exact_material == b""
    assert emission.material["boundary_result"] == {"accepted_count": 0}
    assert output.getvalue() == b""


def test_representation_addresses_one_exact_carried_measurement_result():
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    standing = _standing(ledger)

    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=standing,
        source_occurrence_reference=measurement.identity,
    )

    event = ledger.get(representation["representation_event_identity"])
    locality_evidence = ledger.get(representation["locality_evidence_identity"])
    evidence_of_yield_relation = ledger.get(representation["evidence_of_yield_relation_identity"])
    expected_reference = {
        "recorded_occurrence_identity": measurement.identity,
        "result_identity": measurement.material["result_identity"],
        "act_occurrence_identity": measurement.material["act_occurrence_identity"],
        "responsible_act_evidence_identity": measurement.material[
            "responsible_act_evidence_identity"
        ],
        "evidence_of_yield_relation_identity": measurement.material["evidence_of_yield_relation_identity"],
    }
    assert standing["measurement_occurrences"] == {
        measurement.identity: expected_reference
    }
    assert event.material["source_occurrence_reference"] == measurement.identity
    assert (
        locality_evidence.material["carried_content"]["source_occurrence_reference"]
        == measurement.identity
    )
    assert (
        evidence_of_yield_relation.material["result"]["source_occurrence_reference"]
        == measurement.identity
    )
    for material in (
        event.material,
        locality_evidence.material["carried_content"],
        evidence_of_yield_relation.material["result"],
    ):
        assert "assertions" not in material
        assert "measurement_rule" not in material
        assert "occurrence_preservation" not in material
        assert "representation_rule" not in material
    assert event.exact_material is None
    assert locality_evidence.exact_material is None
    assert evidence_of_yield_relation.exact_material is None
    assert read_operator_representation(ledger, event.identity)[
        "source_occurrence_reference"
    ] == measurement.identity

    with pytest.raises(RepresentationAdmissionError, match="without exact material"):
        admit_representation(ledger, representation)


@pytest.mark.parametrize("measurement_kind", ("pair", "position"))
def test_representation_addresses_each_structured_measurement_family(
    measurement_kind,
):
    ledger = EventLedger()
    measurement = _structured_measurement(ledger, measurement_kind)
    standing = _standing(ledger)

    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=standing,
        source_occurrence_reference=measurement.identity,
    )
    event = ledger.get(representation["representation_event_identity"])

    assert measurement.identity in standing["measurement_occurrences"]
    assert event.exact_material is None
    assert read_operator_representation(ledger, event.identity)[
        "source_occurrence_reference"
    ] == measurement.identity
    with pytest.raises(RepresentationAdmissionError, match="without exact material"):
        admit_representation(ledger, representation)


@pytest.mark.parametrize(
    "coordinate",
    (
        "recorded_occurrence_identity",
        "result_identity",
        "act_occurrence_identity",
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    ),
)
def test_representation_rejects_each_wrong_carried_measurement_coordinate(
    coordinate,
):
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    standing = _standing(ledger)
    standing["measurement_occurrences"][measurement.identity][coordinate] = "other"

    with pytest.raises(ValueError, match="Measurement"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=measurement.identity,
        )


def test_exact_result_carrier_does_not_stand_for_measurement_result_carrier():
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    standing = _standing(ledger)
    standing["measurement_occurrences"] = {}
    standing["exact_result_occurrences"][measurement.identity] = None

    with pytest.raises(ValueError, match="Measurement is not carried"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=measurement.identity,
        )


@pytest.mark.parametrize("carrier", ([], DictSubclass()))
def test_representation_refuses_a_nonexact_measurement_carrier(carrier):
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    standing = _standing(ledger)
    standing["measurement_occurrences"] = carrier

    with pytest.raises(ValueError, match="exact carried Measurement results"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=measurement.identity,
        )


def test_representation_refuses_a_measurement_reference_under_the_wrong_key():
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    standing = _standing(ledger)
    reference = standing["measurement_occurrences"].pop(measurement.identity)
    standing["measurement_occurrences"]["other"] = reference

    with pytest.raises(ValueError, match="Measurement is not carried"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=measurement.identity,
        )


def test_representation_refuses_a_subclassed_measurement_reference():
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    standing = _standing(ledger)
    reference = standing["measurement_occurrences"][measurement.identity]
    standing["measurement_occurrences"][measurement.identity] = DictSubclass(
        reference
    )

    with pytest.raises(ValueError, match="Measurement is not exact"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=measurement.identity,
        )


def test_representation_rejects_corrupted_measurement_yield(monkeypatch):
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    standing = _standing(ledger)
    yield_identity = measurement.material["evidence_of_yield_relation_identity"]
    integrity_of = ledger.integrity_of
    monkeypatch.setattr(
        ledger,
        "integrity_of",
        lambda identity: (
            CORRUPTED if identity == yield_identity else integrity_of(identity)
        ),
    )

    with pytest.raises(ValueError):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=measurement.identity,
        )


def test_unrelated_occurrence_does_not_change_addressed_measurement_result():
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"unrelated",
        source_role="operator",
        source_boundary="fixture boundary",
    )

    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=measurement.identity,
    )

    assert representation["exact_material"] is None
    assert ledger.get(representation["representation_event_identity"]).material[
        "source_occurrence_reference"
    ] == measurement.identity


def test_representation_reader_rejects_a_substituted_measurement_reference():
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=measurement.identity,
    )
    other = _byte_measurement(ledger)
    event = ledger.get(representation["representation_event_identity"])
    event.material["source_occurrence_reference"] = other.identity

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_emission_attempt_reference_cannot_substitute_for_representation_source():
    ledger = EventLedger()
    measurement = _byte_measurement(ledger)
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=measurement.identity,
    )
    event = ledger.get(representation["representation_event_identity"])
    event.material["attempt_reference"] = event.material.pop(
        "source_occurrence_reference"
    )

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_representation_consumes_an_exact_yielded_representation_result():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"\x00\xffresult",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    first = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    first_event = ledger.get(first["representation_event_identity"])
    standing = _standing(ledger)

    second = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=standing,
        source_occurrence_reference=first_event.identity,
    )
    second_event = ledger.get(second["representation_event_identity"])

    assert standing["exact_result_occurrences"] == {
        source.identity: None,
        first_event.identity: None,
    }
    assert second_event.material["source_occurrence_reference"] == first_event.identity
    assert second_event.exact_material == b"\x00\xffresult"
    assert ledger.get(
        second_event.material["evidence_of_yield_relation_identity"]
    ).exact_material == b"\x00\xffresult"


def test_representation_refuses_a_raw_carrier_without_exact_yield():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"result",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    unrelated = ledger.append(
        "unrelated.result",
        {
            "evidence_of_yield_relation_identity": source.material["evidence_of_yield_relation_identity"],
            "responsible_act_evidence_identity": source.material[
                "responsible_act_evidence_identity"
            ],
        },
        exact_material=b"result",
        locality_identity="s",
    )
    standing = _standing(ledger)
    standing["exact_result_occurrences"][unrelated.identity] = None

    with pytest.raises(ValueError, match="Yield is not exact"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=unrelated.identity,
        )


def test_representation_refuses_a_nonidentity_result_carrier():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"result",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    standing = _standing(ledger)
    standing["exact_result_occurrences"] = [source.identity]

    with pytest.raises(ValueError, match="exact carried result occurrences"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=source.identity,
        )


def test_representation_does_not_accept_developer_supplied_exact_material():
    with pytest.raises(TypeError, match="exact_material"):
        record_operator_representation(
            EventLedger(),
            locality_identity="s",
            locality_standing={"through_event_occurrence_identity": None},
            exact_material=b"hello",
        )


def test_representation_refuses_a_missing_source_occurrence():
    ledger = EventLedger()

    with pytest.raises(ValueError, match="missing"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=_standing(ledger),
            source_occurrence_reference="missing-source",
        )


def test_representation_refuses_a_source_from_another_locality():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="first",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )

    with pytest.raises(ValueError, match="distinct Locality"):
        record_operator_representation(
            ledger,
            locality_identity="second",
            locality_standing=_standing(ledger, locality="second"),
            source_occurrence_reference=source.identity,
        )


def test_representation_refuses_a_source_after_its_standing_boundary():
    ledger = EventLedger()
    first = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"first",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    boundary_standing = _standing(ledger)
    later = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"later",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    boundary_standing["exact_result_occurrences"][later.identity] = None

    with pytest.raises(ValueError, match="outside its Standing boundary"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=boundary_standing,
            source_occurrence_reference=later.identity,
        )

    assert first.identity != later.identity


def test_representation_refuses_a_standing_boundary_from_another_locality():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"source",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    other = ingest_material(
        ledger,
        locality_identity="other",
        exact_bytes=b"other",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    standing = _standing(ledger)
    standing["through_event_occurrence_identity"] = other.identity

    with pytest.raises(ValueError, match="Standing boundary is not exact"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=source.identity,
        )


def test_representation_refuses_corrupted_source_material():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    standing = _standing(ledger)
    object.__setattr__(source, "exact_material", b"goodbye")

    with pytest.raises(ValueError, match="not exact"):
        record_operator_representation(
            ledger,
            locality_identity="s",
            locality_standing=standing,
            source_occurrence_reference=source.identity,
        )


def test_representation_reader_and_egress_refuse_changed_material():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    event = ledger.get(representation["representation_event_identity"])
    object.__setattr__(event, "exact_material", b"goodbye")

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)
    with pytest.raises(RepresentationAdmissionError, match="intact Representation"):
        admit_representation(ledger, representation)


def test_exact_egress_reads_the_recorded_representation_material():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    output = BytesIO()
    admission, applicability, standing, boundary = admit_representation(
        ledger, representation, output_stream=output
    )

    emitted = emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )
    assert output.getvalue() == b"hello"
    assert emitted is representation

    attempt = ledger.get(representation["emission_attempt_event_identity"])
    attempt_locality = ledger.get(
        representation["emission_attempt_locality_evidence_identity"]
    )
    event = ledger.get(representation["emitted_event_identity"])
    act_evidence = ledger.get(representation["emission_act_evidence_identity"])
    locality_evidence = ledger.get(
        representation["emission_locality_evidence_identity"]
    )
    evidence_of_yield_relation = ledger.get(representation["emission_evidence_of_yield_relation_identity"])

    assert representation["recorded_occurrence_references"] == tuple(
        occurrence.identity for occurrence in ledger.list()
    )[-len(representation["recorded_occurrence_references"]):]
    assert (
        attempt.exact_material
        == attempt_locality.exact_material
        == event.exact_material
        == locality_evidence.exact_material
        == evidence_of_yield_relation.exact_material
        == b"hello"
    )
    assert attempt_locality.material["attempt_event_identity"] == attempt.identity
    assert event.material["boundary_result"] == {"accepted_count": 5}
    assert event.material["result"] == event.material["boundary_result"]
    assert event.material["locality_relation"] == locality_evidence.material[
        "locality_relation"
    ]
    assert act_evidence.material["act_occurrence_identity"] == event.material[
        "act_occurrence_identity"
    ]
    assert all(
        read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=event.identity,
            evidence_of_yield_relation_event_identity=evidence_of_yield_relation.identity,
            responsible_act_evidence_event_identity=act_evidence.identity,
        ).values()
    )
    forbidden = {
        "representation",
        "representation_kind",
        "output_boundary",
        "content_kind",
        "carried_content",
        "accepted_representation",
        "accepted_representation_kind",
        "emitted_representation",
        "emitted_representation_kind",
        "write_count",
        "boundary",
    }
    for occurrence in (
        attempt,
        attempt_locality,
        act_evidence,
        locality_evidence,
        evidence_of_yield_relation,
        event,
    ):
        assert forbidden.isdisjoint(occurrence.material)
    emitted_material = repr(
        [
            occurrence.material
            for occurrence in (
                attempt,
                attempt_locality,
                act_evidence,
                locality_evidence,
                evidence_of_yield_relation,
                event,
            )
        ]
    )
    assert "text_stream" not in emitted_material
    assert "'text'" not in emitted_material
    assert "image" not in emitted_material
    assert "video" not in emitted_material
    assert "Presentation" not in emitted_material

    representation["exact_material"] = b"goodbye"
    with pytest.raises(ValueError, match="differs"):
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing,
            output_boundary=boundary,
        )


@pytest.mark.parametrize(
    ("boundary_type", "error_type", "reported_count", "error_material"),
    (
        ("short", ValueError, 4, None),
        ("unreported", ValueError, None, None),
        ("write-error", OSError, None, "OSError('write failed')"),
        ("flush-error", OSError, 5, "OSError('flush failed')"),
        (
            "flush-result",
            ValueError,
            5,
            "ValueError('output boundary flush did not report completion')",
        ),
    ),
)
def test_exact_material_emission_preserves_each_bounded_failure_result(
    boundary_type, error_type, reported_count, error_material
):
    class FailedBoundary:
        def write(self, material):
            if boundary_type == "short":
                return len(material) - 1
            if boundary_type == "unreported":
                return None
            if boundary_type == "write-error":
                raise OSError("write failed")
            return len(material)

        def flush(self):
            if boundary_type == "flush-error":
                raise OSError("flush failed")
            if boundary_type == "flush-result":
                return False

    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    failed_boundary = FailedBoundary()
    admission, applicability, standing, boundary = admit_representation(
        ledger, representation, output_stream=failed_boundary
    )

    with pytest.raises(error_type):
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing,
            output_boundary=boundary,
        )

    attempt = ledger.get(representation["emission_attempt_event_identity"])
    failure = ledger.get(representation["boundary_failure_event_identity"])
    act_evidence = ledger.get(
        representation["boundary_failure_act_evidence_identity"]
    )
    evidence_of_yield_relation = ledger.get(
        representation["boundary_failure_evidence_of_yield_relation_identity"]
    )
    assert attempt.exact_material == b"hello"
    assert failure.exact_material is None
    assert failure.material["reported_count"] == reported_count
    assert failure.material["error"] == error_material
    emitted_event_identity = representation["emitted_event_identity"]
    if boundary_type in {"flush-error", "flush-result"}:
        assert emitted_event_identity is not None
        emitted = ledger.get(emitted_event_identity)
        emitted_yield = ledger.get(
            representation["emission_evidence_of_yield_relation_identity"]
        )
        emitted_act = ledger.get(representation["emission_act_evidence_identity"])
        assert emitted.material["boundary_result"] == {"accepted_count": 5}
        assert failure.material["emitted_event_identity"] == emitted.identity
        assert all(
            read_requirements_of_yield_relation(
                ledger,
                recorded_result_event_identity=emitted.identity,
                evidence_of_yield_relation_event_identity=emitted_yield.identity,
                responsible_act_evidence_event_identity=emitted_act.identity,
            ).values()
        )
    else:
        assert failure.material["emitted_event_identity"] is None
        assert emitted_event_identity is None
    assert representation["recorded_occurrence_references"] == tuple(
        occurrence.identity for occurrence in ledger.list()
    )[-len(representation["recorded_occurrence_references"]):]
    assert all(
        read_requirements_of_yield_relation(
            ledger,
            recorded_result_event_identity=failure.identity,
            evidence_of_yield_relation_event_identity=evidence_of_yield_relation.identity,
            responsible_act_evidence_event_identity=act_evidence.identity,
        ).values()
    )
    forbidden = {
        "representation_kind",
        "output_boundary",
        "content_kind",
        "carried_content",
        "accepted_representation_kind",
        "emitted_representation_kind",
        "write_count",
        "boundary",
    }
    assert forbidden.isdisjoint(failure.material)


def test_exact_material_process_death_leaves_only_the_durable_attempt():
    class ProcessDeath(BaseException):
        pass

    class DyingBoundary:
        def write(self, material):
            raise ProcessDeath()

    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    dying_boundary = DyingBoundary()
    admission, applicability, standing, boundary = admit_representation(
        ledger, representation, output_stream=dying_boundary
    )

    with pytest.raises(ProcessDeath):
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing,
            output_boundary=boundary,
        )

    assert representation["emission_attempt_event_identity"] is not None
    assert representation["emission_attempt_locality_evidence_identity"] is not None
    assert representation["boundary_failure_event_identity"] is None
    assert representation["emitted_event_identity"] is None
    assert representation["recorded_occurrence_references"] == tuple(
        occurrence.identity for occurrence in ledger.list()
    )[-len(representation["recorded_occurrence_references"]):]


def test_exact_material_emission_recovers_recorded_order_and_refuses_wrong_occurrence():
    ledger = EventLedger()
    source = ingest_material(
        ledger,
        locality_identity="s",
        exact_bytes=b"hello",
        source_role="operator",
        source_boundary="fixture boundary",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    representation["recorded_occurrence_references"] = tuple(
        reversed(representation["recorded_occurrence_references"])
    )
    admission, applicability, standing, boundary = admit_representation(ledger, representation)

    emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )

    assert representation["recorded_occurrence_references"] == tuple(
        occurrence.identity for occurrence in ledger.list()
    )[-len(representation["recorded_occurrence_references"]):]

    other = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
        source_occurrence_reference=source.identity,
    )
    other_admission, other_applicability, other_standing, other_boundary = admit_representation(
        ledger, other
    )
    other["representation_identity"] = representation["representation_identity"]
    with pytest.raises(ValueError, match="differs"):
        emit_operator_representation_material(
            ledger,
            representation=other,
            admission_result_event_identity=other_admission.identity,
            applicability_result_event_identity=other_applicability.identity,
            locality_standing=other_standing,
            output_boundary=other_boundary,
        )


def test_raw_console_does_not_select_operator_input_for_egress():
    ledger = EventLedger()
    raw_output = BytesIO()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input(b"hello\n"),
        output_stream=StringIO(),
        raw_output_stream=raw_output,
    )

    assert raw_output.getvalue() == b""
    assert not any(
        event.kind == "operator.representation.emission.attempted"
        for event in ledger.list()
    )


@pytest.mark.parametrize(
    "coordinate",
    ("responsible_act_evidence_identity", "locality_evidence_identity", "evidence_of_yield_relation_identity"),
)
def test_representation_reader_refuses_each_missing_evidence_pointer(coordinate):
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    event.material[coordinate] = "missing-evidence"

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_representation_reader_refuses_a_developer_formed_event():
    ledger = EventLedger()
    event = ledger.append(
        "operator.representation.recorded",
        {
            "representation_reference": "developer-supplied",
            "representation_act_identity": "developer-supplied-act",
            "act_occurrence_identity": "developer-supplied-occurrence",
        },
        locality_identity="s",
    )

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_representation_reader_refuses_a_different_carried_result():
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    event.material["representation_result"] = "different"

    with pytest.raises(ValueError, match="Yield is not exact"):
        read_operator_representation(ledger, event.identity)


@pytest.mark.parametrize(
    "evidence_coordinate,event_coordinate",
    (
        ("act_occurrence_identity", "act_occurrence_identity"),
        ("representation_act_identity", "representation_act_identity"),
    ),
)
def test_representation_reader_refuses_different_act_evidence_coordinates(
    evidence_coordinate, event_coordinate
):
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    evidence = ledger.get(event.material["responsible_act_evidence_identity"])
    evidence.material[evidence_coordinate] = (
        f"different-{event.material[event_coordinate]}"
    )

    with pytest.raises(ValueError, match="not exact"):
        read_operator_representation(ledger, event.identity)


def test_representation_reader_refuses_different_locality_evidence_content():
    ledger = EventLedger()
    _, event = _recorded_representation(ledger)
    evidence = ledger.get(event.material["locality_evidence_identity"])
    evidence.material["carried_content"]["known_loss"] = ["different"]

    with pytest.raises(ValueError, match="coordinates are not exact"):
        read_operator_representation(ledger, event.identity)


def test_console_forms_c0_before_first_ingress_and_preserves_provenance_only():
    ledger, _ = _run_console("hello\n")

    # A current Representation existing does not make the newest Ingest and the
    # most recently recorded Representation participants in one Compare.  The
    # occurrence and its exact Yield relation are preserved; no Compare or
    # Identification follows.
    kinds = [event.kind for event in ledger.list()]
    assert kinds == _one_material_console_kinds()
    c0_formed = next(
        event
        for event in ledger.list()
        if event.kind == "operator.representation.recorded"
    )
    assert c0_formed.material["locality_standing_through_event_occurrence_identity"] is None
    assert c0_formed.material["unknown"] == []
    # The console attaches no Representation to the Ingest: recording order
    # does not determine a relation between the two occurrences.
    ingest = next(
        event
        for event in ledger.list()
        if is_exact_ingest_result(event)
    )
    assert ingest.material.get("representation_reference") is None


def test_console_ingest_adds_only_its_exact_occurrences():
    # The required proving: C recorded, E preserved, yield provenance
    # retained, and no Compare or Identification occurrence.  Recency does not
    # make C and E participants in one act; 01.Standing.E.1 requires the act
    # responsible boundary to determine input-to-Act Applicability, and no read
    # Responsibility presently proposes those subjects.
    ledger, _ = _run_console("hello\nsecond\nthird\n")

    kinds = [event.kind for event in ledger.list()]
    assert not any(kind.startswith("operator.interaction.") for kind in kinds)

    # Every Ingest retains an identity distinct from Representation occurrences.
    representations = [e for e in ledger.list() if e.kind == "operator.representation.recorded"]
    ingests = [e for e in ledger.list() if is_exact_ingest_result(e)]
    assert len(ingests) == 3
    # Standing read remains valid and records the occurrences.
    standing = _standing(ledger)
    assert len(standing["ingest_occurrences"]) == 3
    assert all(
        set(occurrence)
        == {
            "subject_reference",
            "standing",
            "authority",
            "evidence_event_identity",
            "source_role",
        }
        for occurrence in standing["ingest_occurrences"]
    )


def test_c0_presents_standing_with_no_developer_semantics():
    ledger = EventLedger()
    standing = _standing(ledger)
    c0 = record_operator_representation(
        ledger, locality_identity="s", locality_standing=standing
    )
    # Empty Standing is legitimately input: the representation Act occurred and
    # recorded what it input, rather than being skipped.
    material = ledger.get(c0["representation_event_identity"]).material
    assert material["locality_standing_through_event_occurrence_identity"] is None
    assert material["unknown"] == []
    assert material["conflicts"] == []

    # No developer-supplied sources, represented relations, or treatment.
    flattened = str(material)
    for injected in (
        "Establish richer shared grammar",
        "Show current Standing",
        "establish no such result relation and stop locally",
        "developer-supplied",
    ):
        assert injected not in flattened, injected


def test_representation_act_dimensions_record_only_coordinates_that_exist():
    ledger = EventLedger()
    standing = _standing(ledger)

    zero = record_operator_representation(
        ledger, locality_identity="s", locality_standing=standing
    )
    dimensions = ledger.get(zero["representation_event_identity"]).material["dimensions"]
    assert dimensions["content"] == (
        "bounded Representation of one exact Locality Standing boundary"
    )
    assert dimensions["occurrence_preservation"] == (
        "Representation Act occurrence recorded"
    )
    # No Assertion of coordinates this Representation does not carry.
    flattened = str(dimensions).lower()
    for forbidden_text in (
        "bounded-alternative",
        "bounded alternative",
        "role-tagged",
        "bindings",
        "represented-source",
    ):
        assert forbidden_text not in flattened, forbidden_text

def test_console_presents_standing_only_across_an_ingest():
    ledger, _ = _run_console("hello\n")

    kinds = [event.kind for event in ledger.list()]
    assert kinds == _one_material_console_kinds()
    # No relation or result-Standing occurrence follows by identity.
    assert not any(k.startswith("operator.interaction.") for k in kinds)

    events = ledger.list()
    representations = [
        event for event in events if event.kind == "operator.representation.recorded"
    ]
    c0 = representations[0]
    c1 = representations[-1]
    ingest = next(
        event for event in events if is_exact_ingest_result(event)
    )
    positions = next(
        event
        for event in events
        if event.kind == "operator.measurement.locality_occurrence_position_recorded"
    )
    # C1 uses Standing that now contains the Ingest occurrence.
    assert (
        c1.material["locality_standing_through_event_occurrence_identity"] == positions.identity
    )
    assert c1.material["source_occurrence_reference"] is None
    assert ingest.identity in dict(
        get_recorded_occurrence_position_measurement(
            ledger,
            positions.identity,
        ).occurrences
    )
    # No developer result semantics anywhere in the locality.
    locality = str([e.material for e in ledger.list()])
    assert "developer-supplied" not in locality
    assert "Establish richer shared grammar" not in locality


def test_c0_and_c1_are_recorded_in_order_without_authored_output():
    ledger, output = _run_console("hello\n")

    events = ledger.list()
    ingest_index = next(
        index
        for index, event in enumerate(events)
        if is_exact_ingest_result(event)
    )
    recorded = [
        i for i, event in enumerate(events)
        if event.kind == "operator.representation.recorded"
    ]
    assert recorded[0] < ingest_index < recorded[-1]
    assert output == ""
    assert not any(
        event.kind == "operator.representation.emitted" for event in events
    )


def test_representations_from_other_localities_cannot_enter():
    ledger = EventLedger()
    _record_fixture_representation(ledger, locality="s1")
    _record_fixture_representation(ledger, locality="s2")

    absent = _standing(ledger, locality="s3")
    assert absent["representations"] == {}
    own = _standing(ledger, locality="s1")
    assert len(own["representations"]) == 1


def test_representation_representation_is_deterministic_under_unrelated_events():
    ledger = EventLedger()
    _record_fixture_representation(ledger)
    before = _standing(ledger)

    ledger.append("unrelated.kind", {"noise": True}, locality_identity="s")
    _record_fixture_representation(ledger, locality="elsewhere")
    after = _standing(ledger)

    assert after == before


def test_next_console_iteration_validates_c1_and_forms_c2():
    # Direct read: after C1 is recorded, the read side returns its exact
    # Representation coordinates.
    ledger = EventLedger()
    c1 = _record_fixture_representation(ledger)
    read = list(_standing(ledger)["representations"].values())[-1]
    assert read["representation_identity"] == c1["representation_identity"]
    assert read["emitted_event_identity"] == c1["emitted_event_identity"]

    # Through the console: the second iteration has as input Standing containing
    # C1 and represents C2.
    console_ledger, output = _run_console("first\nsecond\n")
    standing = _standing(console_ledger)
    assert len(standing["representations"]) == 5
    assert output == ""
    representation_identities = list(standing["representations"])
    c1 = standing["representations"][representation_identities[2]]
    c2 = standing["representations"][representation_identities[4]]
    positions = {
        event.identity: index for index, event in enumerate(console_ledger.list())
    }
    boundary = positions[c2["locality_standing_through_event_occurrence_identity"]]
    assert positions[c1["representation_event_identity"]] < boundary
    assert c1["emitted_event_identity"] is None
    assert c1["representation_identity"] != c2["representation_identity"]


def test_later_operator_material_does_not_replace_an_earlier_focus():
    ledger, _ = _run_console("O1\nO2\nO3\n")
    ingests = [
        event for event in ledger.list() if is_exact_ingest_result(event)
    ]
    standing = _standing(ledger)
    focused = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=standing,
        source_occurrence_reference=ingests[1].identity,
    )
    read = read_operator_representation(
        ledger, focused["representation_event_identity"]
    )

    assert read["source_occurrence_reference"] == ingests[1].identity
    assert read["exact_material"] == b"O2\n"
    assert read["locality_standing_through_event_occurrence_identity"] == standing[
        "through_event_occurrence_identity"
    ]
    assert all(
        event.identity in {
            occurrence["evidence_event_identity"]
            for occurrence in standing["ingest_occurrences"]
        }
        for event in ingests
    )


def test_acquisition_act_and_eof_do_not_manufacture_representation_results():
    ledger, _ = _run_console("first\n")
    events = ledger.list()
    acquire_acts = [
        (position, event)
        for position, event in enumerate(events)
        if event.kind == "operator.material.acquire_act_evidenced"
    ]
    acquire_results = [
        (position, event)
        for position, event in enumerate(events)
        if event.kind == "operator.material.acquire_recorded"
    ]

    assert len(acquire_acts) == 2
    assert len(acquire_results) == 1
    first_act_position = acquire_acts[0][0]
    result_position = acquire_results[0][0]
    assert not [
        event
        for event in events[first_act_position + 1 : result_position]
        if event.kind == "operator.representation.recorded"
    ]
    eof_act_position = acquire_acts[1][0]
    assert not [
        event
        for event in events[eof_act_position + 1 :]
        if event.kind == "operator.representation.recorded"
    ]


def test_first_interaction_attaches_no_representation_to_the_ingest():
    ledger, _ = _run_console("first\n")

    # No Representation is named by the Ingest. Representation and Ingest
    # occurrences retain distinct identities; any relation between them is a
    # later responsible occurrence's to establish and record.
    kinds = {event.kind for event in ledger.list()}
    assert kinds == {
        *_BYTE_PAIR_OCCURRENCE_POSITION_MEASUREMENT_KINDS,
        *_BYTE_MEASUREMENT_KINDS,
        *_OCCURRENCE_POSITION_MEASUREMENT_KINDS,
        *_OPERATOR_MATERIAL_ACQUIRE_BEGIN_KINDS,
        "operator.material.acquire_recorded",
        "operator.representation.act_evidenced",
        "operator.representation.locality_evidenced",
        "operator.representation.recorded",
    }
    ingest = next(
        event
        for event in ledger.list()
        if is_exact_ingest_result(event)
    )
    first_representation = next(iter(_standing(ledger)["representations"].values()))
    assert first_representation["representation_identity"]


def test_each_ingest_freezes_one_exact_byte_measurement_boundary():
    ledger, _ = _run_console("a\nb\n")
    measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == "operator.measurement.byte_counts_recorded"
    )

    assert len(measurements) == 2
    first = assertions_of_recorded_byte_measurement(
        ledger, measurements[0].identity
    )
    second = assertions_of_recorded_byte_measurement(
        ledger, measurements[1].identity
    )
    first_counts = {
        assertion.representation: assertion.material["dimensions"]["content"]["count"]
        for assertion in first
        if assertion.result == "count"
    }
    second_counts = {
        assertion.representation: assertion.material["dimensions"]["content"]["count"]
        for assertion in second
        if assertion.result == "count"
    }

    assert first_counts == {10: 1, 97: 1}
    assert second_counts == {10: 2, 97: 1, 98: 1}


def test_each_ingest_freezes_one_exact_occurrence_position_boundary():
    ledger, _ = _run_console("a\nb\n")
    measurements = tuple(
        event
        for event in ledger.list()
        if event.kind == "operator.measurement.locality_occurrence_position_recorded"
    )

    assert len(measurements) == 2
    findings = tuple(
        get_recorded_occurrence_position_measurement(ledger, event.identity)
        for event in measurements
    )
    for finding in findings:
        expected = ledger.list_locality(
            "s",
            through=finding.completeness_boundary,
        )
        assert finding.occurrences == tuple(
            (event.identity, position)
            for position, event in enumerate(expected)
        )
    assert measurements[0].identity not in dict(findings[0].occurrences)
    assert measurements[0].identity in dict(findings[1].occurrences)
    assert measurements[1].identity not in dict(findings[1].occurrences)


def test_empty_operator_boundary_records_no_measurement():
    ledger = EventLedger()

    run_persistent_operator_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=BytesIO(),
        output_stream=StringIO(),
    )

    assert not any(
        event.kind
        in {
            "operator.measurement.byte_counts_recorded",
            "operator.measurement.locality_occurrence_position_recorded",
        }
        for event in ledger.list()
    )


def test_representation_act_is_recorded_without_manufacturing_emission():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=_standing(ledger),
    )
    assert representation["emitted_event_identity"] is None
    # Representation Act is read; no emission occurrence is manufactured.
    recorded = list(_standing(ledger)["representations"].values())[-1]
    assert recorded["representation_event_identity"] == representation["representation_event_identity"]
    assert recorded["emitted_event_identity"] is None

    representation_event = ledger.get(representation["representation_event_identity"])
    act_evidence = ledger.get(
        representation_event.material["responsible_act_evidence_identity"]
    )
    evidence_of_yield_relation = ledger.get(representation_event.material["evidence_of_yield_relation_identity"])
    locality_evidence = ledger.get(
        representation_event.material["locality_evidence_identity"]
    )
    assert representation["representation_act_identity"] == act_evidence.material[
        "representation_act_identity"
    ]
    assert representation["act_occurrence_identity"] == act_evidence.material[
        "act_occurrence_identity"
    ]
    assert representation["act_occurrence_identity"] == evidence_of_yield_relation.material[
        "dimensions"
    ]["act_occurrence_identity"]
    assert representation["act_occurrence_identity"] == locality_evidence.material[
        "act_occurrence_identity"
    ]
    assert locality_evidence.material["carried_content"]["result_identity"] == (
        representation["representation_identity"]
    )
    assert "input_role" not in representation_event.material

    read = list(_standing(ledger)["representations"].values())[-1]
    assert read["representation_identity"] == representation["representation_identity"]
    assert read["emitted_event_identity"] is None
