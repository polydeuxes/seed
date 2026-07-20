from seed_runtime.bounded_advancement_horizon import (
    EvidenceSnapshotReference,
    NeedFamilyExclusion,
    establish_bounded_advancement_horizon,
)
from seed_runtime.bounded_operator_goal_establishment import (
    establish_bounded_operator_goal_from_interpretation,
)
from seed_runtime.clarification_need_projection import (
    OperatorMeaningUncertaintyTestimony,
    clarification_need_projection_json,
    project_clarification_need,
)
from seed_runtime.goal_consideration_candidate_resolution import (
    GoalConsiderationCandidateTestimony,
    resolve_goal_consideration_candidate,
)
from seed_runtime.goal_orientation_inventory import (
    association_from_bounded_goal,
    build_goal_orientation_inventory,
)
from tests.test_bounded_operator_goal_establishment import _interpretation


def _goal(**overrides):
    return establish_bounded_operator_goal_from_interpretation(
        _interpretation(**overrides), stop_conditions=("stop before clarification",)
    )


def _candidate_resolution(goal):
    inventory = build_goal_orientation_inventory(
        [
            association_from_bounded_goal(
                goal,
                dimension_refs=("knowledge_quality",),
                source_ref="goal-artifact:clarification",
            )
        ]
    )
    return resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "focus:clarification",
                "operator-focus:clarification",
                goal.goal_establishment_id,
            )
        ],
    )


def _horizon(candidate_resolution, goal, **overrides):
    base = dict(
        present_movement_boundary="decide whether explicit operator-meaning uncertainty is material before movement",
        evidence_snapshot_refs=(
            EvidenceSnapshotReference("evidence:meaning:1", "snapshot:meaning:1"),
        ),
        potentially_relevant_need_families=("clarification",),
    )
    base.update(overrides)
    return establish_bounded_advancement_horizon(candidate_resolution, goal, **base)


def _testimony(candidate_resolution, goal, horizon, **overrides):
    base = dict(
        testimony_ref="testimony:meaning:1",
        source_ref="stage-testimony:clarification",
        candidate_resolution_id=candidate_resolution.resolution_id,
        goal_establishment_id=goal.goal_establishment_id,
        horizon_id=horizon.horizon_id,
        evidence_ref="evidence:meaning:1",
        bounded_uncertainty_component_ref="component:operator-meaning:1",
        owning_stage="goal_inquiry_consideration",
        standing="established",
    )
    base.update(overrides)
    return OperatorMeaningUncertaintyTestimony(**base)


def test_projection_requires_exact_candidate_resolution_goal_horizon_and_evidence_identity_matching():
    goal = _goal()
    candidate_resolution = _candidate_resolution(goal)
    horizon = _horizon(candidate_resolution, goal)

    projection = project_clarification_need(
        candidate_resolution,
        goal,
        horizon,
        [
            _testimony(candidate_resolution, goal, horizon),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="bad-candidate_resolution",
                candidate_resolution_id="candidate-resolution:other",
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="bad-goal",
                goal_establishment_id="goal:other",
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="bad-horizon",
                horizon_id="horizon:other",
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="bad-evidence",
                evidence_ref="evidence:other",
            ),
        ],
    )

    assert tuple(item.testimony_ref for item in projection.established) == (
        "testimony:meaning:1",
    )
    assert tuple(item.unclassified_reason for item in projection.unclassified) == (
        "candidate_resolution_identity_mismatch",
        "goal_identity_mismatch",
        "horizon_identity_mismatch",
        "evidence_identity_mismatch",
    )


def test_established_requires_operator_meaning_stage_ownership_component_bound_and_materiality():
    goal = _goal()
    candidate_resolution = _candidate_resolution(goal)
    horizon = _horizon(candidate_resolution, goal)

    projection = project_clarification_need(
        candidate_resolution,
        goal,
        horizon,
        [
            _testimony(candidate_resolution, goal, horizon),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="repo-uncertainty",
                uncertainty_family="repository_state",
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="family-hint",
                stage_owns_operator_meaning=False,
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="generic-ambiguity",
                component_bounded=False,
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="not-material",
                material_to_present_movement_boundary=False,
            ),
        ],
    )

    assert len(projection.established) == 1
    assert tuple(item.unclassified_reason for item in projection.unclassified) == (
        "not_operator_meaning_uncertainty",
        "not_stage_owned",
        "not_component_bounded",
        "not_material_to_horizon",
    )


def test_generic_ambiguity_and_unresolved_goal_fields_are_not_inferred_as_clarification_need():
    goal = _goal(
        unresolved_references=("what is enough is unresolved",),
        unresolved_lexical_bindings=("ambiguous wording",),
    )
    candidate_resolution = _candidate_resolution(goal)
    horizon = _horizon(candidate_resolution, goal)

    projection = project_clarification_need(candidate_resolution, goal, horizon, [])

    assert projection.established == ()
    assert projection.unclassified == ()
    assert projection.requests_clarification is False


def test_mixed_or_non_clarification_components_remain_unclassified():
    goal = _goal()
    candidate_resolution = _candidate_resolution(goal)
    horizon = _horizon(candidate_resolution, goal)

    projection = project_clarification_need(
        candidate_resolution,
        goal,
        horizon,
        [
            _testimony(
                candidate_resolution, goal, horizon, mixed_or_non_clarification_component=True
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="authority-gap",
                uncertainty_family="authority",
            ),
        ],
    )

    assert projection.established == ()
    assert tuple(item.unclassified_reason for item in projection.unclassified) == (
        "mixed_or_non_clarification_component",
        "not_operator_meaning_uncertainty",
    )


def test_non_established_standings_are_preserved_and_excluded_family_overrides_classification():
    goal = _goal()
    candidate_resolution = _candidate_resolution(goal)
    horizon = _horizon(candidate_resolution, goal)

    projection = project_clarification_need(
        candidate_resolution,
        goal,
        horizon,
        [
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="unsupported",
                standing="unsupported",
            ),
            _testimony(
                candidate_resolution, goal, horizon, testimony_ref="unknown", standing="unknown"
            ),
            _testimony(
                candidate_resolution,
                goal,
                horizon,
                testimony_ref="conflicting",
                standing="conflicting",
            ),
        ],
    )

    assert tuple(item.testimony_ref for item in projection.unsupported) == (
        "unsupported",
    )
    assert tuple(item.testimony_ref for item in projection.unknown) == ("unknown",)
    assert tuple(item.testimony_ref for item in projection.conflicting) == (
        "conflicting",
    )

    excluded_horizon = _horizon(
        candidate_resolution,
        goal,
        potentially_relevant_need_families=(),
        explicitly_excluded_need_families=(
            NeedFamilyExclusion("clarification", "outside this slice"),
        ),
    )
    excluded = project_clarification_need(
        candidate_resolution,
        goal,
        excluded_horizon,
        [_testimony(candidate_resolution, goal, excluded_horizon)],
    )
    assert tuple(item.standing for item in excluded.excluded_family) == (
        "excluded_family",
    )


def test_projection_is_read_only_and_does_not_request_open_act_authorize_execute_record_or_mutate():
    goal = _goal()
    candidate_resolution = _candidate_resolution(goal)
    horizon = _horizon(candidate_resolution, goal)

    projection = project_clarification_need(
        candidate_resolution, goal, horizon, [_testimony(candidate_resolution, goal, horizon)]
    )
    payload = clarification_need_projection_json(projection)

    assert payload["requests_clarification"] is False
    assert payload["selects_question_wording"] is False
    assert payload["opens_inquiry"] is False
    assert payload["selects_next_action"] is False
    assert payload["authorizes_work"] is False
    assert payload["starts_execution"] is False
    assert payload["starts_recording"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["read_only"] is True
