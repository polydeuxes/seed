"""Read-only preservation of language-derived candidate requests.

This module intentionally stops at candidate-request preservation. It does not
select capabilities, build runtime Decisions, evaluate policy, or execute tools.
"""

from __future__ import annotations

import re
from importlib.util import find_spec
from typing import Literal

from seed_runtime.base import SeedModel

if find_spec("pydantic") is not None:
    from pydantic import Field
else:
    from seed_runtime._pydantic_compat import Field

CandidateConfidence = Literal["low", "medium", "high"]


class CandidateRequest(SeedModel):
    """A possible operator request preserved before routing or execution."""

    label: str
    confidence: CandidateConfidence
    target_boundary: str
    rationale: str


class CandidateRequestInspection(SeedModel):
    """Read-only inspection result for language-derived candidate requests."""

    raw_text: str
    candidates: list[CandidateRequest] = Field(default_factory=list)
    ambiguity: bool
    boundary: str = "candidate_request_preservation_only"
    notes: list[str] = Field(default_factory=list)


_SUMMARY_SURFACES: tuple[tuple[str, str], ...] = (
    ("state summary", "state-summary read-only inspection surface"),
    ("integrity summary", "projection-integrity read-only inspection surface"),
    ("impact summary", "entity-impact read-only inspection surface"),
)
_STATE_SUMMARY_PATTERN = re.compile(
    r"\b(?:show|display|summarize|summary|give|print)\b.*\bstate\s+summary\b|\bstate\s+summary\b",
    re.IGNORECASE,
)
_GENERIC_SUMMARY_PATTERN = re.compile(
    r"\b(?:show|display|give|print|summarize)\b.*\bsummary\b|^\s*summary\s*$",
    re.IGNORECASE,
)


def inspect_candidate_requests(text: str) -> CandidateRequestInspection:
    """Preserve candidate requests for operator inspection without execution.

    The intentionally small first slice recognizes summary-shaped language only.
    Unknown language is preserved as an unresolved low-confidence candidate rather
    than promoted to a command, capability, Decision, policy check, or tool call.
    """

    raw_text = text
    normalized = " ".join(text.strip().lower().split())
    notes = [
        "candidate_request_not_command",
        "candidate_request_not_capability",
        "candidate_request_not_execution_decision",
        "no_capability_selection",
        "no_policy_execution",
        "no_tool_execution",
    ]

    if _STATE_SUMMARY_PATTERN.search(normalized):
        return CandidateRequestInspection(
            raw_text=raw_text,
            candidates=[
                CandidateRequest(
                    label="state summary",
                    confidence="high",
                    target_boundary="state-summary read-only inspection surface",
                    rationale="explicit state summary wording",
                )
            ],
            ambiguity=False,
            notes=notes,
        )

    if _GENERIC_SUMMARY_PATTERN.search(normalized):
        candidates = [
            CandidateRequest(
                label=label,
                confidence="medium",
                target_boundary=target_boundary,
                rationale="generic summary wording leaves summary target unresolved",
            )
            for label, target_boundary in _SUMMARY_SURFACES
        ]
        return CandidateRequestInspection(
            raw_text=raw_text,
            candidates=candidates,
            ambiguity=True,
            notes=[*notes, "ambiguity_preserved_not_failure"],
        )

    return CandidateRequestInspection(
        raw_text=raw_text,
        candidates=[
            CandidateRequest(
                label=normalized or "unresolved request",
                confidence="low",
                target_boundary="unresolved language-request boundary",
                rationale="no high-confidence candidate rule matched",
            )
        ],
        ambiguity=True,
        notes=[*notes, "clarification_possible_not_rejection"],
    )
