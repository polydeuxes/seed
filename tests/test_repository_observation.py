from __future__ import annotations

from seed_runtime.knowledge.repository_observation import (
    extract_repository_artifact_facts,
)


_SOURCE_PATH = "seed_runtime/runtime.py"


def _facts(text: str):
    return extract_repository_artifact_facts(_SOURCE_PATH, text)


def test_extracts_module_fact_for_source_path():
    facts = _facts("""class Runtime:\n    pass\n""")

    assert any(
        fact.artifact_kind == "module"
        and fact.path == _SOURCE_PATH
        and fact.parent_symbol is None
        and "Module/file seed_runtime/runtime.py exists" in fact.fact
        for fact in facts
    )


def test_extracts_class_definition_fact():
    facts = _facts("""class Runtime:\n    pass\n""")

    assert any(
        fact.artifact_kind == "class"
        and fact.symbol == "Runtime"
        and fact.parent_symbol is None
        and fact.path == _SOURCE_PATH
        for fact in facts
    )


def test_extracts_top_level_function_definition_fact():
    facts = _facts("""def helper():\n    pass\n""")

    assert any(
        fact.artifact_kind == "function"
        and fact.symbol == "helper"
        and fact.parent_symbol is None
        and fact.path == _SOURCE_PATH
        for fact in facts
    )


def test_extracts_class_method_fact_without_top_level_function_fact():
    facts = _facts("""class Runtime:\n    def handle_user_message(self):\n        pass\n""")

    assert any(
        fact.artifact_kind == "class"
        and fact.symbol == "Runtime"
        and fact.parent_symbol is None
        and fact.path == _SOURCE_PATH
        for fact in facts
    )
    assert any(
        fact.artifact_kind == "method"
        and fact.symbol == "handle_user_message"
        and fact.parent_symbol == "Runtime"
        and fact.path == _SOURCE_PATH
        for fact in facts
    )
    assert not any(
        fact.artifact_kind == "function" and fact.symbol == "handle_user_message"
        for fact in facts
    )


def test_extracts_async_class_method_fact():
    facts = _facts("""class Collector:\n    async def collect(self):\n        pass\n""")

    assert any(
        fact.artifact_kind == "method"
        and fact.symbol == "collect"
        and fact.parent_symbol == "Collector"
        and fact.path == _SOURCE_PATH
        for fact in facts
    )


def test_extracts_top_level_async_function_definition_fact():
    facts = _facts("""async def collect():\n    pass\n""")

    assert any(
        fact.artifact_kind == "function"
        and fact.symbol == "collect"
        and fact.parent_symbol is None
        and fact.path == _SOURCE_PATH
        for fact in facts
    )


def test_ignores_nested_function_inside_function():
    facts = _facts("""def outer():\n    def inner():\n        pass\n""")

    assert any(
        fact.artifact_kind == "function"
        and fact.symbol == "outer"
        and fact.parent_symbol is None
        for fact in facts
    )
    assert not any(fact.symbol == "inner" for fact in facts)


def test_extracts_import_facts():
    facts = _facts(
        """import json\nfrom seed_runtime.models import Decision\nfrom seed_runtime.execution import ToolExecutor\n"""
    )

    import_symbols = {
        fact.symbol for fact in facts if fact.artifact_kind == "import"
    }
    assert import_symbols == {
        "json",
        "seed_runtime.models.Decision",
        "seed_runtime.execution.ToolExecutor",
    }
    assert all(fact.parent_symbol is None for fact in facts)


def test_parse_failure_returns_only_module_fact_without_raising():
    facts = _facts("""def broken(\n""")

    assert len(facts) == 1
    assert facts[0].artifact_kind == "module"
    assert facts[0].path == _SOURCE_PATH
    assert facts[0].parent_symbol is None
    assert "could not be parsed" in facts[0].fact


def test_extractor_emits_only_artifact_facts_without_architecture_inference():
    facts = _facts("""class ToolExecutor:\n    pass\n""")

    assert {fact.artifact_kind for fact in facts} == {"module", "class"}
    assert all(not hasattr(fact, "claim_family") for fact in facts)
    assert all(not hasattr(fact, "outcome") for fact in facts)
    assert all("owns" not in fact.fact.lower() for fact in facts)
