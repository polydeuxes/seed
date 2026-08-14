"""A bounded comparison of a recorded finding and its production evidence."""

from __future__ import annotations

import pytest

from seed_runtime.event import Event
from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.adjacent_pair_measurement import measure_after
from seed_runtime.finding_fidelity import (
    ERASURE,
    FAITHFUL_WITHIN_SCOPE,
    FIDELITY_UNKNOWN,
    FIDELITY_FINDING_KIND,
    FIDELITY_CONVENTION,
    FIDELITY_RESULT_KIND,
    INVENTION,
    UNFAITHFUL_CROSSING,
    FindingFidelityError,
    compare_recorded_finding,
    get_recorded_fidelity_finding,
)
from seed_runtime.preserved_material_measurement import (
    INGRESS_OCCURRED_KIND,
    MEASUREMENT_CONVENTION,
    MEASUREMENT_RECORDED_KIND,
    RECURRENCE_RESULT_KIND,
    RESPONSIBILITY_UNRECOVERED,
    DeclaredMeasurement,
    measure_recurrence,
    record_measurement_finding,
)
from seed_runtime.production_evidence import (
    PRODUCTION_EVIDENCE_KIND,
    production_commitment,
)
from seed_runtime.support_basis import support_commitment


def _recorded_in(ledger):
    occurrences = [
        ledger.append(
            INGRESS_OCCURRED_KIND,
            "w",
            {
                "decoded_text": "the cat sat",
                "material_origin": "operator",
                "text_representation": {"available": True},
            },
            session_id="r",
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
        produce_in=(ledger, "w", "r"),
    )
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    return ledger, event


@pytest.fixture
def recorded():
    return _recorded_in(EventLedger())


def test_a_finding_that_names_the_evidence_concerning_it_is_faithful(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    assert result.kind == FIDELITY_FINDING_KIND
    assert result.payload["dimensions"]["standing"] == FAITHFUL_WITHIN_SCOPE
    assert result.payload["observed_crossings"] == []


def test_the_fidelity_finding_carries_evidence_that_the_act_produced_it(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    evidence = ledger.get(result.payload["production_evidence_id"])
    assert evidence.kind == PRODUCTION_EVIDENCE_KIND
    assert evidence.payload["produced_result_kind"] == FIDELITY_RESULT_KIND
    content = dict(result.payload)
    content.pop("production_evidence_id")
    content.pop("occurrence_preservation")
    assert evidence.payload["production_coordinates"] == sorted(content)
    assert evidence.payload["production_commitment"] == production_commitment(
        FIDELITY_CONVENTION, content
    )


def test_production_and_support_commitments_have_distinct_mechanical_domains():
    content = {"a": "b"}
    represented = '{"a":"b"}'
    assert production_commitment("x", content) != support_commitment(
        "x", (represented,)
    )


def test_result_shape_without_the_production_relation_has_no_witness(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    constructed = dict(result.payload)
    constructed.pop("production_evidence_id")
    forged = ledger.append(
        FIDELITY_FINDING_KIND, "w", constructed, session_id="r"
    )
    assert "production_evidence_id" not in forged.payload
    assert result.payload["production_evidence_id"] is not None


def test_a_produced_fidelity_finding_is_occurrence_bound_and_recoverable(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    recovered = get_recorded_fidelity_finding(ledger, result.id)
    assert recovered.recorded_occurrence_id == result.id
    assert recovered.production_evidence_id == result.payload[
        "production_evidence_id"
    ]
    assert recovered.source_finding_event_id == event.id
    assert recovered.standing == FAITHFUL_WITHIN_SCOPE
    assert recovered.reference == {"recorded_occurrence_id": result.id}


def test_recovery_exposes_no_mutable_result_payload(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    recovered = get_recorded_fidelity_finding(ledger, result.id)
    assert not hasattr(recovered, "payload")
    assert recovered.standing == result.payload["dimensions"]["standing"]


def test_recovery_does_not_revalidate_the_historical_input(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    # Recovery of F stands on F's intact recording occurrence and production
    # Evidence. Its source identity travels, but current source availability is
    # a later Act's responsibility. The in-memory ledger has no deletion
    # API, so this exact copy demonstrates that recovery does not require the
    # source to retain its old kind or shape.
    ledger._by_id[event.id] = Event(
        id=event.id,
        kind="representation.changed.after.fidelity",
        workspace_id=event.workspace_id,
        payload={},
        session_id=event.session_id,
    )
    recovered = get_recorded_fidelity_finding(ledger, result.id)
    assert recovered.source_finding_event_id == event.id


def test_a_fidelity_shaped_event_without_production_evidence_is_not_recovered(
    recorded,
):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    forged = dict(result.payload)
    forged.pop("production_evidence_id")
    occurrence = ledger.append(FIDELITY_FINDING_KIND, "w", forged, session_id="r")
    with pytest.raises(FindingFidelityError, match="coordinate surfaces"):
        get_recorded_fidelity_finding(ledger, occurrence.id)


def test_a_changed_fidelity_result_cannot_borrow_the_production_evidence(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    altered = dict(result.payload)
    altered["unknowns"] = ["an Unknown the comparison did not produce"]
    occurrence = ledger.append(FIDELITY_FINDING_KIND, "w", altered, session_id="r")
    with pytest.raises(FindingFidelityError, match="different Fidelity result"):
        get_recorded_fidelity_finding(ledger, occurrence.id)


def test_fidelity_recovery_survives_durable_reopen(tmp_path):
    path = tmp_path / "fidelity-recovery.sqlite"
    ledger, event = _recorded_in(SQLiteEventLedger(path))
    result = compare_recorded_finding(ledger, event.id)
    result_id = result.id
    ledger.close()

    reopened = SQLiteEventLedger(path)
    recovered = get_recorded_fidelity_finding(reopened, result_id)
    assert recovered.recorded_occurrence_id == result_id
    assert recovered.standing == FAITHFUL_WITHIN_SCOPE
    reopened.close()


def test_fidelity_recovery_refuses_an_invented_production_coordinate(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    evidence = ledger.get(result.payload["production_evidence_id"])
    forged_evidence = ledger.append(
        PRODUCTION_EVIDENCE_KIND,
        "w",
        {
            **evidence.payload,
            "production_coordinates": evidence.payload["production_coordinates"]
            + ["invented"],
        },
        session_id="r",
    )
    forged_result = ledger.append(
        FIDELITY_FINDING_KIND,
        "w",
        {**result.payload, "production_evidence_id": forged_evidence.id},
        session_id="r",
    )
    with pytest.raises(FindingFidelityError, match="exact Fidelity result contract"):
        get_recorded_fidelity_finding(ledger, forged_result.id)


def test_corrupted_fidelity_occurrence_cannot_be_recovered(tmp_path):
    ledger, event = _recorded_in(SQLiteEventLedger(tmp_path / "corrupt-result.sqlite"))
    result = compare_recorded_finding(ledger, event.id)
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET content_hash = ? WHERE id = ?",
        ("corrupted", result.id),
    )
    ledger._connection.commit()
    with pytest.raises(FindingFidelityError, match="corrupted occurrence"):
        get_recorded_fidelity_finding(ledger, result.id)
    ledger.close()


def test_a_finding_naming_no_production_evidence_preserves_erasure(recorded):
    ledger, event = recorded
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        "w",
        {**event.payload, "production_evidence_id": None},
        session_id="r",
    )
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["dimensions"]["standing"] == UNFAITHFUL_CROSSING
    assert result.payload["observed_crossings"] == [
        {
            "kind": ERASURE,
            "observation": (
                "the recorded finding does not preserve the required relation "
                "to production evidence"
            ),
        }
    ]


def test_a_content_mismatch_does_not_invent_which_crossing_caused_it(
    recorded,
):
    ledger, event = recorded
    altered = dict(event.payload)
    altered["total_count"] = 999
    forged = ledger.append(MEASUREMENT_RECORDED_KIND, "w", altered, session_id="r")
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["dimensions"]["standing"] == UNFAITHFUL_CROSSING
    assert result.payload["observed_crossings"] == [
        {
            "kind": FIDELITY_UNKNOWN,
            "observation": (
                "the named production evidence does not concern this exact "
                "recorded content"
            ),
        }
    ]


def test_the_comparison_revises_nothing(recorded):
    """`06.Standing.B`: availability is not revision."""

    ledger, event = recorded
    altered = dict(event.payload)
    altered["total_count"] = 999
    forged = ledger.append(MEASUREMENT_RECORDED_KIND, "w", altered, session_id="r")
    compare_recorded_finding(ledger, forged.id)
    # The finding found unfaithful is exactly as it was.
    assert ledger.get(forged.id).payload["total_count"] == 999
    assert ledger.get(forged.id).kind == MEASUREMENT_RECORDED_KIND


def test_it_claims_no_owner_and_no_correction_authority(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    dims = result.payload["dimensions"]
    assert dims["responsibility"] == RESPONSIBILITY_UNRECOVERED
    assert "correction authority" in dims["authority"]
    assert result.payload["revises"] == []


def test_it_preserves_what_the_clause_requires(recorded):
    """`01.External.D` names what a fidelity comparison must preserve."""

    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    for coordinate in (
        "constitutional_subject",
        "bounded_expectation",
        "implementation_witness",
        "observed_crossings",
        "evidence_and_provenance",
        "authority_boundary",
        "preserved_invariants",
        "conflicts",
        "unknowns",
        "lawful_stopping_point",
        "forbidden_inferences",
    ):
        assert coordinate in result.payload


def test_it_does_not_walk_what_the_finding_stood_on(recorded):
    """Each exact Act determines its own applicability -- `01.Standing.E.1`."""

    ledger, event = recorded
    before = len(ledger.list("w"))
    compare_recorded_finding(ledger, event.id)
    # Exactly this result and its production Evidence. Nothing upstream was
    # touched and no downstream applicability was determined.
    appended = ledger.list("w")[before:]
    assert [event.kind for event in appended] == [
        PRODUCTION_EVIDENCE_KIND,
        FIDELITY_FINDING_KIND,
    ]


def test_only_a_recorded_measurement_finding_may_be_compared(recorded):
    ledger, _ = recorded
    other = ledger.append("unrelated.kind", "w", {}, session_id="r")
    with pytest.raises(FindingFidelityError, match="not a recorded measurement"):
        compare_recorded_finding(ledger, other.id)


def test_positional_measurement_is_outside_the_recurrence_fidelity_scope(recorded):
    ledger, event = recorded
    occurrence = ledger.get(event.payload["consumed_event_ids"][0])
    finding = measure_after(
        [occurrence], "the", counting_scope="this locality"
    )
    positional = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    assert "production_evidence_id" not in positional.payload
    with pytest.raises(FindingFidelityError, match="not a recorded recurrence"):
        compare_recorded_finding(ledger, positional.id)


def test_unavailable_named_evidence_leaves_fidelity_unknown(recorded):
    """Naming evidence is not having it."""

    ledger, event = recorded
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        "w",
        {**event.payload, "production_evidence_id": "evt_never_appended"},
        session_id="r",
    )
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["dimensions"]["standing"] == FIDELITY_UNKNOWN
    assert result.payload["observed_crossings"] == []
    assert "unavailable" in " ".join(result.payload["unknowns"])


def test_a_finding_naming_something_that_is_not_production_evidence(recorded):
    ledger, event = recorded
    unrelated = ledger.append("unrelated.kind", "w", {}, session_id="r")
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        "w",
        {**event.payload, "production_evidence_id": unrelated.id},
        session_id="r",
    )
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["observed_crossings"][0]["kind"] == INVENTION


def test_lawful_recording_additions_do_not_change_the_produced_result(recorded):
    ledger, event = recorded
    # Build another lawful recording through the public recorder, because its
    # additive coordinate belongs to recording rather than Measurement.
    occurrences = [ledger.get(event.payload["consumed_event_ids"][0])]
    finding = measure_recurrence(
        occurrences,
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        produce_in=(ledger, "w", "r"),
    )
    added = record_measurement_finding(
        ledger,
        workspace_id="w",
        session_id="r",
        finding=finding,
        extra={"a_recording_coordinate": "kept"},
    )
    assert compare_recorded_finding(ledger, added.id).payload["dimensions"][
        "standing"
    ] == FAITHFUL_WITHIN_SCOPE


def test_missing_production_commitment_is_erasure(recorded):
    ledger, event = recorded
    evidence = ledger.append(
        PRODUCTION_EVIDENCE_KIND,
        "w",
        {
            "production_coordinates": ["total_count"],
            "produced_result_kind": RECURRENCE_RESULT_KIND,
            "production_convention": MEASUREMENT_CONVENTION,
        },
        session_id="r",
    )
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        "w",
        {**event.payload, "production_evidence_id": evidence.id},
        session_id="r",
    )
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["observed_crossings"][0]["kind"] == ERASURE


def test_missing_recorded_produced_coordinate_is_erasure(recorded):
    ledger, event = recorded
    altered = dict(event.payload)
    altered["dimensions"] = dict(altered["dimensions"])
    altered["dimensions"].pop("source_provenance")
    forged = ledger.append(MEASUREMENT_RECORDED_KIND, "w", altered, session_id="r")
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["observed_crossings"][0]["kind"] == ERASURE


def test_absent_locality_remains_absent(recorded):
    ledger, event = recorded
    without_locality = ledger.append(
        MEASUREMENT_RECORDED_KIND, "w", dict(event.payload), session_id=None
    )
    result = compare_recorded_finding(ledger, without_locality.id)
    assert result.payload["dimensions"]["scope_locality"] is None
    assert result.payload["dimensions"]["scope_workspace"] == "w"


def test_foreign_workspace_production_evidence_is_not_faithful(recorded):
    ledger, event = recorded
    foreign = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        "other-workspace",
        dict(event.payload),
        session_id="r",
    )
    result = compare_recorded_finding(ledger, foreign.id)
    assert result.payload["dimensions"]["standing"] == FIDELITY_UNKNOWN
    assert result.payload["observed_crossings"] == []
    assert "cross-workspace movement" in " ".join(result.payload["unknowns"])


def test_recording_coordinates_is_not_part_of_the_produced_fidelity_result(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    evidence = ledger.get(result.payload["production_evidence_id"])
    assert "occurrence_preservation" not in evidence.payload[
        "production_coordinates"
    ]
    assert result.payload["occurrence_preservation"].startswith(
        "Fidelity finding durably recorded"
    )


def test_corrupted_implementation_witness_is_refused(tmp_path):
    from seed_runtime.events import SQLiteEventLedger

    ledger = SQLiteEventLedger(tmp_path / "fidelity.sqlite")
    occurrence = ledger.append(
        INGRESS_OCCURRED_KIND,
        "w",
        {
            "decoded_text": "the cat sat",
            "material_origin": "operator",
            "text_representation": {"available": True},
        },
        session_id="r",
    )
    finding = measure_recurrence(
        [occurrence],
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        produce_in=(ledger, "w", "r"),
    )
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET content_hash = ? WHERE id = ?", ("corrupted", event.id)
    )
    ledger._connection.commit()
    with pytest.raises(FindingFidelityError, match="implementation witness"):
        compare_recorded_finding(ledger, event.id)
    ledger.close()


def test_corrupted_production_evidence_leaves_fidelity_unknown(tmp_path):
    from seed_runtime.events import SQLiteEventLedger

    ledger = SQLiteEventLedger(tmp_path / "fidelity-evidence.sqlite")
    occurrence = ledger.append(
        INGRESS_OCCURRED_KIND,
        "w",
        {
            "decoded_text": "the cat sat",
            "material_origin": "operator",
            "text_representation": {"available": True},
        },
        session_id="r",
    )
    finding = measure_recurrence(
        [occurrence],
        declared=DeclaredMeasurement(
            representation_measured="the",
            equivalence_rule="exact equality between whitespace-separated tokens",
            counting_scope="this locality",
        ),
        occurrences_of=lambda text: text.split().count("the"),
        produce_in=(ledger, "w", "r"),
    )
    event = record_measurement_finding(
        ledger, workspace_id="w", session_id="r", finding=finding
    )
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET content_hash = ? WHERE id = ?",
        ("corrupted", finding.production_evidence_id),
    )
    ledger._connection.commit()
    result = compare_recorded_finding(ledger, event.id)
    assert result.payload["dimensions"]["standing"] == FIDELITY_UNKNOWN
    assert "corrupted" in " ".join(result.payload["conflicts"])
    ledger.close()
