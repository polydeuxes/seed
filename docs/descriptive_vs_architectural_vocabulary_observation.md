---
doc_type: observation
status: exploratory
domain: descriptive vs architectural vocabulary observation
defines:
  - descriptive vocabulary observation
  - architectural vocabulary observation
  - explanatory language boundary evidence
related:
  - learning_as_lens_observation.md
  - lens_as_observation_and_compression_pattern.md
  - orientation_bundle_load_bearing_observation.md
  - inquiry_as_bridge_observation.md
  - inquiry_preservation_observation.md
  - unresolvedness_observation.md
  - pressure_source_observation.md
  - repository_observation_language_boundary.md
  - knowledge_lifecycle_reconciliation.md
  - boundary_preservation_as_architectural_principle.md
---

# Descriptive Vs Architectural Vocabulary Observation

## Status

Exploratory observation only.

This document investigates a recurring repository pattern:

```text
Some concepts appear useful for explanation.

Not all explanatory concepts become architectural concepts.
```

It does not modify implementation, ontology, Inquiry Orientation, State Summary,
runtime concepts, policy, or repository primitives. It does not promote any term
named here. Existing architecture, reconciliation, implementation, tests, and
more-specific observations retain authority for their scopes.

## Question

```text
What distinguishes descriptive vocabulary from architectural vocabulary?
```

The question is intentionally unstable. The repository may not support a sharp
boundary. The apparent distinction may instead describe concept maturity,
authority routing, evidence strength, or the repository's habit of delaying
promotion until reconciliation has enough load-bearing evidence.

## Repository evidence reviewed

This investigation reviewed repository materials around knowledge,
understanding, learning, seeing, orientation, lens, inquiry, unresolvedness,
concern, active edge, frontier, continuation, handoff, observation, claim, goal,
tool need, projection, runtime, reconciliation, and authority boundary.

Representative inspected files:

- `README.md`
- `01-architecture.md`
- `02-domain-model.md`
- `03-runtime-loop.md`
- `04-toolkit-system.md`
- `05-policy-and-safety.md`
- `06-context-engine.md`
- `docs/learning_as_lens_observation.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/inquiry_preservation_observation.md`
- `docs/unresolvedness_observation.md`
- `docs/pressure_source_observation.md`
- `docs/handoff_and_continuation_lineage_frontier.md`
- `docs/operations_frontier.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/repository_observation_language_boundary.md`
- `docs/boundary_preservation_as_architectural_principle.md`
- tests referencing runtime, projection, State Summary, Inquiry Orientation,
  tool needs, handoff, observation, claims, and reconciliation behavior.

The strongest contrast came from comparing architecture/domain documents that
name durable structures with observation documents that explicitly decline to
make ontology, runtime, schema, or policy claims.

## Descriptive vocabulary investigation

Repository evidence supports a cautious descriptive-vocabulary pattern:

```text
descriptive vocabulary helps participants see, explain, group, or preserve a
recurring pressure without itself becoming the object that runtime, projection,
policy, reconciliation, or catalogs must operate on.
```

This pattern appears in several observation documents.

`learning_as_lens_observation.md` treats `learning` as a useful lens over support
change, understanding change, derivation, decompression, contradiction discovery,
interpretation, scope, caveats, and responsibility routing. It explicitly avoids
making learning primary or canonical. The document's force is explanatory: it
helps identify what people may mean when they say learning, while insisting that
more-specific support paths carry the details.

`lens_as_observation_and_compression_pattern.md` makes the pattern more general:
broad language can help a finite participant notice scattered evidence, but it
becomes unsafe if it replaces source authority, support paths, caveats,
relationships, policy boundaries, or validated architecture.

`inquiry_as_bridge_observation.md`, `inquiry_preservation_observation.md`, and
`unresolvedness_observation.md` similarly preserve language that seems useful for
explaining why a branch or future participant can continue work. Their value is
not that they create new runtime entities. Their value is that they describe
recurring movement, open questions, gaps, and unfinished understanding in a way
that can be read against existing surfaces.

Candidate descriptive functions supported by the reviewed documents:

- explanation of recurring patterns;
- intuition for why several documents feel related;
- compression of scattered phenomena into a readable observation;
- preservation of uncertainty without forcing architecture;
- identification of pressure, gap, attention, or unfinished movement;
- a bridge between human understanding and repository-specific mechanisms;
- a warning that a term is carrying too much explanatory load.

Descriptive language is therefore not inferior. It may be the repository's safe
way to investigate before promotion, and sometimes its right final status.

## Architectural vocabulary investigation

Repository evidence supports a different, stronger pattern for architectural
vocabulary:

```text
architectural vocabulary participates in repository structure, authority,
implementation, projection, validation, reconciliation, or runtime behavior.
```

The domain model provides clear examples. `Event`, `Workspace`, `Session`,
`Goal`, `Entity`, `Fact`, `Evidence`, `Fact Support`, `ToolNeed`, `Capability`,
`Tool / Operation`, `Provider`, `Toolkit`, and related catalogs are not merely
reader-facing metaphors. They define boundaries, fields, validation roles,
projection relationships, execution boundaries, and explanatory obligations.

The runtime document provides another cluster. `Runtime`, `DecisionProvider`,
`DecisionValidator`, `PolicyEngine`, `ToolExecutor`, `EventLedger`,
`StateProjector`, `DecisionJournal`, and `RuntimeTrace` participate in a concrete
flow. Their vocabulary is architectural because behavior and authority attach to
them: raw provider output is not executed, only registered operations can enter
execution, request-tool branches record capability gaps rather than executing,
and runtime outcomes are appended as events.

The context and projection materials reinforce the distinction. Context Views,
State projections, Confidence, Evidence Graph, Contradiction Detection, and
State Summary surfaces are architectural when they define what gets projected,
selected, omitted, rendered, or used by decision providers.

Architectural vocabulary therefore tends to show at least some of these signs:

- explicit boundaries or fields;
- named source-of-truth relationships;
- projection participation;
- validation, reconciliation, or test participation;
- runtime routing or execution consequences;
- catalog or schema membership;
- durable event/state representation;
- implementation modules or public APIs;
- documented responsibility for what may or may not happen.

The evidence does not require every architectural term to have all these signs.
For example, some terms are architectural because they are documented boundaries
or catalog concepts even when they are not runtime objects. But the stronger the
participation in these surfaces, the stronger the architectural reading becomes.

## Historical examples

### Learning

`Learning` appears explanatory and cross-cutting. It helps describe improvement
or extension of represented understanding, but recent observation evidence
regularly decomposes learning into support change, understanding change,
derivation, caveat discovery, contradiction visibility, interpretation change,
and responsibility routing. In the reviewed evidence, learning remains primarily
descriptive/lens-like rather than a new architectural primitive.

### Understanding

`Understanding` is more ambiguous. It appears as a human-facing and
explanation-facing concept, but adjacent documents also treat understanding as
claim-like, scoped, supported, challenged, decompressed, and navigable. The
repository evidence suggests understanding can be descriptive in prose while also
pressuring architectural surfaces concerned with support, context, explanation,
and continuation. It is not uniformly one category.

### Knowledge

`Knowledge` has stronger architectural participation than learning because it is
connected to Evidence, Facts, claims, support, State projection, context views,
confidence, contradiction, and reconciliation. Yet `knowledge` can still be used
descriptively when it names the broad system rather than a specific object.
Evidence supports mixed status: architectural in certain documents and surfaces,
descriptive as broad orientation language.

### Seeing

`Seeing` appears mostly descriptive. It helps explain what a lens, observation,
or decompression makes visible. The reviewed evidence did not support `seeing`
as a repository primitive, runtime branch, projection object, or catalog entry.

### Orientation

`Orientation` appears closer to architectural vocabulary than many descriptive
terms, but its status remains careful. Orientation-related documents investigate
whether orientation is load-bearing for current work, selection, concern,
continuation, and resumability. This gives it stronger repository pressure than
`seeing` or `unresolvedness`, but the observation evidence does not by itself
make every orientation phrase architectural.

### Lens

`Lens` is explicitly observed as a compression and observation pattern. It is
useful for grouping phenomena, but the lens observation warns against replacing
detailed support structures with the broad concept. Current evidence supports
lens as primarily descriptive, with diagnostic value.

### Inquiry

`Inquiry` has repeatedly been useful for explaining movement between concern,
question, gap, continuation, and preservation. The reviewed inquiry observations
appear to preserve inquiry as bridge-like or preservation-relevant language while
stopping short of making it a runtime object or ontology term. Current evidence
therefore supports descriptive usefulness without architectural promotion.

### Unresolvedness

`Unresolvedness` appears useful for naming unfinished understanding, gaps,
unsettled authority, and preserved incompletion. Its current evidence seems
stronger as descriptive preservation language than as architecture. The fact that
it can be useful without becoming a projected State structure is one of the
clearest examples motivating this observation.

## Authority investigation

The reviewed repository evidence suggests architectural vocabulary usually has
stronger authority evidence than purely descriptive vocabulary.

Architectural authority often appears through reconciliation, implementation,
projection, runtime routing, source-of-truth designation, or tests. Examples
include:

- append-only events as source material for State and trace reconstruction;
- Facts as projected interpretations of Evidence;
- Context Views as read-only projections for decision providers;
- ToolNeeds as durable records of capability gaps rather than executable calls;
- ToolExecutor and ToolRegistry as the boundary for registered operation
  execution;
- State Summary surfaces as bounded projections rather than arbitrary knowledge
  expansion.

Descriptive vocabulary can still have authority of a different kind: it may have
observation authority inside its document. But that authority is usually bounded
by explicit disclaimers that the document is not ontology, not implementation,
not policy, not schema, not runtime design, and not reconciliation. In other
words, descriptive authority can authorize a way of reading evidence without
authorizing new repository behavior.

## Inquiry and unresolvedness investigation

Recent inquiry and unresolvedness documents repeatedly reach a similar result:

```text
useful, but not promoted.
```

This could mean insufficient evidence. It could also mean the terms belong to a
category of explanatory vocabulary that remains valuable precisely because it is
not forced into architecture. The reviewed evidence does not justify choosing one
explanation exclusively.

The strongest supported reading is weaker and safer:

```text
inquiry and unresolvedness currently help describe movement, pressure, gaps,
continuation, and preserved incompletion, while existing repository structures
carry the authoritative work.
```

Those existing structures include observations, claims, goals, tool needs,
frontiers, handoffs, facts, evidence, reconciliation records, context views, and
projection surfaces. Inquiry and unresolvedness may illuminate how those surfaces
feel or relate without needing to become additional surfaces.

## Lens and orientation investigation

Lens and orientation do not occupy identical positions.

`Lens` appears strongly descriptive in current evidence. It names a way of seeing
or compressing evidence, and the lens observation explicitly warns that lenses
must not replace support details.

`Orientation` appears more load-bearing. Orientation-related work connects to
concern, current work position, selection, continuation, active edge, and what a
future participant needs in order to resume. That gives orientation a stronger
claim to architectural relevance than lens, inquiry, or unresolvedness. However,
the reviewed evidence still preserves caution: orientation may be moving toward
architectural vocabulary in some contexts without every orientation-adjacent term
becoming architectural.

A candidate comparison:

| Term | Current observed role | Architectural evidence strength |
| --- | --- | --- |
| lens | compression/seeing pattern | low to medium |
| learning | broad explanatory lens | low to medium |
| inquiry | bridge/movement/gap explanation | low to medium |
| unresolvedness | preserved incompletion explanation | low |
| orientation | concern/current-work/continuation pressure | medium, possibly increasing |
| fact/evidence/event/tool need/runtime | defined repository structures | high |

This table is not a taxonomy. It records the current reading of evidence.

## Alternative models

The repository also supports several alternative explanations.

### No distinction exists

The apparent distinction may be an artifact of documentation style. Every term
may simply be vocabulary with different levels of explicitness.

### The distinction is artificial

Architectural and descriptive language may not be separate categories. A term may
be architectural in a domain model and descriptive in an observation, depending
on use.

### All vocabulary begins descriptive

A concept may first appear as explanation, then become architectural only after
repeated pressure, reconciliation, implementation, and tests make its boundaries
clear.

### Architectural vocabulary emerges through reconciliation

The repository may intentionally route broad terms through observations,
frontiers, audits, and reconciliations before allowing implementation or ontology
participation.

### Descriptive and architectural language are maturity levels

The difference may be temporal rather than categorical. `Orientation` may be a
case where descriptive language is being tested for load-bearing status.

### The repository avoids early promotion

The repeated `useful but not promoted` outcome may be a repository safety habit:
concepts are allowed to explain before they are allowed to govern structure.

### Descriptive language can be final

Some terms may remain descriptive forever because their job is to preserve human
understanding, not to become objects. `Seeing`, `lens`, and `unresolvedness` may
be examples if no later evidence promotes them.

## Candidate distinction discovered

A cautious candidate distinction is supported:

```text
Descriptive vocabulary
    helps explain, illuminate, group, preserve, or orient attention around
    repository patterns.

Architectural vocabulary
    participates in repository structure, authority, implementation,
    projection, runtime routing, reconciliation, validation, catalogs, tests,
    or durable state/event behavior.
```

This distinction is not absolute. The same word can be descriptive in one context
and architectural in another. A descriptive term can become architectural through
reconciliation. An architectural term can still be used descriptively in prose.
The distinction is therefore best treated as an authority-and-participation
question, not a ranking.

## Uncertainties

- Whether `orientation` is already architectural, still descriptive, or in
  transition remains unresolved.
- Whether `inquiry` should remain purely descriptive or become a named frontier,
  handoff, or continuation surface is not answered here.
- Whether `unresolvedness` is a durable quality of claims/understanding or only a
  helpful prose term remains open.
- Repository terminology is not stable enough to build a fixed taxonomy from
  this observation.
- The reviewed evidence may overrepresent recent exploratory branches that were
  intentionally cautious about promotion.
- Tests and implementation surfaces were sampled by term search, not exhaustively
  reconciled.

## Non-conclusions

This observation does not conclude that:

- new ontology should be created;
- new runtime structures should be added;
- descriptive language is inferior;
- architectural language is superior;
- inquiry should be promoted;
- unresolvedness should be promoted;
- lens and orientation must diverge;
- all useful explanatory language should eventually become architecture;
- all architectural vocabulary begins as descriptive vocabulary.

The current evidence supports preserving the question rather than closing it.
