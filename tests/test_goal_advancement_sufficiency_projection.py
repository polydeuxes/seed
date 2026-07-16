from dataclasses import replace

from seed_runtime.advancement_need_family_coverage_set import (
    FamilyBoundedCandidateSpace,
    FamilyCoverageTestimony,
    assemble_advancement_need_family_coverage_set,
)
from seed_runtime.bounded_advancement_horizon import EvidenceSnapshotReference, NeedFamilyExclusion, establish_bounded_advancement_horizon
from seed_runtime.clarification_need_projection import ClarificationNeedProjection, ClarificationNeedProjectionItem
from seed_runtime.goal_advancement_need_set import assemble_goal_advancement_need_set
from seed_runtime.goal_advancement_sufficiency_projection import (
    goal_advancement_sufficiency_projection_json,
    project_goal_advancement_sufficiency,
)
from tests.test_clarification_need_projection import _goal, _selection
from tests.test_goal_advancement_need_set import _authority, _inquiry, _realization

FAMILIES = ("clarification", "inquiry", "authority", "operational_realization")


def _horizon(selection, goal, **overrides):
    base = dict(
        present_movement_boundary="sufficiency projection for exact selected goal and horizon",
        evidence_snapshot_refs=(EvidenceSnapshotReference("evidence:sufficiency", "snapshot:sufficiency"),),
        potentially_relevant_need_families=FAMILIES,
    )
    base.update(overrides)
    return establish_bounded_advancement_horizon(selection, goal, **base)


def _clarification(selection, goal, horizon, *, established=(), unknown=(), conflicting=()):
    return ClarificationNeedProjection(
        "projection:clarification",
        selection.selection_id,
        goal.goal_establishment_id,
        horizon.horizon_id,
        ("evidence:sufficiency",),
        established,
        (),
        unknown,
        conflicting,
        (),
        (),
    )


def _item(ref, standing="established"):
    return ClarificationNeedProjectionItem(ref, "source:test", f"component:{ref}", "clarification", standing, evidence_ref="evidence:sufficiency")


def _space(family, selection, goal, horizon):
    projection_id = "projection:realization" if family == "operational_realization" else f"projection:{family}"
    return FamilyBoundedCandidateSpace(family, f"space:{family}", selection.selection_id, goal.goal_establishment_id, horizon.horizon_id, projection_id, "snapshot:sufficiency", (f"component:{family}",))


def _testimony(family, selection, goal, horizon, *, complete=True, native_projection_id=None, **overrides):
    projection_id = native_projection_id or ("projection:realization" if family == "operational_realization" else f"projection:{family}")
    base = dict(
        family=family,
        testimony_id=f"testimony:{family}",
        selection_id=selection.selection_id,
        goal_establishment_id=goal.goal_establishment_id,
        horizon_id=horizon.horizon_id,
        native_projection_id=projection_id,
        candidate_space_id=f"space:{family}",
        evidence_snapshot_ref="snapshot:sufficiency",
        covered_component_refs=(f"component:{family}",) if complete else (),
        unexamined_component_refs=() if complete else (f"component:{family}",),
    )
    base.update(overrides)
    return FamilyCoverageTestimony(**base)


def _need_set(selection, goal, horizon, clarification=None):
    return assemble_goal_advancement_need_set(
        horizon,
        clarification=clarification if clarification is not None else _clarification(selection, goal, horizon),
        inquiry=_inquiry(selection, goal, horizon),
        authority=_authority(selection, goal, horizon),
        operational_realization=_realization(selection, goal, horizon),
    )


def _coverage_set(selection, goal, horizon, *, complete=True, families=FAMILIES, testimonies=None):
    return assemble_advancement_need_family_coverage_set(
        horizon,
        candidate_spaces=tuple(_space(f, selection, goal, horizon) for f in families),
        testimonies=tuple(testimonies) if testimonies is not None else tuple(_testimony(f, selection, goal, horizon, complete=complete) for f in families),
    )


def _reason_kinds(projection):
    return {(r.family, r.reason_kind, r.reason) for r in projection.family_reasons}


def test_exact_need_set_and_coverage_set_identity_matching_and_binding_conflict():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    other_horizon = replace(horizon, horizon_id="horizon:other")
    projection = project_goal_advancement_sufficiency(_need_set(selection, goal, horizon), _coverage_set(selection, goal, other_horizon))
    assert projection.conclusion == "conflicting"
    assert ("set", "material_conflict", "need_set_and_coverage_set_identity_mismatch") in _reason_kinds(projection)

    coverage = _coverage_set(selection, goal, horizon)
    bad_binding = replace(
        coverage,
        family_records=frozenset(
            replace(r, native_projection_id="projection:other")
            if r.family == "clarification"
            else r
            for r in coverage.family_records
        ),
    )
    projection = project_goal_advancement_sufficiency(_need_set(selection, goal, horizon), bad_binding)
    assert projection.conclusion == "conflicting"
    assert any(r.reason == "native_projection_identity_mismatch_between_need_and_coverage_sets" for r in projection.family_reasons)


def test_material_conflicts_yield_conflicting():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal, conflicts=("material horizon conflict",))
    projection = project_goal_advancement_sufficiency(_need_set(selection, goal, horizon), _coverage_set(selection, goal, horizon))
    assert projection.conclusion == "conflicting"


def test_established_unresolved_need_is_insufficient_and_unknowns_do_not_hide_it():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    clarification = _clarification(selection, goal, horizon, established=(_item("need:a"),), unknown=(_item("unknown:a", "unknown"),))
    projection = project_goal_advancement_sufficiency(_need_set(selection, goal, horizon, clarification), _coverage_set(selection, goal, horizon, complete=False))
    assert projection.conclusion == "insufficient_for_now"
    assert any(r.reason_kind == "established_unresolved_native_need" for r in projection.family_reasons)
    assert any(r.reason_kind == "unknown" for r in projection.family_reasons)


def test_incomplete_or_absent_coverage_without_established_need_is_unknown_and_not_promoted():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    projection = project_goal_advancement_sufficiency(_need_set(selection, goal, horizon), _coverage_set(selection, goal, horizon, complete=False))
    assert projection.conclusion == "unknown"
    assert projection.promotes_coverage_gap_to_native_need is False
    assert not any(r.reason_kind == "established_unresolved_native_need" for r in projection.family_reasons)


def test_complete_coverage_alone_and_no_established_need_alone_do_not_establish_sufficiency():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    absent_need_projection = assemble_goal_advancement_need_set(horizon)
    complete_coverage = _coverage_set(selection, goal, horizon)
    assert project_goal_advancement_sufficiency(absent_need_projection, complete_coverage).conclusion == "unknown"

    supplied_need_set = _need_set(selection, goal, horizon)
    partial_coverage = _coverage_set(selection, goal, horizon, complete=False)
    assert project_goal_advancement_sufficiency(supplied_need_set, partial_coverage).conclusion == "unknown"


def test_lawful_exclusions_are_neutral_only_with_explicit_non_conflicting_reasons():
    goal = _goal(); selection = _selection(goal)
    horizon = _horizon(selection, goal, explicitly_excluded_need_families=(NeedFamilyExclusion("inquiry", "outside horizon"),))
    need_set = assemble_goal_advancement_need_set(horizon, clarification=_clarification(selection, goal, horizon), authority=_authority(selection, goal, horizon), operational_realization=_realization(selection, goal, horizon))
    coverage = assemble_advancement_need_family_coverage_set(horizon, candidate_spaces=tuple(_space(f, selection, goal, horizon) for f in ("clarification", "authority", "operational_realization")), testimonies=tuple(_testimony(f, selection, goal, horizon) for f in ("clarification", "authority", "operational_realization")))
    projection = project_goal_advancement_sufficiency(need_set, coverage)
    assert projection.conclusion == "sufficient_for_now"
    assert any(r.family == "inquiry" and r.reason_kind == "lawful_exclusion" for r in projection.family_reasons)

    bad = replace(need_set, family_records=frozenset(replace(r, exclusion_reason="") if r.family == "inquiry" else r for r in need_set.family_records))
    assert project_goal_advancement_sufficiency(bad, coverage).conclusion == "unknown"


def test_multiple_established_needs_remain_unordered():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    clarification = _clarification(selection, goal, horizon, established=(_item("need:a"), _item("need:b")))
    projection = project_goal_advancement_sufficiency(_need_set(selection, goal, horizon, clarification), _coverage_set(selection, goal, horizon))
    reasons = [r for r in projection.family_reasons if r.reason_kind == "established_unresolved_native_need"]
    assert projection.conclusion == "insufficient_for_now"
    assert isinstance(projection.family_reasons, frozenset)
    assert {r.reason for r in reasons} == {"need:a", "need:b"}


def test_no_priority_routing_action_authorization_execution_recording_event_ledger_or_mutation():
    goal = _goal(); selection = _selection(goal); horizon = _horizon(selection, goal)
    payload = goal_advancement_sufficiency_projection_json(project_goal_advancement_sufficiency(_need_set(selection, goal, horizon), _coverage_set(selection, goal, horizon)))
    assert payload["ranks_needs"] is False
    assert payload["prioritizes_needs"] is False
    assert payload["selects_route"] is False
    assert payload["selects_next_action"] is False
    assert payload["opens_inquiry"] is False
    assert payload["requests_authority"] is False
    assert payload["selects_authority_source"] is False
    assert payload["selects_realization"] is False
    assert payload["authorizes_work"] is False
    assert payload["starts_execution"] is False
    assert payload["starts_recording"] is False
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False
    assert payload["read_only"] is True
