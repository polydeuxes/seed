from seed_runtime.advancement_need_consideration_selection import (
    AdvancementNeedConsiderationEvidence,
    NeedFocusEvidence,
    advancement_need_consideration_selection_json,
    select_advancement_need_for_consideration,
)
from seed_runtime.advancement_need_reference_set import project_advancement_need_reference_set
from tests.test_advancement_need_reference_set import _need_set


def _reference_set():
    return project_advancement_need_reference_set(_need_set())


def _established_inquiry_ref(reference_set=None):
    reference_set = reference_set or _reference_set()
    return next(ref for ref in reference_set.references if ref.family == "inquiry" and ref.native_bucket == "established")


def _focus(ref, *, evidence_ref="focus:1", **overrides):
    data = dict(
        evidence_ref=evidence_ref,
        source_ref="operator:focus",
        reference_id=ref.reference_id,
        need_set_id=ref.need_set_id,
        selection_id=ref.selection_id,
        goal_establishment_id=ref.goal_establishment_id,
        horizon_id=ref.horizon_id,
        family=ref.family,
        native_projection_id=ref.native_projection_id,
        native_lineage=ref.native_lineage,
    )
    data.update(overrides)
    return AdvancementNeedConsiderationEvidence(**data)


def test_canonical_evidence_drives_selector_and_serialized_output_remains_stable():
    reference_set = _reference_set()
    ref = _established_inquiry_ref(reference_set)

    selection = select_advancement_need_for_consideration(reference_set, [_focus(ref)])
    payload = advancement_need_consideration_selection_json(selection)

    assert selection.selection_state == "selected"
    assert selection.selected_reference == ref
    assert payload["focus_evidence_refs"] == ("focus:1",)
    assert payload["focus_provenance_refs"] == ("operator:focus",)
    assert "consideration_evidence_refs" not in payload
    assert "consideration_provenance_refs" not in payload


def test_compatibility_alias_constructs_the_same_evidence_artifact_and_selector_result():
    reference_set = _reference_set()
    ref = _established_inquiry_ref(reference_set)
    data = dict(
        evidence_ref="focus:alias",
        source_ref="operator:focus",
        reference_id=ref.reference_id,
        need_set_id=ref.need_set_id,
        selection_id=ref.selection_id,
        goal_establishment_id=ref.goal_establishment_id,
        horizon_id=ref.horizon_id,
        family=ref.family,
        native_projection_id=ref.native_projection_id,
        native_lineage=ref.native_lineage,
    )

    canonical = AdvancementNeedConsiderationEvidence(**data)
    compatibility = NeedFocusEvidence(**data)
    canonical_selection = select_advancement_need_for_consideration(reference_set, [canonical])
    compatibility_selection = select_advancement_need_for_consideration(reference_set, [compatibility])

    assert NeedFocusEvidence is AdvancementNeedConsiderationEvidence
    assert compatibility == canonical
    assert compatibility_selection == canonical_selection
    assert advancement_need_consideration_selection_json(compatibility_selection) == advancement_need_consideration_selection_json(canonical_selection)


def test_exact_reference_selection_validates_full_identity_and_preserves_others_visible_unchanged():
    reference_set = _reference_set()
    ref = _established_inquiry_ref(reference_set)

    selection = select_advancement_need_for_consideration(reference_set, [_focus(ref)])

    assert selection.selection_state == "selected"
    assert selection.selected_reference == ref
    assert selection.selected_reference.need_set_id == reference_set.need_set_id
    assert selection.selected_reference.selection_id == reference_set.selection_id
    assert selection.selected_reference.goal_establishment_id == reference_set.goal_establishment_id
    assert selection.selected_reference.horizon_id == reference_set.horizon_id
    assert selection.selected_reference.family == "inquiry"
    assert selection.selected_reference.native_projection_id == ref.native_projection_id
    assert selection.selected_reference.native_lineage == ref.native_lineage
    assert selection.visible_references == reference_set.references
    assert tuple(sorted((r.reference_id, r.native_bucket, r.selectable) for r in selection.non_selected_references)) == tuple(sorted((r.reference_id, r.native_bucket, r.selectable) for r in reference_set.references if r != ref))


def test_unsupported_unknown_conflicting_excluded_outside_scope_and_unclassified_remain_visible_non_selectable():
    reference_set = _reference_set()
    non_selectable_buckets = {"unsupported", "unknown", "conflicting", "excluded_family", "outside_current_scope", "unclassified_here", "unclassified"}
    refs = [ref for ref in reference_set.references if ref.native_bucket in non_selectable_buckets]
    assert refs
    for ref in refs:
        selection = select_advancement_need_for_consideration(reference_set, [_focus(ref, evidence_ref=f"focus:{ref.native_bucket}:{ref.reference_id}")])
        assert ref in selection.visible_references
        assert not ref.selectable
        assert selection.selection_state in {"non_selectable", "duplicate_lineage_conflict"}
        assert selection.selected_reference is None


def test_missing_ambiguous_conflicting_absent_duplicate_lineage_and_mismatched_focus_unresolved():
    reference_set = _reference_set()
    ref = _established_inquiry_ref(reference_set)
    duplicate_ref = next(r for r in reference_set.references if r.conflict)

    missing = select_advancement_need_for_consideration(reference_set, [])
    missing_identity = select_advancement_need_for_consideration(reference_set, [AdvancementNeedConsiderationEvidence("focus:missing", "src", evidence_state="missing_identity")])
    ambiguous = select_advancement_need_for_consideration(reference_set, [AdvancementNeedConsiderationEvidence("focus:amb", "src", evidence_state="ambiguous", candidate_reference_ids=(ref.reference_id, duplicate_ref.reference_id))])
    conflicting = select_advancement_need_for_consideration(reference_set, [_focus(ref), _focus(duplicate_ref, evidence_ref="focus:2")])
    absent = select_advancement_need_for_consideration(reference_set, [_focus(ref, reference_id="advancement-need-reference/absent")])
    duplicate = select_advancement_need_for_consideration(reference_set, [_focus(duplicate_ref)])

    for field, value in [
        ("need_set_id", "other-need-set"),
        ("selection_id", "other-selection"),
        ("goal_establishment_id", "other-goal"),
        ("horizon_id", "other-horizon"),
        ("family", "authority"),
        ("native_projection_id", "other-projection"),
        ("native_lineage", ("other-lineage",)),
    ]:
        mismatch = select_advancement_need_for_consideration(reference_set, [_focus(ref, **{field: value})])
        assert mismatch.selection_state == "reference_mismatch"
        assert mismatch.selected_reference is None

    assert missing.selection_state == "no_focus_evidence"
    assert missing_identity.selection_state == "missing_identity"
    assert ambiguous.selection_state == "ambiguous"
    assert conflicting.selection_state == "conflict"
    assert absent.selection_state == "absent_reference"
    assert duplicate.selection_state == "duplicate_lineage_conflict"
    assert all(item.selected_reference is None for item in (missing, missing_identity, ambiguous, conflicting, absent, duplicate))


def test_uniqueness_and_sufficiency_do_not_select_and_boundary_has_no_side_effects():
    reference_set = _reference_set()
    selection = select_advancement_need_for_consideration(reference_set, [])

    assert selection.selection_state == "no_focus_evidence"
    assert selection.selected_reference is None
    assert any(ref.selectable for ref in selection.visible_references)
    assert not selection.selects_need
    assert not selection.prioritizes_needs
    assert not selection.declares_primary_blocker
    assert not selection.selects_resolution
    assert not selection.selects_next_action
    assert not selection.opens_inquiry
    assert not selection.requests_authority
    assert not selection.selects_realization
    assert not selection.authorizes_work
    assert not selection.starts_execution
    assert not selection.starts_recording
    assert not selection.writes_event_ledger
    assert not selection.mutates_cluster
    assert selection.read_only
