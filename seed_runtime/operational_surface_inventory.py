"""Implementation-backed inventory for operational CLI visibility surfaces."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Any

from seed_runtime.diagnostic_inventory import (
    DIAGNOSTIC_INVENTORY,
    DiagnosticInventoryEntry,
)

_OPERATIONAL_KEYWORDS: tuple[tuple[str, str], ...] = (
    ("diagnostic", "diagnostic"),
    ("audit", "audit"),
    ("inventory", "inventory"),
    ("debug", "debug"),
    ("brief", "view"),
    ("summary", "view"),
    ("view", "view"),
    ("observe", "observation"),
    ("observation", "observation"),
    ("ownership", "analysis"),
    ("analysis", "analysis"),
    ("confidence", "analysis"),
    ("coverage", "analysis"),
)
_AUXILIARY_FLAGS = {
    "--json",
    "--record",
    "--mismatches",
    "--status",
    "--operational-graph-confidence-tier",
}
_MODIFIER_FLAGS = {
    "--json",
    "--record",
    "--mismatches",
    "--status",
    "--include-expired",
    "--include-history",
    "--include-warnings",
    "--quiet-output",
    "--verbose-observations",
    "--observe-timings",
    "--knowledge-reachability-audit-json",
    "--knowledge-reachability-audit-all",
    "--knowledge-reachability-audit-limit",
    "--knowledge-reachability-audit-max-seconds",
    "--operational-graph-confidence-tier",
}
_MANUAL_INPUT_FLAGS = {
    "--alias",
    "--fact",
    "--observe",
    "--observe-json",
    "--fact-expires-at",
    "--fact-ttl-seconds",
}
_LEGACY_HINTS = ("legacy", "no longer accepted")
_FILTER_HINTS = ("limit ", "filter", "only be used with", "kind for", "required by")
_PRIMARY_ACTIONS = {"_StoreTrueAction", "_StoreConstAction"}


@dataclass(frozen=True)
class OperationalSurface:
    name: str
    category: str
    registered: bool
    json_capable: bool
    evidence: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "registered": self.registered,
            "json_capable": self.json_capable,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class OperationalSurfaceClassification:
    surface: str
    classification: str
    reason: str
    registered: bool
    category: str | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "surface": self.surface,
            "classification": self.classification,
            "reason": self.reason,
            "registered": self.registered,
            "category": self.category,
        }


@dataclass(frozen=True)
class OperationalSurfaceClassificationAudit:
    items: tuple[OperationalSurfaceClassification, ...]

    @property
    def counts(self) -> Counter[str]:
        return Counter(item.classification for item in self.items)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "counts": dict(sorted(self.counts.items())),
            "items": [item.to_json_dict() for item in self.items],
        }


@dataclass(frozen=True)
class VisibilityCoverageAudit:
    surfaces: tuple[OperationalSurface, ...]
    classifications: tuple[OperationalSurfaceClassification, ...] = ()

    @property
    def discovered(self) -> int:
        return len(self.surfaces)

    @property
    def registered(self) -> int:
        return sum(surface.registered for surface in self.surfaces)

    @property
    def unregistered(self) -> tuple[OperationalSurface, ...]:
        return tuple(surface for surface in self.surfaces if not surface.registered)

    @property
    def unregistered_classification_counts(self) -> Counter[str]:
        surface_names = {surface.name for surface in self.surfaces}
        return Counter(
            item.classification
            for item in self.classifications
            if not item.registered and item.surface in surface_names
        )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "discovered": self.discovered,
            "registered": self.registered,
            "unregistered": [surface.to_json_dict() for surface in self.unregistered],
            "unregistered_classifications": dict(
                sorted(self.unregistered_classification_counts.items())
            ),
        }


def build_operational_surface_inventory(
    parser: argparse.ArgumentParser,
    *,
    diagnostic_entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> tuple[OperationalSurface, ...]:
    """Discover operational CLI surfaces from argparse declarations."""
    registered_flags, json_flags = _registered_and_json_flags(diagnostic_entries)
    surfaces: list[OperationalSurface] = []
    for action, flags, primary in _iter_public_long_options(parser):
        if primary in _AUXILIARY_FLAGS:
            continue
        category = _category_for(primary, action.help or "")
        if category is None:
            continue
        surfaces.append(
            OperationalSurface(
                name=primary,
                category=category,
                registered=any(flag in registered_flags for flag in flags),
                json_capable=any(flag in json_flags for flag in flags),
                evidence="argparse",
            )
        )
    return tuple(sorted(surfaces, key=lambda surface: surface.name))


def build_operational_surface_classification_audit(
    parser: argparse.ArgumentParser,
    *,
    diagnostic_entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> OperationalSurfaceClassificationAudit:
    registered_flags, _ = _registered_and_json_flags(diagnostic_entries)
    items = []
    for action, flags, primary in _iter_public_long_options(parser):
        classification, reason = _classification_for(primary, action)
        items.append(
            OperationalSurfaceClassification(
                surface=primary,
                classification=classification,
                reason=reason,
                registered=any(flag in registered_flags for flag in flags),
                category=_category_for(primary, action.help or ""),
            )
        )
    return OperationalSurfaceClassificationAudit(
        tuple(sorted(items, key=lambda item: item.surface))
    )


def build_visibility_coverage_audit(
    parser: argparse.ArgumentParser,
    *,
    diagnostic_entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> VisibilityCoverageAudit:
    return VisibilityCoverageAudit(
        build_operational_surface_inventory(parser, diagnostic_entries=diagnostic_entries),
        build_operational_surface_classification_audit(
            parser, diagnostic_entries=diagnostic_entries
        ).items,
    )


def operational_surface_inventory_json(
    surfaces: tuple[OperationalSurface, ...],
) -> dict[str, Any]:
    return {"surfaces": [surface.to_json_dict() for surface in surfaces]}


def operational_surface_classification_audit_json(
    audit: OperationalSurfaceClassificationAudit,
) -> dict[str, Any]:
    return audit.to_json_dict()


def visibility_coverage_audit_json(audit: VisibilityCoverageAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_operational_surface_inventory(
    surfaces: tuple[OperationalSurface, ...],
) -> str:
    lines = ["Operational Surface Inventory", "", f"Discovered: {len(surfaces)}"]
    if not surfaces:
        lines.extend(
            ["", "No operational surfaces discovered from implementation evidence."]
        )
        return "\n".join(lines)
    for surface in surfaces:
        lines.extend(
            [
                "",
                "Surface:",
                f"  {surface.name}",
                "Category:",
                f"  {surface.category}",
                "JSON:",
                f"  {_yes_no(surface.json_capable)}",
                "Registered:",
                f"  {_yes_no(surface.registered)}",
            ]
        )
    return "\n".join(lines)


def format_operational_surface_classification_audit(
    audit: OperationalSurfaceClassificationAudit,
) -> str:
    lines = ["Operational Surface Classification Audit", ""]
    if not audit.items:
        lines.append("No CLI elements discovered from implementation evidence.")
        return "\n".join(lines)
    labels = {
        "primary_surface": "Primary Surfaces",
        "debug_surface": "Debug Surfaces",
        "filter": "Filters",
        "modifier": "Modifiers",
        "manual_input": "Manual Inputs",
        "legacy_surface": "Legacy Surfaces",
        "unknown": "Unknown",
    }
    counts = audit.counts
    for key, label in labels.items():
        lines.append(f"{label}: {counts.get(key, 0)}")
    for item in audit.items:
        lines.extend(
            [
                "",
                item.surface,
                "",
                "Classification:",
                f"  {item.classification}",
                "",
                "Reason:",
                f"  {item.reason}",
            ]
        )
    return "\n".join(lines)


def format_visibility_coverage_audit(audit: VisibilityCoverageAudit) -> str:
    lines = [
        "Visibility Coverage Audit",
        "",
        f"Discovered surfaces: {audit.discovered}",
        f"Registered surfaces: {audit.registered}",
        f"Unregistered surfaces: {len(audit.unregistered)}",
    ]
    counts = audit.unregistered_classification_counts
    if counts:
        labels = {
            "primary_surface": "Unregistered primary surfaces",
            "debug_surface": "Unregistered debug surfaces",
            "filter": "Unregistered filters",
            "modifier": "Unregistered modifiers",
            "manual_input": "Unregistered manual inputs",
            "legacy_surface": "Unregistered legacy surfaces",
            "unknown": "Unregistered unknown",
        }
        for key, label in labels.items():
            if key in counts:
                lines.append(f"{label}: {counts[key]}")
    if not audit.unregistered:
        lines.extend(
            [
                "",
                "All discovered operational surfaces are registered in diagnostic inventory.",
            ]
        )
        return "\n".join(lines)
    by_name = {item.surface: item for item in audit.classifications}
    for surface in audit.unregistered:
        item = by_name.get(surface.name)
        lines.extend(
            [
                "",
                "Surface:",
                f"  {surface.name}",
                "Classification:",
                f"  {item.classification if item else 'unknown'}",
                "Status:",
                "  missing registration",
                "Impact:",
                "  invisible to diagnostic inventory",
            ]
        )
    return "\n".join(lines)


def _iter_public_long_options(parser: argparse.ArgumentParser):
    for action in parser._actions:
        flags = [flag for flag in action.option_strings if flag.startswith("--")]
        if not flags or "--help" in flags or action.help == argparse.SUPPRESS:
            continue
        yield action, flags, max(flags, key=len)


def _registered_and_json_flags(
    diagnostic_entries: tuple[DiagnosticInventoryEntry, ...]
) -> tuple[set[str], set[str]]:
    registered_flags = {flag for entry in diagnostic_entries for flag in entry.cli_flags}
    json_flags = {
        flag
        for entry in diagnostic_entries
        if entry.supports_json
        for flag in entry.cli_flags
    }
    return registered_flags, json_flags


def _classification_for(flag: str, action: argparse.Action) -> tuple[str, str]:
    help_text = action.help or ""
    haystack = f"{flag} {help_text}".lower()
    action_type = type(action).__name__
    if "debug" in haystack:
        return "debug_surface", "argparse help exposes diagnostic/debug behavior"
    if flag in _MANUAL_INPUT_FLAGS or getattr(action, "nargs", None) in {2, 3}:
        return "manual_input", "accepts operator-provided evidence or values instead of exposing a standalone view"
    if flag in _MODIFIER_FLAGS:
        return "modifier", "argparse help and validation show this changes rendering or scope of another command"
    if any(hint in haystack for hint in _LEGACY_HINTS):
        return "legacy_surface", "implementation help or validation marks this as legacy behavior"
    if any(hint in haystack for hint in _FILTER_HINTS):
        return "filter", "argparse help constrains this option to limiting or selecting another command's output"
    category = _category_for(flag, help_text)
    if category and action_type in _PRIMARY_ACTIONS:
        return "primary_surface", "store_true operational flag owns a standalone CLI experience"
    if category and getattr(action, "nargs", None) in {"?", "*"}:
        return "primary_surface", "optional argument operational flag owns dispatch and may accept a query argument"
    if category:
        return "primary_surface", "operational keyword in argparse help indicates a standalone command path"
    return "unknown", "no operational, filter, modifier, debug, manual-input, or legacy evidence was found"


def _category_for(flag: str, help_text: str) -> str | None:
    haystack = f"{flag} {help_text}".lower()
    for keyword, category in _OPERATIONAL_KEYWORDS:
        if keyword in haystack:
            return category
    return None


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"
