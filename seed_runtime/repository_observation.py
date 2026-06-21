"""Read-only generic repository-state observation providers."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RepositoryObservation:
    repository_path: str
    repository_vcs: str | None
    repository_head_commit: str | None
    repository_branch: str | None
    repository_dirty: bool | None
    repository_untracked_count: int | None
    repository_modified_count: int | None
    repository_staged_count: int | None
    repository_remote_present: bool | None
    repository_status_available: bool
    reason: str | None = None
    writes_event_ledger: bool = False
    mutates_cluster: bool = False

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "repository_path": self.repository_path,
            "repository_vcs": self.repository_vcs,
            "repository_head_commit": self.repository_head_commit,
            "repository_branch": self.repository_branch,
            "repository_dirty": self.repository_dirty,
            "repository_untracked_count": self.repository_untracked_count,
            "repository_modified_count": self.repository_modified_count,
            "repository_staged_count": self.repository_staged_count,
            "repository_remote_present": self.repository_remote_present,
            "repository_status_available": self.repository_status_available,
            "reason": self.reason,
            "writes_event_ledger": self.writes_event_ledger,
            "mutates_cluster": self.mutates_cluster,
        }


class RepositoryObservationProvider:
    """Protocol-like base for read-only repository state observers."""

    def observe(self, repository_path: str | Path) -> RepositoryObservation:
        raise NotImplementedError


class GitRepositoryObservationProvider(RepositoryObservationProvider):
    """Observe repository state for an arbitrary git-backed path without writes."""

    def __init__(self, git_binary: str = "git") -> None:
        self.git_binary = git_binary

    def observe(self, repository_path: str | Path) -> RepositoryObservation:
        path = Path(repository_path).expanduser().resolve()
        if shutil.which(self.git_binary) is None:
            return _unavailable(path, "git executable is unavailable")
        if not _git_ok(self.git_binary, path, "rev-parse", "--is-inside-work-tree"):
            return _unavailable(path, "path is not a git work tree")

        head = _git_text(self.git_binary, path, "rev-parse", "HEAD")
        branch = _git_text(self.git_binary, path, "branch", "--show-current")
        remote = _git_text(self.git_binary, path, "remote")
        status = _git_text(self.git_binary, path, "status", "--porcelain=v1")
        if head is None or status is None:
            return _unavailable(path, "git status is unavailable", vcs="git")
        staged = modified = untracked = 0
        for line in status.splitlines():
            if line.startswith("??"):
                untracked += 1
                continue
            index = line[0]
            worktree = line[1] if len(line) > 1 else " "
            if index != " ":
                staged += 1
            if worktree != " ":
                modified += 1
        return RepositoryObservation(
            repository_path=str(path),
            repository_vcs="git",
            repository_head_commit=head.strip() or None,
            repository_branch=(branch or "").strip() or None,
            repository_dirty=bool(status.strip()),
            repository_untracked_count=untracked,
            repository_modified_count=modified,
            repository_staged_count=staged,
            repository_remote_present=bool((remote or "").strip()),
            repository_status_available=True,
        )


def observe_repository(repository_path: str | Path) -> RepositoryObservation:
    return GitRepositoryObservationProvider().observe(repository_path)


def observe_repository_state(repository_path: str | Path) -> RepositoryObservation:
    return observe_repository(repository_path)


def repository_observation_json(observation: RepositoryObservation) -> dict[str, Any]:
    return observation.to_json_dict()


def format_repository_observation(observation: RepositoryObservation) -> str:
    dirty = _value(observation.repository_dirty)
    lines = [
        "Repository Observation",
        f"  repository path: {observation.repository_path}",
        f"  repository vcs: {observation.repository_vcs or 'unknown'}",
        f"  status available: {'yes' if observation.repository_status_available else 'no'}",
    ]
    if observation.reason:
        lines.append(f"  reason: {observation.reason}")
    lines.extend(
        [
            f"  head commit: {observation.repository_head_commit or 'unknown'}",
            f"  branch: {observation.repository_branch or 'unknown'}",
            f"  dirty: {dirty}",
            f"  staged count: {_value(observation.repository_staged_count)}",
            f"  modified count: {_value(observation.repository_modified_count)}",
            f"  untracked count: {_value(observation.repository_untracked_count)}",
            f"  remote present: {_value(observation.repository_remote_present)}",
        ]
    )
    return "\n".join(lines)


def _git_text(git: str, cwd: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(
            [git, *args], cwd=cwd, text=True, capture_output=True, check=False
        )
    except (OSError, ValueError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def _git_ok(git: str, cwd: Path, *args: str) -> bool:
    text = _git_text(git, cwd, *args)
    return text is not None and text.strip() == "true"


def _unavailable(
    path: Path, reason: str, vcs: str | None = None
) -> RepositoryObservation:
    return RepositoryObservation(
        repository_path=str(path),
        repository_vcs=vcs,
        repository_head_commit=None,
        repository_branch=None,
        repository_dirty=None,
        repository_untracked_count=None,
        repository_modified_count=None,
        repository_staged_count=None,
        repository_remote_present=None,
        repository_status_available=False,
        reason=reason,
    )


def _value(value: object) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def repository_state_observation_json(
    observation: RepositoryObservation,
) -> dict[str, Any]:
    return repository_observation_json(observation)


def format_repository_state_observation(observation: RepositoryObservation) -> str:
    return format_repository_observation(observation)
