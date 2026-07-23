from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, NeedFamilyExclusion, establish_bounded_advancement_horizon
from seed_runtime.bounded_operator_goal_establishment import establish_bounded_operator_goal_from_closed_choice
from seed_runtime.goal_consideration_candidate_resolution import (
    GoalConsiderationCandidateTestimony,
    resolve_goal_consideration_candidate,
)
from seed_runtime.goal_orientation_inventory import association_from_bounded_goal, build_goal_orientation_inventory
from seed_runtime.inquiry_need_projection import RepositoryWorldUncertaintyTestimony, inquiry_need_projection_json, project_inquiry_need
from tests.test_bounded_operator_goal_establishment import _choice_binding


def _goal(**overrides):
    token = overrides.pop("token", "2" if overrides else "1")
    return establish_bounded_operator_goal_from_closed_choice(_choice_binding(token), stop_conditions=("stop before inquiry need",))


def _candidate_resolution(goal):
    inventory = build_goal_orientation_inventory([association_from_bounded_goal(goal, dimension_refs=("knowledge_quality",), source_ref="goal-artifact:inquiry")])
    return resolve_goal_consideration_candidate(inventory, [GoalConsiderationCandidateTestimony("focus:inquiry", "operator-focus:inquiry", goal.goal_establishment_id)])


def _horizon(candidate_resolution, goal, **overrides):
    base = dict(
        present_movement_boundary="decide whether explicit repository/world uncertainty is material before movement",
        evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:repo-world:1", "snapshot:repo-world:1"), EvidenceSnapshotReference("evidence:stale", "snapshot:stale", "stale"), EvidenceSnapshotReference("evidence:unavailable", "snapshot:unavailable", "unavailable")),
        potentially_relevant_need_families=("inquiry",),
        stale_evidence_refs=("evidence:stale",),
        unavailable_evidence_refs=("evidence:unavailable",),
    )
    base.update(overrides)
    return establish_bounded_advancement_horizon(candidate_resolution, goal, **base)


def _testimony(candidate_resolution, goal, horizon, **overrides):
    base = dict(
        testimony_ref="testimony:repo-world:1",
        source_ref="stage-testimony:inquiry",
        candidate_resolution_id=candidate_resolution.resolution_id,
        goal_establishment_id=goal.goal_establishment_id,
        horizon_id=horizon.horizon_id,
        evidence_ref="evidence:repo-world:1",
        bounded_uncertainty_component_ref="component:repository-world:1",
        repository_world_subject_ref="subject:repository:diagnostic-registry",
        owning_stage="bounded_advancement_horizon",
        standing="established",
    )
    base.update(overrides)
    return RepositoryWorldUncertaintyTestimony(**base)


def test_requires_exact_candidate_resolution_goal_horizon_component_subject_and_evidence_identity_matching():
    goal = _goal(); candidate_resolution = _candidate_resolution(goal); horizon = _horizon(candidate_resolution, goal)
    projection = project_inquiry_need(candidate_resolution, goal, horizon, [
        _testimony(candidate_resolution, goal, horizon),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="bad-candidate_resolution", candidate_resolution_id="candidate-resolution:other"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="bad-goal", goal_establishment_id="goal:other"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="bad-horizon", horizon_id="horizon:other"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="bad-evidence", evidence_ref="evidence:other"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="bad-component", bounded_uncertainty_component_ref=""),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="bad-subject", repository_world_subject_ref=""),
    ])
    assert tuple(item.testimony_ref for item in projection.established) == ("testimony:repo-world:1",)
    assert tuple(item.unclassified_reason for item in projection.unclassified) == ("candidate_resolution_identity_mismatch", "goal_identity_mismatch", "horizon_identity_mismatch", "evidence_identity_mismatch", "not_component_bounded", "missing_repository_world_subject")


def test_established_requires_repository_world_ownership_and_horizon_materiality():
    goal = _goal(); candidate_resolution = _candidate_resolution(goal); horizon = _horizon(candidate_resolution, goal)
    projection = project_inquiry_need(candidate_resolution, goal, horizon, [
        _testimony(candidate_resolution, goal, horizon),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="operator-meaning", uncertainty_family="operator_meaning"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="not-stage-owned", stage_owns_repository_world_uncertainty=False),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="not-material", material_to_present_movement_boundary=False),
    ])
    assert len(projection.established) == 1
    assert tuple(item.unclassified_reason for item in projection.unclassified) == ("not_repository_world_uncertainty", "not_stage_owned", "not_material_to_horizon")


def test_inquiry_standing_freshness_and_availability_remain_separate():
    goal = _goal(); candidate_resolution = _candidate_resolution(goal); horizon = _horizon(candidate_resolution, goal)
    projection = project_inquiry_need(candidate_resolution, goal, horizon, [
        _testimony(candidate_resolution, goal, horizon, evidence_ref="evidence:stale", evidence_freshness="stale", evidence_availability="available"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="unavailable", evidence_ref="evidence:unavailable", evidence_freshness="current", evidence_availability="unavailable"),
    ])
    assert tuple(item.standing for item in projection.established) == ("established", "established")
    assert tuple(item.evidence_freshness for item in projection.established) == ("stale", "current")
    assert tuple(item.evidence_availability for item in projection.established) == ("available", "unavailable")


def test_generic_unknown_observations_unsupported_facts_absent_artifacts_and_mixed_material_not_inferred():
    goal = _goal(unknowns=("generic Unknown",), unresolved_references=("unsupported fact",))
    candidate_resolution = _candidate_resolution(goal); horizon = _horizon(candidate_resolution, goal, unavailable_evidence_refs=("missing-artifact",))
    assert project_inquiry_need(candidate_resolution, goal, horizon, []).established == ()
    projection = project_inquiry_need(candidate_resolution, goal, horizon, [
        _testimony(candidate_resolution, goal, horizon, testimony_ref="observation", uncertainty_family="observation"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="generic-unknown", uncertainty_family="generic_unknown"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="unsupported-fact", uncertainty_family="unsupported_fact"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="absent-artifact", evidence_ref="missing-artifact"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="mixed", mixed_or_non_inquiry_component=True),
    ])
    assert projection.established == ()
    assert tuple(item.unclassified_reason for item in projection.unclassified) == ("not_repository_world_uncertainty", "not_repository_world_uncertainty", "not_repository_world_uncertainty", "evidence_identity_mismatch", "mixed_or_non_inquiry_component")


def test_clarification_authority_and_realization_components_remain_unclassified():
    goal = _goal(); candidate_resolution = _candidate_resolution(goal); horizon = _horizon(candidate_resolution, goal)
    projection = project_inquiry_need(candidate_resolution, goal, horizon, [
        _testimony(candidate_resolution, goal, horizon, testimony_ref="clarification", uncertainty_family="operator_meaning"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="authority", uncertainty_family="authority"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="realization", uncertainty_family="operational_realization"),
    ])
    assert projection.established == ()
    assert tuple(item.unclassified_reason for item in projection.unclassified) == ("not_repository_world_uncertainty", "not_repository_world_uncertainty", "not_repository_world_uncertainty")


def test_non_established_and_excluded_family_standings_are_preserved():
    goal = _goal(); candidate_resolution = _candidate_resolution(goal); horizon = _horizon(candidate_resolution, goal)
    projection = project_inquiry_need(candidate_resolution, goal, horizon, [
        _testimony(candidate_resolution, goal, horizon, testimony_ref="unsupported", standing="unsupported"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="unknown", standing="unknown"),
        _testimony(candidate_resolution, goal, horizon, testimony_ref="conflicting", standing="conflicting"),
    ])
    assert tuple(item.testimony_ref for item in projection.unsupported) == ("unsupported",)
    assert tuple(item.testimony_ref for item in projection.unknown) == ("unknown",)
    assert tuple(item.testimony_ref for item in projection.conflicting) == ("conflicting",)
    excluded_horizon = _horizon(candidate_resolution, goal, potentially_relevant_need_families=(), explicitly_excluded_need_families=(NeedFamilyExclusion("inquiry", "outside this slice"),))
    excluded = project_inquiry_need(candidate_resolution, goal, excluded_horizon, [_testimony(candidate_resolution, goal, excluded_horizon)])
    assert tuple(item.standing for item in excluded.excluded_family) == ("excluded_family",)


def test_projection_is_read_only_no_open_question_observation_action_sufficiency_execution_recording_event_or_cluster_mutation():
    goal = _goal(); candidate_resolution = _candidate_resolution(goal); horizon = _horizon(candidate_resolution, goal)
    payload = inquiry_need_projection_json(project_inquiry_need(candidate_resolution, goal, horizon, [_testimony(candidate_resolution, goal, horizon)]))
    assert payload["opens_inquiry"] is False
    assert payload["selects_question"] is False
    assert payload["authorizes_observation"] is False
    assert payload["selects_next_action"] is False
    assert payload["judges_sufficiency"] is False
    assert payload["starts_execution"] is False
    assert payload["starts_recording"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["read_only"] is True
