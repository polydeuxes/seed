import pytest
from dataclasses import replace
from seed_runtime.operator_expression_interpretation import attribute_operator_expression, interpret_operator_expression, OperatorExpressionInterpretationProjection
from seed_runtime.operator_authority_scope_binding import *
from tests.test_operator_expression_interpretation import fixture, MECH

def interp(text, *, op="actor", ws="ws", sess="sess", fixture_kw=None):
    rec,g,contract_id=fixture(**(fixture_kw or {}))
    e=attribute_operator_expression(exact_text=text,workspace_ref=ws,session_ref=sess,operator_ref=op,provenance=("input",))
    p=interpret_operator_expression(e,rec,g,interpretation_mechanism_ref=MECH,invocation_contract_ref=contract_id,lexical_support_refs=("lex-operator",))
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
    assert a.binding_projection_id==b.binding_projection_id
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
    assert q.binding_state != "permitted"

def test_activity_scope_authority_and_constraints_states():
    assert bind("What owns storage on node115?")[0].binding_state=="permitted"
    assert bind("Why can't Seed establish stronger service ownership?")[0].requested_activity_class=="constitutional_read"
    repo=bind("Inspect this repository, but do not modify anything.", activity=("local_passive_observation",), scopes=("repo:/workspace/seed",), sources=("standing local passive authority",))[0]
    assert repo.binding_state=="permitted" and repo.operator_stated_effect_constraints==("do not modify anything",) and "read_only_implementation" not in str(repo.to_json_dict())
    active=bind("Run an active scan of node115 and show me JSON.", restrictions=("network_active_observation_not_granted",))[0]
    assert active.binding_state=="blocked"
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

def explain(text, **kw):
    return explain_minimum_lawful_advancement(bind(text, **kw)[0])

def test_minimum_lawful_advancement_explanation_proving_cases():
    missing = explain("Run an active scan of node115 and show me JSON.", restrictions=("network_active_observation_not_granted",))
    assert missing.source_artifact_type == "OperatorAuthorityScopeBindingProjection"
    assert missing.movement_blocked and missing.authority_resolvable
    assert "network_active_observation" in missing.first_missing_boundary
    assert "one exact bounded operator authority grant" in missing.reconsideration_transition
    assert missing.read_only and not missing.writes_event_ledger and not missing.mutates_cluster
    assert "authorize_or_execute_movement" in missing.prohibited_downstream_movement

    e,p,h=interp("Show ownership on node115.")
    p=replace(p, scope_expressions=("every node",))
    h=replace(h, scope_expressions=("every node",))
    oi,wa,sb=ctx(activity=("constitutional_read",), scopes=("node115",))
    outside=explain_minimum_lawful_advancement(bind_operator_authority_scope(p,h,e,oi,wa,sb))
    assert outside.movement_blocked and not outside.authority_resolvable
    assert "all-nodes" in outside.first_missing_boundary
    assert "network_active_observation" not in outside.reconsideration_transition

    unresolved = explain("Show ownership on node116 as JSON.")
    assert unresolved.source_state == "unknown"
    assert not unresolved.authority_resolvable
    assert "node116" in unresolved.first_missing_boundary
    assert "scope evidence or operator clarification" in unresolved.reconsideration_transition

    unknown = explain("Run an active scan of node115 and show me JSON.", activity=(), unknowns=("network authority unresolved",))
    assert unknown.source_state == "unknown"
    assert "Unknown" in unknown.first_missing_boundary
    assert unknown.preserved_unknowns == ("network authority unresolved",)

    e,p,h=interp("Run an active scan of node115 and show me JSON.")
    p=replace(p, operator_stated_effect_constraints=("do not use the network",))
    oi,wa,sb=ctx(activity=("network_active_observation",), scopes=("node115",), sources=("standing network authority",))
    conflict = explain_minimum_lawful_advancement(bind_operator_authority_scope(p,h,e,oi,wa,sb))
    assert conflict.source_state == "conflict"
    assert not conflict.authority_resolvable
    assert "must change before reconsideration" in conflict.reconsideration_transition
    assert conflict.preserved_conflicts

    permitted = explain("Show ownership on node115 as JSON.")
    assert permitted.source_state == "permitted"
    assert not permitted.movement_blocked
    assert permitted.first_missing_boundary == "none"
    assert "originate_bounded_constitutional_question" in permitted.prohibited_downstream_movement
    assert "formulate_bounded_constitutional_question" not in permitted.attempted_movement
    assert "bounded constitutional question formulation" not in permitted.attempted_movement
    assert "permitted binding stops at authority/scope preservation" in permitted.reconsideration_transition


def test_minimum_lawful_advancement_explanation_human_json_same_boundary():
    exp = explain("Run an active scan of node115 and show me JSON.", restrictions=("network_active_observation_not_granted",))
    text = format_minimum_lawful_advancement_explanation(exp)
    js = minimum_lawful_advancement_explanation_json(exp)
    for key in ("source_state", "source_reason", "first_missing_boundary", "authority_resolvable", "reconsideration_transition", "writes_event_ledger", "mutates_cluster"):
        assert key in js
        assert key + ":" in text
    assert js["first_missing_boundary"] in text
    assert js["authority_resolvable"] is True


def test_operator_ingress_binding_stops_without_question_handoff_and_preserves_fields():
    projection, expression, interpretation, _handoff, _oi, _wa, _sb = bind(
        "Show ownership on node115 as JSON.",
    )

    assert projection.binding_state == "permitted"
    assert not hasattr(projection, "future_bounded_question_handoff")
    payload = projection.to_json_dict()
    assert "future_bounded_question_handoff" not in payload
    assert payload["attributed_expression_ref"] == expression.expression_id
    assert payload["interpretation_projection_ref"] == interpretation.interpretation_projection_id
    assert payload["authority_source_refs"] == ["standing constitutional-read authority"]
    assert payload["permitted_scope_refs"] == ["node115"]
    assert payload["requested_activity_class"] == "constitutional_read"
    assert payload["presentation_preference"] == "JSON"
    assert set(("bind", "identity", "input", "scope", "session")).issubset(set(payload["provenance"]))
    assert payload["read_only"] is True
    assert payload["writes_event_ledger"] is False
    assert payload["mutates_cluster"] is False


def test_operator_ingress_non_permitted_preserves_uncertainty_and_read_only_without_handoff():
    projection = bind("Show ownership on node116 as JSON.", unknowns=("scope testimony missing",))[0]

    assert projection.binding_state == "unknown"
    assert not hasattr(projection, "future_bounded_question_handoff")
    assert projection.unresolved_scope_expressions == ("node116",)
    assert projection.unknowns == ("scope testimony missing",)
    assert set(("bind", "identity", "input", "scope", "session")).issubset(set(projection.provenance))
    assert projection.read_only is True
    assert projection.writes_event_ledger is False
    assert projection.mutates_cluster is False


def test_operator_ingress_public_surface_has_no_question_origination_symbols():
    import seed_runtime
    import seed_runtime.operator_authority_scope_binding as binding_module
    import seed_runtime.bounded_constitutional_question as question_module

    deleted = (
        "FutureBoundedConstitutionalQuestionHandoff",
        "formulate_bounded_constitutional_question",
        "BoundedConstitutionalQuestionFormulationError",
        "FORMULATION_CONVENTION",
    )
    for name in deleted:
        assert name not in seed_runtime.__all__
        assert not hasattr(seed_runtime, name)
    assert not hasattr(binding_module, "FutureBoundedConstitutionalQuestionHandoff")
    assert not hasattr(question_module, "formulate_bounded_constitutional_question")


def test_no_operator_ingress_function_can_produce_bounded_constitutional_question():
    import seed_runtime.operator_authority_scope_binding as binding_module
    from seed_runtime.bounded_constitutional_question import BoundedConstitutionalQuestion

    projection = bind("Show ownership on node115 as JSON.")[0]
    for name in ("bind_operator_authority_scope", "explain_minimum_lawful_advancement"):
        assert "BoundedConstitutionalQuestion" not in getattr(binding_module, name).__annotations__.values()
    assert not isinstance(projection, BoundedConstitutionalQuestion)
    assert "BoundedConstitutionalQuestion" not in str(projection.to_json_dict())
