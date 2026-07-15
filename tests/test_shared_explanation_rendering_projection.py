from dataclasses import replace

import pytest

from seed_runtime.operator_authority_scope_binding import explain_minimum_lawful_advancement
from seed_runtime.representation_grammar_applicability import (
    explain_representation_grammar_applicability_advancement,
)
from seed_runtime.shared_explanation_rendering_projection import (
    format_shared_explanation_rendering,
    project_shared_explanation_rendering,
    shared_explanation_rendering_json,
)
from tests.test_operator_authority_scope_binding import bind, ctx, interp
from tests.test_representation_grammar_applicability import demand, proj
from seed_runtime.operator_authority_scope_binding import bind_operator_authority_scope


def test_projects_one_ingress_explanation_without_reinterpreting_stage_material():
    explanation = explain_minimum_lawful_advancement(
        bind(
            "Run an active scan of node115 and show me JSON.",
            restrictions=("network_active_observation_not_granted",),
        )[0]
    )

    projection = project_shared_explanation_rendering(explanation)
    rendered = format_shared_explanation_rendering(projection)
    js = shared_explanation_rendering_json(projection)

    assert projection.source_explanation_identity == explanation.explanation_id
    assert projection.source_artifact_owner == "OperatorAuthorityScopeBindingProjection"
    assert projection.source_state == "blocked"
    assert projection.source_reason == explanation.source_reason
    assert projection.preserved_unknowns == explanation.preserved_unknowns
    assert projection.preserved_conflicts == explanation.preserved_conflicts
    assert projection.prohibited_downstream_movement == explanation.prohibited_downstream_movement
    assert projection.stage_owned_material["first_missing_boundary"] == explanation.first_missing_boundary
    assert projection.stage_owned_material["authority_resolvable"] is True
    assert "authority_resolvable: true" in rendered
    assert js["stage_owned_material"]["authority_resolvable"] is True
    assert js["read_only"] is True
    assert js["writes_event_ledger"] is False
    assert js["mutates_cluster"] is False


def test_projects_one_grammar_applicability_explanation_without_authority_mapping():
    explanation = explain_representation_grammar_applicability_advancement(
        proj(d=demand(required_structures=("imperative",)))
    )

    projection = project_shared_explanation_rendering(explanation)
    rendered = format_shared_explanation_rendering(projection)
    js = shared_explanation_rendering_json(projection)

    assert projection.source_explanation_identity == explanation.explanation_id
    assert projection.source_artifact_owner == "RepresentationGrammarApplicabilityProjection"
    assert projection.source_state == "not_applicable"
    assert projection.stage_owned_material["handoff_permitted"] is False
    assert projection.stage_owned_material["authority_treatment"] == explanation.authority_treatment
    assert "handoff_permitted: false" in rendered
    assert "authority_treatment:" in rendered
    assert "authority_resolvable" not in rendered
    assert "authority_resolvable" not in str(js)
    assert js["stage_owned_material"]["established_applicability_evidence"] == list(
        explanation.established_applicability_evidence
    )


def test_state_distinction_remains_verbatim_and_is_not_generic_blocker():
    blocked = project_shared_explanation_rendering(
        explain_minimum_lawful_advancement(
            bind(
                "Run an active scan of node115 and show me JSON.",
                restrictions=("network_active_observation_not_granted",),
            )[0]
        )
    )
    not_applicable = project_shared_explanation_rendering(
        explain_representation_grammar_applicability_advancement(
            proj(d=demand(required_structures=("imperative",)))
        )
    )

    assert blocked.source_state == "blocked"
    assert not_applicable.source_state == "not_applicable"
    assert blocked.source_state != not_applicable.source_state
    assert "generic" not in format_shared_explanation_rendering(blocked).lower()
    assert "blocker" not in format_shared_explanation_rendering(not_applicable).lower()


def test_single_explanation_boundary_rejects_collections_and_preserves_no_composition():
    one = explain_representation_grammar_applicability_advancement(proj())
    two = explain_representation_grammar_applicability_advancement(
        proj(d=demand(required_structures=("imperative",)))
    )

    with pytest.raises(TypeError):
        project_shared_explanation_rendering((one, two))  # type: ignore[arg-type]

    projection = project_shared_explanation_rendering(one)
    text = format_shared_explanation_rendering(projection)
    assert "Consumes exactly one" in projection.single_explanation_boundary
    assert "compare, aggregate, order, or compose" in text
    assert not hasattr(projection, "selected_explanation")


def test_human_and_json_preserve_unknowns_conflicts_and_stage_values():
    expression, interpretation, handoff = interp("Run an active scan of node115 and show me JSON.")
    interpretation = replace(
        interpretation,
        operator_stated_effect_constraints=("do not use the network",),
    )
    identity, workspace, scope = ctx(
        activity=("network_active_observation",),
        scopes=("node115",),
        sources=("standing network authority",),
    )
    explanation = explain_minimum_lawful_advancement(
        bind_operator_authority_scope(
            interpretation,
            handoff,
            expression,
            identity,
            workspace,
            scope,
            unknowns=("ingress unknown",),
        )
    )

    projection = project_shared_explanation_rendering(explanation)
    rendered = format_shared_explanation_rendering(projection)
    js = shared_explanation_rendering_json(projection)

    assert js["source_state"] == explanation.source_state == "conflict"
    assert "source_state: conflict" in rendered
    assert js["preserved_unknowns"] == list(explanation.preserved_unknowns)
    assert "- ingress unknown" in rendered
    assert js["preserved_conflicts"] == list(explanation.preserved_conflicts)
    for conflict in explanation.preserved_conflicts:
        assert f"- {conflict}" in rendered
    assert js["stage_owned_material"]["movement_blocked"] is explanation.movement_blocked
