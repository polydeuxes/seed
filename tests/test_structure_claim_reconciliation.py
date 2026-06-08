from __future__ import annotations

import sys

from seed_runtime.knowledge.documentation_observation import extract_documentation_claims
from seed_runtime.knowledge.self_model_alignment import (
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


def _claim(claim: str, family: str = "structure") -> DocumentationClaim:
    return DocumentationClaim(
        claim=claim,
        claim_family=family,
        source_path="docs/fixture.md",
    )


def _fact(
    artifact_kind: str,
    symbol: str | None,
    *,
    parent_symbol: str | None = None,
    path: str = "seed_runtime/fixture.py",
) -> RepositoryArtifactFact:
    return RepositoryArtifactFact(
        fact=f"{artifact_kind} {symbol} fixture fact.",
        artifact_kind=artifact_kind,
        path=path,
        symbol=symbol,
        parent_symbol=parent_symbol,
    )


def _single_record(
    claim: DocumentationClaim,
    facts: list[RepositoryArtifactFact],
):
    records = reconcile_claims([claim], facts)
    assert len(records) == 1
    return records[0]


def test_class_with_contained_method_supports_defines_method_structure_claim():
    record = _single_record(
        _claim("Runtime defines method handle_user_message."),
        [
            _fact("class", "Runtime"),
            _fact("method", "handle_user_message", parent_symbol="Runtime"),
        ],
    )

    assert record.outcome == "supported"
    assert record.rule_id == "structure.defines_method.supported"
    assert [fact.artifact_kind for fact in record.artifact_facts] == [
        "class",
        "method",
    ]


def test_top_level_function_does_not_support_defines_method_structure_claim():
    record = _single_record(
        _claim("Runtime defines method handle_user_message."),
        [
            _fact("class", "Runtime"),
            _fact("function", "handle_user_message"),
        ],
    )

    assert record.outcome == "missing_support"
    assert record.rule_id == "structure.defines_method.missing_support"
    assert record.artifact_facts == ()


def test_method_contained_by_other_class_does_not_support_defines_method_structure_claim():
    record = _single_record(
        _claim("Runtime defines method handle_user_message."),
        [
            _fact("class", "Runtime"),
            _fact("method", "handle_user_message", parent_symbol="OtherRuntime"),
        ],
    )

    assert record.outcome == "missing_support"
    assert record.rule_id == "structure.defines_method.missing_support"
    assert record.artifact_facts == ()


def test_unrecognized_structure_prose_is_not_extracted_and_is_not_evaluable():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Structure

Runtime has a handler.
""",
    )
    record = _single_record(
        _claim("Runtime has a handler."),
        [_fact("class", "Runtime")],
    )

    assert claims == []
    assert record.outcome == "not_evaluable"
    assert record.rule_id == "structure.not_evaluable"


def test_documentation_observation_extracts_only_explicit_defines_method_structure_claims():
    claims = extract_documentation_claims(
        "docs/fixture.md",
        """## Structure

Runtime defines method handle_user_message.
ToolExecutor defines method execute.
Runtime has a handler.
""",
    )

    assert [(claim.claim, claim.claim_family) for claim in claims] == [
        ("Runtime defines method handle_user_message.", "structure"),
        ("ToolExecutor defines method execute.", "structure"),
    ]


def test_existence_claim_still_uses_existence_reconciliation():
    record = _single_record(
        _claim("Runtime defines handle_user_message.", family="existence"),
        [
            _fact("class", "Runtime", path="seed_runtime/runtime.py"),
            _fact("function", "handle_user_message", path="seed_runtime/runtime.py"),
        ],
    )

    assert record.outcome == "supported"
    assert record.rule_id == "existence.defines.supported"


def test_ownership_claim_still_uses_ownership_reconciliation():
    record = _single_record(
        _claim("ToolExecutor owns registered-operation execution.", family="ownership"),
        [_fact("class", "ToolExecutor")],
    )

    assert record.outcome == "supported"
    assert record.rule_id == "ownership.tool_executor.supported"


def test_structure_reconciliation_does_not_load_runtime_tool_event_or_projection_modules():
    runtime_modules_before = {name: sys.modules.get(name) for name in _RUNTIME_MODULES}

    claims = extract_documentation_claims(
        "fixtures/self_model.md",
        """## Structure

Runtime defines method handle_user_message.
""",
    )
    records = reconcile_claims(
        claims,
        [
            _fact("class", "Runtime"),
            _fact("method", "handle_user_message", parent_symbol="Runtime"),
        ],
    )

    assert records[0].outcome == "supported"
    assert (
        {name: sys.modules.get(name) for name in _RUNTIME_MODULES}
        == runtime_modules_before
    )
