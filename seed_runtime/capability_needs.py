"""Diagnostic-run scoped capability-need views."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from seed_runtime.state import State


@dataclass
class CapabilityNeedEntry:
    capability: str
    subjects: set[str] = field(default_factory=set)
    diagnostics: set[str] = field(default_factory=set)
    needed_evidence: set[str] = field(default_factory=set)
    diagnostic_runs: set[str] = field(default_factory=set)


def build_capability_needs(
    state: State,
    *,
    subject_filter: str | None = None,
    diagnostic_filter: str | None = None,
) -> list[CapabilityNeedEntry]:
    entries: dict[str, CapabilityNeedEntry] = {}
    for fact in state.facts.values():
        if not fact.subject_id.startswith("diagnostic_run:"):
            continue
        if fact.predicate != "diagnostic_capability_need" or not isinstance(
            fact.value, dict
        ):
            continue
        value: dict[str, Any] = fact.value
        subject = str(value.get("diagnostic_subject") or value.get("subject") or "")
        diagnostic = str(value.get("diagnostic_name") or value.get("diagnostic") or "")
        capability = str(
            value.get("candidate_capability") or value.get("capability") or ""
        )
        needed = str(value.get("needed_evidence") or "")
        if not capability or not subject or not diagnostic:
            continue
        if subject_filter and subject != subject_filter:
            continue
        if diagnostic_filter and diagnostic != diagnostic_filter:
            continue
        entry = entries.setdefault(capability, CapabilityNeedEntry(capability))
        entry.subjects.add(subject)
        entry.diagnostics.add(diagnostic)
        if needed:
            entry.needed_evidence.add(needed)
        entry.diagnostic_runs.add(fact.subject_id)
    return sorted(entries.values(), key=lambda e: (-len(e.subjects), e.capability))


def capability_needs_json(entries: list[CapabilityNeedEntry]) -> list[dict[str, Any]]:
    return [
        {
            "capability": entry.capability,
            "subjects": sorted(entry.subjects),
            "diagnostics": sorted(entry.diagnostics),
            "needed_evidence": sorted(entry.needed_evidence),
        }
        for entry in entries
    ]


def format_capability_needs(entries: list[CapabilityNeedEntry]) -> str:
    lines = ["Capability Needs", ""]
    if not entries:
        lines.append("(none)")
        return "\n".join(lines)
    for entry in entries:
        lines.append(entry.capability)
        lines.append(f"  subjects: {len(entry.subjects)}")
        lines.append(f"  diagnostics: {', '.join(sorted(entry.diagnostics))}")
        lines.append(f"  needed evidence: {', '.join(sorted(entry.needed_evidence))}")
        lines.append("")
    return "\n".join(lines).rstrip()
