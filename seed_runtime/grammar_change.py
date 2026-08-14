"""Exact current and proposed machine-grammar material."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Sequence

from seed_runtime.source_change import (
    AppliedSourceEdit,
    SourceChangeError,
    SourceCheckResult,
    SourceEdit,
    SourceObservation,
    apply_source_edits,
    observe_source_files,
    render_source_diff,
    run_source_check,
)


DEFAULT_GRAMMAR_PATH = "book_of_seed/grammar.json"


class GrammarChangeError(ValueError):
    """Machine-grammar material could not be held or changed exactly."""


@dataclass(frozen=True)
class GrammarChange:
    current: SourceObservation
    proposed: bytes
    edit: SourceEdit
    difference: str


def _grammar_object(material: bytes) -> dict:
    if type(material) is not bytes:
        raise GrammarChangeError("machine grammar must be exact bytes")
    try:
        value = json.loads(material.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GrammarChangeError("machine grammar must be one UTF-8 JSON object") from exc
    if type(value) is not dict:
        raise GrammarChangeError("machine grammar must be one UTF-8 JSON object")
    return value


def observe_grammar(
    root: str | os.PathLike[str],
    *,
    relative_path: str = DEFAULT_GRAMMAR_PATH,
) -> SourceObservation:
    """Observe one exact machine-grammar file and refuse malformed material."""

    try:
        observed = observe_source_files(root, (relative_path,))[0]
    except SourceChangeError as exc:
        raise GrammarChangeError(str(exc)) from exc
    _grammar_object(observed.material)
    return observed


def propose_grammar_change(
    current: SourceObservation,
    proposed: bytes,
) -> GrammarChange:
    """Hold current and proposed grammar separately and render their difference."""

    if not isinstance(current, SourceObservation):
        raise GrammarChangeError("a grammar change requires one exact current observation")
    _grammar_object(current.material)
    _grammar_object(proposed)
    try:
        edit = SourceEdit.from_observation(current, proposed)
        difference = render_source_diff(current, proposed)
    except SourceChangeError as exc:
        raise GrammarChangeError(str(exc)) from exc
    return GrammarChange(
        current=current,
        proposed=proposed,
        edit=edit,
        difference=difference,
    )


def apply_grammar_change(
    root: str | os.PathLike[str],
    change: GrammarChange,
) -> AppliedSourceEdit:
    """Replace only the exact grammar observation carried by ``change``."""

    if not isinstance(change, GrammarChange):
        raise GrammarChangeError("grammar replacement requires one exact change")
    try:
        return apply_source_edits(root, (change.edit,))[0]
    except SourceChangeError as exc:
        raise GrammarChangeError(str(exc)) from exc


def run_grammar_check(
    root: str | os.PathLike[str],
    argv: Sequence[str],
    *,
    timeout_seconds: float = 60.0,
    max_output_bytes: int = 1_000_000,
) -> SourceCheckResult:
    """Return a deterministic check result without declaring the change correct."""

    try:
        return run_source_check(
            root,
            argv,
            timeout_seconds=timeout_seconds,
            max_output_bytes=max_output_bytes,
        )
    except SourceChangeError as exc:
        raise GrammarChangeError(str(exc)) from exc
