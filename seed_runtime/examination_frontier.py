"""Immutable read-only examination frontier projection from explicit campaign inputs."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion

FRONTIER_CONVENTION = "examination_frontier_projection_v1"
BOUNDARY_NOTES = (
    "The frontier is a read-only projection of supplied corpus and work visibility.",
    "The frontier does not discover corpus members.",
    "The frontier does not discover compatible capabilities or projections.",
    "Eligible work has not been selected, authorized, or executed.",
    "Examined work is not necessarily understood, admitted as knowledge, or complete.",
    "Blocked work is distinct from unsupported work.",
    "Failed work is distinct from blocked or permanently unsupported work.",
    "Unknown work remains unclassified because evidence is insufficient.",
    "The frontier is not a scheduler, work queue, priority ranking, or campaign completion verdict.",
    "No comparison, recurrence, semantic interpretation, or responsibility recovery occurs.",
    "This frontier is not runtime Evidence or Fact.",
)

class ExaminationFrontierError(ValueError): pass

def _req(data: dict[str, Any], key: str) -> str:
    v=data.get(key)
    if not isinstance(v,str) or not v: raise ExaminationFrontierError(f"{key} is required")
    return v

def _str_tuple(v: Any) -> tuple[str,...]:
    if v is None: return ()
    if not isinstance(v, list|tuple) or not all(isinstance(x,str) for x in v): raise ExaminationFrontierError("expected list of strings")
    return tuple(v)

def _stable(prefix: str, payload: Any) -> str:
    enc=json.dumps(payload, sort_keys=True, separators=(",",":"), ensure_ascii=False)
    return prefix+":"+hashlib.sha256(enc.encode()).hexdigest()

@dataclass(frozen=True)
class CorpusMember:
    member_id: str; substrate_kind: str; artifact_identity: str; artifact_hash: str=""; material_reference: str=""; scope_status: str="in_scope"; provenance: tuple[str,...]=(); authorization_testimony: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def to_json_dict(self): return asdict(self) | {"provenance":list(self.provenance),"authorization_testimony":list(self.authorization_testimony),"unknowns":list(self.unknowns)}
    @classmethod
    def from_json_dict(cls,d):
        return cls(_req(d,"member_id"), _req(d,"substrate_kind"), _req(d,"artifact_identity"), str(d.get("artifact_hash","") or ""), str(d.get("material_reference","") or ""), str(d.get("scope_status","in_scope") or "in_scope"), _str_tuple(d.get("provenance",())), _str_tuple(d.get("authorization_testimony",())), _str_tuple(d.get("unknowns",())))

@dataclass(frozen=True)
class WorkResultReference:
    result_id: str; corpus_member_id: str; artifact_hash: str; work_kind: str; capability_id: str; convention: str; result_state: str; provenance: tuple[str,...]=()
    def to_json_dict(self): return asdict(self) | {"provenance":list(self.provenance)}
    @classmethod
    def from_json_dict(cls,d): return cls(_req(d,"result_id"),_req(d,"corpus_member_id"),str(d.get("artifact_hash","") or ""),_req(d,"work_kind"),str(d.get("capability_id","") or ""),str(d.get("convention","") or ""),_req(d,"result_state"),_str_tuple(d.get("provenance",())))

@dataclass(frozen=True)
class CandidateWork:
    candidate_work_id: str; corpus_member_id: str; work_kind: str; capability_id: str=""; convention: str=""; compatibility_status: str="unknown"; authorization_status: str="unknown"; existing_results: tuple[WorkResultReference,...]=(); blockers: tuple[str,...]=(); deferral_testimony: tuple[str,...]=(); failure_references: tuple[str,...]=(); supplied_status: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    @classmethod
    def from_json_dict(cls,d):
        return cls(_req(d,"candidate_work_id"),_req(d,"corpus_member_id"),_req(d,"work_kind"),str(d.get("capability_id","") or ""),str(d.get("convention","") or ""),str(d.get("compatibility_status","unknown") or "unknown"),str(d.get("authorization_status","unknown") or "unknown"),tuple(WorkResultReference.from_json_dict(x) for x in d.get("existing_results",()) ),_str_tuple(d.get("blockers",())),_str_tuple(d.get("deferral_testimony",())),_str_tuple(d.get("failure_references",())),str(d.get("supplied_status","") or ""),_str_tuple(d.get("provenance",())),_str_tuple(d.get("unknowns",())))

@dataclass(frozen=True)
class FrontierClassification:
    eligible: bool; examined: bool; blocked: bool; unsupported: bool; deferred: bool; failed: bool; unknown: bool; conflict: bool; newly_eligible: str="unresolved_no_previous_frontier_input"
    def to_json_dict(self): return asdict(self)

@dataclass(frozen=True)
class FrontierWorkItem:
    work_item_id: str; candidate_work_id: str; corpus_member_id: str; artifact_identity: str; artifact_hash: str; work_kind: str; capability_id: str; convention: str; classification: FrontierClassification; reasons: tuple[str,...]; existing_result_references: tuple[WorkResultReference,...]; blocker_references: tuple[str,...]; deferral_testimony: tuple[str,...]; failure_references: tuple[str,...]; unknowns: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES
    def to_json_dict(self):
        d=asdict(self); d["classification"]=self.classification.to_json_dict(); d["reasons"]=list(self.reasons); d["existing_result_references"]=[r.to_json_dict() for r in self.existing_result_references]; d["blocker_references"]=list(self.blocker_references); d["deferral_testimony"]=list(self.deferral_testimony); d["failure_references"]=list(self.failure_references); d["unknowns"]=list(self.unknowns); d["boundary_notes"]=list(self.boundary_notes); return d

@dataclass(frozen=True)
class ExaminationFrontier:
    artifact_type: str; frontier_id: str; inquiry_reference: dict[str,Any]; corpus_id: str; corpus_label: str; frontier_convention: str; corpus_members: tuple[CorpusMember,...]; work_items: tuple[FrontierWorkItem,...]; summary_counts: dict[str,int]; frontier_unknowns: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self): return {"artifact_type":self.artifact_type,"frontier_id":self.frontier_id,"inquiry_reference":self.inquiry_reference,"corpus_id":self.corpus_id,"corpus_label":self.corpus_label,"frontier_convention":self.frontier_convention,"corpus_members":[m.to_json_dict() for m in self.corpus_members],"work_items":[i.to_json_dict() for i in self.work_items],"summary_counts":self.summary_counts,"frontier_unknowns":list(self.frontier_unknowns),"boundary_notes":list(self.boundary_notes),"read_only":self.read_only,"writes_event_ledger":self.writes_event_ledger,"mutates_cluster":self.mutates_cluster}

def input_from_json_dict(data: dict[str,Any]):
    qd=data.get("bounded_inquiry")
    if not isinstance(qd,dict): raise ExaminationFrontierError("bounded_inquiry is required")
    q=BoundedConstitutionalQuestion(**qd)
    corpus=data.get("corpus")
    if not isinstance(corpus,dict): raise ExaminationFrontierError("corpus is required")
    members=tuple(CorpusMember.from_json_dict(x) for x in corpus.get("members",()))
    works=tuple(CandidateWork.from_json_dict(x) for x in data.get("candidate_work",()))
    return q, _req(corpus,"corpus_id"), str(corpus.get("corpus_label","") or ""), members, works, _str_tuple(corpus.get("unknowns",()))

def _work_identity(corpus_id, m: CorpusMember, w: CandidateWork):
    return _stable("examination-frontier-work", {"corpus_id":corpus_id,"member_id":m.member_id,"artifact_identity":m.artifact_identity,"artifact_hash":m.artifact_hash,"work_kind":w.work_kind,"capability_id":w.capability_id,"convention":w.convention})

def project_examination_frontier(q: BoundedConstitutionalQuestion, corpus_id: str, corpus_label: str, members: tuple[CorpusMember,...], works: tuple[CandidateWork,...], frontier_unknowns: tuple[str,...]=()) -> ExaminationFrontier:
    if not isinstance(q, BoundedConstitutionalQuestion): raise ExaminationFrontierError("bounded inquiry input is structurally invalid")
    if not corpus_id: raise ExaminationFrontierError("corpus_id is required")
    by={}
    for m in members:
        if m.member_id in by: raise ExaminationFrontierError("duplicate_corpus_member_id")
        by[m.member_id]=m
    seen=set(); items=[]
    for w in works:
        if w.candidate_work_id in seen: raise ExaminationFrontierError("duplicate_candidate_work_id")
        seen.add(w.candidate_work_id)
        if w.corpus_member_id not in by: raise ExaminationFrontierError("unknown_corpus_member")
        m=by[w.corpus_member_id]
        if w.compatibility_status == "compatible" and not w.capability_id: raise ExaminationFrontierError("capability_id is required")
        reasons=[]; unknowns=list(w.unknowns); conflict=False
        examined=False
        for r in w.existing_results:
            if (r.corpus_member_id,r.artifact_hash,r.work_kind,r.capability_id,r.convention)!=(m.member_id,m.artifact_hash,w.work_kind,w.capability_id,w.convention):
                raise ExaminationFrontierError("existing_result_work_mismatch")
            if r.result_state == "completed": examined=True; reasons.append(f"matching completed result: {r.result_id}")
        unsupported=w.compatibility_status == "unsupported"
        blocked=bool(w.blockers); deferred=bool(w.deferral_testimony); failed=bool(w.failure_references)
        if unsupported: reasons.append("supplied compatibility testimony establishes no compatible implementation")
        if blocked: reasons.append("active blocker testimony supplied")
        if deferred: reasons.append("explicit deferral testimony supplied")
        if failed: reasons.append("failed attempt testimony supplied")
        if w.compatibility_status not in ("compatible","unsupported"):
            unknowns.append("compatibility_status unknown")
        if w.authorization_status not in ("authorized","not_applicable"):
            unknowns.append("authorization_status unknown")
        if w.supplied_status == "eligible" and (examined or unsupported or blocked or deferred or unknowns):
            conflict=True; reasons.append("caller supplied eligible conflicts with status evidence")
        eligible=(w.compatibility_status=="compatible" and w.authorization_status in ("authorized","not_applicable") and not examined and not blocked and not unsupported and not deferred and not unknowns)
        unknown=bool(unknowns) or conflict
        if eligible: reasons.append("compatible, authorized or not applicable, unexamined, nondeferred, unblocked, and no required Unknowns")
        if not reasons: reasons.append("insufficient supplied evidence for deterministic classification")
        cls=FrontierClassification(eligible,examined,blocked,unsupported,deferred,failed,unknown,conflict)
        items.append(FrontierWorkItem(_work_identity(corpus_id,m,w),w.candidate_work_id,m.member_id,m.artifact_identity,m.artifact_hash,w.work_kind,w.capability_id,w.convention,cls,tuple(reasons),w.existing_results,w.blockers,w.deferral_testimony,w.failure_references,tuple(unknowns)))
    items=tuple(sorted(items,key=lambda i:(i.work_item_id,i.candidate_work_id)))
    counts={k:sum(1 for i in items if getattr(i.classification,k)) for k in ("eligible","examined","blocked","unsupported","deferred","failed","unknown","conflict")}
    fid=_stable("examination-frontier", {"inquiry":q.bounded_question_id,"corpus_id":corpus_id,"convention":FRONTIER_CONVENTION,"work_item_ids":[i.work_item_id for i in items]})
    return ExaminationFrontier("ExaminationFrontier", fid, {"bounded_question_id":q.bounded_question_id,"inquiry_provenance":q.inquiry_provenance,"bounded_question":q.bounded_question}, corpus_id, corpus_label, FRONTIER_CONVENTION, tuple(sorted(members,key=lambda m:m.member_id)), items, counts, frontier_unknowns)

def examination_frontier_json(f: ExaminationFrontier): return f.to_json_dict()

def format_examination_frontier(f: ExaminationFrontier) -> str:
    out=["Examination Frontier",f"frontier_id: {f.frontier_id}",f"corpus_id: {f.corpus_id}",f"frontier_convention: {f.frontier_convention}",f"read_only: {str(f.read_only).lower()}",f"writes_event_ledger: {str(f.writes_event_ledger).lower()}",f"mutates_cluster: {str(f.mutates_cluster).lower()}","summary_counts:"]
    out += [f"- {k}: {v}" for k,v in sorted(f.summary_counts.items())]
    out += ["work_items:"]
    for i in f.work_items:
        flags=[k for k,v in i.classification.to_json_dict().items() if v is True]
        out.append(f"- {i.work_item_id}: {i.work_kind} on {i.corpus_member_id} [{', '.join(flags) or 'none'}]")
        out += [f"  reason: {r}" for r in i.reasons]
    out += ["boundary_notes:"] + [f"- {n}" for n in f.boundary_notes]
    return "\n".join(out)
