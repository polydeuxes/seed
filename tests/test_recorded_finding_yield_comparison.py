"""A bounded Compare of a recorded finding and its Yield Evidence."""

from __future__ import annotations

import pytest

from seed_runtime.event import Event
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.adjacency_pair_measurement import measure_after
from seed_runtime.recorded_finding_yield_comparison import (
    ERASURE,
    AGREES_WITH_YIELD_EVIDENCE,
    COMPARISON_UNKNOWN,
    FINDING_YIELD_COMPARISON_KIND,
    FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND,
    FINDING_YIELD_COMPARISON_RESULT_KIND,
    FINDING_YIELD_COMPARISON_RESPONSIBILITY,
    UNSUPPORTED_COORDINATE,
    DIFFERS_FROM_YIELD_EVIDENCE,
    RecordedFindingYieldComparisonError,
    compare_recorded_finding_yield,
    get_recorded_finding_yield_comparison,
)
from seed_runtime.preserved_material_measurement import (
    INGEST_OCCURRED_KIND,
    MEASUREMENT_RECORDED_KIND,
    RECURRENCE_RESULT_KIND,
    DeclaredMeasurement,
    measure_recurrence,
    record_measurement_finding,
)
from seed_runtime.yield_evidence import YIELD_EVIDENCE_KIND


def _recorded_in(ledger):
    occurrences = [
        ledger.append(
            INGEST_OCCURRED_KIND,
            {
                "represented_material": "the cat sat",
            },
            locality_identity="r",
        )
    ]
    finding = measure_recurrence(
        occurrences,
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        yield_in=(ledger, "w", "r"),
    )
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    return ledger, event


@pytest.fixture
def recorded():
    return _recorded_in(EventLedger())


def test_a_finding_that_names_the_evidence_concerning_it_is_agreeing(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    assert result.kind == FINDING_YIELD_COMPARISON_KIND
    assert result.material["dimensions"]["standing"] == AGREES_WITH_YIELD_EVIDENCE
    assert result.material["crossings"] == []


def test_the_comparison_finding_carries_evidence_that_the_act_yielded_it(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    evidence = ledger.get(result.material["yield_evidence_identity"])
    assert evidence.kind == YIELD_EVIDENCE_KIND
    assert evidence.material["result_kind"] == FINDING_YIELD_COMPARISON_RESULT_KIND
    assert evidence.material["dimensions"]["act_occurrence_identity"] == result.material[
        "act_occurrence_identity"
    ]
    content = dict(result.material)
    content.pop("responsible_act_evidence_identity")
    content.pop("yield_evidence_identity")
    content.pop("occurrence_preservation")
    assert evidence.material["yield_coordinates"] == sorted(content)
    assert evidence.material["result"] == content


def test_result_shape_without_the_yield_relation_has_no_witness(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    supplied = dict(result.material)
    supplied.pop("yield_evidence_identity")
    forged = ledger.append(
        FINDING_YIELD_COMPARISON_KIND, supplied, locality_identity="r"
    )
    assert "yield_evidence_identity" not in forged.material
    assert result.material["yield_evidence_identity"] is not None


def test_a_yielded_comparison_finding_is_occurrence_bound_and_addressable(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    read = get_recorded_finding_yield_comparison(ledger, result.identity)
    assert read.recorded_occurrence_identity == result.identity
    assert read.yield_evidence_identity == result.material[
        "yield_evidence_identity"
    ]
    assert read.source_finding_event_identity == event.identity
    assert read.standing == AGREES_WITH_YIELD_EVIDENCE
    assert read.reference == {"recorded_occurrence_identity": result.identity}


def test_validation_exposes_no_mutable_result_material(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    read = get_recorded_finding_yield_comparison(ledger, result.identity)
    assert not hasattr(read, "material")
    assert read.standing == result.material["dimensions"]["standing"]


def test_validation_does_not_revalidate_the_historical_input(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    # Read of F stands on F's intact recording occurrence and yield
    # Evidence. Its source identity travels, but current source availability is
    # a later Act's responsibility. The in-memory ledger has no deletion
    # API, so this exact copy demonstrates that read does not require the
    # source to retain its old kind or shape.
    ledger._by_identity[event.identity] = Event(
        identity=event.identity,
        kind="representation.different.after.comparison",
        material={},
        locality_identity=event.locality_identity,
    )
    read = get_recorded_finding_yield_comparison(ledger, result.identity)
    assert read.source_finding_event_identity == event.identity


def test_a_comparison_shaped_event_without_yield_evidence_is_not_validated(
    recorded,
):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    forged = dict(result.material)
    forged.pop("yield_evidence_identity")
    occurrence = ledger.append(FINDING_YIELD_COMPARISON_KIND, forged, locality_identity="r")
    with pytest.raises(RecordedFindingYieldComparisonError, match="coordinate surfaces"):
        get_recorded_finding_yield_comparison(ledger, occurrence.identity)


def test_a_changed_comparison_result_cannot_borrow_the_yield_evidence(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    altered = dict(result.material)
    altered["unknowns"] = ["an Unknown the comparison did not yield"]
    occurrence = ledger.append(FINDING_YIELD_COMPARISON_KIND, altered, locality_identity="r")
    with pytest.raises(RecordedFindingYieldComparisonError, match="different Compare result"):
        get_recorded_finding_yield_comparison(ledger, occurrence.identity)


def test_comparison_validation_survives_durable_reopen(tmp_path):
    path = tmp_path / "comparison-read.sqlite"
    ledger, event = _recorded_in(SQLiteEventLedger(path))
    result = compare_recorded_finding_yield(ledger, event.identity)
    result_identity = result.identity
    ledger.close()

    reopened = SQLiteEventLedger(path)
    read = get_recorded_finding_yield_comparison(reopened, result_identity)
    assert read.recorded_occurrence_identity == result_identity
    assert read.standing == AGREES_WITH_YIELD_EVIDENCE
    reopened.close()


def test_comparison_validation_refuses_an_unsupported_yield_coordinate(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    evidence = ledger.get(result.material["yield_evidence_identity"])
    forged_evidence = ledger.append(
        YIELD_EVIDENCE_KIND,
        {
            **evidence.material,
            "yield_coordinates": evidence.material["yield_coordinates"]
            + ["unsupported"],
        },
        locality_identity="r",
    )
    forged_result = ledger.append(
        FINDING_YIELD_COMPARISON_KIND,
        {**result.material, "yield_evidence_identity": forged_evidence.identity},
        locality_identity="r",
    )
    with pytest.raises(RecordedFindingYieldComparisonError, match="exact Compare result contract"):
        get_recorded_finding_yield_comparison(ledger, forged_result.identity)


def test_corrupted_comparison_occurrence_cannot_be_validated(tmp_path):
    ledger, event = _recorded_in(SQLiteEventLedger(tmp_path / "corrupt-result.sqlite"))
    result = compare_recorded_finding_yield(ledger, event.identity)
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET occurrence_material_identity = ? WHERE identity= ?",
        ("corrupted", result.identity),
    )
    ledger._connection.commit()
    with pytest.raises(RecordedFindingYieldComparisonError, match="corrupted occurrence"):
        get_recorded_finding_yield_comparison(ledger, result.identity)
    ledger.close()


def test_a_finding_naming_no_yield_evidence_preserves_erasure(recorded):
    ledger, event = recorded
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        {**event.material, "yield_evidence_identity": None},
        locality_identity="r",
    )
    result = compare_recorded_finding_yield(ledger, forged.identity)
    assert result.material["dimensions"]["standing"] == DIFFERS_FROM_YIELD_EVIDENCE
    assert result.material["crossings"] == [
        {
            "kind": ERASURE,
            "material": (
                "the recorded finding does not preserve the required relation "
                "to yield evidence"
            ),
        }
    ]


def test_a_content_mismatch_does_not_assert_which_crossing_caused_it(
    recorded,
):
    ledger, event = recorded
    altered = dict(event.material)
    altered["total_count"] = 999
    forged = ledger.append(MEASUREMENT_RECORDED_KIND, altered, locality_identity="r")
    result = compare_recorded_finding_yield(ledger, forged.identity)
    assert result.material["dimensions"]["standing"] == DIFFERS_FROM_YIELD_EVIDENCE
    assert result.material["crossings"] == [
        {
            "kind": COMPARISON_UNKNOWN,
            "material": (
                "the named yield evidence does not concern this exact "
                "recorded content"
            ),
        }
    ]


def test_the_comparison_revises_nothing(recorded):
    """`06.Standing.B`: availability is not revision."""

    ledger, event = recorded
    altered = dict(event.material)
    altered["total_count"] = 999
    forged = ledger.append(MEASUREMENT_RECORDED_KIND, altered, locality_identity="r")
    compare_recorded_finding_yield(ledger, forged.identity)
    # The finding found differing is exactly as it was.
    assert ledger.get(forged.identity).material["total_count"] == 999
    assert ledger.get(forged.identity).kind == MEASUREMENT_RECORDED_KIND


def test_it_preserves_exact_responsibility_and_no_correction_authority(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    dims = result.material["dimensions"]
    assert dims["responsibility"] == FINDING_YIELD_COMPARISON_RESPONSIBILITY
    assert "correction authority" in dims["authority"]


def test_it_preserves_what_the_clause_requires(recorded):
    """`01.Source.C` names what a comparison comparison must preserve."""

    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    for coordinate in (
        "constitutional_subject",
        "compared_relation",
        "recorded_finding_reference",
        "crossings",
        "evidence_and_provenance",
        "authority_boundary",
        "conflicts",
        "unknowns",
        "limits",
    ):
        assert coordinate in result.material


def test_it_does_not_walk_what_the_finding_stood_on(recorded):
    """Each exact Act determines its own applicability -- `01.Standing.E.1`."""

    ledger, event = recorded
    before = len(ledger.list())
    compare_recorded_finding_yield(ledger, event.identity)
    # Exactly this Act Evidence, Yield Evidence, and result. Nothing upstream was
    # touched and no downstream applicability was determined.
    appended = ledger.list()[before:]
    assert [event.kind for event in appended] == [
        FINDING_YIELD_COMPARISON_ACT_EVIDENCE_KIND,
        YIELD_EVIDENCE_KIND,
        FINDING_YIELD_COMPARISON_KIND,
    ]


def test_only_a_recorded_measurement_finding_may_be_compared(recorded):
    ledger, _ = recorded
    other = ledger.append("unrelated.kind", {}, locality_identity="r")
    with pytest.raises(RecordedFindingYieldComparisonError, match="not a recorded measurement"):
        compare_recorded_finding_yield(ledger, other.identity)


def test_positional_measurement_is_outside_the_recurrence_comparison_scope(recorded):
    ledger, event = recorded
    occurrence = ledger.get(event.material["input_event_identities"][0])
    finding = measure_after(
        [occurrence], "the", counting_scope="this locality"
    )
    positional = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    assert "yield_evidence_identity" not in positional.material
    with pytest.raises(RecordedFindingYieldComparisonError, match="not a recorded recurrence"):
        compare_recorded_finding_yield(ledger, positional.identity)


def test_unavailable_named_evidence_leaves_comparison_unknown(recorded):
    """Naming evidence is not having it."""

    ledger, event = recorded
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        {**event.material, "yield_evidence_identity": "evt_never_appended"},
        locality_identity="r",
    )
    result = compare_recorded_finding_yield(ledger, forged.identity)
    assert result.material["dimensions"]["standing"] == COMPARISON_UNKNOWN
    assert result.material["crossings"] == []
    assert "unavailable" in " ".join(result.material["unknowns"])


def test_a_finding_naming_something_that_is_not_yield_evidence(recorded):
    ledger, event = recorded
    unrelated = ledger.append("unrelated.kind", {}, locality_identity="r")
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        {**event.material, "yield_evidence_identity": unrelated.identity},
        locality_identity="r",
    )
    result = compare_recorded_finding_yield(ledger, forged.identity)
    assert (
        result.material["crossings"][0]["kind"]
        == UNSUPPORTED_COORDINATE
    )


def test_lawful_recording_additions_do_not_change_the_result(recorded):
    ledger, event = recorded
    # Build another lawful recording through the public recorder, because its
    # additive coordinate belongs to recording rather than Measurement.
    occurrences = [ledger.get(event.material["input_event_identities"][0])]
    finding = measure_recurrence(
        occurrences,
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        yield_in=(ledger, "w", "r"),
    )
    added = record_measurement_finding(
        ledger,
        locality_identity="r",
        finding=finding,
        extra={"a_recording_coordinate": "kept"},
    )
    assert compare_recorded_finding_yield(ledger, added.identity).material["dimensions"][
        "standing"
    ] == AGREES_WITH_YIELD_EVIDENCE


def test_missing_yield_result_is_erasure(recorded):
    ledger, event = recorded
    evidence = ledger.append(
        YIELD_EVIDENCE_KIND,
        {
            "yield_coordinates": ["total_count"],
            "result_kind": RECURRENCE_RESULT_KIND,
        },
        locality_identity="r",
    )
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        {**event.material, "yield_evidence_identity": evidence.identity},
        locality_identity="r",
    )
    result = compare_recorded_finding_yield(ledger, forged.identity)
    assert result.material["crossings"][0]["kind"] == ERASURE


def test_missing_recorded_yielded_coordinate_is_erasure(recorded):
    ledger, event = recorded
    altered = dict(event.material)
    altered["dimensions"] = dict(altered["dimensions"])
    altered["dimensions"].pop("source_provenance")
    forged = ledger.append(MEASUREMENT_RECORDED_KIND, altered, locality_identity="r")
    result = compare_recorded_finding_yield(ledger, forged.identity)
    assert result.material["crossings"][0]["kind"] == ERASURE


def test_absent_locality_remains_absent(recorded):
    ledger, event = recorded
    without_locality = ledger.append(
        MEASUREMENT_RECORDED_KIND, dict(event.material), locality_identity=None
    )
    result = compare_recorded_finding_yield(ledger, without_locality.identity)
    assert result.material["dimensions"]["scope_locality"] is None


def test_recording_coordinates_is_not_part_of_the_yielded_comparison_result(recorded):
    ledger, event = recorded
    result = compare_recorded_finding_yield(ledger, event.identity)
    evidence = ledger.get(result.material["yield_evidence_identity"])
    assert "occurrence_preservation" not in evidence.material[
        "yield_coordinates"
    ]
    assert result.material["occurrence_preservation"].startswith(
        "recorded finding Yield comparison durably recorded"
    )


def test_corrupted_recorded_finding_ref_is_refused(tmp_path):
    from seed_runtime.events import SQLiteEventLedger

    ledger = SQLiteEventLedger(tmp_path / "comparison.sqlite")
    occurrence = ledger.append(
        INGEST_OCCURRED_KIND,
        {
            "represented_material": "the cat sat",
        },
        locality_identity="r",
    )
    finding = measure_recurrence(
        [occurrence],
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        yield_in=(ledger, "w", "r"),
    )
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET occurrence_material_identity = ? WHERE identity= ?", ("corrupted", event.identity)
    )
    ledger._connection.commit()
    with pytest.raises(RecordedFindingYieldComparisonError, match="recorded finding"):
        compare_recorded_finding_yield(ledger, event.identity)
    ledger.close()


def test_corrupted_yield_evidence_leaves_comparison_unknown(tmp_path):
    from seed_runtime.events import SQLiteEventLedger

    ledger = SQLiteEventLedger(tmp_path / "comparison-evidence.sqlite")
    occurrence = ledger.append(
        INGEST_OCCURRED_KIND,
        {
            "represented_material": "the cat sat",
        },
        locality_identity="r",
    )
    finding = measure_recurrence(
        [occurrence],
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        yield_in=(ledger, "w", "r"),
    )
    event = record_measurement_finding(
        ledger, locality_identity="r", finding=finding
    )
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET occurrence_material_identity = ? WHERE identity= ?",
        ("corrupted", finding.yield_evidence_identity),
    )
    ledger._connection.commit()
    result = compare_recorded_finding_yield(ledger, event.identity)
    assert result.material["dimensions"]["standing"] == COMPARISON_UNKNOWN
    assert "corrupted" in " ".join(result.material["conflicts"])
    ledger.close()
