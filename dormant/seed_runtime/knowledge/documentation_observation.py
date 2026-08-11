"""Deterministic documentation claim extraction helpers.

This module intentionally works only on caller-provided text. It does not read
files, inspect the repository, use LLMs, or integrate with runtime/tool
execution. Claim extraction parses only simple markdown headings/lines;
navigation metadata observation parses only YAML front matter.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from seed_runtime.knowledge.relationship_observation import (
    RelationshipFact,
    documentation_navigation_relationship_facts,
)

from seed_runtime.knowledge.self_model_alignment import (
    EXISTENCE,
    FRONTIER,
    STRUCTURE,
    OWNERSHIP,
    REJECTED_CONCEPT,
    DocumentationClaim,
)


_HEADING_RE = re.compile(r"^#{1,6}\s+(?P<heading>.*?)\s*#*\s*$")
_BULLET_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)(?P<text>.*)$")
_CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_OWNERSHIP_RE = re.compile(r"\b(?:owns?|owner)\b", re.IGNORECASE)
_EXISTENCE_EXISTS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s+exists\.$")
_EXISTENCE_DEFINES_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*\s+defines\s+[A-Za-z_][A-Za-z0-9_]*\.$"
)
_STRUCTURE_DEFINES_METHOD_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*\s+defines\s+method\s+[A-Za-z_][A-Za-z0-9_]*\.$"
)
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
    headings, skips fenced code blocks, and recognizes only explicit ownership,
    rejected-concept, frontier, existence, and the explicit structure claim family.
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

    if _is_structure_claim(line):
        return [_claim(source_path, source_heading, line, STRUCTURE)]

    if _is_existence_claim(line):
        return [_claim(source_path, source_heading, line, EXISTENCE)]

    return []


def _is_ownership_claim(line: str) -> bool:
    return _OWNERSHIP_RE.search(line) is not None


def _is_structure_claim(line: str) -> bool:
    return _STRUCTURE_DEFINES_METHOD_RE.fullmatch(line) is not None


def _is_existence_claim(line: str) -> bool:
    return (
        _EXISTENCE_EXISTS_RE.fullmatch(line) is not None
        or _EXISTENCE_DEFINES_RE.fullmatch(line) is not None
    )


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


_FRONT_MATTER_DELIMITER = "---"
_METADATA_KEYS = frozenset(
    {"doc_type", "status", "domain", "defines", "depends_on", "related"}
)
_LIST_METADATA_KEYS = frozenset({"defines", "depends_on", "related"})


@dataclass(frozen=True)
class DocumentationMetadataObservation:
    """Authored documentation navigation metadata observed from front matter only."""

    source_path: str
    has_front_matter: bool
    doc_type: str | None = None
    status: str | None = None
    domain: str | None = None
    defines: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    related: tuple[str, ...] = ()


def observe_documentation_metadata(
    source_path: str,
    text: str,
) -> DocumentationMetadataObservation:
    """Observe authored YAML front matter without inspecting document prose."""

    front_matter = _front_matter_text(text)
    if front_matter is None:
        return DocumentationMetadataObservation(
            source_path=source_path,
            has_front_matter=False,
        )

    metadata = _parse_supported_front_matter(front_matter)
    return DocumentationMetadataObservation(
        source_path=source_path,
        has_front_matter=True,
        doc_type=_optional_scalar(metadata, "doc_type"),
        status=_optional_scalar(metadata, "status"),
        domain=_optional_scalar(metadata, "domain"),
        defines=_metadata_list(metadata, "defines"),
        depends_on=_metadata_list(metadata, "depends_on"),
        related=_metadata_list(metadata, "related"),
    )


def extract_documentation_navigation_relationship_facts(
    source_path: str,
    text: str,
) -> list[RelationshipFact]:
    """Extract navigation relationship facts from documentation front matter only."""

    observation = observe_documentation_metadata(source_path, text)
    if not observation.has_front_matter:
        return []
    return documentation_navigation_relationship_facts(
        observation.source_path,
        domain=observation.domain,
        defines=observation.defines,
        depends_on=observation.depends_on,
        related=observation.related,
    )


def _front_matter_text(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FRONT_MATTER_DELIMITER:
        return None

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == _FRONT_MATTER_DELIMITER:
            return "\n".join(lines[1:index])
    return None


def _parse_supported_front_matter(front_matter: str) -> dict[str, str | tuple[str, ...]]:
    parsed: dict[str, str | tuple[str, ...]] = {}
    current_list_key: str | None = None
    list_items: dict[str, list[str]] = {}

    for raw_line in front_matter.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if current_list_key is not None and stripped.startswith("-"):
            item = _clean_yaml_scalar(stripped[1:].strip())
            if item:
                list_items.setdefault(current_list_key, []).append(item)
            continue

        current_list_key = None
        if ":" not in stripped:
            continue

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        if key not in _METADATA_KEYS:
            continue

        value = raw_value.strip()
        if key in _LIST_METADATA_KEYS:
            if value:
                parsed[key] = _inline_or_singleton_list(value)
            else:
                current_list_key = key
                list_items.setdefault(key, [])
        elif value:
            parsed[key] = _clean_yaml_scalar(value)

    for key, items in list_items.items():
        parsed[key] = tuple(items)
    return parsed


def _optional_scalar(
    metadata: dict[str, str | tuple[str, ...]], key: str
) -> str | None:
    value = metadata.get(key)
    if isinstance(value, str) and value:
        return value
    return None


def _metadata_list(
    metadata: dict[str, str | tuple[str, ...]], key: str
) -> tuple[str, ...]:
    value = metadata.get(key)
    if isinstance(value, tuple):
        return value
    if isinstance(value, str) and value:
        return (value,)
    return ()


def _inline_or_singleton_list(value: str) -> tuple[str, ...]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return tuple(
            item
            for item in (
                _clean_yaml_scalar(part.strip()) for part in value[1:-1].split(",")
            )
            if item
        )
    cleaned = _clean_yaml_scalar(value)
    return (cleaned,) if cleaned else ()


def _clean_yaml_scalar(value: str) -> str:
    value = value.split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.strip()
