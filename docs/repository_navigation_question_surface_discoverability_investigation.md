# Repository Navigation Question-to-Surface Discoverability Investigation

## Purpose and boundary

This investigation asks whether Seed can currently help a worker move from a
natural repository question to the self-knowledge surface that can answer it.
It is an understanding document only. It does not implement navigation systems,
command routers, question answering, recommendation engines, CLI behavior,
commands, diagnostics, or new ontology.

Repository authority remains the implementation, tests, and existing
repository-visible documents. The mappings below are descriptive evidence from
current surfaces, not a proposed command contract.

## Evidence reviewed

Primary evidence reviewed:

- `seed --diagnostic-inventory`, which lists operational surfaces, flags, state
  and repository-file use, JSON support, record support, event-ledger behavior,
  and descriptions.
- `seed --diagnostic-shape-audit --mismatches`, which currently reports no
  mismatched diagnostic shape rows across the inventory/spec implementation
  boundary.
- `seed_runtime/diagnostic_inventory.py`, especially the registry entries for
  projection, component, reasoning, selection, reference, operational story,
  capability, pressure, consumer, emitter, and operational graph surfaces.
- `seed_runtime/diagnostic_shape_audit.py`, especially implementation specs that
  bind diagnostic names to modules, build functions, format functions, JSON
  functions, CLI flags, repo-file markers, and diagnostic-fact read markers.
- `docs/source_navigation_surface_reconciliation.md`, which distinguishes
  preservation from navigation and says a repository can preserve source facts
  while still failing navigation when operators must already know exact fact
  shapes.
- `docs/projection_self_description_investigation.md`, which found projection
  behavior visible but not organized into a complete self-description.
- `docs/observation_space_visibility_investigation.md`, which found Seed can
  answer predicate and capability questions better than domain-coverage
  questions.
- `docs/README.md`, which is explicitly the documentation navigation authority
  and routes readers to documents that own answers without restating them.
- Tests around source navigation, inquiry orientation, integrity-summary
  navigation hints, documentation navigation metadata, diagnostic inventory, and
  diagnostic shape audit.

## Central finding

Seed already contains substantial repository self-knowledge, but the path from a
worker's question to the correct surface is uneven.

```text
Seed often has the answering surface.
Seed less often has a repository-visible way to choose that surface.
```

The strongest current pattern is **surface self-description after selection**:
when the worker already selects `projection_shape`, `component_audit`,
`operational_story`, `diagnostic_shape_audit`, or `capability_relationship`, the
surface usually explains its own scope clearly. The weaker pattern is
**question-to-surface discovery before selection**: a new worker must often know
surface names, command flags, and normalized repository vocabulary before the
right answer becomes easy to obtain.

## Common worker question clusters

The examples in the task naturally cluster into recurring repository question
families. These clusters are descriptive; they are not a new schema.

| Worker question family | Example questions | Existing answering surfaces | Discoverability classification | Evidence-based explanation |
| --- | --- | --- | --- | --- |
| Inventory / existence | What exists? Which surfaces exist? Which predicates exist? Which CLI surfaces are visible? | `diagnostic_inventory`, `operational_surface_inventory`, `observation_inventory`, `source_navigation`, `docs/README.md` | Well discoverable for diagnostic surfaces; partially discoverable across all repository knowledge | The diagnostic inventory explicitly lists names, flags, descriptions, JSON/record support, state/repo-file use, and mutation boundaries. Documentation also has a navigation authority. But the worker must still know which inventory applies: diagnostics, operational surfaces, observations, docs, source facts, or repository files. |
| Shape / implementation-backed contract | What shape does this have? Does the registry match implementation? What does projection produce? | `projection_shape`, `diagnostic_shape_audit`, shape-related investigations | Well discoverable once shape language is known; partially discoverable from natural questions | `projection_shape` and `diagnostic_shape_audit` are explicitly named around shape. The shape audit proves registry/spec consistency. Natural questions like “how is this built?” or “what does this produce?” do not automatically route to these surfaces. |
| Component role / ownership-ish location | What owns this? What role does this component play? What consumes it? What implementation evidence names it? | `component_audit`, `consumer_audit`, `emitter_consumer_audit`, `operational_graph`, source navigation | Partially discoverable | `component_audit` summarizes named component role from repository, graph, consumer, test, and architecture evidence. Source navigation cautions that navigation is not ownership. Workers can find role evidence, but ownership, definition, consumption, and reachability are separate questions that require choosing among several surfaces. |
| Producer / consumer / influence | What produces it? What consumes it? What influences it? | `consumer_audit`, `emitter_consumer_audit`, `emitter_attribution_audit`, `projection_shape`, `operational_graph`, `observation_utilization` | Partially discoverable | Producer/consumer words appear in surface names for emitters and consumers, while projection influence appears in `projection_shape` and observation predicate use appears in `observation_utilization`. The relationship among these surfaces is implementation-visible but not presented as a unified question route. |
| Reasoning / derivation | Why is this conclusion true? What evidence supports it? What intermediate conclusions exist? | `reasoning_path`, `why-fact`, fact support views, `operational_story` | Partially discoverable | `reasoning_path` is explicitly evidence-backed derivation from source evidence through conclusions, consumers, and story impact. However, the worker must know whether the target is a fact, operational conclusion, selection outcome, or implementation component. |
| Selection / comparison reference | Why was this selected? What alternatives were not selected? Compared to what? | `selection_path`, `reference_selection`, candidate-baseline and reference-selection investigations | Partially discoverable | `selection_path` names candidates, factors, alternatives, and outcomes. `reference_selection` exposes implementation-selected comparison-reference visibility. These are strong after the worker identifies the question as selection/reference reasoning. |
| Capability / missing evidence | What capability is missing? What pressure exists? What access/benefit/expectation is visible? | `capability_needs`, `capability_relationship`, `pressure_audit`, `privilege_discovery`, `operational_story` | Well discoverable for capability language; partially discoverable for generic “missing” questions | Capability surfaces have explicit names and diagnostic inventory descriptions. Generic “what is missing?” can mean missing observer, missing evidence, missing domain coverage, missing implementation surface, missing relationship, or missing documentation; routing remains contextual. |
| Current operational focus / pressure | What is the repository focused on? What changed? What pressure exists now? | `operational_story`, `pressure_audit`, `ops_brief`, `history_brief`, `impact_audit`, `snapshot_policy_audit`, audit snapshots | Partially discoverable | The operational story composes pressure, capability, privilege, correlation, impact, and investigation-path evidence. History and impact surfaces cover change. The family is visible in inventory, but “current focus” can route to several surfaces depending on whether the worker wants pressure, history, impact, or triage. |
| Source artifact navigation | Where is the relevant source? What defines/imports this? What support chain explains it? | `source_navigation`, current facts, fact support, `why-fact`, repository observation documents | Partially discoverable | Source navigation is repository-visible and read-only, and prior reconciliation explicitly frames navigation as moving from a question to source artifact, relationship, and support. It is limited to preserved source facts and should not overclaim behavior, ownership, or reachability. |
| Domain coverage / observation space | Is this domain observed? Is evidence missing inside a domain or is the domain absent? | `observation_inventory`, `observation_utilization`, `capability_relationship`, `operational_story`, observation-space investigation | Poorly to partially discoverable | Predicate and capability surfaces are strong, but observation-space investigation found domain reasoning is not first-class and must be inferred from predicate inventory, capability names, diagnostics, and documents. |
| Cross-surface follow-up | Which follow-up surface should I use? Which surfaces are related? | `diagnostic_inventory`, `diagnostic_shape_audit` implementation specs, `operational_story`, `ops_brief`, docs map, source-navigation/frontier documents | Poorly to partially discoverable | Relatedness exists in implementation markers and composed surfaces, and docs route readers. But no current repository-visible surface primarily answers “given this question, ask this next surface.” |

## Candidate question-to-surface mappings already implied by repository evidence

The following mappings are supported as current descriptive practice, not as a
complete or normative router.

| Question shape | Likely surface(s) | Confidence | Why this mapping is supported |
| --- | --- | --- | --- |
| Projection composition, stages, observation-to-state flow, inferred facts | `projection_shape` | High | The surface is named for projection shape and is registered as read-only implementation-backed projection stage shape. Prior projection investigation also identifies projection self-description as the relevant gap. |
| Diagnostic registry/implementation consistency | `diagnostic_shape_audit` | High | The shape audit binds inventory entries to implementation specs and currently reports no mismatches. |
| Diagnostic/test-like surface discovery | `diagnostic_inventory` | High | The inventory lists operational diagnostic surfaces with flags, descriptions, state/file usage, JSON/record behavior, fact emission, ledger writes, and mutation boundaries. |
| Component role from repository, graph, consumer, tests, architecture evidence | `component_audit` | High | The inventory description and implementation spec explicitly point at component role evidence across repository and graph sources. |
| Operational pressure and current narrative | `operational_story`, then `pressure_audit` or `ops_brief` | Medium-high | `operational_story` composes pressure/capability/privilege/correlation/impact/investigation-path surfaces; `ops_brief` aggregates triage surfaces. |
| Selection reasoning | `selection_path` | High | The surface is explicitly candidates/factors/non-selected alternatives/outcome. |
| Reference reasoning / comparison baseline visibility | `reference_selection` | High | The surface is explicitly implementation-selected comparison-reference visibility and related investigations treat reference selection as comparison traceability. |
| Derivation reasoning from evidence through conclusions | `reasoning_path` | High | The surface is explicitly evidence-backed derivation paths from source evidence through conclusions, consumers, and story impact. |
| Capability context, missing access, benefit, pressure, attainability, expectation | `capability_relationship`, with `capability_needs` as source pressure | High | The inventory description uses exactly these dimensions and notes diagnostic-fact reads. |
| Producer/consumer relationship around emitted outputs | `emitter_consumer_audit`, `emitter_attribution_audit`, `consumer_audit` | Medium-high | Surface names and descriptions explicitly target emitted outputs, visible consumers, and attribution. |
| Predicate collection and predicate usage | `observation_inventory`, `observation_utilization` | Medium-high | Observation-space investigation identifies these as predicate-level self-knowledge surfaces. |
| Source definition/import/support lookup | `source_navigation`, current facts, fact support, `why-fact` | Medium | Source navigation exists and is tested, but prior reconciliation warns preserved source facts are not automatically ownership, behavior, or reachability truth. |
| Follow-up guidance among surfaces | `operational_story`, `ops_brief`, docs map, diagnostic specs | Low-medium | These surfaces imply relationships or aggregate surfaces, but none is primarily a question router. |

## Surface relationship patterns

Current evidence shows several recurring relationship patterns among surfaces.

### 1. Registry-to-implementation relationship

`diagnostic_inventory` declares public surface shape. `diagnostic_shape_audit`
checks whether implementation specs match that declared shape. This is the
strongest current self-knowledge relationship because it is explicit,
implementation-backed, tested, and auditable.

### 2. Composition relationship

`operational_story` and `ops_brief` aggregate other visibility surfaces instead
of creating new operational facts. This pattern helps workers after they know
they are asking an operational-pressure or triage question. It does not fully
solve natural question routing.

### 3. Derivation / selection / reference relationship

`reasoning_path`, `selection_path`, and `reference_selection` specialize three
explanation families:

```text
derivation: how a conclusion follows
selection: why this item was chosen over alternatives
reference: what comparison point was used
```

This is a strong conceptual cluster, but the cluster is not exposed as a
single navigation domain.

### 4. Producer / consumer / attribution relationship

`consumer_audit`, `emitter_consumer_audit`, `emitter_attribution_audit`,
`operational_graph`, and `observation_utilization` all relate artifacts to use,
emission, attribution, or downstream visibility. They answer adjacent questions
but with different units: predicates, emitted outputs, components, graph nodes,
or implementation paths.

### 5. Preservation-to-navigation relationship

Source navigation evidence repeatedly distinguishes preserved knowledge from
navigable knowledge. Current facts, fact support, and repository observation can
contain answers, while source navigation tries to orient the worker toward the
artifact, relationship, and support chain. This pattern is central to the core
question: answer availability is not the same as surface discoverability.

### 6. Documentation navigation relationship

`docs/README.md` is explicitly a documentation navigation authority. It routes
readers to documents that own answers. That is repository navigation at the
documentation layer, not command routing or executable surface selection.

## Discoverability strengths

1. **Diagnostic surfaces are discoverable as an inventory.** A worker can list
   names, CLI flags, and descriptions for many self-knowledge surfaces.
2. **Diagnostic shape consistency is auditable.** Registry-to-implementation
   agreement is a current repository-visible fact, not just documentation prose.
3. **Several high-value answering surfaces are semantically named.**
   `projection_shape`, `component_audit`, `operational_story`,
   `selection_path`, `reference_selection`, `reasoning_path`, and
   `capability_relationship` communicate their answer family once seen.
4. **Operational composition exists.** `operational_story` and `ops_brief` reduce
   some cross-surface burden by composing existing evidence.
5. **Documentation navigation is explicit.** The docs map already treats
   navigation as a first-class documentation responsibility.
6. **Source navigation is recognized as distinct from source preservation.** The
   repository has already named the failure mode where answers exist but require
   prior knowledge of fact shape.

## Discoverability weaknesses

1. **Question-to-surface routing is mostly implicit.** The repository has
   surface descriptions, but not a reusable surface whose main unit is “worker
   question -> answering surface -> follow-up surface.”
2. **Vocabulary mismatch remains likely.** A worker may ask “what owns this?”
   when the repository distinguishes definition, consumption, source support,
   component role, operational ownership, and authority.
3. **Follow-up guidance is fragmented.** Implementation specs, docs map,
   operational stories, and graph/audit surfaces imply relationships, but no
   current artifact consistently says which surface should follow another for a
   given question.
4. **Domain-level gaps are weaker than predicate/capability gaps.** Observation
   space can be inferred, but the repository does not expose domain coverage as
   first-class self-knowledge.
5. **Surface families use different units.** Some surfaces reason about
   predicates, some components, some emitted outputs, some operational pressure,
   some facts, and some documents. Workers must choose the right unit before
   choosing the right surface.
6. **Navigation vocabulary is partly presentation vocabulary.** Existing
   instructions caution that terms such as source navigation may be presentation
   labels unless implementation evidence supports promotion. This investigation
   therefore treats navigation language as evidence-backed only where files,
   tests, registry entries, or documents support it.

## Are question-to-surface mappings repository-visible?

Partially, yes.

They are repository-visible in these ways:

- CLI flags and descriptions in `diagnostic_inventory` provide an inventory of
  candidate answering surfaces.
- `diagnostic_shape_audit` implementation specs bind many surface names to
  modules, build functions, formatters, JSON functions, flags, and read markers.
- Tests prove several surfaces exist in the inventory and shape audit.
- Documentation map entries route readers to owning documents.
- Prior source-navigation reconciliation names the failure mode where preserved
  knowledge is not enough without navigable orientation.

They are not repository-visible as a complete reusable domain in these ways:

- No reviewed surface uses worker question categories as its primary unit.
- No reviewed surface classifies question-to-surface mappings as well/partial/poor.
- No reviewed executable surface provides follow-up surface guidance as a stable
  contract.
- No reviewed implementation presents “surface relationships” as a general
  self-knowledge graph for question routing.

## Is repository navigation becoming a reusable domain?

Evidence supports a cautious “yes, but not as ontology or a command proposal.”

Supported navigation-like concepts already recur across repository evidence:

- documentation navigation via `docs/README.md`;
- source navigation over preserved source facts;
- knowledge navigation frontier documents;
- inquiry orientation and source-navigation relatedness tests;
- diagnostic inventory and shape-audit registry/spec navigation;
- operational composition surfaces that guide from pressure to related evidence;
- source-navigation reconciliation's explicit distinction between having answers
  and being able to reach them.

What is not supported:

- promoting `navigation`, `question routing`, or `surface relationships` into
  ontology;
- implementing a router or recommender;
- claiming current Seed can reliably translate arbitrary natural questions into
  commands;
- claiming every surface relationship is already represented as durable
  repository knowledge.

## Acceptance answers

### Can Seed currently help workers discover which surface answers a question?

Yes, but unevenly. Seed can help through `diagnostic_inventory`, docs routing,
semantically named surfaces, and composed operational views. It works best when
the worker's vocabulary already resembles a surface name or diagnostic family.
It works poorly when the worker starts from a broad natural question such as
“what owns this?”, “what is missing?”, or “what should I ask next?”

### Where is repository navigation strong?

Repository navigation is strongest for:

- diagnostic surface inventory and registry/implementation shape consistency;
- documentation routing through `docs/README.md`;
- source navigation as a bounded read-only view over preserved source facts;
- operational pressure composition through `operational_story` and `ops_brief`;
- explicit reasoning/selection/reference/capability surfaces once selected.

### Where is repository navigation weak?

Repository navigation is weakest for:

- first-step natural question routing;
- follow-up surface selection;
- cross-surface relationship explanation;
- distinguishing overloaded worker vocabulary such as owner, missing, pressure,
  influence, producer, consumer, role, and authority;
- domain-level observation coverage versus predicate-level and capability-level
  evidence.

### Are question-to-surface mappings becoming repository-visible?

Yes, partially. The evidence is strongest in inventory descriptions,
implementation specs, docs routing, composed operational surfaces, and recurring
investigation language. It is not yet a complete repository-visible model whose
first-class object is a worker question mapped to an answering surface.

### Is navigation itself a missing form of repository self-knowledge?

Likely yes, as an investigation finding. The repository already has many
answering surfaces and several navigation-adjacent artifacts. The repeated gap
is not knowledge acquisition but orientation: helping a worker identify the
question family, the answering surface, related surfaces, and safe follow-up
without already having repository expertise. This conclusion does not imply a
new command, router, assistant, recommendation engine, or ontology change.
