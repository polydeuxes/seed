# Executive Summary

Architectural Findings Vocabulary v1 defines the canonical language Seed uses
when discussing documentation-preserved architectural conclusions, boundaries,
statuses, recommendations, rejections, deferrals, lessons, non-goals, and open
questions.

In Seed, **an Architectural Finding is a documentation-preserved architectural
conclusion, boundary, status, recommendation, rejection, deferral, open question,
or lesson that affects how Seed should be understood, extended, maintained, or
intentionally not extended**.

Architectural Findings are already partially present across Seed's documentation.
They appear in characterizations, vocabularies, reconciliations, summaries,
roadmaps, backlog reviews, status reviews, handoffs, executive summaries,
conclusions, future-work sections, promotion tables, archive tables,
stale/quarantine notices, and non-goal sections. The gap this vocabulary addresses
is shared language, not missing runtime behavior.

This document is vocabulary only. It does not implement an Architectural Findings
Index, authority tracker, supersession tracker, inventory, read model, route,
adapter, schema class, database, engine, Runtime behavior, ToolExecutor behavior,
provider behavior, projection mutation, or event append.

# Purpose

The purpose of this document is to define stable vocabulary for Seed's
Architectural Findings concern.

It serves the same role for Architectural Findings that existing vocabulary
documents serve for their concerns:

- `docs/explanation_contract_vocabulary.md` for explainability;
- `docs/context_composition_vocabulary.md` for context composition;
- `docs/selection_rationale_vocabulary.md` for selection rationale;
- `docs/response_vocabulary.md` for response;
- `docs/capability_verification_vocabulary.md` for capability verification;
- `docs/knowledge_classification_vocabulary.md` for knowledge classification.

The vocabulary is intended to:

- name existing finding-preserving surfaces consistently;
- distinguish findings from runtime behavior, truth arbitration, execution,
  provider calls, projection mutation, and event appends;
- preserve the repeated lesson that architectural memory already exists in
  distributed documentation;
- describe categories, statuses, scopes, authority concepts, supersession
  concepts, consequences, recommendations, relationships, metadata, and
  extensions as documentation language;
- support future documentation-only reconciliation without creating a new owner
  for architecture, truth, workflow, routing, or execution.

This is not an implementation plan, schema contract, runtime contract, API
contract, persistence model, index design, or route design.

# What Is An Architectural Finding

**An Architectural Finding is a documentation-preserved architectural conclusion,
boundary, status, recommendation, rejection, deferral, open question, or lesson
that affects how Seed should be understood, extended, maintained, or
intentionally not extended.**

Architectural Findings may describe:

- conclusions reached by audits, characterizations, reconciliations, summaries,
  or status reviews;
- recommendations for documentation maintenance, roadmap ordering, backlog
  cleanup, promotion, archival, or future work;
- boundaries around ownership, runtime behavior, execution, provider calls,
  projections, event append, mutation, truth arbitration, or response ownership;
- accepted architecture, accepted vocabulary, and accepted composition language;
- rejected concepts, especially repeated engine, runtime-integration,
  ToolExecutor-integration, universal-formatter, and parallel-system proposals;
- deferred concepts waiting for concrete operator questions, evidence, or higher
  priority roadmap work;
- open questions that remain answerable only through future documentation,
  characterization, reconciliation, or evidence-supported acquisition work;
- lessons learned from repeated audit patterns;
- status updates about active, resolved, historical, stale, quarantined,
  archived, or frontier work.

Architectural Findings do **not**:

- execute behavior;
- mutate state;
- mutate projections;
- append events;
- call providers;
- verify capabilities;
- refresh facts;
- determine truth;
- select current beliefs;
- resolve contradictions;
- perform runtime routing;
- own `Runtime`, `ToolExecutor`, `EventLedger`, or `ProjectionStore`;
- create a parallel truth, response, explanation, integrity, context, selection,
  caveat, workflow, or planning system.

This definition intentionally includes more than formal decisions. Seed's current
architectural memory is preserved through distributed documentation rather than a
single decision-log format.

# Canonical Vocabulary

## Architectural Finding

An **Architectural Finding** is a documentation-preserved architectural
conclusion, boundary, status, recommendation, rejection, deferral, open question,
or lesson that affects how Seed should be understood, extended, maintained, or
intentionally not extended.

A finding is an interpretive unit inside architectural memory. It may be recorded
in prose, a table, an executive summary, a conclusion, a non-goal list, a roadmap
entry, a promotion table, an archive table, or a stale/quarantine notice.

A finding is not a runtime artifact, execution hook, provider action, projection
mutation, event, database row, schema class, route, adapter, or engine.

## Finding Category

A **Finding Category** is the kind of architectural meaning a finding preserves.
Canonical categories include Accepted Finding, Rejected Concept, Deferred
Concept, Open Question, Current Frontier, Architectural Lesson, Non-Goal, Status
Update, and Historical Finding.

Categories answer: "What kind of finding is this?"

## Finding Status

A **Finding Status** is the current lifecycle interpretation of a finding as
documentation. Canonical statuses include Active, Resolved, Deferred,
Superseded, Historical, and Unknown.

Status answers: "How should this finding be interpreted now?"

## Accepted Finding

An **Accepted Finding** is a finding that current documentation treats as part of
Seed's architectural understanding.

Examples include distributed ownership, documentation-first vocabulary, read-only
projection-backed characterization, response as communication rather than truth
creation, and repeated rejection of unjustified generic engines.

Accepted does not mean implemented in a new component. Many accepted findings are
boundaries, vocabulary, or documentation conclusions.

## Rejected Concept

A **Rejected Concept** is a proposal, framing, or implementation direction that
repository evidence says should not be pursued under current conditions.

Common rejected concepts include `ExplainabilityEngine`, `IntegrityEngine`,
`SelectionEngine`, `ResponseEngine`, `ContextEngine`, `ReasoningEngine`,
`Planner`, `WorkflowEngine`, universal formatters, runtime integration as a
default solution, ToolExecutor integration as a default solution, and parallel
truth or response systems.

Rejected concepts remain useful findings because they prevent repeated
rediscovery and scope creep.

## Deferred Concept

A **Deferred Concept** is a concept that is not accepted for immediate work, but
is not permanently rejected.

Deferred concepts usually require a concrete operator question, stronger
evidence, a clearer owner, higher roadmap priority, or completion of a safer
vocabulary/reconciliation step before additional work is justified.

## Open Question

An **Open Question** is an unresolved architectural question preserved for later
review.

Open questions may ask which findings are active, authoritative, superseding,
repository-wide, locally scoped, or tied to backlog consequences. An open
question should not be treated as a route, schema, engine, or runtime task by
default.

## Current Frontier

A **Current Frontier** is the documentation-preserved next area of meaningful
architectural or roadmap attention.

Current frontier language appears in roadmap work, status reviews, future-work
sections, and architectural-status documents. A frontier is a prioritization
signal, not a workflow engine or planning authority.

## Architectural Lesson

An **Architectural Lesson** is a durable lesson drawn from repeated repository
findings.

Examples include:

- behavior often already exists;
- vocabulary is often missing;
- composition is often missing;
- ownership is often distributed;
- many proposed engines are not justified;
- documentation-only analysis is often the smallest safe first step.

## Non-Goal

A **Non-Goal** is an explicitly excluded behavior, owner, implementation path,
or scope.

Non-goals protect architectural boundaries. They commonly exclude Runtime
changes, ToolExecutor changes, EventLedger ownership changes, ProjectionStore
ownership changes, inventories, read models, routes, adapters, databases, schema
classes, engines, provider behavior, projection mutation, event append, and
parallel truth or response systems.

## Status Update

A **Status Update** is a finding that records progress, completion, partial
presence, active roadmap work, archival readiness, stale/quarantine status, or
frontier state.

Status updates preserve architectural memory but may become historical if later
documents supersede them.

## Finding Surface

A **Finding Surface** is a concrete documentation surface where findings appear.

Existing surfaces include characterizations, vocabularies, reconciliations,
summaries, roadmaps, backlog reviews, status reviews, handoffs, executive
summaries, conclusions, future-work sections, promotion tables, archive tables,
stale/quarantine notices, non-goal sections, and architecture documents.

A surface preserves findings. It does not automatically make a finding
repository-wide or authoritative.

## Finding Preservation

**Finding Preservation** is the act of keeping a finding available for future
readers through documentation.

Preservation mechanisms include executive summaries, conclusions, scope sections,
non-goals, files-inspected sections, handoff recommendations, roadmap entries,
future-work sections, promotion tables, archive tables, and stale/quarantine
notices.

Preservation is not execution, routing, indexing, mutation, or event append.

## Finding Authority

**Finding Authority** is the documentation concept that one finding or surface may
be more current, canonical, or controlling than another when they discuss the
same architectural concern.

This vocabulary defines the term only. It does not implement authority tracking,
a ranking system, a registry, an index, or a database.

## Finding Scope

**Finding Scope** is the breadth of architecture affected by a finding.

Scope may be repository-wide, local to a concern, local to a document family,
historical, or unknown. Scope is documentation language and does not create an
automated enforcement mechanism.

## Finding Consequence

A **Finding Consequence** is the documented effect a finding has on future
understanding, maintenance, backlog cleanup, roadmap ordering, archival,
promotion, or non-goal enforcement.

Consequences may include adding vocabulary, updating a roadmap, deferring work,
removing duplicate backlog items, preserving a rejection, promoting knowledge to
a canonical document, or leaving behavior unchanged.

## Finding Recommendation

A **Finding Recommendation** is documented guidance derived from a finding.

Recommendations may suggest documentation maintenance, reconciliation,
promotion, archival, future characterization, or backlog cleanup. A
recommendation is not implementation authority by itself.

## Finding Relationship

A **Finding Relationship** is a documented connection between findings or between
a finding and a surface.

Relationships may include supports, refines, repeats, conflicts with, supersedes,
is superseded by, depends on, motivates, constrains, defers, rejects, promotes,
or archives.

This vocabulary defines relationship language only; it does not implement a
relationship graph.

## Supersession

**Supersession** is the documentation concept that a current finding replaces,
updates, narrows, or invalidates an earlier finding for current architectural
interpretation.

Supersession may be explicit through stale/quarantine notices, archive tables, or
promotion guidance, or implicit when later canonical vocabulary/reconciliation
updates older audit language. This vocabulary does not implement supersession
tracking.

## Repository-Wide Finding

A **Repository-Wide Finding** is a finding that applies broadly across Seed,
rather than only to one feature, audit chain, or document family.

Examples include no new generic engines without justified need, no Runtime or
ToolExecutor ownership by default, no parallel truth systems, and preservation of
distributed ownership.

## Local Finding

A **Local Finding** is a finding whose scope is limited to a concern, document
family, component, roadmap slice, audit chain, or vocabulary.

Local findings may still be important, but they should not be generalized across
the repository unless later documentation promotes them.

## Historical Finding

A **Historical Finding** is a preserved finding that remains useful as background,
audit trail, or rejected-path memory, but should not be treated as the current
authority unless a current surface reaffirms it.

Historical findings often appear in stale/quarantined documents, archive
candidates, old audit details, or promoted source documents whose unique content
has moved to canonical owners.

## Active Finding

An **Active Finding** is a finding that current documentation still treats as
applicable.

Active findings may be accepted decisions, current boundaries, active non-goals,
current frontiers, unresolved open questions, or current backlog/status guidance.

## Resolved Finding

A **Resolved Finding** is a finding whose question, recommendation, or work item
has been completed, promoted, rejected, or closed by later documentation.

Resolved findings may remain preserved for history, but should not continue to
create backlog pressure.

## Finding Metadata

**Finding Metadata** is descriptive documentation attached to a finding.

Useful metadata may include category, status, scope, surface, source document,
related documents, recommendation, consequence, owner-by-document, evidence,
relationship notes, date-like context when present, and extension notes.

Metadata is vocabulary only here; this document does not define a schema.

## Finding Extension

A **Finding Extension** is a documentation-only refinement, category, status, or
relationship added later when existing vocabulary is insufficient.

Extensions should preserve local ownership, avoid runtime behavior, and avoid
creating schema or engine obligations by default.

# Finding Categories

## Accepted Finding

An Accepted Finding records architecture that Seed currently treats as valid.
Accepted findings may be conclusions, boundaries, vocabulary terms,
composition-language decisions, ownership statements, or negative findings.

Accepted findings differ from status updates because they describe architectural
meaning, not merely progress. They differ from recommendations because they are
already part of current understanding.

## Rejected Concept

A Rejected Concept records a proposed concept or implementation path that should
not be pursued under current evidence.

Rejected concepts differ from non-goals because a rejection usually responds to a
specific proposed direction, while a non-goal may define broader scope. Rejected
concepts differ from deferred concepts because rejection says "not justified" or
"do not do this," while deferral says "not now unless conditions change."

## Deferred Concept

A Deferred Concept records work or language that may be worth revisiting later,
but is not currently justified.

Deferred concepts differ from open questions because a deferred concept has a
candidate direction waiting for conditions, while an open question asks what is
true or needed.

## Open Question

An Open Question records unresolved architectural uncertainty.

Open questions differ from deferred concepts because they do not necessarily
contain a candidate solution. They differ from current frontiers because they may
not be the next prioritized area of attention.

## Current Frontier

A Current Frontier records the current or next meaningful architectural/roadmap
area.

Current frontiers differ from open questions because they imply priority or
near-term attention. They differ from recommendations because they identify an
area, not necessarily a specific action.

## Architectural Lesson

An Architectural Lesson records a repeated generalizable learning.

Lessons differ from accepted findings because they are pattern-level guidance.
They often constrain future proposals across multiple concerns.

## Non-Goal

A Non-Goal records what a document, concern, or repository direction explicitly
does not do.

Non-goals differ from rejected concepts because they define scope even when no
specific proposal is being rejected. They are frequently repository-wide guardrails.

## Status Update

A Status Update records progress, completion, partial presence, stale state,
archive readiness, active frontier state, or current backlog state.

Status updates differ from accepted findings because they may become outdated
quickly. They need current context to interpret safely.

## Historical Finding

A Historical Finding records architectural memory that remains useful but is not
necessarily current authority.

Historical findings differ from superseded findings because a historical finding
may simply be old or background, while a superseded finding has been replaced or
narrowed by a newer current finding.

# Finding Status Vocabulary

## Active

**Active** means current documentation treats the finding as applicable now.

Active findings can be accepted findings, active non-goals, current frontiers,
current open questions, or current backlog/status guidance.

## Resolved

**Resolved** means the finding's question, recommendation, or work item has been
completed, promoted, rejected, removed, or otherwise closed by later
documentation.

Resolved findings should not keep generating duplicate backlog work.

## Deferred

**Deferred** means the finding is intentionally not current work, but may be
reconsidered if concrete conditions change.

Deferred status should preserve the reason for deferral when known.

## Superseded

**Superseded** means a newer finding or surface has replaced, narrowed, or
corrected the older finding for current interpretation.

Superseded findings may still be preserved for audit trail and historical
context.

## Historical

**Historical** means the finding remains useful as background or architectural
memory, but should not be assumed to be current authority without a current
surface reaffirming it.

Historical is weaker than superseded: it does not necessarily identify a specific
replacement.

## Unknown

**Unknown** means current status cannot be determined from available
documentation.

Unknown status should not be silently converted into Active, Resolved, or
Deferred. Unknown status is a documentation clarity issue, not an implementation
request by itself.

# Relationship To Existing Structures

Architectural Findings vocabulary maps to existing Seed structures as follows:

| Vocabulary term | Existing repository structures | Relationship |
| --- | --- | --- |
| Finding Surface | Characterizations, vocabularies, reconciliations, summaries, roadmaps, backlog reviews, status reviews, handoffs, architecture docs, executive summaries, conclusions, future-work sections, promotion tables, archive tables, stale/quarantine notices, non-goal sections | These are the surfaces where findings are already preserved. |
| Finding Preservation | Executive summaries, conclusions, scope sections, non-goal sections, files-inspected sections, handoff recommendations, promotion guidance, archive readiness, stale/quarantine notices | These mechanisms keep findings discoverable enough to preserve memory, even when fragmented. |
| Accepted Finding | Canonical vocabulary documents, architecture docs, reconciliation conclusions, status summaries | These surfaces stabilize accepted architecture language. |
| Rejected Concept | Non-goal sections, rejection criteria, complexity traps, negative findings, roadmap rationale | These surfaces preserve what should not be built or reintroduced. |
| Deferred Concept | Future-work sections, roadmap missing pieces, backlog/status recommendations, promotion gaps | These surfaces preserve work that waits for evidence, prioritization, or clearer need. |
| Open Question | Characterization questions, unanswered-operator-question sections, frontier assessments, risks | These surfaces preserve unresolved architecture questions. |
| Current Frontier | Roadmaps, architectural-status documents, knowledge-acquisition status, future-work sections | These surfaces preserve prioritized next attention. |
| Architectural Lesson | Executive summaries, conclusions, complexity traps, rejection criteria, repeated audit patterns | These surfaces preserve repeated repository lessons. |
| Non-Goal | Purpose/scope/non-goal sections, rejection criteria, complexity-trap sections | These surfaces preserve boundaries. |
| Status Update | Status reviews, backlog reviews, roadmap triage, archive tables, stale/quarantine notices | These surfaces preserve current or historical progress state. |
| Finding Authority | Canonical docs, architecture docs, later reconciliations, stale/quarantine notices | These surfaces imply authority differences, but no uniform authority mechanism exists. |
| Supersession | Stale/quarantine notices, archive guidance, promotion tables, later canonical vocabularies, later reconciliations | These surfaces sometimes show replacement, but no uniform supersession mechanism exists. |

Important repository-consistent interpretations:

- Characterizations discover what already exists and identify gaps.
- Vocabularies stabilize canonical language.
- Reconciliations align prior findings with current canonical language and
  backlog/status consequences.
- Summaries and navigation documents communicate existing knowledge without
  becoming new truth systems.
- Roadmaps and future-work sections preserve frontier and deferred work.
- Backlog reviews translate findings into maintenance recommendations.
- Handoffs transfer next-step context to future maintainers.
- Executive summaries and conclusions provide compact high-signal finding
  preservation.

# Relationship To Backlog

Findings influence backlog, but backlog does not create findings by itself.

The repository pattern is:

```text
Finding
↓
Backlog update
```

```text
Finding
↓
Deferred work
```

```text
Finding
↓
Removed or de-prioritized work
```

Backlog and status reviews can preserve finding consequences, including:

- promoting a completed audit sequence out of active backlog pressure;
- treating older implementation-oriented items as superseded by newer
  characterization or reconciliation findings;
- organizing future work under Knowledge Acquisition, Knowledge Integrity,
  Knowledge Selection, Response, Capability Growth, or Documentation;
- removing duplicate or obsolete items;
- identifying small documentation updates;
- preserving non-goals and rejection criteria so backlog items do not reintroduce
  engines, Runtime ownership, ToolExecutor ownership, or parallel truth systems.

A backlog item may point to a finding, but the existence of a backlog item does
not make the finding authoritative. Authority remains a documentation concept
owned by current surfaces, not by the backlog itself.

# Relationship To Reconciliation

A common Seed documentation path is:

```text
Characterization
↓
Vocabulary
↓
Reconciliation
↓
Finding
```

This path is supported when:

- a characterization discovers existing behavior, fragmented language, missing
  composition, unclear ownership, or unjustified implementation pressure;
- a vocabulary document names the concern without adding behavior;
- a reconciliation aligns the characterization, vocabulary, existing surfaces,
  backlog status, ownership boundaries, and non-goals;
- the resulting conclusion becomes an Architectural Finding.

Other valid paths also exist:

```text
Audit
↓
Reconciliation
↓
Promotion guidance
↓
Finding
```

```text
Roadmap/status review
↓
Frontier or backlog recommendation
↓
Finding
```

```text
Stale/quarantine notice
↓
Historical or superseded interpretation
↓
Finding
```

```text
Executive summary or conclusion
↓
Accepted finding, rejected concept, or non-goal
```

Reconciliation does not own all findings. It is one strong preservation path
among several existing surfaces.

# Relationship To Architectural Memory

Architectural Findings and Architectural Memory are overlapping but not
identical.

**Architectural Memory** is the broader repository-preserved record of how Seed's
architecture has been understood over time. It includes documentation, audit
history, vocabulary stabilization, reconciliations, roadmaps, handoffs, stale
records, generated architecture artifacts, ownership evidence, rejected paths,
lessons, and open questions.

**Architectural Findings** are the actionable or interpretive units inside that
memory: the specific conclusions, boundaries, recommendations, rejections,
deferrals, lessons, statuses, and open questions that future maintainers need to
understand.

Therefore, Architectural Findings are best described as a **subset and access
pattern of Architectural Memory**:

- subset, because findings are specific preserved units inside the larger memory;
- access pattern, because finding language helps readers ask what is active,
  authoritative, superseded, repository-wide, local, historical, rejected,
  deferred, or frontier-oriented.

This does not require a new architectural-memory engine, index, database, or
runtime integration.

# Existing Findings Surfaces

Seed already preserves findings across several surface types.

| Surface | Common finding categories | Notes |
| --- | --- | --- |
| Characterizations | Accepted Finding, Deferred Concept, Open Question, Architectural Lesson, Non-Goal, Status Update | Discover existing behavior, missing vocabulary, missing composition, ownership ambiguity, and rejected implementation pressure. |
| Vocabularies | Accepted Finding, Non-Goal, Architectural Lesson | Stabilize canonical language without adding runtime behavior. |
| Reconciliations | Accepted Finding, Rejected Concept, Deferred Concept, Status Update, Architectural Lesson, Non-Goal | Align prior audits, vocabulary, current surfaces, backlog consequences, and boundaries. |
| Summaries | Accepted Finding, Status Update, Current Frontier | Communicate compact conclusions and navigation over existing findings or signals. |
| Roadmaps | Current Frontier, Deferred Concept, Open Question, Status Update, Non-Goal | Preserve active and future work, missing pieces, and explicit non-goals. |
| Status Reviews | Status Update, Current Frontier, Rejected Concept, Open Question, Historical Finding | Preserve current architecture state and next-frontier rationale. |
| Backlog Reviews | Finding Consequence, Deferred Concept, Resolved Finding, Rejected Concept, Status Update | Translate findings into backlog cleanup, prioritization, and removal guidance. |
| Handoffs | Finding Recommendation, Current Frontier, Deferred Concept, Status Update | Transfer next-step maintenance and promotion context. |
| Executive Summaries | Accepted Finding, Rejected Concept, Status Update, Architectural Lesson | Provide concise high-signal conclusions. |
| Conclusions | Accepted Finding, Rejected Concept, Deferred Concept, Architectural Lesson | Preserve final interpretation of a document's evidence. |
| Future Work sections | Deferred Concept, Current Frontier, Open Question, Finding Recommendation | Preserve possible documentation-oriented follow-up. |
| Promotion tables | Finding Preservation, Finding Consequence, Resolved Finding, Historical Finding | Track movement from audit evidence to canonical owners. |
| Archive tables | Historical Finding, Superseded Finding, Resolved Finding | Preserve what can become historical after promotion or replacement. |
| Stale/quarantine notices | Historical Finding, Superseded Finding, Finding Authority | Warn readers that a surface is preserved but not current authority. |
| Non-goal sections | Non-Goal, Rejected Concept, Architectural Lesson | Preserve boundaries and anti-scope-creep constraints. |

# Authority Concepts

This section defines vocabulary only. It does not implement authority tracking.

## Finding Authority

Finding Authority is the documentation concept that one finding or surface may be
more current, canonical, or controlling than another when they discuss the same
concern.

Authority may be implied by:

- current canonical vocabulary documents;
- current architecture documents;
- later reconciliations;
- status reviews;
- explicit stale/quarantine notices;
- promotion tables that move knowledge from audits to canonical owners;
- archive guidance that marks old detail as historical.

Authority remains weak and fragmented today. That weakness is a finding, not a
request to build an authority engine.

## Repository-Wide Finding

A Repository-Wide Finding applies broadly across Seed.

Examples include:

- avoid generic engines unless justified by concrete need;
- do not use Runtime or ToolExecutor integration as a default solution;
- preserve EventLedger and ProjectionStore ownership boundaries;
- avoid projection mutation and event append in documentation concerns;
- avoid parallel truth, response, selection, explanation, integrity, context,
  caveat, planning, or workflow systems;
- prefer documentation-first vocabulary and reconciliation before implementation.

## Local Finding

A Local Finding applies to a bounded concern, document family, component, audit
chain, or roadmap slice.

Local findings should remain local unless later documentation promotes them to
repository-wide language.

## Historical Finding

A Historical Finding remains preserved for memory, but should not be treated as
current authority unless reaffirmed by a current surface.

Historical findings may still explain why a concept was rejected, why a roadmap
item moved, or why old implementation-era wording is no longer current.

# Supersession Concepts

This section defines vocabulary only. It does not implement supersession
tracking.

## Supersession

Supersession is the documentation concept that a current finding replaces,
updates, narrows, or invalidates an earlier finding for current architectural
interpretation.

Supersession may be explicit or implicit:

- explicit when a stale/quarantine notice says a document is not current
  authority;
- explicit when a promotion or archive table says unique knowledge has moved;
- implicit when a later vocabulary or reconciliation stabilizes language that
  older audits only sketched;
- implicit when a current status review de-prioritizes or removes older backlog
  pressure.

## Superseded Finding

A Superseded Finding is an older finding that has been replaced, narrowed, or
corrected by a newer current finding.

Superseded findings remain useful as historical context, but should not drive
current backlog or implementation work unless a current surface revives them.

## Current Finding

A Current Finding is the finding that should be used for present architectural
interpretation when multiple findings discuss the same concern.

Current does not imply runtime enforcement. It is a documentation status.

## Historical Finding

In supersession vocabulary, Historical Finding means the older preserved finding
remains available for audit trail, lesson preservation, and rejected-path memory,
but no longer stands alone as current authority.

# Proposed Vocabulary Shape

Architectural Findings may be described using the following documentation-only
shape:

```text
Architectural Finding
  category
  status
  scope
  surface
  recommendation
  consequence
  relationships
  metadata
  extensions
```

Meaning:

- `category`: the kind of finding, such as Accepted Finding, Rejected Concept,
  Deferred Concept, Open Question, Current Frontier, Architectural Lesson,
  Non-Goal, Status Update, or Historical Finding;
- `status`: the current interpretation, such as Active, Resolved, Deferred,
  Superseded, Historical, or Unknown;
- `scope`: repository-wide, local, historical, or unknown breadth;
- `surface`: where the finding is preserved;
- `recommendation`: any documented guidance derived from the finding;
- `consequence`: backlog, roadmap, documentation, archival, promotion, or
  non-goal effect;
- `relationships`: connections such as supports, refines, repeats, conflicts
  with, supersedes, is superseded by, depends on, motivates, constrains,
  defers, rejects, promotes, or archives;
- `metadata`: source document, related documents, evidence notes, owner-by-
  document, current-context notes, or date-like context when present;
- `extensions`: later documentation-only refinements when the vocabulary is
  insufficient.

This shape is not a schema, dataclass, database table, JSON contract, API
contract, index, route, adapter, read model, projection, or runtime contract.

# Complexity Traps

Architectural Findings vocabulary should avoid the following traps.

## ArchitectureEngine

An `ArchitectureEngine` would convert documentation-preserved memory into a new
runtime-like owner. Seed's findings are documentation and evidence, not behavior
that needs a generic engine.

## Architectural Registry

An Architectural Registry would imply centralized ownership, registration,
ranking, and lifecycle enforcement. The current gap is vocabulary and
discoverability, not proof that a registry is needed.

## Decision Database

A Decision Database would create schema, migration, persistence, authority, and
supersession obligations. It would risk becoming a parallel architectural truth
system.

## Architectural Runtime

An Architectural Runtime would incorrectly make architectural memory executable.
Findings do not route, execute, call providers, verify capabilities, mutate
projections, or append events.

## Authority Engine

An Authority Engine would over-solve a documentation problem and create a new
source of authority. This vocabulary only names authority concepts.

## Supersession Engine

A Supersession Engine would turn documentation supersession into automated state
management. Current needs are language and careful future reconciliation, not an
engine.

## Workflow ownership

Workflow ownership is a trap when findings are treated as tasks that must be
orchestrated. Findings may influence backlog or roadmap work, but they do not
own workflows.

## Runtime ownership

Runtime ownership is a trap because finding interpretation is not runtime
routing. Runtime should not become the owner of architectural findings,
architectural memory, authority, or supersession.

## ToolExecutor ownership

ToolExecutor ownership is a trap because findings do not execute tools or
operations. ToolExecutor should not own architectural memory or finding
consequences.

## Universal formatter

A universal formatter is a trap when local documentation and response surfaces
already communicate their own findings. Shared vocabulary does not require one
formatter.

## Parallel truth or response systems

A findings layer must not become a second truth system, response system,
selection system, explanation system, integrity system, context system, caveat
system, planner, or workflow system.

# Non-Goals

This document does not:

- implement an Architectural Findings Index;
- implement authority tracking;
- implement supersession tracking;
- implement inventories;
- implement read models;
- implement routes;
- implement adapters;
- implement databases;
- implement schema classes;
- implement engines;
- implement an architectural registry;
- implement an architectural database;
- implement an architectural runtime;
- modify `Runtime`;
- modify `ToolExecutor`;
- modify `EventLedger` ownership;
- modify `ProjectionStore` ownership;
- mutate projections;
- append events;
- call providers;
- add provider behavior;
- add execution behavior;
- add runtime behavior;
- perform runtime routing;
- determine truth;
- create a parallel truth system;
- create a parallel response system;
- create a parallel explanation system;
- create a parallel selection system;
- create a parallel context system;
- create a parallel integrity system;
- create a parallel caveat system;
- create a planner or workflow engine.

# Future Work

Future work should remain documentation-oriented unless a later, concrete,
evidence-supported operator question justifies otherwise.

Appropriate future work may include:

1. **Architectural Findings Reconciliation**: reconcile this vocabulary with the
   existing Architectural Findings Characterization and status/frontier documents
   to decide which finding terms are sufficient and which remain ambiguous.
2. **Architectural Status Characterization**: document current active,
   historical, deferred, and resolved status language if status ambiguity remains
   painful for maintainers.
3. **Architectural Frontier Characterization**: clarify current frontier language
   only if roadmap and future-work surfaces diverge.
4. **Documentation-only cross-link maintenance**: add links among architectural
   findings, status, roadmap, backlog, preservation, and vocabulary documents
   when needed for discoverability.
5. **Rejected-concept preservation review**: ensure repeated engine, runtime,
   ToolExecutor, and parallel-system rejections remain visible during future
   roadmap refreshes.

Future work should not default to an index, authority tracker, supersession
tracker, registry, database, route, schema, adapter, read model, Runtime
integration, ToolExecutor integration, engine, workflow system, provider action,
projection mutation, or event append.
