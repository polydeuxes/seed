# Documentation Structure Phase 3 Investigation

## Purpose and boundary

This investigation asks what the next safe layer should be after documentation structure visibility and structural recurrence visibility.

This is investigation only.

It does not implement meaning extraction, claim extraction, authority inference, shape inference, ontology promotion, NLP, LLM analysis, workflow systems, or automation.

Repository authority wins.

## Current Phase 1 and Phase 2 capability

Phase 1 established:

```text
prose
    -> observable document structure
```

Current structure visibility includes:

```text
yaml front matter
heading hierarchy
section inventory
structural links
fenced code blocks
document metrics
structural completeness
```

Phase 2 established:

```text
document structure
    -> corpus recurrence visibility
```

Current recurrence visibility includes:

```text
section labels
front matter keys
heading depths
code fence languages
link target classes
```

The current boundary remains:

```text
read only
no prose interpretation
no claim extraction
no authority inference
no shape inference
no ontology promotion
no event ledger writes
no repository mutation
```

This boundary is not incidental.

It is the main reason structure and recurrence can be safely observed without changing repository authority.

## Central finding

Phase 3 should continue structural visibility.

It should not cross into shape pressure yet.

The safest next implementation slice is:

```text
structural families / section skeleton visibility
```

with bounded support for:

```text
common skeletons
rare skeletons
missing common sections
structural outliers
recurrence histograms
```

This keeps Phase 3 inside:

```text
structure
    -> recurrence framing
    -> navigable visibility
```

and outside:

```text
recurrence
    -> candidate shape
    -> meaning
```

Repository authority wins.

## What new visibility structural recurrence makes possible

Structural recurrence now makes the following visibility possible without interpretation.

### Common structures

Examples:

```text
most common section labels
most common front matter keys
most common heading depths
most common code fence languages
```

Already partially visible.

Additional Phase 3 opportunity:

```text
common section skeletons
```

### Rare structures

Examples:

```text
section labels appearing once
rare front matter keys
rare code fence languages
unusual heading depths
```

Current recurrence can expose some of this through min-count controls, but does not frame rare structures directly.

### Missing structures

Examples:

```text
documents missing front matter
documents missing common sections
documents missing H1 headings
documents missing trailing newline
```

Missing front matter exists today.

Missing common sections would be a Phase 3 structural extension.

### Outlier structures

Examples:

```text
largest documents
deepest heading hierarchies
most sections
most links
most code fences
most duplicate headings
```

Current `--top` issue ordering partially supports this, but outlier framing is not yet a first-class visibility view.

### Layout similarity

Examples:

```text
documents with same ordered section labels
documents with same heading-depth profile
documents with similar front matter key sets
```

This is useful but riskier than simple skeleton visibility because similarity can start to imply family or intent.

It remains safe only if it is reported as exact structural matching, not conceptual grouping.

## Recurrence visibility versus candidate pressure

Repository evidence supports a distinction:

```text
recurrence visibility
    -> this structure appears N times
```

versus:

```text
candidate pressure
    -> this recurrence may matter
```

A recurrence row such as:

```text
Purpose: 276
```

is visibility.

It does not mean:

```text
Purpose is semantically important
Purpose is required
Purpose defines a shape
Purpose should be ontology
```

Phase 3 may support candidate pressure only indirectly by improving visibility.

It should not label recurrence as candidate meaning.

Safe wording:

```text
common
rare
missing
outlier
same skeleton
```

Unsafe wording:

```text
important
canonical
required
meaningful
shape candidate
authority-bearing
```

## Recurrence visibility versus shape candidate

### Recurrence visibility

Definition:

```text
observed repetition of structural facts
```

Examples:

```text
section label appears N times
front matter key appears N times
heading depth appears N times
section skeleton appears N times
```

No interpretation required.

### Shape candidate

Definition from prior inquiry:

```text
recurring structure observed across evidence
without requiring ontology promotion
```

Even though this remains weaker than ontology, it still introduces candidate meaning pressure.

It asks whether recurrence expresses a reusable structure.

That is beyond simple recurrence visibility.

### Boundary

```text
recurrence visibility counts and locates structures

shape candidate proposes that recurrence may be a meaningful structure
```

Phase 3 should stay on the first side.

## Phase 3 candidates reviewed

### 1. Structural families

Candidate:

```text
group documents by exact structural skeleton
```

Examples:

```text
Purpose > Findings > Supported Conclusions > Open Questions: 42 docs
Purpose > Non-Goals > Method > Conclusion: 31 docs
```

Usefulness:

```text
shows common document layouts
supports cleanup/navigation
makes recurrence actionable
```

Risk:

```text
family naming can imply meaning
```

Safe form:

```text
structural_skeleton_signature
```

not:

```text
investigation_family
```

Assessment:

```text
strongest Phase 3 candidate
```

### 2. Layout similarity

Candidate:

```text
show documents with similar heading structures
```

Usefulness:

```text
helps find related structure
finds documents that deviate from common layouts
```

Risk:

```text
similarity may imply semantic relatedness
```

Safe form:

```text
exact skeleton match first
```

Avoid fuzzy similarity initially.

Assessment:

```text
useful but should follow exact skeletons
```

### 3. Document grammar visibility

Candidate:

```text
show recurring section order and nesting rules
```

Usefulness:

```text
makes document conventions visible
shows common section order
```

Risk:

```text
grammar can sound prescriptive or semantic
```

Safe form:

```text
observed section order recurrence
```

not:

```text
document grammar rule
```

Assessment:

```text
valuable but wording risk is high
```

### 4. Common/missing section coverage

Candidate:

```text
for sections above recurrence threshold, show docs missing that label
```

Usefulness:

```text
supports consistency cleanup
answers concrete operator questions
```

Risk:

```text
missing common section can be mistaken for required missing section
```

Safe form:

```text
missing observed-common section
not required section
```

Assessment:

```text
high-value and safe if labeled carefully
```

### 5. Recurrence drift over time

Candidate:

```text
compare recurrence between snapshots or commits
```

Usefulness:

```text
shows structural evolution
identifies documentation churn
```

Risk:

```text
requires temporal snapshot/history support
can imply workflow or lineage
may need Git-based analysis or stored snapshots
```

Assessment:

```text
not safest Phase 3
better deferred
```

## Where current surface feels like grep

The recurrence surface still feels grep-like when it emits only raw labels and counts:

```text
Purpose: 276
Conclusion: 86
status: 135
```

without:

```text
example documents
histogram buckets
rare/common framing
outlier framing
section skeletons
missing structure framing
```

In this mode, the operator sees recurrence but not enough structural context to act.

## Where current surface feels like real visibility

It feels like a real visibility layer when it exposes normalized structural observations that grep does not reliably provide:

```text
heading hierarchy
section parent paths
front matter key extraction
code fence closure
link target classification
broken local docs link counts
structural completeness
```

The surface is strongest when it answers questions like:

```text
which documents are structurally incomplete?
which documents have unclosed code fences?
which docs have missing front matter?
which section labels recur?
which heading depths dominate?
```

It weakens when the operator must manually reconstruct actionable structure from raw recurrence counts.

## Risk boundaries

Phase 3 must preserve these boundaries:

```text
no prose interpretation
no claim extraction
no authority inference
no shape inference
no ontology promotion
no NLP
no LLM analysis
no workflow systems
no event ledger writes
no repository mutation
```

Additional Phase 3-specific boundaries:

```text
common does not mean required
rare does not mean wrong
similar does not mean related
missing common section does not mean defect
skeleton does not mean meaning
layout family does not mean semantic family
```

## Counterexamples

### Common structure that is not useful

```text
Purpose
Conclusion
Summary
```

may recur frequently but be too generic to guide action alone.

### Rare structure that is not a problem

A one-off heading may be structurally rare because the document is specialized, not because it is inconsistent.

### Similar skeleton that is not related

Two documents can share section order without sharing topic, meaning, authority, or claim structure.

### Missing common section that is intentional

A document may omit `Non-Goals` or `Open Questions` because its purpose does not require those sections.

### Structural family that becomes shape pressure

If a view names a cluster as an `investigation shape`, it has crossed the boundary.

The safe name is structural:

```text
section skeleton
```

not semantic:

```text
shape candidate
```

## Supported conclusions

1. Phase 1 made document structure visible.
2. Phase 2 made structural recurrence visible.
3. Phase 3 should remain structural.
4. The safest next target is structural skeleton/family visibility, paired with histogram, rare, missing, and outlier framing.
5. Recurrence visibility can support candidate pressure indirectly without becoming shape inference.
6. The boundary between recurrence visibility and shape candidate is whether the surface proposes meaning.
7. Current recurrence is more than grep when it exposes normalized structural observations.
8. Current recurrence feels grep-like when it only emits raw labels and counts.
9. Recurrence drift over time is useful but not the safest next slice.

## Unsupported conclusions

- Phase 3 should implement shape candidates.
- Phase 3 should infer document meaning.
- Common sections are required sections.
- Rare sections are errors.
- Similar layouts imply related documents.
- Structural families imply semantic families.
- Recurrence drift should be implemented before stronger static structural framing.
- Recurrence visibility should promote ontology.

## Recommended next step

The safest Phase 3 implementation target is:

```text
seed --documentation-structure --recurrence --skeletons
```

or equivalent naming that keeps the surface structural.

Suggested Phase 3 slice:

```text
section skeleton signatures
    -> exact ordered section-label/depth sequences

skeleton recurrence counts
    -> common and rare skeletons

example documents per skeleton
    -> bounded examples only

missing common section coverage
    -> threshold-based, non-prescriptive

structural outlier ranking
    -> metrics-only
```

Recommended ordering:

```text
1. recurrence histogram buckets
2. section skeleton signatures
3. bounded examples for recurrence rows
4. rare/common skeleton views
5. missing common section coverage
6. structural outlier ranking
```

The first step should likely be histogram buckets if not already fully implemented.

The best single Phase 3 feature is section skeleton signatures because it adds real structure beyond label counts while staying non-semantic.

## What should remain out of bounds

Explicitly out of bounds:

```text
meaning extraction
claim extraction
authority inference
shape inference
ontology promotion
NLP
LLM analysis
semantic similarity
concept clustering
required-section enforcement
workflow recommendations
```

## Acceptance answers

### What should Phase 3 be?

Phase 3 should be structural framing of recurrence.

The safest center is:

```text
section skeleton signatures / structural families
```

with supporting histogram, rare, missing, and outlier views.

### Should Phase 3 continue structural visibility, or stop before shape pressure?

Phase 3 should continue structural visibility and stop before shape pressure.

It may make recurrence more navigable.

It should not call recurrence a shape candidate.

### What is the safest next implementation slice?

The safest next slice is:

```text
section skeleton signatures
```

bounded by exact structural matching and non-semantic labels.

### What should explicitly remain out of bounds?

```text
meaning extraction
claim extraction
authority inference
shape inference
ontology promotion
NLP
LLM analysis
semantic similarity
concept clustering
required-section enforcement
```

Repository authority wins.
