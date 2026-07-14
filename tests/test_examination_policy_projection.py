import copy, json, subprocess

from seed_runtime.bounded_constitutional_question import produce_bounded_constitutional_question
from seed_runtime.candidate_examination_work import *
from seed_runtime.examination_frontier import CorpusMember, WorkResultReference, project_examination_frontier
from seed_runtime.examination_method_applicability import ExaminationMethodApplicabilityTestimony, project_examination_method_applicability
from seed_runtime.examination_policy_projection import *


def q(id=None):
    return produce_bounded_constitutional_question(operator_inquiry="x",inquiry_provenance="test",bounded_question="What explicit policy governs movement through this frontier?",constitutional_intent="policy projection",scope_status="bounded",bounded_question_id=id)

def rep(kind="exact_text", rid="r", h="h", status="known"):
    return RepresentationVisibility(rid,kind,"artifact",h,"v",status)
def mem(mid="m", h="h", reps=(rep(),)):
    return BoundedCorpusMember(mid,"book","artifact",h,reps)
def contract(cid="c", need="exact_text", out="structural_projection", ver="v1", avail="available"):
    return ExaminationWorkContract(cid,"cap-"+cid,"work-"+cid,need,out,ver,avail,(),("explicit contract",))

def fixtures():
    qq=q(); workset=project_candidate_examination_work("corpus", (mem("a"), mem("b"), mem("c"), mem("d"), mem("e"), mem("f"), mem("g")), (contract("struct"),), ("contracts",))
    cids=[c.candidate_work_id for c in workset.candidate_work]
    testimony=tuple(ExaminationMethodApplicabilityTestimony("mt-"+cid, qq.bounded_question_id, candidate_work_id=cid, artifact_identity="artifact", artifact_hash="h", method_reference="mechanical", applicability="applicable", reason="explicit") for cid in cids)
    app=project_examination_method_applicability(qq, workset, testimony)
    handoff=list(app.to_frontier_candidate_work(workset))
    # Preserve multiple states in one frontier without changing ownership.
    handoff=[h.__class__(**(h.__dict__ | {"authorization_status":"authorized"})) for h in handoff]
    handoff[2]=handoff[2].__class__(**(handoff[2].__dict__ | {"blockers":("blocked",)}))
    handoff[3]=handoff[3].__class__(**(handoff[3].__dict__ | {"compatibility_status":"unsupported","authorization_status":"not_applicable","capability_id":""}))
    handoff[4]=handoff[4].__class__(**(handoff[4].__dict__ | {"deferral_testimony":("deferred",)}))
    res=WorkResultReference("r", handoff[5].corpus_member_id, "h", handoff[5].work_kind, handoff[5].capability_id, handoff[5].convention, "completed")
    handoff[5]=handoff[5].__class__(**(handoff[5].__dict__ | {"existing_results":(res,)}))
    handoff[6]=handoff[6].__class__(**(handoff[6].__dict__ | {"compatibility_status":"unknown","authorization_status":"unknown","capability_id":""}))
    f=project_examination_frontier(qq,"corpus","label", tuple(CorpusMember(x,"book","artifact","h") for x in "abcdefg"), tuple(handoff))
    return qq, workset, app, f

def rt(q, app, f, kind="explicit_work_identity", params=None, tid="rt", **kw):
    return ExaminationResolutionTestimony(tid, q.bounded_question_id, f.frontier_id, app.projection_id, kind, params or {}, **kw)

def test_deterministic_identity_ordering_and_typed_read_only_shape():
    qq, _, app, f=fixtures(); wid=next(i.work_item_id for i in f.work_items if i.classification.eligible)
    p=project_examination_policy(qq, app, f, (rt(qq,app,f,params={"work_item_id":wid}),))
    p2=project_examination_policy(qq, app, f, (rt(qq,app,f,params={"work_item_id":wid}),))
    assert p.projection_id == p2.projection_id
    assert p.in_scope_work_references == tuple(sorted(p.in_scope_work_references))
    assert p.read_only and not p.writes_event_ledger and not p.mutates_cluster
    payload=p.to_json_dict()
    assert payload["artifact_type"] == "ExaminationPolicyProjection"
    assert all(k not in payload for k in ("selected_work","selected_work_id","authorization_decision","execution_decision","priority_score"))
    assert p.to_selector_handoff().to_json_dict()["eligible_in_scope_work_ids"] == [wid]

def test_mismatched_references_unknown_or_inapplicable_and_named_work_must_exist():
    qq, _, app, f=fixtures(); wid=f.work_items[0].work_item_id
    assert project_examination_policy(qq, app, f, ()).policy_state == "unknown"
    badq=rt(qq,app,f,params={"work_item_id":wid}); badq=badq.__class__(**(badq.__dict__ | {"inquiry_reference":"other"}))
    assert project_examination_policy(qq, app, f, (badq,)).policy_state == "unknown"
    badf=rt(qq,app,f,params={"work_item_id":wid}); badf=badf.__class__(**(badf.__dict__ | {"frontier_reference":"other"}))
    assert project_examination_policy(qq, app, f, (badf,)).policy_state == "inapplicable"
    bada=rt(qq,app,f,params={"work_item_id":wid}); bada=bada.__class__(**(bada.__dict__ | {"applicability_projection_reference":"other"}))
    assert project_examination_policy(qq, app, f, (bada,)).policy_state == "inapplicable"
    missing=project_examination_policy(qq, app, f, (rt(qq,app,f,params={"work_item_id":"missing"}),))
    assert missing.policy_state == "inapplicable" and "policy_inapplicable" in missing.no_selection_conditions

def test_applicability_distinct_from_sufficiency_and_no_selection_states_block_handoff():
    qq, _, app, f=fixtures(); by={i.candidate_work_id:i for i in f.work_items}; eligible=next(i for i in f.work_items if i.classification.eligible)
    p=project_examination_policy(qq, app, f, (rt(qq,app,f,params={"work_item_id":eligible.work_item_id}),))
    assert p.policy_state == "applicable" and p.policy_sufficiency == "sufficient_for_selection"
    assert not hasattr(p, "selected_work_id")
    for item in [i for i in f.work_items if not i.classification.eligible]:
        p=project_examination_policy(qq, app, f, (rt(qq,app,f,params={"work_item_id":item.work_item_id}, tid=item.candidate_work_id),))
        assert p.policy_state == "applicable" and p.policy_sufficiency == "insufficient_for_selection"
        assert item.classification.eligible is False
    conflict=project_examination_policy(qq, app, f, (rt(qq,app,f,"explicit_work_identity",{"work_item_id":eligible.work_item_id},"a"), rt(qq,app,f,"no_selection",{},"b")))
    assert conflict.policy_state == "conflict" and conflict.policy_sufficiency == "conflict" and "policy_conflict" in conflict.no_selection_conditions
    inapp=project_examination_policy(qq, app, f, (rt(qq,app,f,params={"work_item_id":"missing"}),))
    assert inapp.policy_sufficiency != "sufficient_for_selection"

def test_all_eligible_no_order_tie_and_no_arbitrary_tiebreak():
    qq, _, app, f=fixtures()
    p=project_examination_policy(qq, app, f, (rt(qq,app,f,"all_eligible_no_order",{}, tie_treatment="require_additional_testimony"),))
    assert p.policy_state == "applicable" and p.policy_sufficiency == "insufficient_for_selection"
    assert len(p.eligible_in_scope_work_references) > 1
    assert "policy_insufficient" in p.no_selection_conditions or "policy insufficient for unique selection" in p.no_selection_conditions
    assert not any(k in p.to_json_dict() for k in ("lexical_tiebreak", "insertion_order_tiebreak", "hash_order_tiebreak"))

def test_prerequisite_first_uses_only_explicit_evidence_missing_is_unknown():
    qq, _, app, f=fixtures(); eligible=[i for i in f.work_items if i.classification.eligible][0]
    missing=project_examination_policy(qq, app, f, (rt(qq,app,f,"prerequisite_first",{}),))
    assert missing.policy_state == "unknown" and "prerequisite evidence absent" in missing.unknowns
    edge={"work_item_id":eligible.work_item_id,"depends_on_work_item_id":"declared-only"}
    p=project_examination_policy(qq, app, f, (rt(qq,app,f,"prerequisite_first",{"prerequisites":[edge]}),))
    assert p.policy_state == "applicable" and p.prerequisite_references
    assert "declared-only" in p.prerequisite_references[0]

def test_methodologically_unknown_or_inapplicable_cannot_enter_ordinary_eligible_scope():
    qq, workset, app, f=fixtures()
    # Same frontier, but method projection with no applicable candidate references.
    app_unknown=project_examination_method_applicability(qq, workset, ())
    p=project_examination_policy(qq, app_unknown, f, (rt(qq,app_unknown,f,"all_eligible_no_order",{}),))
    assert p.policy_state == "applicable"
    assert p.eligible_in_scope_work_references == ()
    assert "no eligible in-scope work" in p.no_selection_conditions

def test_rendering_read_only_non_mutation_and_boundary_notes():
    qq, _, app, f=fixtures(); before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    p=project_examination_policy(qq, app, f, (rt(qq,app,f,"no_selection",{}),))
    human=format_examination_policy_projection(p); js=json.dumps(examination_policy_projection_json(p))
    after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    assert before == after
    assert p.policy_state == "applicable" and p.policy_sufficiency == "insufficient_for_selection"
    for note in BOUNDARY_NOTES: assert note in human and note in js
    for forbidden in "pending_action probe_request authorized executed selected_work priority_score".split():
        assert forbidden not in js
    assert "Observation" not in js
    assert "policy_state" in human and "policy_sufficiency" in human and "tie_treatment" in human and "no_selection_conditions" in human

def test_candidate_frontier_and_method_outputs_unchanged_by_policy_projection():
    qq, workset, app, f=fixtures(); wc=copy.deepcopy(workset.to_json_dict()); ac=copy.deepcopy(app.to_json_dict()); fc=copy.deepcopy(f.to_json_dict())
    project_examination_policy(qq, app, f, (rt(qq,app,f,"all_eligible_no_order",{}),))
    assert workset.to_json_dict() == wc and app.to_json_dict() == ac and f.to_json_dict() == fc
    assert [c.candidate_work_id for c in workset.candidate_work] == [c.candidate_work_id for c in workset.candidate_work]
    assert [i.work_item_id for i in f.work_items] == [i.work_item_id for i in f.work_items]
