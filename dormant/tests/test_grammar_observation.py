from seed_runtime.knowledge.grammar_observation import (
    GRAMMAR_OBSERVATION_BOUNDARY,
    GrammarObservationRecord,
    observe_grammar_observations,
)
from seed_runtime.knowledge.observation_agreement import (
    ObservationAgreementEvidence,
    ObservationAgreementRecord,
)


def _agreement(candidate_agreement, provenance):
    return ObservationAgreementRecord(
        participating_observation_streams=("documentation_architectural_relation", "relationship_fact"),
        supporting_evidence=(
            ObservationAgreementEvidence(
                stream="documentation_architectural_relation",
                provenance=provenance,
                evidence=candidate_agreement,
            ),
            ObservationAgreementEvidence(
                stream="relationship_fact",
                provenance=f"{provenance}:relationship",
                evidence=candidate_agreement,
            ),
        ),
        provenance=(provenance, f"{provenance}:relationship"),
        candidate_agreement=candidate_agreement,
    )


def test_grammar_observation_emits_only_recurring_relation_shapes():
    agreements = (
        _agreement("Structure Observation != Relationship Observation", "docs/a.md:1"),
        _agreement("Observation Agreement != Grammar Observation", "docs/b.md:2"),
        _agreement("single use -> not recurring", "docs/c.md:3"),
    )

    observations = observe_grammar_observations(agreements)

    assert observations == (
        GrammarObservationRecord(
            observed_relation_shape="term != term",
            supporting_agreements=agreements[:2],
            provenance=(
                "docs/a.md:1",
                "docs/a.md:1:relationship",
                "docs/b.md:2",
                "docs/b.md:2:relationship",
            ),
            recurrence_evidence=(
                "Structure Observation != Relationship Observation",
                "Observation Agreement != Grammar Observation",
            ),
        ),
    )
    assert observations[0].non_promotion_boundary == "grammar_observation_only_not_architectural_truth"


def test_grammar_observation_consumes_agreements_without_promoting_semantics():
    agreements = (
        _agreement("Responsibility Recovery != Grammar Observation", "docs/a.md:1"),
        _agreement("Family Recovery != Grammar Observation", "docs/b.md:2"),
    )

    observations = observe_grammar_observations(agreements)

    assert observations[0].observed_relation_shape == "term != term"
    assert observations[0].recurrence_evidence == (
        "Responsibility Recovery != Grammar Observation",
        "Family Recovery != Grammar Observation",
    )


def test_grammar_observation_boundary_rejects_adjacent_ownership_and_mutation():
    assert GRAMMAR_OBSERVATION_BOUNDARY == {
        "consumes_observation_agreement_records": True,
        "observes_recurring_relation_shapes": True,
        "preserves_supporting_evidence": True,
        "preserves_provenance": True,
        "preserves_recurrence_evidence": True,
        "emits_grammar_observations": True,
        "promotes_grammar": False,
        "owns_responsibility_recovery": False,
        "owns_family_recovery": False,
        "owns_lexicon": False,
        "semantic_interpretation": False,
        "architectural_truth": False,
        "capability_promotion": False,
        "runtime_mutation": False,
        "event_writes": False,
        "ledger_writes": False,
        "repository_mutation": False,
        "cluster_mutation": False,
    }
