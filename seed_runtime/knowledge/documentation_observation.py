"""Deterministic documentation claim extraction helpers.

This module intentionally works only on caller-provided text. It does not read
files, inspect the repository, parse markdown beyond simple headings/lines, use
LLMs, or integrate with runtime/tool execution.
"""

from __future__ import annotations

import re

from seed_runtime.knowledge.self_model_alignment import (
    FRONTIER,
    OWNERSHIP,
    REJECTED_CONCEPT,
    DocumentationClaim,
)


_HEADING_RE = re.compile(r"^#{1,6}\s+(?P<heading>.*?)\s*#*\s*$")
_BULLET_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)(?P<text>.*)$")
_CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_OWNERSHIP_RE = re.compile(r"\b(?:owns?|owner)\b", re.IGNORECASE)
_REJECTED_RE = re.compile(r"\bis rejected\.?$", re.IGNORECASE)
_DO_NOT_ADD_RE = re.compile(r"^do not add\s+(?P<concepts>.+?)\.?$", re.IGNORECASE)
_DOES_NOT_RECOMMEND_OR_INTRODUCE_RE = re.compile(
    r"\bdoes not recommend or introduce\s+(?P<concepts>.+?)\.?$",
    re.IGNORECASE,
)
_FRONTIER_RE = re.compile(
    r"\b(?:active capability frontier|current capability-growth priority|current frontier|active frontier)\b",
    re.IGNORECASE,
)
_ACTIVE_CAPABILITY_FRONTIER_RE = re.compile(
    r"^(?P<subject>.+?)\s+[—-]\s+active capability frontier\.?$",
    re.IGNORECASE,
)


def extract_documentation_claims(
    source_path: str,
    text: str,
) -> list[DocumentationClaim]:
    """Extract explicit documentation claims from caller-provided markdown text.

    Extraction is intentionally tiny and deterministic. It tracks simple markdown
    headings, skips fenced code blocks, and recognizes only v0 ownership,
    rejected-concept, and frontier claim families.
    """

    claims: list[DocumentationClaim] = []
    current_heading: str | None = None
    in_code_fence = False

    for raw_line in text.splitlines():
        if _CODE_FENCE_RE.match(raw_line):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        heading_match = _HEADING_RE.match(raw_line)
        if heading_match is not None:
            current_heading = heading_match.group("heading").strip()
            continue

        line = _claim_line_text(raw_line)
        if not line:
            continue

        claims.extend(_claims_from_line(source_path, current_heading, line))

    return claims


def _claim_line_text(raw_line: str) -> str:
    line = raw_line.strip()
    bullet_match = _BULLET_RE.match(line)
    if bullet_match is not None:
        line = bullet_match.group("text").strip()
    return _normalize_inline_text(line)


def _normalize_inline_text(line: str) -> str:
    line = line.strip()
    line = line.replace("`", "")
    return re.sub(r"\s+", " ", line)


def _claims_from_line(
    source_path: str,
    source_heading: str | None,
    line: str,
) -> list[DocumentationClaim]:
    if _is_ownership_claim(line):
        return [_claim(source_path, source_heading, line, OWNERSHIP)]

    rejected_claims = _rejected_concept_claims(source_path, source_heading, line)
    if rejected_claims:
        return rejected_claims

    frontier_claim = _frontier_claim(source_path, source_heading, line)
    if frontier_claim is not None:
        return [frontier_claim]

    return []


def _is_ownership_claim(line: str) -> bool:
    return _OWNERSHIP_RE.search(line) is not None


def _rejected_concept_claims(
    source_path: str,
    source_heading: str | None,
    line: str,
) -> list[DocumentationClaim]:
    if _REJECTED_RE.search(line):
        return [_claim(source_path, source_heading, line, REJECTED_CONCEPT)]

    do_not_add_match = _DO_NOT_ADD_RE.match(line)
    if do_not_add_match is not None:
        return [
            _claim(source_path, source_heading, f"{concept} is rejected.", REJECTED_CONCEPT)
            for concept in _split_concepts(do_not_add_match.group("concepts"))
        ]

    does_not_recommend_match = _DOES_NOT_RECOMMEND_OR_INTRODUCE_RE.search(line)
    if does_not_recommend_match is not None:
        return [
            _claim(source_path, source_heading, f"{concept} is rejected.", REJECTED_CONCEPT)
            for concept in _split_concepts(does_not_recommend_match.group("concepts"))
        ]

    return []


def _split_concepts(concepts_text: str) -> list[str]:
    concepts_text = concepts_text.strip().rstrip(".")
    concepts_text = re.sub(r"\bor\b", ",", concepts_text)
    concepts_text = re.sub(r"\band\b", ",", concepts_text)
    concepts = []
    for concept in concepts_text.split(","):
        concept = concept.strip()
        concept = re.sub(r"^(?:a|an|the)\s+", "", concept, flags=re.IGNORECASE)
        concept = re.sub(r"^new\s+", "", concept, flags=re.IGNORECASE)
        if concept:
            concepts.append(concept)
    return concepts


def _frontier_claim(
    source_path: str,
    source_heading: str | None,
    line: str,
) -> DocumentationClaim | None:
    if _FRONTIER_RE.search(line) is None:
        return None

    active_frontier_match = _ACTIVE_CAPABILITY_FRONTIER_RE.match(line)
    if active_frontier_match is not None:
        subject = active_frontier_match.group("subject").strip()
        line = f"{subject} is the active capability frontier."

    return _claim(source_path, source_heading, line, FRONTIER)


def _claim(
    source_path: str,
    source_heading: str | None,
    claim_text: str,
    claim_family: str,
) -> DocumentationClaim:
    return DocumentationClaim(
        claim=claim_text,
        claim_family=claim_family,
        source_path=source_path,
        source_heading=source_heading,
    )
