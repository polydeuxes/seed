# Observation relationship implementation evidence investigation

## Scope

This is a discovery-only investigation of relationships that already exist in
implementation evidence among observation-related objects. It does not propose or
implement a relationship catalog, ontology, workflow engine, permission system,
runtime behavior, or new visibility surface.

Reviewed object types:

- providers
- predicates
- predicate families
- coverage areas / observation domains
- capability needs and capability pressure
- permission activities and observation classes
- diagnostic conflicts and ownership discrepancies
- visibility outcomes

Repository authority for this investigation came from runtime code, catalog code,
checked-in catalog data, and existing CLI surfaces. Relationship claims below are
limited to what those implementations preserve.

## Relationship category vocabulary

This document classifies discovered relationships as follows:

| Category | Meaning in this investigation |
| --- | --- |
| Explicitly encoded | A code or catalog structure directly stores a mapping, tuple, reference, or record connecting the two objects. |
| Derived | A function computes the relationship from implemented rules or current state rather than storing a durable edge. |
| Surface-local | The relationship exists inside one diagnostic/report/audit surface and is not preserved as a reusable repository-wide relationship. |
| Cross-surface | The relationship crosses implementation surfaces, such as a diagnostic result feeding a capability view or a capability map feeding an observation-domain report. |
| Investigation-only | The relationship is only stated in prior investigation prose or manually reconstructed from multiple outputs. |
| Unsupported | Current implementation evidence does not preserve the relationship. |

## Implementation-backed relationships discovered

### Provider -> predicate

`observation_inventory` preserves the strongest observation-specific object
relationship reviewed here. It discovers provider classes under `seed_runtime/`,
extracts predicate string literals from provider implementations, and returns
provider records with `predicates`. It also inverts that into predicate records
with `providers`.

Implementation evidence:

- `ObservationProviderInventory` contains `name`, provider class metadata, and a
  tuple of `predicates`.
- `ObservationPredicateInventory` contains a predicate and tuple of `providers`.
- `build_observation_inventory()` extracts provider/predicate relationships by
  AST scanning provider classes and `Observation(...)` or `_observation(...)`
  calls.
- The inventory metadata states that providers are discovered from provider-like
  classes and predicates from observation-construction string literals.

Current inventory evidence reported 7 providers, 75 predicates, and 30 families.
Examples from the implementation-backed inventory include:

| Provider | Predicates / predicate families currently connected |
| --- | --- |
| `ansible_inventory` | `group`, `hostname` |
| `local_host` | 68 predicates, including block, CPU, DNS, filesystem, host identity, listener/listening, mount, process, route, user, and OS predicates |
| `prometheus` | `endpoint_role`, `filesystem_avail_bytes`, `filesystem_size_bytes`, `os`, `up` |
| `systemd` | `systemd_unit`, `systemd_unit_file_state` |

Classification: **explicitly encoded**, **derived**, **surface-local**.

Nuance: the provider/predicate relationship is explicit in the inventory data
model once built, but the source of truth is derived by AST inspection rather
than a hand-maintained provider relationship catalog. It is surface-local to the
observation inventory/utilization surfaces unless another surface reuses the
inventory.

### Predicate -> provider

The same inventory preserves the reverse relationship. During inventory build,
`predicate_to_providers` is populated from provider records, and predicate rows
expose all providers that produce a predicate.

Examples from current inventory evidence:

| Predicate/family evidence | Providers currently connected |
| --- | --- |
| `hostname` | `ansible_inventory`, `local_host` |
| `group` family | `ansible_inventory`, `local_host` |
| `filesystem` family | `local_host`, `prometheus` |
| `listener` and `listening` families | `local_host` |
| `endpoint_role` | `prometheus` |
| `systemd_unit`, `systemd_unit_file_state` | `systemd` |

Classification: **derived**, **surface-local**.

### Predicate -> predicate family

`observation_inventory` computes families by splitting predicate names before the
first underscore. Family rows preserve family name, predicates in that family,
and providers contributing those predicates.

Implementation-backed examples:

| Family | Predicates / providers currently connected |
| --- | --- |
| `filesystem` | `filesystem_avail_bytes`, `filesystem_size_bytes`, `filesystem_type`; providers `local_host`, `prometheus` |
| `listener` | `listener_address`, `listener_attribution_status`, `listener_port`, `listener_protocol`, `listener_scope`; provider `local_host` |
| `listening` | `listening_address`, `listening_endpoint`, `listening_port`, `listening_process_id`, `listening_process_name`, `listening_protocol`, `listening_socket`, `listening_socket_family`; provider `local_host` |
| `group` | `group`, `group_account`, `group_gid`, `group_member`; providers `ansible_inventory`, `local_host` |
| `systemd` | `systemd_unit`, `systemd_unit_file_state`; provider `systemd` |

Classification: **derived**, **surface-local**.

Nuance: this is not semantic family membership. It is a prefix rule. A claim like
"the `listener` family contributes to service ownership" requires separate
implementation evidence from diagnostics or utilization, not just the prefix.

### Predicate family -> coverage area / observation domain

`observation_domains` derives coverage entries from inventory families. For most
families, it creates `<family>_observations` domains with classification
`observed`, gap type `unknown`, and evidence text of the form `<family>
observation family observed`.

Implementation-backed examples:

| Family | Coverage area / domain produced |
| --- | --- |
| `filesystem` | `filesystem_observations` |
| `group` | `group_observations` |
| `hostname` | `hostname_observations` |
| `systemd` | `systemd_observations` |
| most other non-special families | `<family>_observations` |

Special cases are also implemented:

- `listener` and `listening` predicates/families contribute to the
  `local_listeners` domain.
- `container` predicates/family, if present, contribute to `container_runtime`.
- Families named `listener`, `listening`, and `container` are excluded from the
  generic `<family>_observations` generation because special logic handles those
  domains.

Classification: **derived**, **surface-local**, and partially **cross-surface**
because `observation_domains` consumes the observation inventory.

Nuance: for generic families, this is coverage-label generation rather than a
cataloged `family contributes_to coverage_area` relationship. The connection is
visible in the domain report output but not preserved as a reusable edge.

### Capability pressure -> coverage area / observation domain

`observation_domains` contains an explicit `CAPABILITY_TO_DOMAIN` map:

| Capability pressure | Domain |
| --- | --- |
| `listener_process_inventory` | `local_listeners` |
| `container_inventory` | `container_runtime` |
| `container_port_mapping` | `container_runtime` |

The report then combines that map with current capability needs. Pressure can
make a domain visible even when no matching observation family exists. Current
CLI evidence showed `container_runtime` as `unobserved` with pressure
`container_inventory` and `container_port_mapping`, and `local_listeners` as
`partially_observed` with pressure `listener_process_inventory`.

Classification: **explicitly encoded**, **derived**, **cross-surface**.

Nuance: the explicit map is small. It does not mean every capability has a
coverage domain, and it does not mean capability pressure is acquisition intent.
`capability_relationship` explicitly keeps pressure as visibility context with
unknown attainability and expectation.

### Diagnostic conflict / ownership discrepancy -> capability pressure

`ownership_discrepancies` explicitly maps selected `(ownership kind, conflict
class)` pairs to needed evidence, candidate capability, and privilege level. The
function `diagnostic_capability_need_records()` converts an
`OwnershipDiscrepancyRow` into diagnostic-only capability-need records.
`capability_needs` then builds capability-pressure entries from current
ownership-discrepancy rows and from recorded diagnostic facts scoped to
`diagnostic_run:*`.

Implementation-backed examples:

| Diagnostic conflict source | Candidate capability pressure |
| --- | --- |
| `service` + `insufficient_evidence` | `process_inventory`, `container_inventory` |
| `service` + `owner_not_observed` | `listener_process_inventory`, `container_port_mapping`, `container_inventory` |
| `storage` + `missing_owner` | `mount_source_inventory`, `export_visibility_inventory` |
| `storage` + `remote_export_attribution_missing` | `nfs_export_inventory`, `smb_share_inventory`, `remote_storage_export_inventory` |
| `service` + `missing_owner` | `tcp_listen_inventory`, `systemd_unit_inventory` |

There is also a conditional relationship: for `service` +
`owner_not_observed`, listener process capability pressure is removed when the
row evidence already includes `listening_process_id` or `listening_process_name`.

Classification: **explicitly encoded**, **derived**, **cross-surface**.

Nuance: this is one of the strongest observation-adjacent relationships because
it is explicitly tabular in code, crosses from a diagnostic row to capability
pressure, and carries `needed_evidence` plus `privilege_level`. It is still not a
general observation relationship catalog.

### Ownership evidence predicates -> ownership discrepancy conflicts

`ownership_discrepancies` also encodes predicate sets used to identify storage
subjects, service subjects, host predicates, local listener predicates, and
service predicates. Diagnostic functions derive candidate owners and conflicts
from facts with those predicates.

Implementation-backed examples:

- Storage subjects are facts whose predicates are in `_STORAGE_PREDICATES`.
- Service subjects are facts whose predicates are in `_SERVICE_PREDICATES`.
- Endpoint-only service evidence can produce `insufficient_evidence`.
- Local listener evidence can produce or retain `owner_not_observed` when service
  ownership remains unverified.
- Storage source/consumer evidence can produce
  `remote_export_attribution_missing`, `multiple_candidate_owners`,
  `mount_source_conflict`, or `consumer_mistaken_as_owner`.

Classification: **explicitly encoded** for predicate sets and conflict maps,
**derived** for row/conflict production, **surface-local** inside ownership
analysis, and **cross-surface** when capability needs consume the result.

### Predicate -> utilization / visibility outcome

`observation_utilization` joins inventory predicates to implementation mention
checks across projection, read-model, and diagnostic source paths. Each predicate
row carries booleans for `collected`, `projected`, `read_model`,
`diagnostic_consumed`, and a `first_loss` visibility outcome.

Classification: **derived**, **surface-local**.

Nuance: this answers whether a predicate appears to be collected/projected/read
or diagnostically consumed. It does not preserve a semantic relationship such as
"provider X improves coverage area Y". It is a visibility/dead-zone audit.

### Capability pressure -> access / operational meaning

`capability_relationship` derives capability relationship rows from current
capability needs and privilege guidance. Each row connects a capability to
current access context, operational benefit, pressure count, unknown
attainability, unknown expectation, reasoning, and limitations.

Classification: **derived**, **surface-local**, **cross-surface** from capability
needs to relationship visibility.

Nuance: this surface is strong about the boundary: capability pressure is
visibility context, not acquisition guidance, deployment expectation, operator
intent, policy, or planning.

### Permission activity -> observation class -> permission state

`observation_permission` contains an explicit map from supported permission
activities/domains to observation classes:

| Permission activity / domain | Observation class |
| --- | --- |
| `neighbor_table_read` | `local_passive` |
| `traffic_capture` | `network_passive` |
| `active_network_probe` | `network_active` |
| `docker_socket_read` | `local_privileged` |
| `external_provider_query` | `external` |

The surface derives permission state from reusable approvals in state: an
approval whose action is `observation.<domain>` or whose constraints contain
`observation_domain=<domain>` makes the entry `granted`; otherwise known domains
require operator expression and unknown domains remain unknown.

Classification: **explicitly encoded**, **derived**, **surface-local**.

Important unsupported boundary: no reviewed implementation connects these
permission activities to providers, predicates, predicate families, capability
pressure, coverage areas, or visibility outcomes. For example, the repository
currently supports `docker_socket_read -> local_privileged`, but not
`docker_socket_read -> container_runtime`.

### Provider/raw predicate -> canonical predicate

Although not always framed as observation visibility, the predicate catalog
contains provider/raw-to-canonical mappings through `PredicateMapping`, and the
predicate normalizer uses those mappings after provider observations are
preserved. This is stronger than most observation-domain relationships because it
is catalog-backed.

Classification: **explicitly encoded**, **cross-surface** when normalization
uses catalog mappings.

Nuance: this relationship connects raw/provider predicates to canonical
predicates. It does not itself connect providers to coverage areas or
capabilities.

## Cross-surface boundaries already present

The investigation found these implementation-backed cross-surface chains:

1. **Provider implementation -> observation inventory -> observation domain**
   - Provider classes and predicate literals are discovered by
     `observation_inventory`.
   - Families are derived by prefix.
   - `observation_domains` consumes families/predicates to produce observed or
     partially observed coverage entries.

2. **Ownership facts -> ownership discrepancy -> capability need -> observation domain**
   - `ownership_discrepancies` derives diagnostic conflicts from facts.
   - Explicit conflict maps produce diagnostic capability-need records.
   - `capability_needs` aggregates current and recorded diagnostic needs.
   - `observation_domains` maps selected capabilities to domains.

3. **Capability need -> capability relationship**
   - `capability_relationship` consumes capability needs and privilege guidance
     to expose access context, benefit, pressure, and non-acquisition boundary.

4. **Permission approval state -> observation permission report**
   - `observation_permission` checks reusable approvals in state and derives
     permission state for supported observation permission activities.

5. **Inventory predicate -> utilization outcome**
   - `observation_utilization` consumes inventory predicates and source-path
     mention scans to compute projection/read-model/diagnostic visibility and
     first loss.

These chains are implementation-backed. However, most chain joins are report
logic, not reusable relationship records.

## Missing relationship visibility

Current implementation evidence does **not** consistently preserve these
relationships:

| Asked relationship | Current status |
| --- | --- |
| Which provider contributes to which final coverage outcome? | Partly reconstructable through provider -> predicate -> prefix family -> generated domain, but not preserved as a single provider-to-domain or provider-to-outcome relationship. |
| Which capability improves which coverage area? | Supported only for `listener_process_inventory`, `container_inventory`, and `container_port_mapping` through `CAPABILITY_TO_DOMAIN`; unsupported for other capability pressures unless another explicit map exists. |
| Which permission activity corresponds to which observation opportunity? | Unsupported beyond permission activity -> observation class and approval-derived permission state. No provider/predicate/domain joins were found. |
| Which mechanism satisfies which pressure? | Not preserved for observation mechanisms generally. Capability catalogs can recommend providers/handoffs for capabilities, but observation-domain pressure satisfaction is not represented as an implemented relationship. |
| Which diagnostic conflict produces which capability pressure? | Strongly supported for selected ownership discrepancy conflicts. Not general across every diagnostic. |
| Which predicate contributes to which semantic family? | Only prefix-derived family membership is supported in observation inventory. Semantic family membership is unsupported unless supplied by another catalog/surface. |
| Which family contributes to which coverage area? | Derived for generic `<family>_observations` and special-cased listener/container domains, but not cataloged as durable relationship records. |

## Comparison with stronger repository relationship structures

Observation relationships are real but generally weaker and less reusable than
several existing repository relationship structures.

### Relationship catalog

The relationship catalog has named relationship definitions with relationship
kind, subject type, object type, and `derived_from_predicates`. It indexes
relationships by predicate and exposes stable lookup/list operations.
Observation relationships usually lack this shape. Provider-to-predicate and
conflict-to-capability are implemented, but observation-domain relationships are
not named first-class relationship definitions with subject/object types.

Assessment: observation relationships are **weaker and less visible** than the
relationship catalog.

### Entity types

Entity types are checked-in catalog objects. Observation classes and coverage
areas are mostly report-local values or hard-coded maps. They do not have the
same catalog identity, validation, or projection role.

Assessment: observation classes/domains are **weaker** than entity types.

### Predicate catalog

The predicate catalog defines canonical predicates and provider/raw mappings.
This is stronger than prefix-derived observation families because mappings are
explicit records that validate against known canonical predicates. Observation
inventory families are computed by string prefix and do not validate semantic
membership.

Assessment: provider/raw -> canonical predicate relationships are **stronger**
than observation family/domain relationships.

### Capability mappings

Capability catalog entries map capabilities to provider/handoff recommendations.
`ownership_discrepancies` maps diagnostic conflicts to candidate capabilities,
and `observation_domains` maps a small subset of capability pressures to
domains. The capability catalog is more durable for recommendation purposes, but
it does not itself answer observation coverage improvement unless joined by
separate code.

Assessment: capability mappings are **stronger for recommendations**; observation
capability-to-domain mappings are **narrower and less visible**.

### Reference selection relationships

Reference selection relationships preserve selection/comparison context more
explicitly than observation domain relationships. Observation relationships often
need reconstruction from reports and code paths.

Assessment: observation relationships are **less visible**.

### Projection stage relationships

Projection stages generally encode transformation boundaries and projection
outputs. Observation relationships have partial transformation chains
(provider/predicate normalization, inventory, domain reports) but not a unified
relationship-preservation model.

Assessment: observation relationships are **weaker as reusable projected
relationships**, though some are strong within local surfaces.

## Supported conclusions

1. The repository already preserves provider -> predicate and predicate ->
   provider relationships through `observation_inventory`.
2. The repository already derives predicate -> prefix family relationships and
   family -> generic coverage labels through `observation_inventory` and
   `observation_domains`.
3. The repository already preserves a small explicit capability pressure ->
   observation domain map for listener process inventory and container inventory
   pressures.
4. The repository already preserves selected diagnostic conflict -> capability
   pressure relationships for ownership discrepancies.
5. The repository already derives predicate visibility outcomes through
   `observation_utilization`.
6. The repository already preserves permission activity -> observation class
   relationships and approval-derived permission state through
   `observation_permission`.
7. Observation relationships exist, but most are local to reporting/diagnostic
   surfaces rather than reusable repository-wide relationships.
8. The strongest observation-adjacent relationships are:
   - provider -> predicate inventory;
   - ownership conflict -> needed evidence/candidate capability;
   - capability pressure -> local listener/container coverage domains;
   - permission activity -> observation class.

## Unsupported conclusions

Current implementation evidence does not support claiming that:

- every provider contributes to a known coverage area;
- every predicate family has semantic coverage meaning beyond its prefix-derived
  label;
- `docker_socket_read` maps to `container_runtime`;
- permission activities map to providers, predicates, or capability pressure;
- capability pressure implies acquisition, deployment expectation, operator
  intent, policy, planning, or runtime action;
- diagnostic conflicts outside reviewed ownership-discrepancy mappings produce
  capability pressures;
- provider recommendations satisfy observation-domain pressure;
- visibility outcomes are durable knowledge relationships rather than report
  results.

## Open questions

1. Should provider -> predicate -> family -> domain joins remain report-local, or
   should they become reusable relationship records?
2. Should observation-domain names become catalog entries with definitions and
   explicit contributors?
3. Should permission activities ever connect to observation opportunities, or is
   the current permission boundary intentionally independent?
4. Should capability pressure -> coverage-area mappings be expanded beyond the
   current listener/container subset?
5. Should diagnostic conflict -> capability pressure mappings exist for other
   diagnostics, or are ownership discrepancies the only implementation-backed
   source today?
6. Should predicate families remain prefix-derived, or should semantically
   meaningful families be cataloged separately?
7. Should observation utilization first-loss outcomes become durable evidence of
   relationship gaps, or remain audit-only output?

## Acceptance answers

### What observation relationships already exist?

Provider -> predicate, predicate -> provider, predicate -> prefix family, family
-> generated observation-domain label, selected capability pressure -> domain,
selected ownership diagnostic conflict -> needed evidence/candidate capability,
predicate -> utilization/first-loss outcome, capability need -> access/benefit
relationship, and permission activity -> observation class/permission state.

### Which are explicitly encoded?

Explicitly encoded relationships include:

- provider inventory data model fields after inventory construction;
- ownership conflict -> needed evidence/candidate capability/privilege tuples;
- capability pressure -> domain entries in `CAPABILITY_TO_DOMAIN`;
- permission activity -> observation class entries in
  `SUPPORTED_OBSERVATION_CLASSES`;
- provider/raw predicate -> canonical predicate mappings in the predicate
  catalog;
- relationship catalog definitions for general topology relationships, by
  comparison.

### Which are derived?

Derived relationships include:

- provider/predicate discovery from AST inspection;
- predicate -> family by prefix split;
- family -> `<family>_observations` coverage labels;
- ownership facts -> diagnostic conflicts;
- capability needs aggregated from current diagnostics and recorded diagnostic
  facts;
- observation-domain classifications and gap types;
- predicate utilization first-loss outcomes;
- approval state -> permission state.

### Which cross-surface boundaries already exist?

Cross-surface boundaries exist from observation inventory to observation domains,
from ownership discrepancies to capability needs, from capability needs to
observation domains, from capability needs to capability relationship visibility,
from state approvals to observation permission visibility, and from observation
inventory to utilization audits.

### Which observation objects remain disconnected?

Permission activities remain disconnected from providers, predicates,
capabilities, and coverage outcomes. Most providers remain disconnected from
final coverage outcomes except by manual reconstruction through inventory family
logic. Most capability pressures remain disconnected from coverage areas except
for the small listener/container map. Observation classes remain disconnected
from predicate families and diagnostic conflicts. Visibility outcomes remain
report rows rather than durable repository relationships.
