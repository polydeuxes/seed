"""A declared measurement over what Seed preserved, recorded so it survives.

Two things separate this from the withdrawn probe at `#2368`.

**What it has as input.** Occurrences come from the ledger, having been recorded
through operator ingest. `#2368` read a file directly, and a measurement over
material Seed never received says nothing about Seed.

**What becomes of the result.** Findings are appended to the ledger, so a later
responsible act may have them participate. `01.Standing.E` permits a bounded comparison
to have as input preserved findings while preserving each input's support support,
confidence, and standing. A finding that vanishes with the process cannot be
input by anything.

`01.Source:28` requires three disclosures of any recurrence assertion. They
are required fields here, and an absent one is refused rather than defaulted.

Nothing here establishes represented relation. `01.Standing.D` refuses relation standing to
co-presence, and a finding reports co-presence.
"""

from __future__ import annotations

import re
from tests.binary_input import binary_input
from io import BytesIO, StringIO

from seed_runtime.event import Event
from seed_runtime.material_ingest import ingested_material_bytes
from seed_runtime.operator_ingest import run_operator_ingest
from seed_runtime.operator_material_boundary import operator_boundary_material
from seed_runtime.preserved_material_measurement import INGEST_OCCURRED_KIND

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.preserved_material_measurement import (
    MATERIAL_AS_SUPPLIED,
    _result_content,
    RESPONSIBILITY_UNESTABLISHED,
    MATERIAL_READ_FROM_LEDGER,
    MEASUREMENT_RECORDED_KIND,
    RecurrenceFinding,
    DeclaredMeasurement,
    PreservedMaterialMeasurementError,
    measure_position_representations,
    measure_recurrence,
    measure_recurrences,
    ingest_occurrences,
    record_measurement_finding,
)
from seed_runtime.yield_evidence import YIELD_EVIDENCE_KIND
from tests.material_fixture_console import run_material_fixture_console
from seed_runtime.input_support import (
    InputSupportError,
    InputSupportValidator,
    declare_input_support,
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
        "counting_scope": "preserved ingest occurrences of this locality",
    }
    return DeclaredMeasurement(**{**base, **overrides})


@pytest.fixture
def locality():
    ledger = EventLedger()
    run_material_fixture_console(
        ledger=ledger,
        locality_identity="s",
        input_stream=binary_input(MATERIAL + ""),
        output_stream=StringIO(),
    )
    return ledger


@pytest.fixture
def occurrences(locality):
    return ingest_occurrences(locality, locality_identity="s")


# --------------------------------------------------------------------------
# What is measured is what Seed preserved.
# --------------------------------------------------------------------------


def test_the_material_measured_is_the_locality_s_own_occurrences(occurrences):
    assert len(occurrences) == 5
    assert all(event.material["dimensions"]["authority"] == "unestablished" for event in occurrences)
    assert all(
        "represented relation Unknown"
        in event.material["dimensions"]["evidence_scope"]
        for event in occurrences
    )


def test_only_an_ingest_occurrence_may_be_measured(locality):
    foreign = locality.append(
        "unrelated.kind", {"represented_material": "x"}, locality_identity="s"
    )
    with pytest.raises(PreservedMaterialMeasurementError):
        measure_position_representations([foreign], declared=_declared(), representation_at=_first_word)


def test_a_finding_names_every_occurrence_that_participated(occurrences):
    finding = measure_position_representations(
        occurrences, declared=_declared(), representation_at=_first_word
    )
    assert finding.input_event_identities == tuple(e.identity for e in occurrences)


def test_an_absent_position_is_absent_not_unknown(occurrences):
    """One line carries no delimiter; it is skipped, not counted as Unknown."""
    finding = measure_position_representations(
        occurrences, declared=_declared(), representation_at=_after_delimiter
    )
    assert finding.position_count == 4
    assert len(finding.input_event_identities) == 5


# --------------------------------------------------------------------------
# 01.Source:28's three disclosures are required.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "missing", ("representation_measured", "equivalence_rule", "counting_scope")
)
def test_a_measurement_without_its_disclosures_is_refused(missing):
    with pytest.raises(PreservedMaterialMeasurementError):
        _declared(**{missing: "   "})


def test_the_disclosures_are_carried_on_the_recorded_finding(locality, occurrences):
    finding = measure_position_representations(
        occurrences, declared=_declared(), representation_at=_first_word
    )
    event = record_measurement_finding(
        locality, locality_identity="s", finding=finding
    )
    for key in ("representation_measured", "equivalence_rule", "counting_scope"):
        assert event.material[key].strip()


# --------------------------------------------------------------------------
# The finding survives, and what it stood on survives with it.
# --------------------------------------------------------------------------


def test_a_recorded_finding_may_participate_in_a_later_act(locality, occurrences):
    finding = measure_position_representations(
        occurrences, declared=_declared(), representation_at=_first_word
    )
    event = record_measurement_finding(
        locality, locality_identity="s", finding=finding
    )
    read = locality.get(event.identity)
    assert read is not None
    assert read.kind == MEASUREMENT_RECORDED_KIND
    assert read.material["representation_counts"]


# --------------------------------------------------------------------------
# The ladder, and what it does not become.
# --------------------------------------------------------------------------


def test_distinct_measurements_yield_distinct_bounded_counts(occurrences):
    unbounded = measure_position_representations(
        occurrences, declared=_declared(), representation_at=_first_word
    )
    bounded = measure_position_representations(
        occurrences, declared=_declared(), representation_at=_after_delimiter
    )
    assert unbounded.highest_count_representation.occurrence_count / unbounded.position_count < 0.5
    assert bounded.highest_count_representation.representation == "is"
    assert bounded.highest_count_representation.occurrence_count / bounded.position_count == 1.0


def test_the_recorded_authority_states_the_clause_s_own_limit(locality, occurrences):
    event = record_measurement_finding(
        locality,
        locality_identity="s",
        finding=measure_position_representations(
            occurrences, declared=_declared(), representation_at=_after_delimiter
        ),
    )
    assert event.material["dimensions"]["authority"] == "unestablished"
    evidence_scope = event.material["dimensions"]["evidence_scope"]
    assert "measurement evidence only" in evidence_scope
    assert "no represented relation, relation" in evidence_scope
    assert event.material["unknowns"] == [
        "what any measured representation means remains Unknown"
    ]


def test_the_finding_disclaims_what_a_dominant_occupant_is_not(locality, occurrences):
    event = record_measurement_finding(
        locality,
        locality_identity="s",
        finding=measure_position_representations(
            occurrences, declared=_declared(), representation_at=_after_delimiter
        ),
    )
    limit_material = " ".join(event.material["limits"])
    assert "is not the represented relation of that position" in limit_material
    assert "establishes no relation" in limit_material


def test_recording_a_finding_does_not_disturb_the_measured_occurrences(
    locality, occurrences
):
    before = [(e.identity, e.material["represented_material"]) for e in occurrences]
    record_measurement_finding(
        locality,
        locality_identity="s",
        finding=measure_position_representations(
            occurrences, declared=_declared(), representation_at=_first_word
        ),
    )
    after = ingest_occurrences(locality, locality_identity="s")
    assert [(e.identity, e.material["represented_material"]) for e in after] == before


def test_raw_material_without_a_supplied_representation_is_refused():
    """A represented-material Measurement cannot silently omit raw material."""

    ledger = EventLedger()
    sink = StringIO()
    for material in (b"the cat jumped\n", b"\xff\xfe\x00binary\n", b"the fence\n"):
        run_operator_ingest(
            ledger=ledger,
            locality_identity="s",
            boundary_material=operator_boundary_material(BytesIO(material)),
        )
    occurrences = ingest_occurrences(ledger, locality_identity="s")

    # All three occurred at exact source occurrences.
    assert len(occurrences) == 3
    assert all("represented_material" not in event.material for event in occurrences)
    assert ingested_material_bytes(occurrences[1]) == b"\xff\xfe\x00binary\n"

    declared = DeclaredMeasurement(
        representation_measured="anything",
        equivalence_rule="byte-for-byte equality; no normalization",
        counting_scope="one bounded locality",
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="no represented material"):
        measure_position_representations(
            occurrences, declared=declared, representation_at=lambda material: None
        )

    # Supplying text is a separate fixture boundary, not a property inferred
    # for either byte occurrence.


def test_an_occurrence_without_represented_material_is_refused():
    declared = DeclaredMeasurement(
        representation_measured="anything",
        equivalence_rule="byte-for-byte equality; no normalization",
        counting_scope="one bounded locality",
    )
    occurrence = Event(
        identity="evt_without_representation",
        kind=INGEST_OCCURRED_KIND,
        locality_identity="s",
        material={},
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="no represented material"):
        measure_position_representations(
            [occurrence], declared=declared, representation_at=lambda material: None
        )


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
    run_material_fixture_console(
        ledger=ledger,
        locality_identity="r",
        input_stream=binary_input(RECURRENCE_MATERIAL + ""),
        output_stream=StringIO(),
    )
    return ledger


@pytest.fixture
def recurrence_occurrences():
    ledger = _recurrence_ledger()
    return ledger, ingest_occurrences(ledger, locality_identity="r")


def _counts(target):
    return lambda text: text.split().count(target)


def _recurrence_declared(target):
    return DeclaredMeasurement(
        representation_measured=target,
        equivalence_rule="exact equality between whitespace-separated tokens",
        counting_scope="preserved operator-ingest occurrences of this locality",
    )


def test_what_is_measured_is_the_representation_not_a_position(recurrence_occurrences):
    _, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences, declared=_recurrence_declared("the"), occurrences_of=_counts("the")
    )
    carried = finding.to_json_dict()
    assert carried["representation_measured"] == "the"
    assert carried["measurement_distinction"] == "recurrence"
    # No positional coordinate is asserted, because none was measured.
    assert "measured_position" not in carried


def test_input_carrying_and_recurrence_counts_remain_distinct(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences, declared=_recurrence_declared("the"), occurrences_of=_counts("the")
    )
    assert finding.input_count == 3
    assert finding.occurrences_carrying == 2
    assert finding.recurrence_count == 3


def test_a_representation_that_never_occurs_yields_a_measurement_finding(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = measure_recurrence(
        occurrences,
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
        yield_in=(ledger, "r"),
    )
    assert finding.recurrence_count == 0
    assert finding.occurrences_carrying == 0
    # The scope is still stated: a bounded measurement assertion under the
    # declared rule and scope, not a failure to measure. It establishes no
    # Standing concerning zebra; `01.Source:28` bounds it to the assertion.
    assert finding.input_count == 3
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    assert event.material["dimensions"]["identity"] == "measurement:zebra"
    assert event.material["input_count"] == 3
    assert event.material["recurrence_count"] == 0


def test_nothing_but_a_ingest_occurrence_occurrence_may_be_recurrence_measured(
    recurrence_occurrences,
):
    ledger, _ = recurrence_occurrences
    foreign = ledger.append(
        "unrelated.kind", {"represented_material": "the"}, locality_identity="r"
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="preserved ingest"):
        measure_recurrence(
            [foreign], declared=_recurrence_declared("the"), occurrences_of=_counts("the")
        )


def test_material_with_no_representation_is_refused(
    recurrence_occurrences,
):
    _, occurrences = recurrence_occurrences
    without_representation = Event(
        identity="evt_no_representation",
        kind=INGEST_OCCURRED_KIND,
        locality_identity="r",
        material={},
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="no represented material"):
        measure_recurrence(
            [without_representation],
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
        yield_in=(ledger, "r"),
    )
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND
    assert event.material["dimensions"]["identity"] == "measurement:the"
    assert event.material["dimensions"]["standing"] == "measured"
    # The three disclosures `01.Source:28` requires all survive recording.
    assert event.material["representation_measured"] == "the"
    assert event.material["equivalence_rule"].startswith("exact equality")
    assert event.material["counting_scope"].startswith("preserved operator-ingest")
    assert event.material["input_event_identities"] == [e.identity for e in occurrences]


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
    inputs = tuple(e.identity for e in occurrences)
    assert all(f.input_event_identities == inputs for f in findings)
    assert all(f.input_count == len(occurrences) for f in findings)


def test_one_pass_is_one_act_occurrence_with_distinct_results(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the", "cat", "zebra")
    findings = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=_counts_in(declared),
        yield_in=(ledger, "r"),
    )

    assert len({finding.downstream_act_identity for finding in findings}) == 1
    assert len({finding.act_occurrence_identity for finding in findings}) == 1
    assert len({finding.declared.representation_measured for finding in findings}) == 3
    assert len({finding.yield_evidence_identity for finding in findings}) == 3


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
    assert findings["zebra"].recurrence_count == 0
    assert findings["zebra"].input_count == 3
    assert findings["the"].recurrence_count == 3


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
    foreign = ledger.append(
        "unrelated.kind", {"represented_material": "the"}, locality_identity="r"
    )
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="preserved ingest"):
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
        INGEST_OCCURRED_KIND,
        {
            "represented_material": "the other body",
        },
        locality_identity="other",
    )
    here = ingest_occurrences(ledger, locality_identity="r")
    finding = measure_recurrence(
        list(here) + [elsewhere],
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
        yield_in=(ledger, "r"),
    )
    assert finding.input_localities == (
        "locality:r",
        "locality:other",
    )
    # Recorded into a third locality; both coordinates survive, distinctly.
    event = record_measurement_finding(
        ledger, locality_identity="recording", finding=finding
    )
    assert event.material["input_localities"] == [
        "locality:r",
        "locality:other",
    ]
    assert (
        event.material["dimensions"]["scope_locality"]
        == "locality:recording"
    )


def test_an_occurrence_carrying_no_locality_records_the_absence(
    recurrence_occurrences,
):
    """Absence of the coordinate is preserved, not filled in."""

    ledger, _ = recurrence_occurrences
    without_locality = Event(
        identity="evt_no_locality",
        kind=INGEST_OCCURRED_KIND,
        material={
            "represented_material": "the cat",
        },
    )
    finding = measure_recurrence(
        [without_locality],
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
    )
    # No Locality was carried, so none is recorded.
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
            locality_identity="r",
            finding=measure_recurrence(
                occurrences, declared=declared[t], occurrences_of=_counts(t),
        yield_in=(ledger, "r"),
    ),
        )
        for t in targets
    ]
    batched = [
        record_measurement_finding(
            ledger, locality_identity="r", finding=finding
        )
        for finding in measure_recurrences(
            occurrences, declared=declared, counts_in=_counts_in(declared),
        yield_in=(ledger, "r"),
    )
    ]
    # Occurrence identity is the Event identity, which is outside the material. The
    # one material coordinate that legitimately differs is `yield_evidence_identity`: these
    # are two yields of the same content, and each names its own evidence.
    def _without_its_own_evidence(event):
        material = dict(event.material)
        material.pop("yield_evidence_identity", None)
        material.pop("downstream_act_identity", None)
        material.pop("act_occurrence_identity", None)
        return material

    assert [_without_its_own_evidence(e) for e in singly] == [
        _without_its_own_evidence(e) for e in batched
    ]


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
    """`measure_position_representations` asserts a count of occurrences too."""

    with pytest.raises(PreservedMaterialMeasurementError, match="more than once"):
        measure_position_representations(
            list(occurrences) + [occurrences[0]],
            declared=_declared(),
            representation_at=_first_word,
        )

# --------------------------------------------------------------------------
# One pass has as input one input sequence, so one support describes every finding.
# `#2486` built InputSupport for exactly this and the recurrence path was
# written without it.
# --------------------------------------------------------------------------


def _input_support_for(occurrences, ledger):
    return declare_input_support(
        locality_identity="r",
        occurrence_kind=INGEST_OCCURRED_KIND,
        boundary=ledger.append_boundary(),
        occurrence_references=[e.identity for e in occurrences],
    )


def test_declared_input_support_replaces_the_enumeration(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the", "cat")
    findings = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=_counts_in(declared),
        input_support=_input_support_for(occurrences, ledger),
        support_validator=InputSupportValidator(ledger),
    )
    for finding in findings:
        carried = finding.to_json_dict()
        assert "input_event_identities" not in carried
        assert carried["input_support"]["support_count"] == len(occurrences)
        # the act still knows what it walked, in memory, while it runs
        assert finding.input_event_identities == tuple(e.identity for e in occurrences)


def test_input_support_and_measurement_input_order_must_be_exact(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    support = _input_support_for(occurrences, ledger)
    with pytest.raises(PreservedMaterialMeasurementError, match="inputs differ"):
        measure_recurrences(
            reversed(occurrences),
            declared=declared,
            counts_in=_counts_in(declared),
            input_support=support,
            support_validator=InputSupportValidator(ledger),
        )


def test_findings_with_and_without_input_support_agree_on_everything_else(
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
        input_support=_input_support_for(occurrences, ledger),
        support_validator=InputSupportValidator(ledger),
    )
    for a, b in zip(plain, based):
        left, right = a.to_json_dict(), b.to_json_dict()
        left.pop("input_event_identities")
        right.pop("input_support")
        assert left == right


def test_input_support_for_one_locality_cannot_describe_several(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    elsewhere = ledger.append(
        INGEST_OCCURRED_KIND,
        {
            "represented_material": "the other body",
        },
        locality_identity="other",
    )
    inputs = list(occurrences) + [elsewhere]
    support = declare_input_support(
        locality_identity="r",
        occurrence_kind=INGEST_OCCURRED_KIND,
        boundary=ledger.append_boundary(),
        occurrence_references=[e.identity for e in inputs],
    )
    declared = _declared_for("the")
    with pytest.raises(InputSupportError, match="declared count"):
        measure_recurrences(
            inputs,
            declared=declared,
            counts_in=_counts_in(declared),
            input_support=support,
            support_validator=InputSupportValidator(ledger),
        )


def test_input_support_for_another_occurrence_kind_is_refused(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    support = declare_input_support(
        locality_identity="r",
        occurrence_kind="some.other.kind",
        boundary=ledger.append_boundary(),
        occurrence_references=[e.identity for e in occurrences],
    )
    declared = _declared_for("the")
    with pytest.raises(InputSupportError, match="declared count"):
        measure_recurrences(
            occurrences,
            declared=declared,
            counts_in=_counts_in(declared),
            input_support=support,
            support_validator=InputSupportValidator(ledger),
        )


def test_input_support_requires_its_ledger_boundary(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the")
    with pytest.raises(PreservedMaterialMeasurementError, match="exact ledger boundary"):
        measure_recurrences(
            occurrences,
            declared=declared,
            counts_in=_counts_in(declared),
            input_support=_input_support_for(occurrences, ledger),
        )


def test_input_support_over_a_subset_is_refused(
    recurrence_occurrences,
):
    """The checks on identities, count, locality and kind all pass on a subset."""

    ledger, occurrences = recurrence_occurrences
    subset = list(occurrences)[:-1]
    support = declare_input_support(
        locality_identity="r",
        occurrence_kind=INGEST_OCCURRED_KIND,
        boundary=ledger.append_boundary(),
        occurrence_references=[e.identity for e in subset],
    )
    declared = _declared_for("the")
    with pytest.raises(InputSupportError, match="validated support"):
        measure_recurrences(
            subset,
            declared=declared,
            counts_in=_counts_in(declared),
            input_support=support,
            support_validator=InputSupportValidator(ledger),
        )


def test_a_finding_measures_what_the_ledger_carries_not_what_was_handed_in(
    recurrence_occurrences,
):
    """An Event can be supplied with any identity and any material."""

    ledger, occurrences = recurrence_occurrences
    # Same identities the ledger preserves; different material.
    forged = [
        Event(
            identity=e.identity,
            kind=e.kind,
            locality_identity="r",
            material={
                "represented_material": "zebra zebra zebra",
            },
        )
        for e in occurrences
    ]
    declared = _declared_for("zebra")
    findings = measure_recurrences(
        forged,
        declared=declared,
        counts_in=_counts_in(declared),
        input_support=_input_support_for(occurrences, ledger),
        support_validator=InputSupportValidator(ledger),
    )
    # The ledger carries no "zebra". The handed-in objects carried nine.
    assert findings[0].recurrence_count == 0


def test_an_identity_the_ledger_does_not_preserve_is_refused(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    absent = Event(
        identity="evt_not_in_ledger",
        kind=INGEST_OCCURRED_KIND,
        locality_identity="r",
        material={"represented_material": "the"},
    )
    declared = _declared_for("the")
    support = declare_input_support(
        locality_identity="r",
        occurrence_kind=INGEST_OCCURRED_KIND,
        boundary=ledger.append_boundary(),
        occurrence_references=[absent.identity],
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="not preserved in the ledger"):
        measure_recurrences(
            [absent],
            declared=declared,
            counts_in=_counts_in(declared),
            input_support=support,
            support_validator=InputSupportValidator(ledger),
        )


def test_a_finding_over_unpreserved_material_cannot_be_recorded():
    """The recorder states provenance it never established."""

    ledger = EventLedger()
    forged = Event(
        identity="evt_never_preserved",
        kind=INGEST_OCCURRED_KIND,
        locality_identity="r",
        material={
            "represented_material": "zebra zebra",
        },
    )
    finding = measure_recurrence(
        [forged],
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
        yield_in=(ledger, "r"),
    )
    assert finding.recurrence_count == 2  # the measurement itself is not the guard
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no such ingest"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=finding
        )


def test_the_positional_path_cannot_record_unpreserved_material_either():
    ledger = EventLedger()
    forged = Event(
        identity="evt_also_never_preserved",
        kind=INGEST_OCCURRED_KIND,
        locality_identity="r",
        material={"represented_material": "the cat"},
    )
    finding = measure_position_representations(
        [forged], declared=_declared(), representation_at=_first_word
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no such ingest"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=finding
        )


def test_a_real_identity_carrying_forged_material_measures_the_ledger(
    recurrence_occurrences,
):
    """`#2510` enforced this for the support path only; every other path trusted
    the object it was handed."""

    ledger, occurrences = recurrence_occurrences
    forged = [
        Event(
            identity=e.identity,
            kind=e.kind,
            locality_identity="r",
            material={
                "represented_material": "zebra zebra zebra",
            },
        )
        for e in occurrences
    ]
    # Unbound: the act measures what it was handed and cannot say otherwise.
    loose = measure_recurrence(
        forged, declared=_recurrence_declared("zebra"), occurrences_of=_counts("zebra")
    )
    assert loose.recurrence_count == 9

    # Bound to the ledger those identities name: the ledger carries no zebra.
    bound = measure_recurrence(
        forged,
        declared=_recurrence_declared("zebra"),
        occurrences_of=_counts("zebra"),
        preserved_in=ledger,
    )
    assert bound.recurrence_count == 0


def test_the_positional_path_can_bind_its_material_too(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    forged = [
        Event(
            identity=occurrences[0].identity,
            kind=INGEST_OCCURRED_KIND,
            locality_identity="r",
            material={"represented_material": "zebra"},
        )
    ]
    finding = measure_position_representations(
        forged, declared=_declared(), representation_at=_first_word, preserved_in=ledger
    )
    assert finding.representation_counts[0].representation == "the"


def test_carrying_a_basis_no_longer_exempts_a_finding_from_the_recorder():
    """Carrying a support is not being verified against one."""

    ledger = EventLedger()
    forged = Event(
        identity="evt_absent_but_asserted",
        kind=INGEST_OCCURRED_KIND,
        locality_identity="r",
        material={"represented_material": "the"},
    )
    finding = measure_recurrence(
        [forged], declared=_recurrence_declared("the"), occurrences_of=_counts("the"),
        yield_in=(ledger, "r"),
    )
    # A InputSupport is a directly formable dataclass; attaching one is
    # not evidence that any act verified it.
    attached = RecurrenceFinding(
        declared=finding.declared,
        input_localities=finding.input_localities,
        occurrences_carrying=finding.occurrences_carrying,
        recurrence_count=finding.recurrence_count,
        input_event_identities=finding.input_event_identities,
        input_support=declare_input_support(
            locality_identity="r",
            occurrence_kind=INGEST_OCCURRED_KIND,
            boundary=ledger.append_boundary(),
            occurrence_references=[forged.identity],
        ),
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="preserves no such ingest"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=attached
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
    # material as well would be two representations of one coordinate.
    assert "material_provenance" not in unbound.to_json_dict()


def test_the_recorder_states_the_provenance_the_measurement_declared(
    recurrence_occurrences,
):
    """The blocker: a real Act over unbound material, recorded as preserved."""

    ledger, occurrences = recurrence_occurrences
    forged = [
        Event(
            identity=e.identity,
            kind=e.kind,
            locality_identity="r",
            material={
                "represented_material": "zebra zebra",
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
        yield_in=(ledger, "r"),
    )
    assert finding.recurrence_count == 6
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    # It records -- the identities exist and the Act occurred -- but it no
    # longer asserts the material was preserved.
    assert event.material["dimensions"]["source_provenance"] == MATERIAL_AS_SUPPLIED
    assert "preserved" not in event.material["dimensions"]["source_provenance"]

    bound = measure_recurrence(
        occurrences,
        declared=_recurrence_declared("the"),
        occurrences_of=_counts("the"),
        preserved_in=ledger,
        yield_in=(ledger, "r"),
    )
    recorded = record_measurement_finding(
        ledger, locality_identity="r", finding=bound
    )
    assert (
        recorded.material["dimensions"]["source_provenance"]
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
        input_support=_input_support_for(occurrences, ledger),
        support_validator=InputSupportValidator(ledger),
    )[0]
    assert finding.material_provenance == MATERIAL_READ_FROM_LEDGER


def test_responsibility_does_not_follow_the_provenance(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    unbound = record_measurement_finding(
        ledger,
        locality_identity="r",
        finding=measure_recurrence(
            occurrences,
            declared=_recurrence_declared("the"),
            occurrences_of=_counts("the"),
        yield_in=(ledger, "r"),
    ),
    )
    bound = record_measurement_finding(
        ledger,
        locality_identity="r",
        finding=measure_recurrence(
            occurrences,
            declared=_recurrence_declared("the"),
            occurrences_of=_counts("the"),
            preserved_in=ledger,
        yield_in=(ledger, "r"),
    ),
    )
    # Provenance differs; Responsibility does not follow it. `#2439` read
    # boundary participant, Act and Standing for declared measurement and left the
    # Responsibility unestablished, and that stays true either way.
    assert unbound.material["dimensions"]["source_provenance"] != bound.material[
        "dimensions"
    ]["source_provenance"]
    assert (
        unbound.material["dimensions"]["responsibility"]
        == bound.material["dimensions"]["responsibility"]
        == RESPONSIBILITY_UNESTABLISHED
    )


# --------------------------------------------------------------------------
# The yield witness. The Book HEAD separates exact input
# from a witnessed yielding-act return; these fix which is which.
# --------------------------------------------------------------------------


def _rebuilt(finding, **different):
    fields = {
        "declared": finding.declared,
        "material_provenance": finding.material_provenance,
        "input_localities": finding.input_localities,
        "occurrences_carrying": finding.occurrences_carrying,
        "recurrence_count": finding.recurrence_count,
        "input_event_identities": finding.input_event_identities,
        "downstream_act_identity": finding.downstream_act_identity,
        "act_occurrence_identity": finding.act_occurrence_identity,
        "input_support": finding.input_support,
        "yield_evidence_identity": finding.yield_evidence_identity,
    }
    fields.update(different)
    return RecurrenceFinding(**fields)


def _yielded(ledger, occurrences, target="the", **kw):
    return measure_recurrence(
        occurrences,
        declared=_recurrence_declared(target),
        occurrences_of=_counts(target),
        yield_in=(ledger, "r"),
        **kw,
    )


def test_a_result_records(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND


def test_an_identical_finding_nobody_yielded_cannot_reuse_the_witness(
    recurrence_occurrences,
):
    """The exact direct-instantiation counterexample: identical fields."""

    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    supplied = _rebuilt(yielded, yield_evidence_identity=None)
    # Every measured coordinate is identical. Only the relation is absent.
    assert _result_content(supplied) == _result_content(yielded)
    with pytest.raises(PreservedMaterialMeasurementError, match="names no yield"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=supplied
        )


def test_another_representation_of_the_same_result_is_lawful(
    recurrence_occurrences,
):
    """Carrying the same evidence is being the same result, not forging one."""

    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    same = _rebuilt(yielded)
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=same
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND


def test_evidence_for_one_result_does_not_carry_another(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    borrowed = _rebuilt(yielded, recurrence_count=yielded.recurrence_count + 1)
    with pytest.raises(PreservedMaterialMeasurementError, match="different result"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=borrowed
        )


def test_results_of_one_act_occurrence_cannot_locality_yield_evidence(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    declared = _declared_for("the", "cat")
    left, right = measure_recurrences(
        occurrences,
        declared=declared,
        counts_in=_counts_in(declared),
        yield_in=(ledger, "r"),
    )
    assert left.act_occurrence_identity == right.act_occurrence_identity
    assert left.yield_evidence_identity != right.yield_evidence_identity

    borrowed = _rebuilt(left, yield_evidence_identity=right.yield_evidence_identity)
    with pytest.raises(PreservedMaterialMeasurementError, match="different result"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=borrowed
        )


@pytest.mark.parametrize(
    "different",
    [
        {"recurrence_count": 999},
        {"occurrences_carrying": 999},
        {"material_provenance": MATERIAL_READ_FROM_LEDGER},
        {"input_localities": ("locality:elsewhere",)},
        {"limits": ("a limit nobody measured",)},
    ],
)
def test_changing_any_yielded_coordinate_cannot_reuse_the_witness(
    recurrence_occurrences, different
):
    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    altered = _rebuilt(yielded, **different)
    with pytest.raises(PreservedMaterialMeasurementError, match="different result"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=altered
        )


def test_changing_input_identities_cannot_reuse_the_yield_witness(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    yielded = _yielded(ledger, occurrences)
    altered = _rebuilt(
        yielded,
        input_event_identities=yielded.input_event_identities[:-1],
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="different result"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=altered
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
            locality_identity="r",
            finding=finding,
            extra={"recurrence_count": 999},
        )
    event = record_measurement_finding(
        ledger,
        locality_identity="r",
        finding=finding,
        extra={"a_recording_coordinate": "kept"},
    )
    assert event.material["a_recording_coordinate"] == "kept"


def test_recording_cannot_restate_the_measurements_own_dimensions(
    recurrence_occurrences,
):
    """`extra` was filtered against the finding's keys only, so `dimensions`
    -- carrying the provenance `#2516` read -- was reachable."""

    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    with pytest.raises(PreservedMaterialMeasurementError, match="may not replace"):
        record_measurement_finding(
            ledger,
            locality_identity="r",
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
        yield_in=(ledger, "where the material lives"),
    )
    event = record_measurement_finding(
        ledger, locality_identity="somewhere else", finding=finding
    )
    assert event.kind == MEASUREMENT_RECORDED_KIND


def test_recurrence_recorder_requires_its_exact_yield_result(
    recurrence_occurrences,
):
    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    evidence = ledger.get(finding.yield_evidence_identity)
    assert evidence.material["dimensions"]["act_occurrence_identity"] == (
        finding.act_occurrence_identity
    )
    altered_result = dict(evidence.material["result"])
    altered_result["recurrence_count"] += 1
    forged = ledger.append(
        YIELD_EVIDENCE_KIND,
        {**evidence.material, "result": altered_result},
        locality_identity="r",
    )
    altered = _rebuilt(finding, yield_evidence_identity=forged.identity)
    with pytest.raises(
        PreservedMaterialMeasurementError, match="different result"
    ):
        record_measurement_finding(
            ledger, locality_identity="r", finding=altered
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
        e for e in ledger.list() if e.kind == YIELD_EVIDENCE_KIND
    ][-1]
    assert witness.material["dimensions"]["responsibility"] == RESPONSIBILITY_UNESTABLISHED
    assert "not the edge or Act occurrence by identity" in (
        witness.material["dimensions"]["occurrence_preservation"]
    )


@pytest.mark.parametrize(
    "addition",
    [
        {"dimensions": {"identity": "something else"}},
        {"unknowns": ["one nobody established"]},
        {"provenance_occurrence_references": ["evt_unsupported"]},
        {"recurrence_count": 999},
    ],
)
def test_recording_may_not_replace_any_coordinate_the_material_carries(
    recurrence_occurrences, addition
):
    """`extra` checked only the finding's keys, so the material's own were
    reachable -- a supplied `dimensions` replaced the whole object and erased
    the measurement's provenance by omission."""

    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    with pytest.raises(PreservedMaterialMeasurementError, match="may not replace"):
        record_measurement_finding(
            ledger, locality_identity="r", finding=finding, extra=addition
        )


def test_recording_may_still_add_its_own_coordinate(recurrence_occurrences):
    ledger, occurrences = recurrence_occurrences
    finding = _yielded(ledger, occurrences)
    event = record_measurement_finding(
        ledger,
        locality_identity="r",
        finding=finding,
        extra={"a_recording_coordinate": "kept"},
    )
    assert event.material["a_recording_coordinate"] == "kept"
    assert event.material["dimensions"]["source_provenance"]
