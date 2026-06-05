"""RuntimeLoop request_tool decision handling."""

from __future__ import annotations

from typing import TYPE_CHECKING

from seed_runtime.decision_journal import DecisionJournal
from seed_runtime.events import EventLedger
from seed_runtime.ids import new_id
from seed_runtime.models import ToolNeed
from seed_runtime.projection_store import ProjectionStore, project_state_with_cache
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.tool_needs import slugify
from seed_runtime.tool_recommendations import ToolRecommendationService

if TYPE_CHECKING:
    from seed_runtime.runtime_loop import Decision, RuntimeInput, RuntimeResult


class RuntimeLoopToolRequestHandler:
    """Handle validated RuntimeLoop ``request_tool`` decisions.

    The handler owns the request-tool side effects and RuntimeResult shaping that
    used to live directly in RuntimeLoop. It intentionally preserves the exact
    event payloads and result fields for thin-runtime extraction only.
    """

    def __init__(
        self,
        *,
        ledger: EventLedger,
        decision_journal: DecisionJournal,
        tool_recommendation_service: ToolRecommendationService,
        projection_store: ProjectionStore | None,
        projector: StateProjector,
    ) -> None:
        self.ledger = ledger
        self.decision_journal = decision_journal
        self.tool_recommendation_service = tool_recommendation_service
        self.projection_store = projection_store
        self.projector = projector

    def handle(
        self,
        *,
        runtime_input: RuntimeInput,
        run_id: str,
        input_event_id: str,
        context_hash: str,
        decision: Decision,
        events_appended: list[str],
    ) -> RuntimeResult:
        """Record a tool need, enrich recommendations, journal, and return result."""
        from seed_runtime.runtime_loop import RuntimeResult

        tool_need = self.build_tool_need(
            runtime_input.workspace_id, decision, input_event_id
        )
        need_event = self.ledger.append(
            "tool_need.created",
            runtime_input.workspace_id,
            {"tool_need": to_plain(tool_need)},
            actor="system",
            causation_id=input_event_id,
        )
        events_appended.append(need_event.id)
        recommendation_state, _cache_status = project_state_with_cache(
            self.ledger,
            runtime_input.workspace_id,
            self.projection_store,
            projector=self.projector,
        )
        recommendations = [
            {
                "provider": recommendation.provider,
                "score": recommendation.score,
                "reasons": list(recommendation.reasons),
            }
            for recommendation in self.tool_recommendation_service.recommend_for(
                tool_need, recommendation_state
            )
        ]
        journal_event = self.decision_journal.append_record(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            decision_kind="request_tool",
            reason=decision.reason,
            context_hash=context_hash,
            policy_allowed=True,
            outcome="tool_requested",
            causation_id=need_event.id,
            correlation_id=input_event_id,
        )
        events_appended.append(journal_event.id)
        record = journal_event.payload["record"]
        return RuntimeResult(
            workspace_id=runtime_input.workspace_id,
            run_id=run_id,
            decision_kind="request_tool",
            response_text=f"Recorded tool need {tool_need.name}.",
            events_appended=events_appended,
            policy_allowed=True,
            error=None,
            decision_id=record["decision_id"],
            context_hash=context_hash,
            decision_reason=decision.reason,
            decision_outcome="tool_requested",
            recommendations=recommendations,
        )

    def build_tool_need(
        self, workspace_id: str, decision: Decision, requested_by_event_id: str
    ) -> ToolNeed:
        """Build a ToolNeed from the validated RuntimeLoop decision payload."""
        payload = decision.tool_need or {}
        name = slugify(str(payload["name"]))
        capability = slugify(str(payload["capability"]))
        return ToolNeed(
            id=new_id("need"),
            workspace_id=workspace_id,
            name=name,
            summary=str(payload["summary"]),
            capability=capability,
            reason=decision.reason,
            requested_by_event_id=requested_by_event_id,
            risk_hint=payload.get("risk_hint"),
            desired_inputs=list(payload.get("desired_inputs", [])),
            desired_outputs=list(payload.get("desired_outputs", [])),
        )
