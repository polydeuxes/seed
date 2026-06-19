# Local Host Bounded Surface Investigation

## Repository evidence found

- `LocalHostObservationSource.collect()` is a single local-host acquisition entrypoint that appends observations from smaller methods: identity, hosts-file, host description, network, mounts/filesystems, storage, listeners, users/groups, packages, and systemd.
- `LocalHostObservationSource` is explicitly read-only/local-only and avoids shell/subprocess execution while reading local platform, disk, network, and mount metadata.
- The local-host constructor already accepts separate inputs for procfs/sysfs, hostname/machine-id, hosts/resolver/systemd-resolved files, passwd/group, dpkg status, and an injectable systemd source.
- Users/groups are a bounded implemented surface: passwd/group records only, with explicit refusals to infer login activity, SSH access, sudo authorization, privilege, reachability, availability, account safety, enablement, or human/system classification.
- Mount/filesystem observation is a bounded implemented surface: `/proc/mounts` only, with explicit refusals to assert health, writability, reachability, storage availability, or device accessibility.
- Storage topology is a bounded implemented surface separate from mounts/filesystems: read-only local block topology and sysfs/proc-derived attributes, with explicit refusals to assert management, availability, health, repairability, backup, redundancy, data safety, or performance adequacy.
- Listener observation is a bounded implemented surface: locally bound TCP/UDP endpoints from procfs socket tables, with explicit refusals to infer reachability, availability, responsiveness, endpoint health, process/service/application ownership, or external accessibility.
- Systemd is already an independently implemented observation source class and local-host delegates to it.
- Systemd observations carry `observation_surface: "systemd"` metadata and are bounded to systemd-reported unit identity, runtime state, substate, and unit-file enablement.
- State Views are implemented as deterministic read-only projections of already-built State; they do not read ledgers, append events, invoke providers, evaluate policy, or execute runtime behavior.
- Context Views are implemented as deterministic projections from already-projected State plus evidence, contradiction, and confidence layers; they form the boundary between Seed knowledge and decision-making.
- Repository authority says Host Observation is not a single source, transport, projection, or truth system; it is a capability area composed of host-scoped observation domains that preserve source, reader, vantage point, and provenance.
- Repository authority names Host Observation domains that correspond closely to current and recent surfaces: identity, platform/OS, resources, network, storage, users/groups, packages, listeners, services, configuration, capabilities, health indicator, state indicator, and relationship observers.
- Repository authority distinguishes readers/transports from host knowledge domains. Local filesystem, SSH reader, mounted rootfs, agent payload, provider API, Prometheus HTTP/sample stream, remote Seed export, and Ansible fact payload are acquisition/vantage paths, not host knowledge domains themselves.
- Repository authority says domain observers may be reused across readers when evidence shape is compatible while preserving distinct provenance.
- Repository authority does not mandate immediate implementation. Future extraction is constrained to narrow domain observers only when there is concrete implementation need, preserving current local collector behavior unless a separate behavior-changing task authorizes otherwise.
- Participant-related authority is weaker than Seed/state/view authority. Repository evidence contains operator, consumer, later-participant, and attention language, but no reviewed authority defines a participant layer.

## Files inspected

- `seed_runtime/observation_sources.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context_views.py`
- `scripts/seed_local.py`
- `13-knowledge-and-evidence.md`
- `docs/host_observation_reconciliation.md`
- `docs/participant_orientation_view_selection_observation.md`
- `docs/capability_ownership_matrix.md`

## Supported observations

- Current local-host observation acts as a container/orchestrator over smaller bounded observable surfaces.
- The strongest implementation support is the local-host `collect()` method, which appends separately collected identity, hosts-file, host description, network, mount/filesystem, storage, listener, user/group, package, and systemd observations.
- Several bounded observable surfaces already exist in implementation: users/groups, mounts/filesystems, storage topology, listeners, packages, network/host configuration inputs, and systemd.
- Systemd is the clearest independently observable surface because it is already a separate `SystemdObservationSource` and local-host delegates to it.
- Users/groups, mounts/filesystems, storage, listeners, packages, and local configuration-like files are bounded in behavior, but most are still implemented as methods inside `LocalHostObservationSource` rather than separate source classes.
- Repository documents already describe similar boundaries through Host Observation Domains and Reader / Transport boundaries.
- Repository evidence supports a shared bounded-surface reading: acquisition readers can feed domain observers, while State Views and Context Views consume projected knowledge for different consumers without becoming acquisition paths.
- Existing State Views and Context Views consume projected State/read-model layers, not raw local-host observer methods.
- Configuration is supported as a host observation domain in repository authority and appears in local-host implementation as configuration-like source files, but it is not currently implemented as a distinct configuration observation source class.
- The same bounded acquired facts can be useful to different consumers after projection: Seed decision context through Context Views, and operator/CLI inspection through State Views and related read surfaces.
- Repository evidence supports preserving authority boundaries: acquisition surfaces produce observations/evidence/facts; State Views and Context Views are read-only projections and do not mutate, execute, or acquire.

## Unsupported observations

- `observer == lens` is unsupported.
- `lens == view` is unsupported.
- `view == orientation` is unsupported.
- A current lens framework is unsupported by the inspected implementation evidence.
- Local-host domain decomposition automatically becoming user-facing UI is unsupported.
- A current participant architectural layer is unsupported.
- Existing State Views or Context Views directly consuming raw bounded local-host surfaces is unsupported.
- Configuration visibility as a named independent observation source class is unsupported by the inspected implementation evidence.
- Systemd observations being participant views is unsupported; implementation identifies systemd as an acquisition observation source/surface, while participant/operator inspection happens through projected read-only surfaces.

## Implementation opportunities directly supported by repository evidence

- Extracting one narrow bounded domain observer from `LocalHostObservationSource` could be supported if there is a concrete implementation need and current behavior is preserved.
- `SystemdObservationSource` is the existing precedent for an independently implemented bounded surface delegated from local-host observation.
- Additional local-host sub-surfaces could use explicit surface metadata analogous to systemd's `observation_surface`, if a concrete implementation task requires clearer provenance or filtering.
- Readers/transports could expose bounded read primitives or payloads that feed host observation domains while preserving provenance, consistent with repository authority.

## LOC changed if implementation occurs

- 0 implementation LOC.
- 1 markdown file added for this investigation record.

## Commit SHA if implementation occurs

- No implementation commit SHA; this investigation produced a documentation-only commit.
