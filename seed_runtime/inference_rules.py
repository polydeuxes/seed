"""Deterministic catalog-driven fact inference for projected state."""

from __future__ import annotations

import json
from typing import Any, Iterable

from seed_runtime.facts import Fact
from seed_runtime.inference_catalog import InferenceCatalog, InferenceRule


def infer_facts(
    facts: Iterable[Fact], inference_catalog: InferenceCatalog | None = None
) -> dict[str, Fact]:
    """Infer facts using the catalog without overwriting observed predicates."""

    catalog = inference_catalog or InferenceCatalog.load()
    observed_facts = [fact for fact in facts if not fact.inferred]
    observed_predicates = {
        (fact.subject_id, fact.predicate) for fact in observed_facts
    }
    inferred: dict[str, Fact] = {}

    for fact in observed_facts:
        for rule in catalog.for_source_predicate(fact.predicate):
            if not _values_equal(fact.value, rule.source_value):
                continue
            if (fact.subject_id, rule.target_predicate) in observed_predicates:
                continue
            inferred_fact = _inferred_fact(fact, rule)
            inferred.setdefault(inferred_fact.id, inferred_fact)

    return inferred


def _inferred_fact(source_fact: Fact, rule: InferenceRule) -> Fact:
    return Fact(
        id=_inferred_fact_id(
            source_fact.subject_id, rule.target_predicate, rule.target_value
        ),
        subject_id=source_fact.subject_id,
        predicate=rule.target_predicate,
        value=rule.target_value,
        dimensions=dict(source_fact.dimensions),
        evidence_ids=list(source_fact.evidence_ids),
        observed_at=source_fact.observed_at,
        expires_at=source_fact.expires_at,
        source_type="inferred",
        confidence=min(source_fact.confidence, rule.confidence_cap),
        inferred=True,
        inference_rule_id=rule.id,
        source_fact_id=source_fact.id,
        confidence_cap=(
            rule.confidence_cap if source_fact.confidence > rule.confidence_cap else None
        ),
    )


def _values_equal(first: Any, second: Any) -> bool:
    return json.dumps(first, sort_keys=True, default=str) == json.dumps(
        second, sort_keys=True, default=str
    )


def _inferred_fact_id(subject_id: str, predicate: str, value: Any) -> str:
    safe_subject = _safe_id_part(subject_id)
    safe_predicate = _safe_id_part(predicate)
    safe_value = _safe_id_part(str(value))
    return f"fact_inferred_{safe_subject}_{safe_predicate}_{safe_value}"


def _safe_id_part(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value)
