from datetime import datetime, timezone

from seed_runtime.events import EventLedger
from seed_runtime.facts import Fact
from seed_runtime.models import Entity
from seed_runtime.serialization import to_plain
from seed_runtime.state import StateProjector
from seed_runtime.state_summary_views import (
    build_operator_state_summary,
    storage_state_projection,
)

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


def _project(*facts: Fact, entities: list[Entity] | None = None):
    ledger = EventLedger()
    for entity in entities or []:
        ledger.append("entity.upserted", "ws", {"entity": to_plain(entity)})
    for fact in facts:
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    return StateProjector(ledger).project("ws")


def test_operator_state_summary_can_be_built_without_cli_parsing():
    state = _project(_fact("fact_os", "example_host", "os", "linux"))

    summary = build_operator_state_summary(state)

    assert summary["entity_count"] == 1
    assert summary["fact_count"] == 1
    assert "availability" not in summary
    assert "availability_by_scope" not in summary
    assert "top_entities" not in summary
    assert "top_entities_by_kind" not in summary


def test_operator_state_summary_preserves_alias_state_without_availability_summary():
    state = _project(
        _fact("fact_host_alias", "example_host", "alias", "192.0.2.115"),
        _fact(
            "fact_host_observed",
            "example_host",
            "local_observation_status",
            "observed",
        ),
        _fact(
            "fact_endpoint_up",
            "192.0.2.115:9100",
            "availability_status",
            "up",
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["entity_count"] == 2
    assert "availability" not in summary
    assert "availability_by_scope" not in summary
    assert "top_entities" not in summary
    assert "top_entities_by_kind" not in summary
    assert "192.0.2.115:9100" in state.current_entity_types
    assert state.get_current_entity_types("192.0.2.115:9100") == ["endpoint"]
    assert (
        state.get_best_fact("192.0.2.115:9100", "availability_status").value
        == "up"
    )


def test_operator_state_summary_counts_durable_and_measurement_facts_without_top_entities():
    endpoint_measurements = [
        _fact(
            f"fact_endpoint_filesystem_free_{index}",
            "192.168.254.116:9100",
            "filesystem_free_bytes",
            1000 + index,
            dimensions={
                "mountpoint": f"/mnt/volume{index}",
                "device": f"/dev/sd{index}",
                "fstype": "ext4",
            },
        )
        for index in range(8)
    ]
    state = _project(
        *endpoint_measurements,
        _fact(
            "fact_endpoint_up",
            "192.168.254.116:9100",
            "availability_status",
            "up",
        ),
        _fact("fact_host_os", "example_host", "os", "linux"),
    )

    summary = build_operator_state_summary(state)

    assert summary["fact_count"] == 11
    assert summary["durable_fact_count"] == 1
    assert summary["measurement_current_sample_count"] == 10
    assert "availability" not in summary
    assert "availability_by_scope" not in summary
    assert "top_entities" not in summary
    assert "top_entities_by_kind" not in summary
    assert (
        state.get_best_fact(
            "192.168.254.116:9100",
            "filesystem_free_bytes",
            dimensions={
                "mountpoint": "/mnt/volume0",
                "device": "/dev/sd0",
                "fstype": "ext4",
            },
        ).value
        == 1000
    )
    assert (
        state.get_best_fact("192.168.254.116:9100", "availability_status").value
        == "up"
    )


def test_operator_state_summary_keeps_availability_facts_out_of_summary():
    state = _project(
        _fact(
            "fact_endpoint_down",
            "10.0.0.1:9100",
            "availability_status",
            "down",
        ),
        _fact("fact_host_os", "example_host", "os", "linux"),
        _fact("fact_host_availability", "example_host", "availability_status", "up"),
    )

    summary = build_operator_state_summary(state)

    assert state.get_best_fact("10.0.0.1:9100", "availability_status").value == "down"
    assert "top_entities" not in summary
    assert "top_entities_by_kind" not in summary
    assert "availability" not in summary
    assert "availability_by_scope" not in summary

def test_operator_state_summary_no_longer_summarizes_endpoint_availability_counts():
    state = _project(
        _fact("fact_endpoint_up", "10.0.0.1:9100", "availability_status", "up"),
        _fact("fact_endpoint_down", "10.0.0.2:9100", "availability_status", "down"),
        entities=[Entity(id="10.0.0.3:9100", kind="endpoint", name="10.0.0.3:9100")],
    )

    summary = build_operator_state_summary(state)

    assert state.get_current_entity_types("10.0.0.1:9100") == ["endpoint"]
    assert state.get_current_entity_types("10.0.0.2:9100") == ["endpoint"]
    assert state.get_current_entity_types("10.0.0.3:9100") == ["endpoint"]
    assert state.get_best_fact("10.0.0.1:9100", "availability_status").value == "up"
    assert state.get_best_fact("10.0.0.2:9100", "availability_status").value == "down"
    assert "top_entities" not in summary
    assert "top_entities_by_kind" not in summary
    assert "availability" not in summary
    assert "availability_by_scope" not in summary


def test_operator_state_summary_no_longer_summarizes_named_non_endpoint_availability():
    state = _project(
        _fact("fact_host_os", "example_host", "os", "linux"),
        _fact("fact_service_note", "api-service", "service_note", "primary"),
        _fact("fact_storage_note", "pool-a", "capacity_note", "primary"),
        entities=[
            Entity(id="api-service", kind="service", name="api-service"),
            Entity(id="pool-a", kind="storage", name="pool-a"),
        ],
    )

    summary = build_operator_state_summary(state)

    assert "top_entities" not in summary
    assert "top_entities_by_kind" not in summary
    assert "availability" not in summary
    assert "availability_by_scope" not in summary


def test_operator_state_summary_excludes_storage_detail_projection_keys():
    state = _project(
        _fact(
            "fact_root_free",
            "example_host:9100",
            "filesystem_free_bytes",
            40,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
        _fact(
            "fact_root_total",
            "example_host:9100",
            "filesystem_total_bytes",
            100,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
    )

    summary = build_operator_state_summary(state)

    assert summary["fact_count"] == 2
    assert summary["measurement_current_sample_count"] == 2
    for key in (
        "filesystems",
        "filesystem_shape_summary",
        "cluster_mount_groups",
        "shared_storage_candidates",
        "storage_topology_ambiguities",
        "storage_topology_summary",
    ):
        assert key not in summary


def test_operator_state_summary_filters_runtime_pseudo_filesystems_only_from_summary():
    state = _project(
        _fact(
            "fact_root_free",
            "example_host:9100",
            "filesystem_free_bytes",
            40,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
        _fact(
            "fact_root_total",
            "example_host:9100",
            "filesystem_total_bytes",
            100,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
        _fact(
            "fact_runtime_free",
            "example_host:9100",
            "filesystem_free_bytes",
            4,
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ),
        _fact(
            "fact_runtime_total",
            "example_host:9100",
            "filesystem_total_bytes",
            10,
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ),
    )

    summary = storage_state_projection(state)

    assert summary["measurement_current_sample_count"] == 4
    assert summary["fact_count"] == 4
    assert summary["filesystems"] == [
        {
            "host": "example_host:9100",
            "mountpoint": "/",
            "free": 40,
            "fstype": "ext4",
            "total": 100,
            "used_bytes": 60,
            "free_percent": 0.4,
            "used_percent": 0.6,
        }
    ]
    assert (
        state.get_best_fact(
            "example_host:9100",
            "filesystem_free_bytes",
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ).value
        == 4
    )
    assert (
        state.get_best_fact(
            "example_host:9100",
            "filesystem_total_bytes",
            dimensions={"mountpoint": "/run", "device": "tmpfs", "fstype": "tmpfs"},
        ).value
        == 10
    )
    support = state.get_fact_support(
        "example_host:9100",
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
            "example_host:9100",
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
            "example_host:9100",
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
            "example_host:9100",
            "filesystem_free_bytes",
            20,
            dimensions={"mountpoint": "/boot", "device": "/dev/sda2", "fstype": "ext4"},
        ),
        _fact(
            "fact_boot_total",
            "example_host:9100",
            "filesystem_total_bytes",
            50,
            dimensions={"mountpoint": "/boot", "device": "/dev/sda2", "fstype": "ext4"},
        ),
        _fact(
            "fact_root_free",
            "example_host:9100",
            "filesystem_free_bytes",
            40,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
        _fact(
            "fact_root_total",
            "example_host:9100",
            "filesystem_total_bytes",
            100,
            dimensions={"mountpoint": "/", "device": "/dev/sda1", "fstype": "ext4"},
        ),
    )

    summary = storage_state_projection(state)

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


def test_operator_state_summary_adds_filesystem_shape_without_changing_filesystem_rows():
    facts = []
    for index in range(12):
        facts.extend(
            _filesystem_facts(
                f"node{index:03d}:9100",
                "/",
                free=1000 + index,
                total=2000 + index,
                prefix=f"shape_root_{index}",
            )
        )
    facts.extend(
        _filesystem_facts(
            "node100:9100",
            "/boot/firmware",
            free=10,
            total=20,
            prefix="shape_boot_firmware",
        )
    )
    facts.extend(
        _filesystem_facts(
            "node101:9100",
            "/System/Volumes/iSCPreboot",
            free=11,
            total=21,
            prefix="shape_preboot",
        )
    )
    facts.extend(
        _filesystem_facts(
            "node102:9100",
            "/mnt/node205/sda1",
            free=12,
            total=22,
            prefix="shape_cluster_node",
        )
    )
    facts.extend(
        _filesystem_facts(
            "node103:9100",
            "/mnt/rpi4/data",
            free=13,
            total=23,
            prefix="shape_cluster_rpi",
        )
    )
    facts.extend(
        _filesystem_facts(
            "node104:9100",
            "/srv/data",
            free=14,
            total=24,
            prefix="shape_other",
        )
    )
    state = _project(*facts)

    summary = storage_state_projection(state)

    assert summary["fact_count"] == len(facts)
    assert summary["measurement_current_sample_count"] == len(facts)
    assert len(summary["filesystems"]) == len(facts) // 2
    assert summary["filesystem_shape_summary"]["counts"] == {
        "root": 12,
        "boot": 2,
        "cluster mounts": 2,
        "other": 1,
    }
    assert summary["filesystem_shape_summary"]["detail_category"] == "root"
    assert summary["filesystem_shape_summary"]["detail_row_count"] == 10
    assert summary["filesystem_shape_summary"]["total_row_count"] == 17
    assert [
        filesystem["mountpoint"]
        for filesystem in summary["filesystem_shape_summary"]["detail_rows"]
    ] == ["/"] * 10
    assert {
        (filesystem["host"], filesystem["mountpoint"], filesystem["free"])
        for filesystem in summary["filesystems"]
    } >= {
        ("node102:9100", "/mnt/node205/sda1", 12),
        ("node103:9100", "/mnt/rpi4/data", 13),
        ("node104:9100", "/srv/data", 14),
    }
    assert (
        state.get_best_fact(
            "node102:9100",
            "filesystem_free_bytes",
            dimensions={
                "mountpoint": "/mnt/node205/sda1",
                "device": "/dev/sda1",
                "fstype": "ext4",
            },
        ).value
        == 12
    )
    assert (
        state.get_fact_support(
            "node103:9100",
            "filesystem_total_bytes",
            dimensions={
                "mountpoint": "/mnt/rpi4/data",
                "device": "/dev/sda1",
                "fstype": "ext4",
            },
        ).value
        == 23
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

    summary = storage_state_projection(state)

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

    summary = storage_state_projection(state)

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

    summary = storage_state_projection(state)

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

    summary = storage_state_projection(state)

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


def _candidate_by_evidence(summary: dict, evidence: list[str]) -> list[dict]:
    return [
        candidate
        for candidate in summary["shared_storage_candidates"]
        if candidate["evidence"] == evidence
    ]


def test_shared_storage_candidates_are_projection_only_not_facts_ownership_or_identity():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node100_candidate_only",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node101_candidate_only",
        ),
    )

    summary = storage_state_projection(state)

    assert summary["fact_count"] == 4
    assert state.relationships == []
    assert summary["shared_storage_candidates"]
    candidate = summary["shared_storage_candidates"][0]
    assert candidate["candidate_kind"] == "candidate_shared_storage"
    assert "shared storage fact" in candidate["boundary"]
    assert "ownership" in candidate["boundary"]
    assert "topology authority" in candidate["boundary"]
    assert "owner" not in candidate
    assert "ownership" not in candidate
    assert "storage_identity" not in candidate
    assert all("ownership" not in fact.predicate for fact in state.facts.values())
    assert all("storage_identity" not in fact.predicate for fact in state.facts.values())
    assert all("shared_storage" not in fact.predicate for fact in state.facts.values())


def test_shared_storage_candidates_preserve_filesystem_facts_and_measurements():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            prefix="node100_candidate_preserved",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            prefix="node101_candidate_preserved",
        ),
    )

    summary = storage_state_projection(state)

    assert summary["fact_count"] == 4
    assert summary["measurement_current_sample_count"] == 4
    assert {fact.predicate for fact in state.facts.values()} == {
        "filesystem_free_bytes",
        "filesystem_total_bytes",
    }
    assert (
        state.get_best_fact(
            "node100:9100",
            "filesystem_free_bytes",
            dimensions={
                "mountpoint": "/mnt/node205/sda1",
                "device": "/dev/sda1",
                "fstype": "ext4",
            },
        ).value
        == 10
    )
    assert (
        state.get_best_fact(
            "node101:9100",
            "filesystem_total_bytes",
            dimensions={
                "mountpoint": "/mnt/node205/sda1",
                "device": "/dev/sda1",
                "fstype": "ext4",
            },
        ).value
        == 100
    )


def test_shared_storage_candidates_allow_multiple_plausible_interpretations():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node100_multi",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/srv/compat/node205",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node101_multi",
        ),
        *_filesystem_facts(
            "node102:9100",
            "/mnt/node205/sda1",
            free=30,
            total=100,
            device="/dev/mapper/compat205",
            prefix="node102_multi",
        ),
    )

    summary = storage_state_projection(state)

    candidates = summary["shared_storage_candidates"]
    assert len(candidates) >= 3
    assert _candidate_by_evidence(
        summary,
        [
            "matching device",
            "matching filesystem type",
            "matching total bytes",
        ],
    )
    assert _candidate_by_evidence(
        summary,
        [
            "matching mountpath",
            "matching filesystem type",
            "matching total bytes",
        ],
    )
    assert _candidate_by_evidence(summary, ["matching total bytes"])


def test_shared_storage_candidates_keep_distinct_evidence_groups_distinct():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node100_distinct",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node101_distinct",
        ),
        *_filesystem_facts(
            "node200:9100",
            "/mnt/node200/sda1",
            free=40,
            total=200,
            device="node200:/exports/sda1",
            prefix="node200_distinct",
        ),
        *_filesystem_facts(
            "node201:9100",
            "/mnt/node200/sda1",
            free=40,
            total=200,
            device="node200:/exports/sda1",
            prefix="node201_distinct",
        ),
    )

    summary = storage_state_projection(state)

    high_candidates = [
        candidate
        for candidate in summary["shared_storage_candidates"]
        if candidate["confidence"] == "high"
    ]
    assert [candidate["mountpaths"] for candidate in high_candidates] == [
        ["/mnt/node200/sda1"],
        ["/mnt/node205/sda1"],
    ]
    assert high_candidates[0]["observed_values"] != high_candidates[1]["observed_values"]


def test_shared_storage_candidates_use_observable_filesystem_evidence_only():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node100_observable",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node101_observable",
        ),
    )

    summary = storage_state_projection(state)

    candidate = summary["shared_storage_candidates"][0]
    assert set(candidate["observed_values"]).issubset(
        {"mountpoint", "device", "fstype", "total", "free"}
    )
    assert candidate["evidence"] == [
        "matching mountpath",
        "matching device",
        "matching filesystem type",
        "matching total bytes",
        "matching free bytes",
    ]
    assert "evidence_ids" not in candidate
    assert "source_type" not in candidate
    assert "operator" not in candidate
    assert "confidence is not certainty" in candidate["confidence_basis"]


def _ambiguity_by_subject(summary: dict, subject: str) -> dict:
    return next(
        ambiguity
        for ambiguity in summary["storage_topology_ambiguities"]
        if ambiguity["subject"] == subject
    )


def test_storage_topology_ambiguities_are_projection_only_not_facts_ownership_or_identity():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node210/sda1",
            free=10,
            total=100,
            device="node210:/exports/sda1",
            prefix="node100_ambiguity_only",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node210/sda1",
            free=10,
            total=100,
            device="node210:/exports/sda1",
            prefix="node101_ambiguity_only",
        ),
    )

    summary = storage_state_projection(state)

    assert summary["storage_topology_ambiguities"]
    ambiguity = _ambiguity_by_subject(summary, "/mnt/node210/sda1")
    assert "ambiguity != fact" in ambiguity["boundary"]
    assert "ownership" in ambiguity["boundary"]
    assert "storage identity" in ambiguity["boundary"]
    assert "owner" not in ambiguity
    assert "storage_identity" not in ambiguity
    assert state.relationships == []
    assert all("ambigu" not in fact.predicate for fact in state.facts.values())
    assert all("ownership" not in fact.predicate for fact in state.facts.values())
    assert all("storage_identity" not in fact.predicate for fact in state.facts.values())


def test_storage_topology_ambiguities_use_shared_storage_candidates_as_pressure():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/srv/data",
            free=10,
            total=100,
            device="shared:/exports/data",
            prefix="node100_shared_ambiguity",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/srv/data-alias",
            free=10,
            total=100,
            device="shared:/exports/data",
            prefix="node101_shared_ambiguity",
        ),
    )

    summary = storage_state_projection(state)

    subjects = {
        ambiguity["subject"] for ambiguity in summary["storage_topology_ambiguities"]
    }
    assert {"/srv/data", "/srv/data-alias"}.issubset(subjects)
    ambiguity = _ambiguity_by_subject(summary, "/srv/data")
    assert "possible shared backing" in ambiguity["candidate_interpretations"]
    assert (
        "shared-storage candidate exists from matching observable filesystem fields"
        in ambiguity["reasons"]
    )
    assert "shared_storage_candidates.evidence" in ambiguity["observable_evidence"]
    assert ambiguity["materiality"] == "medium"


def test_storage_topology_ambiguities_surface_historical_node_style_without_topology_facts():
    state = _project(
        *_filesystem_facts(
            "example_host:9100",
            "/mnt/node210/sda1",
            free=10,
            total=100,
            prefix="example_host_historical_path",
        )
    )

    summary = storage_state_projection(state)

    ambiguity = _ambiguity_by_subject(summary, "/mnt/node210/sda1")
    assert "historical-node-style naming" in ambiguity["candidate_interpretations"]
    assert "possible compatibility path" in ambiguity["candidate_interpretations"]
    assert "mountpath contains node-number path segment" in ambiguity["reasons"]
    assert "filesystem.mountpoint" in ambiguity["observable_evidence"]
    assert "node210 owns" not in str(ambiguity)
    assert "retired" not in str(ambiguity)
    assert all("topology" not in fact.predicate for fact in state.facts.values())


def test_storage_topology_ambiguities_preserve_filesystem_facts_and_measurements():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            prefix="node100_ambiguity_preserved",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=20,
            total=100,
            prefix="node101_ambiguity_preserved",
        ),
    )

    summary = storage_state_projection(state)

    assert summary["fact_count"] == 4
    assert summary["measurement_current_sample_count"] == 4
    assert {fact.predicate for fact in state.facts.values()} == {
        "filesystem_free_bytes",
        "filesystem_total_bytes",
    }
    assert {
        (filesystem["host"], filesystem["mountpoint"], filesystem["free"])
        for filesystem in summary["filesystems"]
    } == {
        ("node100:9100", "/mnt/node205/sda1", 10),
        ("node101:9100", "/mnt/node205/sda1", 20),
    }


def test_storage_topology_ambiguities_allow_multiple_ambiguities_to_coexist():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            prefix="node100_multi_ambiguity_205",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=20,
            total=100,
            prefix="node101_multi_ambiguity_205",
        ),
        *_filesystem_facts(
            "node200:9100",
            "/srv/shared",
            free=30,
            total=200,
            device="shared:/exports/data",
            prefix="node200_multi_ambiguity_shared",
        ),
        *_filesystem_facts(
            "node201:9100",
            "/srv/shared-copy",
            free=30,
            total=200,
            device="shared:/exports/data",
            prefix="node201_multi_ambiguity_shared",
        ),
    )

    summary = storage_state_projection(state)

    subjects = [
        ambiguity["subject"] for ambiguity in summary["storage_topology_ambiguities"]
    ]
    assert "/mnt/node205/sda1" in subjects
    assert "/srv/shared" in subjects
    assert "/srv/shared-copy" in subjects
    assert len(subjects) >= 3


def test_storage_topology_ambiguities_use_observable_projection_evidence_only():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node100_ambiguity_observable",
        ),
        *_filesystem_facts(
            "node101:9100",
            "/mnt/node205/sda1",
            free=10,
            total=100,
            device="node205:/exports/sda1",
            prefix="node101_ambiguity_observable",
        ),
    )

    summary = storage_state_projection(state)

    ambiguity = _ambiguity_by_subject(summary, "/mnt/node205/sda1")
    assert set(ambiguity["observable_evidence"]).issubset(
        {
            "filesystem.mountpoint",
            "cluster_mount_groups.visible_endpoint_count",
            "shared_storage_candidates.evidence",
        }
    )
    assert "evidence_ids" not in ambiguity
    assert "source_type" not in ambiguity
    assert "operator" not in ambiguity
    assert "certainty" in ambiguity["materiality_basis"]


def test_storage_topology_projection_data_survives_bounded_operator_summary():
    facts = []
    for index in range(6):
        mountpoint = f"/mnt/node20{index}/sda1"
        total = 1000 + index
        device = f"node20{index}:/exports/sda1"
        facts.extend(
            _filesystem_facts(
                "node100:9100",
                mountpoint,
                free=100 + index,
                total=total,
                device=device,
                prefix=f"node100_projection_boundary_{index}",
            )
        )
        facts.extend(
            _filesystem_facts(
                "node101:9100",
                mountpoint,
                free=100 + index,
                total=total,
                device=device,
                prefix=f"node101_projection_boundary_{index}",
            )
        )

    state = _project(*facts)
    summary = storage_state_projection(state)

    assert summary["fact_count"] == 24
    assert summary["measurement_current_sample_count"] == 24
    assert len(summary["filesystems"]) == 12
    assert len(summary["cluster_mount_groups"]) == 6
    assert len(summary["shared_storage_candidates"]) >= 6
    assert len(summary["storage_topology_ambiguities"]) == 6
    assert summary["storage_topology_summary"] == {
        "cluster_mount_group_count": 6,
        "shared_storage_candidate_count": len(summary["shared_storage_candidates"]),
        "shared_storage_candidate_confidence_counts": {
            "high": 6,
            "medium": 12,
            "low": 6,
        },
        "storage_topology_ambiguity_count": 6,
        "storage_topology_ambiguity_materiality_counts": {"medium": 6},
    }
    assert {
        ambiguity["subject"]
        for ambiguity in summary["storage_topology_ambiguities"]
    } == {f"/mnt/node20{index}/sda1" for index in range(6)}
    assert all(
        ambiguity["materiality"] == "medium"
        for ambiguity in summary["storage_topology_ambiguities"]
    )
    assert {fact.predicate for fact in state.facts.values()} == {
        "filesystem_free_bytes",
        "filesystem_total_bytes",
    }
    assert state.get_best_fact(
        "node101:9100",
        "filesystem_total_bytes",
        dimensions={
            "mountpoint": "/mnt/node205/sda1",
            "device": "node205:/exports/sda1",
            "fstype": "ext4",
        },
    ).value == 1005


def test_storage_projection_adds_filesystem_arithmetic_only_to_complete_valid_rows():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/",
            free=40,
            total=100,
            prefix="arithmetic_root",
        ),
        _fact(
            "arithmetic_missing_free",
            "node100:9100",
            "filesystem_free_bytes",
            5,
            dimensions={"mountpoint": "/missing-total", "device": "/dev/sdb1", "fstype": "ext4"},
        ),
        _fact(
            "arithmetic_missing_total",
            "node100:9100",
            "filesystem_total_bytes",
            10,
            dimensions={"mountpoint": "/missing-free", "device": "/dev/sdc1", "fstype": "ext4"},
        ),
    )

    summary = storage_state_projection(state)
    filesystems = {
        filesystem["mountpoint"]: filesystem for filesystem in summary["filesystems"]
    }

    assert set(filesystems) == {"/"}
    assert filesystems["/"]["used_bytes"] == 60
    assert filesystems["/"]["free_percent"] == 0.4
    assert filesystems["/"]["used_percent"] == 0.6


def test_storage_projection_omits_filesystem_arithmetic_for_zero_sized_filesystems():
    state = _project(
        *_filesystem_facts(
            "node100:9100",
            "/zero",
            free=0,
            total=0,
            prefix="arithmetic_zero",
        )
    )

    summary = storage_state_projection(state)
    filesystem = summary["filesystems"][0]

    assert filesystem["mountpoint"] == "/zero"
    assert filesystem["free"] == 0
    assert filesystem["total"] == 0
    assert "used_bytes" not in filesystem
    assert "free_percent" not in filesystem
    assert "used_percent" not in filesystem


def test_storage_projection_arithmetic_does_not_forecast_or_create_state_records():
    ledger = EventLedger()
    for fact in _filesystem_facts(
        "node100:9100",
        "/",
        free=25,
        total=100,
        prefix="arithmetic_boundary",
    ):
        ledger.append("fact.observed", "ws", {"fact": to_plain(fact)})
    state = StateProjector(ledger).project("ws")
    before = (
        len(ledger.list_events("ws")),
        len(state.facts),
        len(state.observed_facts),
        len(state.inferred_facts),
        len(state.observations),
    )

    summary = storage_state_projection(state)

    assert before == (
        len(ledger.list_events("ws")),
        len(state.facts),
        len(state.observed_facts),
        len(state.inferred_facts),
        len(state.observations),
    )
    filesystem = summary["filesystems"][0]
    assert filesystem["used_bytes"] == 75
    assert filesystem["free_percent"] == 0.25
    assert filesystem["used_percent"] == 0.75
    assert not any(
        key in filesystem
        for key in (
            "time_to_full",
            "predicted_exhaustion",
            "capacity_warning",
            "critical_pressure",
            "attention_priority",
        )
    )
    assert {event.kind for event in ledger.list_events("ws")} == {"fact.observed"}
