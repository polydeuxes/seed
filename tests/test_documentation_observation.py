from __future__ import annotations

from seed_runtime.knowledge.documentation_observation import extract_documentation_claims


def test_extracts_ownership_claim_with_heading_and_source_path():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Ownership Boundaries

- `ExampleComponent` owns repository inspection.
""",
    )

    assert len(claims) == 1
    claim = claims[0]
    assert claim.claim_family == "ownership"
    assert claim.source_path == "docs/fixture.md"
    assert claim.source_heading == "Ownership Boundaries"
    assert "ExampleComponent" in claim.claim


def test_extracts_rejected_concept_claims():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Rejected Solutions

- Do not add InputEngine, ConversationEngine, or CommandEngine.
""",
    )

    rejected_claims = [claim for claim in claims if claim.claim_family == "rejected_concept"]
    assert {claim.claim for claim in rejected_claims} == {
        "InputEngine is rejected.",
        "ConversationEngine is rejected.",
        "CommandEngine is rejected.",
    }
    assert all(claim.source_heading == "Rejected Solutions" for claim in rejected_claims)


def test_extracts_frontier_claims():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Current Status

- Knowledge Acquisition — active capability frontier
- Users Observation is a current capability-growth priority.
""",
    )

    frontier_claims = [claim for claim in claims if claim.claim_family == "frontier"]
    assert [claim.claim for claim in frontier_claims] == [
        "Knowledge Acquisition is the active capability frontier.",
        "Users Observation is a current capability-growth priority.",
    ]
    assert all(claim.source_heading == "Current Status" for claim in frontier_claims)


def test_ignores_code_fence_claim_text():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """```text
ExampleComponent owns all execution.
```
""",
    )

    assert claims == []


def test_ignores_narrative_non_claim_prose():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """Seed contains a substantial amount of architectural documentation.
This section explains the repository.
""",
    )

    assert claims == []


def test_multiple_headings_assign_nearest_heading():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Ownership Boundaries

- Runtime remains canonical user-message intake and route owner.

## Current Status

- Systemd Observation is a current frontier.
""",
    )

    assert [(claim.claim_family, claim.source_heading) for claim in claims] == [
        ("ownership", "Ownership Boundaries"),
        ("frontier", "Current Status"),
    ]


def test_front_matter_is_detected_correctly():
    from seed_runtime.knowledge.documentation_observation import observe_documentation_metadata

    observation = observe_documentation_metadata(
        "docs/example.md",
        """---
doc_type: frontier
status: active
domain: knowledge navigation
defines:
  - structural navigation
---
# Body
""",
    )

    assert observation.has_front_matter is True
    assert observation.doc_type == "frontier"
    assert observation.status == "active"
    assert observation.domain == "knowledge navigation"
    assert observation.defines == ("structural navigation",)


def test_document_without_front_matter_is_handled_deterministically():
    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
        observe_documentation_metadata,
    )

    text = "# No metadata\n\ndepends_on:\n  - docs/ignored.md\n"

    assert (
        observe_documentation_metadata("docs/no_metadata.md", text).has_front_matter
        is False
    )
    assert (
        extract_documentation_navigation_relationship_facts("docs/no_metadata.md", text)
        == []
    )


def test_depends_on_relationships_are_observed_from_front_matter():
    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
    )

    facts = extract_documentation_navigation_relationship_facts(
        "docs/source.md",
        """---
depends_on:
  - index.md
  - ../README.md
---
Body ignored.
""",
    )

    assert [(fact.relationship_kind, fact.subject, fact.object) for fact in facts] == [
        ("depends_on", "docs/source.md", "docs/index.md"),
        ("depends_on", "docs/source.md", "README.md"),
    ]


def test_related_relationships_are_observed_from_front_matter():
    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
    )

    facts = extract_documentation_navigation_relationship_facts(
        "docs/source.md",
        """---
related:
  - documentation_observation_design.md
---
related:
  - body_must_not_count.md
""",
    )

    assert [(fact.relationship_kind, fact.object) for fact in facts] == [
        ("related_to", "docs/documentation_observation_design.md")
    ]


def test_domain_relationship_is_observed_from_front_matter():
    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
    )

    facts = extract_documentation_navigation_relationship_facts(
        "docs/source.md",
        """---
domain: knowledge navigation
---
""",
    )

    assert [(fact.relationship_kind, fact.subject, fact.object) for fact in facts] == [
        ("belongs_to_domain", "docs/source.md", "knowledge navigation")
    ]


def test_defines_relationships_are_observed_from_front_matter():
    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
    )

    facts = extract_documentation_navigation_relationship_facts(
        "docs/source.md",
        """---
defines:
  - structural navigation
  - architectural navigation
---
The body says this defines prose-derived navigation, but it must be ignored.
""",
    )

    assert [(fact.relationship_kind, fact.subject, fact.object) for fact in facts] == [
        ("defines", "docs/source.md", "structural navigation"),
        ("defines", "docs/source.md", "architectural navigation"),
    ]


def test_document_body_content_is_ignored_for_navigation_metadata():
    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
    )

    facts = extract_documentation_navigation_relationship_facts(
        "docs/source.md",
        """---
depends_on:
  - index.md
---
---
depends_on:
  - body.md
related:
  - body_related.md
domain: body domain
defines:
  - body concept
---
""",
    )

    assert [(fact.relationship_kind, fact.object) for fact in facts] == [
        ("depends_on", "docs/index.md")
    ]


def test_documentation_navigation_relationship_observation_is_deterministic():
    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
    )

    text = """---
domain: knowledge navigation
defines: [structural navigation, architectural navigation]
depends_on:
  - index.md
related:
  - knowledge_representation_map.md
---
"""

    first = extract_documentation_navigation_relationship_facts("docs/source.md", text)
    second = extract_documentation_navigation_relationship_facts("docs/source.md", text)

    assert first == second


def test_documentation_navigation_metadata_requires_no_llm_or_natural_language(monkeypatch):
    import builtins
    from pathlib import Path

    from seed_runtime.knowledge.documentation_observation import (
        extract_documentation_navigation_relationship_facts,
    )

    def fail_open(*args, **kwargs):
        raise AssertionError(
            "documentation metadata observation must use caller-provided text"
        )

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    facts = extract_documentation_navigation_relationship_facts(
        "docs/source.md",
        """---
domain: authored metadata
defines:
  - explicit concept
---
Natural-language prose would mention other concepts if interpreted.
""",
    )

    assert [(fact.relationship_kind, fact.object) for fact in facts] == [
        ("belongs_to_domain", "authored metadata"),
        ("defines", "explicit concept"),
    ]
