"""Local-host mount classification for operator impact rendering."""

from __future__ import annotations

from collections.abc import Iterable

LOCAL_STORAGE_FILESYSTEM_TYPES = {
    "apfs",
    "bcachefs",
    "btrfs",
    "ext2",
    "ext3",
    "ext4",
    "exfat",
    "f2fs",
    "hfs",
    "hfsplus",
    "jfs",
    "ntfs",
    "reiserfs",
    "ufs",
    "vfat",
    "xfs",
    "zfs",
}

PSEUDO_FILESYSTEM_TYPES = {
    "autofs",
    "bdev",
    "binfmt_misc",
    "bpf",
    "cgroup",
    "cgroup2",
    "configfs",
    "debugfs",
    "devpts",
    "devtmpfs",
    "efivarfs",
    "fusectl",
    "hugetlbfs",
    "mqueue",
    "proc",
    "pstore",
    "ramfs",
    "rpc_pipefs",
    "securityfs",
    "sysfs",
    "tmpfs",
    "tracefs",
}

MOUNT_COLLAPSE_GROUP_ORDER = (
    "docker overlay mounts",
    "docker netns mounts",
    "system/pseudo mounts",
    "systemd credential mounts",
)

OPERATOR_RELEVANT_FUSE_FILESYSTEM_TYPES = {"fuse.mergerfs", "fuse.sshfs", "sshfs"}


def _normalized_values(values: Iterable[str]) -> set[str]:
    return {str(value).lower() for value in values}


def classify_mount_collapse_group(
    mount_point: str, devices: Iterable[str] = (), fs_types: Iterable[str] = ()
) -> str | None:
    """Classify noisy local-host mounts that --impact should collapse for operators.

    ``seed_runtime.local_host_mounts`` owns local-host mount classification policy;
    CLI code should use this result only to render the operator impact view.
    """

    normalized_types = _normalized_values(fs_types)
    normalized_devices = _normalized_values(devices)
    if mount_point.startswith("/run/credentials/"):
        return "systemd credential mounts"
    if ("overlay" in normalized_types and "/docker/overlay" in mount_point) or (
        "overlay" in normalized_devices and "/docker/overlay" in mount_point
    ):
        return "docker overlay mounts"
    if mount_point.startswith(("/run/docker/netns/", "/var/run/docker/netns/")):
        return "docker netns mounts"
    if is_operator_relevant_mount(mount_point, normalized_types):
        return None
    if normalized_types and normalized_types <= PSEUDO_FILESYSTEM_TYPES:
        return "system/pseudo mounts"
    return None


def is_operator_relevant_mount(mount_point: str, fs_types: Iterable[str] = ()) -> bool:
    """Return whether a mount should stay visible in --impact operator rendering.

    ``seed_runtime.local_host_mounts`` owns this local-host mount classification so
    the CLI remains responsible for text rendering rather than filesystem taxonomy.
    """

    normalized_types = _normalized_values(fs_types)
    return (
        mount_point == "/"
        or mount_point == "/boot/efi"
        or mount_point.startswith("/mnt/")
        or bool(normalized_types & OPERATOR_RELEVANT_FUSE_FILESYSTEM_TYPES)
        or bool(normalized_types & LOCAL_STORAGE_FILESYSTEM_TYPES)
    )


def mount_display_priority(
    mount_point: str, fs_types: Iterable[str] = ()
) -> tuple[int, str]:
    """Return deterministic sort priority for visible local-host impact mounts.

    ``seed_runtime.local_host_mounts`` owns the operator relevance ordering; CLI
    code should pass the returned key to rendering sorts.
    """

    normalized_types = _normalized_values(fs_types)
    if mount_point == "/":
        return (0, mount_point)
    if mount_point == "/boot/efi":
        return (1, mount_point)
    if mount_point.startswith("/mnt/"):
        return (2, mount_point)
    if normalized_types & OPERATOR_RELEVANT_FUSE_FILESYSTEM_TYPES:
        return (3, mount_point)
    if normalized_types & LOCAL_STORAGE_FILESYSTEM_TYPES:
        return (4, mount_point)
    return (5, mount_point)
