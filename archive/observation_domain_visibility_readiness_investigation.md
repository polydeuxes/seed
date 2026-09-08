# Observation-domain Visibility Readiness Investigation

## Purpose and boundary

This investigation evaluates whether observation-domain visibility is now mature
enough to become a small read-only repository self-knowledge surface. It is an
implementation-readiness report only. It does not implement a domain model,
visibility command, observers, capabilities, ontology, projection behavior,
policy, root access, Docker access, or any new observation acquisition path.

Repository authority used here is implementation-backed evidence from current
observation, capability, projection, pressure, diagnostic-shape, and prior
investigation surfaces. Domain labels in this document are readiness evidence and
candidate visibility constructs only; they are not preserved knowledge,
projected facts, ontology terms, or an implemented taxonomy.

## Evidence reviewed

The reviewed evidence supports a consistent pattern: Seed can already expose
providers, predicates, predicate utilization, capability pressure, capability
context, operational pressure, projection shape, and repository shape coverage,
but it does not expose observation-domain coverage as its own first-class
surface.

| Evidence | Repository-backed role | Relevance to observation-domain visibility |
| --- | --- | --- |
| `observation_inventory` implementation | Discovers observation providers from Python classes implementing `collect()`, discovers predicates from `Observation(predicate=...)` and helper calls, and derives families from predicate prefixes. | Provides provider, predicate, and prefix-family evidence that candidate domains can be derived from, while also showing that families are mechanical rather than semantic domains. |
| `observation_utilization` implementation | Builds on inventory and checks predicate participation across projection, read-model, and diagnostic source paths. | Provides an existing predicate-level reasoning pattern for collected/projected/read/diagnostic-consumed state, but not domain-level coverage. |
| `capability_needs` / `capability_relationship` | Capability needs are pressure evidence; capability relationship explains current access, operational benefit, pressure, and unknown attainability/expectation without acquisition logic. | Provides pressure inputs and a boundary pattern for relating missing evidence to visibility without recommending capability acquisition. |
| `operational_story` | Composes pressure, capability, privilege, correlation, impact, and investigation-path evidence into a read-only operational narrative. | Shows pressure composition is repository-visible, but domain coverage is not yet an explicit part of that narrative. |
| `projection_shape` | Shows read-only implementation-backed projection stages and authority boundaries. | Supports the distinction between visibility about observation flow and changes to projected facts or stored knowledge. |
| `diagnostic_inventory` / `diagnostic_shape_audit` | Diagnostic entries and shape specs declare and check CLI flags, JSON/record support, repo/state reads, diagnostic fact reads, event-ledger writes, and mutation boundaries. | Provides the expected contract if a future observation-domain visibility surface is implemented: registered, shape-audited, read-only, and non-mutating. |
| `observation_space_visibility_investigation` | Previously concluded Seed can reason about observation space indirectly, while observation-domain coverage is not first-class. | Supplies the strongest prior evidence for candidate domains, classifications, pressure-domain mappings, and missing-evidence vs missing-category distinctions. |
| `non_root_observation_expansion_investigation` | Distinguished missing evidence inside explored domains from unexplored categories. | Supplies reusable gap typing and examples without recommending root, Docker, or new observers. |
| `repository_shape_coverage_investigation` | Classified observations as partially shaped because inventory/utilization/source evidence is distributed. | Supports a readiness conclusion that a small visibility slice could consolidate distributed observation-domain evidence. |

## Reusable reasoning patterns

### 1. Inventory-derived grouping

Existing observation inventory provides three implementation-backed ingredients:
provider names, predicate names, and prefix-derived families. Those are enough to
create conservative candidate groupings such as host identity, host substrate,
storage/mounts, listeners, local networking, DNS configuration, users/groups,
systemd, Prometheus topology, repository/VCS context, and meta-observation.

The important constraint is that current families are derived from predicate
prefixes before the first underscore. That makes them useful implementation
evidence but not authoritative domain semantics. A future surface could therefore
reuse families as supporting evidence, not as the domain source of truth.

### 2. Predicate-utilization flow

Observation utilization already asks whether each discovered predicate is
collected, projected, read by read models, or consumed diagnostically. A domain
visibility slice could reuse the same flow at a higher level, for example by
aggregating predicate rows under a candidate domain and preserving per-predicate
supporting evidence.

This is readiness evidence because it demonstrates that Seed already treats
observation implementation as auditable repository self-knowledge. It is also a
boundary: utilization proves predicate flow, not domain completeness.

### 3. Pressure-to-gap mapping

Capability pressure can already be interpreted against observation inventory:

| Pressure evidence | Candidate domain relationship | Gap type supported by evidence |
| --- | --- | --- |
| `listener_process_inventory` | Listener and process-attribution coverage exists, but owner/process attribution can still be insufficient. | Missing evidence inside a partially observed domain. |
| `container_inventory` / `container_port_mapping` | Capability pressure names container evidence while inventory evidence lacks a container observation family. | Missing observation category/domain in the current inventory. |
| Mount-source / export-side pressure | Local filesystem and mount evidence exists; export-side authority is absent from current inventory. | Mixed: missing evidence inside local mount provenance and missing export-side category. |
| Prometheus identity/scope concerns | Prometheus endpoint and filesystem samples exist but endpoint/host/subject boundaries remain constrained. | Missing evidence or authority inside a partially observed provider domain. |
| Neighbor, route-detail, resolver-runtime, link-discovery absence | Interface, address, default gateway, DNS config, and hosts-file evidence exist, while adjacency/runtime/discovery categories are absent. | Missing observation categories adjacent to partially observed network/DNS configuration. |

This pattern is repeatable and improves pressure interpretation without changing
behavior: pressure can be described as an evidence gap, a category gap, or a
mixed/unknown gap.

### 4. Visibility boundary pattern

Several current surfaces show the expected boundary for an observation-domain
surface: read-only output, no event-ledger writes, no cluster mutation, and no
acquisition or policy recommendation. `capability_relationship` is the closest
pattern because it deliberately reports benefit and pressure while leaving
attainability and expectation unknown. `projection_shape` is the closest pattern
for keeping implementation visibility separate from projected truth.

## Candidate classifications

The classification vocabulary is supported if it remains evidence-bound:

- `observed`: inventory contains provider/predicate evidence that supports a
  conservative statement that the domain is represented in current observation
  implementation.
- `partially_observed`: inventory contains some relevant provider/predicate
  evidence, but implementation boundaries, utilization gaps, capability
  pressure, or prior investigations show incomplete adjacent coverage.
- `unobserved`: reviewed inventory and provider evidence do not show a provider
  or predicate category, while pressure or prior investigations identify it as a
  distinct evidence category.
- `unknown`: repository evidence is insufficient to distinguish intentional
  exclusion, safety/privacy policy, unsupported platform scope, naming mismatch,
  or absent implementation.

These classifications can be produced without inventing new knowledge only when
each row carries supporting evidence and known limitations. The classification
itself should be a visibility judgment over repository evidence, not a stored
truth about the environment.

## Missing evidence versus missing observation category

Repository evidence supports this distinction and shows why a domain visibility
surface would add self-knowledge:

- **Missing evidence** means Seed has some relevant observation coverage, but a
  diagnostic or reasoning path lacks a needed fact. Listener process attribution
  is the clearest example: listener evidence exists, while process ownership
  facts may remain absent or insufficient.
- **Missing observation category** means current inventory does not expose a
  provider/predicate category for the kind of evidence at all. Container runtime
  inventory, container port mapping, neighbor tables, link-layer discovery,
  provider metadata, firewall/NAT state, and remote export-side evidence are
  examples under current reviewed evidence.
- **Mixed gaps** occur when an observed local domain borders an absent authority
  or adjacent domain. Mount provenance versus remote export authority is the best
  example: local mount evidence exists, while export-side observation appears
  absent.
- **Unknown gaps** should be used where absence from inventory alone cannot tell
  whether the category is intentionally excluded, unsafe, platform-specific, or
  simply unimplemented.

Current surfaces allow this distinction through manual investigation. No current
surface answers it directly at the observation-domain level.

## Implementation readiness evaluation

| Criterion | Readiness | Evidence-based rationale |
| --- | --- | --- |
| Stable reasoning pattern | Supported | Inventory-derived grouping, predicate-utilization flow, pressure-to-gap mapping, and read-only boundary patterns recur across existing surfaces and investigations. |
| Sufficient evidence | Mostly supported | Current providers, predicates, families, utilization checks, capability pressure, and prior investigations provide enough evidence for conservative domain visibility. The evidence is distributed rather than centralized. |
| Reusable classifications | Supported with constraints | `observed`, `partially_observed`, `unobserved`, and `unknown` are usable if defined as evidence judgments and paired with support/limitations. |
| Clear boundaries | Supported | Existing diagnostic and relationship surfaces demonstrate read-only, no-recording, no-ledger, no-mutation, no-acquisition boundaries. A future surface must stay on the visibility side. |
| Repeatable use cases | Supported | Repeated questions include whether pressure is caused by missing facts or absent categories, whether existing observation space is understood, and where inventory/utilization/capability evidence connects. |
| Taxonomy authority | Not ready as ontology | Candidate domain labels are not authoritative repository knowledge. They require either curated visibility definitions or transparent derivation rules before implementation. |
| Completeness claims | Not supported | Repository evidence can show current coverage and gaps, not prove all possible domains or all safe/useful observations. |

## Required assumptions for any future small read-only slice

A future implementation slice would need to make the following assumptions
explicit:

1. Observation domains are visibility constructs over implementation evidence,
   not preserved knowledge, ontology terms, or projected facts.
2. Domain rows must expose supporting providers, predicates, families,
   utilization evidence, pressure evidence, and limitations.
3. Absence from current inventory can support `unobserved` only when a reviewed
   pressure or investigation identifies a distinct evidence category; otherwise
   absence should become `unknown`.
4. Pressure relationships must not imply acquisition, prioritization, root
   access, Docker access, or policy approval.
5. The surface should be read-only and non-recording unless a later task
   explicitly changes that boundary; if it becomes a diagnostic surface, it must
   be registered in diagnostic inventory and covered by diagnostic shape audit.
6. Prefix-derived families can support domain grouping but cannot be treated as
   authoritative domain semantics.

## Boundary considerations

Observation domains belong on the visibility side of the repository boundary, if
implemented at all. The concept explains existing observation space; it should
not create new observations, capabilities, stored facts, inferred facts, ontology
classes, or projection behavior.

A safe shape would be a small read-only surface that reports candidate domains,
classification, supporting evidence, pressure relationships, gap type, known
limitations, and authority boundary. The output should be framed as
implementation-backed self-knowledge, not environment truth.

This matches existing repository separations:

- `observation_inventory` exposes implementation-discovered observation shape,
  not environment completeness.
- `observation_utilization` exposes source participation, not domain semantics.
- `capability_relationship` exposes pressure context, not acquisition guidance.
- `projection_shape` exposes projection flow, not new projected facts.
- `diagnostic_shape_audit` checks diagnostic contracts, not runtime truth.

## Supported conclusions

1. Observation-domain visibility is now supported by implementation evidence as
   an emerging read-only self-knowledge concept.
2. Candidate domains can be derived from existing inventory and provider evidence
   when derivation remains transparent and evidence-backed.
3. `observed`, `partially_observed`, `unobserved`, and `unknown` classifications
   can be produced without inventing new knowledge if they are evidence judgments
   with support and limitations, not authoritative ontology labels.
4. Operational pressure can be related to observation-domain coverage by mapping
   capability needs and prior pressure evidence to candidate domains and gap
   types.
5. Missing evidence can be distinguished from missing observation categories
   using repository evidence, although the distinction is currently manual and
   distributed across surfaces/docs.
6. A read-only observation-domain visibility surface would increase repository
   self-knowledge because it would connect existing inventory, utilization,
   pressure, and boundary evidence without changing repository behavior.
7. The concept is mature enough to justify a small read-only visibility slice,
   provided it is explicitly non-authoritative, non-mutating, non-recording, and
   shape-audited if exposed as a diagnostic CLI surface.

## Unsupported conclusions

- It is unsupported to implement a domain model, ontology, projection change, or
  observer as part of this investigation.
- It is unsupported to treat candidate domains here as the final taxonomy.
- It is unsupported to claim that unobserved domains should be implemented,
  prioritized, approved, safe, portable, or useful.
- It is unsupported to recommend root access, Docker access, provider metadata
  access, or any capability acquisition.
- It is unsupported to infer environment truth from domain coverage visibility.
- It is unsupported to treat prefix-derived observation families as semantic
  domain authority.
- It is unsupported to attach diagnostic-only domain findings directly to hosts,
  services, filesystems, or runtime entities.

## Open questions

1. Should a future visibility slice use a curated domain registry, transparent
   derivation rules, provider annotations, or a hybrid of those approaches?
2. What minimum evidence threshold should separate `observed` from
   `partially_observed`?
3. Should utilization/projection participation influence domain classification,
   or should classification be based only on collection inventory?
4. How should pressure map to multiple domains without implying priority or
   acquisition guidance?
5. How should intentionally excluded or privacy-sensitive categories be marked
   when repository policy evidence is absent?
6. Should meta-observation be modeled as an observation domain or as a separate
   self-knowledge layer?
7. If exposed as CLI visibility, should the surface support JSON only, human
   output only, both, or snapshot comparison?

## Acceptance answers

### Is observation-domain visibility now supported by repository evidence?

Yes. It is supported as a read-only visibility concept over existing repository
evidence. It is not supported as preserved knowledge, ontology, projection truth,
or an observer implementation.

### Would it improve repository self-knowledge?

Yes. It would make the repository's existing observation space easier to inspect
by connecting providers, predicates, families, utilization, pressure, and known
limitations at a domain level.

### Would it clarify operational pressure?

Yes. It would clarify whether pressure reflects a missing fact inside a partially
observed domain, an absent observation category, a mixed local/remote authority
gap, or an unknown boundary.

### Would it help distinguish missing evidence from missing observation domains?

Yes. Current evidence already supports that distinction manually. A small
read-only surface would make the distinction repeatable and visible without
changing behavior.

### Is the concept mature enough to justify a small read-only visibility slice?

Yes, with constraints. The slice should be conservative, evidence-backed,
non-mutating, non-recording by default, registered and shape-audited if exposed
as a diagnostic CLI surface, and explicit that domain labels are visibility
constructs rather than repository knowledge or projected facts.
