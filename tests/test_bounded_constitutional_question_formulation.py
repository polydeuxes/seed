from dataclasses import replace

import pytest

from seed_runtime.bounded_constitutional_question import (
    BoundedConstitutionalQuestion,
    BoundedConstitutionalQuestionFormulationError,
    FORMULATION_CONVENTION,
    bounded_constitutional_question_json,
    format_bounded_constitutional_question,
    formulate_bounded_constitutional_question,
)
from seed_runtime.constitutional_view_selection import project_constitutional_question
from tests.test_operator_authority_scope_binding import bind, ctx, interp
from seed_runtime.operator_authority_scope_binding import bind_operator_authority_scope


def formulate(text="What owns storage on node115?", **kw):
    projection, expression, interpretation, *_ = bind(text, **kw)
    return formulate_bounded_constitutional_question(
        expression=expression,
        interpretation=interpretation,
        binding=projection,
        handoff=projection.future_bounded_question_handoff,
    ), projection, expression, interpretation


def assert_no_downstream_material(q):
    blob = str(q.__dict__)
    for forbidden in (
        "selection_key", "question_family", "diagnostic_name", "view_name",
        "capability_name", "candidate_realization", "warrant",
        "pending_action", "execution_proposal", "Observation", "Evidence", "Fact",
        "renderer", "scanner", "packets", "root_available",
    ):
        assert forbidden not in blob


def test_permitted_binding_produces_existing_bounded_question_by_delegation_shape():
    q, binding, expression, interpretation = formulate()
    assert isinstance(q, BoundedConstitutionalQuestion)
    assert q.operator_inquiry == expression.exact_text
    assert binding.binding_projection_id in q.inquiry_provenance
    assert interpretation.interpretation_projection_id in q.inquiry_provenance
    assert q.read_only and not q.writes_event_ledger and not q.mutates_cluster
    assert_no_downstream_material(q)


def test_deterministic_identity_ordering_and_all_question_relevant_changes():
    a = formulate()[0]
    assert a.bounded_question_id == formulate()[0].bounded_question_id

    e, p, h = interp("What owns storage on node115?")
    oi1, wa1, sb1 = ctx(sources=("b", "a"))
    oi2, wa2, sb2 = ctx(sources=("a", "b"))
    b1 = bind_operator_authority_scope(p, h, e, oi1, wa1, sb1, provenance=("z", "a"))
    b2 = bind_operator_authority_scope(p, h, e, oi2, wa2, sb2, provenance=("a", "z"))
    assert formulate_bounded_constitutional_question(expression=e, interpretation=p, binding=b1).bounded_question_id == formulate_bounded_constitutional_question(expression=e, interpretation=p, binding=b2).bounded_question_id

    variants = [
        formulate("What owns storage on node115? ")[0],
        formulate("What supports storage ownership on node115?")[0],
        formulate_bounded_constitutional_question(expression=e, interpretation=p, binding=replace(b1, permitted_scope_refs=("node116",), future_bounded_question_handoff=replace(b1.future_bounded_question_handoff, bound_scope_refs=("node116",)))),
        formulate("Inspect this repository, but do not modify anything.", activity=("local_passive_observation",), scopes=("repo:/workspace/seed",), sources=("standing local passive authority",))[0],
        formulate("Show ownership on node115 as JSON.")[0],
        formulate_bounded_constitutional_question(expression=e, interpretation=p, binding=b1, formulation_convention="other_convention"),
        formulate_bounded_constitutional_question(expression=replace(e, unknowns=("new unknown",)), interpretation=p, binding=b1),
    ]
    assert all(v.bounded_question_id != a.bounded_question_id for v in variants)


def test_validation_failures_for_mismatches_and_non_permitted_states():
    q, binding, expression, interpretation = formulate()
    handoff = binding.future_bounded_question_handoff
    replacements = [
        {"authority_scope_binding_ref": "bad"},
        {"interpretation_projection_ref": "bad"},
        {"attributed_expression_ref": "bad"},
        {"operator_identity_ref": "bad"},
        {"workspace_ref": "bad"},
        {"session_ref": "bad"},
        {"inquiry_or_request_kind": "bad"},
        {"requested_activity_class": "bad"},
        {"requested_scope_expressions": ("bad",)},
        {"bound_scope_refs": ("bad",)},
        {"excluded_scope_refs": ("bad",)},
        {"operator_stated_effect_constraints": ("bad",)},
        {"presentation_preference": "YAML"},
    ]
    for kwargs in replacements:
        with pytest.raises(BoundedConstitutionalQuestionFormulationError):
            formulate_bounded_constitutional_question(expression=expression, interpretation=interpretation, binding=binding, handoff=replace(handoff, **kwargs))
    for state in ("blocked", "unknown", "conflict"):
        with pytest.raises(BoundedConstitutionalQuestionFormulationError):
            formulate_bounded_constitutional_question(expression=expression, interpretation=interpretation, binding=replace(binding, binding_state=state))


def test_read_only_ownership_inquiry_no_evidence_or_selection_and_projection_consumable():
    q, *_ = formulate("What owns storage on node115?")
    assert "identify" in q.bounded_question
    assert "ownership" in q.bounded_question
    assert "node115" in q.bounded_question
    assert q.constitutional_intent == "examine current constitutional State"
    assert "Evidence" not in str(q.__dict__)
    assert_no_downstream_material(q)
    projection = project_constitutional_question(q)
    assert projection.bounded_question_id == q.bounded_question_id


def test_explanation_support_unknowns_and_limitation_formulations():
    explain = formulate("Why can't Seed establish stronger service ownership?")[0]
    assert explain.bounded_question.startswith("explain")
    assert "limitations" in explain.bounded_question and "Unknowns" in explain.bounded_question
    assert "view_name" not in str(explain.__dict__)

    support = formulate("What supports storage ownership on node115?")[0]
    assert support.bounded_question.startswith("identify the bounded support")
    assert "Evidence" not in str(support.__dict__)

    unknowns = formulate("What is unknown about service ownership on node115?")[0]
    assert unknowns.bounded_question.startswith("identify unresolved constitutional material")

    e, p, h = interp("What owns storage on node115?")
    p = replace(p, inquiry_or_request_kind="limitations", relation_or_focus_expressions=("attribution",), unresolved_references=("unresolved referent: attribution",))
    h = replace(h, inquiry_or_request_kind="limitations")
    oi, wa, sb = ctx()
    b = bind_operator_authority_scope(p, h, e, oi, wa, sb)
    limited = formulate_bounded_constitutional_question(expression=e, interpretation=p, binding=b)
    assert "attribution" in limited.bounded_question
    assert "unresolved referent: attribution" in limited.uncertainty


def test_presentation_constraints_movement_privilege_and_partial_scope_boundaries():
    json_q, *_ = formulate("Show ownership on node115 as JSON.")
    assert "JSON" not in json_q.bounded_question
    assert ("presentation_preference", "JSON") in json_q.caller_supplied_fields
    assert_no_downstream_material(json_q)

    passive, *_ = formulate("Inspect this repository, but do not modify anything.", activity=("local_passive_observation",), scopes=("repo:/workspace/seed",), sources=("standing local passive authority",))
    assert passive.bounded_question.startswith("determine the next lawful movement")
    assert "do not modify anything" in passive.bounded_question
    assert ("operator_stated_effect_constraints", "do not modify anything") in passive.caller_supplied_fields
    assert "read_only_implementation" not in str(passive.__dict__)

    active, *_ = formulate("Run an active scan of node115 and show me JSON.", activity=("network_active_observation",))
    assert "network-active observation request" in active.bounded_question
    assert "authorize" not in active.bounded_question.lower()
    assert_no_downstream_material(active)

    e, p, h = interp("Show ownership on node115.")
    p = replace(p, requested_movement_class="privileged observation", scope_expressions=("service configuration",), authority_bearing_expressions=("Use root",))
    h = replace(h, scope_expressions=("service configuration",), authority_bearing_expressions=("Use root",))
    oi, wa, sb = ctx(activity=("local_privileged_observation",), scopes=("service-config",))
    privileged_binding = bind_operator_authority_scope(p, h, e, oi, wa, sb)
    privileged = formulate_bounded_constitutional_question(expression=e, interpretation=p, binding=privileged_binding)
    assert "privileged inspection" in privileged.bounded_question
    assert "root_available" not in str(privileged.__dict__)

    partial, binding, expression, interpretation = formulate("Show ownership on node115 as JSON.", scopes=("node115",))
    partial_handoff = replace(binding.future_bounded_question_handoff, requested_scope_expressions=("node115", "node116"), excluded_scope_refs=("node116",))
    partial_binding = replace(binding, requested_scope_expressions=("node115", "node116"), excluded_scope_refs=("node116",), future_bounded_question_handoff=partial_handoff)
    partial_q = formulate_bounded_constitutional_question(expression=expression, interpretation=interpretation, binding=partial_binding, handoff=partial_handoff)
    assert "permitted_scope=node115" in partial_q.scope_status
    assert "excluded_scope=node116" in partial_q.scope_status
    assert "node116" in dict(partial_q.caller_supplied_fields)["excluded_original_scope"]


def test_human_and_json_rendering_preserve_stable_typed_shape():
    q, *_ = formulate("What owns storage on node115?")
    human = format_bounded_constitutional_question(q)
    for expected in (q.operator_inquiry, q.bounded_question, q.constitutional_intent, q.scope_status, "uncertainty:", "unknowns:", "inquiry_provenance:", "read_only_boundaries:"):
        assert expected in human
    data = bounded_constitutional_question_json(q)
    assert data["bounded_question_id"] == q.bounded_question_id
    assert data["operator_inquiry"] == q.operator_inquiry
    assert data["bounded_question"] == q.bounded_question
    assert data["read_only"] is True and data["writes_event_ledger"] is False and data["mutates_cluster"] is False
