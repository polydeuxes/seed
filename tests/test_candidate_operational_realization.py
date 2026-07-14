from dataclasses import FrozenInstanceError

from seed_runtime.examination_probe_request import OperationalRealizationHandoff
from seed_runtime.candidate_operational_realization import *


def handoff():
    return OperationalRealizationHandoff("probe-1","inq-1","artifact-1","hash-1","work-1","literal-output","text/plain","text/plain",{"projection_id":"method-1"})

def bash_inputs(after=True, result="supported"):
    h=handoff(); obs=(MechanismObservation("obs-bash-exists","/bin/bash","executable_path_exists","/bin/bash","5.2",("presence",)),)
    con=(InvocationContract("contract-process","/bin/bash","text/plain","text/plain","opaque bounded process invocation","stdout","process_v1"), InvocationContract("contract-bash-literal","/bin/bash","text/plain","text/plain","echo literal","stdout","bash-fragment-v1"))
    claims=(); grams=(); bobs=(); comps=()
    if after:
        claims=(AttributedMechanismClaim("claim-echo","dungeon-artifact-1","/bin/bash","echo hello produces literal output","literal-output","dungeon",("artifact",)),)
        grams=(RecoveredInvocationGrammar("grammar-echo-literal","/bin/bash","echo hello",supported_structures=("simple literal command",),excluded_structures=("pipelines","redirection","command substitution","general scripting"),source_material_refs=("dungeon-artifact-1",)),)
        bobs=(BehavioralObservation("beh-echo","/bin/bash","echo hello","hello\n","",0,"5.2"),)
        comps=(BehaviorComparison("cmp-echo","grammar-echo-literal","beh-echo",("stdout","stderr","exit_status"),result,"bounded echo comparison"),)
    return h, obs, claims, con, grams, bobs, comps

def project(after=True, result="supported"):
    h, obs, claims, con, grams, bobs, comps = bash_inputs(after,result)
    return project_candidate_operational_realizations(h, mechanism_observations=obs, attributed_claims=claims, invocation_contracts=con, recovered_grammars=grams, behavioral_observations=bobs, behavior_comparisons=comps, shared_provenance=("fixture",))


def test_matching_inputs_immutable_deterministic_preserve_probe_and_order():
    a=project(); b=project()
    assert a == b and a.set_id == b.set_id
    assert tuple(c.candidate_id for c in a.candidates) == tuple(c.candidate_id for c in b.candidates)
    assert a.probe_request_reference == "probe-1" and a.capability_demand_reference == "literal-output"
    assert [c.candidate_id for c in a.candidates] == sorted(c.candidate_id for c in a.candidates)
    try:
        a.candidates = ()
        raise AssertionError("mutable")
    except FrozenInstanceError:
        pass


def test_input_classes_preserve_distinctions_and_declared_schema_not_validated():
    h, obs, claims, con, grams, bobs, comps = bash_inputs(True)
    assert obs[0].observation_kind == "executable_path_exists"
    assert claims[0].source_id == "dungeon-artifact-1"
    assert con[1].argument_grammar == "echo literal"
    assert grams[0].bounded_fragment == "echo hello"
    assert bobs[0].stdout == "hello\n"
    assert comps[0].result == "supported"
    before=project(after=False)
    assert any(c.grammar_standing == "declared_only" for c in before.candidates)
    assert not any(c.grammar_standing == "behaviorally_supported" for c in before.candidates)


def test_supported_and_contradicted_comparison_project_bounded_candidates():
    supported=project(True,"supported")
    contradicted=project(True,"contradicted")
    assert any(c.candidate_standing == "supported" and c.behavior_standing == "supported" for c in supported.candidates)
    bad=[c for c in contradicted.candidates if c.behavior_standing == "contradicted"]
    assert bad and bad[0].candidate_standing == "unsupported"
    assert "behavior contradicted" in bad[0].standing_reasons


def test_missing_behavior_and_mechanism_existence_alone_unknown():
    s=project(after=False)
    assert s.candidates
    assert any(c.candidate_standing == "unknown" for c in s.candidates)
    assert any(c.mechanism_availability_standing == "available" for c in s.candidates)


def test_representation_and_method_compatibility_preserve_incompatible_candidates():
    h=handoff(); con=(InvocationContract("c","m","json","bytes"),)
    b1=OperationalRealizationBasis("b1","m","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="incompatible",methodological_compatibility="satisfies")
    b2=OperationalRealizationBasis("b2","m","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="compatible",methodological_compatibility="violates")
    s=project_candidate_operational_realizations(h, invocation_contracts=con, bases=(b1,b2))
    assert len(s.candidates)==2
    assert {c.representation_compatibility for c in s.candidates} == {"compatible","incompatible"}
    assert any("representation incompatible" in c.standing_reasons for c in s.candidates)
    assert any("methodologically incompatible" in c.standing_reasons for c in s.candidates)


def test_dependency_and_authority_blocked_are_distinct_and_not_policy_denied():
    h=handoff(); con=(InvocationContract("c","m","text/plain","text/plain"),)
    bases=(OperationalRealizationBasis("bd","m","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="unavailable",authority_evidence="reachable",representation_compatibility="compatible",methodological_compatibility="satisfies"), OperationalRealizationBasis("ba","m","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="unavailable",representation_compatibility="compatible",methodological_compatibility="satisfies"))
    s=project_candidate_operational_realizations(h, invocation_contracts=con, bases=bases)
    reasons=tuple(r for c in s.candidates for r in c.standing_reasons)
    assert "dependency blocked" in reasons and "authority blocked" in reasons
    assert all("policy" not in r and "unauthorized" not in r for c in s.candidates for r in c.standing_reasons)


def test_zero_multiple_no_selection_no_reachability_no_invocation_request():
    empty=project_candidate_operational_realizations(handoff())
    assert empty.candidates == () and empty.no_known_realization_observations == ("no known realization",)
    txt=format_candidate_operational_realization_set(empty)
    assert "transformation impossible" not in txt.lower() and "capability reachability" in txt
    multi=project()
    assert len(multi.candidates) >= 2
    data=multi.to_json_dict()
    forbidden=("selected_realization","rank","invocation_request","operation_arguments","execution_proposal","pending_action")
    assert all(f not in str([c.to_json_dict() for c in multi.candidates]) for f in forbidden)
    assert "selected=false" in format_candidate_operational_realization_set(multi)


def test_bash_before_after_bounded_fragment_and_no_global_competency():
    before=project(after=False); after=project(after=True)
    assert {c.mechanism_reference for c in before.candidates} == {"/bin/bash"} == {c.mechanism_reference for c in after.candidates}
    assert {c.mechanism_version for c in before.candidates} == {"5.2"} == {c.mechanism_version for c in after.candidates}
    assert any(c.candidate_standing == "unknown" for c in before.candidates)
    assert any(c.candidate_standing == "supported" for c in after.candidates)
    supported=[c for c in after.candidates if c.candidate_standing=="supported"]
    assert supported and all(c.recovered_grammar_reference == "grammar-echo-literal" for c in supported)
    g=bash_inputs(True)[4][0]
    assert set(g.excluded_structures) == {"pipelines","redirection","command substitution","general scripting"}
    assert "global" not in str(after.to_json_dict()).lower() and "acquired bash" not in str(after.to_json_dict()).lower()


def test_internal_producer_same_shape_without_registry_or_tool_fields():
    h=handoff(); con=(InvocationContract("direct-producer-call-v1","internal:deterministic_literal_producer","text/plain","text/plain","direct producer-call contract"),)
    gram=(RecoveredInvocationGrammar("grammar-direct-literal","internal:deterministic_literal_producer","literal input to literal output",supported_structures=("literal",)),)
    obs=(BehavioralObservation("beh-internal","internal:deterministic_literal_producer","hello","hello","",0),)
    comp=(BehaviorComparison("cmp-internal","grammar-direct-literal","beh-internal",("stdout",),"supported"),)
    b=(OperationalRealizationBasis("basis-internal","internal:deterministic_literal_producer","test-impl",invocation_contract_ref="direct-producer-call-v1",recovered_grammar_ref="grammar-direct-literal",behavior_comparison_refs=("grammar-direct-literal",),availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="compatible",methodological_compatibility="satisfies"),)
    s=project_candidate_operational_realizations(h, invocation_contracts=con, recovered_grammars=gram, behavioral_observations=obs, behavior_comparisons=comp, bases=b)
    assert s.supported_references
    keys=set(s.candidates[0].to_json_dict())
    assert not ({"tool","provider","toolkit","registered_operation"} & keys)
    assert "registry" not in str(s.to_json_dict()).lower()


def test_legacy_records_can_contribute_as_adapters_without_owning_projection():
    h=handoff()
    claim=AttributedMechanismClaim("legacy-catalog-claim","CapabilityCatalog","legacy:spec","catalog says mechanism supports literal-output")
    con=InvocationContract("legacy-toolspec-contract","legacy:spec","text/plain","text/plain","compressed ToolSpec contract")
    s=project_candidate_operational_realizations(h, attributed_claims=(claim,), invocation_contracts=(con,))
    assert s.artifact_type == "CandidateOperationalRealizationSet"
    assert s.candidates[0].mechanism_reference == "legacy:spec"


def test_read_only_future_handoff_rendering_and_no_runtime_artifacts():
    s=project(); h=s.to_future_capability_reachability_handoff()
    assert h.read_only and not h.writes_event_ledger and not h.mutates_cluster
    assert not hasattr(h,"selected_realization")
    rendered=format_candidate_operational_realization_set(s)
    for phrase in ("Mechanism existence", "Declared invocation grammar", "Authority availability", "without ranking"):
        assert phrase in rendered
    data=s.to_json_dict()
    assert data["read_only"] is True and data["writes_event_ledger"] is False and data["mutates_cluster"] is False
    assert "Evidence" not in data["artifact_type"] and "Fact" not in data["artifact_type"] and "Observation" not in data["artifact_type"]
