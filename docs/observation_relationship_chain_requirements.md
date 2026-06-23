# Observation Relationship Chain Implementation Requirements

This document scopes the smallest implementation requirements for making existing observation, capability, and permission relationships visible as reusable reasoning chains. It exists to support capability-under-constraint reasoning, not to start a new conceptual branch.

Repository authority remains executable implementation, tests, diagnostic inventory, shape-audit metadata, and existing read-only boundaries.

## Current implementation map

| Surface | Current representation | Relationship role | Boundary |
| --- | --- | --- | --- |
| `observation_inventory` | `ObservationProviderInventory`, `ObservationPredicateInventory`, and `ObservationFamilyInventory` are built from AST discovery of provider classes and observation predicate literals. | Source-derived provider -> predicate -> family inventory. | Read-only inventory; does not explain why a family matters operationally. |
| `ownership_discrepancies` | `_CAPABILITY_NEEDS_BY_CONFLICT` maps ownership conflict classes to needed evidence, candidate capability, and privilege label; `diagnostic_capability_need_records()` emits diagnostic-only records. | Strongest current source of conflict -> capability pressure. | Can record diagnostic-run scoped facts; tests assert entity facts are not mutated. |
| `capability_needs` | `CapabilityNeedEntry` aggregates current rows and recorded `diagnostic_run:*` facts by capability, subjects, diagnostics, needed evidence, and diagnostic runs. | Reusable pressure aggregation. | Drops most upstream conflict context and does not expose observation domain or permission path. |
| `observation_domains` | `CAPABILITY_TO_DOMAIN` maps `listener_process_inventory`, `container_inventory`, and `container_port_mapping` to domains; report combines inventory families, utilization, capability needs, and classifications. | Strongest existing observation bridge from capability pressure to `local_listeners` / `container_runtime`. | Does not preserve full chain with conflict, operational benefit, access, and permission links. |
| `observation_permission` | `SUPPORTED_OBSERVATION_CLASSES` maps `docker_socket_read` to `local_privileged` and other observation activities to observation classes; approval lookup determines permission state. | Permission/access visibility for observation activities. | Does not link `docker_socket_read` to Docker-backed container capabilities. |
| `privilege_discovery` | `_CAPABILITY_GUIDANCE` maps capabilities to access level, operational benefit, suggested next step, and notes. | Capability -> access/benefit guidance, including Docker-group/root constraints. | Separate from observation domain and permission activity. |
| `capability_relationship` | Combines `capability_needs` pressure with `_guidance_for()` access and operational benefit in one read-only report. | Best existing target for capability/access/benefit co-location. | Does not include observation-domain classifications or permission activities. |

## Relationship chain examples to expose

Minimum reusable chains should be expressible as structured read-model rows, not only prose:

1. `owner_not_observed -> listener_process_inventory -> local_listeners -> partially_observed`.
   - Meaning: `listener_process_inventory` matters because it reduces owner-not-observed pressure for local listener visibility and service ownership attribution.
2. `owner_not_observed -> container_inventory -> container_runtime -> unobserved`.
   - Meaning: `container_inventory` matters because container runtime pressure exists and the container observation domain is unavailable or blocked.
3. `owner_not_observed -> container_port_mapping -> container_runtime -> docker_group_or_root`.
   - Meaning: `container_port_mapping` matters because service attribution needs container port mapping and access is Docker/root constrained.
4. `docker_socket_read -> local_privileged -> docker_group_or_root -> container_inventory/container_port_mapping`.
   - Meaning: `docker_socket_read` matters because it is the local privileged permission/access path relevant to Docker-backed container observation capabilities.

## Visibility gaps

- The relationships are implementation-backed but split across source constants, diagnostic records, and CLI formatting outputs.
- `ownership_discrepancies` knows conflict -> capability pressure, but its records do not preserve downstream observation domain, benefit, or permission path.
- `capability_needs` aggregates pressure but not why the capability matters beyond needed evidence and diagnostics.
- `observation_domains` maps capability -> domain and domain classification, but not upstream conflict details or permission activities.
- `observation_permission` maps observation activity -> observation class and approval state, but not activity -> capability pressure.
- `capability_relationship` co-locates pressure, access, and benefit, but not domain classification or permission activity.
- The chain is therefore manually reconstructable by joining current outputs, not reusable as a read model.

## Candidate implementation locations

| Candidate | Fit | Cost / risk | Recommendation |
| --- | --- | --- | --- |
| Extend `observation_domains` output | Good for capability -> domain and classification. | Would overload a domain report with access and permission details. | Useful later for exact source links, not the smallest full chain. |
| Extend `capability_needs` entries | Good for preserving pressure provenance. | Risks turning an aggregation into a broad relationship explainer. | Avoid as primary target; only add fields if chain builder needs them. |
| Add an observation relationship read-model helper | Best separation: one helper can join existing surfaces without new CLI first. | New helper must stay narrow and avoid becoming a generic catalog. | Recommended smallest implementation target. |
| Teach `capability_relationship` to include observation-domain and permission links | Best existing CLI/read-model shell for operator questions like “why does this capability matter?” | Requires diagnostic inventory and shape-audit updates if output shape changes. | Recommended first exposed surface after adding helper. |
| Record richer diagnostic provenance | Could preserve upstream conflict details. | Recording changes require extra boundary tests and risk diagnostic facts looking like cluster truth. | Not first slice. |
| Add a narrow chain-builder used by existing commands | Good if implemented as a private/read-model helper consumed by `capability_relationship`. | Needs careful tests to prevent conceptual sprawl. | Recommended concrete slice. |

## Recommended smallest slice

Implement a narrow read-model helper, for example `seed_runtime/observation_relationship_chains.py`, that joins existing implementation-backed sources and returns chain rows for only the currently supported capability-under-constraint relationships.

Required row shape:

- `capability`
- `source_diagnostic`
- `source_conflicts`
- `needed_evidence`
- `observation_domain`
- `domain_classification`
- `domain_gap_type`
- `current_access`
- `operational_benefit`
- `permission_activity` when known, such as `docker_socket_read`
- `observation_class` when known, such as `local_privileged`
- `pressure_subject_count`
- `reasoning` as implementation-backed short strings
- `boundary` inherited as read-only, no event-ledger writes, no cluster mutation

Initial supported mappings should be deliberately small:

| Capability | Domain | Permission activity | Reasoning requirement |
| --- | --- | --- | --- |
| `listener_process_inventory` | `local_listeners` | none | Reduces `owner_not_observed` pressure for local listener visibility / service ownership attribution. |
| `container_inventory` | `container_runtime` | `docker_socket_read` | Container runtime pressure exists and observation is unavailable or blocked. |
| `container_port_mapping` | `container_runtime` | `docker_socket_read` | Service attribution needs container port mapping and Docker/root-constrained access. |

Then extend `capability_relationship` rows with the helper output fields. This reuses an existing diagnostic/read-only CLI that already answers capability significance questions and already appears in diagnostic inventory and shape-audit metadata. Because output shape changes, update diagnostic inventory descriptions/specs if needed and add shape-audit coverage.

## Files likely touched

- `seed_runtime/observation_relationship_chains.py` or equivalent narrow helper.
- `seed_runtime/capability_relationship.py` to include chain fields in dataclasses, JSON, and formatting.
- `seed_runtime/diagnostic_inventory.py` if the description or shape metadata needs to reflect the richer read model.
- `seed_runtime/diagnostic_shape_audit.py` if implementation specs need new markers or consistency expectations.
- `tests/test_capability_relationship.py` for human/JSON chain output.
- `tests/test_observation_domains.py` only if exact domain output changes.
- `tests/test_observation_permission.py` only if permission output changes.
- `tests/test_diagnostic_inventory.py` and `tests/test_diagnostic_shape_audit.py` if any diagnostic surface shape/registry entry changes.

## Tests required

Required targeted tests:

- `listener_process_inventory` chain includes `owner_not_observed`, `local_listeners`, `partially_observed`, and service ownership attribution reasoning.
- `container_inventory` chain includes `container_runtime`, `unobserved` or blocked/unavailable classification, Docker/root access, and container observation reasoning.
- `container_port_mapping` chain includes service attribution, container port mapping, `container_runtime`, and Docker/root access.
- `docker_socket_read` chain includes `local_privileged` and links to Docker-backed container capabilities.
- JSON output preserves structured fields, not only prose.
- Human output renders the chain without implying acquisition guidance or permission grant.
- Read-only boundary remains `read_only=true`, `writes_event_ledger=false`, `mutates_cluster=false`.
- Existing diagnostic inventory and shape-audit tests continue to pass.

If a CLI output shape changes, run:

```text
pytest -q tests/test_capability_relationship.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

If `observation_domains` or `observation_permission` output changes, also run their focused tests.

## Risks

- Overloading `capability_needs` with explanation data could obscure its role as pressure aggregation.
- Adding a broad relationship catalog would create conceptual scope beyond the mission.
- Recording richer provenance could blur diagnostic-run facts into cluster truth unless carefully scoped.
- Linking `docker_socket_read` to Docker-backed capabilities must not imply permission is granted.
- Domain classification can be state-dependent; tests should use controlled state or monkeypatched needs rather than assume a live host condition.
- A helper that scans many unrelated surfaces could become a hidden ontology; keep the first mapping explicit and small.

## Non-goals

- No new ontology.
- No runtime authorization enforcement.
- No approval creation.
- No network-active probing.
- No Docker probing.
- No root probing.
- No mutation of cluster truth.
- No diagnostic facts attached directly to hosts, services, filesystems, containers, or runtime entities as truth.
- No new large generic relationship catalog.
- No autonomous acquisition or planning behavior.

## Rollback path

- Revert the helper and `capability_relationship` field additions.
- Restore prior `capability_relationship` JSON and human formatting tests.
- Keep existing `observation_domains`, `observation_permission`, `capability_needs`, and `privilege_discovery` behavior unchanged.
- Because the recommended slice is read-only and should not write events, rollback should not require data migration.

## Recommended next implementation slice

Add the narrow chain-builder helper and consume it from `capability_relationship` only. The first implementation should expose the four acceptance chains above as read-only structured fields and should not add recording, authorization, probing, approvals, cluster mutation, or a generic relationship catalog.
