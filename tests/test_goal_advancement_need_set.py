from dataclasses import replace

from seed_runtime.authority_need_projection import AuthorityNeedProjection
from seed_runtime.bounded_advancement_horizon import (
    EvidenceSnapshotReference,
    NeedFamilyExclusion,
    establish_bounded_advancement_horizon,
)
from seed_runtime.clarification_need_projection import ClarificationNeedProjection
from seed_runtime.goal_advancement_need_set import (
    assemble_goal_advancement_need_set,
    goal_advancement_need_set_json,
)
from seed_runtime.inquiry_need_projection import InquiryNeedProjection
from seed_runtime.operational_realization_need_projection import (
    OperationalRealizationNeedProjection,
)
from tests.test_clarification_need_projection import _goal, _selection


def _horizon(selection, goal, **overrides):
    base = dict(
        present_movement_boundary="assemble preserved need families for this selected goal only",
        evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:need-set", "snapshot:need-set"),),
        potentially_relevant_need_families=(
            "clarification",
            "inquiry",
            "authority",
            "operational_realization",
        ),
        unknowns=("horizon unknown preserved",),
        conflicts=("horizon conflict preserved",),
    )
    base.update(overrides)
    return establish_bounded_advancement_horizon(selection, goal, **base)


def _clarification(selection, goal, horizon):
    return ClarificationNeedProjection(
        "projection:clarification",
        selection.selection_id,
        goal.goal_establishment_id,
        horizon.horizon_id,
        ("evidence:need-set",),
        (),
        (),
        (),
        (),
        (),
        (),
    )


def _inquiry(selection, goal, horizon):
    return InquiryNeedProjection(
        "projection:inquiry",
        selection.selection_id,
        goal.goal_establishment_id,
        horizon.horizon_id,
        ("evidence:need-set",),
        (),
        (),
        (),
        (),
        (),
        (),
    )


def _authority(selection, goal, horizon):
    return AuthorityNeedProjection(
        "projection:authority",
        selection.selection_id,
        goal.goal_establishment_id,
        horizon.horizon_id,
        ("evidence:need-set",),
        (),
        (),
        (),
        (),
        (),
        (),
    )


def _realization(selection, goal, horizon):
    return OperationalRealizationNeedProjection(
        "projection:realization",
        selection.selection_id,
        goal.goal_establishment_id,
        horizon.horizon_id,
        ("evidence:need-set",),
        (),
        (),
        (),
        (),
        (),
        (),
    )


def _records(need_set):
    return {record.family: record for record in need_set.family_records}


def test_requires_exact_selected_goal_and_horizon_identity_and_preserves_conflict_without_repair():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    mismatched = replace(
        _clarification(selection, goal, horizon),
        selection_id="selection:other",
        goal_establishment_id="goal:other",
        horizon_id="horizon:other",
    )

    need_set = assemble_goal_advancement_need_set(horizon, clarification=mismatched)
    record = _records(need_set)["clarification"]

    assert record.disposition == "supplied"
    assert record.projection is mismatched
    assert tuple(conflict.conflict_kind for conflict in record.identity_conflicts) == (
        "selection_identity_mismatch",
        "goal_identity_mismatch",
        "horizon_identity_mismatch",
    )
    assert record.projection.selection_id == "selection:other"


def test_can_refuse_mismatched_projection_without_repairing_it():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    mismatched = replace(_inquiry(selection, goal, horizon), horizon_id="horizon:other")

    need_set = assemble_goal_advancement_need_set(
        horizon, inquiry=mismatched, refuse_mismatched_projection=True
    )
    record = _records(need_set)["inquiry"]

    assert record.disposition == "absent"
    assert record.projection is None
    assert tuple(conflict.actual for conflict in record.identity_conflicts) == (
        "horizon:other",
    )


def test_preserves_all_four_native_projection_types_without_reinterpretation():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)
    clarification = _clarification(selection, goal, horizon)
    inquiry = _inquiry(selection, goal, horizon)
    authority = _authority(selection, goal, horizon)
    realization = _realization(selection, goal, horizon)

    need_set = assemble_goal_advancement_need_set(
        horizon,
        clarification=clarification,
        inquiry=inquiry,
        authority=authority,
        operational_realization=realization,
    )
    records = _records(need_set)

    assert records["clarification"].projection is clarification
    assert records["inquiry"].projection is inquiry
    assert records["authority"].projection is authority
    assert records["operational_realization"].projection is realization
    assert isinstance(records["clarification"].projection, ClarificationNeedProjection)
    assert isinstance(records["inquiry"].projection, InquiryNeedProjection)
    assert isinstance(records["authority"].projection, AuthorityNeedProjection)
    assert isinstance(
        records["operational_realization"].projection,
        OperationalRealizationNeedProjection,
    )


def test_coexisting_needs_are_unordered_records_not_priority_or_blocker():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(selection, goal)

    need_set = assemble_goal_advancement_need_set(
        horizon,
        clarification=_clarification(selection, goal, horizon),
        authority=_authority(selection, goal, horizon),
    )

    assert isinstance(need_set.family_records, frozenset)
    assert {record.family for record in need_set.family_records if record.disposition == "supplied"} == {
        "clarification",
        "authority",
    }
    assert need_set.orders_needs is False
    assert need_set.prioritizes_needs is False
    assert need_set.declares_overall_blocker is False
    assert need_set.selects_next_action is False


def test_supplied_absent_and_excluded_families_remain_distinct():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(
        selection,
        goal,
        potentially_relevant_need_families=("clarification", "authority"),
        explicitly_excluded_need_families=(
            NeedFamilyExclusion("inquiry", "operator excluded repository inquiry"),
        ),
    )

    need_set = assemble_goal_advancement_need_set(
        horizon, clarification=_clarification(selection, goal, horizon)
    )
    records = _records(need_set)

    assert records["clarification"].disposition == "supplied"
    assert records["inquiry"].disposition == "excluded"
    assert records["inquiry"].exclusion_reason == "operator excluded repository inquiry"
    assert records["authority"].disposition == "absent"
    assert records["operational_realization"].disposition == "absent"


def test_preserves_horizon_unknowns_conflicts_exclusions_and_is_read_only_non_mutating():
    goal = _goal()
    selection = _selection(goal)
    horizon = _horizon(
        selection,
        goal,
        explicitly_excluded_need_families=(
            NeedFamilyExclusion("authority", "no authority movement in this horizon"),
        ),
    )

    need_set = assemble_goal_advancement_need_set(horizon)
    payload = goal_advancement_need_set_json(need_set)

    assert payload["horizon_unknowns"] == ("horizon unknown preserved",)
    assert payload["horizon_conflicts"] == ("horizon conflict preserved",)
    assert payload["horizon_exclusions"] == (
        "authority: no authority movement in this horizon",
    )
    assert payload["classifies_need"] is False
    assert payload["declares_overall_blocker"] is False
    assert payload["selects_route"] is False
    assert payload["selects_next_action"] is False
    assert payload["judges_sufficiency"] is False
    assert payload["sufficient_for_now"] is None
    assert payload["opens_inquiry"] is False
    assert payload["requests_authority"] is False
    assert payload["selects_realization"] is False
    assert payload["authorizes_work"] is False
    assert payload["starts_execution"] is False
    assert payload["starts_recording"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["read_only"] is True
