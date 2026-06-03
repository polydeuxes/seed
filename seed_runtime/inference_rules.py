"""Deterministic relationship inference rules for projected state."""

from __future__ import annotations

from typing import Iterable

from seed_runtime.facts import Fact

_MANAGED_BY_BY_RUNTIME = {
    "docker": "docker_container_lifecycle",
    "systemd": "systemctl_cli",
}


def infer_facts(facts: Iterable[Fact]) -> dict[str, Fact]:
    """Infer relationship facts from observed facts without overwriting them.

    Rules are deliberately deterministic and local: only observed runtime
    relationships produce managed_by relationships. If the subject already has
    an observed managed_by fact, the observed fact wins and no managed_by fact is
    inferred for that subject.
    """

    observed_facts = [fact for fact in facts if not fact.inferred]
    observed_predicates = {
        (fact.subject_id, fact.predicate) for fact in observed_facts
    }
    inferred: dict[str, Fact] = {}

    for fact in observed_facts:
        if fact.predicate != "runtime" or not isinstance(fact.value, str):
            continue
        runtime = fact.value.strip().lower()
        managed_by = _MANAGED_BY_BY_RUNTIME.get(runtime)
        if managed_by is None:
            continue
        if (fact.subject_id, "managed_by") in observed_predicates:
            continue

        inferred_fact = _managed_by_fact(fact, managed_by)
        inferred.setdefault(inferred_fact.id, inferred_fact)

    return inferred


def _managed_by_fact(runtime_fact: Fact, managed_by: str) -> Fact:
    return Fact(
        id=_inferred_fact_id(runtime_fact.subject_id, "managed_by", managed_by),
        subject_id=runtime_fact.subject_id,
        predicate="managed_by",
        value=managed_by,
        evidence_ids=list(runtime_fact.evidence_ids),
        observed_at=runtime_fact.observed_at,
        expires_at=runtime_fact.expires_at,
        confidence=runtime_fact.confidence,
        inferred=True,
    )


def _inferred_fact_id(subject_id: str, predicate: str, value: str) -> str:
    safe_subject = _safe_id_part(subject_id)
    safe_predicate = _safe_id_part(predicate)
    safe_value = _safe_id_part(value)
    return f"fact_inferred_{safe_subject}_{safe_predicate}_{safe_value}"


def _safe_id_part(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value)
