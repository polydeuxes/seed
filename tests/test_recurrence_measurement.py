"""Recurrence across bounded exchanges, measured over Seed's own occurrences.

`#2429` built this and called it a "cohort measurement", writing a Responsibility
into every record that nothing established. `#2351` recovered declared
measurement and said no new act, noun, or grammar is required; recurrence and
count are already its findings. What changed here is the subject, not the Act.

These tests pin the three corrections as carefully as the count: the whole
declared identity governs grouping, every occurrence the result stood on
travels with it, and the counting scope says exactly what was consumed.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.adjacent_pair_measurement import measure_after
from seed_runtime.bounded_testimony_comparison import (
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
    FORBIDDEN_INFERENCES,
    RECURRENCE_RECORDED_KIND,
    RecurrenceMeasurementError,
    measure_recurrence,
    record_recurrence_finding,
    render_recurrence,
)
from scripts import seed_local

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
        seed_local.run_persistent_operator_console(
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


def _by_right(ledger):
    return {
        f.distinction.right_representation: f
        for f in measure_recurrence(ledger, workspace_id="w")
    }


# --------------------------------------------------------------------------
# No new Act. A record shape, and declared measurement.
# --------------------------------------------------------------------------


def test_the_recorded_responsibility_is_declared_measurement(compared):
    """`#2429` wrote cohort-measurement-over-recorded-comparisons here."""
    event = record_recurrence_finding(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.payload["dimensions"]["responsibility"] == "declared-measurement"
    assert "cohort" not in str(event.payload).lower()


def test_the_record_shape_is_its_own(compared):
    event = record_recurrence_finding(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.kind == RECURRENCE_RECORDED_KIND
    assert event.kind != MEASUREMENT_RECORDED_KIND
    assert "occupancies" not in event.payload


def test_measuring_without_any_comparison_is_refused():
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO("a word\nexit\n"), output_stream=StringIO())
    with pytest.raises(RecurrenceMeasurementError, match="not preserved\nmaterial|not preserved material"):
        measure_recurrence(ledger, workspace_id="w")


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
        for f in measure_recurrence(compared, workspace_id="w")
        if f.distinction.right_representation == "word"
    }
    assert scopes == {SCOPE, "a different scope"}
    counts = {
        dict(f.distinction.declared)["counting_scope"]: f.recurrence_count
        for f in measure_recurrence(compared, workspace_id="w")
        if f.distinction.right_representation == "word"
    }
    assert counts[SCOPE] == 3            # s1 s2 s3
    assert counts["a different scope"] == 2   # s1 s2 only


# --------------------------------------------------------------------------
# Everything the result stood on travels with it.
# --------------------------------------------------------------------------


def test_the_consumed_measurements_travel_not_only_the_comparisons(compared):
    """`#2429` recorded only comparisons, while using measurements to establish
    two of the three result sets."""
    finding = _by_right(compared)["word"]
    kinds = {compared.get(i).kind for i in finding.consumed_event_ids}
    assert kinds == {
        "operator.measurement.comparison_recorded",
        MEASUREMENT_RECORDED_KIND,
    }


def test_every_exchange_s_measurement_is_among_the_support(compared):
    finding = _by_right(compared)["word"]
    supporting = {
        compared.get(i).payload["dimensions"]["scope_locality"]
        for i in finding.consumed_event_ids
        if compared.get(i).kind == MEASUREMENT_RECORDED_KIND
    }
    assert supporting == set(finding.bounded_exchanges)


# --------------------------------------------------------------------------
# The three results, and what they are called.
# --------------------------------------------------------------------------


def test_it_counts_the_exchanges_the_distinction_recurs_in(compared):
    finding = _by_right(compared)["word"]
    assert finding.recurrence_count == 3
    assert finding.measured_in == (
        "workspace:w;session:s1",
        "workspace:w;session:s2",
        "workspace:w;session:s3",
    )


def test_measuring_the_coordinate_without_the_distinction_is_its_own_result(compared):
    finding = _by_right(compared)["word"]
    assert finding.measured_without_distinction == ("workspace:w;session:s4",)


def test_recurrence_in_one_exchange_is_still_a_finding(compared):
    finding = _by_right(compared)["thing"]
    assert finding.measured_in == ("workspace:w;session:s4",)
    assert finding.recurrence_count == 1


def test_an_exchange_that_never_measured_the_coordinate_is_distinguished(compared):
    seed_local.run_persistent_operator_console(
        ledger=compared, workspace_id="w", session_id="s5",
        input_stream=StringIO("nothing relevant here\nexit\n"),
        output_stream=StringIO())
    occ = preserved_ingress_occurrences(compared, workspace_id="w", session_id="s5")
    record_measurement_finding(
        compared, workspace_id="w", session_id="s5",
        finding=measure_after(occ, "nothing", counting_scope=SCOPE))

    finding = _by_right(compared)["word"]
    assert "workspace:w;session:s5" in finding.coordinate_not_measured
    assert "workspace:w;session:s5" not in finding.measured_without_distinction
    assert "workspace:w;session:s5" not in finding.measured_in


def test_the_three_results_partition_the_bounded_exchanges(compared):
    for finding in measure_recurrence(compared, workspace_id="w"):
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


def test_the_counting_scope_states_what_was_consumed(compared):
    """`#2429` said "which bodies were supplied to this Seed"."""
    event = record_recurrence_finding(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    scope = event.payload["counting_scope"]
    assert "recorded occurrences this measurement consumed" in scope
    assert "no relevant recorded measurement does not appear here" in scope
    assert "supplied to this Seed" not in scope


def test_the_record_refuses_source_independence_and_corroboration(compared):
    event = record_recurrence_finding(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    refused = " ".join(event.payload["forbidden_inferences"])
    assert "independently preserved is not independent" in refused
    assert "repetition is not independent corroboration" in refused
    assert "establishes no relation between the" in refused
    assert set(FORBIDDEN_INFERENCES) <= set(event.payload["forbidden_inferences"])


def test_the_rendering_states_the_literal_sentence(compared):
    rendered = render_recurrence(_by_right(compared)["word"])
    assert "recurs in 3 bounded exchanges" in rendered
    assert SCOPE in rendered
    for word in ("agree", "corroborat", "independent source", "relation",
                 "confirm", "prove", "cohort", "population"):
        assert word not in rendered.lower()


def test_the_vocabulary_is_gone(compared):
    """`cohort`, `population`, `body`, `survey`, `exposed` earned no place."""
    event = record_recurrence_finding(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    rendered = str(event.payload).lower()
    for word in ("cohort", "population", "survey", "exposed", "bodies"):
        assert word not in rendered
