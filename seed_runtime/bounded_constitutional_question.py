"""Deterministic bounded constitutional question production.

This module owns only the Operator Inquiry -> BoundedConstitutionalQuestion
boundary. It preserves explicit caller inputs as evidence/testimony without
projecting views, discovering capabilities, selecting authority, writing ledgers,
or mutating cluster state.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from seed_runtime.serialization import to_plain


@dataclass(frozen=True)
class BoundedConstitutionalQuestion:
    """Immutable provenance-preserving bounded constitutional question artifact."""

    bounded_question_id: str
    operator_inquiry: str
    inquiry_provenance: str
    bounded_question: str
    constitutional_intent: str
    scope_status: str
    uncertainty: tuple[str, ...]
    unknowns: tuple[str, ...]
    caller_supplied_fields: tuple[tuple[str, str], ...] = ()
    testimony_status: str = "operator testimony preserved as evidence, not established fact"
    read_only_boundaries: tuple[str, ...] = (
        "operator inquiry preserved as received",
        "explicit caller-supplied bounded fields only",
        "no natural-language classification",
        "no established fact promotion",
        "no verified claim promotion",
        "no constitutional authority creation",
        "no repository truth creation",
        "no durable knowledge creation",
        "no authoritative capability creation",
        "no constitutional view selection",
        "no QuestionProjection production",
        "no event-ledger writes",
        "no cluster mutation",
    )
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False


def _tuple_of_strings(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(str(value) for value in values)


def _field_items(fields: dict[str, Any] | None) -> tuple[tuple[str, str], ...]:
    if not fields:
        return ()
    return tuple((str(key), str(value)) for key, value in sorted(fields.items()))


def _stable_question_id(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "bounded-constitutional-question:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def produce_bounded_constitutional_question(
    *,
    operator_inquiry: str,
    inquiry_provenance: str,
    bounded_question: str,
    constitutional_intent: str,
    scope_status: str,
    uncertainty: Iterable[str] = (),
    unknowns: Iterable[str] = (),
    bounded_question_id: str | None = None,
    caller_supplied_fields: dict[str, Any] | None = None,
) -> BoundedConstitutionalQuestion:
    """Produce one deterministic bounded question from explicit caller inputs only."""

    uncertainty_tuple = _tuple_of_strings(uncertainty)
    unknowns_tuple = _tuple_of_strings(unknowns)
    caller_fields_tuple = _field_items(caller_supplied_fields)

    identity_payload = {
        "operator_inquiry": operator_inquiry,
        "inquiry_provenance": inquiry_provenance,
        "bounded_question": bounded_question,
        "constitutional_intent": constitutional_intent,
        "scope_status": scope_status,
        "uncertainty": uncertainty_tuple,
        "unknowns": unknowns_tuple,
        "caller_supplied_fields": caller_fields_tuple,
    }

    return BoundedConstitutionalQuestion(
        bounded_question_id=bounded_question_id or _stable_question_id(identity_payload),
        operator_inquiry=operator_inquiry,
        inquiry_provenance=inquiry_provenance,
        bounded_question=bounded_question,
        constitutional_intent=constitutional_intent,
        scope_status=scope_status,
        uncertainty=uncertainty_tuple,
        unknowns=unknowns_tuple,
        caller_supplied_fields=caller_fields_tuple,
    )


def bounded_constitutional_question_json(
    artifact: BoundedConstitutionalQuestion,
) -> dict[str, Any]:
    """Return deterministic JSON-ready bounded-question data."""

    return to_plain(artifact)
