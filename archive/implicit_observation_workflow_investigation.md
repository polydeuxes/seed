# Implicit Observation Workflow Investigation

## Scope

This investigation asks how observation moves from acquisition opportunity to
repository visibility in the repository today. It is documentation-only. It does
not create workflow engines, relationship catalogs, ontologies, registries,
runtime behavior, permission systems, authority systems, acquisition logic, or
new operational surfaces.

Repository authority wins. Conclusions below are limited to implementation-backed
evidence and existing investigation documents already present in the repository.

## Evidence reviewed

Primary implementation files reviewed:

```bash
sed -n '1,220p' seed_runtime/observation_domains.py
sed -n '1,220p' seed_runtime/observation_permission.py
sed -n '1,240p' seed_runtime/observation_inventory.py
sed -n '1,240p' seed_runtime/observation_utilization.py
sed -n '1,220p' seed_runtime/capability_needs.py
sed -n '1,220p' seed_runtime/capability_relationship.py
sed -n '1,260p' seed_runtime/operational_story.py
sed -n '1,260p' seed_runtime/ownership_discrepancies.py
sed -n '1,260p' seed_runtime/privilege_discovery.py
```

Prior observation-domain and permission investigations reviewed:

```bash
sed -n '1,220p' docs/observation_domain_conceptual_object_investigation.md
sed -n '1,180p' docs/observation_domain_permission_authority_reuse_investigation.md
sed -n '1,180p' docs/observation_domain_vocabulary_fragmentation_investigation.md
```

Repository pattern comparison used targeted search rather than treating every
match as equal authority:

```bash
rg -n "reference selection|capability relationship|projection shape|structural membership|diagnostic reasoning|investigation_path|shape|membership|diagnostic_capability_need|first_loss|CAPABILITY_TO_DOMAIN|SUPPORTED_OBSERVATION_CLASSES" seed_runtime docs tests -S
```

## Short answer

The repository already contains a **partial implicit observation workflow**, but
not a first-class workflow model.

The implementation-backed path is strongest in this direction:

```text
projected facts / diagnostic findings
    -> ownership discrepancy or similar diagnostic gap
    -> capability pressure / needed evidence
    -> access or privilege context
    -> coverage/gap classification
    -> utilization/visibility loss classification
```

A second, weaker path exists around acquisition opportunities:

```text
named observation access mechanism or activity
    -> permission class and approval lookup
    -> reusable/future authorization visibility
```

The repository does **not** currently join that second path to coverage outcomes
with implementation-backed relationships. For example, current authority supports
this distinction:

```text
container_runtime = coverage/gap area
docker_socket_read = local privileged observation access mechanism/activity
```

The implementation does not prove this relationship today:

```text
docker_socket_read enables container_runtime visibility
```

That relationship is plausible as an interpretation, but it is not an implemented
mapping in the reviewed code.

## Observation-related object types discovered

### 1. Observation targets / coverage areas

Observation targets appear as coverage or gap areas in
`seed_runtime/observation_domains.py`. The report object is
`ObservationDomainEntry`, with `domain`, `classification`, `gap_type`,
`pressure`, and `evidence` fields.

Implementation-backed examples:

| Target / coverage area | How it appears today | Evidence-backed meaning |
| --- | --- | --- |
| `local_listeners` | Constructed when listener evidence or mapped capability pressure exists. | Listener coverage area that may be observed or partially observed. |
| `container_runtime` | Constructed when container predicates exist or container capability pressure exists. | Container-runtime coverage/gap area. |
| `<family>_observations` | Generated from observation-inventory families other than listener/listening/container. | Predicate-family-derived observed coverage labels. |

These are targets or outcomes, not access mechanisms. They are classified as
`observed`, `partially_observed`, `unobserved`, or `unknown`, with gap types such
as `missing_evidence_inside_observed_domain` or `missing_observation_domain`.

### 2. Observation mechanisms / permission activities

Observation mechanisms appear in `seed_runtime/observation_permission.py` as the
keys of `SUPPORTED_OBSERVATION_CLASSES`.

Implementation-backed examples:

| Mechanism/activity | Observation class | Evidence-backed meaning |
| --- | --- | --- |
| `neighbor_table_read` | `local_passive` | Local passive read activity. |
| `traffic_capture` | `network_passive` | Passive network observation activity. |
| `active_network_probe` | `network_active` | Active network observation activity. |
| `docker_socket_read` | `local_privileged` | Local privileged access mechanism/activity. |
| `external_provider_query` | `external` | External provider query activity. |

The permission implementation checks reusable authority by looking for approvals
whose action is `observation.<domain>` or whose constraints include the same
`observation_domain`. It does not collect observations, enforce permissions,
store approvals, or invoke anything autonomously.

### 3. Observation activities / providers

Observation activities are implementation-discovered provider classes in
`seed_runtime/observation_inventory.py`. The inventory finds Python classes under
`seed_runtime/` that implement `collect()` and look like observation sources,
then extracts predicates from `Observation(predicate=...)` calls or provider
`_observation(..., predicate, ...)` calls.

This object type answers:

```text
what provider can collect which predicates?
```

It does not directly answer:

```text
which permission mechanism authorizes that provider?
which coverage area will be improved by that provider?
```

Families are derived from predicate prefixes before the first underscore. Those
families later feed coverage/gap labels in `observation_domains.py`.

### 4. Capability pressure inputs

Capability pressure appears in `seed_runtime/capability_needs.py`, usually from
ownership discrepancy diagnostics or recorded diagnostic facts. A
`CapabilityNeedEntry` contains a capability name, affected subjects, diagnostics,
needed evidence, and diagnostic runs.

Implementation-backed examples from ownership discrepancy conflicts include:

| Diagnostic conflict area | Needed evidence / capability pressure examples |
| --- | --- |
| Service `insufficient_evidence` | `tcp_listen_inventory`, `process_inventory`, `container_inventory` |
| Service `owner_not_observed` | `listener_process_inventory`, `container_port_mapping`, `container_inventory` |
| Storage `missing_owner` | `mount_source_inventory`, `export_visibility_inventory` |
| Storage `remote_export_attribution_missing` | `nfs_export_inventory`, `smb_share_inventory`, `remote_storage_export_inventory` |

`seed_runtime/observation_domains.py` only maps a subset of capability pressure
to coverage domains:

| Capability pressure | Coverage/gap area |
| --- | --- |
| `listener_process_inventory` | `local_listeners` |
| `container_inventory` | `container_runtime` |
| `container_port_mapping` | `container_runtime` |

This is one of the clearest implementation-backed workflow-like connections.

### 5. Coverage/gap outputs

Coverage and gap outputs are produced by `build_observation_domains()` and by
`build_observation_utilization_audit()`.

`observation_domains` answers:

```text
which coverage areas are observed, partially observed, unobserved, or unknown?
which capability pressures explain that classification?
```

`observation_utilization` answers:

```text
which collected predicates are projected, readable in read models, diagnostic-consumed,
or first lost at unused/projection/read-model/diagnostic stages?
```

Together, these expose both domain-level coverage and predicate-level visibility
loss. They are related by inventory predicates and families, but there is no
single workflow row that directly joins mechanism, provider, predicate, coverage
area, diagnostic use, and authority state.

### 6. Authority boundaries

Authority boundaries are explicit and repeated across the reviewed surfaces:

| Surface | Boundary evidence |
| --- | --- |
| `observation_domains` | Read-only, no event-ledger writes, no cluster mutation. |
| `observation_permission` | Read-only visibility; no recording, permission enforcement, approval storage, or runtime autonomy. |
| `capability_relationship` | Read-only; no recording, event-ledger writes, cluster mutation, acquisition, policy, or planning. |
| `privilege_discovery` | Visibility only; no sudo, privilege escalation, event-ledger writes, or cluster mutation. |
| `operational_story` | Read-only view; no recording, event-ledger writes, cluster mutation, plans, or implementation advice. |

This means the current observation workflow is a **visibility workflow**, not an
acquisition or execution workflow.

## Workflow-like relationships discovered

### Supported relationship A: diagnostic gap to capability pressure

Implementation-backed chain:

```text
projected facts
    -> ownership discrepancy row
    -> diagnostic_capability_need record shape
    -> CapabilityNeedEntry
```

Evidence:

- `build_ownership_discrepancies()` classifies storage and service subjects from
  existing facts.
- `_CAPABILITY_NEEDS_BY_CONFLICT` maps specific ownership conflicts to needed
  evidence, candidate capability, and privilege level.
- `diagnostic_capability_need_records()` emits diagnostic-only capability need
  dictionaries for rows with mapped conflicts.
- `build_capability_needs()` reads both current discrepancy-derived records and
  recorded diagnostic facts scoped under `diagnostic_run:` subjects.

Workflow interpretation supported:

```text
missing or ambiguous evidence creates capability pressure
```

Unsupported extension:

```text
capability pressure automatically triggers acquisition
```

The code explicitly stays read-only and does not invoke capabilities.

### Supported relationship B: capability pressure to coverage/gap area

Implementation-backed chain:

```text
CapabilityNeedEntry
    -> CAPABILITY_TO_DOMAIN
    -> ObservationDomainEntry.pressure
    -> ObservationDomainEntry.classification / gap_type / evidence
```

Evidence:

- `CAPABILITY_TO_DOMAIN` maps `listener_process_inventory` to
  `local_listeners` and maps `container_inventory` plus
  `container_port_mapping` to `container_runtime`.
- `build_observation_domains()` seeds pressure from that map and adds pressure
  found in current capability needs.
- Container pressure without container observation family can produce an
  `unobserved` `container_runtime` domain with `missing_observation_domain`.
- Listener evidence plus listener process pressure can produce a
  `partially_observed` `local_listeners` domain with
  `missing_evidence_inside_observed_domain`.

Workflow interpretation supported:

```text
capability pressure contributes to coverage/gap classification
```

Unsupported extension:

```text
all capabilities map to observation coverage domains
```

Only the three capabilities in `CAPABILITY_TO_DOMAIN` are mapped by current
implementation.

### Supported relationship C: provider predicates to families to coverage labels

Implementation-backed chain:

```text
ObservationSource.collect() provider classes
    -> predicate literals
    -> predicate families
    -> generated <family>_observations domains
```

Evidence:

- `build_observation_inventory()` discovers providers via AST inspection of
  classes implementing `collect()`.
- It extracts predicate string literals.
- `_families()` derives families from predicate prefixes.
- `build_observation_domains()` turns most families into `<family>_observations`
  entries marked `observed`.

Workflow interpretation supported:

```text
implemented collection surfaces create observed coverage labels
```

Unsupported extension:

```text
every generated family label is a curated domain concept
```

Family identity is prefix-derived, not catalog-defined.

### Supported relationship D: collected predicate to visibility loss

Implementation-backed chain:

```text
inventory predicate
    -> projected source scan
    -> read-model source scan
    -> diagnostic source scan
    -> first_loss classification
```

Evidence:

- `build_observation_utilization_audit()` starts from observation inventory
  predicates.
- It scans configured projected, read-model, and diagnostic source files for the
  predicate string.
- It classifies first loss as `unused`, `projection_loss`, `read_model_loss`,
  `diagnostic_loss`, or `none`.

Workflow interpretation supported:

```text
observation can be collected yet lost before operational visibility
```

Unsupported extension:

```text
first_loss proves runtime data actually flowed through those stages
```

The audit is static source evidence, not a runtime trace.

### Supported relationship E: capability pressure to access/privilege context

Implementation-backed chain:

```text
CapabilityNeedEntry
    -> _guidance_for(capability)
    -> PrivilegeDiscoveryCapability or CapabilityRelationship
```

Evidence:

- `privilege_discovery` and `capability_relationship` both iterate
  `build_capability_needs(state)`.
- Both call `_guidance_for()` for access level, operational benefit, suggested
  next step, and notes.
- `capability_relationship` explicitly states that pressure is visibility
  context, not acquisition guidance.

Workflow interpretation supported:

```text
missing capability pressure can be explained in access/benefit terms
```

Unsupported extension:

```text
access guidance is permission to collect or escalate
```

The guidance surfaces are visibility-only and non-mutating.

### Supported relationship F: permission activity to reusable authority state

Implementation-backed chain:

```text
permission-domain string
    -> observation class
    -> approval lookup
    -> permission_state / reusable_permission / future_autonomous_invocation
```

Evidence:

- `SUPPORTED_OBSERVATION_CLASSES` enumerates recognized activity/access names.
- `_approval_for_domain()` checks `Approval.action == "observation.<domain>"` or
  `Approval.constraints["observation_domain"] == domain`.
- `_domain_entry()` reports `granted` when reusable approval exists; otherwise it
  reports `requires_operator_expression` for recognized domains.

Workflow interpretation supported:

```text
access opportunities have explicit authority visibility
```

Unsupported extension:

```text
approved activity is joined to a provider, predicate family, or coverage outcome
```

No reviewed implementation maps `docker_socket_read` to `container_inventory`,
`container_port_mapping`, or `container_runtime`.

### Supported relationship G: operational story composes pressure, capability, constraints, gaps, and path

Implementation-backed chain:

```text
pressure audit + capability needs + privilege discovery + correlation audit + impact audit + investigation path
    -> OperationalStory
```

Evidence:

- `build_operational_story()` composes current pressure, capability needs,
  privilege discovery constraints, correlation gaps, impact, observed outcomes,
  and an investigation path.
- The story object is explicitly a read-only view and does not record facts,
  write the event ledger, or mutate the cluster.

Workflow interpretation supported:

```text
repository visibility can be narrated as an operational story assembled from existing diagnostic surfaces
```

Unsupported extension:

```text
operational story drives observation-domain construction today
```

`observation_domains.py` assigns `story = build_operational_story(state)`, but
this investigation found no subsequent use of `story` in domain construction.

## How observation moves from opportunity/access to visibility today

The most accurate implementation-backed description is not one linear workflow.
It is a set of partially connected chains:

```text
Chain 1: permission/access visibility

observation activity/access name
    -> observation class
    -> approval lookup
    -> permission state and future invocation boundary
```

```text
Chain 2: implementation inventory visibility

provider class with collect()
    -> predicate literals
    -> predicate families
    -> observed family-derived coverage labels
```

```text
Chain 3: diagnostic pressure visibility

projected facts
    -> ownership discrepancy / diagnostic conflict
    -> needed evidence and candidate capability
    -> capability pressure
    -> coverage/gap area classification
```

```text
Chain 4: predicate utilization visibility

collected predicate
    -> projection/read-model/diagnostic source checks
    -> first visible loss stage
```

```text
Chain 5: access-context explanation

capability pressure
    -> current access / operational benefit / notes
    -> visibility-only privilege or capability relationship explanation
```

Current implementation-backed movement from acquisition opportunity to visibility
is therefore **split**:

- Access opportunity is visible through `observation_permission` and
  `privilege_discovery`.
- Collection implementation is visible through `observation_inventory`.
- Visibility outcome is visible through `observation_domains` and
  `observation_utilization`.
- Diagnostic pressure connects gaps to capabilities through
  `ownership_discrepancies` and `capability_needs`.
- The explicit joins between permission activities and coverage outcomes are not
  implemented.

## Comparison with other visible chain patterns

### Reference selection

Reference-selection surfaces preserve a chain from candidate references to a
selected comparison context. Observation has a comparable chain only for some
segments: provider-to-predicate inventory and diagnostic-gap-to-capability
pressure. It lacks a selection-like implementation that chooses an observation
mechanism for a coverage target.

### Capability relationship

Observation most closely resembles capability relationship today.
`capability_relationship` already exposes capability, current access,
operational benefit, pressure, attainability, expectation, reasoning, and
known limitations without acquiring anything. Observation-domain visibility uses
capability pressure similarly: pressure explains what is missing, while boundary
language prevents turning that pressure into action.

### Projection shape

Projection-shape-style chain visibility is present in `observation_utilization`:
collected predicates are checked against projection, read-model, and diagnostic
consumption evidence, yielding a first-loss stage. Unlike projection shape,
observation does not have a declared end-to-end stage model from mechanism to
coverage outcome.

### Structural membership

Structural membership patterns rely on explicit relationships such as membership
or containment. Observation does not currently have explicit membership facts
like:

```text
docker_socket_read member_of container_runtime workflow
container_inventory contributes_to container_runtime coverage
```

The closest implementation-backed membership-like relation is the local
`CAPABILITY_TO_DOMAIN` map.

### Diagnostic reasoning

Observation strongly matches diagnostic reasoning patterns. Ownership
discrepancies reason from facts to conflict classes, conflict classes imply
needed evidence/candidate capabilities, and capability needs feed later read-only
surfaces. This is the strongest current workflow-like structure.

## Evidence supporting workflow interpretation

Supported evidence:

1. The repository contains explicit maps from diagnostic conflicts to needed
   evidence and candidate capabilities.
2. The repository contains an explicit map from selected capabilities to
   coverage/gap domains.
3. The repository statically discovers providers, predicates, and predicate
   families.
4. The repository classifies collected predicates by visibility stage and first
   loss.
5. The repository exposes access/privilege/permission boundaries as read-only
   visibility surfaces.
6. Operational story composes pressure, capability, access constraints,
   correlation gaps, impact, outcomes, and investigation path into one narrative
   view.

These are enough to say a partial implicit workflow exists.

## Evidence against workflow interpretation

Limiting evidence:

1. No reviewed file defines a first-class observation workflow object.
2. No reviewed file maps permission activities such as `docker_socket_read` to
   providers, predicates, capabilities, or coverage areas.
3. No reviewed file maps access mechanisms directly to visibility outcomes.
4. `observation_domains.py` builds an operational story but does not use it in
   domain construction.
5. `observation_inventory.py` discovers provider/predicate shape, not authority
   or outcomes.
6. `observation_utilization.py` uses static source scans, not runtime traces.
7. Capability pressure is explicitly visibility context, not acquisition
   guidance.
8. Permission surfaces explicitly avoid enforcement, approval creation, and
   runtime autonomy.

These prevent claiming a complete observation workflow exists.

## Supported chains

### Chain: service owner ambiguity to listener/container coverage pressure

```text
service ownership evidence
    -> ownership discrepancy conflict: owner_not_observed
    -> needed evidence: listener_process_inventory / container_port_mapping / container_inventory
    -> capability pressure
    -> local_listeners or container_runtime coverage/gap area
```

Implementation-backed relationship status:

- `owner_not_observed` to capability needs: implemented.
- selected capability needs to domains: implemented for three mapped
  capabilities.
- resulting coverage classification: implemented.
- automatic acquisition: not implemented.

### Chain: storage owner gap to capability pressure

```text
storage evidence
    -> ownership discrepancy conflict: missing_owner or remote_export_attribution_missing
    -> needed evidence: mount/export/share inventory capabilities
    -> capability pressure
```

Implementation-backed relationship status:

- conflict to capability needs: implemented.
- mapping from those storage capabilities to observation coverage domains:
  not implemented in `CAPABILITY_TO_DOMAIN`.

### Chain: provider implementation to observed family coverage

```text
ObservationSource implementation
    -> predicate strings
    -> family prefix
    -> <family>_observations coverage entry
```

Implementation-backed relationship status:

- provider discovery: implemented.
- predicate extraction: implemented.
- family derivation: implemented.
- coverage entry generation: implemented for most families.
- curated domain semantics: not implemented.

### Chain: predicate visibility to first loss

```text
collected predicate
    -> projected/read-model/diagnostic evidence scan
    -> first_loss
```

Implementation-backed relationship status:

- static source scan: implemented.
- runtime flow proof: not implemented.

### Chain: observation permission activity to authorization state

```text
neighbor_table_read / traffic_capture / active_network_probe / docker_socket_read / external_provider_query
    -> observation class
    -> approval lookup
    -> permission state
```

Implementation-backed relationship status:

- activity classification: implemented.
- reusable approval lookup: implemented.
- enforcement/acquisition/provider mapping: not implemented.

## Unsupported chains

The following chains are not supported by reviewed implementation evidence:

```text
docker_socket_read
    -> enables
container_runtime visibility
```

```text
neighbor_table_read
    -> contributes_to
network coverage
```

```text
listener_process_inventory
    -> reduces
local_listener ambiguity
```

The repository does support weaker, related statements:

```text
container_inventory / container_port_mapping pressure
    -> maps to
container_runtime coverage/gap area
```

```text
listener_process_inventory pressure
    -> maps to
local_listeners coverage/gap area
```

```text
owner_not_observed conflict
    -> may emit
listener_process_inventory / container_port_mapping / container_inventory capability needs
```

But it does not currently connect permission/access mechanisms to those outcomes.

## Supported conclusions

1. A partial implicit observation workflow exists.
2. The strongest chain is diagnostic gap → needed evidence/capability pressure →
   coverage/gap classification.
3. A separate authority chain exists for observation activities/access
   mechanisms → permission class → reusable approval state.
4. A separate implementation chain exists for provider class → predicates →
   predicate families → family-derived observed coverage labels.
5. A separate utilization chain exists for collected predicate → projection/read
   model/diagnostic consumption → first loss.
6. Observation is currently a visibility and diagnostic reasoning area, not an
   acquisition/execution workflow.
7. `container_runtime` and `docker_socket_read` are different conceptual object
   types today.

## Unsupported conclusions

1. The repository has a complete observation workflow model.
2. The repository has an implemented relationship catalog joining mechanisms,
   activities, capabilities, providers, predicates, and coverage outcomes.
3. The repository proves that `docker_socket_read` enables `container_runtime`
   visibility.
4. The repository proves that `neighbor_table_read` contributes to network
   coverage.
5. The repository proves that any permission-domain approval authorizes a
   concrete provider or collection behavior.
6. The repository treats all observation-domain vocabulary as one coherent
   ontology.
7. The repository should add workflow engines, catalogs, ontologies, registries,
   authority systems, permission systems, or runtime behavior based on this
   investigation alone.

## Open questions

These are unanswered by current implementation evidence:

1. Which, if any, permission activities correspond to concrete observation
   providers?
2. Which providers, if any, are intended to satisfy specific capability needs?
3. Which capability needs beyond `listener_process_inventory`,
   `container_inventory`, and `container_port_mapping` should map to coverage
   areas, if any?
4. Is `observation_domains.py` intended to use `build_operational_story(state)`,
   or is that dependency only a shape-audit/source marker today?
5. Should predicate-family-derived `<family>_observations` be treated as durable
   coverage concepts, or only as inventory-derived visibility labels?
6. Does runtime observation recording preserve enough provenance to join
   provider, predicate, support, diagnostic consumption, and coverage outcome?
7. Are approval constraints intended to remain reusable permission evidence only,
   or eventually to bind to specific providers/actions?

## Final answer to the core question

Observation moves from opportunity or access to repository visibility today by
multiple partial, implementation-backed paths rather than one explicit workflow:

```text
Access path:
observation access/activity name
    -> permission class
    -> approval lookup
    -> authorization visibility
```

```text
Collection path:
provider implementation
    -> predicate inventory
    -> predicate family
    -> observed coverage label
```

```text
Diagnostic pressure path:
projected facts
    -> diagnostic conflict / missing evidence
    -> capability pressure
    -> mapped coverage/gap area
```

```text
Utilization path:
collected predicate
    -> projection/read-model/diagnostic source evidence
    -> first-loss visibility outcome
```

Only selected joins are implementation-backed. The repository currently supports
understanding observation as a set of implicit visibility chains, not as a
created or complete observation workflow system.
