"""Recurrence across bounded localities, measured over Seed's own occurrences.

`#2429` built this and called it a "cohort measurement", writing a Responsibility
into every record that nothing established. `#2351` read declared
measurement and said no new act, noun, or grammar is required; recurrence and
count are already its findings. What different here is the subject, not the Act.

These tests pin the three corrections as carefully as the count: the whole
declared identity governs grouping, every occurrence the result stood on
travels with it, and the counting scope says exactly what was input.
"""

from __future__ import annotations

from dataclasses import replace
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.adjacency_pair_measurement import measure_after
from seed_runtime.assertion_comparison import (
    ASSERTION_YIELD_COMPARISON_RECORDED_KIND,
    AssertionComparisonError,
    _distinction_assertion_identity,
    assertions_of_recorded_assertion_comparison,
    compare_assertion_yields,
    record_assertion_yield_comparison,
)
from seed_runtime.bounded_assertion_comparison import (
    compare_preserved_findings,
    record_comparison_finding,
)
from seed_runtime.events import EventLedger
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    ingest_occurrences,
    record_measurement_finding,
)
from seed_runtime.recurrence_measurement import (
    DECLARED_IDENTITY,
    LOCALITY_COUNT_RECORDED_KIND,
    LIMITS,
    MEASURED_ASSERTION_STANDING_COORDINATE_RESPONSIBILITY,
    RecurrenceMeasurementError,
    assertions_of_recorded_measurement,
    assertions_from_measured_count,
    get_recorded_measured_assertion,
    iter_recorded_measured_assertions,
    measure_locality_counts,
    record_measured_count,
    measured_count_representation,
)
from tests.material_fixture_console import run_material_fixture_console

DECLARED = ("s1", "s2", "s3", "s4")   # a bounded locality is the recorded locality

LOCALITIES = {
    "s1": "a word is here\n",
    "s2": "a word is there\n",
    "s3": "a word is everywhere\n",
    "s4": "a thing is elsewhere\n",
}
SCOPE = "one bounded locality"


def _compare_all(ledger, findings):
    names = sorted(findings)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            record_comparison_finding(
                ledger, locality_identity=a,
                finding=compare_preserved_findings(
                    ledger, [findings[a], findings[b]]))


@pytest.fixture
def compared():
    ledger = EventLedger()
    for locality_identity, material in LOCALITIES.items():
        run_material_fixture_console(
            ledger=ledger, locality_identity=locality_identity,
            input_stream=binary_input(material + ""), output_stream=StringIO())
    findings = {}
    for locality_identity in LOCALITIES:
        occ = ingest_occurrences(
            ledger, locality_identity=locality_identity)
        findings[locality_identity] = record_measurement_finding(
            ledger, locality_identity=locality_identity,
            finding=measure_after(occ, "a", counting_scope=SCOPE)).identity
    _compare_all(ledger, findings)
    return ledger


def _by_right(ledger, declared=None):
    return {
        f.distinction.right_representation: f
        for f in measure_locality_counts(
            ledger, bounded_localities=declared or DECLARED)
    }


def _assertions_by_result(event):
    return {assertion["result"]: assertion for assertion in event.payload["assertions"]}


# --------------------------------------------------------------------------
# No new Act. A record shape, and declared measurement.
# --------------------------------------------------------------------------


def test_assertion_standing_coordinate_responsibility_is_distinct_from_its_yield(compared):
    """The yielding Act and the result's Standing-coordinate responsible boundary remain distinct."""
    event = record_measured_count(
        compared, locality_identity="s1",
        finding=_by_right(compared)["word"])
    assertions = event.payload["assertions"]
    assert assertions
    assert all(
        assertion["dimensions"]["responsibility"]
        == MEASURED_ASSERTION_STANDING_COORDINATE_RESPONSIBILITY
        for assertion in assertions
    )
    assert all(assertion["subject_kind"] == "assertion" for assertion in assertions)
    assert all(
        assertion["responsible_boundary"] == "this recorded assertion"
        for assertion in assertions
    )
    assert event.payload["exact_act"] == "declared measurement"
    assert all(
        assertion["dimensions"]["responsibility"]
        != event.payload["exact_act"]
        for assertion in assertions
    )
    assert "cohort" not in str(event.payload).lower()



def test_the_record_shape_is_its_own(compared):
    event = record_measured_count(
        compared, locality_identity="s1",
        finding=_by_right(compared)["word"])
    assert event.kind == LOCALITY_COUNT_RECORDED_KIND
    assert event.kind != MEASUREMENT_RECORDED_KIND
    assert "occupancies" not in event.payload
    assert "standing" not in event.payload["dimensions"]
    assert "responsibility" not in event.payload["dimensions"]


def test_one_occurrence_preserves_every_distinct_result(compared):
    finding = _by_right(compared)["word"]
    event = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    assertions = _assertions_by_result(event)

    assert set(assertions) == {
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
        "count",
        "recurrence",
    }
    assert assertions["measured_in"]["dimensions"]["content"] == {
        "localities": ["s1", "s2", "s3"]
    }
    assert assertions["count"]["dimensions"]["content"] == {
        "locality_count": 3
    }


def test_recorded_assertions_are_addressable_through_their_occurrence(compared):
    event = record_measured_count(
        compared,
        locality_identity="s1",
        finding=_by_right(compared)["word"],
    )
    assertions = assertions_of_recorded_measurement(event)

    assert len(assertions) == 5
    assert {assertion.result for assertion in assertions} == {
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
        "count",
        "recurrence",
    }
    for assertion in assertions:
        assert assertion.reference == {
            "assertion_identity": assertion.assertion_identity,
            "recorded_occurrence_reference": event.identity,
        }
        assert get_recorded_measured_assertion(
            compared,
            recorded_occurrence_reference=event.identity,
            assertion_identity=assertion.assertion_identity,
        ) == assertion

    by_result = {assertion.result: assertion for assertion in assertions}
    assert by_result["count"].support_assertion_references == (
        {
            "recorded_occurrence_reference": event.identity,
            "assertion_identity": by_result["measured_in"].assertion_identity,
        },
    )
    assert by_result["recurrence"].support_assertion_references == (
        {
            "recorded_occurrence_reference": event.identity,
            "assertion_identity": by_result["count"].assertion_identity,
        },
    )


def test_validation_refuses_assertion_identity_that_does_not_match_content(compared):
    event = record_measured_count(
        compared,
        locality_identity="s1",
        finding=_by_right(compared)["word"],
    ).model_copy(deep=True)
    assertion = _assertions_by_result(event)["count"]
    assertion["dimensions"]["content"]["locality_count"] += 1

    with pytest.raises(
        RecurrenceMeasurementError, match="identity that does not match"
    ):
        assertions_of_recorded_measurement(event)


def test_validation_refuses_non_assertion_and_unresolved_local_support(compared):
    event = record_measured_count(
        compared,
        locality_identity="s1",
        finding=_by_right(compared)["word"],
    ).model_copy(deep=True)
    _assertions_by_result(event)["count"]["subject_kind"] = "not-an-assertion"
    with pytest.raises(RecurrenceMeasurementError, match="not identified"):
        assertions_of_recorded_measurement(event)

    event = record_measured_count(
        compared,
        locality_identity="s1",
        finding=_by_right(compared)["word"],
    ).model_copy(deep=True)
    _assertions_by_result(event)["count"]["input_support"][
        "local_assertion_identities"
    ] = ["absent-assertion"]
    with pytest.raises(RecurrenceMeasurementError, match="unresolved local"):
        assertions_of_recorded_measurement(event)


def test_assertion_identity_and_yielding_occurrence_remain_distinct(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    first_count = _assertions_by_result(first)["count"]
    second_count = _assertions_by_result(second)["count"]

    assert first_count["dimensions"]["identity"] == second_count["dimensions"][
        "identity"
    ]
    assert first.identity != second.identity
    assert get_recorded_measured_assertion(
        compared,
        recorded_occurrence_reference=first.identity,
        assertion_identity=first_count["dimensions"]["identity"],
    ).recorded_occurrence_reference == first.identity


def test_two_yields_of_one_assertion_can_be_compared_without_relation(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    first_count = next(
        assertion
        for assertion in assertions_of_recorded_measurement(first)
        if assertion.result == "count"
    )
    second_count = next(
        assertion
        for assertion in assertions_of_recorded_measurement(second)
        if assertion.result == "count"
    )

    comparison = compare_assertion_yields(
        compared, (first_count.reference, second_count.reference)
    )

    assert comparison.assertion_identity == first_count.assertion_identity
    assert comparison.act == "Compare"
    assert comparison.responsible_boundary == "this bounded comparison occurrence"
    assert comparison.responsibility == (
        "preserve each input's carried Standing coordinates and report literal "
        "sameness, difference, and absence only"
    )
    assert all(distinction.same for distinction in comparison.distinctions)
    assert not hasattr(comparison, "bounded_relation")


def test_assertion_compare_distinguishes_absence_from_carried_none(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    altered_payload = first.model_copy(deep=True).payload
    altered_count = next(
        assertion
        for assertion in altered_payload["assertions"]
        if assertion["result"] == "count"
    )
    assert altered_count["completeness_boundary"] is None
    del altered_count["completeness_boundary"]
    second = compared.append(
        first.kind,
        altered_payload,
        locality_identity=first.locality_identity,
    )
    first_count = next(
        assertion
        for assertion in assertions_of_recorded_measurement(first)
        if assertion.result == "count"
    )
    second_count = next(
        assertion
        for assertion in assertions_of_recorded_measurement(second)
        if assertion.result == "count"
    )

    comparison = compare_assertion_yields(
        compared, (first_count.reference, second_count.reference)
    )
    distinction = next(
        distinction
        for distinction in comparison.distinctions
        if distinction.coordinate == "completeness_boundary"
    )

    assert distinction.present == (True, False)
    assert distinction.values == (None, None)
    assert distinction.same is False


def test_assertion_compare_exposes_changed_support_without_strengthening_it(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    altered_payload = first.model_copy(deep=True).payload
    altered_measured_in = next(
        assertion
        for assertion in altered_payload["assertions"]
        if assertion["result"] == "measured_in"
    )
    altered_measured_in["input_support"]["event_identities"].append(
        "additional-applicable-evidence"
    )
    second = compared.append(
        first.kind,
        altered_payload,
        locality_identity=first.locality_identity,
    )
    first_assertion = next(
        assertion
        for assertion in assertions_of_recorded_measurement(first)
        if assertion.result == "measured_in"
    )
    second_assertion = next(
        assertion
        for assertion in assertions_of_recorded_measurement(second)
        if assertion.result == "measured_in"
    )

    comparison = compare_assertion_yields(
        compared, (first_assertion.reference, second_assertion.reference)
    )
    distinctions = {
        distinction.coordinate: distinction for distinction in comparison.distinctions
    }
    assert distinctions["input_support"].same is False
    assert all(
        distinction.same
        for coordinate, distinction in distinctions.items()
        if coordinate != "input_support"
    )


def test_assertion_compare_refuses_self_and_different_assertions(compared):
    event = record_measured_count(
        compared,
        locality_identity="s1",
        finding=_by_right(compared)["word"],
    )
    assertions = assertions_of_recorded_measurement(event)
    count = next(assertion for assertion in assertions if assertion.result == "count")
    recurrence = next(
        assertion for assertion in assertions if assertion.result == "recurrence"
    )

    with pytest.raises(AssertionComparisonError, match="cannot be compared with itself"):
        compare_assertion_yields(compared, (count.reference, count.reference))
    with pytest.raises(AssertionComparisonError, match="one canonical Assertion"):
        compare_assertion_yields(
            compared,
            (
                count.reference,
                {
                    "recorded_occurrence_reference": "another-event",
                    "assertion_identity": recurrence.assertion_identity,
                },
            ),
        )


def test_assertion_yield_compare_records_each_literal_result_separately(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    first_count = next(
        item for item in assertions_of_recorded_measurement(first)
        if item.result == "count"
    )
    second_count = next(
        item for item in assertions_of_recorded_measurement(second)
        if item.result == "count"
    )
    comparison = compare_assertion_yields(
        compared, (first_count.reference, second_count.reference)
    )

    event = record_assertion_yield_comparison(
        compared,
        locality_identity="s1",
        comparison=comparison,
    )
    assertions = assertions_of_recorded_assertion_comparison(event)

    assert event.kind == ASSERTION_YIELD_COMPARISON_RECORDED_KIND
    assert event.payload["exact_act"] == "Compare"
    assert event.payload["responsible_boundary"] == "this bounded comparison occurrence"
    assert len(assertions) == len(comparison.distinctions) == 10
    assert {item.coordinate for item in assertions} == {
        item.coordinate for item in comparison.distinctions
    }
    assert len({item.assertion_identity for item in assertions}) == 10
    assert all(item.recorded_occurrence_reference == event.identity for item in assertions)
    assert all(
        item.payload["input_support"]["assertion_references"]
        == [first_count.reference, second_count.reference]
        for item in assertions
    )


def test_yielded_assertions_enter_compare_through_exact_input_relations(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    inputs = [
        next(
            item for item in assertions_of_recorded_measurement(event)
            if item.result == "count"
        )
        for event in (first, second)
    ]
    recorded = record_assertion_yield_comparison(
        compared,
        locality_identity="s2",
        comparison=compare_assertion_yields(
            compared, tuple(item.reference for item in inputs)
        ),
    )

    assert len(recorded.payload["input_locality_evidence_identities"]) == 2
    assert len(recorded.payload["input_applicability_event_identities"]) == 2
    for input_reference, locality_identity, applicability_identity, participation in zip(
        recorded.payload["inputs"],
        recorded.payload["input_locality_evidence_identities"],
        recorded.payload["input_applicability_event_identities"],
        recorded.payload["participation"],
    ):
        locality = compared.get(locality_identity)
        applicability = compared.get(applicability_identity)
        assert locality.payload["first_subject"] == input_reference
        assert locality.payload["second_subject"]["act_occurrence_identity"] == (
            recorded.payload["act_occurrence_identity"]
        )
        assert applicability.payload["input_reference"] == input_reference
        assert applicability.payload["locality_evidence_identity"] == locality.identity
        assert applicability.payload["standing"] == "applicable"
        assert participation == {
            "subject_reference": input_reference,
            "role": "compared Assertion",
            "act_occurrence_identity": recorded.payload["act_occurrence_identity"],
            "applicability_event_identity": applicability.identity,
        }


def test_locality_and_applicability_do_not_substitute_for_participation(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    inputs = [
        next(
            item for item in assertions_of_recorded_measurement(event)
            if item.result == "count"
        )
        for event in (first, second)
    ]
    recorded = record_assertion_yield_comparison(
        compared,
        locality_identity="s1",
        comparison=compare_assertion_yields(
            compared, tuple(item.reference for item in inputs)
        ),
    ).model_copy(deep=True)
    assert recorded.payload["input_locality_evidence_identities"]
    assert recorded.payload["input_applicability_event_identities"]
    recorded.payload["participation"] = []

    with pytest.raises(AssertionComparisonError, match="Participation"):
        assertions_of_recorded_assertion_comparison(recorded)


def test_recording_comparison_results_does_not_establish_support_or_revision(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    left = next(
        item for item in assertions_of_recorded_measurement(first)
        if item.result == "count"
    )
    right = next(
        item for item in assertions_of_recorded_measurement(second)
        if item.result == "count"
    )
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    event = record_assertion_yield_comparison(
        compared, locality_identity="s1", comparison=comparison
    )

    represented = str(event.payload)
    assert "recording does not establish Applicability" in represented
    assert "applicability" not in event.payload
    assert "admission" not in event.payload
    assert "input support" not in event.payload
    assert "revision" not in event.payload


def test_recorded_comparison_assertion_identity_is_recomputed(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    event = record_assertion_yield_comparison(
        compared, locality_identity="s1", comparison=comparison
    ).model_copy(deep=True)
    event.payload["assertions"][0]["dimensions"]["identity"] = "asserted-not-canonical"

    with pytest.raises(AssertionComparisonError, match="invalid identity"):
        assertions_of_recorded_assertion_comparison(event)


def test_validation_refuses_a_self_consistent_forged_compare_result(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    event = record_assertion_yield_comparison(
        compared, locality_identity="s1", comparison=comparison
    ).model_copy(deep=True)
    assertion = event.payload["assertions"][0]
    content = assertion["dimensions"]["content"]
    assert content["present"] == [True, True]
    assert content["values"][0] == content["values"][1]
    content["same"] = False
    assertion["dimensions"]["identity"] = _distinction_assertion_identity(
        compared_assertion_identity=assertion["assertion_subject"][
            "compared_assertion_identity"
        ],
        inputs=assertion["input_support"]["assertion_references"],
        locality_identity="s1",
        **content,
    )

    with pytest.raises(AssertionComparisonError, match="output contract"):
        assertions_of_recorded_assertion_comparison(event)


def test_validation_requires_the_exact_compare_coordinate_set(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    event = record_assertion_yield_comparison(
        compared, locality_identity="s1", comparison=comparison
    ).model_copy(deep=True)
    event.payload["assertions"].pop()

    with pytest.raises(AssertionComparisonError, match="every distinct"):
        assertions_of_recorded_assertion_comparison(event)


def test_comparison_assertion_identity_includes_its_recorded_scope(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )

    first_record = record_assertion_yield_comparison(
        compared, locality_identity="s1", comparison=comparison
    )
    second_record = record_assertion_yield_comparison(
        compared, locality_identity="s2", comparison=comparison
    )

    first_identities = {
        item.assertion_identity
        for item in assertions_of_recorded_assertion_comparison(first_record)
    }
    second_identities = {
        item.assertion_identity
        for item in assertions_of_recorded_assertion_comparison(second_record)
    }
    assert first_identities.isdisjoint(second_identities)


def test_recording_refuses_a_comparison_not_established_from_its_inputs(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    second = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    forged = replace(
        comparison,
        distinctions=(
            replace(comparison.distinctions[0], same=not comparison.distinctions[0].same),
            *comparison.distinctions[1:],
        ),
    )

    with pytest.raises(AssertionComparisonError, match="does not match"):
        record_assertion_yield_comparison(
            compared, locality_identity="s1", comparison=forged
        )


def test_recorded_assertion_stream_obeys_sessions_and_boundary(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    boundary = compared.append_boundary()
    record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    record_measured_count(
        compared, locality_identity="s2", finding=finding
    )

    read = list(
        iter_recorded_measured_assertions(
            compared,
            locality_identities=("s1",),
            through=boundary,
        )
    )
    assert len(read) == 5
    assert {assertion.recorded_occurrence_reference for assertion in read} == {first.identity}


def test_exact_sets_keep_completeness_separate_from_support(compared):
    finding = _by_right(compared)["word"]
    assertions = {
        assertion.result: assertion
        for assertion in assertions_from_measured_count(finding)
    }
    boundary = {"identity": finding.input_ledger_boundary.identity}

    for result in (
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
    ):
        encoded = assertions[result].to_json_dict()
        assert encoded["completeness_boundary"] == boundary
        assert encoded["completeness_scope"]["locality_identities"] == list(DECLARED)
        assert encoded["completeness_scope"]["requires_locality_existence"] is True
        assert finding.input_ledger_boundary.identity not in (
            encoded["input_support"]["event_identities"]
            + encoded["input_support"]["local_assertion_identities"]
        )

    assert assertions["measured_in"].support_event_identities
    assert assertions["measured_in"].completeness_occurrence_kinds == (
        MEASUREMENT_RECORDED_KIND,
    )
    assert assertions["measured_without_distinction"].support_event_identities
    assert assertions[
        "measured_without_distinction"
    ].completeness_occurrence_kinds == (MEASUREMENT_RECORDED_KIND,)
    assert assertions["coordinate_not_measured"].support_event_identities == ()
    assert assertions["coordinate_not_measured"].completeness_occurrence_kinds == (
        MEASUREMENT_RECORDED_KIND,
    )


def test_count_and_recurrence_stand_on_assertions_not_raw_events(compared):
    assertions = assertions_from_measured_count(_by_right(compared)["word"])
    by_result = {assertion.result: assertion for assertion in assertions}

    assert by_result["count"].support_event_identities == ()
    assert by_result["count"].support_assertion_identities == (
        by_result["measured_in"].identity,
    )
    assert by_result["count"].completeness_boundary is None
    assert by_result["recurrence"].support_event_identities == ()
    assert by_result["recurrence"].support_assertion_identities == (
        by_result["count"].identity,
    )
    assert by_result["recurrence"].completeness_boundary is None


def test_scope_and_rule_are_part_of_assertion_identity(compared):
    finding = _by_right(compared)["word"]
    declared = dict(finding.distinction.declared)
    other_scope = dict(declared, counting_scope="another bounded scope")
    other_rule = dict(declared, equivalence_rule="another exact rule")

    scoped = replace(
        finding,
        distinction=replace(
            finding.distinction, declared=tuple(other_scope.items())
        ),
    )
    ruled = replace(
        finding,
        distinction=replace(
            finding.distinction, declared=tuple(other_rule.items())
        ),
    )
    identities = [
        {
            assertion.result: assertion.identity
            for assertion in assertions_from_measured_count(candidate)
        }
        for candidate in (finding, scoped, ruled)
    ]
    for result in identities[0]:
        assert len({identified[result] for identified in identities}) == 3
        assert all(
            identified[result].startswith("measured-assertion:")
            for identified in identities
        )


def test_material_beside_the_act_is_not_a_measurement_input():
    ledger = EventLedger()
    run_material_fixture_console(
        ledger=ledger, locality_identity="s",
        input_stream=binary_input("a word\n"), output_stream=StringIO())
    with pytest.raises(RecurrenceMeasurementError, match="not a measured input"):
        measure_locality_counts(
            ledger, bounded_localities=["s"])


def test_declaring_an_locality_does_not_establish_it(compared):
    """`#2431` accepted any name and placed it in coordinate_not_measured.

    Declaring the Scope chooses among established localities. It cannot create
    one by naming it.
    """
    with pytest.raises(RecurrenceMeasurementError, match="no recorded occurrence"):
        measure_locality_counts(
            compared, bounded_localities=DECLARED + ("ghost",))


def test_a_named_locality_cannot_enter_the_third_result_unestablished(compared):
    """The exact consequence: a ghost would have been counted as not measuring.

    The refusal is what this asserts. `#2432` followed it with
    ``all(f.bounded_localities == ("s1",) for f in findings)`` over a
    single-locality declaration, which returns no findings at all — every
    comparison involving `s1` has its other input outside the declared Scope
    and is correctly rejected — so `all([])` passed and established nothing.
    """
    with pytest.raises(RecurrenceMeasurementError, match="ghost"):
        measure_locality_counts(
            compared, bounded_localities=("s1", "ghost"))


def test_a_declaration_of_established_localities_is_accepted(compared):
    """Existence validation passing, asserted on a result that exists."""
    findings = measure_locality_counts(
        compared, bounded_localities=("s1", "s2"))
    assert findings
    assert all(f.bounded_localities == ("s1", "s2") for f in findings)


def test_one_locality_yields_an_exact_count_without_claiming_recurrence(compared):
    findings = measure_locality_counts(
        compared, bounded_localities=("s1",)
    )
    assert len(findings) == 1
    assert findings[0].measured_in == ("s1",)
    assert findings[0].locality_count == 1
    assert findings[0].recurrence_established is False


# --------------------------------------------------------------------------
# The whole declared identity governs grouping.
# --------------------------------------------------------------------------


def test_the_declared_identity_includes_the_counting_scope(compared):
    """`#2429` grouped on left, rule and position, then said "and scope"."""
    assert "counting_scope" in DECLARED_IDENTITY
    assert "representation_measured" in DECLARED_IDENTITY
    assert "measurement_distinction" in DECLARED_IDENTITY
    declared = dict(_by_right(compared)["word"].distinction.declared)
    assert set(declared) == set(DECLARED_IDENTITY)
    assert declared["counting_scope"] == SCOPE


def test_measurements_declaring_different_scopes_do_not_group(compared):
    """Two measurements under different declared scopes are not the same one."""
    other = {}
    for locality_identity in ("s1", "s2"):
        occ = ingest_occurrences(
            compared, locality_identity=locality_identity)
        other[locality_identity] = record_measurement_finding(
            compared, locality_identity=locality_identity,
            finding=measure_after(occ, "a", counting_scope="a different scope")).identity
    _compare_all(compared, other)

    scopes = {
        dict(f.distinction.declared)["counting_scope"]
        for f in measure_locality_counts(compared, bounded_localities=DECLARED)
        if f.distinction.right_representation == "word"
    }
    assert scopes == {SCOPE, "a different scope"}
    counts = {
        dict(f.distinction.declared)["counting_scope"]: f.locality_count
        for f in measure_locality_counts(compared, bounded_localities=DECLARED)
        if f.distinction.right_representation == "word"
    }
    assert counts[SCOPE] == 3            # s1 s2 s3
    assert counts["a different scope"] == 2   # s1 s2 only


# --------------------------------------------------------------------------
# Everything the result stood on travels with it.
# --------------------------------------------------------------------------


def test_only_measurements_that_supply_the_count_travel_as_evidence(compared):
    finding = _by_right(compared)["word"]
    kinds = {compared.get(i).kind for i in finding.input_event_identities}
    assert kinds == {MEASUREMENT_RECORDED_KIND}


def test_every_locality_s_measurement_is_among_the_support(compared):
    finding = _by_right(compared)["word"]
    supporting = {
        compared.get(i).locality_identity
        for i in finding.input_event_identities
        if compared.get(i).kind == MEASUREMENT_RECORDED_KIND
    }
    assert supporting == set(finding.bounded_localities)


def test_the_input_ledger_boundary_is_preserved_as_read_provenance(compared):
    boundary = compared.append_boundary()
    finding = _by_right(compared)["word"]

    assert finding.input_ledger_boundary == boundary
    assert finding.to_json_dict()["input_ledger_boundary"] == {
        "identity": boundary.identity,
    }
    recorded = record_measured_count(
        compared, locality_identity="s1", finding=finding
    )
    assert "input_ledger_boundary" not in recorded.payload
    assertions = _assertions_by_result(recorded)
    for result in (
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
    ):
        assert assertions[result]["completeness_boundary"] == {
            "identity": boundary.identity,
        }


def test_the_old_aggregate_result_is_not_recorded_beside_the_assertions(compared):
    event = record_measured_count(
        compared,
        locality_identity="s1",
        finding=_by_right(compared)["word"],
    )
    old_aggregate_fields = {
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
        "locality_count",
        "recurrence_established",
        "bounded_localities",
        "input_event_identities",
        "input_ledger_boundary",
        "distinction",
    }
    assert old_aggregate_fields.isdisjoint(event.payload)


# --------------------------------------------------------------------------
# The three results, and what they are called.
# --------------------------------------------------------------------------


def test_it_counts_the_localities_the_distinction_recurs_in(compared):
    finding = _by_right(compared)["word"]
    assert finding.locality_count == 3
    assert finding.measured_in == ("s1", "s2", "s3")


def test_measuring_the_coordinate_without_the_distinction_is_its_own_result(compared):
    finding = _by_right(compared)["word"]
    assert finding.measured_without_distinction == ("s4",)


def test_only_relevant_evidence_places_an_locality_in_the_second_result(compared):
    """`#2431`'s unrelated-presence support belongs to the third result.

    Exact-coordinate Measurement and Compare/input Evidence establish
    ``measured_without_distinction``. A later measurement of another coordinate
    in the same locality establishes nothing additional about that result.
    """
    exact_coordinate = next(
        event
        for event in compared.list()
        if event.kind == MEASUREMENT_RECORDED_KIND and event.locality_identity == "s4"
    )
    occurrences = ingest_occurrences(
        compared, locality_identity="s4"
    )
    unrelated = record_measurement_finding(
        compared,
        locality_identity="s4",
        finding=measure_after(occurrences, "nothing", counting_scope=SCOPE),
    )

    finding = _by_right(compared)["word"]

    assert finding.measured_without_distinction == ("s4",)
    assert exact_coordinate.identity in finding.input_event_identities
    assert unrelated.identity not in finding.input_event_identities


def test_a_count_of_one_is_a_finding_and_is_not_recurrence(compared):
    """`01.Source:28` lists count and recurrence as separate findings.

    `#2430` called this shape RecurrenceFinding and represented a count of one as
    "recurs in 1 bounded localities", asserting recurrence where nothing
    recurred.
    """
    finding = _by_right(compared)["thing"]
    assert finding.measured_in == ("s4",)
    assert finding.locality_count == 1
    assert finding.recurrence_established is False
    assert "was measured in 1 bounded locality" in measured_count_representation(finding)
    assert "recurs" not in measured_count_representation(finding)
    assertions = assertions_from_measured_count(finding)
    assert {assertion.result for assertion in assertions} == {
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
        "count",
    }


def test_recurrence_is_established_only_above_one(compared):
    finding = _by_right(compared)["word"]
    assert finding.locality_count == 3
    assert finding.recurrence_established is True
    assert "recurs in 3 bounded localities" in measured_count_representation(finding)


def _add_s5(ledger):
    """An locality that measures a different coordinate entirely."""
    run_material_fixture_console(
        ledger=ledger, locality_identity="s5",
        input_stream=binary_input("nothing relevant here\n"),
        output_stream=StringIO())
    occ = ingest_occurrences(ledger, locality_identity="s5")
    return record_measurement_finding(
        ledger, locality_identity="s5",
        finding=measure_after(occ, "nothing", counting_scope=SCOPE))


def test_an_locality_that_never_measured_the_coordinate_is_distinguished(compared):
    _add_s5(compared)
    declared = DECLARED + ("s5",)
    finding = _by_right(compared, declared)["word"]
    assert "s5" in finding.coordinate_not_measured
    assert "s5" not in finding.measured_without_distinction
    assert "s5" not in finding.measured_in


def test_the_third_result_preserves_its_complete_read_not_copied_identities(compared):
    """The ledger boundary reads the complete negative-classification read."""
    unrelated = _add_s5(compared)
    declared = DECLARED + ("s5",)
    finding = _by_right(compared, declared)["word"]

    assert "s5" in finding.coordinate_not_measured
    assert unrelated.identity not in finding.input_event_identities
    read = compared.iter_locality_kind(
        "s5",
        MEASUREMENT_RECORDED_KIND,
        through=finding.input_ledger_boundary,
    )
    assert unrelated.identity in {event.identity for event in read}


def test_an_undeclared_locality_enters_nothing(compared):
    _add_s5(compared)
    finding = _by_right(compared)["word"]          # s5 not declared
    assert "s5" not in finding.bounded_localities
    assert "s5" not in finding.coordinate_not_measured
    assert len(finding.bounded_localities) == 4


def test_the_bounded_scope_must_be_declared(compared):
    with pytest.raises(RecurrenceMeasurementError, match="no bounded localities were declared"):
        measure_locality_counts(compared, bounded_localities=[])


def test_the_three_results_partition_the_bounded_localities(compared):
    for finding in measure_locality_counts(compared, bounded_localities=DECLARED):
        parts = (
            set(finding.measured_in),
            set(finding.measured_without_distinction),
            set(finding.coordinate_not_measured),
        )
        assert set().union(*parts) == set(finding.bounded_localities)
        assert sum(len(p) for p in parts) == len(finding.bounded_localities)


# --------------------------------------------------------------------------
# What the record says, and refuses.
# --------------------------------------------------------------------------


def test_the_counting_scope_states_the_declaration(compared):
    """`#2429` said "supplied to this Seed"; `#2430` said what it input.

    Neither was the bounded scope `01.Source:28` requires disclosed, because
    both described a set the act discovered rather than one it was given.
    """
    event = record_measured_count(
        compared, locality_identity="s1",
        finding=_by_right(compared)["word"])
    scope = event.payload["counting_scope"]
    assert "declared to this measurement" in scope
    assert "no locality enters by having measured something else" in scope
    assert "supplied to this Seed" not in scope


def test_the_record_refuses_source_independence_and_corroboration(compared):
    event = record_measured_count(
        compared, locality_identity="s1",
        finding=_by_right(compared)["word"])
    refused = " ".join(event.payload["limits"])
    assert "independently preserved is not independent" in refused
    assert "repetition is not independent corroboration" in refused
    assert "establishes no relation between the" in refused
    assert set(LIMITS) <= set(event.payload["limits"])


def test_the_rendering_states_the_literal_sentence(compared):
    represented = measured_count_representation(_by_right(compared)["word"])
    assert "recurs in 3 bounded localities" in represented
    assert SCOPE in represented
    for word in ("agree", "corroborat", "independent source", "relation",
                 "confirm", "prove", "cohort", "population"):
        assert word not in represented.lower()


def test_the_vocabulary_is_gone(compared):
    """`cohort`, `population`, `body`, `survey`, `exposed` earned no place."""
    event = record_measured_count(
        compared, locality_identity="s1",
        finding=_by_right(compared)["word"])
    represented = str(event.payload).lower()
    for word in ("cohort", "population", "survey", "exposed", "bodies"):
        assert word not in represented


# --------------------------------------------------------------------------
# A bounded locality is the recorded locality, and validating one is bounded.
# --------------------------------------------------------------------------


def test_a_payload_string_cannot_manufacture_an_locality(compared):
    """`#2432` established existence from `dimensions.scope_locality`.

    That coordinate's represented relation is itself left Unknown by the same report, and a
    record can say anything in it. The recorded locality boundary is the witness.
    """
    compared.append(
        "operator.measurement.finding_recorded", {"dimensions": {"scope_locality": "locality:ghost"}},
        locality_identity="s1",
    )
    with pytest.raises(RecurrenceMeasurementError, match="no recorded occurrence"):
        measure_locality_counts(
            compared, bounded_localities=DECLARED + ("ghost",))


def test_durable_validation_reads_each_exact_locality(tmp_path):
    from seed_runtime.events import SQLiteEventLedger

    ledger = SQLiteEventLedger(str(tmp_path / "seed.db"))
    try:
        for locality_identity, material in LOCALITIES.items():
            run_material_fixture_console(
                ledger=ledger, locality_identity=locality_identity,
                input_stream=binary_input(material + ""),
                output_stream=StringIO())
        findings = {}
        for locality_identity in LOCALITIES:
            occ = ingest_occurrences(
                ledger, locality_identity=locality_identity)
            findings[locality_identity] = record_measurement_finding(
                ledger, locality_identity=locality_identity,
                finding=measure_after(occ, "a", counting_scope=SCOPE)).identity
        _compare_all(ledger, findings)

        statements = []
        ledger._connection.set_trace_callback(statements.append)
        measure_locality_counts(
            ledger, bounded_localities=DECLARED)
        ledger._connection.set_trace_callback(None)
    finally:
        ledger.close()

    selects = [q for q in statements if q.strip().upper().startswith("SELECT *")]
    assert selects, "the measurement read something"
    for query in selects:
        assert "locality_identity" in query, query
        assert "kind" in query, query
        assert "FROM events WHERE locality_identity" in query, query
    assert len(selects) == len(DECLARED)
    assert sum(
        MEASUREMENT_RECORDED_KIND in query for query in selects
    ) == len(DECLARED)
    assert not any(
        "operator.measurement.comparison_recorded" in query for query in selects
    )


def test_measurement_events_are_folded_without_being_retained(compared):
    """The resource boundary is one streamed Measurement, not all measurements."""
    import gc
    import weakref

    references = []
    live_counts = []
    original_iterator = compared.iter_locality_kind

    def tracked_iterator(locality_identity, kind, *, through=None):
        for stored in original_iterator(
            locality_identity, kind, through=through
        ):
            if kind != MEASUREMENT_RECORDED_KIND:
                yield stored
                continue
            gc.collect()
            live_counts.append(
                sum(reference() is not None for reference in references)
            )
            generated = stored.model_copy(deep=True)
            references.append(weakref.ref(generated))
            yield generated
            del generated

    compared.iter_locality_kind = tracked_iterator
    measure_locality_counts(
        compared, bounded_localities=DECLARED
    )
    gc.collect()

    assert references
    assert max(live_counts) <= 1
    assert all(reference() is None for reference in references)


def test_every_probe_and_pass_reads_one_prefix_despite_a_concurrent_append(compared):
    boundary = compared.append_boundary()
    original_has_locality = compared.has_locality
    original_iterator = compared.iter_locality_kind
    seen_boundaries = []
    appended = False

    comparison = next(
        event
        for event in compared.list()
        if event.kind == "operator.measurement.comparison_recorded"
    )
    payload = comparison.model_copy(deep=True).payload
    payload["shared_occupants"] = [
        *payload.get("shared_occupants", []),
        "after-boundary",
    ]

    def tracked_has_locality(locality_identity, *, through=None):
        seen_boundaries.append(through)
        return original_has_locality(locality_identity, through=through)

    def tracked_iterator(locality_identity, kind, *, through=None):
        nonlocal appended
        seen_boundaries.append(through)
        if not appended:
            appended = True
            compared.append(
                comparison.kind,
                payload,
                locality_identity=comparison.locality_identity,
            )
        yield from original_iterator(
            locality_identity, kind, through=through
        )

    compared.has_locality = tracked_has_locality
    compared.iter_locality_kind = tracked_iterator
    findings = measure_locality_counts(
        compared, bounded_localities=DECLARED
    )

    assert appended is True
    assert seen_boundaries
    assert set(seen_boundaries) == {boundary}
    assert all(finding.input_ledger_boundary == boundary for finding in findings)
    assert "after-boundary" not in {
        finding.distinction.right_representation for finding in findings
    }


# --------------------------------------------------------------------------
# The occurrence-to-result edge remains exactly addressable.
# --------------------------------------------------------------------------


def test_a_durable_yielding_occurrence_is_identifiable_and_verifies(tmp_path):
    """Historical yield Evidence remains occurrence-bound.

    The yielding occurrence is the event carrying the payload, so its own identity
    cannot appear inside that payload. What must hold is that the enclosing
    occurrence is exactly identifiable and verifiable once appended.
    """
    from seed_runtime.events import VERIFIED, SQLiteEventLedger

    path = str(tmp_path / "seed.db")
    ledger = SQLiteEventLedger(path)
    try:
        for locality_identity, material in LOCALITIES.items():
            run_material_fixture_console(
                ledger=ledger, locality_identity=locality_identity,
                input_stream=binary_input(material + ""),
                output_stream=StringIO())
        findings = {}
        for locality_identity in LOCALITIES:
            occ = ingest_occurrences(
                ledger, locality_identity=locality_identity)
            findings[locality_identity] = record_measurement_finding(
                ledger, locality_identity=locality_identity,
                finding=measure_after(occ, "a", counting_scope=SCOPE)).identity
        _compare_all(ledger, findings)
        counted = measure_locality_counts(
            ledger, bounded_localities=DECLARED)
        event = record_measured_count(
            ledger, locality_identity="s1", finding=counted[0])
        boundary = ledger.append_boundary()

        assert ledger.get(event.identity).identity == event.identity
        assert ledger.integrity_of(event.identity) == VERIFIED
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        read = list(
            iter_recorded_measured_assertions(
                reopened,
                locality_identities=("s1",),
                through=boundary,
            )
        )
        assert read
        assert {assertion.recorded_occurrence_reference for assertion in read} == {
            event.identity
        }
        assert get_recorded_measured_assertion(
            reopened,
            recorded_occurrence_reference=event.identity,
            assertion_identity=read[0].assertion_identity,
        ) == read[0]
    finally:
        reopened.close()


# --------------------------------------------------------------------------
# D has as input C without defeating C.
# --------------------------------------------------------------------------


def test_counting_recurrence_does_not_take_comparisons_as_input(compared):
    """The invariant. `recurs in 15` must never become `15 sources agree`.

    Pairwise Compare Events may exist beside the Measurements, but they do not
    enter this Act merely by co-presence. The count's own record also refuses
    corroboration in its own words.
    """
    finding = _by_right(compared)["word"]
    input = [compared.get(i) for i in finding.input_event_identities]
    assert input
    assert {event.kind for event in input} == {MEASUREMENT_RECORDED_KIND}
    assert any(
        event.kind == "operator.measurement.comparison_recorded"
        for event in compared.list()
    )

    event = record_measured_count(
        compared, locality_identity="s1", finding=finding)
    refused = " ".join(event.payload["limits"])
    assert "not independent corroboration" in refused
    assert "establishes no relation between the" in refused
