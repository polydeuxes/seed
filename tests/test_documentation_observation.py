from __future__ import annotations

from seed_runtime.knowledge.documentation_observation import extract_documentation_claims


def test_extracts_ownership_claim_with_heading_and_source_path():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Ownership Boundaries

- `ToolExecutor` owns registered-operation execution.
""",
    )

    assert len(claims) == 1
    claim = claims[0]
    assert claim.claim_family == "ownership"
    assert claim.source_path == "docs/fixture.md"
    assert claim.source_heading == "Ownership Boundaries"
    assert "ToolExecutor" in claim.claim


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
ToolExecutor owns all execution.
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
