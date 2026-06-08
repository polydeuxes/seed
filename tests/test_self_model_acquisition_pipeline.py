from __future__ import annotations

import sys

from seed_runtime.knowledge.documentation_observation import extract_documentation_claims
from seed_runtime.knowledge.repository_observation import extract_repository_artifact_facts
from seed_runtime.knowledge.relationship_observation import (
    RelationshipFact,
    extract_python_import_relationship_facts,
)
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


def test_structure_claim_supported_from_documentation_and_repository_observation():
    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Structure

Runtime defines method handle_user_message.
""",
    )
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/self_model_source.py",
        """class Runtime:
    def handle_user_message(self):
        pass
""",
    )
    alignment_records = reconcile_claims(claims, artifact_facts)

    method_facts = [
        fact
        for fact in artifact_facts
        if fact.artifact_kind == "method"
        and fact.symbol == "handle_user_message"
    ]

    assert len(claims) == 1
    assert claims[0].claim_family == "structure"
    assert any(
        fact.artifact_kind == "class" and fact.symbol == "Runtime"
        for fact in artifact_facts
    )
    assert len(method_facts) == 1
    assert method_facts[0].artifact_kind == "method"
    assert method_facts[0].symbol == "handle_user_message"
    assert method_facts[0].parent_symbol == "Runtime"
    assert len(alignment_records) == 1
    assert alignment_records[0].outcome == "supported"
    assert alignment_records[0].rule_id == "structure.defines_method.supported"


def test_structure_claim_missing_support_for_top_level_function():
    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Structure

Runtime defines method handle_user_message.
""",
    )
    artifact_facts = extract_repository_artifact_facts(
        "fixtures/self_model_source.py",
        """class Runtime:
    pass

def handle_user_message():
    pass
""",
    )
    alignment_records = reconcile_claims(claims, artifact_facts)

    assert len(claims) == 1
    assert claims[0].claim_family == "structure"
    assert any(
        fact.artifact_kind == "class" and fact.symbol == "Runtime"
        for fact in artifact_facts
    )
    assert any(
        fact.artifact_kind == "function"
        and fact.symbol == "handle_user_message"
        and fact.parent_symbol is None
        for fact in artifact_facts
    )
    assert not any(
        fact.artifact_kind == "method"
        and fact.symbol == "handle_user_message"
        and fact.parent_symbol == "Runtime"
        for fact in artifact_facts
    )
    assert len(alignment_records) == 1
    assert alignment_records[0].outcome == "missing_support"
    assert alignment_records[0].rule_id == "structure.defines_method.missing_support"


def test_import_relationship_observation_pipeline():
    source_text = "from seed_runtime.execution import ToolExecutor\n"

    relationship_facts = extract_python_import_relationship_facts(
        "seed_runtime/runtime.py",
        source_text,
    )

    assert len(relationship_facts) == 1
    assert relationship_facts[0].relationship_kind == "imports"
    assert relationship_facts[0].subject == "seed_runtime.runtime"
    assert relationship_facts[0].object == "ToolExecutor"
    assert relationship_facts[0].path == "seed_runtime/runtime.py"


def test_multiple_import_relationship_observation_pipeline():
    source_text = """import seed_runtime.events
from seed_runtime.execution import ToolExecutor
"""

    relationship_facts = extract_python_import_relationship_facts(
        "seed_runtime/runtime.py",
        source_text,
    )

    assert len(relationship_facts) == 2
    assert [fact.relationship_kind for fact in relationship_facts] == [
        "imports",
        "imports",
    ]
    assert [fact.subject for fact in relationship_facts] == [
        "seed_runtime.runtime",
        "seed_runtime.runtime",
    ]
    assert [fact.object for fact in relationship_facts] == [
        "seed_runtime.events",
        "ToolExecutor",
    ]
    assert [fact.path for fact in relationship_facts] == [
        "seed_runtime/runtime.py",
        "seed_runtime/runtime.py",
    ]


def test_relationship_observation_isolation():
    relationship_facts = extract_python_import_relationship_facts(
        "seed_runtime/runtime.py",
        "from seed_runtime.execution import ToolExecutor\n",
    )

    assert relationship_facts
    assert all(isinstance(fact, RelationshipFact) for fact in relationship_facts)
    assert all(not isinstance(fact, DocumentationClaim) for fact in relationship_facts)
    assert all(
        not isinstance(fact, RepositoryArtifactFact)
        for fact in relationship_facts
    )
    assert all(not isinstance(fact, AlignmentRecord) for fact in relationship_facts)


def test_relationship_observation_no_runtime_dependencies():
    runtime_modules_before = {name: sys.modules.get(name) for name in _RUNTIME_MODULES}

    relationship_facts = extract_python_import_relationship_facts(
        "seed_runtime/runtime.py",
        """import seed_runtime.events
from seed_runtime.execution import ToolExecutor
""",
    )

    assert relationship_facts
    assert (
        {name: sys.modules.get(name) for name in _RUNTIME_MODULES}
        == runtime_modules_before
    )


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
