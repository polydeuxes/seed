"""Exact adjacency-pair acquisition and occurrence-bound measurements."""

from __future__ import annotations

import json
from dataclasses import replace
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger, InvalidLedgerBoundary, SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.adjacency_pair_measurement import (
    EQUIVALENCE_RULE,
    enumerate_displacements,
    enumerate_representations,
    measure_after,
    measure_at_displacement,
    AdjacencyPair,
    adjacency_pairs_from_finding,
    measure_adjacency_pairs_from_finding,
    measure_emitted_representation_adjacency,
    compare_emitted_representation_adjacency,
    record_emitted_representation_adjacency,
    record_adjacency_pair_measurement_compare,
    get_recorded_adjacency_pair_measurement_compare,
    compare_adjacency_pair_measurements,
    record_adjacency_pair_measurements,
    get_recorded_adjacency_pair_measurements,
    ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
    ADJACENCY_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND,
    ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND,
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
        locality_identity="s",
        input_stream=binary_input(MATERIAL + ""),
        output_stream=StringIO(),
    )
    return ledger


@pytest.fixture
def occurrences(locality):
    return ingest_occurrences(locality, locality_identity="s")


@pytest.fixture
def recorded_finding(locality, occurrences):
    finding = measure_after(
        occurrences,
        LEFT,
        counting_scope="preserved ingest occurrences of this locality",
    )
    return record_measurement_finding(
        locality, locality_identity="s", finding=finding
    )


# --------------------------------------------------------------------------
# The representation comes out of the record.
# --------------------------------------------------------------------------


def test_a_finding_records_the_representation_it_measured_after(recorded_finding):
    """Without this a finding cannot supply an representation to anything."""
    assert recorded_finding.payload["measured_left_representation"] == LEFT


def test_pairs_are_read_from_the_record_not_supplied(locality, recorded_finding):
    pairs = adjacency_pairs_from_finding(locality, recorded_finding.identity)
    assert pairs
    assert all(pair.left == LEFT for pair in pairs)
    assert AdjacencyPair(left="it", right="is") in pairs


def test_every_occupancy_becomes_a_pair_with_no_filtering(locality, recorded_finding):
    """No count or share decides which pairs are returned."""
    pairs = adjacency_pairs_from_finding(locality, recorded_finding.identity)
    assert len(pairs) == len(recorded_finding.payload["occupancies"])


def test_a_finding_that_names_no_representation_cannot_supply_one(locality, occurrences):
    event = record_measurement_finding(
        locality,
        locality_identity="s",
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
        adjacency_pairs_from_finding(locality, event.identity)


def test_pairs_must_come_from_a_measurement_finding(locality, occurrences):
    foreign = locality.append("unrelated.kind", {"occupancies": []}, locality_identity="s")
    with pytest.raises(PreservedMaterialMeasurementError):
        adjacency_pairs_from_finding(locality, foreign.identity)



# --------------------------------------------------------------------------
# Exact pair occurrences are extended one position on each side.
# --------------------------------------------------------------------------


def _measurement_road(lines: tuple[str, ...], measured_lefts: tuple[str, ...]):
    ledger = EventLedger()
    for line in lines:
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_identity="adjacent-measurement",
        )
    material = ingest_occurrences(
        ledger, locality_identity="adjacent-measurement"
    )
    measurements = []
    for measured_left in measured_lefts:
        finding = record_measurement_finding(
            ledger,
            locality_identity="adjacent-measurement",
            finding=measure_after(
                material,
                measured_left,
                counting_scope="exact bounded measurement fixture",
            ),
        )
        measurements.extend(
            measure_adjacency_pairs_from_finding(
                ledger,
                finding_event_identity=finding.identity,
                occurrences=material,
            )
        )
    return ledger, tuple(measurements)


def test_every_exact_pair_occurrence_preserves_its_adjacency_pair_measurement_and_evidence():
    ledger, measurements = _measurement_road(
        ("L a b R a b Z",),
        ("a",),
    )

    assert len(measurements) == 2
    assert [measurement.exact_order for measurement in measurements] == [
        (0, 1, 2, 3),
        (3, 4, 5, 6),
    ]
    for measurement in measurements:
        source = ledger.get(measurement.source_occurrence_identity)
        pair_finding = ledger.get(measurement.evidence["adjacency_evidence_event_identity"])
        assert pair_finding.kind == MEASUREMENT_RECORDED_KIND
        assert measurement.evidence == {
            "source_occurrence_identity": source.identity,
            "adjacency_evidence_event_identity": pair_finding.identity,
            "evidence_occurrence_identities": [
                pair_finding.identity,
                source.identity,
            ],
            "source_kind": INGEST_OCCURRED_KIND,
            "locality_identity": "adjacent-measurement",
            "exact_representation": source.payload["represented_material"],
        }
        assert measurement.pair_occurrence.right.position == (
            measurement.pair_occurrence.left.position + 1
        )
        assert measurement.fully_bounded_coordinates["identity"] == {
            "adjacency_evidence_event_identity": pair_finding.identity,
            "source_occurrence_identity": source.identity,
            "positions": list(measurement.exact_order),
        }


def test_adjacency_pair_measurement_refuses_a_different_or_rewritten_source_occurrence():
    ledger = EventLedger()
    for line in ("L a b R", "X a b Y"):
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_identity="adjacent-measurement",
        )
    material = ingest_occurrences(
        ledger, locality_identity="adjacent-measurement"
    )
    finding = record_measurement_finding(
        ledger,
        locality_identity="adjacent-measurement",
        finding=measure_after(material, "a", counting_scope="exact fixture"),
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="differ from the finding's exact Evidence",
    ):
        measure_adjacency_pairs_from_finding(
            ledger,
            finding_event_identity=finding.identity,
            occurrences=reversed(material),
        )

    rewritten = material[0].model_copy(deep=True)
    rewritten.payload["represented_material"] = "L a b different"
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="source-occurrence Evidence does not read",
    ):
        measure_adjacency_pairs_from_finding(
            ledger,
            finding_event_identity=finding.identity,
            occurrences=(rewritten, material[1]),
        )

    relocated = material[0].model_copy(
        deep=True,
        update={"locality_identity": "other"},
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="source-occurrence Evidence does not read",
    ):
        measure_adjacency_pairs_from_finding(
            ledger,
            finding_event_identity=finding.identity,
            occurrences=(relocated, material[1]),
        )


def test_system_bytes_do_not_become_represented_material():
    import seed_runtime.adjacency_pair_measurement as module

    system_material = preserve_system_material(
        EventLedger(),
        locality_identity="adjacent-measurement",
        exact_bytes=b"L a b R",
        observed_boundary="system boundary",
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="carries no represented material",
    ):
        module._measure_adjacency_pair_measurements(
            (system_material,),
            (AdjacencyPair("a", "b"),),
            adjacency_evidence_event_identity="evidence_not_consulted",
        )


def test_direct_measurement_input_cannot_rewrite_order_adjacency_or_evidence():
    _, measurements = _measurement_road(("L a b R",), ("a",))
    measurement = measurements[0]

    mutations = (
        lambda item: replace(item, exact_order=(0, 2, 1, 3)),
        lambda item: replace(
            item,
            left_occurrence=replace(item.left_occurrence, position=7),
        ),
        lambda item: replace(
            item,
            evidence={**item.evidence, "source_occurrence_identity": "another"},
        ),
        lambda item: replace(
            item,
            evidence={**item.evidence, "exact_representation": "L a different R"},
        ),
    )
    for mutate in mutations:
        with pytest.raises(PreservedMaterialMeasurementError):
            mutate(measurement)


def test_compare_refuses_duplicate_or_non_measurement_inputs():
    _, measurements = _measurement_road(("L a b R",), ("a",))
    measurement = measurements[0]

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="same exact adjacency-pair measurement",
    ):
        compare_adjacency_pair_measurements((measurement, measurement))
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="exact bounded measurements",
    ):
        compare_adjacency_pair_measurements((measurement, {"looks": "similar"}))


def test_boundary_absence_is_preserved_without_filling_positions():
    _, measurements = _measurement_road(
        ("a b R", "L a b", "a b"),
        ("a",),
    )

    assert [
        (
            measurement.left_occurrence is not None,
            measurement.right_occurrence is not None,
            measurement.fully_bounded_coordinates is not None,
        )
        for measurement in measurements
    ] == [
        (False, True, False),
        (True, False, False),
        (False, False, False),
    ]


def test_identical_representations_do_not_identify_occurrences():
    _, measurements = _measurement_road(
        ("L a b R", "L a b R"),
        ("a",),
    )

    first, second = (
        measurement.fully_bounded_coordinates for measurement in measurements
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
    _, measurements = _measurement_road(
        (
            "L a b R",
            "L a b R",
            "X a b Y",
            "L c d R",
        ),
        ("a", "c"),
    )

    compared = compare_adjacency_pair_measurements(measurements)
    assert compared == {
        "measurement_count": 4,
        "fully_bounded_measurement_count": 4,
        "boundary_measurement_count": 0,
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


def test_adjacency_pair_measurement_measurement_records_exact_coordinates_and_reads_result():
    ledger = EventLedger()
    for line in ("L a b R", "X a b Y"):
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_identity="adjacent-measurement",
        )
    material = ingest_occurrences(
        ledger, locality_identity="adjacent-measurement"
    )
    finding = record_measurement_finding(
        ledger,
        locality_identity="adjacent-measurement",
        finding=measure_after(material, "a", counting_scope="exact fixture"),
    )

    recorded = record_adjacency_pair_measurements(
        ledger,
        locality_identity="adjacent-measurement",
        finding_event_identity=finding.identity,
    )
    read = get_recorded_adjacency_pair_measurements(
        ledger, recorded.identity
    )

    assert recorded.kind == ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND
    assert read == measure_adjacency_pairs_from_finding(
        ledger,
        finding_event_identity=finding.identity,
        occurrences=material,
    )
    assert len(read) == 2
    act_evidence = ledger.get(recorded.payload["responsible_act_evidence_identity"])
    yield_evidence = ledger.get(recorded.payload["yield_evidence_identity"])
    locality_evidence = ledger.get(recorded.payload["locality_evidence_identity"])
    assert act_evidence.kind == ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND
    assert locality_evidence.kind == ADJACENCY_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND
    assert (
        recorded.payload["act_occurrence_identity"]
        == act_evidence.payload["act_occurrence_identity"]
        == yield_evidence.payload["dimensions"]["act_occurrence_identity"]
        == locality_evidence.payload["act_occurrence_identity"]
    )
    assert act_evidence.payload["input_applicability"] == [
        {
            "input_reference": finding.identity,
            "role": "read ordered-pair finding",
            "standing": "applicable",
        },
        *[
            {
                "input_reference": event.identity,
                "role": "exact preserved source occurrence",
                "standing": "applicable",
            }
            for event in material
        ],
    ]
    assert recorded.payload["participation"] == act_evidence.payload["participation"]
    assert recorded.payload["participation"] == [
        {
            "subject_reference": finding.identity,
            "role": "read ordered-pair finding",
            "act_occurrence_identity": recorded.payload["act_occurrence_identity"],
        },
        *[
            {
                "subject_reference": event.identity,
                "role": "exact preserved source occurrence",
                "act_occurrence_identity": recorded.payload["act_occurrence_identity"],
            }
            for event in material
        ],
    ]
    assert recorded.payload["dimensions"]["authority"] == "unestablished"
    assert recorded.payload["dimensions"]["evidence_scope"].endswith(
        "Standing beyond this result"
    )


def test_adjacency_pair_measurement_read_does_not_repeat_measurement(monkeypatch):
    import seed_runtime.adjacency_pair_measurement as module

    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    finding_identity = measurements[0].evidence["adjacency_evidence_event_identity"]
    recorded = record_adjacency_pair_measurements(
        ledger,
        locality_identity="adjacent-measurement",
        finding_event_identity=finding_identity,
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("historical address repeated Measurement")

    monkeypatch.setattr(module, "_measure_adjacency_pair_measurements", forbidden)
    assert get_recorded_adjacency_pair_measurements(ledger, recorded.identity)


def test_adjacency_pair_measurement_read_refuses_changed_result_or_input_evidence():
    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    finding_identity = measurements[0].evidence["adjacency_evidence_event_identity"]
    recorded = record_adjacency_pair_measurements(
        ledger,
        locality_identity="adjacent-measurement",
        finding_event_identity=finding_identity,
    )

    different = recorded.model_copy(deep=True)
    different.payload["measurements"][0]["exact_order"] = [0, 1, 3, 2]
    different = ledger.append(
        different.kind,
        different.payload,
        locality_identity=different.locality_identity,
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="edge Evidence concerns different coordinates",
    ):
        get_recorded_adjacency_pair_measurements(ledger, different.identity)

    act_evidence = ledger.get(recorded.payload["responsible_act_evidence_identity"])
    altered_act_payload = json.loads(json.dumps(act_evidence.payload))
    altered_act_payload["input_applicability"][0]["standing"] = "Unknown"
    altered_act = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
        altered_act_payload,
        locality_identity="adjacent-measurement",
    )
    altered_event_payload = json.loads(json.dumps(recorded.payload))
    altered_event_payload["responsible_act_evidence_identity"] = altered_act.identity
    altered_event = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND,
        altered_event_payload,
        locality_identity="adjacent-measurement",
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="Act Evidence concerns different inputs",
    ):
        get_recorded_adjacency_pair_measurements(
            ledger, altered_event.identity
        )


def test_adjacency_pair_measurement_endpoints_do_not_establish_participation():
    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    recorded = record_adjacency_pair_measurements(
        ledger,
        locality_identity="adjacent-measurement",
        finding_event_identity=measurements[0].evidence["adjacency_evidence_event_identity"],
    )

    missing = recorded.model_copy(deep=True)
    missing.payload.pop("participation")
    missing = ledger.append(
        missing.kind,
        missing.payload,
        locality_identity=missing.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Participation"):
        get_recorded_adjacency_pair_measurements(ledger, missing.identity)

    wrong = recorded.model_copy(deep=True)
    wrong.payload["participation"][0]["act_occurrence_identity"] = "other-occurrence"
    wrong = ledger.append(
        wrong.kind,
        wrong.payload,
        locality_identity=wrong.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Participation"):
        get_recorded_adjacency_pair_measurements(ledger, wrong.identity)


def test_adjacency_pair_measurement_read_refuses_self_consistent_counterfeit_source_text():
    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    finding_identity = measurements[0].evidence["adjacency_evidence_event_identity"]
    recorded = record_adjacency_pair_measurements(
        ledger,
        locality_identity="adjacent-measurement",
        finding_event_identity=finding_identity,
    )

    altered_result = {
        "adjacency_evidence_event_identity": recorded.payload[
            "adjacency_evidence_event_identity"
        ],
        "source_occurrence_identities": recorded.payload["source_occurrence_identities"],
        "measurements": json.loads(json.dumps(recorded.payload["measurements"])),
    }
    altered_result["measurements"][0]["evidence"]["exact_representation"] = (
        "L a b counterfeit"
    )
    altered_result["measurements"][0]["right_occurrence"]["representation"] = (
        "counterfeit"
    )
    act_payload = json.loads(
        json.dumps(
            ledger.get(recorded.payload["responsible_act_evidence_identity"]).payload
        )
    )
    act_evidence = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
        act_payload,
        locality_identity="adjacent-measurement",
    )
    yield_payload = json.loads(
        json.dumps(ledger.get(recorded.payload["yield_evidence_identity"]).payload)
    )
    yield_payload["result"] = altered_result
    yield_evidence = ledger.append(
        "operator.yield.evidence_recorded",
        yield_payload,
        locality_identity="adjacent-measurement",
    )
    locality_payload = json.loads(
        json.dumps(ledger.get(recorded.payload["locality_evidence_identity"]).payload)
    )
    locality_payload["carried_content"] = altered_result
    locality_evidence = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND,
        locality_payload,
        locality_identity="adjacent-measurement",
    )
    event_payload = json.loads(json.dumps(recorded.payload))
    event_payload.update(altered_result)
    event_payload["responsible_act_evidence_identity"] = act_evidence.identity
    event_payload["yield_evidence_identity"] = yield_evidence.identity
    event_payload["locality_evidence_identity"] = locality_evidence.identity
    event = ledger.append(
        ADJACENCY_PAIR_MEASUREMENT_RECORDED_KIND,
        event_payload,
        locality_identity="adjacent-measurement",
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="different Evidence",
    ):
        get_recorded_adjacency_pair_measurements(ledger, event.identity)



def test_a_pair_must_be_two_exact_representations():
    for bad in (("", "is"), ("it", ""), (None, "is")):
        with pytest.raises(PreservedMaterialMeasurementError):
            AdjacencyPair(*bad)


def test_emitted_representation_adjacency_requires_exact_locality():
    ledger = EventLedger()
    representation = record_operator_representation(
        ledger,
        locality_identity="emission-measurement",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="emission-measurement"
        ),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    emitted = emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    emission = ledger.get(emitted["emitted_event_identity"])

    measurements = measure_emitted_representation_adjacency(
        ledger, emission_event_identity=emission.identity
    )
    assert measurements
    assert all(item.source_occurrence_identity == emission.identity for item in measurements)
    assert all(
        item.evidence["source_kind"] == "operator.representation.emitted"
        for item in measurements
    )
    assert all(
        item.evidence["adjacency_evidence_event_identity"]
        == emission.payload["locality_evidence_identity"]
        for item in measurements
    )
    recorded_measurements = record_emitted_representation_adjacency(
        ledger,
        emission_event_identity=emission.identity,
    )
    assert get_recorded_adjacency_pair_measurements(
        ledger, recorded_measurements.identity
    ) == measurements
    assert recorded_measurements.payload["adjacency_evidence_event_identity"] == (
        emission.payload["locality_evidence_identity"]
    )
    assert [
        item["subject_reference"] for item in recorded_measurements.payload["participation"]
    ] == [emission.payload["locality_evidence_identity"], emission.identity]

    copied = emission.model_copy(deep=True)
    copied.payload["locality_evidence_identity"] = None
    copied = ledger.append(
        copied.kind,
        copied.payload,
        locality_identity=copied.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        measure_emitted_representation_adjacency(
            ledger, emission_event_identity=copied.identity
        )

    repeated = emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    repeated_emission = ledger.get(repeated["emitted_event_identity"])
    assert (
        repeated_emission.payload["emitted_representation"]
        == emission.payload["emitted_representation"]
    )
    repeated_measurements = record_emitted_representation_adjacency(
        ledger,
        emission_event_identity=repeated_emission.identity,
    )
    recorded_compare = record_adjacency_pair_measurement_compare(
        ledger,
        locality_identity="emission-measurement",
        measurement_event_identities=(
            recorded_measurements.identity,
            repeated_measurements.identity,
        ),
    )
    read_compare = get_recorded_adjacency_pair_measurement_compare(
        ledger,
        recorded_compare.identity,
    )
    assert read_compare == compare_emitted_representation_adjacency(
        ledger,
        emission_event_identities=(emission.identity, repeated_emission.identity),
    )
    assert [
        item["subject_reference"] for item in recorded_compare.payload["participation"]
    ] == [recorded_measurements.identity, repeated_measurements.identity]
    wrong_occurrence = emission.model_copy(deep=True)
    wrong_occurrence.payload["locality_evidence_identity"] = repeated_emission.payload[
        "locality_evidence_identity"
    ]
    wrong_occurrence = ledger.append(
        wrong_occurrence.kind,
        wrong_occurrence.payload,
        locality_identity=wrong_occurrence.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        measure_emitted_representation_adjacency(
            ledger, emission_event_identity=wrong_occurrence.identity
        )

    compared = compare_emitted_representation_adjacency(
        ledger,
        emission_event_identities=(emission.identity, repeated_emission.identity),
    )
    assert compared["measurement_count"] == 2 * len(measurements)
    assert (
        compared["distinct_fully_bounded_occurrences"]
        == compared["fully_bounded_measurement_count"]
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
            emission_event_identities=("same", "same"),
        )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="intact emission occurrence",
    ):
        compare_emitted_representation_adjacency(
            ledger,
            emission_event_identities=("missing-one", "missing-two"),
        )


def test_emission_adjacency_refuses_corrupted_locality_evidence(tmp_path):
    ledger = SQLiteEventLedger(tmp_path / "emission-adjacency.sqlite")
    representation = record_operator_representation(
        ledger,
        locality_identity="s",
        locality_standing=read_operator_locality_standing(
            ledger, locality_identity="s"
        ),
        alternative_sources=BOUNDED_ALTERNATIVE_FIXTURE_SOURCES,
    )
    emitted = emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    emission = ledger.get(emitted["emitted_event_identity"])
    locality_identity = emission.payload["locality_evidence_identity"]
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET content_hash = ? WHERE identity= ?",
        ("corrupted", locality_identity),
    )
    ledger._connection.commit()

    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        measure_emitted_representation_adjacency(
            ledger,
            emission_event_identity=emission.identity,
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
        locality_identity="s",
        input_stream=binary_input("alpha beta\n"),
        output_stream=StringIO(),
    )
    occurrences = ingest_occurrences(
        ledger, locality_identity="s"
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
