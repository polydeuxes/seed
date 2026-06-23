# Observation-Domain Vocabulary Fragmentation Investigation

## Scope

This investigation asks how observation domains are represented across the
repository today. It does not propose or implement catalogs, registries, APIs,
visibility surfaces, inheritance, policy, permission behavior, or runtime
behavior.

Repository authority wins: every conclusion below is limited to implementation
and existing documentation evidence found in this repository.

## Commands and evidence reviewed

Implementation-backed checks used during this investigation:

```bash
rg -n "observation_domain|observation domains|observation-domain|observation_permission|capability pressure|operational story|capability relationship" -S .
sed -n '1,260p' seed_runtime/observation_domains.py
sed -n '1,280p' seed_runtime/observation_permission.py
sed -n '1,260p' seed_runtime/observation_inventory.py
sed -n '1,220p' seed_runtime/observation_utilization.py
sed -n '1,160p' seed_runtime/capability_needs.py
sed -n '1,130p' seed_runtime/capability_relationship.py
sed -n '330,405p' seed_runtime/diagnostic_inventory.py
sed -n '330,382p' seed_runtime/diagnostic_shape_audit.py
sed -n '1,180p' seed_runtime/entity_type_catalog.py
sed -n '1,130p' seed_runtime/predicate_catalog.py
sed -n '1,130p' seed_runtime/relationship_catalog.py
sed -n '1288,1308p' scripts/seed_local.py
sed -n '6320,6352p' scripts/seed_local.py
python scripts/seed_local.py --observation-domains --json
python scripts/seed_local.py --observation-permission --json
```

## Short answer

The repository does not currently have one coherent, first-class
observation-domain concept with cross-surface identity.

Current implementation evidence shows at least two observation-domain
vocabularies:

1. **Observation-domain visibility domains** in
   `seed_runtime/observation_domains.py`, derived from observation inventory
   families, predicate utilization, capability pressure, and operational-story
   evidence.
2. **Observation-permission domains** in
   `seed_runtime/observation_permission.py`, explicitly enumerated in
   `SUPPORTED_OBSERVATION_CLASSES` and used to produce permission visibility.

These vocabularies overlap conceptually because both are called observation
`domain` and both describe boundaries around observation activity, but their
identities come from different mechanisms, are consumed by different surfaces,
and are not joined by a shared source of truth.

## Vocabulary 1: observation-domain visibility domains

### Definition source

`ObservationDomainEntry` defines a report entry with these fields:

- `domain`
- `classification`
- `gap_type`
- `pressure`
- `evidence`

This is a diagnostic output shape, not a catalog definition object.

### Identity derivation

Domain identity in `observation_domains.py` is derived rather than cataloged.
The implementation creates domains from three mechanisms:

1. A hard-coded capability-to-domain map:

   | Capability | Derived domain |
   | --- | --- |
   | `listener_process_inventory` | `local_listeners` |
   | `container_inventory` | `container_runtime` |
   | `container_port_mapping` | `container_runtime` |

2. Observation inventory families and predicates. Listener predicates can create
   `local_listeners`; container predicates can create `container_runtime`; all
   other observed families become generated names of the form
   `<family>_observations`.

3. Capability pressure from `build_capability_needs(state)`. Capability pressure
   can cause a domain to appear even when no observation family is observed. The
   current `container_runtime` behavior is the clearest example: capability
   pressure can produce an `unobserved` domain with
   `missing_observation_domain`.

The module also builds an operational story, but current implementation evidence
only shows `story = build_operational_story(state)` being assigned; no later code
uses that value in domain construction. Therefore, operational story is a
registered source marker and dependency candidate for shape-audit purposes, but
this investigation did not find current domain identity derived from the story
value itself.

### Current exposed examples

`python scripts/seed_local.py --observation-domains --json` exposes domains such
as:

- `address_observations`
- `architecture_observations`
- `block_observations`
- `boot_observations`
- `container_runtime`
- `cpu_observations`
- `default_observations`
- `disk_observations`
- `dns_observations`
- `endpoint_observations`
- `filesystem_observations`
- `fqdn_observations`

The complete set is runtime-derived from currently discoverable provider
predicates and capability pressure, not from a stable domain catalog.

### Consumers and exposure

`observation_domains` is consumed by the CLI through `--observation-domains` and
can render human-readable or JSON output. It is registered in diagnostic
inventory as a read-only diagnostic that uses projected state, repository files,
JSON output, and diagnostic facts. The diagnostic shape-audit spec names
`build_observation_domains`, `format_observation_domains`, and
`observation_domains_json`, and lists inventory/utilization/operational-story
markers plus capability-needs diagnostic-fact reads.

## Vocabulary 2: observation-permission domains

### Definition source

`ObservationPermissionDomain` defines a permission report entry with these
fields:

- `domain`
- `observation_class`
- `permission_state`
- `authority_evidence`
- `reasoning`
- `known_limitations`
- `reusable_permission`
- `future_autonomous_invocation`

The domain vocabulary is the key set of `SUPPORTED_OBSERVATION_CLASSES`:

| Permission domain | Observation class |
| --- | --- |
| `neighbor_table_read` | `local_passive` |
| `traffic_capture` | `network_passive` |
| `active_network_probe` | `network_active` |
| `docker_socket_read` | `local_privileged` |
| `external_provider_query` | `external` |

### Identity derivation

Domain identity here is explicit and local to `observation_permission.py`.
`build_observation_permission` lists the sorted keys of
`SUPPORTED_OBSERVATION_CLASSES` when no filter is passed. If a filter is passed,
the requested string becomes the domain under analysis, and any string absent
from the map is treated as an unknown domain.

Permission-domain identity is also used to search state approvals by either
`approval.action == f"observation.{domain}"` or
`approval.constraints["observation_domain"] == domain`.

### Current exposed examples

`python scripts/seed_local.py --observation-permission --json` exposes exactly
these recognized domains when unfiltered:

- `active_network_probe`
- `docker_socket_read`
- `external_provider_query`
- `neighbor_table_read`
- `traffic_capture`

Each receives a class, permission state, reasoning, limitations, reusable
permission state, and future autonomous invocation state.

### Consumers and exposure

`observation_permission` is consumed by the CLI through `--observation-permission`
and can render human-readable or JSON output. It is registered in diagnostic
inventory as read-only permission visibility with no recording, no event-ledger
writes, no cluster mutation, no enforcement, no approval storage, and no runtime
autonomy. Its shape-audit spec points to `seed_runtime/observation_permission.py`
and checks that the implementation does not use mutation or ingestion markers.

## Other related vocabularies and derivation inputs

### Observation inventory families

`observation_inventory` discovers providers and predicates by AST inspection of
observation-producing classes. It derives families from predicate prefixes before
the first underscore. These families are not called domains in the inventory
model, but `observation_domains.py` promotes most families into domain names via
`<family>_observations`.

This means a third vocabulary participates indirectly: predicate-family names
such as `address`, `architecture`, `block`, `boot`, `cpu`, and `filesystem` can
be transformed into observation-domain visibility names.

### Observation utilization predicates

`observation_utilization` audits predicate participation after collection. It
tracks predicate-level fields such as `projected`, `read_model`,
`diagnostic_consumed`, and `first_loss`. It does not define domains, but
`observation_domains.py` consults diagnostic-consumed predicates to add evidence
for the `local_listeners` domain.

### Capability pressure

`capability_needs` defines capability names such as
`listener_process_inventory`, `container_port_mapping`, and
`container_inventory`. These are not observation domains, but
`observation_domains.py` maps them into visibility domains through
`CAPABILITY_TO_DOMAIN`.

`capability_relationship` consumes capability needs to explain access, benefit,
pressure, attainability, expectation, reasoning, and limitations. It does not
consume observation domains directly. It preserves an important boundary:
capability pressure is visibility context, not acquisition guidance.

### Operational story

`observation_domains.py` imports and calls `build_operational_story(state)`, and
the diagnostic shape spec lists `build_operational_story` as a repo-file marker.
However, the built `story` value is not consumed by later domain construction in
the current implementation. Existing documentation frequently discusses
observation-domain pressure in relation to operational story, but current code
does not make operational story a direct source of domain identity.

### Prior observation-domain investigations

The prior observation-class investigation already found that permission domains
and observation-domain visibility domains are different vocabularies and not
unified by a shared catalog. This investigation confirms that finding with the
current implementation and expands it to the wider question of domain identity,
consumers, exposure, and comparison to other repository vocabularies.

## Where observation domains are defined, derived, consumed, and exposed

| Surface | Defines domains? | Derives domains? | Consumes domains? | Exposes domains? | Notes |
| --- | --- | --- | --- | --- | --- |
| `seed_runtime/observation_domains.py` | Partially, as report entries and `CAPABILITY_TO_DOMAIN` values | Yes, from capability pressure, inventory families, and predicates | Yes, filter input and internal map keys | Yes, `--observation-domains` human/JSON | Most domain identities are derived, not cataloged. |
| `seed_runtime/observation_permission.py` | Yes, as keys of `SUPPORTED_OBSERVATION_CLASSES` | No, except unknown filtered strings become unknown entries | Yes, filter input and approval lookup | Yes, `--observation-permission` human/JSON | Explicit permission-domain vocabulary. |
| `seed_runtime/observation_inventory.py` | No domains | Derives families | No direct domain consumption | Exposes families/predicates | Families feed visibility domains indirectly. |
| `seed_runtime/observation_utilization.py` | No domains | No domains | No direct domain consumption | Exposes predicates/utilization | Predicate utilization adds evidence to visibility domains. |
| `seed_runtime/capability_needs.py` | No domains | No domains | No direct domain consumption | Exposes capabilities | Capability names are mapped into visibility domains. |
| `seed_runtime/capability_relationship.py` | No domains | No domains | No direct domain consumption | Exposes capabilities/pressure | Related to pressure, not domain identity. |
| `scripts/seed_local.py` | No domains | No domains | Consumes CLI domain filters | Exposes both domain surfaces | The same word `DOMAIN` appears for both flags. |
| Diagnostic inventory / shape audit | No domain vocabulary | No domains | Consumes diagnostic names/specs | Exposes/validates surfaces | Governs the two diagnostics, not domain identity. |

## Overlaps and conflicts

### Names do not overlap directly in current recognized sets

The current explicit permission domains are:

- `neighbor_table_read`
- `traffic_capture`
- `active_network_probe`
- `docker_socket_read`
- `external_provider_query`

The current visibility domains include names like:

- `local_listeners`
- `container_runtime`
- `<family>_observations`

No current implementation evidence shows a direct shared canonical name between
these two vocabularies.

### Conceptual overlap exists

Even though names differ, several entries appear to describe adjacent or
overlapping conceptual areas:

| Permission vocabulary | Visibility vocabulary | Relationship supported by evidence |
| --- | --- | --- |
| `docker_socket_read` | `container_runtime` | Both relate to container-runtime observation, but one is an access/permission domain and the other is coverage/gap visibility. No implementation-backed identity link was found. |
| `neighbor_table_read` | possibly network/address/endpoint/fqdn observation families | Both can relate to local passive network-adjacent observation, but no current map links neighbor-table permission to a visibility domain. |
| `traffic_capture` / `active_network_probe` | network/address/endpoint/fqdn-derived observation families | Both can relate to network observation activity, but the repository does not currently define a canonical relation between them. |
| `external_provider_query` | generated family observations or provider-derived inventory | Both can describe observation acquisition from non-local sources, but current inventory family derivation does not encode external-provider permission identity. |

These are conceptual overlaps, not implementation-backed equivalences.
Repository authority does not support saying that any pair above is the same
object today.

### Classification words are overloaded

`observation_domains.py` uses `classification` values such as `observed`,
`partially_observed`, and `unobserved`. `observation_permission.py` uses
`observation_class` values such as `local_passive`, `network_active`, and
`local_privileged`. These classify different things: coverage/gap state versus
permission/observation style. No current code bridges them.

### Unknown handling differs

In visibility domains, a filtered unknown domain returns an entry with unknown
classification, unknown gap type, and evidence saying repository evidence is
insufficient for the requested observation domain.

In permission domains, a filtered unknown domain receives `observation_class =
unknown`, `permission_state = unknown`, `reusable_permission = unknown`, and
reasoning that the domain is not recognized by implementation evidence.

Both surfaces support unknown domain strings, but unknown means different
surface-local things.

## Comparison with stronger repository concepts

Entity types, predicates, and relationships have explicit catalog structures:

- entity types load `EntityTypeDefinition` records and require unique names plus
  an `unknown` entry;
- predicates load `PredicateDefinition` records and provider-to-canonical
  mappings;
- relationships load `RelationshipDefinition` records, require unique names, and
  index definitions by derived predicates.

Observation domains do not currently have comparable characteristics:

| Characteristic | Entity types | Predicates | Relationships | Observation domains today |
| --- | --- | --- | --- | --- |
| Definition records | Yes | Yes | Yes | No shared record type; only diagnostic entry dataclasses. |
| Built-in catalog file | Yes | Yes | Yes | None found. |
| Canonical lookup API | Yes | Yes | Yes | No shared lookup across domain surfaces. |
| Provider/raw-to-canonical mapping | Not applicable | Yes | Derived from predicates | No map between permission domains, visibility domains, families, and capabilities. |
| Uniqueness validation | Yes | By dict construction and mapping validation | Yes | No global uniqueness validation. |
| Cross-surface identity | Stronger | Stronger | Stronger | Fragmented. |

Capabilities are closer to observation domains than catalogs are: capability
names are implementation-backed strings derived from diagnostics and surfaced by
capability-needs/relationship views. However, capabilities still have a clearer
cross-surface path than observation domains in this area: `capability_needs`
produces capability names, `capability_relationship` consumes the same names,
and `observation_domains.py` explicitly maps some capability names into domains.
No analogous shared path connects permission domains to visibility domains.

## Are permission domains the same conceptual objects as visibility domains?

Current evidence supports **overlap**, not sameness.

They are not the same implementation objects:

- permission domains are keys in `SUPPORTED_OBSERVATION_CLASSES`;
- visibility domains are entries derived from families, predicates, and
  capability pressure;
- the two modules do not import a shared domain definition source;
- neither module imports the other;
- no relationship catalog entry, predicate catalog entry, entity type, approval
  constraint normalization, or diagnostic-shape spec links the two vocabularies.

They are not fully independent either:

- both surfaces use the term observation domain;
- both expose a `domain` field;
- both are governed diagnostics with read-only/no-mutation boundaries;
- both can be filtered by a CLI `DOMAIN` argument;
- both reason about observation activity boundaries.

The best-supported current description is: **permission domains and visibility
domains are overlapping surface-local vocabularies, not a single coherent
repository concept**.

## Is there a de facto authoritative source?

No single de facto authoritative source was found.

There are local authorities:

- `SUPPORTED_OBSERVATION_CLASSES` is authoritative for currently recognized
  observation-permission domains.
- `CAPABILITY_TO_DOMAIN`, observation families, predicates, and capability
  pressure are authoritative for `observation_domains.py` output construction.
- Observation inventory family derivation is authoritative for family names, but
  not for observation-domain identity generally.
- Capability-needs output is authoritative for capability pressure, but not for
  domain identity generally.

None of these acts as a repository-wide observation-domain authority.

## Supported conclusions

1. The repository currently contains multiple observation-domain vocabularies.
2. Permission-domain identity is explicit and local to
   `SUPPORTED_OBSERVATION_CLASSES`.
3. Visibility-domain identity is mostly derived from observation inventory
   families, predicates, and capability pressure, plus a small hard-coded
   capability-to-domain map.
4. The two vocabularies are exposed through separate diagnostic CLI surfaces:
   `--observation-domains` and `--observation-permission`.
5. The two vocabularies are diagnostic-governed and read-only, but diagnostic
   governance validates surface behavior rather than domain identity.
6. Existing first-class concepts such as entity types, predicates, and
   relationships have catalog/definition/lookup patterns that observation
   domains do not currently have.
7. Current evidence supports conceptual overlap between the two domain
   vocabularies, especially around container runtime and network observation,
   but does not support canonical equivalence.
8. Observation-domain identity is currently fragmented.

## Unsupported conclusions

The current evidence does not support concluding that:

- observation domains already have one repository-wide canonical definition
  source;
- permission domains and visibility domains are intentionally distinct by a
  documented design contract;
- permission domains are projections of visibility domains;
- visibility domains are projections of permission domains;
- observation classes should become catalogs or inheritance structures now;
- a new observation-domain catalog, registry, API, visibility surface, ontology,
  or policy layer is required by current implementation evidence;
- operational story currently contributes direct domain identity values to
  `observation_domains.py` despite being built by that module.

## Open questions

1. Should the word `domain` intentionally mean different things in
   `--observation-domains` and `--observation-permission`, or is this accidental
   vocabulary convergence?
2. Is `docker_socket_read` an access mechanism for the `container_runtime`
   visibility domain, an independent permission domain, or something else?
3. Should family-derived names such as `filesystem_observations` be treated as
   durable domain identities or only as generated visibility labels?
4. Should capability-derived names such as `local_listeners` and
   `container_runtime` be interpreted as operational coverage areas, observation
   domains, or gap labels?
5. Should approval constraints using `observation_domain` refer only to
   permission domains, or can they refer to visibility domains too?
6. Is the unused `story = build_operational_story(state)` call in
   `observation_domains.py` intended future integration, historical residue, or
   an incomplete implementation?
7. What evidence would prove that two surface-local domain names refer to the
   same conceptual observation boundary?

## Acceptance answers

### What is an observation domain?

Today, repository authority gives two answers depending on surface:

- in `observation_domains.py`, an observation domain is a read-only visibility
  entry describing observation coverage, gap classification, capability
  pressure, and evidence;
- in `observation_permission.py`, an observation domain is a permission-visible
  observation activity boundary mapped to an observation class and permission
  state.

There is no current repository-wide definition that subsumes both.

### Where does its identity come from?

Visibility-domain identity comes from a mixture of `CAPABILITY_TO_DOMAIN`,
observation families, predicate prefixes, and capability pressure.
Permission-domain identity comes from `SUPPORTED_OBSERVATION_CLASSES` keys and
filtered requested strings.

### Does the repository have a coherent observation-domain concept?

Not yet, based on current implementation evidence. The repository has coherent
surface-local observation-domain concepts, but not a coherent cross-surface
observation-domain concept with canonical naming or shared identity.

### Are multiple domain vocabularies currently describing overlapping ideas?

Yes. The current vocabularies are not identical and do not share names, but they
appear to describe overlapping observation-boundary ideas: coverage/gap domains
on one side and permission/access domains on the other. Current evidence
supports overlap and fragmentation, not canonical equivalence.
