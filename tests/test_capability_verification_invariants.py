from __future__ import annotations

from pathlib import Path


VOCABULARY_DOC = Path("docs/capability_verification_vocabulary.md")
INVARIANTS_DOC = Path("docs/invariants.md")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_capability_verification_vocabulary_defines_supported_terms():
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


def test_capability_standing_is_evidence_dependent():
    text = _read(VOCABULARY_DOC)

    evidence_examples = [
        "observation-derived facts",
        "linked Evidence",
        "operator-supplied testimony",
        "provider reports\nadmitted as testimony",
        "freshness or expiry\nboundaries",
        "bounded verification status projections",
    ]

    for example in evidence_examples:
        assert example in text

    assert "the inventory entry is only as strong as the supporting\nFact/FactSupport/Evidence it exposes" in text


def test_requested_known_candidate_and_provider_reported_are_not_verified():
    text = _read(VOCABULARY_DOC)

    distinctions = [
        "A requested capability means Seed has recorded a capability gap or desired\nability.",
        "A known capability does not imply that the capability is available",
        "A candidate capability is only a possibility.",
        "provider-reported support",
        "Provider-reported status by itself: testimony that may be admitted as evidence,\n  not automatic proof or Seed's own verification conclusion.",
    ]

    for distinction in distinctions:
        assert distinction in text


def test_verification_evidence_is_not_verification():
    text = _read(VOCABULARY_DOC)

    assert "An observation, observation-derived fact, linked Evidence item, confidence" in text
    assert "is a verified capability without a scoped verification status model" in text


def test_stale_verification_is_not_current_and_failed_requires_negative_evidence():
    vocabulary = _read(VOCABULARY_DOC)
    invariants = _read(INVARIANTS_DOC)

    for text in (vocabulary, invariants):
        assert "Stale verification must not be treated as current positive verification." in text
        assert "Failed verification requires accepted negative evidence" in text
        assert "absence of positive evidence" in text


def test_read_only_verification_views_do_not_create_capability_standing():
    text = _read(VOCABULARY_DOC)

    assert "verification views are read-only" in text.lower()
    assert "The inventory is read-only." in text
    assert "appends no\nevents" in text
    assert "cause capability resolution to produce a verified capability" in text


def test_active_invariants_do_not_preserve_deleted_runtime_roads():
    text = _read(INVARIANTS_DOC)

    forbidden = [
        "`Runtime` is canonical",
        "request_tool records and resolves a capability gap",
        "ActionPlan may be retained",
        "HandoffPlan may be retained",
        "ExecutionProposal may be retained",
        "ExecutionAuthorization may be retained",
        "If retained, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and",
    ]

    for phrase in forbidden:
        assert phrase not in text


def test_active_architecture_doc_does_not_claim_deleted_runtime_pipeline():
    text = Path("docs/architecture.md").read_text(encoding="utf-8")

    forbidden = [
        "Runtime is the canonical",
        "Runtime is canonical",
        "Input -> Events -> State -> Context -> Decision -> Policy -> Execution -> Events",
        "Context -> Decision",
        "Decision -> Policy",
        "Policy -> Execution",
    ]

    for phrase in forbidden:
        assert phrase not in text


def test_original_numbered_seed_corpus_is_archived_not_root_active_docs():
    numbered_files = [
        "01-architecture.md",
        "02-domain-model.md",
        "03-runtime-loop.md",
        "04-toolkit-system.md",
        "05-policy-and-safety.md",
        "06-context-engine.md",
        "07-builder-service.md",
        "08-small-model-strategy.md",
        "09-pseudocode.md",
        "10-build-plan.md",
        "11-naming.md",
        "12-open-questions.md",
        "13-knowledge-and-evidence.md",
    ]
    archive = Path("docs/archive/original_book_of_seed")

    for name in numbered_files:
        assert not Path(name).exists(), f"root active copy remains: {name}"
        assert (archive / name).is_file(), f"archived corpus file missing: {name}"


def test_original_numbered_seed_corpus_readme_denies_current_authority():
    text = _read(Path("docs/archive/original_book_of_seed/README.md"))

    required = [
        "This directory preserves the original numbered Seed design corpus.",
        "They are not:",
        "current Seed architecture",
        "canonical constitutional grammar",
        "current domain vocabulary",
        "implementation ownership evidence",
        "an operator guide",
        "an invariant source",
        "authority to retain or recreate an implementation artifact",
        "The canonical constitutional corpus is:",
        "book_of_seed/",
        "Current implementation standing must be recovered from the current witness",
    ]

    for phrase in required:
        assert phrase in text
