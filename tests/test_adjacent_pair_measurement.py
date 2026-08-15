"""Exact adjacent-pair acquisition and occurrence-bound observations."""

from __future__ import annotations

import json
from dataclasses import replace
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger, InvalidLedgerBoundary, SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.adjacent_pair_measurement import (
    EQUIVALENCE_RULE,
    enumerate_displacements,
    enumerate_representations,
    measure_after,
    measure_at_displacement,
    AdjacentPair,
    adjacent_pairs_from_finding,
    observe_adjacent_pair_observations_from_finding,
    observe_emitted_representation_adjacency,
    compare_emitted_representation_adjacency,
    record_emitted_representation_adjacency,
    record_adjacent_pair_observation_compare,
    get_recorded_adjacent_pair_observation_compare,
    compare_adjacent_pair_observations,
    record_adjacent_pair_observations,
    get_recorded_adjacent_pair_observations,
    ADJACENT_PAIR_OBSERVATION_ACT_EVIDENCE_KIND,
    ADJACENT_PAIR_OBSERVATION_LOCALITY_EVIDENCE_KIND,
    ADJACENT_PAIR_OBSERVATION_CONVENTION,
    ADJACENT_PAIR_OBSERVATION_RECORDED_KIND,
)
from seed_runtime.preserved_material_measurement import (
    INGEST_OCCURRED_KIND,
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    Occupancy,
    PreservedMaterialMeasurementError,
    measure_occupancy,
    premise_chain,
    ingest_occurrences,
    record_measurement_finding,
)
from tests.material_fixture_console import run_material_fixture_console
from seed_runtime.operator_representation import (
    emit_operator_representation,
    record_operator_representation,
)
from seed_runtime.operator_locality_standing import read_operator_locality_standing
from tests.bounded_alternative_fixture import BOUNDED_ALTERNATIVE_FIXTURE_SOURCES
from seed_runtime.yield_evidence import yield_commitment
from seed_runtime.system_material import preserve_system_material

SCOPE = "whole locality"
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
def locality():
    ledger = EventLedger()
    run_material_fixture_console(
        ledger=ledger,
        locality_id="s",
        input_stream=binary_input(MATERIAL + ""),
        output_stream=StringIO(),
    )
    return ledger


@pytest.fixture
def occurrences(locality):
    return ingest_occurrences(locality, locality_id="s")


@pytest.fixture
def recorded_finding(locality, occurrences):
    finding = measure_after(
        occurrences,
        LEFT,
        counting_scope="preserved ingest occurrences of this locality",
    )
    return record_measurement_finding(
        locality, locality_id="s", finding=finding
    )


# --------------------------------------------------------------------------
# The representation comes out of the record.
# --------------------------------------------------------------------------


def test_a_finding_records_the_representation_it_measured_after(recorded_finding):
    """Without this a finding cannot supply an representation to anything."""
    assert recorded_finding.payload["measured_left_representation"] == LEFT


def test_pairs_are_read_from_the_record_not_supplied(locality, recorded_finding):
    pairs = adjacent_pairs_from_finding(locality, recorded_finding.id)
    assert pairs
    assert all(pair.left == LEFT for pair in pairs)
    assert AdjacentPair(left="it", right="is") in pairs


def test_every_occupancy_becomes_a_pair_with_no_filtering(locality, recorded_finding):
    """No count, share, or threshold decides which pairs are returned."""
    pairs = adjacent_pairs_from_finding(locality, recorded_finding.id)
    assert len(pairs) == len(recorded_finding.payload["occupancies"])


def test_a_finding_that_names_no_representation_cannot_supply_one(locality, occurrences):
    event = record_measurement_finding(
        locality,
        locality_id="s",
        finding=measure_occupancy(
            occurrences,
            declared=DeclaredMeasurement(
                representation_measured="the first representation",
                equivalence_rule=EQUIVALENCE_RULE,
                counting_scope="this locality",
            ),
            occupant_of=lambda t: (t.split() or [None])[0],
        ),
    )
    with pytest.raises(PreservedMaterialMeasurementError):
        adjacent_pairs_from_finding(locality, event.id)


def test_pairs_must_come_from_a_measurement_finding(locality, occurrences):
    foreign = locality.append("unrelated.kind", {"occupancies": []}, locality_id="s")
    with pytest.raises(PreservedMaterialMeasurementError):
        adjacent_pairs_from_finding(locality, foreign.id)



# --------------------------------------------------------------------------
# Exact pair occurrences are extended one position on each side.
# --------------------------------------------------------------------------


def _observation_road(lines: tuple[str, ...], measured_lefts: tuple[str, ...]):
    ledger = EventLedger()
    for line in lines:
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_id="adjacent-observation",
        )
    material = ingest_occurrences(
        ledger, locality_id="adjacent-observation"
    )
    observations = []
    for measured_left in measured_lefts:
        finding = record_measurement_finding(
            ledger,
            locality_id="adjacent-observation",
            finding=measure_after(
                material,
                measured_left,
                counting_scope="exact bounded observation fixture",
            ),
        )
        observations.extend(
            observe_adjacent_pair_observations_from_finding(
                ledger,
                finding_event_id=finding.id,
                occurrences=material,
            )
        )
    return ledger, tuple(observations)


def test_every_exact_pair_occurrence_preserves_its_adjacent_pair_observation_and_evidence():
    ledger, observations = _observation_road(
        ("L a b R a b Z",),
        ("a",),
    )

    assert len(observations) == 2
    assert [observation.exact_order for observation in observations] == [
        (0, 1, 2, 3),
        (3, 4, 5, 6),
    ]
    for observation in observations:
        source = ledger.get(observation.source_occurrence_id)
        pair_finding = ledger.get(observation.evidence["adjacency_evidence_event_id"])
        assert pair_finding.kind == MEASUREMENT_RECORDED_KIND
        assert observation.evidence == {
            "source_occurrence_id": source.id,
            "adjacency_evidence_event_id": pair_finding.id,
            "evidence_occurrence_ids": [
                pair_finding.id,
                source.id,
            ],
            "source_kind": INGEST_OCCURRED_KIND,
            "locality_id": "adjacent-observation",
            "exact_representation": source.payload["represented_material"],
        }
        assert observation.pair_occurrence.right.position == (
            observation.pair_occurrence.left.position + 1
        )
        assert observation.fully_bounded_coordinates["identity"] == {
            "adjacency_evidence_event_id": pair_finding.id,
            "source_occurrence_id": source.id,
            "positions": list(observation.exact_order),
        }


def test_adjacent_pair_observation_refuses_a_different_or_rewritten_source_occurrence():
    ledger = EventLedger()
    for line in ("L a b R", "X a b Y"):
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_id="adjacent-observation",
        )
    material = ingest_occurrences(
        ledger, locality_id="adjacent-observation"
    )
    finding = record_measurement_finding(
        ledger,
        locality_id="adjacent-observation",
        finding=measure_after(material, "a", counting_scope="exact fixture"),
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="differ from the finding's exact Evidence",
    ):
        observe_adjacent_pair_observations_from_finding(
            ledger,
            finding_event_id=finding.id,
            occurrences=reversed(material),
        )

    rewritten = material[0].model_copy(deep=True)
    rewritten.payload["represented_material"] = "L a b different"
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="source-occurrence Evidence does not read",
    ):
        observe_adjacent_pair_observations_from_finding(
            ledger,
            finding_event_id=finding.id,
            occurrences=(rewritten, material[1]),
        )

    relocated = material[0].model_copy(
        deep=True,
        update={"locality_id": "other"},
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="source-occurrence Evidence does not read",
    ):
        observe_adjacent_pair_observations_from_finding(
            ledger,
            finding_event_id=finding.id,
            occurrences=(relocated, material[1]),
        )


def test_system_bytes_do_not_become_represented_material():
    import seed_runtime.adjacent_pair_measurement as module

    system_material = preserve_system_material(
        EventLedger(),
        locality_id="adjacent-observation",
        exact_bytes=b"L a b R",
        observed_boundary="system boundary",
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="carries no represented material",
    ):
        module._observe_adjacent_pair_observations(
            (system_material,),
            (AdjacentPair("a", "b"),),
            adjacency_evidence_event_id="evidence_not_consulted",
        )


def test_direct_observation_input_cannot_rewrite_order_adjacency_or_evidence():
    _, observations = _observation_road(("L a b R",), ("a",))
    observation = observations[0]

    mutations = (
        lambda item: replace(item, exact_order=(0, 2, 1, 3)),
        lambda item: replace(
            item,
            left_occurrence=replace(item.left_occurrence, position=7),
        ),
        lambda item: replace(
            item,
            evidence={**item.evidence, "source_occurrence_id": "another"},
        ),
        lambda item: replace(
            item,
            evidence={**item.evidence, "exact_representation": "L a different R"},
        ),
    )
    for mutate in mutations:
        with pytest.raises(PreservedMaterialMeasurementError):
            mutate(observation)


def test_compare_refuses_duplicate_or_non_observation_inputs():
    _, observations = _observation_road(("L a b R",), ("a",))
    observation = observations[0]

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="same exact adjacent-pair observation",
    ):
        compare_adjacent_pair_observations((observation, observation))
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="exact bounded observations",
    ):
        compare_adjacent_pair_observations((observation, {"looks": "similar"}))


def test_boundary_absence_is_preserved_without_filling_positions():
    _, observations = _observation_road(
        ("a b R", "L a b", "a b"),
        ("a",),
    )

    assert [
        (
            observation.left_occurrence is not None,
            observation.right_occurrence is not None,
            observation.fully_bounded_coordinates is not None,
        )
        for observation in observations
    ] == [
        (False, True, False),
        (True, False, False),
        (False, False, False),
    ]


def test_identical_representations_do_not_identify_occurrences():
    _, observations = _observation_road(
        ("L a b R", "L a b R"),
        ("a",),
    )

    first, second = (
        observation.fully_bounded_coordinates for observation in observations
    )
    assert first["left_occurrence"]["representation"] == second["left_occurrence"][
        "representation"
    ]
    assert first["pair_occurrence"]["ordered_pair"] == second["pair_occurrence"][
        "ordered_pair"
    ]
    assert first["right_occurrence"]["representation"] == second["right_occurrence"][
        "representation"
    ]
    assert first["identity"] != second["identity"]


def test_compare_reports_only_adjacency_coordinates_that_survive_counterexamples():
    _, observations = _observation_road(
        (
            "L a b R",
            "L a b R",
            "X a b Y",
            "L c d R",
        ),
        ("a", "c"),
    )

    compared = compare_adjacent_pair_observations(observations)
    assert compared == {
        "observation_count": 4,
        "fully_bounded_observation_count": 4,
        "boundary_observation_count": 0,
        "distinct_fully_bounded_occurrences": 4,
        "distinct_representation_triples": 3,
        "counterexamples": {
            "representation_triple_groups_with_multiple_occurrences": 1,
            "ordered_pair_groups_with_multiple_endpoint_representations": 1,
            "endpoint_groups_with_multiple_ordered_pairs": 1,
        },
        "distinct_adjacency_coordinates": [
            {
                "left_present": True,
                "right_present": True,
                "ordered_displacements": [1, 1, 1],
            }
        ],
    }


def test_adjacent_pair_observation_measurement_records_exact_coordinates_and_reads_result():
    ledger = EventLedger()
    for line in ("L a b R", "X a b Y"):
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_id="adjacent-observation",
        )
    material = ingest_occurrences(
        ledger, locality_id="adjacent-observation"
    )
    finding = record_measurement_finding(
        ledger,
        locality_id="adjacent-observation",
        finding=measure_after(material, "a", counting_scope="exact fixture"),
    )

    recorded = record_adjacent_pair_observations(
        ledger,
        locality_id="adjacent-observation",
        finding_event_id=finding.id,
    )
    read = get_recorded_adjacent_pair_observations(
        ledger, recorded.id
    )

    assert recorded.kind == ADJACENT_PAIR_OBSERVATION_RECORDED_KIND
    assert read == observe_adjacent_pair_observations_from_finding(
        ledger,
        finding_event_id=finding.id,
        occurrences=material,
    )
    assert len(read) == 2
    act_evidence = ledger.get(recorded.payload["responsible_act_evidence_id"])
    yield_evidence = ledger.get(recorded.payload["yield_evidence_id"])
    locality_evidence = ledger.get(recorded.payload["locality_evidence_id"])
    assert act_evidence.kind == ADJACENT_PAIR_OBSERVATION_ACT_EVIDENCE_KIND
    assert locality_evidence.kind == ADJACENT_PAIR_OBSERVATION_LOCALITY_EVIDENCE_KIND
    assert (
        recorded.payload["act_occurrence_id"]
        == act_evidence.payload["act_occurrence_id"]
        == yield_evidence.payload["dimensions"]["act_occurrence_id"]
        == locality_evidence.payload["act_occurrence_id"]
    )
    assert act_evidence.payload["input_applicability"] == [
        {
            "input_reference": finding.id,
            "role": "read ordered-pair finding",
            "standing": "applicable",
        },
        *[
            {
                "input_reference": event.id,
                "role": "exact preserved source occurrence",
                "standing": "applicable",
            }
            for event in material
        ],
    ]
    assert recorded.payload["participation"] == act_evidence.payload["participation"]
    assert recorded.payload["participation"] == [
        {
            "subject_reference": finding.id,
            "role": "read ordered-pair finding",
            "act_occurrence_id": recorded.payload["act_occurrence_id"],
        },
        *[
            {
                "subject_reference": event.id,
                "role": "exact preserved source occurrence",
                "act_occurrence_id": recorded.payload["act_occurrence_id"],
            }
            for event in material
        ],
    ]
    assert recorded.payload["dimensions"]["authority"] == "unestablished"
    assert recorded.payload["dimensions"]["evidence_scope"].endswith(
        "Standing beyond this result"
    )


def test_adjacent_pair_observation_read_does_not_repeat_measurement(monkeypatch):
    import seed_runtime.adjacent_pair_measurement as module

    ledger, observations = _observation_road(("L a b R",), ("a",))
    finding_id = observations[0].evidence["adjacency_evidence_event_id"]
    recorded = record_adjacent_pair_observations(
        ledger,
        locality_id="adjacent-observation",
        finding_event_id=finding_id,
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("historical address repeated Measurement")

    monkeypatch.setattr(module, "_observe_adjacent_pair_observations", forbidden)
    assert get_recorded_adjacent_pair_observations(ledger, recorded.id)


def test_adjacent_pair_observation_read_refuses_changed_result_or_input_evidence():
    ledger, observations = _observation_road(("L a b R",), ("a",))
    finding_id = observations[0].evidence["adjacency_evidence_event_id"]
    recorded = record_adjacent_pair_observations(
        ledger,
        locality_id="adjacent-observation",
        finding_event_id=finding_id,
    )

    different = recorded.model_copy(deep=True)
    different.payload["observations"][0]["exact_order"] = [0, 1, 3, 2]
    different = ledger.append(
        different.kind,
        different.payload,
        locality_id=different.locality_id,
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="edge Evidence concerns different coordinates",
    ):
        get_recorded_adjacent_pair_observations(ledger, different.id)

    act_evidence = ledger.get(recorded.payload["responsible_act_evidence_id"])
    altered_act_payload = json.loads(json.dumps(act_evidence.payload))
    altered_act_payload["input_applicability"][0]["standing"] = "Unknown"
    altered_act = ledger.append(
        ADJACENT_PAIR_OBSERVATION_ACT_EVIDENCE_KIND,
        altered_act_payload,
        locality_id="adjacent-observation",
    )
    altered_event_payload = json.loads(json.dumps(recorded.payload))
    altered_event_payload["responsible_act_evidence_id"] = altered_act.id
    altered_event = ledger.append(
        ADJACENT_PAIR_OBSERVATION_RECORDED_KIND,
        altered_event_payload,
        locality_id="adjacent-observation",
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="Act Evidence concerns different inputs",
    ):
        get_recorded_adjacent_pair_observations(
            ledger, altered_event.id
        )


def test_adjacent_pair_observation_endpoints_do_not_establish_participation():
    ledger, observations = _observation_road(("L a b R",), ("a",))
    recorded = record_adjacent_pair_observations(
        ledger,
        locality_id="adjacent-observation",
        finding_event_id=observations[0].evidence["adjacency_evidence_event_id"],
    )

    missing = recorded.model_copy(deep=True)
    missing.payload.pop("participation")
    missing = ledger.append(
        missing.kind,
        missing.payload,
        locality_id=missing.locality_id,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Participation"):
        get_recorded_adjacent_pair_observations(ledger, missing.id)

    wrong = recorded.model_copy(deep=True)
    wrong.payload["participation"][0]["act_occurrence_id"] = "other-occurrence"
    wrong = ledger.append(
        wrong.kind,
        wrong.payload,
        locality_id=wrong.locality_id,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Participation"):
        get_recorded_adjacent_pair_observations(ledger, wrong.id)


def test_adjacent_pair_observation_read_refuses_self_consistent_counterfeit_source_text():
    ledger, observations = _observation_road(("L a b R",), ("a",))
    finding_id = observations[0].evidence["adjacency_evidence_event_id"]
    recorded = record_adjacent_pair_observations(
        ledger,
        locality_id="adjacent-observation",
        finding_event_id=finding_id,
    )

    altered_result = {
        "adjacency_evidence_event_id": recorded.payload[
            "adjacency_evidence_event_id"
        ],
        "source_occurrence_ids": recorded.payload["source_occurrence_ids"],
        "observations": json.loads(json.dumps(recorded.payload["observations"])),
    }
    altered_result["observations"][0]["evidence"]["exact_representation"] = (
        "L a b counterfeit"
    )
    altered_result["observations"][0]["right_occurrence"]["representation"] = (
        "counterfeit"
    )
    commitment = yield_commitment(ADJACENT_PAIR_OBSERVATION_CONVENTION, altered_result)

    act_payload = json.loads(
        json.dumps(
            ledger.get(recorded.payload["responsible_act_evidence_id"]).payload
        )
    )
    act_payload["result_commitment"] = commitment
    act_evidence = ledger.append(
        ADJACENT_PAIR_OBSERVATION_ACT_EVIDENCE_KIND,
        act_payload,
        locality_id="adjacent-observation",
    )
    yield_payload = json.loads(
        json.dumps(ledger.get(recorded.payload["yield_evidence_id"]).payload)
    )
    yield_payload["yield_commitment"] = commitment
    yield_evidence = ledger.append(
        "operator.yield.evidence_recorded",
        yield_payload,
        locality_id="adjacent-observation",
    )
    locality_payload = json.loads(
        json.dumps(ledger.get(recorded.payload["locality_evidence_id"]).payload)
    )
    locality_payload["carried_content"] = altered_result
    locality_evidence = ledger.append(
        ADJACENT_PAIR_OBSERVATION_LOCALITY_EVIDENCE_KIND,
        locality_payload,
        locality_id="adjacent-observation",
    )
    event_payload = json.loads(json.dumps(recorded.payload))
    event_payload.update(altered_result)
    event_payload["responsible_act_evidence_id"] = act_evidence.id
    event_payload["yield_evidence_id"] = yield_evidence.id
    event_payload["locality_evidence_id"] = locality_evidence.id
    event = ledger.append(
        ADJACENT_PAIR_OBSERVATION_RECORDED_KIND,
        event_payload,
        locality_id="adjacent-observation",
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="different Evidence",
    ):
        get_recorded_adjacent_pair_observations(ledger, event.id)



def test_a_pair_must_be_two_exact_representations():
    for bad in (("", "is"), ("it", ""), (None, "is")):
        with pytest.raises(PreservedMaterialMeasurementError):
            AdjacentPair(*bad)


def test_emitted_representation_adjacency_requires_exact_locality():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_id="emission-observation",
        locality_standing=read_operator_locality_standing(
            ledger, locality_id="emission-observation"
        ),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    emitted = emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    emission = ledger.get(emitted["emitted_event_id"])

    observations = observe_emitted_representation_adjacency(
        ledger, emission_event_id=emission.id
    )
    assert observations
    assert all(item.source_occurrence_id == emission.id for item in observations)
    assert all(
        item.evidence["source_kind"] == "operator.representation.emitted"
        for item in observations
    )
    assert all(
        item.evidence["adjacency_evidence_event_id"]
        == emission.payload["locality_evidence_id"]
        for item in observations
    )
    recorded_observations = record_emitted_representation_adjacency(
        ledger,
        emission_event_id=emission.id,
    )
    assert get_recorded_adjacent_pair_observations(
        ledger, recorded_observations.id
    ) == observations
    assert recorded_observations.payload["adjacency_evidence_event_id"] == (
        emission.payload["locality_evidence_id"]
    )
    assert [
        item["subject_reference"] for item in recorded_observations.payload["participation"]
    ] == [emission.payload["locality_evidence_id"], emission.id]

    copied = emission.model_copy(deep=True)
    copied.payload["locality_evidence_id"] = None
    copied = ledger.append(
        copied.kind,
        copied.payload,
        locality_id=copied.locality_id,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        observe_emitted_representation_adjacency(
            ledger, emission_event_id=copied.id
        )

    repeated = emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    repeated_emission = ledger.get(repeated["emitted_event_id"])
    assert (
        repeated_emission.payload["emitted_representation"]
        == emission.payload["emitted_representation"]
    )
    repeated_observations = record_emitted_representation_adjacency(
        ledger,
        emission_event_id=repeated_emission.id,
    )
    recorded_compare = record_adjacent_pair_observation_compare(
        ledger,
        locality_id="emission-observation",
        observation_event_ids=(
            recorded_observations.id,
            repeated_observations.id,
        ),
    )
    read_compare = get_recorded_adjacent_pair_observation_compare(
        ledger,
        recorded_compare.id,
    )
    assert read_compare == compare_emitted_representation_adjacency(
        ledger,
        emission_event_ids=(emission.id, repeated_emission.id),
    )
    assert [
        item["subject_reference"] for item in recorded_compare.payload["participation"]
    ] == [recorded_observations.id, repeated_observations.id]
    wrong_occurrence = emission.model_copy(deep=True)
    wrong_occurrence.payload["locality_evidence_id"] = repeated_emission.payload[
        "locality_evidence_id"
    ]
    wrong_occurrence = ledger.append(
        wrong_occurrence.kind,
        wrong_occurrence.payload,
        locality_id=wrong_occurrence.locality_id,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        observe_emitted_representation_adjacency(
            ledger, emission_event_id=wrong_occurrence.id
        )

    compared = compare_emitted_representation_adjacency(
        ledger,
        emission_event_ids=(emission.id, repeated_emission.id),
    )
    assert compared["observation_count"] == 2 * len(observations)
    assert (
        compared["distinct_fully_bounded_occurrences"]
        == compared["fully_bounded_observation_count"]
    )
    assert (
        compared["counterexamples"][
            "representation_triple_groups_with_multiple_occurrences"
        ]
        > 0
    )


def test_emission_adjacency_compare_requires_distinct_real_occurrences():
    ledger = EventLedger()
    with pytest.raises(PreservedMaterialMeasurementError, match="at least two distinct"):
        compare_emitted_representation_adjacency(
            ledger,
            emission_event_ids=("same", "same"),
        )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="intact emission occurrence",
    ):
        compare_emitted_representation_adjacency(
            ledger,
            emission_event_ids=("missing-one", "missing-two"),
        )


def test_emission_adjacency_refuses_corrupted_locality_evidence(tmp_path):
    ledger = SQLiteEventLedger(tmp_path / "emission-adjacency.sqlite")
    representation = record_operator_representation(
        ledger,
        locality_id="s",
        locality_standing=read_operator_locality_standing(
            ledger, locality_id="s"
        ),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    emitted = emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    emission = ledger.get(emitted["emitted_event_id"])
    locality_id = emission.payload["locality_evidence_id"]
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET content_hash = ? WHERE id = ?",
        ("corrupted", locality_id),
    )
    ledger._connection.commit()

    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        observe_emitted_representation_adjacency(
            ledger,
            emission_event_id=emission.id,
        )
    ledger.close()


# --------------------------------------------------------------------------
# Rung 0: the material offers the representations, and nobody names one.
# --------------------------------------------------------------------------


def test_representations_are_enumerated_from_the_material(occurrences):
    """No representation is supplied, preferred, or filtered by count."""
    representations = enumerate_representations(occurrences)
    offered = {
        token
        for event in occurrences
        for token in event.payload["represented_material"].split()
    }
    assert set(representations) == offered
    assert representations == sorted(representations)


def test_comparability_restricts_representations_without_judging_them(occurrences):
    """`present_in` keeps what every scope can answer, not what looks useful."""
    scopes = [occurrences[:2], occurrences[2:]]
    restricted = enumerate_representations(occurrences, present_in=scopes)
    everywhere = set.intersection(
        *[
            {t for e in scope for t in e.payload["represented_material"].split()}
            for scope in scopes
        ]
    )
    assert set(restricted) == everywhere
    assert set(restricted) <= set(enumerate_representations(occurrences))


def test_measuring_after_a_representation_records_which(occurrences):
    finding = measure_after(occurrences, "it", counting_scope="this locality")
    assert finding.declared.measured_after == "it"
    assert finding.highest_count_occupancy.representation == "is"



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
        len(e.payload["represented_material"].split())
        for e in occurrences
        if "it" in e.payload["represented_material"].split()
    )
    assert max(reachable) < longest


def test_a_displacement_absent_from_the_material_is_simply_absent(locality):
    """Absent because nothing reaches it, not because it was judged dull."""
    ledger = EventLedger()
    run_material_fixture_console(
        ledger=ledger,
        locality_id="s",
        input_stream=binary_input("alpha beta\n"),
        output_stream=StringIO(),
    )
    occurrences = ingest_occurrences(
        ledger, locality_id="s"
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
