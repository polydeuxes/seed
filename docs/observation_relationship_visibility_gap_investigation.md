# Observation Relationship Visibility Gap Investigation

This is a discovery-only investigation. It does not implement new surfaces,
relationship catalogs, workflow systems, runtime behavior, authority behavior, or
ontology changes. Repository authority remains implementation-backed behavior,
tests, executable diagnostics, and existing repository-visible documents.

## Scope and method

Reviewed implementation-backed observation surfaces:

- `observation_inventory`
- `ownership_discrepancies`
- `capability_needs`
- `observation_domains`
- `observation_permission`

Reviewed stronger comparison surfaces:

- `reference_selection`
- `capability_relationship`
- `projection_shape`
- consumer/structural drilldown style visibility through `consumer_audit`
- `relationship_catalog`

Visibility categories used here:

| Category | Meaning in this investigation |
| --- | --- |
| `repository_visible` | A reusable CLI/API/repository surface exposes the relationship as a relationship, not just as separate facts. |
| `surface_visible_only` | One surface exposes the relation locally, but another repository surface does not preserve or navigate it as reusable explanation. |
| `reconstructable` | The relationship can be manually reconstructed by combining implementation-backed outputs or source evidence. |
| `implementation_hidden` | The relationship exists in implementation constants, branching, private helper behavior, or formatting logic but is not visible as output. |
| `unsupported` | The searched-for relationship is not supported by current implementation evidence. |

## Relationship chains reviewed

### `observation_inventory`

`observation_inventory` preserves provider-to-predicate and predicate-to-family
relationships. It discovers provider classes under `seed_runtime/`, extracts
`Observation(predicate=...)` string literals and provider observation helper
calls, groups providers by predicate, and derives families from predicate name
prefixes before the first underscore.

Visible relationships:

| Relationship | Evidence location | Visibility classification | Visibility boundary |
| --- | --- | --- | --- |
| provider -> predicate | `ObservationProviderInventory.predicates`; JSON `providers[].predicates` | `repository_visible` | Preserved in `--observation-inventory` output. |
| predicate -> provider | `ObservationPredicateInventory.providers`; JSON `predicates[].providers` | `repository_visible` | Preserved in `--observation-inventory` output. |
| predicate -> family | `_families()` groups predicate prefixes | `surface_visible_only` | Exposed inside inventory, but not connected to domain pressure or permission reasoning. |
| family -> observed observation family | `observation_domains` consumes inventory families | `reconstructable` | Domain surface uses families, but inventory output itself does not explain domain significance. |
| predicate/provider -> diagnostic consumption | `observation_utilization` and `consumer_audit`, not inventory | `reconstructable` | Requires leaving inventory and joining with utilization/consumer surfaces. |

Visibility loss:

- Inventory can say that listener predicates exist and which provider emits them.
- It cannot say why the listener family matters, which diagnostic pressure it
  reduces, or whether a domain is partially observed.
- The family derivation is reusable only as inventory data, not as an explanation
  edge from `listener` family to `local_listeners` domain pressure.

### `ownership_discrepancies`

`ownership_discrepancies` preserves diagnostic relationships among evidence,
ownership candidates, conflicts, reasons, and diagnostic-only capability needs.
It includes implementation-backed maps from conflict class to needed evidence,
candidate capability, and privilege level.

Visible relationships:

| Relationship | Evidence location | Visibility classification | Visibility boundary |
| --- | --- | --- | --- |
| evidence predicate -> service/storage ownership row | `_SERVICE_PREDICATES`, `_STORAGE_PREDICATES`, diagnostic builders | `surface_visible_only` | Output rows show evidence and reason, but predicate class membership is mostly source-level. |
| local listener evidence -> owner_not_observed | `_diagnose_service_subject()` listener branch | `surface_visible_only` | Human/JSON row can expose conflict and reason for a subject. |
| owner_not_observed -> listener_process_inventory | `_CAPABILITY_NEEDS_BY_CONFLICT` | `surface_visible_only` | Recorded through diagnostic capability need records; not explained as reducing pressure. |
| owner_not_observed -> container_port_mapping | `_CAPABILITY_NEEDS_BY_CONFLICT` | `surface_visible_only` | Same boundary. |
| owner_not_observed -> container_inventory | `_CAPABILITY_NEEDS_BY_CONFLICT` | `surface_visible_only` | Same boundary. |
| observed listener process evidence -> suppress listener_process_inventory need | `diagnostic_capability_need_records()` filters the need | `implementation_hidden` | The absence of the need is visible, but the suppression reason is not output as a reusable relationship. |

Visibility loss:

- The surface explains a discrepancy row locally.
- It emits/derives capability-need records, but those records do not preserve the
  full explanation: conflict -> missing evidence -> candidate capability ->
  observation domain -> operational benefit.
- The most important hidden edge is negative/conditional: if listener process
  predicates are already present, `listener_process_inventory` is removed from
  pressure. That reasoning is implementation-backed but not repository-visible as
  an explanation.

### `capability_needs`

`capability_needs` aggregates current and recorded diagnostic capability needs by
capability. It reads current `ownership_discrepancies` rows and recorded
`diagnostic_run:*` facts with predicate `diagnostic_capability_need`.

Visible relationships:

| Relationship | Evidence location | Visibility classification | Visibility boundary |
| --- | --- | --- | --- |
| diagnostic conflict record -> capability | `_add_capability_need()` extracts `candidate_capability` | `repository_visible` | Output groups by capability. |
| capability -> affected subjects | `CapabilityNeedEntry.subjects` | `repository_visible` | Output shows subject count and JSON subject list. |
| capability -> diagnostics | `CapabilityNeedEntry.diagnostics` | `repository_visible` | Output shows diagnostic names. |
| capability -> needed evidence | `CapabilityNeedEntry.needed_evidence` | `repository_visible` | Output shows needed evidence labels. |
| capability -> diagnostic run scope | `CapabilityNeedEntry.diagnostic_runs` | `surface_visible_only` | Present in object, not included in JSON formatter. |
| capability priority ordering | `_capability_priority()` | `implementation_hidden` | Sorting exists but is not explained as a relationship. |

Visibility loss:

- The surface preserves pressure, but not the upstream conflict reason and not the
  downstream observation-domain classification.
- `listener_process_inventory` can be seen as needed evidence/capability, but the
  repository-visible output does not say it matters because it reduces
  `owner_not_observed` pressure for `local_listeners`.

### `observation_domains`

`observation_domains` combines inventory families, utilization diagnostic
consumption, capability needs, and a hard-coded capability-to-domain mapping.
It is the strongest current observation-specific bridge, but it still summarizes
rather than preserves complete chains.

Visible relationships:

| Relationship | Evidence location | Visibility classification | Visibility boundary |
| --- | --- | --- | --- |
| listener_process_inventory -> local_listeners | `CAPABILITY_TO_DOMAIN` | `repository_visible` | Output exposes local listener pressure. |
| container_inventory -> container_runtime | `CAPABILITY_TO_DOMAIN` | `repository_visible` | Output exposes container runtime pressure. |
| container_port_mapping -> container_runtime | `CAPABILITY_TO_DOMAIN` | `repository_visible` | Output exposes container runtime pressure. |
| inventory families/predicates -> observed domain | `listener_observed`, `container_observed` checks | `surface_visible_only` | Output gives classification/evidence, not exact predicates/providers. |
| capability pressure -> partially_observed/unobserved classification | classification branches | `repository_visible` | Output exposes classification and pressure. |
| diagnostic-consumed listener predicates -> domain evidence | utilization intersection | `surface_visible_only` | Output says consumed by diagnostics, but not which diagnostic or why. |

Visibility loss:

- This surface can answer whether `local_listeners` is partially observed and
  whether `container_runtime` is unobserved.
- It cannot preserve the full upstream chain from `owner_not_observed` to the
  pressure without manually consulting `ownership_discrepancies` and
  `capability_needs`.
- It uses `CAPABILITY_TO_DOMAIN` as implementation authority, but that mapping is
  not navigable outside the surface except by reading source or inferring from
  domain output.

### `observation_permission`

`observation_permission` preserves domain-to-observation-class and
domain-to-permission-state relationships for a small set of observation activity
names.

Visible relationships:

| Relationship | Evidence location | Visibility classification | Visibility boundary |
| --- | --- | --- | --- |
| docker_socket_read -> local_privileged | `SUPPORTED_OBSERVATION_CLASSES` | `repository_visible` | Output exposes observation class. |
| active_network_probe -> network_active | `SUPPORTED_OBSERVATION_CLASSES` | `repository_visible` | Output exposes observation class. |
| traffic_capture -> network_passive | `SUPPORTED_OBSERVATION_CLASSES` | `repository_visible` | Output exposes observation class. |
| neighbor_table_read -> local_passive | `SUPPORTED_OBSERVATION_CLASSES` | `repository_visible` | Output exposes observation class. |
| domain approval -> granted reusable permission | `_approval_for_domain()` and `_domain_entry()` | `repository_visible` | Output exposes approval evidence when present. |
| manual invocation -> no reusable permission | `_domain_entry().reasoning` | `repository_visible` | Output explains boundary. |

Visibility loss:

- The surface can explain permission/authority boundaries for
  `docker_socket_read`, but it does not connect `docker_socket_read` to
  container inventory or container port mapping pressure.
- Therefore `docker_socket_read matters` is only partially answerable: it matters
  as a local privileged observation activity; its relationship to container
  runtime pressure is reconstructable through privilege/capability guidance, not
  directly preserved by `observation_permission`.

## End-to-end reasoning tests

### Why does `listener_process_inventory` matter?

Implementation-backed links:

1. `owner_not_observed` service conflicts create `listener_process_inventory`
   needs in `ownership_discrepancies`.
2. `capability_needs` aggregates that capability by affected subjects,
   diagnostics, and needed evidence.
3. `observation_domains` maps `listener_process_inventory` to
   `local_listeners`.
4. `capability_relationship` adds operational benefit: service ownership
   attribution.

Where visibility is lost:

- No single repository-visible surface preserves the complete sentence:
  `listener_process_inventory matters because it reduces owner_not_observed
  pressure for local listener visibility and improves service ownership
  attribution`.

Classification: `reconstructable`.

Current repository-visible explanation possible: partially. The repository can
show capability pressure, local listener domain pressure, and operational benefit,
but the complete causal/explanatory chain must be manually joined.

### Why does `container_inventory` matter?

Implementation-backed links:

1. `owner_not_observed` and `insufficient_evidence` service conflicts create
   `container_inventory` needs.
2. `capability_needs` aggregates affected subjects and diagnostics.
3. `observation_domains` maps `container_inventory` to `container_runtime` and
   classifies the domain as `unobserved` when pressure exists without container
   observation family evidence.
4. `capability_relationship` gives operational benefit: container ownership
   attribution.
5. `privilege_discovery` says access is `docker_group_or_root` and commonly
   requires Docker socket, Docker group, or root-equivalent visibility.

Where visibility is lost:

- `observation_domains` preserves domain pressure but not the ownership conflict
  origin.
- `capability_relationship` preserves benefit but not the observation-domain
  classification.

Classification: `reconstructable`.

Current repository-visible explanation possible: partially. It can answer that
container runtime is unobserved and under `container_inventory` pressure, and
that the capability benefits container ownership attribution. It cannot present
that as one reusable chain.

### Why does `container_port_mapping` matter?

Implementation-backed links:

1. `owner_not_observed` service conflicts create `container_port_mapping` needs.
2. `capability_needs` aggregates them.
3. `observation_domains` maps `container_port_mapping` to `container_runtime`.
4. `capability_relationship` gives operational benefit: container
   port-to-service attribution.
5. `privilege_discovery` ties it to Docker socket/group/root visibility.

Where visibility is lost:

- Same as `container_inventory`: conflict origin, observation-domain pressure,
  permission/access boundary, and operational benefit live on separate surfaces.

Classification: `reconstructable`.

Current repository-visible explanation possible: partially.

### Why does `owner_not_observed` create pressure?

Implementation-backed links:

1. `ownership_discrepancies` creates `owner_not_observed` when local listener
   evidence confirms a socket but service/container ownership remains
   unverified, or process/container owner attribution is unavailable.
2. `_CAPABILITY_NEEDS_BY_CONFLICT` maps that conflict to listener process,
   container port mapping, and container inventory needs.
3. `diagnostic_capability_need_records()` emits diagnostic-only records for that
   conflict.
4. `capability_needs` aggregates the records.

Where visibility is lost:

- The local ownership row reason is visible.
- The capability pressure is visible.
- The explicit bridge from row reason/conflict to downstream domain pressure is
  not reusable as one repository-visible relationship.

Classification: `surface_visible_only` for the conflict-to-capability map;
`reconstructable` for the full pressure explanation.

Current repository-visible explanation possible: partially.

### Why does `local_listeners` appear partially observed?

Implementation-backed links:

1. `observation_inventory` can discover listener/listening predicate families.
2. `observation_utilization` can detect diagnostic consumption of listener
   predicates.
3. `observation_domains` maps `listener_process_inventory` pressure to
   `local_listeners`.
4. `observation_domains` classifies a listener domain with observed listener
   predicates plus pressure as `partially_observed` with gap type
   `missing_evidence_inside_observed_domain`.

Where visibility is lost:

- `observation_domains` output explains classification at a summary level, but
  does not preserve exact provider/predicate evidence or upstream ownership
  conflict origin.

Classification: `repository_visible` for classification; `reconstructable` for
complete cause.

Current repository-visible explanation possible: mostly yes for the domain-level
answer, not for the full diagnostic origin.

### Why does `container_runtime` appear unobserved?

Implementation-backed links:

1. `observation_domains` maps `container_inventory` and
   `container_port_mapping` pressure to `container_runtime`.
2. `observation_inventory` lacks a container observation family in current
   evidence.
3. `observation_domains` classifies pressure without observed container family as
   `unobserved` with gap type `missing_observation_domain`.

Where visibility is lost:

- Domain-level explanation is repository-visible.
- The upstream conflict origin and downstream access/permission boundary are not
  joined in one explanation.

Classification: `repository_visible` for domain classification; `reconstructable`
for end-to-end pressure.

Current repository-visible explanation possible: yes for the direct domain
classification.

### Why does `docker_socket_read` matter?

Implementation-backed links:

1. `observation_permission` maps `docker_socket_read` to `local_privileged` and
   explains reusable permission and future autonomous invocation boundaries.
2. `privilege_discovery` guidance for `container_inventory` and
   `container_port_mapping` mentions Docker socket visibility, docker group
   membership, or root-equivalent visibility.
3. `capability_relationship` explains the operational benefit of those container
   capabilities.
4. `observation_domains` maps those capabilities to `container_runtime`.

Where visibility is lost:

- No direct repository-visible edge connects `docker_socket_read` to
  `container_inventory`, `container_port_mapping`, or `container_runtime`.
- The connection is inferential: Docker socket read is an observation permission
  domain; container capabilities often require Docker socket visibility.

Classification: `reconstructable`, with the direct
`docker_socket_read -> container_runtime pressure` relationship
`implementation_hidden`/not first-class.

Current repository-visible explanation possible: partial and indirect.

## Comparison with stronger visibility chains

| Stronger surface | What it preserves well | Difference from observation relationship visibility |
| --- | --- | --- |
| `reference_selection` | Selected reference, rationale, alternatives, authority boundary, and limitations are preserved together. | Observation chains usually preserve facts and summaries on separate surfaces; rationale and alternatives are not joined. |
| `capability_relationship` | Capability, access, operational benefit, pressure, expectation/attainability limits, reasoning, and boundary are co-present. | Observation surfaces have capability pressure and domains, but not one row that combines conflict, domain, benefit, access, and permission. |
| `projection_shape` | Stage consumes/produces/influences/does-not-influence and authority boundary are explicit. | Observation chains lack equivalent stage-like preservation for provider -> predicate -> family -> domain -> pressure. |
| `consumer_audit` / structural drilldown style | Predicate consumers can be checked by category, and orphaned status is visible. | Observation domain relationships can be reconstructed, but diagnostic consumer links do not become domain explanations. |
| `relationship_catalog` | Relationship definitions are keyed by relationship name and derived predicates. | Observation-domain relationships are mostly local maps/constants, not catalog entries. This is an observation about visibility, not a recommendation to create a catalog. |

Observation relationships are therefore mostly missing explanation and navigation,
not missing implementation-backed objects. Some preservation exists in
`observation_domains` and `capability_relationship`, but the complete chains are
not preserved end to end.

## Repository-visible explanations currently possible

The repository can currently explain:

- which observation providers emit which predicates;
- which predicates belong to derived inventory families;
- which ownership discrepancy rows exist and which local evidence supports them;
- which diagnostic capability needs exist and which diagnostics/subjects they
  affect;
- that `local_listeners` is partially observed when listener evidence exists but
  listener capability pressure remains;
- that `container_runtime` is unobserved when container pressure exists but no
  container observation family is observed;
- that `docker_socket_read` is a local privileged observation activity requiring
  operator expression unless reusable approval is present;
- that container inventory and port mapping have Docker-group/root access
  implications and operational benefits.

## Repository-visible explanations currently impossible as one reusable chain

The repository cannot currently expose, without manual reconstruction:

- `listener_process_inventory matters because it reduces owner_not_observed
  pressure for local listener visibility`;
- `container_inventory matters because owner_not_observed or insufficient service
  evidence creates container-runtime observation pressure and the container
  observation family is absent`;
- `container_port_mapping matters because owner_not_observed service attribution
  pressure maps to the unobserved container_runtime domain`;
- `docker_socket_read matters because it is a local-privileged permission path
  relevant to Docker-backed container inventory and port mapping pressure`;
- exact provider/predicate evidence for an observation-domain classification in
  the same repository-visible row that shows the pressure source.

## Supported conclusions

1. The repository is not primarily missing observation objects for these examples;
   the reviewed relationships already exist in source, diagnostics, tests, or
   output shapes.
2. `observation_inventory` preserves provider/predicate/family visibility but not
   domain-pressure explanations.
3. `ownership_discrepancies` preserves the strongest conflict-to-capability
   pressure implementation, but that relation is mostly local to diagnostic need
   records.
4. `capability_needs` preserves aggregation of pressure but drops most conflict
   reasoning and domain classification context.
5. `observation_domains` is the strongest observation relationship bridge, but
   still summarizes exact upstream and downstream links.
6. `observation_permission` preserves permission-class boundaries but does not
   connect permission activities to capability pressure chains.
7. Stronger surfaces preserve rationale, boundary, influence, or operational
   benefit together; observation relationships usually require manual joins.
8. The gap is best described as missing preservation/navigation/explanation of
   already implementation-backed relationships, not as absent objects or a need
   for new ontology.

## Unsupported conclusions

Current evidence does not support concluding that:

- every observation relationship should become a new catalog entry;
- observation-domain pressure should mutate cluster truth;
- diagnostic findings should attach directly to hosts, services, filesystems, or
  runtime entities;
- Docker socket visibility is currently a granted permission;
- container runtime observation is implemented as a provider;
- `docker_socket_read` directly maps to `container_inventory` in
  `observation_permission`.

## Open questions

- Should future investigations treat conditional negative edges, such as
  suppressing `listener_process_inventory` when listener process predicates are
  present, as first-class visibility gaps?
- Which existing surface, if any, is the least intrusive place to explain an
  end-to-end chain without adding runtime behavior or cluster truth?
- Can `observation_domains` expose exact source links without becoming a new
  relationship catalog?
- Should recorded diagnostic facts retain enough provenance to reconstruct
  conflict -> capability -> domain chains without reading implementation source?
- Is `docker_socket_read` intentionally separate from container capability
  pressure, or is that only an accidental visibility boundary?
