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
    EXCHANGE_COUNT_RECORDED_KIND,
    FORBIDDEN_INFERENCES,
    RecurrenceMeasurementError,
    measure_exchange_counts,
    record_measured_count,
    render_measured_count,
)
from scripts import seed_local

DECLARED = tuple(f"workspace:w;session:{s}" for s in ("s1","s2","s3","s4"))

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


def _by_right(ledger, declared=None):
    return {
        f.distinction.right_representation: f
        for f in measure_exchange_counts(
            ledger, workspace_id="w", bounded_exchanges=declared or DECLARED)
    }


# --------------------------------------------------------------------------
# No new Act. A record shape, and declared measurement.
# --------------------------------------------------------------------------


def test_the_producer_responsibility_stays_unrecovered(compared):
    """`#2429` invented one; `#2430` put the Act in its place.

    `#2423` recovered that declared measurement has no production owner in
    active law — "the act that would produce the finding has no named owner".
    Writing `declared-measurement` there asserts the owner that recovery says
    is absent.
    """
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    responsibility = event.payload["dimensions"]["responsibility"]
    assert responsibility.startswith("unrecovered")
    assert "#2423" in responsibility
    assert responsibility != "declared-measurement"
    assert "cohort" not in str(event.payload).lower()


def test_the_record_shape_is_its_own(compared):
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.kind == EXCHANGE_COUNT_RECORDED_KIND
    assert event.kind != MEASUREMENT_RECORDED_KIND
    assert "occupancies" not in event.payload


def test_measuring_without_any_comparison_is_refused():
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO("a word\nexit\n"), output_stream=StringIO())
    with pytest.raises(RecurrenceMeasurementError, match="not preserved\nmaterial|not preserved material"):
        measure_exchange_counts(ledger, workspace_id="w", bounded_exchanges=DECLARED)


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
    assert finding.exchange_count == 3
    assert finding.measured_in == (
        "workspace:w;session:s1",
        "workspace:w;session:s2",
        "workspace:w;session:s3",
    )


def test_measuring_the_coordinate_without_the_distinction_is_its_own_result(compared):
    finding = _by_right(compared)["word"]
    assert finding.measured_without_distinction == ("workspace:w;session:s4",)


def test_a_count_of_one_is_a_finding_and_is_not_recurrence(compared):
    """`01.External:28` lists count and recurrence as separate findings.

    `#2430` called this shape RecurrenceFinding and rendered a count of one as
    "recurs in 1 bounded exchanges", asserting recurrence where nothing
    recurred.
    """
    finding = _by_right(compared)["thing"]
    assert finding.measured_in == ("workspace:w;session:s4",)
    assert finding.exchange_count == 1
    assert finding.recurrence_established is False
    assert "was measured in 1 bounded exchange" in render_measured_count(finding)
    assert "recurs" not in render_measured_count(finding)


def test_recurrence_is_established_only_above_one(compared):
    finding = _by_right(compared)["word"]
    assert finding.exchange_count == 3
    assert finding.recurrence_established is True
    assert "recurs in 3 bounded exchanges" in render_measured_count(finding)


def _add_s5(ledger):
    """An exchange that measures a different coordinate entirely."""
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s5",
        input_stream=StringIO("nothing relevant here\nexit\n"),
        output_stream=StringIO())
    occ = preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s5")
    return record_measurement_finding(
        ledger, workspace_id="w", session_id="s5",
        finding=measure_after(occ, "nothing", counting_scope=SCOPE))


def test_an_exchange_that_never_measured_the_coordinate_is_distinguished(compared):
    _add_s5(compared)
    declared = DECLARED + ("workspace:w;session:s5",)
    finding = _by_right(compared, declared)["word"]
    assert "workspace:w;session:s5" in finding.coordinate_not_measured
    assert "workspace:w;session:s5" not in finding.measured_without_distinction
    assert "workspace:w;session:s5" not in finding.measured_in


def test_what_places_an_exchange_in_the_third_result_travels_as_support(compared):
    """If Evidence changes a field of the result, it participated in it.

    `#2430` cited only occurrences matching the grouped identity, so s5's
    unrelated measurement could place s5 in `coordinate_not_measured` while
    being absent from `consumed_event_ids`.
    """
    unrelated = _add_s5(compared)
    declared = DECLARED + ("workspace:w;session:s5",)
    finding = _by_right(compared, declared)["word"]
    assert "workspace:w;session:s5" in finding.coordinate_not_measured
    assert unrelated.id in finding.consumed_event_ids


def test_an_undeclared_exchange_enters_nothing(compared):
    """`#2430` swept the workspace, so any measurement enlarged the denominator."""
    _add_s5(compared)
    finding = _by_right(compared)["word"]          # s5 not declared
    assert "workspace:w;session:s5" not in finding.bounded_exchanges
    assert "workspace:w;session:s5" not in finding.coordinate_not_measured
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
    """`#2429` said "supplied to this Seed"; `#2430` said what it consumed.

    Neither was the bounded scope `01.External:28` requires disclosed, because
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
