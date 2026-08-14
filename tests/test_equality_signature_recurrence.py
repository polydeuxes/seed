from copy import deepcopy

import pytest

from seed_runtime.adjacent_pair_measurement import AdjacentPair
from seed_runtime.assertion_comparison import (
    compare_positional_result_assertions,
    record_positional_result_comparison,
)
from seed_runtime.equality_signature_measurement import (
    record_equality_signature_layer,
)
from seed_runtime.equality_signature_recurrence import (
    EqualitySignatureRecurrenceError,
    _identity,
    assertions_of_recorded_equality_signature_count,
    get_recorded_equality_signature_count,
    measure_equality_signature_counts,
    record_equality_signature_count_layer,
)
from seed_runtime.events import EventLedger
from tests.test_positional_result_comparison import _record_following


def _record_compare(ledger, left, right):
    return record_positional_result_comparison(
        ledger,
        workspace_id="w",
        session_id="comparisons",
        comparison=compare_positional_result_assertions(
            ledger, (left.reference, right.reference)
        ),
    )


def _signatures():
    ledger = EventLedger()
    pair = AdjacentPair("it", "is")
    a = _record_following(ledger, "s1", "it is here\n", pair)
    b = _record_following(ledger, "s2", "it is there\n", pair)
    same_as_a = _record_following(ledger, "s3", "it is here\n", pair)
    _record_compare(ledger, a, b)
    _record_compare(ledger, a, b)
    _record_compare(ledger, a, b)
    _record_compare(ledger, a, same_as_a)
    assert record_equality_signature_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("comparisons",),
        recording_session_id="signatures",
    ) == 4
    return ledger


def test_identity_groups_supply_exact_counts_without_pair_formation():
    ledger = _signatures()

    findings = list(
        measure_equality_signature_counts(
            ledger, workspace_id="w", source_session_ids=("signatures",)
        )
    )
    assert len(findings) == 2
    assert sorted(item.count for item in findings) == [1, 3]
    assert sum(item.count for item in findings) == 4
    assert all(
        {ref["assertion_id"] for ref in item.production_refs}
        == {item.measured_assertion_id}
        for item in findings
    )


def test_streaming_reuses_signature_events_and_fetches_each_source_compare_once(
    monkeypatch,
):
    ledger = _signatures()
    signature_events = ledger.list_session("w", "signatures")
    signature_ids = {event.id for event in signature_events}
    source_ids = {event.payload["source_compare_event_id"] for event in signature_events}
    calls = []
    original_get = ledger.get

    def counted(event_id):
        calls.append(event_id)
        return original_get(event_id)

    monkeypatch.setattr(ledger, "get", counted)
    list(
        measure_equality_signature_counts(
            ledger, workspace_id="w", source_session_ids=("signatures",)
        )
    )

    assert signature_ids.isdisjoint(calls)
    assert all(calls.count(source_id) == 1 for source_id in source_ids)


def test_recording_fans_out_set_count_and_conditional_recurrence():
    ledger = _signatures()

    assert record_equality_signature_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("signatures",),
        recording_session_id="counts",
    ) == 2
    reconstructed = [
        assertions_of_recorded_equality_signature_count(event)
        for event in ledger.list_session("w", "counts")
    ]

    assert sorted(len(items) for items in reconstructed) == [2, 3]
    by_count = {
        next(
            item.payload["dimensions"]["content"]["production_count"]
            for item in items
            if item.result == "count"
        ): {item.result for item in items}
        for items in reconstructed
    }
    assert by_count == {
        1: {"exact_production_set", "count"},
        3: {"exact_production_set", "count", "recurrence"},
    }


def test_ledger_validation_proves_the_complete_bounded_signature_set():
    ledger = _signatures()
    record_equality_signature_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("signatures",),
        recording_session_id="counts",
    )

    for event in ledger.list_session("w", "counts"):
        for assertion in assertions_of_recorded_equality_signature_count(event):
            assert get_recorded_equality_signature_count(
                ledger,
                producing_event_id=event.id,
                assertion_id=assertion.assertion_id,
            ) == assertion


def test_validation_refuses_a_self_consistent_truncated_production_set():
    ledger = _signatures()
    record_equality_signature_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("signatures",),
        recording_session_id="counts",
    )
    event = next(
        event
        for event in ledger.list_session("w", "counts")
        if len(event.payload["assertions"]) == 3
    )
    production_set, count, recurrence = event.payload["assertions"]
    refs = deepcopy(production_set["support_basis"]["assertion_refs"][:-1])
    production_set["support_basis"] = {"assertion_refs": refs}
    production_set["dimensions"]["content"] = {"production_refs": refs}
    set_id = _identity(
        result="exact_production_set",
        subject=production_set["assertion_subject"],
        scope=production_set["assertion_scope"],
        content=production_set["dimensions"]["content"],
    )
    production_set["dimensions"]["identity"] = set_id
    count["dimensions"]["content"] = {"production_count": len(refs)}
    count_id = _identity(
        result="count",
        subject=count["assertion_subject"],
        scope=count["assertion_scope"],
        content=count["dimensions"]["content"],
    )
    count["dimensions"]["identity"] = count_id
    count["support_basis"] = {"local_assertion_ids": [set_id]}
    recurrence["support_basis"] = {"local_assertion_ids": [count_id]}

    with pytest.raises(
        EqualitySignatureRecurrenceError,
        match="does not equal the complete bounded read",
    ):
        get_recorded_equality_signature_count(
            ledger,
            producing_event_id=event.id,
            assertion_id=set_id,
        )


def test_results_preserve_the_dependency_chain_without_copying_support():
    ledger = _signatures()
    record_equality_signature_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("signatures",),
        recording_session_id="counts",
    )
    event = next(
        event
        for event in ledger.list_session("w", "counts")
        if len(event.payload["assertions"]) == 3
    )
    by_result = {item["result"]: item for item in event.payload["assertions"]}

    assert "assertion_refs" in by_result["exact_production_set"]["support_basis"]
    assert by_result["count"]["support_basis"] == {
        "local_assertion_ids": [
            by_result["exact_production_set"]["dimensions"]["identity"]
        ]
    }
    assert by_result["recurrence"]["support_basis"] == {
        "local_assertion_ids": [by_result["count"]["dimensions"]["identity"]]
    }
    assert "completeness_boundary" not in by_result["count"]
    assert "completeness_boundary" not in by_result["recurrence"]


@pytest.mark.parametrize("recording_session_id", ("", None, 7))
def test_recording_requires_an_exact_session(recording_session_id):
    ledger = _signatures()

    with pytest.raises(EqualitySignatureRecurrenceError, match="exact session"):
        record_equality_signature_count_layer(
            ledger,
            workspace_id="w",
            source_session_ids=("signatures",),
            recording_session_id=recording_session_id,
        )


def test_measurement_refuses_an_absent_declared_source_session():
    with pytest.raises(EqualitySignatureRecurrenceError, match="absent"):
        measure_equality_signature_counts(
            EventLedger(), workspace_id="w", source_session_ids=("missing",)
        )
