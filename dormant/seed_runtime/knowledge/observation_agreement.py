"""Read-only Observation Agreement over already-observed records.

Observation Agreement consumes supplied observation records and emits candidate
agreement records with provenance. It does not parse Markdown, parse Python,
read repositories, scan runtime, execute tools, infer semantics, recover
responsibility, own grammar, own lexicon, promote architectural truth, write
ledgers, or mutate runtime/repository/cluster state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from seed_runtime.documentation_structure import DocumentationArchitecturalRelationRecord
from seed_runtime.knowledge.relationship_observation import RelationshipFact
from seed_runtime.knowledge.self_model_alignment import RepositoryArtifactFact

OBSERVATION_AGREEMENT_BOUNDARY = {
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

_DOCUMENTATION_ARCHITECTURAL_RELATION = "documentation_architectural_relation"
_REPOSITORY_ARTIFACT = "repository_artifact"
_RELATIONSHIP_FACT = "relationship_fact"
_CANDIDATE_ONLY = "candidate_only_not_architectural_truth"


@dataclass(frozen=True)
class ObservationAgreementEvidence:
    """Provenance-preserving reference to one supplied observation record."""

    stream: str
    provenance: str
    evidence: str


@dataclass(frozen=True)
class ObservationAgreementRecord:
    """Candidate agreement between independent supplied observation streams."""

    participating_observation_streams: tuple[str, ...]
    supporting_evidence: tuple[ObservationAgreementEvidence, ...]
    provenance: tuple[str, ...]
    candidate_agreement: str
    non_promotion_boundary: str = _CANDIDATE_ONLY


def observe_observation_agreements(
    documentation_relations: Sequence[DocumentationArchitecturalRelationRecord] = (),
    repository_facts: Sequence[RepositoryArtifactFact] = (),
    relationship_facts: Sequence[RelationshipFact] = (),
) -> tuple[ObservationAgreementRecord, ...]:
    """Emit candidate agreement records from already-observed inputs only.

    The rule is intentionally small: two or more independent observation streams
    agree only when their supplied evidence text is exactly the same after
    trimming surrounding whitespace. Exact evidence equality preserves candidate
    agreement and provenance without parsing substrates, canonicalizing terms,
    interpreting semantics, or promoting the result to truth.
    """

    evidence_by_text: dict[str, list[ObservationAgreementEvidence]] = {}
    for evidence in _supplied_evidence(
        documentation_relations, repository_facts, relationship_facts
    ):
        evidence_by_text.setdefault(evidence.evidence.strip(), []).append(evidence)

    agreements: list[ObservationAgreementRecord] = []
    for evidence_text in sorted(evidence_by_text):
        evidence_records = tuple(evidence_by_text[evidence_text])
        streams = tuple(dict.fromkeys(record.stream for record in evidence_records))
        if len(streams) < 2:
            continue
        agreements.append(
            ObservationAgreementRecord(
                participating_observation_streams=streams,
                supporting_evidence=evidence_records,
                provenance=tuple(record.provenance for record in evidence_records),
                candidate_agreement=evidence_text,
            )
        )
    return tuple(agreements)


def _supplied_evidence(
    documentation_relations: Sequence[DocumentationArchitecturalRelationRecord],
    repository_facts: Sequence[RepositoryArtifactFact],
    relationship_facts: Sequence[RelationshipFact],
) -> tuple[ObservationAgreementEvidence, ...]:
    evidence: list[ObservationAgreementEvidence] = []
    for relation in documentation_relations:
        evidence.append(
            ObservationAgreementEvidence(
                stream=_DOCUMENTATION_ARCHITECTURAL_RELATION,
                provenance=f"{relation.source_path}:{relation.line_number}",
                evidence=relation.evidence,
            )
        )
    for fact in repository_facts:
        evidence.append(
            ObservationAgreementEvidence(
                stream=_REPOSITORY_ARTIFACT,
                provenance=fact.path,
                evidence=fact.fact,
            )
        )
    for fact in relationship_facts:
        evidence.append(
            ObservationAgreementEvidence(
                stream=_RELATIONSHIP_FACT,
                provenance=fact.path,
                evidence=fact.evidence,
            )
        )
    return tuple(evidence)
