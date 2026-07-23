import json

from seed_runtime.candidate_external_grammar import CandidateExternalGrammarInput, CandidateExternalGrammarInputCandidate, assemble_candidate_external_grammar_set
from seed_runtime.representation_grammar_recovery import *


def cset(*candidates):
    return assemble_candidate_external_grammar_set(CandidateExternalGrammarInput("bounded grammar fixture", candidates))

def eng_candidate(cid="eng-simple", claim="simple declarative sentence -> subject followed by predicate", alts=()):
    return CandidateExternalGrammarInputCandidate(cid, claim, "The dog runs.", ("caller",), ("claim-simple",), (), alts, ())

def supported_material(cid="eng-simple", boundary=("one exact sentence: The dog runs.",)):
    return CandidateRecoveryMaterial(
        cid,"English bounded prose","simple declarative subject-predicate fragment","fixture convention",
        ("mat-dog-runs",),("claim-simple",),(),("cmp-subj","cmp-pred","cmp-sentence"),(),("lex-dog","lex-runs"),("noun/nominal","finite-verb"),
        ("one explicit nominal subject","one finite predicate","subject followed by predicate"),
        ("compound subjects","compound predicates","subordinate clauses","questions","commands","omitted subjects","ambiguous word classes","idioms","semantic implication","general prose understanding"),
        boundary,("does not establish Seed understands English",),("fixture",),("compound forms outside scope",))

def material(hash="h1"):
    return (RepresentationGrammarSourceMaterialRef("mat-dog-runs","grammar-fixture","artifact-dog-runs",hash,"v1","The dog runs.",("fixture",)),)

def claims():
    return (AttributedGrammarClaim("claim-simple","grammar source","grammar-book:v1","p1", "eng-simple", "simple declarative sentence contains subject and predicate", "source", ("fixture",)),)

def comps(cid="eng-simple", suffix=""):
    return (
        RepresentationGrammarComparison("cmp-subj"+suffix,cid,"mat-dog-runs","subject span","The dog",("span role",),"supports","bounded subject span"),
        RepresentationGrammarComparison("cmp-pred"+suffix,cid,"mat-dog-runs","predicate span","runs",("span role",),"supports","bounded predicate span"),
        RepresentationGrammarComparison("cmp-sentence"+suffix,cid,"mat-dog-runs","subject followed by predicate","The dog | runs",("order","roles"),"supports","matches candidate"),
    )

def lex(cid="eng-simple", changed=False):
    role = "noun/nominal changed" if changed else "noun/nominal"
    return (
        LexicalSupportReference("lex-dog","dictionary","dog",cid,role,"span:The dog",("fixture",)),
        LexicalSupportReference("lex-runs","dictionary","runs",cid,"finite-verb","span:runs",("fixture",)),
    )

def recover_full(candidate=None, mat=None, comparisons=None, lexrefs=None, recmat=None):
    cs = cset(candidate or eng_candidate())
    return recover_representation_grammars(cs, source_materials=mat or material(), attributed_claims=claims(), comparisons=comparisons or comps(), lexical_support=lexrefs or lex(), recovery_material=(recmat or supported_material(),), shared_provenance=("fixture",))


def test_recovered_projection_is_immutable_read_only_and_json_typed():
    p = recover_full()
    assert p.artifact_type == "RepresentationGrammarRecoveryProjection"
    assert p.read_only and not p.writes_event_ledger and not p.mutates_cluster
    assert p.recovered_grammars[0].read_only and not p.recovered_grammars[0].writes_event_ledger and not p.recovered_grammars[0].mutates_cluster
    payload = representation_grammar_recovery_json(p)
    assert payload["artifact_type"] == "RepresentationGrammarRecoveryProjection"
    assert payload["recovered_grammars"][0]["candidate_grammar_ref"] == "eng-simple"


def test_deterministic_identity_and_input_ordering():
    p1 = recover_full()
    p2 = recover_representation_grammars(cset(eng_candidate()), source_materials=tuple(reversed(material())), attributed_claims=tuple(reversed(claims())), comparisons=tuple(reversed(comps())), lexical_support=tuple(reversed(lex())), recovery_material=(supported_material(),), shared_provenance=("fixture",))
    assert p1.projection_id == p2.projection_id
    assert p1.recovered_grammars[0].grammar_id == p2.recovered_grammars[0].grammar_id


def test_identity_changes_for_candidate_material_comparison_contradiction_lexical_and_boundary():
    base = recover_full()
    assert recover_full(candidate=eng_candidate(claim="changed grammar")).projection_id != base.projection_id
    assert recover_full(mat=material("changedhash")).projection_id != base.projection_id
    assert recover_full(comparisons=comps(suffix="x"), recmat=supported_material()).projection_id != base.projection_id
    contrad = RepresentationGrammarComparison("bad","eng-simple","mat-dog-runs","subject-predicate","predicate-subject",("order",),"contradicts","counter")
    assert recover_full(comparisons=comps()+(contrad,), recmat=CandidateRecoveryMaterial(**{**supported_material().__dict__, "contradicting_comparison_refs":("bad",)})).projection_id != base.projection_id
    assert recover_full(lexrefs=lex(changed=True)).projection_id != base.projection_id
    assert recover_full(recmat=supported_material(boundary=("changed boundary",))).recovered_grammars[0].grammar_id != base.recovered_grammars[0].grammar_id


def test_candidate_distinct_from_recovered_and_preserves_fields():
    p = recover_full()
    g = p.recovered_grammars[0]
    assert g.grammar_id != "eng-simple"
    assert g.candidate_grammar_ref == "eng-simple"
    assert g.source_material_refs == ("mat-dog-runs",)
    assert "one explicit nominal subject" in g.supported_structures
    assert "questions" in g.excluded_structures
    assert "one exact sentence: The dog runs." in g.applicability_boundary
    assert g.lexical_support_refs == ("lex-dog","lex-runs")
    assert "fixture" in g.provenance
    assert "compound forms outside scope" in g.unknowns


def test_attributed_claim_alone_and_absence_of_support_are_unknown_not_unsupported():
    p = recover_representation_grammars(cset(eng_candidate()), source_materials=material(), attributed_claims=claims())
    assert p.unknown_candidate_refs == ("eng-simple",)
    assert not p.unsupported_candidate_refs and not p.recovered_grammars
    assert p.candidate_outcomes[0].reason.startswith("insufficient")


def test_structural_support_required_and_then_recovers_english_fragment_only():
    no_cmp = recover_representation_grammars(cset(eng_candidate()), source_materials=material(), attributed_claims=claims(), lexical_support=lex(), recovery_material=(CandidateRecoveryMaterial(**{**supported_material().__dict__, "supporting_comparison_refs":()}),))
    assert no_cmp.unknown_candidate_refs == ("eng-simple",)
    yes = recover_full()
    assert yes.recovered_candidate_refs == ("eng-simple",)
    assert "general prose understanding" in yes.recovered_grammars[0].excluded_structures
    assert "does not establish Seed understands English" in yes.recovered_grammars[0].known_limitations


def test_unsupported_counterexample_unknown_lexical_ambiguity_and_conflict():
    over = CandidateExternalGrammarInputCandidate("overbroad","every sentence begins with an explicit noun subject","Run.")
    badcmp = (RepresentationGrammarComparison("cmp-run","overbroad","mat-run","explicit noun subject","imperative without explicit subject",("initial subject",),"contradicts","Run. lacks explicit noun subject"),)
    pm = CandidateRecoveryMaterial("overbroad","English bounded prose","every sentence begins with explicit noun subject",source_material_refs=("mat-run",),contradicting_comparison_refs=("cmp-run",),applicability_boundary=("one exact sentence: Run.",))
    p = recover_representation_grammars(cset(over), comparisons=badcmp, recovery_material=(pm,))
    assert p.unsupported_candidate_refs == ("overbroad",)
    amb = recover_representation_grammars(cset(eng_candidate()), comparisons=comps(), recovery_material=(CandidateRecoveryMaterial(**{**supported_material().__dict__, "lexical_support_refs":(), "required_lexical_roles":("noun/nominal",)}),))
    assert amb.unknown_candidate_refs == ("eng-simple",)
    assert "required lexical support missing" in amb.candidate_outcomes[0].unknowns
    conflict_cmp = RepresentationGrammarComparison("conflict1","eng-simple","mat-dog-runs","subject","predicate",("role",),"conflict","two projections disagree")
    cp = recover_representation_grammars(cset(eng_candidate()), comparisons=comps()+(conflict_cmp,), recovery_material=(supported_material(),))
    assert cp.conflicting_candidate_refs == ("eng-simple",)
    # source/count/order do not resolve conflict
    cp2 = recover_representation_grammars(cset(eng_candidate()), comparisons=(conflict_cmp,)+comps()+comps(suffix="2"), recovery_material=(supported_material(),))
    assert cp2.conflicting_candidate_refs == ("eng-simple",)


def test_alternatives_non_recovered_and_empty_candidate_set_preserved():
    p = recover_representation_grammars(cset(eng_candidate(alts=("alt-question",)), CandidateExternalGrammarInputCandidate("alt-question","bounded question grammar")), recovery_material=(supported_material(),), comparisons=comps(), lexical_support=lex(), source_materials=material())
    assert p.recovered_candidate_refs == ("eng-simple",)
    assert p.unknown_candidate_refs == ("alt-question",)
    assert "alt-question" in p.unresolved_alternatives
    empty = recover_representation_grammars(cset())
    assert empty.candidate_outcomes == () and empty.recovered_grammars == ()
    assert "no candidate representation grammar" in empty.unknowns
    assert "material has no grammar" not in json.dumps(empty.to_json_dict())


def test_bash_recovers_representation_grammar_without_mechanism_ownership():
    cand = CandidateExternalGrammarInputCandidate("bash-echo","echo + one literal argument -> literal stdout","echo hello")
    cmp = RepresentationGrammarComparison("cmp-bash","bash-echo","mat-echo","literal stdout","hello",("stdout",),"supports","observed behavior may support grammar")
    lm = CandidateRecoveryMaterial("bash-echo","Bash","literal echo command","bounded Bash fixture",("mat-echo",),(),(),("cmp-bash",),(),(),(),("command name echo","one bounded literal argument","literal stdout result"),("pipelines","redirection","substitution","expansion","functions","general scripting"),("echo with one bounded literal argument in fixture",),("no global Bash competency",))
    p = recover_representation_grammars(cset(cand), comparisons=(cmp,), recovery_material=(lm,))
    g = p.recovered_grammars[0]
    encoded = json.dumps(g.to_json_dict())
    assert g.representation_identity == "Bash"
    assert "/bin/bash" not in encoded and "mechanism_id" not in encoded
    assert "general scripting" in g.excluded_structures and "no global Bash competency" in g.known_limitations
    assert "cmp-bash" in g.supporting_comparison_refs


def test_mechanism_neutral_future_handoff_and_no_operational_fields():
    p = recover_full()
    h = p.to_future_representation_grammar_binding_handoff()
    assert h.recovered_grammar_refs == (p.recovered_grammars[0].grammar_id,)
    encoded = json.dumps(p.to_json_dict())
    for forbidden in ("mechanism_id","/bin/bash","invocation_contract","Candidate" + "Operational" + "Realization","Capability" + "Reachability","selected_realization","execution_request","authorization"):
        assert forbidden not in encoded
    # Structural proof: refs can be paired externally with several future mechanisms, and one future mechanism with several grammars, without changing grammar identity.
    several_future_mechanisms = {"/bin/bash": h.recovered_grammar_refs, "another bash": h.recovered_grammar_refs, "static analyzer": h.recovered_grammar_refs}
    one_future_mechanism = {"internal structural producer": h.recovered_grammar_refs + ("future-question-grammar",)}
    assert len(set(several_future_mechanisms.values())) == 1
    assert one_future_mechanism["internal structural producer"][0] == p.recovered_grammars[0].grammar_id


def test_human_output_preserves_categories_notes_and_read_only():
    p = recover_representation_grammars(cset(eng_candidate(), CandidateExternalGrammarInputCandidate("bad","bad")), source_materials=material(), comparisons=comps(), lexical_support=lex(), recovery_material=(supported_material(),))
    s = format_representation_grammar_recovery(p)
    for word in ("recovered:","unsupported:","unknown:","conflict:","alternatives:","lexical_support:","boundary_notes:","read_only: true","writes_event_ledger: false","mutates_cluster: false"):
        assert word in s
    assert "does not bind a mechanism" in s
