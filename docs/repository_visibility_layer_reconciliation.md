# Repository Visibility Layer Reconciliation

## Purpose and boundary

This reconciliation asks what repository-visible layers have already been discovered across prior investigations involving language, prose, observation, structure, recurrence, and documentation structure.

This is investigation only.

It does not implement NLP, LLM analysis, claim extraction, semantic interpretation, authority inference, ontology promotion, classification systems, recommendation systems, workflow systems, or automation.

Repository authority wins.

## Central finding

Repository evidence supports a layered visibility model, but only up to structural coverage and source-location visibility.

The strongest currently supported stack is:

```text
artifact visibility
    -> language visibility
    -> structure visibility
    -> recurrence visibility
    -> distribution / drilldown / membership / coverage visibility
```

The highest repository-visible layer currently supported is:

```text
structural recurrence coverage and source-location visibility
```

This includes:

```text
what exists
what structural form it has
what recurs
how recurrence is distributed
where recurrence occurs
which documents are exact members
how much of the corpus is covered
```

The current boundary remains before:

```text
semantic interpretation
claim extraction
intent inference
authority promotion
shape inference
ontology promotion
truth / correctness / contradiction / supersession
```

## Identified visibility layers

### 1. Artifact visibility

Supported visibility:

```text
document exists
file exists
repository artifact exists
language-bearing artifact exists
```

Evidence:

Repository observation work frames repository observation as language-neutral acquisition of direct structural facts about repository artifacts.

Documentation prose reconciliation treats documentation as an observed repository artifact before treating it as architecture, truth, request, or command.

Supported boundary:

```text
artifact exists
    !=
artifact meaning is known
```

Status:

```text
strongly supported
```

### 2. Language visibility

Supported visibility:

```text
artifact contains language
operator supplied words
documentation contains prose
language can be quoted, inspected, attributed, compared, and cited
```

Evidence:

Documentation prose reconciliation found that prose is language-bearing material, but its architectural role comes from source context, document role, authority scope, observation boundary, interpretation boundary, promotion rules, routing rules, and execution authority.

Natural language reconciliation found that language observations preserve words with source, time, scope, and attribution context.

Supported boundary:

```text
language content
    !=
operator communicative act
```

and:

```text
instruction-like wording
    !=
executable instruction by default
```

Status:

```text
strongly supported as observation source
not supported as automatic meaning, truth, or authority
```

### 3. Structure visibility

Supported visibility:

```text
yaml front matter
document titles
section headings
heading hierarchy
metadata fields
structural links
fenced code blocks
document metrics
structural completeness
```

Evidence:

Repository prose structure visibility established:

```text
prose
    -> observable structure
```

before:

```text
prose
    -> meaning
```

Current documentation structure surfaces expose deterministic structural observations without reading document meaning.

Supported boundary:

```text
structure
    !=
meaning
```

Status:

```text
strongly supported and implemented as documentation structure visibility
```

### 4. Recurrence visibility

Supported visibility:

```text
section label recurrence
front matter key recurrence
heading depth recurrence
code fence language recurrence
link target class recurrence
section skeleton recurrence
rare/common structures
distribution buckets
```

Evidence:

Structural recurrence visibility established that recurrence can exist at the structure layer without prose interpretation.

Documentation structure recurrence review confirmed recurrence counts such as:

```text
Purpose: 276/277
Non-Goals: 106
Conclusion: 86
Central Finding: 63
status: 135
domain: 93
doc_type: 90
```

Supported boundary:

```text
structural recurrence
    !=
meaning recurrence
```

Status:

```text
strongly supported and implemented as corpus-level recurrence visibility
```

### 5. Distribution visibility

Supported visibility:

```text
long-tail recurrence buckets
rare structures
common structures
singleton-heavy section labels
outlier structures
```

Evidence:

Documentation structure recurrence review identified histogram buckets, rare structures, common structures, and outlier ranking as structural framing. Later context indicates these capabilities now exist.

Supported boundary:

```text
rare
    !=
wrong

common
    !=
required
```

Status:

```text
supported as structural recurrence framing
```

### 6. Drilldown visibility

Supported visibility:

```text
recurrence row
    -> bounded source locations
```

Examples:

```text
section-label:Purpose
    -> document paths
    -> line numbers
    -> heading depth

front-matter-key:status
    -> document paths

code-fence-language:python
    -> document paths and line ranges
```

Evidence:

Structural drilldown investigation established:

```text
recurrence visibility
    -> what recurs and how often

structural drilldown
    -> where does that recurrence occur
```

Supported boundary:

```text
drilldown
    !=
recommendation
```

and:

```text
source location
    !=
meaning
```

Status:

```text
supported as safe source-location visibility
```

### 7. Membership visibility

Supported visibility:

```text
exact observed inclusion in a structural recurrence set
```

Examples:

```text
document belongs to section-label:Purpose

document belongs to front-matter-key:status

document belongs to exact skeleton signature S

document belongs to outlier signal X
```

Evidence:

Structural membership investigation found membership to be a narrow set-oriented distinction, derivable from drilldown and recurrence, useful when asking which documents belong to an exact structural set.

Supported boundary:

```text
membership
    !=
relatedness

membership
    !=
similarity

membership
    !=
document family

membership
    !=
document type

membership
    !=
shape candidate
```

Status:

```text
supported as derived visibility
not clearly requiring standalone primitive status
```

### 8. Coverage visibility

Supported visibility:

```text
presence
absence
counts
percentages
membership totals
corpus denominator
```

Examples:

```text
front-matter-key:status
    present: 135
    missing: 307
    coverage: 30.5%
```

Evidence:

Structural coverage investigation found coverage to be membership plus corpus denominator plus absence visibility.

Supported boundary:

```text
coverage
    !=
compliance

coverage
    !=
policy

coverage
    !=
correctness

coverage
    !=
required shape
```

Status:

```text
supported as derived structural visibility
```

## Distinctions between structure, language, meaning, and authority

### Language

Language is visible as material or communicative act.

It can be preserved, attributed, cited, and interpreted later.

But language alone does not determine truth, authority, request status, command status, or execution authority.

### Structure

Structure is visible as deterministic organization.

Examples:

```text
yaml
headings
sections
links
code fences
metrics
```

Structure can be observed without semantic interpretation.

### Meaning

Meaning requires interpretation.

Examples:

```text
what claim is made
what concept is present
what intent is expressed
what the document means
```

Meaning is not currently part of the documentation structure observer boundary.

### Authority

Authority requires scoped repository support, promotion, acceptance, implementation evidence, claim support, policy, or lifecycle ownership.

Descriptive language and recurring structure do not create authority.

### Knowledge

Knowledge requires more than visibility.

Visibility can provide artifacts, language, structure, recurrence, location, membership, and coverage.

Knowledge requires appropriate evidence, support, authority, and projection boundaries.

## What can be observed without interpretation or promotion?

Current repository-visible information includes:

```text
document paths
file existence
language-bearing artifact existence
yaml front matter presence
front matter keys
document title presence
heading count
heading hierarchy
section labels
section counts
structural links
link target classes
fenced code blocks
code fence languages
code fence closure
document metrics
structural completeness
recurrence counts
recurrence distribution buckets
rare/common structures
structural outliers
section skeleton signatures
bounded drilldown locations
exact structural membership
structural coverage counts and percentages
```

These remain visible without:

```text
semantic interpretation
claim extraction
intent inference
authority promotion
```

## Layered model reconciliation

The best-supported layered model is:

```text
artifact visibility
    -> artifact exists

language visibility
    -> artifact or operator source contains words

structure visibility
    -> artifact has deterministic organization

recurrence visibility
    -> observed structure repeats across corpus

distribution visibility
    -> recurrence has corpus shape / tail / commonness / rarity

drilldown visibility
    -> recurrence has source locations

membership visibility
    -> recurrence has exact member documents

coverage visibility
    -> recurrence covers a proportion of a defined corpus
```

This is not an ontology claim.

It is a reconciliation of already discovered visibility layers.

## Current highest repository-visible layer

The highest currently supported layer is:

```text
structural coverage over exact structural recurrence sets
```

paired with:

```text
source-location drilldown
```

In fuller form:

```text
for exact observed document structures,
Seed can know what exists,
what recurs,
how recurrence is distributed,
where recurrence occurs,
which documents are exact members,
and what proportion of the corpus participates.
```

The highest layer is not:

```text
meaning
intent
truth
correctness
contradiction
supersession
explanation
shape authority
```

## What remains outside visibility boundaries

Explicitly outside current supported visibility:

```text
document meaning
operator intent as truth
claim truth
claim extraction
semantic recurrence
concept recurrence
contradiction detection
supersession
correctness
importance
document relatedness
semantic similarity
document family
document type inferred from structure
recommendation
workflow guidance
shape inference
ontology promotion
authority inference
explanation of why the prose matters
```

Some of these may exist as candidate or interpretation topics in other documents.

They are not part of the current non-interpretive visibility stack.

## Counterexamples

### Language and structure may overlap

A section label such as `Supported Conclusions` is both language and structure.

However the visibility layer can observe it structurally as a heading label without interpreting the conclusions inside it.

Therefore:

```text
language visibility
and
structure visibility
```

are not completely separate materials.

They are separate observation modes.

### Recurrence may be a projection of existing visibility

Recurrence does not introduce new source material.

It aggregates existing structural observations.

Therefore recurrence may be better understood as a projection or corpus view over structure visibility rather than a primitive.

This does not make it useless.

It means recurrence authority depends on the underlying structural observations.

### Membership and coverage are derived layers

Membership and coverage can be derived from recurrence, drilldown, and corpus denominator.

They may not require standalone repository primitives.

This supports the user's observation that membership and coverage are derived visibility layers.

### No coherent visibility stack may exist yet

The stack is reconciled from investigation conclusions, not declared by implementation as a single unified model.

Therefore the report should not claim Seed already owns a formal visibility stack.

The supported claim is weaker:

```text
prior investigations have discovered compatible visibility layers
```

not:

```text
Seed has implemented a unified visibility model
```

### High structural visibility can still be low semantic value

A document can be fully visible structurally while its meaning remains completely unobserved.

This preserves the boundary:

```text
visibility
    !=
understanding
```

## Supported conclusions

1. Repository evidence supports multiple visibility layers discovered across prior investigations.
2. Artifact visibility, language visibility, structure visibility, and recurrence visibility are strongly supported.
3. Distribution, drilldown, membership, and coverage are supported as derived structural visibility layers.
4. Language visibility and structure visibility are distinct observation modes, even when they inspect the same textual artifact.
5. Recurrence visibility is best understood as an aggregate projection over observed structure, not a semantic claim.
6. Membership and coverage are useful but appear derived, not primitive.
7. The current highest repository-visible layer is structural coverage and source-location visibility over exact structural recurrence sets.
8. Meaning, intent, truth, correctness, contradiction, supersession, explanation, recommendation, shape inference, and authority promotion remain outside the current visibility boundary.
9. Repository evidence does not yet support claiming a formal unified visibility model exists.
10. Repository evidence does support a coherent candidate reconciliation of discovered visibility layers.

## Unsupported conclusions

- Structure visibility proves meaning.
- Language visibility proves intent.
- Recurrence proves semantic recurrence.
- Coverage proves compliance.
- Membership proves relatedness.
- Drilldown recommends inspection targets.
- Structural skeletons define document families.
- Section labels define shape candidates.
- Documentation prose is inert.
- Documentation prose is automatically authoritative.
- Operator language automatically authorizes execution.
- Seed already has a formal unified visibility stack.

## Recommended next investigation

The logical next investigation is:

```text
visibility boundary reconciliation
```

Central question:

```text
At what point does visibility become interpretation?
```

Recommended focus:

```text
structural visibility
    -> candidate pressure

language visibility
    -> interpretation pressure

recurrence visibility
    -> shape pressure

coverage visibility
    -> compliance pressure

drilldown visibility
    -> recommendation pressure
```

Purpose:

```text
identify boundary-crossing pressures without implementing interpretation, shape inference, claim extraction, recommendation, or authority promotion
```

This should follow the current reconciliation because the visibility layers are now visible enough to ask where each layer pressures the next unsupported layer.

## Acceptance answers

### What visibility layers has the repository already discovered?

```text
artifact visibility
language visibility
structure visibility
recurrence visibility
distribution visibility
drilldown visibility
membership visibility
coverage visibility
```

### Which layers are supported by evidence?

Strongly supported:

```text
artifact visibility
language visibility
structure visibility
recurrence visibility
```

Supported as derived structural layers:

```text
distribution visibility
drilldown visibility
membership visibility
coverage visibility
```

### Which layers remain unsupported?

Unsupported as visibility layers today:

```text
meaning visibility
intent visibility as truth
claim truth visibility
semantic recurrence visibility
shape visibility
authority visibility from prose alone
correctness visibility
contradiction visibility
supersession visibility
recommendation visibility
```

### What is the current visibility boundary?

The current boundary is:

```text
exact observed artifacts, language, structure, recurrence, location, membership, and coverage
```

but not:

```text
semantic interpretation, claim extraction, intent inference, authority promotion, shape inference, ontology promotion, truth, correctness, contradiction, supersession, or explanation
```

### What cannot yet be observed?

Current surfaces cannot yet observe:

```text
what a document means
whether a prose claim is true
whether a document supersedes another
whether documents contradict
whether documents are semantically related
whether a structure is authoritative
whether a recurring structure is a shape
whether a missing structure is non-compliant
whether a document should be recommended
```

### What investigation should logically follow?

```text
visibility boundary reconciliation
```

focused on where structural, language, recurrence, drilldown, membership, and coverage visibility create pressure toward interpretation, authority, recommendation, compliance, or shape inference.

Repository authority wins.
