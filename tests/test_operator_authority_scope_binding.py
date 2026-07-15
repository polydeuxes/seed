import pytest
from dataclasses import replace
from seed_runtime.operator_expression_interpretation import attribute_operator_expression, interpret_operator_expression, OperatorExpressionInterpretationProjection
from seed_runtime.operator_authority_scope_binding import *
from tests.test_operator_expression_interpretation import fixture, MECH

def interp(text, *, op="actor", ws="ws", sess="sess", fixture_kw=None):
    rec,g,app,c=fixture(**(fixture_kw or {}))
    e=attribute_operator_expression(exact_text=text,workspace_ref=ws,session_ref=sess,operator_ref=op,provenance=("input",))
    p=interpret_operator_expression(e,rec,g,app,interpretation_mechanism_ref=MECH,invocation_contract_ref=c.contract_id,lexical_support_refs=("lex-operator",))
    return e,p,p.future_authority_scope_binding_handoff

def ctx(activity=("constitutional_read",), scopes=("node115",), *, op="actor", ws="ws", sess="sess", sources=("standing constitutional-read authority",), unknowns=(), restrictions=(), grantable=()):
    oi=OperatorIdentityContext(op,"operator:verified:"+op,activity,grantable,("identity",),unknowns)
    wa=WorkspaceSessionAuthorityContext(ws,sess,"authctx",True,scopes,(),restrictions,sources,("session",),unknowns)
    sb=ScopeBindingContext("scopectx",ws,(("node115","node115"),("this repository","repo:/workspace/seed"),("service configuration","service-config"),("every node","all-nodes")),(),(),("scope",),unknowns)
    return oi,wa,sb

def bind(text, activity=("constitutional_read",), scopes=("node115",), **kw):
    ikw={k:kw.pop(k) for k in list(kw) if k in ("op","ws","sess","fixture_kw")}
    e,p,h=interp(text, **ikw)
    for k in ("op","ws","sess"):
        if k in ikw: kw[k]=ikw[k]
    oi,wa,sb=ctx(activity,scopes, **kw)
    return bind_operator_authority_scope(p,h,e,oi,wa,sb,provenance=("bind",)), e,p,h,oi,wa,sb

def test_permitted_projection_identity_ordering_and_input_changes():
    a,*_=bind("Show ownership on node115 as JSON.")
    b,*_=bind("Show ownership on node115 as JSON.")
    assert a.artifact_type=="OperatorAuthorityScopeBindingProjection" and a.binding_state=="permitted"
    assert a.binding_projection_id==b.binding_projection_id and a.future_bounded_question_handoff is not None
    variants=[
        bind("Why stronger service ownership on node115?")[0],
        bind("Show ownership on node116 as JSON.")[0],
        bind("Show ownership on node115 as JSON.", op="other")[0],
        bind("Show ownership on node115 as JSON.", ws="ws2")[0],
        bind("Show ownership on node115 as JSON.", sess="sess2")[0],
        bind("Run an active scan of node115 and show me JSON.", activity=("network_active_observation",))[0],
        bind("Show ownership on node115 as JSON.", scopes=())[0],
        bind("Show ownership on node115 as JSON.", scopes=("node115",), sources=("other authority",))[0],
    ]
    assert all(v.binding_projection_id != a.binding_projection_id for v in variants)
    oi,wa,sb=ctx(sources=("b","a")); e,p,h=interp("Show ownership on node115 as JSON.")
    x=bind_operator_authority_scope(p,h,e,oi,wa,sb,provenance=("z","a"))
    oi2,wa2,sb2=ctx(sources=("a","b")); y=bind_operator_authority_scope(p,h,e,oi2,wa2,sb2,provenance=("a","z"))
    assert x.binding_projection_id==y.binding_projection_id

def test_mismatches_and_non_interpreted_do_not_permit():
    e,p,h=interp("Show ownership on node115 as JSON."); oi,wa,sb=ctx()
    with pytest.raises(OperatorAuthorityScopeBindingError): bind_operator_authority_scope(p,replace(h,interpretation_projection_id="bad"),e,oi,wa,sb)
    with pytest.raises(OperatorAuthorityScopeBindingError): bind_operator_authority_scope(p,h,replace(e,expression_id="bad"),oi,wa,sb)
    with pytest.raises(OperatorAuthorityScopeBindingError): bind_operator_authority_scope(p,h,e,replace(oi,operator_ref="bad"),wa,sb)
    with pytest.raises(OperatorAuthorityScopeBindingError): bind_operator_authority_scope(p,h,e,oi,replace(wa,workspace_ref="bad"),sb)
    with pytest.raises(OperatorAuthorityScopeBindingError): bind_operator_authority_scope(p,h,e,oi,replace(wa,session_ref="bad"),sb)
    e2,p2,h2=interp("Show me that."); assert h2 is None
    hfake=replace(h, interpretation_projection_id=p2.interpretation_projection_id, attributed_expression_ref=e2.expression_id)
    q=bind_operator_authority_scope(p2,hfake,e2,oi,wa,sb)
    assert q.binding_state != "permitted" and q.future_bounded_question_handoff is None

def test_activity_scope_authority_and_constraints_states():
    assert bind("What owns storage on node115?")[0].binding_state=="permitted"
    assert bind("Why can't Seed establish stronger service ownership?")[0].requested_activity_class=="constitutional_read"
    repo=bind("Inspect this repository, but do not modify anything.", activity=("local_passive_observation",), scopes=("repo:/workspace/seed",), sources=("standing local passive authority",))[0]
    assert repo.binding_state=="permitted" and repo.operator_stated_effect_constraints==("do not modify anything",) and "read_only_implementation" not in str(repo.to_json_dict())
    active=bind("Run an active scan of node115 and show me JSON.", restrictions=("network_active_observation_not_granted",))[0]
    assert active.binding_state=="blocked" and active.future_bounded_question_handoff is None
    unk=bind("Run an active scan of node115 and show me JSON.", activity=(), unknowns=("network authority unresolved",))[0]
    assert unk.binding_state=="unknown"
    e_priv,p_priv,h_base=interp("Show ownership on node115.")
    p_priv=replace(p_priv, requested_movement_class="privileged observation", scope_expressions=("service configuration",))
    h_priv=replace(h_base, scope_expressions=("service configuration",))
    oi_priv,wa_priv,sb_priv=ctx(activity=(), scopes=("service-config",))
    priv=bind_operator_authority_scope(p_priv,h_priv,e_priv,oi_priv,wa_priv,sb_priv)
    assert priv.binding_state!="permitted"
    e_every,p_every,h_every=interp("Show ownership on node115.")
    p_every=replace(p_every, scope_expressions=("every node",))
    h_every=replace(h_every, scope_expressions=("every node",))
    oi_every,wa_every,sb_every=ctx(scopes=("node115",))
    every=bind_operator_authority_scope(p_every,h_every,e_every,oi_every,wa_every,sb_every)
    assert every.binding_state in ("blocked","unknown") and (every.excluded_scope_refs or every.unresolved_scope_expressions)
    conflict=bind("Show ownership on node115.")[0]
    e,p,h=interp("Show ownership on node115."); oi,wa,sb=ctx(); sb=replace(sb,conflicting_scope_expressions=("node115",))
    conflict=bind_operator_authority_scope(p,h,e,oi,wa,sb); assert conflict.binding_state=="conflict"

def test_authority_language_identity_defaults_and_boundary_exclusions():
    granted=bind("Run an active scan of node115 and show me JSON.", activity=(), grantable=("network_active_observation",))[0]
    assert granted.binding_state=="permitted" and "explicit_operator_grant" in granted.authority_source_refs
    not_granted=bind("Run an active scan of node115 and show me JSON.", activity=())[0]
    assert not_granted.binding_state in ("blocked","unknown")
    noauth=bind("Show ownership on node115 as JSON.", activity=(), unknowns=())[0]
    assert noauth.binding_state=="blocked"
    assert "renderer" not in str(granted.to_json_dict())
    blob=str(granted.to_json_dict())
    for forbidden in ("bounded_question': ", "constitutional_intent", "selection_key", "diagnostic", "constitutional_view", "execution_proposal", "pending_action", "Observation", "Evidence", "Fact", "root_available"):
        assert forbidden not in blob
    text=format_operator_authority_scope_binding(granted)
    for term in ("state:","reason:","activity_class:","permitted_scope:","authority_sources:","operator_constraints:","unknowns:","conflicts:","boundary_notes:"):
        assert term in text
    js=operator_authority_scope_binding_json(granted)
    assert js["read_only"] and not js["writes_event_ledger"] and not js["mutates_cluster"]
