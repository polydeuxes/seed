"""Read-only selection of zero or one operational realization."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any
from seed_runtime.candidate_operational_realization import CandidateOperationalRealizationSet
from seed_runtime.capability_reachability_projection import CapabilityReachabilityProjection, FutureOperationalRealizationSelectionHandoff

CONVENTION="operational_realization_selection_v1"
BOUNDARY_NOTES=(
 "This artifact selects zero or one supported realization; it does not warrant reliance upon the selection.",
 "Selection policy determines choice; candidate ordering does not.",
 "A supporting candidate may remain non-selected without becoming unsupported.",
 "Selection does not construct an invocation request.",
 "Selection does not translate Seed-native meaning into an external representation.",
 "Selection does not authorize, schedule, or execute.",
 "Authority-related selection constraints are distinct from constitutional authorization.",
 "No tool, provider, toolkit, or registered-operation concept is required by this selection.",
)
class OperationalRealizationSelectionError(ValueError): pass

def _stable(prefix:str,payload:Any)->str:
 return prefix+":"+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def _list(x): return list(x) if isinstance(x,tuple) else x

def _jd(o): return o.to_json_dict() if hasattr(o,"to_json_dict") else asdict(o)

@dataclass(frozen=True)
class OperationalRealizationSelectionPolicy:
 policy_id:str; capability_demand_reference:str; policy_kind:str; required_candidate_references:tuple[str,...]=(); allowed_mechanism_references:tuple[str,...]=(); required_representation_pair:tuple[str,str]|None=None; required_methodological_compatibility:str=""; allowed_authority_standings:tuple[str,...]=(); allowed_dependency_standings:tuple[str,...]=(); policy_unknowns:tuple[str,...]=(); policy_conflicts:tuple[str,...]=(); provenance:tuple[str,...]=(); read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False
 @staticmethod
 def exact_candidate(capability_demand_reference:str,candidate_reference:str,policy_id:str|None=None):
  pid=policy_id or _stable("operational-realization-selection-policy",{"kind":"exact_candidate","demand":capability_demand_reference,"required":[candidate_reference],"convention":CONVENTION})
  return OperationalRealizationSelectionPolicy(pid,capability_demand_reference,"exact_candidate",(candidate_reference,))
 @staticmethod
 def sole_supported_candidate(capability_demand_reference:str,policy_id:str|None=None):
  pid=policy_id or _stable("operational-realization-selection-policy",{"kind":"sole_supported_candidate","demand":capability_demand_reference,"convention":CONVENTION})
  return OperationalRealizationSelectionPolicy(pid,capability_demand_reference,"sole_supported_candidate")
 @staticmethod
 def select_none(capability_demand_reference:str,policy_id:str|None=None):
  pid=policy_id or _stable("operational-realization-selection-policy",{"kind":"select_none","demand":capability_demand_reference,"convention":CONVENTION})
  return OperationalRealizationSelectionPolicy(pid,capability_demand_reference,"select_none")
 @staticmethod
 def constraints(capability_demand_reference:str,*,allowed_mechanism_references=(),required_representation_pair=None,required_methodological_compatibility="",allowed_authority_standings=(),allowed_dependency_standings=(),policy_id=None):
  payload={"kind":"constraints","demand":capability_demand_reference,"mechanisms":sorted(allowed_mechanism_references),"rep":required_representation_pair,"method":required_methodological_compatibility,"auth":sorted(allowed_authority_standings),"dep":sorted(allowed_dependency_standings),"convention":CONVENTION}
  return OperationalRealizationSelectionPolicy(policy_id or _stable("operational-realization-selection-policy",payload),capability_demand_reference,"constraints",(),tuple(allowed_mechanism_references),required_representation_pair,required_methodological_compatibility,tuple(allowed_authority_standings),tuple(allowed_dependency_standings))
 def to_json_dict(self):
  d=asdict(self)
  for k in ("required_candidate_references","allowed_mechanism_references","allowed_authority_standings","allowed_dependency_standings","policy_unknowns","policy_conflicts","provenance"): d[k]=list(getattr(self,k))
  if self.required_representation_pair is not None: d["required_representation_pair"]=list(self.required_representation_pair)
  return d

@dataclass(frozen=True)
class NonSelectedOperationalRealization:
 candidate_reference:str; non_selection_reason:str
 def to_json_dict(self): return asdict(self)

@dataclass(frozen=True)
class FutureOperationalRealizationWarrantHandoff:
 selection_id:str; probe_request_reference:str; capability_demand_reference:str; candidate_set_reference:str; reachability_projection_reference:str; selected_candidate_reference:str; selection_policy_reference:str; selection_reason:str; non_selected_alternative_references:tuple[str,...]; provenance:tuple[str,...]; unknowns:tuple[str,...]; conflicts:tuple[str,...]; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False
 def to_json_dict(self):
  d=asdict(self)
  for k in ("non_selected_alternative_references","provenance","unknowns","conflicts"): d[k]=list(getattr(self,k))
  return d

@dataclass(frozen=True)
class OperationalRealizationSelection:
 artifact_type:str; selection_id:str; probe_request_reference:str; capability_demand_reference:str; candidate_set_reference:str; reachability_projection_reference:str; future_selection_handoff_reference:str; selection_policy_reference:str; selection_state:str; selected_candidate_reference:str|None; eligible_candidate_references:tuple[str,...]; non_selected_supporting_candidates:tuple[NonSelectedOperationalRealization,...]; policy_ineligible_supporting_candidate_references:tuple[str,...]; blocked_candidate_references:tuple[str,...]; unsupported_candidate_references:tuple[str,...]; unknown_candidate_references:tuple[str,...]; conflicting_candidate_references:tuple[str,...]; selection_reason:str; reachability_reason:str; policy_unknowns:tuple[str,...]; policy_conflicts:tuple[str,...]; provenance:tuple[str,...]; future_warrant_handoff:FutureOperationalRealizationWarrantHandoff|None; boundary_notes:tuple[str,...]=BOUNDARY_NOTES; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False; selection_convention:str=CONVENTION
 def to_json_dict(self):
  d=asdict(self); d["non_selected_supporting_candidates"]=[x.to_json_dict() for x in self.non_selected_supporting_candidates]; d["future_warrant_handoff"]=self.future_warrant_handoff.to_json_dict() if self.future_warrant_handoff else None
  for k in ("eligible_candidate_references","policy_ineligible_supporting_candidate_references","blocked_candidate_references","unsupported_candidate_references","unknown_candidate_references","conflicting_candidate_references","policy_unknowns","policy_conflicts","provenance","boundary_notes"): d[k]=list(getattr(self,k))
  return d

def _validate(cs, rp, h, pol):
 if h is None: raise OperationalRealizationSelectionError("future selection handoff is required")
 if h.reachability_projection_id != rp.projection_id: raise OperationalRealizationSelectionError("handoff does not reference supplied reachability projection")
 if h.candidate_set_reference != cs.set_id or rp.candidate_set_reference != cs.set_id: raise OperationalRealizationSelectionError("candidate-set identity mismatch")
 if h.probe_request_reference != cs.probe_request_reference or rp.probe_request_reference != cs.probe_request_reference: raise OperationalRealizationSelectionError("probe-request identity mismatch")
 if h.capability_demand_reference != cs.capability_demand_reference or rp.capability_demand_reference != cs.capability_demand_reference or pol.capability_demand_reference != cs.capability_demand_reference: raise OperationalRealizationSelectionError("capability-demand identity mismatch")
 by={c.candidate_id:c for c in cs.candidates}
 for ref in rp.supporting_candidate_references+rp.blocked_candidate_references+rp.unsupported_candidate_references+rp.unknown_candidate_references+rp.conflicting_candidate_references:
  if ref not in by: raise OperationalRealizationSelectionError("missing referenced candidate")
 for ref in rp.supporting_candidate_references:
  if by[ref].candidate_standing != "supported": raise OperationalRealizationSelectionError("candidate standing mismatch")
 if set(h.supporting_candidate_references)!=set(rp.supporting_candidate_references) or set(h.blocked_candidate_references)!=set(rp.blocked_candidate_references): raise OperationalRealizationSelectionError("selection handoff candidate partition mismatch")

def select_operational_realization(reachability_projection:CapabilityReachabilityProjection, future_selection_handoff:FutureOperationalRealizationSelectionHandoff, candidate_set:CandidateOperationalRealizationSet, selection_policy:OperationalRealizationSelectionPolicy|None)->OperationalRealizationSelection:
 if selection_policy is None:
  selection_policy=OperationalRealizationSelectionPolicy(_stable("operational-realization-selection-policy",{"kind":"insufficient","demand":reachability_projection.capability_demand_reference,"convention":CONVENTION}),reachability_projection.capability_demand_reference,"insufficient")
 _validate(candidate_set,reachability_projection,future_selection_handoff,selection_policy)
 by={c.candidate_id:c for c in candidate_set.candidates}; supporting=tuple(sorted(reachability_projection.supporting_candidate_references)); eligible=supporting if reachability_projection.reachability_state=="reachable" else ()
 state="no_selection"; selected=None; reason="policy insufficient"; ineligible=(); conflicts=tuple(selection_policy.policy_conflicts)
 if reachability_projection.reachability_state!="reachable": reason="reachability_not_reachable"
 elif conflicts or (selection_policy.policy_kind=="exact_candidate" and len(set(selection_policy.required_candidate_references))>1): state="conflict"; reason="policy contains incompatible required candidates"; conflicts=conflicts or ("incompatible required candidate identities",)
 elif selection_policy.policy_kind in ("insufficient",""): reason="policy insufficient"
 elif selection_policy.policy_kind=="select_none": reason="policy selects none"
 elif selection_policy.policy_kind=="exact_candidate":
  req=selection_policy.required_candidate_references[0] if selection_policy.required_candidate_references else ""
  if req in eligible: state="selected"; selected=req; reason="explicit candidate policy matched one eligible supporting candidate"
  else: reason="required candidate is not eligible"
 elif selection_policy.policy_kind=="sole_supported_candidate":
  if len(eligible)==1: state="selected"; selected=eligible[0]; reason="sole-supported-candidate policy matched exactly one supporting candidate"
  elif len(eligible)==0: reason="no_supporting_candidate"
  else: reason="unresolved_tie"
 elif selection_policy.policy_kind=="constraints":
  matches=[]
  for cid in eligible:
   c=by[cid]; ok=True
   if selection_policy.allowed_mechanism_references and c.mechanism_reference not in selection_policy.allowed_mechanism_references: ok=False
   if selection_policy.required_representation_pair and (c.accepted_input_representation,c.produced_output_representation)!=tuple(selection_policy.required_representation_pair): ok=False
   if selection_policy.required_methodological_compatibility and c.methodological_compatibility!=selection_policy.required_methodological_compatibility: ok=False
   if selection_policy.allowed_authority_standings and c.authority_standing not in selection_policy.allowed_authority_standings: ok=False
   if selection_policy.allowed_dependency_standings and c.dependency_standing not in selection_policy.allowed_dependency_standings: ok=False
   if ok: matches.append(cid)
  if len(matches)==1: state="selected"; selected=matches[0]; reason="explicit constraints matched one eligible supporting candidate"
  elif len(matches)>1: reason="unresolved_tie"
  else: reason="no_candidate_satisfies_policy"
 non=[]; policy_in=[]
 for cid in supporting:
  if cid==selected: continue
  nr="alternative_candidate" if selected else ("unresolved_tie" if reason=="unresolved_tie" else "selection_policy_chose_none" if reason=="policy selects none" else "not_required_candidate" if selection_policy.policy_kind=="exact_candidate" else "policy_constraint_not_satisfied")
  non.append(NonSelectedOperationalRealization(cid,nr))
  if nr=="policy_constraint_not_satisfied": policy_in.append(cid)
 payload={"probe":candidate_set.probe_request_reference,"demand":candidate_set.capability_demand_reference,"set":candidate_set.set_id,"reachability":reachability_projection.projection_id,"handoff":future_selection_handoff.to_json_dict(),"policy":selection_policy.to_json_dict(),"eligible":eligible,"state":state,"selected":selected,"non_selected":[x.to_json_dict() for x in non],"reason":reason,"conflicts":conflicts,"convention":CONVENTION}
 sid=_stable("operational-realization-selection",payload)
 wh=None
 if state=="selected" and selected:
  wh=FutureOperationalRealizationWarrantHandoff(sid,candidate_set.probe_request_reference,candidate_set.capability_demand_reference,candidate_set.set_id,reachability_projection.projection_id,selected,selection_policy.policy_id,reason,tuple(x.candidate_reference for x in non),candidate_set.shared_provenance,selection_policy.policy_unknowns,conflicts)
 return OperationalRealizationSelection("OperationalRealizationSelection",sid,candidate_set.probe_request_reference,candidate_set.capability_demand_reference,candidate_set.set_id,reachability_projection.projection_id,future_selection_handoff.reachability_projection_id,selection_policy.policy_id,state,selected,eligible,tuple(non),tuple(policy_in),reachability_projection.blocked_candidate_references,reachability_projection.unsupported_candidate_references,reachability_projection.unknown_candidate_references,reachability_projection.conflicting_candidate_references,reason,reachability_projection.conclusion_reason,selection_policy.policy_unknowns,conflicts,candidate_set.shared_provenance,wh)

def operational_realization_selection_json(s): return s.to_json_dict()
def format_operational_realization_selection(s):
 lines=["Operational Realization Selection",f"selection_id: {s.selection_id}",f"state: {s.selection_state}",f"selected_candidate_reference: {s.selected_candidate_reference if s.selected_candidate_reference else 'none'}",f"selection_reason: {s.selection_reason}",f"reachability_reason: {s.reachability_reason}",f"read_only: {str(s.read_only).lower()}",f"writes_event_ledger: {str(s.writes_event_ledger).lower()}",f"mutates_cluster: {str(s.mutates_cluster).lower()}","eligible_candidates:"]
 lines += [f"- {x}" for x in s.eligible_candidate_references] or ["- none"]
 lines += ["non_selected_supporting_candidates:"] + ([f"- {x.candidate_reference}: {x.non_selection_reason}" for x in s.non_selected_supporting_candidates] or ["- none"])
 for name,vals in (("blocked_candidates",s.blocked_candidate_references),("unsupported_candidates",s.unsupported_candidate_references),("unknown_candidates",s.unknown_candidate_references),("conflicting_candidates",s.conflicting_candidate_references),("policy_unknowns",s.policy_unknowns),("policy_conflicts",s.policy_conflicts)):
  lines += [f"{name}:"]+([f"- {x}" for x in vals] or ["- none"])
 lines += ["boundary_notes:"]+[f"- {x}" for x in s.boundary_notes]
 return "\n".join(lines)
