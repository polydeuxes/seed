from dataclasses import FrozenInstanceError, replace
import pytest

from seed_runtime.candidate_operational_realization import *
from seed_runtime.examination_probe_request import OperationalRealizationHandoff
from seed_runtime.capability_reachability_projection import *


def handoff(demand="literal-output"):
    return OperationalRealizationHandoff("probe-1","inq-1","artifact-1","hash-1","work-1",demand,"text/plain","text/plain",{"projection_id":"method-1"})

def cand_set(*bases, demand="literal-output", set_unknowns=(), comps=(), grams=(), contracts=None, obs=()):
    h=handoff(demand)
    if contracts is None: contracts=(InvocationContract("c","m","text/plain","text/plain","echo literal"),)
    return project_candidate_operational_realizations(h, invocation_contracts=contracts, recovered_grammars=grams, behavioral_observations=obs, behavior_comparisons=comps, bases=tuple(bases), set_unknowns=set_unknowns, shared_provenance=("fixture",))

def supported_basis(b="b", m="m", dep="available", auth="reachable"):
    return OperationalRealizationBasis(b,m,"1",invocation_contract_ref="c",recovered_grammar_ref="g",behavior_comparison_refs=("g",),availability_evidence="available",dependency_evidence=dep,authority_evidence=auth,representation_compatibility="compatible",methodological_compatibility="satisfies")

def supported_set(n=1, demand="literal-output", dep="available", auth="reachable"):
    bases=tuple(supported_basis(f"b{i}", f"m{i}", dep, auth) for i in range(n))
    contracts=tuple(InvocationContract("c", f"m{i}", "text/plain", "text/plain", "echo literal") for i in range(n)) or (InvocationContract("c","m0","text/plain","text/plain","echo literal"),)
    grams=tuple(RecoveredInvocationGrammar("g", f"m{i}", "echo hi", supported_structures=("literal",), excluded_structures=("pipelines","redirection","command substitution","general scripting")) for i in range(n))
    obs=tuple(BehavioralObservation(f"o{i}", f"m{i}", "echo hi", "hi\n", "", 0, "1") for i in range(n))
    comps=tuple(BehaviorComparison(f"cmp{i}", "g", f"o{i}", ("stdout",), "supported") for i in range(n))
    return cand_set(*bases, demand=demand, contracts=contracts, grams=grams, obs=obs, comps=comps)

def proj(s): return project_capability_reachability(s, s.to_future_capability_reachability_handoff())


def test_matching_inputs_immutable_deterministic_identity_and_ordering_changes():
    s=supported_set(1); p=proj(s); p2=proj(s)
    assert p == p2 and p.projection_id == p2.projection_id
    assert p.artifact_type == "CapabilityReachabilityProjection"
    assert p.supporting_candidate_references == tuple(c.candidate_id for c in s.candidates if c.candidate_standing=="supported")
    with pytest.raises(FrozenInstanceError): p.reachability_state="x"
    changed=replace(s, set_id=s.set_id+":changed")
    assert proj(changed).projection_id != p.projection_id
    sdep=supported_set(1, dep="unavailable"); sauth=supported_set(1, auth="unavailable")
    assert proj(sdep).projection_id != p.projection_id
    assert proj(sauth).projection_id != p.projection_id
    unsupported=cand_set(OperationalRealizationBasis("b","m","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="incompatible",methodological_compatibility="satisfies"))
    assert proj(unsupported).projection_id != p.projection_id

@pytest.mark.parametrize("mut,msg",[
    (lambda s,h: replace(h,candidate_set_id="wrong"),"candidate set"),
    (lambda s,h: replace(h,probe_request_reference="wrong"),"probe-request"),
    (lambda s,h: replace(h,capability_demand_reference="wrong"),"capability-demand"),
    (lambda s,h: replace(h,candidate_references=h.candidate_references+("missing",)),"candidate references"),
    (lambda s,h: replace(h,candidate_standings={**h.candidate_standings,h.candidate_references[0]:"unknown"}),"standing mismatch"),
    (lambda s,h: replace(h,dependency_observations=("unknown",)),"dependency"),
    (lambda s,h: replace(h,authority_observations=("unknown",)),"authority"),
])
def test_mismatched_candidate_set_and_handoff_fail_deterministically(mut,msg):
    s=supported_set(1); h=s.to_future_capability_reachability_handoff()
    with pytest.raises(CapabilityReachabilityProjectionError, match=msg):
        project_capability_reachability(s, mut(s,h))


def test_reachable_multiple_preserves_all_and_selects_none():
    p=proj(supported_set(2))
    assert p.reachability_state == "reachable"
    assert len(p.supporting_candidate_references) == 2
    assert p.future_selection_handoff and p.future_selection_handoff.selection_lawful_now is True
    assert not hasattr(p, "selected_candidate") and "selected_candidate: none" in format_capability_reachability_projection(p)


def test_blocked_authority_dependency_distinct_not_policy_denied():
    pdep=proj(supported_set(1, dep="unavailable")); pauth=proj(supported_set(1, auth="unavailable"))
    assert pdep.reachability_state == pauth.reachability_state == "blocked"
    assert pdep.dependency_blockers and not pdep.authority_blockers
    assert pauth.authority_blockers and not pauth.dependency_blockers
    text=format_capability_reachability_projection(pauth).lower()
    assert "unauthorized" not in text and "policy denied" not in text


def test_unsupported_requires_positive_bounded_evidence_and_completeness_not_invented():
    a=OperationalRealizationBasis("a","ma","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="incompatible",methodological_compatibility="satisfies")
    b=OperationalRealizationBasis("b","mb","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="compatible",methodological_compatibility="violates")
    s=cand_set(a,b); assert proj(s).reachability_state == "unsupported"
    sincomplete=replace(s, unknowns=("candidate_space_incomplete",))
    assert proj(sincomplete).reachability_state == "unknown"
    assert "candidate_space_incomplete" in proj(sincomplete).unknowns


def test_zero_no_known_realization_unknown_not_impossible_or_unsupported():
    p=proj(project_candidate_operational_realizations(handoff()))
    assert p.reachability_state == "unknown"
    assert p.conclusion_reason == "no known realization"
    assert p.no_known_realization_observations == ("no known realization",)
    assert p.reachability_state != "unsupported" and "transformation impossible" not in format_capability_reachability_projection(p).lower()


def test_unknown_dimensions_and_conflict():
    u=cand_set(OperationalRealizationBasis("u","m","",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="unknown",methodological_compatibility="cannot_establish"))
    p=proj(u)
    assert p.reachability_state == "unknown" and p.unknown_candidate_references
    conflict=cand_set(OperationalRealizationBasis("x","m","",invocation_contract_ref="c",availability_evidence="conflict",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="compatible",methodological_compatibility="satisfies",conflicts=("same candidate incompatible standings",)))
    assert proj(conflict).reachability_state == "conflict"


def test_bash_before_after_distinct_demands_no_global_competency():
    before_literal=cand_set(OperationalRealizationBasis("b","/bin/bash","5.2",invocation_contract_ref="c",availability_evidence="available",dependency_evidence="available",authority_evidence="reachable",representation_compatibility="compatible",methodological_compatibility="satisfies"), contracts=(InvocationContract("c","/bin/bash","text/plain","text/plain","echo literal"),))
    before_opaque=supported_set(1, demand="invoke /bin/bash as one opaque bounded process")
    after=supported_set(1, demand="produce bounded literal output through constructed Bash grammar")
    assert proj(before_literal).reachability_state == "unknown"
    assert proj(before_opaque).reachability_state == "reachable"
    assert before_literal.capability_demand_reference != before_opaque.capability_demand_reference
    pa=proj(after)
    assert pa.reachability_state == "reachable"
    assert {c.mechanism_version for c in after.candidates} == {"1"}
    assert all("general" not in r.lower() for r in pa.supporting_candidate_references)
    assert "global bash" not in str(pa.to_json_dict()).lower()


def test_internal_producer_no_registry_and_read_only_non_mutation():
    p=proj(supported_set(1, demand="internal deterministic producer literal output"))
    assert p.reachability_state == "reachable"
    data=p.to_json_dict(); txt=format_capability_reachability_projection(p)
    assert data["read_only"] is True and data["writes_event_ledger"] is False and data["mutates_cluster"] is False
    for word in ("tool_registry","invocation_request","operation_arguments","execution_proposal","pending_action"):
        assert word not in str(data).lower()
    assert "boundary_notes" in txt and "supporting_candidates" in txt and "unknowns" in txt and "conflicts" in txt
    assert p.future_selection_handoff and not hasattr(p.future_selection_handoff,"invocation_request")
