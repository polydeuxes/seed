from io import BytesIO

import pytest

FIDELITY_SUBJECT = "applicability_determination"

from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from seed_runtime.operator_locality_standing import (
    read_operator_locality_standing,
    read_operator_locality_standing_through,
)
from seed_runtime.operator_representation import (
    EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
    emit_operator_representation_material,
    record_operator_representation,
)
from seed_runtime.operator_egress import (
    EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    operator_emission_boundary,
)
from seed_runtime.operator_representation_applicability import (
    RepresentationApplicabilityError,
    get_recorded_representation_emission_applicability,
    record_representation_emission_applicability_act_evidence,
    record_representation_emission_applicability_result,
)
from tests.representation_admission import admit_representation


class IntegrityAdversaryLedger(EventLedger):
    def __init__(self):
        super().__init__()
        self.corrupted_identities = set()

    def mark_corrupted(self, event_identity):
        self.corrupted_identities.add(event_identity)

    def integrity_of(self, event_identity):
        if event_identity in self.corrupted_identities:
            return CORRUPTED
        return super().integrity_of(event_identity)


def _representation(ledger, exact=b"applicable material"):
    source = record_witness_material_acquisition(
        ledger,
        locality_identity="seed-locality",
        exact_bytes=exact,
        source_boundary="exact fixture boundary",
    )
    return record_operator_representation(
        ledger,
        locality_identity="seed-locality",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="seed-locality"
        ),
        source_occurrence_reference=source.identity,
    )


def test_admission_applicability_participation_and_emission_remain_distinct():
    ledger = EventLedger()
    representation = _representation(ledger)
    output = BytesIO()
    admission, applicability_event, standing, boundary = admit_representation(
        ledger, representation, output_stream=output
    )
    applicability = get_recorded_representation_emission_applicability(
        ledger, applicability_event.identity
    )

    emitted = emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability_event.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )

    emission = ledger.get(emitted["emitted_event_identity"])
    act_evidence = ledger.get(emission.material["responsible_act_evidence_identity"])
    assert output.getvalue() == b"applicable material"
    assert applicability["standing"] == "applicable"
    assert applicability["support_relation_standing"] == "admitted"
    assert applicability["representation_reference"]["representation_rule"] == (
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
    )
    assert applicability["destination_operator_boundary_rule"] == (
        EXACT_MATERIAL_WRITE_BOUNDARY_RULE
    )
    assert applicability["representation_rule_to_boundary_rule_relation"] == {
        "first_subject": EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
        "relation": "applicable_to",
        "second_subject": EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    }
    assert applicability["validation"] == {
        "exact_material_Admission": True,
        "exact_Representation_rule": True,
        "exact_destination_boundary_rule": True,
        "Representation_rule_applicable_to_destination_boundary_rule": True,
        "current_Admission_Standing": True,
        "same_Representation": True,
        "same_destination_operator_boundary": True,
        "same_destination_operator_Locality": True,
        "same_emission_Act_occurrence": True,
        "same_emission_result_boundary": True,
    }
    assert applicability["admission_result_event_identity"] == admission.identity
    assert applicability["addressed_act_occurrence_identity"] == (
        emission.material["act_occurrence_identity"]
    )
    assert act_evidence.material["input_applicability_event_identity"] == (
        applicability_event.identity
    )
    assert len(
        {
            admission.material["result_identity"],
            applicability["result_identity"],
            emission.material["result_identity"],
        }
    ) == 3


def test_emitter_refuses_applicability_absent_from_current_standing():
    ledger = EventLedger()
    representation = _representation(ledger)
    admission, applicability, _standing, boundary = admit_representation(
        ledger, representation
    )
    standing_before_applicability = read_operator_locality_standing_through(
        ledger,
        locality_identity="seed-locality",
        through_event_occurrence_identity=admission.identity,
    )

    with pytest.raises(ValueError, match="Applicability"):
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing_before_applicability,
            output_boundary=boundary,
        )


def test_applicability_refuses_a_destination_that_lost_write_capability():
    class ExpiringBoundary:
        def __init__(self):
            self.read_count = 0

        @property
        def write(self):
            self.read_count += 1
            if self.read_count < 3:
                return lambda material: len(material)
            return None

    ledger = EventLedger()
    representation = _representation(ledger)

    with pytest.raises(TypeError, match="writable boundary"):
        admit_representation(
            ledger,
            representation,
            output_stream=ExpiringBoundary(),
        )

    assert not tuple(
        ledger.iter_locality_kind(
            "seed-locality",
            "operator.representation.emission_applicability_act_evidenced",
        )
    )


def test_applicability_refuses_a_distinct_destination_boundary_rule():
    ledger = EventLedger()
    representation = _representation(ledger)
    admission, _applicability, _standing, boundary = admit_representation(
        ledger, representation
    )
    distinct_rule_boundary = operator_emission_boundary(
        BytesIO(),
        boundary_identity=boundary[1],
        locality_identity=boundary[2],
        boundary_rule="render terminal cells",
    )

    with pytest.raises(
        RepresentationApplicabilityError,
        match="exact admitted destination",
    ):
        record_representation_emission_applicability_act_evidence(
            ledger,
            admission_result_event_identity=admission.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity="seed-locality"
            ),
            destination_operator_boundary=distinct_rule_boundary,
        )


def test_applicability_for_another_admission_cannot_participate():
    ledger = EventLedger()
    first = _representation(ledger, b"first")
    first_admission, _first_applicability, _first_standing, first_boundary = (
        admit_representation(ledger, first)
    )
    second = _representation(ledger, b"second")
    _second_admission, second_applicability, second_standing, _second_boundary = (
        admit_representation(ledger, second)
    )

    with pytest.raises(ValueError, match="Applicability"):
        emit_operator_representation_material(
            ledger,
            representation=first,
            admission_result_event_identity=first_admission.identity,
            applicability_result_event_identity=second_applicability.identity,
            locality_standing=second_standing,
            output_boundary=first_boundary,
        )


def test_one_applicability_act_cannot_yield_twice():
    ledger = EventLedger()
    representation = _representation(ledger)
    _admission, applicability, _standing, _boundary = admit_representation(
        ledger, representation
    )

    with pytest.raises(
        RepresentationApplicabilityError, match="already carries a Yield"
    ):
        record_representation_emission_applicability_result(
            ledger,
            responsible_act_evidence_event_identity=applicability.material[
                "responsible_act_evidence_identity"
            ],
        )


def test_applicability_refuses_corrupted_yield_evidence():
    ledger = IntegrityAdversaryLedger()
    representation = _representation(ledger)
    _admission, applicability, _standing, _boundary = admit_representation(
        ledger, representation
    )
    ledger.mark_corrupted(
        applicability.material["evidence_of_yield_relation_identity"]
    )

    with pytest.raises(RepresentationApplicabilityError, match="exact Yield"):
        get_recorded_representation_emission_applicability(
            ledger, applicability.identity
        )


def test_applicability_standing_survives_durable_reopen(tmp_path):
    path = tmp_path / "representation-applicability.sqlite"
    ledger = SQLiteEventLedger(str(path))
    representation = _representation(ledger)
    _admission, applicability, standing, _boundary = admit_representation(
        ledger, representation
    )
    applicability_identity = applicability.identity
    assert standing["applicability_result_occurrences"] == {
        applicability_identity: None
    }
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        recorded = get_recorded_representation_emission_applicability(
            reopened, applicability_identity
        )
        replayed = read_operator_locality_standing(
            reopened, locality_identity="seed-locality"
        )
        assert recorded["standing"] == "applicable"
        assert replayed["applicability_result_occurrences"] == {
            applicability_identity: None
        }
    finally:
        reopened.close()
