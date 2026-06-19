"""Read-only diagnostics for projected entity classification coverage."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from seed_runtime.state import GraphValidationIssue, State

UNKNOWN_EXAMPLE_LIMIT = 3
TOP_UNKNOWN_LIMIT = 10

CLASSIFICATION_ORDER = [
    "host",
    "service",
    "group",
    "endpoint",
    "monitoring_system",
    "capability",
    "document",
    "concept",
    "domain",
    "unknown",
]


@dataclass(frozen=True)
class ClassificationCoverageDiagnostic:
    diagnostic_name: str
    observed_at: datetime
    projection_version: str
    last_event_id: str | None
    entity_count: int
    classified_entity_count: int
    unknown_entity_count: int
    unknown_percentage: float
    classification_distribution: dict[str, int]
    unknown_subject_graph_issue_count: int
    unknown_object_graph_issue_count: int
    both_unknown_graph_issue_count: int
    concrete_mismatch_graph_issue_count: int
    catalog_type_counts: dict[str, int]
    top_unknown_predicates: list[tuple[str, int]] = field(default_factory=list)
    unknown_predicate_examples: dict[str, list[str]] = field(default_factory=dict)
    top_unknown_relationship_categories: list[tuple[str, int]] = field(
        default_factory=list
    )
    top_unknown_graph_issue_categories: list[tuple[str, int]] = field(
        default_factory=list
    )

    def record_facts(self) -> dict[str, Any]:
        """Return bounded facts suitable for self-observation evidence."""

        return {
            "diagnostic name": self.diagnostic_name,
            "diagnostic observed_at": self.observed_at.isoformat(),
            "projection version": self.projection_version,
            "last event id": self.last_event_id,
            "entity count": self.entity_count,
            "classified entity count": self.classified_entity_count,
            "unknown entity count": self.unknown_entity_count,
            "unknown percentage": self.unknown_percentage,
            "unknown-subject graph issue count": self.unknown_subject_graph_issue_count,
            "unknown-object graph issue count": self.unknown_object_graph_issue_count,
            "both-unknown graph issue count": self.both_unknown_graph_issue_count,
            "concrete-mismatch graph issue count": self.concrete_mismatch_graph_issue_count,
            "top unknown predicate examples": {
                predicate: examples
                for predicate, examples in self.unknown_predicate_examples.items()
            },
        }


def build_classification_coverage_diagnostic(
    state: State, *, observed_at: datetime | None = None
) -> ClassificationCoverageDiagnostic:
    """Build a non-mutating entity-classification diagnostic from projected State."""

    observed_at = observed_at or datetime.now(timezone.utc)
    current_types = state.current_entity_types
    entity_count = len(current_types)
    classification_distribution = {name: 0 for name in CLASSIFICATION_ORDER}
    catalog_type_counts: Counter[str] = Counter()
    classified_entity_count = 0
    unknown_entity_count = 0

    for entity_types in current_types.values():
        if entity_types == ["unknown"]:
            unknown_entity_count += 1
            classification_distribution["unknown"] += 1
        else:
            classified_entity_count += 1
            for entity_type in entity_types:
                classification_distribution.setdefault(entity_type, 0)
                classification_distribution[entity_type] += 1
        for entity_type in entity_types:
            catalog_type_counts[entity_type] += 1

    unknown_entities = {
        entity_id
        for entity_id, entity_types in current_types.items()
        if entity_types == ["unknown"]
    }
    issues = state.get_graph_issues()
    unknown_subject_issues = [
        issue for issue in issues if _issue_subject_unknown(issue, unknown_entities)
    ]
    unknown_object_issues = [
        issue for issue in issues if _issue_object_unknown(issue, unknown_entities)
    ]
    both_unknown_issues = [
        issue
        for issue in issues
        if _issue_subject_unknown(issue, unknown_entities)
        and _issue_object_unknown(issue, unknown_entities)
    ]
    concrete_mismatch_issues = [
        issue
        for issue in issues
        if not _issue_subject_unknown(issue, unknown_entities)
        and not _issue_object_unknown(issue, unknown_entities)
    ]

    unknown_predicates: Counter[str] = Counter()
    unknown_predicate_example_sets: dict[str, set[str]] = {}
    for fact in state.facts.values():
        value = fact.value if isinstance(fact.value, str) else None
        examples: list[str] = []
        if fact.subject_id in unknown_entities:
            examples.append(fact.subject_id)
        if value in unknown_entities:
            examples.append(value)
        if examples:
            unknown_predicates[fact.predicate] += 1
            unknown_predicate_example_sets.setdefault(fact.predicate, set()).update(
                examples
            )

    relationship_categories: Counter[str] = Counter()
    for relationship in state.relationships:
        if (
            relationship.subject in unknown_entities
            or relationship.object in unknown_entities
        ):
            relationship_categories[str(relationship.relationship_kind)] += 1

    issue_categories: Counter[str] = Counter()
    for issue in unknown_subject_issues + unknown_object_issues:
        issue_categories[
            f"{issue.severity} | {issue.relationship} | {issue.reason}"
        ] += 1

    unknown_percentage = (
        (unknown_entity_count / entity_count * 100.0) if entity_count else 0.0
    )
    return ClassificationCoverageDiagnostic(
        diagnostic_name="entity_classification_coverage",
        observed_at=observed_at,
        projection_version=state.projection_version,
        last_event_id=state.last_event_id,
        entity_count=entity_count,
        classified_entity_count=classified_entity_count,
        unknown_entity_count=unknown_entity_count,
        unknown_percentage=unknown_percentage,
        classification_distribution=classification_distribution,
        unknown_subject_graph_issue_count=len(unknown_subject_issues),
        unknown_object_graph_issue_count=len(unknown_object_issues),
        both_unknown_graph_issue_count=len(both_unknown_issues),
        concrete_mismatch_graph_issue_count=len(concrete_mismatch_issues),
        catalog_type_counts=dict(sorted(catalog_type_counts.items())),
        top_unknown_predicates=_top_counter_items(unknown_predicates),
        unknown_predicate_examples={
            predicate: sorted(unknown_predicate_example_sets.get(predicate, ()))[
                :UNKNOWN_EXAMPLE_LIMIT
            ]
            for predicate, _count in _top_counter_items(unknown_predicates)
        },
        top_unknown_relationship_categories=_top_counter_items(relationship_categories),
        top_unknown_graph_issue_categories=_top_counter_items(issue_categories),
    )


def format_classification_coverage(diagnostic: ClassificationCoverageDiagnostic) -> str:
    """Format the classification coverage diagnostic for CLI inspection."""

    lines = [
        "Entity Classification Coverage",
        "",
        "Totals:",
        f"  entities: {diagnostic.entity_count}",
        f"  classified entities: {diagnostic.classified_entity_count}",
        f"  unknown entities: {diagnostic.unknown_entity_count}",
        f"  unknown percentage: {diagnostic.unknown_percentage:.1f}%",
        "",
        "Classification distribution:",
    ]
    for entity_type in CLASSIFICATION_ORDER:
        lines.append(
            f"  {entity_type}: {diagnostic.classification_distribution.get(entity_type, 0)}"
        )
    lines.extend(
        [
            "",
            "Graph issue impact:",
            f"  issues involving unknown subject: {diagnostic.unknown_subject_graph_issue_count}",
            f"  issues involving unknown object: {diagnostic.unknown_object_graph_issue_count}",
            f"  issues involving both unknown: {diagnostic.both_unknown_graph_issue_count}",
            f"  issues involving concrete type mismatch: {diagnostic.concrete_mismatch_graph_issue_count}",
            "",
            "Coverage visibility:",
            "  catalog type | assigned count",
        ]
    )
    if diagnostic.catalog_type_counts:
        for entity_type, count in diagnostic.catalog_type_counts.items():
            lines.append(f"  {entity_type}: {count}")
    else:
        lines.append("  none: 0")
    lines.extend(
        [
            "",
            "Unknown contributor visibility:",
            "  top predicates involving unknown entities:",
        ]
    )
    _append_predicate_lines(
        lines, diagnostic.top_unknown_predicates, diagnostic.unknown_predicate_examples
    )
    lines.append("  top relationship categories involving unknown entities:")
    _append_counter_lines(lines, diagnostic.top_unknown_relationship_categories)
    lines.append("  top graph issue categories involving unknown entities:")
    _append_counter_lines(lines, diagnostic.top_unknown_graph_issue_categories)
    return "\n".join(lines)


def _top_counter_items(counter: Counter[str]) -> list[tuple[str, int]]:
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[
        :TOP_UNKNOWN_LIMIT
    ]


def _append_predicate_lines(
    lines: list[str],
    items: list[tuple[str, int]],
    examples_by_predicate: dict[str, list[str]],
) -> None:
    if not items:
        lines.append("    none: 0")
        return
    for name, count in items:
        lines.append(f"    {name}: {count}")
        examples = examples_by_predicate.get(name, [])[:UNKNOWN_EXAMPLE_LIMIT]
        if examples:
            lines.append("      examples:")
            for example in examples:
                lines.append(f"        - {example}")


def _append_counter_lines(lines: list[str], items: list[tuple[str, int]]) -> None:
    if not items:
        lines.append("    none: 0")
        return
    for name, count in items:
        lines.append(f"    {name}: {count}")


def _issue_subject_unknown(
    issue: GraphValidationIssue, unknown_entities: set[str]
) -> bool:
    return "unknown" in issue.actual_subject_types or issue.subject in unknown_entities


def _issue_object_unknown(
    issue: GraphValidationIssue, unknown_entities: set[str]
) -> bool:
    return "unknown" in issue.actual_object_types or issue.object in unknown_entities
