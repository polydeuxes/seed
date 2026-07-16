from seed_runtime.advancement_need_reference_set import project_advancement_need_reference_set
from seed_runtime.authority_need_projection import AuthorityNeedProjection, AuthorityNeedProjectionItem
from seed_runtime.clarification_need_projection import ClarificationNeedProjection, ClarificationNeedProjectionItem
from seed_runtime.goal_advancement_need_set import GoalAdvancementNeedSet, NeedFamilyAssemblyRecord
from seed_runtime.inquiry_need_projection import InquiryNeedProjection, InquiryNeedProjectionItem
from seed_runtime.operational_realization_need_projection import OperationalRealizationNeedProjection, OperationalRealizationNeedProjectionItem


def _clar_item(ref, component, standing, evidence="e:1"):
    return ClarificationNeedProjectionItem(ref, "src", component, "stage", standing, evidence_ref=evidence)


def _inq_item(ref, component, subject, standing, freshness="current"):
    return InquiryNeedProjectionItem(ref, "src", component, subject, "stage", standing, "e:1", freshness, "available")


def _auth_item(req, auth, component, klass, scope, standing):
    return AuthorityNeedProjectionItem(req, auth, component, klass, scope, "stage", "required", "unavailable", "applicable", "material", standing, ("e:1", "e:2"))


def _real_item(req, standing_ref, component, transformation, scope, standing):
    return OperationalRealizationNeedProjectionItem(req, standing_ref, component, transformation, scope, "stage", "required", "unavailable", "complete_for_horizon", "operational_realization", "applicable", "material", standing, ("e:1", "e:2"))


def _need_set():
    clarification = ClarificationNeedProjection(
        "proj:clar", "sel:1", "goal:1", "horizon:1", ("e:1",),
        (_clar_item("clar:same", "component:stable", "established"),),
        (_clar_item("clar:same", "component:stable", "unsupported"),),
        (_clar_item("clar:unknown", "component:unknown", "unknown"),),
        (_clar_item("clar:conflict", "component:conflict", "conflicting"),),
        (_clar_item("clar:excluded", "component:excluded", "excluded_family"),),
        (ClarificationNeedProjectionItem("clar:unclassified", "src", "component:unclassified", "stage", None, "not_material_to_horizon", "e:1"),),
    )
    inquiry = InquiryNeedProjection(
        "proj:inq", "sel:1", "goal:1", "horizon:1", ("e:1",),
        (_inq_item("inq:1", "component:shared", "subject:a", "established", "stale"),),
        (_inq_item("inq:1", "component:shared", "subject:b", "unsupported"),),
        (), (), (), (),
    )
    authority = AuthorityNeedProjection(
        "proj:auth", "sel:1", "goal:1", "horizon:1", ("e:1", "e:2"),
        (_auth_item("req:1", "auth:1", "auth-component", "class", "scope", "established"),),
        (_auth_item("req:2", "auth:2", "auth-component", "class", "scope", "unsupported"),),
        (_auth_item("req:3", "auth:3", "auth-component", "class", "scope", "unknown"),),
        (_auth_item("req:4", "auth:4", "auth-component", "class", "scope", "conflicting"),),
        (_auth_item("req:5", "auth:5", "auth-component", "class", "scope", "outside_current_scope"),),
        (AuthorityNeedProjectionItem("req:6", "", "auth-component", "class", "scope", "stage", None, None, None, None, None, ("e:1",), "not_authority_standing_component"),),
    )
    realization = OperationalRealizationNeedProjection(
        "proj:real", "sel:1", "goal:1", "horizon:1", ("e:1", "e:2"),
        (_real_item("rreq:1", "rstand:1", "real-component", "transform", "scope", "established"),),
        (_real_item("rreq:2", "rstand:2", "real-component", "transform", "scope", "unsupported"),),
        (_real_item("rreq:3", "rstand:3", "real-component", "transform", "scope", "unknown"),),
        (_real_item("rreq:4", "rstand:4", "real-component", "transform", "scope", "conflicting"),),
        (_real_item("rreq:5", "rstand:5", "real-component", "transform", "scope", "unclassified_here"),),
        (OperationalRealizationNeedProjectionItem("rreq:6", "", "real-component", "transform", "scope", "stage", None, None, None, None, None, None, None, ("e:1",), "not_standing_component"),),
    )
    return GoalAdvancementNeedSet(
        "need-set:immutable", "GoalAdvancementNeedSet", "sel:1", "goal:1", "horizon:1",
        frozenset({
            NeedFamilyAssemblyRecord("clarification", "supplied", clarification),
            NeedFamilyAssemblyRecord("inquiry", "supplied", inquiry),
            NeedFamilyAssemblyRecord("authority", "supplied", authority),
            NeedFamilyAssemblyRecord("operational_realization", "supplied", realization),
        }), (), (), (), False,
    )


def test_references_bind_to_exact_need_set_goal_horizon_family_and_projection_and_family_lineage():
    refs = project_advancement_need_reference_set(_need_set()).references
    assert refs
    for ref in refs:
        assert ref.need_set_id == "need-set:immutable"
        assert ref.selection_id == "sel:1"
        assert ref.goal_establishment_id == "goal:1"
        assert ref.horizon_id == "horizon:1"
        assert ref.native_projection_id.startswith("proj:")
        assert ref.reference_id.startswith("advancement-need-reference/need-set%3Aimmutable/")
    by_family = {ref.family: ref.native_lineage for ref in refs if ref.native_bucket == "established"}
    assert by_family["clarification"] == ("clar:same", "component:stable")
    assert by_family["inquiry"] == ("inq:1", "component:shared", "subject:a")
    assert by_family["authority"] == ("req:1", "auth:1", "auth-component", "class", "scope")
    assert by_family["operational_realization"] == ("rreq:1", "rstand:1", "real-component", "transform", "scope")


def test_standing_and_bucket_are_metadata_all_records_visible_only_established_selectable_duplicate_conflict():
    reference_set = project_advancement_need_reference_set(_need_set())
    refs = reference_set.references
    assert len(refs) == 20
    assert all(ref.visible for ref in refs)
    assert {ref.native_bucket for ref in refs} >= {"established", "unsupported", "unknown", "conflicting", "excluded_family", "outside_current_scope", "unclassified_here", "unclassified"}
    assert all(ref.selectable == (ref.native_bucket == "established" and ref.native_standing == "established") for ref in refs)
    duplicate_refs = [ref for ref in refs if ref.family == "clarification" and ref.native_lineage == ("clar:same", "component:stable")]
    assert len(duplicate_refs) == 2
    assert duplicate_refs[0].reference_id == duplicate_refs[1].reference_id
    assert {ref.native_bucket for ref in duplicate_refs} == {"established", "unsupported"}
    assert all(ref.conflict and ref.conflict_kind == "duplicate_native_lineage" for ref in duplicate_refs)
    assert reference_set.conflicts == reference_set.conflicts
    conflict = reference_set.conflicts[0]
    assert conflict.native_lineage == ("clar:same", "component:stable")
    assert not any("sha" in value.lower() or value.isdigit() for value in conflict.native_lineage)


def test_deterministic_and_read_only_without_routing_recording_or_mutation():
    need_set = _need_set()
    first = project_advancement_need_reference_set(need_set)
    second = project_advancement_need_reference_set(need_set)
    assert first == second
    assert not first.reclassifies_need
    assert not first.selects_need
    assert not first.prioritizes_needs
    assert not first.selects_route
    assert not first.requests_clarification
    assert not first.opens_inquiry
    assert not first.requests_authority
    assert not first.selects_realization
    assert not first.authorizes_work
    assert not first.starts_execution
    assert not first.starts_recording
    assert not first.writes_event_ledger
    assert not first.mutates_cluster
    assert first.read_only
