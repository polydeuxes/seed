from __future__ import annotations

import builtins
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


_RUNTIME_MODULES = (
    "seed_runtime.runtime",
    "seed_runtime.execution",
    "seed_runtime.events",
    "seed_runtime.projection_store",
)


def _load_relationship_observation_module() -> ModuleType:
    module_name = "relationship_observation_under_test"
    module_path = (
        Path(__file__).resolve().parents[1]
        / "seed_runtime"
        / "knowledge"
        / "relationship_observation.py"
    )
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_simple_import_extracts_one_imports_relationship():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_import_relationship_facts(
        "fixtures/source.py",
        "import seed_runtime.events\n",
    )

    assert len(facts) == 1
    assert facts[0].relationship_kind == "imports"
    assert facts[0].subject == "fixtures.source"
    assert facts[0].object == "seed_runtime.events"
    assert facts[0].path == "fixtures/source.py"


def test_from_import_extracts_imported_symbol_object():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_import_relationship_facts(
        "fixtures/source.py",
        "from seed_runtime.execution import ToolExecutor\n",
    )

    assert len(facts) == 1
    assert facts[0].relationship_kind == "imports"
    assert "ToolExecutor" in facts[0].object
    assert facts[0].object == "ToolExecutor"


def test_multiple_imports_extract_multiple_imports_relationships():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_import_relationship_facts(
        "fixtures/source.py",
        """import a
import b
from c import D
""",
    )

    assert len(facts) == 3
    assert [fact.relationship_kind for fact in facts] == ["imports", "imports", "imports"]
    assert [fact.object for fact in facts] == ["a", "b", "D"]


def test_parse_failure_returns_empty_relationship_list():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_import_relationship_facts(
        "fixtures/source.py",
        "def broken(\n",
    )

    assert facts == []


def test_compatibility_wrapper_returns_identical_relationships():
    relationship_observation = _load_relationship_observation_module()

    direct_facts = relationship_observation.extract_python_import_relationship_facts(
        "fixtures/source.py",
        "import seed_runtime.events\nfrom seed_runtime.execution import ToolExecutor\n",
    )
    wrapper_facts = relationship_observation.extract_relationship_facts(
        "fixtures/source.py",
        "import seed_runtime.events\nfrom seed_runtime.execution import ToolExecutor\n",
    )

    assert wrapper_facts == direct_facts


def test_relationship_observation_import_does_not_load_runtime_components():
    before = {name: sys.modules.get(name) for name in _RUNTIME_MODULES}
    for name in _RUNTIME_MODULES:
        sys.modules.pop(name, None)

    try:
        relationship_observation = _load_relationship_observation_module()

        assert relationship_observation.extract_python_import_relationship_facts(
            "fixtures/source.py",
            "import seed_runtime.events\nfrom seed_runtime.execution import ToolExecutor\n",
        )
        assert all(name not in sys.modules for name in _RUNTIME_MODULES)
    finally:
        for name, module in before.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def test_relationship_observation_uses_inline_text_without_file_reads(monkeypatch):
    relationship_observation = _load_relationship_observation_module()

    def fail_open(*args, **kwargs):
        raise AssertionError("relationship observation must not read files")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    facts = relationship_observation.extract_python_import_relationship_facts(
        "fixtures/source.py",
        "import seed_runtime.events\n",
    )

    assert len(facts) == 1
    assert facts[0].relationship_kind == "imports"


def test_function_definition_extracts_definition_relationship():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_definition_relationship_facts(
        "fixtures/source.py",
        "def build_state_summary(state):\n    return state\n",
    )

    assert len(facts) == 1
    assert facts[0].relationship_kind == "defines"
    assert facts[0].subject == "fixtures.source"
    assert facts[0].object == "fixtures.source.build_state_summary"
    assert facts[0].path == "fixtures/source.py"
    assert "function build_state_summary" in facts[0].evidence
    assert "fixtures/source.py:1-2" in facts[0].evidence


def test_class_definition_extracts_definition_relationship():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_definition_relationship_facts(
        "fixtures/source.py",
        "class StateSummaryRenderer:\n    pass\n",
    )

    assert len(facts) == 1
    assert facts[0].relationship_kind == "defines"
    assert facts[0].object == "fixtures.source.StateSummaryRenderer"
    assert "class StateSummaryRenderer" in facts[0].evidence
    assert "fixtures/source.py:1-2" in facts[0].evidence


def test_definition_observation_does_not_change_import_relationships():
    relationship_observation = _load_relationship_observation_module()
    text = "import seed_runtime.events\nfrom seed_runtime.execution import ToolExecutor\n"

    facts = relationship_observation.extract_python_import_relationship_facts(
        "fixtures/source.py",
        text,
    )

    assert [fact.relationship_kind for fact in facts] == ["imports", "imports"]
    assert [fact.object for fact in facts] == ["seed_runtime.events", "ToolExecutor"]


def test_definition_observation_does_not_emit_call_relationships():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_definition_relationship_facts(
        "fixtures/source.py",
        "def caller():\n    project_state_with_cache()\n",
    )

    assert {fact.relationship_kind for fact in facts} == {"defines"}
    assert all("calls" not in fact.evidence for fact in facts)
    assert all("project_state_with_cache" not in fact.object for fact in facts)


def test_definition_observation_does_not_emit_ownership_claims():
    relationship_observation = _load_relationship_observation_module()

    facts = relationship_observation.extract_python_definition_relationship_facts(
        "fixtures/source.py",
        "class ProjectionCapability:\n    pass\n",
    )

    assert {fact.relationship_kind for fact in facts} == {"defines"}
    assert all("owns" not in fact.evidence for fact in facts)
    assert all("capability authority" not in fact.evidence.lower() for fact in facts)
    assert all("implemented_by" not in fact.evidence for fact in facts)


def test_definition_observation_remains_source_observation_only(monkeypatch):
    relationship_observation = _load_relationship_observation_module()

    def fail_open(*args, **kwargs):
        raise AssertionError("definition observation must not read files")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "open", fail_open)

    facts = relationship_observation.extract_python_definition_relationship_facts(
        "fixtures/source.py",
        "def source_only():\n    return 1\n",
    )

    assert len(facts) == 1
    assert facts[0].relationship_kind == "defines"
