from __future__ import annotations

from pathlib import Path


VOCABULARY_DOC = Path("docs/capability_verification_vocabulary.md")
INVARIANTS_DOC = Path("docs/invariants.md")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_capability_verification_vocabulary_defines_required_terms():
    text = _read(VOCABULARY_DOC)

    required_headings = [
        "### Capability",
        "### Requested capability",
        "### Known capability",
        "### Candidate capability",
        "### Provider-recommended capability",
        "### Verified capability",
        "### Unverified capability",
        "### Stale verification",
        "### Failed verification",
    ]

    for heading in required_headings:
        assert heading in text


def test_vocabulary_documents_non_verified_capability_examples():
    text = _read(VOCABULARY_DOC)

    non_verified_examples = [
        "`ToolNeed`: records a requested capability gap.",
        "`ToolSpec.capabilities`: inert registered-operation discovery metadata.",
        "`CapabilityCatalog` recommendation: static provider or handoff metadata.",
        "A registered operation candidate: a possible operation match, not verified",
    ]

    for example in non_verified_examples:
        assert example in text


def test_vocabulary_documents_future_evidence_classes_without_behavior():
    text = _read(VOCABULARY_DOC)

    evidence_headings = [
        "### Observation-derived fact",
        "### Provider-reported status",
        "### Verification operation result",
    ]

    for heading in evidence_headings:
        assert heading in text

    assert "These are vocabulary only and do not create runtime behavior." in text
    assert "This document does not define executable verification algorithms" in text


def test_invariants_state_capability_resolution_never_implies_verification():
    text = _read(INVARIANTS_DOC)

    invariants = [
        "Capability resolution never implies verification.",
        "ToolNeed creation never implies verification.",
        "Provider recommendation never implies verification.",
        "Registered operation candidate discovery never implies verification.",
        "A `verify_*` operation name never implies verification.",
    ]

    for invariant in invariants:
        assert invariant in text


def test_invariants_preserve_runtime_and_tool_executor_boundaries():
    text = _read(INVARIANTS_DOC)

    boundary_invariants = [
        "Capability verification is not implemented in the current runtime.",
        "`Runtime` must not add implicit verification behavior during capability",
        "`ToolExecutor` must not interpret capability metadata as verification.",
        "`CapabilityCatalog` remains read-only metadata",
    ]

    for invariant in boundary_invariants:
        assert invariant in text
