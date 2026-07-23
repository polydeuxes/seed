"""Read-only applicability projection from recovered representation grammar to one mechanism contract."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.representation_grammar_recovery import RecoveredRepresentationGrammar, RepresentationGrammarRecoveryProjection

CONVENTION = "representation_grammar_applicability_v1"
STATES = ("applicable", "not_applicable", "unknown", "conflict")
BOUNDARY_NOTES = (
    "This artifact projects whether one recovered representation grammar is applicable through one mechanism and invocation contract for one exact bounded demand.",
    "The recovered grammar remains mechanism-neutral.",
    "Applicability does not recover or broaden grammar.",
    "Applicability does not construct material under the grammar.",
    "Applicability does not establish candidate realization in every operational dimension.",
    "Applicability does not project capability reachability.",
    "Applicability does not select or warrant a realization.",
    "Applicability does not authorize, emit, or execute.",
    "Invocation-contract compatibility does not make representation grammar into invocation grammar.",
    "No tool, provider, toolkit, or registered-operation concept is required by this projection.",
    "The mechanism may apply the grammar; it does not own the grammar.",
    "One grammar may support several future realizations and one mechanism may participate in several grammar applications.",
)

class RepresentationGrammarApplicabilityError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _refs(xs): return tuple(sorted({x for x in xs if x}))

@dataclass(frozen=True)
class ApplicabilityDemandMaterial:
    material_class_identity: str
    source_representation: str
    required_target_representation: str
    required_structures: tuple[str,...]=()
    excluded_or_counterexample_structures: tuple[str,...]=()
    lexical_support_refs: tuple[str,...]=()
    required_lexical_refs: tuple[str,...]=()
    applicability_boundary_refs: tuple[str,...]=()
    fidelity_constraints: tuple[str,...]=()
    attribution_constraints: tuple[str,...]=()
    claim_treatment_constraints: tuple[str,...]=()
    known_loss_refs: tuple[str,...]=()
    provenance: tuple[str,...]=()
    unknowns: tuple[str,...]=()
    conflicts: tuple[str,...]=()
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d

@dataclass(frozen=True)
class RepresentationGrammarApplicabilityProjection:
    artifact_type: str; applicability_projection_id: str; recovery_projection_ref: str; recovered_grammar_ref: str; probe_request_ref: str; capability_demand_ref: str; mechanism_ref: str; invocation_contract_ref: str; source_representation: str; required_target_representation: str; material_class: str; applicability_state: str; applicability_reason: str; grammar_standing: str; material_compatibility: str; source_representation_compatibility: str; target_representation_compatibility: str; invocation_contract_compatibility: str; lexical_support_standing: str; applicability_boundary_standing: str; fidelity_standing: str; attribution_standing: str; claim_treatment_standing: str; known_limitations_or_loss: tuple[str,...]; supporting_references: tuple[str,...]; provenance: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False; applicability_convention: str=CONVENTION
    def __post_init__(self):
        if self.applicability_state not in STATES: raise RepresentationGrammarApplicabilityError("invalid applicability state")
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d


def project_representation_grammar_applicability(recovery_projection: RepresentationGrammarRecoveryProjection, recovered_grammar: RecoveredRepresentationGrammar, handoff, mechanism_ref: str, invocation_contract, demand_material: ApplicabilityDemandMaterial, *, applicability_state: str|None=None, applicability_reason: str="", supporting_references: tuple[str,...]=(), provenance: tuple[str,...]=(), unknowns: tuple[str,...]=(), conflicts: tuple[str,...]=()) -> RepresentationGrammarApplicabilityProjection:
    if recovered_grammar.grammar_id not in {g.grammar_id for g in recovery_projection.recovered_grammars}: raise RepresentationGrammarApplicabilityError("recovered grammar does not belong to recovery projection")
    if recovered_grammar.candidate_grammar_ref not in recovery_projection.recovered_candidate_refs: raise RepresentationGrammarApplicabilityError("grammar candidate was not recovered")
    if handoff.probe_request_id != demand_material.provenance[0] if demand_material.provenance else False: raise RepresentationGrammarApplicabilityError("probe identity mismatch")
    if invocation_contract.mechanism_id != mechanism_ref: raise RepresentationGrammarApplicabilityError("invocation contract mechanism mismatch")
    if handoff.required_input_representation != demand_material.source_representation: raise RepresentationGrammarApplicabilityError("handoff source representation mismatch")
    if handoff.requested_output_representation != demand_material.required_target_representation: raise RepresentationGrammarApplicabilityError("handoff target representation mismatch")

    grammar_standing="recovered" if not recovered_grammar.conflicts else "conflict"
    source="compatible" if recovered_grammar.representation_identity == demand_material.source_representation else "incompatible"
    target="compatible" if invocation_contract.produced_output_representation == demand_material.required_target_representation else "incompatible"
    contract="compatible" if invocation_contract.accepted_input_representation == recovered_grammar.representation_identity and invocation_contract.produced_output_representation == demand_material.required_target_representation else "incompatible"
    req=set(demand_material.required_structures); supported=set(recovered_grammar.supported_structures); excluded=set(recovered_grammar.excluded_structures)|set(demand_material.excluded_or_counterexample_structures)
    material="compatible" if req and req <= supported else ("incompatible" if req & excluded else "unknown")
    boundary="compatible" if set(demand_material.applicability_boundary_refs or (demand_material.material_class_identity,)) <= set(recovered_grammar.applicability_boundary) else ("incompatible" if req & excluded else "unknown")
    lex="sufficient" if set(demand_material.required_lexical_refs) <= set(demand_material.lexical_support_refs)|set(recovered_grammar.lexical_support_refs) else "unknown"
    fidelity="satisfied" if not demand_material.fidelity_constraints or not demand_material.known_loss_refs else "incompatible"
    attribution="satisfied" if not demand_material.attribution_constraints else "satisfied"
    claim="satisfied" if not demand_material.claim_treatment_constraints else "satisfied"
    all_unknowns=_refs((*recovery_projection.unknowns,*recovered_grammar.unknowns,*invocation_contract.unknowns,*demand_material.unknowns,*unknowns))
    all_conflicts=_refs((*recovery_projection.conflicts,*recovered_grammar.conflicts,*demand_material.conflicts,*conflicts))
    if all_conflicts: state="conflict"; reason="conflicting applicability evidence is preserved"
    elif "incompatible" in (source,target,contract,material,boundary,fidelity): state="not_applicable"; reason="bounded positive evidence establishes incompatibility"
    elif all_unknowns or "unknown" in (material,boundary,lex): state="unknown"; reason="missing bounded support prevents applicability conclusion"
    else: state="applicable"; reason="recovered grammar, exact demand, mechanism, and invocation contract are bounded-compatible"
    if applicability_state:
        state=applicability_state; reason=applicability_reason or reason
    payload={"recovery":recovery_projection.projection_id,"grammar":recovered_grammar.grammar_id,"probe":handoff.probe_request_id,"handoff":handoff.to_json_dict(),"demand":handoff.capability_identity,"mechanism":mechanism_ref,"contract":invocation_contract.to_json_dict(),"material":demand_material.to_json_dict(),"source":demand_material.source_representation,"target":demand_material.required_target_representation,"known_loss":sorted(demand_material.known_loss_refs),"unknowns":list(all_unknowns),"conflicts":list(all_conflicts),"state":state,"reason":reason,"convention":CONVENTION}
    pid=_stable("representation-grammar-applicability-projection", payload)
    prov=_refs((*provenance,*demand_material.provenance,*recovered_grammar.provenance,recovery_projection.projection_id,recovered_grammar.grammar_id,handoff.probe_request_id,invocation_contract.contract_id))
    return RepresentationGrammarApplicabilityProjection("RepresentationGrammarApplicabilityProjection",pid,recovery_projection.projection_id,recovered_grammar.grammar_id,handoff.probe_request_id,handoff.capability_identity,mechanism_ref,invocation_contract.contract_id,demand_material.source_representation,demand_material.required_target_representation,demand_material.material_class_identity,state,reason,grammar_standing,material,source,target,contract,lex,boundary,fidelity,attribution,claim,_refs((*recovered_grammar.known_limitations,*demand_material.known_loss_refs)),_refs((*supporting_references,*recovered_grammar.supporting_comparison_refs,*recovered_grammar.lexical_support_refs)),prov,all_unknowns,all_conflicts)


EXPLANATION_CONVENTION = "representation_grammar_applicability_advancement_explanation_v1"

@dataclass(frozen=True)
class RepresentationGrammarApplicabilityAdvancementExplanation:
    artifact_type: str
    explanation_id: str
    source_artifact_ref: str
    source_artifact_type: str
    producer: str
    attempted_movement: str
    examined_grammar: str
    examined_demand: str
    examined_mechanism: str
    examined_contract: str
    source_state: str
    source_reason: str
    established_applicability_evidence: tuple[str,...]
    next_handoff_boundary: str
    handoff_permitted: bool
    reconsideration_evidence: tuple[str,...]
    authority_treatment: str
    prohibited_downstream_movement: tuple[str,...]
    preserved_unknowns: tuple[str,...]
    preserved_conflicts: tuple[str,...]
    preserved_known_loss: tuple[str,...]
    preserved_provenance: tuple[str,...]
    explanation_boundary: str
    compatibility_boundary_changed: bool=False
    read_only: bool=True
    writes_event_ledger: bool=False
    mutates_cluster: bool=False
    explanation_convention: str=EXPLANATION_CONVENTION
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d

def _standing(label: str, value: str) -> str:
    return f"{label}={value}"

def explain_representation_grammar_applicability_advancement(p: RepresentationGrammarApplicabilityProjection) -> RepresentationGrammarApplicabilityAdvancementExplanation:
    attempted="advance one recovered representation grammar applicability result within the representation-grammar applicability boundary"
    established=(
        _standing("grammar_standing", p.grammar_standing),
        _standing("material_compatibility", p.material_compatibility),
        _standing("source_representation_compatibility", p.source_representation_compatibility),
        _standing("target_representation_compatibility", p.target_representation_compatibility),
        _standing("invocation_contract_compatibility", p.invocation_contract_compatibility),
        _standing("lexical_support_standing", p.lexical_support_standing),
        _standing("applicability_boundary_standing", p.applicability_boundary_standing),
        _standing("fidelity_standing", p.fidelity_standing),
        _standing("attribution_standing", p.attribution_standing),
        _standing("claim_treatment_standing", p.claim_treatment_standing),
    )
    prohibited=("select_or_warrant_realization", "authorize_emit_or_execute", "recover_or_broaden_grammar")
    reconsideration=("none; the source artifact remains within representation-grammar applicability",)
    boundary="grammar applicability boundary is satisfied; explanation emits no handoff"
    handoff_permitted=False
    if p.applicability_state=="not_applicable":
        bad=tuple(x for x in established if x.endswith("=incompatible")) or (p.applicability_reason,)
        boundary="bounded positive applicability evidence establishes incompatibility; representation-grammar applicability is not established"
        reconsideration=tuple(f"changed source-artifact evidence for {x.split('=')[0]}" for x in bad)
    elif p.applicability_state=="unknown":
        missing=tuple(x for x in established if x.endswith("=unknown")) or p.unknowns or (p.applicability_reason,)
        boundary="required bounded support is absent or unresolved; representation-grammar applicability is not established"
        reconsideration=tuple(f"bounded applicability evidence resolving {x.split('=')[0] if '=' in x else x}" for x in missing)
    elif p.applicability_state=="conflict":
        boundary="preserved applicability evidence supports incompatible conclusions; representation-grammar applicability is not established"
        reconsideration=("changed source-artifact evidence that removes the preserved applicability conflict without ordering, source count, preferred grammar, or mechanism availability",)
    payload={"source":p.applicability_projection_id,"state":p.applicability_state,"reason":p.applicability_reason,"evidence":established,"boundary":boundary,"reconsideration":reconsideration,"unknowns":p.unknowns,"conflicts":p.conflicts,"convention":EXPLANATION_CONVENTION}
    return RepresentationGrammarApplicabilityAdvancementExplanation(
        "RepresentationGrammarApplicabilityAdvancementExplanation",
        _stable("representation-grammar-applicability-advancement-explanation", payload),
        p.applicability_projection_id, p.artifact_type, "RepresentationGrammarApplicabilityProjection", attempted,
        p.recovered_grammar_ref, p.capability_demand_ref, p.mechanism_ref, p.invocation_contract_ref, p.applicability_state, p.applicability_reason,
        established, boundary, handoff_permitted, reconsideration,
        "additional operator authority is not a resolution for missing or incompatible applicability evidence",
        prohibited, p.unknowns, p.conflicts, p.known_limitations_or_loss, p.provenance,
        "Stage-local read-only explanation derived only from RepresentationGrammarApplicabilityProjection; it does not reclassify states, recover or broaden grammar, construct realization, request authority, write events, or mutate cluster state.")

def representation_grammar_applicability_advancement_explanation_json(e): return e.to_json_dict()

def format_representation_grammar_applicability_advancement_explanation(e: RepresentationGrammarApplicabilityAdvancementExplanation) -> str:
    lines=["Representation Grammar Applicability Advancement Explanation",f"explanation_id: {e.explanation_id}",f"source_artifact_ref: {e.source_artifact_ref}",f"producer: {e.producer}",f"attempted_movement: {e.attempted_movement}",f"examined_grammar: {e.examined_grammar}",f"examined_demand: {e.examined_demand}",f"examined_mechanism: {e.examined_mechanism}",f"examined_contract: {e.examined_contract}",f"source_state: {e.source_state}",f"source_reason: {e.source_reason}",f"next_handoff_boundary: {e.next_handoff_boundary}",f"handoff_permitted: {str(e.handoff_permitted).lower()}",f"authority_treatment: {e.authority_treatment}",f"compatibility_boundary_changed: {str(e.compatibility_boundary_changed).lower()}",f"read_only: {str(e.read_only).lower()}",f"writes_event_ledger: {str(e.writes_event_ledger).lower()}",f"mutates_cluster: {str(e.mutates_cluster).lower()}",f"explanation_boundary: {e.explanation_boundary}"]
    for label, vals in (("established_applicability_evidence",e.established_applicability_evidence),("reconsideration_evidence",e.reconsideration_evidence),("prohibited_downstream_movement",e.prohibited_downstream_movement),("preserved_unknowns",e.preserved_unknowns),("preserved_conflicts",e.preserved_conflicts),("preserved_known_loss",e.preserved_known_loss),("preserved_provenance",e.preserved_provenance)):
        lines.append(label+":"); lines += [f"- {x}" for x in vals] or ["- none"]
    return "\n".join(lines)

def representation_grammar_applicability_json(p): return p.to_json_dict()

def format_representation_grammar_applicability(p: RepresentationGrammarApplicabilityProjection) -> str:
    lines=["Representation Grammar Applicability Projection",f"applicability_projection_id: {p.applicability_projection_id}",f"recovered_grammar_ref: {p.recovered_grammar_ref}",f"demand: {p.capability_demand_ref}",f"mechanism: {p.mechanism_ref}",f"invocation_contract: {p.invocation_contract_ref}",f"state: {p.applicability_state}",f"reason: {p.applicability_reason}",f"source_representation: {p.source_representation}",f"required_target_representation: {p.required_target_representation}",f"lexical_support: {p.lexical_support_standing}",f"boundary: {p.applicability_boundary_standing}",f"read_only: {str(p.read_only).lower()}",f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",f"mutates_cluster: {str(p.mutates_cluster).lower()}","unknowns:"]
    lines += [f"- {x}" for x in p.unknowns] or ["- none"]
    lines += ["conflicts:"] + ([f"- {x}" for x in p.conflicts] or ["- none"])
    lines += ["boundary_notes:"] + [f"- {x}" for x in p.boundary_notes]
    return "\n".join(lines)
