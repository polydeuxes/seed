"""Exact current and proposed machine-grammar material."""

from __future__ import annotations

from dataclasses import dataclass
import difflib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile
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


@dataclass(frozen=True)
class GrammarCreation:
    source_root: str
    source_root_device: int
    source_root_inode: int
    relative_path: str
    proposed: bytes
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


def _new_grammar_path(root: Path, relative_path: str) -> tuple[Path, Path]:
    if type(relative_path) is not str or not relative_path:
        raise GrammarChangeError("a grammar path must be an exact relative path")
    relative = PurePosixPath(relative_path)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise GrammarChangeError("a grammar path must remain beneath its repository")
    exact_root = root.resolve(strict=True)
    parent = exact_root
    for part in relative.parts[:-1]:
        parent = parent / part
        if parent.is_symlink():
            raise GrammarChangeError("a grammar path may not cross a symbolic link")
    try:
        exact_parent = parent.resolve(strict=True)
    except OSError as exc:
        raise GrammarChangeError("a grammar parent path must already exist") from exc
    if exact_parent != exact_root and exact_root not in exact_parent.parents:
        raise GrammarChangeError("a grammar path escaped its repository")
    destination = exact_parent / relative.name
    if destination.exists() or destination.is_symlink():
        raise GrammarChangeError("the proposed grammar path already exists")
    return exact_root, destination


def propose_grammar_creation(
    root: str | os.PathLike[str],
    proposed: bytes,
    *,
    relative_path: str = DEFAULT_GRAMMAR_PATH,
) -> GrammarCreation:
    """Hold the first machine grammar for an exact repository and absent path."""

    _grammar_object(proposed)
    exact_root, _destination = _new_grammar_path(Path(root), relative_path)
    root_stat = exact_root.stat()
    rendered = proposed.decode("utf-8").splitlines(keepends=True)
    difference = "".join(
        difflib.unified_diff(
            [],
            rendered,
            fromfile="/dev/null",
            tofile=f"b/{relative_path}",
        )
    )
    return GrammarCreation(
        source_root=str(exact_root),
        source_root_device=root_stat.st_dev,
        source_root_inode=root_stat.st_ino,
        relative_path=relative_path,
        proposed=proposed,
        difference=difference,
    )


def apply_grammar_creation(
    root: str | os.PathLike[str],
    creation: GrammarCreation,
) -> SourceObservation:
    """Create one still-absent grammar without an overwrite window."""

    if not isinstance(creation, GrammarCreation):
        raise GrammarChangeError("grammar creation requires one exact proposal")
    exact_root, destination = _new_grammar_path(Path(root), creation.relative_path)
    root_stat = exact_root.stat()
    if (
        str(exact_root) != creation.source_root
        or root_stat.st_dev != creation.source_root_device
        or root_stat.st_ino != creation.source_root_inode
    ):
        raise GrammarChangeError("a grammar creation belongs to another repository")

    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".seed-grammar",
        dir=destination.parent,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(creation.proposed)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination, follow_symlinks=False)
        except FileExistsError as exc:
            raise GrammarChangeError(
                "the proposed grammar path appeared after observation"
            ) from exc
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    return observe_grammar(
        exact_root,
        relative_path=creation.relative_path,
    )


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
