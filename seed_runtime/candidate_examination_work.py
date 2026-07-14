"""Read-only candidate examination work projection from explicit corpus and contract visibility."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.examination_frontier import CandidateWork

CONVENTION = "candidate_examination_work_projection_v1"
BOUNDARY_NOTES = (
    "Candidate work is derived from explicit corpus membership, known representations, and visible contracts.",
    "A candidate work record is not selected, eligible, authorized, scheduled, or executed.",
    "Contract compatibility does not establish capability sufficiency.",
    "Missing prerequisites are preserved without being classified as blockers.",
    "Unavailable capability is distinct from incompatible representation.",
    "No semantic interpretation, comparison, recurrence, priority, or campaign planning occurs.",
    "This artifact is not runtime Evidence or Fact.",
)
EMIT_OBSERVATIONS = {"compatible","missing_required_representation","capability_unavailable","contract_unknown","representation_unknown"}

class CandidateExaminationWorkError(ValueError): pass

def _req(d,k):
    v=d.get(k)
    if not isinstance(v,str) or not v: raise CandidateExaminationWorkError(f"{k} is required")
    return v

def _tuple(v=()):
    if v is None: return ()
    if not isinstance(v, (list,tuple)) or not all(isinstance(x,str) for x in v): raise CandidateExaminationWorkError("expected list of strings")
    return tuple(v)

def _stable(prefix,payload):
    return prefix+":"+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

@dataclass(frozen=True)
class RepresentationVisibility:
    representation_id: str; representation_kind: str; artifact_identity: str; artifact_hash: str=""; convention: str=""; evidence_status: str="known"; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    @classmethod
    def from_json_dict(cls,d): return cls(_req(d,"representation_id"),_req(d,"representation_kind"),_req(d,"artifact_identity"),str(d.get("artifact_hash","") or ""),str(d.get("convention","") or ""),str(d.get("evidence_status","known") or "known"),_tuple(d.get("provenance",())),_tuple(d.get("unknowns",())))
    def to_json_dict(self):
        x=asdict(self); x["provenance"]=list(self.provenance); x["unknowns"]=list(self.unknowns); return x

@dataclass(frozen=True)
class BoundedCorpusMember:
    member_id: str; substrate_kind: str; artifact_identity: str; artifact_hash: str=""; representations: tuple[RepresentationVisibility,...]=(); provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    @classmethod
    def from_json_dict(cls,d): return cls(_req(d,"member_id"),_req(d,"substrate_kind"),_req(d,"artifact_identity"),str(d.get("artifact_hash","") or ""),tuple(RepresentationVisibility.from_json_dict(x) for x in d.get("representations",())),_tuple(d.get("provenance",())),_tuple(d.get("unknowns",())))
    def to_json_dict(self):
        return {"member_id":self.member_id,"substrate_kind":self.substrate_kind,"artifact_identity":self.artifact_identity,"artifact_hash":self.artifact_hash,"representations":[r.to_json_dict() for r in self.representations],"provenance":list(self.provenance),"unknowns":list(self.unknowns)}

@dataclass(frozen=True)
class ExaminationWorkContract:
    contract_id: str; capability_id: str; work_kind: str; accepted_input_representation: str; produced_output_representation: str; convention: str; availability: str="available"; applicable_member_ids: tuple[str,...]=(); provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    @classmethod
    def from_json_dict(cls,d): return cls(_req(d,"contract_id"),_req(d,"capability_id"),_req(d,"work_kind"),_req(d,"accepted_input_representation"),_req(d,"produced_output_representation"),_req(d,"convention"),str(d.get("availability","available") or "available"),_tuple(d.get("applicable_member_ids",())),_tuple(d.get("provenance",())),_tuple(d.get("unknowns",())))
    def to_json_dict(self):
        x=asdict(self); x["applicable_member_ids"]=list(self.applicable_member_ids); x["provenance"]=list(self.provenance); x["unknowns"]=list(self.unknowns); return x

@dataclass(frozen=True)
class CandidateExaminationWorkRecord:
    candidate_work_id: str; corpus_member_id: str; artifact_identity: str; artifact_hash: str; contract_id: str; capability_id: str; work_kind: str; required_input_representation: str; available_matching_representation: str; produced_representation: str; contract_convention: str; compatibility_observation: str; missing_prerequisites: tuple[str,...]=(); availability_observation: str="available"; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def to_json_dict(self):
        x=asdict(self); x["missing_prerequisites"]=list(self.missing_prerequisites); x["provenance"]=list(self.provenance); x["unknowns"]=list(self.unknowns); return x
    def to_frontier_candidate_work(self) -> CandidateWork:
        status = "compatible" if self.compatibility_observation == "compatible" else "unknown"
        unknowns = self.unknowns + (() if status == "compatible" else (self.compatibility_observation,))
        return CandidateWork(self.candidate_work_id,self.corpus_member_id,self.work_kind,self.capability_id,self.contract_convention,status,"unknown",(),(),(),(),"",self.provenance,unknowns)

@dataclass(frozen=True)
class CandidateExaminationWorkSet:
    artifact_type: str; work_set_id: str; corpus_id: str; contract_set_provenance: tuple[str,...]; candidate_work: tuple[CandidateExaminationWorkRecord,...]; exclusions: tuple[dict[str,str],...]; set_unknowns: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False; projection_convention: str=CONVENTION
    def to_json_dict(self): return {"artifact_type":self.artifact_type,"work_set_id":self.work_set_id,"corpus_id":self.corpus_id,"contract_set_provenance":list(self.contract_set_provenance),"candidate_work":[c.to_json_dict() for c in self.candidate_work],"exclusions":list(self.exclusions),"set_unknowns":list(self.set_unknowns),"boundary_notes":list(self.boundary_notes),"read_only":self.read_only,"writes_event_ledger":self.writes_event_ledger,"mutates_cluster":self.mutates_cluster,"projection_convention":self.projection_convention}
    def to_frontier_candidate_work(self): return tuple(c.to_frontier_candidate_work() for c in self.candidate_work)

def project_candidate_examination_work(corpus_id: str, members: tuple[BoundedCorpusMember,...], contracts: tuple[ExaminationWorkContract,...], contract_set_provenance: tuple[str,...]=(), set_unknowns: tuple[str,...]=()) -> CandidateExaminationWorkSet:
    if not corpus_id: raise CandidateExaminationWorkError("corpus_id is required")
    by={}
    for m in members:
        if m.member_id in by: raise CandidateExaminationWorkError("duplicate_corpus_member_id")
        by[m.member_id]=m
    seen_contract=set()
    for c in contracts:
        if c.contract_id in seen_contract: raise CandidateExaminationWorkError("duplicate_contract_id")
        seen_contract.add(c.contract_id)
        for mid in c.applicable_member_ids:
            if mid not in by: raise CandidateExaminationWorkError("unknown_corpus_member")
    out=[]; exclusions=[]; ids=set()
    for c in sorted(contracts,key=lambda x:x.contract_id):
        target_ids=c.applicable_member_ids or tuple(sorted(by))
        for mid in target_ids:
            m=by[mid]
            reps=tuple(r for r in m.representations if r.representation_kind==c.accepted_input_representation)
            unknown_rep=any(r.evidence_status=="unknown" for r in m.representations)
            if c.availability == "unknown": obs="contract_unknown"
            elif c.availability == "unavailable": obs="capability_unavailable"
            elif reps: obs="compatible"
            elif unknown_rep: obs="representation_unknown"
            else: obs="missing_required_representation"
            if obs not in EMIT_OBSERVATIONS:
                exclusions.append({"corpus_member_id":mid,"contract_id":c.contract_id,"reason":"incompatible"}); continue
            match=reps[0].representation_id if reps else ""
            missing=() if reps else (c.accepted_input_representation,)
            cid=_stable("candidate-examination-work",{"corpus_id":corpus_id,"corpus_member_id":m.member_id,"artifact_identity":m.artifact_identity,"artifact_hash":m.artifact_hash,"contract_id":c.contract_id,"capability_id":c.capability_id,"input_representation":c.accepted_input_representation,"output_representation":c.produced_output_representation,"contract_convention":c.convention})
            if cid in ids: raise CandidateExaminationWorkError("duplicate_candidate_work_id")
            ids.add(cid)
            out.append(CandidateExaminationWorkRecord(cid,m.member_id,m.artifact_identity,m.artifact_hash,c.contract_id,c.capability_id,c.work_kind,c.accepted_input_representation,match,c.produced_output_representation,c.convention,obs,missing,c.availability,m.provenance+c.provenance,m.unknowns+c.unknowns))
    out=tuple(sorted(out,key=lambda r:(r.corpus_member_id,r.contract_id,r.candidate_work_id)))
    wid=_stable("candidate-examination-work-set",{"corpus_id":corpus_id,"ids":[r.candidate_work_id for r in out],"convention":CONVENTION})
    return CandidateExaminationWorkSet("CandidateExaminationWorkSet",wid,corpus_id,contract_set_provenance,out,tuple(exclusions),set_unknowns)

def candidate_examination_work_json(ws): return ws.to_json_dict()

def format_candidate_examination_work(ws):
    lines=["Candidate Examination Work Projection",f"work_set_id: {ws.work_set_id}",f"corpus_id: {ws.corpus_id}",f"projection_convention: {ws.projection_convention}",f"read_only: {str(ws.read_only).lower()}",f"writes_event_ledger: {str(ws.writes_event_ledger).lower()}",f"mutates_cluster: {str(ws.mutates_cluster).lower()}","candidate_work:"]
    lines += [f"- {c.candidate_work_id}: {c.work_kind} for {c.corpus_member_id}; observation={c.compatibility_observation}; availability={c.availability_observation}" for c in ws.candidate_work] or ["- none"]
    lines += ["boundary_notes:"]+[f"- {n}" for n in ws.boundary_notes]
    return "\n".join(lines)

def input_from_json_dict(data: dict[str,Any]):
    if not isinstance(data,dict): raise CandidateExaminationWorkError("input must be an object")
    corpus=data.get("corpus")
    if not isinstance(corpus,dict): raise CandidateExaminationWorkError("corpus is required")
    members=tuple(BoundedCorpusMember.from_json_dict(x) for x in corpus.get("members",()))
    contracts=tuple(ExaminationWorkContract.from_json_dict(x) for x in data.get("contracts",()))
    ignored=data.get("candidate_work_names",())
    if ignored is not None and not isinstance(ignored,(list,tuple)): raise CandidateExaminationWorkError("candidate_work_names must be a list")
    return _req(corpus,"corpus_id"), members, contracts, _tuple(data.get("contract_set_provenance",())), _tuple(corpus.get("unknowns",()))
