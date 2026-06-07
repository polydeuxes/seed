# Storage Topology Observation v1

Storage Topology Observation v1 is a Knowledge Acquisition slice in Tier 3 — Host Topology. It enriches Seed's local knowledge model through the existing Observation → Evidence → Fact → Projection path only.

It is observation, not management. It does not change Runtime, ToolExecutor, orchestration, providers, execution behavior, or local host state.

## Local sources

The local host source uses read-only local files only:

- `/sys/block/*`
- `/sys/block/*/size`
- `/sys/block/*/queue/rotational`
- `/sys/block/*/removable`
- `/sys/block/*/device/model`
- `/sys/block/*/device/vendor`
- `/sys/class/block/*/size`
- `/proc/partitions`

It does not use `lsblk`, `blkid`, `findmnt`, `udevadm`, `smartctl`, `dmsetup`, `mdadm`, `zpool`, `btrfs`, shells, subprocesses, sudo, network probing, DNS, Prometheus, provider APIs, or LLM-generated host facts.

## Representation

Storage facts are host-scoped local topology facts. The host remains the fact subject. Device names are represented as values and also repeated in dimensions so multiple devices can coexist deterministically in current facts.

Predicates added for v1:

- `block_device`
- `partition`
- `block_device_size_bytes`
- `block_device_rotational`
- `block_device_removable`
- `block_device_model`
- `block_device_vendor`
- `block_device_parent`

Relationship representation is deliberately narrow: parent-child storage shape is a `block_device_parent` fact whose value is the parent device and whose dimensions identify the child device and parent. This preserves the existing fact model without adding storage-specific graph ownership.

Mounted devices are not re-modeled. `--impact HOST` correlates storage names with existing `mounted_device` and `mount_point` facts when a mounted device path matches `/dev/<observed-storage-name>`.

## Capability Extension Methodology

| Predicate | Question | Evidence | Fact | Non-inferences |
| --- | --- | --- | --- | --- |
| `block_device` | What block devices are visible locally? | `/sys/block/*`, with `/proc/partitions` as bounded local fallback context. | The named block device was observed locally. | `block_device` != healthy, available, reachable, safe, redundant, performant, or mounted. |
| `partition` | What partitions are visible locally? | `/sys/block/<device>/<partition>/partition`, `/proc/partitions`. | The named partition was observed locally. | `partition` != mounted, healthy, repairable, safe, or backed up. |
| `block_device_size_bytes` | How large is this observed block device or partition? | `/sys/block/<device>/size`, `/sys/class/block/<partition>/size`; sectors are converted with 512 bytes per sector. | The locally exposed size in bytes. | `block_device_size_bytes` != free space, usable space, performance, health, or capacity planning adequacy. |
| `block_device_rotational` | Does local sysfs mark this storage device as rotational? | `/sys/block/<device>/queue/rotational`. | The local marker value, stored as `true` or `false`. | `block_device_rotational` != performance adequacy, latency, health, or suitability. |
| `block_device_removable` | Does local sysfs mark this storage device as removable? | `/sys/block/<device>/removable`. | The local marker value, stored as `true` or `false`. | `block_device_removable` != safe to remove, mounted state, hotplug success, or data safety. |
| `block_device_model` | What model string is exposed locally for this block device? | `/sys/block/<device>/device/model`. | The bounded first-line model string. | `block_device_model` != identity uniqueness, health, supportability, performance, or vendor warranty. |
| `block_device_vendor` | What vendor string is exposed locally for this block device? | `/sys/block/<device>/device/vendor`. | The bounded first-line vendor string. | `block_device_vendor` != ownership, supportability, authenticity, or health. |
| `block_device_parent` | What parent block device is exposed locally for this partition? | Sysfs partition children under `/sys/block/<device>/`. | The parent device for the child named in dimensions. | `block_device_parent` != RAID membership, redundancy, safety, mount status, or device health. |

## Bounded-read behavior

Storage observation uses the same bounded local-read behavior as other local observation slices:

- fixed-size sysfs/procfs reads are bounded;
- regular files larger than the configured bound are skipped;
- streams or pseudo-files that fill the full bound are treated as possibly truncated and skipped;
- oversized or possibly truncated inputs are not partially projected.

## Impact and current facts

`--current-facts` exposes every emitted storage fact.

`--impact HOST` includes a compact `storage topology` section with devices, partitions, parent relationships, and mount relationships that can be correlated from existing mount facts. The impact output remains a summary and does not hide facts; use `--current-facts` for the full projected storage fact list.

## Non-inference boundaries

Storage topology facts must not imply:

- availability;
- reachability;
- filesystem health;
- storage health;
- repairability;
- backup status;
- redundancy;
- data safety;
- performance adequacy;
- safe removal;
- successful mounting.

Examples:

- `block_device` != healthy;
- `partition` != mounted;
- `mounted_device` != healthy;
- `block_device_size_bytes` != free space;
- `block_device_rotational` != performance adequacy;
- `block_device_removable` != safe to remove.
