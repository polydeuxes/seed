"""Recurrence across bounded exchanges, measured over Seed's own occurrences.

`#2429` built this and called it a "cohort measurement", writing a Responsibility
into every record that nothing established. `#2351` reconstructed declared
measurement and said no new act, noun, or grammar is required; recurrence and
count are already its findings. What changed here is the subject, not the Act.

These tests pin the three corrections as carefully as the count: the whole
declared identity governs grouping, every occurrence the result stood on
travels with it, and the counting scope says exactly what was input.
"""

from __future__ import annotations

from dataclasses import replace
from io import StringIO

import pytest

from seed_runtime.adjacent_pair_measurement import measure_after
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
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from seed_runtime.recurrence_measurement import (
    DECLARED_IDENTITY,
    EXCHANGE_COUNT_RECORDED_KIND,
    FORBIDDEN_INFERENCES,
    MEASURED_ASSERTION_STANDING_COORDINATE_RESPONSIBILITY,
    RecurrenceMeasurementError,
    assertions_of_recorded_measurement,
    assertions_from_measured_count,
    get_recorded_measured_assertion,
    iter_recorded_measured_assertions,
    measure_exchange_counts,
    record_measured_count,
    render_measured_count,
)
from seed_runtime.operator_console import run_persistent_operator_console

DECLARED = ("s1", "s2", "s3", "s4")   # a bounded exchange is the recorded session

EXCHANGES = {
    "s1": "a word is here\n",
    "s2": "a word is there\n",
    "s3": "a word is everywhere\n",
    "s4": "a thing is elsewhere\n",
}
SCOPE = "one bounded exchange"


def _compare_all(ledger, findings):
    names = sorted(findings)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            record_comparison_finding(
                ledger, workspace_id="w", session_id=a,
                finding=compare_preserved_findings(
                    ledger, [findings[a], findings[b]]))


@pytest.fixture
def compared():
    ledger = EventLedger()
    for session_id, material in EXCHANGES.items():
        run_persistent_operator_console(
            ledger=ledger, workspace_id="w", session_id=session_id,
            input_stream=StringIO(material + "exit\n"), output_stream=StringIO())
    findings = {}
    for session_id in EXCHANGES:
        occ = preserved_ingress_occurrences(
            ledger, workspace_id="w", session_id=session_id)
        findings[session_id] = record_measurement_finding(
            ledger, workspace_id="w", session_id=session_id,
            finding=measure_after(occ, "a", counting_scope=SCOPE)).id
    _compare_all(ledger, findings)
    return ledger


def _by_right(ledger, declared=None):
    return {
        f.distinction.right_representation: f
        for f in measure_exchange_counts(
            ledger, workspace_id="w", bounded_exchanges=declared or DECLARED)
    }


def _assertions_by_result(event):
    return {assertion["result"]: assertion for assertion in event.payload["assertions"]}


# --------------------------------------------------------------------------
# No new Act. A record shape, and declared measurement.
# --------------------------------------------------------------------------


def test_assertion_standing_coordinate_responsibility_is_distinct_from_its_yield(compared):
    """The yielding Act and the result's Standing-coordinate responsible boundary remain distinct."""
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
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
    assert event.payload["yielding_act"] == "declared measurement"
    assert all(
        assertion["dimensions"]["responsibility"]
        != event.payload["yielding_act"]
        for assertion in assertions
    )
    assert "cohort" not in str(event.payload).lower()



def test_the_record_shape_is_its_own(compared):
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.kind == EXCHANGE_COUNT_RECORDED_KIND
    assert event.kind != MEASUREMENT_RECORDED_KIND
    assert "occupancies" not in event.payload
    assert event.payload["dimensions"]["standing"] == "recorded"
    assert "responsibility" not in event.payload["dimensions"]


def test_one_occurrence_preserves_every_distinct_result(compared):
    finding = _by_right(compared)["word"]
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
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
        "exchanges": ["s1", "s2", "s3"]
    }
    assert assertions["count"]["dimensions"]["content"] == {
        "exchange_count": 3
    }


def test_recorded_assertions_are_addressable_through_their_occurrence(compared):
    event = record_measured_count(
        compared,
        workspace_id="w",
        session_id="s1",
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
            "assertion_id": assertion.assertion_id,
            "yielding_event_id": event.id,
        }
        assert get_recorded_measured_assertion(
            compared,
            yielding_event_id=event.id,
            assertion_id=assertion.assertion_id,
        ) == assertion

    by_result = {assertion.result: assertion for assertion in assertions}
    assert by_result["count"].support_assertion_refs == (
        {
            "yielding_event_id": event.id,
            "assertion_id": by_result["measured_in"].assertion_id,
        },
    )
    assert by_result["recurrence"].support_assertion_refs == (
        {
            "yielding_event_id": event.id,
            "assertion_id": by_result["count"].assertion_id,
        },
    )


def test_validation_refuses_assertion_identity_that_does_not_match_content(compared):
    event = record_measured_count(
        compared,
        workspace_id="w",
        session_id="s1",
        finding=_by_right(compared)["word"],
    ).model_copy(deep=True)
    assertion = _assertions_by_result(event)["count"]
    assertion["dimensions"]["content"]["exchange_count"] += 1

    with pytest.raises(
        RecurrenceMeasurementError, match="identity that does not match"
    ):
        assertions_of_recorded_measurement(event)


def test_validation_refuses_non_assertion_and_unresolved_local_support(compared):
    event = record_measured_count(
        compared,
        workspace_id="w",
        session_id="s1",
        finding=_by_right(compared)["word"],
    ).model_copy(deep=True)
    _assertions_by_result(event)["count"]["subject_kind"] = "not-an-assertion"
    with pytest.raises(RecurrenceMeasurementError, match="not identified"):
        assertions_of_recorded_measurement(event)

    event = record_measured_count(
        compared,
        workspace_id="w",
        session_id="s1",
        finding=_by_right(compared)["word"],
    ).model_copy(deep=True)
    _assertions_by_result(event)["count"]["support_basis"][
        "local_assertion_ids"
    ] = ["absent-assertion"]
    with pytest.raises(RecurrenceMeasurementError, match="unresolved local"):
        assertions_of_recorded_measurement(event)


def test_assertion_identity_and_yielding_occurrence_remain_distinct(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    first_count = _assertions_by_result(first)["count"]
    second_count = _assertions_by_result(second)["count"]

    assert first_count["dimensions"]["identity"] == second_count["dimensions"][
        "identity"
    ]
    assert first.id != second.id
    assert get_recorded_measured_assertion(
        compared,
        yielding_event_id=first.id,
        assertion_id=first_count["dimensions"]["identity"],
    ).yielding_event_id == first.id


def test_two_yields_of_one_assertion_can_be_compared_without_relation(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
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

    assert comparison.assertion_id == first_count.assertion_id
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
        compared, workspace_id="w", session_id="s1", finding=finding
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
        first.workspace_id,
        altered_payload,
        session_id=first.session_id,
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
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    altered_payload = first.model_copy(deep=True).payload
    altered_measured_in = next(
        assertion
        for assertion in altered_payload["assertions"]
        if assertion["result"] == "measured_in"
    )
    altered_measured_in["support_basis"]["event_ids"].append(
        "additional-applicable-evidence"
    )
    second = compared.append(
        first.kind,
        first.workspace_id,
        altered_payload,
        session_id=first.session_id,
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
    assert distinctions["support_basis"].same is False
    assert all(
        distinction.same
        for coordinate, distinction in distinctions.items()
        if coordinate != "support_basis"
    )


def test_assertion_compare_refuses_self_and_different_assertions(compared):
    event = record_measured_count(
        compared,
        workspace_id="w",
        session_id="s1",
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
                    "yielding_event_id": "another-event",
                    "assertion_id": recurrence.assertion_id,
                },
            ),
        )


def test_assertion_yield_compare_records_each_literal_result_separately(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
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
        workspace_id="w",
        session_id="s1",
        comparison=comparison,
    )
    assertions = assertions_of_recorded_assertion_comparison(event)

    assert event.kind == ASSERTION_YIELD_COMPARISON_RECORDED_KIND
    assert event.payload["yielding_act"] == "Compare"
    assert event.payload["responsible_boundary"] == "this bounded comparison occurrence"
    assert len(assertions) == len(comparison.distinctions) == 10
    assert {item.coordinate for item in assertions} == {
        item.coordinate for item in comparison.distinctions
    }
    assert len({item.assertion_id for item in assertions}) == 10
    assert all(item.yielding_event_id == event.id for item in assertions)
    assert all(
        item.payload["support_basis"]["assertion_refs"]
        == [first_count.reference, second_count.reference]
        for item in assertions
    )


def test_recording_comparison_results_does_not_establish_support_or_revision(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
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
        compared, workspace_id="w", session_id="s1", comparison=comparison
    )

    rendered = str(event.payload)
    assert "recording does not establish Applicability" in rendered
    assert "applicability" not in event.payload
    assert "admission" not in event.payload
    assert "input support" not in event.payload
    assert "revision" not in event.payload


def test_recorded_comparison_assertion_identity_is_recomputed(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    event = record_assertion_yield_comparison(
        compared, workspace_id="w", session_id="s1", comparison=comparison
    ).model_copy(deep=True)
    event.payload["assertions"][0]["dimensions"]["identity"] = "asserted-not-canonical"

    with pytest.raises(AssertionComparisonError, match="invalid identity"):
        assertions_of_recorded_assertion_comparison(event)


def test_validation_refuses_a_self_consistent_forged_compare_result(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    event = record_assertion_yield_comparison(
        compared, workspace_id="w", session_id="s1", comparison=comparison
    ).model_copy(deep=True)
    assertion = event.payload["assertions"][0]
    content = assertion["dimensions"]["content"]
    assert content["present"] == [True, True]
    assert content["values"][0] == content["values"][1]
    content["same"] = False
    assertion["dimensions"]["identity"] = _distinction_assertion_identity(
        compared_assertion_id=assertion["assertion_subject"][
            "compared_assertion_id"
        ],
        inputs=assertion["support_basis"]["assertion_refs"],
        workspace_id="w",
        session_id="s1",
        **content,
    )

    with pytest.raises(AssertionComparisonError, match="output contract"):
        assertions_of_recorded_assertion_comparison(event)


def test_validation_requires_the_exact_compare_coordinate_set(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )
    event = record_assertion_yield_comparison(
        compared, workspace_id="w", session_id="s1", comparison=comparison
    ).model_copy(deep=True)
    event.payload["assertions"].pop()

    with pytest.raises(AssertionComparisonError, match="every distinct"):
        assertions_of_recorded_assertion_comparison(event)


def test_comparison_assertion_identity_includes_its_recorded_scope(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    left = assertions_of_recorded_measurement(first)[0]
    right = assertions_of_recorded_measurement(second)[0]
    comparison = compare_assertion_yields(
        compared, (left.reference, right.reference)
    )

    first_record = record_assertion_yield_comparison(
        compared, workspace_id="w", session_id="s1", comparison=comparison
    )
    second_record = record_assertion_yield_comparison(
        compared, workspace_id="w", session_id="s2", comparison=comparison
    )

    first_ids = {
        item.assertion_id
        for item in assertions_of_recorded_assertion_comparison(first_record)
    }
    second_ids = {
        item.assertion_id
        for item in assertions_of_recorded_assertion_comparison(second_record)
    }
    assert first_ids.isdisjoint(second_ids)


def test_recording_refuses_a_comparison_not_established_from_its_inputs(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    second = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
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
            compared, workspace_id="w", session_id="s1", comparison=forged
        )


def test_recorded_assertion_stream_obeys_sessions_and_boundary(compared):
    finding = _by_right(compared)["word"]
    first = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    boundary = compared.capture_boundary()
    record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    record_measured_count(
        compared, workspace_id="w", session_id="s2", finding=finding
    )

    reconstructed = list(
        iter_recorded_measured_assertions(
            compared,
            workspace_id="w",
            session_ids=("s1",),
            through=boundary,
        )
    )
    assert len(reconstructed) == 5
    assert {assertion.yielding_event_id for assertion in reconstructed} == {first.id}


def test_exact_sets_keep_completeness_separate_from_support(compared):
    finding = _by_right(compared)["word"]
    assertions = {
        assertion.result: assertion
        for assertion in assertions_from_measured_count(finding)
    }
    boundary = {"commitment": finding.input_ledger_boundary.commitment}

    for result in (
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
    ):
        encoded = assertions[result].to_json_dict()
        assert encoded["completeness_boundary"] == boundary
        assert encoded["completeness_scope"]["workspace_id"] == "w"
        assert encoded["completeness_scope"]["session_ids"] == list(DECLARED)
        assert encoded["completeness_scope"]["requires_session_existence"] is True
        assert finding.input_ledger_boundary.commitment not in (
            encoded["support_basis"]["event_ids"]
            + encoded["support_basis"]["local_assertion_ids"]
        )

    assert assertions["measured_in"].support_event_ids
    assert assertions["measured_in"].completeness_occurrence_kinds == (
        "operator.measurement.comparison_recorded",
    )
    assert assertions["measured_without_distinction"].support_event_ids
    assert assertions[
        "measured_without_distinction"
    ].completeness_occurrence_kinds == (
        MEASUREMENT_RECORDED_KIND,
        "operator.measurement.comparison_recorded",
    )
    assert assertions["coordinate_not_measured"].support_event_ids == ()
    assert assertions["coordinate_not_measured"].completeness_occurrence_kinds == (
        MEASUREMENT_RECORDED_KIND,
    )


def test_count_and_recurrence_stand_on_assertions_not_raw_events(compared):
    assertions = assertions_from_measured_count(_by_right(compared)["word"])
    by_result = {assertion.result: assertion for assertion in assertions}

    assert by_result["count"].support_event_ids == ()
    assert by_result["count"].support_assertion_ids == (
        by_result["measured_in"].identity,
    )
    assert by_result["count"].completeness_boundary is None
    assert by_result["recurrence"].support_event_ids == ()
    assert by_result["recurrence"].support_assertion_ids == (
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
    other_workspace = replace(finding, workspace_id="another-workspace")

    identities = [
        {
            assertion.result: assertion.identity
            for assertion in assertions_from_measured_count(candidate)
        }
        for candidate in (finding, scoped, ruled, other_workspace)
    ]
    for result in identities[0]:
        assert len({identified[result] for identified in identities}) == 4
        assert all(
            identified[result].startswith("measured-assertion:")
            for identified in identities
        )


def test_measuring_without_any_comparison_is_refused():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO("a word\nexit\n"), output_stream=StringIO())
    with pytest.raises(RecurrenceMeasurementError, match="not preserved material"):
        measure_exchange_counts(
            ledger, workspace_id="w",
            bounded_exchanges=["s"])


def test_declaring_an_exchange_does_not_establish_it(compared):
    """`#2431` accepted any name and placed it in coordinate_not_measured.

    Declaring the Scope chooses among established exchanges. It cannot create
    one by naming it — the caller-side twin of the workspace sweeping `#2431`
    had just removed.
    """
    with pytest.raises(RecurrenceMeasurementError, match="no recorded occurrence"):
        measure_exchange_counts(
            compared, workspace_id="w",
            bounded_exchanges=DECLARED + ("ghost",))


def test_a_named_exchange_cannot_enter_the_third_result_unestablished(compared):
    """The exact consequence: a ghost would have been counted as not measuring.

    The refusal is what this asserts. `#2432` followed it with
    ``all(f.bounded_exchanges == ("s1",) for f in findings)`` over a
    single-exchange declaration, which returns no findings at all — every
    comparison involving `s1` has its other input outside the declared Scope
    and is correctly rejected — so `all([])` passed and established nothing.
    """
    with pytest.raises(RecurrenceMeasurementError, match="ghost"):
        measure_exchange_counts(
            compared, workspace_id="w", bounded_exchanges=("s1", "ghost"))


def test_a_declaration_of_established_exchanges_is_accepted(compared):
    """Existence validation passing, asserted on a result that exists."""
    findings = measure_exchange_counts(
        compared, workspace_id="w", bounded_exchanges=("s1", "s2"))
    assert findings
    assert all(f.bounded_exchanges == ("s1", "s2") for f in findings)


def test_declaring_one_exchange_yields_no_findings_and_that_is_not_a_pass(compared):
    """Recorded because it is what made the vacuous assertion look green.

    A comparison has as input two exchanges. Declaring one leaves every comparison
    with an undeclared input, so nothing contributes. That is correct behaviour
    and an empty result, which no assertion over the result can witness.
    """
    assert measure_exchange_counts(
        compared, workspace_id="w", bounded_exchanges=("s1",)) == []


# --------------------------------------------------------------------------
# The whole declared identity governs grouping.
# --------------------------------------------------------------------------


def test_the_declared_identity_includes_the_counting_scope(compared):
    """`#2429` grouped on left, rule and position, then said "and scope"."""
    assert "counting_scope" in DECLARED_IDENTITY
    assert "representation_measured" in DECLARED_IDENTITY
    assert "measurement_form" in DECLARED_IDENTITY
    declared = dict(_by_right(compared)["word"].distinction.declared)
    assert set(declared) == set(DECLARED_IDENTITY)
    assert declared["counting_scope"] == SCOPE


def test_measurements_declaring_different_scopes_do_not_group(compared):
    """Two measurements under different declared scopes are not the same one."""
    other = {}
    for session_id in ("s1", "s2"):
        occ = preserved_ingress_occurrences(
            compared, workspace_id="w", session_id=session_id)
        other[session_id] = record_measurement_finding(
            compared, workspace_id="w", session_id=session_id,
            finding=measure_after(occ, "a", counting_scope="a different scope")).id
    _compare_all(compared, other)

    scopes = {
        dict(f.distinction.declared)["counting_scope"]
        for f in measure_exchange_counts(compared, workspace_id="w", bounded_exchanges=DECLARED)
        if f.distinction.right_representation == "word"
    }
    assert scopes == {SCOPE, "a different scope"}
    counts = {
        dict(f.distinction.declared)["counting_scope"]: f.exchange_count
        for f in measure_exchange_counts(compared, workspace_id="w", bounded_exchanges=DECLARED)
        if f.distinction.right_representation == "word"
    }
    assert counts[SCOPE] == 3            # s1 s2 s3
    assert counts["a different scope"] == 2   # s1 s2 only


# --------------------------------------------------------------------------
# Everything the result stood on travels with it.
# --------------------------------------------------------------------------


def test_participating_measurements_travel_not_only_the_comparisons(compared):
    """`#2429` recorded only comparisons, while using measurements to establish
    two of the three result sets."""
    finding = _by_right(compared)["word"]
    kinds = {compared.get(i).kind for i in finding.input_event_ids}
    assert kinds == {
        "operator.measurement.comparison_recorded",
        MEASUREMENT_RECORDED_KIND,
    }


def test_every_exchange_s_measurement_is_among_the_support(compared):
    finding = _by_right(compared)["word"]
    supporting = {
        compared.get(i).session_id
        for i in finding.input_event_ids
        if compared.get(i).kind == MEASUREMENT_RECORDED_KIND
    }
    assert supporting == set(finding.bounded_exchanges)


def test_the_input_ledger_boundary_is_preserved_as_read_provenance(compared):
    boundary = compared.capture_boundary()
    finding = _by_right(compared)["word"]

    assert finding.input_ledger_boundary == boundary
    assert finding.to_json_dict()["input_ledger_boundary"] == {
        "commitment": boundary.commitment,
    }
    recorded = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding
    )
    assert "input_ledger_boundary" not in recorded.payload
    assertions = _assertions_by_result(recorded)
    for result in (
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
    ):
        assert assertions[result]["completeness_boundary"] == {
            "commitment": boundary.commitment,
        }


def test_the_old_aggregate_result_is_not_recorded_beside_the_assertions(compared):
    event = record_measured_count(
        compared,
        workspace_id="w",
        session_id="s1",
        finding=_by_right(compared)["word"],
    )
    old_aggregate_fields = {
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
        "exchange_count",
        "recurrence_established",
        "bounded_exchanges",
        "input_event_ids",
        "input_ledger_boundary",
        "workspace_id",
        "distinction",
    }
    assert old_aggregate_fields.isdisjoint(event.payload)


# --------------------------------------------------------------------------
# The three results, and what they are called.
# --------------------------------------------------------------------------


def test_it_counts_the_exchanges_the_distinction_recurs_in(compared):
    finding = _by_right(compared)["word"]
    assert finding.exchange_count == 3
    assert finding.measured_in == ("s1", "s2", "s3")


def test_measuring_the_coordinate_without_the_distinction_is_its_own_result(compared):
    finding = _by_right(compared)["word"]
    assert finding.measured_without_distinction == ("s4",)


def test_only_relevant_evidence_places_an_exchange_in_the_second_result(compared):
    """`#2431`'s unrelated-presence support belongs to the third result.

    Exact-coordinate Measurement and Compare/input Evidence establish
    ``measured_without_distinction``. A later measurement of another coordinate
    in the same exchange establishes nothing additional about that result.
    """
    exact_coordinate = next(
        event
        for event in compared.list("w")
        if event.kind == MEASUREMENT_RECORDED_KIND and event.session_id == "s4"
    )
    occurrences = preserved_ingress_occurrences(
        compared, workspace_id="w", session_id="s4"
    )
    unrelated = record_measurement_finding(
        compared,
        workspace_id="w",
        session_id="s4",
        finding=measure_after(occurrences, "nothing", counting_scope=SCOPE),
    )

    finding = _by_right(compared)["word"]

    assert finding.measured_without_distinction == ("s4",)
    assert exact_coordinate.id in finding.input_event_ids
    assert unrelated.id not in finding.input_event_ids


def test_a_count_of_one_is_a_finding_and_is_not_recurrence(compared):
    """`01.Source:28` lists count and recurrence as separate findings.

    `#2430` called this shape RecurrenceFinding and rendered a count of one as
    "recurs in 1 bounded exchanges", asserting recurrence where nothing
    recurred.
    """
    finding = _by_right(compared)["thing"]
    assert finding.measured_in == ("s4",)
    assert finding.exchange_count == 1
    assert finding.recurrence_established is False
    assert "was measured in 1 bounded exchange" in render_measured_count(finding)
    assert "recurs" not in render_measured_count(finding)
    assertions = assertions_from_measured_count(finding)
    assert {assertion.result for assertion in assertions} == {
        "measured_in",
        "measured_without_distinction",
        "coordinate_not_measured",
        "count",
    }


def test_recurrence_is_established_only_above_one(compared):
    finding = _by_right(compared)["word"]
    assert finding.exchange_count == 3
    assert finding.recurrence_established is True
    assert "recurs in 3 bounded exchanges" in render_measured_count(finding)


def _add_s5(ledger):
    """An exchange that measures a different coordinate entirely."""
    run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s5",
        input_stream=StringIO("nothing relevant here\nexit\n"),
        output_stream=StringIO())
    occ = preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s5")
    return record_measurement_finding(
        ledger, workspace_id="w", session_id="s5",
        finding=measure_after(occ, "nothing", counting_scope=SCOPE))


def test_an_exchange_that_never_measured_the_coordinate_is_distinguished(compared):
    _add_s5(compared)
    declared = DECLARED + ("s5",)
    finding = _by_right(compared, declared)["word"]
    assert "s5" in finding.coordinate_not_measured
    assert "s5" not in finding.measured_without_distinction
    assert "s5" not in finding.measured_in


def test_the_third_result_preserves_its_complete_read_not_copied_ids(compared):
    """The ledger boundary reconstructs the complete negative-classification read."""
    unrelated = _add_s5(compared)
    declared = DECLARED + ("s5",)
    finding = _by_right(compared, declared)["word"]

    assert "s5" in finding.coordinate_not_measured
    assert unrelated.id not in finding.input_event_ids
    reconstructed = compared.iter_session_kind(
        "w",
        "s5",
        MEASUREMENT_RECORDED_KIND,
        through=finding.input_ledger_boundary,
    )
    assert unrelated.id in {event.id for event in reconstructed}


def test_an_undeclared_exchange_enters_nothing(compared):
    """`#2430` swept the workspace, so any measurement enlarged the denominator."""
    _add_s5(compared)
    finding = _by_right(compared)["word"]          # s5 not declared
    assert "s5" not in finding.bounded_exchanges
    assert "s5" not in finding.coordinate_not_measured
    assert len(finding.bounded_exchanges) == 4


def test_the_bounded_scope_must_be_declared(compared):
    with pytest.raises(RecurrenceMeasurementError, match="no bounded exchanges were declared"):
        measure_exchange_counts(compared, workspace_id="w", bounded_exchanges=[])


def test_the_three_results_partition_the_bounded_exchanges(compared):
    for finding in measure_exchange_counts(compared, workspace_id="w", bounded_exchanges=DECLARED):
        parts = (
            set(finding.measured_in),
            set(finding.measured_without_distinction),
            set(finding.coordinate_not_measured),
        )
        assert set().union(*parts) == set(finding.bounded_exchanges)
        assert sum(len(p) for p in parts) == len(finding.bounded_exchanges)


# --------------------------------------------------------------------------
# What the record says, and refuses.
# --------------------------------------------------------------------------


def test_the_counting_scope_states_the_declaration(compared):
    """`#2429` said "supplied to this Seed"; `#2430` said what it input.

    Neither was the bounded scope `01.Source:28` requires disclosed, because
    both described a set the act discovered rather than one it was given.
    """
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    scope = event.payload["counting_scope"]
    assert "declared to this measurement" in scope
    assert "no exchange enters by having measured something else" in scope
    assert "supplied to this Seed" not in scope


def test_the_record_refuses_source_independence_and_corroboration(compared):
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    refused = " ".join(event.payload["forbidden_inferences"])
    assert "independently preserved is not independent" in refused
    assert "repetition is not independent corroboration" in refused
    assert "establishes no relation between the" in refused
    assert set(FORBIDDEN_INFERENCES) <= set(event.payload["forbidden_inferences"])


def test_the_rendering_states_the_literal_sentence(compared):
    rendered = render_measured_count(_by_right(compared)["word"])
    assert "recurs in 3 bounded exchanges" in rendered
    assert SCOPE in rendered
    for word in ("agree", "corroborat", "independent source", "relation",
                 "confirm", "prove", "cohort", "population"):
        assert word not in rendered.lower()


def test_the_vocabulary_is_gone(compared):
    """`cohort`, `population`, `body`, `survey`, `exposed` earned no place."""
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    rendered = str(event.payload).lower()
    for word in ("cohort", "population", "survey", "exposed", "bodies"):
        assert word not in rendered


# --------------------------------------------------------------------------
# A bounded exchange is the recorded session, and validating one is bounded.
# --------------------------------------------------------------------------


def test_a_payload_string_cannot_manufacture_an_exchange(compared):
    """`#2432` established existence from `dimensions.scope_locality`.

    That coordinate's represented relation is itself left Unknown by the same report, and a
    record can say anything in it. The recorded session boundary is the witness.
    """
    compared.append(
        "operator.measurement.finding_recorded", "w",
        {"dimensions": {"scope_locality": "workspace:w;session:ghost"}},
        session_id="s1",
    )
    with pytest.raises(RecurrenceMeasurementError, match="no recorded occurrence"):
        measure_exchange_counts(
            compared, workspace_id="w", bounded_exchanges=DECLARED + ("ghost",))


def test_durable_validation_does_not_read_the_whole_workspace(tmp_path):
    """`#2416` removed this shape and measured 20x; it must not return.

    Asserted on the durable ledger, where `list_session` is an indexed query.
    The in-memory ledger implements `list_session` as a comprehension over the
    workspace list, which `#2416` recorded, so it cannot witness this.
    """
    from seed_runtime.events import SQLiteEventLedger

    ledger = SQLiteEventLedger(str(tmp_path / "seed.db"))
    try:
        for session_id, material in EXCHANGES.items():
            run_persistent_operator_console(
                ledger=ledger, workspace_id="w", session_id=session_id,
                input_stream=StringIO(material + "exit\n"),
                output_stream=StringIO())
        findings = {}
        for session_id in EXCHANGES:
            occ = preserved_ingress_occurrences(
                ledger, workspace_id="w", session_id=session_id)
            findings[session_id] = record_measurement_finding(
                ledger, workspace_id="w", session_id=session_id,
                finding=measure_after(occ, "a", counting_scope=SCOPE)).id
        _compare_all(ledger, findings)

        statements = []
        ledger._connection.set_trace_callback(statements.append)
        measure_exchange_counts(
            ledger, workspace_id="w", bounded_exchanges=DECLARED)
        ledger._connection.set_trace_callback(None)
    finally:
        ledger.close()

    selects = [q for q in statements if q.strip().upper().startswith("SELECT *")]
    assert selects, "the measurement read something"
    for query in selects:
        assert "session_id" in query, query
        assert "kind" in query, query
        assert "FROM events WHERE workspace_id" in query, query
    # Two passes name each session and exact relevant kind; none sweeps the
    # workspace or materialises irrelevant occurrences.
    assert len(selects) == 2 * len(DECLARED)
    assert sum(
        MEASUREMENT_RECORDED_KIND in query for query in selects
    ) == len(DECLARED)
    assert sum(
        "operator.measurement.comparison_recorded" in query for query in selects
    ) == len(DECLARED)


def test_comparison_events_are_folded_without_being_retained(compared):
    """The resource boundary is one streamed comparison, not all comparisons."""
    import gc
    import weakref

    references = []
    live_counts = []
    original_iterator = compared.iter_session_kind

    def tracked_iterator(workspace_id, session_id, kind, *, through=None):
        for stored in original_iterator(
            workspace_id, session_id, kind, through=through
        ):
            if kind != "operator.measurement.comparison_recorded":
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

    compared.iter_session_kind = tracked_iterator
    measure_exchange_counts(
        compared, workspace_id="w", bounded_exchanges=DECLARED
    )
    gc.collect()

    assert references
    assert max(live_counts) <= 1
    assert all(reference() is None for reference in references)


def test_every_probe_and_pass_reads_one_prefix_despite_a_concurrent_append(compared):
    boundary = compared.capture_boundary()
    original_has_session = compared.has_session
    original_iterator = compared.iter_session_kind
    seen_boundaries = []
    appended = False

    comparison = next(
        event
        for event in compared.list("w")
        if event.kind == "operator.measurement.comparison_recorded"
    )
    payload = comparison.model_copy(deep=True).payload
    payload["shared_occupants"] = [
        *payload.get("shared_occupants", []),
        "after-boundary",
    ]

    def tracked_has_session(workspace_id, session_id, *, through=None):
        seen_boundaries.append(through)
        return original_has_session(
            workspace_id, session_id, through=through
        )

    def tracked_iterator(workspace_id, session_id, kind, *, through=None):
        nonlocal appended
        seen_boundaries.append(through)
        if not appended:
            appended = True
            compared.append(
                comparison.kind,
                comparison.workspace_id,
                payload,
                actor=comparison.actor,
                session_id=comparison.session_id,
                causation_id=comparison.causation_id,
                correlation_id=comparison.correlation_id,
            )
        yield from original_iterator(
            workspace_id, session_id, kind, through=through
        )

    compared.has_session = tracked_has_session
    compared.iter_session_kind = tracked_iterator
    findings = measure_exchange_counts(
        compared, workspace_id="w", bounded_exchanges=DECLARED
    )

    assert appended is True
    assert seen_boundaries
    assert set(seen_boundaries) == {boundary}
    assert all(finding.input_ledger_boundary == boundary for finding in findings)
    assert "after-boundary" not in {
        finding.distinction.right_representation for finding in findings
    }


# --------------------------------------------------------------------------
# The occurrence-to-result edge remains exactly reconstructible.
# --------------------------------------------------------------------------


def test_a_durable_yielding_occurrence_is_identifiable_and_verifies(tmp_path):
    """Historical yield Evidence remains occurrence-bound.

    The yielding occurrence is the event carrying the payload, so its own id
    cannot appear inside that payload. What must hold is that the enclosing
    occurrence is exactly identifiable and verifiable once appended.
    """
    from seed_runtime.events import VERIFIED, SQLiteEventLedger

    path = str(tmp_path / "seed.db")
    ledger = SQLiteEventLedger(path)
    try:
        for session_id, material in EXCHANGES.items():
            run_persistent_operator_console(
                ledger=ledger, workspace_id="w", session_id=session_id,
                input_stream=StringIO(material + "exit\n"),
                output_stream=StringIO())
        findings = {}
        for session_id in EXCHANGES:
            occ = preserved_ingress_occurrences(
                ledger, workspace_id="w", session_id=session_id)
            findings[session_id] = record_measurement_finding(
                ledger, workspace_id="w", session_id=session_id,
                finding=measure_after(occ, "a", counting_scope=SCOPE)).id
        _compare_all(ledger, findings)
        counted = measure_exchange_counts(
            ledger, workspace_id="w", bounded_exchanges=DECLARED)
        event = record_measured_count(
            ledger, workspace_id="w", session_id="s1", finding=counted[0])
        boundary = ledger.capture_boundary()

        assert ledger.get(event.id).id == event.id
        assert ledger.integrity_of(event.id) == VERIFIED
    finally:
        ledger.close()

    reopened = SQLiteEventLedger(path)
    try:
        reconstructed = list(
            iter_recorded_measured_assertions(
                reopened,
                workspace_id="w",
                session_ids=("s1",),
                through=boundary,
            )
        )
        assert reconstructed
        assert {assertion.yielding_event_id for assertion in reconstructed} == {
            event.id
        }
        assert get_recorded_measured_assertion(
            reopened,
            yielding_event_id=event.id,
            assertion_id=reconstructed[0].assertion_id,
        ) == reconstructed[0]
    finally:
        reopened.close()


# --------------------------------------------------------------------------
# D has as input C without defeating C.
# --------------------------------------------------------------------------


def test_counting_recurrence_does_not_strengthen_any_comparison(compared):
    """The invariant. `recurs in 15` must never become `15 sources agree`.

    Every comparison this count input still records `Unknown`, and the
    count's own record refuses corroboration in its own words.
    """
    finding = _by_right(compared)["word"]
    input = [compared.get(i) for i in finding.input_event_ids]
    comparisons = [
        e for e in input
        if e.kind == "operator.measurement.comparison_recorded"
    ]
    assert comparisons
    for comparison in comparisons:
        assert comparison.payload["bounded_relation"] == "Unknown"

    event = record_measured_count(
        compared, workspace_id="w", session_id="s1", finding=finding)
    refused = " ".join(event.payload["forbidden_inferences"])
    assert "not independent corroboration" in refused
    assert "establishes no relation between the" in refused
