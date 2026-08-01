"""Bounded constitutional question artifact and renderers.

This module preserves explicitly supplied BoundedConstitutionalQuestion fields.
It preserves explicit caller inputs as evidence/testimony without
projecting views, discovering capabilities, selecting authority, writing ledgers,
or mutating cluster state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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


def bounded_constitutional_question_json(
    artifact: BoundedConstitutionalQuestion,
) -> dict[str, Any]:
    """Return deterministic JSON-ready bounded-question data."""

    return to_plain(artifact)


def format_bounded_constitutional_question(
    artifact: BoundedConstitutionalQuestion,
) -> str:
    """Return a stable human-readable bounded-question rendering."""

    lines = [
        "Bounded Constitutional Question",
        f"bounded_question_id: {artifact.bounded_question_id}",
        f"operator_inquiry: {artifact.operator_inquiry}",
        f"bounded_question: {artifact.bounded_question}",
        f"constitutional_intent: {artifact.constitutional_intent}",
        f"scope_status: {artifact.scope_status}",
        f"inquiry_provenance: {artifact.inquiry_provenance}",
        f"testimony_status: {artifact.testimony_status}",
        f"read_only: {str(artifact.read_only).lower()}",
        f"writes_event_ledger: {str(artifact.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(artifact.mutates_cluster).lower()}",
    ]
    for label, values in (
        ("uncertainty", artifact.uncertainty),
        ("unknowns", artifact.unknowns),
        ("caller_supplied_fields", tuple(f"{k}={v}" for k, v in artifact.caller_supplied_fields)),
        ("read_only_boundaries", artifact.read_only_boundaries),
    ):
        lines.append(label + ":")
        lines += [f"- {value}" for value in values] or ["- none"]
    return "\n".join(lines)
