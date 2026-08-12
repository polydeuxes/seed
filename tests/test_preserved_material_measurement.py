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
    measure_recurrence,
    measure_recurrences,
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


# --------------------------------------------------------------------------
# Recurrence: what is measured is the representation, not a position.
#
# `01.External:28` grants recurrence by name. Until this existed the only
# measurement primitive was positional, which is why every finding Seed had
# ever recorded was about a slot defined relative to a representation rather
# than about a representation.
#
# None of this establishes that the representation is a constitutional
# subject. The recorded identity is still `measurement:<representation>`, a
# subject reference, and `01.External:28` bounds the result to the
# measurement assertion. These tests assert what was measured and what was
# disclosed, and nothing about subject identity or Standing.
# --------------------------------------------------------------------------


RECURRENCE_MATERIAL = (
    "the cat sat on the mat\n"      # "the" twice in one occurrence
    "a dog barked\n"                # "the" absent
    "the end\n"                     # "the" once
)


def _recurrence_ledger():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="r",
        input_stream=StringIO(RECURRENCE_MATERIAL + "exit\n"),
        output_stream=StringIO(),
    )
    return ledger


@pytest.fixture
def recurrence_occurrences():
    ledger = _recurrence_ledger()
    return ledger, preserved_ingress_occurrences(ledger, workspace_id="w", session_id="r")


def _counts(target):
    return lambda text: text.split().count(target)


def _recurrence_declared(target, premise_event_id=None):
    return DeclaredMeasurement(
        representation_measured=target,
        equivalence_rule="exact equality between whitespace-separated tokens",
        counting_scope="preserved operator-ingress occurrences of this session",
        premise_event_id=premise_event_id,
    )


def test_what_is_measured_is_the_representation_not_a_position(recurrence_occurrences):
    _, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences, declared=_recurrence_declared("the"), occurrences_of=_counts("the")
    )
    carried = finding.to_json_dict()
    assert carried["representation_measured"] == "the"
    assert carried["measurement_form"] == "recurrence"
    # No positional coordinate is claimed, because none was measured.
    assert "measured_position" not in carried
    assert "measured_relative_to" not in carried


def test_material_examined_carrying_and_total_are_three_different_counts(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences, declared=_recurrence_declared("the"), occurrences_of=_counts("the")
    )
    # Three occurrences examined; two carry "the"; it occurs three times in all,
    # because the first occurrence carries it twice.
    assert finding.occurrences_examined == 3
    assert finding.occurrences_carrying == 2
    assert finding.total_count == 3


def test_a_representation_that_never_occurs_produces_a_measurement_finding(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences,
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
    )
    assert finding.total_count == 0
    assert finding.occurrences_carrying == 0
    # The scope is still stated: a bounded measurement assertion under the
    # declared rule and scope, not a failure to measure. It establishes no
    # Standing concerning zebra; `01.External:28` bounds it to the assertion.
    assert finding.occurrences_examined == 3
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    assert event.payload["dimensions"]["identity"] == "measurement:zebra"
    assert event.payload["total_count"] == 0


def test_nothing_but_a_preserved_ingress_occurrence_may_be_recurrence_measured(
    recurrence_occurrences,
):
    ledger, _ = recurrence_occurrences
    foreign = ledger.append("unrelated.kind", "w", {"decoded_text": "the"}, session_id="r")
    with pytest.raises(PreservedMaterialMeasurementError, match="preserved ingress"):
        measure_recurrence(
            [foreign], declared=_recurrence_declared("the"), occurrences_of=_counts("the")
        )


def test_material_with_no_available_text_representation_is_refused(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    without_text = Event(
        id="evt_no_text",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="r",
        payload={"text_representation": {"available": False}},
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="no available text"):
        measure_recurrence(
            [without_text],
            declared=_recurrence_declared("the"),
            occurrences_of=_counts("the"),
        )


@pytest.mark.parametrize("bad", [True, False, 1.0, -1, "2", None])
def test_a_count_that_is_not_a_non_negative_integer_is_refused(
    recurrence_occurrences, bad
):
    _, occurrences = recurrence_occurrences
    with pytest.raises(PreservedMaterialMeasurementError, match="non-negative integer"):
        measure_recurrence(
            occurrences,
            declared=_recurrence_declared("the"),
            occurrences_of=lambda text: bad,
        )


def test_a_recurrence_finding_records_through_the_existing_path(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences, declared=_recurrence_declared("the"), occurrences_of=_counts("the")
    )
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND
    assert event.payload["dimensions"]["identity"] == "measurement:the"
    assert event.payload["dimensions"]["standing"] == "measured"
    # The three disclosures `01.External:28` requires all survive recording.
    assert event.payload["representation_measured"] == "the"
    assert event.payload["equivalence_rule"].startswith("exact equality")
    assert event.payload["counting_scope"].startswith("preserved operator-ingress")
    assert event.payload["consumed_event_ids"] == [e.id for e in occurrences]


def test_a_recurrence_finding_may_stand_on_a_premise(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    first = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id="r",
        finding=measure_recurrence(
            occurrences,
            declared=_recurrence_declared("the"),
            occurrences_of=_counts("the"),
        ),
    )
    second = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id="r",
        finding=measure_recurrence(
            occurrences,
            declared=_recurrence_declared("cat", premise_event_id=first.id),
            occurrences_of=_counts("cat"),
        ),
    )
    assert premise_chain(ledger, second.id) == [first.id]


# --------------------------------------------------------------------------
# Measuring many representations across one pass of the material.
#
# Many already-declared representations measured over one bounded occurrence
# population. One at a time, that re-walks and re-splits the whole population
# once per representation. These tests hold the findings identical; the speed
# is measured in the PR, not asserted here.
# --------------------------------------------------------------------------


def _counts_in(declared):
    def counts(text):
        found = {}
        for word in text.split():
            if word in declared:
                found[word] = found.get(word, 0) + 1
        return found
    return counts


def _declared_for(*targets):
    return {t: _recurrence_declared(t) for t in targets}


def test_one_pass_produces_the_same_findings_as_one_at_a_time(recurrence_occurrences):
    _, occurrences = recurrence_occurrences
    targets = ("the", "cat", "a", "zebra")
    declared = _declared_for(*targets)
    batched = measure_recurrences(
        occurrences, declared=declared, counts_in=_counts_in(declared)
    )
    singly = [
        measure_recurrence(
            occurrences, declared=declared[t], occurrences_of=_counts(t)
        )
        for t in targets
    ]
    assert [f.to_json_dict() for f in batched] == [f.to_json_dict() for f in singly]


def test_every_finding_carries_the_same_consumed_population(recurrence_occurrences):
    _, occurrences = recurrence_occurrences
    declared = _declared_for("the", "zebra")
    findings = measure_recurrences(
        occurrences, declared=declared, counts_in=_counts_in(declared)
    )
    population = tuple(e.id for e in occurrences)
    assert all(f.consumed_event_ids == population for f in findings)
    assert all(f.occurrences_examined == len(occurrences) for f in findings)


def test_a_declared_representation_that_never_occurs_still_gets_a_finding(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    declared = _declared_for("the", "zebra")
    findings = {
        f.declared.representation_measured: f
        for f in measure_recurrences(
            occurrences, declared=declared, counts_in=_counts_in(declared)
        )
    }
    assert findings["zebra"].total_count == 0
    assert findings["zebra"].occurrences_examined == 3
    assert findings["the"].total_count == 3


def test_counting_a_representation_that_was_not_declared_is_refused(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="not declared"):
        measure_recurrences(
            occurrences,
            declared=declared,
            counts_in=lambda text: {"the": 1, "undeclared": 1},
        )


def test_a_declaration_must_measure_the_representation_it_is_filed_under(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    with pytest.raises(PreservedMaterialMeasurementError, match="measures"):
        measure_recurrences(
            occurrences,
            declared={"the": _recurrence_declared("cat")},
            counts_in=lambda text: {},
        )


def test_measuring_nothing_is_refused(recurrence_occurrences):
    _, occurrences = recurrence_occurrences
    with pytest.raises(PreservedMaterialMeasurementError, match="at least one"):
        measure_recurrences(occurrences, declared={}, counts_in=lambda text: {})


@pytest.mark.parametrize("bad", [True, 1.0, -1, "2", None])
def test_a_batched_count_must_also_be_a_non_negative_integer(
    recurrence_occurrences, bad
):
    _, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="non-negative integer"):
        measure_recurrences(
            occurrences, declared=declared, counts_in=lambda text: {"the": bad}
        )


def test_counts_must_be_returned_as_a_mapping(recurrence_occurrences):
    _, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="mapping"):
        measure_recurrences(
            occurrences, declared=declared, counts_in=lambda text: [("the", 1)]
        )


def test_the_batch_refuses_the_same_material_the_single_measurement_refuses(
    recurrence_occurrences,
):
    ledger, _ = recurrence_occurrences
    foreign = ledger.append("unrelated.kind", "w", {"decoded_text": "the"}, session_id="r")
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="preserved ingress"):
        measure_recurrences(
            [foreign], declared=declared, counts_in=_counts_in(declared)
        )


# --------------------------------------------------------------------------
# Fidelity of the one-pass batch: what it discloses must be what it did.
# --------------------------------------------------------------------------


def test_one_pass_refuses_declarations_disclosing_different_scopes(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    declared = {
        "the": DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="corpus A",
        ),
        "cat": DeclaredMeasurement(
            representation_measured="cat",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="corpus B",
        ),
    }
    with pytest.raises(PreservedMaterialMeasurementError, match="same counting scope"):
        measure_recurrences(
            occurrences, declared=declared, counts_in=_counts_in(declared)
        )


def test_a_declared_representation_absent_from_the_result_counted_zero(
    recurrence_occurrences,
):
    """Sparse omission is the convention, and it equals an explicit zero."""

    _, occurrences = recurrence_occurrences
    declared = _declared_for("the", "zebra")
    sparse = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=lambda text: {"the": text.split().count("the")}
        if "the" in text.split()
        else {},
    )
    explicit = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=lambda text: {
            "the": text.split().count("the"),
            "zebra": text.split().count("zebra"),
        },
    )
    assert [f.to_json_dict() for f in sparse] == [f.to_json_dict() for f in explicit]


def test_a_finding_preserves_the_localities_it_consumed(recurrence_occurrences):
    """`06.Standing.B`: consumed locality is preserved and stays distinct from
    the locality recorded into."""

    ledger, _ = recurrence_occurrences
    elsewhere = ledger.append(
        INGRESS_OCCURRED_KIND,
        "w",
        {
            "decoded_text": "the other body",
            "material_origin": "operator",
            "text_representation": {"available": True},
        },
        session_id="other",
    )
    here = preserved_ingress_occurrences(ledger, workspace_id="w", session_id="r")
    finding = measure_recurrence(
        list(here) + [elsewhere],
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
    )
    assert finding.consumed_localities == (
        "workspace:w;session:r",
        "workspace:w;session:other",
    )
    # Recorded into a third locality; both coordinates survive, distinctly.
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="recording", finding=finding
    )
    assert event.payload["consumed_localities"] == [
        "workspace:w;session:r",
        "workspace:w;session:other",
    ]
    assert (
        event.payload["dimensions"]["scope_locality"]
        == "workspace:w;session:recording"
    )


def test_an_occurrence_carrying_no_session_locality_asserts_none(
    recurrence_occurrences,
):
    """Absence of the witness is not an asserted locality value."""

    ledger, _ = recurrence_occurrences
    without_session = Event(
        id="evt_no_locality",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        payload={
            "decoded_text": "the cat",
            "material_origin": "operator",
            "text_representation": {"available": True},
        },
    )
    finding = measure_recurrence(
        [without_session],
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
    )
    assert finding.consumed_localities == ("workspace:w",)
    assert "None" not in finding.consumed_localities[0]


def test_batch_and_single_survive_the_recording_boundary_identically(
    recurrence_occurrences,
):
    """Equivalence must hold across preservation, not only serialization."""

    ledger, occurrences = recurrence_occurrences
    targets = ("the", "cat", "zebra")
    declared = _declared_for(*targets)
    singly = [
        record_measurement_finding(
            ledger,
            workspace_id="w",
            session_id="r",
            finding=measure_recurrence(
                occurrences, declared=declared[t], occurrences_of=_counts(t)
            ),
        )
        for t in targets
    ]
    batched = [
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=finding
        )
        for finding in measure_recurrences(
            occurrences, declared=declared, counts_in=_counts_in(declared)
        )
    ]
    # Occurrence identity is the Event id, which is outside the payload, so
    # the payloads themselves must match completely -- lineage included.
    assert [e.payload for e in singly] == [e.payload for e in batched]
