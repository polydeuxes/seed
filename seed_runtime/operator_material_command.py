"""Bounded filesystem reads for the operator `/material` command."""

from __future__ import annotations

from dataclasses import dataclass
import os
import stat

from seed_runtime.material_availability import (
    MaterialIdentity,
    ProcessLocalMaterial,
    record_transient_material,
)
from seed_runtime.operator_command import OperatorCommandContext


MATERIAL_TARGET_READ_KIND = "operator.command.material_target_read"
MATERIAL_RELATED_KIND = "operator.command.material_related"
MATERIAL_REFUSED_KIND = "operator.command.material_refused"

DEFAULT_FILE_BYTE_BOUND = 64 * 1024 * 1024
DEFAULT_DIRECTORY_ENTRY_BOUND = 256


class OperatorMaterialCommandError(ValueError):
    """The material command's mechanical bounds are malformed."""


@dataclass(frozen=True)
class OperatorMaterialResult:
    target_kind: str
    read_event_id: str | None
    material_event_id: str | None
    material_identity: MaterialIdentity | None


def _exact_bound(name: str, value: int) -> int:
    if type(value) is not int or value < 0:
        raise OperatorMaterialCommandError(
            f"{name} must be an exact non-negative integer"
        )
    return value


def _stat_material(value: os.stat_result) -> dict[str, int]:
    return {
        "device": value.st_dev,
        "inode": value.st_ino,
        "mode": value.st_mode,
        "byte_count": value.st_size,
        "mtime_ns": value.st_mtime_ns,
    }


def _target_kind(mode: int) -> str:
    if stat.S_ISREG(mode):
        return "regular_file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symbolic_link"
    return "other"


class OperatorMaterialCommand:
    """Read one exact path without recursive expansion or partial holding."""

    def __init__(
        self,
        *,
        holder: ProcessLocalMaterial | None = None,
        file_byte_bound: int = DEFAULT_FILE_BYTE_BOUND,
        directory_entry_bound: int = DEFAULT_DIRECTORY_ENTRY_BOUND,
    ) -> None:
        self.holder = holder if holder is not None else ProcessLocalMaterial()
        if not isinstance(self.holder, ProcessLocalMaterial):
            raise OperatorMaterialCommandError(
                "material command requires a process-local material holder"
            )
        self.file_byte_bound = _exact_bound("file_byte_bound", file_byte_bound)
        self.directory_entry_bound = _exact_bound(
            "directory_entry_bound", directory_entry_bound
        )

    def _refuse(
        self,
        context: OperatorCommandContext,
        *,
        path: bytes,
        reason: str,
        failure_type: str | None = None,
        target_byte_count: int | None = None,
    ) -> OperatorMaterialResult:
        context.ledger.append(
            MATERIAL_REFUSED_KIND,
            context.workspace_id,
            {
                "command_id": context.command_id,
                "addressed_event_id": context.addressed_event_id,
                "path_bytes_hex": path.hex(),
                "reason": reason,
                "failure_type": failure_type,
                "target_byte_count": target_byte_count,
                "file_byte_bound": self.file_byte_bound,
                "directory_entry_bound": self.directory_entry_bound,
                "standing": "material occurrence not established",
                "authority": "unestablished",
                "mutates_cluster": False,
            },
            locality_id=context.locality_id,
        )
        return OperatorMaterialResult(
            target_kind="refused",
            read_event_id=None,
            material_event_id=None,
            material_identity=None,
        )

    def _read_directory(
        self,
        context: OperatorCommandContext,
        *,
        path: bytes,
        before: os.stat_result,
    ) -> OperatorMaterialResult:
        entries: list[dict[str, object]] = []
        complete = True
        try:
            with os.scandir(path) as scanned:
                for index, entry in enumerate(scanned):
                    if index >= self.directory_entry_bound:
                        complete = False
                        break
                    name = entry.name
                    if type(name) is not bytes:
                        raise OperatorMaterialCommandError(
                            "a byte path must yield exact byte entry names"
                        )
                    try:
                        entry_stat = entry.stat(follow_symlinks=False)
                    except OSError as exc:
                        entries.append(
                            {
                                "name_bytes_hex": name.hex(),
                                "target_kind": "Unknown",
                                "failure_type": type(exc).__name__,
                            }
                        )
                        continue
                    entries.append(
                        {
                            "name_bytes_hex": name.hex(),
                            "target_kind": _target_kind(entry_stat.st_mode),
                            "stat": _stat_material(entry_stat),
                        }
                    )
            after = os.lstat(path)
        except (OSError, OperatorMaterialCommandError) as exc:
            return self._refuse(
                context,
                path=path,
                reason="directory read did not complete under its boundary",
                failure_type=type(exc).__name__,
            )

        read = context.ledger.append(
            MATERIAL_TARGET_READ_KIND,
            context.workspace_id,
            {
                "command_id": context.command_id,
                "addressed_event_id": context.addressed_event_id,
                "path_bytes_hex": path.hex(),
                "target_kind": "directory",
                "stat_before": _stat_material(before),
                "stat_after": _stat_material(after),
                "same_stat_during_read": _stat_material(before)
                == _stat_material(after),
                "directory_entry_bound": self.directory_entry_bound,
                "entries_read": entries,
                "complete_under_entry_bound": complete,
                "recursive": False,
                "standing": "read",
                "authority": "unestablished",
                "unknowns": [
                    "what any entry represents remains Unknown",
                    *(
                        []
                        if complete
                        else ["entries beyond the exact read bound remain Unknown"]
                    ),
                ],
                "mutates_cluster": False,
            },
            locality_id=context.locality_id,
        )
        return OperatorMaterialResult(
            target_kind="directory",
            read_event_id=read.id,
            material_event_id=None,
            material_identity=None,
        )

    def _read_file(
        self,
        context: OperatorCommandContext,
        *,
        path: bytes,
        before: os.stat_result,
    ) -> OperatorMaterialResult:
        if before.st_size > self.file_byte_bound:
            return self._refuse(
                context,
                path=path,
                reason="regular file exceeds the exact process-local byte bound",
                target_byte_count=before.st_size,
            )

        flags = os.O_RDONLY
        flags |= getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(path, flags)
            try:
                opened = os.fstat(descriptor)
                exact_bytes = os.read(descriptor, self.file_byte_bound + 1)
                while len(exact_bytes) <= self.file_byte_bound:
                    part = os.read(
                        descriptor,
                        self.file_byte_bound + 1 - len(exact_bytes),
                    )
                    if not part:
                        break
                    exact_bytes += part
                after = os.fstat(descriptor)
            finally:
                os.close(descriptor)
        except OSError as exc:
            return self._refuse(
                context,
                path=path,
                reason="regular file read did not complete under its boundary",
                failure_type=type(exc).__name__,
            )

        if len(exact_bytes) > self.file_byte_bound:
            return self._refuse(
                context,
                path=path,
                reason="regular file exceeded the exact process-local byte bound while read",
                target_byte_count=len(exact_bytes),
            )
        if (
            not stat.S_ISREG(opened.st_mode)
            or _stat_material(before) != _stat_material(opened)
            or _stat_material(opened) != _stat_material(after)
            or len(exact_bytes) != after.st_size
        ):
            return self._refuse(
                context,
                path=path,
                reason="regular file identity or extent changed across the read boundary",
                target_byte_count=len(exact_bytes),
            )

        read = context.ledger.append(
            MATERIAL_TARGET_READ_KIND,
            context.workspace_id,
            {
                "command_id": context.command_id,
                "addressed_event_id": context.addressed_event_id,
                "path_bytes_hex": path.hex(),
                "target_kind": "regular_file",
                "stat": _stat_material(after),
                "file_byte_bound": self.file_byte_bound,
                "standing": "read",
                "authority": "unestablished",
                "mutates_cluster": False,
            },
            locality_id=context.locality_id,
        )
        identity = self.holder.hold(exact_bytes)
        material = record_transient_material(
            context.ledger,
            workspace_id=context.workspace_id,
            locality_id=context.locality_id,
            holder=self.holder,
            identity=identity,
            material_origin="system",
            occurrence_boundary=(
                f"filesystem read addressed by command occurrence {context.addressed_event_id}"
            ),
        )
        context.ledger.append(
            MATERIAL_RELATED_KIND,
            context.workspace_id,
            {
                "first_subject": read.id,
                "second_subject": material.id,
                "command_id": context.command_id,
                "addressed_event_id": context.addressed_event_id,
                "read_event_id": read.id,
                "material_occurrence_id": material.id,
                "standing": "related",
                "authority": "unestablished",
                "evidence_scope": (
                    "this exact filesystem read-to-material occurrence only"
                ),
                "mutates_cluster": False,
            },
            locality_id=context.locality_id,
        )
        return OperatorMaterialResult(
            target_kind="regular_file",
            read_event_id=read.id,
            material_event_id=material.id,
            material_identity=identity,
        )

    def __call__(self, context: OperatorCommandContext) -> OperatorMaterialResult:
        path = context.frame.arguments
        if not path:
            return self._refuse(
                context,
                path=path,
                reason="material command requires exact path bytes",
            )
        if b"\x00" in path:
            return self._refuse(
                context,
                path=path,
                reason="filesystem paths cannot contain a zero byte",
            )
        try:
            target_stat = os.lstat(path)
        except OSError as exc:
            return self._refuse(
                context,
                path=path,
                reason="addressed filesystem target was not read",
                failure_type=type(exc).__name__,
            )

        kind = _target_kind(target_stat.st_mode)
        if kind == "directory":
            return self._read_directory(context, path=path, before=target_stat)
        if kind == "regular_file":
            return self._read_file(context, path=path, before=target_stat)
        return self._refuse(
            context,
            path=path,
            reason=f"addressed filesystem target kind is {kind}",
            target_byte_count=target_stat.st_size,
        )
