"""Seed's measurement occurrences become a subject Seed can measure.

`#2396` found that ordered material separates from shuffled material on one
source and not another. Reading the five forms, a reader can see that every one
of them measures exactly one position away, and can therefore suspect that what
separates is dense immediate arrangement.

Seed could not see that. The distance lived in the indexing. A coordinate that
is never recorded cannot be observed to have never varied, so the observation
was available to a reader and to nothing else.

Each measurement now records where it measured, as coordinates. This surveys
those records and reports how many distinct values each coordinate was recorded
with.

**The survey reports variation and proposes nothing.** These tests pin the
restraint as carefully as the result: a coordinate observed with one value is
recorded as a coordinate observed with one value, and the record says in its own
payload that this is neither a defect nor an instruction to vary it. A survey
that recommended would be a reader's conclusion wearing Seed's provenance.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.adjacent_pair_measurement import (
    MEASURED_POSITIONS,
    AdjacentPair,
    enumerate_representations,
    measure_adjacent_pair,
    measure_after,
)
from seed_runtime.events import EventLedger
from seed_runtime.measurement_continuation import continue_measurements
from seed_runtime.measurement_self_survey import (
    SELF_SURVEY_RECORDED_KIND,
    record_self_survey,
    render_survey,
    survey_measured_positions,
    surveyed_occurrences,
)
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    PreservedMaterialMeasurementError,
    measure_occupancy,
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from scripts import seed_local

MATERIAL = (
    "it is a word and it is a thing\n"
    "It is another word\n"
    "and it is not a word\n"
    "it may be a word\n"
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
def exhausted(session):
    occurrences = preserved_ingress_occurrences(
        session, workspace_id="w", session_id="s"
    )
    seed = None
    for representation in enumerate_representations(occurrences):
        finding = measure_after(occurrences, representation, counting_scope=SCOPE)
        if finding.occupancies:
            seed = finding
            break
    record_measurement_finding(
        session, workspace_id="w", session_id="s", finding=seed
    )
    continue_measurements(
        session,
        occurrences,
        workspace_id="w",
        session_id="s",
        counting_scope=SCOPE,
        passes=40,
    )
    return session


# --------------------------------------------------------------------------
# Every measurement now says where it measured.
# --------------------------------------------------------------------------


def test_every_form_states_its_measured_position():
    assert set(MEASURED_POSITIONS) == {
        "after",
        "preceding",
        "following",
        "before_same_right",
        "after_same_left",
    }
    for position in MEASURED_POSITIONS.values():
        assert set(position) == {"anchored_on", "direction", "displacement"}


def test_a_recorded_finding_carries_where_it_measured(session):
    occurrences = preserved_ingress_occurrences(
        session, workspace_id="w", session_id="s"
    )
    event = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_after(occurrences, "it", counting_scope=SCOPE),
    )
    assert event.payload["measured_position"] == MEASURED_POSITIONS["after"]


def test_the_pair_forms_record_their_own_positions(session):
    occurrences = preserved_ingress_occurrences(
        session, workspace_id="w", session_id="s"
    )
    seed = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_after(occurrences, "it", counting_scope=SCOPE),
    )
    findings = measure_adjacent_pair(
        occurrences,
        AdjacentPair("it", "is"),
        counting_scope=SCOPE,
        premise_event_id=seed.id,
    )
    for name, finding in findings.items():
        assert finding.declared.measured_position == MEASURED_POSITIONS[name]


# --------------------------------------------------------------------------
# The survey's subject is Seed's own occurrences.
# --------------------------------------------------------------------------


def test_the_survey_measures_recorded_occurrences_not_material(exhausted):
    surveyed = surveyed_occurrences(exhausted, workspace_id="w", session_id="s")
    assert surveyed
    assert all(event.kind == MEASUREMENT_RECORDED_KIND for event in surveyed)


def test_a_finding_that_states_no_position_is_not_surveyed(session):
    occurrences = preserved_ingress_occurrences(
        session, workspace_id="w", session_id="s"
    )
    record_measurement_finding(
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
    assert surveyed_occurrences(session, workspace_id="w", session_id="s") == []
    with pytest.raises(PreservedMaterialMeasurementError):
        survey_measured_positions(session, workspace_id="w", session_id="s")


# --------------------------------------------------------------------------
# What the survey found.
# --------------------------------------------------------------------------


def test_the_survey_counts_distinct_values_per_coordinate(exhausted):
    variations = {
        v.coordinate: v
        for v in survey_measured_positions(
            exhausted, workspace_id="w", session_id="s"
        )
    }
    assert set(variations) == {"anchored_on", "direction", "displacement"}
    assert variations["direction"].varied
    assert variations["anchored_on"].varied


def test_one_coordinate_was_recorded_with_a_single_value(exhausted):
    """The observation a reader could make and Seed could not."""
    variations = {
        v.coordinate: v
        for v in survey_measured_positions(
            exhausted, workspace_id="w", session_id="s"
        )
    }
    displacement = variations["displacement"]
    assert not displacement.varied
    assert displacement.values == ("1",)
    # Every surveyed occurrence, not a sample of them.
    assert displacement.occurrence_count == len(
        surveyed_occurrences(exhausted, workspace_id="w", session_id="s")
    )


def test_the_survey_is_recorded_in_the_shape_of_what_it_measured(exhausted):
    """It counted coordinate values, so it records coordinate values.

    An earlier version forced each coordinate through `Occupancy` as
    ``representation="displacement=1"``. Nothing occupied a measured position
    there, and borrowing that vocabulary made the record claim a kind of thing
    it is not. A downstream shape does not decide an upstream subject.
    """
    event = record_self_survey(
        exhausted,
        workspace_id="w",
        session_id="s",
        variations=survey_measured_positions(
            exhausted, workspace_id="w", session_id="s"
        ),
    )
    assert event.kind == SELF_SURVEY_RECORDED_KIND
    assert event.kind != MEASUREMENT_RECORDED_KIND
    assert event.payload["surveyed_subject"] == "recorded measurement occurrences"
    assert "occupancies" not in event.payload
    assert "positions_measured" not in event.payload

    by_name = {c["coordinate"]: c for c in event.payload["coordinates"]}
    assert by_name["displacement"]["observed_values"] == ["1"]
    assert by_name["displacement"]["distinct_value_count"] == 1
    assert by_name["displacement"]["occurrences_carrying_it"] == len(
        surveyed_occurrences(exhausted, workspace_id="w", session_id="s")
    )

    authority = event.payload["dimensions"]["authority_warrant"]
    assert "measurement evidence only" in authority
    assert event.payload["coordinates_observed_with_one_value"] == ["displacement"]
    assert event.payload["coordinates_observed_with_several"] == [
        "anchored_on",
        "direction",
    ]


def test_the_survey_does_not_appear_as_a_positional_measurement(exhausted):
    """A survey of measurements must not be counted as one of them."""
    before = len(surveyed_occurrences(exhausted, workspace_id="w", session_id="s"))
    record_self_survey(
        exhausted,
        workspace_id="w",
        session_id="s",
        variations=survey_measured_positions(
            exhausted, workspace_id="w", session_id="s"
        ),
    )
    assert (
        len(surveyed_occurrences(exhausted, workspace_id="w", session_id="s"))
        == before
    )


# --------------------------------------------------------------------------
# The restraint, pinned as carefully as the result.
# --------------------------------------------------------------------------


def test_the_record_refuses_to_recommend(exhausted):
    """A survey that recommended would be a reader's conclusion in Seed's voice."""
    event = record_self_survey(
        exhausted,
        workspace_id="w",
        session_id="s",
        variations=survey_measured_positions(
            exhausted, workspace_id="w", session_id="s"
        ),
    )
    assert event.payload["forbidden_inference"] == (
        "a coordinate observed with one value is not thereby a defect, "
        "a degree of freedom, or an instruction to vary it"
    )
    rendered = str(event.payload)
    for word in ("should", "recommend", "try", "instead", "better", "wider"):
        assert word not in rendered.lower()


def test_varied_reports_observation_not_possibility(exhausted):
    """`varied` says what was seen, never what could have been."""
    for variation in survey_measured_positions(
        exhausted, workspace_id="w", session_id="s"
    ):
        assert variation.varied == (len(variation.values) > 1)


def test_the_rendering_states_the_counts_and_nothing_else(exhausted):
    rendered = render_survey(
        survey_measured_positions(exhausted, workspace_id="w", session_id="s")
    )
    assert "displacement" in rendered
    assert "distinct values observed" in rendered
    for word in ("should", "only", "never", "problem", "limit"):
        assert word not in rendered.lower()
