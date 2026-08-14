"""Literal Compare over exact positional result Assertion yields."""

from dataclasses import replace
from io import StringIO

import pytest

from seed_runtime.adjacent_pair_measurement import (
    AdjacentPair,
    assertion_of_recorded_adjacent_pair_result,
    measure_adjacent_pair,
    measure_after,
    record_pair_measurements,
)
from seed_runtime.assertion_comparison import (
    POSITIONAL_RESULT_COORDINATES,
    POSITIONAL_RESULT_COMPARISON_RECORDED_KIND,
    POSITIONAL_RESULT_COMPARISON_AUTHORITY,
    POSITIONAL_RESULT_COMPARISON_FORBIDDEN_INFERENCES,
    POSITIONAL_RESULT_COMPARISON_PROVENANCE,
    POSITIONAL_RESULT_COMPARISON_UNKNOWNS,
    AssertionComparisonError,
    _positional_result_distinction_identity,
    assertions_of_recorded_positional_result_comparison,
    compare_positional_result_assertions,
    get_recorded_positional_result_distinction,
    iter_positional_result_comparison_inputs,
    record_positional_result_comparison,
    record_positional_result_comparison_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.preserved_material_measurement import (
    preserved_ingress_occurrences,
    record_measurement_finding,
)


def _record_following(ledger, session_id, material, pair=AdjacentPair("it", "is")):
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id=session_id,
        input_stream=StringIO(material + "exit\n"),
        output_stream=StringIO(),
    )
    occurrences = preserved_ingress_occurrences(
        ledger, workspace_id="w", session_id=session_id
    )
    premise = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id=session_id,
        finding=measure_after(
            occurrences,
            pair.left,
            counting_scope=f"recorded exchange {session_id}",
        ),
    )
    event = record_pair_measurements(
        ledger,
        workspace_id="w",
        session_id=session_id,
        pair=pair,
        findings=measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope=f"recorded exchange {session_id}",
            premise_event_id=premise.id,
        ),
        completeness_boundary=ledger.capture_boundary(),
    )["following"]
    return assertion_of_recorded_adjacent_pair_result(event)


@pytest.fixture
def comparable():
    ledger = EventLedger()
    left = _record_following(ledger, "s1", "it is red\n")
    right = _record_following(ledger, "s2", "it is blue\n")
    return ledger, left, right


def test_same_exact_subject_supplies_a_bounded_compare(comparable):
    ledger, left, right = comparable
    before = tuple(event.id for event in ledger.list("w"))

    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    distinctions = {item.coordinate: item for item in comparison.distinctions}

    assert comparison.act == "Compare"
    assert comparison.responsible_boundary == "this bounded comparison occurrence"
    assert comparison.subject == left.payload["assertion_subject"]
    assert set(distinctions) == set(POSITIONAL_RESULT_COORDINATES)
    assert distinctions["positions_measured"].same is True
    assert distinctions["occupancies"].same is False
    assert distinctions["occupancies"].present == (True, True)
    assert distinctions["scope"].same is False
    assert distinctions["standing"].same is True
    assert tuple(event.id for event in ledger.list("w")) == before


def test_compare_preserves_exact_occurrence_bound_inputs(comparable):
    ledger, left, right = comparable
    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )

    assert [item.assertion_id for item in comparison.inputs] == [
        left.assertion_id,
        right.assertion_id,
    ]
    assert [item.yielding_event_id for item in comparison.inputs] == [
        left.yielding_event_id,
        right.yielding_event_id,
    ]


@pytest.mark.parametrize(
    ("coordinate", "field"),
    (
        ("source_provenance", "source_provenance"),
        ("responsibility", "responsibility"),
        ("authority", "authority"),
    ),
)
def test_compare_does_not_erase_established_fidelity_coordinates(
    comparable, coordinate, field
):
    ledger, left, right = comparable
    right.payload["dimensions"][field] = f"different {field}"

    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    distinction = {
        item.coordinate: item for item in comparison.distinctions
    }[coordinate]

    assert distinction.present == (True, True)
    assert distinction.same is False
    assert distinction.values[0] != distinction.values[1]


def test_compare_refuses_different_carried_subjects(comparable):
    ledger, left, _ = comparable
    other = _record_following(
        ledger, "s3", "it may change\n", pair=AdjacentPair("it", "may")
    )

    with pytest.raises(AssertionComparisonError, match="one exact carried"):
        compare_positional_result_assertions(
            ledger, (left.reference, other.reference)
        )


@pytest.mark.parametrize("references", [(), ({"yielding_event_id": "x", "assertion_id": "y"},)])
def test_compare_requires_exactly_two_inputs(comparable, references):
    ledger, _, _ = comparable
    with pytest.raises(AssertionComparisonError, match="exactly two"):
        compare_positional_result_assertions(ledger, references)


def test_compare_refuses_one_yield_twice(comparable):
    ledger, left, _ = comparable
    with pytest.raises(AssertionComparisonError, match="cannot be compared with itself"):
        compare_positional_result_assertions(
            ledger, (left.reference, left.reference)
        )


def test_compare_does_not_assertion_relation_recurrence_or_meaning(comparable):
    ledger, left, right = comparable
    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    represented = str(comparison).lower()

    assert "relation=" not in represented
    assert "recurrence=" not in represented
    assert "represented relation=" not in represented
    assert "similarity=" not in represented


def test_every_equal_subject_yield_pair_is_formed_without_comparing(comparable):
    ledger, left, right = comparable
    boundary = ledger.capture_boundary()
    before = tuple(event.id for event in ledger.list("w"))
    formed = list(
        iter_positional_result_comparison_inputs(
            ledger,
            workspace_id="w",
            session_ids=("s1", "s2"),
            through=boundary,
        )
    )

    assert len(formed) == 4  # one pair for each of the four exact form subjects
    assert (left.reference, right.reference) in formed
    assert tuple(event.id for event in ledger.list("w")) == before


def test_representation_act_boundary_excludes_later_yields(comparable):
    ledger, _, _ = comparable
    boundary = ledger.capture_boundary()
    _record_following(ledger, "s3", "it is green\n")

    bounded = list(
        iter_positional_result_comparison_inputs(
            ledger,
            workspace_id="w",
            session_ids=("s1", "s2", "s3"),
            through=boundary,
        )
    )
    current = list(
        iter_positional_result_comparison_inputs(
            ledger,
            workspace_id="w",
            session_ids=("s1", "s2", "s3"),
            through=ledger.capture_boundary(),
        )
    )

    assert len(bounded) == 4
    assert len(current) == 12


def test_representation_act_does_not_filter_different_result_content(comparable):
    ledger, left, right = comparable
    formed = list(
        iter_positional_result_comparison_inputs(
            ledger,
            workspace_id="w",
            session_ids=("s1", "s2"),
            through=ledger.capture_boundary(),
        )
    )

    assert left.payload["dimensions"]["content"] != right.payload["dimensions"][
        "content"
    ]
    assert (left.reference, right.reference) in formed


def test_representation_act_validates_each_session_boundary_once(comparable):
    ledger, _, _ = comparable
    original = ledger.iter_session_kind
    ingress_reads = []

    def tracked(workspace_id, session_id, kind, **kwargs):
        if kind == "operator.ingress.ingress_occurred":
            ingress_reads.append((session_id, kwargs.get("through")))
        return original(workspace_id, session_id, kind, **kwargs)

    ledger.iter_session_kind = tracked
    list(
        iter_positional_result_comparison_inputs(
            ledger,
            workspace_id="w",
            session_ids=("s1", "s2"),
            through=ledger.capture_boundary(),
        )
    )

    assert [session_id for session_id, _ in ingress_reads] == ["s1", "s2"]


def test_validated_representation_act_retains_only_occurrence_bound_references(comparable):
    import seed_runtime.assertion_comparison as module

    ledger, _, _ = comparable
    grouped = module._positional_result_assertions_by_subject(
        ledger,
        workspace_id="w",
        session_ids=("s1", "s2"),
        through=ledger.capture_boundary(),
    )

    assert grouped
    assert all(
        set(reference) == {"yielding_event_id", "assertion_id"}
        for references in grouped.values()
        for reference in references
    )
    assert not any(
        "payload" in reference
        for references in grouped.values()
        for reference in references
    )


def test_one_layer_records_every_formed_comparison_and_nothing_more(comparable):
    ledger, _, _ = comparable
    before = {event.id for event in ledger.list("w")}

    recorded_count = record_positional_result_comparison_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("s1", "s2"),
        recording_session_id="comparison-session",
    )
    recorded = [event for event in ledger.list("w") if event.id not in before]

    assert recorded_count == 4
    assert len(recorded) == 4
    assert all(
        event.kind == POSITIONAL_RESULT_COMPARISON_RECORDED_KIND
        for event in recorded
    )
    assert all(len(event.payload["assertions"]) == len(POSITIONAL_RESULT_COORDINATES) for event in recorded)
    for event in recorded:
        results = assertions_of_recorded_positional_result_comparison(event)
        assert get_recorded_positional_result_distinction(
            ledger,
            yielding_event_id=event.id,
            assertion_id=results[0].assertion_id,
        ) == results[0]


def test_one_layer_batches_storage_without_batching_compare_occurrences(comparable):
    ledger, _, _ = comparable
    original = ledger.append_many
    batches = []

    def tracked(events, **kwargs):
        supplied = list(events)
        batches.append(len(supplied))
        return original(supplied, **kwargs)

    ledger.append_many = tracked
    recorded_count = record_positional_result_comparison_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("s1", "s2"),
        recording_session_id="comparison-session",
    )

    assert recorded_count == 4
    assert batches == [4]
    assert len(
        [
            event
            for event in ledger.list("w")
            if event.kind == POSITIONAL_RESULT_COMPARISON_RECORDED_KIND
        ]
    ) == 4


def test_one_layer_boundary_excludes_results_made_available_during_the_run(
    comparable, monkeypatch
):
    import seed_runtime.assertion_comparison as module

    ledger, _, _ = comparable
    original = module._positional_result_assertions_by_subject

    def inject_later_result(*args, **kwargs):
        _record_following(ledger, "s1", "it is green\n")
        return original(*args, **kwargs)

    monkeypatch.setattr(module, "_positional_result_assertions_by_subject", inject_later_result)
    recorded_count = record_positional_result_comparison_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("s1", "s2"),
        recording_session_id="comparison-session",
    )

    assert recorded_count == 4


def test_one_layer_refuses_an_absent_declared_session(comparable):
    ledger, _, _ = comparable
    before = tuple(event.id for event in ledger.list("w"))

    with pytest.raises(AssertionComparisonError, match="absent through"):
        record_positional_result_comparison_layer(
            ledger,
            workspace_id="w",
            source_session_ids=("s1", "absent"),
            recording_session_id="comparison-session",
        )

    assert tuple(event.id for event in ledger.list("w")) == before


def test_recording_preserves_one_assertion_per_compare_coordinate(comparable):
    ledger, left, right = comparable
    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    before = len(ledger.list("w"))
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=comparison,
    )

    assert event.kind == POSITIONAL_RESULT_COMPARISON_RECORDED_KIND
    assert len(ledger.list("w")) == before + 1
    assert len(event.payload["assertions"]) == len(POSITIONAL_RESULT_COORDINATES)
    assert "distinctions" not in event.payload
    assert "relation" not in event.payload
    assert "recurrence" not in event.payload
    assert event.payload["inputs"] == [left.reference, right.reference]


def test_recorded_compare_results_are_occurrence_addressable(comparable):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )
    reconstructed = assertions_of_recorded_positional_result_comparison(event)

    assert {item.coordinate for item in reconstructed} == set(
        POSITIONAL_RESULT_COORDINATES
    )
    for item in reconstructed:
        assert item.reference == {
            "yielding_event_id": event.id,
            "assertion_id": item.assertion_id,
        }
        assert item.payload["support_basis"]["assertion_refs"] == [
            left.reference,
            right.reference,
        ]
        assert get_recorded_positional_result_distinction(
            ledger,
            yielding_event_id=event.id,
            assertion_id=item.assertion_id,
        ) == item


@pytest.mark.parametrize(
    ("field", "replacement"),
    (
        ("standing", "established"),
        ("source_provenance", "another provenance"),
        ("responsibility", "revise an input Assertion"),
        ("authority", "establishes relation"),
    ),
)
def test_validation_refuses_changed_result_assertion_dimensions(
    comparable, field, replacement
):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    ).model_copy(deep=True)
    event.payload["assertions"][0]["dimensions"][field] = replacement

    with pytest.raises(AssertionComparisonError, match="incoherent"):
        assertions_of_recorded_positional_result_comparison(event)


@pytest.mark.parametrize(
    ("field", "replacement"),
    (
        ("responsible_boundary", "an input Assertion"),
        ("unknowns", ["nothing remains Unknown"]),
        ("forbidden_inferences", []),
    ),
)
def test_validation_refuses_changed_result_assertion_fidelity_shell(
    comparable, field, replacement
):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    ).model_copy(deep=True)
    event.payload["assertions"][0][field] = replacement

    with pytest.raises(AssertionComparisonError, match="incoherent"):
        assertions_of_recorded_positional_result_comparison(event)


def test_recorded_result_assertion_shell_is_exactly_bounded(comparable):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )
    assertion = event.payload["assertions"][0]

    assert assertion["dimensions"]["standing"] == "compared"
    assert (
        assertion["dimensions"]["source_provenance"]
        == POSITIONAL_RESULT_COMPARISON_PROVENANCE
    )
    assert (
        assertion["dimensions"]["authority"]
        == POSITIONAL_RESULT_COMPARISON_AUTHORITY
    )
    assert assertion["unknowns"] == list(POSITIONAL_RESULT_COMPARISON_UNKNOWNS)
    assert assertion["forbidden_inferences"] == list(
        POSITIONAL_RESULT_COMPARISON_FORBIDDEN_INFERENCES
    )


def test_recording_recomputes_compare_from_occurrence_bound_inputs(comparable):
    ledger, left, right = comparable
    comparison = compare_positional_result_assertions(
        ledger, (left.reference, right.reference)
    )
    altered = replace(
        comparison,
        distinctions=(
            replace(comparison.distinctions[0], same=not comparison.distinctions[0].same),
            *comparison.distinctions[1:],
        ),
    )

    with pytest.raises(AssertionComparisonError, match="does not match its inputs"):
        record_positional_result_comparison(
            ledger,
            workspace_id="w",
            session_id="comparison-session",
            comparison=altered,
        )


def test_validation_refuses_a_self_consistent_forged_compare_result(comparable):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    ).model_copy(deep=True)
    assertion = next(
        item
        for item in event.payload["assertions"]
        if item["dimensions"]["content"]["coordinate"] == "standing"
    )
    content = assertion["dimensions"]["content"]
    content["same"] = False
    assertion["dimensions"]["identity"] = _positional_result_distinction_identity(
        subject=event.payload["compared_subject"],
        inputs=event.payload["inputs"],
        workspace_id=event.workspace_id,
        session_id=event.session_id,
        **content,
    )

    with pytest.raises(AssertionComparisonError, match="unlawful"):
        assertions_of_recorded_positional_result_comparison(event)


def test_ledger_validation_refuses_self_consistent_results_for_other_inputs(comparable):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )
    reconstructed = assertions_of_recorded_positional_result_comparison(event)
    event.payload["compared_subject"] = {
        **event.payload["compared_subject"],
        "measurement_form": "preceding",
    }
    for assertion in event.payload["assertions"]:
        assertion["assertion_subject"]["compared_subject"] = event.payload[
            "compared_subject"
        ]
        content = assertion["dimensions"]["content"]
        assertion["dimensions"]["identity"] = (
            _positional_result_distinction_identity(
                subject=event.payload["compared_subject"],
                inputs=event.payload["inputs"],
                workspace_id=event.workspace_id,
                session_id=event.session_id,
                **content,
            )
        )

    with pytest.raises(AssertionComparisonError, match="replayed Act"):
        get_recorded_positional_result_distinction(
            ledger,
            yielding_event_id=event.id,
            assertion_id=reconstructed[0].assertion_id,
        )


@pytest.mark.parametrize(
    ("field", "replacement"),
    (
        ("yielding_act", "Measure"),
        ("responsible_boundary", "an input Assertion"),
        ("responsibility", "revise the compared Assertions"),
    ),
)
def test_ledger_validation_refuses_changed_outer_compare_law(
    comparable, field, replacement
):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )
    reconstructed = assertions_of_recorded_positional_result_comparison(event)
    event.payload[field] = replacement

    with pytest.raises(AssertionComparisonError, match="replayed Act"):
        get_recorded_positional_result_distinction(
            ledger,
            yielding_event_id=event.id,
            assertion_id=reconstructed[0].assertion_id,
        )


def test_recorded_compare_does_not_perform_automatic_reliance(comparable):
    ledger, left, right = comparable
    event = record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparison-session",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )

    assert all(
        "input support" in assertion["forbidden_inferences"][-1]
        for assertion in event.payload["assertions"]
    )
    assert all("applicability" not in assertion for assertion in event.payload["assertions"])
