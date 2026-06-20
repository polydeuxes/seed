"""Implementation-backed inventory for operational CLI visibility surfaces."""

from __future__ import annotations

import argparse
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
    ("analysis", "analysis"),
    ("coverage", "analysis"),
)
_AUXILIARY_FLAGS = {"--json", "--record", "--mismatches", "--status"}


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
class VisibilityCoverageAudit:
    surfaces: tuple[OperationalSurface, ...]

    @property
    def discovered(self) -> int:
        return len(self.surfaces)

    @property
    def registered(self) -> int:
        return sum(surface.registered for surface in self.surfaces)

    @property
    def unregistered(self) -> tuple[OperationalSurface, ...]:
        return tuple(surface for surface in self.surfaces if not surface.registered)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "discovered": self.discovered,
            "registered": self.registered,
            "unregistered": [surface.to_json_dict() for surface in self.unregistered],
        }


def build_operational_surface_inventory(
    parser: argparse.ArgumentParser,
    *,
    diagnostic_entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> tuple[OperationalSurface, ...]:
    """Discover operational CLI surfaces from argparse declarations."""
    registered_flags = {
        flag for entry in diagnostic_entries for flag in entry.cli_flags
    }
    json_flags = {
        flag
        for entry in diagnostic_entries
        if entry.supports_json
        for flag in entry.cli_flags
    }
    surfaces: list[OperationalSurface] = []
    for action in parser._actions:
        flags = [flag for flag in action.option_strings if flag.startswith("--")]
        if not flags:
            continue
        primary = max(flags, key=len)
        if primary in _AUXILIARY_FLAGS or action.help == argparse.SUPPRESS:
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


def build_visibility_coverage_audit(
    parser: argparse.ArgumentParser,
    *,
    diagnostic_entries: tuple[DiagnosticInventoryEntry, ...] = DIAGNOSTIC_INVENTORY,
) -> VisibilityCoverageAudit:
    return VisibilityCoverageAudit(
        build_operational_surface_inventory(
            parser, diagnostic_entries=diagnostic_entries
        )
    )


def operational_surface_inventory_json(
    surfaces: tuple[OperationalSurface, ...],
) -> dict[str, Any]:
    return {"surfaces": [surface.to_json_dict() for surface in surfaces]}


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


def format_visibility_coverage_audit(audit: VisibilityCoverageAudit) -> str:
    lines = [
        "Visibility Coverage Audit",
        "",
        f"Discovered surfaces: {audit.discovered}",
        f"Registered surfaces: {audit.registered}",
        f"Unregistered surfaces: {len(audit.unregistered)}",
    ]
    if not audit.unregistered:
        lines.extend(
            [
                "",
                "All discovered operational surfaces are registered in diagnostic inventory.",
            ]
        )
        return "\n".join(lines)
    for surface in audit.unregistered:
        lines.extend(
            [
                "",
                "Surface:",
                f"  {surface.name}",
                "Status:",
                "  missing registration",
                "Impact:",
                "  invisible to diagnostic inventory",
            ]
        )
    return "\n".join(lines)


def _category_for(flag: str, help_text: str) -> str | None:
    haystack = f"{flag} {help_text}".lower()
    for keyword, category in _OPERATIONAL_KEYWORDS:
        if keyword in haystack:
            return category
    return None


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"
