"""Shared recommendation enrichment for tool needs."""

from __future__ import annotations

from seed_runtime.capability_catalog import CapabilityCatalog
from seed_runtime.models import ToolNeed
from seed_runtime.recommendation_ranker import RankedRecommendation, RecommendationRanker
from seed_runtime.state import State


class ToolRecommendationService:
    """Look up and rank catalog recommendations for a tool need.

    The service is intentionally read-only: it uses the capability catalog and
    ranker to produce the same enriched recommendation data Runtime historically
    returned without creating providers, registering tools, or mutating state.
    """

    def __init__(
        self,
        capability_catalog: CapabilityCatalog | None = None,
        recommendation_ranker: RecommendationRanker | None = None,
    ) -> None:
        self.capability_catalog = capability_catalog or CapabilityCatalog.load()
        self.recommendation_ranker = recommendation_ranker or RecommendationRanker()

    def recommend_for(
        self, tool_need: ToolNeed, state: State
    ) -> list[RankedRecommendation]:
        """Return ranked recommendations for ``tool_need`` against projected state."""
        return self.recommendation_ranker.rank(
            tool_need.capability,
            self.capability_catalog.recommend_for(tool_need),
            state,
        )
