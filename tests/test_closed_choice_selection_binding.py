import pytest

from seed_runtime.closed_choice_selection_binding import (
    ClosedChoiceOption,
    ClosedChoiceSelectionBindingError,
    OperatorSelectionTokenCapture,
    PresentedClosedChoiceSet,
    bind_closed_choice_selection,
    closed_choice_selection_binding_json,
)


def choice_set(ref="set-a"):
    return PresentedClosedChoiceSet(
        choice_set_ref=ref,
        prompt="Choose one bounded read-only surface.",
        options=(
            ClosedChoiceOption("1", "show_inventory", "Show inventory"),
            ClosedChoiceOption("2", "show_shape_audit", "Show shape audit"),
        ),
        presentation_ref="presentation-a",
        provenance=("presented-choice-set",),
    )


def capture(token="1", ref="set-a", *, unknowns=(), conflicts=()):
    return OperatorSelectionTokenCapture(
        capture_ref=f"capture:{ref}:{token}",
        choice_set_ref=ref,
        captured_token=token,
        provenance=("operator-token",),
        unknowns=unknowns,
        conflicts=conflicts,
    )


def test_exact_set_binding_preserves_presented_choice_set_and_token():
    binding = bind_closed_choice_selection(choice_set(), capture("1"))

    assert binding.binding_state == "bound"
    assert binding.binding_reason == "captured_token_belongs_to_exact_choice_set"
    assert binding.captured_token == "1"
    assert binding.bound_option_ref == "show_inventory"
    assert binding.presented_options == choice_set().options
    assert binding.exact_choice_set_fingerprint == choice_set().exact_choice_set_fingerprint
    assert binding.read_only and not binding.writes_event_ledger and not binding.mutates_cluster


def test_token_binds_only_to_the_exact_choice_set_it_references():
    with pytest.raises(ClosedChoiceSelectionBindingError):
        bind_closed_choice_selection(choice_set("set-a"), capture("1", "set-b"))


def test_unsupported_unknown_and_conflicting_selection_evidence_is_preserved():
    unsupported = bind_closed_choice_selection(choice_set(), capture("9"))
    assert unsupported.binding_state == "unsupported"
    assert unsupported.bound_option_ref is None
    assert "unsupported token: 9" in unsupported.unsupported_selection_evidence

    unknown = bind_closed_choice_selection(choice_set(), capture("1", unknowns=("token capture source uncertain",)))
    assert unknown.binding_state == "unknown"
    assert unknown.bound_option_ref is None
    assert unknown.unknown_selection_evidence == ("token capture source uncertain",)

    conflict = bind_closed_choice_selection(choice_set(), capture("1", conflicts=("two different tokens observed",)))
    assert conflict.binding_state == "conflict"
    assert conflict.bound_option_ref is None
    assert conflict.conflicting_selection_evidence == ("two different tokens observed",)


def test_same_token_has_local_meaning_in_different_choice_sets():
    first = choice_set("set-a")
    second = PresentedClosedChoiceSet(
        choice_set_ref="set-b",
        prompt="Choose one non-transition boundary proof.",
        options=(
            ClosedChoiceOption("1", "prove_non_transition", "Prove non-transition"),
            ClosedChoiceOption("2", "preserve_unknown", "Preserve unknown"),
        ),
        presentation_ref="presentation-b",
    )

    a = bind_closed_choice_selection(first, capture("1", "set-a"))
    b = bind_closed_choice_selection(second, capture("1", "set-b"))

    assert a.captured_token == b.captured_token == "1"
    assert a.bound_option_ref == "show_inventory"
    assert b.bound_option_ref == "prove_non_transition"
    assert a.exact_choice_set_fingerprint != b.exact_choice_set_fingerprint
    assert a.binding_id != b.binding_id


def test_binding_stops_before_goal_inquiry_authority_or_execution_transition():
    binding = bind_closed_choice_selection(choice_set(), capture("2"))
    data = closed_choice_selection_binding_json(binding)

    assert data["applied_to_goal"] is False
    assert data["inquiry_frontier_transition"] is False
    assert data["operator_authority_granted"] is False
    assert data["execution_authorized"] is False
    assert binding.bound_option_ref == "show_shape_audit"
    forbidden = str(data)
    assert "goal_transition_handoff" not in forbidden
    assert "inquiry_selection_handoff" not in forbidden
    assert "execution_handoff" not in forbidden
