import copy, json, subprocess
import pytest

from seed_runtime.candidate_examination_work import ExaminationWorkContract, project_candidate_examination_work
from seed_runtime.examination_frontier import CorpusMember, project_examination_frontier
from seed_runtime.examination_method_applicability import ExaminationMethodApplicabilityTestimony, project_examination_method_applicability
from seed_runtime.examination_policy_projection import project_examination_policy
from seed_runtime.examination_probe_request import *
from seed_runtime.examination_work_selection import select_examination_work
from tests.test_examination_policy_projection import q, mem, rep, rt


def scenario(contract_id="struct", need="exact_text", out="structural_projection", hashv="h", member_id="a", method_state="applicable", extra_testimony=()):
    qq=q(); ws=project_candidate_examination_work("corpus", (mem(member_id, hashv, (rep(need, "r", hashv),)),), (ExaminationWorkContract(contract_id,"cap-"+contract_id,"work-"+contract_id,need,out,"v1","available",(),("contract-prov",)),), ("contracts",))
    c=ws.candidate_work[0]
    t=ExaminationMethodApplicabilityTestimony("mt-"+c.candidate_work_id+method_state, qq.bounded_question_id, candidate_work_id=c.candidate_work_id, artifact_identity="artifact", artifact_hash=hashv, method_reference="mechanical", applicability=method_state, reason="explicit", fidelity_constraints=("preserve artifact hash/version", "preserve exact span binding"), attribution_constraints=("preserve provider attribution",), claim_treatment_constraints=("do not promote the result to Evidence or Fact",), supporting_references=("method-doc",))
    app=project_examination_method_applicability(qq, ws, (t,)+extra_testimony)
    hand=[h.__class__(**(h.__dict__ | {"authorization_status":"authorized"})) for h in app.to_frontier_candidate_work(ws)]
    f=project_examination_frontier(qq,"corpus","label", (CorpusMember(member_id,"book","artifact",hashv),), tuple(hand))
    item=f.work_items[0]
    p=project_examination_policy(qq, app, f, (rt(qq,app,f,params={"work_item_id":item.work_item_id}),))
    s=select_examination_work(f,p,p.to_selector_handoff())
    return qq, ws, app, f, p, s, s.future_probe_request_handoff

def bind(**kw):
    qq,ws,app,f,p,s,h=scenario(**kw)
    return bind_examination_probe_request(s,h,f,ws,app), (qq,ws,app,f,p,s,h)

def test_matching_artifacts_produce_immutable_bound_request_and_handoff():
    r,_=bind()
    assert r.artifact_type == "ExaminationProbeRequest" and r.request_state == "bound"
    assert r.read_only and not r.writes_event_ledger and not r.mutates_cluster
    with pytest.raises(Exception): r.request_state = "changed"
    handoff=r.to_operational_realization_handoff().to_json_dict()
    js=json.dumps(r.to_json_dict()) + json.dumps(handoff)
    for forbidden in ("provider_choice", "selected_provider", "registered_operation", "operation_arguments", "authorization_decision", "pending_action", "execution_state", "tool_name"):
        assert forbidden not in js
    assert handoff["probe_request_id"] == r.request_id


def test_deterministic_identity_and_changed_inputs_change_identity():
    r,_=bind(); r2,_=bind(); assert r.request_id == r2.request_id
    assert bind(hashv="h2")[0].request_id != r.request_id
    assert bind(member_id="b")[0].request_id != r.request_id
    assert bind(contract_id="surface", need="structural_projection", out="surface_features")[0].request_id != r.request_id
    qq,ws,app,f,p,s,h=scenario()
    app2=app.__class__(**(app.__dict__ | {"projection_id":"changed-method"}))
    h2=h.__class__(**(h.__dict__ | {"method_constraint_reference":{"projection_id":"changed-method"}}))
    assert bind_examination_probe_request(s,h2,f,ws,app2).request_id != r.request_id


def test_surface_feature_preserves_structural_input_and_output_contract():
    r,_=bind(contract_id="surface", need="structural_projection", out="surface_feature_projection")
    assert r.required_input_representation == "structural_projection"
    assert r.requested_output_representation == "surface_feature_projection"


def test_representations_reason_constraints_and_human_json_shape():
    r,_=bind(); human=format_examination_probe_request(r); payload=examination_probe_request_json(r)
    assert r.required_input_representation == "exact_text" and r.requested_output_representation == "structural_projection"
    assert r.selection_reason == "explicit policy work identity matched one eligible item"
    assert r.fidelity_constraints == ("preserve artifact hash/version", "preserve exact span binding")
    assert r.attribution_constraints == ("preserve provider attribution",)
    assert r.claim_treatment_constraints == ("do not promote the result to Evidence or Fact",)
    assert "requested_outcome" in human and "boundary_notes" in human and "provenance" in human
    assert payload["read_only"] and payload["writes_event_ledger"] is False and payload["mutates_cluster"] is False

@pytest.mark.parametrize("mut, msg", [
    (lambda s,h,f,ws,app: (s.__class__(**(s.__dict__ | {"selection_state":"no_selection","selected_work_reference":None,"future_probe_request_handoff":None})),h,f,ws,app), "selection must contain exactly one"),
    (lambda s,h,f,ws,app: (s.__class__(**(s.__dict__ | {"selection_state":"conflict"})),h,f,ws,app), "selection must contain exactly one"),
    (lambda s,h,f,ws,app: (s,h.__class__(**(h.__dict__ | {"selection_id":"other"})),f,ws,app), "handoff does not belong"),
    (lambda s,h,f,ws,app: (s,h.__class__(**(h.__dict__ | {"frontier_reference":{"frontier_id":"other"}})),f,ws,app), "frontier"),
    (lambda s,h,f,ws,app: (s,h,f.__class__(**(f.__dict__ | {"work_items":()})),ws,app), "selected frontier work is absent"),
    (lambda s,h,f,ws,app: (s,h,f,ws.__class__(**(ws.__dict__ | {"candidate_work":()})),app), "candidate-work record is absent"),
    (lambda s,h,f,ws,app: (s,h,f.__class__(**(f.__dict__ | {"work_items":(f.work_items[0].__class__(**(f.work_items[0].__dict__ | {"candidate_work_id":"other"})),)})),ws,app), "candidate-work record is absent"),
    (lambda s,h,f,ws,app: (s,h,f.__class__(**(f.__dict__ | {"work_items":(f.work_items[0].__class__(**(f.work_items[0].__dict__ | {"artifact_hash":"other"})),)})),ws,app), "artifact identity or version mismatch"),
    (lambda s,h,f,ws,app: (s,h,f,ws.__class__(**(ws.__dict__ | {"candidate_work":(ws.candidate_work[0].__class__(**(ws.candidate_work[0].__dict__ | {"contract_id":"other"})),)})),app), "contract"),
    (lambda s,h,f,ws,app: (s,h,f.__class__(**(f.__dict__ | {"work_items":(f.work_items[0].__class__(**(f.work_items[0].__dict__ | {"capability_id":"other"})),)})),ws,app), "capability"),
    (lambda s,h,f,ws,app: (s,h,f,ws,app.__class__(**(app.__dict__ | {"candidate_applicability":()}))), "method-applicability record is absent"),
])
def test_mismatches_fail_deterministically(mut, msg):
    *_,s,h=scenario(); qq,ws,app,f,p,s,h=scenario(); args=mut(s,h,f,ws,app)
    with pytest.raises(ExaminationProbeRequestError, match=msg): bind_examination_probe_request(*args)

@pytest.mark.parametrize("state", ["inapplicable", "unknown"])
def test_non_applicable_methods_cannot_bind(state):
    r,(qq,ws,app_ok,f,p,s,h)=bind()
    c=ws.candidate_work[0]
    t=ExaminationMethodApplicabilityTestimony("mt-"+state, qq.bounded_question_id, candidate_work_id=c.candidate_work_id, artifact_identity="artifact", artifact_hash="h", method_reference="mechanical", applicability=state)
    app=project_examination_method_applicability(qq, ws, (t,))
    h2=h.__class__(**(h.__dict__ | {"method_constraint_reference":{"projection_id":app.projection_id}}))
    with pytest.raises(ExaminationProbeRequestError, match="method applicability"):
        bind_examination_probe_request(s,h2,f,ws,app)

def test_conflicting_method_applicability_cannot_bind():
    qq,ws,app,f,p,s,h=scenario()
    c=ws.candidate_work[0]
    t2=ExaminationMethodApplicabilityTestimony("conflict", qq.bounded_question_id, candidate_work_id=c.candidate_work_id, artifact_identity="artifact", artifact_hash="h", method_reference="other", applicability="inapplicable", contradicting_references=("x",))
    app_conflict=project_examination_method_applicability(qq, ws, (ExaminationMethodApplicabilityTestimony("ok", qq.bounded_question_id, candidate_work_id=c.candidate_work_id, artifact_identity="artifact", artifact_hash="h", method_reference="mechanical", applicability="applicable"), t2))
    h2=h.__class__(**(h.__dict__ | {"method_constraint_reference":{"projection_id":app_conflict.projection_id}}))
    with pytest.raises(ExaminationProbeRequestError, match="conflict|is conflict"):
        bind_examination_probe_request(s,h2,f,ws,app_conflict)

def test_read_only_no_mutation_no_external_surfaces():
    r,(qq,ws,app,f,p,s,h)=bind(); before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    originals=[copy.deepcopy(x.to_json_dict()) for x in (ws,app,f,p,s)]
    format_examination_probe_request(r); examination_probe_request_json(r); r.to_operational_realization_handoff().to_json_dict()
    after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    assert before == after
    assert [x.to_json_dict() for x in (ws,app,f,p,s)] == originals
    js=json.dumps(r.to_json_dict())
    for forbidden in ("Observation", "registry", "selected_provider", "operation_arguments", "ExecutionProposal"):
        assert forbidden not in js
