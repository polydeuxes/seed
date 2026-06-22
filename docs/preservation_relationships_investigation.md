# Preservation Relationships Investigation

## Purpose and boundary

This investigation asks whether preservation is already a recurring repository-visible relationship pattern.

This is investigation only.

It does not implement preservation graphs, artifact graphs, inquiry graphs, lineage, inquiry movement, pressure transformation, prose ingestion, workflow systems, or automation.

Repository authority remains implementation-backed surfaces, executable diagnostics, repository-visible documents, and recorded operator output such as `seed --inquiry-artifacts`.

## Central finding

Repository evidence supports preservation as a recurring pattern more strongly than it supports causation, transformation, production, or lineage as repository-visible relationships.

The strongest repository-visible preservation pattern remains:

```text
boundary
    -> limitation
    -> unknown remains unknown
```

This is visible in classification, mutation, read-only, capability, and visibility boundary cases.

However preservation also appears outside `boundary -> unknown`.

The broader supported shape is:

```text
surface or boundary
    declines unsupported change
    preserves visible state
```

Examples:

```text
classification boundary
    -> preserves unknown classification

mutation refusal
    -> preserves unresolved or unpromoted state

read-only behavior
    -> preserves unknown capability or unfilled state

artifact-attached limitation
    -> preserves no movement inference

artifact-attached limitation
    -> preserves no transformation inference

evidence attachment
    -> preserves support context for an artifact

visibility classification
    -> preserves artifact strength without promotion
```

Preservation appears to be one of the earliest relationship types becoming visible because it can be observed statically.

It does not require proving that one artifact caused, produced, transformed, or generated another.

## Evidence baseline

The artifact relationship investigations established:

```text
artifact visibility exists
artifact-attached structure exists
artifact-to-artifact structure remains mostly human-interpreted
```

The repository-visible attached structure includes:

```text
artifact
    -> visibility

artifact
    -> evidence

artifact
    -> limitation
```

The boundary preservation investigation refined the strongest candidate artifact relationship from:

```text
boundary
    -> unknown
```

into:

```text
boundary
    -> limitation
    -> unknown
```

with the strongest evidence in:

```text
classification boundary
    -> unknown classification remains unknown

mutation boundary
    -> unknown remains unpromoted

read-only boundary
    -> unknown remains unfilled
```

That refinement matters because preservation does not require a causal chain.

It requires visible state retained under a conservative refusal.

## Repository-visible preservation examples

### Unknown preservation

Shape:

```text
boundary
    -> preserves
    -> unknown
```

Strongest examples:

```text
classification boundary
    -> unknown classification remains unknown

mutation boundary
    -> unknown remains unpromoted

read-only boundary
    -> unknown remains unfilled
```

Evidence surfaces:

```text
classification_coverage
operational_surface_classification_audit
diagnostic_inventory
diagnostic_shape_audit
knowledge_reachability
privilege_discovery
capability_relationship
seed --inquiry-artifacts
```

Status:

```text
strongest preservation relationship candidate
not first-class implemented relationship
```

### Classification preservation

Shape:

```text
classification surface
    -> preserves classification state
```

Repository-visible examples:

```text
unknown classification remains unknown
classified entities remain classified
classification coverage reports distribution rather than repairing it
operational surface classification audit preserves unknown CLI element classification
```

Preservation meaning:

The surface reports classification state without silently promoting unknowns or changing entity type.

Status:

```text
strong implementation-backed preservation pattern
```

### Evidence preservation

Shape:

```text
artifact
    -> evidence
```

Repository-visible examples:

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
    -> reasoning_path

pressure
    -> selection_path
```

Preservation meaning:

The evidence source remains attached to the artifact so the artifact is not merely a prose label.

This preserves support context.

Status:

```text
strong artifact-attached preservation
not artifact-to-artifact preservation
```

### Limitation preservation

Shape:

```text
artifact
    -> limitation
```

Repository-visible examples:

```text
unknown
    -> no inquiry movement inference

pressure
    -> no transformation inference

boundary
    -> no unsupported promotion or mutation
```

Preservation meaning:

A limitation preserves what the repository cannot support.

It keeps the unsupported state visible rather than resolving it through inference.

Status:

```text
strong bridge from artifact-attached structure to preservation relationship
```

### Visibility preservation

Shape:

```text
visibility class
    -> preserves artifact strength
```

Repository-visible examples:

```text
unknown              repository_visible
boundary             repository_visible
pressure             partially_visible
finding              partially_visible
gap                  partially_visible
supported_conclusion document_visible
unsupported_conclusion document_visible
open_question        document_visible
```

Preservation meaning:

The visibility gradient prevents weakly visible artifacts from being promoted into repository-visible state without stronger evidence.

Status:

```text
moderate preservation pattern
important anti-overclaim boundary
```

### Diagnostic preservation

Shape:

```text
diagnostic surface
    -> inspects state
    -> preserves unresolved state
```

Repository-visible examples:

```text
diagnostic_inventory
    -> inventory remains diagnostic, not repair

diagnostic_shape_audit
    -> checks shape consistency without inventing new relationships

classification_coverage
    -> reports unknown classification without assigning non-unknown type

graph_issue_summary
    -> reports issues without resolving them by summary
```

Preservation meaning:

Diagnostics can increase visibility while preserving unresolvedness.

Status:

```text
strong operational preservation pattern
```

### Context and relationship preservation

Shape:

```text
investigation document
    -> preserves context or relationship pressure
```

Repository-visible examples:

```text
context preservation investigations
relationship preservation investigations
artifact relationship investigations
boundary preservation investigation
```

Preservation meaning:

The documents preserve distinctions, candidate relationships, counterexamples, and unsupported conclusions so later work does not have to reconstruct everything from scratch.

Status:

```text
document-visible preservation pattern
weaker than diagnostic or artifact-attached preservation
```

This matters but remains more document-backed than implementation-backed.

## Does preservation occur outside boundary -> unknown?

Yes.

Repository evidence supports preservation outside `boundary -> unknown` in at least four forms:

```text
evidence preservation
limitation preservation
classification preservation
visibility preservation
```

Document-visible evidence also supports:

```text
context preservation
relationship preservation
counterexample preservation
unsupported-conclusion preservation
open-question preservation
```

However these are not all equivalent.

Classification, diagnostic, limitation, and evidence preservation are stronger because they are tied to implemented or recorded surfaces.

Context and relationship preservation are weaker because they are mostly document-visible and depend more on human reading.

## Preservation versus transformation

### Preservation

Shape:

```text
state A remains visible as A
unsupported change is refused
supporting context is retained
```

Examples:

```text
unknown remains unknown
classification remains unknown
limitation remains explicit
evidence remains attached
visibility class remains weaker than promotion
```

Preservation is conservative.

It resists unsupported change.

### Transformation

Shape:

```text
state A becomes state B
pressure A becomes pressure B
question A becomes question B
```

Examples from pressure transformation work:

```text
pressure
    -> finding
    -> supported conclusion
    -> transformed pressure
```

Transformation is directional.

It changes the inquiry state.

### Distinction

```text
preservation
    retains state under boundary or limitation

transformation
    changes state through finding, conclusion, pressure, or reframing
```

Repository evidence supports preservation more directly because surfaces can expose retained state.

Transformation usually requires human reconstruction of movement across investigations.

## Preservation versus coexistence

### Coexistence

Shape:

```text
boundary exists
unknown exists
```

No supported claim that one preserves the other.

Counterexample:

```text
scope boundary
    coexists with unrelated unknown
```

### Preservation

Shape:

```text
boundary or limitation prevents unsupported change
unknown or unresolved state remains visible
```

Evidence threshold:

```text
1. preserved state is visible
2. conservative refusal is visible
3. the surface does not infer, mutate, promote, or repair the state
4. the state remains available for later inspection
```

This threshold separates preservation from mere coexistence.

## Preservation before causation

Repository evidence supports preservation relationships becoming visible before causal relationships.

Preservation can be static:

```text
classification remains unknown
limitation remains explicit
evidence remains attached
visibility class remains constrained
```

Causation requires stronger claims:

```text
artifact A produced artifact B
finding caused boundary
pressure caused investigation
conclusion created next pressure
```

Current repository evidence usually keeps causal relationships human-interpreted.

Therefore preservation appears earlier because it can be observed without proving production, transformation, lineage, or movement.

## Artifact-to-artifact or artifact-to-state?

Preservation appears to be both, but not equally.

### Stronger current form: artifact to state

Examples:

```text
artifact
    -> visibility state

artifact
    -> evidence state

artifact
    -> limitation state

classification boundary
    -> unknown classification state
```

This is the strongest repository-visible form.

### Weaker emerging form: artifact to artifact

Examples:

```text
boundary
    -> preserves
    -> unknown

limitation
    -> preserves
    -> unknown
```

This is the strongest candidate artifact-to-artifact form, but it is not first-class implemented relationship state.

Conclusion:

```text
preservation is currently strongest as artifact-to-state
and emerging as artifact-to-artifact
```

## Candidate preservation relationship classes

### Strongest

```text
classification preserves unknown classification
mutation refusal preserves unresolved state
read-only behavior preserves unfilled state
diagnostic inspection preserves unresolvedness
artifact limitation preserves unsupportedness
```

### Moderate

```text
visibility classification preserves artifact strength
evidence attachment preserves support context
capability boundary preserves unknown capability state
```

### Weak or document-visible

```text
context preservation
relationship preservation
counterexample preservation
open-question preservation
unsupported-conclusion preservation
```

These are important but less implementation-backed.

## Counterexamples

### Apparent preservation that is actually coexistence

```text
boundary exists
unknown exists
```

without evidence that the boundary prevents unsupported resolution.

Examples:

```text
scope boundary near unrelated unknown
format boundary near unresolved classification
rendering boundary near missing evidence
operator-interface boundary near capability unknown
```

These should not be treated as preservation relationships.

### Apparent preservation that is actually transformation

```text
pressure remains visible
but has been reframed into a new pressure
```

or:

```text
unknown appears preserved
but was converted into a new classification or unsupported-domain claim
```

or:

```text
relationship appears retained
but the later investigation changed its meaning
```

These are transformation cases, not preservation cases.

### Preservation-looking evidence attachment that is not relationship preservation

```text
artifact
    -> evidence source
```

This preserves support context.

It does not prove an artifact-to-artifact relationship.

### Limitation that does not preserve state

```text
output is capped
surface is curated
format is constrained
presentation is partial
```

These limitations may preserve caution, but they do not necessarily preserve a specific unknown or unresolved state.

## Important distinctions

### Preservation

Retention of visible state or support context under a conservative refusal to infer, mutate, promote, repair, or transform.

### Coexistence

Two things appear together without evidence that one retains or protects the other.

### Constraint

A limit on possible action or interpretation.

Constraint may support preservation but is not identical to preservation.

### Limitation

A visible statement of what cannot be inferred, mutated, observed, or claimed.

Limitation is often the bridge into preservation.

### Retention

State continues to exist.

Retention becomes preservation only when there is evidence of conservative refusal or boundary pressure.

### Transformation

State changes into another state or pressure.

Transformation is directional and usually requires movement evidence.

### Production

One artifact or process creates another.

Current repository evidence rarely supports production as first-class inquiry relationship.

### Causation

One thing causes another.

Causation requires stronger evidence than preservation and remains mostly human-interpreted in inquiry artifacts.

## Historical perspective

The repeated appearance of:

```text
context preservation
relationship preservation
unknown preservation
```

supports preservation as a recurring repository pattern.

However the strength varies by evidence class.

Strongest:

```text
unknown preservation
classification preservation
limitation preservation
diagnostic preservation
```

Moderate:

```text
evidence preservation
visibility preservation
```

Weaker:

```text
context preservation
relationship preservation
```

The current repository trajectory appears to be:

```text
visibility
    -> attachment
    -> preservation
    -> candidate relationship
```

Preservation is therefore likely one of the earliest relationship types becoming visible in inquiry artifacts, precisely because it does not require lineage or causation.

## Supported conclusions

1. Repository evidence supports preservation as a recurring pattern.
2. Preservation is strongest where visible state is retained under explicit limitation, boundary, or diagnostic refusal.
3. Preservation exists outside `boundary -> unknown`.
4. Classification preservation, diagnostic preservation, limitation preservation, evidence preservation, and visibility preservation are all supported to different degrees.
5. Preservation is different from transformation.
6. Preservation can become visible before causal or transformational relationships become visible.
7. Preservation is currently stronger as artifact-to-state than artifact-to-artifact.
8. `boundary -> limitation -> unknown` is the strongest preservation bridge toward artifact-to-artifact structure.
9. Preservation is one of the earliest relationship types becoming visible in inquiry artifacts.

## Unsupported conclusions

- Preservation is a first-class implemented relationship today.
- All preservation candidates are equivalent.
- All limitations preserve state.
- All boundaries preserve unknowns.
- Preservation is the same as coexistence.
- Preservation is the same as transformation.
- Context preservation is as implementation-backed as classification preservation.
- Relationship preservation is fully repository-visible without human interpretation.
- Causal relationships are repository-visible at the same strength as preservation relationships.

## Open questions

- What evidence threshold would make preservation first-class repository-visible structure?
- Can preservation be typed without implementing preservation graphs?
- Which limitations are preservational versus merely descriptive?
- Can relationship preservation become visible without lineage?
- Can artifact-to-state preservation be enough before artifact-to-artifact preservation exists?
- Is preservation the safest first relationship vocabulary because it avoids causation claims?

## Acceptance answers

### Does repository evidence support preservation as a recurring pattern?

Yes.

Repository evidence supports preservation as a recurring pattern, especially in classification, diagnostic, limitation, evidence, and visibility surfaces.

### Does preservation exist outside boundary -> unknown?

Yes.

Preservation also appears as evidence preservation, limitation preservation, classification preservation, diagnostic preservation, and visibility preservation.

Context and relationship preservation also recur, but remain more document-visible and less implementation-backed.

### Can preservation relationships become visible before causal or transformational relationships?

Yes.

Preservation can be observed statically as retained state under conservative refusal.

Causation and transformation require stronger movement, production, or lineage evidence.

### Is preservation fundamentally different from transformation?

Yes.

Preservation retains state or support context.

Transformation changes state, pressure, question, or framing.

### Is preservation one of the earliest relationship types becoming visible in inquiry artifacts?

Yes, partially.

Preservation appears earlier than causal or transformational relationships because it can be observed through visibility, limitation, diagnostic refusal, and retained unknown state without implementing lineage or inquiry movement.
