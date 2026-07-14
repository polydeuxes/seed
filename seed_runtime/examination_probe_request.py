"""Immutable examination probe request binding from selected work to exact request meaning."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.candidate_examination_work import CandidateExaminationWorkSet
from seed_runtime.examination_frontier import ExaminationFrontier
from seed_runtime.examination_method_applicability import ExaminationMethodApplicabilityProjection
from seed_runtime.examination_work_selection import ExaminationWorkSelection, FutureProbeRequestHandoff

CONVENTION = "examination_probe_request_v1"
REQUEST_STATES = ("bound", "unknown", "conflict", "invalid")
BOUNDARY_NOTES = (
    "This artifact binds selected examination meaning; it does not choose an operational realization.",
    "The work contract is not a registered operation.",
    "The requested probe contains no provider, tool name, or operation arguments.",
    "Methodological, fidelity, attribution, and claim-treatment constraints remain request constraints.",
    "The request does not authorize, schedule, execute, or create a pending action.",
    "A bound request may remain operationally unrealizable.",
    "This artifact is not runtime Evidence or Fact.",
)

class ExaminationProbeRequestError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

@dataclass(frozen=True)
class OperationalRealizationHandoff:
    probe_request_id: str; inquiry_identity: str; artifact_identity: str; artifact_hash: str; work_contract_reference: str; capability_identity: str; required_input_representation: str; requested_output_representation: str; method_constraint_reference: dict[str, Any]; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self): return asdict(self)

@dataclass(frozen=True)
class ExaminationProbeRequest:
    artifact_type: str; request_id: str; request_state: str; inquiry_reference: dict[str, Any]; selection_reference: dict[str, Any]; frontier_reference: dict[str, Any]; policy_reference: dict[str, Any]; selected_work_reference: str; candidate_work_reference: str; work_contract_reference: str; corpus_member_reference: str; artifact_identity: str; artifact_hash: str; work_kind: str; capability_identity: str; required_input_representation: str; requested_output_representation: str; contract_convention: str; requested_outcome: str; selection_reason: str; method_reference: str; method_applicability_reference: dict[str, Any]; fidelity_constraints: tuple[str,...]; attribution_constraints: tuple[str,...]; claim_treatment_constraints: tuple[str,...]; supporting_references: tuple[str,...]; provenance: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False; request_convention: str=CONVENTION
    def to_json_dict(self):
        d=asdict(self)
        for k in ("fidelity_constraints","attribution_constraints","claim_treatment_constraints","supporting_references","provenance","unknowns","conflicts","boundary_notes"):
            d[k]=list(getattr(self,k))
        return d
    def to_operational_realization_handoff(self) -> OperationalRealizationHandoff | None:
        if self.request_state != "bound": return None
        return OperationalRealizationHandoff(self.request_id, str(self.inquiry_reference.get("bounded_question_id", "")), self.artifact_identity, self.artifact_hash, self.work_contract_reference, self.capability_identity, self.required_input_representation, self.requested_output_representation, self.method_applicability_reference)

def _only_selected(selection: ExaminationWorkSelection) -> str:
    if selection.selection_state != "selected" or not selection.selected_work_reference or not selection.future_probe_request_handoff:
        raise ExaminationProbeRequestError("selection must contain exactly one selected work item")
    return selection.selected_work_reference

def bind_examination_probe_request(selection: ExaminationWorkSelection, handoff: FutureProbeRequestHandoff, frontier: ExaminationFrontier, work_set: CandidateExaminationWorkSet, applicability: ExaminationMethodApplicabilityProjection) -> ExaminationProbeRequest:
    selected=_only_selected(selection)
    if handoff.selection_id != selection.selection_id: raise ExaminationProbeRequestError("handoff does not belong to supplied selection")
    if handoff.selected_work_reference != selected: raise ExaminationProbeRequestError("handoff selected work does not match selection")
    if handoff.frontier_reference.get("frontier_id") != frontier.frontier_id or selection.frontier_reference.get("frontier_id") != frontier.frontier_id: raise ExaminationProbeRequestError("handoff does not reference supplied frontier")
    if len({str(x.get("bounded_question_id", "")) for x in (selection.inquiry_reference, handoff.inquiry_reference, frontier.inquiry_reference, applicability.bounded_inquiry_reference)}) != 1: raise ExaminationProbeRequestError("inquiry references do not match")
    if handoff.method_constraint_reference.get("projection_id") != applicability.projection_id: raise ExaminationProbeRequestError("handoff method applicability reference does not match supplied projection")
    if applicability.candidate_work_set_reference.get("work_set_id") != work_set.work_set_id: raise ExaminationProbeRequestError("method applicability does not reference supplied candidate work set")
    frontier_by={i.work_item_id:i for i in frontier.work_items}
    if selected not in frontier_by: raise ExaminationProbeRequestError("selected frontier work is absent")
    f=frontier_by[selected]
    if f.work_item_id != handoff.selected_work_reference: raise ExaminationProbeRequestError("selected frontier work is not the work named by handoff")
    cand_by={c.candidate_work_id:c for c in work_set.candidate_work}
    if f.candidate_work_id not in cand_by: raise ExaminationProbeRequestError("candidate-work record is absent")
    c=cand_by[f.candidate_work_id]
    if c.candidate_work_id != f.candidate_work_id: raise ExaminationProbeRequestError("candidate identity mismatch")
    if (c.artifact_identity, c.artifact_hash) != (f.artifact_identity, f.artifact_hash): raise ExaminationProbeRequestError("artifact identity or version mismatch")
    if (c.corpus_member_id, c.work_kind, c.capability_id, c.contract_convention) != (f.corpus_member_id, f.work_kind, f.capability_id, f.convention): raise ExaminationProbeRequestError("capability, work kind, or convention mismatch")
    rec_by={r.candidate_work_id:r for r in applicability.candidate_applicability}
    if c.candidate_work_id not in rec_by: raise ExaminationProbeRequestError("method-applicability record is absent")
    m=rec_by[c.candidate_work_id]
    if m.applicability_state == "conflict" or m.conflict_details: raise ExaminationProbeRequestError("method applicability has unresolved conflict")
    if m.applicability_state != "applicable": raise ExaminationProbeRequestError(f"method applicability is {m.applicability_state}")
    if (m.artifact_identity, m.artifact_hash) != (c.artifact_identity, c.artifact_hash): raise ExaminationProbeRequestError("method constraints artifact version mismatch")
    if (m.contract_id, m.capability_id) != (c.contract_id, c.capability_id): raise ExaminationProbeRequestError("method constraints contract or capability mismatch")
    requested_outcome=f"produce {c.produced_representation} from {c.required_input_representation} for artifact {c.artifact_identity}@{c.artifact_hash}"
    rid=_stable("examination-probe-request", {"inquiry":selection.inquiry_reference.get("bounded_question_id"),"selection":selection.selection_id,"selected_work":selected,"candidate_work":c.candidate_work_id,"work_contract":c.contract_id,"artifact_identity":c.artifact_identity,"artifact_hash":c.artifact_hash,"method_applicability":applicability.projection_id,"convention":CONVENTION})
    return ExaminationProbeRequest("ExaminationProbeRequest", rid, "bound", selection.inquiry_reference, {"selection_id":selection.selection_id,"selection_convention":"examination_work_selection_v1"}, {"frontier_id":frontier.frontier_id,"frontier_convention":frontier.frontier_convention}, handoff.policy_reference, f.work_item_id, c.candidate_work_id, c.contract_id, c.corpus_member_id, c.artifact_identity, c.artifact_hash, c.work_kind, c.capability_id, c.required_input_representation, c.produced_representation, c.contract_convention, requested_outcome, handoff.selection_reason, m.method_reference, {"projection_id":applicability.projection_id,"applicability_convention":applicability.applicability_convention,"candidate_work_id":m.candidate_work_id}, m.fidelity_constraints, m.attribution_constraints, m.claim_treatment_constraints, m.supporting_references, tuple(dict.fromkeys(c.provenance + m.supporting_references + (selection.selection_id, frontier.frontier_id, work_set.work_set_id, applicability.projection_id))), tuple(dict.fromkeys(c.unknowns + m.unknowns)), (), BOUNDARY_NOTES)

def examination_probe_request_json(r: ExaminationProbeRequest): return r.to_json_dict()

def format_examination_probe_request(r: ExaminationProbeRequest) -> str:
    lines=["Examination Probe Request", f"request_id: {r.request_id}", f"request_state: {r.request_state}", f"selected_work_reference: {r.selected_work_reference}", f"candidate_work_reference: {r.candidate_work_reference}", f"work_contract_reference: {r.work_contract_reference}", f"artifact: {r.artifact_identity}@{r.artifact_hash}", f"requested_outcome: {r.requested_outcome}", f"representations: {r.required_input_representation} -> {r.requested_output_representation}", f"selection_reason: {r.selection_reason}", f"method_reference: {r.method_reference or 'unknown'}", f"read_only: {str(r.read_only).lower()}", f"writes_event_ledger: {str(r.writes_event_ledger).lower()}", f"mutates_cluster: {str(r.mutates_cluster).lower()}", "fidelity_constraints:"]
    lines += [f"- {x}" for x in r.fidelity_constraints] or ["- none"]
    lines += ["attribution_constraints:"] + ([f"- {x}" for x in r.attribution_constraints] or ["- none"])
    lines += ["claim_treatment_constraints:"] + ([f"- {x}" for x in r.claim_treatment_constraints] or ["- none"])
    lines += ["provenance:"] + ([f"- {x}" for x in r.provenance] or ["- none"])
    lines += ["boundary_notes:"] + [f"- {x}" for x in r.boundary_notes]
    return "\n".join(lines)
