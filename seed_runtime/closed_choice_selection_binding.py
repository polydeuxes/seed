"""Read-only binding for a token selected from one exact closed choice set."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Iterable

CONVENTION = "closed_choice_selection_binding_v1"
BOUNDARY_NOTES = (
    "Selection binding is not a goal transition.",
    "A selection token has only local meaning inside the exact presented choice set.",
    "A bound option is not operator authority, inquiry selection, execution, or authorization.",
    "This projection stops before applying the selected option to any operator goal or inquiry frontier.",
)


class ClosedChoiceSelectionBindingError(ValueError):
    pass


def _refs(values: Iterable[str] = ()) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if value}))


def _stable(prefix: str, payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return prefix + ":" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class ClosedChoiceOption:
    token: str
    option_ref: str
    presented_label: str
    presented_detail: str = ""

    def __post_init__(self) -> None:
        if not self.token:
            raise ClosedChoiceSelectionBindingError("closed choice option token is required")
        if not self.option_ref:
            raise ClosedChoiceSelectionBindingError("closed choice option_ref is required")


@dataclass(frozen=True)
class PresentedClosedChoiceSet:
    choice_set_ref: str
    prompt: str
    options: tuple[ClosedChoiceOption, ...]
    presentation_ref: str = ""
    provenance: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.choice_set_ref:
            raise ClosedChoiceSelectionBindingError("choice_set_ref is required")
        tokens = [option.token for option in self.options]
        if len(tokens) != len(set(tokens)):
            raise ClosedChoiceSelectionBindingError("choice set tokens must be unique inside one exact set")

    @property
    def exact_choice_set_fingerprint(self) -> str:
        return _stable(
            "closed-choice-set",
            {
                "choice_set_ref": self.choice_set_ref,
                "prompt": self.prompt,
                "options": [asdict(option) for option in self.options],
                "presentation_ref": self.presentation_ref,
                "convention": CONVENTION,
            },
        )


@dataclass(frozen=True)
class OperatorSelectionTokenCapture:
    capture_ref: str
    choice_set_ref: str
    captured_token: str
    provenance: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()


@dataclass(frozen=True)
class ClosedChoiceSelectionBinding:
    artifact_type: str
    binding_id: str
    choice_set_ref: str
    exact_choice_set_fingerprint: str
    presented_prompt: str
    presented_options: tuple[ClosedChoiceOption, ...]
    token_capture_ref: str
    captured_token: str
    binding_state: str
    binding_reason: str
    bound_option_ref: str | None
    bound_option_label: str | None
    unsupported_selection_evidence: tuple[str, ...]
    unknown_selection_evidence: tuple[str, ...]
    conflicting_selection_evidence: tuple[str, ...]
    applied_to_goal: bool = False
    inquiry_frontier_transition: bool = False
    operator_authority_granted: bool = False
    execution_authorized: bool = False
    read_only: bool = True
    writes_event_ledger: bool = False
    mutates_cluster: bool = False
    boundary_notes: tuple[str, ...] = BOUNDARY_NOTES
    binding_convention: str = CONVENTION

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        for key, value in data.items():
            if isinstance(value, tuple):
                data[key] = list(value)
        return data


def bind_closed_choice_selection(
    choice_set: PresentedClosedChoiceSet,
    token_capture: OperatorSelectionTokenCapture,
    *,
    unsupported_selection_evidence: tuple[str, ...] = (),
    unknown_selection_evidence: tuple[str, ...] = (),
    conflicting_selection_evidence: tuple[str, ...] = (),
) -> ClosedChoiceSelectionBinding:
    """Bind a captured token only against the exact presented closed choice set."""
    if token_capture.choice_set_ref != choice_set.choice_set_ref:
        raise ClosedChoiceSelectionBindingError("selection token capture references a different choice set")

    options_by_token = {option.token: option for option in choice_set.options}
    all_unknowns = _refs((*choice_set.unknowns, *token_capture.unknowns, *unknown_selection_evidence))
    all_conflicts = _refs((*choice_set.conflicts, *token_capture.conflicts, *conflicting_selection_evidence))
    unsupported = _refs(unsupported_selection_evidence)

    bound = options_by_token.get(token_capture.captured_token)
    state = "bound"
    reason = "captured_token_belongs_to_exact_choice_set"
    if all_conflicts:
        state = "conflict"
        reason = "conflicting_selection_evidence_preserved"
        bound = None
    elif bound is None:
        state = "unsupported"
        reason = "captured_token_not_in_exact_choice_set"
        unsupported = _refs((*unsupported, f"unsupported token: {token_capture.captured_token}"))
    elif all_unknowns:
        state = "unknown"
        reason = "selection_evidence_unknown_preserved"
        bound = None

    payload = {
        "choice_set_ref": choice_set.choice_set_ref,
        "choice_set_fingerprint": choice_set.exact_choice_set_fingerprint,
        "capture_ref": token_capture.capture_ref,
        "captured_token": token_capture.captured_token,
        "state": state,
        "reason": reason,
        "bound_option_ref": bound.option_ref if bound else None,
        "unsupported": unsupported,
        "unknowns": all_unknowns,
        "conflicts": all_conflicts,
        "convention": CONVENTION,
    }
    return ClosedChoiceSelectionBinding(
        "ClosedChoiceSelectionBinding",
        _stable("closed-choice-selection-binding", payload),
        choice_set.choice_set_ref,
        choice_set.exact_choice_set_fingerprint,
        choice_set.prompt,
        choice_set.options,
        token_capture.capture_ref,
        token_capture.captured_token,
        state,
        reason,
        bound.option_ref if bound else None,
        bound.presented_label if bound else None,
        unsupported,
        all_unknowns,
        all_conflicts,
    )


def closed_choice_selection_binding_json(binding: ClosedChoiceSelectionBinding) -> dict[str, object]:
    return binding.to_json_dict()
