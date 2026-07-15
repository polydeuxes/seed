"""Read-only warrant for relying on one selected operational realization."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.candidate_operational_realization import CandidateOperationalRealization, CandidateOperationalRealizationSet
from seed_runtime.capability_reachability_projection import CapabilityReachabilityProjection
from seed_runtime.operational_realization_selection import OperationalRealizationSelection, FutureOperationalRealizationWarrantHandoff

CONVENTION="operational_realization_warrant_v1"
BOUNDARY_NOTES=(
 "This artifact warrants or refuses reliance upon one exact selected realization.",
 "Reachability does not warrant the selected realization.",
 "Selection does not warrant the selected realization.",
 "The warrant is bounded to the exact demand, candidate, grammar, contract, support, and current State.",
 "The warrant does not construct an external representation.",
 "The warrant does not authorize, schedule, emit, or execute.",
 "Authority reachability is distinct from constitutional authorization.",
 "A declared invocation contract is not sufficient without the required bounded support.",
 "A warranted realization is not a standing registry warrant.",
 "No tool, provider, toolkit, or registered-operation concept is required by this artifact.",
)
class OperationalRealizationWarrantError(ValueError): pass

def _stable(prefix:str,payload:Any)->str:
 return prefix+":"+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def _jd(o): return o.to_json_dict() if hasattr(o,"to_json_dict") else asdict(o)
def _uniq(xs): return tuple(dict.fromkeys(x for x in xs if x))

@dataclass(frozen=True)
class FutureBoundedEgressTranslationHandoff:
 warrant_reference:str; probe_request_reference:str; capability_demand_reference:str; selection_reference:str; selected_candidate_reference:str; mechanism_reference:str; representation_grammar_reference:str; invocation_contract_reference:str; required_input_representation:str; requested_output_representation:str; applicability_boundary_reference:str; known_limitations_or_loss:tuple[str,...]; dependency_standing:str; authority_standing:str; provenance:tuple[str,...]; unknowns:tuple[str,...]; conflicts:tuple[str,...]; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False
 def to_json_dict(self):
  d=asdict(self)
  for k in ("known_limitations_or_loss","provenance","unknowns","conflicts"): d[k]=list(getattr(self,k))
  return d

@dataclass(frozen=True)
class OperationalRealizationWarrant:
 artifact_type:str; warrant_id:str; probe_request_reference:str; capability_demand_reference:str; candidate_set_reference:str; reachability_projection_reference:str; selection_reference:str; selection_policy_reference:str; selected_candidate_reference:str; mechanism_reference:str; representation_grammar_reference:str; invocation_contract_reference:str; accepted_input_representation:str; produced_output_representation:str; warrant_state:str; warrant_reason:str; grammar_support:str; behavioral_support:str; representation_support:str; methodological_support:str; mechanism_standing:str; dependency_standing:str; authority_standing:str; applicability_boundary_reference:str; supporting_basis_references:tuple[str,...]; known_limitations_or_loss:tuple[str,...]; provenance:tuple[str,...]; unknowns:tuple[str,...]; conflicts:tuple[str,...]; non_selected_alternative_references:tuple[str,...]; boundary_notes:tuple[str,...]; future_egress_translation_handoff:FutureBoundedEgressTranslationHandoff|None; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False; warrant_convention:str=CONVENTION
 def to_json_dict(self):
  d=asdict(self); d["future_egress_translation_handoff"]=self.future_egress_translation_handoff.to_json_dict() if self.future_egress_translation_handoff else None
  for k in ("supporting_basis_references","known_limitations_or_loss","provenance","unknowns","conflicts","non_selected_alternative_references","boundary_notes"): d[k]=list(getattr(self,k))
  return d

def _validate(sel:OperationalRealizationSelection,h:FutureOperationalRealizationWarrantHandoff,rp:CapabilityReachabilityProjection,cs:CandidateOperationalRealizationSet,c:CandidateOperationalRealization):
 if h is None: raise OperationalRealizationWarrantError("future warrant handoff is required")
 if h.selection_id!=sel.selection_id: raise OperationalRealizationWarrantError("future warrant handoff does not belong to selection")
 if sel.selection_state!="selected" or not sel.selected_candidate_reference: raise OperationalRealizationWarrantError("selection state is not selected")
 if len([sel.selected_candidate_reference])!=1: raise OperationalRealizationWarrantError("exactly one selected candidate is required")
 if h.selected_candidate_reference!=sel.selected_candidate_reference or c.candidate_id!=sel.selected_candidate_reference: raise OperationalRealizationWarrantError("selected-candidate identity mismatch")
 if sel.selection_id!=h.selection_id: raise OperationalRealizationWarrantError("selection identity mismatch")
 if h.capability_demand_reference!=sel.capability_demand_reference or rp.capability_demand_reference!=sel.capability_demand_reference or cs.capability_demand_reference!=sel.capability_demand_reference or c.capability_demand_reference!=sel.capability_demand_reference: raise OperationalRealizationWarrantError("capability-demand identity mismatch")
 if h.probe_request_reference!=sel.probe_request_reference or rp.probe_request_reference!=sel.probe_request_reference or cs.probe_request_reference!=sel.probe_request_reference or c.probe_request_reference!=sel.probe_request_reference: raise OperationalRealizationWarrantError("probe-request identity mismatch")
 if h.candidate_set_reference!=sel.candidate_set_reference or rp.candidate_set_reference!=sel.candidate_set_reference or cs.set_id!=sel.candidate_set_reference: raise OperationalRealizationWarrantError("candidate-set identity mismatch")
 if h.reachability_projection_reference!=sel.reachability_projection_reference or rp.projection_id!=sel.reachability_projection_reference: raise OperationalRealizationWarrantError("reachability-projection identity mismatch")
 if h.selection_policy_reference!=sel.selection_policy_reference: raise OperationalRealizationWarrantError("selection-policy identity mismatch")
 if rp.reachability_state!="reachable": raise OperationalRealizationWarrantError("reachability state is not reachable")
 by={x.candidate_id:x for x in cs.candidates}
 if c.candidate_id not in by: raise OperationalRealizationWarrantError("selected candidate missing from candidate set")
 if by[c.candidate_id]!=c: raise OperationalRealizationWarrantError("selected-candidate reference was rewritten")
 if c.candidate_id not in rp.supporting_candidate_references: raise OperationalRealizationWarrantError("selected candidate not supporting by reachability")
 if c.candidate_id not in sel.eligible_candidate_references: raise OperationalRealizationWarrantError("selected candidate was not eligible under selection")
 if c.candidate_standing!="supported": raise OperationalRealizationWarrantError("selected candidate standing mismatch")
 if c.read_only is not True or c.writes_event_ledger or c.mutates_cluster: raise OperationalRealizationWarrantError("candidate read-only boundary mismatch")

def _state(c:CandidateOperationalRealization):
 conflicts=tuple(c.conflicts)
 unknowns=tuple(c.unknowns)
 bad=[]; unk=[]
 if not c.supporting_basis_references: bad.append("required support reference absent")
 if not c.provenance: unk.append("provenance incomplete")
 if not c.invocation_contract_reference: bad.append("invocation contract reference absent")
 if not c.recovered_grammar_reference: unk.append("representation grammar reference unresolved")
 dims=(c.representation_compatibility,c.methodological_compatibility,c.grammar_standing,c.behavior_standing,c.mechanism_availability_standing,c.dependency_standing,c.authority_standing)
 if "conflict" in dims or c.methodological_compatibility=="conflicts_with" or conflicts: return "conflict","preserved candidate-specific material contains unresolved conflicts"
 if c.representation_compatibility=="incompatible": bad.append("representation support insufficient")
 if c.methodological_compatibility=="violates": bad.append("method support insufficient")
 if c.grammar_standing in ("insufficient","behaviorally_contradicted"): bad.append("grammar support insufficient")
 if c.behavior_standing=="contradicted": bad.append("behavioral support insufficient")
 if c.mechanism_availability_standing=="unavailable": bad.append("mechanism unavailable")
 if c.dependency_standing=="unavailable": bad.append("dependency unavailable")
 if c.authority_standing=="unavailable": bad.append("authority standing unavailable")
 if c.representation_compatibility=="unknown": unk.append("representation compatibility unknown")
 if c.methodological_compatibility=="cannot_establish": unk.append("method compatibility cannot establish")
 if c.grammar_standing in ("unknown","declared_only","recovered_only"): unk.append("grammar standing unknown or not behaviorally supported")
 if c.behavior_standing=="unknown": unk.append("behavior standing unknown")
 if c.mechanism_availability_standing=="unknown": unk.append("mechanism standing unknown")
 if c.dependency_standing=="unknown": unk.append("dependency standing unknown")
 if c.authority_standing=="unknown": unk.append("authority standing unknown")
 if bad: return "insufficient","; ".join(bad)
 if unknowns or unk: return "unknown","; ".join(_uniq(unk+list(unknowns)))
 return "warranted","selected realization has sufficient bounded candidate-specific support for this exact demand"

def project_operational_realization_warrant(selection:OperationalRealizationSelection,future_warrant_handoff:FutureOperationalRealizationWarrantHandoff,reachability_projection:CapabilityReachabilityProjection,candidate_set:CandidateOperationalRealizationSet,selected_candidate:CandidateOperationalRealization)->OperationalRealizationWarrant:
 _validate(selection,future_warrant_handoff,reachability_projection,candidate_set,selected_candidate)
 state,reason=_state(selected_candidate)
 unknowns=_uniq(selection.policy_unknowns+future_warrant_handoff.unknowns+selected_candidate.unknowns)
 conflicts=_uniq(selection.policy_conflicts+future_warrant_handoff.conflicts+selected_candidate.conflicts)
 limitations=tuple(x for x in selected_candidate.standing_reasons if x)
 provenance=_uniq(candidate_set.shared_provenance+selection.provenance+future_warrant_handoff.provenance+selected_candidate.provenance)
 payload={"probe":selection.probe_request_reference,"demand":selection.capability_demand_reference,"set":candidate_set.set_id,"reachability":reachability_projection.projection_id,"selection":selection.selection_id,"policy":selection.selection_policy_reference,"candidate":selected_candidate.to_json_dict(),"mechanism":selected_candidate.mechanism_reference,"grammar":selected_candidate.recovered_grammar_reference,"contract":selected_candidate.invocation_contract_reference,"basis":selected_candidate.supporting_basis_references,"dependency":selected_candidate.dependency_standing,"authority":selected_candidate.authority_standing,"provenance":provenance,"unknowns":unknowns,"conflicts":conflicts,"state":state,"reason":reason,"convention":CONVENTION}
 wid=_stable("operational-realization-warrant",payload)
 eh=None
 if state=="warranted":
  eh=FutureBoundedEgressTranslationHandoff(wid,selection.probe_request_reference,selection.capability_demand_reference,selection.selection_id,selected_candidate.candidate_id,selected_candidate.mechanism_reference,selected_candidate.recovered_grammar_reference,selected_candidate.invocation_contract_reference,selected_candidate.accepted_input_representation,selected_candidate.produced_output_representation,selected_candidate.recovered_grammar_reference,limitations,selected_candidate.dependency_standing,selected_candidate.authority_standing,provenance,unknowns,conflicts)
 return OperationalRealizationWarrant("OperationalRealizationWarrant",wid,selection.probe_request_reference,selection.capability_demand_reference,candidate_set.set_id,reachability_projection.projection_id,selection.selection_id,selection.selection_policy_reference,selected_candidate.candidate_id,selected_candidate.mechanism_reference,selected_candidate.recovered_grammar_reference,selected_candidate.invocation_contract_reference,selected_candidate.accepted_input_representation,selected_candidate.produced_output_representation,state,reason,selected_candidate.grammar_standing,selected_candidate.behavior_standing,selected_candidate.representation_compatibility,selected_candidate.methodological_compatibility,selected_candidate.mechanism_availability_standing,selected_candidate.dependency_standing,selected_candidate.authority_standing,selected_candidate.recovered_grammar_reference,selected_candidate.supporting_basis_references,limitations,provenance,unknowns,conflicts,future_warrant_handoff.non_selected_alternative_references,BOUNDARY_NOTES,eh)

def operational_realization_warrant_json(w): return w.to_json_dict()
def format_operational_realization_warrant(w):
 lines=["Operational Realization Warrant",f"warrant_id: {w.warrant_id}",f"state: {w.warrant_state}",f"reason: {w.warrant_reason}",f"selected_candidate_reference: {w.selected_candidate_reference}",f"mechanism_reference: {w.mechanism_reference}",f"representation_grammar_reference: {w.representation_grammar_reference}",f"invocation_contract_reference: {w.invocation_contract_reference}",f"read_only: {str(w.read_only).lower()}",f"writes_event_ledger: {str(w.writes_event_ledger).lower()}",f"mutates_cluster: {str(w.mutates_cluster).lower()}"]
 for name,vals in (("supporting_basis_references",w.supporting_basis_references),("known_limitations_or_loss",w.known_limitations_or_loss),("provenance",w.provenance),("unknowns",w.unknowns),("conflicts",w.conflicts),("boundary_notes",w.boundary_notes)):
  lines += [f"{name}:"]+([f"- {x}" for x in vals] or ["- none"])
 return "\n".join(lines)
