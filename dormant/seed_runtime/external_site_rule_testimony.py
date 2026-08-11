"""Caller-supplied external site-rule testimony preservation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

BOUNDARY_NOTES: tuple[str, ...] = (
    "External site rules are preserved as attributed testimony, not Seed authority.",
    "Each testimony retains its independent source and claimed scope.",
    "The testimony set does not determine permission, prohibition, applicability, or precedence.",
    "Site-reported permission does not grant Seed authorization.",
    "Absence of prohibition is not permission.",
    "robots.txt is not treated as complete site policy.",
    "Possible consistency or conflict is preserved without resolution.",
    "This artifact does not select or authorize external movement.",
)

DISALLOWED_INTERPRETATION_STATUSES: frozenset[str] = frozenset(
    {
        "authorized",
        "permitted",
        "prohibited",
        "applicable",
        "binding",
        "overrides",
        "safe_to_execute",
    }
)


class ExternalSiteRuleTestimonyValidationError(ValueError):
    """Structural validation failure for caller-supplied site-rule testimony."""


@dataclass(frozen=True)
class ExternalSiteRuleTestimonyInputTestimony:
    testimony_id: str
    source_url: str
    acquired_at: str
    content_hash: str
    bounded_rule_text: str
    claimed_scope: str
    rule_kind: str
    discovery_route: str
    operator_supplied_seed: bool
    interpretation_status: str
    unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalSiteRuleTestimonyInputTestimony":
        return cls(
            testimony_id=_required_str(data, "testimony_id"),
            source_url=_required_str(data, "source_url"),
            acquired_at=_required_str(data, "acquired_at"),
            content_hash=_required_str(data, "content_hash"),
            bounded_rule_text=_required_str(data, "bounded_rule_text"),
            claimed_scope=_required_str(data, "claimed_scope"),
            rule_kind=_required_str(data, "rule_kind"),
            discovery_route=_required_str(data, "discovery_route"),
            operator_supplied_seed=_required_bool(data, "operator_supplied_seed"),
            interpretation_status=_required_str(data, "interpretation_status"),
            unknowns=_str_tuple(data.get("unknowns", ()), "unknowns"),
        )

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["unknowns"] = list(self.unknowns)
        return data


@dataclass(frozen=True)
class ExternalSiteRuleTestimonyInput:
    site_scope: str
    testimonies: tuple[ExternalSiteRuleTestimonyInputTestimony, ...] = ()
    set_unknowns: tuple[str, ...] = ()

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "ExternalSiteRuleTestimonyInput":
        raw_testimonies = data.get("testimonies", ())
        if not isinstance(raw_testimonies, list):
            raise ExternalSiteRuleTestimonyValidationError("testimonies must be a list")
        return cls(
            site_scope=_required_str(data, "site_scope"),
            testimonies=tuple(
                ExternalSiteRuleTestimonyInputTestimony.from_json_dict(testimony)
                for testimony in raw_testimonies
            ),
            set_unknowns=_str_tuple(data.get("set_unknowns", ()), "set_unknowns"),
        )


@dataclass(frozen=True)
class ExternalSiteRuleTestimonySet:
    site_scope: str
    testimonies: tuple[ExternalSiteRuleTestimonyInputTestimony, ...]
    set_unknowns: tuple[str, ...]
    boundary_notes: tuple[str, ...]
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, object]:
        return {
            "artifact_type": "ExternalSiteRuleTestimonySet",
            "site_scope": self.site_scope,
            "testimonies": [testimony.to_json_dict() for testimony in self.testimonies],
            "set_unknowns": list(self.set_unknowns),
            "boundary_notes": list(self.boundary_notes),
            "read_only": self.read_only,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


def assemble_external_site_rule_testimony_set(
    supplied: ExternalSiteRuleTestimonyInput,
) -> ExternalSiteRuleTestimonySet:
    seen: set[str] = set()
    for testimony in supplied.testimonies:
        if testimony.testimony_id in seen:
            raise ExternalSiteRuleTestimonyValidationError(
                f"duplicate testimony_id: {testimony.testimony_id}"
            )
        seen.add(testimony.testimony_id)
        if testimony.interpretation_status in DISALLOWED_INTERPRETATION_STATUSES:
            raise ExternalSiteRuleTestimonyValidationError(
                f"interpretation_status is a Seed verdict, not testimony preservation: {testimony.interpretation_status}"
            )
    return ExternalSiteRuleTestimonySet(
        site_scope=supplied.site_scope,
        testimonies=supplied.testimonies,
        set_unknowns=supplied.set_unknowns,
        boundary_notes=BOUNDARY_NOTES,
    )


def external_site_rule_testimony_json(artifact: ExternalSiteRuleTestimonySet) -> dict[str, object]:
    return artifact.to_json_dict()


def format_external_site_rule_testimony(artifact: ExternalSiteRuleTestimonySet) -> str:
    lines = [
        "External Site Rule Testimony Set",
        f"site_scope: {artifact.site_scope}",
        f"read_only: {str(artifact.read_only).lower()}",
        f"writes_event_ledger: {str(artifact.writes_event_ledger).lower()}",
        f"mutates_cluster: {str(artifact.mutates_cluster).lower()}",
        "boundary_notes:",
    ]
    lines.extend(f"- {note}" for note in artifact.boundary_notes)
    lines.append("set_unknowns:")
    lines.extend(f"- {unknown}" for unknown in artifact.set_unknowns)
    if not artifact.set_unknowns:
        lines.append("- none supplied")
    lines.append("testimonies:")
    if not artifact.testimonies:
        lines.append("- none supplied (zero-testimony set, not failure)")
    for testimony in artifact.testimonies:
        lines.extend(
            [
                f"- testimony_id: {testimony.testimony_id}",
                f"  source_url: {testimony.source_url}",
                f"  acquired_at: {testimony.acquired_at}",
                f"  content_hash: {testimony.content_hash}",
                f"  bounded_rule_text: {testimony.bounded_rule_text}",
                f"  claimed_scope: {testimony.claimed_scope}",
                f"  rule_kind: {testimony.rule_kind}",
                f"  discovery_route: {testimony.discovery_route}",
                f"  operator_supplied_seed: {str(testimony.operator_supplied_seed).lower()}",
                f"  interpretation_status: {testimony.interpretation_status}",
                f"  unknowns: {_joined(testimony.unknowns)}",
            ]
        )
    return "\n".join(lines)


def _joined(values: tuple[str, ...]) -> str:
    return ", ".join(values) if values else "none supplied"


def _required_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ExternalSiteRuleTestimonyValidationError(f"{key} is required")
    return value


def _required_bool(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        raise ExternalSiteRuleTestimonyValidationError(f"{key} must be a boolean")
    return value


def _str_tuple(value: Any, key: str) -> tuple[str, ...]:
    if not isinstance(value, list | tuple):
        raise ExternalSiteRuleTestimonyValidationError(f"{key} must be a list")
    if not all(isinstance(item, str) for item in value):
        raise ExternalSiteRuleTestimonyValidationError(f"{key} entries must be strings")
    return tuple(value)
