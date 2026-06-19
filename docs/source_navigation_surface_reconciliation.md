---
doc_type: reconciliation
status: active
domain: source navigation
defines:
  - source navigation surface reconciliation
  - source knowledge preservation boundary
  - source navigation prerequisites
  - source observation navigation distinction
related:
  - source_definitions_and_entrypoint_observation_reconciliation.md
  - source_observation_queryability_audit.md
  - source_navigation_query_surface_design_audit.md
  - source_navigation_without_grep_audit.md
  - source_observation_duplicate_fact_audit.md
  - repository_observation_implementation_inventory_audit.md
---

# Source Navigation Surface Reconciliation

## Purpose

This reconciliation investigates what distinguishes source knowledge preservation from source navigation, and what must already exist before source navigation becomes possible.

It is not an implementation, proposal, roadmap, workflow definition, schema definition, API definition, CLI design, or command design.

It does not modify runtime behavior, repository observation behavior, fact projection behavior, source observation behavior, current-facts behavior, why-fact behavior, state summary behavior, or operator commands.

Repository authority remains distributed across the implementation, existing reconciliations, audits, and read-model documents. This document reconciles the boundary between preserved source knowledge and navigable source knowledge.

---

## Central Finding

The repository already distinguishes source observation from source navigation.

```text
source observation
        preserves evidence-backed source relationships

source navigation
        lets an operator move from a question to the relevant source artifact,
        relationship, and support without first knowing the exact fact shape
```

The strongest reconciliation is:

```text
Preservation is prerequisite.
Navigation is orientation over preserved knowledge.
Navigation is not a new observation.
Navigation is not a stronger fact.
Navigation is not ownership, reachability, explanation, or implementation knowledge by itself.
```

A repository can preserve imports, definitions, entrypoints, source paths, dimensions, fact support, and current projections while still failing navigation if operators cannot discover the correct subject, predicate, object, path, and support chain from natural implementation questions.

---

## Evidence Reviewed

This reconciliation reviewed repository evidence related to:

- source observation and repository observation;
- import observations;
- definition observations;
- entrypoint observations where discussed or tested;
- current-facts projection;
- fact support projection;
- why-fact behavior;
- state summary and state views;
- source observation audits;
- source definitions and entrypoint reconciliation;
- implementation navigation findings.

The strongest evidence surfaces are:

| Evidence surface | Relevant finding |
| --- | --- |
| `source_definitions_and_entrypoint_observation_reconciliation.md` | Imports, definitions, entrypoints, and behavior edges answer different implementation questions and must not collapse into one relationship. |
| `source_observation_queryability_audit.md` | Source facts can be preserved but remain brittle to query when operators must know exact normalized fact shapes. |
| `source_navigation_query_surface_design_audit.md` | A source navigation surface should be a read-only view over existing source facts, not a new source of truth or ingestion path. |
| `source_navigation_without_grep_audit.md` | Grep is an acquisition capability, not Seed self-knowledge; navigation should come from preserved observations and support. |
| `source_observation_duplicate_fact_audit.md` | Repeated observation should accumulate support rather than make durable source relationships look duplicated. |
| `repository_observation_implementation_inventory_audit.md` | Observation primitives, observation sources, acquisition workflows, and operator entrypoints are distinct layers. |
| `seed_runtime/observation_sources.py` | `RepositorySourceObservationSource` collects imports and definitions as ordinary observations with source path dimensions and metadata. |
| `seed_runtime/knowledge/relationship_observation.py` | Relationship extraction is deterministic and bounded; it parses caller-provided source text and preserves imports/definitions without reading files itself. |
| `seed_runtime/state_views.py` | Current fact views are read-only projections over an already-built state and include support/event context. |
| `scripts/seed_local.py` | Existing operator surfaces include current facts, fact support, why-fact, relationships, and state summary, but these are general read-model surfaces rather than source-specific navigation. |
| Tests around repository current facts | Current facts can surface repository `imports` and `defines` and can filter by subject/predicate, confirming repository support for preserved source facts. |

---

## Source Observation Versus Source Navigation

### Source Observation

Source observation answers:

```text
What source relationship was observed?
What evidence supports that relationship?
Where did the observation come from?
When was it observed?
What dimensions identify the source artifact?
```

For repository source relationships, the current implementation shape is:

```text
source file text
        ↓
relationship extractor
        ↓
relationship observation
        ↓
evidence-backed fact
        ↓
projected current fact / fact support
```

A source observation can say:

```text
module imports symbol
module defines symbol
source path supports this relationship
```

It should not by itself say:

```text
the symbol is operator-reachable
the behavior is invoked
the file owns a capability
the source is correct
the result is the best place to start
the operator has enough context to navigate
```

### Source Navigation

Source navigation answers:

```text
How does an operator locate the source artifact relevant to a question?
How does an operator move from a symbol, file, module, behavior name, or command-like surface to preserved source evidence?
Which preserved relationship should be inspected next?
Which support chain explains why that relationship is believed?
```

Navigation is therefore a selection and orientation layer over preserved source relationships.

It does not create source facts. It arranges access to source facts.

It does not strengthen source facts. It prevents operators from needing accidental prior knowledge of normalized fact identities.

---

## What Must Already Exist Before Navigation Becomes Possible

Source navigation becomes possible only after several preservation dependencies exist.

### 1. Durable Source Artifacts

Navigation needs stable source artifact identifiers:

```text
repository path
module identity
source file identity
```

Without paths, navigation cannot return an inspectable artifact. Without module identity, navigation cannot connect Python source relationships to fact subjects. Without a boundary between path identity and module identity, operators encounter the path/module mismatch already documented by queryability audits.

### 2. Preserved Definitions

Definitions are the strongest prerequisite for symbol-location navigation.

They answer:

```text
Where is this symbol declared?
Which file owns this definition location?
What definitions exist in this module?
```

A definition is not an invocation or reachability proof, but it is the clearest current evidence for source ownership.

### 3. Preserved Imports

Imports are prerequisites for dependency navigation.

They answer:

```text
What does this file depend on?
Which modules mention or require this symbol?
What source relationships may lead from one module to another?
```

Imports do not answer ownership and do not prove behavior. They still help navigation by showing possible dependency paths and next artifacts to inspect.

### 4. Preserved Entrypoints, If Present

Entrypoints are prerequisites for reachability-oriented navigation.

They answer:

```text
Where is this operator or runtime surface declared?
What source artifact exposes this behavior?
What source surface could lead into this implementation?
```

Current repository evidence treats entrypoints as a distinct relationship class in reconciliation and test expectations. Where entrypoint facts are absent, navigation must not pretend definitions or imports prove reachability.

### 5. Preserved Support

Navigation requires support because it must move from answer to evidence.

The fact alone is not enough. Operators also need:

```text
supporting evidence identifiers
observation metadata
source path dimensions
relationship evidence text
currentness / support projection status
```

Without support, navigation degenerates into a search result with no explanation trail.

### 6. Projection Stability

Navigation needs current-facts and fact-support projection to avoid duplicate-looking or stale-looking answers.

The duplicate-fact audit's key preservation lesson is that repeated observation should not make a durable source relationship appear to exist multiple times. Stable support grouping lets navigation say "this relationship is current and supported" rather than flooding the operator with repeated rows.

### 7. Relationship Boundaries

Navigation depends on preserving relationship distinctions:

```text
imports != defines
defines != invokes
entrypoint != capability
path != module
symbol != behavior
ownership != reachability
support != authority
```

If those boundaries collapse, navigation may become convenient but misleading.

---

## Ownership Findings

Ownership questions include:

```text
Who owns this symbol?
Who owns this file?
Who owns this definition?
```

The strongest current answer is definition preservation.

A `defines` relationship can identify the source artifact that owns the canonical declaration of a symbol. A module or file that defines `state_summary` is the owner of that definition location.

However, ownership must remain scoped:

| Question | Strongest repository support | Boundary |
| --- | --- | --- |
| Who owns this symbol definition? | `defines` relationship plus source path dimension. | Does not prove invocation or behavioral responsibility. |
| Who owns this file? | Repository path and documentation/source authority may identify artifact location. | File ownership is not the same as capability ownership or runtime state ownership. |
| Who owns this behavior? | May require definitions plus explicit registrations, calls, entrypoints, or documentation authority. | A definition alone is insufficient. |
| Who owns this capability? | Capability catalogs, registrations, or scoped docs if present. | Source definition does not automatically become capability ownership. |

Ownership is therefore narrower than navigation. Navigation may use ownership as one waypoint, but a navigation answer may also route through imports, support, paths, entrypoints, or current projection surfaces.

---

## Reachability Findings

Reachability questions include:

```text
Can an operator reach this behavior?
Can this definition be invoked?
Can this symbol be discovered?
```

The strongest current distinction is:

```text
definition existence
        !=
operator reachability
```

A definition can be discoverable through source navigation without being invoked by any runtime path.

An import can show dependency without invocation.

An entrypoint can show a reachability surface without proving the full behavior chain unless dispatch/call relationships also exist.

| Question | Evidence needed | Boundary |
| --- | --- | --- |
| Can an operator reach this behavior? | Entrypoint plus dispatch/call or registration evidence. | Definition alone does not answer. |
| Can this definition be invoked? | Call, registration, dispatch, framework, or test evidence. | Import alone does not answer. |
| Can this symbol be discovered? | Preserved definition/import/path facts and navigable projection. | Discoverability is not runtime reachability. |

The repository's current support for reachability is strongest as a documented boundary rather than a complete implemented source graph. Navigation must therefore expose uncertainty instead of filling gaps with inference.

---

## Navigation Findings

Navigation questions include:

```text
How does an operator locate a source artifact?
How does an operator move from question to source evidence?
Where is state_summary defined?
Which file owns this symbol?
What definitions exist in this module?
What imports exist in this file?
Which source observations support this answer?
```

The strongest current repository support for navigation is:

1. source relationship facts for imports and definitions;
2. path dimensions on repository source observations;
3. support projection over facts;
4. read-only current-facts and fact-support surfaces;
5. why-fact explanation path for exact fact identities;
6. state views that present projected state without mutating runtime behavior;
7. source audits identifying path/module and short-symbol/qualified-symbol mismatches.

The strongest current gap is not missing source knowledge preservation. It is source-specific orientation.

A general current-facts stream can contain the answer but still fail the navigation task because the operator must already know:

```text
canonical module subject
canonical predicate
fully qualified symbol object
path dimension conventions
whether the fact is represented as current support
```

Navigation begins when the operator can start with the artifact as they know it:

```text
state_summary
seed_runtime/state_summary_views.py
seed_runtime.state_summary_views
--state-build
```

and reach the preserved evidence without first reverse-engineering the fact shape.

This reconciliation does not define the route, command, API, or workflow for doing that. It only records what the route would have to preserve.

---

## Preservation Findings

The strongest preservation dependencies are:

| Preserved thing | Why navigation depends on it |
| --- | --- |
| Definitions | Anchor symbol-location and ownership questions. |
| Paths | Return inspectable artifacts and bridge repository layout to module facts. |
| Module identities | Preserve language-specific source subjects and avoid path-only ambiguity. |
| Imports | Support dependency-oriented navigation and next-artifact discovery. |
| Entrypoints | Support reachability-oriented navigation where implemented. |
| Support links | Let navigation answer "why do we believe this?" instead of only "where might it be?" |
| Dimensions | Carry path and other scoping context without overloading subject/object. |
| Relationship kind | Prevent imports, definitions, entrypoints, calls, and ownership from collapsing. |
| Current projection | Prevent stale or duplicated observations from masquerading as multiple current facts. |
| Documentation authority boundaries | Prevent navigation documents from becoming implementation or runtime authority. |

The most important preservation rule is:

```text
Navigation can be derived only from what preservation kept distinct.
```

If source observation collapses a path into a module, a definition into a behavior, or an entrypoint into a capability, navigation can no longer produce careful answers.

---

## Strongest Navigation Surfaces Already Present

The repository already contains partial navigation surfaces:

| Surface | Current navigation value | Limitation |
| --- | --- | --- |
| `--current-facts` | Can show preserved source facts, including imports and definitions. | Too broad; requires exact subject/predicate filtering for source-specific use. |
| `--fact-support` | Can show support for a known subject/predicate. | Requires the operator to know the fact shape. |
| `--why-fact` | Can explain a known fact. | Brittle for path-like or short-symbol questions. |
| `--relationships` | Exposes relationship catalog/navigation around relationship kinds. | Not a source-specific locator by itself. |
| State views | Provide read-only projected rows with support context. | General projection layer, not source navigation. |
| Repository source observation source | Preserves imports/definitions with paths. | Observation source, not operator navigation. |
| Source audits and reconciliations | Preserve distinctions and findings. | Documentation authority only; not executable navigation. |

The strongest current support is therefore architectural and factual, not yet navigationally ergonomic.

---

## Required Tensions

### Navigation Versus Ownership

Navigation may use ownership, but ownership is only one kind of answer.

A `defines` fact can identify the owner of a symbol definition. Navigation must also help the operator move to dependencies, support, paths, or reachability surfaces. Treating navigation as ownership would hide import and support paths.

### Navigation Versus Reachability

Navigation can make a symbol discoverable even when no operator path reaches it.

Reachability needs entrypoint, dispatch, registration, call, framework, or test evidence. Navigation must not imply that a located definition is invocable.

### Navigation Versus Preservation

Preservation stores the distinct source facts and their support. Navigation organizes access to them.

Preservation can exist without navigation. Navigation cannot be trustworthy without preservation.

### Navigation Versus Explanation

Explanation answers why a fact is believed. Navigation answers how to find the relevant source artifact and evidence.

A good navigation answer should link to explanation support, but explanation alone may be unusable if the operator cannot identify the fact to ask about.

### Navigation Versus Implementation Knowledge

Implementation knowledge includes ownership, dependencies, reachability, calls, registrations, reads, writes, emits, and behavior markers.

Navigation is a way to traverse implementation knowledge. It is not the complete implementation model.

### Navigation Versus Source Observation

Source observation records what was seen. Navigation answers how an operator finds and uses what was seen.

Observation should remain conservative. Navigation should not silently upgrade an observation into a stronger relationship.

---

## Reconciled Answers To The Prompted Questions

### What answers: Who owns this symbol?

A preserved `defines` relationship is the strongest source-level answer for ownership of a symbol's definition. Additional ownership claims require documentation, catalog, registration, or architectural support.

### What answers: Who owns this file?

Repository path identity and documentation/source authority identify the file as an artifact. They do not by themselves identify behavioral, capability, or runtime-state ownership.

### What answers: Who owns this definition?

The source artifact that emits the `defines` relationship owns the definition location. The support chain should show the observed path and evidence.

### What answers: Can an operator reach this behavior?

Entrypoint plus dispatch/call/registration evidence can answer. Definitions and imports alone cannot.

### What answers: Can this definition be invoked?

Invocation requires call, dispatch, registration, framework, or test evidence. A definition can exist without any preserved invocation relationship.

### What answers: Can this symbol be discovered?

Discovery requires preserved source relationships plus a navigable surface over symbol, module, and path identities. This is weaker than runtime reachability.

### What answers: How does an operator locate a source artifact?

Navigation over preserved paths, modules, definitions, imports, entrypoints, and support can locate the artifact. General current-facts can contain the same data but is not necessarily an adequate navigation surface.

### What answers: How does an operator move from question to source evidence?

The operator needs a bridge from human-known identifiers to preserved fact identities and support. The repository already preserves much of the evidence; the unresolved surface is the source-specific orientation over it.

### What must survive for navigation to become possible?

Definitions, paths, module identities, ownership distinctions, support chains, relationship kinds, source dimensions, current projection semantics, and authority boundaries must survive. Calls, registrations, and entrypoints must survive where reachability or behavior navigation is expected.

---

## Unresolved Tensions

1. **Path identity versus module identity.** Operators often know repository paths, while facts often use module subjects.
2. **Short symbol versus qualified symbol.** Operators ask for `state_summary`; facts may preserve `seed_runtime.state_summary_views.state_summary`.
3. **General fact surfaces versus source-specific orientation.** Current facts can preserve answers without being a good source navigation surface.
4. **Definition ownership versus behavior ownership.** A source file can own a definition without owning every behavior associated with a concept.
5. **Discoverability versus reachability.** A symbol may be navigable as a source artifact while remaining unproven as operator-reachable behavior.
6. **Explanation entrypoint brittleness.** Why-fact can explain exact facts but may fail operator questions that use paths, short symbols, or behavior labels.
7. **Relationship incompleteness.** Imports and definitions are strong prerequisites, but behavior navigation needs relationships that may not yet be preserved.
8. **Documentation authority.** Reconciliations can preserve distinctions and findings, but they must not become implementation commands or runtime contracts.

---

## Final Reconciliation

Source knowledge preservation is the repository's ability to keep distinct, evidence-backed source relationships alive across observation, evidence, fact promotion, support grouping, and projection.

Source navigation is the operator-facing ability to move from a question to the preserved source artifact, relationship, and support chain that can answer it.

Navigation becomes possible when preservation has already kept enough distinct structure:

```text
paths
modules
symbols
definitions
imports
entrypoints where present
support
relationship kinds
current projection status
authority boundaries
```

The repository currently has strong prerequisites for navigation, especially imports, definitions, source paths, support projection, and read-only fact views. Its main unresolved issue is not whether source observations can be preserved. It is whether operators can traverse those preserved observations without already knowing the normalized fact model.
