from io import BytesIO

import pytest


from seed_runtime.events import CORRUPTED, EventLedger, SQLiteEventLedger
from seed_runtime.witness_material_acquisition import record_witness_material_acquisition
from seed_runtime.operator_egress import (
    EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    operator_emission_boundary,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from seed_runtime.operator_representation import (
    EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE,
    emit_operator_representation_material,
    record_operator_representation,
)
from seed_runtime.operator_representation_admission import (
    RepresentationAdmissionError,
    get_recorded_exact_material_representation_admission,
    get_recorded_representation_candidate,
    record_representation_candidate_responsibility_assignment,
    record_representation_candidate_act_evidence,
    record_representation_candidate_result,
    record_exact_material_representation_admission_responsibility_assignment,
    record_exact_material_representation_admission_act_evidence,
    record_exact_material_representation_admission_result,
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


def _exact_representation(ledger, exact=b"hello"):
    source = record_witness_material_acquisition(
        ledger,
        locality_identity="seed-locality",
        exact_bytes=exact,
        source_boundary="fixture boundary",
    )
    return record_operator_representation(
        ledger,
        locality_identity="seed-locality",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="seed-locality"
        ),
        source_occurrence_reference=source.identity,
    )


def test_candidate_admission_and_emission_remain_three_distinct_results():
    ledger = EventLedger()
    representation = _exact_representation(ledger)
    output = BytesIO()
    admission_event, applicability, standing, boundary = admit_representation(
        ledger, representation, output_stream=output
    )
    admission = get_recorded_exact_material_representation_admission(
        ledger, admission_event.identity
    )
    candidate = get_recorded_representation_candidate(
        ledger, admission["candidate_reference"]["recorded_occurrence_identity"]
    )
    emitted = emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission_event.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )

    emission = ledger.get(emitted["emitted_event_identity"])
    assert output.getvalue() == b"hello"
    assert candidate["standing"] == "candidate"
    assert candidate["representation_source_standing_boundary_identity"] != (
        candidate["assignment_standing_boundary_identity"]
    )
    assert candidate["assignment_standing_boundary_identity"] == (
        representation["representation_event_identity"]
    )
    assert admission["standing"] == "admitted"
    assert candidate["destination_operator_boundary_rule"] == (
        EXACT_MATERIAL_WRITE_BOUNDARY_RULE
    )
    assert admission["destination_operator_boundary_rule"] == (
        EXACT_MATERIAL_WRITE_BOUNDARY_RULE
    )
    assert admission["representation_rule_to_boundary_rule_relation"] == {
        "first_subject": representation["representation_rule"],
        "relation": "applicable_to",
        "second_subject": EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    }
    assert emission.material["result_identity"] == admission[
        "emission_result_boundary_identity"
    ]
    assert len(
        {
            candidate["result_identity"],
            admission["result_identity"],
            emission.material["result_identity"],
        }
    ) == 3
    assert standing["candidate_result_occurrences"] == {
        admission["candidate_reference"]["recorded_occurrence_identity"]: None
    }
    assert standing["admission_result_occurrences"] == {
        admission_event.identity: None
    }


def test_exact_material_emission_does_not_promote_statement_to_seed_truth():
    ledger = EventLedger()
    statement_material = b"2+2=5"
    source = record_witness_material_acquisition(
        ledger,
        locality_identity="seed-locality",
        exact_bytes=statement_material,
        source_boundary="supplied statement occurrence",
    )
    representation = record_operator_representation(
        ledger,
        locality_identity="seed-locality",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="seed-locality"
        ),
        source_occurrence_reference=source.identity,
    )
    output = BytesIO()
    admission, applicability, standing, boundary = admit_representation(
        ledger,
        representation,
        boundary_identity="statement-material-boundary",
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

    emission = ledger.get(emitted["emitted_event_identity"])
    assert output.getvalue() == statement_material
    assert source.material["unknown"] == [
        "represented_relation",
        "source_relation",
    ]
    assert representation["representation_rule"] == (
        EXACT_SOURCE_MATERIAL_REPRESENTATION_RULE
    )
    assert emission.exact_material == statement_material
    assert emission.material["destination_operator_boundary_identity"] == (
        "statement-material-boundary"
    )
    assert "represented_relation" not in representation
    assert "source_relation" not in representation
    assert "truth" not in representation
    assert "represented_relation" not in emission.material
    assert "source_relation" not in emission.material
    assert "truth" not in emission.material


def test_admission_refuses_an_undeclared_representation_and_boundary_rule_pair():
    ledger = EventLedger()
    representation = _exact_representation(ledger)

    with pytest.raises(
        RepresentationAdmissionError,
        match="applicable Representation and destination boundary rule pair",
    ):
        admit_representation(
            ledger,
            representation,
            boundary_rule="render terminal cells",
        )
    assert not read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )["admission_result_occurrences"]


def test_admission_to_one_operator_locality_does_not_admit_another():
    ledger = EventLedger()
    first = _exact_representation(ledger)
    first_admission, first_applicability, first_standing, first_boundary = admit_representation(
        ledger,
        first,
        boundary_identity="first-boundary",
        operator_locality_identity="first-locality",
    )
    second = _exact_representation(ledger, b"hello again")
    second_admission, _second_applicability, second_standing, _second_boundary = admit_representation(
        ledger,
        second,
        boundary_identity="second-boundary",
        operator_locality_identity="second-locality",
    )

    with pytest.raises(ValueError, match="another Representation"):
        emit_operator_representation_material(
            ledger,
            representation=second,
            admission_result_event_identity=first_admission.identity,
            applicability_result_event_identity=first_applicability.identity,
            locality_standing=first_standing,
            output_boundary=first_boundary,
        )

    first_material = get_recorded_exact_material_representation_admission(
        ledger, first_admission.identity
    )
    second_material = get_recorded_exact_material_representation_admission(
        ledger, second_admission.identity
    )
    assert first_material["destination_operator_locality_identity"] != (
        second_material["destination_operator_locality_identity"]
    )
    assert second_admission.identity in second_standing[
        "admission_result_occurrences"
    ]


def test_admission_refuses_a_different_invoked_operator_boundary():
    ledger = EventLedger()
    representation = _exact_representation(ledger)
    admission, applicability, standing, _admitted_boundary = admit_representation(
        ledger,
        representation,
        boundary_identity="first-boundary",
        operator_locality_identity="first-locality",
    )
    other_boundary = operator_emission_boundary(
        BytesIO(),
        boundary_identity="other-boundary",
        locality_identity="other-locality",
        boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
    )

    with pytest.raises(ValueError, match="Admission, Applicability, and destination"):
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=standing,
            output_boundary=other_boundary,
        )


def test_emission_refuses_admission_not_carried_by_current_standing():
    ledger = EventLedger()
    representation = _exact_representation(ledger)
    before_admission = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    admission, applicability, _, boundary = admit_representation(ledger, representation)

    with pytest.raises(ValueError, match="carried Admission"):
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=before_admission,
            output_boundary=boundary,
        )


def test_one_admission_participates_in_only_one_emission_attempt():
    ledger = EventLedger()
    representation = _exact_representation(ledger)
    admission, applicability, standing, boundary = admit_representation(ledger, representation)
    emit_operator_representation_material(
        ledger,
        representation=representation,
        admission_result_event_identity=admission.identity,
        applicability_result_event_identity=applicability.identity,
        locality_standing=standing,
        output_boundary=boundary,
    )

    with pytest.raises(ValueError, match="already participated"):
        emit_operator_representation_material(
            ledger,
            representation=representation,
            admission_result_event_identity=admission.identity,
            applicability_result_event_identity=applicability.identity,
            locality_standing=read_operator_locality_standing(
                ledger, locality_identity="seed-locality"
            ),
            output_boundary=boundary,
        )


def test_structured_representation_may_be_candidate_but_raw_admission_refuses():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="seed-locality",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="seed-locality"
        ),
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    assignment = record_representation_candidate_responsibility_assignment(
        ledger,
        representation_event_identity=representation[
            "representation_event_identity"
        ],
        locality_standing=standing,
        destination_operator_boundary=operator_emission_boundary(
            BytesIO(),
            boundary_identity="raw-boundary",
            locality_identity="raw-locality",
            boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
        ),
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    candidate_act = record_representation_candidate_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=standing,
    )
    candidate = record_representation_candidate_result(
        ledger, responsible_act_evidence_event_identity=candidate_act.identity
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    admission_assignment = (
        record_exact_material_representation_admission_responsibility_assignment(
            ledger,
            candidate_result_event_identity=candidate.identity,
            locality_standing=standing,
        )
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    admission_act = record_exact_material_representation_admission_act_evidence(
        ledger,
        assignment_event_identity=admission_assignment.identity,
        locality_standing=standing,
    )

    with pytest.raises(RepresentationAdmissionError, match="without exact material"):
        record_exact_material_representation_admission_result(
            ledger,
            responsible_act_evidence_event_identity=admission_act.identity,
        )
    assert not read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )["admission_result_occurrences"]


def test_one_candidate_or_admission_act_cannot_yield_twice():
    ledger = EventLedger()
    representation = _exact_representation(ledger)
    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    assignment = record_representation_candidate_responsibility_assignment(
        ledger,
        representation_event_identity=representation[
            "representation_event_identity"
        ],
        locality_standing=standing,
        destination_operator_boundary=operator_emission_boundary(
            BytesIO(),
            boundary_identity="raw-boundary",
            locality_identity="raw-locality",
            boundary_rule=EXACT_MATERIAL_WRITE_BOUNDARY_RULE,
        ),
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    act = record_representation_candidate_act_evidence(
        ledger,
        assignment_event_identity=assignment.identity,
        locality_standing=standing,
    )
    candidate = record_representation_candidate_result(
        ledger, responsible_act_evidence_event_identity=act.identity
    )
    with pytest.raises(RepresentationAdmissionError, match="already carries a Yield"):
        record_representation_candidate_result(
            ledger, responsible_act_evidence_event_identity=act.identity
        )

    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    admission_assignment = (
        record_exact_material_representation_admission_responsibility_assignment(
            ledger,
            candidate_result_event_identity=candidate.identity,
            locality_standing=standing,
        )
    )
    standing = read_operator_locality_standing(
        ledger, locality_identity="seed-locality"
    )
    admission_act = record_exact_material_representation_admission_act_evidence(
        ledger,
        assignment_event_identity=admission_assignment.identity,
        locality_standing=standing,
    )
    record_exact_material_representation_admission_result(
        ledger, responsible_act_evidence_event_identity=admission_act.identity
    )
    with pytest.raises(RepresentationAdmissionError, match="already carries a Yield"):
        record_exact_material_representation_admission_result(
            ledger,
            responsible_act_evidence_event_identity=admission_act.identity,
        )


@pytest.mark.parametrize("result_family", ("candidate", "admission"))
def test_candidate_and_admission_refuse_corrupted_yield_evidence(result_family):
    ledger = IntegrityAdversaryLedger()
    representation = _exact_representation(ledger)
    admission, _applicability, _standing, _boundary = admit_representation(ledger, representation)
    candidate = ledger.get(
        admission.material["candidate_reference"]["recorded_occurrence_identity"]
    )
    if result_family == "candidate":
        result = candidate
        reader = get_recorded_representation_candidate
    else:
        result = admission
        reader = get_recorded_exact_material_representation_admission

    ledger.mark_corrupted(result.material["evidence_of_yield_relation_identity"])
    with pytest.raises(RepresentationAdmissionError, match="exact Yield"):
        reader(ledger, result.identity)


def test_candidate_admission_standing_survives_durable_reopen(tmp_path):
    path = tmp_path / "representation-admission.sqlite"
    ledger = SQLiteEventLedger(str(path))
    representation = _exact_representation(ledger)
    admission, applicability, standing, _boundary = admit_representation(ledger, representation)
    admission_identity = admission.identity
    expected_candidate = dict(standing["candidate_result_occurrences"])
    ledger.close()

    reopened = SQLiteEventLedger(str(path))
    try:
        recorded = get_recorded_exact_material_representation_admission(
            reopened, admission_identity
        )
        replayed = read_operator_locality_standing(
            reopened, locality_identity="seed-locality"
        )
        assert recorded["standing"] == "admitted"
        assert replayed["candidate_result_occurrences"] == expected_candidate
        assert replayed["admission_result_occurrences"] == {
            admission_identity: None
        }
    finally:
        reopened.close()
