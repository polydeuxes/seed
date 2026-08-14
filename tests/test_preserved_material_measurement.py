"""A declared measurement over what Seed preserved, recorded so it survives.

Two things separate this from the withdrawn probe at `#2368`.

**What it has as input.** Occurrences come from the ledger, having been recorded
through operator ingress. `#2368` read a file directly, and a measurement over
material Seed never received says nothing about Seed.

**What becomes of the result.** Findings are appended to the ledger, so a later
responsible act may have them participate. `01.Standing.E` permits a bounded comparison
to have as input preserved findings while preserving each input's support basis,
confidence, and standing. A finding that vanishes with the process cannot be
input by anything.

`01.Source:28` requires three disclosures of any recurrence assertion. They
are required fields here, and an absent one is refused rather than defaulted.

Nothing here establishes represented relation. `01.Standing.D` refuses relation standing to
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
    MATERIAL_AS_SUPPLIED,
    _yielded_content,
    RESPONSIBILITY_UNESTABLISHED,
    MATERIAL_READ_FROM_LEDGER,
    MEASUREMENT_RECORDED_KIND,
    RecurrenceFinding,
    DeclaredMeasurement,
    PreservedMaterialMeasurementError,
    measure_occupancy,
    measure_recurrence,
    measure_recurrences,
    premise_chain,
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from seed_runtime.yield_evidence import YIELD_EVIDENCE_KIND
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.support_basis import (
    SupportBasisError,
    SupportValidator,
    declare_complete_inputs,
)

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
        event.payload["dimensions"]["authority"]
        == "occurrence-only; represented relation Unknown"
        for event in occurrences
    )


def test_nothing_but_a_preserved_ingress_occurrence_may_be_measured(session):
    foreign = session.append("unrelated.kind", "w", {"decoded_text": "x"}, session_id="s")
    with pytest.raises(PreservedMaterialMeasurementError):
        measure_occupancy([foreign], declared=_declared(), occupant_of=_first_word)


def test_a_finding_names_every_occurrence_that_participated(occurrences):
    finding = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_first_word
    )
    assert finding.input_event_ids == tuple(e.id for e in occurrences)


def test_an_absent_position_is_absent_not_unknown(occurrences):
    """One line carries no delimiter; it is skipped, not counted as Unknown."""
    finding = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_after_delimiter
    )
    assert finding.positions_measured == 4
    assert len(finding.input_event_ids) == 5


# --------------------------------------------------------------------------
# 01.Source:28's three disclosures are required.
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


def test_a_recorded_finding_may_participate_in_a_later_act(session, occurrences):
    finding = measure_occupancy(
        occurrences, declared=_declared(), occupant_of=_first_word
    )
    event = record_measurement_finding(
        session, workspace_id="w", session_id="s", finding=finding
    )
    reconstructed = session.get(event.id)
    assert reconstructed is not None
    assert reconstructed.kind == MEASUREMENT_RECORDED_KIND
    assert reconstructed.payload["occupancies"]


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
    assert first.id in second.payload["provenance_occurrence_refs"]
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

    This is not a Assertion that premises always sharpen. It records that the
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
    authority = event.payload["dimensions"]["authority"]
    assert "measurement evidence only" in authority
    assert "no represented relation, relation" in authority
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
    assert "is not the represented relation of that position" in notes
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
    """A text measurement over a inputs containing non-text refuses.

    Skipping would silently narrow the counting scope the finding goes on to
    disclose, and a inputs measured is not a inputs partly measured. A
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
# `01.Source:28` grants recurrence by name. Until this existed the only
# measurement primitive was positional, which is why every finding Seed had
# ever recorded was about a slot defined relative to a representation rather
# than about a representation.
#
# None of this establishes that the representation is a constitutional
# subject. The recorded identity is still `measurement:<representation>`, a
# subject reference, and `01.Source:28` bounds the result to the
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
    # No positional coordinate is asserted, because none was measured.
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


def test_a_representation_that_never_occurs_yields_a_measurement_finding(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences,
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
        yield_in=(ledger, "w", "r"),
    )
    assert finding.total_count == 0
    assert finding.occurrences_carrying == 0
    # The scope is still stated: a bounded measurement assertion under the
    # declared rule and scope, not a failure to measure. It establishes no
    # Standing concerning zebra; `01.Source:28` bounds it to the assertion.
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
        occurrences, declared=_recurrence_declared("the"), occurrences_of=_counts("the"),
        yield_in=(ledger, "w", "r"),
    )
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND
    assert event.payload["dimensions"]["identity"] == "measurement:the"
    assert event.payload["dimensions"]["standing"] == "measured"
    # The three disclosures `01.Source:28` requires all survive recording.
    assert event.payload["representation_measured"] == "the"
    assert event.payload["equivalence_rule"].startswith("exact equality")
    assert event.payload["counting_scope"].startswith("preserved operator-ingress")
    assert event.payload["input_event_ids"] == [e.id for e in occurrences]


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
        yield_in=(ledger, "w", "r"),
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
        yield_in=(ledger, "w", "r"),
    ),
    )
    assert premise_chain(ledger, second.id) == [first.id]


# --------------------------------------------------------------------------
# Measuring many representations across one pass of the material.
#
# Many already-declared representations measured over one bounded occurrence
# inputs. One at a time, that re-walks and re-splits the whole inputs
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


def test_one_pass_yields_the_same_findings_as_one_at_a_time(recurrence_occurrences):
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


def test_every_finding_carries_the_same_participating_inputs(recurrence_occurrences):
    _, occurrences = recurrence_occurrences
    declared = _declared_for("the", "zebra")
    findings = measure_recurrences(
        occurrences, declared=declared, counts_in=_counts_in(declared)
    )
    inputs = tuple(e.id for e in occurrences)
    assert all(f.input_event_ids == inputs for f in findings)
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
# One-pass batch boundary: what it discloses must be what it did.
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


def test_a_finding_preserves_its_participating_localities(recurrence_occurrences):
    """`06.Standing.B`: input locality is preserved and stays distinct from
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
        yield_in=(ledger, "w", "r"),
    )
    assert finding.input_localities == (
        "workspace:w;session:r",
        "workspace:w;session:other",
    )
    # Recorded into a third locality; both coordinates survive, distinctly.
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="recording", finding=finding
    )
    assert event.payload["input_localities"] == [
        "workspace:w;session:r",
        "workspace:w;session:other",
    ]
    assert (
        event.payload["dimensions"]["scope_locality"]
        == "workspace:w;session:recording"
    )


def test_an_occurrence_carrying_no_locality_records_the_absence(
    recurrence_occurrences,
):
    """Absence of the coordinate is preserved, not filled in."""

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
    # No locality was carried, so none is recorded. The workspace is a
    # different member of `06.Standing.A`'s boundary and cannot stand in.
    assert finding.input_localities == (None,)


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
                occurrences, declared=declared[t], occurrences_of=_counts(t),
        yield_in=(ledger, "w", "r"),
    ),
        )
        for t in targets
    ]
    batched = [
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=finding
        )
        for finding in measure_recurrences(
            occurrences, declared=declared, counts_in=_counts_in(declared),
        yield_in=(ledger, "w", "r"),
    )
    ]
    # Occurrence identity is the Event id, which is outside the payload. The
    # one payload coordinate that legitimately differs is `yield_evidence_id`: these
    # are two yields of the same content, and each names its own evidence.
    def _without_its_own_evidence(event):
        payload = dict(event.payload)
        payload.pop("yield_evidence_id", None)
        payload.pop("target_act_id", None)
        payload.pop("act_occurrence_id", None)
        return payload

    assert [_without_its_own_evidence(e) for e in singly] == [
        _without_its_own_evidence(e) for e in batched
    ]


def test_material_declaring_text_it_does_not_carry_is_refused(recurrence_occurrences):
    """The flag is a Assertion about the material, not the material."""

    _, _ = recurrence_occurrences
    lying = Event(
        id="evt_asserts_text",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="r",
        payload={"text_representation": {"available": True}},
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no decoded text"):
        measure_recurrence(
            [lying], declared=_recurrence_declared("the"), occurrences_of=_counts("the")
        )
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no decoded text"):
        measure_recurrences([lying], declared=declared, counts_in=_counts_in(declared))


def test_one_occurrence_twice_in_a_inputs_is_refused(recurrence_occurrences):
    """`01.Source.E.1`: each counted occurrence is distinguished by identity."""

    _, occurrences = recurrence_occurrences
    doubled = list(occurrences) + [occurrences[0]]
    with pytest.raises(PreservedMaterialMeasurementError, match="more than once"):
        measure_recurrence(
            doubled, declared=_recurrence_declared("the"), occurrences_of=_counts("the")
        )
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="more than once"):
        measure_recurrences(doubled, declared=declared, counts_in=_counts_in(declared))


def test_the_positional_path_also_refuses_a_repeated_occurrence(occurrences):
    """`measure_occupancy` asserts a count of occurrences too."""

    with pytest.raises(PreservedMaterialMeasurementError, match="more than once"):
        measure_occupancy(
            list(occurrences) + [occurrences[0]],
            declared=_declared(),
            occupant_of=_first_word,
        )

# --------------------------------------------------------------------------
# One pass has as input one input sequence, so one basis describes every finding.
# `#2486` built SupportBasis for exactly this and the recurrence path was
# written without it.
# --------------------------------------------------------------------------


def _basis_for(occurrences, ledger):
    return declare_complete_inputs(
        workspace_id="w",
        session_id="r",
        occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=ledger.capture_boundary(),
        identities=[e.id for e in occurrences],
    )


def test_a_declared_basis_replaces_the_enumeration(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the", "cat")
    findings = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=_counts_in(declared),
        support_basis=_basis_for(occurrences, ledger),
        support_validator=SupportValidator(ledger),
    )
    for finding in findings:
        carried = finding.to_json_dict()
        assert "input_event_ids" not in carried
        assert carried["input_support"]["support_count"] == len(occurrences)
        # the act still knows what it walked, in memory, while it runs
        assert finding.input_event_ids == tuple(e.id for e in occurrences)


def test_a_basis_that_does_not_commit_to_the_inputs_is_refused(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    wrong = _basis_for(occurrences[:1], ledger)
    with pytest.raises(PreservedMaterialMeasurementError, match="does not commit"):
        measure_recurrences(
            occurrences,
            declared=declared,
            counts_in=_counts_in(declared),
            support_basis=wrong,
        )


def test_findings_with_and_without_a_basis_agree_on_everything_else(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the", "zebra")
    plain = measure_recurrences(
        occurrences, declared=declared, counts_in=_counts_in(declared)
    )
    based = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=_counts_in(declared),
        support_basis=_basis_for(occurrences, ledger),
        support_validator=SupportValidator(ledger),
    )
    for a, b in zip(plain, based):
        left, right = a.to_json_dict(), b.to_json_dict()
        left.pop("input_event_ids")
        right.pop("input_support")
        assert left == right


def test_a_basis_scoped_to_one_locality_cannot_describe_several(
    recurrence_occurrences,
):
    """Committing to the identities is not describing the inputs."""

    ledger, occurrences = recurrence_occurrences
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
    inputs = list(occurrences) + [elsewhere]
    # The basis commits to exactly these identities and declares one locality.
    basis = declare_complete_inputs(
        workspace_id="w",
        session_id="r",
        occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=ledger.capture_boundary(),
        identities=[e.id for e in inputs],
    )
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="scoped to"):
        measure_recurrences(
            inputs,
            declared=declared,
            counts_in=_counts_in(declared),
            support_basis=basis,
        )


def test_a_basis_selecting_another_occurrence_kind_is_refused(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    basis = declare_complete_inputs(
        workspace_id="w",
        session_id="r",
        occurrence_kind="some.other.kind",
        boundary=ledger.capture_boundary(),
        identities=[e.id for e in occurrences],
    )
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="selects some.other.kind"):
        measure_recurrences(
            occurrences,
            declared=declared,
            counts_in=_counts_in(declared),
            support_basis=basis,
        )


def test_a_basis_is_refused_without_the_means_to_establish_its_selection(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="requires a SupportValidator"):
        measure_recurrences(
            occurrences,
            declared=declared,
            counts_in=_counts_in(declared),
            support_basis=_basis_for(occurrences, ledger),
        )


def test_a_basis_asserting_completeness_over_a_subset_is_refused(
    recurrence_occurrences,
):
    """The checks on ids, count, locality and kind all pass on a subset."""

    ledger, occurrences = recurrence_occurrences
    subset = list(occurrences)[:-1]
    basis = declare_complete_inputs(
        workspace_id="w",
        session_id="r",
        occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=ledger.capture_boundary(),
        identities=[e.id for e in subset],
    )
    declared = _declared_for("the")
    with pytest.raises(SupportBasisError, match="validated support"):
        measure_recurrences(
            subset,
            declared=declared,
            counts_in=_counts_in(declared),
            support_basis=basis,
            support_validator=SupportValidator(ledger),
        )


def test_a_finding_measures_what_the_ledger_carries_not_what_was_handed_in(
    recurrence_occurrences,
):
    """An Event can be constructed with any id and any payload."""

    ledger, occurrences = recurrence_occurrences
    # Same identities the ledger preserves; different material.
    forged = [
        Event(
            id=e.id,
            kind=e.kind,
            workspace_id="w",
            session_id="r",
            payload={
                "decoded_text": "zebra zebra zebra",
                "material_origin": "operator",
                "text_representation": {"available": True},
            },
        )
        for e in occurrences
    ]
    declared = _declared_for("zebra")
    findings = measure_recurrences(
        forged,
        declared=declared,
        counts_in=_counts_in(declared),
        support_basis=_basis_for(occurrences, ledger),
        support_validator=SupportValidator(ledger),
    )
    # The ledger carries no "zebra". The handed-in objects carried nine.
    assert findings[0].total_count == 0


def test_an_identity_the_ledger_does_not_preserve_is_refused(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    absent = Event(
        id="evt_not_in_ledger",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="r",
        payload={"decoded_text": "the", "text_representation": {"available": True}},
    )
    declared = _declared_for("the")
    basis = declare_complete_inputs(
        workspace_id="w",
        session_id="r",
        occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=ledger.capture_boundary(),
        identities=[absent.id],
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="not preserved in the ledger"):
        measure_recurrences(
            [absent],
            declared=declared,
            counts_in=_counts_in(declared),
            support_basis=basis,
            support_validator=SupportValidator(ledger),
        )


def test_the_positional_path_also_refuses_incoherent_material(recurrence_occurrences):
    """`measure_occupancy` had its own copy of the check and never gained the fix."""

    _, _ = recurrence_occurrences
    lying = Event(
        id="evt_positional_asserts_text",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="r",
        payload={"text_representation": {"available": True}},
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no decoded text"):
        measure_occupancy([lying], declared=_declared(), occupant_of=_first_word)


def test_a_finding_over_unpreserved_material_cannot_be_recorded():
    """The recorder states provenance it never established."""

    ledger = EventLedger()
    forged = Event(
        id="evt_never_preserved",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="r",
        payload={
            "decoded_text": "zebra zebra",
            "material_origin": "operator",
            "text_representation": {"available": True},
        },
    )
    finding = measure_recurrence(
        [forged],
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
        yield_in=(ledger, "w", "r"),
    )
    assert finding.total_count == 2  # the measurement itself is not the guard
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no such ingress"):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=finding
        )


def test_the_positional_path_cannot_record_unpreserved_material_either():
    ledger = EventLedger()
    forged = Event(
        id="evt_also_never_preserved",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="r",
        payload={"decoded_text": "the cat", "text_representation": {"available": True}},
    )
    finding = measure_occupancy(
        [forged], declared=_declared(), occupant_of=_first_word
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no such ingress"):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=finding
        )


def test_a_real_identity_carrying_forged_material_measures_the_ledger(
    recurrence_occurrences,
):
    """`#2510` closed this for the basis path only; every other path trusted
    the object it was handed."""

    ledger, occurrences = recurrence_occurrences
    forged = [
        Event(
            id=e.id,
            kind=e.kind,
            workspace_id="w",
            session_id="r",
            payload={
                "decoded_text": "zebra zebra zebra",
                "material_origin": "operator",
                "text_representation": {"available": True},
            },
        )
        for e in occurrences
    ]
    # Unbound: the act measures what it was handed and cannot say otherwise.
    loose = measure_recurrence(
        forged, declared=_recurrence_declared("zebra"), occurrences_of=_counts("zebra")
    )
    assert loose.total_count == 9

    # Bound to the ledger those identities name: the ledger carries no zebra.
    bound = measure_recurrence(
        forged,
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
        preserved_in=ledger,
    )
    assert bound.total_count == 0


def test_the_positional_path_can_bind_its_material_too(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    forged = [
        Event(
            id=occurrences[0].id,
            kind=INGRESS_OCCURRED_KIND,
            workspace_id="w",
            session_id="r",
            payload={"decoded_text": "zebra", "text_representation": {"available": True}},
        )
    ]
    finding = measure_occupancy(
        forged, declared=_declared(), occupant_of=_first_word, preserved_in=ledger
    )
    assert finding.occupancies[0].representation == "the"


def test_carrying_a_basis_no_longer_exempts_a_finding_from_the_recorder():
    """Carrying a basis is not being verified against one."""

    ledger = EventLedger()
    forged = Event(
        id="evt_absent_but_asserted",
        kind=INGRESS_OCCURRED_KIND,
        workspace_id="w",
        session_id="r",
        payload={"decoded_text": "the", "text_representation": {"available": True}},
    )
    finding = measure_recurrence(
        [forged], declared=_recurrence_declared("the"), occurrences_of=_counts("the"),
        yield_in=(ledger, "w", "r"),
    )
    # A SupportBasis is a directly constructible dataclass; attaching one is
    # not evidence that any act verified it.
    attached = RecurrenceFinding(
        declared=finding.declared,
        input_localities=finding.input_localities,
        occurrences_examined=finding.occurrences_examined,
        occurrences_carrying=finding.occurrences_carrying,
        total_count=finding.total_count,
        input_event_ids=finding.input_event_ids,
        support_basis=declare_complete_inputs(
            workspace_id="w",
            session_id="r",
            occurrence_kind=INGRESS_OCCURRED_KIND,
            boundary=ledger.capture_boundary(),
            identities=[forged.id],
        ),
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no such ingress"):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=attached
        )


def test_a_finding_carries_where_its_material_came_from(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    unbound = measure_recurrence(
        occurrences, declared=_recurrence_declared("the"), occurrences_of=_counts("the")
    )
    bound = measure_recurrence(
        occurrences,
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
        preserved_in=ledger,
    )
    assert unbound.material_provenance == MATERIAL_AS_SUPPLIED
    assert bound.material_provenance == MATERIAL_READ_FROM_LEDGER
    # Stated once, where the recorder reads it. Carrying it in the finding
    # payload as well would be two representations of one coordinate.
    assert "material_provenance" not in unbound.to_json_dict()


def test_the_recorder_states_the_provenance_the_measurement_declared(
    recurrence_occurrences,
):
    """The blocker: a real Act over unbound material, recorded as preserved."""

    ledger, occurrences = recurrence_occurrences
    forged = [
        Event(
            id=e.id,
            kind=e.kind,
            workspace_id="w",
            session_id="r",
            payload={
                "decoded_text": "zebra zebra",
                "material_origin": "operator",
                "text_representation": {"available": True},
            },
        )
        for e in occurrences
    ]
    # A lawful measurement, over material the ledger does not carry, with
    # identities the ledger does.
    finding = measure_recurrence(
        forged,
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
        yield_in=(ledger, "w", "r"),
    )
    assert finding.total_count == 6
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    # It records -- the identities exist and the Act occurred -- but it no
    # longer asserts the material was preserved.
    assert event.payload["dimensions"]["source_provenance"] == MATERIAL_AS_SUPPLIED
    assert "preserved" not in event.payload["dimensions"]["source_provenance"]

    bound = measure_recurrence(
        occurrences,
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
        preserved_in=ledger,
        yield_in=(ledger, "w", "r"),
    )
    recorded = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=bound
    )
    assert (
        recorded.payload["dimensions"]["source_provenance"]
        == MATERIAL_READ_FROM_LEDGER
    )


def test_the_basis_path_reports_the_ledger_it_read_from(recurrence_occurrences):
    """It re-reads every occurrence and used to record them as supplied."""

    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    finding = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=_counts_in(declared),
        support_basis=_basis_for(occurrences, ledger),
        support_validator=SupportValidator(ledger),
    )[0]
    assert finding.material_provenance == MATERIAL_READ_FROM_LEDGER


def test_responsibility_does_not_follow_the_provenance(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    unbound = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id="r",
        finding=measure_recurrence(
            occurrences,
            declared=_recurrence_declared("the"),
            occurrences_of=_counts("the"),
        yield_in=(ledger, "w", "r"),
    ),
    )
    bound = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id="r",
        finding=measure_recurrence(
            occurrences,
            declared=_recurrence_declared("the"),
            occurrences_of=_counts("the"),
            preserved_in=ledger,
        yield_in=(ledger, "w", "r"),
    ),
    )
    # Provenance differs; Responsibility does not follow it. `#2439` reconstructed
    # boundary participant, Act and Standing for declared measurement and left the
    # Responsibility unestablished, and that stays true either way.
    assert unbound.payload["dimensions"]["source_provenance"] != bound.payload[
        "dimensions"
    ]["source_provenance"]
    assert (
        unbound.payload["dimensions"]["responsibility"]
        == bound.payload["dimensions"]["responsibility"]
        == RESPONSIBILITY_UNESTABLISHED
    )


# --------------------------------------------------------------------------
# The yield witness. The Book HEAD separates mechanical construction
# from a witnessed yielding-act return; these fix which is which.
# --------------------------------------------------------------------------


def _rebuilt(finding, **changed):
    fields = {
        "declared": finding.declared,
        "material_provenance": finding.material_provenance,
        "input_localities": finding.input_localities,
        "occurrences_examined": finding.occurrences_examined,
        "occurrences_carrying": finding.occurrences_carrying,
        "total_count": finding.total_count,
        "input_event_ids": finding.input_event_ids,
        "target_act_id": finding.target_act_id,
        "act_occurrence_id": finding.act_occurrence_id,
        "support_basis": finding.support_basis,
        "yield_evidence_id": finding.yield_evidence_id,
    }
    fields.update(changed)
    return RecurrenceFinding(**fields)


def _yielded(ledger, occurrences, target="the", **kw):
    return measure_recurrence(
        occurrences,
        declared=_recurrence_declared(target),
        occurrences_of=_counts(target),
        yield_in=(ledger, "w", "r"),
        **kw,
    )


def test_a_yielded_result_records(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND


def test_an_identical_finding_nobody_yielded_cannot_reuse_the_witness(
    recurrence_occurrences,
):
    """The exact direct-instantiation counterexample: identical fields."""

    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    constructed = _rebuilt(yielded, yield_evidence_id=None)
    # Every measured coordinate is identical. Only the relation is absent.
    assert _yielded_content(constructed) == _yielded_content(yielded)
    with pytest.raises(PreservedMaterialMeasurementError, match="names no yield"):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=constructed
        )


def test_another_representation_of_the_same_yielded_result_is_lawful(
    recurrence_occurrences,
):
    """Carrying the same evidence is being the same result, not forging one."""

    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    same = _rebuilt(yielded)
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=same
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND


def test_evidence_for_one_result_does_not_carry_another(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    borrowed = _rebuilt(yielded, total_count=yielded.total_count + 1)
    with pytest.raises(PreservedMaterialMeasurementError, match="different result"):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=borrowed
        )


@pytest.mark.parametrize(
    "changed",
    [
        {"total_count": 999},
        {"occurrences_carrying": 999},
        {"occurrences_examined": 999},
        {"material_provenance": MATERIAL_READ_FROM_LEDGER},
        {"input_localities": ("workspace:w;session:elsewhere",)},
        {"boundary_notes": ("a limit nobody measured",)},
    ],
)
def test_changing_any_yielded_coordinate_cannot_reuse_the_witness(
    recurrence_occurrences, changed
):
    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    altered = _rebuilt(yielded, **changed)
    with pytest.raises(PreservedMaterialMeasurementError, match="different result"):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=altered
        )


def test_recording_cannot_overwrite_what_the_measurement_established(
    recurrence_occurrences,
):
    """`extra` may add recording coordinates; it may not replace Yield-edge ones."""

    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    # Refused rather than quietly dropped: a caller asked to record one thing
    # and silently recording another is its own defect.
    with pytest.raises(PreservedMaterialMeasurementError, match="may not replace"):
        record_measurement_finding(
            ledger,
            workspace_id="w",
            session_id="r",
            finding=finding,
            extra={"total_count": 999},
        )
    event = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id="r",
        finding=finding,
        extra={"a_recording_coordinate": "kept"},
    )
    assert event.payload["a_recording_coordinate"] == "kept"


def test_recording_cannot_restate_the_measurements_own_dimensions(
    recurrence_occurrences,
):
    """`extra` was filtered against the finding's keys only, so `dimensions`
    -- carrying the provenance `#2516` reconstructed -- was reachable."""

    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    with pytest.raises(PreservedMaterialMeasurementError, match="may not replace"):
        record_measurement_finding(
            ledger,
            workspace_id="w",
            session_id="r",
            finding=finding,
            extra={"dimensions": {"source_provenance": "whatever I want"}},
        )


def test_yield_and_recording_may_be_in_different_localities(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences,
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
        yield_in=(ledger, "w", "where the material lives"),
    )
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="somewhere else", finding=finding
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND


def test_yield_evidence_cannot_be_borrowed_across_workspaces(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    with pytest.raises(
        PreservedMaterialMeasurementError, match="same workspace"
    ):
        record_measurement_finding(
            ledger,
            workspace_id="another-workspace",
            session_id="r",
            finding=finding,
        )


def test_recurrence_recorder_requires_its_yield_convention(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    evidence = ledger.get(finding.yield_evidence_id)
    assert evidence.payload["dimensions"]["act_occurrence_id"] == (
        finding.act_occurrence_id
    )
    forged = ledger.append(
        YIELD_EVIDENCE_KIND,
        "w",
        {**evidence.payload, "yield_convention": "another convention"},
        session_id="r",
    )
    altered = _rebuilt(finding, yield_evidence_id=forged.id)
    with pytest.raises(
        PreservedMaterialMeasurementError, match="different yield convention"
    ):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=altered
        )


def test_no_public_operation_attaches_yield_to_an_arbitrary_finding():
    import seed_runtime.preserved_material_measurement as module

    public = [n for n in dir(module) if not n.startswith("_")]
    assert not [n for n in public if "yield" in n or "yield" in n]


def test_the_witness_asserts_no_responsibility(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    _yielded(ledger, occurrences)
    witness = [
        e for e in ledger.list("w") if e.kind == YIELD_EVIDENCE_KIND
    ][-1]
    assert witness.payload["dimensions"]["responsibility"] == RESPONSIBILITY_UNESTABLISHED
    assert "not the edge or Act occurrence by identity" in (
        witness.payload["dimensions"]["occurrence_preservation"]
    )


@pytest.mark.parametrize(
    "addition",
    [
        {"dimensions": {"identity": "something else"}},
        {"mutates_cluster": True},
        {"unknowns": ["one nobody established"]},
        {"provenance_occurrence_refs": ["evt_unsupported"]},
        {"total_count": 999},
    ],
)
def test_recording_may_not_replace_any_coordinate_the_payload_carries(
    recurrence_occurrences, addition
):
    """`extra` checked only the finding's keys, so the payload's own were
    reachable -- a supplied `dimensions` replaced the whole object and erased
    the measurement's provenance by omission."""

    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    with pytest.raises(PreservedMaterialMeasurementError, match="may not replace"):
        record_measurement_finding(
            ledger, workspace_id="w", session_id="r", finding=finding, extra=addition
        )


def test_recording_may_still_add_its_own_coordinate(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    event = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id="r",
        finding=finding,
        extra={"a_recording_coordinate": "kept"},
    )
    assert event.payload["a_recording_coordinate"] == "kept"
    assert event.payload["dimensions"]["source_provenance"]
