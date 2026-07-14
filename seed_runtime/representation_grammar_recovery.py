"""Bounded, mechanism-neutral representation grammar recovery."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib, json
from typing import Any

from seed_runtime.candidate_external_grammar import CandidateExternalGrammarSet

CONVENTION = "representation_grammar_recovery_v1"
STANDINGS = ("recovered", "unsupported", "unknown", "conflict")
COMPARISON_RESULTS = ("supports", "contradicts", "unknown", "conflict")
BOUNDARY_NOTES = (
    "Candidate grammars are hypotheses; they do not become recovered grammar merely by being proposed.",
    "Attributed source claims contribute material; they do not establish recovery by themselves.",
    "Recovered representation grammar governs material; it does not govern mechanism invocation.",
    "Recovered grammar is bounded by its explicit applicability boundary.",
    "Lexical support is referenced separately from grammar structure.",
    "Excluded structures are outside the recovered boundary and are not automatically contradicted.",
    "Recovered grammar does not establish global language competency.",
    "This artifact does not bind a mechanism, an invocation contract, or an operational realization.",
    "This artifact does not project capability reachability.",
)

class RepresentationGrammarRecoveryError(ValueError): pass

def _stable(prefix: str, payload: Any) -> str:
    return prefix + ":" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _sorted_unique(xs): return tuple(sorted({x for x in xs if x}))

def _listify(d, keys):
    for k in keys: d[k] = list(d[k])
    return d

@dataclass(frozen=True)
class RepresentationGrammarSourceMaterialRef:
    material_id: str; source_id: str=""; artifact_id: str=""; artifact_hash: str=""; version: str=""; exact_text_ref: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def to_json_dict(self): return _listify(asdict(self), ("provenance","unknowns"))

@dataclass(frozen=True)
class AttributedGrammarClaim:
    claim_id: str; source_identity: str; source_artifact_identity: str; claim_reference: str; candidate_grammar_ref: str; exact_claim: str=""; attribution: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=(); contradictions: tuple[str,...]=()
    def to_json_dict(self): return _listify(asdict(self), ("provenance","unknowns","contradictions"))

@dataclass(frozen=True)
class RepresentationGrammarComparison:
    comparison_id: str; candidate_grammar_ref: str; exact_material_ref: str; expected_structure_ref: str; observed_structure_ref: str; compared_dimensions: tuple[str,...]; result: str; reason: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=()
    def __post_init__(self):
        if self.result not in COMPARISON_RESULTS: raise RepresentationGrammarRecoveryError("invalid comparison result")
    def to_json_dict(self): return _listify(asdict(self), ("compared_dimensions","provenance","unknowns"))

@dataclass(frozen=True)
class LexicalSupportReference:
    lexical_ref_id: str; lexical_source_identity: str; term_or_relation_identity: str; candidate_grammar_ref: str; supported_role_or_distinction: str; material_span_ref: str=""; provenance: tuple[str,...]=(); unknowns: tuple[str,...]=(); conflicts: tuple[str,...]=()
    def to_json_dict(self): return _listify(asdict(self), ("provenance","unknowns","conflicts"))

@dataclass(frozen=True)
class CandidateRecoveryMaterial:
    candidate_grammar_ref: str
    representation_identity: str
    bounded_fragment: str
    convention_or_dialect: str=""
    source_material_refs: tuple[str,...]=()
    supporting_claim_refs: tuple[str,...]=()
    contradicting_claim_refs: tuple[str,...]=()
    supporting_comparison_refs: tuple[str,...]=()
    contradicting_comparison_refs: tuple[str,...]=()
    lexical_support_refs: tuple[str,...]=()
    required_lexical_roles: tuple[str,...]=()
    supported_structures: tuple[str,...]=()
    excluded_structures: tuple[str,...]=()
    applicability_boundary: tuple[str,...]=()
    known_limitations: tuple[str,...]=()
    provenance: tuple[str,...]=()
    unknowns: tuple[str,...]=()
    conflicts: tuple[str,...]=()
    refinement_reason: str=""
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d

@dataclass(frozen=True)
class RecoveredRepresentationGrammar:
    grammar_id: str; candidate_grammar_ref: str; representation_identity: str; bounded_fragment: str; convention_or_dialect: str; source_material_refs: tuple[str,...]; supporting_claim_refs: tuple[str,...]; supporting_comparison_refs: tuple[str,...]; contradicting_refs: tuple[str,...]; supported_structures: tuple[str,...]; excluded_structures: tuple[str,...]; applicability_boundary: tuple[str,...]; lexical_support_refs: tuple[str,...]; known_limitations: tuple[str,...]; provenance: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; refinement_reason: str=""; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d

@dataclass(frozen=True)
class RepresentationGrammarCandidateOutcome:
    candidate_grammar_ref: str; standing: str; reason: str; recovered_grammar_ref: str=""; source_material_refs: tuple[str,...]=(); supporting_claim_refs: tuple[str,...]=(); contradicting_claim_refs: tuple[str,...]=(); supporting_comparison_refs: tuple[str,...]=(); contradicting_comparison_refs: tuple[str,...]=(); lexical_support_refs: tuple[str,...]=(); applicability_boundary: tuple[str,...]=(); supported_structures: tuple[str,...]=(); excluded_structures: tuple[str,...]=(); unknowns: tuple[str,...]=(); conflicts: tuple[str,...]=(); unresolved_alternatives: tuple[str,...]=()
    def __post_init__(self):
        if self.standing not in STANDINGS: raise RepresentationGrammarRecoveryError("invalid recovery standing")
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d

@dataclass(frozen=True)
class FutureRepresentationGrammarBindingHandoff:
    recovery_projection_id: str; recovered_grammar_refs: tuple[str,...]; candidate_source_refs: tuple[str,...]; representation_identities: tuple[str,...]; applicability_boundaries: tuple[str,...]; lexical_support_refs: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False
    def to_json_dict(self):
        d=asdict(self)
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d

@dataclass(frozen=True)
class RepresentationGrammarRecoveryProjection:
    artifact_type: str; projection_id: str; candidate_set_ref: str; source_material_refs: tuple[str,...]; recovered_grammars: tuple[RecoveredRepresentationGrammar,...]; candidate_outcomes: tuple[RepresentationGrammarCandidateOutcome,...]; recovered_candidate_refs: tuple[str,...]; unsupported_candidate_refs: tuple[str,...]; unknown_candidate_refs: tuple[str,...]; conflicting_candidate_refs: tuple[str,...]; unresolved_alternatives: tuple[str,...]; shared_lexical_support_refs: tuple[str,...]; provenance: tuple[str,...]; unknowns: tuple[str,...]; conflicts: tuple[str,...]; boundary_notes: tuple[str,...]=BOUNDARY_NOTES; read_only: bool=True; writes_event_ledger: bool=False; mutates_cluster: bool=False; projection_convention: str=CONVENTION
    def to_json_dict(self):
        d=asdict(self); d["recovered_grammars"]=[g.to_json_dict() for g in self.recovered_grammars]; d["candidate_outcomes"]=[o.to_json_dict() for o in self.candidate_outcomes]
        for k,v in d.items():
            if isinstance(v, tuple): d[k]=list(v)
        return d
    def to_future_representation_grammar_binding_handoff(self):
        return FutureRepresentationGrammarBindingHandoff(self.projection_id, tuple(g.grammar_id for g in self.recovered_grammars), self.source_material_refs, tuple(sorted({g.representation_identity for g in self.recovered_grammars})), tuple(sorted({b for g in self.recovered_grammars for b in g.applicability_boundary})), self.shared_lexical_support_refs, self.unknowns, self.conflicts)


def recover_representation_grammars(candidate_set: CandidateExternalGrammarSet, *, source_materials: tuple[RepresentationGrammarSourceMaterialRef,...]=(), attributed_claims: tuple[AttributedGrammarClaim,...]=(), comparisons: tuple[RepresentationGrammarComparison,...]=(), lexical_support: tuple[LexicalSupportReference,...]=(), recovery_material: tuple[CandidateRecoveryMaterial,...]=(), shared_provenance: tuple[str,...]=(), set_unknowns: tuple[str,...]=()) -> RepresentationGrammarRecoveryProjection:
    material_by = {m.material_id:m for m in source_materials}
    claims_by = {c.claim_id:c for c in attributed_claims}
    comps_by = {c.comparison_id:c for c in comparisons}
    lex_by = {l.lexical_ref_id:l for l in lexical_support}
    mats = {m.candidate_grammar_ref:m for m in recovery_material}
    recovered=[]; outcomes=[]
    for cand in sorted(candidate_set.candidates, key=lambda c:c.candidate_id):
        m = mats.get(cand.candidate_id) or CandidateRecoveryMaterial(cand.candidate_id, candidate_set.representation_scope, cand.structural_claim, source_material_refs=(), supporting_claim_refs=cand.supporting_testimony, contradicting_claim_refs=cand.contradicting_testimony, unknowns=cand.explicit_unknowns)
        sup = tuple(c for c in (comps_by.get(r) for r in m.supporting_comparison_refs) if c and c.result=="supports")
        con = tuple(c for c in (comps_by.get(r) for r in m.contradicting_comparison_refs) if c and c.result=="contradicts")
        conflict_refs = _sorted_unique((*m.conflicts, *(c.comparison_id for c in comparisons if c.candidate_grammar_ref==cand.candidate_id and c.result=="conflict")))
        lex_unknown = bool(m.required_lexical_roles) and not all(any(l.candidate_grammar_ref==cand.candidate_id and role in l.supported_role_or_distinction for l in lexical_support) for role in m.required_lexical_roles)
        if conflict_refs or (sup and con and set(m.supporting_comparison_refs) & set(m.contradicting_comparison_refs)):
            standing="conflict"; reason="bounded material supports incompatible grammar conclusions"
        elif con and not sup:
            standing="unsupported"; reason="bounded positive counterevidence contradicts the candidate grammar"
        elif sup and not con and m.applicability_boundary and m.supported_structures and not lex_unknown:
            standing="recovered"; reason="bounded positive comparison support and applicability boundary warrant recovery"
        else:
            standing="unknown"; reason="insufficient bounded support to recover or reject the candidate grammar"
        gid=""
        if standing=="recovered":
            payload={"candidate":cand.to_json_dict(),"representation":m.representation_identity,"fragment":m.bounded_fragment,"dialect":m.convention_or_dialect,"materials":[material_by[r].to_json_dict() if r in material_by else r for r in sorted(m.source_material_refs)],"supporting_comparisons":[comps_by[r].to_json_dict() if r in comps_by else r for r in sorted(m.supporting_comparison_refs)],"contradictions":[comps_by[r].to_json_dict() if r in comps_by else r for r in sorted(m.contradicting_comparison_refs)],"supported":sorted(m.supported_structures),"excluded":sorted(m.excluded_structures),"boundary":sorted(m.applicability_boundary),"lexical":[lex_by[r].to_json_dict() if r in lex_by else r for r in sorted(m.lexical_support_refs)],"unknowns":sorted((*m.unknowns,*cand.explicit_unknowns)),"conflicts":list(conflict_refs),"convention":CONVENTION}
            gid=_stable("recovered-representation-grammar", payload)
            recovered.append(RecoveredRepresentationGrammar(gid,cand.candidate_id,m.representation_identity,m.bounded_fragment,m.convention_or_dialect,_sorted_unique(m.source_material_refs),_sorted_unique(m.supporting_claim_refs),_sorted_unique(m.supporting_comparison_refs),_sorted_unique((*m.contradicting_claim_refs,*m.contradicting_comparison_refs)),tuple(sorted(m.supported_structures)),tuple(sorted(m.excluded_structures)),tuple(sorted(m.applicability_boundary)),_sorted_unique(m.lexical_support_refs),tuple(sorted(m.known_limitations)),_sorted_unique((*m.provenance,*cand.provenance)),_sorted_unique((*m.unknowns,*cand.explicit_unknowns)),conflict_refs,m.refinement_reason))
        outcomes.append(RepresentationGrammarCandidateOutcome(cand.candidate_id,standing,reason,gid,_sorted_unique(m.source_material_refs),_sorted_unique(m.supporting_claim_refs),_sorted_unique(m.contradicting_claim_refs),_sorted_unique(m.supporting_comparison_refs),_sorted_unique(m.contradicting_comparison_refs),_sorted_unique(m.lexical_support_refs),tuple(sorted(m.applicability_boundary)),tuple(sorted(m.supported_structures)),tuple(sorted(m.excluded_structures)),_sorted_unique((*m.unknowns,*cand.explicit_unknowns,*( ("required lexical support missing",) if lex_unknown else () ))),conflict_refs,_sorted_unique(cand.unresolved_alternatives)))
    recovered=tuple(sorted(recovered,key=lambda g:g.grammar_id)); outcomes=tuple(sorted(outcomes,key=lambda o:o.candidate_grammar_ref))
    zero = ("no candidate representation grammar",) if not candidate_set.candidates else ()
    pid=_stable("representation-grammar-recovery-projection", {"candidate_set":candidate_set.to_json_dict(),"materials":[m.to_json_dict() for m in sorted(source_materials,key=lambda x:x.material_id)],"claims":[c.to_json_dict() for c in sorted(attributed_claims,key=lambda x:x.claim_id)],"comparisons":[c.to_json_dict() for c in sorted(comparisons,key=lambda x:x.comparison_id)],"lexical":[l.to_json_dict() for l in sorted(lexical_support,key=lambda x:x.lexical_ref_id)],"outcomes":[o.to_json_dict() for o in outcomes],"grammars":[g.to_json_dict() for g in recovered],"convention":CONVENTION})
    return RepresentationGrammarRecoveryProjection("RepresentationGrammarRecoveryProjection",pid,_stable("candidate-external-grammar-set", candidate_set.to_json_dict()),_sorted_unique(m.material_id for m in source_materials),recovered,outcomes,tuple(o.candidate_grammar_ref for o in outcomes if o.standing=="recovered"),tuple(o.candidate_grammar_ref for o in outcomes if o.standing=="unsupported"),tuple(o.candidate_grammar_ref for o in outcomes if o.standing=="unknown"),tuple(o.candidate_grammar_ref for o in outcomes if o.standing=="conflict"),_sorted_unique(x for c in candidate_set.candidates for x in c.unresolved_alternatives),_sorted_unique(l.lexical_ref_id for l in lexical_support),_sorted_unique(shared_provenance),_sorted_unique((*set_unknowns,*candidate_set.set_unknowns,*zero)),_sorted_unique(x for o in outcomes for x in o.conflicts))

def representation_grammar_recovery_json(p): return p.to_json_dict()

def format_representation_grammar_recovery(p: RepresentationGrammarRecoveryProjection) -> str:
    lines=["Representation Grammar Recovery Projection",f"projection_id: {p.projection_id}",f"read_only: {str(p.read_only).lower()}",f"writes_event_ledger: {str(p.writes_event_ledger).lower()}",f"mutates_cluster: {str(p.mutates_cluster).lower()}","recovered:"]
    lines += [f"- {g.grammar_id}: candidate={g.candidate_grammar_ref}; fragment={g.bounded_fragment}; representation={g.representation_identity}; boundary={', '.join(g.applicability_boundary) or 'none'}; lexical_refs={', '.join(g.lexical_support_refs) or 'none'}" for g in p.recovered_grammars] or ["- none"]
    for label, refs in (("unsupported",p.unsupported_candidate_refs),("unknown",p.unknown_candidate_refs),("conflict",p.conflicting_candidate_refs),("alternatives",p.unresolved_alternatives),("lexical_support",p.shared_lexical_support_refs),("boundary_notes",p.boundary_notes)):
        lines.append(label+":"); lines += [f"- {x}" for x in refs] or ["- none"]
    lines.append("outcomes:"); lines += [f"- {o.candidate_grammar_ref}: {o.standing}; {o.reason}" for o in p.candidate_outcomes] or ["- none"]
    return "\n".join(lines)
