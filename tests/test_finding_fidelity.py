"""A bounded comparison of a recorded finding against the act that produced it."""

from __future__ import annotations

import pytest

from seed_runtime.event import Event
from seed_runtime.events import EventLedger
from seed_runtime.finding_fidelity import (
    FAITHFUL_WITHIN_SCOPE,
    FIDELITY_FINDING_KIND,
    INVENTION,
    MUTATION,
    UNFAITHFUL_CROSSING,
    FindingFidelityError,
    compare_recorded_finding,
)
from seed_runtime.preserved_material_measurement import (
    INGRESS_OCCURRED_KIND,
    MEASUREMENT_RECORDED_KIND,
    RESPONSIBILITY_UNRECOVERED,
    DeclaredMeasurement,
    measure_recurrence,
    record_measurement_finding,
)


@pytest.fixture
def recorded():
    ledger = EventLedger()
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


def test_a_finding_that_names_the_evidence_concerning_it_is_faithful(recorded):
    ledger, event = recorded
    result = compare_recorded_finding(ledger, event.id)
    assert result.kind == FIDELITY_FINDING_KIND
    assert result.payload["dimensions"]["standing"] == FAITHFUL_WITHIN_SCOPE
    assert result.payload["observed_crossings"] == []


def test_a_finding_naming_no_production_evidence_is_invention(recorded):
    ledger, event = recorded
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        "w",
        {**event.payload, "production_evidence_id": None},
        session_id="r",
    )
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["dimensions"]["standing"] == UNFAITHFUL_CROSSING
    assert result.payload["observed_crossings"] == [INVENTION]


def test_a_finding_whose_content_its_evidence_does_not_concern_is_mutation(
    recorded,
):
    ledger, event = recorded
    altered = dict(event.payload)
    altered["total_count"] = 999
    forged = ledger.append(MEASUREMENT_RECORDED_KIND, "w", altered, session_id="r")
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["dimensions"]["standing"] == UNFAITHFUL_CROSSING
    assert result.payload["observed_crossings"] == [MUTATION]


def test_the_comparison_revises_nothing(recorded):
    """`01.Uptake.A`: availability is not revision."""

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
    assert dims["producer"] == RESPONSIBILITY_UNRECOVERED
    assert dims["responsibility"] == RESPONSIBILITY_UNRECOVERED
    assert "correction authority" in dims["authority_warrant"]
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
        "unknowns",
        "forbidden_inferences",
    ):
        assert coordinate in result.payload


def test_it_does_not_walk_what_the_finding_stood_on(recorded):
    """Each consumer determines its own applicability -- `01.Standing.E.1`."""

    ledger, event = recorded
    before = len(ledger.list("w"))
    compare_recorded_finding(ledger, event.id)
    # Exactly one occurrence: this comparison. Nothing upstream was touched.
    assert len(ledger.list("w")) == before + 1


def test_only_a_recorded_measurement_finding_may_be_compared(recorded):
    ledger, _ = recorded
    other = ledger.append("unrelated.kind", "w", {}, session_id="r")
    with pytest.raises(FindingFidelityError, match="not a recorded measurement"):
        compare_recorded_finding(ledger, other.id)


def test_a_finding_naming_evidence_that_is_not_preserved_is_invention(recorded):
    """Naming evidence is not having it."""

    ledger, event = recorded
    forged = ledger.append(
        MEASUREMENT_RECORDED_KIND,
        "w",
        {**event.payload, "production_evidence_id": "evt_never_appended"},
        session_id="r",
    )
    result = compare_recorded_finding(ledger, forged.id)
    assert result.payload["dimensions"]["standing"] == UNFAITHFUL_CROSSING
    assert result.payload["observed_crossings"] == [INVENTION]


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
    assert result.payload["observed_crossings"] == [INVENTION]
