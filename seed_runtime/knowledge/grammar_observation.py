"""Read-only Grammar Observation over Observation Agreement records.

Grammar Observation consumes only ``ObservationAgreementRecord`` instances and
emits implementation-local grammar observations for recurring relation shapes.
It preserves supporting agreements, provenance, and recurrence evidence without
parsing Markdown, Python, runtime state, or repositories.

This module is intentionally internal: it does not add CLI, JSON, schema,
diagnostic, event, ledger, runtime, repository, or cluster behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from seed_runtime.knowledge.observation_agreement import ObservationAgreementRecord

GRAMMAR_OBSERVATION_BOUNDARY = {
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

_RECURRING_SHAPE_ONLY = "grammar_observation_only_not_architectural_truth"
_RELATION_OPERATORS = ("!=", "->", "=>", "==", "=")


@dataclass(frozen=True)
class GrammarObservationRecord:
    """Implementation-local observation of a recurring relation shape.

    The record intentionally preserves shape recurrence only. It does not carry
    responsibility, family, lexicon, semantic meaning, or architectural truth.
    """

    observed_relation_shape: str
    supporting_agreements: tuple[ObservationAgreementRecord, ...]
    provenance: tuple[str, ...]
    recurrence_evidence: tuple[str, ...]
    non_promotion_boundary: str = _RECURRING_SHAPE_ONLY


def observe_grammar_observations(
    observation_agreements: Sequence[ObservationAgreementRecord],
) -> tuple[GrammarObservationRecord, ...]:
    """Emit grammar observations from recurring Observation Agreement shapes.

    Shape detection is deliberately narrow and syntactic: a candidate agreement
    with one known relation operator and non-empty text on both sides contributes
    the operator-shaped form ``term <operator> term``. At least two supplied
    agreement records must share the same shape before a grammar observation is
    emitted. No source files, repositories, runtime state, or lower-level
    observation records are consumed.
    """

    agreements_by_shape: dict[str, list[ObservationAgreementRecord]] = {}
    for agreement in observation_agreements:
        shape = _relation_shape(agreement.candidate_agreement)
        if shape is None:
            continue
        agreements_by_shape.setdefault(shape, []).append(agreement)

    observations: list[GrammarObservationRecord] = []
    for shape in sorted(agreements_by_shape):
        agreements = tuple(agreements_by_shape[shape])
        if len(agreements) < 2:
            continue
        observations.append(
            GrammarObservationRecord(
                observed_relation_shape=shape,
                supporting_agreements=agreements,
                provenance=tuple(
                    provenance
                    for agreement in agreements
                    for provenance in agreement.provenance
                ),
                recurrence_evidence=tuple(
                    agreement.candidate_agreement for agreement in agreements
                ),
            )
        )
    return tuple(observations)


def _relation_shape(candidate_agreement: str) -> str | None:
    text = candidate_agreement.strip()
    for operator in _RELATION_OPERATORS:
        if text.count(operator) != 1:
            continue
        left, right = (part.strip() for part in text.split(operator, 1))
        if left and right:
            return f"term {operator} term"
    return None
