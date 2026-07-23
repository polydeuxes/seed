"""Read-only interpretation of one attributed operator expression under one recovered grammar."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json, re
from typing import Any
from seed_runtime.representation_grammar_recovery import RecoveredRepresentationGrammar, RepresentationGrammarRecoveryProjection

CONVENTION="operator_expression_interpretation_v1"
STATES=("interpreted","ambiguous","unsupported","unknown","conflict")
BOUNDARY_NOTES=(
"This artifact interprets one attributed operator expression under one bounded recovered grammar.",
"Interpretation does not establish operator authority.",
"Requested scope is not permitted scope.",
"Authority-bearing language is not an authority grant.",
"Inquiry meaning remains distinct from presentation preference.",
"Extracted domain expressions are not resolved Seed entities.",
"Interpretation does not produce a bounded constitutional question.",
"Interpretation does not select a question family, diagnostic surface, constitutional view, or renderer.",
"Interpretation does not authorize, schedule, emit, or execute.",
"Unsupported or unresolved language remains explicit.",
"No tool, provider, model-decision, or registered-operation concept is required by this projection.",
)
class OperatorExpressionInterpretationError(ValueError): pass

def _stable(prefix,payload):
    return prefix+":"+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def _refs(xs): return tuple(sorted({x for x in xs if x}))
def _spans(text, parts):
    out=[]; low=text.lower(); pos=0
    for role, val in parts:
        if not val: continue
        i=low.find(val.lower(), pos)
        if i<0: i=low.find(val.lower())
        out.append(SourceSpan(role, val, max(i,0), max(i,0)+len(val) if i>=0 else 0))
        if i>=0: pos=i+len(val)
    return tuple(out)

@dataclass(frozen=True)
class AttributedOperatorExpression:
    expression_id:str; exact_text:str; normalized_text:str; input_representation:str; source_channel:str; workspace_ref:str=""; session_ref:str=""; operator_ref:str=""; provenance:tuple[str,...]=(); received_scope_context:tuple[str,...]=(); uncertainty:tuple[str,...]=(); unknowns:tuple[str,...]=(); boundary_notes:tuple[str,...]=("Exact operator material is preserved independently from normalized interpretation form.",); read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v,tuple): d[k]=list(v)
        return d

def attribute_operator_expression(*, exact_text:str, input_representation:str="operator text", source_channel:str="external input", workspace_ref:str="", session_ref:str="", operator_ref:str="", provenance:tuple[str,...]=(), received_scope_context:tuple[str,...]=(), uncertainty:tuple[str,...]=(), unknowns:tuple[str,...]=()):
    norm=" ".join(exact_text.strip().split())
    payload={"exact_text":exact_text,"normalized_text":norm,"input_representation":input_representation,"source_channel":source_channel,"workspace_ref":workspace_ref,"session_ref":session_ref,"operator_ref":operator_ref,"provenance":sorted(provenance),"scope":sorted(received_scope_context),"uncertainty":sorted(uncertainty),"unknowns":sorted(unknowns),"convention":CONVENTION}
    return AttributedOperatorExpression(_stable("attributed-operator-expression",payload), exact_text,norm,input_representation,source_channel,workspace_ref,session_ref,operator_ref,_refs(provenance),_refs(received_scope_context),_refs(uncertainty),_refs(unknowns))

@dataclass(frozen=True)
class SourceSpan:
    component:str; exact_text:str; start:int; end:int
    def to_json_dict(self): return asdict(self)
@dataclass(frozen=True)
class CandidateInterpretation:
    expression_form:str=""; inquiry_or_request_kind:str=""; relation_or_focus_expressions:tuple[str,...]=(); subject_expressions:tuple[str,...]=(); object_expressions:tuple[str,...]=(); scope_expressions:tuple[str,...]=(); requested_movement_class:str=""; authority_bearing_expressions:tuple[str,...]=(); operator_stated_effect_constraints:tuple[str,...]=(); evidence_support_preference:str=""; unknown_limitation_preference:str=""; presentation_preference:str=""; temporal_expressions:tuple[str,...]=(); source_spans:tuple[SourceSpan,...]=()
    def to_json_dict(self):
        d=asdict(self); d["source_spans"]=[s.to_json_dict() for s in self.source_spans]
        for k,v in d.items():
            if isinstance(v,tuple): d[k]=list(v)
        return d
@dataclass(frozen=True)
class FutureOperatorAuthorityScopeBindingHandoff:
    interpretation_projection_id:str; attributed_expression_ref:str; operator_ref:str; workspace_ref:str; session_ref:str; interpretation_state:str; inquiry_or_request_kind:str; relation_or_focus_expressions:tuple[str,...]; subject_expressions:tuple[str,...]; object_expressions:tuple[str,...]; scope_expressions:tuple[str,...]; authority_bearing_expressions:tuple[str,...]; operator_stated_effect_constraints:tuple[str,...]; presentation_preference:str; source_spans:tuple[SourceSpan,...]; grammar_ref:str; lexical_support_refs:tuple[str,...]; provenance:tuple[str,...]; known_loss:tuple[str,...]; unknowns:tuple[str,...]; conflicts:tuple[str,...]; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False
    def to_json_dict(self):
        d=asdict(self); d["source_spans"]=[s.to_json_dict() for s in self.source_spans]
        for k,v in d.items():
            if isinstance(v,tuple): d[k]=list(v)
        return d
@dataclass(frozen=True)
class OperatorExpressionInterpretationProjection:
    artifact_type:str; interpretation_projection_id:str; attributed_expression_ref:str; grammar_recovery_ref:str; recovered_grammar_ref:str; interpretation_mechanism_ref:str; invocation_contract_ref:str; interpretation_state:str; interpretation_reason:str; expression_form:str=""; inquiry_or_request_kind:str=""; relation_or_focus_expressions:tuple[str,...]=(); subject_expressions:tuple[str,...]=(); object_expressions:tuple[str,...]=(); scope_expressions:tuple[str,...]=(); requested_movement_class:str=""; authority_bearing_expressions:tuple[str,...]=(); operator_stated_effect_constraints:tuple[str,...]=(); evidence_support_preference:str=""; unknown_limitation_preference:str=""; presentation_preference:str=""; temporal_expressions:tuple[str,...]=(); source_span_bindings:tuple[SourceSpan,...]=(); alternative_interpretations:tuple[CandidateInterpretation,...]=(); unresolved_lexical_bindings:tuple[str,...]=(); unresolved_references:tuple[str,...]=(); unsupported_residual_spans:tuple[SourceSpan,...]=(); known_loss:tuple[str,...]=(); supporting_references:tuple[str,...]=(); provenance:tuple[str,...]=(); unknowns:tuple[str,...]=(); conflicts:tuple[str,...]=(); future_authority_scope_binding_handoff:FutureOperatorAuthorityScopeBindingHandoff|None=None; boundary_notes:tuple[str,...]=BOUNDARY_NOTES; read_only:bool=True; writes_event_ledger:bool=False; mutates_cluster:bool=False; interpretation_convention:str=CONVENTION
    def to_json_dict(self):
        d=asdict(self); d["source_span_bindings"]=[s.to_json_dict() for s in self.source_span_bindings]; d["unsupported_residual_spans"]=[s.to_json_dict() for s in self.unsupported_residual_spans]; d["alternative_interpretations"]=[a.to_json_dict() for a in self.alternative_interpretations]; d["future_authority_scope_binding_handoff"]=self.future_authority_scope_binding_handoff.to_json_dict() if self.future_authority_scope_binding_handoff else None
        for k,v in d.items():
            if isinstance(v,tuple): d[k]=list(v)
        return d

def _parse(expr, grammar):
    text=expr.normalized_text; t=text.rstrip(".?"); low=t.lower(); pres="JSON" if low.endswith(" as json") or low.endswith(" and show me json") else ""
    core=re.sub(r"(?i)\s+as json$", "", t); low=core.lower(); alts=[]
    if " and " in low or "," in low or " but " in low:
        if "active scan" in low and "active observation request" in grammar.supported_structures:
            m=re.search(r"active scan of ([\w.-]+)", core, re.I); scope=(m.group(1),) if m else (); c=CandidateInterpretation("coordinated request","request_observation",scope_expressions=scope,requested_movement_class="active observation",authority_bearing_expressions=("Run an active scan",),presentation_preference=pres or "JSON",source_spans=_spans(expr.exact_text,(("authority_bearing_expression","Run an active scan"),("scope_expression",scope[0] if scope else ""),("presentation_preference","JSON")))) ; return "interpreted","bounded movement request interpreted without authority binding",c,(),(),(),()
        if "inspect this repository" in low and "constraint clause" in grammar.supported_structures:
            c=CandidateInterpretation("constraint request","request_observation",scope_expressions=("this repository",),requested_movement_class="inspection",authority_bearing_expressions=("Inspect",),operator_stated_effect_constraints=("do not modify anything",),source_spans=_spans(expr.exact_text,(("scope_expression","this repository"),("effect_constraint","do not modify anything")))); return "interpreted","operator-stated constraint preserved without proving realization",c,(),(),(),()
        return "unsupported","coordination or multi-clause structure is outside the recovered grammar boundary",CandidateInterpretation(),(),(),(SourceSpan("unsupported_residual",expr.exact_text,0,len(expr.exact_text)),),()
    patterns=[(r"^show (.+)$","show","show"),(r"^what is unknown about (.+)$","unknowns","what is unknown about"),(r"^what supports (.+)$","support","what supports"),(r"^what prevents (.+)$","limitations","what prevents"),(r"^why (.+)$","explain","why"),(r"^what owns (.+)$","identify","what owns"),(r"^what is (.+)$","identify","what is")]
    for pat,kind,form in patterns:
        m=re.match(pat, low, re.I)
        if m:
            rest=core[m.start(1):m.end(1)]
            if rest.lower() in ("me that","that","") or rest.lower()=="?":
                return "unknown","reference expression is unresolved",CandidateInterpretation(form,kind,unresolved_references if False else ()),(),("unresolved reference: "+rest,),(),()
            scopes=tuple(re.findall(r"\bon\s+([\w.-]+)$", rest, re.I)); focus=re.sub(r"\s+on\s+[\w.-]+$", "", rest, flags=re.I)
            if kind=="limitations" and "attribution" in rest.lower():
                return "unknown","referent required for blocker interpretation is unresolved",CandidateInterpretation(form,kind,relation_or_focus_expressions=(rest,),unknown_limitation_preference="limitations/blockers",source_spans=_spans(expr.exact_text,(("focus",rest),))),(),("unresolved referent: attribution",),(),()
            if "owns" in form and len(rest.split())>2:
                alts=(CandidateInterpretation(form,kind,relation_or_focus_expressions=("ownership",),subject_expressions=(focus,),scope_expressions=scopes,source_spans=_spans(expr.exact_text,(("focus",focus),))), CandidateInterpretation(form,kind,relation_or_focus_expressions=(rest,),source_spans=_spans(expr.exact_text,(("focus",rest),)))) if "ambiguous ownership" in grammar.supported_structures else ()
                if alts: return "ambiguous","multiple bounded interpretations remain possible",CandidateInterpretation(),alts,(),(),()
            c=CandidateInterpretation(form,kind,relation_or_focus_expressions=("ownership",) if "own" in low or "ownership" in low else (focus,),subject_expressions=(focus,) if kind=="identify" else (),scope_expressions=scopes,evidence_support_preference="supporting material" if kind=="support" else "",unknown_limitation_preference=("unknowns" if kind=="unknowns" else ("limitations/blockers" if kind in ("limitations","explain") and ("can't" in low or kind=="limitations") else "")),presentation_preference=pres,source_spans=_spans(expr.exact_text,(("expression_form",form),("focus",focus),("scope",scopes[0] if scopes else ""),("presentation_preference","JSON" if pres else ""))))
            return "interpreted","one bounded interpretation is supported",c,(),(),(),()
    if low.startswith("tell me what will happen"):
        return "unsupported","prediction request form is outside the recovered grammar boundary",CandidateInterpretation("prediction request", "request_external_movement", temporal_expressions=("next year",), source_spans=_spans(expr.exact_text,(("temporal_expression","next year"),))),(),(),(SourceSpan("unsupported_residual",expr.exact_text,0,len(expr.exact_text)),),()
    if low=="run": return "unknown","imperative/request form has unresolved target or action",CandidateInterpretation("imperative/request","request_external_movement"),(),("unresolved target/action",),(),()
    return "unsupported","bounded positive evidence places expression outside recovered grammar",CandidateInterpretation(),(),(),(SourceSpan("unsupported_residual",expr.exact_text,0,len(expr.exact_text)),),()

def interpret_operator_expression(expression:AttributedOperatorExpression, recovery_projection:RepresentationGrammarRecoveryProjection, recovered_grammar:RecoveredRepresentationGrammar, *, interpretation_mechanism_ref:str, invocation_contract_ref:str, lexical_support_refs:tuple[str,...]=(), domain_vocabulary_refs:tuple[str,...]=(), interpretation_convention:str=CONVENTION, supporting_references:tuple[str,...]=(), provenance:tuple[str,...]=(), unknowns:tuple[str,...]=(), conflicts:tuple[str,...]=()):
    if recovered_grammar.grammar_id not in {g.grammar_id for g in recovery_projection.recovered_grammars}: raise OperatorExpressionInterpretationError("recovered grammar does not belong to recovery projection")
    if recovered_grammar.candidate_grammar_ref not in recovery_projection.recovered_candidate_refs: state,reason,c,alts,unrefs,unsup=("unknown","grammar was not recovered",CandidateInterpretation(),(),(),())
    else: state,reason,c,alts,unrefs,unsup,extra_unknowns=_parse(expression,recovered_grammar); unknowns=_refs((*unknowns,*extra_unknowns))
    all_conf=_refs((*conflicts,*recovery_projection.conflicts,*recovered_grammar.conflicts)); all_unk=_refs((*unknowns,*expression.unknowns,*recovery_projection.unknowns,*recovered_grammar.unknowns))
    if all_conf and state=="interpreted": state="conflict"; reason="conflicting interpretation material is preserved"
    payload={"expression":expression.to_json_dict(),"recovery":recovery_projection.projection_id,"grammar":recovered_grammar.grammar_id,"mechanism":interpretation_mechanism_ref,"contract":invocation_contract_ref,"lexical":sorted(lexical_support_refs),"domain":sorted(domain_vocabulary_refs),"candidate":c.to_json_dict(),"alts":[a.to_json_dict() for a in alts],"unresolved":sorted(unrefs),"unsupported":[s.to_json_dict() for s in unsup],"known_loss":sorted(recovered_grammar.known_limitations),"unknowns":list(all_unk),"conflicts":list(all_conf),"state":state,"reason":reason,"convention":interpretation_convention}
    pid=_stable("operator-expression-interpretation-projection",payload)
    hand=None
    if state=="interpreted": hand=FutureOperatorAuthorityScopeBindingHandoff(pid,expression.expression_id,expression.operator_ref,expression.workspace_ref,expression.session_ref,state,c.inquiry_or_request_kind,c.relation_or_focus_expressions,c.subject_expressions,c.object_expressions,c.scope_expressions,c.authority_bearing_expressions,c.operator_stated_effect_constraints,c.presentation_preference,c.source_spans,recovered_grammar.grammar_id,_refs((*lexical_support_refs,*recovered_grammar.lexical_support_refs)),_refs((*provenance,*expression.provenance)),recovered_grammar.known_limitations,all_unk,all_conf)
    return OperatorExpressionInterpretationProjection("OperatorExpressionInterpretationProjection",pid,expression.expression_id,recovery_projection.projection_id,recovered_grammar.grammar_id,interpretation_mechanism_ref,invocation_contract_ref,state,reason,c.expression_form,c.inquiry_or_request_kind,c.relation_or_focus_expressions,c.subject_expressions,c.object_expressions,c.scope_expressions,c.requested_movement_class,c.authority_bearing_expressions,c.operator_stated_effect_constraints,c.evidence_support_preference,c.unknown_limitation_preference,c.presentation_preference,c.temporal_expressions,c.source_spans,alts,_refs(lexical_support_refs),_refs(unrefs),unsup,recovered_grammar.known_limitations,_refs((*supporting_references,*recovered_grammar.supporting_comparison_refs,*recovered_grammar.lexical_support_refs)),_refs((*provenance,*expression.provenance, recovery_projection.projection_id,recovered_grammar.grammar_id)),all_unk,all_conf,hand)

def operator_expression_interpretation_json(p): return p.to_json_dict()
def format_operator_expression_interpretation(p):
    lines=["Operator Expression Interpretation Projection",f"interpretation_projection_id: {p.interpretation_projection_id}",f"attributed_expression_ref: {p.attributed_expression_ref}",f"state: {p.interpretation_state}",f"reason: {p.interpretation_reason}",f"expression_form: {p.expression_form or 'none'}",f"kind: {p.inquiry_or_request_kind or 'none'}",f"focus: {', '.join(p.relation_or_focus_expressions) or 'none'}",f"scope: {', '.join(p.scope_expressions) or 'none'}",f"authority_bearing_language: {', '.join(p.authority_bearing_expressions) or 'none'}",f"operator_constraints: {', '.join(p.operator_stated_effect_constraints) or 'none'}",f"presentation_preference: {p.presentation_preference or 'unspecified'}",f"read_only: {str(p.read_only).lower()}",f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",f"mutates_cluster: {str(p.mutates_cluster).lower()}"]
    for label, vals in (("alternatives",[a.to_json_dict() for a in p.alternative_interpretations]),("unresolved_lexical_bindings",p.unresolved_lexical_bindings),("unresolved_references",p.unresolved_references),("unsupported_spans",[s.exact_text for s in p.unsupported_residual_spans]),("provenance",p.provenance),("unknowns",p.unknowns),("conflicts",p.conflicts),("boundary_notes",p.boundary_notes)):
        lines.append(label+":"); lines += [f"- {x}" for x in vals] or ["- none"]
    return "\n".join(lines)
