import pytest
from seed_runtime.candidate_external_grammar import CandidateExternalGrammarInput, CandidateExternalGrammarInputCandidate, assemble_candidate_external_grammar_set
from seed_runtime.representation_grammar_recovery import CandidateRecoveryMaterial, RepresentationGrammarComparison, LexicalSupportReference, recover_representation_grammars
from seed_runtime.representation_grammar_applicability import ApplicabilityDemandMaterial, RepresentationGrammarApplicabilityError, project_representation_grammar_applicability, format_representation_grammar_applicability
from seed_runtime.candidate_operational_realization import InvocationContract, MechanismObservation, project_candidate_operational_realizations
from seed_runtime.examination_probe_request import OperationalRealizationHandoff


def recovery(cid="eng-simple", scope="english text"):
    cs=assemble_candidate_external_grammar_set(CandidateExternalGrammarInput(scope,(CandidateExternalGrammarInputCandidate(cid,"simple declarative sentence -> explicit subject + simple predicate", provenance=("candidate-source",)),)))
    cmp=(RepresentationGrammarComparison("cmp-"+cid,cid,"mat","subject+predicate","subject+predicate",("structure",),"supports","fixture support"),)
    lex=(LexicalSupportReference("lex-dog", "fixture", "dog/runs", cid, "subject predicate roles"),)
    mat=(CandidateRecoveryMaterial(cid,scope,"simple declarative sentence -> explicit subject + simple predicate",source_material_refs=("mat",),supporting_comparison_refs=("cmp-"+cid,),lexical_support_refs=("lex-dog",),supported_structures=("explicit subject","simple predicate","literal output"),excluded_structures=("imperative","pipeline","subordinate clause"),applicability_boundary=("simple declarative English sentence","bounded literal output"),known_limitations=("not full English",),provenance=("recovery-fixture",)),)
    p=recover_representation_grammars(cs, comparisons=cmp, lexical_support=lex, recovery_material=mat)
    return p,p.recovered_grammars[0]

def handoff(probe="probe-1", demand="project subject predicate", inp="english text", out="subject/predicate projection"):
    return OperationalRealizationHandoff(probe,"inq","artifact","hash","work",demand,inp,out,{"projection_id":"method"})

def contract(cid="contract-1", mech="internal:deterministic-structural-producer", inp="english text", out="subject/predicate projection"):
    return InvocationContract(cid,mech,inp,out,"exact text + recovered grammar ref","bounded projection",provenance=("contract-src",))

def demand(**kw):
    d=dict(material_class_identity="simple declarative English sentence",source_representation="english text",required_target_representation="subject/predicate projection",required_structures=("explicit subject","simple predicate"),lexical_support_refs=("lex-dog",),required_lexical_refs=("lex-dog",),applicability_boundary_refs=("simple declarative English sentence",),provenance=("probe-1",))
    d.update(kw); return ApplicabilityDemandMaterial(**d)

def proj(**kw):
    p,g=recovery(); h=kw.pop("h", handoff()); c=kw.pop("c", contract()); m=kw.pop("m", c.mechanism_id); d=kw.pop("d", demand())
    return project_representation_grammar_applicability(p,g,h,m,c,d,**kw)


def test_applicable_projection_shape_rendering_and_read_only_handoff():
    a=proj()
    assert a.artifact_type=="RepresentationGrammarApplicabilityProjection"
    assert a.applicability_state=="applicable"
    assert a.future_candidate_realization_handoff is not None
    assert a.read_only and not a.writes_event_ledger and not a.mutates_cluster
    text=format_representation_grammar_applicability(a)
    assert "mechanism" in text and "does not own the grammar" in text
    assert "CapabilityReachability" not in a.future_candidate_realization_handoff.to_json_dict()


def test_identity_is_deterministic_order_independent_and_changes_for_relevant_inputs():
    a=proj(); b=proj(); assert a.applicability_projection_id==b.applicability_projection_id
    variants=[
        dict(d=demand(required_structures=("simple predicate","explicit subject"), lexical_support_refs=("lex-dog",))),
        dict(c=contract(cid="contract-2")),
        dict(c=contract(mech="internal:other"), m="internal:other"),
        dict(h=handoff(probe="probe-2"), d=demand(provenance=("probe-2",))),
        dict(h=handoff(demand="other demand")),
        dict(h=handoff(inp="other"), d=demand(source_representation="other")),
        dict(h=handoff(out="other"), c=contract(out="other"), d=demand(required_target_representation="other")),
        dict(d=demand(lexical_support_refs=("lex-other",), required_lexical_refs=("lex-other",))),
        dict(d=demand(applicability_boundary_refs=("bounded literal output",), material_class_identity="bounded literal output", required_structures=("literal output",))),
        dict(d=demand(fidelity_constraints=("lossless",), known_loss_refs=("loss",))),
        dict(d=demand(attribution_constraints=("preserve attribution",))),
        dict(d=demand(claim_treatment_constraints=("preserve claim treatment",))),
        dict(d=demand(known_loss_refs=("loss-2",))),
        dict(d=demand(unknowns=("u",))),
        dict(d=demand(conflicts=("c",))),
        dict(applicability_state="unknown", applicability_reason="forced unknown"),
    ]
    assert all(proj(**v).applicability_projection_id != a.applicability_projection_id for v in variants)
    p2,g2=recovery(cid="eng-simple-2"); assert project_representation_grammar_applicability(p2,g2, handoff(), contract().mechanism_id, contract(), demand()).applicability_projection_id != a.applicability_projection_id


def test_identity_validation_and_candidate_rejection_controls():
    p,g=recovery(); p2,_=recovery(cid="other")
    with pytest.raises(RepresentationGrammarApplicabilityError): project_representation_grammar_applicability(p2,g,handoff(),contract().mechanism_id,contract(),demand())
    with pytest.raises(RepresentationGrammarApplicabilityError): project_representation_grammar_applicability(p,g,handoff(probe="x"),contract().mechanism_id,contract(),demand())
    with pytest.raises(RepresentationGrammarApplicabilityError): project_representation_grammar_applicability(p,g,handoff(inp="x"),contract().mechanism_id,contract(),demand())
    with pytest.raises(RepresentationGrammarApplicabilityError): project_representation_grammar_applicability(p,g,handoff(),"wrong",contract(),demand())


def test_states_for_english_boundaries_lexical_unknown_counterexample_and_contract_mismatch():
    assert proj(d=demand(required_structures=("subordinate clause",))).applicability_state=="not_applicable"
    assert proj(d=demand(required_structures=("coordination",))).applicability_state=="unknown"
    assert proj(d=demand(required_lexical_refs=("lex-ambiguous",))).applicability_state=="unknown"
    assert proj(d=demand(required_structures=("imperative",), material_class_identity="imperative English sentence")).applicability_state=="not_applicable"
    assert proj(c=contract(inp="json"), d=demand()).applicability_state=="not_applicable"


def test_bash_literal_excluded_unknown_and_no_execution_or_command_construction():
    p,g=recovery(cid="bash-literal", scope="bounded Bash source representation")
    h=handoff(demand="produce one bounded literal output", inp="bounded Bash source representation", out="stdout/stderr/status")
    c=contract(cid="bash-contract", mech="/bin/bash", inp="bounded Bash source representation", out="stdout/stderr/status")
    d=demand(material_class_identity="bounded literal output", source_representation="bounded Bash source representation", required_target_representation="stdout/stderr/status", required_structures=("literal output",), applicability_boundary_refs=("bounded literal output",), provenance=("probe-1",))
    a=project_representation_grammar_applicability(p,g,h,"/bin/bash",c,d)
    assert a.applicability_state=="applicable"
    assert "echo hello" not in str(a.to_json_dict())
    assert project_representation_grammar_applicability(p,g,h,"/bin/bash",c,ApplicabilityDemandMaterial(**{**d.to_json_dict(),"required_structures":("pipeline",)})).applicability_state=="not_applicable"
    assert project_representation_grammar_applicability(p,g,h,"/bin/bash",c,ApplicabilityDemandMaterial(**{**d.to_json_dict(),"required_structures":("brace expansion",)})).applicability_state=="unknown"


def test_multiple_mechanisms_multiple_grammars_no_selection_and_candidate_integration_without_legacy_grammar():
    a=proj(); a2=proj(c=contract(cid="contract-2", mech="internal:producer-2"), m="internal:producer-2")
    assert a.future_candidate_realization_handoff.mechanism_ref != a2.future_candidate_realization_handoff.mechanism_ref
    assert a.applicability_projection_id != a2.applicability_projection_id
    p2,g2=recovery(cid="bash-literal", scope="english text")
    a3=project_representation_grammar_applicability(p2,g2,handoff(),contract().mechanism_id,contract(),demand())
    assert a3.recovered_grammar_ref != a.recovered_grammar_ref
    cs=project_candidate_operational_realizations(handoff(), invocation_contracts=(contract(),), mechanism_observations=(MechanismObservation("obs", contract().mechanism_id, "identity", "internal"),), representation_grammar_applicability_handoffs=(a.future_candidate_realization_handoff,))
    assert len(cs.candidates)==1
    cand=cs.candidates[0]
    assert cand.recovered_grammar_reference==a.recovered_grammar_ref
    assert cand.invocation_contract_reference==contract().contract_id
    assert cand.mechanism_reference==contract().mechanism_id
    assert cand.grammar_standing=="recovered_only"
    assert not hasattr(cs,"selected_candidate")


def test_non_applicable_unknown_conflict_emit_no_positive_handoff_and_do_not_mutate():
    assert proj(d=demand(required_structures=("imperative",))).future_candidate_realization_handoff is None
    assert proj(d=demand(required_structures=("coordination",))).future_candidate_realization_handoff is None
    assert proj(d=demand(conflicts=("conflict",))).future_candidate_realization_handoff is None
