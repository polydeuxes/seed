from __future__ import annotations

import sys

from seed_runtime.knowledge.documentation_observation import extract_documentation_claims
from seed_runtime.knowledge.repository_observation import extract_repository_artifact_facts
from seed_runtime.knowledge.self_model_alignment import (
    DocumentationClaim,
    RepositoryArtifactFact,
    reconcile_claims,
)


def _claim(claim: str, family: str = "existence") -> DocumentationClaim:
    return DocumentationClaim(
        claim=claim,
        claim_family=family,
        source_path="docs/fixture.md",
    )


def _fact(symbol: str, artifact_kind: str = "class") -> RepositoryArtifactFact:
    return RepositoryArtifactFact(
        fact=f"{artifact_kind.title()} {symbol} exists in seed_runtime/fixture.py.",
        artifact_kind=artifact_kind,
        path="seed_runtime/fixture.py",
        symbol=symbol,
    )


def _single_record(
    claim: DocumentationClaim,
    facts: list[RepositoryArtifactFact],
):
    return reconcile_claims([claim], facts)[0]


def test_tool_executor_exists_with_tool_executor_class_is_supported():
    record = _single_record(
        _claim("ToolExecutor exists."),
        [_fact("ToolExecutor")],
    )

    assert record.outcome == "supported"
    assert record.rule_id == "existence.exists.supported"
    assert [fact.symbol for fact in record.artifact_facts] == ["ToolExecutor"]


def test_magic_executor_exists_without_magic_executor_class_is_missing_support():
    record = _single_record(
        _claim("MagicExecutor exists."),
        [_fact("ToolExecutor")],
    )

    assert record.outcome == "missing_support"
    assert record.rule_id == "existence.exists.missing_support"
    assert record.artifact_facts == ()


def test_runtime_defines_handle_user_message_with_both_symbols_is_supported():
    record = _single_record(
        _claim("Runtime defines handle_user_message."),
        [_fact("Runtime"), _fact("handle_user_message", artifact_kind="function")],
    )

    assert record.outcome == "supported"
    assert record.rule_id == "existence.defines.supported"
    assert {fact.symbol for fact in record.artifact_facts} == {
        "Runtime",
        "handle_user_message",
    }


def test_runtime_defines_handle_user_message_with_only_runtime_is_missing_support():
    record = _single_record(
        _claim("Runtime defines handle_user_message."),
        [_fact("Runtime")],
    )

    assert record.outcome == "missing_support"
    assert record.rule_id == "existence.defines.missing_support"
    assert record.artifact_facts == ()


def test_vague_existence_like_prose_is_not_extracted():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Architecture

ToolExecutor appears important.
Runtime probably has a user-message path.
Execution capability is present.
""",
    )

    assert claims == []


def test_manually_constructed_vague_existence_claim_is_not_evaluable():
    record = _single_record(
        _claim("ToolExecutor appears important."),
        [_fact("ToolExecutor")],
    )

    assert record.outcome == "not_evaluable"
    assert record.rule_id == "existence.not_evaluable"
    assert record.artifact_facts == ()


def test_explicit_existence_claims_are_extracted_from_documentation():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Repository Artifacts

ToolExecutor exists.
ProjectionStore exists.
Runtime defines handle_user_message.
""",
    )

    assert [(claim.claim, claim.claim_family) for claim in claims] == [
        ("ToolExecutor exists.", "existence"),
        ("ProjectionStore exists.", "existence"),
        ("Runtime defines handle_user_message.", "existence"),
    ]
    assert {claim.source_heading for claim in claims} == {"Repository Artifacts"}


def test_ownership_claim_still_uses_ownership_semantics():
    record = _single_record(
        _claim("ToolExecutor owns registered-operation execution.", family="ownership"),
        [_fact("ToolExecutor")],
    )

    assert record.outcome == "supported"
    assert record.rule_id == "ownership.tool_executor.supported"


def test_fixture_pipeline_does_not_require_runtime_tool_event_or_projection_loading():
    runtime_modules = (
        "seed_runtime.runtime",
        "seed_runtime.execution",
        "seed_runtime.events",
        "seed_runtime.projection_store",
    )
    runtime_modules_before = {name: sys.modules.get(name) for name in runtime_modules}

    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Repository Artifacts

Runtime defines handle_user_message.
""",
    )
    facts = extract_repository_artifact_facts(
        "fixtures/runtime.py",
        """class Runtime:
    pass

def handle_user_message():
    pass
""",
    )

    records = reconcile_claims(claims, facts)

    assert [claim.claim_family for claim in claims] == ["existence"]
    assert any(fact.symbol == "Runtime" for fact in facts)
    assert any(fact.symbol == "handle_user_message" for fact in facts)
    assert len(records) == 1
    assert records[0].outcome == "supported"
    assert (
        {name: sys.modules.get(name) for name in runtime_modules}
        == runtime_modules_before
    )
