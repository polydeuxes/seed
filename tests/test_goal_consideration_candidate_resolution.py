from seed_runtime.goal_consideration_candidate_resolution import (
    GoalConsiderationCandidateTestimony,
    goal_consideration_candidate_resolution_json,
    resolve_goal_consideration_candidate,
)
from seed_runtime.goal_orientation_inventory import (
    GoalOrientationAssociation,
    build_goal_orientation_inventory,
)


def _inventory():
    return build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "bounded_goal", "goal:one", "src:g1", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "bounded_goal", "goal:two", "src:g2", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "pressure", "pressure:one", "src:p1", ("knowledge_quality",)
            ),
        ]
    )


def test_one_exact_visible_goal_identity_resolves_and_preserves_provenance():
    resolution = resolve_goal_consideration_candidate(
        _inventory(),
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:1", "closed-choice:1", "goal:one"
            )
        ],
    )

    assert resolution.resolution_state == "resolved"
    assert resolution.resolved_goal_establishment_id == "goal:one"
    assert resolution.resolved_goal_source_ref == "src:g1"
    assert resolution.candidate_testimony_refs == ("candidate-testimony:1",)
    assert resolution.candidate_source_refs == ("closed-choice:1",)
    assert resolution.inventory_candidate_set_id.startswith("goal_candidate_set:")


def test_no_candidate_is_resolved_without_attributed_testimony():
    resolution = resolve_goal_consideration_candidate(_inventory())

    assert resolution.resolution_state == "no_candidate_testimony"
    assert resolution.resolved_goal_establishment_id is None
    assert [goal.artifact_ref for goal in resolution.visible_goal_candidates] == [
        "goal:one",
        "goal:two",
    ]


def test_null_dimensions_and_pressure_records_do_not_resolve_as_goals():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "pressure", "pressure:one", "src:p1", ("resource_stewardship",)
            )
        ]
    )

    missing = resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:null",
                "operator:testimony",
                testimony_state="missing_goal_identity",
                unknowns=("Null dimension operator_interaction is not a bounded goal",),
            )
        ],
    )
    pressure = resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:pressure",
                "operator:testimony",
                "pressure:one",
            )
        ],
    )

    assert missing.resolution_state == "missing_goal_identity"
    assert missing.resolved_goal_establishment_id is None
    assert missing.missing_identity_testimony_refs == ("candidate-testimony:null",)
    assert pressure.resolution_state == "inventory_mismatch"
    assert pressure.inventory_mismatch_goal_refs == ("pressure:one",)


def test_missing_ambiguous_conflicting_and_mismatched_identities_remain_unresolved():
    inventory = _inventory()

    missing = resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:missing",
                "operator:testimony",
                testimony_state="missing_goal_identity",
            )
        ],
    )
    ambiguous = resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:ambiguous",
                "operator:testimony",
                testimony_state="ambiguous",
                candidate_goal_refs=("goal:one", "goal:two"),
            )
        ],
    )
    conflicting = resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:a", "operator:testimony", "goal:one"
            ),
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:b", "operator:testimony", "goal:two"
            ),
        ],
    )
    mismatched = resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:absent",
                "operator:testimony",
                "goal:not-visible",
            )
        ],
    )

    assert missing.resolution_state == "missing_goal_identity"
    assert ambiguous.resolution_state == "ambiguous"
    assert ambiguous.ambiguous_goal_refs == ("goal:one", "goal:two")
    assert conflicting.resolution_state == "conflict"
    assert conflicting.ambiguous_goal_refs == ("goal:one", "goal:two")
    assert mismatched.resolution_state == "inventory_mismatch"
    assert all(
        item.resolved_goal_establishment_id is None
        for item in (missing, ambiguous, conflicting, mismatched)
    )


def test_duplicate_visible_identity_is_ambiguous():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "bounded_goal", "goal:dup", "src:g1", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "bounded_goal", "goal:dup", "src:g2", ("resource_stewardship",)
            ),
        ]
    )

    resolution = resolve_goal_consideration_candidate(
        inventory,
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:dup", "operator:testimony", "goal:dup"
            )
        ],
    )

    assert resolution.resolution_state == "ambiguous"
    assert resolution.resolved_goal_establishment_id is None
    assert resolution.ambiguous_goal_refs == ("goal:dup", "goal:dup")


def test_resolution_does_not_claim_selection_focus_priority_or_movement():
    resolution = resolve_goal_consideration_candidate(
        _inventory(),
        [
            GoalConsiderationCandidateTestimony(
                "candidate-testimony:1", "closed-choice:1", "goal:one"
            )
        ],
    )
    data = goal_consideration_candidate_resolution_json(resolution)

    assert data["read_only"] is True
    assert data["selects_goal"] is False
    assert data["establishes_focus"] is False
    assert data["prioritizes"] is False
    assert data["activates_goal"] is False
    assert data["classifies_advancement_need"] is False
    assert data["requires_inquiry"] is False
    assert data["opens_inquiry"] is False
    assert data["moves_frontier"] is False
    assert data["authorizes_work"] is False
    assert data["starts_execution"] is False
    assert data["starts_recording"] is False
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False
