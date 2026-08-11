from copy import deepcopy

import pytest

from seed_runtime.adjacent_pair_measurement import AdjacentPair
from seed_runtime.assertion_comparison import (
    POSITIONAL_RESULT_COORDINATES,
    compare_positional_result_assertions,
    record_positional_result_comparison,
)
from seed_runtime.equality_signature_measurement import (
    EqualitySignatureMeasurementError,
    _identity,
    assertion_of_recorded_equality_signature,
    get_recorded_equality_signature,
    measure_equality_signatures,
    record_equality_signature_layer,
)
from seed_runtime.events import EventLedger
from tests.test_positional_result_comparison import _record_following


def _record_compare(ledger, *, left, right):
    return record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparisons",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )


def _comparison(ledger):
    pair = AdjacentPair("it", "is")
    left = _record_following(ledger, "s1", "it is here\n", pair)
    right = _record_following(ledger, "s2", "it is there\n", pair)
    return _record_compare(ledger, left=left, right=right)


def test_measurement_emits_the_complete_maximal_signature():
    ledger = EventLedger()
    source = _comparison(ledger)

    findings = list(
        measure_equality_signatures(
            ledger, workspace_id="w", source_session_ids=("comparisons",)
        )
    )

    assert len(findings) == 1
    finding = findings[0]
    assert finding.source_event_id == source.id
    assert set(finding.same_coordinates).isdisjoint(finding.different_coordinates)
    assert set(finding.same_coordinates) | set(finding.different_coordinates) == set(
        POSITIONAL_RESULT_COORDINATES
    )
    assert len(finding.source_assertions) == len(POSITIONAL_RESULT_COORDINATES)


def test_same_signature_has_one_identity_across_distinct_compares():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    left = _record_following(ledger, "s1", "it is here\n", pair)
    right = _record_following(ledger, "s2", "it is there\n", pair)
    first = _record_compare(ledger, left=left, right=right)
    second = _record_compare(ledger, left=left, right=right)

    assert record_equality_signature_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="signatures",
    ) == 2
    events = ledger.list_session("w", "signatures")
    recovered = [assertion_of_recorded_equality_signature(event) for event in events]

    assert len({item.assertion_id for item in recovered}) == 1
    assert {item.payload["source_compare_event_id"] for item in recovered} == {
        first.id,
        second.id,
    }
    assert all(
        len(item.payload["support_basis"]["assertion_refs"])
        == len(POSITIONAL_RESULT_COORDINATES)
        for item in recovered
    )


def test_ledger_recovery_replays_the_complete_source_surface():
    ledger = EventLedger()
    _comparison(ledger)
    record_equality_signature_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="signatures",
    )
    event = ledger.list_session("w", "signatures")[0]
    assertion = assertion_of_recorded_equality_signature(event)

    assert get_recorded_equality_signature(
        ledger,
        producing_event_id=event.id,
        assertion_id=assertion.assertion_id,
    ) == assertion


def test_recovery_refuses_an_incomplete_signature():
    ledger = EventLedger()
    _comparison(ledger)
    record_equality_signature_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="signatures",
    )
    event = ledger.list_session("w", "signatures")[0].model_copy(deep=True)
    assertion = event.payload["assertions"][0]
    moved = assertion["dimensions"]["content"]["same_coordinates"].pop()
    assertion["dimensions"]["content"]["different_coordinates"].append(moved)

    with pytest.raises(EqualitySignatureMeasurementError):
        assertion_of_recorded_equality_signature(event)


def test_ledger_recovery_refuses_a_self_consistent_false_signature():
    ledger = EventLedger()
    _comparison(ledger)
    record_equality_signature_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="signatures",
    )
    original = ledger.list_session("w", "signatures")[0]
    payload = deepcopy(original.payload)
    assertion = payload["assertions"][0]
    content = assertion["dimensions"]["content"]
    moved = content["same_coordinates"].pop()
    content["different_coordinates"] = [
        name
        for name in POSITIONAL_RESULT_COORDINATES
        if name in {*content["different_coordinates"], moved}
    ]
    assertion["dimensions"]["identity"] = _identity(
        scope=assertion["assertion_scope"], content=content
    )
    forged = ledger.append(
        original.kind,
        "w",
        payload,
        session_id="signatures",
    )

    with pytest.raises(
        EqualitySignatureMeasurementError,
        match="does not match its complete source Compare surface",
    ):
        get_recorded_equality_signature(
            ledger,
            producing_event_id=forged.id,
            assertion_id=assertion["dimensions"]["identity"],
        )


def test_signature_does_not_claim_equivalence_or_select_a_subset():
    ledger = EventLedger()
    _comparison(ledger)
    record_equality_signature_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="signatures",
    )
    event = ledger.list_session("w", "signatures")[0]
    assertion = event.payload["assertions"][0]

    assert assertion["assertion_subject"]["declared_coordinate_surface"] == list(
        POSITIONAL_RESULT_COORDINATES
    )
    assert "no Equivalence" in assertion["dimensions"]["authority_warrant"]
    assert "not Equivalence" in assertion["forbidden_inferences"][0]
    assert "selected_coordinates" not in str(event.payload)
