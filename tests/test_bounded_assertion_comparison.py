"""The smallest bounded Assertion comparison, and what it refuses to conclude.

`01.Standing.E` permits it. `#2416` reconstructed its responsible boundary as local to each
instantiated comparison and never universal, so these tests pin that the
comparison is an occurrence and not a service: nothing survives a call, and
there is no object to hold.

The restraint is pinned as carefully as the result. Two measurements over
different bounded exchanges are each exact within their own scope, so differing
results are not disagreement and matching results are not corroboration. A test
that let this yield `agreement` across exchanges would be manufacturing the
cross-body conclusion the whole arc has been avoiding.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.bounded_assertion_comparison import (
    COMPARISON_RECORDED_KIND,
    INPUT_COORDINATES,
    BoundedComparisonError,
    compare_preserved_findings,
    record_comparison_finding,
)
from seed_runtime.events import EventLedger
from seed_runtime.adjacent_pair_measurement import measure_after
from seed_runtime.preserved_material_measurement import (
    preserved_ingress_occurrences,
    record_measurement_finding,
)
from seed_runtime.operator_console import run_persistent_operator_console

BODIES = {
    "s1": "a noun is a word\nand a verb is a word\n",
    "s2": "a noun is a thing\nand a verb is a thing\n",
}
SCOPE = "one bounded exchange"


@pytest.fixture
def ledger():
    led = EventLedger()
    for session_id, material in BODIES.items():
        run_persistent_operator_console(
            ledger=led, workspace_id="w", session_id=session_id,
            input_stream=StringIO(material + "exit\n"), output_stream=StringIO())
    return led


def _finding(led, session_id, representation="a", scope=SCOPE):
    occurrences = preserved_ingress_occurrences(
        led, workspace_id="w", session_id=session_id
    )
    return record_measurement_finding(
        led, workspace_id="w", session_id=session_id,
        finding=measure_after(occurrences, representation, counting_scope=scope),
    )


# --------------------------------------------------------------------------
# It is an occurrence, not a service.
# --------------------------------------------------------------------------


def test_a_comparison_needs_more_than_one_preserved_finding(ledger):
    one = _finding(ledger, "s1")
    with pytest.raises(BoundedComparisonError, match="exactly two"):
        compare_preserved_findings(ledger, [one.id])


def test_more_than_two_inputs_are_refused(ledger):
    """The report said n-ary comparison was unbuilt; the runtime built it.

    An earlier form accepted any number and intersected them all, so a
    three-body comparison existed and nothing said what it established. What
    more than two inputs jointly establish is not reconstructed, and a set
    intersection is not that reconstruction.
    """
    a, b, c = (_finding(ledger, s) for s in ("s1", "s2", "s1"))
    with pytest.raises(BoundedComparisonError, match="more than two is unbuilt"):
        compare_preserved_findings(ledger, [a.id, b.id, c.id])


def test_an_input_compared_with_itself_is_refused(ledger):
    one = _finding(ledger, "s1")
    with pytest.raises(BoundedComparisonError, match="compared with itself"):
        compare_preserved_findings(ledger, [one.id, one.id])


def test_only_recorded_measurement_findings_may_be_consumed(ledger):
    one = _finding(ledger, "s1")
    ingress = preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s1")[0]
    with pytest.raises(BoundedComparisonError, match="not a recorded measurement"):
        compare_preserved_findings(ledger, [one.id, ingress.id])


def test_an_unpreserved_input_is_refused(ledger):
    one = _finding(ledger, "s1")
    with pytest.raises(BoundedComparisonError, match="no such preserved occurrence"):
        compare_preserved_findings(ledger, [one.id, "evt_does_not_exist"])


def test_the_recorded_responsible_boundary_is_local_to_the_occurrence(ledger):
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    event = record_comparison_finding(
        ledger, workspace_id="w", session_id="s1",
        finding=compare_preserved_findings(ledger, [a.id, b.id]))
    assert "local to the instantiated comparison" in event.payload["responsible_boundary"]
    assert "not named universally" in event.payload["responsible_boundary"]


# --------------------------------------------------------------------------
# Each input arrives with what it carries, and what it lacks is named.
# --------------------------------------------------------------------------


def test_each_input_keeps_the_coordinates_it_carries(ledger):
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    for supplied, preserved in zip((a, b), finding.inputs):
        assert preserved.event_id == supplied.id
        assert preserved.carried["standing"] == "measured"
        assert preserved.carried["subject"] == supplied.payload["dimensions"]["identity"]
        assert preserved.carried["forbidden_inferences"] == supplied.payload["boundary_notes"]


def test_an_absent_coordinate_is_named_and_not_supplied(ledger):
    """`#2419`: preserving does not supply what an input lacks."""
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    for preserved in finding.inputs:
        assert "confidence_or_uncertainty" in preserved.absent
        assert "confidence_or_uncertainty" not in preserved.carried
    assert "confidence_or_uncertainty" in INPUT_COORDINATES


def test_the_support_basis_travels_with_its_input(ledger):
    seed = _finding(ledger, "s1")
    occurrences = preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s1")
    standing_on = record_measurement_finding(
        ledger, workspace_id="w", session_id="s1",
        finding=measure_after(occurrences, "is", counting_scope=SCOPE, premise_event_id=seed.id))
    other = _finding(ledger, "s2")
    finding = compare_preserved_findings(ledger, [standing_on.id, other.id])
    assert finding.inputs[0].support_basis == (seed.id,)
    assert finding.inputs[1].support_basis == ()


# --------------------------------------------------------------------------
# What it establishes, and what it refuses to.
# --------------------------------------------------------------------------


def test_it_reports_which_occupants_both_findings_hold(ledger):
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    assert "noun" in finding.shared_occupants
    assert "verb" in finding.shared_occupants
    assert set(finding.occupants_in_one_only) == {a.id, b.id}


def test_findings_from_different_exchanges_do_not_reach_agreement(ledger):
    """The restraint. Each is exact within its own scope."""
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    assert finding.bounded_relation == "Unknown"
    assert "different bounded exchanges" in finding.relation_basis
    assert "not disagreement" in finding.relation_basis
    assert "not corroboration" in finding.relation_basis


def test_a_different_measured_subject_yields_Unknown(ledger):
    a = _finding(ledger, "s1", representation="a")
    b = _finding(ledger, "s2", representation="is")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    assert finding.bounded_relation == "Unknown"
    assert "same representation" in finding.relation_basis
    assert not [d for d in finding.distinctions
               if d.coordinate == "representation_measured" and d.same]


def test_two_findings_in_one_exchange_may_reach_agreement(ledger):
    """Within one scope the relation is establishable, and only there."""
    a, b = _finding(ledger, "s1"), _finding(ledger, "s1")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    assert finding.bounded_relation == "agreement"
    assert all(d.same for d in finding.distinctions)


def test_the_left_representation_is_compared_as_a_coordinate(ledger):
    """Pair identity must not be reconstructed from prose.

    `representation_measured` is a sentence. The anchor a finding measured from
    is carried structurally, and a comparison asking whether two findings share
    a left representation must read that rather than parse the sentence.
    """
    a = _finding(ledger, "s1", representation="a")
    b = _finding(ledger, "s2", representation="a")
    by_name = {d.coordinate: d for d in
               compare_preserved_findings(ledger, [a.id, b.id]).distinctions}
    assert by_name["measured_left_representation"].same
    assert by_name["measured_left_representation"].values == ("a", "a")

    c = _finding(ledger, "s2", representation="is")
    by_name = {d.coordinate: d for d in
               compare_preserved_findings(ledger, [a.id, c.id]).distinctions}
    assert not by_name["measured_left_representation"].same
    assert by_name["measured_left_representation"].values == ("a", "is")


def test_a_different_left_representation_yields_Unknown(ledger):
    a = _finding(ledger, "s1", representation="a")
    b = _finding(ledger, "s1", representation="is")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    assert finding.bounded_relation == "Unknown"
    assert "same representation" in finding.relation_basis


def test_the_distinctions_are_literal(ledger):
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    finding = compare_preserved_findings(ledger, [a.id, b.id])
    by_name = {d.coordinate: d for d in finding.distinctions}
    assert by_name["representation_measured"].same
    assert by_name["equivalence_rule"].same
    assert not by_name["bounded_exchange"].same
    assert by_name["bounded_exchange"].values == (
        "workspace:w;session:s1", "workspace:w;session:s2")


# --------------------------------------------------------------------------
# The recorded occurrence.
# --------------------------------------------------------------------------


def test_the_comparison_is_recorded_as_its_own_kind(ledger):
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    event = record_comparison_finding(
        ledger, workspace_id="w", session_id="s1",
        finding=compare_preserved_findings(ledger, [a.id, b.id]))
    assert event.kind == COMPARISON_RECORDED_KIND
    assert event.payload["input_event_ids"] == [a.id, b.id]
    assert event.payload["dimensions"]["standing"] == "compared"


def test_the_record_refuses_the_inferences_the_clause_forbids(ledger):
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    event = record_comparison_finding(
        ledger, workspace_id="w", session_id="s1",
        finding=compare_preserved_findings(ledger, [a.id, b.id]))
    notes = " ".join(event.payload["boundary_notes"])
    assert "is not a relation between what they measured" in notes
    assert "establishes no relation between" in notes
    assert "no truth, support, input support, source independence, or corroboration" in notes
    assert "whether the compared bodies stand in any relation remains Unknown" in (
        event.payload["unknowns"])


def test_recording_a_comparison_does_not_disturb_its_inputs(ledger):
    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    before = (dict(a.payload), dict(b.payload))
    record_comparison_finding(
        ledger, workspace_id="w", session_id="s1",
        finding=compare_preserved_findings(ledger, [a.id, b.id]))
    assert (ledger.get(a.id).payload, ledger.get(b.id).payload) == before


def test_a_comparison_is_not_a_measurement(ledger):
    from seed_runtime.preserved_material_measurement import MEASUREMENT_RECORDED_KIND

    a, b = _finding(ledger, "s1"), _finding(ledger, "s2")
    event = record_comparison_finding(
        ledger, workspace_id="w", session_id="s1",
        finding=compare_preserved_findings(ledger, [a.id, b.id]))
    assert event.kind != MEASUREMENT_RECORDED_KIND
    assert "occupancies" not in event.payload
