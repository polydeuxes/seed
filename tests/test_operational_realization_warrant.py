from dataclasses import FrozenInstanceError, replace
import json, subprocess, pytest
from seed_runtime.candidate_operational_realization import *
from seed_runtime.capability_reachability_projection import *
from seed_runtime.operational_realization_selection import *
from seed_runtime.operational_realization_warrant import *
from seed_runtime.examination_probe_request import OperationalRealizationHandoff

def handoff(demand="identify repository files whose contents contain story or stories"):
 return OperationalRealizationHandoff("probe-1","inq-1","artifact-1","hash-1","work-1",demand,"text/plain","text/plain",{"projection_id":"method-1"})
def basis(b,m,contract="c",grammar="g",dep="available",auth="reachable",rep="compatible",meth="satisfies",beh=True,prov=("source:fixture",)):
 return OperationalRealizationBasis(b,m,"1",invocation_contract_ref=contract,recovered_grammar_ref=grammar,behavior_comparison_refs=(grammar,) if beh else (),availability_evidence="available",dependency_evidence=dep,authority_evidence=auth,representation_compatibility=rep,methodological_compatibility=meth,provenance=prov)
def cand_set(n=1,demand=None, *, mech0="internal:repo_search", grammar_fragment="bounded lexical alternatives story stories", excluded=(), **kw):
 h=handoff(demand or "identify repository files whose contents contain story or stories")
 bases=tuple(basis(f"b{i}", mech0 if i==0 else f"/bin/search{i}", contract=f"c{i}", grammar=f"g{i}", **kw) for i in range(n))
 contracts=tuple(InvocationContract(f"c{i}", bases[i].mechanism_id,"text/plain","text/plain","direct internal producer" if i==0 and bases[i].mechanism_id.startswith("internal:") else "bounded process request/result contract",provenance=("contract-src",)) for i in range(n))
 grams=tuple(RecoveredInvocationGrammar(f"g{i}", bases[i].mechanism_id,grammar_fragment,supported_structures=("literal",),excluded_structures=excluded,provenance=("grammar-src",)) for i in range(n))
 obs=tuple(BehavioralObservation(f"o{i}", bases[i].mechanism_id,"opaque-preserved-input","", "", 0, provenance=("obs-src",)) for i in range(n))
 comps=tuple(BehaviorComparison(f"cmp{i}", f"g{i}", f"o{i}", ("stdout","result-representation"), "supported", provenance=("cmp-src",)) for i in range(n))
 return project_candidate_operational_realizations(h, invocation_contracts=contracts, recovered_grammars=grams, behavioral_observations=obs, behavior_comparisons=comps, bases=bases, shared_provenance=("fixture",))
def proj(s): return project_capability_reachability(s,s.to_future_capability_reachability_handoff())
def selected(s, idx=0):
 p=proj(s); c=s.candidates[idx]; sel=select_operational_realization(p,p.future_selection_handoff,s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,c.candidate_id)); return p, sel, c
def warrant(s=None, c=None):
 s=s or cand_set(); p,sel,orig=selected(s); c=c or orig
 return project_operational_realization_warrant(sel,sel.future_warrant_handoff,p,s,c)
def warrant_changed(original, changed_candidate):
 p,sel,_=selected(original)
 changed_set=replace(original,candidates=tuple(changed_candidate if x.candidate_id==changed_candidate.candidate_id else x for x in original.candidates))
 return project_operational_realization_warrant(sel,sel.future_warrant_handoff,p,changed_set,changed_candidate)
def mutate_candidate(s, **kw):
 c=replace(s.candidates[0], **kw); return replace(s,candidates=(c,)+s.candidates[1:]), c

def test_warrant_immutable_deterministic_ordering_and_identity_changes():
 s=cand_set(2); p,sel,c=selected(s); a=project_operational_realization_warrant(sel,sel.future_warrant_handoff,p,s,c); b=project_operational_realization_warrant(sel,sel.future_warrant_handoff,p,replace(s,candidates=tuple(reversed(s.candidates))),c)
 assert a==project_operational_realization_warrant(sel,sel.future_warrant_handoff,p,s,c)
 assert a.warrant_id==b.warrant_id and a.warrant_state=="warranted"
 with pytest.raises(FrozenInstanceError): a.warrant_state="x"
 assert project_operational_realization_warrant(replace(sel,selection_id="sel2"),replace(sel.future_warrant_handoff,selection_id="sel2"),p,s,c).warrant_id != a.warrant_id
 assert project_operational_realization_warrant(replace(sel,reachability_projection_reference="reach2"),replace(sel.future_warrant_handoff,reachability_projection_reference="reach2"),replace(p,projection_id="reach2"),s,c).warrant_id != a.warrant_id
 for field,val in (("recovered_grammar_reference","g2"),("invocation_contract_reference","c2"),("behavior_standing","not_required"),("representation_compatibility","unknown"),("methodological_compatibility","cannot_establish"),("dependency_standing","unknown"),("authority_standing","unknown"),("provenance",("changed",)),("unknowns",("u",)),("conflicts",("conflict",))):
  ss,cc=mutate_candidate(s,**{field:val}); assert project_operational_realization_warrant(sel,sel.future_warrant_handoff,p,ss,cc).warrant_id != a.warrant_id
 assert selected(cand_set(2),1)[1].selection_id != sel.selection_id

def test_validation_mismatches_fail_deterministically_and_no_selection_control():
 s=cand_set(); p,sel,c=selected(s); h=sel.future_warrant_handoff
 bads=[(replace(h,selection_id="x"),p,s,c,"handoff"),(replace(h,probe_request_reference="x"),p,s,c,"probe-request"),(replace(h,capability_demand_reference="x"),p,s,c,"capability-demand"),(replace(h,candidate_set_reference="x"),p,s,c,"candidate-set"),(replace(h,reachability_projection_reference="x"),p,s,c,"reachability-projection"),(replace(h,selected_candidate_reference="x"),p,s,c,"selected-candidate")]
 for bh,bp,bs,bc,msg in bads:
  with pytest.raises(OperationalRealizationWarrantError, match=msg): project_operational_realization_warrant(sel,bh,bp,bs,bc)
 with pytest.raises(OperationalRealizationWarrantError, match="future warrant handoff"):
  no=select_operational_realization(p,p.future_selection_handoff,s,OperationalRealizationSelectionPolicy.select_none(s.capability_demand_reference)); project_operational_realization_warrant(no,None,p,s,c)
 with pytest.raises(OperationalRealizationWarrantError, match="missing"):
  project_operational_realization_warrant(sel,h,p,replace(s,candidates=()),c)
 with pytest.raises(OperationalRealizationWarrantError, match="not supporting"):
  project_operational_realization_warrant(sel,h,replace(p,supporting_candidate_references=()),s,c)
 with pytest.raises(OperationalRealizationWarrantError, match="not reachable"):
  project_operational_realization_warrant(sel,h,replace(p,reachability_state="unknown"),s,c)

def test_state_model_selection_and_reachability_do_not_force_warrant():
 assert warrant(cand_set()).warrant_state=="warranted"
 cases=[({"grammar_standing":"insufficient"},"insufficient"),({"behavior_standing":"contradicted"},"insufficient"),({"representation_compatibility":"incompatible"},"insufficient"),({"methodological_compatibility":"violates"},"insufficient"),({"supporting_basis_references":()},"insufficient"),({"recovered_grammar_reference":""},"unknown"),({"provenance":()},"unknown"),({"unknowns":("relevant unknown",)},"unknown"),({"behavior_standing":"conflict","conflicts":("support and contradiction",)},"conflict")]
 for kw,state in cases:
  s=cand_set(); ss,c=mutate_candidate(s,**kw); w=warrant_changed(s,c); assert w.warrant_state==state and w.future_egress_translation_handoff is None
 # count and order do not resolve conflicts
 s=cand_set(2); ss,c=mutate_candidate(s,behavior_standing="conflict",conflicts=("contradicting behavior",)); w1=warrant_changed(s,c); ss2=replace(ss,candidates=tuple(reversed(ss.candidates))); p0,sel0,_=selected(s); w2=project_operational_realization_warrant(sel0,sel0.future_warrant_handoff,p0,ss2,c); assert w1.warrant_state==w2.warrant_state=="conflict"

def test_authority_dependency_registry_contract_and_policy_boundaries():
 s=cand_set(); p,sel,c=selected(s); base=warrant(s,c)
 assert base.authority_standing=="reachable" and "authorized" not in json.dumps(base.to_json_dict()).lower()
 assert base.dependency_standing=="available"
 for kw in ({"recovered_grammar_reference":"","behavior_standing":"unknown","provenance":()}, {"supporting_basis_references":(),"provenance":()}):
  ss,cc=mutate_candidate(s,**kw); assert warrant_changed(s,cc).warrant_state!="warranted"
 polsel=select_operational_realization(p,p.future_selection_handoff,s,OperationalRealizationSelectionPolicy.exact_candidate(s.capability_demand_reference,c.candidate_id,policy_id="changed-policy"))
 assert project_operational_realization_warrant(polsel,polsel.future_warrant_handoff,p,s,c).warrant_state=="warranted"
 assert "registry" not in base.mechanism_reference.lower()

def test_repository_bash_english_internal_and_future_handoff_boundaries():
 repo=warrant(cand_set(2), selected(cand_set(2))[2] if False else None); assert repo.warrant_state=="warranted"
 local=cand_set(1,mech0="/bin/search",grammar_fragment="recovered search grammar"); assert warrant(local).warrant_state=="warranted"
 tmp=cand_set(); ss,cc=mutate_candidate(tmp,behavior_standing="unknown"); assert warrant_changed(tmp,cc).warrant_state=="unknown"
 bash=cand_set(1,"produce bounded literal output",mech0="/bin/bash",grammar_fragment="recovered literal-command fragment",excluded=("pipelines","redirection","command substitution","general scripting")); bw=warrant(bash); assert bw.warrant_state=="warranted" and bw.representation_grammar_reference=="g0" and "echo hello" not in json.dumps(bw.to_json_dict()).lower()
 eng=cand_set(1,"interpret subordinate-clause meaning",mech0="internal:english",grammar_fragment="simple declarative English sentence"); es,ec=mutate_candidate(eng,grammar_standing="insufficient",standing_reasons=("subordinate clauses excluded",)); assert warrant_changed(eng,ec).warrant_state=="insufficient"
 internal=cand_set(1,mech0="internal:deterministic-producer"); iw=warrant(internal); assert iw.warrant_state=="warranted" and "registry" not in iw.mechanism_reference.lower()
 eh=iw.future_egress_translation_handoff.to_json_dict(); text=json.dumps(eh).lower()
 for forbidden in ("command text","argv","stdin","cwd","environment","authorization","authorized","pending_action","execution_proposal"):
  assert forbidden not in text
 assert iw.future_egress_translation_handoff is not None
 for statekw in ({"grammar_standing":"insufficient"},{"unknowns":("u",)},{"conflicts":("c",)}):
  s=internal; ss,cc=mutate_candidate(s,**statekw); assert warrant_changed(s,cc).future_egress_translation_handoff is None

def test_rendering_json_read_only_and_no_mutation():
 before=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
 w=warrant(cand_set()); human=format_operational_realization_warrant(w); data=operational_realization_warrant_json(w); after=subprocess.run(["git","status","--short"],text=True,capture_output=True,check=True).stdout
 assert before==after and data["read_only"] and not data["writes_event_ledger"] and not data["mutates_cluster"]
 assert w.future_egress_translation_handoff.read_only and not w.future_egress_translation_handoff.writes_event_ledger and not w.future_egress_translation_handoff.mutates_cluster
 for phrase in ("state", "reason", "selected_candidate_reference", "supporting_basis_references", "provenance", "unknowns", "conflicts", "boundary_notes"):
  assert phrase in human
 js=json.dumps(data).lower()
 for forbidden in ("argv","stdin","cwd","environment","pending_action","execution_proposal","runtime observation"):
  assert forbidden not in js
