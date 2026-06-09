from seed_runtime.local_host_mounts import (
    MOUNT_COLLAPSE_GROUP_ORDER,
    classify_mount_collapse_group,
    mount_display_priority,
)


def test_local_host_mounts_owns_collapse_policy_for_operator_impact_rendering():
    assert (
        classify_mount_collapse_group(
            "/var/lib/docker/overlay2/a/merged", ["overlay"], ["overlay"]
        )
        == "docker overlay mounts"
    )
    assert (
        classify_mount_collapse_group("/run/docker/netns/abc", ["nsfs"], ["nsfs"])
        == "docker netns mounts"
    )
    assert (
        classify_mount_collapse_group("/proc", ["proc"], ["proc"])
        == "system/pseudo mounts"
    )
    assert (
        classify_mount_collapse_group(
            "/run/credentials/systemd-sysusers.service", ["ramfs"], ["ramfs"]
        )
        == "systemd credential mounts"
    )


# This test describes the ownership boundary: runtime classifies what remains
# visible, while scripts/seed_local.py only renders the returned grouping.
def test_local_host_mounts_owns_visible_mount_policy_for_operator_impact_rendering():
    assert classify_mount_collapse_group("/", ["/dev/sda1"], ["ext4"]) is None
    assert classify_mount_collapse_group("/boot/efi", ["/dev/sda15"], ["vfat"]) is None
    assert (
        classify_mount_collapse_group("/mnt/merged", ["mergerfs"], ["fuse.mergerfs"])
        is None
    )
    assert (
        classify_mount_collapse_group(
            "/mnt/node200/sda1", ["node200:/sda1"], ["fuse.sshfs"]
        )
        is None
    )
    assert classify_mount_collapse_group("/data", ["/dev/sdb1"], ["ext4"]) is None


def test_local_host_mounts_owns_visible_mount_display_priority():
    mounts = [
        ("/data", ["ext4"]),
        ("/mnt/node200/sda1", ["fuse.sshfs"]),
        ("/boot/efi", ["vfat"]),
        ("/mnt/merged", ["fuse.mergerfs"]),
        ("/", ["ext4"]),
    ]

    assert sorted(mounts, key=lambda item: mount_display_priority(*item)) == [
        ("/", ["ext4"]),
        ("/boot/efi", ["vfat"]),
        ("/mnt/merged", ["fuse.mergerfs"]),
        ("/mnt/node200/sda1", ["fuse.sshfs"]),
        ("/data", ["ext4"]),
    ]


def test_local_host_mounts_owns_collapse_group_order():
    assert MOUNT_COLLAPSE_GROUP_ORDER == (
        "docker overlay mounts",
        "docker netns mounts",
        "system/pseudo mounts",
        "systemd credential mounts",
    )
