"""Capability-need views from recorded diagnostics and current read-only diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from seed_runtime.ownership_discrepancies import (
    build_ownership_discrepancies,
    diagnostic_capability_need_records,
)
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
    for row in build_ownership_discrepancies(state, subject_filter=subject_filter):
        for value in diagnostic_capability_need_records(row):
            _add_capability_need(
                entries,
                value,
                diagnostic_run="current_projection",
                subject_filter=subject_filter,
                diagnostic_filter=diagnostic_filter,
            )
    for fact in state.facts.values():
        if not fact.subject_id.startswith("diagnostic_run:"):
            continue
        if fact.predicate != "diagnostic_capability_need" or not isinstance(
            fact.value, dict
        ):
            continue
        _add_capability_need(
            entries,
            fact.value,
            diagnostic_run=fact.subject_id,
            subject_filter=subject_filter,
            diagnostic_filter=diagnostic_filter,
        )
    return sorted(
        entries.values(),
        key=lambda e: (
            -len(e.subjects),
            _capability_priority(e.capability),
            e.capability,
        ),
    )


def _capability_priority(capability: str) -> int:
    return {
        "listener_process_inventory": 0,
        "container_port_mapping": 1,
        "container_inventory": 2,
    }.get(capability, 100)


def _add_capability_need(
    entries: dict[str, CapabilityNeedEntry],
    value: dict[str, Any],
    *,
    diagnostic_run: str,
    subject_filter: str | None,
    diagnostic_filter: str | None,
) -> None:
    subject = str(value.get("diagnostic_subject") or value.get("subject") or "")
    diagnostic = str(value.get("diagnostic_name") or value.get("diagnostic") or "")
    capability = str(
        value.get("candidate_capability") or value.get("capability") or ""
    )
    needed = str(value.get("needed_evidence") or "")
    if not capability or not subject or not diagnostic:
        return
    if subject_filter and subject != subject_filter:
        return
    if diagnostic_filter and diagnostic != diagnostic_filter:
        return
    entry = entries.setdefault(capability, CapabilityNeedEntry(capability))
    entry.subjects.add(subject)
    entry.diagnostics.add(diagnostic)
    if needed:
        entry.needed_evidence.add(needed)
    entry.diagnostic_runs.add(diagnostic_run)


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
