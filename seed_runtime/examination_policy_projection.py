"""Read-only examination policy projection over an immutable frontier."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion
from seed_runtime.examination_frontier import ExaminationFrontier
from seed_runtime.examination_method_applicability import ExaminationMethodApplicabilityProjection

CONVENTION = "examination_policy_projection_v1"
POLICY_KINDS = ("explicit_work_identity", "all_eligible_no_order", "prerequisite_first", "no_selection")
POLICY_STATES = ("applicable", "inapplicable", "unknown", "conflict")
SUFFICIENCY_STATES = ("sufficient_for_selection", "insufficient_for_selection", "unknown", "conflict")
TIE_TREATMENTS = ("refuse_selection", "require_additional_testimony", "preserve_all_as_equally_permitted")
BOUNDARY_NOTES = (
    "This projection preserves examination policy; it does not select a work item.",
    "An applicable policy may still be insufficient for a unique lawful selection.",
    "No-selection is distinct from campaign completion.",
    "Policy does not authorize, schedule, execute, or mark work examined.",
    "Policy constraints do not become semantic truth, priority scores, or knowledge admission.",
    "The ExaminationFrontier remains the source of work classification.",
    "Method applicability remains owned by ExaminationMethodApplicabilityProjection.",
    "This artifact is not runtime Evidence or Fact.",
)

class ExaminationPolicyProjectionError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _tuple(v: Any=()) -> tuple[str,...]:
    if v is None: return ()
    if not isinstance(v, (list, tuple)) or not all(isinstance(x, str) for x in v):
        raise ExaminationPolicyProjectionError("expected list of strings")
    return tuple(v)

@dataclass(frozen=True)
class ExaminationResolutionTestimony:
    testimony_id: str
    inquiry_reference: str
    frontier_reference: str
    applicability_projection_reference: str
    policy_kind: str
    policy_parameters: dict[str, Any]
    candidate_scope: tuple[str,...] = ()
    prerequisite_treatment: tuple[str,...] = ()
    tie_treatment: str = "require_additional_testimony"
    no_selection_conditions: tuple[str,...] = ()
    continuation_testimony: tuple[str,...] = ()
    resource_operation_constraints: tuple[str,...] = ()
    supporting_references: tuple[str,...] = ()
    contradicting_references: tuple[str,...] = ()
    provenance: tuple[str,...] = ()
    unknowns: tuple[str,...] = ()

    def __post_init__(self):
        if not self.testimony_id:
            raise ExaminationPolicyProjectionError("testimony_id is required")
        if self.policy_kind and self.policy_kind not in POLICY_KINDS:
            raise ExaminationPolicyProjectionError("unsupported policy_kind")
        if self.tie_treatment not in TIE_TREATMENTS:
            raise ExaminationPolicyProjectionError("unsupported tie_treatment")

    def to_json_dict(self):
        d=asdict(self)
        for k in ("candidate_scope","prerequisite_treatment","no_selection_conditions","continuation_testimony","resource_operation_constraints","supporting_references","contradicting_references","provenance","unknowns"):
            d[k]=list(d[k])
        return d

@dataclass(frozen=True)
class ExaminationPolicySelectorHandoff:
    frontier_id: str
    policy_projection_id: str
    policy_kind: str
    policy_sufficiency: str
    eligible_in_scope_work_ids: tuple[str,...]
    prerequisite_references: tuple[str,...]
    tie_treatment: str
    no_selection_conditions: tuple[str,...]
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    def to_json_dict(self):
        return asdict(self) | {"eligible_in_scope_work_ids":list(self.eligible_in_scope_work_ids),"prerequisite_references":list(self.prerequisite_references),"no_selection_conditions":list(self.no_selection_conditions)}

@dataclass(frozen=True)
class ExaminationPolicyProjection:
    artifact_type: str; projection_id: str; inquiry_reference: dict[str,Any]; frontier_reference: dict[str,Any]; method_applicability_reference: dict[str,Any]; resolution_testimony_references: tuple[str,...]; policy_kind: str; policy_state: str; policy_sufficiency: str; policy_parameters: dict[str,Any]; in_scope_work_references: tuple[str,...]; eligible_in_scope_work_references: tuple[str,...]; policy_excluded_work_references: tuple[str,...]; prerequisite_references: tuple[str,...]; tie_treatment: str; no_selection_conditions: tuple[str,...]; continuation_or_stop_testimony: tuple[str,...]; resource_operation_constraints: tuple[str,...]; supporting_references: tuple[str,...]; contradicting_references: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k in ("resolution_testimony_references","in_scope_work_references","eligible_in_scope_work_references","policy_excluded_work_references","prerequisite_references","no_selection_conditions","continuation_or_stop_testimony","resource_operation_constraints","supporting_references","contradicting_references","unknowns","conflicts","boundary_notes"):
            d[k]=list(d[k])
        return d
    def to_selector_handoff(self):
        return ExaminationPolicySelectorHandoff(self.frontier_reference["frontier_id"], self.projection_id, self.policy_kind, self.policy_sufficiency, self.eligible_in_scope_work_references, self.prerequisite_references, self.tie_treatment, self.no_selection_conditions)

def project_examination_policy(q: BoundedConstitutionalQuestion, applicability: ExaminationMethodApplicabilityProjection, frontier: ExaminationFrontier, testimony: tuple[ExaminationResolutionTestimony,...]=()) -> ExaminationPolicyProjection:
    if not isinstance(q, BoundedConstitutionalQuestion): raise ExaminationPolicyProjectionError("bounded inquiry input is structurally invalid")
    work_by_id={i.work_item_id:i for i in frontier.work_items}
    cand_to_work={i.candidate_work_id:i.work_item_id for i in frontier.work_items}
    eligible={i.work_item_id for i in frontier.work_items if i.classification.eligible and i.candidate_work_id in applicability.applicable_candidate_references}
    unknowns=[]; conflicts=[]; contradict=[]
    if not testimony:
        unknowns.append("resolution_testimony_absent")
    kinds={t.policy_kind for t in testimony if t.policy_kind}
    params={json.dumps(t.policy_parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=False) for t in testimony}
    if len(kinds)>1 or len(params)>1 or any(t.contradicting_references for t in testimony):
        conflicts.append("conflicting resolution testimony for inquiry/frontier policy")
    for t in testimony:
        if t.inquiry_reference != q.bounded_question_id: unknowns.append(f"{t.testimony_id}: mismatched inquiry reference")
        if t.frontier_reference != frontier.frontier_id: contradict.append(f"{t.testimony_id}: mismatched frontier reference")
        if t.applicability_projection_reference != applicability.projection_id: contradict.append(f"{t.testimony_id}: mismatched method-applicability projection reference")
    policy_kind=next(iter(kinds), "")
    tie= testimony[0].tie_treatment if testimony else "require_additional_testimony"
    params_obj=testimony[0].policy_parameters if testimony else {}
    all_work=tuple(i.work_item_id for i in frontier.work_items)
    in_scope=all_work; prereq=(); no_select=[]
    supports=tuple(sorted({x for t in testimony for x in ((t.supporting_references or (t.testimony_id,))) }))
    contradict=tuple(sorted(set(contradict) | {x for t in testimony for x in t.contradicting_references}))
    continuation=tuple(sorted({x for t in testimony for x in t.continuation_testimony}))
    resources=tuple(sorted({x for t in testimony for x in t.resource_operation_constraints}))
    if conflicts:
        state="conflict"; suff="conflict"; no_select.append("policy_conflict")
    elif unknowns or not policy_kind:
        state="unknown"; suff="unknown"; no_select.append("policy_unknown")
    elif contradict:
        state="inapplicable"; suff="unknown"; no_select.append("policy_inapplicable")
    elif policy_kind == "explicit_work_identity":
        wid=str(params_obj.get("work_item_id","") or "")
        if not wid:
            state="unknown"; suff="unknown"; unknowns.append("explicit_work_identity missing work_item_id"); no_select.append("policy_unknown")
        elif wid not in work_by_id:
            state="inapplicable"; suff="unknown"; contradict+=("named work does not belong to frontier",); no_select.append("policy_inapplicable")
        else:
            state="applicable"; in_scope=(wid,); suff="sufficient_for_selection" if wid in eligible else "insufficient_for_selection"
            if wid not in eligible: no_select.append("no eligible in-scope work")
    elif policy_kind == "all_eligible_no_order":
        state="applicable"; suff="insufficient_for_selection" if len(eligible)!=1 or tie != "preserve_all_as_equally_permitted" else "sufficient_for_selection"
        if len(eligible)==0: no_select.append("no eligible in-scope work")
        elif len(eligible)>1: no_select.append("policy insufficient for unique selection")
    elif policy_kind == "no_selection":
        state="applicable"; suff="insufficient_for_selection"; no_select.append("testimony explicitly requires no selection")
    elif policy_kind == "prerequisite_first":
        edges=tuple(params_obj.get("prerequisites",()) or ())
        if not edges:
            state="unknown"; suff="unknown"; unknowns.append("prerequisite evidence absent"); no_select.append("policy_unknown")
        else:
            prereq=tuple(sorted(json.dumps(e, sort_keys=True) for e in edges))
            dependents={cand_to_work.get(e.get("work_item_id", e.get("dependent_work_item_id",""))) for e in edges if isinstance(e,dict)}
            roots=tuple(sorted(w for w in eligible if w not in dependents))
            state="applicable"; in_scope=roots; suff="sufficient_for_selection" if len(roots)==1 else "insufficient_for_selection"
            if len(roots)==0: no_select.append("no eligible in-scope work")
            elif len(roots)>1: no_select.append("tie lacks unique prerequisite-first basis")
    else:
        state="unknown"; suff="unknown"; no_select.append("policy_unknown")
    eligible_scope=tuple(w for w in in_scope if w in eligible)
    excluded=tuple(w for w in all_work if w not in in_scope)
    if suff != "sufficient_for_selection" and "policy insufficient for unique selection" not in no_select and state == "applicable": no_select.append("policy_insufficient")
    pid=_stable("examination-policy", {"inquiry":q.bounded_question_id,"frontier":frontier.frontier_id,"method_applicability":applicability.projection_id,"convention":CONVENTION,"testimony_ids":sorted(t.testimony_id for t in testimony),"policy_kind":policy_kind,"policy_parameters":params_obj})
    return ExaminationPolicyProjection("ExaminationPolicyProjection", pid, {"bounded_question_id":q.bounded_question_id}, {"frontier_id":frontier.frontier_id,"frontier_convention":frontier.frontier_convention}, {"projection_id":applicability.projection_id,"applicability_convention":applicability.applicability_convention}, tuple(sorted(t.testimony_id for t in testimony)), policy_kind, state, suff, params_obj, tuple(sorted(in_scope)), tuple(sorted(eligible_scope)), tuple(sorted(excluded)), prereq, tie, tuple(sorted(set(no_select) | {x for t in testimony for x in t.no_selection_conditions})), continuation, resources, supports, contradict, tuple(sorted(set(unknowns) | {x for t in testimony for x in t.unknowns})), tuple(sorted(conflicts)))

def examination_policy_projection_json(p): return p.to_json_dict()

def format_examination_policy_projection(p):
    lines=["Examination Policy Projection",f"projection_id: {p.projection_id}",f"policy_kind: {p.policy_kind or 'unknown'}",f"policy_state: {p.policy_state}",f"policy_sufficiency: {p.policy_sufficiency}",f"tie_treatment: {p.tie_treatment}",f"read_only: {str(p.read_only).lower()}",f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",f"mutates_cluster: {str(p.mutates_cluster).lower()}","eligible_in_scope_work_references:"]
    lines += [f"- {w}" for w in p.eligible_in_scope_work_references] or ["- none"]
    lines += ["no_selection_conditions:"] + ([f"- {c}" for c in p.no_selection_conditions] or ["- none"])
    lines += ["boundary_notes:"] + [f"- {n}" for n in p.boundary_notes]
    return "\n".join(lines)
