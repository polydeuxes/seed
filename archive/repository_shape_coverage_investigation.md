# Repository Shape Coverage Investigation

## Scope

This investigation asks which repository domains already have repository-visible
answers to shape questions such as what exists, what consumes or produces it,
what influences it, what does not influence it, what authority applies, and what
boundaries apply. It is an evidence summary, not an implementation plan.

The investigation treats implementation and registered diagnostic surfaces as
authoritative. It does not assume every domain needs the same shape.

## Evidence reviewed

Primary evidence:

- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/operational_graph.py`
- `seed_runtime/component_audit.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/capability_relationship.py`
- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/architecture_conformance_audit.py`

Supporting evidence:

- repository test modules for the surfaces above
- CLI wiring in `scripts/seed_local.py`
- adjacent audit and catalog modules under `seed_runtime/`

Two commands were used as repository-visible checks during the investigation:

```bash
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --diagnostic-shape-audit --json
```

At investigation time, the diagnostic inventory reported 36 registered diagnostic
or diagnostic-like surfaces, and the diagnostic shape audit reported 324 checked
rows with no non-consistent statuses.

## Classification vocabulary

- `shaped`: explicit repository-visible shape exists for the domain's relevant
  questions and includes boundaries or authority where applicable.
- `partially_shaped`: explicit shape exists for some questions or subdomains, but
  coverage is scoped, specialized, or known-limited.
- `implicitly_shaped`: implementation structure, tests, schemas, or catalogs imply
  shape, but no general surface answers shape questions for the domain.
- `unshaped`: no meaningful repository-visible shape evidence was found.
- `unknown`: evidence is insufficient to classify confidently.

## Domain coverage summary

| Domain | Status | Evidence | Shape currently visible | Principal gap |
| --- | --- | --- | --- | --- |
| Diagnostics | shaped | `diagnostic_inventory`, `diagnostic_shape_audit` | Surface identity, CLI flags, JSON/record support, state/repo use, ledger and mutation boundary, implementation contract checks | Domain is diagnostic-specific, not a repository-wide shape map |
| Operational surfaces | shaped | `operational_surface_inventory`, diagnostic inventory, operational graph | CLI-discovered surfaces and read-only diagnostic registration | Shape is strongest for CLI/audit surfaces, weaker for internal-only helpers |
| Operational relationships | shaped | `operational_graph`, confidence, taxonomy | Nodes, edges, relationship types, evidence categories, confidence, aggregate/concrete taxonomy, read-only boundary | Low-confidence edges remain evidence-limited by design |
| Projection | shaped | `projection_shape` | Projection stages, consumes, produces, influences, does-not-influence, authority boundary, event-ledger and mutation boundary | It shapes projection flow, not all consumers' interpretation of projected truth |
| Components | partially_shaped | `component_audit`, operational graph, architecture conformance | Definitions, references, tests, consumers, architecture evidence, overlap, status, unresolved questions | Per-component and query-driven; no complete repository component catalog is exposed by this surface |
| Architecture | partially_shaped | `architecture_conformance_audit` | Architecture terms, architecture evidence paths, operational evidence, conformance classification, realization/significance concepts | Architecture authority is limited to selected docs and implementation-visible graph evidence |
| Capabilities | partially_shaped | `capability_needs`, `capability_relationship`, privilege discovery | Need pressure, current access, operational benefit, reasoning, known limitations, acquisition boundary | Attainability and expectation are explicitly unknown in relationship output |
| Selection | partially_shaped | `selection_path`, `reference_selection`, context-selection code/tests | Selected item, candidates, factors, alternatives, outcome, unknowns, authority boundary for history references | Implemented only for specific targets/domains; unsupported targets return unknown |
| References / historical comparison | partially_shaped | `reference_selection`, `impact_audit`, `history_brief`, `snapshot_policy_audit` | Selected history reference, rationale, alternatives, limitations, snapshot policy evidence | Only the `history` reference-selection domain is implementation-backed |
| Reasoning / derivation | partially_shaped | `reasoning_path`, `operational_story`, pressure/capability audits | Evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, read-only boundary | Uses implemented diagnostics; it is not a general proof engine for all repository conclusions |
| Claims / facts / supports / conflicts | partially_shaped | `facts`, `fact_index`, fact support/conflict views, projection shape | Fact support projection, conflict handling, current fact selection influence, evidence/provenance mechanisms | The domain has projection and view shape, but no single general claim-shape coverage surface |
| Relationships | partially_shaped | `relationship_catalog`, `relationship_observation`, `operational_graph`, projection shape | Catalog relationship projection, legacy relationship projection, operational graph relationships | Runtime/domain relationships and operational implementation relationships are shaped by different surfaces |
| Observations | partially_shaped | `observation_inventory`, `observation_utilization`, observation normalizers/sources | Observation sources, utilization, predicates, and projection consumption | Observation shape is distributed across inventory/utilization/catalog modules |
| Predicates / inference rules | partially_shaped | `predicate_catalog`, `inference_catalog`, `inference_rules`, projection shape | Predicate catalog and inference stage consumption/production | Catalog-level shape exists, but influence/non-influence is mainly visible through projection shape |
| History | partially_shaped | `history_brief`, `impact_audit`, `reference_selection`, audit snapshots | Snapshot comparison, historical references, history summary | History is shaped around audit snapshots, not as a complete temporal model |
| Operational story / pressure | partially_shaped | `operational_story`, `pressure_audit`, `selection_path` | Focus, pressure candidates, selection explanation, story impact | It shapes operational narrative/pressure rather than all repository work prioritization |
| Authority | partially_shaped | projection authority boundaries, architecture authority paths, reference authority boundary, diagnostic registry | Several surfaces expose authority or authority boundaries | Authority is a repeated field pattern, not a centralized repository authority graph |
| Boundaries | shaped for diagnostics and visibility surfaces; partially shaped globally | diagnostic inventory, shape audit specs, projection shape, capability relationship, reasoning/selection audits | Read-only status, records-facts status, event-ledger writes, mutates-cluster status, record scope | Boundaries are consistently visible for diagnostics, less systematic for ordinary library code |
| Implementation reconstruction | partially_shaped | operational graph, component audit, architecture conformance | Repo-file evidence, definitions, consumers, graph evidence, conformance comparison | Reconstruction is query- or surface-specific; no general implementation reconstruction surface exists |
| Repository domains as a whole | partially_shaped | inventory plus specialized audits | Many important domains can be reasoned about from explicit surfaces | No general repository shape coverage inventory exists |

No reviewed evidence established a domain that is both important and completely
`unshaped` in the strong sense of having no observable implementation, tests,
or visibility. However, several domains remain only partially or implicitly
shaped because their evidence is distributed rather than surfaced as a single
shape answer.

## Findings by domain

### Diagnostics are explicitly shaped

Diagnostics have the strongest and most general shape visibility. The inventory
entry model records identity, CLI flags, whether projected state or repository
files are used, JSON and record support, record scope, diagnostic versus cluster
fact emission, event-ledger writes, cluster mutation, diagnostic-fact reads, and
description. The shape-audit implementation then checks registered diagnostics
against implementation specs, including build/format/JSON functions and expected
markers.

This means diagnostics answer all core shape questions at least at the surface
contract level:

- what exists: inventory entries
- what consumes/produces: diagnostic-fact and cluster-fact fields, plus shape
  audit implementation specs
- what authority/boundary applies: record scope, event-ledger writes,
  `mutates_cluster`, read/record behavior
- what is unknown or mismatched: shape-audit status rows

Classification: `shaped`.

### Operational surfaces and operational relationships are explicitly shaped

Operational surfaces are shaped through diagnostic registration and CLI discovery.
Operational relationships are shaped by the operational graph, which composes
implementation-backed emitter/consumer and consumer-dependency audits into nodes,
edges, evidence, confidence, node classification, taxonomy, and metadata.

The graph makes a reusable relationship form explicit:

```text
node -> edge -> node
edge evidence -> confidence
node classification -> aggregate/concrete taxonomy
metadata -> read-only boundary
```

The confidence and taxonomy companion views make uncertainty and node-kind shape
visible rather than hidden. Aggregate nodes and low-confidence edges are not
failures; they are explicit shape evidence that implementation reconstruction is
partial at those points.

Classification: `shaped` for registered/CLI operational surfaces and
implementation-backed operational relationships; `partially_shaped` for internal
helpers not represented as surfaces or graph nodes.

### Projection is explicitly shaped

Projection has a dedicated shape surface. It names stages and records each
stage's consumed inputs, produced outputs, influences, non-influences, and
authority boundary. It also exposes the read-only/no-ledger/no-cluster-mutation
boundary for the diagnostic itself.

This is the clearest evidence that shape visibility is not limited to surface
inventory. Projection shape answers both positive and negative influence
questions, such as which stages affect selection, inference, relationships, graph
issues, conflict handling, or event-ledger mutation.

Classification: `shaped` for projection mechanics.

### Components and architecture are partially shaped

Components can be investigated with `component_audit`, which searches definitions,
references, tests, consumers, operational graph matches, architecture evidence,
possible overlap, status evidence, and unresolved questions for a named component.
This is explicit shape for a requested component, but it is not a complete
component inventory.

Architecture conformance compares selected architecture evidence against
operational graph evidence and classifies alignment, drift, underspecification,
obsolete design, emergent structure, and unknowns. It includes architecture terms
and authority paths, but those paths are finite and curated.

Classification: `partially_shaped`.

### Capability shape exists but preserves unknowns

Capability relationship visibility connects capability needs to current access,
operational benefit, pressure, attainability, expectation, reasoning, known
limitations, and boundary. The implementation deliberately reports attainability
and expectation as unknown when repository evidence does not establish operator
intent or deployment expectation.

This is important: the shape is not just what is known. It also preserves where
repository authority stops.

Classification: `partially_shaped`.

### Selection, references, and reasoning are partially shaped

Selection has explicit surfaces for implemented operational selections and for
history reference selection. The selection path shows selected item, candidates,
selection factors, non-selected candidates, evidence, outcome, unknowns, and
boundary. Reference selection shows a selected reference, rationale,
alternatives, authority boundary, limitations, and no-mutation/no-ledger status.

Reasoning path visibility shows evidence, intermediate conclusions, derived
conclusions, consumers, story impact, unknowns, and read-only boundary. It builds
from implemented diagnostics rather than from a general proof system.

Classification: `partially_shaped` because the surfaces are explicit but scoped.
Unsupported targets and domains return unknown rather than reconstructing new
logic.

### Claims, supports, conflicts, relationships, observations, predicates, and inference are distributed-shape domains

These domains have real implementation and tests. They also have shape-relevant
visibility through projection shape, catalogs, views, current-fact and support
surfaces, conflict views, relationship catalogs, observation inventories, and
inference catalogs.

However, their shape is distributed:

- projection shape explains how facts, supports, conflicts, relationships,
  observations, predicates, and inference participate in projection;
- catalogs define accepted predicates, relationships, entity types, and inference
  rules;
- state views expose current facts, support, conflicts, inferred facts, graph
  issues, relationships, and observations;
- tests preserve many invariants.

The repository can answer many local shape questions in these domains, but no
single general domain-shape surface answers all core questions for claims,
supports, conflicts, observations, or inference.

Classification: `partially_shaped` or `implicitly_shaped` depending on the
question. Projection participation is explicit; full domain shape is not.

## Shape gaps

The gaps below are descriptive, not recommendations.

1. **No general repository shape coverage inventory.** The repository has a
   diagnostic inventory and many domain-specific surfaces, but no general
   inventory of all domains and their shape status.
2. **Distributed shape for knowledge domains.** Claims, facts, supports,
   conflicts, observations, predicates, relationships, and inference are visible
   through projection, catalogs, and views, but not through a single shape map.
3. **Query-scoped reconstruction.** Component audit and several path audits are
   strong for a requested target but do not enumerate all possible targets.
4. **Authority is repeated, not centralized.** Authority boundaries appear in
   projection shape, reference selection, architecture conformance, diagnostic
   inventory, and capability relationship, but there is no single authority
   topology.
5. **Boundaries are strongest for operational visibility.** Read-only,
   record-scope, event-ledger, and cluster-mutation boundaries are explicit for
   diagnostic/visibility surfaces. Ordinary internal implementation modules rely
   more on tests and code structure.
6. **Unknowns are shaped only where surfaces choose to expose them.** Several
   surfaces preserve unknowns explicitly, but this is not yet universal across
   all domains.

## Common shape patterns supported by repository evidence

The recurring pattern is real. Shape visibility is emerging around a small set of
reusable forms:

### Identity

Many surfaces start by naming the thing under investigation: diagnostic name,
CLI flag, projection stage, graph node, component, capability, domain, subject,
target, reference, predicate, relationship, or snapshot kind.

### Relationship

Operational graph edges, projection consumes/produces/influences fields,
capability pressure relationships, component consumers, fact supports, and
reference alternatives all make relationships visible.

### Selection

Selection appears in projection current-fact selection, measurement retention,
selection path candidates, history reference selection, snapshot comparison, and
operational pressure focus.

### Reference

Reference appears as implementation evidence sources, architecture evidence
paths, audit snapshots, selected history references, event/evidence provenance,
and graph edge evidence.

### Authority

Authority appears as projection authority boundaries, architecture evidence
paths, reference-selection authority boundaries, diagnostic implementation specs,
and explicit statements that capability expectation or deployment intent is
unknown.

### Boundary

Boundaries appear as read-only status, writes-event-ledger status,
mutates-cluster status, record scope, records-facts status, and capability
acquisition/planning exclusions.

### Visibility of non-influence and unknowns

Projection shape explicitly records `does_not_influence`. Selection,
reference-selection, reasoning, architecture conformance, component audit, and
capability relationship surfaces expose unknowns, limitations, unresolved
questions, or low-confidence evidence instead of silently inventing certainty.

### Confidence / evidence strength

Operational graph confidence, architecture evidence confidence, diagnostic shape
status, component status evidence, and capability reasoning all show that shape
is often evidence-graded rather than binary.

## Supported conclusions

1. **Diagnostics are already shaped.** The inventory plus shape audit provide a
   general surface-level diagnostic shape contract.
2. **Projection is already shaped.** Projection stages explicitly expose inputs,
   outputs, influence, non-influence, authority, and boundary.
3. **Operational relationships are already shaped.** The operational graph makes
   implementation-backed nodes, edges, evidence, confidence, and taxonomy
   visible.
4. **Capabilities, components, architecture, selection, references, reasoning,
   history, observations, facts, supports, conflicts, relationships, predicates,
   and inference are partially shaped.** Their shape exists, but is scoped,
   query-driven, or distributed across multiple surfaces.
5. **Shape visibility is emerging as a general repository pattern.** The repeated
   identity/relationship/selection/reference/authority/boundary/unknown pattern
   appears independently across several implementations.
6. **Repository shape coverage can be reasoned about systematically.** The
   repository already contains enough shape-bearing surfaces to classify domains,
   identify evidence, and distinguish explicit, partial, implicit, and unknown
   shape without designing new machinery.

## Unsupported conclusions

The investigation does not support these stronger claims:

- Every repository domain is fully shaped.
- Every domain should have the same kind of shape.
- A centralized ontology or architecture redesign is required.
- Presentation vocabulary is automatically repository knowledge.
- Diagnostic findings should become cluster truth.
- Capability pressure implies acquisition intent.
- Reference selection is implemented for every domain.
- Operational graph confidence gaps are defects rather than explicit evidence
  limits.

## Open questions

These questions remain open because the current repository evidence does not
answer them generally:

1. What is the complete set of repository domains if domains are not limited to
   diagnostic or CLI surfaces?
2. Which internal-only modules should count as domains rather than implementation
   details?
3. Where should the boundary be drawn between projection shape and claim/fact
   domain shape?
4. Is authority intended to remain surface-local, or merely not yet centralized?
5. Should query-scoped audits such as component audit be treated as sufficient
   shape for their domains, or only as reconstruction tools?
6. Are distributed catalog/view/test invariants enough to classify a domain as
   partially shaped, or should they remain `implicitly_shaped` until a dedicated
   surface exists?
7. Which unknowns are intentionally preserved, and which are merely not yet
   represented?

## Direct acceptance answers

### Which repository domains are already shaped?

Diagnostics, diagnostic implementation contracts, projection mechanics,
registered operational surfaces, and implementation-backed operational
relationships are already shaped.

### Which remain unshaped?

No important reviewed domain was proven completely unshaped. The stronger finding
is that several domains are not generally shaped: they are partial, implicit, or
distributed.

### Which are partially shaped?

Components, architecture, capabilities, selection, references, reasoning,
history, operational story/pressure, claims/facts/supports/conflicts,
relationships, observations, predicates, inference, authority, implementation
reconstruction, and repository domains as a whole are partially shaped.

### Is shape visibility emerging as a general repository pattern?

Yes. The same reusable patterns recur across independent surfaces: identity,
relationship, selection, reference, authority, boundary, unknowns, and
evidence/confidence.

### Can repository shape coverage be reasoned about systematically?

Yes, with the current evidence. The repository already supports systematic
classification by looking for explicit surfaces, scoped surfaces, implementation
and test-backed implicit shape, unknown preservation, and boundary/authority
statements. It does not yet provide a single general coverage inventory, so the
systematic reasoning still requires cross-surface investigation.
