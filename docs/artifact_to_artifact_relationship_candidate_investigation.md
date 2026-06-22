# Artifact-to-Artifact Relationship Candidate Investigation

## Purpose and boundary

This investigation asks which artifact-to-artifact relationship, if any, already has implementation-backed evidence.

This is investigation only.

It does not implement inquiry graphs, attachment systems, lineage systems, inquiry movement systems, prose ingestion, workflow systems, or automation.

Repository authority remains implementation-backed surfaces, executable diagnostics, repository-visible documents, and recorded operator output such as `seed --inquiry-artifacts`.

## Central finding

Repository evidence supports one candidate artifact-to-artifact relationship more strongly than the others:

```text
boundary
    -> unknown
```

The evidence is still not strong enough to call this a first-class implemented artifact relationship.

It is the strongest candidate because both sides are repository-visible inquiry artifacts, both recur in implementation-backed surfaces, and the relationship can often be observed as a boundary preserving or exposing an unknown without requiring a full investigation-chain reconstruction.

The next strongest candidates are weaker:

```text
pressure
    -> boundary

pressure
    -> surface

gap
    -> pressure

finding
    -> boundary
```

These recur, but they depend more heavily on investigation prose, human interpretation, or non-artifact endpoints.

## Current evidence baseline

Earlier investigations established a three-level model:

```text
artifact visibility
    -> repository-visible today

artifact-attached structure
    -> repository-visible today

artifact-to-artifact structure
    -> mostly human-interpreted today
```

The implemented `seed --inquiry-artifacts` output supports:

```text
artifact
    -> visibility

artifact
    -> evidence

artifact
    -> limitation
```

Examples from the recorded output and earlier investigations include:

```text
unknown
    -> diagnostic_inventory

unknown
    -> diagnostic_shape_audit

unknown
    -> knowledge_reachability

boundary
    -> privilege_discovery

boundary
    -> capability_relationship

pressure
    -> pressure_audit

pressure
    -> capability_relationship

pressure
    -> reasoning_path

pressure
    -> selection_path

gap
    -> observation_domains
```

This is repository-visible artifact-attached structure.

It is not automatically artifact-to-artifact structure.

## Candidate relationships reviewed

### 1. Boundary to unknown

Candidate:

```text
boundary
    -> unknown
```

Evidence:

```text
unknown
    -> repository_visible

boundary
    -> repository_visible
```

Both are stronger than pressure, finding, gap, supported conclusion, unsupported conclusion, and open question in the current visibility gradient.

Implementation-backed surfaces repeatedly expose both:

```text
diagnostic_inventory
    exposes diagnostic boundaries and unknown diagnostic shape status

diagnostic_shape_audit
    checks diagnostic shape consistency and mismatch absence

knowledge_reachability
    treats unknown as a candidate kind

capability_relationship
    exposes capability pressure and acquisition boundaries

privilege_discovery
    exposes read-only privilege boundaries

operational_surface_classification_audit
    preserves unknown classification for unsupported or unclassified surfaces
```

Why this is strongest:

A boundary often preserves an unknown instead of resolving it.

This can be observed from implemented surfaces without needing the full investigation prose chain.

Example shape:

```text
read-only boundary
    -> unknown remains unfilled

mutation boundary
    -> unknown remains unpromoted

classification boundary
    -> unknown remains classified unknown

capability boundary
    -> unknown capability state remains visible
```

Status:

```text
strongest candidate
not first-class implemented relationship
repository-visible endpoints
partially repository-visible relation
```

### 2. Pressure to boundary

Candidate:

```text
pressure
    -> boundary
```

Evidence:

Pressure is partially visible through surfaces such as:

```text
pressure_audit
capability_relationship
reasoning_path
selection_path
```

Boundaries are repository-visible through surfaces such as:

```text
privilege_discovery
capability_relationship
diagnostic_inventory
```

The relationship recurs when pressure narrows against limits:

```text
capability pressure
    -> acquisition boundary

selection pressure
    -> selection-path boundary

reasoning pressure
    -> reasoning-path boundary
```

Why it is weaker than boundary-to-unknown:

Pressure is only partially repository-visible.

The movement from pressure to boundary usually requires interpreting why a pressure narrowed.

Status:

```text
strong candidate
more human-interpreted than boundary -> unknown
```

### 3. Pressure to surface

Candidate:

```text
pressure
    -> surface
```

Evidence:

Earlier inquiry movement work identified question-to-surface and pressure-to-implementation as the strongest repository-visible movement forms.

Examples:

```text
selection rationale pressure
    -> selection_path

reference pressure
    -> reference_selection

projection pressure
    -> projection_shape

pressure
    -> implementation surface
```

Why it is not the strongest artifact-to-artifact relationship:

`surface` is not clearly an inquiry artifact in the same sense as boundary, unknown, pressure, finding, gap, supported conclusion, unsupported conclusion, or open question.

This may be the strongest movement relationship, but it is not clearly artifact-to-artifact.

Status:

```text
strong implemented movement
weak artifact-to-artifact candidate
```

### 4. Gap to pressure

Candidate:

```text
gap
    -> pressure
```

Evidence:

Gap and pressure recur across investigations.

Gap has attached evidence through `observation_domains` in the inquiry-artifacts model.

Pressure has attached evidence through `pressure_audit`, `capability_relationship`, `reasoning_path`, and `selection_path`.

Why it is weaker:

The relationship is mostly reconstructed from investigation chains.

Implemented surfaces can expose gaps and pressures as endpoints, but they do not clearly emit:

```text
gap produces pressure
```

Status:

```text
recurring candidate
mostly human-interpreted
```

### 5. Finding to boundary

Candidate:

```text
finding
    -> boundary
```

Evidence:

Findings and boundaries recur in investigations.

Boundary is repository-visible.

Finding is only partially visible.

Why it is weaker:

The transition from finding to boundary usually depends on reading the investigation prose.

Implemented surfaces preserve boundaries, but they do not clearly expose which finding produced the boundary.

Status:

```text
useful investigation-chain relationship
not currently implementation-backed as relationship
```

### 6. Finding to supported conclusion

Candidate:

```text
finding
    -> supported_conclusion
```

Evidence:

This appears repeatedly in report structure.

Why it is weak:

Supported conclusions remain document-visible.

The relationship usually exists because humans read the report sequence.

Status:

```text
document-visible
not implementation-backed
```

## Multi-surface recurrence

The strongest recurrence cluster is:

```text
boundary
unknown
pressure
```

Observed across:

```text
diagnostic_inventory
diagnostic_shape_audit
knowledge_reachability
operational_surface_classification_audit
capability_relationship
privilege_discovery
pressure_audit
reasoning_path
selection_path
```

The relationship candidate with the best recurrence is:

```text
boundary
    -> unknown
```

because:

```text
boundary and unknown are both repository-visible
multiple implemented surfaces preserve both
boundaries frequently explain why unknowns remain unknown
unknown preservation can be seen without full prose-chain reconstruction
```

Pressure-related candidates recur in more surfaces, but pressure itself remains partially visible and the relationship often requires human interpretation.

## Distinguishing artifact-to-evidence from artifact-to-artifact

### Artifact to evidence

Shape:

```text
artifact
    -> evidence source
```

Example:

```text
unknown
    -> knowledge_reachability

boundary
    -> privilege_discovery

pressure
    -> pressure_audit
```

Meaning:

The evidence source supports visibility or characterization of the artifact.

The target is not itself necessarily an inquiry artifact.

### Artifact to artifact

Shape:

```text
artifact A
    -> artifact B
```

Example candidate:

```text
boundary
    -> unknown
```

Meaning:

One inquiry artifact constrains, preserves, produces, qualifies, or redirects another inquiry artifact.

The target must be an artifact, not merely a surface, diagnostic, document, or evidence source.

### Boundary between them

The strongest remaining boundary is:

```text
attached evidence identifies why an artifact is visible

artifact-to-artifact structure identifies how one artifact relates to another artifact
```

Current implementation mostly emits the first.

It does not yet emit the second as first-class structure.

## Can relationships become visible before lineage, movement, or transformation?

Yes, partially.

The `boundary -> unknown` candidate can become visible as a static relationship before lineage, movement, or transformation is visible.

It does not require knowing:

```text
where the unknown came from
how inquiry moved to it
whether a pressure transformed into it
whether a later investigation resolved it
```

It only requires observing:

```text
a boundary exists
an unknown remains visible
that boundary prevents filling, promotion, mutation, or classification beyond current evidence
```

This suggests artifact-to-artifact structure can emerge before inquiry movement becomes visible.

However, richer relationships such as:

```text
pressure
    -> transformed pressure

finding
    -> new question

supported conclusion
    -> next investigation
```

still require movement or lineage interpretation.

## Counterexamples

### Artifact-attached structure without artifact-to-artifact structure

The inquiry-artifacts surface exposes:

```text
artifact
    -> visibility

artifact
    -> evidence

artifact
    -> limitation
```

without exposing:

```text
finding
    -> boundary

pressure
    -> finding

gap
    -> pressure
```

This is the clearest counterexample.

### Surface evidence that is not artifact relationship

```text
pressure
    -> pressure_audit

unknown
    -> knowledge_reachability

boundary
    -> privilege_discovery
```

These are artifact-to-evidence relations, not artifact-to-artifact relations.

### Human-reconstructed chain

```text
gap
    -> pressure
    -> finding
    -> boundary
    -> unknown
```

This chain is useful, recurring, and likely meaningful.

But current repository evidence does not emit the whole chain as structure.

### Document-visible artifact relationship

```text
finding
    -> supported_conclusion

supported_conclusion
    -> open_question
```

These remain report-structure relationships.

They are not implementation-backed artifact relationships today.

## Historical perspective

Inquiry artifacts currently resemble:

```text
entities with attributes
```

more than:

```text
entities with relationships
```

Current repository-visible attributes include:

```text
visibility class
evidence
limitation
surface recurrence
```

The best relationship-like behavior is beginning to appear around:

```text
boundary
unknown
pressure
```

But this still looks like emerging relationship evidence rather than implemented relationship state.

## Supported conclusions

1. The strongest candidate artifact-to-artifact relationship is `boundary -> unknown`.
2. `boundary -> unknown` has stronger implementation-backed evidence than `gap -> pressure`, `pressure -> finding`, or `finding -> boundary`.
3. The relationship is not yet first-class repository-visible structure.
4. Artifact-attached structure is already repository-visible through visibility, evidence, and limitation attachments.
5. Artifact-to-artifact structure remains mostly human-interpreted, with `boundary -> unknown` as the best partial exception.
6. Artifact-to-artifact structure can begin to emerge before lineage, movement, or transformation become visible.
7. Inquiry artifacts currently behave more like entities with attributes than entities with relationships.
8. Pressure-to-surface is a strong movement relationship but not clearly artifact-to-artifact.

## Unsupported conclusions

- Artifact-to-artifact relationships are fully implemented today.
- `boundary -> unknown` is emitted as a first-class relationship today.
- `gap -> pressure` is implementation-backed today.
- `pressure -> finding` is implementation-backed today.
- `finding -> supported_conclusion` is implementation-backed today.
- Inquiry movement is required for all artifact-to-artifact relationship visibility.
- Lineage is visible today as implementation-backed structure.
- Prose ingestion is needed to continue this investigation path.

## Open questions

- What evidence threshold would promote `boundary -> unknown` from candidate to repository-visible relationship?
- Are limitations the bridge from artifact-attached structure to artifact-to-artifact structure?
- Can `pressure -> boundary` become visible through existing capability surfaces without prose interpretation?
- Is `surface` an inquiry artifact, an evidence source, or a non-artifact implementation endpoint?
- Can repeated co-occurrence across diagnostics distinguish relationship from shared evidence source?
- Can relationship visibility be represented without implying lineage, movement, or transformation?

## Acceptance answers

### Does any artifact-to-artifact relationship already have implementation-backed evidence?

Partially yes.

`boundary -> unknown` has the strongest implementation-backed evidence, but it is not emitted as a first-class implemented relationship.

### Which candidate relationship is strongest?

```text
boundary
    -> unknown
```

It is strongest because both endpoints are repository-visible, both recur in implemented surfaces, and boundaries often preserve unknowns without requiring full investigation-chain reconstruction.

### Can artifact-to-artifact structure emerge before inquiry movement becomes visible?

Yes.

A static relationship such as `boundary -> unknown` can become partially visible before lineage, movement, or pressure transformation are visible.

### Do inquiry artifacts currently behave more like entities-with-attributes or entities-with-relationships?

More like entities with attributes.

Repository-visible attributes include visibility, evidence, and limitation.

Relationship candidates exist, but most are not first-class repository-visible relationships.

### What is the strongest remaining boundary between artifact-attached structure and artifact-to-artifact structure?

Artifact-attached structure answers:

```text
what evidence or limitation attaches to this artifact?
```

Artifact-to-artifact structure answers:

```text
how does this artifact constrain, preserve, produce, qualify, or redirect another artifact?
```

Current repository evidence strongly supports the first and only partially supports the second.
