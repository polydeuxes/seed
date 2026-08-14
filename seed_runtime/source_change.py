"""Bounded observation and change of source files.

This module supplies mechanics for changing another repository without letting
a guessed path or stale read overwrite current material.  Every edit names an
exact relative path and the exact material observed there.  All preconditions
are checked before the first file is replaced.

The mechanism does not decide what should change.  A caller must supply the
new bytes and the exact check command.  A successful write also does not imply
that the change is correct; the check result is returned as separate material.
"""

from __future__ import annotations

from dataclasses import dataclass
import difflib
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
from typing import Iterable, Sequence

from seed_runtime.material_availability import MaterialIdentity


class SourceChangeError(ValueError):
    """A source observation, edit, or check could not be performed as stated."""


def _relative_path(value: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise SourceChangeError("a source path must be a non-empty relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise SourceChangeError("a source path must remain beneath its declared root")
    return path


def _source_path(root: Path, relative_path: str) -> Path:
    relative = _relative_path(relative_path)
    candidate = root.joinpath(*relative.parts)
    walked = root
    for part in relative.parts:
        walked = walked / part
        if walked.is_symlink():
            raise SourceChangeError("a source path may not cross a symbolic link")
    resolved_root = root.resolve(strict=True)
    resolved = candidate.resolve(strict=True)
    if resolved.parent != resolved_root and resolved_root not in resolved.parents:
        raise SourceChangeError("a source path escaped its declared root")
    if not resolved.is_file():
        raise SourceChangeError(f"source path is not a regular file: {relative_path}")
    return resolved


@dataclass(frozen=True)
class SourceObservation:
    relative_path: str
    material: bytes
    identity: MaterialIdentity

    @classmethod
    def read(cls, root: Path, relative_path: str) -> "SourceObservation":
        path = _source_path(root, relative_path)
        material = path.read_bytes()
        return cls(
            relative_path=str(_relative_path(relative_path)),
            material=material,
            identity=MaterialIdentity.of(material),
        )


@dataclass(frozen=True)
class SourceEdit:
    relative_path: str
    expected: MaterialIdentity
    replacement: bytes

    def __post_init__(self) -> None:
        object.__setattr__(self, "relative_path", str(_relative_path(self.relative_path)))
        if not isinstance(self.expected, MaterialIdentity):
            raise SourceChangeError("a source edit requires its exact observed identity")
        if type(self.replacement) is not bytes:
            raise SourceChangeError("source replacement material must be exact bytes")

    @classmethod
    def from_observation(
        cls, observation: SourceObservation, replacement: bytes
    ) -> "SourceEdit":
        if not isinstance(observation, SourceObservation):
            raise SourceChangeError("a source edit requires an exact observation")
        return cls(
            relative_path=observation.relative_path,
            expected=observation.identity,
            replacement=replacement,
        )

    @property
    def replacement_identity(self) -> MaterialIdentity:
        return MaterialIdentity.of(self.replacement)


@dataclass(frozen=True)
class AppliedSourceEdit:
    relative_path: str
    before: MaterialIdentity
    after: MaterialIdentity


@dataclass(frozen=True)
class SourceCheckResult:
    argv: tuple[str, ...]
    returncode: int
    stdout: bytes
    stderr: bytes
    stdout_total_bytes: int
    stderr_total_bytes: int

    @property
    def passed(self) -> bool:
        return self.returncode == 0

    @property
    def stdout_complete(self) -> bool:
        return len(self.stdout) == self.stdout_total_bytes

    @property
    def stderr_complete(self) -> bool:
        return len(self.stderr) == self.stderr_total_bytes


def observe_source_files(
    root: str | os.PathLike[str], relative_paths: Iterable[str]
) -> tuple[SourceObservation, ...]:
    """Read only the exact source paths supplied by the caller."""

    source_root = Path(root)
    paths = tuple(relative_paths)
    if not paths:
        raise SourceChangeError("source observation requires at least one path")
    normalized = tuple(str(_relative_path(path)) for path in paths)
    if len(set(normalized)) != len(normalized):
        raise SourceChangeError("one source path may be observed only once per call")
    return tuple(SourceObservation.read(source_root, path) for path in normalized)


def render_source_diff(observation: SourceObservation, replacement: bytes) -> str:
    """Render a deterministic unified diff for one exact text observation."""

    if not isinstance(observation, SourceObservation):
        raise SourceChangeError("a source diff requires an exact observation")
    if type(replacement) is not bytes:
        raise SourceChangeError("source replacement material must be exact bytes")
    try:
        before = observation.material.decode("utf-8").splitlines(keepends=True)
        after = replacement.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError as exc:
        raise SourceChangeError("source diff material must be UTF-8 text") from exc
    path = observation.relative_path
    return "".join(
        difflib.unified_diff(before, after, fromfile=f"a/{path}", tofile=f"b/{path}")
    )


def apply_source_edits(
    root: str | os.PathLike[str], edits: Iterable[SourceEdit]
) -> tuple[AppliedSourceEdit, ...]:
    """Replace exact files after validating every preimage.

    Files are staged beside their destinations before replacement.  The
    precondition check covers the complete supplied set; filesystem replacement
    remains one file at a time and is not represented as a multi-file atomic
    transaction.
    """

    source_root = Path(root)
    supplied = tuple(edits)
    if not supplied:
        raise SourceChangeError("a source change requires at least one edit")
    if not all(isinstance(edit, SourceEdit) for edit in supplied):
        raise SourceChangeError("every source change must be a SourceEdit")
    paths = tuple(edit.relative_path for edit in supplied)
    if len(set(paths)) != len(paths):
        raise SourceChangeError("one source path may be changed only once per call")

    checked: list[tuple[SourceEdit, Path, SourceObservation]] = []
    for edit in supplied:
        observation = SourceObservation.read(source_root, edit.relative_path)
        if observation.identity != edit.expected:
            raise SourceChangeError(
                f"source changed after observation: {edit.relative_path}"
            )
        checked.append((edit, _source_path(source_root, edit.relative_path), observation))

    staged: list[tuple[Path, Path]] = []
    try:
        for edit, destination, _observation in checked:
            descriptor, temporary = tempfile.mkstemp(
                prefix=f".{destination.name}.",
                suffix=".seed-change",
                dir=destination.parent,
            )
            temporary_path = Path(temporary)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(edit.replacement)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temporary_path, destination.stat().st_mode)
            staged.append((temporary_path, destination))
        expected_by_path = {
            checked_path: observation.identity
            for _edit, checked_path, observation in checked
        }
        for _temporary, destination in staged:
            expected = expected_by_path[destination]
            current = MaterialIdentity.of(destination.read_bytes())
            if current != expected:
                raise SourceChangeError(
                    f"source changed while replacements were staged: "
                    f"{destination.relative_to(source_root.resolve(strict=True))}"
                )
        for temporary, destination in staged:
            os.replace(temporary, destination)
    finally:
        for temporary, _destination in staged:
            if temporary.exists():
                temporary.unlink()

    return tuple(
        AppliedSourceEdit(
            relative_path=edit.relative_path,
            before=observation.identity,
            after=edit.replacement_identity,
        )
        for edit, _destination, observation in checked
    )


def run_source_check(
    root: str | os.PathLike[str],
    argv: Sequence[str],
    *,
    timeout_seconds: float = 60.0,
    max_output_bytes: int = 1_000_000,
) -> SourceCheckResult:
    """Run one explicit command without a shell and bound returned output.

    Each stream retains its total extent.  If it exceeds ``max_output_bytes``,
    the returned prefix is explicitly incomplete rather than represented as the
    complete stream.
    """

    command = tuple(argv)
    if not command or not all(isinstance(part, str) and part for part in command):
        raise SourceChangeError("a source check requires exact non-empty arguments")
    if timeout_seconds <= 0:
        raise SourceChangeError("a source check timeout must be positive")
    if type(max_output_bytes) is not int or max_output_bytes < 0:
        raise SourceChangeError("a source check output boundary must be non-negative")
    with tempfile.TemporaryFile() as stdout_stream, tempfile.TemporaryFile() as stderr_stream:
        completed = subprocess.run(
            command,
            cwd=Path(root).resolve(strict=True),
            stdin=subprocess.DEVNULL,
            stdout=stdout_stream,
            stderr=stderr_stream,
            shell=False,
            timeout=timeout_seconds,
            check=False,
        )
        stdout_total = stdout_stream.tell()
        stderr_total = stderr_stream.tell()
        stdout_stream.seek(0)
        stderr_stream.seek(0)
        stdout = stdout_stream.read(max_output_bytes)
        stderr = stderr_stream.read(max_output_bytes)
    return SourceCheckResult(
        argv=command,
        returncode=completed.returncode,
        stdout=stdout,
        stderr=stderr,
        stdout_total_bytes=stdout_total,
        stderr_total_bytes=stderr_total,
    )
