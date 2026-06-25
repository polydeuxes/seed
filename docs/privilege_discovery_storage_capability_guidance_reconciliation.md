---
scope: privilege discovery storage capability guidance reconciliation
status: investigation-only
---

# Privilege Discovery Storage Capability Guidance Reconciliation

## Boundary

This investigation asks only whether `privilege_discovery` is ready to register
implementation-backed guidance for storage capability needs that are already
emitted by existing diagnostics:

- `mount_source_inventory`
- `export_visibility_inventory`
- `smb_share_inventory`
- `remote_storage_export_inventory`

It does not implement filesystem ownership, add observations, add an authority
framework, add a planner, or introduce a new storage inquiry domain.

## Answer

Yes. Privilege discovery is ready to mature its existing storage capability
guidance for the implemented portions of these capability needs. Doing so would
complete an existing subsystem boundary: `ownership_discrepancies` already emits
these storage capability needs, `capability_needs` already aggregates them, and
`privilege_discovery` already has the registration mechanism that maps capability
need names to authority guidance.

The readiness is uneven:

- `mount_source_inventory` is implemented as local passive mount-table evidence.
- `export_visibility_inventory` is partially implemented as passive export/share
  visibility evidence consumed by storage ownership discrepancy diagnostics, but
  there is no dedicated collector for export configuration visibility.
- `smb_share_inventory` is placeholder-only as an emitted need and consumed
  predicate vocabulary; there is no SMB share collector.
- `remote_storage_export_inventory` is placeholder-only as an emitted need; there
  is no generic remote export collector.

Therefore the smallest implementation slice is to register guidance only where
repository evidence supports it, and intentionally leave unsupported mappings as
`unknown`.

## Reconciliation Matrix

| Capability need | Implementation status | Supported authority mapping | Unsupported authority mapping | Strongest supporting evidence | Strongest contradictory evidence |
| --- | --- | --- | --- | --- | --- |
| `mount_source_inventory` | implemented | `local_passive` or equivalent non-escalating local visibility wording | `root`, `docker_group_or_root`, network probe | Local host mount collection emits `mount_source`, `mount_source_host`, `mount_source_path`, and `mount_attribution_status` from `/proc/mounts` without invoking mount/findmnt commands. | Mount facts explicitly do not assert export existence, reachability, device accessibility, or storage ownership. |
| `export_visibility_inventory` | partially implemented | `partial_non_root` / passive visibility only, if phrased as existing export/share evidence consumption rather than collection | full `root` requirement for all export visibility; full non-root export ownership | `ownership_discrepancies` consumes `export_path`, `shared_path`, `nfs_export`, `smb_share`, and `storage_owner_candidate` as export/candidate evidence, and emits `export_visibility_inventory` for missing storage owners. | No dedicated export-visibility collector is present; `nfs_export_inventory` remains the only explicit root guidance. |
| `smb_share_inventory` | placeholder only | none beyond `unknown` | `local_passive`, `root`, `docker_group_or_root` | The predicate `smb_share` is consumed as storage candidate evidence, and the capability need is emitted for remote export attribution gaps. | There is no SMB share observation source or privilege guidance implementation. |
| `remote_storage_export_inventory` | placeholder only | none beyond `unknown` | `local_passive`, `root`, active network probing, external provider query | The capability need is emitted for remote export attribution gaps alongside NFS and SMB-specific needs. | There is no generic remote export observation implementation, and active remote probing remains outside this investigation boundary. |

## Evidence by Subsystem

### `ownership_discrepancies`

`ownership_discrepancies` already owns the storage conflicts that create this
pressure. Storage `missing_owner` emits `mount_source_inventory` and
`export_visibility_inventory`; storage `remote_export_attribution_missing` emits
`nfs_export_inventory`, `smb_share_inventory`, and
`remote_storage_export_inventory`.

The storage diagnostic also consumes local mount source evidence and export/share
vocabulary. Remote source facts create candidate owners but intentionally preserve
`remote_export_attribution_missing` when export attribution is not verified.
Export/share predicates are consumed as candidate evidence, but that consumption
is not the same as implementing an export collector.

### `capability_needs`

`capability_needs` is already generic enough for this slice. It reads current
`ownership_discrepancies` rows, reads recorded `diagnostic_capability_need` facts
scoped to `diagnostic_run:*`, groups by capability, and returns deterministic
entries. No storage-specific expansion is needed to expose the capability needs.

### `privilege_discovery`

`privilege_discovery` already provides the exact registration seam. Registered
capabilities receive specific access guidance; unregistered capabilities fall
through to `unknown` with instructions to inspect implementation evidence before
requesting privileges. Today this means `nfs_export_inventory` has root guidance,
while the four capability needs under review fall through to `unknown`.

### `observation_sources` and `local_host_mounts`

Local mount-source observation is implemented. The local host source reads
`/proc/mounts`, emits mount source fields, parses common remote source syntax,
and marks remote source attribution as export-unattributed rather than ownership.
This supports local passive guidance for `mount_source_inventory` only.

Local block-device and mount rendering helpers provide storage context, but they
do not implement export visibility, SMB share inventory, or generic remote
storage export inventory. They also explicitly preserve the boundary between
visibility and ownership.

## Question Answers

### 1. Implementation status for each existing storage capability need

- `mount_source_inventory`: implemented. It maps directly to existing
  mount-source observations from local mount-table inspection.
- `export_visibility_inventory`: partially implemented. The diagnostic consumes
  export/share evidence if present and emits this need for missing storage
  owners, but there is no dedicated collector for export visibility.
- `smb_share_inventory`: placeholder only. It is vocabulary consumed by
  diagnostics and emitted as a capability need, but there is no collector or
  guidance.
- `remote_storage_export_inventory`: placeholder only. It is emitted as a generic
  capability need for unresolved remote export attribution, but no generic
  implementation exists.

### 2. Authority implied by implemented capabilities

- `mount_source_inventory`: the repository implies local passive authority. The
  implementation reads local kernel mount-table text from `/proc/mounts` and
  explicitly avoids shelling out to `mount`, `findmnt`, or other commands.
- `export_visibility_inventory`: the repository implies only partial passive
  visibility where export/share facts already exist. It does not imply complete
  export ownership or a universal root requirement.
- `smb_share_inventory`: unknown.
- `remote_storage_export_inventory`: unknown.

### 3. Existing subsystem completion or new repository concepts?

Registering guidance for supported mappings would complete the existing
privilege-discovery subsystem. It would not introduce new repository concepts:
the capability need names, diagnostic rows, aggregation path, unknown fallback,
and root guidance precedent already exist.

### 4. Capability needs intentionally remaining unknown

Yes. `smb_share_inventory` and `remote_storage_export_inventory` should remain
unknown until implementation evidence exists. `export_visibility_inventory` should
not be promoted beyond partial passive guidance unless a collector or explicit
root-backed export visibility implementation is added.

### 5. Is privilege discovery the limiting subsystem for richer filesystem ownership reasoning?

Only narrowly. Privilege discovery is the narrowest current bottleneck for
explaining the authority boundary of existing storage capability needs. It is not
the bottleneck preventing full filesystem ownership reasoning. The repository
already has mount visibility, storage topology, storage projection, and storage
ownership discrepancy diagnostics, but it intentionally does not convert remote
source visibility or shared measurement similarity into ownership truth. Richer
filesystem ownership would still require implementation-backed export attribution
evidence outside this privilege-guidance-only slice.

## Implementation Readiness

Ready, but bounded:

1. Register `mount_source_inventory` with local passive guidance.
2. Register `export_visibility_inventory` only as partial passive visibility, with
   notes that full export attribution remains implementation-dependent.
3. Keep `smb_share_inventory` unknown.
4. Keep `remote_storage_export_inventory` unknown.
5. Add privilege discovery tests proving the supported storage mappings render as
   registered guidance and unsupported storage mappings remain unknown.

This slice strengthens the existing privilege discovery subsystem; it does not
create a filesystem ownership subsystem.

## Strongest Supporting Evidence

1. Storage conflicts already emit the capability need names under review.
2. Capability needs already aggregate diagnostic capability records from current
   projections and recorded diagnostic runs.
3. Privilege discovery already has a capability-guidance registry and unknown
   fallback.
4. Local mount-source observation is implemented from `/proc/mounts` and emits
   remote source host/path hints with explicit export-unattributed status.
5. Existing tests prove remote mount source evidence records export attribution
   capability needs while preserving uncertainty and avoiding owner facts on
   entity subjects.

## Strongest Contradictory Evidence

1. There is no dedicated export visibility collector.
2. There is no SMB share inventory collector.
3. There is no generic remote storage export collector.
4. Mount source visibility explicitly does not assert export existence or storage
   ownership.
5. Current privilege discovery deliberately returns `unknown` for unregistered
   capabilities.

## Report

### Files inspected

- `seed_runtime/privilege_discovery.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`
- `tests/test_privilege_discovery.py`
- `seed_runtime/local_host_mounts.py`
- `seed_runtime/observation_sources.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_observation_sources.py`
- `docs/filesystem_ownership_constrained_authority_reconciliation.md`

### Files changed

- `docs/privilege_discovery_storage_capability_guidance_reconciliation.md`

### LOC changed

- Added 222 lines.

### Tests run

- `pytest -q tests/test_privilege_discovery.py tests/test_ownership_discrepancies.py tests/test_observation_sources.py`

### Recommended implementation slice

Register and test privilege guidance for the two supported storage mappings only:

- `mount_source_inventory` -> local passive mount-source visibility.
- `export_visibility_inventory` -> partial passive export/share visibility.

Leave `smb_share_inventory` and `remote_storage_export_inventory` intentionally
unknown until repository implementation evidence exists.
