from seed_runtime.goal_orientation_inventory import (
    SUPPORTED_GOAL_DIMENSIONS,
    GoalOrientationAssociation,
    build_goal_orientation_inventory,
    goal_orientation_inventory_json,
)


def _entry(inventory, dimension):
    return next(
        entry for entry in inventory.dimensions if entry.dimension_ref == dimension
    )


def test_all_supported_dimensions_visible_and_empty_dimensions_remain_null():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                artifact_kind="pressure",
                artifact_ref="pressure:operator:1",
                source_ref="pressure-source:1",
                dimension_refs=("operator_interaction",),
            )
        ]
    )

    assert [entry.dimension_ref for entry in inventory.dimensions] == list(
        SUPPORTED_GOAL_DIMENSIONS
    )
    assert _entry(inventory, "operator_interaction").state == "Associated"
    assert _entry(inventory, "resource_stewardship").state == "Null"
    assert _entry(inventory, "resource_stewardship").pressures == ()
    assert _entry(inventory, "resource_stewardship").bounded_goals == ()
    assert _entry(inventory, "resource_stewardship").inquiry_references == ()


def test_one_dimension_may_contain_several_pressures_goals_and_inquiry_references():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "pressure", "pressure:1", "src:p1", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "pressure", "pressure:2", "src:p2", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "bounded_goal", "goal:1", "src:g1", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "bounded_goal", "goal:2", "src:g2", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "inquiry_reference", "inquiry:1", "src:i1", ("knowledge_quality",)
            ),
            GoalOrientationAssociation(
                "inquiry_reference", "inquiry:2", "src:i2", ("knowledge_quality",)
            ),
        ]
    )

    entry = _entry(inventory, "knowledge_quality")
    assert [view.artifact_ref for view in entry.pressures] == [
        "pressure:1",
        "pressure:2",
    ]
    assert [view.artifact_ref for view in entry.bounded_goals] == ["goal:1", "goal:2"]
    assert [view.artifact_ref for view in entry.inquiry_references] == [
        "inquiry:1",
        "inquiry:2",
    ]


def test_one_artifact_can_be_explicitly_associated_with_several_dimensions():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "bounded_goal",
                "goal:shared",
                "src:goal",
                ("operator_interaction", "operational_continuity"),
            )
        ]
    )

    assert (
        _entry(inventory, "operator_interaction").bounded_goals[0].artifact_ref
        == "goal:shared"
    )
    assert (
        _entry(inventory, "operational_continuity").bounded_goals[0].artifact_ref
        == "goal:shared"
    )


def test_missing_association_remains_unknown_not_inferred_from_wording():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "pressure",
                "pressure:capability-wording",
                "src:capability-prose",
                (),
                label="please recover the missing capability",
            )
        ]
    )

    assert _entry(inventory, "capability_recovery").state == "Null"
    assert [view.artifact_ref for view in inventory.unknown_association_material] == [
        "pressure:capability-wording"
    ]


def test_duplicates_preserve_source_identity():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "pressure", "pressure:dup", "src:a", ("resource_stewardship",)
            ),
            GoalOrientationAssociation(
                "pressure", "pressure:dup", "src:b", ("resource_stewardship",)
            ),
        ]
    )

    entry = _entry(inventory, "resource_stewardship")
    assert [(view.artifact_ref, view.source_ref) for view in entry.pressures] == [
        ("pressure:dup", "src:a"),
        ("pressure:dup", "src:b"),
    ]


def test_conflicts_and_unmatched_material_remain_visible():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "material",
                "material:unmatched",
                "src:u",
                ("not_a_supported_dimension",),
            ),
            GoalOrientationAssociation(
                "bounded_goal",
                "goal:conflict",
                "src:c",
                ("implementation_maintenance",),
                association_state="conflicting",
                conflict_refs=("conflict:1",),
            ),
        ]
    )

    assert [view.artifact_ref for view in inventory.unmatched_material] == [
        "material:unmatched"
    ]
    assert [view.artifact_ref for view in inventory.conflicting_material] == [
        "goal:conflict"
    ]
    assert _entry(inventory, "implementation_maintenance").bounded_goals[
        0
    ].conflict_refs == ("conflict:1",)


def test_inventory_does_not_activate_prioritize_move_authorize_execute_record_or_mutate():
    inventory = build_goal_orientation_inventory(
        [
            GoalOrientationAssociation(
                "bounded_goal", "goal:1", "src:g", ("operator_interaction",)
            )
        ]
    )
    data = goal_orientation_inventory_json(inventory)

    assert data["read_only"] is True
    assert data["activates_goals"] is False
    assert data["moves_inquiries"] is False
    assert data["prioritizes"] is False
    assert data["schedules"] is False
    assert data["authorizes_work"] is False
    assert data["starts_execution"] is False
    assert data["starts_recording"] is False
    assert data["writes_event_ledger"] is False
    assert data["mutates_cluster"] is False
