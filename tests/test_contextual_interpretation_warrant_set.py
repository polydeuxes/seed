import pytest

from seed_runtime.contextual_interpretation_warrant_set import (
    ClarificationEvidence,
    ContextualInterpretationWarrantSetError,
    CorrectionCandidate,
    ExactOperatorMaterial,
    InterpretationCandidate,
    RetrospectiveEvidence,
    SourceSpan,
    produce_contextual_interpretation_warrant_set,
)


def material():
    return ExactOperatorMaterial(
        material_ref="operator-material:1",
        exact_text="fix teh cache; maybe inspect yesterday's note",
        source_spans=(
            SourceSpan("span:fix", "operator:turn", 0, 11, "fix teh cache"),
            SourceSpan("span:retro", "operator:turn", 19, 43, "inspect yesterday's note"),
        ),
        provenance=("exact-operator-material",),
    )


def candidates():
    return (
        InterpretationCandidate("cand:repair", "repair cache typo", ("span:fix",), "operator asks to fix the cache"),
        InterpretationCandidate("cand:inspect", "inspect cache note", ("span:retro",), "operator asks for read-only inspection"),
    )


def test_candidate_local_evidence_and_corrections_are_preserved_without_selection():
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=candidates(),
        corrections=(CorrectionCandidate("corr:teh", "cand:repair", ("span:fix",), "teh", "the", ("typo-evidence",)),),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:repair-support", "cand:repair", "supporting", "retro:1", "cache was broken"),
            RetrospectiveEvidence("ev:inspect-support", "cand:inspect", "supporting", "retro:2", "note mentions inspection"),
        ),
        closed_choice_selection_binding_ref="closed-choice-selection-binding:abc",
    )

    repair, inspect = warrant_set.candidate_warrants
    assert repair.candidate_ref == "cand:repair"
    assert repair.proposed_corrections[0].original_text == "teh"
    assert repair.proposed_corrections[0].corrected_text == "the"
    assert [e.evidence_ref for e in repair.supporting_evidence] == ["ev:repair-support"]
    assert [e.evidence_ref for e in inspect.supporting_evidence] == ["ev:inspect-support"]
    assert warrant_set.closed_choice_selection_binding_ref == "closed-choice-selection-binding:abc"
    assert warrant_set.selected_candidate_ref is None
    assert warrant_set.interpretation_selected is False
    assert warrant_set.goal_bound is False
    assert warrant_set.inquiry_moved is False
    assert warrant_set.authorized is False
    assert warrant_set.executed is False
    assert warrant_set.read_only and not warrant_set.writes_event_ledger and not warrant_set.mutates_state


def test_retrospective_dispositions_do_not_turn_examined_material_into_support():
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=(candidates()[0],),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:s", "cand:repair", "supporting", "retro:s", "supports repair"),
            RetrospectiveEvidence("ev:c", "cand:repair", "contradicting", "retro:c", "says do not repair"),
            RetrospectiveEvidence("ev:i", "cand:repair", "irrelevant", "retro:i", "unrelated cache label"),
            RetrospectiveEvidence("ev:u", "cand:repair", "unresolved", "retro:u", "ambiguous timestamp"),
        ),
    )

    warrant = warrant_set.candidate_warrants[0]
    assert [e.evidence_ref for e in warrant.examined_retrospective_material] == ["ev:s", "ev:c", "ev:i", "ev:u"]
    assert [e.evidence_ref for e in warrant.supporting_evidence] == ["ev:s"]
    assert [e.evidence_ref for e in warrant.contradicting_evidence] == ["ev:c"]
    assert [e.evidence_ref for e in warrant.irrelevant_evidence] == ["ev:i"]
    assert [e.evidence_ref for e in warrant.unresolved_evidence] == ["ev:u"]
    assert warrant.warrant_standing == "unresolved"


def test_cross_candidate_leakage_is_refused_for_unknown_candidate_refs():
    with pytest.raises(ContextualInterpretationWarrantSetError):
        produce_contextual_interpretation_warrant_set(
            operator_material=material(),
            candidates=(candidates()[0],),
            retrospective_evidence=(RetrospectiveEvidence("ev:foreign", "cand:inspect", "supporting", "retro:x", "foreign support"),),
        )


def test_unresolved_ambiguity_clarification_residual_source_and_known_loss_are_preserved():
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=(candidates()[0],),
        clarification_evidence=(ClarificationEvidence("clar:1", "cand:repair", "operator might mean inspect only"),),
        unknowns_by_candidate={"cand:repair": ("whether fix is imperative or example",)},
        known_loss_by_candidate={"cand:repair": ("tone cannot be recovered from transcript",)},
    )

    warrant = warrant_set.candidate_warrants[0]
    assert warrant.warrant_standing == "unresolved"
    assert warrant.clarification_evidence[0].clarification_ref == "clar:1"
    assert warrant.unknowns == ("whether fix is imperative or example",)
    assert warrant.known_loss == ("tone cannot be recovered from transcript",)
    assert [span.span_ref for span in warrant.residual_source_material] == ["span:retro"]


def test_multiple_warranted_candidates_are_not_selected():
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=candidates(),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:repair", "cand:repair", "supporting", "retro:1", "supports repair"),
            RetrospectiveEvidence("ev:inspect", "cand:inspect", "supporting", "retro:2", "supports inspect"),
        ),
    )

    assert [w.warrant_standing for w in warrant_set.candidate_warrants] == ["warranted", "warranted"]
    assert warrant_set.selected_candidate_ref is None
    assert warrant_set.interpretation_selected is False
    assert "unique warranted candidate is not a selected candidate" in " ".join(warrant_set.boundary_notes).lower()
