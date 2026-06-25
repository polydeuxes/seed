---
scope: filesystem ownership constrained-authority investigation
status: investigation-only
---

# Filesystem Ownership Under Constrained Authority

## Boundary

This reconciliation asks only whether the current repository can express
`filesystem ownership` as a bounded authority-aware inquiry under this constrained
profile:

```text
root = unavailable
docker_socket_read = unavailable
local_passive = available
active_network_probe = unauthorized
external_provider_query = unknown
```

No implementation was changed. No filesystem framework, storage framework,
planner, inquiry runtime, strategy engine, conversation runtime, presentation
abstraction, or new authority domain is recommended here.

## Answer

Yes, but only as a bounded **investigation shape**, not as a new implemented
runtime surface.

Current implementation evidence already supports observations that contribute to
filesystem ownership pressure: local mount-table inspection, local block-device
inventory, Prometheus filesystem measurements, storage projection summaries,
shared-storage candidates, storage topology ambiguities, and
`ownership_discrepancies` storage rows.

Under the constrained profile, the natural current strategy is **composite local
storage attribution from existing read-only evidence**:

1. local passive mount inspection;
2. local passive filesystem inventory / measurement projection;
3. local passive block-device observations;
4. storage ownership discrepancy analysis;
5. privilege guidance for deeper export/source attribution when ownership cannot
   be resolved.

That strategy is **partially reachable**. Mount visibility, filesystem type,
mounted device, mount source text, local block-device shape, and already-ingested
filesystem measurements remain observable without root or Docker. Stronger
remote export ownership evidence is blocked or unknown because current privilege
guidance registers `nfs_export_inventory` as root-only and leaves analogous
storage-source capabilities such as `mount_source_inventory`,
`export_visibility_inventory`, `smb_share_inventory`, and
`remote_storage_export_inventory` without registered implementation-backed
privilege guidance.

## Existing observations capable of contributing

Only existing observations are listed here.

| Existing observation | Current implementation evidence | Contribution to filesystem ownership inquiry | Boundary |
| --- | --- | --- | --- |
| `mount_point` / `mount_target` | local mount-table collection from `/proc/mounts` | shows where a filesystem is visible locally | visibility only |
| `filesystem_type` / `mount_fstype` | local mount-table collection from `/proc/mounts` | identifies mounted filesystem type | not health or ownership |
| `mounted_device` / `mount_source` | local mount-table collection from `/proc/mounts` | identifies the source string backing a mount | not device accessibility or ownership |
| `mount_source_host` / `mount_source_path` | remote-source parsing from mount source strings | can reveal a remote source host/path when parseable | export attribution remains unverified |
| `mount_options` / `mount_option` | local mount-table collection | adds local mount context | not writability assertion |
| `block_device`, `partition` | local sysfs/procfs storage topology | shows locally visible block devices and partitions | topology shape only |
| `block_device_parent` | local sysfs/procfs storage topology | relates partition to parent block device | not storage ownership |
| `block_device_size_bytes`, `block_device_rotational`, `block_device_removable`, `block_device_model`, `block_device_vendor` | local sysfs attributes | adds device evidence and possible local-storage context | not health/repairability/data safety |
| `filesystem_free_bytes`, `filesystem_total_bytes` | current measurement facts and Prometheus mappings | supports filesystem inventory/projection by subject, mountpoint, device, and fstype | endpoint-visible measurement, not host/storage owner |
| `storage_owner_candidate` and storage owner predicates consumed by diagnostics | `ownership_discrepancies` storage predicate set | explicit candidate evidence when present | diagnostic candidate only |

## Supported authority

Current privilege guidance is sparse but decisive where it exists.

- Local mount inspection is implemented as reading `/proc/mounts`; the collector
  explicitly avoids invoking `mount`, `findmnt`, or other commands.
- Local block-device inventory is implemented from sysfs/procfs paths and states
  that it is read-only local storage topology evidence.
- `nfs_export_inventory` is explicitly registered as `root` because export details
  may require root-owned configuration visibility.
- `ownership_discrepancies` emits diagnostic capability needs for storage
  conflicts, including `mount_source_inventory`, `export_visibility_inventory`,
  `nfs_export_inventory`, `smb_share_inventory`, and
  `remote_storage_export_inventory`.
- Privilege guidance only knows `nfs_export_inventory` among those storage
  capabilities. The remaining storage capability needs currently fall through to
  `unknown` guidance.

## Constrained-profile evaluation

### Observable

With `local_passive = available`, current implementation supports observing:

- local mount visibility;
- mounted device/source strings;
- filesystem type and mount options;
- parseable remote mount source host/path when the source string exposes them;
- locally visible block devices, partitions, parent relationships, and selected
  sysfs attributes;
- already-ingested filesystem measurement facts and storage projections;
- diagnostic storage ownership discrepancies derived from existing facts.

### Blocked

With `root = unavailable`, current implementation blocks root-only export
attribution where the needed capability is `nfs_export_inventory`.

With `docker_socket_read = unavailable`, there is no direct effect on filesystem
ownership evidence except for Docker-specific mount noise or container-runtime
interpretation; current filesystem ownership evidence is not Docker-runtime based.

With `active_network_probe = unauthorized`, the inquiry cannot promote remote
reachability or actively verify a remote storage endpoint.

### Uncertain

The following remain uncertain because implementation evidence is missing or
bounded:

- whether a local mount source string represents actual ownership, export
  authority, or only consumption;
- whether matching mountpoint/device/fstype/size across endpoints indicates one
  shared storage object;
- whether a remote source host owns, exports, merely proxies, or aliases the
  storage;
- privilege requirements for `mount_source_inventory`,
  `export_visibility_inventory`, `smb_share_inventory`, and
  `remote_storage_export_inventory`, because they are emitted as capability needs
  but do not have registered guidance;
- whether external provider evidence could resolve ownership, because
  `external_provider_query` is unknown and current authority slices do not use it
  to promote ownership.

## Inquiry-state shape

The existing inquiry-state discipline naturally applies as an analysis shape:

| Field | Filesystem ownership value supported by current evidence |
| --- | --- |
| desired observation | `filesystem ownership` |
| current strategy | composite local storage attribution from existing read-only evidence |
| required observations | mount inspection, filesystem inventory/projection, device observations, storage ownership discrepancy diagnostics, export/source attribution when needed |
| required authority | local passive for implemented mount/device observations; root for `nfs_export_inventory`; unknown for several emitted storage capability needs |
| available authority | root unavailable; Docker socket unavailable; local passive available; active network probe unauthorized; external provider query unknown |
| strategy status | partially reachable |
| remaining observations | root-only or unknown-guidance storage export/source attribution |
| uncertainty | ownership versus visibility, export attribution, shared-storage identity, provider evidence |
| boundary | read-only investigation; no acquisition, no permission creation, no event-ledger write, no cluster mutation |

This shape is currently **not implemented** as a first-class filesystem ownership
authority CLI or runtime object. It reuses the same discipline visible in the
recent container and service authority slices: keep the desired observation
stable, derive strategy from the bounded inquiry, let authority determine state,
and preserve uncertainty and boundary explicitly.

## Comparison to container and service ownership

Filesystem ownership most closely resembles **service ownership**, not container
ownership, but it is not identical.

- Container ownership is a single strategy in current code: container runtime
  observation. Under the constrained profile it is fully blocked because both
  `container_inventory` and `container_port_mapping` require Docker/root
  authority.
- Service ownership is composite. Local listener and systemd evidence are
  reachable, while container observations are blocked under the same profile.
- Filesystem ownership is also composite. Local passive mount/device/filesystem
  evidence is reachable, while stronger export/source ownership attribution is
  blocked or unknown.

The repository does not justify inventing a new taxonomy. It demonstrates another
bounded composite ownership inquiry where local passive evidence can answer
visibility and partial attribution, but not full ownership.

## Missing subsystem or subsystem maturity?

This does not expose a missing generic filesystem/storage/inquiry framework. It
reveals that existing subsystems are only partially mature for this bounded
question:

- local-host observation already collects mount and device evidence;
- storage projection already summarizes filesystem evidence and exposes
  ambiguity without claiming ownership;
- `ownership_discrepancies` already has storage conflict classes and storage
  capability needs;
- `privilege_discovery` lacks registered guidance for several storage capability
  needs that `ownership_discrepancies` can emit;
- there is no filesystem ownership authority slice equivalent to the recent
  container/service slices, but this report does not recommend implementing one.

## Strongest supporting evidence

1. Local mount collection emits mount point, filesystem type, mounted device,
   mount source, mount source host/path, and attribution status, while explicitly
   denying health, writability, reachability, availability, device accessibility,
   export existence, and storage ownership.
2. Local storage topology collection emits block-device and partition facts from
   sysfs/procfs, while explicitly denying management, availability, health,
   repairability, backup, redundancy, data-safety, and performance assertions.
3. Storage projection derives filesystem summaries, cluster mount groups,
   shared-storage candidates, and storage topology ambiguities, while explicitly
   warning that candidates and ambiguities are not ownership or topology truth.
4. `ownership_discrepancies` already has a `storage` kind, storage predicates,
   storage conflict classes, and diagnostic capability needs for missing owner
   and remote export attribution.
5. `privilege_discovery` already marks `nfs_export_inventory` as root-only,
   preserving the authorization boundary for deeper export ownership evidence.

## Strongest contradictory evidence

1. No first-class `filesystem_ownership_authority` evaluator, CLI, diagnostic
   inventory entry, or shape-audit spec exists.
2. Current storage projection deliberately refuses to promote shared-storage
   candidates, mount groups, or ambiguities into ownership truth.
3. Prometheus filesystem measurements remain endpoint-visible measurements; they
   do not prove host identity, physical disk owner, storage authority, or service
   responsibility.
4. Several storage capability needs emitted by `ownership_discrepancies` have no
   registered privilege guidance, so the authority model for deeper storage
   attribution is incomplete.

## What filesystem ownership teaches about what Seed can learn without root

Without root, Seed can learn a meaningful amount about **filesystem visibility**:
current local mounts, mounted source strings, filesystem types, mount options,
parseable remote source hints, local block-device topology, partition shape, and
current filesystem measurements if already ingested. It can also expose ownership
pressure and uncertainty diagnostically.

Without root, current implementation does **not** support silently converting that
visibility into filesystem ownership truth. Export attribution, physical storage
control, shared-storage identity, and remote storage authority remain blocked or
uncertain unless stronger authorized observations are available.

## Recommended next bounded implementation slice

If implementation is later requested, the smallest bounded slice would be to
register and test privilege guidance for the existing storage capability needs
already emitted by `ownership_discrepancies`:

- `mount_source_inventory`;
- `export_visibility_inventory`;
- `smb_share_inventory`;
- `remote_storage_export_inventory`.

That slice would mature an existing subsystem boundary without introducing a new
filesystem framework, storage framework, planner, generic inquiry framework, or
new authority domain.

## Files inspected

- `AGENTS.md`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/local_host_mounts.py`
- `seed_runtime/predicate_catalog.py`
- `predicate_catalog/core.json`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_seed_local_script.py`
- `tests/test_state_summary_views.py`
- `tests/test_fact_support_aggregation.py`
- `docs/ownership_model_design_space_audit.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/local_host_observation_entity_boundary_reconciliation.md`

## Files changed

- `docs/filesystem_ownership_constrained_authority_reconciliation.md`

## LOC changed

- Added 290 lines.

## Tests and checks run

- `python scripts/seed_local.py --container-ownership-authority --json`
- `python scripts/seed_local.py --service-ownership-authority --json`
- `python scripts/seed_local.py --privilege-discovery --json`
- `python scripts/seed_local.py --diagnostic-inventory --json | python -m json.tool | head -n 80`
- `pytest -q tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py tests/test_privilege_discovery.py`
