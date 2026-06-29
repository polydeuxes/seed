from seed_runtime.documentation_structure import DocumentationArchitecturalRelationRecord
from seed_runtime.knowledge.observation_agreement import (
    OBSERVATION_AGREEMENT_BOUNDARY,
    ObservationAgreementRecord,
    observe_observation_agreements,
)
from seed_runtime.knowledge.relationship_observation import RelationshipFact
from seed_runtime.knowledge.self_model_alignment import RepositoryArtifactFact


def test_observation_agreement_preserves_candidate_agreement_and_provenance():
    agreements = observe_observation_agreements(
        documentation_relations=(
            DocumentationArchitecturalRelationRecord(
                left_term="Observation Agreement",
                relation="!=",
                right_term="Grammar Observation",
                source_path="docs/architecture.md",
                line_number=7,
                evidence="Observation Agreement != Grammar Observation",
            ),
        ),
        repository_facts=(
            RepositoryArtifactFact(
                fact="Observation Agreement != Grammar Observation",
                artifact_kind="class",
                path="seed_runtime/knowledge/observation_agreement.py",
                symbol="ObservationAgreementRecord",
            ),
        ),
        relationship_facts=(
            RelationshipFact(
                relationship_kind="defines",
                subject="seed_runtime.knowledge.observation_agreement",
                object="ObservationAgreementRecord",
                path="seed_runtime/knowledge/observation_agreement.py",
                evidence="Observation Agreement != Grammar Observation",
            ),
        ),
    )

    assert agreements == (
        ObservationAgreementRecord(
            participating_observation_streams=(
                "documentation_architectural_relation",
                "repository_artifact",
                "relationship_fact",
            ),
            supporting_evidence=agreements[0].supporting_evidence,
            provenance=(
                "docs/architecture.md:7",
                "seed_runtime/knowledge/observation_agreement.py",
                "seed_runtime/knowledge/observation_agreement.py",
            ),
            candidate_agreement="Observation Agreement != Grammar Observation",
        ),
    )
    assert agreements[0].non_promotion_boundary == "candidate_only_not_architectural_truth"
    assert [e.evidence for e in agreements[0].supporting_evidence] == [
        "Observation Agreement != Grammar Observation",
        "Observation Agreement != Grammar Observation",
        "Observation Agreement != Grammar Observation",
    ]


def test_observation_agreement_requires_independent_streams_and_does_not_infer_semantics():
    agreements = observe_observation_agreements(
        documentation_relations=(
            DocumentationArchitecturalRelationRecord(
                left_term="Observation Agreement",
                relation="!=",
                right_term="Grammar Observation",
                source_path="docs/architecture.md",
                line_number=7,
                evidence="Observation Agreement != Grammar Observation",
            ),
        ),
        repository_facts=(
            RepositoryArtifactFact(
                fact="ObservationAgreementRecord is separate from grammar",
                artifact_kind="class",
                path="seed_runtime/knowledge/observation_agreement.py",
                symbol="ObservationAgreementRecord",
            ),
        ),
    )

    assert agreements == ()


def test_observation_agreement_boundary_rejects_promotion_and_mutation():
    assert OBSERVATION_AGREEMENT_BOUNDARY == {
        "consumes_supplied_observation_records": True,
        "preserves_candidate_agreement": True,
        "preserves_provenance": True,
        "preserves_observation_independence": True,
        "emits_candidate_agreement_records": True,
        "promotes_agreement": False,
        "owns_grammar": False,
        "owns_responsibility_recovery": False,
        "owns_family_recovery": False,
        "owns_lexicon": False,
        "semantic_interpretation": False,
        "architectural_truth": False,
        "runtime_mutation": False,
        "event_writes": False,
        "ledger_writes": False,
        "repository_mutation": False,
        "cluster_mutation": False,
    }
