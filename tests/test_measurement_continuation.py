"""The cycle continues itself, and stops only when it would repeat a question.

`#2392` removed the last supplied representation. One selection remained and it
was ours: after each round a reader looked at the findings and said *measure on
that one next*. These tests pin that nothing does that any more.

A recorded finding now states the form of measurement that produced it and the
exact representations it was performed relative to. Without both, the next
question cannot be formed from it without a reader restating the first, which
is why a finding lacking them is refused as a source of measurements.

**No judgement appears anywhere in the loop.** No count, share, threshold, or
notion of interest decides which finding is continued. An occupancy measured
once yields exactly the same measurements as one measured a thousand times.

**Stopping here is not constitutional Stopping.** A pass forming no measurement
the ledger does not already hold ends the run; that is a harness declining to
ask a finite question twice, and `08.Stopping` is untouched.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.adjacent_pair_measurement import (
    enumerate_representations,
    measure_after,
)
from seed_runtime.events import EventLedger
from seed_runtime.measurement_continuation import (
    PAIR_FORMS,
    SINGLE_FORMS,
    PendingMeasurement,
    continue_measurements,
    measurements_from_finding,
    performed_measurements,
)
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    PreservedMaterialMeasurementError,
    premise_chain,
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from scripts import seed_local

MATERIAL = (
    "it is a word and it is a thing\n"
    "It is another word\n"
    "and it is not a word\n"
    "it may be a word\n"
    "of the word and of the thing\n"
)
SCOPE = "whole session"


@pytest.fixture
def session():
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO(MATERIAL + "exit\n"),
        output_stream=StringIO(),
    )
    return ledger


@pytest.fixture
def occurrences(session):
    return preserved_ingress_occurrences(session, workspace_id="w", session_id="s")


@pytest.fixture
def seeded(session, occurrences):
    """One finding, on a representation the material offered."""
    representation = enumerate_representations(occurrences)[0]
    return record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_after(occurrences, representation, counting_scope=SCOPE),
    )


# --------------------------------------------------------------------------
# A finding states what question produced it.
# --------------------------------------------------------------------------


def test_a_finding_states_its_form_and_what_it_measured_relative_to(seeded):
    assert seeded.payload["measurement_form"] == "after"
    assert seeded.payload["measured_relative_to"] == [
        seeded.payload["measured_left_representation"]
    ]


def test_a_finding_without_that_cannot_form_the_next_question(session, occurrences):
    from seed_runtime.preserved_material_measurement import (
        DeclaredMeasurement,
        measure_occupancy,
    )

    event = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences,
            declared=DeclaredMeasurement(
                representation_measured="the first representation",
                equivalence_rule="byte-for-byte equality; no normalization",
                counting_scope=SCOPE,
            ),
            occupant_of=lambda t: (t.split() or [None])[0],
        ),
    )
    with pytest.raises(PreservedMaterialMeasurementError):
        measurements_from_finding(event)


def test_measurements_are_formed_from_recorded_findings_only(session):
    foreign = session.append("unrelated.kind", "w", {"occupancies": []}, session_id="s")
    with pytest.raises(PreservedMaterialMeasurementError):
        measurements_from_finding(foreign)


# --------------------------------------------------------------------------
# Every occupancy is carried forward. Counts are not reasons.
# --------------------------------------------------------------------------


def test_every_occupancy_yields_every_permitted_form(seeded):
    pending = measurements_from_finding(seeded)
    occupants = [o["representation"] for o in seeded.payload["occupancies"]]
    assert len(pending) == len(occupants) * len(PAIR_FORMS)
    for occupant in occupants:
        formed = {p.form for p in pending if p.relative_to[1] == occupant}
        assert formed == set(PAIR_FORMS)


def test_an_occupancy_measured_once_is_carried_like_any_other(seeded):
    """A count is not a reason, so the loop may not use one as one."""
    pending = measurements_from_finding(seeded)
    counts = {
        o["representation"]: o["occurrence_count"]
        for o in seeded.payload["occupancies"]
    }
    assert min(counts.values()) == 1, "the fixture should contain a single-count occupancy"
    rare = min(counts, key=counts.get)
    common = max(counts, key=counts.get)
    formed = lambda r: {p.form for p in pending if p.relative_to[1] == r}
    assert formed(rare) == formed(common)


def test_a_pair_finding_offers_its_occupancies_as_new_anchors(session, occurrences, seeded):
    rounds = continue_measurements(
        session,
        occurrences,
        workspace_id="w",
        session_id="s",
        counting_scope=SCOPE,
        passes=2,
    )
    pair_findings = [
        event for event in rounds[0] if len(event.payload["measured_relative_to"]) == 2
    ]
    assert pair_findings
    pending = measurements_from_finding(pair_findings[0])
    assert all(len(p.relative_to) == 1 for p in pending)
    assert all(p.form in SINGLE_FORMS for p in pending)


# --------------------------------------------------------------------------
# The loop continues itself, and stops by exhaustion.
# --------------------------------------------------------------------------


def test_the_cycle_runs_without_anyone_choosing_what_to_continue(
    session, occurrences, seeded
):
    rounds = continue_measurements(
        session,
        occurrences,
        workspace_id="w",
        session_id="s",
        counting_scope=SCOPE,
        passes=12,
    )
    assert len(rounds) > 3
    assert sum(len(r) for r in rounds) > 20


def test_it_stops_because_nothing_new_is_formed_not_because_of_a_budget(
    session, occurrences, seeded
):
    rounds = continue_measurements(
        session,
        occurrences,
        workspace_id="w",
        session_id="s",
        counting_scope=SCOPE,
        passes=12,
    )
    assert rounds[-1] == [], "the run should end by exhausting the forms"


def test_a_spent_budget_is_distinguishable_from_exhaustion(
    session, occurrences, seeded
):
    rounds = continue_measurements(
        session,
        occurrences,
        workspace_id="w",
        session_id="s",
        counting_scope=SCOPE,
        passes=1,
    )
    assert rounds[-1] != [], "a budget-limited run must not look exhausted"


def test_the_same_question_is_never_asked_twice(session, occurrences, seeded):
    continue_measurements(
        session,
        occurrences,
        workspace_id="w",
        session_id="s",
        counting_scope=SCOPE,
        passes=12,
    )
    keys = [
        (
            event.payload["measurement_form"],
            tuple(event.payload["measured_relative_to"]),
            event.payload["counting_scope"],
        )
        for event in session.list("w")
        if event.kind == MEASUREMENT_RECORDED_KIND
        and event.payload.get("measurement_form")
    ]
    assert len(keys) == len(set(keys))


def test_a_second_run_over_the_same_ledger_adds_nothing(session, occurrences, seeded):
    continue_measurements(
        session, occurrences, workspace_id="w", session_id="s",
        counting_scope=SCOPE, passes=12,
    )
    before = len(session.list("w"))
    again = continue_measurements(
        session, occurrences, workspace_id="w", session_id="s",
        counting_scope=SCOPE, passes=12,
    )
    assert again == [[]]
    assert len(session.list("w")) == before


def test_a_different_scope_is_a_different_question(session, occurrences, seeded):
    continue_measurements(
        session, occurrences, workspace_id="w", session_id="s",
        counting_scope=SCOPE, passes=12,
    )
    performed = performed_measurements(session, workspace_id="w", session_id="s")
    sample = next(iter(performed))
    assert PendingMeasurement(sample[0], sample[1], seeded.id).key(
        "a different scope"
    ) not in performed


# --------------------------------------------------------------------------
# Depth does not become strength.
# --------------------------------------------------------------------------


def test_every_finding_keeps_the_finding_it_was_formed_from(
    session, occurrences, seeded
):
    rounds = continue_measurements(
        session, occurrences, workspace_id="w", session_id="s",
        counting_scope=SCOPE, passes=12,
    )
    for recorded in rounds:
        for event in recorded:
            assert event.payload["premise_event_id"]
            assert premise_chain(session, event.id)


def test_a_deep_chain_is_still_a_chain_of_counts(session, occurrences, seeded):
    """Depth is provenance, not accumulation."""
    continue_measurements(
        session, occurrences, workspace_id="w", session_id="s",
        counting_scope=SCOPE, passes=12,
    )
    findings = [
        event
        for event in session.list("w")
        if event.kind == MEASUREMENT_RECORDED_KIND
    ]
    depths = {len(premise_chain(session, event.id)) for event in findings}
    assert max(depths) >= 3
    for event in findings:
        authority = event.payload["dimensions"]["authority_warrant"]
        assert "measurement evidence only" in authority
        assert event.payload["unknowns"] == [
            "what any measured representation means remains Unknown"
        ]
