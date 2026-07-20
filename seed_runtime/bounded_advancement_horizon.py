"""Read-only bounded advancement horizon construction.

A horizon preserves a caller-supplied present movement boundary for one bounded
goal whose identity has been resolved against a visible inventory snapshot. It
does not select the goal, classify needs, judge sufficiency, choose a next step,
authorize work, execute, record, or mutate state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Iterable, Literal

from seed_runtime.bounded_operator_goal_establishment import (
    BoundedOperatorGoalEstablishment,
)
from seed_runtime.goal_consideration_candidate_resolution import (
    GoalConsiderationCandidateResolution,
)

HorizonState = Literal["bounded", "refused"]
RefusalReason = Literal[
    "candidate_not_resolved",
    "goal_artifact_identity_mismatch",
    "goal_artifact_not_established",
    "missing_present_movement_boundary",
    "excluded_need_family_missing_reason",
]

NEED_CLASSIFICATION_FIELDS: tuple[str, ...] = (
    "clarification_need",
    "inquiry_need",
    "authority_need",
    "operational_realization_need",
    "sufficient_for_now",
    "selected_next_action",
)

BOUNDARY_NOTES: tuple[str, ...] = (
    "BoundedAdvancementHorizon is not the goal itself.",
    "Resolved candidate identity is not Seed-owned goal selection, constitutional focus, priority, or advancement.",
    "BoundedAdvancementHorizon preserves a supplied movement boundary; it does not produce that boundary's constitutional standing.",
    "Included need family means potentially relevant to preserve, not that a need exists.",
    "Excluded need families must carry explicit reasons.",
    "The horizon is read-only and does not open inquiry, authorize, execute, record, or mutate state.",
)


@dataclass(frozen=True)
class NeedFamilyExclusion:
    need_family: str
    reason: str


@dataclass(frozen=True)
