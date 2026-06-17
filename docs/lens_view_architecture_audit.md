---
status: audit
scope: lens/view architecture investigation
created: 2026-06-17
---

# Lens / View Architecture Audit

## Status

This is an architectural audit only. It does not implement views, implement
dashboards, redesign State Summary, create Seed Ops, create HomeOps, or promote a
new canonical lens/view ontology.

Repository authority is stronger for `State`, `projection`, and existing
`State Views` / `Context Views` than it is for a general `lens` primitive. Lens
language exists mostly in exploratory observations and scope reviews. View
language exists both in implementation and architecture documentation, but the
repository uses it in at least two senses: concrete read-only projection objects
and broader operator-facing surfaces.

## Audit Question

```text
What is a lens?
What is a view?
How do they relate to State?
How do they differ from projections?
```

The answer must use repository evidence rather than inventing architecture.

## Repository Evidence

### Files Inspected

Implementation and tests:

- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/context_views.py`
- `seed_runtime/inquiry_orientation.py`
- `tests/test_state_views.py`
- `tests/test_state_summary_views.py`
- `tests/test_context_views.py`
- `tests/test_inquiry_orientation.py`

Architecture and repository orientation:

- `README.md`
- `01-architecture.md`
- `13-knowledge-and-evidence.md`
- `IMPLEMENTATION.md`
- `docs/README.md`
- `docs/index.md`
- `docs/architecture.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/ontology.md`
- `docs/foundational_ontology_reconciliation.md`

State Summary and read-surface materials:

- `docs/state_summary_scope_review.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/state_summary_cli_boundary_audit.md`
- `docs/state_summary_top_entity_selection_audit.md`
- `docs/state_summary_endpoint_prominence_audit.md`
- `docs/state_summary_filesystem_projection_boundary_audit.md`
- `docs/state_summary_empty_operator_kind_buckets_audit.md`
- `docs/state_summary_performance_inquiry_lineage_report.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/entity_impact_drilldown_reconciliation.md`

Lens, observation, understanding, knowledge, work-position, and orientation
materials:

- `docs/lens_catalog_observation.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/learning_as_lens_observation.md`
- `docs/inquiry_preservation_observation.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/operator_surface_activation_against_knowledge_and_understanding_audit.md`
- `docs/understanding_visibility_existing_surface_audit.md`
- `docs/understanding_navigation_observation.md`
- `docs/understanding_claim_and_decompression_observation.md`
- `docs/knowledge_and_understanding_distinction_observation.md`
- `docs/knowledge_representation_map.md`
- `docs/knowledge_representation_reconciliation.md`
- `docs/current_work_position_frontier.md`
- `docs/orientation_object_observation.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/orientation_non_convergence_audit.md`
- `docs/work_shape_and_orientation_observation.md`
- `docs/inquiry_note_orientation_probe_plan.md`
- `docs/inquiry_note_orientation_probe_work_order.md`
- `docs/inquiry_note_orientation_surface_reachability_observation.md`
- `docs/storage_topology_observation.md`
- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`

### Strongest Evidence Points

1. `StateProjector` rebuilds inspectable state from ledger events and derives
   projection indexes. `State` contains entities, facts, observations,
   evidence, relationships, aliases, fact support, conflicts, graph issues,
   goals, tool needs, approvals, plans, and tools.
2. `State Views` are implemented as deterministic read-only projections of an
   already-built `State`; they do not read ledgers, append events, call
   providers, evaluate policy, or execute runtime behavior.
3. `Context Views` are implemented as read-only deterministic projections from
   already-projected `State` plus evidence graph, contradiction detection, and
   confidence aggregation. They form the boundary from knowledge to future
   decision providers.
4. `state_summary_views.py` explicitly describes its module as semantic
   aggregation for the operator State Summary and states that CLI code should
   render returned data rather than decide what the summary means.
5. `State Summary Scope Review` distinguishes the compact projected world-model
   summary from the richer operator State Summary. Counts and projection
   identity are closest to State itself; top entities, endpoint visibility,
   availability scope, and storage interpretation are lens/view choices.
6. `View Authority And Surface Responsibility Reconciliation` treats output
   disagreements as authority disagreements and distinguishes evidence,
   interpretation, integrity, and navigation surfaces.
7. `Lens Catalog Observation` offers a cautious working definition: a lens is a
   deterministic, read-only way of viewing projected State for a bounded
   question, attention pattern, or interpretive purpose.
8. `Lens As Observation And Compression Pattern` is weaker authority: it says
   lens language is often a broad observation stance or compression pattern, not
   a runtime primitive, authority source, policy, goal, identity, or sufficient
   explanation.
9. `Lens, Orientation, And Dashboard Observation` records an exploratory shift
   from `one State -> one dashboard` toward `one State -> many views/lenses`,
   while explicitly refusing to define canonical architecture.

## State Responsibilities

Repository evidence supports these responsibilities for State:

- hold the current projected read model derived from the event ledger;
- preserve inspectable current structures: entities, facts, observations,
  evidence, relationships, aliases, entity type assertions, fact supports,
  conflicts, graph issues, goals, tool needs, approvals, plans, handoffs, tools,
  projection version, and last event identity;
- be deterministic and rebuildable from event history;
- preserve current knowledge and integrity structures without becoming raw
  reality, authority outside its evidence, or a UI/dashboard;
- support read-only queries and downstream projections.

State should not own:

- provider calls;
- shell/network execution;
- policy evaluation as part of read surfaces;
- operator dashboard design;
- hidden mutation paths;
- unbounded interpretation beyond projected evidence.

## Projection Responsibilities

Repository evidence uses projection in two related but different ways.

### State Projection

The `StateProjector` reads ledger events, applies event payloads, and finalizes
derived indexes. Its responsibilities include:

- replaying append-only events into State;
- retaining current measurement history according to projection rules;
- deriving inferred facts;
- resolving aliases from explicit alias facts;
- building FactSupport aggregates;
- projecting relationship edges from facts;
- projecting entity type assertions;
- validating graph issues;
- projecting fact conflicts;
- producing deterministic diagnostics and counts when requested.

### Read/View Projection

State Views and Context Views are also called projections. In this sense,
projection means deterministic selection/transformation of already-projected
State into read-only structures for a consumer. These projections:

- do not create a second state store;
- do not append events;
- do not mutate State;
- do not call providers, tools, LLMs, shell commands, or networks;
- may select, summarize, sort, mark, group, or expose fields for a bounded
  consumer.

Therefore, projection is broader than `StateProjector`. It includes the State
projection boundary and later read-model projections.

## Lens Responsibilities

Repository authority for lens is exploratory rather than canonical. The safest
audit finding is:

```text
A lens is a bounded way of viewing already-projected State or repository
knowledge for a question, attention pattern, interpretive concern, or operator
purpose.
```

Responsibilities that appear lens-like:

- select which parts of State matter to a bounded question;
- group, rank, suppress, caveat, or classify already-projected material;
- preserve the path back to evidence/provenance when compression hides detail;
- make a family of related signals visible without claiming to be the family;
- state its authority and non-authority so compressed output is not mistaken for
  truth, ownership, health, topology, action priority, or operator intent.

Lens non-responsibilities:

- not State;
- not environmental truth;
- not a mutation path;
- not a live probe;
- not a provider, tool, policy, goal, or decision authority;
- not a sufficient explanation once compressed distinctions matter;
- not necessarily a runtime object or schema until reconciled elsewhere.

## View Responsibilities

The repository already has concrete view implementations and broader view/surface
discussion.

A view appears to be a read-only representation rendered or consumable by a
particular actor or downstream component. In implementation, a view is often a
projection object or dictionary built from State. In documentation, a view or
surface also carries consumer-specific authority.

View responsibilities:

- expose selected projected knowledge without requiring callers to read raw
  events;
- answer a stated consumer question;
- preserve enough information for the view's authority: evidence surfaces should
  preserve inspectability; interpretation surfaces may summarize but need paths
  back to evidence; integrity surfaces should preserve uncertainty/conflict;
  navigation surfaces should route attention without hiding authority limits;
- render or package lens/projection output for a caller or operator;
- avoid inventing stronger claims than the underlying State/projection/lens
  supports.

View non-responsibilities:

- not a separate persistence system;
- not automatically a dashboard;
- not automatically presentation-only, because some views own selection and
  authority boundaries before rendering;
- not a permission to hide evidence in evidence-oriented surfaces;
- not execution, provider invocation, policy evaluation, or State mutation.

## Candidate Architecture

The strongest repository-consistent candidate relationship is:

```text
Event Ledger
    -> State Projection
    -> Projected State
    -> Read/View Projections
    -> Lens-scoped interpretation/selection/grouping
    -> View/surface rendering or downstream consumption
```

This is a candidate architecture, not a new canonical contract.

### Hypothesis A

```text
Projection creates structure
Lens interprets structure
View renders structure
```

Partly supported, but too clean.

- State projection clearly creates/derives structures from events.
- Read/view projections also create read-only structures from State.
- Lenses often interpret/select/group projected structures for bounded purposes.
- Views render or expose structures, but views are not merely rendering: view
  authority determines what may be summarized, grouped, or hidden.

A safer version:

```text
Projection deterministically derives or selects structures.
Lens names the bounded viewing purpose and interpretation authority.
View exposes that selected structure to a consumer, possibly rendered.
```

### Hypothesis B

```text
Lens is itself a projection
```

Sometimes plausible, not fully established.

Implementation does not define a `Lens` type. Existing `State Views`, `Context
Views`, State Summary sections, source navigation, and storage projection can be
read as lens-like projections. Exploratory lens documents support `many possible
read-only views` over one deterministic State. However, lens language also covers
observation/compression patterns in documentation, which are not necessarily
runtime projections.

Conclusion: a runtime lens may be implemented as a read-only projection, but the
repository has not canonically stated that every lens is a projection or that
`Lens` is a first-class projection type.

### Hypothesis C

```text
View is presentation only
```

Not supported.

Views can include rendering, but repository evidence treats view responsibility
as authority-bearing. Evidence, interpretation, integrity, and navigation
surfaces differ in what information must remain visible and what may be
summarized. `Context Views` are not merely presentation; they are the supported
boundary between knowledge and future decision providers. `State Views` are
projection objects, not just text formatting.

Conclusion: presentation is one view responsibility, but view authority and
consumer-specific selection are architectural responsibilities too.

### Hypothesis D

```text
State supports many lenses
Lens supports many views
```

Partly supported and useful, but not canonical.

The first line is strongly supported by lens catalog and dashboard observations:
one deterministic State can support current facts, State Summary, source
navigation, storage topology, integrity, impact/detail, context views, and
inquiry-orientation surfaces.

The second line is plausible but less directly evidenced. A storage lens could
support a summary panel, node detail view, or topology drilldown if caveats are
preserved. An availability lens could support State Summary counts or a future
HomeOps-oriented panel. But the repository has not established a formal
`Lens -> many Views` contract.

## State Summary Classification

State Summary should be considered a combination, with two distinct layers.

1. `seed_runtime/state_views.py::build_state_summary(state)` is closest to a
   compact read-only projection / state view. It counts projected facts,
   observations, requirements, capabilities, issues, and projection identity.
2. `seed_runtime/state_summary_views.py::state_summary(state)` is a richer
   operator summary over projected State. It combines State/projection counts,
   integrity-adjacent accounting, observation accounting, prominence lenses,
   availability-by-scope lenses, and storage projection helpers.

Therefore:

```text
State Summary = combination
    compact State View / projection
    + operator-facing summary surface
    + several lens-like selections and caveats
```

It should not be treated as a dashboard, impact surface, runtime health checker,
storage-topology authority, recommendation engine, or the only canonical operator
surface.

## Emerging Surfaces

### Seed Ops

Repository evidence suggests `Seed Ops` is not implemented and not defined as a
canonical surface. If it emerges, it should first be investigated as an operator
surface family or navigation/operations lens over projected Seed-runtime
knowledge, not assumed to be a dashboard.

Candidate classification: unresolved; likely lens/view family, not State.

### HomeOps

`HomeOps` appears as an operator-oriented possibility in lens/dashboard
conversation, not as a current implementation or architecture. It may be an
operator-oriented surface over availability, topology, storage, capability, and
integrity lenses.

Candidate classification: unresolved; likely view/dashboard candidate composed
from lenses, not a projection authority by itself.

### Storage

Storage has the strongest concrete implementation evidence among candidate
surfaces. `storage_state_projection(state)` builds an explicit
storage/filesystem topology projection surface from projected State. It includes
filesystem summaries, cluster mount groups, shared-storage candidates, and
storage-topology ambiguities, with explicit boundaries that candidates are not
facts, ownership, storage identities, or topology truth.

Candidate classification: read-only projection with lens-like interpretation;
may feed future views.

### Topology

Topology is present as relationship and graph projection, graph validation, and
storage-topology ambiguity/candidate language. Storage topology candidates are
explicitly non-authoritative. General topology should not be assumed from
presentation grouping.

Candidate classification: projection when derived by catalog/graph rules;
lens/view when grouped for operator interpretation; unresolved as a dashboard
surface.

### Capability Readiness

Capability readiness is already visible through ToolNeeds, CapabilityCatalog,
capability resolution/recommendations, and capability/status views. It is
downstream of projected knowledge and not execution authority.

Candidate classification: projection/read view today; potential lens or
navigation surface for operators.

### Repository Understanding

Understanding documents distinguish knowledge from understanding and often treat
understanding as decompression, navigation, or operator activation concern.
Existing repository understanding surfaces are mostly documentation/navigation
surfaces and observation/audit materials, not State projections unless backed by
implemented source navigation or inquiry-orientation structures.

Candidate classification: repository/documentation navigation lens; not current
State by default.

## Summary / Dashboard / Orientation Distinctions

- **Summary**: compact accounting or aggregation. It may be narrow State shape
  (`build_state_summary`) or richer operator aggregation (`state_summary`).
- **Dashboard**: an operator-facing composition of multiple concerns. The
  repository treats the old `one State -> one dashboard` pressure as a problem,
  not as an architectural target.
- **Orientation**: not simply knowledge. Orientation appears to concern the
  relationship between participant, current concern, inquiry, active edge,
  continuation, and preserved knowledge. It may emerge through interaction with
  surfaces rather than exist as a first-class object.

## Operator Notes Versus Structured Lens/View Contract

Operator notes remain appropriate today because the repository has not reconciled
a structured lens/view contract. They are especially appropriate for preserving:

- boundary warnings;
- current work position;
- inspected evidence;
- unresolved pressure;
- why a surface should not be interpreted as authority.

A more structured contract is emerging, but not settled. The likely contract
questions are:

```text
consumer
primary question
input projections
selection rules
compression rules
evidence path / drilldown path
authority boundary
non-authority boundary
rendering responsibility
```

The repository should not implement dashboards or new views before reconciling
that contract.

## Non-Conclusions

This audit does not conclude that:

- `Lens` is a canonical runtime class;
- every lens is a projection;
- every view is presentation-only;
- State Summary should be redesigned now;
- Seed Ops or HomeOps should exist;
- Storage Topology candidates are topology facts;
- availability summaries are live health checks;
- orientation is a first-class object;
- operator notes should be replaced immediately.

## Recommended Next Investigation

Recommended next investigation:

```text
View/lens contract reconciliation before implementation.
```

Scope:

- inventory existing read surfaces by consumer and authority;
- define whether `lens` remains documentation vocabulary or becomes an
  implementation contract;
- distinguish projection objects, lens semantics, and rendered views;
- specify mandatory caveat/evidence-path fields for compressed surfaces;
- decide whether State Summary should merely label its existing sub-lenses or
  split later into separate surfaces;
- evaluate Seed Ops, HomeOps, Storage, Topology, capability readiness, and
  repository understanding as candidate lens/view families without implementing
  them.
