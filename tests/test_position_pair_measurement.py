"""Exact position-pair acquisition and occurrence-bound measurements."""

from __future__ import annotations

from copy import deepcopy
import json
from dataclasses import replace
from tests.binary_input import binary_input
from io import StringIO

import pytest

from seed_runtime.events import EventLedger, InvalidLedgerBoundary, SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.position_pair_measurement import (
    EQUIVALENCE_RULE,
    enumerate_position_difference,
    enumerate_representations,
    measure_after,
    measure_at_position_difference,
    PositionPair,
    position_pairs_from_finding,
    measure_position_pairs_from_finding,
    measure_emitted_representation_position_pair,
    compare_emitted_representation_position_pair,
    record_emitted_representation_position_pair,
    record_position_pair_measurement_compare,
    get_recorded_position_pair_measurement_compare,
    compare_position_pair_measurements,
    record_position_pair_measurements,
    get_recorded_position_pair_measurements,
    POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
    POSITION_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND,
    POSITION_PAIR_MEASUREMENT_RECORDED_KIND,
)
from seed_runtime.preserved_material_measurement import (
    INGEST_OCCURRED_KIND,
    MEASUREMENT_RECORDED_KIND,
    DeclaredMeasurement,
    RepresentationCount,
    PreservedMaterialMeasurementError,
    measure_position_representations,
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
from seed_runtime.material_ingest import ingest_material

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
    assert recorded_finding.material["relative_representation"] == LEFT


def test_pairs_are_read_from_the_record_not_supplied(locality, recorded_finding):
    pairs = position_pairs_from_finding(locality, recorded_finding.identity)
    assert pairs
    assert all(pair.first == LEFT for pair in pairs)
    assert PositionPair(first="it", second="is") in pairs


def test_every_measured_representation_becomes_a_pair(locality, recorded_finding):
    """No count or share decides which pairs are returned."""
    pairs = position_pairs_from_finding(locality, recorded_finding.identity)
    assert len(pairs) == len(recorded_finding.material["representation_counts"])


def test_a_finding_that_names_no_representation_cannot_supply_one(locality, occurrences):
    event = record_measurement_finding(
        locality,
        locality_identity="s",
        finding=measure_position_representations(
            occurrences,
            declared=DeclaredMeasurement(
                representation_measured="the first representation",
                equivalence_rule=EQUIVALENCE_RULE,
                counting_scope="this locality",
            ),
            representation_at=lambda t: (t.split() or [None])[0],
        ),
    )
    with pytest.raises(PreservedMaterialMeasurementError):
        position_pairs_from_finding(locality, event.identity)


def test_pairs_must_come_from_a_measurement_finding(locality, occurrences):
    foreign = locality.append("unrelated.kind", {"representation_counts": []}, locality_identity="s")
    with pytest.raises(PreservedMaterialMeasurementError):
        position_pairs_from_finding(locality, foreign.identity)



# --------------------------------------------------------------------------
# Exact pair occurrences are extended one position on each side.
# --------------------------------------------------------------------------


def _measurement_road(lines: tuple[str, ...], measured_lefts: tuple[str, ...]):
    ledger = EventLedger()
    for line in lines:
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_identity="position-measurement",
        )
    material = ingest_occurrences(
        ledger, locality_identity="position-measurement"
    )
    measurements = []
    for measured_left in measured_lefts:
        finding = record_measurement_finding(
            ledger,
            locality_identity="position-measurement",
            finding=measure_after(
                material,
                measured_left,
                counting_scope="exact bounded measurement fixture",
            ),
        )
        measurements.extend(
            measure_position_pairs_from_finding(
                ledger,
                finding_event_identity=finding.identity,
                occurrences=material,
            )
        )
    return ledger, tuple(measurements)


def test_every_exact_pair_occurrence_preserves_its_position_pair_measurement_and_evidence():
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
        pair_finding = ledger.get(measurement.evidence["position_pair_evidence_event_identity"])
        assert pair_finding.kind == MEASUREMENT_RECORDED_KIND
        assert measurement.evidence == {
            "source_occurrence_identity": source.identity,
            "position_pair_evidence_event_identity": pair_finding.identity,
            "evidence_occurrence_identities": [
                pair_finding.identity,
                source.identity,
            ],
            "source_kind": INGEST_OCCURRED_KIND,
            "locality_identity": "position-measurement",
            "exact_representation": source.material["represented_material"],
        }
        assert measurement.pair_occurrence.second.position == (
            measurement.pair_occurrence.first.position + 1
        )
        assert measurement.fully_bounded_coordinates["identity"] == {
            "position_pair_evidence_event_identity": pair_finding.identity,
            "source_occurrence_identity": source.identity,
            "exact_order": list(measurement.exact_order),
        }


def test_position_pair_measurement_refuses_a_different_or_rewritten_source_occurrence():
    ledger = EventLedger()
    for line in ("L a b R", "X a b Y"):
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_identity="position-measurement",
        )
    material = ingest_occurrences(
        ledger, locality_identity="position-measurement"
    )
    finding = record_measurement_finding(
        ledger,
        locality_identity="position-measurement",
        finding=measure_after(material, "a", counting_scope="exact fixture"),
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="differ from the finding's exact Evidence",
    ):
        measure_position_pairs_from_finding(
            ledger,
            finding_event_identity=finding.identity,
            occurrences=reversed(material),
        )

    rewritten = deepcopy(material[0])
    rewritten.material["represented_material"] = "L a b different"
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="source-occurrence Evidence does not read",
    ):
        measure_position_pairs_from_finding(
            ledger,
            finding_event_identity=finding.identity,
            occurrences=(rewritten, material[1]),
        )

    relocated = deepcopy(material[0])
    object.__setattr__(relocated, "locality_identity", "other")
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="source-occurrence Evidence does not read",
    ):
        measure_position_pairs_from_finding(
            ledger,
            finding_event_identity=finding.identity,
            occurrences=(relocated, material[1]),
        )


def test_system_bytes_do_not_become_represented_material():
    import seed_runtime.position_pair_measurement as module

    system_material = ingest_material(
        EventLedger(),
        locality_identity="position-measurement",
        exact_bytes=b"L a b R",
        source_role="system",
        source_boundary="system boundary",
        known_loss=(
            "material before the supplied system boundary is not available here",
        ),
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="carries no represented material",
    ):
        module._measure_position_pair_measurements(
            (system_material,),
            (PositionPair("a", "b"),),
            position_pair_evidence_event_identity="evidence_not_consulted",
        )


def test_direct_measurement_input_cannot_rewrite_order_position_pair_or_evidence():
    _, measurements = _measurement_road(("L a b R",), ("a",))
    measurement = measurements[0]

    mutations = (
        lambda item: replace(item, exact_order=(0, 2, 1, 3)),
        lambda item: replace(
            item,
            before_occurrence=replace(item.before_occurrence, position=7),
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
        match="same exact position-pair measurement",
    ):
        compare_position_pair_measurements((measurement, measurement))
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="exact bounded measurements",
    ):
        compare_position_pair_measurements((measurement, {"looks": "similar"}))


def test_boundary_absence_is_preserved_without_filling_positions():
    _, measurements = _measurement_road(
        ("a b R", "L a b", "a b"),
        ("a",),
    )

    assert [
        (
            measurement.before_occurrence is not None,
            measurement.after_occurrence is not None,
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
    assert first["before_occurrence"]["representation"] == second["before_occurrence"][
        "representation"
    ]
    assert first["pair_occurrence"]["ordered_pair"] == second["pair_occurrence"][
        "ordered_pair"
    ]
    assert first["after_occurrence"]["representation"] == second["after_occurrence"][
        "representation"
    ]
    assert first["identity"] != second["identity"]


def test_compare_reports_only_position_pair_coordinates_that_survive_counterexamples():
    _, measurements = _measurement_road(
        (
            "L a b R",
            "L a b R",
            "X a b Y",
            "L c d R",
        ),
        ("a", "c"),
    )

    compared = compare_position_pair_measurements(measurements)
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
        "distinct_position_pair_coordinates": [
            {
                "before_present": True,
                "after_present": True,
                "exact_order_difference": [1, 1, 1],
            }
        ],
    }


def test_position_pair_measurement_measurement_records_exact_coordinates_and_reads_result():
    ledger = EventLedger()
    for line in ("L a b R", "X a b Y"):
        ledger.append(
            INGEST_OCCURRED_KIND,
            {"represented_material": line},
            locality_identity="position-measurement",
        )
    material = ingest_occurrences(
        ledger, locality_identity="position-measurement"
    )
    finding = record_measurement_finding(
        ledger,
        locality_identity="position-measurement",
        finding=measure_after(material, "a", counting_scope="exact fixture"),
    )

    recorded = record_position_pair_measurements(
        ledger,
        locality_identity="position-measurement",
        finding_event_identity=finding.identity,
    )
    read = get_recorded_position_pair_measurements(
        ledger, recorded.identity
    )

    assert recorded.kind == POSITION_PAIR_MEASUREMENT_RECORDED_KIND
    assert read == measure_position_pairs_from_finding(
        ledger,
        finding_event_identity=finding.identity,
        occurrences=material,
    )
    assert len(read) == 2
    act_evidence = ledger.get(recorded.material["responsible_act_evidence_identity"])
    yield_evidence = ledger.get(recorded.material["yield_evidence_identity"])
    locality_evidence = ledger.get(recorded.material["locality_evidence_identity"])
    assert act_evidence.kind == POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND
    assert locality_evidence.kind == POSITION_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND
    assert (
        recorded.material["act_occurrence_identity"]
        == act_evidence.material["act_occurrence_identity"]
        == yield_evidence.material["dimensions"]["act_occurrence_identity"]
        == locality_evidence.material["act_occurrence_identity"]
    )
    assert act_evidence.material["input_applicability"] == [
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
    assert recorded.material["participation"] == act_evidence.material["participation"]
    assert recorded.material["participation"] == [
        {
            "subject_reference": finding.identity,
            "role": "read ordered-pair finding",
            "act_occurrence_identity": recorded.material["act_occurrence_identity"],
        },
        *[
            {
                "subject_reference": event.identity,
                "role": "exact preserved source occurrence",
                "act_occurrence_identity": recorded.material["act_occurrence_identity"],
            }
            for event in material
        ],
    ]
    assert recorded.material["dimensions"]["authority"] == "unestablished"
    assert recorded.material["dimensions"]["evidence_scope"].endswith(
        "Standing beyond this result"
    )


def test_position_pair_measurement_read_does_not_repeat_measurement(monkeypatch):
    import seed_runtime.position_pair_measurement as module

    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    finding_identity = measurements[0].evidence["position_pair_evidence_event_identity"]
    recorded = record_position_pair_measurements(
        ledger,
        locality_identity="position-measurement",
        finding_event_identity=finding_identity,
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("historical address repeated Measurement")

    monkeypatch.setattr(module, "_measure_position_pair_measurements", forbidden)
    assert get_recorded_position_pair_measurements(ledger, recorded.identity)


def test_position_pair_measurement_read_refuses_changed_result_or_input_evidence():
    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    finding_identity = measurements[0].evidence["position_pair_evidence_event_identity"]
    recorded = record_position_pair_measurements(
        ledger,
        locality_identity="position-measurement",
        finding_event_identity=finding_identity,
    )

    different = deepcopy(recorded)
    different.material["measurements"][0]["exact_order"] = [0, 1, 3, 2]
    different = ledger.append(
        different.kind,
        different.material,
        locality_identity=different.locality_identity,
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="relation Evidence carries different coordinates",
    ):
        get_recorded_position_pair_measurements(ledger, different.identity)

    act_evidence = ledger.get(recorded.material["responsible_act_evidence_identity"])
    altered_act_material = json.loads(json.dumps(act_evidence.material))
    altered_act_material["input_applicability"][0]["standing"] = "Unknown"
    altered_act = ledger.append(
        POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
        altered_act_material,
        locality_identity="position-measurement",
    )
    altered_event_material = json.loads(json.dumps(recorded.material))
    altered_event_material["responsible_act_evidence_identity"] = altered_act.identity
    altered_event = ledger.append(
        POSITION_PAIR_MEASUREMENT_RECORDED_KIND,
        altered_event_material,
        locality_identity="position-measurement",
    )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="Act Evidence carries different inputs",
    ):
        get_recorded_position_pair_measurements(
            ledger, altered_event.identity
        )


def test_position_pair_measurement_endpoints_do_not_establish_participation():
    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    recorded = record_position_pair_measurements(
        ledger,
        locality_identity="position-measurement",
        finding_event_identity=measurements[0].evidence["position_pair_evidence_event_identity"],
    )

    missing = deepcopy(recorded)
    missing.material.pop("participation")
    missing = ledger.append(
        missing.kind,
        missing.material,
        locality_identity=missing.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Participation"):
        get_recorded_position_pair_measurements(ledger, missing.identity)

    wrong = deepcopy(recorded)
    wrong.material["participation"][0]["act_occurrence_identity"] = "other-occurrence"
    wrong = ledger.append(
        wrong.kind,
        wrong.material,
        locality_identity=wrong.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Participation"):
        get_recorded_position_pair_measurements(ledger, wrong.identity)


def test_position_pair_measurement_read_refuses_self_consistent_counterfeit_source_text():
    ledger, measurements = _measurement_road(("L a b R",), ("a",))
    finding_identity = measurements[0].evidence["position_pair_evidence_event_identity"]
    recorded = record_position_pair_measurements(
        ledger,
        locality_identity="position-measurement",
        finding_event_identity=finding_identity,
    )

    altered_result = {
        "result_identity": recorded.material["result_identity"],
        "position_pair_evidence_event_identity": recorded.material[
            "position_pair_evidence_event_identity"
        ],
        "source_occurrence_identities": recorded.material["source_occurrence_identities"],
        "measurements": json.loads(json.dumps(recorded.material["measurements"])),
    }
    altered_result["measurements"][0]["evidence"]["exact_representation"] = (
        "L a b counterfeit"
    )
    altered_result["measurements"][0]["after_occurrence"]["representation"] = (
        "counterfeit"
    )
    act_material = json.loads(
        json.dumps(
            ledger.get(recorded.material["responsible_act_evidence_identity"]).material
        )
    )
    act_evidence = ledger.append(
        POSITION_PAIR_MEASUREMENT_ACT_EVIDENCE_KIND,
        act_material,
        locality_identity="position-measurement",
    )
    yield_material = json.loads(
        json.dumps(ledger.get(recorded.material["yield_evidence_identity"]).material)
    )
    yield_material["result"] = altered_result
    yield_evidence = ledger.append(
        "operator.yield.evidence_recorded",
        yield_material,
        locality_identity="position-measurement",
    )
    locality_material = json.loads(
        json.dumps(ledger.get(recorded.material["locality_evidence_identity"]).material)
    )
    locality_material["carried_content"] = altered_result
    locality_evidence = ledger.append(
        POSITION_PAIR_MEASUREMENT_LOCALITY_EVIDENCE_KIND,
        locality_material,
        locality_identity="position-measurement",
    )
    event_material = json.loads(json.dumps(recorded.material))
    event_material.update(altered_result)
    event_material["responsible_act_evidence_identity"] = act_evidence.identity
    event_material["yield_evidence_identity"] = yield_evidence.identity
    event_material["locality_evidence_identity"] = locality_evidence.identity
    event = ledger.append(
        POSITION_PAIR_MEASUREMENT_RECORDED_KIND,
        event_material,
        locality_identity="position-measurement",
    )

    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="different Evidence",
    ):
        get_recorded_position_pair_measurements(ledger, event.identity)



def test_a_pair_must_be_two_exact_representations():
    for bad in (("", "is"), ("it", ""), (None, "is")):
        with pytest.raises(PreservedMaterialMeasurementError):
            PositionPair(*bad)


def test_emitted_representation_position_pair_requires_exact_locality():
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

    measurements = measure_emitted_representation_position_pair(
        ledger, emission_event_identity=emission.identity
    )
    assert measurements
    assert all(item.source_occurrence_identity == emission.identity for item in measurements)
    assert all(
        item.evidence["source_kind"] == "operator.representation.emitted"
        for item in measurements
    )
    assert all(
        item.evidence["position_pair_evidence_event_identity"]
        == emission.material["locality_evidence_identity"]
        for item in measurements
    )
    recorded_measurements = record_emitted_representation_position_pair(
        ledger,
        emission_event_identity=emission.identity,
    )
    assert get_recorded_position_pair_measurements(
        ledger, recorded_measurements.identity
    ) == measurements
    assert recorded_measurements.material["position_pair_evidence_event_identity"] == (
        emission.material["locality_evidence_identity"]
    )
    assert [
        item["subject_reference"] for item in recorded_measurements.material["participation"]
    ] == [emission.material["locality_evidence_identity"], emission.identity]

    copied = deepcopy(emission)
    copied.material["locality_evidence_identity"] = None
    copied = ledger.append(
        copied.kind,
        copied.material,
        locality_identity=copied.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        measure_emitted_representation_position_pair(
            ledger, emission_event_identity=copied.identity
        )

    repeated = emit_operator_representation(
        ledger,
        representation=representation,
        output_stream=StringIO(),
    )
    repeated_emission = ledger.get(repeated["emitted_event_identity"])
    assert (
        repeated_emission.material["emitted_representation"]
        == emission.material["emitted_representation"]
    )
    repeated_measurements = record_emitted_representation_position_pair(
        ledger,
        emission_event_identity=repeated_emission.identity,
    )
    recorded_compare = record_position_pair_measurement_compare(
        ledger,
        locality_identity="emission-measurement",
        measurement_event_identities=(
            recorded_measurements.identity,
            repeated_measurements.identity,
        ),
    )
    read_compare = get_recorded_position_pair_measurement_compare(
        ledger,
        recorded_compare.identity,
    )
    assert read_compare == compare_emitted_representation_position_pair(
        ledger,
        emission_event_identities=(emission.identity, repeated_emission.identity),
    )
    assert [
        item["subject_reference"] for item in recorded_compare.material["participation"]
    ] == [recorded_measurements.identity, repeated_measurements.identity]
    wrong_occurrence = deepcopy(emission)
    wrong_occurrence.material["locality_evidence_identity"] = repeated_emission.material[
        "locality_evidence_identity"
    ]
    wrong_occurrence = ledger.append(
        wrong_occurrence.kind,
        wrong_occurrence.material,
        locality_identity=wrong_occurrence.locality_identity,
    )
    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        measure_emitted_representation_position_pair(
            ledger, emission_event_identity=wrong_occurrence.identity
        )

    compared = compare_emitted_representation_position_pair(
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


def test_emission_position_pair_compare_requires_distinct_real_occurrences():
    ledger = EventLedger()
    with pytest.raises(PreservedMaterialMeasurementError, match="at least two distinct"):
        compare_emitted_representation_position_pair(
            ledger,
            emission_event_identities=("same", "same"),
        )
    with pytest.raises(
        PreservedMaterialMeasurementError,
        match="intact emission occurrence",
    ):
        compare_emitted_representation_position_pair(
            ledger,
            emission_event_identities=("missing-one", "missing-two"),
        )


def test_emission_position_pair_refuses_corrupted_locality_evidence(tmp_path):
    ledger = SQLiteEventLedger(tmp_path / "emission-position_pair.sqlite")
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
    locality_identity = emission.material["locality_evidence_identity"]
    ledger._connection.execute("DROP TRIGGER events_refuse_update")
    ledger._connection.execute(
        "UPDATE events SET occurrence_material_identity = ? WHERE identity= ?",
        ("corrupted", locality_identity),
    )
    ledger._connection.commit()

    with pytest.raises(PreservedMaterialMeasurementError, match="Locality Evidence"):
        measure_emitted_representation_position_pair(
            ledger,
            emission_event_identity=emission.identity,
        )
    ledger.close()


# --------------------------------------------------------------------------
# The material offers the representations, and nobody names one.
# --------------------------------------------------------------------------


def test_representations_are_enumerated_from_the_material(occurrences):
    """No representation is supplied, preferred, or filtered by count."""
    representations = enumerate_representations(occurrences)
    offered = {
        token
        for event in occurrences
        for token in event.material["represented_material"].split()
    }
    assert set(representations) == offered
    assert representations == sorted(representations)


def test_comparability_restricts_representations_without_judging_them(occurrences):
    """`present_in` keeps what every scope returns, not what looks useful."""
    scopes = [occurrences[:2], occurrences[2:]]
    restricted = enumerate_representations(occurrences, present_in=scopes)
    everywhere = set.intersection(
        *[
            {t for e in scope for t in e.material["represented_material"].split()}
            for scope in scopes
        ]
    )
    assert set(restricted) == everywhere
    assert set(restricted) <= set(enumerate_representations(occurrences))


def test_measuring_after_a_representation_records_which(occurrences):
    finding = measure_after(occurrences, "it", counting_scope="this locality")
    assert finding.declared.relative_representation == "it"
    assert finding.highest_count_representation.representation == "is"



def test_agreement_is_the_discriminator_not_a_count(occurrences):
    """A frequent representation that disagrees across scopes is not preferred."""
    scopes = [occurrences[:3], occurrences[3:]]
    disagreeing = []
    for representation in enumerate_representations(occurrences, present_in=scopes):
        results = [
            f.highest_count_representation.representation
            for scope in scopes
            if (f := measure_after(scope, representation, counting_scope="a scope"))
            and f.highest_count_representation is not None
        ]
        if len(results) == len(scopes) and len(set(results)) > 1:
            disagreeing.append(representation)
    # Nothing here promotes a disagreeing representation; it is simply not agreed.
    for representation in disagreeing:
        whole = measure_after(occurrences, representation, counting_scope="whole")
        assert whole.highest_count_representation is not None


def test_position_differences_are_enumerated_from_the_material(occurrences):
    differences = enumerate_position_difference(occurrences, "it")
    assert differences
    assert differences == sorted(differences)
    assert 0 not in differences
    longest = max(
        len(e.material["represented_material"].split())
        for e in occurrences
        if "it" in e.material["represented_material"].split()
    )
    assert max(abs(difference) for difference in differences) < longest


def test_a_position_difference_absent_from_the_material_is_absent(locality):
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
    assert enumerate_position_difference(occurrences, "alpha") == [1]


def test_each_position_difference_is_recorded_on_its_own_finding(occurrences):
    for difference in (-2, -1, 1, 2):
        finding = measure_at_position_difference(
            occurrences, "it", difference=difference, counting_scope=SCOPE
        )
        assert finding.declared.measured_position == {"difference": difference}


def test_no_position_difference_is_preferred(occurrences):
    findings = [
        measure_at_position_difference(
            occurrences, "it", difference=difference, counting_scope=SCOPE
        )
        for difference in enumerate_position_difference(occurrences, "it")
    ]
    assert len({type(f) for f in findings}) == 1
    for finding in findings:
        assert finding.declared.equivalence_rule == EQUIVALENCE_RULE
        assert finding.declared.counting_scope == SCOPE


def test_measuring_before_is_the_same_family(occurrences):
    after = measure_at_position_difference(
        occurrences, "is", difference=1, counting_scope=SCOPE
    )
    before = measure_at_position_difference(
        occurrences, "is", difference=-1, counting_scope=SCOPE
    )
    assert after.declared.measured_position == {"difference": 1}
    assert before.declared.measured_position == {"difference": -1}


def test_measure_after_is_one_position_difference_of_the_family(occurrences):
    assert (
        measure_after(occurrences, "it", counting_scope=SCOPE).to_json_dict()
        == measure_at_position_difference(
            occurrences, "it", difference=1, counting_scope=SCOPE
        ).to_json_dict()
    )


def test_zero_position_difference_is_refused(occurrences):
    for bad in (0, False):
        with pytest.raises(PreservedMaterialMeasurementError):
            measure_at_position_difference(
                occurrences, "it", difference=bad, counting_scope=SCOPE
            )
