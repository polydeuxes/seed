# Observation Goal Common Implementation Shape Investigation

## Purpose and boundary

This report characterizes whether the existing implementation-backed observation goals for container ownership, service ownership, and local listener endpoint inventory share a recurring reasoning shape.

This is a characterization only. It does not propose or design a framework, planner, generic evaluator, authority engine, ontology, capability model, or observation model.

## Constraint profile reviewed

| Authority input | Profile state |
| --- | --- |
| `root` | `unavailable` |
| `docker_socket_read` | `unavailable` |
| `active_network_probe` | `unauthorized` |
| `local_passive` | `available` |
| `external_provider_query` | `unknown` |

## Files inspected

Implementation files:

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/observation_inventory.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

Existing investigation and evidence reports:

- `docs/container_ownership_authority_cli_report.md`
- `docs/service_ownership_authority_slice_investigation.md`
- `docs/reachable_observation_third_slice_investigation.md`
- `docs/constraint_aware_observation_reachability_investigation.md`
- `docs/observation_relationship_implementation_evidence_investigation.md`
- `docs/reasoning_chain_visibility_investigation.md`
- `docs/listening_port_observation.md`
- `docs/non_root_observation_expansion_investigation.md`

Tests reviewed as implementation evidence:

- `tests/test_container_ownership_authority.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_privilege_discovery.py`
- `tests/test_observation_domains.py`
- `tests/test_observation_permission.py`
- `tests/test_observation_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

## Short answer

Yes, the three examples can be described as instances of one recurring implementation-backed reasoning pattern, but only at the characterization level:

```text
bounded desired observation
    -> required observations / capability needs
    -> implementation-backed observation/domain evidence
    -> implementation-backed authority guidance
    -> supplied authority profile
    -> outcome plus explicit uncertainty and boundary
```

The smallest description is:

> Seed repeatedly narrows an operational question to a bounded desired observation, identifies the observations needed for that bounded claim from existing diagnostic capability pressure or provider inventory, joins those observations to current domain/provider evidence and privilege or permission guidance, compares that guidance with the supplied authority profile, and reports whether the bounded claim is reachable, partially reachable, blocked, or unknown while preserving uncertainty and read-only boundaries.

This is a pattern already visible in the implementation and reports. It is not currently a generic evaluator: container ownership has an implemented evaluator; service ownership and listener endpoint inventory are investigation-backed characterizations assembled from existing implementation surfaces.

## Comparison matrix

| Observation goal | Desired observation | Required observations | Required authority | Authority sources | Observation sources | Outcome under profile | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Container ownership | `container ownership` | `container_inventory`, `container_port_mapping` | Both map to `docker_group_or_root`; profile has `root=unavailable` and `docker_socket_read=unavailable` | `container_ownership_authority.CONSTRAINED_AUTHORITY_PROFILE`; `privilege_discovery._guidance_for`; `observation_permission.SUPPORTED_OBSERVATION_CLASSES` recognizes `docker_socket_read` as `local_privileged` | `observation_domains.CAPABILITY_TO_DOMAIN` maps both observations to `container_runtime`; `capability_needs` can detect subject-specific ownership pressure from `ownership_discrepancies` | `blocked` | External provider query is unknown and not mapped; local passive evidence is insufficient for Docker/root container runtime evidence; subject-specific pressure only exists when ownership diagnostics emit matching conflicts |
| Service ownership | `service ownership` | `tcp_listen_inventory`, `listener_process_inventory`, `process_inventory`, `systemd_unit_inventory`, `container_inventory`, `container_port_mapping` depending on conflict | Listener and systemd portions are local/partial/available; container portions require Docker/root; generic process and tcp-listen names have incomplete dedicated guidance | `ownership_discrepancies._CAPABILITY_NEEDS_BY_CONFLICT`; `privilege_discovery._CAPABILITY_GUIDANCE`; `observation_permission` for activity classes; systemd source metadata as read-only local evidence | Service and listener predicates in `ownership_discrepancies`; `observation_domains` local listener and container runtime classifications; `observation_inventory` provider/family evidence; `SystemdObservationSource` | `partially reachable` | Local listener/systemd evidence can support shape and candidate attribution, but process ownership can be incomplete, container-backed attribution is blocked, and `systemd_unit_inventory`/`systemd_inventory` plus `tcp_listen_inventory`/listener-domain names are not perfectly aligned |
| Local listener endpoint inventory | local TCP/UDP endpoint inventory bounded to protocol/address/port bind state | `listening_endpoint`, `listener_protocol`, `listener_address`, `listener_port` and related listener/listening predicates; explicitly not process/service/container ownership | `local_passive=available`; no root, Docker socket read, active probe, or external provider query required for the bounded endpoint claim | Listener observation implementation boundary; `observation_inventory` provider/predicate/family discovery; `observation_domains` local listener evidence; profile `local_passive=available` | `LocalHostObservationSource` / listener socket table observation; `observation_inventory` provider/family discovery; `docs/listening_port_observation.md` boundary; local-listener domain evidence | `reachable` for bounded endpoint inventory, with uncertainty outside the goal | Does not prove process owner, service owner, application owner, health, responsiveness, external accessibility, DNS validity, or remote network reachability |

## Common implementation joins

### 1. Desired observation to required observations

The first common join is from a bounded desired observation to a smaller set of required observations.

- Container ownership performs this directly in `evaluate_container_ownership_authority_slice`: it fixes `DESIRED_OBSERVATION = "container ownership"`, filters `CONTAINER_OBSERVATIONS`, and keeps only capabilities mapped to `container_runtime`.
- Service ownership does not have a single evaluator, but `ownership_discrepancies` maps service conflict classes to capability needs such as `tcp_listen_inventory`, `listener_process_inventory`, `process_inventory`, `systemd_unit_inventory`, `container_inventory`, and `container_port_mapping`.
- Local listener endpoint inventory is bounded by implementation-backed listener facts: endpoint, protocol, address, and port, rather than owner, health, responsiveness, or external reachability.

### 2. Diagnostic conflict to capability pressure

For ownership-shaped goals, the repository repeatedly uses diagnostic ownership gaps as capability pressure.

```text
ownership_discrepancies row
    -> diagnostic_capability_need_records
    -> capability_needs aggregation
```

This join is strongest for service ownership and container ownership. It is weaker for listener endpoint inventory because the endpoint goal is satisfied by provider/inventory evidence rather than by an ownership conflict.

### 3. Capability need to observation domain

`observation_domains` contains the concrete join from selected capabilities to observation domains:

```text
listener_process_inventory -> local_listeners
container_inventory -> container_runtime
container_port_mapping -> container_runtime
```

This join is common to the ownership-oriented examples and provides supporting boundary evidence for listener endpoint inventory. It is not a complete semantic map for every service capability because `tcp_listen_inventory`, `process_inventory`, and `systemd_unit_inventory` are not all first-class entries in that map.

### 4. Capability need to privilege guidance

`privilege_discovery` provides recurring implementation-backed authority guidance:

```text
listener_process_inventory -> partial_non_root
container_inventory -> docker_group_or_root
container_port_mapping -> docker_group_or_root
systemd_inventory -> available
unknown names -> unknown guidance
```

This is a common join for comparing required observations against the constrained profile. The join is complete for container ownership, partial for service ownership, and intentionally avoided for bounded listener endpoint inventory where local passive provider evidence is enough for the narrowed claim.

### 5. Observation activity to permission class

`observation_permission` maps known activity names to permission classes:

```text
active_network_probe -> network_active
docker_socket_read -> local_privileged
external_provider_query -> external
neighbor_table_read -> local_passive
traffic_capture -> network_passive
```

This join supports profile interpretation but does not itself evaluate root/Docker availability or synthesize an outcome.

### 6. Provider/predicate implementation to observed families

`observation_inventory` discovers providers, predicates, and families from implemented Python observation providers. This is the strongest common evidence source for avoiding aspirational claims. Listener endpoint inventory depends on it directly; service ownership and container ownership use it indirectly through domain classifications and absence/presence of observed families.

## Joins that differ by goal

### Container-specific joins

- The implemented evaluator hard-codes the constrained profile keys and desired observation.
- It filters only `container_inventory` and `container_port_mapping` through `CAPABILITY_TO_DOMAIN == container_runtime`.
- It calls `_guidance_for` and requires all required observations to have `docker_group_or_root` guidance before returning `blocked`.
- It treats the supplied profile as authoritative and explicitly says state approvals never grant authority for this evaluator.

### Service-specific joins

- Service ownership begins in `ownership_discrepancies` service predicates and service conflict classes, not in a dedicated service evaluator.
- Different service conflicts produce different required observations.
- The service slice joins local listener evidence, listener process attribution, process inventory, systemd unit inventory, container inventory, and container port mapping.
- Some service joins are incomplete or name-mismatched: `systemd_unit_inventory` versus `systemd_inventory`, `tcp_listen_inventory` versus listener-domain inventory, and `process_inventory` lacking dedicated privilege guidance.

### Listener-specific joins

- The listener endpoint slice is provider/inventory bounded rather than ownership-conflict bounded.
- It uses local socket-table observation facts as sufficient for protocol/address/port endpoint inventory.
- It explicitly excludes process owner, service owner, application owner, health, responsiveness, DNS validity, external accessibility, and remote reachability from the bounded desired observation.
- Its outcome is reachable because the bounded claim needs only local passive evidence, not because all local-listener-adjacent ownership questions are reachable.

## Common outcome vocabulary

The exact vocabulary is mixed between implementation and investigation text.

| Term | Implementation-backed? | Evidence status |
| --- | --- | --- |
| `blocked` | Yes for container ownership | `evaluate_container_ownership_authority_slice` returns `blocked` when required container observations all require `docker_group_or_root` and both root and Docker socket read are unavailable. |
| `observed` | Yes, but domain visibility rather than authority reachability | `observation_domains` emits `observed` for domains/families with implementation-backed observed evidence and no capability pressure. |
| `partially_observed` | Yes, but domain visibility rather than authority reachability | `observation_domains` emits `partially_observed` when a domain has observed evidence plus pressure. |
| `unobserved` | Yes, but domain visibility rather than authority reachability | `observation_domains` emits `unobserved` when pressure exists without observed family evidence. |
| `unknown` | Yes in several surfaces | Container evaluator can return `unknown`; observation domains and permission surfaces also use `unknown` for insufficient evidence or unknown classes. |
| `partially reachable` | Investigation-backed, not a shared implementation enum | Used by service ownership and reachability investigations to characterize mixed reachable/blocked evidence; not currently a common code-level outcome. |
| `reachable` | Investigation-backed for authority reachability, implementation-backed indirectly by available/local observed evidence | Used by the third-slice investigation for bounded listener endpoint inventory; not a shared code-level outcome enum. |
| `reachable with uncertainty` | Investigation vocabulary | Useful distinction in the listener report, but not a recurring code-level outcome. |

Conclusion: a common outcome vocabulary is emerging, but only `blocked` and `unknown` are directly represented in the container evaluator. `observed`, `partially_observed`, and `unobserved` are implementation-backed visibility classifications, not identical to authority reachability outcomes. `reachable` and `partially reachable` are recurring investigation vocabulary supported by implementation evidence, but they are not yet a common implementation enum.

## Minimum information necessary to evaluate an observation goal

Across the three examples, the smallest necessary information appears to be:

1. **Bounded goal name / desired observation.** Without narrowing, listener endpoint inventory can be confused with service ownership or external network reachability.
2. **Required observations for that bounded claim.** Container ownership needs container inventory and port mapping; service ownership needs a mix of listener, process, systemd, and container observations; listener endpoint inventory needs only local endpoint facts.
3. **Implementation evidence that those observations exist, are absent, or are only pressure.** This comes from observation inventory, observation domains, ownership discrepancies, and capability needs.
4. **Authority requirement for each required observation.** This comes from privilege guidance, permission classes, or the observation implementation boundary.
5. **Authority profile.** The constrained profile decides whether Docker/root, active probing, local passive reads, or external providers are available.
6. **Boundary / non-inference statements.** These are necessary to avoid turning a reachable endpoint inventory into an ownership or health claim.
7. **Uncertainty.** Each example preserves what remains unknown after the bounded outcome.

## Information that appears unnecessary for these three examples

The reviewed examples did not need:

- A generic planner.
- A generic reachability engine.
- A new ontology.
- A new capability model.
- A new observation model.
- Provider acquisition logic.
- Permission creation or approval storage.
- Event-ledger writes.
- Cluster mutation.
- Active network probe results.
- External provider query results.
- Full host/service/container truth.
- Health, intent, dependency, causality, or desired-state interpretation.
- Network reachability from a remote vantage point.
- A complete graph of all possible observations.

They also did not require every related implementation name to be normalized. Name mismatch is a limitation, but the existing examples can still be characterized without introducing a new model.

## Strongest supporting evidence

1. **Container ownership is an implemented authority slice.** It has a fixed desired observation, fixed required observations, required authority guidance, supplied authority profile, outcome, remaining observations, uncertainty, and read-only boundary.
2. **Ownership diagnostics already produce capability needs.** Service conflicts map to required observations/capabilities, and `capability_needs` aggregates those current and recorded diagnostic needs.
3. **Observation domains already bridge some capabilities to observed/unobserved domains.** Listener process pressure maps to `local_listeners`; container inventory and container port mapping map to `container_runtime`.
4. **Privilege discovery already distinguishes authority requirements.** Listener process inventory is partial non-root, container capabilities require Docker/root, and systemd inventory is available.
5. **Observation inventory is implementation-derived.** Provider and predicate evidence is discovered from Python implementations rather than invented by reports.
6. **The listener endpoint slice is bounded by implemented local passive facts.** It can be reachable without asserting ownership, health, or external network reachability.

## Strongest contradictory evidence

1. **Only container ownership has a dedicated evaluator.** Service ownership and listener endpoint inventory are investigation-backed assemblies of existing evidence, not peer evaluator outputs.
2. **Outcome terms are not one shared code enum.** `blocked` is implemented for container ownership; `partially reachable` and `reachable` are investigation vocabulary; `partially_observed` and `unobserved` are domain visibility classifications rather than authority outcomes.
3. **Service capability names are not fully aligned.** `systemd_unit_inventory` does not exactly match `systemd_inventory`; `tcp_listen_inventory` is not the same as `listener_process_inventory`; `process_inventory` lacks dedicated guidance.
4. **Observation permission does not evaluate the whole constrained profile.** It classifies observation activities and reusable approval state, but it does not synthesize root/Docker/local-passive/network/external authority into an outcome.
5. **Observation domains can mark local listeners as partially observed when ownership pressure exists.** This means listener endpoint inventory must stay narrowly bounded; otherwise it collapses into partial service ownership.

## Answer to the acceptance question

### Are these three observation goals instances of the same reasoning pattern?

Yes, with an important boundary: they are instances of the same recurring reasoning shape, not instances of one existing generic implementation.

The shared shape is visible in how each example:

1. Narrows the desired observation.
2. Identifies the observations required for that bounded claim.
3. Checks implementation-backed observation/domain/provider evidence.
4. Joins required observations to privilege or permission guidance where available.
5. Applies the constrained authority profile.
6. Reports an outcome with explicit remaining uncertainty.
7. Preserves read-only / no-mutation boundaries.

### Smallest implementation-backed description of the pattern

```text
A bounded observation goal is evaluated by comparing its required observations
against implementation-backed observation evidence and authority guidance under
a supplied authority profile, then reporting the bounded outcome and the
uncertainty that remains outside or inside the goal.
```

That description is intentionally descriptive. It does not require a framework, planner, evaluator abstraction, ontology, or model change.

## Files changed

- `docs/observation_goal_common_shape_investigation.md`

## LOC changed

- Added this investigation report only.

## Tests and checks run

- `python scripts/seed_local.py --container-ownership-authority --json`
- `python scripts/seed_local.py --observation-domains local_listeners --json`
- `python scripts/seed_local.py --observation-domains container_runtime --json`
- `python scripts/seed_local.py --observation-inventory --json`
- `python scripts/seed_local.py --observation-permission --json`
- `python scripts/seed_local.py --privilege-discovery --json`
- `python -m pytest -q tests/test_container_ownership_authority.py tests/test_ownership_discrepancies.py tests/test_privilege_discovery.py tests/test_observation_domains.py tests/test_observation_permission.py tests/test_observation_inventory.py`
- Initial broader pytest command including `tests/test_capability_needs.py` failed because that test file does not exist in this repository.

## Recommended next investigation

Investigate only the name-alignment gaps that affected this characterization:

```text
systemd_unit_inventory vs systemd_inventory
tcp_listen_inventory vs local listener endpoint inventory
listener_process_inventory vs bounded listener endpoint inventory
process_inventory privilege guidance
```

The next investigation should remain descriptive unless a specific failing command or visibility gap requires implementation work.
