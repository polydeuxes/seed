"""What recurs across the preserved bodies, and every stronger reading refused.

`#2420` recorded the gap this closes: Seed held each pairwise sharing, and the
sentence "appears in 7 of 16 bodies" was a reader's tally over them. The cohort
is a fact about the population of preserved testimony that no single comparison
contains.

The refusals are pinned as carefully as the count. A cohort is repetition, and
`05.Testimony.E` holds that repetition is not independent corroboration.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.adjacent_pair_measurement import measure_after
from seed_runtime.bounded_testimony_comparison import (
    compare_preserved_findings,
    record_comparison_finding,
)
from seed_runtime.cohort_measurement import (
    COHORT_RECORDED_KIND,
    FORBIDDEN_INFERENCES,
    CohortMeasurementError,
    measure_cohorts,
    record_cohort,
    render_cohort,
    surveyed_occurrences,
)
from seed_runtime.events import EventLedger
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from scripts import seed_local

# Four bodies. Three put "word" after "a"; the fourth exposes the coordinate
# and puts "thing" there instead.
BODIES = {
    "s1": "a word is here\n",
    "s2": "a word is there\n",
    "s3": "a word is everywhere\n",
    "s4": "a thing is elsewhere\n",
}
SCOPE = "one bounded exchange"


@pytest.fixture
def compared():
    ledger = EventLedger()
    for session_id, material in BODIES.items():
        seed_local.run_persistent_operator_console(
            ledger=ledger, workspace_id="w", session_id=session_id,
            input_stream=StringIO(material + "exit\n"), output_stream=StringIO())
    findings = {}
    for session_id in BODIES:
        occ = preserved_ingress_occurrences(
            ledger, workspace_id="w", session_id=session_id)
        findings[session_id] = record_measurement_finding(
            ledger, workspace_id="w", session_id=session_id,
            finding=measure_after(occ, "a", counting_scope=SCOPE)).id
    names = sorted(findings)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            record_comparison_finding(
                ledger, workspace_id="w", session_id=a,
                finding=compare_preserved_findings(
                    ledger, [findings[a], findings[b]]))
    return ledger


def _by_right(ledger):
    return {c.distinction.right: c for c in measure_cohorts(ledger, workspace_id="w")}


# --------------------------------------------------------------------------
# Its subject is what Compare recorded.
# --------------------------------------------------------------------------


def test_the_subject_is_recorded_comparisons(compared):
    surveyed = surveyed_occurrences(compared, workspace_id="w")
    assert surveyed
    assert {e.kind for e in surveyed} == {
        "operator.measurement.comparison_recorded"
    }


def test_measuring_without_any_comparison_is_refused():
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO("a word\nexit\n"), output_stream=StringIO())
    with pytest.raises(CohortMeasurementError, match="what Compare recorded"):
        measure_cohorts(ledger, workspace_id="w")


def test_a_cohort_is_not_a_comparison_or_a_measurement(compared):
    cohort = _by_right(compared)["word"]
    event = record_cohort(compared, workspace_id="w", session_id="s1", cohort=cohort)
    assert event.kind == COHORT_RECORDED_KIND
    assert event.kind != MEASUREMENT_RECORDED_KIND
    assert "occupancies" not in event.payload
    assert "shared_occupants" not in event.payload


# --------------------------------------------------------------------------
# The count, and the three-way distinction.
# --------------------------------------------------------------------------


def test_it_counts_the_bodies_that_carried_the_distinction(compared):
    cohort = _by_right(compared)["word"]
    assert cohort.cohort_size == 3
    assert cohort.carried_by == (
        "workspace:w;session:s1",
        "workspace:w;session:s2",
        "workspace:w;session:s3",
    )


def test_exposing_the_coordinate_without_carrying_it_is_its_own_case(compared):
    """s4 measured the same position and put something else there."""
    cohort = _by_right(compared)["word"]
    assert cohort.exposed_without_it == ("workspace:w;session:s4",)
    assert "workspace:w;session:s4" not in cohort.carried_by


def test_not_carrying_and_not_exposing_are_recorded_separately(compared):
    cohort = _by_right(compared)["word"]
    payload = cohort.to_json_dict()
    assert set(payload) >= {
        "carried_by", "exposed_without_it", "coordinate_not_exposed"
    }
    # every body here exposed the coordinate, so the third case is empty and
    # is recorded as empty rather than folded into the second
    assert payload["coordinate_not_exposed"] == []


def test_a_cohort_of_one_is_still_a_cohort(compared):
    """s4 alone puts 'thing' there, and one body carrying it is the finding.

    An earlier form attributed only occupants a comparison found on *both*
    sides, so a distinction held by exactly one body was reported as carried by
    nobody. The size distribution gave it away: 77,663 cohorts of zero and no
    cohorts of one.
    """
    cohort = _by_right(compared)["thing"]
    assert cohort.carried_by == ("workspace:w;session:s4",)
    assert cohort.cohort_size == 1
    assert set(cohort.exposed_without_it) == {
        "workspace:w;session:s1",
        "workspace:w;session:s2",
        "workspace:w;session:s3",
    }


def test_the_consumed_comparisons_travel_with_the_cohort(compared):
    cohort = _by_right(compared)["word"]
    assert cohort.consumed_event_ids
    for event_id in cohort.consumed_event_ids:
        assert compared.get(event_id).kind == "operator.measurement.comparison_recorded"


# --------------------------------------------------------------------------
# Only comparisons that observed the same distinction contribute.
# --------------------------------------------------------------------------


def test_differently_measured_comparisons_do_not_contribute(compared):
    """Two findings measured from different anchors observed different things."""
    occ_a = preserved_ingress_occurrences(compared, workspace_id="w", session_id="s1")
    occ_b = preserved_ingress_occurrences(compared, workspace_id="w", session_id="s2")
    other = record_comparison_finding(
        compared, workspace_id="w", session_id="s1",
        finding=compare_preserved_findings(compared, [
            record_measurement_finding(
                compared, workspace_id="w", session_id="s1",
                finding=measure_after(occ_a, "is", counting_scope=SCOPE)).id,
            record_measurement_finding(
                compared, workspace_id="w", session_id="s2",
                finding=measure_after(occ_b, "a", counting_scope=SCOPE)).id,
        ]))
    assert not [
        d for d in other.payload["distinctions"]
        if d["coordinate"] == "measured_left_representation" and d["same"]
    ]
    # the mismatched comparison contributes nothing to any cohort
    for cohort in measure_cohorts(compared, workspace_id="w"):
        assert other.id not in cohort.consumed_event_ids


# --------------------------------------------------------------------------
# Every stronger reading is refused in the record.
# --------------------------------------------------------------------------


def test_the_record_refuses_source_independence_and_corroboration(compared):
    event = record_cohort(
        compared, workspace_id="w", session_id="s1",
        cohort=_by_right(compared)["word"])
    refused = " ".join(event.payload["forbidden_inferences"])
    assert "independently preserved is not independent" in refused
    assert "repetition is not independent corroboration" in refused
    assert "establishes no relation between the" in refused
    assert set(FORBIDDEN_INFERENCES) <= set(event.payload["forbidden_inferences"])


def test_the_denominator_is_recorded_as_supply_not_as_a_score(compared):
    event = record_cohort(
        compared, workspace_id="w", session_id="s1",
        cohort=_by_right(compared)["word"])
    assert "which bodies were supplied" in event.payload["population_scope"]
    assert "a property of the material" in " ".join(
        event.payload["forbidden_inferences"])
    assert event.payload["population_size"] == 4


def test_the_unknowns_survive_the_count(compared):
    event = record_cohort(
        compared, workspace_id="w", session_id="s1",
        cohort=_by_right(compared)["word"])
    unknowns = " ".join(event.payload["unknowns"])
    assert "means remains Unknown" in unknowns
    assert "stand in any relation remains Unknown" in unknowns
    assert "sources are independent remains Unknown" in unknowns


def test_the_rendering_states_the_literal_sentence(compared):
    rendered = render_cohort(_by_right(compared)["word"])
    assert rendered.startswith("3 independently preserved bodies carry")
    for word in ("agree", "corroborat", "independent source", "relation",
                 "confirm", "prove"):
        assert word not in rendered.lower()


def test_the_third_state_is_proven_not_left_over(compared):
    """Curator's caution, pinned.

    An earlier form computed "coordinate not exposed" as the residue after
    carrying and not-carrying, from comparisons alone. A body whose finding
    exists at the coordinate but which was never compared against a carrier
    falls into that residue and would have been reported as never having
    exposed the coordinate. The recorded measurement occurrences answer it.
    """
    from seed_runtime.cohort_measurement import measured_coordinates

    exposed = measured_coordinates(compared, workspace_id="w")
    keys = [k for k in exposed if k[0] == "a"]
    assert keys, "the measurement occurrences say who measured this coordinate"
    # all four bodies measured after 'a'
    assert len(exposed[keys[0]]) == 4

    cohort = _by_right(compared)["word"]
    # so nothing is 'not exposed', even though only three carried it
    assert cohort.coordinate_not_exposed == ()
    assert len(cohort.carried_by) == 3
    assert len(cohort.exposed_without_it) == 1


def test_a_body_that_never_measured_the_coordinate_is_distinguished(compared):
    """The state that comparisons alone cannot supply."""
    ledger = compared
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s5",
        input_stream=StringIO("nothing relevant here\nexit\n"),
        output_stream=StringIO())
    occ = preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s5")
    # s5 measures a different coordinate entirely, so it joins the population
    record_measurement_finding(
        ledger, workspace_id="w", session_id="s5",
        finding=measure_after(occ, "nothing", counting_scope=SCOPE))

    cohort = _by_right(ledger)["word"]
    assert "workspace:w;session:s5" in cohort.coordinate_not_exposed
    assert "workspace:w;session:s5" not in cohort.exposed_without_it
    assert "workspace:w;session:s5" not in cohort.carried_by


def test_the_three_states_partition_the_population(compared):
    """An invariant, not a coincidence: every body lands in exactly one state.

    On the sixteen-body corpus every cohort sums to sixteen. A cohort where
    they do not sum has lost a body between the recorded measurements and the
    recorded comparisons.
    """
    for cohort in measure_cohorts(compared, workspace_id="w"):
        states = (
            set(cohort.carried_by),
            set(cohort.exposed_without_it),
            set(cohort.coordinate_not_exposed),
        )
        union = set().union(*states)
        assert union == set(cohort.population)
        assert sum(len(s) for s in states) == len(cohort.population)
