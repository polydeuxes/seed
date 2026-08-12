"""A declared measurement over what Seed preserved, recorded so it survives.

Two things separate this from the withdrawn probe at `#2368`.

**What it consumes.** Occurrences come from the ledger, having been recorded
through operator ingress. `#2368` read a file directly, and a measurement over
material Seed never received says nothing about Seed.

**What becomes of the result.** Findings are appended to the ledger, so a later
responsible act may consume them. `05.Testimony:27` permits a bounded comparison
to consume preserved findings while preserving each input's support basis,
confidence, and standing. A finding that vanishes with the process cannot be
consumed by anything.

`01.External:28` requires three disclosures of any recurrence assertion. They
are required fields here, and an absent one is refused rather than defaulted.

Nothing here establishes meaning. `01.Standing.D` refuses relation standing to
co-presence, and a finding reports co-presence.
"""

from __future__ import annotations

import re
from io import BytesIO, StringIO

from seed_runtime.event import Event
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material
from seed_runtime.preserved_material_measurement import INGRESS_OCCURRED_KIND
from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.preserved_material_measurement import (
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    PreservedMaterialMeasurementError,
    measure_occupancy,
    premise_chain,
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from seed_runtime.operator_console import run_persistent_operator_console

MATERIAL = (
    "_The_ is the definite article.\n"
    "_Best_ is a common adjective.\n"
    "_And_, is a conjunction.\n"
    "plain prose carrying no delimiter\n"
    "_Most_ is an adverb.\n"
)
DELIMITED = re.compile(r"^_([^_]{1,40})_(.*)$")


def _first_word(text):
    parts = text.split()
    return parts[0] if parts else None


def _after_delimiter(text):
    match = DELIMITED.match(text)
    if not match:
        return None
    tail = match.group(2).strip(" ,")
    return tail.split(" ")[0] if tail else None


def _declared(**overrides):
    base = {
        "representation_measured": "the first representation of each occurrence",
        "equivalence_rule": "byte-for-byte equality; no normalization",
        "counting_scope": "preserved ingress occurrences of this session",
    }
    return DeclaredMeasurement(**{**base, **overrides})


@pytest.fixture
def session():
    ledger = EventLedger()
    run_persistent_operator_console(
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


# --------------------------------------------------------------------------
# What is measured is what Seed preserved.
# --------------------------------------------------------------------------


def test_the_material_measured_is_the_session_s_own_occurrences(occurrences):
    assert len(occurrences) == 5
    assert all(
        event.payload["dimensions"]["authority_warrant"]
        == "occurrence-only; meaning Unknown"
        for event in occurrences
    )


def test_nothing_but_a_preserved_ingress_occurrence_may_be_measured(session):
    foreign = session.append("unrelated.kind", "w", {"decoded_text": "x"}, session_id="s")
    with pytest.raises(PreservedMaterialMeasurementError):
        measure_occupancy([foreign], declared=_declared(), occupant_of=_first_word)


def test_a_finding_names_every_occurrence_it_consumed(occurrences):
    finding = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_first_word
    )
    assert finding.consumed_event_ids == tuple(e.id for e in occurrences)


def test_an_absent_position_is_absent_not_unknown(occurrences):
    """One line carries no delimiter; it is skipped, not counted as Unknown."""
    finding = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_after_delimiter
    )
    assert finding.positions_measured == 4
    assert len(finding.consumed_event_ids) == 5


# --------------------------------------------------------------------------
# 01.External:28's three disclosures are required.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "missing", ("representation_measured", "equivalence_rule", "counting_scope")
)
def test_a_measurement_without_its_disclosures_is_refused(missing):
    with pytest.raises(PreservedMaterialMeasurementError):
        _declared(**{missing: "   "})


def test_the_disclosures_are_carried_on_the_recorded_finding(session, occurrences):
    finding = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_first_word
    )
    event = record_measurement_finding(
        session, workspace_id="w", session_id="s", finding=finding
    )
    for key in ("representation_measured", "equivalence_rule", "counting_scope"):
        assert event.payload[key].strip()


# --------------------------------------------------------------------------
# The finding survives, and what it stood on survives with it.
# --------------------------------------------------------------------------


def test_a_recorded_finding_is_consumable_by_a_later_act(session, occurrences):
    finding = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_first_word
    )
    event = record_measurement_finding(
        session, workspace_id="w", session_id="s", finding=finding
    )
    recovered = session.get(event.id)
    assert recovered is not None
    assert recovered.kind == MEASUREMENT_RECORDED_KIND
    assert recovered.payload["occupancies"]


def test_a_finding_standing_on_another_preserves_which(session, occurrences):
    first = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences, declared=_declared(), occupant_of=_first_word
        ),
    )
    second = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences,
            declared=_declared(premise_event_id=first.id),
            occupant_of=_after_delimiter,
        ),
    )
    assert second.payload["premise_event_id"] == first.id
    assert first.id in second.payload["lineage"]
    assert premise_chain(session, second.id) == [first.id]


def test_a_premise_must_itself_be_a_recorded_finding(session, occurrences):
    finding = measure_occupancy(
        occurrences,
        declared=_declared(premise_event_id="evt_absent"),
        occupant_of=_first_word,
    )
    with pytest.raises(PreservedMaterialMeasurementError):
        record_measurement_finding(
            session, workspace_id="w", session_id="s", finding=finding
        )


def test_a_finding_without_a_premise_records_none(session, occurrences):
    event = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences, declared=_declared(), occupant_of=_first_word
        ),
    )
    assert event.payload["premise_event_id"] is None
    assert premise_chain(session, event.id) == []


# --------------------------------------------------------------------------
# The ladder, and what it does not become.
# --------------------------------------------------------------------------


def test_a_premise_that_bounds_a_position_sharpens_the_next_finding(occurrences):
    """`#2387`'s measured result, at this module's scale.

    This is not a claim that premises always sharpen. It records that the
    same material measured at two representations yields different concentrations.
    """
    unbounded = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_first_word
    )
    bounded = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_after_delimiter
    )
    assert unbounded.highest_count_occupancy.occurrence_count / unbounded.positions_measured < 0.5
    assert bounded.highest_count_occupancy.representation == "is"
    assert bounded.highest_count_occupancy.occurrence_count / bounded.positions_measured == 1.0


def test_the_recorded_authority_states_the_clause_s_own_limit(session, occurrences):
    event = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences, declared=_declared(), occupant_of=_after_delimiter
        ),
    )
    authority = event.payload["dimensions"]["authority_warrant"]
    assert "measurement evidence only" in authority
    assert "no meaning, relation" in authority
    assert event.payload["unknowns"] == [
        "what any measured representation means remains Unknown"
    ]


def test_the_finding_disclaims_what_a_dominant_occupant_is_not(session, occurrences):
    event = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences, declared=_declared(), occupant_of=_after_delimiter
        ),
    )
    notes = " ".join(event.payload["boundary_notes"])
    assert "is not the meaning of that position" in notes
    assert "establishes no relation" in notes
    assert "not stronger than a finding without one" in notes


def test_recording_a_finding_does_not_disturb_the_measured_occurrences(
    session, occurrences
):
    before = [(e.id, e.payload["decoded_text"]) for e in occurrences]
    record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences, declared=_declared(), occupant_of=_first_word
        ),
    )
    after = preserved_ingress_occurrences(session, workspace_id="w", session_id="s")
    assert [(e.id, e.payload["decoded_text"]) for e in after] == before


def test_material_without_a_text_representation_is_refused_not_skipped():
    """A text measurement over a population containing non-text refuses.

    Skipping would silently narrow the counting scope the finding goes on to
    disclose, and a population measured is not a population partly measured. A
    selection admitting only text-representable material is its own declared
    scope and does not exist yet.
    """

    ledger = EventLedger()
    sink = StringIO()
    for material in (b"the cat jumped\n", b"\xff\xfe\x00binary\n", b"the fence\n"):
        run_operator_ingress_attempt(
            ledger=ledger,
            workspace_id="w",
            session_id="s",
            captured_ingress=capture_stdin_material(BytesIO(material)),
            output_stream=sink,
        )
    occurrences = preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s")

    # All three occurred, and each says whose material it is.
    assert len(occurrences) == 3
    assert {event.payload["material_origin"] for event in occurrences} == {"operator"}
    available = [
        event.payload["text_representation"]["available"] for event in occurrences
    ]
    assert available == [True, False, True]
    unrepresented = occurrences[1].payload
    assert "decoded_text" not in unrepresented
    assert unrepresented["byte_count"] == len(b"\xff\xfe\x00binary\n")
    assert unrepresented["text_representation"]["decoder_outcome"] == "bytes_rejected"

    declared = DeclaredMeasurement(
        representation_measured="anything",
        equivalence_rule="byte-for-byte equality; no normalization",
        counting_scope="one bounded exchange",
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="no available text"):
        measure_occupancy(occurrences, declared=declared, occupant_of=lambda text: None)

    # The two that do carry one remain measurable together.
    text_only = [occurrences[0], occurrences[2]]
    finding = measure_occupancy(
        text_only, declared=declared, occupant_of=lambda text: text.split()[0]
    )
    assert finding.positions_measured == 2


def test_an_occurrence_predating_the_coordinate_stays_measurable():
    """Absence of the coordinate is read as what such an occurrence carried."""

    older = Event(
        id="evt_older",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="s",
        payload={"decoded_text": "the cat jumped"},
    )
    declared = DeclaredMeasurement(
        representation_measured="anything",
        equivalence_rule="byte-for-byte equality; no normalization",
        counting_scope="one bounded exchange",
    )
    finding = measure_occupancy(
        [older], declared=declared, occupant_of=lambda text: text.split()[0]
    )
    assert finding.positions_measured == 1

    without_either = Event(
        id="evt_neither",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="s",
        payload={},
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="no available text"):
        measure_occupancy([without_either], declared=declared, occupant_of=lambda t: None)
