# Documentation Authority Reconciliation

## 1. Purpose and scope

This document is a documentation-only audit of authority and ownership boundaries
across Seed's major architectural documentation surfaces.

It answers one narrow question:

```text
Which document owns which answer?
```

The concern is duplicate authority across navigation documents, status documents,
preservation documents, maps, roadmaps, reconciliations, audits,
characterizations, vocabularies, and canonical architecture documents.

In scope:

- identifying the current authority surfaces readers encounter;
- separating authority from reference, navigation, preservation, and provenance;
- identifying overlaps where multiple documents appear to own the same answer;
- proposing the smallest authority-boundary clarification needed to reduce
  ambiguity.

Out of scope:

- archiving, moving, deleting, renaming, or restructuring documents;
- creating generated documentation, inventories, projections, or automation;
- changing documentation lifecycle definitions;
- modifying production code, tests, runtime behavior, event schemas, projection
  schemas, providers, acquisition logic, policy behavior, or execution behavior;
- redesigning Seed's documentation system.

This document does not make another architecture system authoritative. It audits
where authority already appears to live and where references should replace
restatements.

## 2. Documents inspected

Primary documents inspected:

- `docs/README.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_findings_preservation.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/reasoning_roadmap.md`
- `docs/documentation_lifecycle_reconciliation.md`
- `docs/canonical_documentation_reconciliation.md`
- `docs/documentation_architecture_audit.md`

Additional major authority-adjacent documents inspected or sampled:

- `docs/architecture.md`
- `docs/architecture_principles.md`
- `docs/state.md`
- `docs/invariants.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_representation_map.md`
- `docs/knowledge_representation_reconciliation.md`
- `docs/architectural_findings_characterization.md`
- `docs/architectural_findings_vocabulary.md`
- `docs/architectural_findings_reconciliation.md`
- `docs/roadmap_reconciliation.md`
- `docs/roadmap_and_methodology_reconciliation.md`
- `docs/backlog_and_status_reconciliation.md`
- `docs/durable_lifecycle_reconciliation.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/input_source_authority_reconciliation.md`
- `docs/repository_reconciliation_characterization.md`
- `docs/repository_reconciliation_frontier.md`
- `docs/repository_reconciliation_v1_frontier.md`
- `docs/documentation_observation_characterization.md`
- `docs/documentation_observation_design.md`
- `docs/documentation_observation_frontier.md`
- representative characterization, vocabulary, audit, inventory, and
  reconciliation documents under `docs/` and `docs/audit/`.

## 3. Existing authority surfaces

Seed currently has several documentation surfaces that carry authority-like
language. They are useful, but their authority is not always scoped in the same
way.

| Surface | Current apparent role | Authority it should own |
| --- | --- | --- |
| `docs/README.md` | Repository documentation entry point and recommended reading order. | Navigation authority: where a reader should start and what to read next. |
| `docs/architectural_knowledge_map.md` | Lightweight map of concerns, canonical documents, findings, rejected concepts, status, and frontiers. | Orientation authority only: how major concerns relate and where to find owners. |
| `docs/architecture.md` | Current architecture summary and runtime/knowledge boundary description. | Canonical architecture authority for Seed's present architectural shape, subject to more specific canonical docs. |
| `docs/architecture_principles.md` | Directional statement about what Seed is and is not. | Identity and architectural-direction authority for the short answer to "What is Seed?" |
| `docs/state.md` | State, state views, evidence graph, and confidence semantics. | Canonical state/knowledge-model authority for state semantics. |
| `docs/invariants.md` | Repository invariants. | Canonical invariant authority for accepted runtime and architecture boundaries. |
| `docs/knowledge_acquisition_and_selection.md` | Canonical acquisition/selection relationship. | Canonical authority for the acquisition-to-selection flow. |
| `docs/knowledge_lifecycle_reconciliation.md` | Reconciliation of the knowledge lifecycle. | Canonical/reference authority for lifecycle relationships after reconciliation. |
| `docs/knowledge_maintenance_reconciliation.md` | Integrity terminology and maintenance boundaries. | Canonical/reference authority for Knowledge Integrity semantics. |
| `docs/architectural_findings_preservation.md` | Preservation of completed findings, negative findings, rejected concepts, deferred concepts, and frontier handoff. | Preservation authority: what was learned, rejected, deferred, or preserved from completed audit chains. |
| `docs/architectural_status_and_next_frontier.md` | Current status and active frontier across major concerns. | Status and active-frontier authority. |
| `docs/reasoning_roadmap.md` | Historical roadmap, concern evolution, and future work. | Roadmap authority: sequencing, backlog context, and historical evolution of planned work. |
| `docs/documentation_lifecycle_reconciliation.md` | Documentation lifecycle roles, archival/supersession vocabulary, and duplicate-authority problem framing. | Lifecycle-role authority, not per-topic content authority. |
| `docs/canonical_documentation_reconciliation.md` | Prior canonical/generated/roadmap/status/historical/archive-candidate reconciliation. | Reconciliation provenance for canonical-documentation classification; should not out-rank the lifecycle reconciliation after adoption. |
| Recent `*_reconciliation.md` documents | Boundary-specific decision records. | Decision-provenance authority for the scoped question they reconcile. |
| `*_vocabulary.md` documents | Term definitions for a bounded concern. | Vocabulary authority for their own term family. |
| `*_characterization.md`, `*_audit.md`, and `*_inventory.md` documents | Evidence collection and observed behavior/structure. | Characterization or audit authority for what was observed in that scope, not current global status. |
| Generated architecture files under `docs/generated/` | Machine-readable or rendered outputs. | Generated-reference authority only for the generation scope; not ownership authority for human architectural answers. |

## 4. Authority overlaps

The strongest duplicate-authority risk is not that documents disagree. The risk
is that several documents answer the same reader question without clearly saying
which answer is primary.

### 4.1 Navigation overlaps

`docs/README.md`, `docs/architectural_knowledge_map.md`, and parts of
`docs/reasoning_roadmap.md` all tell readers where to go next. The clean boundary
is:

```text
README routes.
Architectural Knowledge Map orients.
Roadmap sequences future work.
```

The map may include reading order as a convenience, but the README should own the
entry-point answer to "What should I read next?"

### 4.2 Status and frontier overlaps

`docs/README.md`, `docs/architectural_knowledge_map.md`,
`docs/architectural_findings_preservation.md`, `docs/reasoning_roadmap.md`, and
`docs/architectural_status_and_next_frontier.md` all contain current-state or
frontier language.

The clean boundary is:

```text
Architectural Status And Next Frontier owns current status and active frontier.
Other documents may summarize status only as a pointer to that document.
```

### 4.3 Rejected concept overlaps

`docs/README.md`, `docs/architectural_knowledge_map.md`,
`docs/architectural_findings_preservation.md`, and several scoped
reconciliations list rejected concepts or negative findings.

The clean boundary is:

```text
Scoped reconciliations own why a scoped option was rejected.
Architectural Findings Preservation owns the discoverable cross-document list.
README and map should reference or briefly summarize, not become rejection logs.
```

### 4.4 Canonical-document overlaps

`docs/architectural_knowledge_map.md`,
`docs/documentation_lifecycle_reconciliation.md`, and
`docs/canonical_documentation_reconciliation.md` all discuss canonical documents.

The clean boundary is:

```text
Documentation Lifecycle Reconciliation owns lifecycle roles.
Canonical Documentation Reconciliation preserves the prior classification pass.
Architectural Knowledge Map lists canonical destinations for navigation only.
Canonical architecture documents own their own architectural claims.
```

### 4.5 Roadmap and backlog overlaps

`docs/reasoning_roadmap.md`, `docs/roadmap_reconciliation.md`,
`docs/roadmap_and_methodology_reconciliation.md`,
`docs/backlog_and_status_reconciliation.md`, and status/frontier documents all
contain future-work language.

The clean boundary is:

```text
Reasoning Roadmap owns roadmap context and future sequencing.
Status And Next Frontier owns the current active frontier.
Roadmap reconciliations own provenance for why roadmap items were promoted,
paused, or reframed.
```

### 4.6 Vocabulary overlaps

Vocabulary documents, reconciliation documents, maps, and status documents all
use and sometimes define terms such as canonical, active, frontier, historical,
preservation, finding, status, and authority.

The clean boundary is:

```text
The vocabulary or lifecycle document that scopes a term owns the definition.
Other documents should use the term and link to the owner instead of redefining
it.
```

## 5. Ownership analysis

### `docs/README.md`

Primary responsibility:

- Entry-point navigation.
- Recommended reading order.
- High-level concern routing.

Questions it owns:

- "What should I read next?"
- "Where do I start?"
- "Which major document family should I open for a concern?"

Questions it may reference:

- "What is Seed?"
- "What is current?"
- "What was rejected?"
- "What was learned?"
- "What is canonical?"

Questions it should not own:

- Detailed canonical architecture.
- Current status or active frontier details.
- Rejected-concept rationale.
- Preservation of completed findings.
- Lifecycle-state definitions.

### `docs/architectural_knowledge_map.md`

Primary responsibility:

- Orientation across architectural concerns.
- Cross-document map of where major knowledge lives.
- Lightweight reduction of rediscovery cost.

Questions it owns:

- "How are the major documentation concerns connected?"
- "Which document family should I consult for a concern?"
- "Where is the canonical owner for this topic?"

Questions it may reference:

- "What is current?"
- "What is canonical?"
- "What was rejected?"
- "What is the active frontier?"
- "What should I read next?"

Questions it should not own:

- Canonical architecture truth.
- Active status.
- Preservation history.
- Roadmap sequencing.
- Rejection rationale.

The map already says it is not a source of truth. Its highest-value role is to
keep that promise consistently.

### `docs/architecture_principles.md`

Primary responsibility:

- Seed identity and directional principles.
- Boundaries on what Seed is and is not.

Questions it owns:

- "What is Seed?" at the architectural identity level.
- "What is Seed not?"
- "What direction should architectural choices preserve?"

Questions it may reference:

- Detailed runtime architecture.
- State semantics.
- Roadmap and current status.

Questions it should not own:

- Current frontier.
- Preservation history.
- Per-concern vocabulary.
- Detailed implementation ownership.

### `docs/architecture.md`

Primary responsibility:

- Current canonical architecture summary.
- Runtime, state, projection, evidence, confidence, and knowledge-flow boundary
  summary.

Questions it owns:

- "What is canonical?" for the broad present architecture, subject to scoped
  canonical documents.
- "Which major runtime and knowledge components own which boundary?"

Questions it may reference:

- More specific state, invariant, lifecycle, acquisition, and maintenance
  authorities.
- Roadmap or status documents for what is not yet built.

Questions it should not own:

- Reader navigation.
- Historical roadmap evolution.
- Audit preservation.
- Rejected solution catalogs outside architectural non-goals.

### `docs/state.md`

Primary responsibility:

- State, state-view, evidence-graph, confidence, and projection semantics.

Questions it owns:

- "What is canonical?" for state semantics.
- "What is current state versus historical event truth?"
- "How do evidence, facts, support, contradictions, and confidence relate?"

Questions it may reference:

- Architecture summary.
- Knowledge acquisition/selection flow.
- Integrity reconciliation.

Questions it should not own:

- Documentation lifecycle.
- Roadmap status.
- Cross-document navigation.

### `docs/invariants.md`

Primary responsibility:

- Accepted repository and architecture invariants.

Questions it owns:

- "What boundaries must not drift?"
- "Which runtime and architecture constraints are accepted invariants?"

Questions it may reference:

- Architecture summary.
- Runtime ownership audits.
- Historical quarantine records.

Questions it should not own:

- Current roadmap.
- Reader navigation.
- Preservation lists.

### `docs/architectural_findings_preservation.md`

Primary responsibility:

- Preservation of learned findings across completed audit chains.
- Negative findings and rejected concepts.
- Deferred concepts and handoff context.

Questions it owns:

- "What was learned?"
- "What was rejected?" at the discoverable cross-document level.
- "What was deferred or paused?"
- "What historical findings must not be lost?"

Questions it may reference:

- Current status.
- Roadmap sequencing.
- Specific reconciliation rationale.
- Canonical architecture documents where findings were promoted.

Questions it should not own:

- Current active frontier as the primary authority.
- Reader entry-point navigation.
- Canonical architecture definitions.
- Roadmap sequencing.

### `docs/architectural_status_and_next_frontier.md`

Primary responsibility:

- Current repository architectural status.
- Completed audit-chain status.
- Active frontier and next capability-growth priorities.

Questions it owns:

- "What is current?"
- "What is the active frontier?"
- "Which major concern is stable, paused, complete, or active?"

Questions it may reference:

- Preservation of completed findings.
- Roadmap context.
- Canonical architecture documents.
- Navigation surfaces.

Questions it should not own:

- Historical preservation.
- Rejected-concept rationale beyond status impact.
- Documentation lifecycle definitions.
- General reading order.

### `docs/reasoning_roadmap.md`

Primary responsibility:

- Roadmap authority for reasoning-system evolution.
- Backlog context.
- Historical concern evolution.
- Future-work sequencing.

Questions it owns:

- "What might be worked on next after the active frontier?"
- "How did roadmap concerns evolve?"
- "Which future work is deferred, paused, or sequenced?"

Questions it may reference:

- Current active frontier.
- Current status.
- Preservation findings.
- Reconciliation decisions.

Questions it should not own:

- Current status as a primary board.
- Canonical architecture definitions.
- Rejection rationale already owned by scoped reconciliation or preservation.
- Reader entry-point navigation.

### `docs/documentation_lifecycle_reconciliation.md`

Primary responsibility:

- Lifecycle-role authority for documentation roles such as canonical, active,
  reference, historical, superseded, and archived.
- Duplicate-authority problem framing.
- Metadata and supersession guidance.

Questions it owns:

- "What is historical?" as a lifecycle-state definition.
- "What does canonical mean as a documentation lifecycle role?"
- "How should active, reference, historical, superseded, and archived documents
  be distinguished?"

Questions it may reference:

- Specific canonical documents.
- Status documents.
- Preservation documents.
- Prior canonical-documentation reconciliation.

Questions it should not own:

- The current status of each architectural concern.
- The substantive architecture of Seed.
- Detailed per-topic vocabulary outside lifecycle terms.

### `docs/canonical_documentation_reconciliation.md`

Primary responsibility:

- Provenance for a prior canonical/generated/roadmap/status/historical/archive
  classification pass.

Questions it owns:

- "Why did a prior pass classify documentation categories this way?"
- "Which canonical-documentation options were considered in that pass?"

Questions it may reference:

- Documentation lifecycle reconciliation.
- Architectural knowledge map.
- Specific canonical documents.

Questions it should not own:

- The current definition of lifecycle roles if superseded by the lifecycle
  reconciliation.
- The current owner of every architectural answer.
- Reader navigation.

### Recent `*_reconciliation.md` documents

Primary responsibility:

- Decision provenance for a scoped question.
- Boundary clarification after an audit or characterization chain.
- Explicit non-goals and rejected alternatives for that scope.

Questions they own:

- "Why was this scoped decision made?"
- "What alternatives were rejected for this scoped concern?"
- "What boundary did this reconciliation establish?"

Questions they may reference:

- Canonical architecture documents.
- Vocabulary documents.
- Status/frontier documents.
- Preservation documents after findings are promoted.

Questions they should not own:

- Global navigation.
- Global current status.
- Cross-document preservation lists.
- Broad canonical architecture outside their scope.

### `*_vocabulary.md` documents

Primary responsibility:

- Vocabulary authority for their bounded term family.

Questions they own:

- "What does this term mean in this concern?"
- "Which terms should be used or avoided here?"

Questions they may reference:

- Characterization and reconciliation documents that justify the vocabulary.

Questions they should not own:

- Current status.
- Roadmap sequencing.
- Canonical architecture beyond term definitions.

### `*_characterization.md`, `*_audit.md`, and `*_inventory.md` documents

Primary responsibility:

- Observed evidence, inventory, and characterization of a scoped concern.

Questions they own:

- "What was observed during this audit?"
- "What inventory existed at the time of inspection?"
- "What behavior or structure was characterized?"

Questions they may reference:

- Reconciliation documents that interpret the observations.
- Canonical documents that preserve promoted conclusions.

Questions they should not own:

- Current status after later reconciliation.
- Global roadmap.
- Canonical architecture unless explicitly promoted and still current.

## 6. Proposed authority boundaries

The smallest useful authority model is:

```text
Navigation authority: docs/README.md
Orientation/map authority: docs/architectural_knowledge_map.md
Identity/direction authority: docs/architecture_principles.md
Canonical architecture authority: docs/architecture.md plus scoped canonical docs
State/knowledge semantics authority: docs/state.md and scoped lifecycle docs
Invariant authority: docs/invariants.md
Status/frontier authority: docs/architectural_status_and_next_frontier.md
Preservation authority: docs/architectural_findings_preservation.md
Roadmap authority: docs/reasoning_roadmap.md
Lifecycle-role authority: docs/documentation_lifecycle_reconciliation.md
Decision-provenance authority: scoped *_reconciliation.md documents
Vocabulary authority: scoped *_vocabulary.md documents
Characterization authority: scoped *_characterization.md, *_audit.md, and *_inventory.md documents
Generated-reference authority: docs/generated/* within generation scope only
```

This model does not create new categories. It assigns an owner role to document
families that already exist.

## 7. Reference-vs-authority guidance

A document is acting as an authority when it answers a question directly and a
reader could reasonably treat that answer as current, canonical, or final.

A document is acting as a reference when it names the owner and provides only
minimal context needed to route the reader.

Use these rules:

1. If a document is a map, it should route to authorities instead of restating
   their conclusions in detail.
2. If a document is a status surface, it may summarize completed work but should
   route to preservation for durable findings and to roadmap for future
   sequencing.
3. If a document is a preservation surface, it may mention current frontier as
   handoff context but should route to status for currentness.
4. If a document is a roadmap, it may mention current status as an input but
   should route to the status/frontier document for the current board.
5. If a document is a reconciliation, it should own the rationale for its scoped
   decision, not become a global map or status document.
6. If a document is a vocabulary, it should define terms for its scope, not make
   architecture-wide status decisions.
7. If a document is a characterization or audit, it should preserve observations,
   not supersede later reconciliations or canonical documents.
8. If a document is generated, it should not become human architectural
   governance or ownership authority.

## 8. Remaining ambiguities

Remaining ambiguity is concentrated in four places:

1. **The phrase "canonical documents" appears in navigation and lifecycle
   surfaces.** The map needs the phrase to route readers, but the lifecycle
   reconciliation owns what canonical means as a role, and the scoped canonical
   documents own their content.
2. **Current/frontier language appears in maps, preservation, and roadmap
   documents.** Status/frontier should own currentness; other documents should
   treat frontier language as a reference or historical handoff.
3. **Rejected concepts appear in multiple summaries.** Preservation should own
   the consolidated list; scoped reconciliations should own the rationale; maps
   and README should avoid becoming rejection authorities.
4. **Roadmap documents also contain status history.** The roadmap should own
   sequencing and evolution, while status/frontier owns the current board.

These ambiguities do not require a new documentation system. They require clearer
"owns versus references" wording in the existing high-traffic documents.

## 9. Non-goals

This reconciliation does not propose:

- archiving documents;
- deleting historical records;
- moving files;
- creating a documentation registry;
- creating generated documentation as the solution;
- adding projections or automation;
- changing lifecycle definitions;
- replacing existing maps, roadmaps, preservation documents, or status boards;
- changing production code, tests, runtime behavior, schemas, providers,
  acquisition logic, projections, or policy behavior.

## 10. Rejected solutions

Rejected solution: make `docs/architectural_knowledge_map.md` the global source
of truth.

Reason rejected: the map already declares that it is not a source of truth. Making
it authoritative would centralize too many answers and recreate the duplicate
authority problem in a single document.

Rejected solution: make `docs/README.md` answer every top-level question.

Reason rejected: the README should route readers. If it owns status, roadmap,
preservation, canonicality, and rejected concepts, it becomes a second map,
second status page, and second preservation surface.

Rejected solution: make `docs/architectural_findings_preservation.md` the status
board.

Reason rejected: preservation and currentness are different questions. A
preservation surface can keep findings discoverable without owning whether a
frontier is active today.

Rejected solution: make `docs/reasoning_roadmap.md` the status authority.

Reason rejected: roadmap sequencing and current status overlap but are not the
same. A roadmap can explain future work and historical evolution without owning
the current status board.

Rejected solution: solve authority with generated documentation, inventories,
projections, or automation.

Reason rejected: the present problem is semantic ownership, not document volume
or lack of extraction. Automation could reproduce duplicate authority unless the
human authority boundaries are clear first.

Rejected solution: create a new documentation category for every question.

Reason rejected: the existing document families are sufficient. The smallest
safe change is boundary clarification, not more categories.

## 11. Direct answer

### Which document should answer which question?

| Reader question | Primary authority | Secondary reference/provenance |
| --- | --- | --- |
| 1. What is Seed? | `docs/architecture_principles.md` for identity and direction; `docs/architecture.md` for current architecture summary. | `docs/README.md` and `docs/architectural_knowledge_map.md` may route to these. |
| 2. What is canonical? | `docs/documentation_lifecycle_reconciliation.md` for canonical as a lifecycle role; `docs/architecture.md`, `docs/state.md`, `docs/invariants.md`, and scoped canonical docs for canonical content. | `docs/architectural_knowledge_map.md` may list destinations; `docs/canonical_documentation_reconciliation.md` preserves prior classification provenance. |
| 3. What is current? | `docs/architectural_status_and_next_frontier.md`. | `docs/README.md`, `docs/architectural_knowledge_map.md`, `docs/reasoning_roadmap.md`, and preservation docs should reference it. |
| 4. What was rejected? | `docs/architectural_findings_preservation.md` for consolidated discovery; scoped `*_reconciliation.md` documents for rationale. | `docs/README.md` and the map may provide short pointers only. |
| 5. What was learned? | `docs/architectural_findings_preservation.md`. | Scoped characterization, audit, vocabulary, and reconciliation chains provide evidence and detail. |
| 6. What is the active frontier? | `docs/architectural_status_and_next_frontier.md`. | `docs/reasoning_roadmap.md` may explain future sequencing; preservation may mention handoff context. |
| 7. Why was a decision made? | The scoped `*_reconciliation.md` document for that decision. | The preceding audit/characterization/inventory and following canonical or preservation documents. |
| 8. What is historical? | `docs/documentation_lifecycle_reconciliation.md` for the lifecycle meaning of historical; scoped historical/audit/reconciliation documents for historical evidence. | `docs/architectural_findings_preservation.md` for preserved historical findings. |
| 9. What should I read next? | `docs/README.md`. | `docs/architectural_knowledge_map.md` can orient once the reader has entered the documentation set. |

### Which documents currently have duplicate authority?

The documents most visibly overlapping in authority are:

- `docs/README.md` and `docs/architectural_knowledge_map.md` for reading order
  and navigation.
- `docs/architectural_knowledge_map.md`,
  `docs/architectural_status_and_next_frontier.md`,
  `docs/architectural_findings_preservation.md`, and
  `docs/reasoning_roadmap.md` for current/frontier language.
- `docs/README.md`, `docs/architectural_knowledge_map.md`,
  `docs/architectural_findings_preservation.md`, and scoped
  `*_reconciliation.md` documents for rejected concepts.
- `docs/architectural_knowledge_map.md`,
  `docs/documentation_lifecycle_reconciliation.md`, and
  `docs/canonical_documentation_reconciliation.md` for canonical-document
  classification language.
- `docs/reasoning_roadmap.md`, `docs/roadmap_reconciliation.md`,
  `docs/roadmap_and_methodology_reconciliation.md`,
  `docs/backlog_and_status_reconciliation.md`, and
  `docs/architectural_status_and_next_frontier.md` for roadmap/status/backlog
  boundaries.

### Which documents are redefining questions already owned elsewhere?

- `docs/README.md` risks redefining current status, rejected concepts, and
  concern findings already owned by status, preservation, and scoped
  reconciliation documents.
- `docs/architectural_knowledge_map.md` risks redefining canonicality, status,
  frontier, rejection, and reading-order questions already owned elsewhere.
- `docs/architectural_findings_preservation.md` risks redefining active frontier
  if handoff language is read as current status rather than preserved context.
- `docs/reasoning_roadmap.md` risks redefining current status if roadmap history
  is read as the current board.
- `docs/canonical_documentation_reconciliation.md` risks redefining lifecycle
  role language if treated as newer or stronger than the lifecycle
  reconciliation.

### Which documents should reference another authority rather than restating it?

- `docs/README.md` should reference status, preservation, roadmap, map, and
  canonical architecture owners rather than restating their substantive answers.
- `docs/architectural_knowledge_map.md` should reference canonical, status,
  preservation, roadmap, lifecycle, vocabulary, and reconciliation authorities
  rather than restating their decisions in detail.
- `docs/architectural_findings_preservation.md` should reference
  `docs/architectural_status_and_next_frontier.md` for current status and
  `docs/reasoning_roadmap.md` for future sequencing.
- `docs/architectural_status_and_next_frontier.md` should reference
  preservation for completed findings and roadmap for future sequencing beyond
  the active frontier.
- `docs/reasoning_roadmap.md` should reference status/frontier for currentness
  and preservation/reconciliations for settled or rejected findings.
- `docs/canonical_documentation_reconciliation.md` should reference
  `docs/documentation_lifecycle_reconciliation.md` for current lifecycle-role
  language if the lifecycle reconciliation is the adopted role authority.

### Are any documents attempting to act as map, status, preservation, roadmap, and authority simultaneously?

Yes. The strongest candidate is `docs/architectural_knowledge_map.md`, because it
contains map/orientation material, status overview, canonical-document pointers,
findings, rejected concepts, current frontiers, and reading-order guidance.
That breadth is useful for orientation, but it should remain reference-only.

`docs/README.md` is a smaller candidate because it routes readers but also
summarizes concerns, frontiers, rejected concepts, and recurring lessons. Its
safe role is navigation authority, not content authority.

`docs/reasoning_roadmap.md` also carries roadmap, history, status, and future
frontier language. Its safe role is roadmap authority; current status should stay
with `docs/architectural_status_and_next_frontier.md`.

### What is the smallest change needed to reduce documentation ambiguity?

The smallest change is to add or tighten explicit authority disclaimers in the
high-traffic documents, without moving or archiving anything:

1. `docs/README.md`: state that it owns navigation only.
2. `docs/architectural_knowledge_map.md`: keep and strengthen its existing
   "not a source of truth" boundary by naming the documents that own status,
   preservation, roadmap, lifecycle, vocabulary, and canonical content.
3. `docs/architectural_status_and_next_frontier.md`: state that it owns current
   status and active frontier.
4. `docs/architectural_findings_preservation.md`: state that it owns preserved
   findings, learned lessons, rejected concepts, and deferred concepts, but not
   current status.
5. `docs/reasoning_roadmap.md`: state that it owns roadmap sequencing and
   historical evolution, but not the current status board.
6. `docs/documentation_lifecycle_reconciliation.md`: state that it owns lifecycle
   role definitions, not per-topic architectural content.

This is a boundary-clarification change, not a documentation-system redesign.
