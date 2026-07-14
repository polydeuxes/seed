from dataclasses import FrozenInstanceError, replace
import json, subprocess, pytest
from seed_runtime.candidate_operational_realization import *
from seed_runtime.capability_reachability_projection import *
from seed_runtime.operational_realization_selection import *
from seed_runtime.examination_probe_request import OperationalRealizationHandoff

def handoff(demand="identify repository files whose contents contain story or stories"):
 return OperationalRealizationHandoff("probe-1","inq-1","artifact-1","hash-1","work-1",demand,"text/plain","text/plain",{"projection_id":"method-1"})
def basis(b,m,contract="c",grammar="g",dep="available",auth="reachable",rep="compatible",meth="satisfies",beh=True):
 return OperationalRealizationBasis(b,m,"1",invocation_contract_ref=contract,recovered_grammar_ref=grammar,behavior_comparison_refs=(grammar,) if beh else (),availability_evidence="available",dependency_evidence=dep,authority_evidence=auth,representation_compatibility=rep,methodological_compatibility=meth)
def cand_set(n=2,demand=None, **kw):
 h=handoff(demand or "identify repository files whose contents contain story or stories")
 bases=tuple(basis(f"b{i}", f"internal:repo_search" if i==0 else f"/bin/search{i}", contract=f"c{i}", grammar=f"g{i}", **kw) for i in range(n))
 contracts=tuple(InvocationContract(f"c{i}", bases[i].mechanism_id,"text/plain","text/plain","opaque bounded process invocation" if i else "direct internal producer") for i in range(n))
 grams=tuple(RecoveredInvocationGrammar(f"g{i}", bases[i].mechanism_id,"opaque-ref",supported_structures=("literal",)) for i in range(n))
 obs=tuple(BehavioralObservation(f"o{i}", bases[i].mechanism_id,"opaque-ref","", "", 0) for i in range(n))
 comps=tuple(BehaviorComparison(f"cmp{i}", f"g{i}", f"o{i}", ("stdout",), "supported") for i in range(n))
 return project_candidate_operational_realizations(h, invocation_contracts=contracts, recovered_grammars=grams, behavioral_observations=obs, behavior_comparisons=comps, bases=bases, shared_provenance=("fixture",))
def proj(s): return project_capability_reachability(s, s.to_future_capability_reachability_handoff())
def by_mech(s): return {c.mechanism_reference:c.candidate_id for c in s.candidates}
def sel(s, policy=None):
 p=proj(s); return select_operational_realization(p,p.future_selection_handoff,s,policy)

def test_matching_immutable_deterministic_and_input_identity_changes():
 s=cand_set(1); p=proj(s); pol=OperationalRealizationSelectionPolicy.sole_supported_candidate(s.capability_demand_reference)
 a=select_operational_realization(p,p.future_selection_handoff,s,pol); b=select_operational_realization(p,p.future_selection_handoff,s,pol)
 assert a==b and a.selection_id==b.selection_id and a.selection_state=="selected"
 with pytest.raises(FrozenInstanceError): a.selection_state="x"
 assert select_operational_realization(replace(p,projection_id="changed"),replace(p.future_selection_handoff,reachability_projection_id="changed"),s,pol).selection_id != a.selection_id
 s_changed=replace(s,set_id="changed"); p_changed=replace(p,candidate_set_reference="changed"); h_changed=replace(p.future_selection_handoff,candidate_set_reference="changed")
 assert select_operational_realization(p_changed,h_changed,s_changed,pol).selection_id != a.selection_id
 assert select_operational_realization(p,p.future_selection_handoff,s,replace(pol,policy_id="changed")).selection_id != a.selection_id
 assert select_operational_realization(p,p.future_selection_handoff,s,replace(pol,policy_kind="select_none",policy_id="none")).selection_id != a.selection_id

def test_ordering_does_not_change_identity_and_selected_changes_identity():
 s=cand_set(2); p=proj(s); ids=tuple(c.candidate_id for c in s.candidates)
 a=select_operational_realization(p,p.future_selection_handoff,s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,ids[0]))
 rev=replace(s,candidates=tuple(reversed(s.candidates)))
 assert select_operational_realization(p,p.future_selection_handoff,rev,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,ids[0])).selection_id==a.selection_id
 b=select_operational_realization(p,p.future_selection_handoff,s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,ids[1]))
 assert a.selection_id != b.selection_id

def test_mismatches_and_missing_fail_deterministically():
 s=cand_set(1); p=proj(s); h=p.future_selection_handoff; pol=OperationalRealizationSelectionPolicy.sole_supported_candidate(s.capability_demand_reference)
 for bad,msg in [(replace(h,candidate_set_reference="x"),"candidate-set"),(replace(h,probe_request_reference="x"),"probe-request"),(replace(h,capability_demand_reference="x"),"capability-demand")]:
  with pytest.raises(OperationalRealizationSelectionError, match=msg): select_operational_realization(p,bad,s,pol)
 with pytest.raises(OperationalRealizationSelectionError, match="capability-demand"): select_operational_realization(p,h,s,replace(pol,capability_demand_reference="x"))
 with pytest.raises(OperationalRealizationSelectionError, match="missing referenced candidate"): select_operational_realization(replace(p,supporting_candidate_references=("missing",)),replace(h,supporting_candidate_references=("missing",)),s,pol)
 badc=s.candidates[0].__class__(**(s.candidates[0].__dict__ | {"candidate_standing":"unknown"}))
 with pytest.raises(OperationalRealizationSelectionError, match="candidate standing mismatch"): select_operational_realization(p,h,replace(s,candidates=(badc,)),pol)

def test_no_default_policy_exact_sole_none_tie_and_preservation():
 s=cand_set(2); ids=tuple(c.candidate_id for c in s.candidates)
 no=sel(s); assert no.selection_state=="no_selection" and no.selection_reason=="policy insufficient"
 one=sel(cand_set(1)); assert one.selection_state=="no_selection"
 sole=sel(cand_set(1),OperationalRealizationSelectionPolicy.sole_supported_candidate(s.capability_demand_reference)); assert sole.selection_state=="selected"
 tie=sel(s,OperationalRealizationSelectionPolicy.sole_supported_candidate(s.capability_demand_reference)); assert tie.selection_state=="no_selection" and tie.selection_reason=="unresolved_tie"
 exact=sel(s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,ids[0])); assert exact.selection_state=="selected" and exact.selected_candidate_reference==ids[0]
 assert {x.candidate_reference for x in exact.non_selected_supporting_candidates}=={ids[1]}
 assert ids[1] not in exact.unsupported_candidate_references
 none=sel(s,OperationalRealizationSelectionPolicy.select_none(s.capability_demand_reference)); assert none.selection_reason=="policy selects none"
 missing=sel(s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,"missing")); assert missing.selection_reason=="required candidate is not eligible"
 conflict=sel(s,OperationalRealizationSelectionPolicy(s.capability_demand_reference+":conf",s.capability_demand_reference,"exact_candidate",ids)); assert conflict.selection_state=="conflict"

def test_non_reachable_and_policy_cannot_override_partitions():
 cases=[cand_set(1,dep="unavailable"), cand_set(1,rep="incompatible"), project_candidate_operational_realizations(handoff()), cand_set(1,rep="conflict")]
 for s in cases:
  p=proj(s); h=p.future_selection_handoff or FutureOperationalRealizationSelectionHandoff(p.projection_id,p.probe_request_reference,p.capability_demand_reference,p.candidate_set_reference,p.reachability_state,p.supporting_candidate_references,p.blocked_candidate_references,p.unknown_candidate_references,p.conflicts,p.conclusion_reason,False)
  r=select_operational_realization(p,h,s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,(s.candidates[0].candidate_id if s.candidates else "x")))
  assert r.selection_state=="no_selection" and r.selected_candidate_reference is None and r.selection_reason=="reachability_not_reachable"

def test_exact_policy_cannot_select_non_supporting_candidates():
 for kw in ({"dep":"unavailable"},{"rep":"incompatible"}):
  s=cand_set(1,**kw); p=proj(s); ref=s.candidates[0].candidate_id
  h=p.future_selection_handoff or FutureOperationalRealizationSelectionHandoff(p.projection_id,p.probe_request_reference,p.capability_demand_reference,p.candidate_set_reference,p.reachability_state,p.supporting_candidate_references,p.blocked_candidate_references,p.unknown_candidate_references,p.conflicts,p.conclusion_reason,False)
  r=select_operational_realization(p,h,s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,ref))
  assert r.selection_state=="no_selection"

def test_constraints_use_projected_dimensions_and_do_not_recompute_or_prefer():
 s=cand_set(2); ids=tuple(c.candidate_id for c in s.candidates)
 amb=sel(s,OperationalRealizationSelectionPolicy.constraints(s.capability_demand_reference, required_representation_pair=("text/plain","text/plain")))
 assert amb.selection_state=="no_selection" and amb.selection_reason=="unresolved_tie"
 internal=sel(s,OperationalRealizationSelectionPolicy.constraints(s.capability_demand_reference, allowed_mechanism_references=("internal:repo_search",)))
 assert internal.selection_state=="selected" and by_mech(s)["internal:repo_search"]==internal.selected_candidate_reference
 external=sel(s,OperationalRealizationSelectionPolicy.constraints(s.capability_demand_reference, allowed_mechanism_references=("/bin/search1",)))
 assert external.selection_state=="selected" and by_mech(s)["/bin/search1"]==external.selected_candidate_reference
 assert "grammar_sufficiency" not in json.dumps(internal.to_json_dict())

def test_repository_bash_internal_fixtures_handoffs_and_no_forbidden_outputs():
 repo=cand_set(2); assert sel(repo).selection_state=="no_selection"; assert sel(repo,OperationalRealizationSelectionPolicy.exact_candidate(repo.capability_demand_reference,repo.candidates[0].candidate_id)).selection_state=="selected"
 bash1=cand_set(1,"produce bounded literal output through constructed Bash grammar"); bashsel=sel(bash1,OperationalRealizationSelectionPolicy.sole_supported_candidate(bash1.capability_demand_reference)); assert bashsel.selection_state=="selected"
 bash2=cand_set(2,"produce bounded literal output through constructed Bash grammar"); assert sel(bash2).selection_state=="no_selection"
 internal=sel(repo,OperationalRealizationSelectionPolicy.exact_candidate(repo.capability_demand_reference,repo.candidates[0].candidate_id)); assert "registry" not in json.dumps(internal.to_json_dict()).lower()
 assert internal.future_warrant_handoff and "warrant_conclusion" not in internal.future_warrant_handoff.to_json_dict()
 for r in (sel(repo), sel(repo,OperationalRealizationSelectionPolicy(s.capability_demand_reference if False else repo.capability_demand_reference+":c",repo.capability_demand_reference,"exact_candidate",tuple(c.candidate_id for c in repo.candidates)))):
  assert r.future_warrant_handoff is None
 js=json.dumps(internal.to_json_dict()).lower()
 for forbidden in ("echo hello","argv","stdin","cwd","environment","authorizes_now","pending_action","execution_proposal","runtime observation"):
  assert forbidden not in js

def test_rendering_json_read_only_and_no_mutation():
 s=cand_set(2); before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
 r=sel(s); human=format_operational_realization_selection(r); data=operational_realization_selection_json(r)
 after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
 assert before==after and data["read_only"] and not data["writes_event_ledger"] and not data["mutates_cluster"]
 for phrase in ("state", "selected_candidate_reference", "non_selected_supporting_candidates", "policy_unknowns", "policy_conflicts", "boundary_notes"):
  assert phrase in human
