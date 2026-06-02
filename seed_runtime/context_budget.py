"""Priority-based context selection for model-visible packets.

The budget deliberately does not estimate tokens. It answers a simpler runtime
question: when state grows, which categories are allowed into the next model
context first?
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence, TypeVar

T = TypeVar("T")

CURRENT_INPUT = "current_input"
ACTIVE_GOALS = "active_goals"
OPEN_TOOL_NEEDS = "open_tool_needs"
RECENT_FACTS = "recent_facts"
RECENT_EVIDENCE = "recent_evidence"
ENTITIES = "entities"
HISTORICAL_EVENTS = "historical_events"

DEFAULT_SECTION_PRIORITIES: dict[str, int] = {
    CURRENT_INPUT: 100,
    ACTIVE_GOALS: 90,
    OPEN_TOOL_NEEDS: 80,
    RECENT_FACTS: 70,
    RECENT_EVIDENCE: 60,
    ENTITIES: 50,
    HISTORICAL_EVENTS: 20,
}

DEFAULT_SECTION_LIMITS: dict[str, int | None] = {
    CURRENT_INPUT: 1,
    ACTIVE_GOALS: 1,
    OPEN_TOOL_NEEDS: None,
    RECENT_FACTS: 30,
    RECENT_EVIDENCE: 30,
    ENTITIES: 20,
    HISTORICAL_EVENTS: 20,
}


@dataclass(frozen=True)
class BudgetTrace:
    """Inspectable accounting for a context budget pass."""

    priorities: dict[str, int]
    section_limits: dict[str, int | None]
    max_items: int | None
    selected_counts: dict[str, int]
    dropped_counts: dict[str, int]
    section_order: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "priorities": self.priorities.copy(),
            "section_limits": self.section_limits.copy(),
            "max_items": self.max_items,
            "selected_counts": self.selected_counts.copy(),
            "dropped_counts": self.dropped_counts.copy(),
            "section_order": list(self.section_order),
        }


@dataclass(frozen=True)
class BudgetedContext:
    """Selected context sections plus trace metadata."""

    sections: dict[str, list[Any]]
    trace: BudgetTrace


@dataclass(frozen=True)
class ContextBudget:
    """Select context items by section priority instead of token estimates.

    ``max_items`` is an optional global cap across all budgeted sections. When it
    is set, higher-priority sections fill the packet first. ``section_limits``
    keeps any one state category from growing without bound even when no global
    cap is configured.
    """

    max_items: int | None = None
    priorities: Mapping[str, int] = field(default_factory=dict)
    section_limits: Mapping[str, int | None] = field(default_factory=dict)

    def priority_for(self, section: str) -> int:
        return int(
            self.priorities.get(section, DEFAULT_SECTION_PRIORITIES.get(section, 0))
        )

    def limit_for(self, section: str) -> int | None:
        if section in self.section_limits:
            return self.section_limits[section]
        return DEFAULT_SECTION_LIMITS.get(section)

    def select_sections(self, sections: Mapping[str, Sequence[T]]) -> BudgetedContext:
        """Return selected items for every input section.

        Items must already be ordered from most to least useful inside their
        section; this class only applies per-section limits and cross-section
        priorities.
        """
        ordered_names = sorted(
            sections,
            key=lambda name: (-self.priority_for(name), name),
        )
        remaining = self.max_items
        selected: dict[str, list[Any]] = {name: [] for name in sections}
        selected_counts: dict[str, int] = {}
        dropped_counts: dict[str, int] = {}

        for name in ordered_names:
            items = list(sections[name])
            section_limit = self.limit_for(name)
            allowed = (
                len(items)
                if section_limit is None
                else min(len(items), section_limit)
            )
            if remaining is not None:
                allowed = min(allowed, max(remaining, 0))
            selected[name] = items[:allowed]
            selected_counts[name] = allowed
            dropped_counts[name] = len(items) - allowed
            if remaining is not None:
                remaining -= allowed

        effective_priorities = {name: self.priority_for(name) for name in sections}
        effective_limits = {name: self.limit_for(name) for name in sections}
        return BudgetedContext(
            sections=selected,
            trace=BudgetTrace(
                priorities=effective_priorities,
                section_limits=effective_limits,
                max_items=self.max_items,
                selected_counts=selected_counts,
                dropped_counts=dropped_counts,
                section_order=ordered_names,
            ),
        )
