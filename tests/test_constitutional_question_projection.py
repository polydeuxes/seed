from dataclasses import asdict

from seed_runtime.bounded_constitutional_question import produce_bounded_constitutional_question
from seed_runtime.constitutional_view_selection import (
    ConstitutionalCapabilityProjection,
    ConstitutionalQuestionProjection,
    project_constitutional_question,
    select_constitutional_views,
)


def _bounded(**overrides):
    inputs = {
        "operator_inquiry": "Operator says process compatibility may matter.",
        "inquiry_provenance": "operator:projection-test",
        "bounded_question": "Explain compatibility for the bounded inquiry.",
        "constitutional_intent": "caller-preserved compatibility request",
        "scope_status": "caller-bounded; not independently verified",
        "uncertainty": ["scope supplied by caller"],
        "unknowns": ["capability support unknown before selection"],
        "bounded_question_id": "bounded-question:projection-test",
        "caller_supplied_fields": {
            "selection_key:process": "explicit caller selection key",
            "note": "operator testimony remains evidence",
        },
    }
    inputs.update(overrides)
    return produce_bounded_constitutional_question(**inputs)


def test_projection_accepts_real_bounded_question_and_preserves_identity_boundaries_and_uncertainty():
    bounded = _bounded()

    projection = project_constitutional_question(bounded)

    assert isinstance(projection, ConstitutionalQuestionProjection)
    assert projection.bounded_question_id == bounded.bounded_question_id
    assert projection.selection_keys == ("process",)
    assert projection.uncertainty == (
        "scope supplied by caller",
        "unknown: capability support unknown before selection",
    )
    assert projection.read_only is True
    assert projection.writes_event_ledger is False
    assert projection.mutates_cluster is False


def test_equivalent_bounded_questions_produce_equivalent_projections_and_do_not_mutate_source():
    first = _bounded()
    second = _bounded()
    before = asdict(first)

    assert project_constitutional_question(first) == project_constitutional_question(second)
    assert asdict(first) == before


def test_projection_does_not_promote_testimony_or_create_downstream_artifacts():
    bounded = _bounded()

    projection_payload = asdict(project_constitutional_question(bounded))

    assert bounded.operator_inquiry == "Operator says process compatibility may matter."
    assert bounded.inquiry_provenance == "operator:projection-test"
    assert bounded.testimony_status == "operator testimony preserved as evidence, not established fact"
    assert "operator_inquiry" not in projection_payload
    assert "inquiry_provenance" not in projection_payload
    assert "established_fact" not in projection_payload
    assert "verified_claim" not in projection_payload
    assert "authoritative_capability" not in projection_payload
    assert "registered_view_name" not in projection_payload
    assert "selected_view_names" not in projection_payload
    assert "composition_purpose" not in projection_payload


def test_missing_explicit_projection_information_is_not_guessed():
    bounded = _bounded(caller_supplied_fields={"note": "no exact key supplied"})

    projection = project_constitutional_question(bounded)

    assert projection.selection_keys == ()
    assert "process" not in projection.selection_keys
    assert "compatibility" not in projection.selection_keys


def test_manual_projection_fixtures_remain_supported():
    projection = ConstitutionalQuestionProjection(
        bounded_question_id="manual:fixture",
        selection_keys=("governance",),
        uncertainty=("manual uncertainty",),
    )

    assert projection.bounded_question_id == "manual:fixture"
    assert projection.selection_keys == ("governance",)
    assert projection.uncertainty == ("manual uncertainty",)


def test_real_projected_question_can_be_consumed_by_existing_selection_with_explicit_capability_projection():
    projection = project_constitutional_question(_bounded())

    selected = select_constitutional_views(
        question_projection=projection,
        capability_projections=(
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_process",
                capability_keys=("process",),
            ),
        ),
    )

    assert selected.bounded_question_id == "bounded-question:projection-test"
    assert selected.selected_view_names == ("constitutional_process",)
    assert "scope supplied by caller" in selected.selection_uncertainty
    assert "unknown: capability support unknown before selection" in selected.selection_uncertainty
    assert selected.read_only is True
    assert selected.writes_event_ledger is False
    assert selected.mutates_cluster is False
