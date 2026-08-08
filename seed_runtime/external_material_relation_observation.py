"""Read-only generic relation observation over an external-material structural projection.

The existing surface-feature projection measures how long lines are.  This
module measures how preserved representations stand to one another: which are
equal, which recur, which share a leading form, and which occur next to which.

Every finding is *enumerated from the material*, never tested against a
supplied candidate.  The observer is not asked "does `OBS. ` recur"; it reports
which representations recur, and `OBS. ` appears in the answer only if the
source put it there.  That direction matters: asking about a chosen form would
select the measurement to match material a developer already understood.

Findings are confined to those `01.External.E` permits a declared measurement
to produce -- exact equality, count, recurrence, prefix occurrence, and
adjacency.  The clause also requires a recurrence assertion to disclose the
representation measured, the rule by which equivalence or sameness was
determined, and the bounded scope within which occurrences were counted.  Those
three are carried on every observation as `representation_measured`,
`equivalence_rule`, and `counting_scope`.

Nothing here identifies headings, citations, definitions, sections, or grammar,
and nothing here interprets any representation.  A recurring form is a fact
about the artifact, not evidence that the form means anything.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any

from seed_runtime.external_material_structural_projection import (
    ExternalMaterialProjectedLine,
    ExternalMaterialStructuralProjection,
)

OBSERVATION_CONVENTION = "external_material_relation_observation_v1"

REPRESENTATION_MEASURED = (
    "the exact line text of each projected line, including its line terminator"
)
EQUIVALENCE_RULE = (
    "byte-for-byte equality of the exact preserved line text under the "
    "projection's declared encoding; no case, whitespace, punctuation, or "
    "Unicode normalization is applied"
)
COUNTING_SCOPE = (
    "the projected lines of one selected artifact within one manifest; "
    "occurrences outside that artifact are not counted and not claimed absent"
)

BOUNDARY_NOTES: tuple[str, ...] = (
    "Relation findings are deterministic measurements of an existing structural projection.",
    "Findings are enumerated from the material, not tested against supplied candidates.",
    "Recurrence establishes that a representation occurs more than once, nothing further.",
    "A shared prefix is a measured leading form, not a marker, label, heading, or kind.",
    "Adjacency is positional order within the artifact, not sequence, cause, or relation of meaning.",
    "Equal representations are not thereby the same subject, occurrence, or assertion.",
    "This observation does not identify headings, citations, definitions, rules, examples, or grammar.",
    "This observation is not runtime Evidence, Fact, candidate verification, or capability evidence.",
    "Counts are bounded by the counting scope and establish nothing about the wider source.",
)


class ExternalMaterialRelationObservationError(ValueError):
    """Raised when a relation observation cannot be produced."""


@dataclass(frozen=True)
class ExternalMaterialEqualityFinding:
    """One distinct representation and every projected line carrying it."""

    representation_hash: str
    representation: str
    character_count: int
    occurrence_count: int
    line_ids: tuple[str, ...]
    line_numbers: tuple[int, ...]
    is_blank: bool
    unknowns: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["line_ids"] = list(self.line_ids)
        data["line_numbers"] = list(self.line_numbers)
        data["unknowns"] = list(self.unknowns)
        return data


@dataclass(frozen=True)
class ExternalMaterialPrefixFinding:
    """One leading form shared by two or more distinct representations."""

    prefix: str
    prefix_character_count: int
    distinct_representation_count: int
    occurrence_count: int
    line_ids: tuple[str, ...]
    unknowns: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["line_ids"] = list(self.line_ids)
        data["unknowns"] = list(self.unknowns)
        return data


@dataclass(frozen=True)
class ExternalMaterialAdjacencyFinding:
    """One ordered pair of representations occurring on consecutive lines."""

    earlier_representation_hash: str
    later_representation_hash: str
    occurrence_count: int
    earlier_line_numbers: tuple[int, ...]
    unknowns: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["earlier_line_numbers"] = list(self.earlier_line_numbers)
        data["unknowns"] = list(self.unknowns)
        return data


@dataclass(frozen=True)
class ExternalMaterialRelationObservation:
    """Bounded relation findings over one structural projection."""

    manifest_id: str
    source_id: str
    artifact_id: str
    artifact_hash: str
    structural_projection_identity: str
    projected_line_count: int
    distinct_representation_count: int
    equality_findings: tuple[ExternalMaterialEqualityFinding, ...]
    recurring_representation_count: int
    prefix_findings: tuple[ExternalMaterialPrefixFinding, ...]
    adjacency_findings: tuple[ExternalMaterialAdjacencyFinding, ...]
    representation_measured: str = REPRESENTATION_MEASURED
    equivalence_rule: str = EQUIVALENCE_RULE
    counting_scope: str = COUNTING_SCOPE
    observation_unknowns: tuple[str, ...] = ()
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    observation_convention: str = OBSERVATION_CONVENTION

    def to_json_dict(self) -> dict[str, object]:
        return external_material_relation_observation_json(self)


def observe_external_material_relations(
    structural_projection: ExternalMaterialStructuralProjection,
) -> ExternalMaterialRelationObservation:
    """Enumerate equality, recurrence, prefix, and adjacency findings."""

    if structural_projection.projection_convention != "external_material_structural_projection_v1":
        raise ExternalMaterialRelationObservationError("unsupported_projection_convention")
    lines = structural_projection.lines
    equality = _equality_findings(lines)
    by_hash = {finding.representation_hash: finding for finding in equality}
    return ExternalMaterialRelationObservation(
        manifest_id=structural_projection.manifest_id,
        source_id=structural_projection.source_id,
        artifact_id=structural_projection.artifact_id,
        artifact_hash=structural_projection.artifact_hash,
        structural_projection_identity=_projection_identity(structural_projection),
        projected_line_count=len(lines),
        distinct_representation_count=len(equality),
        equality_findings=equality,
        recurring_representation_count=sum(
            1 for finding in equality if finding.occurrence_count > 1
        ),
        prefix_findings=_prefix_findings(equality),
        adjacency_findings=_adjacency_findings(lines, by_hash),
    )


def external_material_relation_observation_json(
    observation: ExternalMaterialRelationObservation,
) -> dict[str, object]:
    data = asdict(observation)
    data["equality_findings"] = [f.to_json_dict() for f in observation.equality_findings]
    data["prefix_findings"] = [f.to_json_dict() for f in observation.prefix_findings]
    data["adjacency_findings"] = [f.to_json_dict() for f in observation.adjacency_findings]
    data["observation_unknowns"] = list(observation.observation_unknowns)
    data["boundary_notes"] = list(observation.boundary_notes)
    return data


def format_external_material_relation_observation(
    observation: ExternalMaterialRelationObservation,
) -> str:
    """Render the observation for inspection without asserting anything further."""

    rows = [
        "External material relation observation",
        f"  artifact: {observation.artifact_id} ({observation.artifact_hash[:12]})",
        f"  projected lines: {observation.projected_line_count}",
        f"  distinct representations: {observation.distinct_representation_count}",
        f"  recurring representations: {observation.recurring_representation_count}",
        f"  representation measured: {observation.representation_measured}",
        f"  equivalence rule: {observation.equivalence_rule}",
        f"  counting scope: {observation.counting_scope}",
        "  recurrence findings:",
    ]
    for finding in observation.equality_findings:
        if finding.occurrence_count > 1:
            rows.append(
                f"    {finding.occurrence_count:>6}x  {finding.representation!r}"
            )
    rows.append("  shared leading forms:")
    for finding in observation.prefix_findings:
        rows.append(
            f"    {finding.occurrence_count:>6} lines  {finding.prefix!r}"
        )
    return "\n".join(rows) + "\n"


def _projection_identity(projection: ExternalMaterialStructuralProjection) -> str:
    material = "\x1f".join(
        (
            projection.manifest_id,
            projection.source_id,
            projection.artifact_id,
            projection.artifact_hash,
            projection.projection_convention,
            str(len(projection.lines)),
        )
    )
    return sha256(material.encode("utf-8")).hexdigest()


def _representation_hash(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _equality_findings(
    lines: tuple[ExternalMaterialProjectedLine, ...],
) -> tuple[ExternalMaterialEqualityFinding, ...]:
    grouped: dict[str, list[ExternalMaterialProjectedLine]] = {}
    for line in lines:
        grouped.setdefault(_representation_hash(line.text), []).append(line)
    findings = [
        ExternalMaterialEqualityFinding(
            representation_hash=digest,
            representation=members[0].text,
            character_count=members[0].character_count,
            occurrence_count=len(members),
            line_ids=tuple(m.line_id for m in members),
            line_numbers=tuple(m.line_number for m in members),
            is_blank=members[0].is_blank,
        )
        for digest, members in grouped.items()
    ]
    # Most-recurrent first, then by first appearance, so the ordering is a
    # property of the material rather than of dictionary insertion.
    findings.sort(key=lambda f: (-f.occurrence_count, f.line_numbers[0]))
    return tuple(findings)


def _prefix_findings(
    equality: tuple[ExternalMaterialEqualityFinding, ...],
) -> tuple[ExternalMaterialPrefixFinding, ...]:
    """Maximal leading forms shared by adjacent representations in sorted order.

    Sorting distinct representations places every pair sharing a leading form
    next to one another, so the longest common prefix of each adjacent pair
    enumerates the shared forms present without any prefix being proposed.
    """

    distinct = sorted(
        (f for f in equality if not f.is_blank), key=lambda f: f.representation
    )
    accumulated: dict[str, dict[str, Any]] = {}
    for earlier, later in zip(distinct, distinct[1:]):
        shared = _longest_common_prefix(earlier.representation, later.representation)
        if not shared.strip():
            continue
        entry = accumulated.setdefault(
            shared, {"representations": set(), "line_ids": [], "occurrences": 0}
        )
        for finding in (earlier, later):
            if finding.representation_hash in entry["representations"]:
                continue
            entry["representations"].add(finding.representation_hash)
            entry["line_ids"].extend(finding.line_ids)
            entry["occurrences"] += finding.occurrence_count
    findings = [
        ExternalMaterialPrefixFinding(
            prefix=prefix,
            prefix_character_count=len(prefix),
            distinct_representation_count=len(entry["representations"]),
            occurrence_count=entry["occurrences"],
            line_ids=tuple(entry["line_ids"]),
        )
        for prefix, entry in accumulated.items()
    ]
    findings.sort(key=lambda f: (-f.occurrence_count, -f.prefix_character_count, f.prefix))
    return tuple(findings)


def _longest_common_prefix(earlier: str, later: str) -> str:
    limit = min(len(earlier), len(later))
    index = 0
    while index < limit and earlier[index] == later[index]:
        index += 1
    return earlier[:index]


def _adjacency_findings(
    lines: tuple[ExternalMaterialProjectedLine, ...],
    by_hash: dict[str, ExternalMaterialEqualityFinding],
) -> tuple[ExternalMaterialAdjacencyFinding, ...]:
    grouped: dict[tuple[str, str], list[int]] = {}
    for earlier, later in zip(lines, lines[1:]):
        key = (_representation_hash(earlier.text), _representation_hash(later.text))
        grouped.setdefault(key, []).append(earlier.line_number)
    findings = [
        ExternalMaterialAdjacencyFinding(
            earlier_representation_hash=key[0],
            later_representation_hash=key[1],
            occurrence_count=len(numbers),
            earlier_line_numbers=tuple(numbers),
        )
        for key, numbers in grouped.items()
        if len(numbers) > 1
    ]
    findings.sort(key=lambda f: (-f.occurrence_count, f.earlier_line_numbers[0]))
    return tuple(findings)
