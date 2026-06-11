from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.state_summary_views import build_operator_state_summary

NOW = datetime(2026, 6, 4, 12, 0, tzinfo=timezone.utc)


def _fact(
    fact_id: str,
    subject: str,
    predicate: str,
    value: object,
    *,
    dimensions: dict[str, str] | None = None,
) -> Fact:
    return Fact(
        id=fact_id,
        subject_id=subject,
        predicate=predicate,
        value=value,
        source_type="imported",
        confidence=0.91,
        observed_at=NOW,
        evidence_ids=["evidence_1"],
        dimensions=dimensions or {},
    )


def _project(*facts: Fact):
    ledger = EventLedger()
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(ledger).project("ws")


def test_operator_state_summary_can_be_built_without_cli_parsing():
    state = _project(_fact("fact_os", "node115", "os", "linux"))

    summary = build_operator_state_summary(state)

    assert summary["entity_count"] == 1
    assert summary["fact_count"] == 1
    assert summary["availability"] == {"up": 0, "down": 0, "unknown": 1}
    assert summary["top_entities"] == [
        {"name": "node115", "alias_count": 0, "fact_count": 1}
    ]


def test_operator_state_summary_preserves_availability_and_alias_semantics():
    state = _project(
        _fact("fact_host_alias", "node115", "alias", "192.168.254.115"),
        _fact(
            "fact_host_observed",
            "node115",
            "local_observation_status",
            "observed",
        ),
        _fact(
            "fact_endpoint_up",
            "192.168.254.115:9100",
            "availability_status",
            "up",
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["entity_count"] == 2
    assert summary["availability"] == {"up": 1, "down": 0, "unknown": 1}
    assert {
        entity["name"]: entity["alias_count"] for entity in summary["top_entities"]
    } == {
        "node115": 1,
        "192.168.254.115:9100": 0,
    }


def test_operator_state_summary_filters_runtime_pseudo_filesystems_only_from_summary():
    state = _project(
        _fact(
            "fact_root_free",
            "node115:9100",
            "filesystem_free_bytes",
            40,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
        _fact(
            "fact_root_total",
            "node115:9100",
            "filesystem_total_bytes",
            100,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
        _fact(
            "fact_runtime_free",
            "node115:9100",
            "filesystem_free_bytes",
            4,
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ),
        _fact(
            "fact_runtime_total",
            "node115:9100",
            "filesystem_total_bytes",
            10,
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["measurement_current_sample_count"] == 4
    assert summary["fact_count"] == 4
    assert summary["filesystems"] == [
        {
            "host": "node115:9100",
            "mountpoint": "/",
            "free": 40,
            "fstype": "ext4",
            "total": 100,
        }
    ]
    assert (
        state.get_best_fact(
            "node115:9100",
            "filesystem_free_bytes",
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ).value
        == 4
    )
    assert (
        state.get_best_fact(
            "node115:9100",
            "filesystem_total_bytes",
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ).value
        == 10
    )
    support = state.get_fact_support(
        "node115:9100",
        "filesystem_free_bytes",
        dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
    )
    assert support is not None
    assert support.value == 4
    assert support.supporting_fact_ids == ["fact_runtime_free"]


def test_operator_state_summary_prioritizes_operator_relevant_filesystem_order():
    state = _project(
        _fact(
            "fact_mnt_free",
            "node115:9100",
            "filesystem_free_bytes",
            200,
            dimensions={
                "mountpoint": "/mnt/merged",
                "device": "mergerfs",
                "fstype": "fuse.mergerfs",
            },
        ),
        _fact(
            "fact_mnt_total",
            "node115:9100",
            "filesystem_total_bytes",
            400,
            dimensions={
                "mountpoint": "/mnt/merged",
                "device": "mergerfs",
                "fstype": "fuse.mergerfs",
            },
        ),
        _fact(
            "fact_boot_free",
            "node115:9100",
            "filesystem_free_bytes",
            20,
            dimensions={"mountpoint": "/boot", "device": "/dev/sda2", "fstype": "ext4"},
        ),
        _fact(
            "fact_boot_total",
            "node115:9100",
            "filesystem_total_bytes",
            50,
            dimensions={"mountpoint": "/boot", "device": "/dev/sda2", "fstype": "ext4"},
        ),
        _fact(
            "fact_root_free",
            "node115:9100",
            "filesystem_free_bytes",
            40,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
        _fact(
            "fact_root_total",
            "node115:9100",
            "filesystem_total_bytes",
            100,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
    )

    summary = build_operator_state_summary(state)

    assert [filesystem["mountpoint"] for filesystem in summary["filesystems"]] == [
        "/",
        "/mnt/merged",
        "/boot",
    ]


def _filesystem_facts(
    subject: str,
    mountpoint: str,
    *,
    free: int,
    total: int,
    device: str = "/dev/sda1",
    fstype: str = "ext4",
    prefix: str | None = None,
) -> tuple[Fact, Fact]:
    fact_prefix = prefix or f"{subject}_{mountpoint}".replace(":", "_").replace("/", "_")
    dimensions = {"mountpoint": mountpoint, "device": device, "fstype": fstype}
    return (
        _fact(
            f"{fact_prefix}_free",
            subject,
            "filesystem_free_bytes",
            free,
            dimensions=dimensions,
        ),
        _fact(
            f"{fact_prefix}_total",
            subject,
            "filesystem_total_bytes",
            total,
            dimensions=dimensions,
        ),
    )


def test_operator_state_summary_groups_repeated_mount_visibility_by_mountpoint():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node100_shared",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=20,
            total=100,
            device="/dev/mapper/compat205",
            prefix="node101_shared",
        ),
        *_filesystem_facts(
            "node200:9100",
            "/mnt/node205/sda1",
            free=30,
            total=100,
            device="server:/legacy/node205/sda1",
            prefix="node200_shared",
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["cluster_mount_groups"] == [
        {
            "mountpoint": "/mnt/node205/sda1",
            "visible_endpoint_count": 3,
            "visible_endpoints": ["node100:9100", "node101:9100", "node200:9100"],
        }
    ]


def test_operator_state_summary_mount_grouping_preserves_filesystem_facts_and_measurements():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            prefix="node100_shared_preserved",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=20,
            total=100,
            prefix="node101_shared_preserved",
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["fact_count"] == 4
    assert summary["measurement_current_sample_count"] == 4
    assert len(summary["filesystems"]) == 2
    assert {
        (filesystem["host"], filesystem["mountpoint"], filesystem["free"])
        for filesystem in summary["filesystems"]
    } == {
        ("node100:9100", "/mnt/node205/sda1", 10),
        ("node101:9100", "/mnt/node205/sda1", 20),
    }
    assert (
        state.get_best_fact(
            "node101:9100",
            "filesystem_free_bytes",
            dimensions={
                "mountpoint": "/mnt/node205/sda1",
                "device": "/dev/sda1",
                "fstype": "ext4",
            },
        ).value
        == 20
    )


def test_operator_state_summary_mount_grouping_does_not_imply_ownership_or_identity():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node100_no_ownership",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=20,
            total=100,
            device="/dev/sdb1",
            prefix="node101_no_ownership",
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["cluster_mount_groups"] == [
        {
            "mountpoint": "/mnt/node205/sda1",
            "visible_endpoint_count": 2,
            "visible_endpoints": ["node100:9100", "node101:9100"],
        }
    ]
    # Grouped mount visibility is not shared storage identity and not ownership.
    assert "owner" not in summary["cluster_mount_groups"][0]
    assert "storage_identity" not in summary["cluster_mount_groups"][0]
    assert all("ownership" not in fact.predicate for fact in state.facts.values())
    assert all("storage_identity" not in fact.predicate for fact in state.facts.values())


def test_operator_state_summary_distinct_mountpaths_remain_distinct_groups():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            prefix="node100_node205",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=20,
            total=100,
            prefix="node101_node205",
        ),
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node200/sda1",
            free=30,
            total=200,
            prefix="node100_node200",
        ),
        *_filesystem_facts(
            "node200:9100",
            "/mnt/node200/sda1",
            free=40,
            total=200,
            prefix="node200_node200",
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["cluster_mount_groups"] == [
        {
            "mountpoint": "/mnt/node200/sda1",
            "visible_endpoint_count": 2,
            "visible_endpoints": ["node100:9100", "node200:9100"],
        },
        {
            "mountpoint": "/mnt/node205/sda1",
            "visible_endpoint_count": 2,
            "visible_endpoints": ["node100:9100", "node101:9100"],
        },
    ]
