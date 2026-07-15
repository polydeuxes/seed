"""Read-only ingress authority/scope binding for one interpreted operator request."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json
from typing import Iterable
from seed_runtime.operator_expression_interpretation import AttributedOperatorExpression, OperatorExpressionInterpretationProjection, FutureOperatorAuthorityScopeBindingHandoff

CONVENTION="operator_authority_scope_binding_v1"
STATES=("permitted","blocked","unknown","conflict")
BOUNDARY_NOTES=(
"This artifact binds one interpreted operator request to established ingress authority and scope.",
"Authority-bearing language is not itself an authority grant.",
"Requested scope is not automatically permitted scope.",
"Operator identity is not unlimited authority.",
"Permission to request movement is distinct from authorization of a concrete realization.",
"Standing inquiry authority is distinct from observation and mutation authority.",
"Operator-stated effect constraints remain requirements; they are not proof that a future realization satisfies them.",
"Ingress authority does not establish mechanism availability, capability reachability, selection, warrant, or execution.",
"This artifact does not produce a bounded constitutional question.",
"No tool, provider, model-decision, or registered-operation concept is required by this projection.",
)
_ACTIVITY_MAP={"":"constitutional_read","active observation":"network_active_observation","inspection":"local_passive_observation","privileged observation":"local_privileged_observation","external movement":"external_effectful_movement","presentation":"presentation_request"}
_CONSTRAINT_CONFLICTS={("network_active_observation","do not use the network"),("local_privileged_observation","do not use root"),("external_effectful_movement","do not change anything"),("external_effectful_movement","do not modify anything")}
class OperatorAuthorityScopeBindingError(ValueError): pass

def _refs(xs:Iterable[str]=()): return tuple(sorted({str(x) for x in xs if x}))
def _stable(prefix,payload): return prefix+":"+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

@dataclass(frozen=True)
class OperatorIdentityContext:
    operator_ref:str; verified_identity_ref:str=""; authority_classes:tuple[str,...]=(); grantable_authority_classes:tuple[str,...]=(); provenance:tuple[str,...]=(); unknowns:tuple[str,...]=(); conflicts:tuple[str,...]=()

@dataclass(frozen=True)
class WorkspaceSessionAuthorityContext:
    workspace_ref:str; session_ref:str=""; authority_context_ref:str=""; required_session_ref:bool=True; permitted_scope_refs:tuple[str,...]=(); prohibited_scope_refs:tuple[str,...]=(); restrictions:tuple[str,...]=(); authority_sources:tuple[str,...]=(); provenance:tuple[str,...]=(); unknowns:tuple[str,...]=(); conflicts:tuple[str,...]=()

@dataclass(frozen=True)
class ScopeBindingContext:
    scope_context_ref:str; workspace_ref:str; resolved_scope_refs:tuple[tuple[str,str],...]=(); conflicting_scope_expressions:tuple[str,...]=(); unresolved_scope_expressions:tuple[str,...]=(); provenance:tuple[str,...]=(); unknowns:tuple[str,...]=(); conflicts:tuple[str,...]=()

@dataclass(frozen=True)
class FutureBoundedConstitutionalQuestionHandoff:
    authority_scope_binding_ref:str; interpretation_projection_ref:str; attributed_expression_ref:str; operator_identity_ref:str; workspace_ref:str; session_ref:str; inquiry_or_request_kind:str; requested_activity_class:str; relation_or_focus_expressions:tuple[str,...]; subject_expressions:tuple[str,...]; object_expressions:tuple[str,...]; requested_scope_expressions:tuple[str,...]; bound_scope_refs:tuple[str,...]; excluded_scope_refs:tuple[str,...]; authority_source_refs:tuple[str,...]; operator_stated_effect_constraints:tuple[str,...]; presentation_preference:str; source_span_refs:tuple[str,...]; grammar_ref:str; grammar_applicability_ref:str; provenance:tuple[str,...]; known_loss:tuple[str,...]; unknowns:tuple[str,...]; conflicts:tuple[str,...]; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v,tuple): d[k]=list(v)
        return d

@dataclass(frozen=True)
class OperatorAuthorityScopeBindingProjection:
    artifact_type:str; binding_projection_id:str; interpretation_projection_ref:str; attributed_expression_ref:str; operator_identity_ref:str; workspace_ref:str; session_ref:str; inquiry_or_request_kind:str; requested_activity_class:str; requested_scope_expressions:tuple[str,...]; resolved_scope_refs:tuple[str,...]; permitted_scope_refs:tuple[str,...]; excluded_scope_refs:tuple[str,...]; unresolved_scope_expressions:tuple[str,...]; authority_bearing_expressions:tuple[str,...]; authority_source_refs:tuple[str,...]; required_authority_class:str; operator_stated_effect_constraints:tuple[str,...]; presentation_preference:str; binding_state:str; binding_reason:str; required_additional_authority:tuple[str,...]; supporting_references:tuple[str,...]; provenance:tuple[str,...]; unknowns:tuple[str,...]; conflicts:tuple[str,...]; future_bounded_question_handoff:FutureBoundedConstitutionalQuestionHandoff|None; boundary_notes:tuple[str,...]=BOUNDARY_NOTES; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False; binding_convention:str=CONVENTION
    def to_json_dict(self):
        d=asdict(self); d["future_bounded_question_handoff"]=self.future_bounded_question_handoff.to_json_dict() if self.future_bounded_question_handoff else None
        for k,v in d.items():
            if isinstance(v,tuple): d[k]=list(v)
        return d

def _activity(interp):
    if interp.requested_movement_class in _ACTIVITY_MAP: return _ACTIVITY_MAP[interp.requested_movement_class]
    if interp.inquiry_or_request_kind in ("identify","explain","support","unknowns","limitations","show"): return "constitutional_read"
    return "unsupported"

def bind_operator_authority_scope(interpretation:OperatorExpressionInterpretationProjection, handoff:FutureOperatorAuthorityScopeBindingHandoff, expression:AttributedOperatorExpression, operator_identity:OperatorIdentityContext, workspace_session:WorkspaceSessionAuthorityContext, scope_binding:ScopeBindingContext, *, supporting_references:tuple[str,...]=(), provenance:tuple[str,...]=(), unknowns:tuple[str,...]=(), conflicts:tuple[str,...]=()):
    if handoff.interpretation_projection_id != interpretation.interpretation_projection_id: raise OperatorAuthorityScopeBindingError("interpretation handoff mismatch")
    if interpretation.attributed_expression_ref != expression.expression_id or handoff.attributed_expression_ref != expression.expression_id: raise OperatorAuthorityScopeBindingError("attributed expression mismatch")
    if handoff.operator_ref != operator_identity.operator_ref or expression.operator_ref != operator_identity.operator_ref: raise OperatorAuthorityScopeBindingError("operator identity mismatch")
    if expression.workspace_ref != workspace_session.workspace_ref or handoff.workspace_ref != workspace_session.workspace_ref or scope_binding.workspace_ref != workspace_session.workspace_ref: raise OperatorAuthorityScopeBindingError("workspace authority mismatch")
    if workspace_session.required_session_ref and (expression.session_ref != workspace_session.session_ref or handoff.session_ref != workspace_session.session_ref): raise OperatorAuthorityScopeBindingError("session authority mismatch")
    activity=_activity(interpretation); required=activity
    req_scopes=_refs(interpretation.scope_expressions); resmap=dict(scope_binding.resolved_scope_refs); resolved=_refs(resmap.get(s,"") for s in req_scopes)
    unresolved=_refs((*scope_binding.unresolved_scope_expressions, *(s for s in req_scopes if s not in resmap)))
    permitted=_refs(r for r in resolved if r in set(workspace_session.permitted_scope_refs))
    excluded=_refs((*[r for r in resolved if r not in set(workspace_session.permitted_scope_refs)], *[r for r in resolved if r in set(workspace_session.prohibited_scope_refs)]))
    all_unknowns=_refs((*unknowns,*interpretation.unknowns,*handoff.unknowns,*operator_identity.unknowns,*workspace_session.unknowns,*scope_binding.unknowns))
    all_conflicts=_refs((*conflicts,*interpretation.conflicts,*handoff.conflicts,*operator_identity.conflicts,*workspace_session.conflicts,*scope_binding.conflicts))
    reason="within_established_authority_and_scope"; state="permitted"; add=()
    constraint_conflicts=tuple(f"operator_constraint_prohibits_{activity}" for c in interpretation.operator_stated_effect_constraints if (activity,c.lower()) in _CONSTRAINT_CONFLICTS)
    if interpretation.interpretation_state != "interpreted": state,reason="unknown","interpretation_not_interpreted"
    elif all_conflicts or scope_binding.conflicting_scope_expressions or constraint_conflicts: state,reason="conflict","conflicting_authority_scope_or_constraints"; all_conflicts=_refs((*all_conflicts,*constraint_conflicts,*scope_binding.conflicting_scope_expressions))
    elif activity=="unsupported": state,reason="unknown","activity_class_unresolved"; add=("recognized_activity_class",)
    elif unresolved: state,reason="unknown","requested_scope_unresolved"; add=("scope_binding",)
    elif required not in operator_identity.authority_classes:
        if required in operator_identity.grantable_authority_classes and interpretation.authority_bearing_expressions:
            reason="within_explicit_operator_grant"
        elif f"{required}_not_granted" in workspace_session.restrictions or required in workspace_session.restrictions:
            state,reason="blocked",f"{required}_not_granted"; add=(required,)
        elif all_unknowns: state,reason="unknown","authority_source_unresolved"; add=(required,)
        else: state,reason="blocked","requested_activity_not_granted"; add=(required,)
    elif not resolved and req_scopes: state,reason="unknown","required_scope_binding_unavailable"; add=("scope_binding",)
    elif excluded and not permitted: state,reason="blocked","requested_scope_exceeds_authority"; add=(required,)
    elif any(r in workspace_session.restrictions for r in ("workspace_restriction","session_restriction")): state,reason="blocked","workspace_or_session_restriction"; add=(required,)
    sources=_refs((*workspace_session.authority_sources,*(("explicit_operator_grant",) if reason=="within_explicit_operator_grant" else ())))
    payload={"interpretation":interpretation.interpretation_projection_id,"expression":expression.expression_id,"operator":operator_identity.verified_identity_ref or operator_identity.operator_ref,"workspace":workspace_session.workspace_ref,"session":workspace_session.session_ref,"kind":interpretation.inquiry_or_request_kind,"activity":activity,"requested_scope":req_scopes,"resolved":resolved,"permitted":permitted,"excluded":excluded,"unresolved":unresolved,"authority_bearing":_refs(interpretation.authority_bearing_expressions),"sources":sources,"required":required,"constraints":_refs(interpretation.operator_stated_effect_constraints),"presentation":interpretation.presentation_preference,"supporting":_refs(supporting_references),"provenance":_refs((*provenance,*interpretation.provenance,*operator_identity.provenance,*workspace_session.provenance,*scope_binding.provenance)),"unknowns":all_unknowns,"conflicts":all_conflicts,"state":state,"reason":reason,"convention":CONVENTION}
    bid=_stable("operator-authority-scope-binding-projection",payload)
    future=None
    if state=="permitted":
        future=FutureBoundedConstitutionalQuestionHandoff(bid,interpretation.interpretation_projection_id,expression.expression_id,operator_identity.verified_identity_ref or operator_identity.operator_ref,workspace_session.workspace_ref,workspace_session.session_ref,interpretation.inquiry_or_request_kind,activity,interpretation.relation_or_focus_expressions,interpretation.subject_expressions,interpretation.object_expressions,req_scopes,permitted,excluded,sources,_refs(interpretation.operator_stated_effect_constraints),interpretation.presentation_preference,tuple(f"{s.component}:{s.start}-{s.end}" for s in interpretation.source_span_bindings),interpretation.recovered_grammar_ref,interpretation.grammar_applicability_ref,_refs((*provenance,*interpretation.provenance,*scope_binding.provenance)),interpretation.known_loss,all_unknowns,all_conflicts)
    return OperatorAuthorityScopeBindingProjection("OperatorAuthorityScopeBindingProjection",bid,interpretation.interpretation_projection_id,expression.expression_id,operator_identity.verified_identity_ref or operator_identity.operator_ref,workspace_session.workspace_ref,workspace_session.session_ref,interpretation.inquiry_or_request_kind,activity,req_scopes,resolved,permitted,excluded,unresolved,_refs(interpretation.authority_bearing_expressions),sources,required,_refs(interpretation.operator_stated_effect_constraints),interpretation.presentation_preference,state,reason,_refs(add),_refs(supporting_references),payload["provenance"],all_unknowns,all_conflicts,future)


EXPLANATION_CONVENTION="minimum_lawful_advancement_explanation_v1"

@dataclass(frozen=True)
class MinimumLawfulAdvancementExplanation:
    artifact_type:str
    explanation_id:str
    source_artifact_ref:str
    source_artifact_type:str
    producer:str
    attempted_movement:str
    established:str
    source_state:str
    source_reason:str
    first_missing_boundary:str
    movement_blocked:bool
    authority_resolvable:bool
    reconsideration_transition:str
    prohibited_downstream_movement:tuple[str,...]
    preserved_unknowns:tuple[str,...]
    preserved_conflicts:tuple[str,...]
    explanation_boundary:str
    read_only:bool=True
    writes_event_ledger:bool=False
    mutates_cluster:bool=False
    explanation_convention:str=EXPLANATION_CONVENTION
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v,tuple): d[k]=list(v)
        return d

def explain_minimum_lawful_advancement(p:OperatorAuthorityScopeBindingProjection):
    attempted="advance one interpreted operator request from authority/scope binding to bounded constitutional question formulation"
    established=(f"activity={p.requested_activity_class}; requested_scope={', '.join(p.requested_scope_expressions) or 'none'}; "
                 f"permitted_scope={', '.join(p.permitted_scope_refs) or 'none'}; excluded_scope={', '.join(p.excluded_scope_refs) or 'none'}; "
                 f"unresolved_scope={', '.join(p.unresolved_scope_expressions) or 'none'}; authority_sources={', '.join(p.authority_source_refs) or 'none'}; "
                 f"required_authority={p.required_authority_class}; constraints={', '.join(p.operator_stated_effect_constraints) or 'none'}")
    prohibited=("formulate_bounded_constitutional_question", "select_diagnostic_view_capability_or_realization", "authorize_or_execute_movement")
    movement_blocked=p.binding_state in ("blocked","conflict")
    authority_resolvable=False
    boundary="none"
    transition="no transition required; binding may advance according to the existing permitted handoff"
    if p.binding_state=="permitted":
        prohibited=("select_diagnostic_view_capability_or_realization", "authorize_or_execute_movement")
    elif p.binding_reason in ("requested_activity_not_granted", f"{p.requested_activity_class}_not_granted"):
        boundary=f"required ingress authority not established: {', '.join(p.required_additional_authority) or p.required_authority_class}"
        authority_resolvable=True
        transition=f"one exact bounded operator authority grant for {', '.join(p.required_additional_authority) or p.required_authority_class} could permit reconsideration"
    elif p.binding_reason=="requested_scope_exceeds_authority":
        boundary=f"requested scope outside established authority: {', '.join(p.excluded_scope_refs) or 'none'}"
        transition=f"scope evidence or permission for the exact excluded scope {', '.join(p.excluded_scope_refs) or 'none'} could permit reconsideration"
    elif p.binding_reason in ("requested_scope_unresolved","required_scope_binding_unavailable"):
        boundary=f"requested target cannot be bound: {', '.join(p.unresolved_scope_expressions) or ', '.join(p.requested_scope_expressions) or 'none'}"
        transition="scope evidence or operator clarification for the unresolved referent could permit reconsideration"
    elif p.binding_reason=="authority_source_unresolved" or p.binding_state=="unknown":
        boundary="authority or binding evidence remains Unknown; permission and denial are both unestablished"
        transition="authority or scope evidence resolving the preserved Unknown could permit reconsideration"
    elif p.binding_state=="conflict":
        boundary=f"operator authority/scope or stated constraint conflict remains: {', '.join(p.conflicts) or p.binding_reason}"
        transition="the request or conflicting constraint must change before reconsideration"
    else:
        boundary=p.binding_reason
        transition="narrow source-artifact evidence addressing the stated boundary could permit reconsideration"
    payload={"source":p.binding_projection_id,"state":p.binding_state,"reason":p.binding_reason,"boundary":boundary,"transition":transition,"unknowns":p.unknowns,"conflicts":p.conflicts,"convention":EXPLANATION_CONVENTION}
    return MinimumLawfulAdvancementExplanation("MinimumLawfulAdvancementExplanation",_stable("minimum-lawful-advancement-explanation",payload),p.binding_projection_id,p.artifact_type,"OperatorAuthorityScopeBindingProjection",attempted,established,p.binding_state,p.binding_reason,boundary,movement_blocked,authority_resolvable,transition,prohibited,p.unknowns,p.conflicts,"Explains only the first ingress authority/scope boundary owned by the source projection; does not reclassify, grant authority, formulate a bounded question, select a realization, emit events, or mutate cluster state.")

def minimum_lawful_advancement_explanation_json(e): return e.to_json_dict()
def format_minimum_lawful_advancement_explanation(e):
    lines=["Minimum Lawful Advancement Explanation",f"explanation_id: {e.explanation_id}",f"source_artifact_ref: {e.source_artifact_ref}",f"producer: {e.producer}",f"attempted_movement: {e.attempted_movement}",f"established: {e.established}",f"source_state: {e.source_state}",f"source_reason: {e.source_reason}",f"first_missing_boundary: {e.first_missing_boundary}",f"movement_blocked: {str(e.movement_blocked).lower()}",f"authority_resolvable: {str(e.authority_resolvable).lower()}",f"reconsideration_transition: {e.reconsideration_transition}",f"read_only: {str(e.read_only).lower()}",f"writes_event_ledger: {str(e.writes_event_ledger).lower()}",f"mutates_cluster: {str(e.mutates_cluster).lower()}",f"explanation_boundary: {e.explanation_boundary}"]
    for label, vals in (("prohibited_downstream_movement",e.prohibited_downstream_movement),("preserved_unknowns",e.preserved_unknowns),("preserved_conflicts",e.preserved_conflicts)):
        lines.append(label+":"); lines += [f"- {x}" for x in vals] or ["- none"]
    return "\n".join(lines)

def operator_authority_scope_binding_json(p): return p.to_json_dict()
def format_operator_authority_scope_binding(p):
    lines=["Operator Authority Scope Binding Projection",f"binding_projection_id: {p.binding_projection_id}",f"interpretation_projection_ref: {p.interpretation_projection_ref}",f"operator_identity_ref: {p.operator_identity_ref}",f"activity_class: {p.requested_activity_class}",f"requested_scope: {', '.join(p.requested_scope_expressions) or 'none'}",f"permitted_scope: {', '.join(p.permitted_scope_refs) or 'none'}",f"excluded_scope: {', '.join(p.excluded_scope_refs) or 'none'}",f"unresolved_scope: {', '.join(p.unresolved_scope_expressions) or 'none'}",f"authority_sources: {', '.join(p.authority_source_refs) or 'none'}",f"required_authority: {p.required_authority_class}",f"operator_constraints: {', '.join(p.operator_stated_effect_constraints) or 'none'}",f"presentation_preference: {p.presentation_preference or 'unspecified'}",f"state: {p.binding_state}",f"reason: {p.binding_reason}",f"required_additional_authority: {', '.join(p.required_additional_authority) or 'none'}",f"read_only: {str(p.read_only).lower()}",f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",f"mutates_cluster: {str(p.mutates_cluster).lower()}"]
    for label, vals in (("provenance",p.provenance),("unknowns",p.unknowns),("conflicts",p.conflicts),("boundary_notes",p.boundary_notes)):
        lines.append(label+":"); lines += [f"- {x}" for x in vals] or ["- none"]
    return "\n".join(lines)
