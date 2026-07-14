"""Demand-level capability reachability projection from candidate realizations."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.candidate_operational_realization import CandidateOperationalRealizationSet, FutureCapabilityReachabilityHandoff

CONVENTION = "capability_reachability_projection_v1"
BOUNDARY_NOTES = (
    "Capability is projected reachability of this exact bounded transformation; it is not possession of a mechanism.",
    "This artifact consumes candidate-realization projections; it does not construct or reinterpret candidate realizations.",
    "Reachability does not select a realization.",
    "Mechanical reachability is distinct from dependency availability, authority availability, and policy authorization.",
    "No known realization does not mean the transformation is impossible.",
    "Unsupported requires bounded positive evidence; absence alone produces Unknown.",
    "Multiple supported realizations establish no preference among them.",
    "This artifact does not authorize, schedule, execute, or create a pending action.",
    "No tool, provider, toolkit, or registered-operation concept is required by this projection.",
)

class CapabilityReachabilityProjectionError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _asdict(obj): return obj.to_json_dict() if hasattr(obj, "to_json_dict") else asdict(obj)
def _uniq(xs): return tuple(dict.fromkeys(x for x in xs if x))

@dataclass(frozen=True)
class FutureOperationalRealizationSelectionHandoff:
    reachability_projection_id: str; probe_request_reference: str; capability_demand_reference: str; candidate_set_reference: str; reachability_state: str; supporting_candidate_references: tuple[str,...]; blocked_candidate_references: tuple[str,...]; unknown_candidate_references: tuple[str,...]; conflict_references: tuple[str,...]; conclusion_reason: str; selection_lawful_now: bool; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k in ("supporting_candidate_references","blocked_candidate_references","unknown_candidate_references","conflict_references"): d[k]=list(getattr(self,k))
        return d

@dataclass(frozen=True)
class CapabilityReachabilityProjection:
    artifact_type: str; projection_id: str; probe_request_reference: str; capability_demand_reference: str; candidate_set_reference: str; future_handoff_reference: str; reachability_state: str; conclusion_reason: str; supporting_candidate_references: tuple[str,...]; blocked_candidate_references: tuple[str,...]; unsupported_candidate_references: tuple[str,...]; unknown_candidate_references: tuple[str,...]; conflicting_candidate_references: tuple[str,...]; dependency_blockers: tuple[str,...]; authority_blockers: tuple[str,...]; representation_blockers: tuple[str,...]; methodological_blockers: tuple[str,...]; grammar_insufficiencies: tuple[str,...]; behavioral_contradictions: tuple[str,...]; no_known_realization_observations: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; mechanical_reachability: str; dependency_reachability: str; authority_reachability: str; grammar_sufficiency: str; behavioral_support: str; representation_support: str; method_support: str; future_selection_handoff: FutureOperationalRealizationSelectionHandoff|None; provenance: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False; projection_convention: str=CONVENTION
    def to_json_dict(self):
        d=asdict(self)
        for k in ("supporting_candidate_references","blocked_candidate_references","unsupported_candidate_references","unknown_candidate_references","conflicting_candidate_references","dependency_blockers","authority_blockers","representation_blockers","methodological_blockers","grammar_insufficiencies","behavioral_contradictions","no_known_realization_observations","unknowns","conflicts","provenance","boundary_notes"): d[k]=list(getattr(self,k))
        d["future_selection_handoff"] = self.future_selection_handoff.to_json_dict() if self.future_selection_handoff else None
        return d

def _summary(vals, good, bad, unknown="unknown"):
    vals=set(vals)
    if "conflict" in vals or "conflicts_with" in vals: return "conflict"
    if vals and vals <= {good}: return good
    if vals and vals <= {bad}: return bad
    if good in vals and bad in vals: return "conflict"
    return unknown

def _validate(s: CandidateOperationalRealizationSet, h: FutureCapabilityReachabilityHandoff):
    if h.candidate_set_id != s.set_id: raise CapabilityReachabilityProjectionError("future handoff does not belong to supplied candidate set")
    if h.probe_request_reference != s.probe_request_reference: raise CapabilityReachabilityProjectionError("probe-request identity mismatch")
    if h.capability_demand_reference != s.capability_demand_reference: raise CapabilityReachabilityProjectionError("capability-demand identity mismatch")
    ids=tuple(c.candidate_id for c in s.candidates)
    if tuple(h.candidate_references) != ids: raise CapabilityReachabilityProjectionError("candidate references or ordering mismatch")
    if set(h.candidate_standings) != set(ids): raise CapabilityReachabilityProjectionError("candidate standing references mismatch")
    for c in s.candidates:
        if h.candidate_standings.get(c.candidate_id) != c.candidate_standing: raise CapabilityReachabilityProjectionError("candidate standing mismatch")
    if tuple(h.dependency_observations) != tuple(c.dependency_standing for c in s.candidates): raise CapabilityReachabilityProjectionError("dependency observations mismatch")
    if tuple(h.authority_observations) != tuple(c.authority_standing for c in s.candidates): raise CapabilityReachabilityProjectionError("authority observations mismatch")
    if tuple(h.unknowns) != tuple(s.unknowns): raise CapabilityReachabilityProjectionError("Unknown references mismatch")
    if tuple(h.conflicts) != tuple(s.conflicts): raise CapabilityReachabilityProjectionError("conflict references mismatch")
    if not s.capability_demand_reference or any(x in s.capability_demand_reference.lower() for x in (" and ", ";")):
        raise CapabilityReachabilityProjectionError("capability demand must name one exact bounded transformation")

def project_capability_reachability(candidate_set: CandidateOperationalRealizationSet, future_handoff: FutureCapabilityReachabilityHandoff) -> CapabilityReachabilityProjection:
    _validate(candidate_set, future_handoff)
    cs=tuple(candidate_set.candidates)
    supporting=tuple(c.candidate_id for c in cs if c.candidate_standing=="supported" and c.dependency_standing=="available" and c.authority_standing=="reachable" and c.mechanism_availability_standing=="available")
    blocked=tuple(c.candidate_id for c in cs if c.candidate_standing in ("supported","unknown") and (c.dependency_standing=="unavailable" or c.authority_standing=="unavailable" or c.mechanism_availability_standing=="unavailable") and c.representation_compatibility=="compatible" and c.methodological_compatibility=="satisfies")
    unsupported=tuple(c.candidate_id for c in cs if c.candidate_standing=="unsupported")
    unknown=tuple(c.candidate_id for c in cs if c.candidate_standing=="unknown" and c.candidate_id not in blocked)
    conflicting=tuple(c.candidate_id for c in cs if c.candidate_standing=="conflict" or c.conflicts)
    dep_block=tuple(c.candidate_id for c in cs if c.dependency_standing=="unavailable")
    auth_block=tuple(c.candidate_id for c in cs if c.authority_standing=="unavailable")
    rep_block=tuple(c.candidate_id for c in cs if c.representation_compatibility=="incompatible")
    meth_block=tuple(c.candidate_id for c in cs if c.methodological_compatibility=="violates")
    gram_ins=tuple(c.candidate_id for c in cs if c.grammar_standing in ("unknown","insufficient","declared_only","recovered_only"))
    beh_con=tuple(c.candidate_id for c in cs if c.behavior_standing=="contradicted")
    unknowns=_uniq(candidate_set.unknowns + tuple(u for c in cs for u in c.unknowns))
    conflicts=_uniq(candidate_set.conflicts + tuple(x for c in cs for x in c.conflicts))
    incomplete=any("candidate_space_incomplete" in x or "candidate_space_unknown" in x for x in unknowns)
    if conflicting or conflicts:
        state="conflict"; reason="preserved candidate conclusions cannot be reconciled lawfully"
    elif supporting:
        state="reachable"; reason="at least one candidate supports the full exact demand under current mechanism, grammar, behavior, representation, method, dependency, and authority state"
    elif blocked and not supporting and all(c.candidate_id in blocked or c.candidate_standing=="unsupported" for c in cs):
        state="blocked"; reason="otherwise sufficient candidates exist, but all are blocked by current dependency or authority state"
    elif not cs:
        state="unknown"; reason="no known realization"
    elif unsupported and len(unsupported)==len(cs) and not incomplete:
        state="unsupported"; reason="all bounded relevant known candidates positively fail one or more required demand dimensions"
    else:
        state="unknown"; reason="current evidence does not establish a supported realization or bounded unsupportedness"
    payload={"probe":candidate_set.probe_request_reference,"demand":candidate_set.capability_demand_reference,"set":candidate_set.set_id,"handoff":_asdict(future_handoff),"candidates":[c.to_json_dict() for c in cs],"state":state,"reason":reason,"convention":CONVENTION}
    pid=_stable("capability-reachability-projection", payload)
    fsh=None
    if state in ("reachable","blocked"):
        fsh=FutureOperationalRealizationSelectionHandoff(pid,candidate_set.probe_request_reference,candidate_set.capability_demand_reference,candidate_set.set_id,state,supporting,blocked,unknown,conflicts,reason,state=="reachable")
    return CapabilityReachabilityProjection("CapabilityReachabilityProjection",pid,candidate_set.probe_request_reference,candidate_set.capability_demand_reference,candidate_set.set_id,_stable("future-capability-reachability-handoff",_asdict(future_handoff)),state,reason,supporting,blocked,unsupported,unknown,conflicting,dep_block,auth_block,rep_block,meth_block,gram_ins,beh_con,candidate_set.no_known_realization_observations,unknowns,conflicts,_summary((c.mechanism_availability_standing for c in cs),"available","unavailable"),_summary((c.dependency_standing for c in cs),"available","unavailable"),_summary((c.authority_standing for c in cs),"reachable","unavailable"),_summary(("sufficient" if c.grammar_standing=="behaviorally_supported" else "insufficient" if c.grammar_standing in ("insufficient","declared_only","recovered_only") else c.grammar_standing for c in cs),"sufficient","insufficient"),_summary((c.behavior_standing for c in cs),"supported","contradicted"),_summary((c.representation_compatibility for c in cs),"compatible","incompatible"),_summary((c.methodological_compatibility for c in cs),"satisfies","violates"),fsh,candidate_set.shared_provenance)

def capability_reachability_projection_json(p: CapabilityReachabilityProjection): return p.to_json_dict()

def format_capability_reachability_projection(p: CapabilityReachabilityProjection) -> str:
    lines=["Capability Reachability Projection",f"projection_id: {p.projection_id}",f"probe_request_reference: {p.probe_request_reference}",f"capability_demand_reference: {p.capability_demand_reference}",f"candidate_set_reference: {p.candidate_set_reference}",f"state: {p.reachability_state}",f"reason: {p.conclusion_reason}",f"read_only: {str(p.read_only).lower()}",f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",f"mutates_cluster: {str(p.mutates_cluster).lower()}"]
    for name, vals in (("supporting_candidates",p.supporting_candidate_references),("blocked_candidates",p.blocked_candidate_references),("unsupported_candidates",p.unsupported_candidate_references),("unknown_candidates",p.unknown_candidate_references),("conflicting_candidates",p.conflicting_candidate_references),("dependency_blockers",p.dependency_blockers),("authority_blockers",p.authority_blockers),("unknowns",p.unknowns),("conflicts",p.conflicts)):
        lines += [f"{name}:"] + ([f"- {x}" for x in vals] or ["- none"])
    lines += ["boundary_notes:"] + [f"- {x}" for x in p.boundary_notes]
    lines.append("selected_candidate: none")
    return "\n".join(lines)
