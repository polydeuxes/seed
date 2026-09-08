# Observation-Domain Conceptual Object Investigation

## Scope

This investigation asks what kinds of conceptual objects are currently being
called `observation domain` in repository-backed code and prior investigations.
It is intentionally not implementation, redesign, ontology creation, catalog
design, registry design, inheritance design, permission propagation, or runtime
behavior change.

Repository authority wins. Conclusions below are limited to implementation and
existing documentation evidence in this repository.

## Evidence reviewed

Implementation-backed evidence reviewed during this investigation:

```bash
sed -n '1,240p' seed_runtime/observation_domains.py
sed -n '1,260p' seed_runtime/observation_permission.py
sed -n '1,260p' seed_runtime/observation_inventory.py
sed -n '1,220p' seed_runtime/observation_utilization.py
sed -n '1,220p' seed_runtime/capability_needs.py
sed -n '1,220p' seed_runtime/capability_relationship.py
sed -n '1,260p' tests/test_observation_domains.py
sed -n '1,260p' tests/test_observation_permission.py
sed -n '1,520p' docs/observation_domain_vocabulary_fragmentation_investigation.md
sed -n '1,520p' docs/observation_class_repository_concept_investigation.md
sed -n '1,220p' docs/observation_domain_permission_authority_reuse_investigation.md
rg -n "observation[_ -]?domain|SUPPORTED_OBSERVATION_CLASSES|CAPABILITY_TO_DOMAIN|ObservationDomainEntry|ObservationPermissionDomain|selection|projection stage|predicate famil|observation famil|capability" seed_runtime tests docs scripts -S
```

The broad `rg` command produced many matches, so the conclusions below rely on
the directly inspected implementation and existing investigation files rather
than on every documentation mention as equal authority.

## Short answer

Current repository evidence does **not** support one coherent conceptual object
called `observation domain`.

It supports at least two different conceptual object families sharing the word
`domain`:

1. **Visibility / coverage domains** in `observation_domains.py`: diagnostic
   entries that classify whether an area of observation is observed,
   partially observed, unobserved, or unknown, and that attach capability
   pressure plus evidence.
2. **Permission / access domains** in `observation_permission.py`: named
   observation activities or access mechanisms that can be recognized, assigned
   an observation class, checked against reusable approvals, and rendered with a
   permission state.

These are not the same object today. They can participate in the same
observation workflow. For example, `container_runtime` reads like a coverage or
target area whose observations are missing, while `docker_socket_read` reads
like a privileged local access mechanism that could enable observation of that
area. No current implementation-backed mapping proves they are identical.

## Conceptual categories discovered

### 1. Visibility / coverage areas

`observation_domains.py` creates `ObservationDomainEntry` records with:

- `domain`
- `classification`
- `gap_type`
- `pressure`
- `evidence`

The object being classified is a surface-local coverage area, not an access
action. Its classifications are coverage/gap states such as `observed`,
`partially_observed`, `unobserved`, and `unknown`.

Examples:

- `local_listeners`
- `container_runtime`
- generated names like `filesystem_observations`, `dns_observations`, and other
  `<family>_observations` names

Evidence supporting this category:

- The module constructs entries from observation inventory families,
  predicates, capability pressure, and a hard-coded capability-to-domain map.
- `local_listeners` becomes partially observed when listener evidence exists but
  `listener_process_inventory` pressure remains.
- `container_runtime` can become unobserved from `container_inventory` and
  `container_port_mapping` pressure even when no container observation family is
  observed.
- Other inventory families are transformed into `<family>_observations`, which
  are explicitly marked `observed` when a family is present.

Evidence against treating these as one complete domain ontology:

- The identities are derived, not loaded from a domain catalog.
- Family-derived names come from predicate prefixes, not from explicit domain
  definitions.
- Capability-derived names come from `CAPABILITY_TO_DOMAIN`, not from the same
  source as family-derived names.
- The report entry is diagnostic visibility; its boundary is read-only and does
  not write the event ledger or mutate cluster state.

Best category name for understanding: **observation coverage/gap area**.

### 2. Permission / access mechanisms and observation activities

`observation_permission.py` creates `ObservationPermissionDomain` records with:

- `domain`
- `observation_class`
- `permission_state`
- `authority_evidence`
- `reasoning`
- `known_limitations`
- `reusable_permission`
- `future_autonomous_invocation`

The object being authorized is a named observation activity/access boundary, not
a coverage area. Recognized names are keys of `SUPPORTED_OBSERVATION_CLASSES`:

| Permission-domain name | Observation class | Apparent conceptual object |
| --- | --- | --- |
| `neighbor_table_read` | `local_passive` | local passive read activity / source access |
| `traffic_capture` | `network_passive` | passive network observation activity |
| `active_network_probe` | `network_active` | active network observation activity |
| `docker_socket_read` | `local_privileged` | privileged local access mechanism |
| `external_provider_query` | `external` | external-source query activity |

Evidence supporting this category:

- The vocabulary is explicit in `SUPPORTED_OBSERVATION_CLASSES`.
- Unknown filtered strings become unknown permission entries, showing this map
  is the recognized-domain authority for that diagnostic.
- Approval lookup is by `action == "observation.<domain>"` or by an approval
  constraint named `observation_domain` equal to the same string.
- Tests prove the permission state changes to granted when an `Approval` exists
  for `observation.neighbor_table_read`.
- The report explicitly says it is visibility only: no permission enforcement,
  no approval storage, and no runtime autonomy.

Evidence against treating these as coverage areas:

- Names are verbs/actions/mechanisms (`*_read`, `capture`, `probe`, `query`) more
  than observed subject areas.
- They do not derive from observation inventory families.
- They do not carry coverage classification or gap type.
- Current code does not map them to visibility domains such as
  `container_runtime` or `local_listeners`.

Best category name for understanding: **observation permission activity/access
mechanism**.

### 3. Observation families and predicate families

`observation_inventory.py` derives families from predicate names by taking the
prefix before the first underscore. These families are not called domains inside
that module, but `observation_domains.py` converts most families into
`<family>_observations` visibility domains.

Examples include family-derived areas such as:

- `filesystem_observations`
- `dns_observations`
- `endpoint_observations`
- other generated `<family>_observations`

Evidence supporting this category:

- Inventory metadata says providers are discovered from observation provider
  classes, predicates from AST string literals, and families from predicate name
  prefixes.
- `observation_domains.py` directly transforms `families - {"listener",
  "listening", "container"}` into domain names.

Evidence against treating families as permission domains:

- Families do not know permission state, approval state, observation class, or
  reusable permission.
- Family names identify predicate groupings, not access mechanisms.

Best category name for understanding: **observation/predicate family-derived
coverage labels**.

### 4. Capability pressure projected into coverage domains

`capability_needs.py` exposes capability pressure such as:

- `listener_process_inventory`
- `container_inventory`
- `container_port_mapping`

These are not called observation domains by that module, but
`observation_domains.py` maps them to visibility domains through
`CAPABILITY_TO_DOMAIN`.

Evidence supporting this category:

- `CAPABILITY_TO_DOMAIN` maps multiple capability names to `container_runtime`
  and one to `local_listeners`.
- Tests assert that `container_runtime` includes `container_inventory` and
  `container_port_mapping` pressure, and that `local_listeners` includes
  `listener_process_inventory` pressure.
- `capability_relationship.py` treats capability pressure as read-only
  visibility context, not acquisition or policy guidance.

Evidence against treating capabilities as domains:

- Capability needs have subjects, diagnostics, needed evidence, and diagnostic
  runs, not domain classification or permission state.
- Capability relationship output is keyed by capability, not observation domain.

Best category name for understanding: **capability pressure feeding coverage/gap
classification**.

## Observation-domain entries reviewed

### Entries in `observation_domains.py`

| Entry pattern | Source of identity | What is classified? | What is observed? | What grants it? | What constrains it? |
| --- | --- | --- | --- | --- | --- |
| `local_listeners` | `CAPABILITY_TO_DOMAIN`, listener families/predicates | coverage/gap status | listener observations and missing listener ownership/process evidence | nothing; no permission check | inventory evidence and capability pressure |
| `container_runtime` | `CAPABILITY_TO_DOMAIN`, container families/predicates | coverage/gap status | container-runtime facts or their absence | nothing; no permission check | missing observation family and capability pressure |
| `<family>_observations` | observation inventory family prefix | observed coverage label | predicates in that family | nothing; no permission check | presence of provider predicates |
| filtered unknown string | CLI/user filter | unknown coverage/gap state | nothing known | nothing | insufficient repository evidence |

### Entries in `observation_permission.py`

| Entry | Source of identity | What is authorized? | What is observed? | What grants it? | What constrains it? |
| --- | --- | --- | --- | --- | --- |
| `neighbor_table_read` | `SUPPORTED_OBSERVATION_CLASSES` | local passive neighbor-table read activity | likely neighbor/network-adjacent information, but no target mapping is encoded | matching `Approval` action/constraint | approval scope/expiry/constraints, otherwise operator expression |
| `traffic_capture` | `SUPPORTED_OBSERVATION_CLASSES` | passive traffic capture activity | network traffic | matching `Approval` action/constraint | approval scope/expiry/constraints, otherwise operator expression |
| `active_network_probe` | `SUPPORTED_OBSERVATION_CLASSES` | active network probing activity | network targets reached by probe | matching `Approval` action/constraint | approval scope/expiry/constraints, otherwise operator expression |
| `docker_socket_read` | `SUPPORTED_OBSERVATION_CLASSES` | privileged Docker socket read access/activity | container runtime through Docker socket, by inference from name | matching `Approval` action/constraint | approval scope/expiry/constraints, otherwise operator expression |
| `external_provider_query` | `SUPPORTED_OBSERVATION_CLASSES` | external provider query activity | external-source data | matching `Approval` action/constraint | approval scope/expiry/constraints, otherwise operator expression |
| filtered unknown string | CLI/user filter | unknown activity | unknown | none recognized | unknown implementation evidence |

The `docker_socket_read` row intentionally says "by inference from name" for
container runtime because current code does not encode a target map from
`docker_socket_read` to `container_runtime`.

## Comparison to existing repository concepts

### Capabilities

Permission-domain entries resemble capabilities in that both can describe a
thing an operator or runtime might need in order to observe more. However,
capability surfaces currently preserve pressure, access context, benefit,
attainability, and expectation, while permission domains preserve class,
approval evidence, permission state, and future invocation state.

Visibility domains are downstream of some capability names: capability pressure
is mapped into coverage/gap domains. That makes visibility domains closer to a
coverage view over capability gaps than to capabilities themselves.

### Relationships

Relationships are catalog-backed and preserve subject/object/predicate meaning.
No implementation evidence shows observation domains as relationship kinds,
relationship subjects, or relationship objects. Observation-domain entries are
report rows, not graph relationship definitions.

### References and selection objects

Selection objects choose among candidates or explain why an operational
conclusion/reference was selected. Observation domains do not currently select
objects. A filtered domain argument chooses one report row to render, but that is
CLI filtering rather than repository selection semantics.

### Projection stages

Projection stages describe how event/fact state is built or passed into read
models. Visibility domains use projected state and inventory evidence, and
permission domains inspect approvals in state, but neither vocabulary is itself
implemented as a projection stage.

### Observation families and predicate families

Visibility domains strongly resemble observation families because many domain
names are generated directly from family names. Permission domains do not: they
resemble activity/access mechanism names more closely than predicate families.

### Predicate families

`<family>_observations` domains are closest to predicate-family labels. They are
not the same as predicates because they group multiple predicates and add a
coverage classification.

## Acceptance answers

### What object is actually being authorized?

In current implementation evidence, `observation_permission.py` authorizes—or
more precisely reports permission visibility for—a named observation activity or
access mechanism. The authorization key is the domain string in
`SUPPORTED_OBSERVATION_CLASSES`, matched against approval action strings like
`observation.<domain>` or approval constraints with `observation_domain`.

### What object is actually being observed?

In `observation_domains.py`, the observed object is a coverage area derived from
families, predicates, and capability pressure. Examples include local listener
coverage, container-runtime coverage, and generated family coverage such as
filesystem or DNS observations.

In `observation_permission.py`, the observed target is not generally encoded as
a separate object. Some names imply targets (`docker_socket_read` implies Docker
socket/container-runtime access; `traffic_capture` implies traffic), but current
code does not preserve target identity separately from the activity/access name.

### What object is actually being classified?

Two different objects are classified:

- `observation_domains.py` classifies coverage/gap domains with values such as
  `observed`, `partially_observed`, `unobserved`, and `unknown`.
- `observation_permission.py` classifies permission-domain activities with
  observation classes such as `local_passive`, `network_passive`,
  `network_active`, `local_privileged`, `external`, and `unknown`.

These classifications are not interchangeable.

### What object is actually being granted permission?

The object granted permission is the permission-domain activity/access mechanism,
not the visibility coverage domain. A reusable approval grants a string such as
`observation.neighbor_table_read` or carries a constraint
`observation_domain=neighbor_table_read`. No current evidence shows an approval
granted to `container_runtime` or `filesystem_observations` by this mechanism.

### Are current observation-domain vocabularies describing the same thing?

No. Current evidence supports overlap, not sameness. They describe different
objects participating in observation workflows:

- visibility/coverage domains describe where evidence exists or is missing;
- permission/access domains describe what activity/access would require operator
  expression or reusable approval.

`container_runtime` and `docker_socket_read` are the clearest example. The first
is currently a coverage/gap area; the second is currently a privileged local
access mechanism. They may participate in the same workflow, but repository
authority does not identify them as the same object.

## Supported conclusions

1. Current observation-domain vocabularies are fragmented by implementation
   source and conceptual role.
2. `observation_domains.py` entries are best understood as read-only
   coverage/gap visibility areas.
3. `observation_permission.py` entries are best understood as read-only
   permission visibility over observation activities or access mechanisms.
4. Family-derived visibility domains are closest to observation/predicate
   families, not to permission domains.
5. Capability-derived visibility domains are coverage labels informed by
   capability pressure, not capabilities themselves.
6. Permission domains resemble mechanisms/activities/capabilities more than they
   resemble coverage areas, but they are not capability records because their
   core fields are permission/class/approval-oriented.
7. Existing code does not preserve a separate model for observation target,
   observation mechanism, observation source, observation grant, and observation
   boundary. Some of those roles are currently collapsed into the overloaded
   word `domain`.

## Unsupported conclusions

Current repository evidence does not support concluding that:

- all observation-domain strings name one coherent object type;
- permission domains inherit from visibility domains;
- visibility domains inherit from permission domains;
- `docker_socket_read` is canonically the same object as `container_runtime`;
- `neighbor_table_read`, `traffic_capture`, or `active_network_probe` are
  canonically mapped to generated network, endpoint, DNS, or address visibility
  domains;
- observation classes are sufficient to reason about observation-domain
  coverage;
- visibility-domain classification is sufficient to reason about permission;
- a catalog, registry, inheritance model, propagation model, authority model, or
  ontology should be introduced by this investigation.

## Open questions

1. Should future code reserve `domain` for coverage boundaries, permission
   activities, or neither without a qualifier?
2. If `docker_socket_read` enables `container_runtime` observation, should that
   be represented as a mechanism-to-target relationship, or remain only an
   investigation inference?
3. Should family-derived names such as `filesystem_observations` remain
   generated visibility labels rather than durable domain identities?
4. Should approval constraints named `observation_domain` be understood only as
   permission-domain constraints, or can they ever target visibility domains?
5. What evidence would be required to say that an observation activity, an
   access mechanism, and an observation target are parts of one explicit
   workflow?
6. Should future diagnostic wording distinguish `coverage domain`, `permission
   domain`, `observation activity`, `access mechanism`, and `observation target`
   before any first-class catalog work is considered?
