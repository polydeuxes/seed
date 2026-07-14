import copy, json, subprocess
import pytest

from seed_runtime.examination_policy_projection import project_examination_policy
from seed_runtime.examination_work_selection import *
from tests.test_examination_policy_projection import fixtures, rt


def selection(kind="explicit_work_identity", item=None, **kw):
    qq, _, app, f=fixtures()
    if item is None:
        item=next(i for i in f.work_items if i.classification.eligible)
    params=kw.pop("params", {"work_item_id":item.work_item_id} if kind=="explicit_work_identity" else {})
    p=project_examination_policy(qq, app, f, (rt(qq,app,f,kind,params, **kw),))
    return qq, app, f, p, select_examination_work(f,p,p.to_selector_handoff())

def test_deterministic_identity_ordering_and_changed_inputs_change_identity():
    _,_,f,p,s=selection(); s2=select_examination_work(f,p,p.to_selector_handoff())
    assert s.selection_id == s2.selection_id
    assert [r.work_reference for r in s.non_selected_eligible_work] == sorted(r.work_reference for r in s.non_selected_eligible_work)
    qq,_,app,f2=fixtures(); f2=f2.__class__(**(f2.__dict__ | {"frontier_id":"changed"}))
    p2=p.__class__(**(p.__dict__ | {"frontier_reference":{"frontier_id":"changed","frontier_convention":f.frontier_convention}}))
    h2=p2.to_selector_handoff()
    assert select_examination_work(f2,p2,h2).selection_id != s.selection_id
    p3=p.__class__(**(p.__dict__ | {"projection_id":"changed"}))
    h3=p3.to_selector_handoff()
    assert select_examination_work(f,p3,h3).selection_id != s.selection_id

def test_mismatched_handoff_policy_frontier_fails_deterministically():
    _,_,f,p,_=selection(); h=p.to_selector_handoff()
    with pytest.raises(ExaminationWorkSelectionError, match="handoff does not reference supplied policy"):
        select_examination_work(f,p,h.__class__(**(h.__dict__ | {"policy_projection_id":"other"})))
    with pytest.raises(ExaminationWorkSelectionError, match="handoff does not reference supplied frontier"):
        select_examination_work(f,p,h.__class__(**(h.__dict__ | {"frontier_id":"other"})))
    with pytest.raises(ExaminationWorkSelectionError, match="policy does not reference supplied frontier"):
        select_examination_work(f,p.__class__(**(p.__dict__ | {"frontier_reference":{"frontier_id":"other"}})),h)

def test_policy_states_that_cannot_select():
    qq,_,app,f=fixtures(); eligible=next(i for i in f.work_items if i.classification.eligible)
    unknown=project_examination_policy(qq,app,f,())
    assert select_examination_work(f,unknown,unknown.to_selector_handoff()).selection_state == "unknown"
    conflict=project_examination_policy(qq,app,f,(rt(qq,app,f,"explicit_work_identity",{"work_item_id":eligible.work_item_id},"a"), rt(qq,app,f,"no_selection",{},"b")))
    assert select_examination_work(f,conflict,conflict.to_selector_handoff()).selection_state == "conflict"
    inapp=project_examination_policy(qq,app,f,(rt(qq,app,f,"explicit_work_identity",{"work_item_id":"missing"}),))
    assert select_examination_work(f,inapp,inapp.to_selector_handoff()).selected_work_reference is None
    multi=project_examination_policy(qq,app,f,(rt(qq,app,f,"all_eligible_no_order",{}),))
    assert select_examination_work(f,multi,multi.to_selector_handoff()).selection_state == "no_selection"

def test_explicit_work_selects_one_and_preserves_alternatives():
    _,_,f,p,s=selection()
    assert s.selection_state == "selected" and s.selected_work_reference in p.eligible_in_scope_work_references
    assert len([s.selected_work_reference]) == 1
    assert s.selection_reason == "explicit policy work identity matched one eligible item"
    all_eligible={i.work_item_id for i in f.work_items if i.classification.eligible}
    assert {r.work_reference for r in s.non_selected_eligible_work} == all_eligible - {s.selected_work_reference}
    assert all(r.non_selection_reason == "not named by explicit-work policy" for r in s.non_selected_eligible_work)
    assert s.future_probe_request_handoff and s.future_probe_request_handoff.selected_work_reference == s.selected_work_reference

def test_explicit_work_does_not_select_non_eligible_classifications():
    qq,_,app,f=fixtures()
    for pred in ("blocked","unsupported","deferred","examined","unknown","conflict"):
        items=[i for i in f.work_items if getattr(i.classification,pred)]
        if not items: continue
        p=project_examination_policy(qq,app,f,(rt(qq,app,f,"explicit_work_identity",{"work_item_id":items[0].work_item_id}, pred),))
        s=select_examination_work(f,p,p.to_selector_handoff())
        assert s.selection_state == "no_selection"
        assert s.selected_work_reference is None
        assert getattr(items[0].classification,pred) is True

def test_all_eligible_no_order_and_ties_do_not_select_arbitrary_item():
    qq,_,app,f=fixtures()
    p=project_examination_policy(qq,app,f,(rt(qq,app,f,"all_eligible_no_order",{}, tie_treatment="preserve_all_as_equally_permitted"),))
    s=select_examination_work(f,p,p.to_selector_handoff())
    assert s.selection_state == "no_selection" and s.selected_work_reference is None
    assert "lawful tie-break" in s.selection_reason
    assert "selected_work_reference" in s.to_json_dict() and s.to_json_dict()["selected_work_reference"] is None

def test_sole_eligible_selected_only_when_sufficient():
    qq,_,app,f=fixtures(); one=next(i for i in f.work_items if i.classification.eligible).work_item_id
    p=project_examination_policy(qq,app,f,(rt(qq,app,f,"all_eligible_no_order",{}, tie_treatment="preserve_all_as_equally_permitted"),))
    p=p.__class__(**(p.__dict__ | {"policy_sufficiency":"sufficient_for_selection","eligible_in_scope_work_references":(one,),"in_scope_work_references":(one,)}))
    s=select_examination_work(f,p,p.to_selector_handoff())
    assert s.selection_state == "selected" and s.selected_work_reference == one
    p_bad=p.__class__(**(p.__dict__ | {"policy_sufficiency":"insufficient_for_selection"}))
    assert select_examination_work(f,p_bad,p_bad.to_selector_handoff()).selected_work_reference is None

def test_prerequisite_first_unique_and_unresolved_ties():
    qq,_,app,f=fixtures(); elig=[i.work_item_id for i in f.work_items if i.classification.eligible]
    p=project_examination_policy(qq,app,f,(rt(qq,app,f,"prerequisite_first",{"prerequisites":[{"work_item_id":elig[1],"depends_on_work_item_id":elig[0]}]}),))
    p=p.__class__(**(p.__dict__ | {"policy_sufficiency":"sufficient_for_selection","eligible_in_scope_work_references":(elig[0],),"in_scope_work_references":(elig[0],)}))
    s=select_examination_work(f,p,p.to_selector_handoff())
    assert s.selection_state == "selected" and s.selection_reason == "one unique prerequisite-permitted item remained"
    p2=p.__class__(**(p.__dict__ | {"policy_sufficiency":"insufficient_for_selection","eligible_in_scope_work_references":tuple(elig[:2]),"in_scope_work_references":tuple(elig[:2])}))
    s2=select_examination_work(f,p2,p2.to_selector_handoff())
    assert s2.selection_state == "no_selection" and s2.selected_work_reference is None

def test_no_selection_no_eligible_and_failed_but_eligible_behavior():
    qq,_,app,f=fixtures()
    p=project_examination_policy(qq,app,f,(rt(qq,app,f,"no_selection",{}),))
    s=select_examination_work(f,p,p.to_selector_handoff())
    assert s.selection_state == "no_selection" and s.future_probe_request_handoff is None
    p2=p.__class__(**(p.__dict__ | {"policy_kind":"all_eligible_no_order","policy_state":"applicable","policy_sufficiency":"sufficient_for_selection","eligible_in_scope_work_references":(),"in_scope_work_references":()}))
    assert select_examination_work(f,p2,p2.to_selector_handoff()).selection_state == "no_selection"
    base_item=next(i for i in f.work_items if i.classification.eligible)
    mutated=base_item.__class__(**(base_item.__dict__ | {"classification": base_item.classification.__class__(**(base_item.classification.__dict__ | {"failed": True})), "failure_references": ("failed-once",)}))
    f2=f.__class__(**(f.__dict__ | {"work_items": tuple(mutated if i.work_item_id==base_item.work_item_id else i for i in f.work_items)}))
    p3=project_examination_policy(qq,app,f2,(rt(qq,app,f2,"explicit_work_identity",{"work_item_id":mutated.work_item_id}),))
    assert select_examination_work(f2,p3,p3.to_selector_handoff()).selected_work_reference == mutated.work_item_id
    p4=project_examination_policy(qq,app,f2,(rt(qq,app,f2,"all_eligible_no_order",{}),))
    assert select_examination_work(f2,p4,p4.to_selector_handoff()).selected_work_reference is None

def test_shape_read_only_no_forbidden_outputs_and_rendering_non_mutation():
    _,_,f,p,s=selection(); before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    human=format_examination_work_selection(s); payload=examination_work_selection_json(s); js=json.dumps(payload)
    after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    assert before == after
    assert payload["read_only"] and not payload["writes_event_ledger"] and not payload["mutates_cluster"]
    for forbidden in "operation_args authorization_decision execution_decision pending_action provider_request priority_score".split():
        assert forbidden not in js
    assert "selection_reason" in human and "non_selected_eligible_work" in human and "boundary_notes" in human
    assert "authorize" in human and "Non-selected alternatives" in human
    original=copy.deepcopy(f.to_json_dict()); select_examination_work(f,p,p.to_selector_handoff()); assert f.to_json_dict() == original
