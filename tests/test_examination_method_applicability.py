import json, subprocess

import pytest

from seed_runtime.bounded_constitutional_question import produce_bounded_constitutional_question
from seed_runtime.candidate_examination_work import *
from seed_runtime.examination_frontier import CorpusMember, project_examination_frontier
from seed_runtime.examination_method_applicability import *


def q(id=None):
    return produce_bounded_constitutional_question(operator_inquiry="x",inquiry_provenance="test",bounded_question="For each compatible work item, what method evidence applies?",constitutional_intent="method applicability",scope_status="bounded",bounded_question_id=id)

def rep(kind="exact_text", rid="r", h="h", status="known"):
    return RepresentationVisibility(rid,kind,"artifact",h,"v",status)
def mem(mid="m", h="h", reps=(rep(),)):
    return BoundedCorpusMember(mid,"book","artifact",h,reps)
def contract(cid="c", need="exact_text", out="structural_projection", ver="v1", avail="available"):
    return ExaminationWorkContract(cid,"cap-"+cid,"work-"+cid,need,out,ver,avail,(),("explicit contract",))
def ws():
    return project_candidate_examination_work("corpus", (mem("a"), mem("b", reps=(rep("structural_projection","s"),)), mem("c", reps=(rep("other"),)), mem("d")), (contract("struct"), contract("surface","structural_projection","surface_feature_projection"), contract("unavail", avail="unavailable")), ("contracts",))
def t(qid, cid, state="applicable", method="mechanical", h="h", fid=("preserve exact source identity",), att=(), claim=("do not promote output to Evidence or Fact",), refs=("testimony",)):
    return ExaminationMethodApplicabilityTestimony("t-"+cid+state, qid, candidate_work_id=cid, artifact_identity="artifact", artifact_hash=h, method_reference=method, applicability=state, reason=state+" by explicit testimony", fidelity_constraints=fid, attribution_constraints=att, claim_treatment_constraints=claim, supporting_references=refs)

def byid(p): return {r.candidate_work_id:r for r in p.candidate_applicability}

def test_deterministic_identity_ordering_and_boundary_notes():
    q1=q(); w=ws(); cids=[c.candidate_work_id for c in w.candidate_work]
    p=project_examination_method_applicability(q1,w,(t(q1.bounded_question_id,cids[0]),))
    p2=project_examination_method_applicability(q1,w,(t(q1.bounded_question_id,cids[0]),))
    assert p.projection_id == p2.projection_id
    assert [r.candidate_work_id for r in p.candidate_applicability] == sorted(r.candidate_work_id for r in p.candidate_applicability)
    assert p.read_only and not p.writes_event_ledger and not p.mutates_cluster
    human=format_examination_method_applicability(p); data=json.dumps(examination_method_applicability_json(p))
    for note in BOUNDARY_NOTES: assert note in human and note in data

def test_unknown_candidate_reference_and_mismatched_inquiry_or_version_do_not_apply():
    q1=q(); w=ws(); cid=w.candidate_work[0].candidate_work_id
    with pytest.raises(ExaminationMethodApplicabilityError, match="unknown_candidate_work_id"):
        project_examination_method_applicability(q1,w,(t(q1.bounded_question_id,"missing"),))
    r=byid(project_examination_method_applicability(q1,w,(t("other-question",cid),)))[cid]
    assert r.applicability_state == "unknown" and "mismatched inquiry reference" in r.contradicting_references[0]
    r=byid(project_examination_method_applicability(q1,w,(t(q1.bounded_question_id,cid,h="different"),)))[cid]
    assert r.applicability_state == "unknown" and "mismatched artifact version" in r.contradicting_references[0]

def test_technical_compatibility_alone_unknown_and_matching_testimony_applicable():
    q1=q(); w=ws(); cid=w.candidate_work[0].candidate_work_id
    assert w.candidate_work[0].compatibility_observation == "compatible"
    p=project_examination_method_applicability(q1,w,())
    assert byid(p)[cid].applicability_state == "unknown"
    p=project_examination_method_applicability(q1,w,(t(q1.bounded_question_id,cid),))
    r=byid(p)[cid]
    assert r.applicability_state == "applicable"
    assert "preserve exact source identity" in r.fidelity_constraints
    assert not any(hasattr(r,x) for x in "selected eligible authorized scheduled executed examined complete priority".split())

def test_conflict_inapplicable_unavailable_and_missing_representation_are_distinct():
    q1=q(); w=ws(); by={(c.compatibility_observation,c.contract_id):c for c in w.candidate_work}
    compatible=w.candidate_work[0].candidate_work_id
    unavailable=next(c for c in w.candidate_work if c.compatibility_observation=="capability_unavailable").candidate_work_id
    missing=next(c for c in w.candidate_work if c.compatibility_observation=="missing_required_representation").candidate_work_id
    p=project_examination_method_applicability(q1,w,(t(q1.bounded_question_id,compatible), t(q1.bounded_question_id,compatible,"inapplicable"), t(q1.bounded_question_id,unavailable,"inapplicable")))
    assert byid(p)[compatible].applicability_state == "conflict" and compatible in p.unknown_candidate_references
    assert byid(p)[unavailable].applicability_state == "inapplicable"
    assert next(c for c in w.candidate_work if c.candidate_work_id==unavailable).compatibility_observation == "capability_unavailable"
    assert byid(p)[missing].applicability_state == "unknown"
    assert next(c for c in w.candidate_work if c.candidate_work_id==missing).compatibility_observation == "missing_required_representation"

def test_external_method_constraints_no_authorization_and_no_priority():
    q1=q(); w=ws(); cid=w.candidate_work[0].candidate_work_id
    ext=t(q1.bounded_question_id,cid,method="external-prose-method",att=("preserve provider attribution",),fid=("preserve exact span binding", "preserve competing interpretations"),claim=("do not promote output to Fact", "provider authorization remains downstream"))
    r=byid(project_examination_method_applicability(q1,w,(ext,)))[cid]
    assert r.applicability_state == "applicable"
    assert "preserve provider attribution" in r.attribution_constraints
    assert "provider authorization remains downstream" in r.claim_treatment_constraints
    assert not hasattr(r,"priority") and not hasattr(r,"authorized")

def test_frontier_handoff_only_applicable_compatible_candidates_and_preserves_alternatives():
    q1=q(); w=ws(); cids=[c.candidate_work_id for c in w.candidate_work]
    compatible=next(c for c in w.candidate_work if c.compatibility_observation=="compatible")
    missing=next(c for c in w.candidate_work if c.compatibility_observation=="missing_required_representation")
    p=project_examination_method_applicability(q1,w,(t(q1.bounded_question_id,compatible.candidate_work_id), t(q1.bounded_question_id,missing.candidate_work_id,"inapplicable")))
    handoff=p.to_frontier_candidate_work(w)
    assert [h.candidate_work_id for h in handoff] == [compatible.candidate_work_id]
    assert missing.candidate_work_id in p.inapplicable_candidate_references
    f=project_examination_frontier(q1,"corpus","label",(CorpusMember("a","book","artifact","h"), CorpusMember("b","book","artifact","h"), CorpusMember("c","book","artifact","h"), CorpusMember("d","book","artifact","h")),handoff)
    assert f.work_items[0].candidate_work_id == compatible.candidate_work_id
    assert f.summary_counts["unknown"] == 1  # frontier ownership still handles authorization unknown


def test_projection_and_rendering_are_read_only_no_events_actions_tools_or_facts():
    before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    q1=q(); w=ws(); p=project_examination_method_applicability(q1,w,())
    _=format_examination_method_applicability(p); blob=json.dumps(p.to_json_dict())
    after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
    assert before == after
    forbidden="event_ledger_entry pending_action tool_invocation provider_invocation observation_id runtime_fact_id state_mutation frontier_mutation selected_work".split()
    assert not any(x in blob.lower() for x in forbidden)
