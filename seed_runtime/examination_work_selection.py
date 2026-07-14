"""Read-only examination work selection over a policy projection and frontier."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.examination_frontier import ExaminationFrontier
from seed_runtime.examination_policy_projection import ExaminationPolicyProjection, ExaminationPolicySelectorHandoff

CONVENTION = "examination_work_selection_v1"
SELECTION_STATES = ("selected", "no_selection", "unknown", "conflict", "invalid")
BOUNDARY_NOTES = (
    "This artifact applies an existing examination policy; it does not create or alter policy.",
    "At most one eligible work item may be selected.",
    "Selection does not authorize, schedule, execute, or mark work examined.",
    "Non-selected alternatives remain preserved and are not rejected.",
    "No-selection is a lawful result and is not a campaign-completion verdict.",
    "No lexical, insertion-order, hash-order, or arbitrary tie-break is used.",
    "The ExaminationFrontier remains the source of work classification.",
    "Methodological applicability and constraints remain owned upstream.",
    "This artifact is not runtime Evidence or Fact.",
)

class ExaminationWorkSelectionError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

@dataclass(frozen=True)
class NonSelectedEligibleWork:
    work_reference: str
    non_selection_reason: str
    def to_json_dict(self): return asdict(self)

@dataclass(frozen=True)
class FutureProbeRequestHandoff:
    selection_id: str; inquiry_reference: dict[str, Any]; frontier_reference: dict[str, Any]; policy_reference: dict[str, Any]; selected_work_reference: str; selection_reason: str; method_constraint_reference: dict[str, Any]; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self): return asdict(self)

@dataclass(frozen=True)
class ExaminationWorkSelection:
    artifact_type: str; selection_id: str; inquiry_reference: dict[str, Any]; frontier_reference: dict[str, Any]; policy_projection_reference: dict[str, Any]; selector_handoff_reference: dict[str, Any]; policy_kind: str; selection_state: str; selected_work_reference: str | None; selection_basis: str; selection_reason: str; non_selected_eligible_work: tuple[NonSelectedEligibleWork,...]; policy_excluded_work_references: tuple[str,...]; unchanged_blocked_references: tuple[str,...]; unchanged_unsupported_references: tuple[str,...]; unchanged_deferred_references: tuple[str,...]; unchanged_examined_references: tuple[str,...]; unchanged_failed_references: tuple[str,...]; unchanged_conflict_unknown_references: tuple[str,...]; no_selection_reasons: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; future_probe_request_handoff: FutureProbeRequestHandoff | None; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k in ("policy_excluded_work_references","unchanged_blocked_references","unchanged_unsupported_references","unchanged_deferred_references","unchanged_examined_references","unchanged_failed_references","unchanged_conflict_unknown_references","no_selection_reasons","unknowns","conflicts","boundary_notes"):
            d[k]=list(getattr(self,k))
        d["non_selected_eligible_work"]=[r.to_json_dict() for r in self.non_selected_eligible_work]
        d["future_probe_request_handoff"]=self.future_probe_request_handoff.to_json_dict() if self.future_probe_request_handoff else None
        return d

def _handoff_id(h: ExaminationPolicySelectorHandoff) -> str:
    return _stable("examination-policy-selector-handoff", h.to_json_dict())

def _validate(frontier: ExaminationFrontier, policy: ExaminationPolicyProjection, handoff: ExaminationPolicySelectorHandoff):
    if handoff.policy_projection_id != policy.projection_id: raise ExaminationWorkSelectionError("handoff does not reference supplied policy projection")
    if policy.frontier_reference.get("frontier_id") != frontier.frontier_id: raise ExaminationWorkSelectionError("policy does not reference supplied frontier")
    if handoff.frontier_id != frontier.frontier_id: raise ExaminationWorkSelectionError("handoff does not reference supplied frontier")
    for attr in ("policy_kind","policy_sufficiency","tie_treatment"):
        if getattr(handoff, attr) != getattr(policy, attr): raise ExaminationWorkSelectionError(f"handoff {attr} does not match policy")
    if tuple(handoff.eligible_in_scope_work_ids) != tuple(policy.eligible_in_scope_work_references): raise ExaminationWorkSelectionError("handoff eligible references do not match policy")
    if tuple(handoff.prerequisite_references) != tuple(policy.prerequisite_references): raise ExaminationWorkSelectionError("handoff prerequisite references do not match policy")
    if tuple(handoff.no_selection_conditions) != tuple(policy.no_selection_conditions): raise ExaminationWorkSelectionError("handoff no-selection conditions do not match policy")
    by={i.work_item_id:i for i in frontier.work_items}
    for wid in tuple(policy.in_scope_work_references)+tuple(policy.eligible_in_scope_work_references):
        if wid not in by: raise ExaminationWorkSelectionError("policy references work absent from frontier")
    for wid in policy.eligible_in_scope_work_references:
        if not by[wid].classification.eligible: raise ExaminationWorkSelectionError("eligible policy reference is not frontier-eligible")
    return by

def select_examination_work(frontier: ExaminationFrontier, policy: ExaminationPolicyProjection, handoff: ExaminationPolicySelectorHandoff) -> ExaminationWorkSelection:
    by=_validate(frontier, policy, handoff)
    eligible=tuple(w for w in policy.eligible_in_scope_work_references if w in by and by[w].classification.eligible)
    frontier_eligible=tuple(sorted(w for w,i in by.items() if i.classification.eligible))
    state="no_selection"; selected=None; reason=""; basis=policy.policy_kind or "unknown_policy"; unknowns=tuple(policy.unknowns); conflicts=tuple(policy.conflicts); no_reasons=list(policy.no_selection_conditions)
    if policy.policy_state == "conflict" or policy.policy_sufficiency == "conflict":
        state="conflict"; reason="conflicting policy projection cannot produce selection"; no_reasons.append(reason)
    elif policy.policy_state == "unknown" or policy.policy_sufficiency == "unknown":
        state="unknown"; reason="required selection evidence is unresolved"; no_reasons.append(reason)
    elif policy.policy_state != "applicable":
        state="no_selection"; reason="policy is not applicable to the supplied frontier"; no_reasons.append(reason)
    elif policy.policy_kind == "no_selection":
        state="no_selection"; reason="explicit no-selection policy applied"; no_reasons.append(reason)
    elif policy.policy_sufficiency != "sufficient_for_selection":
        state="no_selection"
        if policy.policy_kind == "all_eligible_no_order" and len(eligible) > 1: reason="multiple eligible items remained without a lawful tie-break"
        elif not eligible: reason="no eligible in-scope work"
        else: reason="policy is insufficient for selection"
        no_reasons.append(reason)
    elif policy.policy_kind == "explicit_work_identity":
        named=str(policy.policy_parameters.get("work_item_id", "") or "")
        if named in eligible and named not in policy.policy_excluded_work_references:
            state="selected"; selected=named; reason="explicit policy work identity matched one eligible item"
        elif named in by:
            state="no_selection"; reason="named work was not currently eligible"; no_reasons.append(reason)
        else:
            state="no_selection"; reason="named work was absent from the frontier"; no_reasons.append(reason)
    elif policy.policy_kind == "all_eligible_no_order":
        if len(eligible) == 1:
            state="selected"; selected=eligible[0]; reason="one sole eligible in-scope item remained under sufficient no-order policy"
        elif len(eligible) == 0:
            state="no_selection"; reason="no eligible in-scope work"; no_reasons.append(reason)
        else:
            state="no_selection"; reason="multiple eligible items remained without a lawful tie-break"; no_reasons.append(reason)
    elif policy.policy_kind == "prerequisite_first":
        if len(eligible) == 1:
            state="selected"; selected=eligible[0]; reason="one unique prerequisite-permitted item remained"
        elif len(eligible) == 0:
            state="no_selection"; reason="no eligible in-scope work"; no_reasons.append(reason)
        else:
            state="no_selection"; reason="multiple prerequisite-permitted items remained without a lawful tie-break"; no_reasons.append(reason)
    else:
        state="unknown"; reason="unsupported policy kind in selection boundary"; no_reasons.append(reason)
    def ns_reason(w):
        if policy.policy_kind == "explicit_work_identity": return "not named by explicit-work policy"
        if w not in policy.in_scope_work_references: return "outside policy scope"
        if policy.policy_kind == "prerequisite_first": return "not uniquely permitted by prerequisite policy" if state=="selected" else "equally permitted but unresolved by tie treatment"
        if policy.policy_kind == "all_eligible_no_order": return "equally permitted but unresolved by tie treatment" if state!="selected" else "not selected by sole-eligible policy realization"
        return "explicit no-selection policy applied"
    preserved_eligible = frontier_eligible if policy.policy_kind == "explicit_work_identity" else eligible
    non_selected=tuple(NonSelectedEligibleWork(w, ns_reason(w)) for w in preserved_eligible if w != selected)
    blocked=tuple(sorted(w for w,i in by.items() if i.classification.blocked)); unsupported=tuple(sorted(w for w,i in by.items() if i.classification.unsupported)); deferred=tuple(sorted(w for w,i in by.items() if i.classification.deferred)); examined=tuple(sorted(w for w,i in by.items() if i.classification.examined)); failed=tuple(sorted(w for w,i in by.items() if i.classification.failed)); cu=tuple(sorted(w for w,i in by.items() if i.classification.conflict or i.classification.unknown))
    sel_id=_stable("examination-work-selection", {"frontier":frontier.frontier_id,"policy":policy.projection_id,"handoff":handoff.to_json_dict(),"state":state,"selected":selected,"reason":reason,"convention":CONVENTION})
    future=None
    if state == "selected" and selected:
        future=FutureProbeRequestHandoff(sel_id, policy.inquiry_reference, policy.frontier_reference, {"projection_id":policy.projection_id,"policy_kind":policy.policy_kind}, selected, reason, policy.method_applicability_reference)
    return ExaminationWorkSelection("ExaminationWorkSelection", sel_id, policy.inquiry_reference, policy.frontier_reference, {"projection_id":policy.projection_id,"policy_convention":"examination_policy_projection_v1"}, {"handoff_id":_handoff_id(handoff),"policy_projection_id":handoff.policy_projection_id}, policy.policy_kind, state, selected, basis, reason, non_selected, tuple(policy.policy_excluded_work_references), blocked, unsupported, deferred, examined, failed, cu, tuple(dict.fromkeys(no_reasons)), unknowns, conflicts, future)

def examination_work_selection_json(selection: ExaminationWorkSelection): return selection.to_json_dict()

def format_examination_work_selection(selection: ExaminationWorkSelection) -> str:
    out=["Examination Work Selection",f"selection_id: {selection.selection_id}",f"selection_state: {selection.selection_state}",f"policy_kind: {selection.policy_kind}",f"selected_work_reference: {selection.selected_work_reference or 'none'}",f"selection_reason: {selection.selection_reason}",f"read_only: {str(selection.read_only).lower()}",f"writes_event_ledger: {str(selection.writes_event_ledger).lower()}",f"mutates_cluster: {str(selection.mutates_cluster).lower()}","non_selected_eligible_work:"]
    out += [f"- {r.work_reference}: {r.non_selection_reason}" for r in selection.non_selected_eligible_work] or ["- none"]
    out += ["no_selection_reasons:"] + ([f"- {r}" for r in selection.no_selection_reasons] or ["- none"])
    out += ["boundary_notes:"] + [f"- {n}" for n in selection.boundary_notes]
    return "\n".join(out)
