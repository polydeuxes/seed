from seed_runtime.contextual_interpretation_selection import (
    CandidateSelectionEvidence,
    select_contextual_interpretation,
)
from seed_runtime.contextual_interpretation_warrant_set import (
    CorrectionCandidate,
    ExactOperatorMaterial,
    InterpretationCandidate,
    RetrospectiveEvidence,
    SourceSpan,
    produce_contextual_interpretation_warrant_set,
)


def material():
    return ExactOperatorMaterial(
        material_ref="operator-material:selection",
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


def warranted_set():
    return produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=candidates(),
        corrections=(CorrectionCandidate("corr:teh", "cand:repair", ("span:fix",), "teh", "the", ("typo-evidence",)),),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:repair", "cand:repair", "supporting", "retro:1", "supports repair"),
            RetrospectiveEvidence("ev:inspect", "cand:inspect", "supporting", "retro:2", "supports inspect"),
        ),
        unknowns_by_candidate={"cand:inspect": ("which note is yesterday's note",)},
        conflicts_by_candidate={"cand:inspect": ("operator also mentioned maybe",)},
    )


def selection_evidence(candidate_ref="cand:repair", evidence_ref="sel:repair"):
    return CandidateSelectionEvidence(
        evidence_ref,
        candidate_ref,
        "exact_operator_clarification",
        "I mean the repair-cache interpretation.",
        ("operator-clarification:exact",),
    )


def test_exact_operator_clarification_selects_one_warranted_candidate_and_preserves_source():
    warrant_set = warranted_set()
    result = select_contextual_interpretation(warrant_set, selection_evidence=(selection_evidence(),))

    assert result.outcome == "selected"
    assert result.interpretation_selected is True
    assert result.selected_candidate_ref == "cand:repair"
    assert result.selected_candidate.label == "repair cache typo"
    assert result.operator_material.exact_text == "fix teh cache; maybe inspect yesterday's note"
    assert warrant_set.operator_material.exact_text == "fix teh cache; maybe inspect yesterday's note"
    assert result.selection_evidence[0].exact_text == "I mean the repair-cache interpretation."
    assert result.selection_provenance == ("sel:repair", "operator-clarification:exact")


def test_proposed_corrections_non_selected_residual_unknowns_and_conflicts_remain_explicit():
    result = select_contextual_interpretation(warranted_set(), selection_evidence=(selection_evidence(),))

    assert result.proposed_corrections[0].original_text == "teh"
    assert result.proposed_corrections[0].corrected_text == "the"
    assert [candidate.candidate_ref for candidate in result.non_selected_candidates] == ["cand:inspect"]
    assert [span.span_ref for span in result.residual_source_material] == ["span:retro", "span:fix"]
    assert result.unknowns == ("which note is yesterday's note",)
    assert "operator also mentioned maybe" in result.conflicts


def test_no_selection_occurs_without_candidate_bound_selection_evidence_even_for_unique_warranted_candidate():
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=candidates(),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:repair", "cand:repair", "supporting", "retro:1", "supports repair"),
            RetrospectiveEvidence("ev:inspect", "cand:inspect", "contradicting", "retro:2", "contradicts inspect"),
        ),
    )

    result = select_contextual_interpretation(warrant_set)

    assert result.outcome == "warranted_candidate_without_selection_evidence"
    assert result.selected_candidate_ref is None
    assert result.interpretation_selected is False
    assert [candidate.candidate_ref for candidate in result.non_selected_candidates] == ["cand:repair", "cand:inspect"]


def test_multiple_warranted_candidates_remain_unresolved_without_selection_evidence():
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=candidates(),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:repair", "cand:repair", "supporting", "retro:1", "supports repair"),
            RetrospectiveEvidence("ev:inspect", "cand:inspect", "supporting", "retro:2", "supports inspect"),
        ),
    )
    result = select_contextual_interpretation(warrant_set)

    assert result.outcome == "multiple_warranted_candidates_without_selection_evidence"
    assert result.selected_candidate_ref is None
    assert result.interpretation_selected is False


def test_conflicting_selection_evidence_produces_conflict_and_no_selection():
    result = select_contextual_interpretation(
        warranted_set(),
        selection_evidence=(selection_evidence("cand:repair", "sel:repair"), selection_evidence("cand:inspect", "sel:inspect")),
    )

    assert result.outcome == "conflicting_selection_evidence"
    assert result.selected_candidate_ref is None
    assert result.interpretation_selected is False
    assert any("multiple candidates" in conflict for conflict in result.conflicts)


def test_selection_of_unwarranted_candidate_is_refused():
    warrant_set = produce_contextual_interpretation_warrant_set(
        operator_material=material(),
        candidates=candidates(),
        retrospective_evidence=(
            RetrospectiveEvidence("ev:repair", "cand:repair", "supporting", "retro:1", "supports repair"),
            RetrospectiveEvidence("ev:inspect", "cand:inspect", "contradicting", "retro:2", "contradicts inspect"),
        ),
    )

    result = select_contextual_interpretation(warrant_set, selection_evidence=(selection_evidence("cand:inspect"),))

    assert result.outcome == "selection_refused_unwarranted_candidate"
    assert result.selected_candidate_ref is None
    assert result.interpretation_selected is False
    assert any("standing unwarranted" in conflict for conflict in result.conflicts)


def test_selection_has_no_downstream_or_mutation_effects():
    result = select_contextual_interpretation(warranted_set(), selection_evidence=(selection_evidence(),))

    assert result.downstream_applicability is None
    assert result.downstream_admission is None
    assert result.goal_bound is False
    assert result.inquiry_moved is False
    assert result.authorized is False
    assert result.executed is False
    assert result.recorded is False
    assert result.mutates_conversation is False
    assert result.read_only is True
    assert result.writes_event_ledger is False
    assert result.mutates_state is False
    assert result.mutates_cluster is False
