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
    occurrences_of_declared_exchanges,
    EXCHANGE_COUNT_RECORDED_KIND,
    FORBIDDEN_INFERENCES,
    RecurrenceMeasurementError,
    measure_exchange_counts,
    record_measured_count,
    render_measured_count,
)
from scripts import seed_local

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

    A comparison consumes two exchanges. Declaring one leaves every comparison
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
        compared.get(i).session_id
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
    assert finding.measured_in == ("s1", "s2", "s3")


def test_measuring_the_coordinate_without_the_distinction_is_its_own_result(compared):
    finding = _by_right(compared)["word"]
    assert finding.measured_without_distinction == ("s4",)


def test_a_count_of_one_is_a_finding_and_is_not_recurrence(compared):
    """`01.External:28` lists count and recurrence as separate findings.

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
    declared = DECLARED + ("s5",)
    finding = _by_right(compared, declared)["word"]
    assert "s5" in finding.coordinate_not_measured
    assert "s5" not in finding.measured_without_distinction
    assert "s5" not in finding.measured_in


def test_what_places_an_exchange_in_the_third_result_travels_as_support(compared):
    """If Evidence changes a field of the result, it participated in it.

    `#2430` cited only occurrences matching the grouped identity, so s5's
    unrelated measurement could place s5 in `coordinate_not_measured` while
    being absent from `consumed_event_ids`.
    """
    unrelated = _add_s5(compared)
    declared = DECLARED + ("s5",)
    finding = _by_right(compared, declared)["word"]
    assert "s5" in finding.coordinate_not_measured
    assert unrelated.id in finding.consumed_event_ids


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


# --------------------------------------------------------------------------
# A bounded exchange is the recorded session, and validating one is bounded.
# --------------------------------------------------------------------------


def test_a_payload_string_cannot_manufacture_an_exchange(compared):
    """`#2432` established existence from `dimensions.scope_locality`.

    That coordinate's meaning is itself left Unknown by the same report, and a
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
            seed_local.run_persistent_operator_console(
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
        assert "FROM events WHERE workspace_id" in query, query
    # every read named a session; none swept the workspace
    assert len(selects) == len(DECLARED)


def test_the_declared_exchanges_bound_what_is_read(compared):
    """Reading two declared exchanges does not deserialize the other two."""
    by_exchange = occurrences_of_declared_exchanges(
        compared, workspace_id="w", bounded_exchanges=("s1", "s2"))
    assert set(by_exchange) == {"s1", "s2"}
    for exchange, events in by_exchange.items():
        assert events
        assert {e.session_id for e in events} == {exchange}


# --------------------------------------------------------------------------
# Producer is not the Responsibility, and not the occurrence either.
# --------------------------------------------------------------------------


def test_a_durable_producing_occurrence_is_identifiable_and_verifies(tmp_path):
    """`#2439` proved producer_evidence existed, not that it identifies one.

    The producing occurrence is the event carrying the payload, so its own id
    cannot appear inside that payload. What must hold is that the enclosing
    occurrence is exactly identifiable and verifiable once appended.
    """
    from seed_runtime.events import VERIFIED, SQLiteEventLedger

    ledger = SQLiteEventLedger(str(tmp_path / "seed.db"))
    try:
        for session_id, material in EXCHANGES.items():
            seed_local.run_persistent_operator_console(
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

        assert ledger.get(event.id).id == event.id
        assert ledger.integrity_of(event.id) == VERIFIED
    finally:
        ledger.close()


def test_the_record_names_a_producer(compared):
    """`#2423` found no production *owner*; owner is not Producer.

    `01.External:31` lists producer beside provenance as its own dimension, so
    the absence of a recovered owner does not remove the Producer.
    """
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.payload["producer"] == "this Seed"
    assert event.payload["producer_evidence"]
    assert "06.Constructors:13" in event.payload["producer_evidence"]


def test_the_producer_is_not_the_producing_occurrence(compared):
    """Collapsing participant into occurrence is the same compression."""
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.payload["producer"] != event.id
    assert event.id not in event.payload["producer"]


def test_the_producer_is_not_the_provenance(compared):
    """`01.Kinds:73`: represented provenance != verified producer occurrence."""
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.payload["producer"] != event.payload["dimensions"][
        "source_provenance"]


def test_the_responsibility_stays_unknown_beside_a_known_producer(compared):
    """The partial shape is ordinary, not contradictory."""
    event = record_measured_count(
        compared, workspace_id="w", session_id="s1",
        finding=_by_right(compared)["word"])
    assert event.payload["producer"] == "this Seed"
    assert event.payload["dimensions"]["responsibility"].startswith("unrecovered")
    assert event.payload["dimensions"]["standing"] == "measured"


# --------------------------------------------------------------------------
# D consumes C without defeating C.
# --------------------------------------------------------------------------


def test_counting_recurrence_does_not_strengthen_any_comparison(compared):
    """The invariant. `recurs in 15` must never become `15 sources agree`.

    Every comparison this count consumed still records `Unknown`, and the
    count's own record refuses corroboration in its own words.
    """
    finding = _by_right(compared)["word"]
    consumed = [compared.get(i) for i in finding.consumed_event_ids]
    comparisons = [
        e for e in consumed
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
