from seed_runtime.goal_inquiry_consideration_selection import (
    GoalFocusEvidence,
    goal_inquiry_consideration_selection_json,
    select_goal_for_inquiry_consideration,
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


def test_one_exact_visible_goal_can_be_selected_and_preserves_provenance():
    selection = select_goal_for_inquiry_consideration(
        _inventory(),
        [GoalFocusEvidence("focus:1", "closed-choice:1", "goal:one")],
    )

    assert selection.selection_state == "selected"
    assert selection.selected_goal_establishment_id == "goal:one"
    assert selection.selected_goal_source_ref == "src:g1"
    assert selection.focus_evidence_refs == ("focus:1",)
    assert selection.focus_provenance_refs == ("closed-choice:1",)
    assert selection.inventory_candidate_set_id.startswith("goal_candidate_set:")


def test_no_selection_occurs_without_explicit_focus_evidence_even_with_visible_goals():
    selection = select_goal_for_inquiry_consideration(_inventory())

    assert selection.selection_state == "no_focus_evidence"
    assert selection.selected_goal_establishment_id is None
    assert [goal.artifact_ref for goal in selection.non_selected_goals] == [
        "goal:one",
        "goal:two",
    ]


def test_null_dimensions_and_pressure_records_cannot_be_selected_as_goals():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "pressure", "pressure:one", "src:p1", ("resource_stewardship",)
            )
        ]
    )

    null_dimension = select_goal_for_inquiry_consideration(
        inventory,
        [
            GoalFocusEvidence(
                "focus:null-dimension",
                "operator:text",
                evidence_state="missing_goal_identity",
                unknowns=("Null dimension operator_interaction is not a bounded goal",),
            )
        ],
    )
    pressure = select_goal_for_inquiry_consideration(
        inventory,
        [GoalFocusEvidence("focus:pressure", "operator:text", "pressure:one")],
    )

    assert null_dimension.selection_state == "missing_goal_identity"
    assert null_dimension.selected_goal_establishment_id is None
    assert null_dimension.missing_identity_evidence_refs == ("focus:null-dimension",)
    assert pressure.selection_state == "inventory_mismatch"
    assert pressure.inventory_mismatch_goal_refs == ("pressure:one",)
    assert pressure.selected_goal_establishment_id is None


def test_missing_ambiguous_conflicting_and_mismatched_identities_remain_unresolved():
    inventory = _inventory()

    missing = select_goal_for_inquiry_consideration(
        inventory,
        [GoalFocusEvidence("focus:topic", "operator:text", evidence_state="missing_goal_identity")],
    )
    ambiguous = select_goal_for_inquiry_consideration(
        inventory,
        [
            GoalFocusEvidence(
                "focus:ambiguous",
                "operator:text",
                evidence_state="ambiguous",
                candidate_goal_refs=("goal:one", "goal:two"),
            )
        ],
    )
    conflicting = select_goal_for_inquiry_consideration(
        inventory,
        [
            GoalFocusEvidence("focus:a", "operator:text", "goal:one"),
            GoalFocusEvidence("focus:b", "operator:text", "goal:two"),
        ],
    )
    mismatched = select_goal_for_inquiry_consideration(
        inventory,
        [GoalFocusEvidence("focus:missing", "operator:text", "goal:not-visible")],
    )

    assert missing.selection_state == "missing_goal_identity"
    assert ambiguous.selection_state == "ambiguous"
    assert ambiguous.ambiguous_goal_refs == ("goal:one", "goal:two")
    assert conflicting.selection_state == "conflict"
    assert conflicting.ambiguous_goal_refs == ("goal:one", "goal:two")
    assert mismatched.selection_state == "inventory_mismatch"
    assert mismatched.inventory_mismatch_goal_refs == ("goal:not-visible",)
    assert all(
        item.selected_goal_establishment_id is None
        for item in (missing, ambiguous, conflicting, mismatched)
    )


def test_duplicate_visible_identity_is_ambiguous_not_selected():
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

    selection = select_goal_for_inquiry_consideration(
        inventory, [GoalFocusEvidence("focus:dup", "operator:text", "goal:dup")]
    )

    assert selection.selection_state == "ambiguous"
    assert selection.selected_goal_establishment_id is None
    assert selection.ambiguous_goal_refs == ("goal:dup", "goal:dup")


def test_all_non_selected_goals_remain_visible_and_unchanged():
    inventory = _inventory()

    selection = select_goal_for_inquiry_consideration(
        inventory,
        [GoalFocusEvidence("focus:2", "closed-choice:2", "goal:two")],
    )

    assert [goal.artifact_ref for goal in selection.non_selected_goals] == ["goal:one"]
    assert selection.non_selected_goals[0].source_ref == "src:g1"
    assert selection.non_selected_goals[0].association_state == "associated"


def test_selection_causes_no_priority_activation_inquiry_authorization_execution_recording_or_mutation():
    selection = select_goal_for_inquiry_consideration(
        _inventory(),
        [GoalFocusEvidence("focus:1", "closed-choice:1", "goal:one")],
    )
    data = goal_inquiry_consideration_selection_json(selection)

    assert data["read_only"] is True
    assert data["prioritizes"] is False
    assert data["activates_goal"] is False
    assert data["requires_inquiry"] is False
    assert data["opens_inquiry"] is False
    assert data["moves_frontier"] is False
    assert data["authorizes_work"] is False
    assert data["starts_execution"] is False
    assert data["starts_recording"] is False
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False
