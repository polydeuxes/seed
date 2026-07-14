"""Read-only examination-method applicability projection for candidate work."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion
from seed_runtime.candidate_examination_work import CandidateExaminationWorkSet
from seed_runtime.examination_frontier import CandidateWork

CONVENTION = "examination_method_applicability_projection_v1"
BOUNDARY_NOTES = (
    "This projection evaluates methodological applicability, not technical compatibility.",
    "Technical compatibility alone does not establish that a manner of examination is lawful for the inquiry.",
    "Applicability does not select, prioritize, authorize, schedule, or execute work.",
    "External grammar applicability does not authorize an external provider invocation.",
    "Fidelity and attribution requirements remain constraints, not priority scores or semantic conclusions.",
    "Inapplicable and Unknown candidates remain preserved.",
    "No interpretation, comparison, recurrence, or knowledge admission occurs.",
    "This artifact is not runtime Evidence or Fact.",
)
STATES = ("applicable", "inapplicable", "unknown", "conflict")

class ExaminationMethodApplicabilityError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _tuple(v: Any=()) -> tuple[str,...]:
    if v is None: return ()
    if not isinstance(v, (list, tuple)) or not all(isinstance(x, str) for x in v):
        raise ExaminationMethodApplicabilityError("expected list of strings")
    return tuple(v)

@dataclass(frozen=True)
class ExaminationMethodApplicabilityTestimony:
    testimony_id: str
    inquiry_reference: str
    candidate_work_id: str = ""
    contract_id: str = ""
    artifact_identity: str = ""
    artifact_hash: str = ""
    method_reference: str = ""
    applicability: str = "unknown"
    reason: str = ""
    fidelity_constraints: tuple[str,...] = ()
    attribution_constraints: tuple[str,...] = ()
    claim_treatment_constraints: tuple[str,...] = ()
    supporting_references: tuple[str,...] = ()
    contradicting_references: tuple[str,...] = ()
    unknowns: tuple[str,...] = ()

    def __post_init__(self):
        if self.applicability not in STATES:
            raise ExaminationMethodApplicabilityError("invalid applicability testimony")
        if not self.testimony_id or not self.inquiry_reference:
            raise ExaminationMethodApplicabilityError("testimony_id and inquiry_reference are required")

    @classmethod
    def from_json_dict(cls, d: dict[str,Any]):
        return cls(
            str(d.get("testimony_id","") or ""), str(d.get("inquiry_reference","") or ""),
            str(d.get("candidate_work_id","") or ""), str(d.get("contract_id","") or ""),
            str(d.get("artifact_identity","") or ""), str(d.get("artifact_hash","") or ""),
            str(d.get("method_reference","") or ""), str(d.get("applicability","unknown") or "unknown"),
            str(d.get("reason","") or ""), _tuple(d.get("fidelity_constraints",())),
            _tuple(d.get("attribution_constraints",())), _tuple(d.get("claim_treatment_constraints",())),
            _tuple(d.get("supporting_references",())), _tuple(d.get("contradicting_references",())), _tuple(d.get("unknowns",())),
        )
    def to_json_dict(self):
        d=asdict(self)
        for k in ("fidelity_constraints","attribution_constraints","claim_treatment_constraints","supporting_references","contradicting_references","unknowns"):
            d[k]=list(d[k])
        return d

@dataclass(frozen=True)
class CandidateMethodApplicabilityRecord:
    candidate_work_id: str; artifact_identity: str; artifact_hash: str; contract_id: str; capability_id: str; method_reference: str; applicability_state: str; applicability_reason: str; fidelity_constraints: tuple[str,...]; attribution_constraints: tuple[str,...]; claim_treatment_constraints: tuple[str,...]; supporting_references: tuple[str,...]; contradicting_references: tuple[str,...]; unknowns: tuple[str,...]; conflict_details: tuple[str,...]
    def to_json_dict(self):
        d=asdict(self)
        for k in ("fidelity_constraints","attribution_constraints","claim_treatment_constraints","supporting_references","contradicting_references","unknowns","conflict_details"):
            d[k]=list(d[k])
        return d

@dataclass(frozen=True)
class ExaminationMethodApplicabilityProjection:
    artifact_type: str; projection_id: str; bounded_inquiry_reference: dict[str,Any]; candidate_work_set_reference: dict[str,Any]; applicability_convention: str; candidate_applicability: tuple[CandidateMethodApplicabilityRecord,...]; applicable_candidate_references: tuple[str,...]; inapplicable_candidate_references: tuple[str,...]; unknown_candidate_references: tuple[str,...]; conflict_candidate_references: tuple[str,...]; projection_unknowns: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self):
        return {"artifact_type":self.artifact_type,"projection_id":self.projection_id,"bounded_inquiry_reference":self.bounded_inquiry_reference,"candidate_work_set_reference":self.candidate_work_set_reference,"applicability_convention":self.applicability_convention,"candidate_applicability":[r.to_json_dict() for r in self.candidate_applicability],"applicable_candidate_references":list(self.applicable_candidate_references),"inapplicable_candidate_references":list(self.inapplicable_candidate_references),"unknown_candidate_references":list(self.unknown_candidate_references),"conflict_candidate_references":list(self.conflict_candidate_references),"projection_unknowns":list(self.projection_unknowns),"boundary_notes":list(self.boundary_notes),"read_only":self.read_only,"writes_event_ledger":self.writes_event_ledger,"mutates_cluster":self.mutates_cluster}
    def to_frontier_candidate_work(self, work_set: CandidateExaminationWorkSet) -> tuple[CandidateWork,...]:
        by={c.candidate_work_id:c for c in work_set.candidate_work}
        allowed=set(self.applicable_candidate_references)
        return tuple(by[cid].to_frontier_candidate_work() for cid in self.applicable_candidate_references if cid in by and by[cid].compatibility_observation == "compatible")

def project_examination_method_applicability(q: BoundedConstitutionalQuestion, work_set: CandidateExaminationWorkSet, testimony: tuple[ExaminationMethodApplicabilityTestimony,...]=(), projection_unknowns: tuple[str,...]=()) -> ExaminationMethodApplicabilityProjection:
    if not isinstance(q, BoundedConstitutionalQuestion): raise ExaminationMethodApplicabilityError("bounded inquiry input is structurally invalid")
    by={c.candidate_work_id:c for c in work_set.candidate_work}
    for t in testimony:
        if t.candidate_work_id and t.candidate_work_id not in by: raise ExaminationMethodApplicabilityError("unknown_candidate_work_id")
        if not t.candidate_work_id and t.contract_id and not any(c.contract_id==t.contract_id for c in work_set.candidate_work): raise ExaminationMethodApplicabilityError("unknown_contract_id")
    records=[]
    for c in sorted(work_set.candidate_work, key=lambda x:x.candidate_work_id):
        relevant=[]; ignored=[]
        for t in testimony:
            targets=(t.candidate_work_id==c.candidate_work_id) or (not t.candidate_work_id and t.contract_id==c.contract_id)
            if not targets: continue
            mism=[]
            if t.inquiry_reference != q.bounded_question_id: mism.append("mismatched inquiry reference")
            if t.artifact_identity and t.artifact_identity != c.artifact_identity: mism.append("mismatched artifact identity")
            if t.artifact_hash and t.artifact_hash != c.artifact_hash: mism.append("mismatched artifact version")
            if mism: ignored.append(f"{t.testimony_id}: " + "; ".join(mism)); continue
            relevant.append(t)
        states={t.applicability for t in relevant if t.applicability != "unknown"}
        constraints_payload={(t.fidelity_constraints,t.attribution_constraints,t.claim_treatment_constraints) for t in relevant}
        conflict = len(states) > 1 or len(constraints_payload) > 1 or any(t.contradicting_references for t in relevant)
        if conflict:
            state="conflict"; reason="conflicting methodology testimony or required constraints"
        elif len(relevant)==0:
            state="unknown"; reason="no matching methodology testimony establishes applicability"
        elif any(t.applicability == "inapplicable" for t in relevant):
            state="inapplicable"; reason=relevant[0].reason or "explicit methodology testimony establishes inapplicability"
        elif all(t.applicability == "applicable" for t in relevant) and relevant:
            state="applicable"; reason=relevant[0].reason or "explicit methodology testimony establishes applicability"
        else:
            state="unknown"; reason="methodology testimony is incomplete or Unknown"
        fidelity=tuple(sorted({x for t in relevant for x in t.fidelity_constraints}))
        attribution=tuple(sorted({x for t in relevant for x in t.attribution_constraints}))
        claim=tuple(sorted({x for t in relevant for x in t.claim_treatment_constraints}))
        supports=tuple(sorted({x for t in relevant for x in ((t.supporting_references or (t.testimony_id,))) }))
        contradicts=tuple(sorted(set(ignored) | {x for t in relevant for x in t.contradicting_references}))
        unknowns=tuple(sorted(set(c.unknowns) | {x for t in relevant for x in t.unknowns} | (set() if relevant else {"methodology_evidence_absent"})))
        conflicts=tuple(sorted({f"{t.testimony_id}:{t.applicability}" for t in relevant})) if conflict else ()
        method=",".join(sorted({t.method_reference for t in relevant if t.method_reference}))
        records.append(CandidateMethodApplicabilityRecord(c.candidate_work_id,c.artifact_identity,c.artifact_hash,c.contract_id,c.capability_id,method,state,reason,fidelity,attribution,claim,supports,contradicts,unknowns,conflicts))
    applicable=tuple(r.candidate_work_id for r in records if r.applicability_state=="applicable")
    inapplicable=tuple(r.candidate_work_id for r in records if r.applicability_state=="inapplicable")
    conflicts=tuple(r.candidate_work_id for r in records if r.applicability_state=="conflict")
    unknown=tuple(r.candidate_work_id for r in records if r.applicability_state in ("unknown","conflict"))
    pid=_stable("examination-method-applicability", {"inquiry":q.bounded_question_id,"work_set":work_set.work_set_id,"convention":CONVENTION,"records":[r.to_json_dict() for r in records]})
    return ExaminationMethodApplicabilityProjection("ExaminationMethodApplicabilityProjection",pid,{"bounded_question_id":q.bounded_question_id,"inquiry_provenance":q.inquiry_provenance,"bounded_question":q.bounded_question},{"work_set_id":work_set.work_set_id,"corpus_id":work_set.corpus_id},CONVENTION,tuple(records),applicable,inapplicable,unknown,conflicts,projection_unknowns)

def examination_method_applicability_json(p): return p.to_json_dict()

def format_examination_method_applicability(p):
    lines=["Examination Method Applicability Projection",f"projection_id: {p.projection_id}",f"applicability_convention: {p.applicability_convention}",f"read_only: {str(p.read_only).lower()}",f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",f"mutates_cluster: {str(p.mutates_cluster).lower()}","candidate_applicability:"]
    lines += [f"- {r.candidate_work_id}: {r.applicability_state}; method={r.method_reference or 'unknown'}; reason={r.applicability_reason}" for r in p.candidate_applicability] or ["- none"]
    lines += ["boundary_notes:"]+[f"- {n}" for n in p.boundary_notes]
    return "\n".join(lines)
