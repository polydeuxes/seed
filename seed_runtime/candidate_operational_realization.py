"""Read-only candidate operational realization projection for one exact handoff."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.examination_probe_request import OperationalRealizationHandoff
from seed_runtime.representation_grammar_applicability import FutureCandidateOperationalRealizationHandoff

CONVENTION = "candidate_operational_realization_projection_v1"
BOUNDARY_NOTES = (
    "This artifact projects candidate operational realizations; it does not project overall capability reachability.",
    "Mechanism existence does not establish capability reachability.",
    "Declared invocation grammar does not establish behaviorally validated competency.",
    "Behavioral support is bounded to the observed mechanism, version, invocation grammar, and probe conditions.",
    "Authority availability is distinct from policy authorization.",
    "Candidates are preserved without ranking or selection.",
    "No known realization does not mean the transformation is impossible.",
    "No tool, provider, toolkit, or registered-operation concept is required by this artifact.",
)
STANDINGS = ("supported", "unsupported", "unknown", "conflict")
COMPAT = ("compatible", "incompatible", "unknown", "conflict")
METHOD = ("satisfies", "violates", "cannot_establish", "conflicts_with")
AVAIL = ("available", "unavailable", "unknown", "conflict")
AUTH = ("reachable", "unavailable", "unknown", "conflict")
GRAMMAR_STANDINGS = ("declared_only", "recovered_only", "behaviorally_supported", "behaviorally_contradicted", "unknown", "insufficient", "conflict")
BEHAVIOR_STANDINGS = ("supported", "contradicted", "unknown", "conflict", "not_required")

class CandidateOperationalRealizationError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _refs(xs): return tuple(sorted({x for x in xs if x}))

@dataclass(frozen=True)
class MechanismObservation:
    observation_id: str; mechanism_id: str; observation_kind: str; observed_value: str; mechanism_version: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def to_json_dict(self): d=asdict(self); d["provenance"]=list(self.provenance); d["unknowns"]=list(self.unknowns); return d

@dataclass(frozen=True)
class AttributedMechanismClaim:
    claim_id: str; source_id: str; mechanism_id: str; claim_reference: str; claimed_transformation: str=""; attribution: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=(); contradictions: tuple[str,...]=()
    def to_json_dict(self): d=asdict(self); [d.__setitem__(k,list(getattr(self,k))) for k in ("provenance","unknowns","contradictions")]; return d

@dataclass(frozen=True)
class InvocationContract:
    contract_id: str; mechanism_id: str; accepted_input_representation: str; produced_output_representation: str; argument_grammar: str=""; result_grammar: str=""; convention: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def to_json_dict(self): d=asdict(self); d["provenance"]=list(self.provenance); d["unknowns"]=list(self.unknowns); return d

@dataclass(frozen=True)
class RecoveredInvocationGrammar:
    grammar_id: str; mechanism_id: str; bounded_fragment: str; convention: str=""; supported_structures: tuple[str,...]=(); excluded_structures: tuple[str,...]=(); source_material_refs: tuple[str,...]=(); provenance: tuple[str,...]=(); unknowns: tuple[str,...]=(); conflicts: tuple[str,...]=()
    def to_json_dict(self): d=asdict(self); [d.__setitem__(k,list(getattr(self,k))) for k in ("supported_structures","excluded_structures","source_material_refs","provenance","unknowns","conflicts")]; return d

@dataclass(frozen=True)
class BehavioralObservation:
    observation_id: str; mechanism_id: str; exact_invocation_input: str; stdout: str=""; stderr: str=""; exit_status: int|None=None; mechanism_version: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def to_json_dict(self): d=asdict(self); d["provenance"]=list(self.provenance); d["unknowns"]=list(self.unknowns); return d

@dataclass(frozen=True)
class BehaviorComparison:
    comparison_id: str; reference_id: str; behavioral_observation_id: str; compared_dimensions: tuple[str,...]; result: str; reason: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def __post_init__(self):
        if self.result not in ("supported","contradicted","unknown","conflict"): raise CandidateOperationalRealizationError("invalid behavior comparison result")
    def to_json_dict(self): d=asdict(self); d["compared_dimensions"]=list(self.compared_dimensions); d["provenance"]=list(self.provenance); d["unknowns"]=list(self.unknowns); return d

@dataclass(frozen=True)
class OperationalRealizationBasis:
    basis_id: str; mechanism_id: str; mechanism_version: str; mechanism_observation_refs: tuple[str,...]=(); attributed_claim_refs: tuple[str,...]=(); invocation_contract_ref: str=""; recovered_grammar_ref: str=""; behavioral_observation_refs: tuple[str,...]=(); behavior_comparison_refs: tuple[str,...]=(); availability_evidence: str="unknown"; dependency_evidence: str="unknown"; authority_evidence: str="unknown"; representation_compatibility: str="unknown"; methodological_compatibility: str="cannot_establish"; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=(); conflicts: tuple[str,...]=()
    def to_json_dict(self): d=asdict(self); [d.__setitem__(k,list(getattr(self,k))) for k in ("mechanism_observation_refs","attributed_claim_refs","behavioral_observation_refs","behavior_comparison_refs","provenance","unknowns","conflicts")]; return d

@dataclass(frozen=True)
class CandidateOperationalRealization:
    candidate_id: str; probe_request_reference: str; capability_demand_reference: str; mechanism_reference: str; mechanism_version: str; invocation_contract_reference: str; recovered_grammar_reference: str; accepted_input_representation: str; produced_output_representation: str; mechanism_availability_standing: str; grammar_standing: str; behavior_standing: str; representation_compatibility: str; methodological_compatibility: str; dependency_standing: str; authority_standing: str; supporting_basis_references: tuple[str,...]; provenance: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; candidate_standing: str; standing_reasons: tuple[str,...]; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k in ("supporting_basis_references","provenance","unknowns","conflicts","standing_reasons"): d[k]=list(getattr(self,k))
        return d

@dataclass(frozen=True)
class FutureCapabilityReachabilityHandoff:
    candidate_set_id: str; probe_request_reference: str; capability_demand_reference: str; candidate_references: tuple[str,...]; candidate_standings: dict[str,str]; dependency_observations: tuple[str,...]; authority_observations: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self): d=asdict(self); [d.__setitem__(k,list(getattr(self,k))) for k in ("candidate_references","dependency_observations","authority_observations","unknowns","conflicts")]; return d

@dataclass(frozen=True)
class CandidateOperationalRealizationSet:
    artifact_type: str; set_id: str; probe_request_reference: str; capability_demand_reference: str; candidates: tuple[CandidateOperationalRealization,...]; supported_references: tuple[str,...]; unsupported_references: tuple[str,...]; unknown_references: tuple[str,...]; conflict_references: tuple[str,...]; no_known_realization_observations: tuple[str,...]; shared_provenance: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False; projection_convention: str=CONVENTION
    def to_json_dict(self):
        d=asdict(self); d["candidates"]=[c.to_json_dict() for c in self.candidates]
        for k in ("supported_references","unsupported_references","unknown_references","conflict_references","no_known_realization_observations","shared_provenance","unknowns","conflicts","boundary_notes"): d[k]=list(getattr(self,k))
        return d
    def to_future_capability_reachability_handoff(self):
        return FutureCapabilityReachabilityHandoff(self.set_id,self.probe_request_reference,self.capability_demand_reference,tuple(c.candidate_id for c in self.candidates),{c.candidate_id:c.candidate_standing for c in self.candidates},tuple(c.dependency_standing for c in self.candidates),tuple(c.authority_standing for c in self.candidates),self.unknowns,self.conflicts)

def _projection_for(basis, contract, grammar, comps, representation_grammar_applicable=False):
    rep=basis.representation_compatibility if basis.representation_compatibility in COMPAT else "unknown"
    meth=basis.methodological_compatibility if basis.methodological_compatibility in METHOD else "cannot_establish"
    mech={"available":"available","unavailable":"unavailable","conflict":"conflict"}.get(basis.availability_evidence,"unknown")
    dep={"available":"available","unavailable":"unavailable","conflict":"conflict"}.get(basis.dependency_evidence,"unknown")
    auth={"reachable":"reachable","unavailable":"unavailable","conflict":"conflict"}.get(basis.authority_evidence,"unknown")
    if any(c.result=="conflict" for c in comps): beh="conflict"
    elif any(c.result=="contradicted" for c in comps): beh="contradicted"
    elif any(c.result=="supported" for c in comps): beh="supported"
    elif comps: beh="unknown"
    else: beh="not_required" if (representation_grammar_applicable or (not grammar and contract and contract.argument_grammar.startswith("opaque"))) else "unknown"
    if representation_grammar_applicable: gram="recovered_only"
    elif grammar and beh=="supported": gram="behaviorally_supported"
    elif grammar and beh=="contradicted": gram="behaviorally_contradicted"
    elif grammar: gram="recovered_only"
    elif contract and contract.argument_grammar: gram="declared_only"
    else: gram="unknown"
    reasons=[]
    if mech=="unavailable": reasons.append("mechanism unavailable")
    if dep=="unavailable": reasons.append("dependency blocked")
    if auth=="unavailable": reasons.append("authority blocked")
    if rep=="incompatible": reasons.append("representation incompatible")
    if meth=="violates": reasons.append("methodologically incompatible")
    if beh=="contradicted": reasons.append("behavior contradicted")
    if gram in ("unknown","declared_only","recovered_only") and beh not in ("not_required","supported"): reasons.append("grammar insufficient")
    if "conflict" in (mech,dep,auth,rep) or meth=="conflicts_with" or beh=="conflict": standing="conflict"
    elif beh=="contradicted" or rep=="incompatible" or meth=="violates": standing="unsupported"
    elif mech=="available" and dep!="unavailable" and rep=="compatible" and meth=="satisfies" and (beh in ("supported","not_required")) and gram not in ("unknown",): standing="supported"
    else: standing="unknown"
    return mech, gram, beh, rep, meth, dep, auth, standing, tuple(reasons)

def project_candidate_operational_realizations(handoff: OperationalRealizationHandoff, *, mechanism_observations: tuple[MechanismObservation,...]=(), attributed_claims: tuple[AttributedMechanismClaim,...]=(), invocation_contracts: tuple[InvocationContract,...]=(), recovered_grammars: tuple[RecoveredInvocationGrammar,...]=(), representation_grammar_applicability_handoffs: tuple[FutureCandidateOperationalRealizationHandoff,...]=(), behavioral_observations: tuple[BehavioralObservation,...]=(), behavior_comparisons: tuple[BehaviorComparison,...]=(), bases: tuple[OperationalRealizationBasis,...]=(), shared_provenance: tuple[str,...]=(), set_unknowns: tuple[str,...]=()) -> CandidateOperationalRealizationSet:
    obs_by_mech={}
    for o in mechanism_observations: obs_by_mech.setdefault(o.mechanism_id,[]).append(o)
    claims_by_mech={}
    for c in attributed_claims: claims_by_mech.setdefault(c.mechanism_id,[]).append(c)
    contracts_by_mech={}
    for c in invocation_contracts: contracts_by_mech.setdefault(c.mechanism_id,[]).append(c)
    grammars_by_mech={}
    for g in recovered_grammars: grammars_by_mech.setdefault(g.mechanism_id,[]).append(g)
    app_by_key={(h.mechanism_ref,h.invocation_contract_ref,h.recovered_grammar_ref):h for h in representation_grammar_applicability_handoffs if h.probe_request_ref==handoff.probe_request_id and h.capability_demand_ref==handoff.capability_identity}
    bobs={o.observation_id:o for o in behavioral_observations}; comps_by_ref={}
    for c in behavior_comparisons: comps_by_ref.setdefault(c.reference_id,[]).append(c)
    if not bases:
        mechs=sorted(set(obs_by_mech)|set(claims_by_mech)|set(contracts_by_mech)|set(grammars_by_mech)|{h.mechanism_ref for h in representation_grammar_applicability_handoffs}|{o.mechanism_id for o in behavioral_observations})
        tmp=[]
        for mid in mechs:
            obs=obs_by_mech.get(mid,()); ver=next((o.mechanism_version for o in obs if o.mechanism_version),"")
            contracts=contracts_by_mech.get(mid) or (InvocationContract("",mid,"unknown","unknown"),)
            grammars=grammars_by_mech.get(mid) or (None,)
            app_hands=tuple(h for h in representation_grammar_applicability_handoffs if h.mechanism_ref==mid)
            for con in contracts:
                expanded=(tuple(h for h in app_hands if h.invocation_contract_ref==con.contract_id) or grammars)
                for gr in expanded:
                    bid=_stable("operational-realization-basis",{"probe":handoff.probe_request_id,"demand":handoff.capability_identity,"mechanism":mid,"version":ver,"contract":con.contract_id,"grammar":getattr(gr,"grammar_id",getattr(gr,"recovered_grammar_ref",""))})
                    rep="compatible" if con.accepted_input_representation==handoff.required_input_representation and con.produced_output_representation==handoff.requested_output_representation else "unknown" if con.accepted_input_representation=="unknown" else "incompatible"
                    tmp.append(OperationalRealizationBasis(bid,mid,ver,_refs(o.observation_id for o in obs),_refs(c.claim_id for c in claims_by_mech.get(mid,())),con.contract_id,getattr(gr,"grammar_id",getattr(gr,"recovered_grammar_ref","")) if gr else "",(),(),"available" if obs else "unknown","available" if obs else "unknown","reachable" if obs else "unknown",rep,"satisfies",tuple(x for o in obs for x in o.provenance)))
        bases=tuple(tmp)
    candidates=[]
    for b in sorted(bases,key=lambda x:x.basis_id):
        con=next((c for c in invocation_contracts if c.contract_id==b.invocation_contract_ref), None)
        gr=next((g for g in recovered_grammars if g.grammar_id==b.recovered_grammar_ref), None)
        app_handoff=app_by_key.get((b.mechanism_id,b.invocation_contract_ref,b.recovered_grammar_ref))
        comps=tuple(c for ref in (b.behavior_comparison_refs or ((gr.grammar_id,) if gr else (con.contract_id if con else "",))) for c in comps_by_ref.get(ref,()) if (not c.behavioral_observation_id or c.behavioral_observation_id in bobs))
        mech,gram,beh,rep,meth,dep,auth,standing,reasons=_projection_for(b,con,gr,comps, bool(app_handoff))
        cid=_stable("candidate-operational-realization",{"probe":handoff.probe_request_id,"demand":handoff.capability_identity,"mechanism":b.mechanism_id,"version":b.mechanism_version,"contract":b.invocation_contract_ref,"grammar":b.recovered_grammar_ref,"input":con.accepted_input_representation if con else handoff.required_input_representation,"output":con.produced_output_representation if con else handoff.requested_output_representation,"method":handoff.method_constraint_reference,"basis":b.basis_id,"standing":standing,"comparison_ids":[c.comparison_id for c in comps],"convention":CONVENTION})
        candidates.append(CandidateOperationalRealization(cid,handoff.probe_request_id,handoff.capability_identity,b.mechanism_id,b.mechanism_version,b.invocation_contract_ref,b.recovered_grammar_ref,con.accepted_input_representation if con else handoff.required_input_representation,con.produced_output_representation if con else handoff.requested_output_representation,mech,gram,beh,rep,meth,dep,auth,(b.basis_id,),b.provenance,b.unknowns,b.conflicts,standing,reasons))
    candidates=tuple(sorted(candidates,key=lambda c:(c.mechanism_reference,c.invocation_contract_reference,c.recovered_grammar_reference,c.candidate_id)))
    no=() if candidates else ("no known realization",)
    sid=_stable("candidate-operational-realization-set",{"probe":handoff.probe_request_id,"demand":handoff.capability_identity,"candidate_ids":[c.candidate_id for c in candidates],"convention":CONVENTION})
    return CandidateOperationalRealizationSet("CandidateOperationalRealizationSet",sid,handoff.probe_request_id,handoff.capability_identity,candidates,tuple(c.candidate_id for c in candidates if c.candidate_standing=="supported"),tuple(c.candidate_id for c in candidates if c.candidate_standing=="unsupported"),tuple(c.candidate_id for c in candidates if c.candidate_standing=="unknown"),tuple(c.candidate_id for c in candidates if c.candidate_standing=="conflict"),no,shared_provenance,set_unknowns,tuple(x for c in candidates for x in c.conflicts))

def candidate_operational_realization_json(s: CandidateOperationalRealizationSet): return s.to_json_dict()

def format_candidate_operational_realization_set(s: CandidateOperationalRealizationSet) -> str:
    lines=["Candidate Operational Realization Projection",f"set_id: {s.set_id}",f"probe_request_reference: {s.probe_request_reference}",f"capability_demand_reference: {s.capability_demand_reference}",f"read_only: {str(s.read_only).lower()}",f"writes_event_ledger: {str(s.writes_event_ledger).lower()}",f"mutates_cluster: {str(s.mutates_cluster).lower()}","candidates:"]
    lines += [f"- {c.candidate_id}: mechanism={c.mechanism_reference}; standing={c.candidate_standing}; grammar={c.grammar_standing}; behavior={c.behavior_standing}; representation={c.representation_compatibility}; method={c.methodological_compatibility}; dependency={c.dependency_standing}; authority={c.authority_standing}; selected=false" for c in s.candidates] or ["- none"]
    if s.no_known_realization_observations: lines += ["no_known_realization_observations:"]+[f"- {x}" for x in s.no_known_realization_observations]
    lines += ["unknowns:"]+([f"- {x}" for x in s.unknowns] or ["- none"])
    lines += ["conflicts:"]+([f"- {x}" for x in s.conflicts] or ["- none"])
    lines += ["boundary_notes:"]+[f"- {x}" for x in s.boundary_notes]
    return "\n".join(lines)
