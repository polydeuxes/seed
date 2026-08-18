from copy import deepcopy
import ast
import inspect

import pytest

import seed_runtime.measurement_of_source_position_coordinates_carrying_addressed_material as module
import seed_runtime.addressed_byte_occurrence_reference_determination as d2_module
import seed_runtime.measurement_of_shared_position_of_byte_pair_occurrences as shared_module
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.operator_locality_standing import (
    advance_operator_locality_standing,
    read_operator_locality_standing,
)
from seed_runtime.standing_measurement_declarations import (
    _record_declared_measurements_from_carried_standing,
    record_declared_measurements_from_current_standing,
)
from tests.test_addressed_byte_occurrence_reference_determination import (
    _direct,
    _record,
)


class AppendMutationLedger(EventLedger):
    mutate_kind = None

    def append(self, kind, material, **kwargs):
        event = super().append(kind, material, **kwargs)
        if kind == self.mutate_kind:
            self.mutate_kind = None
            event.material["unknown"].append("append callback mutation")
        return event


class YieldInterleaveLedger(EventLedger):
    inject_boundary = None

    def append(self, kind, material, **kwargs):
        event = super().append(kind, material, **kwargs)
        if (
            kind == module.RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND
            and material.get("occurrence_boundary") == self.inject_boundary
        ):
            self.inject_boundary = None
            super().append(
                "test.addressed_material.unrelated",
                {"unknown": ["interleaved after Yield Evidence"]},
                locality_identity=kwargs["locality_identity"],
            )
        return event


def _family_results(recorded):
    return tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == module.MEASUREMENT_RESULT_KIND
    )


def _advance(ledger, standing, event):
    return advance_operator_locality_standing(
        ledger,
        (event.identity,),
        locality_identity=standing["locality_identity"],
        prior=standing,
    )


def _public_lifecycle(ledger, standing, addressed_result):
    assignment = module.record_addressed_material_coordinate_measurement_responsibility_assignment(
        ledger,
        addressed_determination_result_event_identity=addressed_result.identity,
        locality_standing=standing,
    )
    standing = _advance(ledger, standing, assignment)
    applicability_act = module.record_addressed_material_coordinate_measurement_applicability_act_evidence(
        ledger,
        responsibility_assignment_event_identity=assignment.identity,
        responsibility_assignment_standing=standing,
    )
    standing = _advance(ledger, standing, applicability_act)
    applicability = module.record_addressed_material_coordinate_measurement_applicability_result(
        ledger,
        applicability_act_evidence_event_identity=applicability_act.identity,
    )
    standing = _advance(ledger, standing, applicability)
    act = module.record_addressed_material_coordinate_measurement_act_evidence(
        ledger,
        applicability_result_event_identity=applicability.identity,
        applicability_standing=standing,
    )
    standing = _advance(ledger, standing, act)
    result = module.record_addressed_material_coordinate_measurement_result(
        ledger, measurement_act_evidence_event_identity=act.identity
    )
    standing = _advance(ledger, standing, result)
    return standing, assignment, applicability_act, applicability, act, result


def test_dispatcher_derives_once_without_full_public_reference_population(monkeypatch):
    ledger = EventLedger()
    addressed = _record(ledger, exact=b"aba", position=0, locality="material-fanout")
    _direct(ledger, exact=b"cabaca", locality="material-fanout")
    calls = 0
    d2_reads = 0
    shared_reads = 0
    original = module._measured_coordinates
    original_d2_read = shared_module._read_determination_result
    original_shared_read = shared_module._read_measurement_result

    def record_measurement_call(*args, **kwargs):
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    def record_d2_read(*args, **kwargs):
        nonlocal d2_reads
        d2_reads += 1
        return original_d2_read(*args, **kwargs)

    def record_shared_read(*args, **kwargs):
        nonlocal shared_reads
        shared_reads += 1
        return original_shared_read(*args, **kwargs)

    monkeypatch.setattr(module, "_measured_coordinates", record_measurement_call)
    monkeypatch.setattr(shared_module, "_read_determination_result", record_d2_read)
    monkeypatch.setattr(shared_module, "_read_measurement_result", record_shared_read)
    # This removed API path is an explicit siren: the family must use the
    # direct result reader and targeted coordinate constructor.
    import seed_runtime.measurement_of_position_coordinates_of_byte_pair_occurrences as direct

    monkeypatch.setattr(
        direct,
        "references_to_recorded_position_coordinates_of_byte_pair_occurrences",
        lambda *_args, **_kwargs: pytest.fail("full reference population was decoded"),
    )
    recorded = record_declared_measurements_from_current_standing(
        ledger, locality_identity="material-fanout"
    )
    result, = _family_results(recorded)
    findings = result.material["ordered_source_position_coordinate_findings"]

    assert calls == 1
    assert d2_reads == 2
    assert shared_reads == 0
    assert [finding["source_position_coordinate_reference"]["position"] for finding in findings] == [0, 2, 1, 3, 5]
    assert len({finding["source_position_coordinate_reference"]["identity"] for finding in findings}) == 5
    assert all(finding["direct_pair_position_result_reference"] for finding in findings)
    assert all(finding["pair_position_assertion_reference"] for finding in findings)
    assert addressed["direct_result"].identity in {
        reference["recorded_occurrence_identity"]
        for reference in result.material["direct_pair_position_result_references"]
    }
    downstream_d2 = tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == d2_module.DETERMINATION_RESULT_KIND
    )
    downstream_shared = tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == shared_module.SHARED_POSITION_MEASUREMENT_RESULT_KIND
    )
    assert len(downstream_d2) == 4
    assert tuple(
        event.material["addressed_source_byte_position_coordinate_reference"][
            "position"
        ]
        for event in downstream_d2
    ) == (2, 1, 3, 5)
    assert tuple(
        len(event.material["ordered_assertion_references"])
        for event in downstream_d2
    ) == (1, 2, 2, 1)
    assert len(downstream_shared) == 2
    assert recorded.locality_standing == read_operator_locality_standing(
        ledger, locality_identity="material-fanout"
    )
    assert record_declared_measurements_from_current_standing(
        ledger, locality_identity="material-fanout"
    ).result_occurrences == ()
    d2_assignment = next(
        event
        for event in ledger.list()
        if event.kind == d2_module.RESPONSIBILITY_ASSIGNMENT_KIND
        and event.material["addressed_source_byte_position_coordinate_reference"]
        ["position"]
        == 2
    )
    d2_assignment.material.pop("direct_pair_position_result_reference")
    with pytest.raises(ValueError):
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="material-fanout"
        )


def test_first_malformed_candidate_refuses_without_skipping_or_changing_standing():
    ledger = EventLedger()
    addressed = _record(
        ledger, exact=b"aba", position=0, locality="candidate-refusal"
    )
    _direct(ledger, exact=b"cabaca", locality="candidate-refusal")
    standing = read_operator_locality_standing(
        ledger, locality_identity="candidate-refusal"
    )
    standing, _assignment, _app_act, _applicability, _act, result = (
        _public_lifecycle(ledger, standing, addressed["result"])
    )
    findings = result.material["ordered_source_position_coordinate_findings"]
    assert len(findings) > 1
    findings[0]["direct_pair_position_result_reference"].pop(
        "recorded_occurrence_identity"
    )
    before = deepcopy(standing)
    boundary = ledger.append_boundary()

    with pytest.raises(ValueError, match="malformed addressed-material finding"):
        _record_declared_measurements_from_carried_standing(
            ledger,
            standing,
            locality_identity="candidate-refusal",
        )

    assert standing == before
    assert ledger.append_boundary() == boundary
    assert not any(
        event.kind == d2_module.RESPONSIBILITY_ASSIGNMENT_KIND
        and event.material["addressed_source_byte_position_coordinate_reference"]
        ["position"]
        != 0
        for event in ledger.list()
    )


def test_discovery_uses_only_results_carried_by_its_exact_locality_standing():
    ledger = EventLedger()
    foreign = _record(ledger, exact=b"xyx", position=0, locality="foreign-fanout")
    _direct(ledger, exact=b"zxyxz", locality="foreign-fanout")
    local = _record(ledger, exact=b"aba", position=0, locality="local-fanout")
    _direct(ledger, exact=b"cabaca", locality="local-fanout")

    recorded = record_declared_measurements_from_current_standing(
        ledger, locality_identity="local-fanout"
    )
    local_sources = {
        event.material["direct_pair_position_result_reference"][
            "recorded_occurrence_identity"
        ]
        for event in recorded.result_occurrences
        if event.kind == d2_module.DETERMINATION_RESULT_KIND
    }
    assert local_sources
    assert foreign["direct_result"].identity not in local_sources
    assert local["direct_result"].identity in {
        reference["recorded_occurrence_identity"]
        for event in recorded.result_occurrences
        if event.kind == module.MEASUREMENT_RESULT_KIND
        for reference in event.material["direct_pair_position_result_references"]
    }


def test_declaration_adapters_are_value_neutral():
    import seed_runtime.standing_measurement_declarations as declarations

    functions = (
        declarations._discover_d2_from_addressed_material_coordinate,
        declarations._record_d2_from_addressed_material_coordinate,
        declarations._discover_shared_position_from_d2_result,
        declarations._record_shared_position_from_d2_result,
        d2_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing,
        shared_module._record_shared_position_measurement_lifecycle_from_carried_d2_result,
    )
    constants = tuple(
        node.value
        for function in functions
        for node in ast.walk(ast.parse(inspect.getsource(function)))
        if isinstance(node, ast.Constant)
    )
    assert b"=" not in constants
    assert "=" not in constants
    assert "0x3d" not in constants
    assert 4 not in constants
    sources = "\n".join(inspect.getsource(function) for function in functions)
    assert "result_content ==" not in sources
    assert '.get("result_content")' not in sources


def test_manual_same_subject_d2_is_not_given_declaration_trigger_provenance():
    import seed_runtime.standing_measurement_declarations as declarations

    ledger = EventLedger()
    addressed = _record(
        ledger, exact=b"aba", position=0, locality="origin-collision"
    )
    _direct(ledger, exact=b"cabaca", locality="origin-collision")
    standing = read_operator_locality_standing(
        ledger, locality_identity="origin-collision"
    )
    standing, _assignment, _app_act, _applicability, _act, material_result = (
        _public_lifecycle(ledger, standing, addressed["result"])
    )
    finding = next(
        item
        for item in material_result.material[
            "ordered_source_position_coordinate_findings"
        ]
        if item["source_position_coordinate_reference"]["position"] == 2
    )
    standing, manual_d2 = d2_module._record_addressed_byte_occurrence_reference_determination_lifecycle_from_carried_standing(
        ledger,
        direct_result_event_identity=finding[
            "direct_pair_position_result_reference"
        ]["recorded_occurrence_identity"],
        addressed_source_byte_position_coordinate_reference=finding[
            "source_position_coordinate_reference"
        ],
        locality_standing=standing,
    )
    assert not declarations._d2_subject_was_emitted_by_addressed_material(
        ledger,
        standing=standing,
        determination_result=manual_d2,
    )

    recorded = _record_declared_measurements_from_carried_standing(
        ledger,
        standing,
        locality_identity="origin-collision",
    )
    assert any(
        event.kind == module.MEASUREMENT_RESULT_KIND
        and event.material["addressed_determination_result_reference"]
        ["recorded_occurrence_identity"]
        == manual_d2.identity
        for event in recorded.result_occurrences
    )


def test_public_d2_read_refuses_unrelated_declaration_source_corruption():
    ledger = EventLedger()
    _record(ledger, exact=b"aba", position=0, locality="origin-corruption")
    _direct(ledger, exact=b"cabaca", locality="origin-corruption")
    record_declared_measurements_from_current_standing(
        ledger, locality_identity="origin-corruption"
    )
    assignment = next(
        event
        for event in ledger.list()
        if event.kind == d2_module.RESPONSIBILITY_ASSIGNMENT_KIND
        and d2_module.STANDING_DECLARATION_TRIGGER_COORDINATE in event.material
    )
    trigger_identity = assignment.material[
        d2_module.STANDING_DECLARATION_TRIGGER_COORDINATE
    ]["measurement_result_reference"]["recorded_occurrence_identity"]
    ledger.get(trigger_identity).material["unknown"].append(
        "unrelated declaration source corruption"
    )

    with pytest.raises(ValueError):
        d2_module.get_addressed_byte_occurrence_reference_determination_responsibility_assignment(
            ledger, assignment.identity
        )


def test_empty_result_is_lawful_and_completed_subject_does_not_rerun():
    ledger = EventLedger()
    _record(ledger, exact=b"a", position=0, locality="empty-fanout")
    recorded = record_declared_measurements_from_current_standing(
        ledger, locality_identity="empty-fanout"
    )
    result, = _family_results(recorded)
    assert result.material["ordered_source_position_coordinate_findings"] == []
    assert not tuple(
        event
        for event in recorded.result_occurrences
        if event.kind == shared_module.SHARED_POSITION_MEASUREMENT_RESULT_KIND
    )
    assert _family_results(
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="empty-fanout"
        )
    ) == ()


def test_changed_direct_result_set_is_a_new_bounded_subject_once():
    ledger = EventLedger()
    _record(ledger, exact=b"a", position=0, locality="set-fanout")
    first, = _family_results(
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="set-fanout"
        )
    )
    assert first.material["ordered_source_position_coordinate_findings"] == []
    _direct(ledger, exact=b"cad", locality="set-fanout")
    second, = _family_results(
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="set-fanout"
        )
    )
    assert len(second.material["ordered_source_position_coordinate_findings"]) == 1
    assert first.material["responsibility_assignment_reference"] != second.material[
        "responsibility_assignment_reference"
    ]
    assert _family_results(
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="set-fanout"
        )
    ) == ()


def test_public_lifecycle_and_restart_reconstruct_exact_result(tmp_path):
    path = tmp_path / "addressed-material.sqlite"
    ledger = SQLiteEventLedger(path)
    addressed = _record(ledger, exact=b"aba", position=0, locality="restart-fanout")
    _direct(ledger, exact=b"cad", locality="restart-fanout")
    standing = read_operator_locality_standing(ledger, locality_identity="restart-fanout")
    standing, assignment, applicability_act, applicability, act, result = _public_lifecycle(
        ledger, standing, addressed["result"]
    )
    dispatched = record_declared_measurements_from_current_standing(
        ledger, locality_identity="restart-fanout"
    )
    downstream_d2 = tuple(
        event
        for event in dispatched.result_occurrences
        if event.kind == d2_module.DETERMINATION_RESULT_KIND
    )
    downstream_shared = tuple(
        event
        for event in dispatched.result_occurrences
        if event.kind == shared_module.SHARED_POSITION_MEASUREMENT_RESULT_KIND
    )
    standing = dispatched.locality_standing
    expected = deepcopy(result.material)
    ledger.close()

    reopened = SQLiteEventLedger(path)
    assert module.get_addressed_material_coordinate_measurement_responsibility_assignment(
        reopened, assignment.identity
    ) == assignment.material
    assert module.get_addressed_material_coordinate_measurement_applicability_act_evidence(
        reopened, applicability_act.identity
    ) == applicability_act.material
    assert module.get_recorded_addressed_material_coordinate_measurement_applicability(
        reopened, applicability.identity
    ) == applicability.material
    assert module.get_addressed_material_coordinate_measurement_act_evidence(
        reopened, act.identity
    ) == act.material
    assert module.get_recorded_addressed_material_coordinate_measurement(
        reopened, result.identity
    ) == expected
    assert all(
        d2_module.get_recorded_addressed_byte_occurrence_reference_determination(
            reopened, event.identity
        )
        == event.material
        for event in downstream_d2
    )
    assert all(
        shared_module.get_recorded_shared_position_measurement(
            reopened, event.identity
        )
        for event in downstream_shared
    )
    assert read_operator_locality_standing(
        reopened, locality_identity="restart-fanout"
    ) == standing
    assert record_declared_measurements_from_current_standing(
        reopened, locality_identity="restart-fanout"
    ).result_occurrences == ()
    reopened.close()


def test_corrupted_assignment_refuses_carried_standing_atomically():
    ledger = EventLedger()
    addressed = _record(ledger, exact=b"aba", position=0, locality="atomic-fanout")
    standing = addressed["standing"]
    assignment = module.record_addressed_material_coordinate_measurement_responsibility_assignment(
        ledger,
        addressed_determination_result_event_identity=addressed["result"].identity,
        locality_standing=standing,
    )
    before = deepcopy(standing)
    assignment.material["unknown"].append("forged partial Standing")

    with pytest.raises(module.AddressedMaterialCoordinateMeasurementError):
        _advance(ledger, standing, assignment)
    assert standing == before


def test_source_mutation_during_derivation_refuses_without_lifecycle(monkeypatch):
    ledger = EventLedger()
    _record(ledger, exact=b"aba", position=0, locality="callback-fanout")
    _source, _direct_result_event, _standing = _direct(
        ledger, exact=b"cad", locality="callback-fanout"
    )
    original = module._direct_result
    mutated = False

    def mutate_after_read(*args, **kwargs):
        nonlocal mutated
        read = original(*args, **kwargs)
        if not mutated:
            mutated = True
            read[0].material["unknown"].append("callback mutation")
        return read

    monkeypatch.setattr(module, "_direct_result", mutate_after_read)
    before = read_operator_locality_standing(
        ledger, locality_identity="callback-fanout"
    )
    prior = deepcopy(before)
    with pytest.raises(
        module.AddressedMaterialCoordinateMeasurementError,
        match="changed during derivation|requires intact direct results",
    ):
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="callback-fanout"
        )
    assert not any(
        event.kind in {
            module.RESPONSIBILITY_ASSIGNMENT_KIND,
            module.APPLICABILITY_ACT_EVIDENCE_KIND,
            module.APPLICABILITY_RESULT_KIND,
            module.MEASUREMENT_ACT_EVIDENCE_KIND,
            module.MEASUREMENT_RESULT_KIND,
        }
        for event in ledger.list()
    )
    assert before == prior
    with pytest.raises(ValueError):
        read_operator_locality_standing(
            ledger, locality_identity="callback-fanout"
        )


def test_assignment_append_mutation_refuses_before_standing_carry():
    ledger = AppendMutationLedger()
    _record(ledger, exact=b"aba", position=0, locality="append-fanout")
    before = read_operator_locality_standing(ledger, locality_identity="append-fanout")
    prior = deepcopy(before)
    ledger.mutate_kind = module.RESPONSIBILITY_ASSIGNMENT_KIND

    with pytest.raises(
        module.AddressedMaterialCoordinateMeasurementError,
        match="changed while it was recorded",
    ):
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="append-fanout"
        )
    assert before == prior
    with pytest.raises(module.AddressedMaterialCoordinateMeasurementError):
        read_operator_locality_standing(
            ledger, locality_identity="append-fanout"
        )
    assert not any(
        event.kind in {
            module.APPLICABILITY_ACT_EVIDENCE_KIND,
            module.APPLICABILITY_RESULT_KIND,
            module.MEASUREMENT_ACT_EVIDENCE_KIND,
            module.MEASUREMENT_RESULT_KIND,
        }
        for event in ledger.list()
    )


def test_discovery_refuses_malformed_carried_address_without_key_error():
    ledger = EventLedger()
    addressed = _record(ledger, exact=b"aba", position=0, locality="shape-fanout")
    addressed["result"].material["direct_pair_position_result_reference"] = {}

    with pytest.raises(
        ValueError,
        match="direct source|inexact addressed|determination result coordinates",
    ):
        record_declared_measurements_from_current_standing(
            ledger, locality_identity="shape-fanout"
        )


@pytest.mark.parametrize(
    ("boundary", "forbidden_kind"),
    (
        (module.APPLICABILITY_BOUNDARY, module.APPLICABILITY_RESULT_KIND),
        (module.MEASUREMENT_BOUNDARY, module.MEASUREMENT_RESULT_KIND),
    ),
)
def test_yield_interleave_refuses_result_and_preserves_supplied_standing(
    boundary, forbidden_kind
):
    ledger = YieldInterleaveLedger()
    _record(ledger, exact=b"aba", position=0, locality="yield-callback-fanout")
    supplied = read_operator_locality_standing(
        ledger, locality_identity="yield-callback-fanout"
    )
    before = deepcopy(supplied)
    ledger.inject_boundary = boundary

    with pytest.raises(
        module.AddressedMaterialCoordinateMeasurementError,
        match="Yield Evidence at the append tip",
    ):
        module._record_addressed_material_coordinate_measurement_lifecycle_from_carried_standing(
            ledger,
            addressed_determination_result_event_identity=next(
                identity
                for identity in supplied["measurement_occurrences"]
                if ledger.get(identity).kind
                == module.ADDRESSED_REFERENCE_RESULT_KIND
            ),
            locality_standing=supplied,
        )
    assert supplied == before
    assert not any(event.kind == forbidden_kind for event in ledger.list())


FIDELITY_SUBJECTS = {
    "source_position_coordinates_carrying_addressed_material_measurement": (
        test_dispatcher_derives_once_without_full_public_reference_population,
        test_first_malformed_candidate_refuses_without_skipping_or_changing_standing,
        test_discovery_uses_only_results_carried_by_its_exact_locality_standing,
        test_declaration_adapters_are_value_neutral,
        test_manual_same_subject_d2_is_not_given_declaration_trigger_provenance,
        test_public_d2_read_refuses_unrelated_declaration_source_corruption,
        test_empty_result_is_lawful_and_completed_subject_does_not_rerun,
        test_changed_direct_result_set_is_a_new_bounded_subject_once,
        test_public_lifecycle_and_restart_reconstruct_exact_result,
        test_corrupted_assignment_refuses_carried_standing_atomically,
        test_source_mutation_during_derivation_refuses_without_lifecycle,
        test_assignment_append_mutation_refuses_before_standing_carry,
        test_discovery_refuses_malformed_carried_address_without_key_error,
        test_yield_interleave_refuses_result_and_preserves_supplied_standing,
    )
}
