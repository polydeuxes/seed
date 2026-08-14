"""A recorded finding supplies the next representation, and every pair gets the same battery.

`#2391` recovered ordered pairs whose adjacency reproduces across independently
bounded scopes, without a reader naming a representation, occupant, or
delimiter. It left one gap: the candidates were enumerated in a scratch run, so
the loop was demonstrated rather than preserved.

This closes that. :func:`adjacent_pairs_from_finding` reads pairs out of a recorded
measurement finding, which is why a finding must record the representation it measured
after — a finding that does not is refused as a source of pairs. Every
measurement then carries that finding as its premise, so the chain is
recoverable from the ledger rather than from a transcript.

The battery is four generic adjacency questions applied to every pair without
exception. A question whose answer is absent is still asked and still recorded;
dropping empty results would report only the questions that happened to
succeed.

Nothing here establishes represented relation, grammatical kind, relation, or truth.
"""

from __future__ import annotations

import json
from io import StringIO
from itertools import product

import pytest

from seed_runtime.events import EventLedger, InvalidLedgerBoundary
from seed_runtime.support_basis import SupportBasis, SupportRecovery
from seed_runtime.event import Event
from seed_runtime.adjacent_pair_measurement import (
    AdjacentPairMeasurementIndex,
    EQUIVALENCE_RULE,
    enumerate_displacements,
    enumerate_representations,
    measure_after,
    measure_at_displacement,
    AdjacentPair,
    measure_adjacent_pair,
    adjacent_pairs_from_finding,
    assertion_of_recorded_adjacent_pair_result,
    get_recorded_adjacent_pair_result_assertion,
    record_pair_measurements,
    record_adjacent_pair_measurement_layer,
    group_by_highest_count_occupant,
    occupant_agreement_across_scopes,
)
from seed_runtime.preserved_material_measurement import (
    INGRESS_OCCURRED_KIND,
    DeclaredMeasurement,
    Occupancy,
    PreservedMaterialMeasurementError,
    measure_occupancy,
    premise_chain,
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from seed_runtime.operator_console import run_persistent_operator_console

SCOPE = "whole session"
MATERIAL = (
    "it is a word and it is a thing\n"
    "It is another word\n"
    "and it is not a word\n"
    "it may be a word\n"
    "of the word and of the thing\n"
)
LEFT = "it"


def _after_left(text):
    parts = text.split()
    for index in range(len(parts) - 1):
        if parts[index] == LEFT:
            return parts[index + 1]
    return None


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


@pytest.fixture
def recorded_finding(session, occurrences):
    finding = measure_after(
        occurrences,
        LEFT,
        counting_scope="preserved ingress occurrences of this session",
    )
    return record_measurement_finding(
        session, workspace_id="w", session_id="s", finding=finding
    )


# --------------------------------------------------------------------------
# The representation comes out of the record.
# --------------------------------------------------------------------------


def test_a_finding_records_the_representation_it_measured_after(recorded_finding):
    """Without this a finding cannot supply an representation to anything."""
    assert recorded_finding.payload["measured_left_representation"] == LEFT


def test_pairs_are_read_from_the_record_not_supplied(session, recorded_finding):
    pairs = adjacent_pairs_from_finding(session, recorded_finding.id)
    assert pairs
    assert all(pair.left == LEFT for pair in pairs)
    assert AdjacentPair(left="it", right="is") in pairs


def test_every_occupancy_becomes_a_pair_with_no_filtering(session, recorded_finding):
    """No count, share, or threshold decides which pairs are returned."""
    pairs = adjacent_pairs_from_finding(session, recorded_finding.id)
    assert len(pairs) == len(recorded_finding.payload["occupancies"])


def test_a_finding_that_names_no_representation_cannot_supply_one(session, occurrences):
    event = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_occupancy(
            occurrences,
            declared=DeclaredMeasurement(
                representation_measured="the first representation",
                equivalence_rule=EQUIVALENCE_RULE,
                counting_scope="this session",
            ),
            occupant_of=lambda t: (t.split() or [None])[0],
        ),
    )
    with pytest.raises(PreservedMaterialMeasurementError):
        adjacent_pairs_from_finding(session, event.id)


def test_pairs_must_come_from_a_measurement_finding(session, occurrences):
    foreign = session.append("unrelated.kind", "w", {"occupancies": []}, session_id="s")
    with pytest.raises(PreservedMaterialMeasurementError):
        adjacent_pairs_from_finding(session, foreign.id)


# --------------------------------------------------------------------------
# The battery is applied symmetrically.
# --------------------------------------------------------------------------


def test_every_pair_receives_every_question(occurrences, recorded_finding):
    expected = {"preceding", "following", "before_same_right", "after_same_left"}
    for pair in (AdjacentPair("it", "is"), AdjacentPair("it", "may"), AdjacentPair("of", "the")):
        findings = measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        )
        assert set(findings) == expected


def test_batched_pair_measurement_is_exactly_the_existing_battery(
    occurrences, recorded_finding
):
    pairs = (
        AdjacentPair("it", "is"),
        AdjacentPair("it", "may"),
        AdjacentPair("of", "the"),
    )
    index = AdjacentPairMeasurementIndex(occurrences)

    measured = index.measure_all(
        ((pair, recorded_finding.id) for pair in pairs),
        counting_scope="this session",
    )

    assert [pair for pair, _ in measured] == list(pairs)
    for pair, findings in measured:
        assert findings == measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        )


def test_batched_pair_measurement_tokenizes_each_occurrence_once(
    monkeypatch, occurrences, recorded_finding
):
    import seed_runtime.adjacent_pair_measurement as module

    calls = 0
    original = module._positions

    def counted(text):
        nonlocal calls
        calls += 1
        return original(text)

    monkeypatch.setattr(module, "_positions", counted)
    index = AdjacentPairMeasurementIndex(occurrences)
    pairs = (
        AdjacentPair("it", "is"),
        AdjacentPair("it", "may"),
        AdjacentPair("of", "the"),
    )
    index.measure_all(
        ((pair, recorded_finding.id) for pair in pairs),
        counting_scope="this session",
    )

    assert calls == len(occurrences)


def test_batched_pair_measurement_requires_each_premise_identity(occurrences):
    pair = AdjacentPair("it", "is")
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="no premise occurrence identity",
    ):
        AdjacentPairMeasurementIndex(occurrences).measure_all(
            ((pair, ""),), counting_scope="this session"
        )


def test_batched_pair_measurement_preserves_duplicate_subject_premises(occurrences):
    pair = AdjacentPair("it", "is")
    measured = AdjacentPairMeasurementIndex(occurrences).measure_all(
        ((pair, "premise-1"), (pair, "premise-2")),
        counting_scope="this session",
    )

    assert [pair for pair, _ in measured] == [pair, pair]
    assert [
        findings["preceding"].declared.premise_event_id
        for _, findings in measured
    ] == ["premise-1", "premise-2"]


def test_batched_pair_index_preserves_first_match_semantics_exhaustively():
    alphabet = ("a", "b", "c")
    occurrences = [
        Event(
            id=f"event-{index}",
            kind="operator.ingress.ingress_occurred",
            workspace_id="w",
            session_id="s",
            payload={"decoded_text": " ".join(parts)},
        )
        for index, parts in enumerate(
            parts
            for length in range(1, 6)
            for parts in product(alphabet, repeat=length)
        )
    ]
    index = AdjacentPairMeasurementIndex(occurrences)

    for left in alphabet:
        for right in alphabet:
            pair = AdjacentPair(left, right)
            assert index.measure(
                pair,
                counting_scope="exhaustive bounded fixture",
                premise_event_id="premise",
            ) == measure_adjacent_pair(
                occurrences,
                pair,
                counting_scope="exhaustive bounded fixture",
                premise_event_id="premise",
            )


def test_one_layer_records_every_pair_form_and_nothing_beyond(
    session, recorded_finding
):
    before = {event.id for event in session.list("w")}
    boundary = session.capture_boundary()
    pair_count = len(recorded_finding.payload["occupancies"])

    recorded_count = record_adjacent_pair_measurement_layer(
        session,
        workspace_id="w",
        session_id="s",
        counting_scope="this session",
    )
    recorded = [event for event in session.list("w") if event.id not in before]

    assert recorded_count == pair_count * 4
    assert len(recorded) == recorded_count
    assert {event.payload["measurement_form"] for event in recorded} == {
        "preceding",
        "following",
        "before_same_right",
        "after_same_left",
    }
    assert {event.payload["premise_event_id"] for event in recorded} == {
        recorded_finding.id
    }
    assert all(event.payload["measurement_form"] != "after" for event in recorded)
    assert all(
        assertion_of_recorded_adjacent_pair_result(event).producing_event_id
        == event.id
        for event in recorded
    )
    assert {
        event.payload["completeness_boundary"]["commitment"] for event in recorded
    } == {boundary.commitment}


def test_one_layer_preserves_duplicate_pair_subject_productions(
    session, recorded_finding
):
    second_premise = session.append(
        recorded_finding.kind,
        recorded_finding.workspace_id,
        recorded_finding.model_copy(deep=True).payload,
        session_id=recorded_finding.session_id,
    )
    pair_count = len(recorded_finding.payload["occupancies"])

    recorded_count = record_adjacent_pair_measurement_layer(
        session,
        workspace_id="w",
        session_id="s",
        counting_scope="this session",
    )
    produced = [
        event
        for event in session.list("w")
        if event.payload.get("premise_event_id")
        in {recorded_finding.id, second_premise.id}
    ]

    assert recorded_count == pair_count * 2 * 4
    assert len(produced) == recorded_count
    assert {
        premise: sum(
            event.payload["premise_event_id"] == premise for event in produced
        )
        for premise in (recorded_finding.id, second_premise.id)
    } == {
        recorded_finding.id: pair_count * 4,
        second_premise.id: pair_count * 4,
    }


def test_one_layer_refuses_claimed_after_premises_without_exact_coordinates(
    session, recorded_finding
):
    malformed = []
    mutations = (
        lambda payload: payload.update(
            measured_position={
                "anchored_on": "the representation",
                "direction": "before",
                "displacement": 1,
            }
        ),
        lambda payload: payload.update(measured_relative_to=["another"]),
        lambda payload: payload.update(
            equivalence_rule="a different asserted equivalence rule"
        ),
        lambda payload: payload.update(convention="another-convention"),
    )
    for mutate in mutations:
        payload = recorded_finding.model_copy(deep=True).payload
        mutate(payload)
        malformed.append(
            session.append(
                recorded_finding.kind,
                recorded_finding.workspace_id,
                payload,
                session_id=recorded_finding.session_id,
            )
        )

    recorded_count = record_adjacent_pair_measurement_layer(
        session,
        workspace_id="w",
        session_id="s",
        counting_scope="this session",
    )
    produced = [
        event
        for event in session.list("w")
        if event.payload.get("premise_event_id") is not None
    ]

    assert recorded_count == len(recorded_finding.payload["occupancies"]) * 4
    assert {event.payload["premise_event_id"] for event in produced} == {
        recorded_finding.id
    }
    assert not ({event.id for event in malformed} & {
        event.payload["premise_event_id"] for event in produced
    })


def test_one_layer_persists_results_in_a_bounded_batch(session, recorded_finding):
    batches = []
    original = session.append_many

    def tracked(events, **kwargs):
        supplied = list(events)
        batches.append(len(supplied))
        return original(supplied, **kwargs)

    session.append_many = tracked
    recorded_count = record_adjacent_pair_measurement_layer(
        session,
        workspace_id="w",
        session_id="s",
        counting_scope="this session",
    )

    assert recorded_count == len(recorded_finding.payload["occupancies"]) * 4
    assert batches == [recorded_count]


def test_a_question_that_found_nothing_is_still_recorded(
    session, occurrences, recorded_finding
):
    """`of the` never appears with anything after it in this material."""
    pair = AdjacentPair("of", "the")
    findings = measure_adjacent_pair(
        occurrences,
        pair,
        counting_scope="this session",
        premise_event_id=recorded_finding.id,
    )
    recorded = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pair,
        findings=findings,
        completeness_boundary=session.capture_boundary(),
    )
    assert set(recorded) == set(findings)
    assert any(f.highest_count_occupancy is None for f in findings.values())
    for event in recorded.values():
        assert "occupancies" in event.payload


def test_an_absent_position_is_absent_not_unknown(occurrences, recorded_finding):
    findings = measure_adjacent_pair(
        occurrences,
        AdjacentPair("it", "is"),
        counting_scope="this session",
        premise_event_id=recorded_finding.id,
    )
    preceding = findings["preceding"]
    assert preceding.positions_measured < len(preceding.consumed_event_ids)
    assert "Unknown" not in str(preceding.occupancies)


# --------------------------------------------------------------------------
# The premise travels with every measurement.
# --------------------------------------------------------------------------


def test_each_measurement_records_its_premise(
    session, occurrences, recorded_finding
):
    pair = AdjacentPair("it", "is")
    recorded = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pair,
        findings=measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        ),
        completeness_boundary=session.capture_boundary(),
    )
    for name, event in recorded.items():
        assert event.payload["premise_event_id"] == recorded_finding.id
        assert event.payload["measurement"] == name
        assert event.payload["pair_left"] == "it"
        assert event.payload["pair_right"] == "is"
        assert premise_chain(session, event.id) == [recorded_finding.id]


def test_recording_does_not_alter_the_premise(session, occurrences, recorded_finding):
    before = dict(recorded_finding.payload)
    pair = AdjacentPair("it", "is")
    record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pair,
        findings=measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        ),
        completeness_boundary=session.capture_boundary(),
    )
    assert session.get(recorded_finding.id).payload == before


def test_each_pair_result_is_one_addressable_assertion(
    session, occurrences, recorded_finding
):
    pair = AdjacentPair("it", "is")
    boundary = session.capture_boundary()
    recorded = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pair,
        findings=measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        ),
        completeness_boundary=boundary,
    )

    for event in recorded.values():
        assertion = assertion_of_recorded_adjacent_pair_result(event)
        assert assertion.producing_event_id == event.id
        assert assertion.reference == {
            "producing_event_id": event.id,
            "assertion_id": event.payload["dimensions"]["identity"],
        }
        assert event.payload["dimensions"]["content"] == {
            "positions_measured": event.payload["positions_measured"],
            "occupancies": event.payload["occupancies"],
        }
        assert event.payload["completeness_boundary"] == {
            "commitment": boundary.commitment
        }
        assert "consumed_event_ids" not in event.payload
        assert event.payload["support_basis"]["basis"] == event.payload["consumed_support"]
        assert get_recorded_adjacent_pair_result_assertion(
            session,
            producing_event_id=event.id,
            assertion_id=assertion.assertion_id,
        ) == assertion
        recovered_ingress = list(
            session.iter_session_kind(
                "w",
                "s",
                "operator.ingress.ingress_occurred",
                through=assertion.completeness_boundary,
            )
        )
        basis = SupportBasis.from_json_dict(event.payload["consumed_support"])
        assert basis.support_count == event.payload["consumed_count"]
        assert [item.id for item in recovered_ingress] == list(
            SupportRecovery(session).recover(basis)
        )


def test_repeated_exact_result_has_one_assertion_identity_and_two_productions(
    session, occurrences, recorded_finding
):
    pair = AdjacentPair("it", "is")
    findings = measure_adjacent_pair(
        occurrences,
        pair,
        counting_scope="this session",
        premise_event_id=recorded_finding.id,
    )
    boundary = session.capture_boundary()
    first = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pair,
        findings=findings,
        completeness_boundary=boundary,
    )["following"]
    second = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pair,
        findings=findings,
        completeness_boundary=boundary,
    )["following"]

    first_assertion = assertion_of_recorded_adjacent_pair_result(first)
    second_assertion = assertion_of_recorded_adjacent_pair_result(second)
    assert first_assertion.assertion_id == second_assertion.assertion_id
    assert first_assertion.producing_event_id != second_assertion.producing_event_id


def test_result_assertion_identity_includes_exact_scope(
    session, occurrences, recorded_finding
):
    pair = AdjacentPair("it", "is")
    boundary = session.capture_boundary()

    def recorded_identity(counting_scope):
        event = record_pair_measurements(
            session,
            workspace_id="w",
            session_id="s",
            pair=pair,
            findings=measure_adjacent_pair(
                occurrences,
                pair,
                counting_scope=counting_scope,
                premise_event_id=recorded_finding.id,
            ),
            completeness_boundary=boundary,
        )["following"]
        return assertion_of_recorded_adjacent_pair_result(event).assertion_id

    assert recorded_identity("scope one") != recorded_identity("scope two")


def test_result_recovery_refuses_identity_that_does_not_match_content(
    session, occurrences, recorded_finding
):
    pair = AdjacentPair("it", "is")
    event = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pair,
        findings=measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        ),
        completeness_boundary=session.capture_boundary(),
    )["following"].model_copy(deep=True)
    event.payload["dimensions"]["content"]["positions_measured"] += 1

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="incoherent positional result coordinates",
    ):
        assertion_of_recorded_adjacent_pair_result(event)


def test_ledger_recovery_refuses_a_boundary_not_owned_by_the_ledger(
    session, occurrences, recorded_finding
):
    event = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=AdjacentPair("it", "is"),
        findings=measure_adjacent_pair(
            occurrences,
            AdjacentPair("it", "is"),
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        ),
        completeness_boundary=session.capture_boundary(),
    )["following"]
    assertion = assertion_of_recorded_adjacent_pair_result(event)
    # Forged consistently in both places. A boundary the ledger never issued
    # must still be refused when nothing internally disagrees about it.
    event.payload["completeness_boundary"]["commitment"] = "not-a-ledger-prefix"
    event.payload["consumed_support"]["boundary"]["commitment"] = "not-a-ledger-prefix"
    event.payload["support_basis"]["basis"]["boundary"]["commitment"] = "not-a-ledger-prefix"

    with pytest.raises(InvalidLedgerBoundary):
        get_recorded_adjacent_pair_result_assertion(
            session,
            producing_event_id=event.id,
            assertion_id=assertion.assertion_id,
        )


def test_ledger_recovery_refuses_an_incomplete_claimed_ingress_read(
    session, occurrences, recorded_finding
):
    event = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=AdjacentPair("it", "is"),
        findings=measure_adjacent_pair(
            occurrences,
            AdjacentPair("it", "is"),
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        ),
        completeness_boundary=session.capture_boundary(),
    )["following"]
    assertion = assertion_of_recorded_adjacent_pair_result(event)

    # The occurrence no longer carries a list that could be shortened, so the
    # tamper surface is the basis. Every part of it must refuse, and each fails
    # for its own reason rather than one check covering the others.
    intact = json.loads(json.dumps(event.payload["consumed_support"]))

    def tampered(**changes):
        basis = json.loads(json.dumps(intact))
        basis.update(changes)
        event.payload["consumed_support"] = basis
        event.payload["support_basis"]["basis"] = basis
        return basis

    tampered(support_count=intact["support_count"] - 1)
    with pytest.raises(PreservedMaterialMeasurementError, match="support count"):
        get_recorded_adjacent_pair_result_assertion(
            session, producing_event_id=event.id, assertion_id=assertion.assertion_id
        )

    tampered(commitment="0" * 64)
    with pytest.raises(PreservedMaterialMeasurementError, match="committed digest"):
        get_recorded_adjacent_pair_result_assertion(
            session, producing_event_id=event.id, assertion_id=assertion.assertion_id
        )

    tampered(selection_rule="a selection nobody established")
    with pytest.raises(PreservedMaterialMeasurementError, match="recoverable support basis"):
        get_recorded_adjacent_pair_result_assertion(
            session, producing_event_id=event.id, assertion_id=assertion.assertion_id
        )

    scope = dict(intact["scope"], session_id="another")
    tampered(scope=scope)
    with pytest.raises(PreservedMaterialMeasurementError, match="outside its own scope"):
        get_recorded_adjacent_pair_result_assertion(
            session, producing_event_id=event.id, assertion_id=assertion.assertion_id
        )

    event.payload["consumed_support"] = intact
    event.payload["support_basis"]["basis"] = intact
    assert get_recorded_adjacent_pair_result_assertion(
        session, producing_event_id=event.id, assertion_id=assertion.assertion_id
    ) == assertion


def test_recovery_refuses_a_claimed_form_with_other_position_coordinates(
    session, occurrences, recorded_finding
):
    event = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=AdjacentPair("it", "is"),
        findings=measure_adjacent_pair(
            occurrences,
            AdjacentPair("it", "is"),
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        ),
        completeness_boundary=session.capture_boundary(),
    )["following"].model_copy(deep=True)
    malformed_position = {
        "anchored_on": "left",
        "direction": "before",
        "displacement": 17,
    }
    event.payload["measured_position"] = malformed_position
    event.payload["assertion_subject"]["measured_position"] = malformed_position

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="incoherent positional result coordinates",
    ):
        assertion_of_recorded_adjacent_pair_result(event)


# --------------------------------------------------------------------------
# What agreement between pairs is, and is not.
# --------------------------------------------------------------------------


def test_agreement_is_counted_not_scored(occurrences, recorded_finding):
    scopes = [occurrences[:3], occurrences[3:]]
    occupant, agreeing, answered = occupant_agreement_across_scopes(
        scopes,
        AdjacentPair("it", "is"),
        "before_same_right",
        counting_scope="a bounded scope",
        premise_event_id=recorded_finding.id,
    )
    assert agreeing <= answered <= len(scopes)
    assert occupant is None or isinstance(occupant, str)


def test_group_by_highest_count_occupant_groups_without_claiming_a_kind(
    occurrences, recorded_finding
):
    measurements = {
        str(pair): measure_adjacent_pair(
            occurrences,
            pair,
            counting_scope="this session",
            premise_event_id=recorded_finding.id,
        )
        for pair in (AdjacentPair("it", "is"), AdjacentPair("it", "may"))
    }
    grouped = group_by_highest_count_occupant(measurements, "before_same_right")
    assert all(isinstance(labels, list) for labels in grouped.values())
    # Grouping is agreement between counts. No relation, kind, or standing.
    assert not any("kind" in key or "relation" in key for key in grouped)


def test_a_pair_must_be_two_exact_representations():
    for bad in (("", "is"), ("it", ""), (None, "is")):
        with pytest.raises(PreservedMaterialMeasurementError):
            AdjacentPair(*bad)


# --------------------------------------------------------------------------
# Rung 0: the material offers the representations, and nobody names one.
# --------------------------------------------------------------------------


def test_representations_are_enumerated_from_the_material(occurrences):
    """No representation is supplied, preferred, or filtered by count."""
    representations = enumerate_representations(occurrences)
    offered = {
        token
        for event in occurrences
        for token in event.payload["decoded_text"].split()
    }
    assert set(representations) == offered
    assert representations == sorted(representations)


def test_comparability_restricts_representations_without_judging_them(occurrences):
    """`present_in` keeps what every scope can answer, not what looks useful."""
    scopes = [occurrences[:2], occurrences[2:]]
    restricted = enumerate_representations(occurrences, present_in=scopes)
    everywhere = set.intersection(
        *[
            {t for e in scope for t in e.payload["decoded_text"].split()}
            for scope in scopes
        ]
    )
    assert set(restricted) == everywhere
    assert set(restricted) <= set(enumerate_representations(occurrences))


def test_measuring_after_an_representation_records_which(occurrences):
    finding = measure_after(occurrences, "it", counting_scope="this session")
    assert finding.declared.measured_after == "it"
    assert finding.highest_count_occupancy.representation == "is"


def test_the_whole_chain_runs_without_a_supplied_representation(
    session, occurrences
):
    """Rung 0 to rung 2 with no representation named by this test.

    The only inputs are the preserved occurrences and the fixed battery. Every
    representation appearing anywhere below came out of the material.
    """
    scopes = [occurrences[:3], occurrences[3:]]
    representations = enumerate_representations(occurrences, present_in=scopes)
    assert representations

    agreed = []
    for representation in representations:
        answers = [
            finding.highest_count_occupancy.representation
            for scope in scopes
            if (finding := measure_after(scope, representation, counting_scope="a scope"))
            and finding.highest_count_occupancy is not None
        ]
        if answers and len(set(answers)) == 1 and len(answers) == len(scopes):
            agreed.append(representation)
    assert agreed, "the material offered no representation with an agreeing occupant"

    recorded_first = record_measurement_finding(
        session,
        workspace_id="w",
        session_id="s",
        finding=measure_after(
            occurrences, agreed[0], counting_scope="whole session"
        ),
    )
    pairs = adjacent_pairs_from_finding(session, recorded_first.id)
    assert pairs

    recorded_second = record_pair_measurements(
        session,
        workspace_id="w",
        session_id="s",
        pair=pairs[0],
        findings=measure_adjacent_pair(
            occurrences,
            pairs[0],
            counting_scope="whole session",
            premise_event_id=recorded_first.id,
        ),
        completeness_boundary=session.capture_boundary(),
    )
    for event in recorded_second.values():
        assert premise_chain(session, event.id) == [recorded_first.id]


def test_agreement_is_the_discriminator_not_a_count(occurrences):
    """A frequent occupant that disagrees across scopes is not preferred."""
    scopes = [occurrences[:3], occurrences[3:]]
    disagreeing = []
    for representation in enumerate_representations(occurrences, present_in=scopes):
        answers = [
            f.highest_count_occupancy.representation
            for scope in scopes
            if (f := measure_after(scope, representation, counting_scope="a scope"))
            and f.highest_count_occupancy is not None
        ]
        if len(answers) == len(scopes) and len(set(answers)) > 1:
            disagreeing.append(representation)
    # Nothing here promotes a disagreeing representation; it is simply not agreed.
    for representation in disagreeing:
        whole = measure_after(occurrences, representation, counting_scope="whole")
        assert whole.highest_count_occupancy is not None


# --------------------------------------------------------------------------
# Displacement is a coordinate of the measurement, not a constant of the code.
# --------------------------------------------------------------------------


def test_displacements_are_enumerated_from_the_material(occurrences):
    """What the material reaches, not what anyone thought worth measuring."""
    reachable = enumerate_displacements(occurrences, "it")
    assert reachable
    assert reachable == sorted(reachable)
    assert min(reachable) == 1
    longest = max(
        len(e.payload["decoded_text"].split())
        for e in occurrences
        if "it" in e.payload["decoded_text"].split()
    )
    assert max(reachable) < longest


def test_a_displacement_absent_from_the_material_is_simply_absent(session):
    """Absent because nothing reaches it, not because it was judged dull."""
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("alpha beta\nexit\n"),
        output_stream=StringIO(),
    )
    occurrences = preserved_ingress_occurrences(
        ledger, workspace_id="w", session_id="s"
    )
    assert enumerate_displacements(occurrences, "alpha") == [1]


def test_each_displacement_is_recorded_on_its_own_finding(occurrences):
    for displacement in (1, 2):
        finding = measure_at_displacement(
            occurrences, "it", displacement=displacement, counting_scope=SCOPE
        )
        assert finding.declared.measured_position["displacement"] == displacement
        assert finding.declared.measured_position["direction"] == "after"


def test_no_displacement_is_preferred(occurrences):
    """The family treats every displacement the same way."""
    findings = [
        measure_at_displacement(
            occurrences, "it", displacement=d, counting_scope=SCOPE
        )
        for d in enumerate_displacements(occurrences, "it")
    ]
    assert len({type(f) for f in findings}) == 1
    for finding in findings:
        assert finding.declared.equivalence_rule == EQUIVALENCE_RULE
        assert finding.declared.counting_scope == SCOPE


def test_measuring_before_is_the_same_family(occurrences):
    after = measure_at_displacement(
        occurrences, "is", displacement=1, direction="after", counting_scope=SCOPE
    )
    before = measure_at_displacement(
        occurrences, "is", displacement=1, direction="before", counting_scope=SCOPE
    )
    assert after.declared.measured_position["direction"] == "after"
    assert before.declared.measured_position["direction"] == "before"


def test_measure_after_is_one_displacement_of_the_family(occurrences):
    """Kept for the continuation, carrying no privilege."""
    assert (
        measure_after(occurrences, "it", counting_scope=SCOPE).to_json_dict()
        == measure_at_displacement(
            occurrences, "it", displacement=1, direction="after", counting_scope=SCOPE
        ).to_json_dict()
    )


def test_a_displacement_below_one_is_refused(occurrences):
    for bad in (0, -1):
        with pytest.raises(PreservedMaterialMeasurementError):
            measure_at_displacement(
                occurrences, "it", displacement=bad, counting_scope=SCOPE
            )


def test_a_direction_outside_the_two_is_refused(occurrences):
    with pytest.raises(PreservedMaterialMeasurementError):
        enumerate_displacements(occurrences, "it", direction="sideways")


def test_answering_contexts_measure_what_every_context_would_have():
    """Visiting only the occurrences that can answer must change no finding.

    Every form is keyed, and a measurement already skips a `None` occupant, so
    an occurrence carrying none of the keys contributes nothing. This holds
    that equivalence over material chosen to exercise the ways it could break:
    a pair in no occurrence, a pair in several, a representation that is left
    of many rights, and one that is right of many lefts.
    """

    lines = [
        "the cat jumped the fence",
        "the cat sat",
        "a cat jumped over",
        "the dog jumped the gate",
        "nothing relevant here at all",
        "the cat jumped the fence",
    ]
    events = [
        Event(
            id=f"evt_{index:03d}",
            kind=INGRESS_OCCURRED_KIND,
            workspace_id="w",
            session_id="s",
            payload={"decoded_text": text},
        )
        for index, text in enumerate(lines)
    ]
    index = AdjacentPairMeasurementIndex(events)

    pairs = [AdjacentPair(left="the", right="cat"), AdjacentPair(left="cat", right="jumped"),
             AdjacentPair(left="jumped", right="the"), AdjacentPair(left="the", right="fence"),
             AdjacentPair(left="a", right="cat"), AdjacentPair(left="the", right="dog"),
             AdjacentPair(left="absent", right="entirely"),
             AdjacentPair(left="the", right="absent")]

    for pair in pairs:
        findings = index.measure(pair, counting_scope="s", premise_event_id="evt_000")
        for form, finding in findings.items():
            counts: dict[str, int] = {}
            measured = 0
            for context in index._contexts:
                occupant = index._occupant(context, pair, form)
                if occupant is None:
                    continue
                measured += 1
                counts[occupant] = counts.get(occupant, 0) + 1
            expected = tuple(
                Occupancy(representation=representation, occurrence_count=count)
                for representation, count in sorted(
                    counts.items(), key=lambda item: (-item[1], item[0])
                )
            )
            assert finding.positions_measured == measured, (pair, form)
            assert finding.occupancies == expected, (pair, form)
            assert finding.consumed_event_ids == tuple(event.id for event in events)


def test_an_unknown_form_is_refused_before_any_occurrence_is_visited():
    events = [
        Event(id="evt_1", kind=INGRESS_OCCURRED_KIND, workspace_id="w",
              session_id="s", payload={"decoded_text": "the cat"}),
    ]
    index = AdjacentPairMeasurementIndex(events)
    with pytest.raises(PreservedMaterialMeasurementError, match="unknown adjacent-pair form"):
        index._answering_contexts(AdjacentPair(left="the", right="cat"), "invented")


def test_a_support_binding_is_formed_over_its_population_not_paired_with_one():
    """Putting a basis beside a population does not bind it to that population.

    An earlier revision was a dataclass holding an identities tuple and a
    `SupportBasis` side by side, with prose saying the second was bound to the
    first and nothing enforcing it. A basis carrying a forged commitment and
    count could be placed beside an honest population and would be carried onto
    every Assertion the layer recorded.

    The binding now forms the basis itself, so that state is not constructable
    rather than merely refused.
    """

    import inspect

    from seed_runtime.adjacent_pair_measurement import (
        _DeclaredSupportBinding, _support_for,
    )
    from seed_runtime.preserved_material_measurement import INGRESS_OCCURRED_KIND
    from seed_runtime.support_basis import declare_complete_population

    def bodied(prefix):
        ledger = EventLedger()
        events = [
            Event(id=f"{prefix}_{index}", kind=INGRESS_OCCURRED_KIND, workspace_id="w",
                  session_id="s", payload={"decoded_text": "the cat jumped"})
            for index in range(3)
        ]
        ledger.append_many(events)
        index = AdjacentPairMeasurementIndex(events)
        finding = index.measure(
            AdjacentPair(left="the", right="cat"),
            counting_scope="s", premise_event_id=f"{prefix}_0",
        )["following"]
        return ledger, index, finding

    ledger, index, finding = bodied("evt")
    boundary = ledger.capture_boundary()

    # A basis cannot be supplied at all: the binding forms it.
    assert "basis" not in inspect.signature(_DeclaredSupportBinding.__init__).parameters

    binding = _DeclaredSupportBinding(
        workspace_id="w", session_id="s", occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=boundary, identities=index.event_ids,
    )
    assert finding.consumed_event_ids is index.event_ids
    assert binding.basis == declare_complete_population(
        workspace_id="w", session_id="s", occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=boundary, identities=index.event_ids,
    )

    supplied = _support_for(
        workspace_id="w", session_id="s", completeness_boundary=boundary,
        finding=finding, declared_support=binding,
    )
    assert supplied == binding.basis
    # Declaring afresh yields the same basis, which is why reuse is lawful.
    assert _support_for(
        workspace_id="w", session_id="s", completeness_boundary=boundary,
        finding=finding, declared_support=None,
    ) == binding.basis

    # A different population of the same size is refused. Under a count check
    # this passed and carried a basis describing material never consumed.
    _, _, other_finding = bodied("other")
    assert len(other_finding.consumed_event_ids) == len(finding.consumed_event_ids)
    assert other_finding.consumed_event_ids != finding.consumed_event_ids
    with pytest.raises(PreservedMaterialMeasurementError, match="population object"):
        _support_for(
            workspace_id="w", session_id="s", completeness_boundary=boundary,
            finding=other_finding, declared_support=binding,
        )

    # An equal copy may well be the same population; the fast path simply has
    # not established that, so it is refused rather than assumed. Built from a
    # list because `tuple(t)` returns `t` itself for a tuple.
    rebuilt = tuple(list(index.event_ids))
    assert rebuilt == index.event_ids and rebuilt is not index.event_ids
    equal_binding = _DeclaredSupportBinding(
        workspace_id="w", session_id="s", occurrence_kind=INGRESS_OCCURRED_KIND,
        boundary=boundary, identities=rebuilt,
    )
    # Its basis is identical, because it is the same population.
    assert equal_binding.basis == binding.basis
    with pytest.raises(PreservedMaterialMeasurementError, match="population object"):
        _support_for(
            workspace_id="w", session_id="s", completeness_boundary=boundary,
            finding=finding, declared_support=equal_binding,
        )

    # And the scope is still checked once the population object matches.
    for changes in ({"session_id": "another"}, {"workspace_id": "another"}):
        elsewhere = _DeclaredSupportBinding(
            workspace_id=changes.get("workspace_id", "w"),
            session_id=changes.get("session_id", "s"),
            occurrence_kind=INGRESS_OCCURRED_KIND,
            boundary=boundary, identities=index.event_ids,
        )
        with pytest.raises(PreservedMaterialMeasurementError, match="scope"):
            _support_for(
                workspace_id="w", session_id="s", completeness_boundary=boundary,
                finding=finding, declared_support=elsewhere,
            )
