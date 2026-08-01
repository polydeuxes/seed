"""Deletion guard for the demandless closed-choice binding branch."""

from importlib.util import find_spec
import inspect
from pathlib import Path

import seed_runtime
import seed_runtime.bounded_operator_goal_establishment as goal_establishment
from seed_runtime.contextual_interpretation_warrant_set import (
    ContextualInterpretationWarrantSet,
    produce_contextual_interpretation_warrant_set,
)


DELETED_EXPORTS = {
    "ClosedChoiceOption",
    "PresentedClosedChoiceSet",
    "OperatorSelectionTokenCapture",
    "ClosedChoiceSelectionBinding",
    "ClosedChoiceSelectionBindingError",
    "bind_closed_choice_selection",
    "closed_choice_selection_binding_json",
    "establish_bounded_operator_goal_from_closed_choice",
}


def test_closed_choice_binding_branch_remains_absent():
    assert find_spec("seed_runtime.closed_choice_selection_binding") is None
    assert DELETED_EXPORTS.isdisjoint(seed_runtime.__all__)
    assert all(not hasattr(seed_runtime, name) for name in DELETED_EXPORTS)
    assert not hasattr(
        goal_establishment, "establish_bounded_operator_goal_from_closed_choice"
    )

    runtime_root = Path(seed_runtime.__file__).parent
    production_sources = (*runtime_root.glob("*.py"), *Path("scripts").glob("*.py"))
    assert all(
        "closed_choice_selection_binding" not in source.read_text()
        for source in production_sources
    )
    assert all("closed choice" not in source.read_text().lower() for source in production_sources)

    assert "closed_choice_selection_binding_ref" not in {
        field.name for field in inspect.signature(ContextualInterpretationWarrantSet).parameters.values()
    }
    assert "closed_choice_selection_binding_ref" not in inspect.signature(
        produce_contextual_interpretation_warrant_set
    ).parameters
