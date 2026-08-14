import json
from io import StringIO
from pathlib import Path

from seed_runtime.byte_measurement import (
    _pair_input_applicability,
    assertions_of_recorded_byte_measurement,
    record_byte_count_layer,
)
from seed_runtime.events import EventLedger
from seed_runtime.operator_console import run_persistent_operator_console


GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed/grammar.json"

EXACT = "exact"
INAPPLICABLE = "inapplicable"
UNKNOWN = "Unknown"
MISSING = "missing"
CONTRADICTION = "contradiction"


def _clause(clause_id: str) -> dict:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["clauses"][clause_id]


def _source_assertion():
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="source",
        input_stream=StringIO("ta\nexit\n"),
        output_stream=StringIO(),
    )
    measurement = record_byte_count_layer(
        ledger,
        workspace_id="w",
        source_session_ids=("source",),
        recording_session_id="byte-measurement",
    )
    assertion = next(
        item
        for item in assertions_of_recorded_byte_measurement(ledger, measurement.id)
        if item.result == "exact_source_material_set"
    )
    return assertion


def _assertion_projection(assertion) -> dict[str, str]:
    payload = assertion.payload
    dimensions = payload["dimensions"]
    return {
        # Runtime identity commits to result, subject, Scope, and content.  The
        # grammar currently names asserted content alone.  Projection exposes
        # the disagreement; it does not choose which side should change.
        "identity": CONTRADICTION,
        # support_basis is not silently promoted into Evidence.
        "Evidence": MISSING,
        "provenance": EXACT if dimensions.get("source_provenance") else MISSING,
        "Scope": EXACT if payload.get("assertion_scope") else MISSING,
        "Authority": EXACT if dimensions.get("authority") else MISSING,
        "conflicts": MISSING,
        "limits": EXACT if payload.get("forbidden_inferences") else MISSING,
        "Unknowns": EXACT if payload.get("unknowns") else MISSING,
        "Standing": EXACT if dimensions.get("standing") else MISSING,
    }


def _applicability_projection(applicability: dict) -> dict[str, str]:
    content = applicability["dimensions"]["content"]
    treatment = applicability["coordinate_treatment"]
    return {
        "input_identity": (
            EXACT if applicability.get("input_assertion_ref") else MISSING
        ),
        "exact_Act": EXACT if applicability.get("target_act_id") else MISSING,
        "subject": EXACT if content.get("target_act") else MISSING,
        "result_boundary": EXACT if applicability.get("result_boundary") else MISSING,
        "Scope": EXACT if applicability.get("scope_locality") else MISSING,
        "locality": EXACT if applicability.get("act_context") else MISSING,
        "Authority": EXACT if applicability["dimensions"].get("authority") else MISSING,
        "participants_and_roles": MISSING,
        "provenance": (
            EXACT
            if applicability["dimensions"].get("source_provenance")
            else MISSING
        ),
        "Standing": (
            EXACT if applicability["dimensions"].get("standing") else MISSING
        ),
        # Applicability explicitly establishes no input-to-result support
        # relation, but the runtime carries no coordinate saying so.
        "support_relation_Standing": MISSING,
        "currentness": (
            INAPPLICABLE
            if treatment.get("currentness", {}).get("treatment")
            == "not required for this historical bounded population"
            else MISSING
        ),
        "occurrence_identity": (
            EXACT if applicability.get("applicability_act_occurrence_id") else MISSING
        ),
        "known_loss": (
            UNKNOWN
            if treatment.get("known_loss", {}).get("treatment")
            == "not represented by input"
            else MISSING
        ),
        "conflicts": EXACT if "conflicts" in applicability else MISSING,
        "Unknowns": EXACT if applicability.get("unknowns") else MISSING,
        "negative_Authority": (
            EXACT if treatment.get("negative_authority") else MISSING
        ),
    }


def test_assertion_clause_projects_onto_a_live_byte_assertion():
    clause = _clause("01.Standing.D.1")
    projection = _assertion_projection(_source_assertion())

    assert set(projection) == {"identity", *clause["responsibility"]["coordinates"]}
    assert projection == {
        "identity": CONTRADICTION,
        "Evidence": MISSING,
        "provenance": EXACT,
        "Scope": EXACT,
        "Authority": EXACT,
        "conflicts": MISSING,
        "limits": EXACT,
        "Unknowns": EXACT,
        "Standing": EXACT,
    }


def test_applicability_clause_projects_onto_a_live_pair_determination():
    clause = _clause("01.Standing.E.1")
    source = _source_assertion()
    applicability = _pair_input_applicability(
        source,
        target_act_id="pair-act",
        applicability_act_id="applicability-act",
        applicability_act_occurrence_id="applicability-occurrence",
        act_workspace_id="w",
        measurement_session_id="measurement",
    )
    projection = _applicability_projection(applicability)

    assert set(projection) == set(clause["coordinates"])
    assert projection == {
        "input_identity": EXACT,
        "exact_Act": EXACT,
        "subject": EXACT,
        "result_boundary": EXACT,
        "Scope": EXACT,
        "locality": EXACT,
        "Authority": EXACT,
        "participants_and_roles": MISSING,
        "provenance": EXACT,
        "Standing": EXACT,
        "support_relation_Standing": MISSING,
        "currentness": INAPPLICABLE,
        "occurrence_identity": EXACT,
        "known_loss": UNKNOWN,
        "conflicts": EXACT,
        "Unknowns": EXACT,
        "negative_Authority": EXACT,
    }
