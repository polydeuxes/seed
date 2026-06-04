"""Deterministic fact projection driven by :mod:`seed_runtime.inference_catalog`."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from seed_runtime.facts import Fact
from seed_runtime.inference_catalog import InferenceCatalog, InferenceRule
from seed_runtime.predicate_catalog import PredicateCatalog


def infer_facts(
    facts: Iterable[Fact],
    inference_catalog: InferenceCatalog,
    predicate_catalog: PredicateCatalog,
) -> dict[str, Fact]:
    """Project catalog rules from current observed facts without side effects."""

    observed_facts = [fact for fact in facts if not fact.inferred]
    observed_predicates = {
        (fact.subject_id, fact.predicate) for fact in observed_facts
    }
    candidates: dict[tuple[str, str], list[tuple[Fact, InferenceRule]]] = (
        defaultdict(list)
    )

    for fact in observed_facts:
        for rule in inference_catalog.matching_rules(fact.predicate, fact.value):
            if (fact.subject_id, rule.then_predicate) in observed_predicates:
                continue
            candidates[(fact.subject_id, rule.then_predicate)].append((fact, rule))

    inferred: dict[str, Fact] = {}
    for (_, predicate), projections in sorted(candidates.items()):
        definition = predicate_catalog.get(predicate)
        if definition is not None and definition.cardinality == "single":
            projected_values = {_value_key(rule.then_value) for _, rule in projections}
            if len(projected_values) != 1:
                continue
        for source_fact, rule in projections:
            inferred_fact = _inferred_fact(source_fact, rule)
            inferred.setdefault(inferred_fact.id, inferred_fact)

    return inferred


def _inferred_fact(source_fact: Fact, rule: InferenceRule) -> Fact:
    return Fact(
        id=_inferred_fact_id(
            source_fact.subject_id, rule.then_predicate, rule.then_value
        ),
        subject_id=source_fact.subject_id,
        predicate=rule.then_predicate,
        value=rule.then_value,
        dimensions=dict(source_fact.dimensions),
        evidence_ids=list(source_fact.evidence_ids),
        observed_at=source_fact.observed_at,
        expires_at=source_fact.expires_at,
        source_type="inferred",
        confidence=min(source_fact.confidence, rule.confidence),
        inferred=True,
        source_fact_id=source_fact.id,
        inference_rule_id=rule.id,
    )


def _inferred_fact_id(subject_id: str, predicate: str, value: object) -> str:
    safe_subject = _safe_id_part(subject_id)
    safe_predicate = _safe_id_part(predicate)
    safe_value = _safe_id_part(str(value))
    return f"fact_inferred_{safe_subject}_{safe_predicate}_{safe_value}"


def _safe_id_part(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value)


def _value_key(value: object) -> str:
    return repr(value)
