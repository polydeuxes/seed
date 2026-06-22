# Inquiry Artifact Relationships Investigation

## Central finding

Repository evidence supports a stronger conclusion than the original visibility-only model.

```text
artifact visibility exists

artifact-attached structure exists

artifact-to-artifact structure remains mostly human-interpreted
```

The implemented `seed --inquiry-artifacts` surface does more than classify artifacts.

It exposes repeatable relationships between:

```text
artifact
    -> visibility class

artifact
    -> evidence

artifact
    -> limitation
```

These relationships are implementation-backed and repository-visible.

## Current visibility baseline

The implementation-backed artifact visibility model is:

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

Unlike earlier interpretations, the surface also exposes supporting evidence and limitations for every artifact.

## Three levels of artifact structure

### Level 1: Artifact visibility

Repository-visible today.

```text
artifact
    -> visibility class
```

Examples:

```text
unknown
    -> repository_visible

pressure
    -> partially_visible
```

### Level 2: Artifact-attached structure

Repository-visible today.

```text
artifact
    -> evidence

artifact
    -> limitation
```

Examples:

```text
unknown
    -> diagnostic_inventory

unknown
    -> diagnostic_shape_audit

unknown
    -> knowledge_reachability

boundary
    -> capability_relationship

boundary
    -> privilege_discovery

pressure
    -> pressure_audit

pressure
    -> capability_relationship

pressure
    -> selection_path

pressure
    -> reasoning_path
```

And:

```text
pressure
    -> no transformation inference

unknown
    -> no inquiry movement inference
```

through limitations.

This is already structure.

### Level 3: Artifact-to-artifact structure

Mostly human-interpreted today.

Examples:

```text
gap
    -> pressure

pressure
    -> finding

finding
    -> boundary

boundary
    -> unknown

finding
    -> supported conclusion

supported conclusion
    -> new pressure
```

These appear repeatedly across investigations but are not repository-visible as first-class relationships.

## Implementation-backed relationships today

The strongest implementation-backed relationships are:

```text
artifact
    -> visibility class

artifact
    -> evidence

artifact
    -> limitation
```

This is stronger than a pure label model.

The inquiry-artifacts surface emits artifacts together with supporting evidence and explicit boundaries.

## Repository-visible relationships

Repository-visible relationships include:

```text
artifact
    -> visibility class

artifact
    -> evidence source

artifact
    -> limitation
```

Examples:

```text
unknown
    -> diagnostic_inventory

unknown
    -> operational_surface_classification_audit

boundary
    -> privilege_discovery

pressure
    -> pressure_audit

gap
    -> observation_domains
```

These are directly emitted by implementation-backed output.

## Human-interpreted relationships

The following remain primarily investigation-chain relationships:

```text
gap
    -> pressure

pressure
    -> finding

finding
    -> boundary

boundary
    -> unknown

finding
    -> supported conclusion

supported conclusion
    -> new pressure

open question
    -> next investigation
```

These relationships remain useful and recurrent.

However they still depend on human reconstruction.

## Do inquiry artifacts behave as labels or related units?

Repository evidence supports a layered answer.

### As labels

The surface exposes visibility classes.

### As structured units

The surface also exposes:

```text
artifact
    -> evidence

artifact
    -> limitation
```

This means artifacts already carry attached structure.

### As related units

Investigation chains continue to show:

```text
gap produces pressure

pressure produces finding

finding produces boundary

boundary preserves unknown
```

These relationships remain mostly outside repository-visible structure.

## Attachment candidates

The strongest attachment-style behavior already visible is:

```text
artifact
    -> evidence

artifact
    -> limitation
```

Examples:

```text
pressure
    attaches to
    pressure_audit evidence

boundary
    attaches to
    privilege_discovery evidence

unknown
    attaches to
    knowledge_reachability evidence
```

This is evidence for attachment-like structure.

It is not evidence for artifact-to-artifact attachment.

## Lineage candidates

Potential lineage-like behavior remains mostly human-interpreted.

Examples:

```text
pressure
    -> finding

finding
    -> supported conclusion

supported conclusion
    -> pressure
```

Repository-visible evidence remains limited.

## Structural meaning indicators

Evidence that an artifact relationship is structurally meaningful includes:

```text
repeatability
multiple investigations
multiple surfaces
stable recurrence
visibility without prose interpretation
```

Current status:

```text
artifact -> visibility      supported
artifact -> evidence        supported
artifact -> limitation      supported
artifact -> artifact        mostly human interpreted
```

## Counterexamples

### Visibility without richer structure

```text
supported_conclusion
    -> document_visible

open_question
    -> document_visible
```

Visibility classification alone does not imply structure.

### Structure without artifact-to-artifact relationships

The inquiry-artifacts surface itself.

It exposes:

```text
artifact
    -> evidence

artifact
    -> limitation
```

without exposing:

```text
finding
    -> boundary
```

or similar inquiry relationships.

### Relationships supported by prose only

```text
finding
    -> supported conclusion

supported conclusion
    -> new pressure

open question
    -> next investigation
```

remain document-visible.

## Historical perspective

The current situation resembles:

```text
artifact visibility
    -> artifact-attached structure
    -> artifact-to-artifact structure
```

more than:

```text
artifact visibility
    -> artifact relationships
```

The inquiry-artifacts surface appears to have crossed the second boundary already.

## Important distinctions

### Artifact visibility

Classification of visibility.

### Artifact-attached structure

Evidence and limitations attached directly to an artifact.

### Artifact relationship

A relationship between artifacts.

### Artifact attachment

Local attachment behavior.

### Artifact lineage

Longer inquiry evolution relationships.

### Artifact structure

The combination of repeatable visibility, evidence attachment, limitations, relationships, or lineage.

## Supported conclusions

1. Repository-visible artifact visibility exists.
2. Repository-visible artifact-attached structure exists.
3. Artifact-to-artifact structure remains mostly human-interpreted.
4. The strongest implementation-backed relationships are artifact-to-visibility, artifact-to-evidence, and artifact-to-limitation.
5. Inquiry artifacts behave as more than isolated labels.
6. The inquiry-artifacts surface already exposes attachment-like structure.
7. The strongest missing boundary is artifact-to-artifact structure rather than basic artifact structure.
8. The current situation resembles visibility, then attachment, then relationship visibility.

## Unsupported conclusions

- Artifact-to-artifact relationships are repository-visible today.
- Attachment between artifacts is implementation-backed today.
- Lineage is implementation-backed today.
- Inquiry graphs should be implemented.
- Linguistic branching is more than an analogy.
- The identified relationship hierarchy is canonical.

## Open questions

- Which artifact-to-artifact relationship can become repository-visible first?
- Is artifact-to-evidence the foundational attachment relationship?
- Can partially visible artifacts gain attachment structure before relationship structure?
- What distinguishes stable attachment from repeated association?
- Can lineage become visible without movement visibility?

## Acceptance answers

### Do repository-visible artifact relationships already exist?

Yes. Artifact-to-visibility, artifact-to-evidence, and artifact-to-limitation relationships are implementation-backed and repository-visible.

### Which artifact relationships are implementation-backed?

Artifact-to-visibility, artifact-to-evidence, and artifact-to-limitation are the strongest implementation-backed relationships.

### Which relationships remain human interpreted?

Gap-to-pressure, pressure-to-finding, finding-to-boundary, boundary-to-unknown, finding-to-supported-conclusion, supported-conclusion-to-new-pressure, and open-question-to-next-investigation.

### Do inquiry artifacts behave more like isolated labels or related units?

More like structured units with attached evidence and limitations, though most artifact-to-artifact relationships remain human interpreted.

### Does repository evidence support moving from artifact visibility toward artifact structure?

Yes. The inquiry-artifacts surface already demonstrates artifact-attached structure and suggests a progression toward richer artifact structure.