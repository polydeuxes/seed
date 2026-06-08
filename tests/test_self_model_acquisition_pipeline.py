from __future__ import annotations

import sys

from seed_runtime.knowledge.documentation_observation import extract_documentation_claims
from seed_runtime.knowledge.repository_observation import extract_repository_artifact_facts
from seed_runtime.knowledge.self_model_alignment import (
    AlignmentRecord,
    DocumentationClaim,
    RepositoryArtifactFact,
    reconcile_claims,
)


_RUNTIME_MODULES = (
    "seed_runtime.runtime",
    "seed_runtime.execution",
    "seed_runtime.events",
    "seed_runtime.projection_store",
)


def test_supported_ownership_claim_flows_from_documentation_and_source_fixtures():
    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Ownership Boundaries

ToolExecutor owns registered-operation execution.
""",
    )
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/self_model_source.py",
        """class ToolExecutor:
    pass
""",
    )
    alignment_records = reconcile_claims(claims, artifact_facts)

    assert len(claims) == 1
    assert isinstance(claims[0], DocumentationClaim)
    assert claims[0].claim_family == "ownership"
    assert claims[0].source_heading == "Ownership Boundaries"
    assert any(
        isinstance(fact, RepositoryArtifactFact)
        and fact.artifact_kind == "class"
        and fact.symbol == "ToolExecutor"
        for fact in artifact_facts
    )
    assert len(alignment_records) == 1
    assert isinstance(alignment_records[0], AlignmentRecord)
    assert alignment_records[0].outcome == "supported"


def test_unmatched_v0_ownership_rule_is_not_evaluable():
    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Ownership Boundaries

MagicExecutor owns all execution.
""",
    )
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/self_model_source.py",
        """class ToolExecutor:
    pass
""",
    )
    alignment_records = reconcile_claims(claims, artifact_facts)

    assert len(claims) == 1
    assert claims[0].claim == "MagicExecutor owns all execution."
    assert any(fact.symbol == "ToolExecutor" for fact in artifact_facts)
    assert len(alignment_records) == 1
    assert alignment_records[0].outcome == "not_evaluable"
    assert alignment_records[0].rule_id == "ownership.not_evaluable"


def test_supported_frontier_uses_current_reconciliation_semantics():
    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Current Status

Users Observation is a current capability-growth priority.
""",
    )
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/users.py",
        """def unrelated_helper():
    pass
""",
    )
    alignment_records = reconcile_claims(claims, artifact_facts)

    assert len(claims) == 1
    assert claims[0].claim_family == "frontier"
    # Current v0 matching is conservative; observe_users does not represent
    # Users Observation unless reconciliation rules explicitly say so.
    assert any(fact.symbol == "unrelated_helper" for fact in artifact_facts)
    assert len(alignment_records) == 1
    assert alignment_records[0].claim == claims[0]
    assert alignment_records[0].outcome == "supported"
    assert alignment_records[0].rule_id == "frontier.supported"


def test_multiple_claims_and_artifacts_produce_multiple_alignment_records():
    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Ownership Boundaries

ToolExecutor owns registered-operation execution.
ProjectionStore owns cached projected-state snapshots.
""",
    )
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/self_model_source.py",
        """class ToolExecutor:
    pass

class ProjectionStore:
    pass
""",
    )
    alignment_records = reconcile_claims(claims, artifact_facts)

    class_facts = [fact for fact in artifact_facts if fact.artifact_kind == "class"]

    assert [claim.claim for claim in claims] == [
        "ToolExecutor owns registered-operation execution.",
        "ProjectionStore owns cached projected-state snapshots.",
    ]
    assert {fact.symbol for fact in class_facts} == {"ToolExecutor", "ProjectionStore"}
    assert len(alignment_records) == 2
    assert [record.claim for record in alignment_records] == claims
    assert {record.outcome for record in alignment_records} == {"supported"}


def test_documentation_observation_does_not_emit_repository_facts():
    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Ownership Boundaries

ToolExecutor owns registered-operation execution.
""",
    )

    assert claims
    assert all(isinstance(claim, DocumentationClaim) for claim in claims)
    assert all(not isinstance(claim, RepositoryArtifactFact) for claim in claims)
    assert all(not hasattr(claim, "artifact_kind") for claim in claims)
    assert all(not hasattr(claim, "symbol") for claim in claims)


def test_repository_observation_does_not_emit_documentation_claims():
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/self_model_source.py",
        """class ToolExecutor:
    pass
""",
    )

    assert artifact_facts
    assert all(isinstance(fact, RepositoryArtifactFact) for fact in artifact_facts)
    assert all(not isinstance(fact, DocumentationClaim) for fact in artifact_facts)
    assert all(not hasattr(fact, "claim_family") for fact in artifact_facts)
    assert all(not hasattr(fact, "source_heading") for fact in artifact_facts)


def test_pipeline_does_not_load_or_instantiate_runtime_components():
    runtime_modules_before = {name: sys.modules.get(name) for name in _RUNTIME_MODULES}

    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Ownership Boundaries

ToolExecutor owns registered-operation execution.
ProjectionStore owns cached projected-state snapshots.
""",
    )
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/self_model_source.py",
        """class ToolExecutor:
    pass

class ProjectionStore:
    pass
""",
    )
    alignment_records = reconcile_claims(claims, artifact_facts)

    assert claims
    assert artifact_facts
    assert alignment_records
    assert (
        {name: sys.modules.get(name) for name in _RUNTIME_MODULES}
        == runtime_modules_before
    )
