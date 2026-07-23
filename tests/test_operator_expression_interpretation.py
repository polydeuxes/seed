import pytest
from seed_runtime.candidate_external_grammar import CandidateExternalGrammarInput, CandidateExternalGrammarInputCandidate, assemble_candidate_external_grammar_set
from seed_runtime.representation_grammar_recovery import CandidateRecoveryMaterial, RepresentationGrammarComparison, LexicalSupportReference, recover_representation_grammars
from seed_runtime.operator_expression_interpretation import attribute_operator_expression, interpret_operator_expression, format_operator_expression_interpretation, operator_expression_interpretation_json, OperatorExpressionInterpretationError

MECH="internal:operator-expression-interpreter"

def fixture(cid="operator-grammar", structures=None, conflicts=(), unknowns=(), lex=("lex-operator",)):
    structures=structures or ("show form","what is form","what owns form","why form","what supports form","what is unknown about form","what prevents form","presentation clause","active observation request","constraint clause","imperative/request")
    cs=assemble_candidate_external_grammar_set(CandidateExternalGrammarInput("operator expression text",(CandidateExternalGrammarInputCandidate(cid,"bounded operator expression grammar",provenance=("candidate",)),)))
    cmp=(RepresentationGrammarComparison("cmp-"+cid,cid,"mat","bounded forms","bounded forms",("structure",),"supports","fixture"),)
    lxs=tuple(LexicalSupportReference(x,"fixture",x,cid,"operator-expression lexical role") for x in lex)
    mat=(CandidateRecoveryMaterial(cid,"operator expression text","bounded operator expression grammar",source_material_refs=("mat",),supporting_comparison_refs=("cmp-"+cid,),lexical_support_refs=lex,supported_structures=structures,excluded_structures=("unrestricted coordination","prediction request","full English"),applicability_boundary=("operator-expression interpretation mechanism","single attributed operator expression"),known_limitations=("not full English",),provenance=("recovery",),unknowns=unknowns,conflicts=conflicts),)
    rec=recover_representation_grammars(cs,comparisons=cmp,lexical_support=lxs,recovery_material=mat)
    g=rec.recovered_grammars[0]
    return rec,g,"contract-oe"

def interp(text, **kw):
    rec,g,contract_id=fixture(**kw.pop("fixture",{}))
    expr=attribute_operator_expression(exact_text=text,workspace_ref="ws",session_ref="sess",operator_ref="actor",provenance=("input",))
    return interpret_operator_expression(expr,rec,g,interpretation_mechanism_ref=MECH,invocation_contract_ref=contract_id,lexical_support_refs=kw.pop("lexical_support_refs",("lex-operator",)),**kw)

def test_projection_shape_deterministic_identity_and_read_only_handoff():
    a=interp("Show ownership on node115 as JSON."); b=interp("Show ownership on node115 as JSON.")
    assert a.artifact_type=="OperatorExpressionInterpretationProjection"
    assert a.interpretation_projection_id==b.interpretation_projection_id
    assert a.interpretation_state=="interpreted"
    assert a.presentation_preference=="JSON" and not hasattr(a,"renderer")
    assert a.future_authority_scope_binding_handoff is not None
    assert a.read_only and not a.writes_event_ledger and not a.mutates_cluster
    assert "BoundedConstitutionalQuestion" not in str(a.to_json_dict())

def test_identity_changes_for_required_semantic_inputs_and_order_independent():
    base=interp("What supports storage ownership on node115?")
    variants=[
        interp(" What supports storage ownership on node115?"),
        interp("What supports storage ownership on node116?"),
        interp("What supports storage ownership on node115?", fixture={"cid":"operator-grammar-2"}),
        interp("What supports storage ownership on node115?", lexical_support_refs=("lex-other",)),
        interp("What supports storage ownership on node115?", unknowns=("u",)),
        interp("What supports storage ownership on node115?", conflicts=("c",)),
    ]
    assert all(v.interpretation_projection_id != base.interpretation_projection_id for v in variants)
    ordered=interp("What supports storage ownership on node115?", lexical_support_refs=("b","a"))
    ordered2=interp("What supports storage ownership on node115?", lexical_support_refs=("a","b"))
    assert ordered.interpretation_projection_id==ordered2.interpretation_projection_id

def test_mismatched_inputs_fail_and_non_applicable_states_do_not_interpret_or_handoff():
    rec,g,c=fixture(); rec2,g2,c2=fixture(cid="other")
    expr=attribute_operator_expression(exact_text="Show ownership on node115")
    with pytest.raises(OperatorExpressionInterpretationError): interpret_operator_expression(expr,rec2,g,interpretation_mechanism_ref=MECH,invocation_contract_ref=c)
    p=interp("Show ownership on node115", conflicts=("interpretation conflict",))
    assert p.interpretation_state == "conflict"
    assert p.future_authority_scope_binding_handoff is None

def test_proving_cases_and_boundaries():
    owns=interp("What owns storage on node115?", fixture={"structures":("what owns form","ambiguous ownership","show form")})
    assert owns.interpretation_state=="ambiguous" and len(owns.alternative_interpretations)==2
    assert interp("Why can't Seed establish stronger service ownership?").inquiry_or_request_kind=="explain"
    assert interp("What supports storage ownership on node115?").evidence_support_preference=="supporting material"
    unk=interp("What is unknown about service ownership on node115?"); assert unk.inquiry_or_request_kind=="unknowns" and unk.unknown_limitation_preference=="unknowns"
    blocker=interp("What prevents stronger attribution?"); assert blocker.interpretation_state=="unknown"
    active=interp("Run an active scan of node115 and show me JSON."); assert active.requested_movement_class=="active observation" and active.future_authority_scope_binding_handoff is not None and "authority_granted" not in str(active.to_json_dict()) and "pending" not in str(active.to_json_dict())
    constraint=interp("Inspect this repository, but do not modify anything."); assert constraint.operator_stated_effect_constraints==("do not modify anything",)
    ref=interp("Show me that."); assert ref.interpretation_state=="unknown"
    multi=interp("What owns storage on node115, why does Seed believe that, and what remains unknown?"); assert multi.interpretation_state=="unsupported"
    pred=interp("Tell me what will happen to node115 next year."); assert pred.interpretation_state=="unsupported"
    run=interp("Run."); assert run.interpretation_state=="unknown"

def test_no_resolution_selection_dispatch_execution_or_mutation_and_rendering_shape():
    p=interp("Show ownership on node115 as JSON.")
    blob=str(p.to_json_dict())
    for forbidden in ("selection_key","diagnostic_name","constitutional_view","question_family","authority_granted","scope_permitted","execution_proposal","Observation","Evidence","Fact"):
        assert forbidden not in blob
    assert p.scope_expressions==("node115",) and "resolved_entity" not in blob
    text=format_operator_expression_interpretation(p)
    assert "state:" in text and "boundary_notes:" in text and "presentation_preference: JSON" in text
    js=operator_expression_interpretation_json(p)
    assert js["read_only"] is True and js["writes_event_ledger"] is False and js["mutates_cluster"] is False
